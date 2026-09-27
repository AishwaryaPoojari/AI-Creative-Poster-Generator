"""
Neural Style Transfer (Gatys et al.) using PyTorch
---------------------------------------------------
Implements Neural Style Transfer using pre-trained VGG19.
Includes:
- Content Loss (Mean Squared Error on deep feature maps)
- Style Loss (Gram Matrix correlation across multi-scale layers)
- Dual-Style Interpolation (blend two distinct artistic styles)
- Color Preservation (transfers texture while retaining original content colors)
- Fast execution option for real-time classroom demos
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image
import numpy as np


class ContentLoss(nn.Module):
    def __init__(self, target):
        super(ContentLoss, self).__init__()
        # Detach target to avoid computing gradients for the target content representation
        self.target = target.detach()
        self.loss = 0.0

    def forward(self, input):
        self.loss = F.mse_loss(input, self.target)
        return input


def gram_matrix(input_tensor):
    """Computes normalized Gram Matrix representing style correlations."""
    b, c, h, w = input_tensor.size()
    features = input_tensor.view(b * c, h * w)
    G = torch.mm(features, features.t())
    # Normalize by number of elements to prevent layer scale dominance
    return G.div(b * c * h * w)


class StyleLoss(nn.Module):
    def __init__(self, target_feature):
        super(StyleLoss, self).__init__()
        self.target = gram_matrix(target_feature).detach()
        self.loss = 0.0

    def forward(self, input):
        G = gram_matrix(input)
        self.loss = F.mse_loss(G, self.target)
        return input


class Normalization(nn.Module):
    def __init__(self, mean, std):
        super(Normalization, self).__init__()
        self.mean = mean.clone().detach().view(-1, 1, 1)
        self.std = std.clone().detach().view(-1, 1, 1)

    def forward(self, img):
        return (img - self.mean) / self.std


class StyleTransferModel:
    def __init__(self, device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        vgg = models.vgg19(weights=models.VGG19_Weights.DEFAULT).features.to(self.device).eval()
        for param in vgg.parameters():
            param.requires_grad = False
        self.vgg = vgg

        self.cnn_normalization_mean = torch.tensor([0.485, 0.456, 0.406], device=self.device)
        self.cnn_normalization_std = torch.tensor([0.229, 0.224, 0.225], device=self.device)

    def _preprocess(self, pil_img, target_size=(384, 384)):
        """Resizes and converts PIL image to normalized tensor."""
        if pil_img.mode != "RGB":
            pil_img = pil_img.convert("RGB")
        loader = transforms.Compose([
            transforms.Resize(target_size),
            transforms.ToTensor(),
        ])
        return loader(pil_img).unsqueeze(0).to(self.device, torch.float)

    def _deprocess(self, tensor):
        """Converts PyTorch tensor back to PIL Image."""
        t = tensor.detach().clone().squeeze(0).cpu()
        t = torch.clamp(t, 0.0, 1.0)
        t = transforms.ToPILImage()(t)
        return t

    def _build_model_and_losses(
        self,
        content_img,
        style_img1,
        style_img2=None,
        style_blend_ratio=0.5,
        content_layers=("conv_4",),
        style_layers=("conv_1", "conv_2", "conv_3", "conv_4", "conv_5"),
    ):
        """Builds sequential pipeline inserting ContentLoss and StyleLoss layers."""
        norm = Normalization(self.cnn_normalization_mean, self.cnn_normalization_std).to(self.device)

        content_losses = []
        style_losses = []

        model = nn.Sequential(norm)

        i = 0
        block = 1
        for layer in self.vgg.children():
            if isinstance(layer, nn.Conv2d):
                i += 1
                name = f"conv_{block}"
            elif isinstance(layer, nn.ReLU):
                name = f"relu_{block}_{i}"
                layer = nn.ReLU(inplace=False)
            elif isinstance(layer, nn.MaxPool2d):
                name = f"pool_{block}"
                block += 1
                i = 0
            elif isinstance(layer, nn.BatchNorm2d):
                name = f"bn_{block}_{i}"
            else:
                raise RuntimeError(f"Unrecognized layer: {layer.__class__.__name__}")

            model.add_module(name, layer)

            if name in content_layers:
                target = model(content_img).detach()
                c_loss = ContentLoss(target)
                model.add_module(f"content_loss_{name}", c_loss)
                content_losses.append(c_loss)

            if name in style_layers:
                target_s1 = model(style_img1).detach()
                if style_img2 is not None:
                    target_s2 = model(style_img2).detach()
                    # Interpolate gram matrices between two styles
                    gram1 = gram_matrix(target_s1)
                    gram2 = gram_matrix(target_s2)
                    blended_gram = (1.0 - style_blend_ratio) * gram1 + style_blend_ratio * gram2
                    s_loss = StyleLoss(target_s1)
                    s_loss.target = blended_gram
                else:
                    s_loss = StyleLoss(target_s1)
                model.add_module(f"style_loss_{name}", s_loss)
                style_losses.append(s_loss)

        # Trim unnecessary layers after the last content or style loss
        for i in range(len(model) - 1, -1, -1):
            if isinstance(model[i], (ContentLoss, StyleLoss)):
                break
        model = model[: i + 1]

        return model, style_losses, content_losses

    def transfer_style(
        self,
        content_pil,
        style_pil_1,
        style_pil_2=None,
        style_blend_ratio=0.5,
        steps=150,
        style_weight=1000000.0,
        content_weight=1.0,
        image_size=384,
        preserve_color=False,
        progress_callback=None,
    ):
        """
        Executes Gatys Neural Style Transfer.
        Returns the stylized PIL Image.
        """
        orig_w, orig_h = content_pil.size
        # Sizing: maintain aspect ratio or square
        target_size = (image_size, image_size)

        content_tensor = self._preprocess(content_pil, target_size)
        style_tensor1 = self._preprocess(style_pil_1, target_size)
        style_tensor2 = self._preprocess(style_pil_2, target_size) if style_pil_2 is not None else None

        # Optimization begins from content image (faster convergence and structure preservation)
        input_tensor = content_tensor.clone()
        input_tensor.requires_grad_(True)

        model, style_losses, content_losses = self._build_model_and_losses(
            content_tensor,
            style_tensor1,
            style_tensor2,
            style_blend_ratio,
        )

        optimizer = torch.optim.LBFGS([input_tensor], lr=1.0)
        run = [0]

        while run[0] <= steps:
            def closure():
                with torch.no_grad():
                    input_tensor.clamp_(0, 1)

                optimizer.zero_grad()
                model(input_tensor)
                style_score = 0.0
                content_score = 0.0

                for sl in style_losses:
                    style_score += sl.loss
                for cl in content_losses:
                    content_score += cl.loss

                style_score *= style_weight
                content_score *= content_weight

                loss = style_score + content_score
                loss.backward()

                run[0] += 1
                if run[0] % 15 == 0 or run[0] == steps:
                    if progress_callback:
                        progress_pct = min(run[0] / steps, 1.0)
                        current_preview = self._deprocess(input_tensor)
                        status_str = f"Step {run[0]}/{steps} | Style Loss: {style_score.item():.2f} | Content Loss: {content_score.item():.2f}"
                        progress_callback(progress_pct, current_preview, status_str)

                return loss

            optimizer.step(closure)

        with torch.no_grad():
            input_tensor.clamp_(0, 1)
        final_image = self._deprocess(input_tensor)

        # Color preservation mode (transfer style texture onto original luminance)
        if preserve_color:
            final_image = self._preserve_color_ycbcr(content_pil.resize(target_size), final_image)

        # Resize back to original aspect ratio
        final_image = final_image.resize((orig_w, orig_h), Image.Resampling.LANCZOS)
        return final_image

    @staticmethod
    def _preserve_color_ycbcr(content_img, stylized_img):
        """Preserves original content color by replacing Y (luminance) channel only."""
        content_ycbcr = content_img.convert("YCbCr")
        stylized_ycbcr = stylized_img.convert("YCbCr")

        _, cb, cr = content_ycbcr.split()
        y, _, _ = stylized_ycbcr.split()

        preserved = Image.merge("YCbCr", (y, cb, cr)).convert("RGB")
        return preserved
