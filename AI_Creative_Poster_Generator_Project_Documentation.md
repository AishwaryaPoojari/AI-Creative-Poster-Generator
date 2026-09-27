# AI Creative Poster Generator Using Generative AI

## 1. Project Overview

### Project Title
**AI Creative Poster Generator Using Generative AI**

### Project Category
**Image Generation using Generative AI**

### Purpose

The project is a web-based AI application that converts a user's creative idea into an original poster artwork.

The system does **not** depend on fixed poster templates. Instead, the user provides information such as poster type, title, description, theme, mood, color preference, and artistic style. A pretrained generative AI model creates the visual artwork, and the application then places the user's exact textual information on the generated artwork.

The project demonstrates the intersection of:

- Generative AI
- AI-generated art
- Neural style transfer
- Image manipulation
- Computer vision
- PyTorch/TensorFlow concepts
- Human creativity and AI-assisted creativity

---

# 2. Problem Statement

Designing an attractive poster normally requires graphic-design skills, knowledge of layouts, suitable images, typography, and image-editing software.

The proposed system simplifies this process by allowing a user to describe the desired poster in natural language and select creative parameters. Generative AI then creates original visual artwork based on those inputs.

The objective is not to replace the user's creative decision-making, but to use AI to transform the user's idea into a visual design.

---

# 3. Objectives

The project must:

1. Allow users to enter a creative poster idea.
2. Allow users to select a poster category.
3. Allow users to select an artistic style.
4. Allow users to select mood and color preferences.
5. Generate original visual artwork using a pretrained generative AI model.
6. Demonstrate image manipulation/style transfer.
7. Add exact user-provided text separately so that important information is readable and correctly spelled.
8. Allow the user to preview the generated poster.
9. Allow the user to regenerate another variation.
10. Allow the final poster to be downloaded as an image.
11. Demonstrate practical use of PyTorch or TensorFlow.
12. Keep the implementation feasible for a student project without training a large generative model from scratch.

---

# 4. Alignment With Module 3 Requirements

The module is about **AI-Generated Art and Creativity** and encourages experimentation with generative models, style transfer, and image manipulation.

The project satisfies these concepts as follows:

| Module Concept | Project Implementation |
|---|---|
| AI-generated art | AI generates the poster artwork |
| Generative models | A pretrained text-to-image model is used |
| Creativity | User controls theme, mood, style, colors, and description |
| Style transfer | Optional artistic style transfer is applied to generated/selected artwork |
| Image manipulation | Resize, crop, blend, overlay, and composition operations are performed |
| TensorFlow/PyTorch | PyTorch is the recommended implementation framework |
| Image-generation category | The final output is an AI-generated visual poster |

**Important:** The project should clearly contain an AI-generated image component. A normal template editor alone does not satisfy the objective.

---

# 5. Core Project Idea

The central pipeline is:

```text
USER CREATIVE IDEA
        |
        v
POSTER INPUT FORM
        |
        v
PROMPT BUILDER
        |
        v
GENERATIVE AI MODEL
        |
        v
AI-GENERATED ARTWORK
        |
        +----------------------+
        |                      |
        v                      v
STYLE TRANSFER           IMAGE MANIPULATION
(optional)               / COMPOSITION
        |                      |
        +----------+-----------+
                   |
                   v
           POSTER COMPOSER
                   |
                   v
        EXACT USER TEXT OVERLAY
                   |
                   v
          FINAL POSTER IMAGE
```

---

# 6. User Inputs

The application should provide the following input fields.

## Required Inputs

### 6.1 Poster Type

Dropdown:

- Event Poster
- Movie Poster
- Book Cover
- Album Cover
- Invitation
- Advertisement
- Social Media Post
- Festival Poster
- Awareness Poster
- Custom Poster

### 6.2 Title

Example:

```text
TECHFEST 2026
```

### 6.3 Description

Example:

```text
A college technology festival featuring AI, robotics, coding competitions,
workshops, and innovation.
```

### 6.4 Theme

Examples:

- Technology
- Nature
- Fantasy
- Education
- Business
- Space
- Sports
- Music
- Celebration
- Environment
- Custom

### 6.5 Mood

