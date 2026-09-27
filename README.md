# ArtGen Studio: Generative AI & Creative Poster Suite

**Course Assignment:** Generative AI — Module 3: *AI-Generated Art and Creativity*  
**Frameworks:** PyTorch, Torchvision, Streamlit, Pillow  

---

## 📌 Project Highlights

- **Lightweight & Fast:** Engineered specifically to run smoothly on standard student laptops (CPU or GPU) without freezing or exhausting memory.
- **Three Creative Generative Modes:**
  1. **Mode 1: AI Creative Poster Generator (6 Thematic Categories):** Converts natural language concepts (Title, Theme, Mood, Art Style, Colors, Creativity level) into an AI-synthesized artistic background with exact, crisp typography overlay. Features 6 quick-load topic presets matching rich visuals:
     - 🚀 **Movie Poster (Sci-Fi):** *The Last Signal* (Deep space, astronaut & planetary rings)
     - 🌆 **Event Poster (College Fest):** *TECHFEST 2026* (Cyberpunk neon skyline & tech silhouette)
     - 🌸 **Invitation Card:** *Sarah's 21st Birthday* (Blush roses & botanical frame)
     - 🎧 **Album Cover:** *Midnight* (Lo-fi twilight anime skyline & moon)
     - 🌲 **Book Cover:** *The Forgotten Forest* (Enchanted forest & glowing stag)
     - ⌚ **Advertisement Poster:** *Smart Watch* (Premium dark studio product ad)
  2. **Mode 2: Neural Style Transfer (Gatys et al.):** Uses pre-trained VGG19 with Gram matrix feature correlations. Includes **Dual-Style Blending** and **Color-Preservation** mode.
  3. **Mode 3: Google DeepDream Lab:** Performs layer-selective gradient ascent activation maximization across multi-scale octave pyramids.
- **Embedded Academic Theory:** Built-in formulas, loss curves, and viva Q&A for academic presentations.
- **One-Click Export:** Download generated posters and artwork in high-resolution PNG format.

---

## 🚀 Quick Start Guide (Windows)

### Option A — 1-Click Launch (Recommended)
If you extracted this folder and the `venv` is already created:
1. Double-click **`run.bat`**  
2. Your web browser will automatically open at `http://localhost:8501`.

### Option B — Manual Setup via Terminal
Open **PowerShell** or **Command Prompt** in this project directory:

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
.\venv\Scripts\activate

# 3. Install lightweight dependencies
pip install -r requirements.txt

# 4. Run the application
streamlit run app.py
```

---

## 📁 Project Structure

```
d:/assignmentGenAI/
├── app.py                      # Main Streamlit web application
├── models/
│   ├── deepdream.py            # DeepDream generator (gradient ascent on feature maps)
│   ├── style_transfer.py      # Gatys Neural Style Transfer with Gram matrices
│   └── poster_generator.py     # Structured prompt builder and topic background library
├── utils/
│   ├── poster_composer.py      # Pillow-based specialized graphic design & typography compositor
│   └── image_ops.py            # Image transforms, downsampling & sample assets generator
├── assets/
│   ├── topics/                 # 6 High-resolution topic-specific AI generated backgrounds
│   ├── content/                # Pre-loaded sample content photographs
│   └── styles/                 # Masterpiece style images (Van Gogh, Cyberpunk, Cubism)
├── requirements.txt            # Minimal dependencies (torch, torchvision, streamlit, pillow)
├── run.bat                     # 1-click application runner for Windows
├── setup_env.bat               # 1-click environment installer
├── README.md                   # Project overview & instructions
└── ASSIGNMENT_REPORT.md        # Comprehensive academic submission report
```

---

## 🎨 How to Demonstrate to Faculty / "Mam"

1. **AI Poster Generation (Tab 1):**
   - Select a poster type (e.g. *Event Poster* or *Movie Poster*).
   - Enter a title and adjust the **Creativity Level** slider (Balanced vs. Surreal) to show how generative parameters affect visual complexity.
   - Click **Generate Artwork & Poster** and show the instant preview and PNG download.
2. **Neural Style Transfer (Tab 2):**
   - Select *Campus Building* and *Starry Night*.
   - Toggle **Dual-Style Blending** (e.g., 60% Van Gogh + 40% Cyberpunk) to demonstrate style mixing.
   - Click **Run Neural Style Transfer** to show live optimization progress.
3. **DeepDream Lab (Tab 3):**
   - Select an image and switch between *Layer 4 (Textures)* and *Layer 16 (Geometries)* to explain how deep neural networks represent visual features hierarchically.
4. **Theory & Viva (Tab 4):**
   - Walk through the mathematical formulas for Content Loss, Gram Matrix Style Loss, and DeepDream activation maximization.
