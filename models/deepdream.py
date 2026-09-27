"""
DeepDream Generator using PyTorch
---------------------------------
Implements Google DeepDream via gradient ascent on CNN feature maps.
Allows selecting specific layers to visualize texture vs. semantic hallucinations.
Optimized for fast CPU/GPU execution using octave pyramids.
"""

import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image, ImageFilter
import numpy as np


class DeepDreamModel:
    def __init__(self, device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        # Load pre-trained VGG16 (features only, very lightweight ~50MB)
        vgg = models.vgg16(weights=models.VGG16_Weights.DEFAULT)
        self.features = vgg.features.to(self.device).eval()
        for param in self.features.parameters():
            param.requires_grad = False

        # Map user-friendly names to VGG16 layer indices
        # VGG16 conv layers: 0, 2, 5, 7, 10, 12, 14, 17, 19, 21, 24, 26, 28
        self.available_layers = {
            "Layer 4 (Textures & Brushstrokes)": 4,
            "Layer 9 (Patterns & Swirls)": 9,
            "Layer 16 (Complex Geometries)": 16,
            "Layer 23 (Hallucinatory Shapes)": 23,
            "Layer 28 (Deep Surreal Dreams)": 28,
        }

        self.mean = torch.tensor([0.485, 0.456, 0.406], device=self.device).view(1, 3, 1, 1)
        self.std = torch.tensor([0.229, 0.224, 0.225], device=self.device).view(1, 3, 1, 1)

    def _preprocess(self, pil_img):
        """Convert PIL Image to normalized PyTorch tensor."""
        if pil_img.mode != "RGB":
            pil_img = pil_img.convert("RGB")
        tensor = transforms.ToTensor()(pil_img).unsqueeze(0).to(self.device)
        return (tensor - self.mean) / self.std

    def _deprocess(self, tensor):
        """Convert PyTorch tensor back to PIL Image."""
        t = tensor.detach().clone() * self.std + self.mean
        t = torch.clamp(t, 0.0, 1.0)
        t = t.squeeze(0).cpu().permute(1, 2, 0).numpy()
        t = (t * 255).astype(np.uint8)
        return Image.fromarray(t)

    def _dream_step(self, image_tensor, target_layer_idx, step_size=0.03):
        """Performs one gradient ascent step to maximize activations at target_layer_idx."""
        img_var = image_tensor.detach().clone()
        img_var.requires_grad_(True)

        # Jitter to avoid pixel grid artifacts
        ox, oy = int(np.random.randint(-4, 5)), int(np.random.randint(-4, 5))
        jittered = torch.roll(torch.roll(img_var, shifts=ox, dims=-1), shifts=oy, dims=-2)

        x = jittered
        for idx, layer in enumerate(self.features):
            x = layer(x)
            if idx == target_layer_idx:
                break

        # Loss is the mean activation square (energy) of the chosen layer
        loss = x.norm()

        # Compute gradient directly via autograd to avoid non-leaf .grad is None errors
        grads = torch.autograd.grad(loss, img_var, retain_graph=False)[0]

        # Un-jitter gradients
        grad = torch.roll(torch.roll(grads, shifts=-ox, dims=-1), shifts=-oy, dims=-2)

        # Normalize gradient to prevent exploding values
        grad_std = grad.std()
        if grad_std > 1e-7:
            grad = grad / grad_std

        # Gradient ascent step
        with torch.no_grad():
            output_tensor = image_tensor.detach().clone() + step_size * grad

        return output_tensor

    def dream(
        self,
        pil_image,
        layer_name="Layer 16 (Complex Geometries)",
        octaves=3,
        octave_scale=1.4,
        iterations_per_octave=12,
        step_size=0.03,
        progress_callback=None,
    ):
        """
        Runs multi-octave DeepDream on the input PIL image.
        Yields intermediate PIL images if progress_callback is set.
        """
        layer_idx = self.available_layers.get(layer_name, 16)
        if pil_image.mode != "RGB":
            pil_image = pil_image.convert("RGB")
        orig_w, orig_h = pil_image.size

        # Build octave pyramid (from small to large)
        octave_images = [pil_image]
        for _ in range(octaves - 1):
            w = int(octave_images[-1].width / octave_scale)
            h = int(octave_images[-1].height / octave_scale)
            downsampled = octave_images[-1].resize((max(w, 64), max(h, 64)), Image.Resampling.BILINEAR)
            octave_images.append(downsampled)

        octave_images.reverse()  # Start from smallest octave

        dream_tensor = None
        total_steps = octaves * iterations_per_octave
        current_step = 0

        for oct_idx, base_img in enumerate(octave_images):
            target_size = base_img.size
            base_tensor = self._preprocess(base_img)

            if dream_tensor is None:
                dream_tensor = base_tensor.clone()
            else:
                # Upsample previous dream to current octave resolution
                dream_tensor = torch.nn.functional.interpolate(
                    dream_tensor,
                    size=(target_size[1], target_size[0]),
                    mode="bilinear",
                    align_corners=False,
                )

            # Gradient ascent iterations for this octave
            for i in range(iterations_per_octave):
                dream_tensor = self._dream_step(dream_tensor, layer_idx, step_size=step_size)
                current_step += 1

                if progress_callback:
                    progress_pct = current_step / total_steps
                    preview_img = self._deprocess(dream_tensor)
                    progress_callback(progress_pct, preview_img, f"Octave {oct_idx+1}/{octaves} - Step {i+1}/{iterations_per_octave}")

        final_img = self._deprocess(dream_tensor)
        if final_img.size != (orig_w, orig_h):
            final_img = final_img.resize((orig_w, orig_h), Image.Resampling.LANCZOS)
        return final_img
