"""
ArtGen Studio: Generative AI & Creative Poster Suite
----------------------------------------------------
Streamlit web application demonstrating:
1. Mode 1: AI Creative Poster Generator (Category Sub-Styles Dropdown + Dynamic Palette Recolor + Specialized Layouts)
2. Mode 2: Neural Style Transfer (Gatys et al., Dual-Style Blending, Color Preservation)
3. Mode 3: DeepDream Lab (Layer Activation Maximization & Octave Pyramid)
4. Theoretical Concepts & Academic Documentation (Formulas, Architectures, Viva Prep)
"""

import streamlit as st
import os
import io
import torch
from PIL import Image

# Import internal modules
from models.poster_generator import PosterGenerator
from utils.poster_composer import PosterComposer
from utils.image_ops import ensure_sample_assets

# Page configuration
st.set_page_config(
    page_title="ArtGen Studio | AI Creative Poster Suite",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Glassmorphic Modern CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-bottom: 1.2rem;
    }
    .topic-preset-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 12px;
        padding: 0.8rem;
        text-align: center;
        transition: all 0.2s ease-in-out;
    }
    .topic-preset-card:hover {
        border-color: #38bdf8;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# Ensure sample assets exist
content_dir, style_dir = ensure_sample_assets("assets")

# Device detection
device_str = "CUDA (NVIDIA GPU)" if torch.cuda.is_available() else "CPU (Optimized)"

# Sidebar
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3", use_container_width=True)
    st.markdown("### 🎨 ArtGen Studio")
    st.caption("Module 3: AI-Generated Art & Creativity")
    st.write(f"**Execution Hardware:** `{device_str}`")
    st.info("💡 **Fast & Lightweight:** Offline neural computation with dynamic color palette tinting.")
    st.markdown("---")
    st.markdown("#### Quick Navigation")
    st.markdown("""
    - 🖼️ **AI Poster Generator** (Topic & Palette Controls)
    - 📚 **Theory & Viva Prep**
    """)

# Main Header
st.markdown('<div class="main-header">🎨 AI Creative Poster Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Turn your ideas into stunning visuals with Generative AI, Multiple Artwork Sub-Styles, and Dynamic Color Palette Controls!</div>', unsafe_allow_html=True)

# Tabs
tab1, tab_theory = st.tabs([
    "🖼️ AI Creative Poster Generator",
    "📚 Theory & Viva Prep",
])

poster_engine = PosterGenerator()
composer_engine = PosterComposer()

# ----------------------------------------------------------------------------------
# TAB 1: AI CREATIVE POSTER GENERATOR
# ----------------------------------------------------------------------------------
with tab1:
    st.markdown("### 🌟 Choose a Topic Category or Customize Your Theme & Color Palette")
    st.write("Selecting a poster category reveals a **dropdown of multiple background sub-styles**. Changing the **Color Palette, Theme, Mood, or Style** dynamically recolors and restyles the poster!")

    # 6 Topic Presets Definition
    presets_data = {
        "1. Movie Poster": {
            "type": "Movie Poster",
            "title": "THE LAST SIGNAL",
            "genre": "Sci-Fi",
            "mood": "Mysterious",
            "theme": "Space & Cosmic",
            "style": "Digital Art",
            "colors": "Deep Cosmic (Space)",
            "desc": "A lone deep-space scientist intercepts an ancient, encrypted alien signal echoing from an unknown forbidden star system.",
            "tagline": "SOME SIGNALS ARE NOT MEANT TO BE FOUND",
            "date": "IN CINEMAS OCTOBER 2026",
            "venue": "IMAX & WORLDWIDE THEATERS",
            "time": "NOW SHOWING",
            "organizer": "ARTGEN CINEMAS & NOVA STUDIOS",
            "substyle": "Style 1: Sci-Fi Space & Planet (Cosmic Orb & Astronaut)",
            "img_file": "movie_scifi.png",
        },
        "2. Event Poster (College Fest)": {
            "type": "Event Poster",
            "title": "TECHFEST 2026",
            "genre": "Technology",
            "mood": "Energetic",
            "theme": "Technology",
            "style": "Cyberpunk",
            "colors": "Vibrant Neon (Cyberpunk)",
            "desc": "National collegiate technology symposium featuring AI hackathons, robotics challenges, coding wars, and keynote guest lectures.",
            "tagline": "A FESTIVAL OF IDEAS, TECHNOLOGY & YOU",
            "date": "15 - 17 APR 2026",
            "venue": "Campus Main Auditorium & Tech Labs",
            "time": "09:30 AM - 06:00 PM",
            "organizer": "DEPT. OF COMPUTER SCIENCE & AI",
            "substyle": "Style 1: Cyberpunk Techfest (Metropolis & Tech Silhouette)",
            "img_file": "event_techfest.png",
        },
        "3. Invitation Card": {
            "type": "Invitation Card",
            "title": "Sarah's 21st Birthday",
            "genre": "Birthday / Celebration",
            "mood": "Calm",
            "theme": "Floral & Botanical",
            "style": "Watercolor",
            "colors": "Floral Blush (Pink/Green/Cream)",
            "desc": "An elegant evening banquet celebrating 21 milestones filled with laughter, dinner, acoustic melodies, and memorable moments.",
            "tagline": "Celebrate • Reminisce • Joy",
            "date": "Saturday, 28th March 2026",
            "venue": "The Grand Orchid Ballroom, Sunset Blvd",
            "time": "06:30 PM Onwards",
            "organizer": "Warmly Hosted by the Miller Family",
            "substyle": "Style 1: Elegant Floral (Blush Roses & Peonies Frame)",
            "img_file": "invitation_floral.png",
        },
        "4. Album Cover": {
            "type": "Album Cover",
            "title": "Midnight Reverie",
            "genre": "Lo-fi",
            "mood": "Calm",
            "theme": "Music & Culture",
            "style": "Digital Art",
            "colors": "Blue + Purple (Cyber/Tech)",
            "desc": "Chill lo-fi study beats and nostalgic ambient synthesizers for rainy midnight strolls and quiet rooftop contemplations.",
            "tagline": "DREAMS • CHILL • REPEAT",
            "date": "STREAMING ON ALL PLATFORMS",
            "venue": "STEREO VINYL EDITION",
            "time": "RUNTIME: 42 MINS",
            "organizer": "LO-FI DREAMS RECORDINGS",
            "substyle": "Style 1: Lo-Fi Twilight Rooftop (Anime City & Moon)",
            "img_file": "album_lofi.png",
        },
        "5. Book Cover": {
            "type": "Book Cover",
            "title": "The Forgotten Forest",
            "genre": "Fantasy",
            "mood": "Mysterious",
            "theme": "Nature & Ecology",
            "style": "Fantasy",
            "colors": "Emerald Nature (Green/Teal)",
            "desc": "An epic fantasy novel chronicling a young ranger who wanders past the ancient mist boundary into a kingdom ruled by forgotten beasts.",
            "tagline": "SOME REALMS SHOULD REMAIN UNTOUCHED",
            "date": "NATIONAL BESTSELLER",
            "venue": "FIRST HARDBACK EDITION",
            "time": "",
            "organizer": "A FANTASY NOVEL BY E. R. VANCE",
            "substyle": "Style 1: Enchanted Forest & Stag (Magical Sunbeams)",
            "img_file": "book_fantasy.png",
        },
        "6. Advertisement Poster": {
            "type": "Advertisement Poster",
            "title": "NEXA PULSE 5 PRO",
            "genre": "Product Showcase",
            "mood": "Futuristic",
            "theme": "Technology",
            "style": "Digital Art",
            "colors": "Monochrome & Minimalist",
            "desc": "Next-generation aerospace titanium smartwatch with real-time biometric tracking, holographic OLED display, and 14-day endurance battery.",
            "tagline": "SMARTER TODAY • BRIGHTER TOMORROW",
            "date": "PRE-ORDER AVAILABLE NOW",
            "venue": "OFFICIAL FLAGSHIP STORES",
            "time": "LIMITED LAUNCH EDITION",
            "organizer": "NEXA ADVANCED TECHNOLOGIES",
            "substyle": "Style 1: Smartwatch Studio (Dark Metallic & Neon Rim)",
            "img_file": "ad_smartwatch.png",
        },
    }

    # Initialize default form values if not already in session state
    default_init = {
        "form_type": "Event Poster",
        "form_title": "TECHFEST 2026",
        "form_tagline": "A FESTIVAL OF IDEAS, TECHNOLOGY & YOU",
        "form_desc": "National collegiate technology symposium featuring AI hackathons, robotics challenges, coding wars, and keynote guest lectures.",
        "form_theme": "Technology",
        "form_mood": "Energetic",
        "form_style": "Cyberpunk",
        "form_colors": "Vibrant Neon (Cyberpunk)",
        "form_date": "15 - 17 APR 2026",
        "form_venue": "Campus Main Auditorium & Tech Labs",
        "form_time": "09:30 AM - 06:00 PM",
        "form_organizer": "DEPT. OF COMPUTER SCIENCE & AI",
        "form_substyle": "Style 1: Cyberpunk Techfest (Metropolis & Tech Silhouette)",
        "form_bg_mode": "✨ Topic Sub-Style AI Artwork (Selected Dropdown)",
        "form_creativity": "Experimental",
        "form_seed": 42,
        "selected_preset_key": "2. Event Poster (College Fest)",
        "poster_generated": False,
    }
    for k, v in default_init.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # Display 6 Showcase Preset Buttons in a 6-Column Grid
    st.markdown("#### ⚡ Quick-Load Topic Showcase")
    st.caption("👉 Click any card below to **instantly populate all professional poster details AND generate the artwork** for your guide!")
    p_cols = st.columns(6)
    for idx, (p_name, p_val) in enumerate(presets_data.items()):
        with p_cols[idx]:
            thumb_path = os.path.join("assets", "topics", p_val["img_file"])
            if os.path.exists(thumb_path):
                st.image(thumb_path, use_container_width=True)
            if st.button(f"Load {p_val['type']}", key=f"btn_p_{idx}", use_container_width=True):
                # Populate all input fields with the preset values
                st.session_state["selected_preset_key"] = p_name
                st.session_state["form_type"] = p_val["type"]
                st.session_state["form_title"] = p_val["title"]
                st.session_state["form_desc"] = p_val["desc"]
                st.session_state["form_tagline"] = p_val["tagline"]
                st.session_state["form_theme"] = p_val["theme"]
                st.session_state["form_mood"] = p_val["mood"]
                st.session_state["form_style"] = p_val["style"]
                st.session_state["form_colors"] = p_val["colors"]
                st.session_state["form_date"] = p_val["date"]
                st.session_state["form_venue"] = p_val["venue"]
                st.session_state["form_time"] = p_val["time"]
                st.session_state["form_organizer"] = p_val["organizer"]
                st.session_state["form_substyle"] = p_val.get("substyle", "")
                st.session_state["form_bg_mode"] = "✨ Topic Sub-Style AI Artwork (Selected Dropdown)"
                # Trigger instant generation so the guide immediately sees the finished result!
                st.session_state["trigger_generate"] = True
                st.rerun()

    st.markdown("---")

    # Main Form & Output Columns
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f"#### 1. Input Parameters ({st.session_state.get('form_type', 'Event Poster')})")

        type_options = ["Event Poster", "Movie Poster", "Invitation Card", "Album Cover", "Book Cover", "Advertisement Poster", "Custom"]
        if st.session_state.get("form_type") not in type_options:
            st.session_state["form_type"] = type_options[0]
        c_type = st.selectbox(
            "Poster Type / Template",
            type_options,
            key="form_type"
        )

        # Dynamic Sub-Style Dropdown
        available_substyles = poster_engine.get_substyles_for_category(c_type)
        if st.session_state.get("form_substyle") not in available_substyles:
            st.session_state["form_substyle"] = available_substyles[0]
        c_substyle = st.selectbox(
            f"🎨 Select Artwork Sub-Style for {c_type}",
            available_substyles,
            key="form_substyle",
            help="Choose from multiple background art variations tailored to this topic!"
        )

        c_title = st.text_input("Main Title / Name / Headline", key="form_title")
        c_tagline = st.text_input("Tagline / Subtext / Slogan", key="form_tagline")
        c_desc = st.text_area("Concept Description", key="form_desc", height=70)

        sub_c1, sub_c2 = st.columns(2)
        with sub_c1:
            theme_list = ["Technology", "Space & Cosmic", "Floral & Botanical", "Nature & Ecology", "Music & Culture", "Cyberpunk", "Minimalist"]
            if st.session_state.get("form_theme") not in theme_list:
                st.session_state["form_theme"] = theme_list[0]
            c_theme = st.selectbox("Theme", theme_list, key="form_theme")

            mood_list = ["Energetic", "Dramatic", "Futuristic", "Mysterious", "Calm", "Inspirational"]
            if st.session_state.get("form_mood") not in mood_list:
                st.session_state["form_mood"] = mood_list[0]
            c_mood = st.selectbox("Mood", mood_list, key="form_mood")

            style_list = ["Cyberpunk", "Digital Art", "Watercolor", "Oil Painting", "Minimalist", "Fantasy"]
            if st.session_state.get("form_style") not in style_list:
                st.session_state["form_style"] = style_list[0]
            c_style = st.selectbox("Artistic Style", style_list, key="form_style")

        with sub_c2:
            pal_list = list(poster_engine.color_palettes.keys())
            if st.session_state.get("form_colors") not in pal_list:
                st.session_state["form_colors"] = pal_list[0]
            c_colors = st.selectbox("Color Palette (Dynamically Recolors Artwork)", pal_list, key="form_colors")

            c_creativity = st.select_slider("Creativity Level", options=["Balanced", "Artistic", "Experimental", "Surreal"], key="form_creativity")
            c_seed = st.number_input("Random Seed (Vary for new visual patterns)", step=1, key="form_seed")

        st.markdown("#### 2. Background Artwork Source")
        bg_modes = ["✨ Topic Sub-Style AI Artwork (Selected Dropdown)", "🎨 Procedural Neural Synthesizer", "📁 Upload Custom Background Image"]
        if st.session_state.get("form_bg_mode") not in bg_modes:
            st.session_state["form_bg_mode"] = bg_modes[0]
        bg_mode = st.radio(
            "Artwork Generation Mode:",
            bg_modes,
            key="form_bg_mode",
            horizontal=False
        )

        custom_bg_img = None
        if "Upload" in bg_mode:
            up_art = st.file_uploader("Upload Background Image", type=["jpg", "jpeg", "png"], key="custom_bg_upload")
            if up_art:
                custom_bg_img = Image.open(up_art)

        st.markdown("#### 3. Specific Text & Layout Details")
        tc1, tc2 = st.columns(2)
        with tc1:
            c_date = st.text_input("Date / Release Tag", key="form_date")
            c_venue = st.text_input("Venue / Location", key="form_venue")
        with tc2:
            c_time = st.text_input("Time / Event Duration", key="form_time")
            c_organizer = st.text_input("Brand / Organizer / Author / Billing", key="form_organizer")

        generate_btn = st.button("🚀 Generate Artwork & Poster", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 4. AI Output Preview & Export")

        prompt, neg_prompt = poster_engine.build_structured_prompt(
            poster_type=c_type,
            title=c_title,
            description=c_desc,
            theme=c_theme,
            mood=c_mood,
            art_style=c_style,
            colors=c_colors,
            creativity=c_creativity,
            substyle=c_substyle,
        )

        with st.expander("📝 View Structured AI Prompt Construction", expanded=False):
            st.code(prompt, language="text")
            st.caption(f"**Negative Prompt:** {neg_prompt}")

        # Only generate on explicit button click — no auto-generation on load
        should_run = generate_btn or st.session_state.get("trigger_generate", False)
        if "trigger_generate" in st.session_state:
            del st.session_state["trigger_generate"]

        if should_run:
            with st.spinner("✨ Synthesizing selected sub-style AI artwork with dynamic color palette..."):
                if custom_bg_img is not None:
                    art = custom_bg_img
                elif "Topic Sub-Style" in bg_mode:
                    art = poster_engine.synthesize_art_canvas(
                        poster_type=c_type,
                        theme=c_theme,
                        mood=c_mood,
                        art_style=c_style,
                        colors=c_colors,
                        creativity=c_creativity,
                        substyle=c_substyle,
                        seed=c_seed,
                        use_topic_preset=True,
                    )
                else:
                    art = poster_engine.synthesize_art_canvas(
                        poster_type=c_type,
                        theme=c_theme,
                        mood=c_mood,
                        art_style=c_style,
                        colors=c_colors,
                        creativity=c_creativity,
                        substyle=c_substyle,
                        seed=c_seed,
                        use_topic_preset=False,
                    )

                # Extract accent RGB tuple from selected Color Palette
                pal_tuples = poster_engine.color_palettes.get(c_colors, [(56, 189, 248), (56, 189, 248), (56, 189, 248), (56, 189, 248)])
                accent_rgb = pal_tuples[3] if len(pal_tuples) > 3 else pal_tuples[0]

                final_p = composer_engine.compose_poster(
                    artwork_img=art,
                    title=c_title,
                    poster_type=c_type,
                    theme=c_theme,
                    description=c_desc,
                    date_str=c_date,
                    time_str=c_time,
                    venue_str=c_venue,
                    organizer_str=c_organizer,
                    tagline=c_tagline,
                    accent_color=accent_rgb,
                )
                st.session_state["last_art"] = art
                st.session_state["last_poster"] = final_p
                st.session_state["poster_generated"] = True

        if st.session_state.get("poster_generated") and "last_poster" in st.session_state:
            st.image(st.session_state["last_poster"], caption=f"Generated {c_type} — {c_colors}", use_container_width=True)
            buf = io.BytesIO()
            st.session_state["last_poster"].save(buf, format="PNG")
            st.download_button(
                label="📥 Download High-Res Poster (PNG)",
                data=buf.getvalue(),
                file_name=f"poster_{c_title.replace(' ', '_').lower()}.png",
                mime="image/png",
                use_container_width=True,
            )
        else:
            # Welcome placeholder — nothing generated yet
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, rgba(30,41,59,0.85) 0%, rgba(15,23,42,0.95) 100%);
                border: 2px dashed rgba(99,102,241,0.45);
                border-radius: 18px;
                padding: 3.5rem 2rem;
                text-align: center;
                min-height: 480px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            ">
                <div style="font-size:4rem;margin-bottom:1rem;">🎨</div>
                <div style="font-size:1.5rem;font-weight:700;color:#818cf8;margin-bottom:0.5rem;">Your Poster Preview Will Appear Here</div>
                <div style="color:#94a3b8;font-size:1rem;max-width:340px;line-height:1.6;">
                    Choose a <strong style='color:#38bdf8'>Poster Type</strong>, select a
                    <strong style='color:#c084fc'>Sub-Style</strong> and a
                    <strong style='color:#f472b6'>Color Palette</strong>, then click
                    <strong style='color:#34d399'>🚀 Generate Artwork</strong> below.
                </div>
                <div style="margin-top:1.8rem;font-size:2.2rem;">⬅️</div>
                <div style="color:#64748b;font-size:0.85rem;margin-top:0.4rem;">Fill in the form on the left to get started</div>
            </div>
            """, unsafe_allow_html=True)

# ----------------------------------------------------------------------------------
# THEORY & ACADEMIC VIVA QUESTIONS
# ----------------------------------------------------------------------------------
with tab_theory:
    st.markdown("### 📚 Academic Concepts & Theory (Module 3)")
    st.markdown("""
    Use these theoretical explanations, mathematical formulas, and concepts when presenting to your faculty / "mam" during viva or project evaluation:
    """)

    with st.expander("1. Neural Style Transfer Mathematical Formulation (Gatys et al.)", expanded=True):
        st.markdown(r"""
        **Content Representation & Loss:**
        Given an original image $\vec{p}$ and generated image $\vec{x}$, their feature representations in layer $l$ are $P^l$ and $F^l$.
        The content loss is the Mean Squared Error:
        $$\mathcal{L}_{\text{content}}(\vec{p}, \vec{x}, l) = \frac{1}{2} \sum_{i,j} \left( F_{ij}^l - P_{ij}^l \right)^2$$

        **Style Representation (Gram Matrix):**
        Style is captured by feature cross-correlations across filter channels, represented by the Gram matrix $G^l \in \mathbb{R}^{N_l \times N_l}$:
        $$G_{ij}^l = \sum_k F_{ik}^l F_{jk}^l$$
        
        The style loss between style image $\vec{a}$ and generated image $\vec{x}$ across layer $l$:
        $$\mathcal{L}_{\text{style}}(\vec{a}, \vec{x}) = \sum_l w_l \frac{1}{4 N_l^2 M_l^2} \sum_{i,j} \left( G_{ij}^l - A_{ij}^l \right)^2$$

        **Total Loss Optimized:**
        $$\mathcal{L}_{\text{total}}(\vec{p}, \vec{a}, \vec{x}) = \alpha \mathcal{L}_{\text{content}} + \beta \mathcal{L}_{\text{style}}$$
        """)

    with st.expander("2. DeepDream: Gradient Ascent & Activation Maximization"):
        st.markdown(r"""
        Unlike standard neural network training where weights $\theta$ are updated to minimize classification error,
        **DeepDream fixes network weights** and performs **gradient ascent directly on the input image pixels $I$**:
        $$I \leftarrow I + \eta \cdot \frac{\partial \|a^l(I)\|^2}{\partial I}$$
        where $a^l(I)$ is the activation of convolutional layer $l$, and $\eta$ is the step size.
        - **Shallow Layers (conv1, conv2):** Maximize edge, swirl, and texture responses.
        - **Deep Layers (conv4, conv5):** Maximize complex features such as eyes, geometric curves, and hallucinatory patterns.
        """)

    with st.expander("3. Why Separate Typography Composition from AI Art Generation?"):
        st.markdown("""
        Text-to-image generative models often struggle with exact textual spelling (producing garbled or unreadable characters) because diffusion/GAN models learn pixel distributions rather than semantic character glyphs.
        
        **Our Hybrid Architecture Solution:**
        1. Generative AI is utilized for **conceptual background artwork, style synthesis, and aesthetics**.
        2. A deterministic **Typography Engine (Pillow/OpenCV)** is utilized for **exact title, dates, venues, and contact information**.
        3. This delivers the best of both worlds: **limitless AI visual creativity** combined with **100% accurate, professional graphic design output**.
        """)

    with st.expander("4. Common Viva & Evaluation Questions"):
        st.markdown("""
        - **Q: Why use VGG19 instead of ResNet for Neural Style Transfer?**  
          *A:* VGG features preserve spatial pixel arrangements through straightforward pooling layers without skip-connections, which yields richer, more coherent texture transfer.
        - **Q: What is the purpose of the Gram matrix?**  
          *A:* It calculates feature correlations across channels, discarding spatial location information (content) while preserving overall textures, color frequencies, and stroke patterns (style).
        - **Q: How does DeepDream create fractal patterns?**  
          *A:* By using an **octave pyramid**, the image is downscaled and upscaled recursively so that patterns maximized at lower resolutions become high-frequency textures at higher resolutions.
        """)
