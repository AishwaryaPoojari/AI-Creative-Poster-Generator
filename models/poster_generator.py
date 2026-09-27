"""
AI Creative Poster Generator Engine
-----------------------------------
1. Structured Prompt Construction with Category & Sub-Style Enhancements
2. Multiple Background Artwork Sub-Styles per Poster Category (4 per category)
3. Full Palette & Theme Integration - palette changes are STRONGLY visible (75% blend)
4. Helper drawing routines: radial glow, stars, grid, gradient background
5. Mood-based final brightness/contrast adjustments
"""

import math
import random
import os
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps
import numpy as np


class PosterGenerator:
    def __init__(self, assets_dir="assets"):
        self.assets_dir = assets_dir
        self.topics_dir = os.path.join(assets_dir, "topics")

        # Color palette mappings: [dark-bg, mid, accent1, accent2/highlight]
        self.color_palettes = {
            "Blue + Purple (Cyber/Tech)":     [(20,20,60),    (30,80,190),   (140,45,225),  (60,220,255)],
            "Vibrant Neon (Cyberpunk)":       [(15,10,30),    (255,0,128),   (0,240,255),   (130,0,255)],
            "Warm Sunset (Red/Orange/Gold)":  [(40,10,15),    (220,50,40),   (250,140,30),  (255,215,80)],
            "Emerald Nature (Green/Teal)":    [(10,30,20),    (20,100,60),   (45,185,120),  (160,240,190)],
            "Deep Cosmic (Space)":            [(5,5,20),      (30,20,70),    (90,60,180),   (230,200,255)],
            "Floral Blush (Pink/Green/Cream)":[(248,244,240), (230,160,180), (120,165,130), (210,90,130)],
            "Monochrome & Minimalist":        [(15,15,20),    (70,70,80),    (170,170,180), (245,245,250)],
            "Pastel Dream":                   [(230,220,245), (250,200,210), (190,230,240), (255,240,200)],
        }

        self.category_substyles = {
            "Invitation Card": [
                "Style 1: Elegant Floral (Blush Roses & Peonies Frame)",
                "Style 2: Royal Gold Foil & White Marble Geometric",
                "Style 3: Tropical Botanical & Emerald Leaf Border",
                "Style 4: Minimalist Pastel & Decorative Gold Line",
            ],
            "Movie Poster": [
                "Style 1: Sci-Fi Space & Planet (Cosmic Orb & Astronaut)",
                "Style 2: Action & Explosion (Cinematic Ember Glow)",
                "Style 3: Dark Thriller & Noir (Ominous Fog & Spotlight)",
                "Style 4: Cyberpunk Sci-Fi (Neon Sky & Beams)",
            ],
            "Event Poster": [
                "Style 1: Cyberpunk Techfest (Metropolis & Tech Silhouette)",
                "Style 2: EDM Music & Stage Lasers (Concert Beams)",
                "Style 3: Hackathon & Digital Grid (Matrix Binary Nodes)",
                "Style 4: Retro Synthwave Sunset (80s Neon Sun & Grid)",
            ],
            "Album Cover": [
                "Style 1: Lo-Fi Twilight Rooftop (Anime City & Moon)",
                "Style 2: Vintage Vinyl Record (Radial Sunset Glow)",
                "Style 3: Synthwave Neon Grid (Vaporwave Aesthetic)",
                "Style 4: Acoustic Sunbeam Glow (Warm Bokeh Light)",
            ],
            "Book Cover": [
                "Style 1: Enchanted Forest & Stag (Magical Sunbeams)",
                "Style 2: Gothic Castle & Stormy Moon (Ominous Fortress)",
                "Style 3: Sci-Fi Space Portal (Hyper-Drive Starfield)",
                "Style 4: Ornate Leather & Gold (Classic Bestseller)",
            ],
            "Advertisement Poster": [
                "Style 1: Smartwatch Studio (Dark Metallic & Neon Rim)",
                "Style 2: Modern Wireless Audio (Sleek Product Glow)",
                "Style 3: Energy Splash & Motion (Dynamic Particles)",
                "Style 4: Glassmorphic Minimalist (Frosted Glass Glow)",
            ],
        }

        self.topic_presets = {
            "Movie Poster":         "movie_scifi.png",
            "Event Poster":         "event_techfest.png",
            "Invitation Card":      "invitation_floral.png",
            "Album Cover":          "album_lofi.png",
            "Book Cover":           "book_fantasy.png",
            "Advertisement Poster": "ad_smartwatch.png",
        }

    def get_substyles_for_category(self, category_name):
        for key in self.category_substyles:
            if key.lower() in category_name.lower() or category_name.lower() in key.lower():
                return self.category_substyles[key]
        return ["Style 1: AI Artwork","Style 2: Geometric Glow",
                "Style 3: Cosmic Nebula","Style 4: Minimalist Studio"]

    def get_topic_background(self, poster_type, width=768, height=1152):
        for p_key, filename in self.topic_presets.items():
            if p_key.lower() in poster_type.lower() or poster_type.lower() in p_key.lower():
                path = os.path.join(self.topics_dir, filename)
                if os.path.exists(path):
                    try:
                        img = Image.open(path).convert("RGB")
                        return img.resize((width, height), Image.Resampling.LANCZOS)
                    except Exception:
                        pass
        return None

    def _apply_palette_tint(self, image, palette_name):
        """75% palette colour mapping so changes are clearly visible."""
        palette = self.color_palettes.get(palette_name)
        if not palette:
            return image
        bg_dark, color_mid, color_accent1, color_accent2 = palette
        gray_np = np.array(ImageOps.grayscale(image), dtype=np.float32) / 255.0
        h, w = gray_np.shape
        recolored = np.zeros((h, w, 3), dtype=np.float32)
        p0 = np.array(bg_dark,       dtype=np.float32)
        p1 = np.array(color_mid,     dtype=np.float32)
        p2 = np.array(color_accent1, dtype=np.float32)
        p3 = np.array(color_accent2, dtype=np.float32)
        t0 = np.clip(gray_np / 0.33,        0, 1)[..., None]
        t1 = np.clip((gray_np-0.33)/0.33,   0, 1)[..., None]
        t2 = np.clip((gray_np-0.66)/0.34,   0, 1)[..., None]
        m0 = gray_np < 0.33
        m1 = (gray_np >= 0.33) & (gray_np < 0.66)
        m2 = gray_np >= 0.66
        recolored[m0] = (1-t0[m0])*p0 + t0[m0]*p1
        recolored[m1] = (1-t1[m1])*p1 + t1[m1]*p2
        recolored[m2] = (1-t2[m2])*p2 + t2[m2]*p3
        rc = Image.fromarray(np.clip(recolored, 0, 255).astype(np.uint8))
        tinted = Image.blend(image, rc, alpha=0.75)
        return ImageEnhance.Color(tinted).enhance(1.25)

    def _gradient_bg(self, width, height, top_color, bottom_color):
        arr = np.zeros((height, width, 3), dtype=np.uint8)
        for y in range(height):
            t = y / (height - 1)
            for c in range(3):
                arr[y, :, c] = int(top_color[c]*(1-t) + bottom_color[c]*t)
        return Image.fromarray(arr)

    def _draw_stars(self, draw, width, height, count=140, rng=None):
        rng = rng or random
        for _ in range(count):
            sx,sy = rng.randint(0,width), rng.randint(0,height)
            sr = rng.randint(1,3)
            draw.ellipse([sx,sy,sx+sr,sy+sr], fill=(255,255,255,rng.randint(100,255)))

    def _draw_grid(self, draw, width, height, color, spacing=30, alpha=45):
        for x in range(0, width, spacing):
            draw.line([(x,0),(x,height)], fill=(color[0],color[1],color[2],alpha), width=1)
        for y in range(0, height, spacing):
            draw.line([(0,y),(width,y)], fill=(color[0],color[1],color[2],alpha), width=1)

    def _radial_glow(self, draw, cx, cy, max_r, color, step=16, base_alpha=65):
        for r in range(max_r, 15, -step):
            t = 1.0 - r/max_r
            a = int(base_alpha * (t**1.6))
            draw.ellipse([cx-r,cy-r,cx+r,cy+r], fill=(color[0],color[1],color[2],a))

    def build_structured_prompt(self, poster_type="Event Poster", title="TECHFEST 2026",
            description="A premier college festival.", theme="Technology", mood="Energetic",
            art_style="Cyberpunk", colors="Blue + Purple (Cyber/Tech)",
            creativity="Experimental", substyle=None):
        prompt = (
            f"Create an original {poster_type} visual artwork background.\n"
            f"Main Concept: {description}\nSub-Style: {substyle or 'Default'}\n"
            f"Theme: {theme}\nMood: {mood}\nArtistic Style: {art_style}\n"
            f"Color Palette: {colors}\nCreativity: {creativity}\n"
            "No text, watermarks or logos in the image."
        )
        neg = "blurry, low quality, distorted, watermarks, text, pixelated, amateur"
        return prompt, neg

    def synthesize_art_canvas(self, poster_type="Event Poster", theme="Technology",
            mood="Energetic", art_style="Cyberpunk",
            colors="Blue + Purple (Cyber/Tech)", creativity="Experimental",
            substyle=None, seed=None, width=768, height=1152, use_topic_preset=True):

        rng = random.Random(seed) if seed is not None else random
        if seed is not None:
            np.random.seed(seed % (2**31 - 1))

        palette = self.color_palettes.get(colors, self.color_palettes["Blue + Purple (Cyber/Tech)"])
        bg_dark, color_mid, color_accent1, color_accent2 = palette

        # Style 1 uses preset image + strong palette recolor
        if use_topic_preset and (substyle is None or "Style 1" in substyle):
            topic_bg = self.get_topic_background(poster_type, width, height)
            if topic_bg is not None:
                img = self._apply_palette_tint(topic_bg, colors)
                if "Dark" in mood or "Mysterious" in mood:
                    img = ImageEnhance.Brightness(img).enhance(0.80)
                elif "Energetic" in mood or "Futuristic" in mood:
                    img = ImageEnhance.Contrast(img).enhance(1.20)
                if seed is not None and seed != 42:
                    img = ImageEnhance.Color(img).enhance(1.0+((seed%10)-5)*0.04)
                return img

        p_lower = poster_type.lower()
        sub_str = str(substyle).lower() if substyle else ""
        cx, cy  = width//2, int(height*0.42)

        img  = self._gradient_bg(width, height, bg_dark, color_mid)
        draw = ImageDraw.Draw(img, "RGBA")

        # Global atmospheric glow
        max_r = int(math.hypot(width,height)*0.68)
        for r in range(max_r, 30, -22):
            t = 1.0 - r/max_r
            col = color_accent1 if r < max_r*0.45 else color_mid
            draw.ellipse([cx-r,cy-r,cx+r,cy+r], fill=(col[0],col[1],col[2],int(70*(t**1.5))))

        # ======= INVITATION CARD =======
        if "invitation" in p_lower:
            if "style 2" in sub_str or "marble" in sub_str or "gold" in sub_str:
                img  = self._gradient_bg(width, height, bg_dark, tuple(min(255,c+20) for c in bg_dark))
                draw = ImageDraw.Draw(img, "RGBA")
                for _ in range(28):
                    x1,y1 = rng.randint(0,width), rng.randint(0,height)
                    draw.line([(x1,y1),(x1+rng.randint(-280,280),y1+rng.randint(80,350))],
                              fill=(color_mid[0],color_mid[1],color_mid[2],rng.randint(28,75)),
                              width=rng.randint(1,3))
                self._radial_glow(draw,cx,cy,360,color_accent1,14,65)
                m=55
                draw.rectangle([m,m,width-m,height-m],
                               outline=(color_accent2[0],color_accent2[1],color_accent2[2],230),width=3)
                draw.rectangle([m+18,m+18,width-m-18,height-m-18],
                               outline=(color_accent1[0],color_accent1[1],color_accent1[2],150),width=1)
                for px,py in [(m,m),(width-m,m),(m,height-m),(width-m,height-m)]:
                    draw.polygon([(px,py-22),(px+22,py),(px,py+22),(px-22,py)],
                                 fill=(color_accent2[0],color_accent2[1],color_accent2[2],200))
            elif "style 3" in sub_str or "tropical" in sub_str or "botanical" in sub_str:
                img  = self._gradient_bg(width, height, bg_dark, color_mid)
                draw = ImageDraw.Draw(img, "RGBA")
                for _ in range(65):
                    lx = rng.choice([rng.randint(0,200), rng.randint(width-200,width)])
                    ly = rng.randint(0,height)
                    rad = rng.randint(35,120)
                    col = rng.choice([color_mid,color_accent1,color_accent2])
                    draw.ellipse([lx-rad,ly-rad*2,lx+rad,ly+rad*2],
                                 fill=(col[0],col[1],col[2],rng.randint(45,130)))
                self._radial_glow(draw,cx,cy,280,color_accent2,14,50)
                draw.rectangle([48,48,width-48,height-48],
                               outline=(color_accent2[0],color_accent2[1],color_accent2[2],190),width=2)
            elif "style 4" in sub_str or "minimalist" in sub_str or "pastel" in sub_str:
                img  = self._gradient_bg(width, height, color_accent2, bg_dark)
                draw = ImageDraw.Draw(img, "RGBA")
                draw.ellipse([width//4,height//5,width*3//4,height*4//5],
                             fill=(color_mid[0],color_mid[1],color_mid[2],90))
                draw.ellipse([width//3,height//4,width*2//3,height*3//4],
                             fill=(color_accent1[0],color_accent1[1],color_accent1[2],60))
                for mg in [65,82]:
                    draw.rectangle([mg,mg,width-mg,height-mg],
                                   outline=(color_accent1[0],color_accent1[1],color_accent1[2],170-mg),width=2)
            else:
                for corner in [(0,0),(width,0),(0,height),(width,height)]:
                    for _ in range(14):
                        pr = rng.randint(30,90)
                        ppx = corner[0]+rng.randint(-90,90)
                        ppy = corner[1]+rng.randint(-90,90)
                        col = rng.choice([color_mid,color_accent1,color_accent2])
                        draw.ellipse([ppx-pr,ppy-pr,ppx+pr,ppy+pr],
                                     fill=(col[0],col[1],col[2],rng.randint(40,100)))
                draw.ellipse([width//4,height//3,width*3//4,height*2//3],
                             fill=(color_accent2[0],color_accent2[1],color_accent2[2],70))

        # ======= MOVIE POSTER =======
        elif "movie" in p_lower:
            if "style 2" in sub_str or "action" in sub_str or "explosion" in sub_str:
                img  = self._gradient_bg(width, height, bg_dark, color_mid)
                draw = ImageDraw.Draw(img, "RGBA")
                ecx,ecy = width//2, int(height*0.55)
                for r in range(500,8,-12):
                    t = 1.0-r/500
                    col = color_accent2 if r<160 else (color_accent1 if r<300 else color_mid)
                    draw.ellipse([ecx-r,ecy-r,ecx+r,ecy+r],fill=(col[0],col[1],col[2],int(240*(t**1.2))))
                for _ in range(120):
                    ex,ey = rng.randint(0,width),rng.randint(80,height-80)
                    er = rng.randint(2,7)
                    draw.ellipse([ex,ey,ex+er,ey+er],
                                 fill=(color_accent1[0],color_accent1[1],color_accent1[2],rng.randint(100,240)))
                for _ in range(18):
                    sx = rng.randint(0,width)
                    draw.line([(sx,0),(sx+rng.randint(-30,30),height)],
                              fill=(color_accent2[0],color_accent2[1],color_accent2[2],40),width=rng.randint(1,3))
            elif "style 3" in sub_str or "thriller" in sub_str or "noir" in sub_str:
                img  = self._gradient_bg(width, height, bg_dark, bg_dark)
                draw = ImageDraw.Draw(img, "RGBA")
                for i in range(8):
                    fy = int(height*(0.28+i*0.07))
                    draw.ellipse([-100,fy,width+100,fy+rng.randint(55,140)],
                                 fill=(color_mid[0],color_mid[1],color_mid[2],rng.randint(16,45)))
                draw.polygon([(cx-65,0),(cx+65,0),(cx+290,height),(cx-290,height)],
                             fill=(color_accent1[0],color_accent1[1],color_accent1[2],28))
                draw.polygon([(cx-22,0),(cx+22,0),(cx+130,height),(cx-130,height)],
                             fill=(color_accent2[0],color_accent2[1],color_accent2[2],50))
                img = img.filter(ImageFilter.GaussianBlur(14))
            elif "style 4" in sub_str or "cyberpunk" in sub_str or "neon sky" in sub_str:
                img  = self._gradient_bg(width, height, bg_dark, color_mid)
                draw = ImageDraw.Draw(img, "RGBA")
                for i in range(0,width,55):
                    bh = rng.randint(int(height*0.3),height)
                    col = rng.choice([color_accent1,color_accent2,color_mid])
                    draw.line([(i,height-bh),(i,height)],
                              fill=(col[0],col[1],col[2],rng.randint(50,130)),width=rng.randint(1,4))
                self._radial_glow(draw,cx,int(height*0.62),260,color_accent2,14,55)
                for y in range(0,height,4):
                    draw.line([(0,y),(width,y)],fill=(color_mid[0],color_mid[1],color_mid[2],12),width=1)
            else:
                self._draw_stars(draw,width,height,160,rng)
                for r in range(320,20,-12):
                    col = rng.choice([color_mid,color_accent1,color_accent2])
                    draw.ellipse([cx-r,cy-r,cx+r,cy+r],
                                 outline=(col[0],col[1],col[2],rng.randint(80,220)),width=rng.randint(1,3))
                self._radial_glow(draw,cx,cy,120,color_accent1,8,100)

        # ======= EVENT POSTER =======
        elif "event" in p_lower:
            if "style 2" in sub_str or "edm" in sub_str or "laser" in sub_str or "music" in sub_str:
                img  = self._gradient_bg(width, height, bg_dark, color_mid)
                draw = ImageDraw.Draw(img, "RGBA")
                sy = int(height*0.42)
                for i in range(-width//2,width+width//2,35):
                    draw.line([(cx,sy),(i,0)],fill=(color_accent2[0],color_accent2[1],color_accent2[2],55),width=rng.randint(1,3))
                for i in range(0,width,40):
                    draw.line([(cx,sy),(i,height)],fill=(color_accent1[0],color_accent1[1],color_accent1[2],70),width=rng.randint(1,3))
                self._radial_glow(draw,cx,sy,160,color_mid,10,90)
                for fy in range(sy+20,height,30):
                    draw.line([(0,fy),(width,fy)],fill=(color_accent1[0],color_accent1[1],color_accent1[2],25),width=2)
            elif "style 3" in sub_str or "hackathon" in sub_str or "grid" in sub_str or "matrix" in sub_str:
                img  = self._gradient_bg(width, height, bg_dark, color_mid)
                draw = ImageDraw.Draw(img, "RGBA")
                self._draw_grid(draw,width,height,color_mid,30,40)
                nodes=[(rng.randint(0,width//30)*30,rng.randint(0,height//30)*30) for _ in range(70)]
                for nx,ny in nodes:
                    draw.ellipse([nx-5,ny-5,nx+5,ny+5],fill=(color_accent2[0],color_accent2[1],color_accent2[2],220))
                for i,(nx1,ny1) in enumerate(nodes):
                    for nx2,ny2 in nodes[i+1:i+4]:
                        if abs(nx1-nx2)<180 and abs(ny1-ny2)<180:
                            draw.line([(nx1,ny1),(nx2,ny2)],fill=(color_accent1[0],color_accent1[1],color_accent1[2],60),width=1)
            elif "style 4" in sub_str or "synthwave" in sub_str or "retro" in sub_str:
                img  = self._gradient_bg(width, height, bg_dark, color_mid)
                draw = ImageDraw.Draw(img, "RGBA")
                hy = int(height*0.5)
                for r in range(180,8,-10):
                    t = 1.0-r/180
                    col = color_accent1 if t<0.5 else color_accent2
                    draw.ellipse([cx-r,hy-r,cx+r,hy+r],fill=(col[0],col[1],col[2],int(200*(t**1.3))))
                for sy2 in range(hy-160,hy,12):
                    draw.line([(0,sy2),(width,sy2)],fill=(bg_dark[0],bg_dark[1],bg_dark[2],180),width=4)
                for i2 in range(-20,22,2):
                    gx = cx+i2*40
                    draw.line([(cx,hy),(gx*2-cx,height)],fill=(color_accent2[0],color_accent2[1],color_accent2[2],80),width=1)
                for fy2 in range(hy+20,height,28):
                    draw.line([(0,fy2),(width,fy2)],fill=(color_accent1[0],color_accent1[1],color_accent1[2],90),width=2)
            else:
                self._draw_grid(draw,width,height,color_mid,40,30)
                for _ in range(12):
                    bw = rng.randint(80,width); by = rng.randint(0,height); bx2 = rng.randint(0,width-bw)
                    draw.rectangle([bx2,by,bx2+bw,by+rng.randint(2,8)],
                                   fill=(color_accent1[0],color_accent1[1],color_accent1[2],rng.randint(30,90)))
                self._radial_glow(draw,cx,cy,300,color_accent2,18,60)

        # ======= ALBUM COVER =======
        elif "album" in p_lower:
            if "style 2" in sub_str or "vinyl" in sub_str or "vintage" in sub_str:
                img  = self._gradient_bg(width, height, bg_dark, color_mid)
                draw = ImageDraw.Draw(img, "RGBA")
                vcx,vcy = width//2,height//2
                for r in range(340,30,-10):
                    t = r/340
                    col = color_accent1 if (r//20)%2==0 else color_mid
                    draw.ellipse([vcx-r,vcy-r,vcx+r,vcy+r],
                                 outline=(col[0],col[1],col[2],int(160*(1-t**0.5))),width=2)
                self._radial_glow(draw,vcx,vcy,70,color_accent2,6,200)
            elif "style 3" in sub_str or "synthwave" in sub_str or "vaporwave" in sub_str or "neon" in sub_str:
                img  = self._gradient_bg(width, height, bg_dark, color_mid)
                draw = ImageDraw.Draw(img, "RGBA")
                self._draw_grid(draw,width,height,color_accent1,40,60)
                self._radial_glow(draw,cx,cy,200,color_accent2,10,120)
                for y in range(0,height,6):
                    draw.line([(0,y),(width,y)],fill=(bg_dark[0],bg_dark[1],bg_dark[2],25),width=1)
                sz=180
                draw.polygon([(0,0),(sz,0),(0,sz)],fill=(color_accent2[0],color_accent2[1],color_accent2[2],70))
                draw.polygon([(width,height),(width-sz,height),(width,height-sz)],fill=(color_accent1[0],color_accent1[1],color_accent1[2],70))
            elif "style 4" in sub_str or "acoustic" in sub_str or "sunbeam" in sub_str:
                img  = self._gradient_bg(width, height, bg_dark, color_mid)
                draw = ImageDraw.Draw(img, "RGBA")
                for angle in range(0,360,15):
                    rad = math.radians(angle)
                    draw.line([(cx,cy),(cx+int(math.cos(rad)*420),cy+int(math.sin(rad)*620))],
                              fill=(color_accent2[0],color_accent2[1],color_accent2[2],22),width=rng.randint(1,5))
                for _ in range(55):
                    bx5,by5 = rng.randint(0,width),rng.randint(0,height)
                    br5 = rng.randint(20,110)
                    col = rng.choice([color_accent1,color_accent2,color_mid])
                    draw.ellipse([bx5-br5,by5-br5,bx5+br5,by5+br5],fill=(col[0],col[1],col[2],rng.randint(18,65)))
                self._radial_glow(draw,cx,cy,250,color_accent1,14,80)
            else:
                self._draw_stars(draw,width,height,100,rng)
                draw.ellipse([cx-90,int(height*0.18)-90,cx+90,int(height*0.18)+90],
                             fill=(color_accent2[0],color_accent2[1],color_accent2[2],220))
                for i in range(0,width,rng.randint(20,45)):
                    bh = rng.randint(80,280); bw2 = rng.randint(18,50)
                    draw.rectangle([i,height-bh,i+bw2,height],
                                   fill=(bg_dark[0]+10,bg_dark[1]+10,bg_dark[2]+10,240))

        # ======= BOOK COVER =======
        elif "book" in p_lower:
            if "style 2" in sub_str or "gothic" in sub_str or "castle" in sub_str:
                img  = self._gradient_bg(width, height, bg_dark, color_mid)
                draw = ImageDraw.Draw(img, "RGBA")
                self._draw_stars(draw,width,height,90,rng)
                self._radial_glow(draw,cx,int(height*0.28),160,color_accent2,12,180)
                castle_y = int(height*0.55)
                for tower in [(cx-160,castle_y,cx-80,height),(cx-80,castle_y+60,cx+80,height),(cx+80,castle_y,cx+160,height)]:
                    draw.rectangle(tower,fill=(bg_dark[0]+5,bg_dark[1]+5,bg_dark[2]+5,240))
                for tx in [cx-160,cx-80,cx+80]:
                    for mx in range(tx,tx+80,16):
                        draw.rectangle([mx,castle_y-20,mx+10,castle_y],fill=(bg_dark[0]+5,bg_dark[1]+5,bg_dark[2]+5,240))
                img = img.filter(ImageFilter.GaussianBlur(3))
            elif "style 3" in sub_str or "space portal" in sub_str or "starfield" in sub_str:
                img  = self._gradient_bg(width, height, bg_dark, color_mid)
                draw = ImageDraw.Draw(img, "RGBA")
                self._draw_stars(draw,width,height,180,rng)
                for r in range(340,20,-14):
                    col = rng.choice([color_mid,color_accent1,color_accent2])
                    draw.ellipse([cx-r,cy-r,cx+r,cy+r],outline=(col[0],col[1],col[2],rng.randint(70,220)),width=rng.randint(1,3))
                self._radial_glow(draw,cx,cy,90,color_accent2,8,180)
            elif "style 4" in sub_str or "ornate" in sub_str or "leather" in sub_str or "gold" in sub_str:
                img  = self._gradient_bg(width, height, bg_dark, color_mid)
                arr  = np.array(img)
                noise = np.random.randint(-18,18,arr.shape,dtype=np.int16)
                arr2 = np.clip(arr.astype(np.int16)+noise,0,255).astype(np.uint8)
                img  = Image.fromarray(arr2)
                draw = ImageDraw.Draw(img, "RGBA")
                for mg in [30,50,68]:
                    draw.rectangle([mg,mg,width-mg,height-mg],
                                   outline=(color_accent2[0],color_accent2[1],color_accent2[2],220-mg*2),
                                   width=3 if mg==30 else 1)
                for cpx,cpy in [(30,30),(width-30,30),(30,height-30),(width-30,height-30)]:
                    for r in range(22,4,-4):
                        t2 = 1-r/22
                        draw.ellipse([cpx-r,cpy-r,cpx+r,cpy+r],
                                     outline=(color_accent1[0],color_accent1[1],color_accent1[2],int(200*t2)))
            else:
                sun_cx,sun_cy = cx, int(height*0.22)
                for angle in range(0,360,10):
                    rad = math.radians(angle)
                    draw.line([(sun_cx,sun_cy),(sun_cx+int(math.cos(rad)*700),sun_cy+int(math.sin(rad)*900))],
                              fill=(color_accent2[0],color_accent2[1],color_accent2[2],18),width=rng.randint(2,8))
                for i in range(0,width,rng.randint(15,35)):
                    th = rng.randint(200,500); tw = rng.randint(12,35)
                    draw.rectangle([i,height-th,i+tw,height],fill=(bg_dark[0]+8,bg_dark[1]+12,bg_dark[2]+8,220))
                self._radial_glow(draw,sun_cx,sun_cy,180,color_accent1,12,70)

        # ======= ADVERTISEMENT =======
        else:
            if "style 2" in sub_str or "audio" in sub_str or "wireless" in sub_str:
                img  = self._gradient_bg(width, height, bg_dark, color_mid)
                draw = ImageDraw.Draw(img, "RGBA")
                pcx,pcy = cx,height//2
                for r in range(300,20,-16):
                    t = 1.0-r/300
                    draw.ellipse([pcx-r,pcy-r,pcx+r,pcy+r],
                                 outline=(color_accent2[0],color_accent2[1],color_accent2[2],int(180*(t**1.5))),width=2)
                for _ in range(60):
                    angle = rng.uniform(0,2*math.pi); dist = rng.randint(160,310)
                    px2 = int(pcx+math.cos(angle)*dist); py2 = int(pcy+math.sin(angle)*dist)
                    pr2 = rng.randint(2,6)
                    draw.ellipse([px2-pr2,py2-pr2,px2+pr2,py2+pr2],
                                 fill=(color_accent1[0],color_accent1[1],color_accent1[2],rng.randint(100,220)))
            elif "style 3" in sub_str or "energy" in sub_str or "splash" in sub_str or "motion" in sub_str:
                img  = self._gradient_bg(width, height, bg_dark, color_mid)
                draw = ImageDraw.Draw(img, "RGBA")
                for _ in range(90):
                    px3,py3 = rng.randint(0,width),rng.randint(80,height-80)
                    pr3 = rng.randint(4,16)
                    col = rng.choice([color_accent1,color_accent2,color_mid])
                    draw.ellipse([px3-pr3,py3-pr3,px3+pr3,py3+pr3],fill=(col[0],col[1],col[2],rng.randint(80,220)))
                for _ in range(35):
                    sx2,sy2 = rng.randint(0,width),rng.randint(0,height)
                    length = rng.randint(40,200); ang = rng.uniform(-0.4,0.4)
                    draw.line([(sx2,sy2),(sx2+int(length*math.cos(ang)),sy2+int(length*math.sin(ang)))],
                              fill=(color_accent2[0],color_accent2[1],color_accent2[2],rng.randint(50,150)),width=rng.randint(1,4))
                self._radial_glow(draw,cx,cy,220,color_accent1,14,55)
            elif "style 4" in sub_str or "glassmorphic" in sub_str or "frosted" in sub_str:
                img  = self._gradient_bg(width, height, bg_dark, color_mid)
                draw = ImageDraw.Draw(img, "RGBA")
                for _ in range(30):
                    bx4,by4 = rng.randint(0,width),rng.randint(0,height)
                    br4 = rng.randint(40,150)
                    col = rng.choice([color_accent1,color_accent2])
                    draw.ellipse([bx4-br4,by4-br4,bx4+br4,by4+br4],fill=(col[0],col[1],col[2],rng.randint(15,45)))
                img  = img.filter(ImageFilter.GaussianBlur(6))
                draw = ImageDraw.Draw(img, "RGBA")
                draw.rounded_rectangle([55,100,width-55,height-100],radius=24,
                    fill=(color_mid[0],color_mid[1],color_mid[2],100),
                    outline=(color_accent2[0],color_accent2[1],color_accent2[2],160),width=2)
                draw.rounded_rectangle([75,108,width-200,160],radius=14,fill=(255,255,255,20))
            else:
                self._draw_grid(draw,width,height,color_mid,45,25)
                draw.ellipse([cx-300,height-280,cx+300,height-60],fill=(color_mid[0],color_mid[1],color_mid[2],90))
                for r in range(280,10,-18):
                    t = 1.0-r/280
                    draw.ellipse([cx-r,cy-r,cx+r,cy+r],
                                 outline=(color_accent2[0],color_accent2[1],color_accent2[2],int(120*(t**1.5))),width=2)
                for y in range(0,height,5):
                    draw.line([(0,y),(width,y)],fill=(color_mid[0],color_mid[1],color_mid[2],15),width=1)

        # Artistic style filters
        if "Watercolor" in art_style:
            img = img.filter(ImageFilter.GaussianBlur(2.5))
            img = img.filter(ImageFilter.SMOOTH_MORE)
        elif "Oil" in art_style:
            img = img.filter(ImageFilter.EDGE_ENHANCE)
            img = img.filter(ImageFilter.SMOOTH)
        elif "Cyberpunk" in art_style or "Digital Art" in art_style:
            img = ImageEnhance.Color(img).enhance(1.35)
            img = ImageEnhance.Contrast(img).enhance(1.18)
        elif "Fantasy" in art_style:
            img = ImageEnhance.Color(img).enhance(1.20)
            img = img.filter(ImageFilter.SMOOTH)
        elif "Minimalist" in art_style:
            img = ImageEnhance.Color(img).enhance(0.70)
            img = ImageEnhance.Contrast(img).enhance(0.90)

        if "Dark" in mood or "Mysterious" in mood:
            img = ImageEnhance.Brightness(img).enhance(0.82)
        elif "Energetic" in mood or "Futuristic" in mood:
            img = ImageEnhance.Contrast(img).enhance(1.12)

        return img