Examples:

- Energetic
- Calm
- Mysterious
- Professional
- Joyful
- Dramatic
- Futuristic
- Inspirational
- Dark
- Dreamy

### 6.6 Artistic Style

Examples:

- Digital Art
- Watercolor
- Oil Painting
- Minimalist
- Vintage
- Cyberpunk
- Fantasy
- Cinematic
- Abstract
- Pencil Art

### 6.7 Color Preference

Examples:

- Blue
- Purple
- Red
- Green
- Orange
- Black and White
- Pastel
- Custom

### 6.8 Creativity Level

Options:

- Balanced
- Artistic
- Experimental
- Surreal

### 6.9 Optional Details

Depending on poster type:

- Date
- Time
- Venue
- Organizer
- Website
- Contact
- Call to action

These details must be added using normal image/text composition rather than relying on the image-generation model to spell them correctly.

---

# 7. Example Input and Output

## Example A — College Technology Festival

### Input

```text
Poster Type: Event Poster
Title: TECHFEST 2026
Description: A technology festival with AI, robotics, coding and innovation.
Theme: Technology
Mood: Energetic
Style: Futuristic / Cyberpunk
Colors: Blue + Purple
Creativity: Experimental
```

### AI Processing

The prompt builder converts these values into a structured generation prompt.

### Output

A futuristic technology festival artwork containing elements such as:

- futuristic city
- glowing technology
- robotics
- digital patterns
- energetic lighting

The exact title, date, venue, and event details are then placed on top by the poster compositor.

---

# 8. AI Architecture

## 8.1 Recommended Architecture

```text
                    USER
                     |
                     v
             FRONTEND UI
                     |
                     v
             BACKEND API
                     |
          +----------+----------+
          |                     |
          v                     v
    INPUT VALIDATOR        PROMPT BUILDER
                                |
                                v
                       GENERATIVE MODEL
                                |
                                v
                       GENERATED IMAGE
                                |
                 +--------------+--------------+
                 |                             |
                 v                             v
          STYLE TRANSFER                 IMAGE PROCESSOR
          (optional)                     (Pillow/OpenCV)
                 |                             |
                 +--------------+--------------+
                                |
                                v
                         POSTER COMPOSER
                                |
                                v
                           FINAL PNG
```

---

# 9. Recommended Technology Stack

## Frontend

Recommended:

- HTML
- CSS
- JavaScript

Optional:

- React

For a student project, plain HTML/CSS/JavaScript is sufficient and easier to maintain.

## Backend

Recommended:

- Python
- FastAPI or Flask

FastAPI is preferred for a clean API structure.

## AI / Deep Learning

Recommended:

- PyTorch
- Hugging Face Diffusers
- Transformers where required
- Torchvision
- OpenCV
- Pillow

## Database

A database is optional.

If history is required:

- SQLite

The first version can work without a database.

## Output

- PNG
- JPEG

PNG is recommended for the final poster.

---

# 10. Recommended AI Approach

## Important Design Decision

Do **not** train a large generative model from scratch.

Training a modern image-generation model from scratch requires substantial GPU resources and datasets.

Instead, use a **pretrained model** and demonstrate how generative AI can be used creatively.

### Recommended primary approach

Use a pretrained text-to-image diffusion model through:

```text
PyTorch + Hugging Face Diffusers
```

Possible model families:

- Stable Diffusion
- Stable Diffusion XL, if hardware allows
- Another compatible pretrained diffusion model available through Hugging Face

The exact model can be changed without changing the application architecture.

---

# 11. Style Transfer Component

To explicitly demonstrate the module's style-transfer concept, provide an optional style-transfer mode.

## Recommended approach

Use:

- PyTorch
- pretrained VGG19
- neural style transfer

### Input

```text
Content Image
+
Style Image
```

### Process

1. Load content image.
2. Load style image.
3. Extract feature representations using pretrained VGG19.
4. Calculate content loss.
5. Calculate style loss using Gram matrices.
6. Optimize an output image.
7. Return the stylized image.

### Output

A new artwork that preserves the content structure while adopting visual characteristics of the selected style.

---

# 12. Two AI Modes

The application can expose two modes.

