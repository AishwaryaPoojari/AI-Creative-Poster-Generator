# ACADEMIC PROJECT REPORT

## Course: Generative Artificial Intelligence
### Module 3: AI-Generated Art and Creativity
**Project Title:** ArtGen Studio: Generative AI & Creative Poster Suite using DeepDream and Neural Style Transfer  
**Frameworks:** PyTorch, Torchvision, Streamlit, Pillow  

---

## 1. Executive Summary & Objective

The objective of this project is to explore the intersection of artificial intelligence and human creativity by developing an end-to-end generative design system. Built upon **PyTorch**, the application investigates how deep convolutional neural networks (CNNs) can be utilized not merely as passive classifiers, but as active generative engines capable of:
1. Translating natural language creative concepts into visual poster art.
2. Transferring classical artistic painting styles (Van Gogh, Picasso, Cyberpunk) onto real-world images using **Neural Style Transfer (NST)**.
3. Synthesizing hallucinatory, surreal textures and fractal forms through **Google DeepDream** gradient ascent.
4. Implementing automated graphic design and typography composition to overcome the known spelling and layout limitations of pure image diffusion models.

---

## 2. Theoretical Foundation & Mathematical Formulation

### 2.1 Neural Style Transfer (Gatys et al., 2015)

Neural Style Transfer separates and recombines image content and style using representations learned by deep convolutional networks (specifically **VGG19** pre-trained on ImageNet).

#### 2.1.1 Content Representation and Loss
Let $\vec{p}$ be the original content image and $\vec{x}$ be the generated image. Let $F^l \in \mathbb{R}^{N_l \times M_l}$ be the feature representation of $\vec{x}$ at layer $l$, where $N_l$ is the number of feature maps and $M_l$ is the spatial height $\times$ width. Similarly, let $P^l$ be the feature representation of $\vec{p}$.

The **Content Loss** measures feature divergence at a deep convolutional layer (`conv4_2`):
$$\mathcal{L}_{\text{content}}(\vec{p}, \vec{x}, l) = \frac{1}{2} \sum_{i=1}^{N_l} \sum_{j=1}^{M_l} \left( F_{ij}^l - P_{ij}^l \right)^2$$

#### 2.1.2 Style Representation and Gram Matrix
Artistic style is independent of spatial scene arrangement. It is captured by the correlations between different filter responses across the entire feature map. The **Gram Matrix** $G^l \in \mathbb{R}^{N_l \times N_l}$ is defined as the inner product of vectorized feature maps:
$$G_{ij}^l = \sum_{k=1}^{M_l} F_{ik}^l F_{jk}^l$$

Let $\vec{a}$ be the style image with Gram representation $A^l$. The **Style Loss** across multiple layers ($l \in \{\text{conv1\_1, conv2\_1, conv3\_1, conv4\_1, conv5\_1}\}$) is:
$$\mathcal{L}_{\text{style}}(\vec{a}, \vec{x}) = \sum_{l} w_l \cdot \frac{1}{4 N_l^2 M_l^2} \sum_{i=1}^{N_l} \sum_{j=1}^{N_l} \left( G_{ij}^l - A_{ij}^l \right)^2$$
where $w_l$ is the weighting factor for layer $l$.

#### 2.1.3 Total Objective Function
The synthesized image $\vec{x}^*$ minimizes the weighted sum:
$$\mathcal{L}_{\text{total}}(\vec{p}, \vec{a}, \vec{x}) = \alpha \mathcal{L}_{\text{content}}(\vec{p}, \vec{x}) + \beta \mathcal{L}_{\text{style}}(\vec{a}, \vec{x})$$
Optimization is performed directly on the image pixel tensor using the **L-BFGS** optimizer.

---

### 2.2 DeepDream: Activation Maximization via Gradient Ascent

DeepDream inverts the traditional CNN training objective. During training, network weights $\theta$ are updated via gradient descent to minimize cross-entropy loss:
$$\theta \leftarrow \theta - \eta \nabla_{\theta} \mathcal{L}_{\text{task}}$$

In **DeepDream**, network weights $\theta$ are frozen. Instead, gradient ascent is applied to the **input image pixels $I$** to maximize the activation $a^l(I)$ of a chosen layer:
$$I \leftarrow I + \eta \cdot \frac{\partial \|a^l(I)\|^2}{\partial I}$$

#### Octave Pyramid Processing
To produce scale-invariant, fractal patterns without pixel grid artifacts:
1. An octave pyramid downsamples the input image into multiple spatial scales.
2. Gradient ascent is performed iteratively from the coarsest octave to the finest octave.
3. Spatial jitter (random 2D roll) is applied before forward passes and subtracted before backpropagation to smooth high-frequency noise.

---

## 3. System Architecture & Methodology

```
+-------------------------------------------------------------------------+
|                              USER INTERFACE                             |
|       (Interactive Streamlit Web App: Form Inputs, Sliders, Previews)   |
+------------------------------------+------------------------------------+
                                     |
         +---------------------------+---------------------------+
         |                                                       |
         v                                                       v
+------------------------------------+  +------------------------------------+
|     MODE 1: POSTER GENERATOR       |  |      MODE 2: NST & DEEPDREAM       |
|  - Structured Prompt Construction  |  |  - Pre-trained VGG16/VGG19 Feature |
|  - Generative Art Canvas Synth     |  |    Extraction                      |
|  - Creativity Scaling (Bal/Surr)   |  |  - Gram Matrix Style Blending      |
|  - Pillow Typography & Layout      |  |  - Layer Activation Maximization   |
+-----------------+------------------+  +-----------------+------------------+
                  |                                        |
                  +-------------------+--------------------+
                                      |
                                      v
+-------------------------------------------------------------------------+
|                             EXPORT ENGINE                               |
|        High-Resolution PNG Render | Downloadable Masterpiece Artwork    |
+-------------------------------------------------------------------------+
```

---

## 4. Key Experimental Features & Innovation

1. **Lightweight Execution on Laptop Hardware:**
   By utilizing pre-trained feature extraction backbones with optimized intermediate resolution (256–384px), the system completes stylization and poster generation in seconds without requiring multi-gigabyte GPU downloads.
2. **Dual-Style Blending:**
   Allows interpolating the Gram matrices of two distinct artists (e.g., $G_{\text{blend}} = (1-\lambda)G_{\text{VanGogh}} + \lambda G_{\text{Cyberpunk}}$), producing entirely new hybrid art forms.
3. **Color-Preserving Style Transfer:**
   Separates luminance ($Y$) from chrominance ($Cb, Cr$) channels to transfer painterly brushwork while retaining the original photograph's natural colors.
4. **Hybrid Typography Engine:**
   Combines generative visual imagination with deterministic PIL typography layout to guarantee that event titles, dates, and venues are 100% legibly spelled.

---

## 5. Conclusion & Learning Outcomes

This project successfully implements the concepts required for **Module 3: AI-Generated Art and Creativity**:
- Implemented deep generative modeling principles in PyTorch.
- Analyzed the mathematical distinction between spatial content and second-order statistical style correlations.
- Explored layer-wise feature visualization via DeepDream.
- Delivered an intuitive, interactive software application enabling non-technical users to collaborate creatively with artificial intelligence.
