"""
Poster Composer & Typography Engine
-----------------------------------
Composites exact user-provided textual information, topic-specific atmospheric overlays,
and graphic design elements onto AI-generated artwork using Pillow.
Supports dedicated layout architectures for:
1. Movie Posters (Cinematic titles, billing blocks, taglines)
2. Event Posters / College Fests (Top slogans, badges for workshops/hackathons, event cards)
3. Invitation Cards (Floral borders, cursive/serif calligraphy headers, celebratory copy)
4. Album Covers (Lo-fi / vinyl typography, track subtitling, mood bars)
5. Book Covers (Embossed golden fantasy serif, author banners, bestseller tags)
6. Advertisement Posters (High-impact marketing headlines, product specs & feature pills)
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import os
import math


class PosterComposer:
    def __init__(self):
        # Font directories
        self.font_dir = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts")

    def _get_font(self, size, font_style="sans", bold=False):
        """
        Loads specialized fonts based on layout style:
        - 'sans': Arial / Segoe UI (Tech, Event, Modern)
        - 'serif': Georgia / Times New Roman (Book, Luxury, Fantasy)
        - 'cinema': Impact / Arial Bold (Movie titles, Big Headlines)
        - 'script': Segoe Script / Georgia Italic (Invitations, Lo-fi Album)
        """
        candidates = []
        if font_style == "cinema":
            candidates = ["impact.ttf", "arialbd.ttf", "segoeuib.ttf"]
        elif font_style == "serif":
            candidates = ["georgiab.ttf" if bold else "georgia.ttf", "timesbd.ttf" if bold else "times.ttf"]
        elif font_style == "script":
            candidates = ["segoesc.ttf", "georgiai.ttf", "segoeui.ttf"]
        else:  # 'sans'
            candidates = ["segoeuib.ttf" if bold else "segoeui.ttf", "arialbd.ttf" if bold else "arial.ttf"]

        for fname in candidates:
            path = os.path.join(self.font_dir, fname)
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size)
                except Exception:
                    continue

        return ImageFont.load_default()

    def _wrap_text(self, draw, text, font, max_width):
        """Wraps text into multiple lines fitting within max_width."""
        words = text.split()
        lines = []
        cur_line = []
        for w in words:
            cur_line.append(w)
            test_line = " ".join(cur_line)
            try:
                line_w = draw.textbbox((0, 0), test_line, font=font)[2]
            except Exception:
                line_w = len(test_line) * (font.size if hasattr(font, "size") else 14) * 0.55
            if line_w > max_width:
                cur_line.pop()
                if cur_line:
                    lines.append(" ".join(cur_line))
                cur_line = [w]
        if cur_line:
            lines.append(" ".join(cur_line))
        return lines

    def _draw_text_with_shadow(self, draw, pos, text, font, fill_color, shadow_color=(0, 0, 0, 220), offset=(2, 2)):
        """Draws text with a clean drop shadow."""
        x, y = pos
        ox, oy = offset
        draw.text((x + ox, y + oy), text, fill=shadow_color, font=font)
        draw.text((x, y), text, fill=fill_color, font=font)

    def compose_poster(
        self,
        artwork_img,
        title="TECHFEST 2026",
        poster_type="Event Poster",
        theme="Technology & Innovation",
        description="A tech and innovation festival with workshops, hackathons and fun events.",
        date_str="15 - 17 APR 2026",
        time_str="10:00 AM - 6:00 PM",
        venue_str="Main Auditorium",
        organizer_str="DEPT. OF COMPUTER SCIENCE & AI",
        tagline="SOME SIGNALS ARE NOT MEANT TO BE FOUND",
        subtext="A FESTIVAL OF IDEAS, TECHNOLOGY & YOU",
        accent_color=(56, 189, 248),
        extra_badges=None,
    ):
        """Master compositor: delegates to specialized layout renderer based on poster_type."""
        p_type_lower = poster_type.lower()

        if "movie" in p_type_lower:
            return self.compose_movie_poster(
                artwork_img=artwork_img,
                title=title,
                tagline=tagline or "SOME SIGNALS ARE NOT MEANT TO BE FOUND",
                description=description,
                date_str=date_str,
                accent_color=accent_color,
            )
        elif "invitation" in p_type_lower:
            return self.compose_invitation_card(
                artwork_img=artwork_img,
                title=title,
                subtitle=subtext or "Sarah's 21st Birthday",
                description=description or "Join us to celebrate 21 years of awesomeness!",
                date_str=date_str or "15th March 2026",
                time_str=time_str or "6:00 PM",
                venue_str=venue_str or "The Grand Banquet Hall",
                footer_str=organizer_str or "Food • Music • Fun",
            )
        elif "album" in p_type_lower:
            return self.compose_album_cover(
                artwork_img=artwork_img,
                title=title or "Midnight",
                subtitle=subtext or "LO-FI",
                description=description,
                footer_bar=tagline or "DREAMS • CHILL • REPEAT",
                accent_color=accent_color,
            )
        elif "book" in p_type_lower:
            return self.compose_book_cover(
                artwork_img=artwork_img,
                title=title or "THE FORGOTTEN FOREST",
                author_str=organizer_str or "A NOVEL BY E. R. VANCE",
                tagline=tagline or "SOME PLACES SHOULD STAY HIDDEN",
                genre_str=theme or "FANTASY NOVEL",
            )
        elif "ad" in p_type_lower or "commercial" in p_type_lower or "product" in p_type_lower:
            return self.compose_ad_poster(
                artwork_img=artwork_img,
                headline=title or "SMARTER TODAY BRIGHTER TOMORROW",
                tagline=tagline or "Track • Connect • Achieve",
                product_name=organizer_str or "NEXA Smart Watch",
                description=description,
                accent_color=accent_color,
            )
        else:
            # Default / Event Poster
            return self.compose_event_poster(
                artwork_img=artwork_img,
                title=title,
                theme=theme,
                description=description,
                date_str=date_str,
                venue_str=venue_str,
                organizer_str=organizer_str,
                accent_color=accent_color,
            )

    # ----------------------------------------------------------------------------------
    # 1. MOVIE POSTER LAYOUT
    # ----------------------------------------------------------------------------------
    def compose_movie_poster(self, artwork_img, title, tagline, description, date_str, accent_color=(60, 220, 255)):
        w, h = 768, 1152
        base = artwork_img.convert("RGB").resize((w, h), Image.Resampling.LANCZOS)
        
        # Vignette overlay (dark at top and bottom for readability)
        overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw_ov = ImageDraw.Draw(overlay)
        # Top gradient
        for y in range(int(h * 0.3)):
            a = int(220 * (1.0 - (y / (h * 0.3))) ** 1.5)
            draw_ov.line([(0, y), (w, y)], fill=(5, 10, 20, a))
        # Bottom gradient
        bottom_start = int(h * 0.65)
        for y in range(bottom_start, h):
            prog = (y - bottom_start) / (h - bottom_start)
            a = int(240 * (prog ** 1.2))
            draw_ov.line([(0, y), (w, y)], fill=(5, 10, 20, a))

        poster = Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGBA")
        draw = ImageDraw.Draw(poster)

        # Fonts
        lead_font = self._get_font(20, "sans", bold=True)
        title_font = self._get_font(52, "cinema", bold=True)
        tagline_font = self._get_font(18, "sans", bold=True)
        billing_font = self._get_font(13, "sans", bold=False)
        date_font = self._get_font(22, "sans", bold=True)

        # 1. Top Cinematic Header
        top_text = "THE"
        bbox = draw.textbbox((0, 0), top_text, font=lead_font)
        draw.text(((w - (bbox[2] - bbox[0])) // 2, 130), top_text, fill=(200, 230, 255, 230), font=lead_font)

        # 2. Main Title (Placed in upper-middle area like in classic sci-fi posters)
        title_clean = title.replace("THE ", "").replace("The ", "").strip().upper()
        lines = self._wrap_text(draw, title_clean, title_font, w - 80)
        title_y = 165
        for line in lines[:2]:
            bbox = draw.textbbox((0, 0), line, font=title_font)
            tx = (w - (bbox[2] - bbox[0])) // 2
            self._draw_text_with_shadow(draw, (tx, title_y), line, title_font, (255, 255, 255, 255), shadow_color=(0, 0, 0, 240), offset=(3, 3))
            title_y += 60

        # 3. Bottom Tagline
        tagline_clean = tagline.strip().upper()
        bbox = draw.textbbox((0, 0), tagline_clean, font=tagline_font)
        draw.text(((w - (bbox[2] - bbox[0])) // 2, h - 140), tagline_clean, fill=(180, 210, 240, 240), font=tagline_font)

        # 4. Cinematic Release Date / Billing
        date_text = date_str.upper() if date_str else "IN CINEMAS WORLDWIDE • 2026"
        bbox = draw.textbbox((0, 0), date_text, font=date_font)
        draw.text(((w - (bbox[2] - bbox[0])) // 2, h - 95), date_text, fill=(255, 255, 255, 255), font=date_font)

        # Cinematic small credits line
        credit_line = "WRITTEN & DIRECTED BY GENERATIVE AI • CINEMATOGRAPHY BY NEURAL DIFFUSION"
        bbox = draw.textbbox((0, 0), credit_line, font=billing_font)
        draw.text(((w - (bbox[2] - bbox[0])) // 2, h - 50), credit_line, fill=(130, 150, 175, 180), font=billing_font)

        return poster.convert("RGB")

    # ----------------------------------------------------------------------------------
    # 2. EVENT POSTER (COLLEGE FEST) LAYOUT
    # ----------------------------------------------------------------------------------
    def compose_event_poster(self, artwork_img, title, theme, description, date_str, venue_str, organizer_str, accent_color=(0, 240, 255)):
        w, h = 768, 1152
        base = artwork_img.convert("RGB").resize((w, h), Image.Resampling.LANCZOS)

        overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw_ov = ImageDraw.Draw(overlay)
        # Top banner shade
        for y in range(int(h * 0.38)):
            a = int(230 * (1.0 - (y / (h * 0.38))) ** 1.3)
            draw_ov.line([(0, y), (w, y)], fill=(15, 10, 30, a))
        # Bottom details shade
        bottom_start = int(h * 0.68)
        for y in range(bottom_start, h):
            prog = (y - bottom_start) / (h - bottom_start)
            a = int(245 * (prog ** 1.1))
            draw_ov.line([(0, y), (w, y)], fill=(10, 8, 25, a))

        poster = Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGBA")
        draw = ImageDraw.Draw(poster)

        # Fonts
        slogan_font = self._get_font(17, "sans", bold=True)
        title_font = self._get_font(52, "sans", bold=True)
        sub_font = self._get_font(18, "sans", bold=True)
        badge_font = self._get_font(15, "sans", bold=True)
        detail_font = self._get_font(16, "sans", bold=False)

        # 1. Top Slogan Pill
        slogan_text = "INNOVATE  •  CREATE  •  INSPIRE"
        bbox = draw.textbbox((0, 0), slogan_text, font=slogan_font)
        draw.text(((w - (bbox[2] - bbox[0])) // 2, 70), slogan_text, fill=(200, 230, 255, 220), font=slogan_font)

        # 2. Main Fest Title (Bold Neon)
        title_clean = title.strip().upper()
        lines = self._wrap_text(draw, title_clean, title_font, w - 80)
        ty = 110
        for line in lines[:2]:
            bbox = draw.textbbox((0, 0), line, font=title_font)
            tx = (w - (bbox[2] - bbox[0])) // 2
            # Cyan/Magenta Glow shadow
            draw.text((tx + 2, ty + 2), line, fill=(0, 200, 255, 180), font=title_font)
            draw.text((tx - 2, ty - 2), line, fill=(255, 0, 128, 180), font=title_font)
            draw.text((tx, ty), line, fill=(255, 255, 255, 255), font=title_font)
            ty += 60

        # Subtitle
        sub_text = "A FESTIVAL OF IDEAS, TECHNOLOGY & YOU"
        bbox = draw.textbbox((0, 0), sub_text, font=sub_font)
        draw.text(((w - (bbox[2] - bbox[0])) // 2, ty + 10), sub_text, fill=(180, 210, 255, 220), font=sub_font)

        # 3. Feature Badges (Workshops, Hackathon, Fun Events)
        badges = ["⚡ WORKSHOPS", "💻 HACKATHON", "🎉 FUN EVENTS"]
        badge_y = h - 170
        badge_w = (w - 120) // 3
        for i, b_text in enumerate(badges):
            bx = 40 + i * (badge_w + 20)
            draw.rounded_rectangle([bx, badge_y, bx + badge_w, badge_y + 45], radius=10, fill=(30, 20, 55, 200), outline=(130, 0, 255, 180), width=1)
            bbox = draw.textbbox((0, 0), b_text, font=badge_font)
            draw.text((bx + (badge_w - (bbox[2] - bbox[0])) // 2, badge_y + 13), b_text, fill=(255, 255, 255, 240), font=badge_font)

        # 4. Date & Venue Bar at Bottom
        bot_y = h - 90
        info_text = f"📅 {date_str or '15 - 17 APR 2026'}   •   📍 {venue_str or 'Main Auditorium'}"
        bbox = draw.textbbox((0, 0), info_text, font=detail_font)
        draw.text(((w - (bbox[2] - bbox[0])) // 2, bot_y), info_text, fill=(200, 225, 255, 240), font=detail_font)

        return poster.convert("RGB")

    # ----------------------------------------------------------------------------------
    # 3. INVITATION CARD (FLORAL & BIRTHDAY / WEDDING)
    # ----------------------------------------------------------------------------------
    def compose_invitation_card(self, artwork_img, title, subtitle, description, date_str, time_str, venue_str, footer_str):
        w, h = 768, 1152
        base = artwork_img.convert("RGB").resize((w, h), Image.Resampling.LANCZOS)
        poster = base.convert("RGBA")
        draw = ImageDraw.Draw(poster)

        # Fonts
        top_font = self._get_font(18, "sans", bold=True)
        name_font = self._get_font(44, "script", bold=True)
        sub_font = self._get_font(22, "sans", bold=False)
        detail_font = self._get_font(17, "sans", bold=False)
        badge_font = self._get_font(16, "sans", bold=True)

        center_y = h // 2

        # 1. Top invitation greeting
        top_text = "YOU ARE INVITED TO"
        bbox = draw.textbbox((0, 0), top_text, font=top_font)
        draw.text(((w - (bbox[2] - bbox[0])) // 2, center_y - 220), top_text, fill=(140, 110, 120, 220), font=top_font)

        # 2. Celebration Title (E.g. Sarah's 21st Birthday in elegant cursive/rose tint)
        title_clean = title or "Sarah's 21st Birthday"
        lines = self._wrap_text(draw, title_clean, name_font, w - 160)
        ty = center_y - 170
        for line in lines[:2]:
            bbox = draw.textbbox((0, 0), line, font=name_font)
            tx = (w - (bbox[2] - bbox[0])) // 2
            # Rose / burgundy color
            draw.text((tx, ty), line, fill=(185, 60, 95, 255), font=name_font)
            ty += 54

        # Decorative floral divider line
        div_w = 120
        draw.line([((w - div_w) // 2, ty + 8), ((w + div_w) // 2, ty + 8)], fill=(200, 140, 160, 180), width=2)

        # 3. Message / Description
        desc_text = description or "Join us to celebrate 21 years of awesomeness!"
        d_lines = self._wrap_text(draw, desc_text, sub_font, w - 180)
        dy = ty + 28
        for dline in d_lines[:2]:
            bbox = draw.textbbox((0, 0), dline, font=sub_font)
            draw.text(((w - (bbox[2] - bbox[0])) // 2, dy), dline, fill=(90, 80, 85, 230), font=sub_font)
            dy += 30

        # 4. Event Details Card (Date, Time, Venue)
        card_y = dy + 35
        card_h = 135
        card_w = w - 200
        cx = 100
        draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + card_h], radius=16, fill=(255, 255, 255, 170), outline=(220, 180, 195, 180), width=1)

        # Details
        d_items = [
            f"📅  {date_str or '15th March 2026'}",
            f"⏰  {time_str or '6:00 PM'}",
            f"📍  {venue_str or 'The Grand Banquet Hall'}",
        ]
        item_y = card_y + 18
        for it in d_items:
            bbox = draw.textbbox((0, 0), it, font=detail_font)
            draw.text(((w - (bbox[2] - bbox[0])) // 2, item_y), it, fill=(70, 60, 65, 240), font=detail_font)
            item_y += 34

        # 5. Footer (Food • Music • Fun)
        foot_text = footer_str or "Food  •  Music  •  Fun"
        bbox = draw.textbbox((0, 0), foot_text, font=badge_font)
        draw.text(((w - (bbox[2] - bbox[0])) // 2, card_y + card_h + 30), foot_text, fill=(160, 100, 120, 220), font=badge_font)

        return poster.convert("RGB")

    # ----------------------------------------------------------------------------------
    # 4. ALBUM COVER (LO-FI / VINYL)
    # ----------------------------------------------------------------------------------
    def compose_album_cover(self, artwork_img, title, subtitle, description, footer_bar, accent_color=(190, 140, 255)):
        w, h = 768, 1152
        base = artwork_img.convert("RGB").resize((w, h), Image.Resampling.LANCZOS)

        overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw_ov = ImageDraw.Draw(overlay)
        # Top gradient
        for y in range(int(h * 0.25)):
            a = int(180 * (1.0 - (y / (h * 0.25))) ** 1.3)
            draw_ov.line([(0, y), (w, y)], fill=(10, 15, 30, a))
        # Bottom gradient
        b_start = int(h * 0.72)
        for y in range(b_start, h):
            prog = (y - b_start) / (h - b_start)
            a = int(230 * (prog ** 1.2))
            draw_ov.line([(0, y), (w, y)], fill=(10, 10, 25, a))

        poster = Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGBA")
        draw = ImageDraw.Draw(poster)

        # Fonts
        title_font = self._get_font(56, "script", bold=True)
        sub_font = self._get_font(20, "sans", bold=True)
        pill_font = self._get_font(16, "sans", bold=True)

        # 1. Main Album Title (placed on upper sky area)
        title_clean = title or "Midnight"
        bbox = draw.textbbox((0, 0), title_clean, font=title_font)
        tx = (w - (bbox[2] - bbox[0])) // 2
        ty = 130
        self._draw_text_with_shadow(draw, (tx, ty), title_clean, title_font, (255, 255, 255, 255), shadow_color=(0, 0, 0, 220), offset=(3, 3))

        # 2. Genre Tag
        sub_clean = subtitle or "LO - FI"
        bbox = draw.textbbox((0, 0), sub_clean, font=sub_font)
        draw.text(((w - (bbox[2] - bbox[0])) // 2, ty + 70), sub_clean, fill=(220, 200, 255, 220), font=sub_font)

        # 3. Bottom Pill Bar (DREAMS • CHILL • REPEAT)
        pill_text = footer_bar or "DREAMS  •  CHILL  •  REPEAT"
        bbox = draw.textbbox((0, 0), pill_text, font=pill_font)
        pw, ph = bbox[2] - bbox[0], bbox[3] - bbox[1]
        px = (w - pw) // 2
        py = h - 110

        draw.rounded_rectangle([px - 25, py - 10, px + pw + 25, py + ph + 10], radius=14, fill=(20, 15, 35, 210), outline=(200, 150, 255, 150), width=1)
        draw.text((px, py), pill_text, fill=(240, 225, 255, 240), font=pill_font)

        return poster.convert("RGB")

    # ----------------------------------------------------------------------------------
    # 5. BOOK COVER (FANTASY NOVEL)
    # ----------------------------------------------------------------------------------
    def compose_book_cover(self, artwork_img, title, author_str, tagline, genre_str):
        w, h = 768, 1152
        base = artwork_img.convert("RGB").resize((w, h), Image.Resampling.LANCZOS)

        overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw_ov = ImageDraw.Draw(overlay)
        # Top gradient for author & title
        for y in range(int(h * 0.32)):
            a = int(220 * (1.0 - (y / (h * 0.32))) ** 1.4)
            draw_ov.line([(0, y), (w, y)], fill=(10, 20, 15, a))
        # Bottom gradient for tagline
        b_start = int(h * 0.75)
        for y in range(b_start, h):
            prog = (y - b_start) / (h - b_start)
            a = int(240 * (prog ** 1.3))
            draw_ov.line([(0, y), (w, y)], fill=(5, 15, 10, a))

        poster = Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGBA")
        draw = ImageDraw.Draw(poster)

        # Fonts
        author_font = self._get_font(18, "sans", bold=True)
        title_font = self._get_font(48, "serif", bold=True)
        tag_font = self._get_font(17, "serif", bold=True)

        # 1. Author Top Header
        auth_text = author_str or "A NOVEL BY E. R. VANCE"
        bbox = draw.textbbox((0, 0), auth_text, font=author_font)
        draw.text(((w - (bbox[2] - bbox[0])) // 2, 75), auth_text, fill=(220, 200, 140, 230), font=author_font)

        # 2. Main Title (Embossed Gold Serif in Upper Canopy)
        title_clean = title or "THE FORGOTTEN FOREST"
        lines = self._wrap_text(draw, title_clean.upper(), title_font, w - 100)
        ty = 120
        for line in lines[:2]:
            bbox = draw.textbbox((0, 0), line, font=title_font)
            tx = (w - (bbox[2] - bbox[0])) // 2
            # Gold shadow and glow
            draw.text((tx + 2, ty + 2), line, fill=(20, 30, 20, 240), font=title_font)
            draw.text((tx, ty), line, fill=(245, 205, 110, 255), font=title_font)
            ty += 56

        # 3. Bottom Mystery Tagline
        tag_text = tagline or "SOME PLACES SHOULD STAY HIDDEN"
        bbox = draw.textbbox((0, 0), tag_text.upper(), font=tag_font)
        draw.text(((w - (bbox[2] - bbox[0])) // 2, h - 90), tag_text.upper(), fill=(230, 215, 160, 240), font=tag_font)

        return poster.convert("RGB")

    # ----------------------------------------------------------------------------------
    # 6. ADVERTISEMENT POSTER (SMARTWATCH / PRODUCT AD)
    # ----------------------------------------------------------------------------------
    def compose_ad_poster(self, artwork_img, headline, tagline, product_name, description, accent_color=(0, 240, 255)):
        w, h = 768, 1152
        base = artwork_img.convert("RGB").resize((w, h), Image.Resampling.LANCZOS)

        overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw_ov = ImageDraw.Draw(overlay)
        # Top gradient for headline
        for y in range(int(h * 0.28)):
            a = int(230 * (1.0 - (y / (h * 0.28))) ** 1.3)
            draw_ov.line([(0, y), (w, y)], fill=(8, 12, 18, a))
        # Bottom gradient for specs and branding
        b_start = int(h * 0.70)
        for y in range(b_start, h):
            prog = (y - b_start) / (h - b_start)
            a = int(245 * (prog ** 1.2))
            draw_ov.line([(0, y), (w, y)], fill=(5, 10, 15, a))

        poster = Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGBA")
        draw = ImageDraw.Draw(poster)

        # Fonts
        head_font = self._get_font(40, "sans", bold=True)
        tag_font = self._get_font(18, "sans", bold=False)
        spec_font = self._get_font(14, "sans", bold=True)
        brand_font = self._get_font(28, "sans", bold=True)
        sub_brand_font = self._get_font(15, "sans", bold=False)

        # 1. Top High-Impact Headline
        hl_clean = headline or "SMARTER TODAY\nBRIGHTER TOMORROW"
        lines = hl_clean.split("\n") if "\n" in hl_clean else self._wrap_text(draw, hl_clean.upper(), head_font, w - 80)
        ty = 65
        for line in lines[:2]:
            bbox = draw.textbbox((0, 0), line.strip(), font=head_font)
            tx = (w - (bbox[2] - bbox[0])) // 2
            self._draw_text_with_shadow(draw, (tx, ty), line.strip(), head_font, (255, 255, 255, 255), shadow_color=(0, 0, 0, 200))
            ty += 48

        # Tagline
        tag_clean = tagline or "Track  •  Connect  •  Achieve"
        bbox = draw.textbbox((0, 0), tag_clean, font=tag_font)
        draw.text(((w - (bbox[2] - bbox[0])) // 2, ty + 10), tag_clean, fill=(160, 215, 245, 230), font=tag_font)

        # 2. Product Specs (Health Tracking, 14-Day Battery, Water Resistant)
        specs = ["❤️ HEALTH TRACKING", "🔋 14-DAY BATTERY", "💧 WATER RESISTANT"]
        spec_y = h - 170
        spec_w = (w - 100) // 3
        for i, sp in enumerate(specs):
            sx = 35 + i * (spec_w + 15)
            draw.rounded_rectangle([sx, spec_y, sx + spec_w, spec_y + 40], radius=8, fill=(15, 25, 35, 190), outline=(0, 220, 255, 120), width=1)
            bbox = draw.textbbox((0, 0), sp, font=spec_font)
            draw.text((sx + (spec_w - (bbox[2] - bbox[0])) // 2, spec_y + 12), sp, fill=(220, 240, 255, 240), font=spec_font)

        # 3. Bottom Brand Name
        b_name = product_name or "NEXA"
        bbox = draw.textbbox((0, 0), b_name.upper(), font=brand_font)
        draw.text(((w - (bbox[2] - bbox[0])) // 2, h - 100), b_name.upper(), fill=(255, 255, 255, 255), font=brand_font)

        b_sub = "Smart Watch — Evolve Your Life"
        bbox = draw.textbbox((0, 0), b_sub, font=sub_brand_font)
        draw.text(((w - (bbox[2] - bbox[0])) // 2, h - 60), b_sub, fill=(140, 175, 200, 220), font=sub_brand_font)

        return poster.convert("RGB")