## Mode 1 — AI Poster Generation

```text
Text Input
   |
   v
Prompt Builder
   |
   v
Text-to-Image Model
   |
   v
Generated Artwork
   |
   v
Poster Composition
```

## Mode 2 — AI Style Transfer

```text
Content Image + Style Image
          |
          v
     VGG19 Features
          |
          v
   Style Optimization
          |
          v
   Stylized Artwork
          |
          v
    Poster Composition
```

This gives the project a strong connection to both **generative AI** and **style transfer**.

---

# 13. Prompt Construction

The application should not simply send the user's raw description to the model.

Create a structured prompt.

## Prompt Template

```text
Create an original {poster_type} artwork.

Main concept:
{description}

Theme:
{theme}

Mood:
{mood}

Artistic style:
{style}

Color palette:
{colors}

Composition:
Create a visually balanced poster-oriented composition with a clear
central visual subject, suitable negative space for title and information,
strong depth, attractive lighting, and professional visual hierarchy.

Creativity level:
{creativity}

The image should be original, visually expressive, high quality,
and suitable as a poster background.

Do not render important event details or long text inside the artwork.
Leave suitable space for the application to add exact text later.
```

The system can append category-specific instructions.

For example, a movie poster can include:

```text
cinematic composition, dramatic lighting, strong focal subject,
professional movie-poster atmosphere
```

A festival poster can include:

```text
dynamic composition, energetic lighting, modern event atmosphere,
technology-inspired visual elements
```

---

# 14. Negative Prompt

If the selected model supports negative prompts, use:

```text
blurry, low quality, distorted objects, malformed objects,
duplicate subjects, watermark, logo, unreadable text,
random letters, excessive text, cropped main subject
```

The exact negative prompt can be adjusted according to the model.

---

# 15. Poster Composition

The generated image should be treated as the **artwork/background**, not as the complete final poster.

Use Pillow or OpenCV to compose the final design.

## Composition Steps

1. Generate artwork.
2. Resize artwork to the selected output size.
3. Crop while maintaining important content.
4. Add optional dark/light gradient overlays.
5. Add title.
6. Add subtitle.
7. Add date/time.
8. Add venue.
9. Add organizer information.
10. Add decorative shapes if required.
11. Add optional logo supplied by the user.
12. Export the final image.

---

# 16. Text Rendering

Do not depend on the generative model to produce exact poster text.

Use Pillow's `ImageDraw` and `ImageFont`, or another controlled text-rendering library.

This guarantees:

- correct spelling
- correct dates
- correct times
- readable text
- predictable placement

Example:

```text
AI-generated background
        +
Exact application-rendered title
        +
Exact event information
        =
Final poster
```

---

# 17. Suggested Poster Layout

A simple layout can be:

```text
+--------------------------------------+
|              SMALL LABEL             |
|                                      |
|          MAIN POSTER TITLE           |
|                                      |
|                                      |
|          AI GENERATED ART            |
|                                      |
|                                      |
|       SHORT DESCRIPTION              |
|                                      |
|  DATE        TIME        VENUE       |
|                                      |
|            ORGANIZER                 |
+--------------------------------------+
```

The actual layout should adapt according to the poster type.

---

# 18. Main Application Screens

## Screen 1 — Home

Display:

```text
AI CREATIVE STUDIO

Turn your idea into an original AI-generated design.

[Create Poster]
```

---

## Screen 2 — Create

Show:

```text
Poster Type
Title
Description
Theme
Mood
Art Style
Colors
Creativity Level
Date
Time
Venue
```

Button:

```text
GENERATE ARTWORK
```

---

## Screen 3 — Generation

Show:

```text
Creating your artwork...

Generating visual concept
Applying selected style
Preparing composition
```

A progress indicator can be displayed.

---

## Screen 4 — Preview

Display:

```text
GENERATED POSTER
```

Buttons:

```text
Regenerate
Change Style
Edit Text
Download
Start New
```

---

# 19. Regeneration Feature

The user should be able to generate another variation using the same inputs.

Example:

```text
Generation 1
Generation 2
Generation 3
```

The system should vary the random seed when supported.

This demonstrates that generative AI can produce different outputs from the same creative concept.

---

# 20. Creativity Experiment

This is an important feature for demonstrating the **creativity** component of the assignment.

Allow the user to change:

```text
Creativity:
Balanced
Artistic
Experimental
Surreal
```

Then compare the outputs.

### Example

Same input:

```text
Theme: Space
Mood: Mysterious
```

Balanced:

```text
realistic space environment
```

Experimental:

```text
surreal cosmic architecture
```

Surreal:

```text
impossible floating planets and dream-like structures
```

This provides an excellent demonstration during evaluation.

---

# 21. Style Experiment

Another useful demonstration:

Keep the same input and change only the style.

```text
Same idea
    |
    +--> Watercolor
    |
    +--> Cyberpunk
    |
    +--> Vintage
    |
    +--> Oil Painting
    |
    +--> Digital Art
```

The application generates visually different results.

This directly demonstrates **style manipulation**.

---

# 22. Suggested API Endpoints

## Generate Poster

```http
POST /api/poster/generate
```

Request:

```json
{
  "poster_type": "event",
  "title": "TECHFEST 2026",
  "description": "Technology festival with AI and robotics",
  "theme": "technology",
  "mood": "energetic",
  "style": "cyberpunk",
  "colors": ["blue", "purple"],
  "creativity": "experimental",
  "date": "15 April 2026",
  "time": "10:00 AM",
  "venue": "Main Auditorium"
}
```

Response:

```json
{
  "success": true,
  "image_url": "/outputs/poster_001.png"
}
```

---

## Generate Artwork Only

```http
POST /api/art/generate
```

Response:

```json
{
  "success": true,
  "image_url": "/outputs/art_001.png"
}
```

---

## Style Transfer

```http
POST /api/style-transfer
```

Input:

```text
content_image
style_image
style_strength
```

Response:

```json
{
  "success": true,
  "image_url": "/outputs/stylized_001.png"
}
```

---

# 23. Suggested Project Folder Structure

```text
ai-creative-poster-generator/
│
├── backend/
│   ├── main.py
│   ├── config.py
│   │
│   ├── api/
│   │   ├── poster_routes.py
│   │   ├── generation_routes.py
│   │   └── style_routes.py
│   │
│   ├── services/
│   │   ├── prompt_builder.py
│   │   ├── image_generator.py
│   │   ├── style_transfer.py
│   │   ├── poster_composer.py
│   │   └── image_utils.py
│   │
│   ├── models/
│   │   └── model_loader.py
│   │
│   └── outputs/
│
├── frontend/
│   ├── index.html
│   ├── create.html
│   ├── preview.html
│   │
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       ├── app.js
│       ├── form.js
│       └── preview.js
│
├── assets/
│   ├── styles/
│   └── fonts/
│
├── tests/
│   ├── test_prompt_builder.py
│   ├── test_composer.py
│   └── test_api.py
│
├── requirements.txt
├── .env.example
├── README.md
└── PROJECT_DOCUMENTATION.md
```

---

# 24. Module Responsibilities

## `prompt_builder.py`

Responsible for:

- validating creative inputs
- converting selections into a generation prompt
- adding category-specific instructions
- adding style instructions
- adding color instructions
- adding negative prompts

It must not generate images itself.

---

## `image_generator.py`

Responsible for:

- loading the selected generative model
- receiving a prompt
- generating an image
- controlling image dimensions
- controlling random seed
- saving the generated image

---

## `style_transfer.py`

Responsible for:

- loading VGG19
- extracting content/style features
- calculating content loss
- calculating style loss
- optimizing the output
- returning the stylized image

---

## `poster_composer.py`

Responsible for:

- resizing images
- cropping
- adding overlays
- placing title
- placing subtitle
- placing event details
- adding decorative elements
- exporting final PNG

---

## `image_utils.py`

Responsible for:

- format conversion
- image validation
- resizing
- safe file naming
- output directory management

---

# 25. Hardware Strategy

The project must be designed so that the AI model can be replaced depending on available hardware.

## If GPU is available

Use a pretrained diffusion model locally.

Enable:

- GPU inference
- half precision where supported
- memory-efficient attention where supported

## If only CPU is available

Options:

1. Use a smaller compatible pretrained model.
2. Use an external inference API if permitted by the institution.
3. Run generation at a smaller resolution.
4. Keep style transfer resolution small.
5. Separate the AI generation service from the frontend/backend.

The application architecture must not hard-code one model.

---

# 26. Performance Requirements

The application should:

- avoid loading the AI model for every request
- load the model once and reuse it
- validate uploaded files
- resize very large images before processing
- use reasonable generation resolution
- save generated outputs with unique names
- avoid storing unnecessary temporary files

For a student demonstration, image quality should be balanced against generation time.

---

# 27. Security and Validation

The backend must validate:

- input text length
- image file type
- image file size
- supported output formats
- required fields

Do not allow arbitrary filesystem paths from the client.

Generated filenames should be created by the server.

Example:

```text
poster_20260910_001.png
```

instead of allowing the client to specify:

```text
../../some_file.png
```

---

# 28. Error Handling

Possible errors:

### Model loading error

Display:

```text
AI model could not be loaded. Please check the model configuration.
```

### Generation error

Display:

```text
Artwork generation failed. Please try again.
```

### Invalid image

Display:

```text
Please upload a supported image format.
```

### Missing required field

Display:

```text
Please enter a poster title.
```

The backend should log technical details while the frontend shows user-friendly messages.

---

# 29. Development Plan

## Phase 1 — Environment Setup

Install:

```text
Python
PyTorch
Pillow
OpenCV
FastAPI
Uvicorn
Diffusers
Transformers
Accelerate
```

Create a virtual environment.

Verify:

```python
import torch

print(torch.__version__)
print(torch.cuda.is_available())
```

If CUDA is available, use the GPU.

---

# 30. Phase 2 — Build the Basic Frontend

Create:

- home page
- poster form
- preview area
- generate button

At this stage, use a dummy image to test the interface.

---

# 31. Phase 3 — Implement Prompt Builder

Create the structured prompt from the user's inputs.

Test several combinations.

Example:

```text
Event + Technology + Futuristic
```

should create a different prompt from:

```text
Book Cover + Fantasy + Mystical
```

---

# 32. Phase 4 — Integrate Generative AI

Implement:

```text
prompt
   |
   v
pretrained diffusion model
   |
   v
generated image
```

Do not build a training pipeline unless specifically required by the instructor.

---

# 33. Phase 5 — Implement Image Manipulation

Use Pillow/OpenCV for:

- resizing
- cropping
- brightness adjustment
- overlays
- blending
- composition

---

# 34. Phase 6 — Implement Style Transfer

Implement optional VGG19-based neural style transfer.

Start with small images for testing.

Parameters should include:

```text
style_strength
content_strength
number_of_iterations
```

Do not use excessive resolution or iterations during development.

---

# 35. Phase 7 — Build Poster Composer

Combine:

```text
AI artwork
+
title
+
description
+
date
+
time
+
venue
+
organizer
```

Export:

```text
final_poster.png
```

---

# 36. Phase 8 — Regeneration

Add a regenerate button.

Each generation should use a different random seed where supported.

Store generation metadata:

```text
prompt
seed
style
poster_type
timestamp
```

This makes experiments reproducible.

---

# 37. Phase 9 — Testing

Test the following:

### Test 1

```text
Event Poster
Technology
Futuristic
```

Expected: technology-themed artwork.

### Test 2

```text
Movie Poster
Science Fiction
Dark
```

Expected: cinematic sci-fi artwork.

### Test 3

```text
Book Cover
Fantasy
Mystical
```

Expected: fantasy artwork.

### Test 4

Generate the same input multiple times.

Expected: visually different variations.

### Test 5

Change only the style.

Expected: same concept with visibly different artistic treatment.

### Test 6

Use long title/details.

Expected: exact readable text in the final composition.

---

# 38. Evaluation Criteria

The project can be evaluated using:

| Criterion | Expected Result |
|---|---|
| Input handling | All creative fields work |
| AI generation | Original artwork is generated |
| Creativity | Different inputs produce different designs |
| Style manipulation | Style changes visibly affect output |
| Image manipulation | Images can be composed and modified |
| Text accuracy | User information remains exact |
| UI | Simple and understandable |
| Performance | Generation completes within reasonable time |
| Reliability | Errors are handled gracefully |

---

# 39. Demonstration Plan

During the project demonstration, use one fixed idea and progressively change the creative parameters.

## Demonstration 1 — Basic Generation

Input:

```text
College Tech Fest
Futuristic
Energetic
Blue/Purple
```

Show generated artwork.

## Demonstration 2 — Change Style

Keep the same concept.

Change:

```text
Cyberpunk -> Watercolor
```

Generate again.

Explain that the same concept produces a different visual interpretation.

## Demonstration 3 — Change Mood

Keep everything else the same.

Change:

```text
Energetic -> Mysterious
```

Generate again.

## Demonstration 4 — Final Poster

Show:

```text
AI artwork
+
exact event information
=
final poster
```

## Demonstration 5 — Style Transfer

Show:

```text
Original artwork
+
selected style image
=
stylized artwork
```

This directly demonstrates style-transfer capability.

---

# 40. What Makes This Different From a Normal Poster Maker?

A conventional poster maker usually provides:

```text
Template
+
User Text
+
Manual Editing
```

This project provides:

```text
User Idea
+
Creative Parameters
+
Generative AI
+
Style Manipulation
+
Image Processing
=
Original AI Artwork
```

The key innovation is that the visual artwork is **generated dynamically**, rather than selected from a fixed template library.

---

# 41. Optional Advanced Features

These features should only be implemented after the core system works.

## 41.1 Multiple Variations

Generate four visual concepts from one input.

## 41.2 Style Comparison

Display:

```text
Original | Watercolor | Cyberpunk | Vintage
```

## 41.3 AI Background Generator

Generate only the background and reserve the foreground for exact text.

## 41.4 User Image + AI Artwork

Allow an optional user image to be incorporated into the final poster.

## 41.5 Poster History

Save previous generations using SQLite.

## 41.6 Favorite Designs

Allow users to mark generated posters as favorites.

## 41.7 Prompt Editing

Show the generated prompt and allow the user to modify it.

---

# 42. Features That Should NOT Be Prioritized

Avoid spending most of the project time on:

- complicated authentication
- payment systems
- social networking
- large databases
- training a diffusion model from scratch
- complicated animations
- unnecessary admin dashboards

The assignment is primarily about **AI-generated art and creativity**, so the AI pipeline should remain the central feature.

---

# 43. Minimum Viable Product

If development time is limited, implement only:

```text
1. Poster input form
2. Prompt builder
3. Pretrained generative image model
4. AI artwork generation
5. Pillow/OpenCV poster composition
6. Exact text overlay
7. Preview
8. Regenerate
9. Download
```

This is sufficient for a strong basic demonstration.

---

# 44. Recommended Final Feature Set

For the best balance between creativity and feasibility:

### Core

- AI poster generation
- 8–10 poster categories
- theme selection
- mood selection
- artistic style selection
- color selection
- creativity level
- description input
- exact text overlay
- regeneration
- download

### AI Feature

- pretrained diffusion-based image generation

### Module-Specific Feature

- VGG19 neural style transfer

### Image Processing

- Pillow/OpenCV
- crop
- resize
- blend
- overlay
- composition

---

# 45. Example End-to-End Flow

```text
User opens application
        |
        v
Selects "Event Poster"
        |
        v
Enters "TECHFEST 2026"
        |
        v
Writes event description
        |
        v
Selects:
Technology
Futuristic
Energetic
Blue + Purple
Experimental
        |
        v
Clicks "Generate"
        |
        v
Backend validates input
        |
        v
Prompt Builder creates structured prompt
        |
        v
PyTorch generative model creates artwork
        |
        v
Optional style manipulation
        |
        v
Pillow/OpenCV processes artwork
        |
        v
Poster Composer adds exact text
        |
        v
Final PNG generated
        |
        v
User previews poster
        |
        +------> Regenerate
        |
        +------> Change Style
        |
        +------> Download
```

---

# 46. Suggested Project Name Options

Primary recommendation:

**AI Creative Poster Generator**

Other options:

1. **AI Creative Studio**
2. **PosterGen AI**
3. **ArtPoster AI**
4. **CreativeGen**
5. **GenPoster**
6. **AI PosterCraft**
7. **Idea2Art**
8. **VisionCraft AI**

For academic documentation, use:

> **AI Creative Poster Generator Using Generative AI**

---

# 47. Expected Outcome

At the end of the project, the user should be able to provide a creative concept and receive an original poster design.

The system demonstrates that generative AI can:

- interpret creative instructions,
- generate visual content,
- manipulate artistic style,
- produce multiple creative variations,
- combine AI-generated artwork with exact user information,
- and convert an abstract idea into a usable visual artifact.

---

# 48. Final Technical Requirement

The implementation must keep the AI component clearly identifiable.

At minimum:

```text
PyTorch
    |
    +--> Pretrained generative model
    |
    +--> Optional VGG19 style-transfer model
    |
    +--> Image processing
    |
    +--> Final poster composition
```

Do not present the project as a simple HTML/CSS poster editor.

The final project should demonstrate:

> **Human Idea → Generative AI → AI Artwork → Style/Image Manipulation → Final Creative Poster**

---

# 49. Instructions for Any LLM Developing This Project

If this document is provided to another LLM, the LLM should follow these rules:

1. Read this entire document before generating code.
2. Treat the project requirements in this document as the source of truth.
3. Do not replace the AI-generated artwork component with static templates.
4. Do not train a large generative model from scratch unless explicitly requested.
5. Prefer pretrained models compatible with PyTorch.
6. Keep the generative model behind a service/module interface so it can be replaced.
7. Keep poster text rendering separate from image generation.
8. Never rely on the image-generation model for exact dates, names, venues, or long text.
9. Keep the frontend simple and student-project friendly.
10. Build and test the project incrementally.
11. Explain every major AI component in terms suitable for a student viva.
12. Include error handling and validation.
13. Keep all generated files inside controlled output directories.
14. Provide installation instructions and dependency versions.
15. Provide a README with setup, execution, and troubleshooting steps.
16. Prefer a working minimum viable product over unnecessary advanced features.
17. If hardware limitations make the selected model impractical, replace it with a lighter compatible pretrained model without changing the overall architecture.
18. Preserve the two central AI capabilities:
    - generative image creation
    - style/image manipulation
19. Make the final demonstration clearly show how changing creative inputs changes the generated artwork.
20. When generating code, create complete files rather than isolated snippets whenever possible.

---

# 50. Definition of Done

The project is considered complete when all of the following are true:

- [ ] Application launches successfully.
- [ ] User can select a poster type.
- [ ] User can enter title and description.
- [ ] User can select theme.
- [ ] User can select mood.
- [ ] User can select artistic style.
- [ ] User can select colors.
- [ ] User can select creativity level.
- [ ] Backend validates the input.
- [ ] Prompt builder creates a structured prompt.
- [ ] Generative AI model creates original artwork.
- [ ] Artwork can be processed using Pillow/OpenCV.
- [ ] Exact poster text can be added.
- [ ] Final poster can be previewed.
- [ ] User can regenerate a variation.
- [ ] Final poster can be downloaded.
- [ ] Style-transfer functionality is demonstrated or implemented as an optional mode.
- [ ] The project runs using PyTorch/TensorFlow concepts as required.
- [ ] README contains installation and execution instructions.
- [ ] Project documentation explains the AI pipeline.
- [ ] A final demonstration can show at least two different outputs from different creative inputs.

---

# 51. Short Project Summary

**AI Creative Poster Generator** is a generative-AI-based image application that transforms user-provided creative ideas into original poster artwork. Users specify the poster type, title, description, theme, mood, color palette, artistic style, and creativity level. A pretrained generative model creates the visual artwork, while PyTorch-based neural style transfer and Pillow/OpenCV image manipulation can be used to experiment with artistic transformations. Exact textual information is added programmatically to create a readable final poster.

The project demonstrates the use of **generative AI, image generation, style transfer, image manipulation, and human-AI creativity**, making it directly relevant to the **AI-Generated Art and Creativity** module.
