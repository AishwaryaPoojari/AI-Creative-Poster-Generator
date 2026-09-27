"""
Image Operations and Utility Functions
--------------------------------------
Provides helper functions for image transformations, sample assets creation,
and preview generation.
"""

from PIL import Image, ImageDraw, ImageFilter
import os
import math


def ensure_sample_assets(assets_dir="assets"):
    """Generates sample style and content images if not already present."""
    content_dir = os.path.join(assets_dir, "content")
    style_dir = os.path.join(assets_dir, "styles")
    os.makedirs(content_dir, exist_ok=True)
    os.makedirs(style_dir, exist_ok=True)

    # 1. Sample Content: Campus / City Architecture
    campus_path = os.path.join(content_dir, "campus_building.png")
    if not os.path.exists(campus_path):
        img = Image.new("RGB", (512, 512), (180, 210, 240))
        draw = ImageDraw.Draw(img)
        # Ground
        draw.rectangle([0, 380, 512, 512], fill=(60, 90, 60))
        # Building
        draw.rectangle([100, 180, 412, 380], fill=(220, 215, 200), outline=(80, 80, 90), width=3)
        # Windows
        for row in range(4):
            for col in range(5):
                wx = 130 + col * 55
                wy = 210 + row * 40
                draw.rectangle([wx, wy, wx + 35, wy + 25], fill=(70, 130, 180), outline=(40, 50, 60), width=2)
        # Sun
        draw.ellipse([380, 40, 460, 120], fill=(255, 220, 60))
        img.save(campus_path)

    # 2. Sample Content: Portrait Silhouette
    portrait_path = os.path.join(content_dir, "portrait_silhouette.png")
    if not os.path.exists(portrait_path):
        img = Image.new("RGB", (512, 512), (240, 235, 220))
        draw = ImageDraw.Draw(img)
        # Silhouette
        draw.ellipse([180, 100, 330, 260], fill=(40, 45, 55))
        draw.polygon([(140, 512), (200, 270), (312, 270), (372, 512)], fill=(40, 45, 55))
        img.save(portrait_path)

    # 3. Sample Style: Starry Night (Swirling impressionism)
    starry_path = os.path.join(style_dir, "starry_night_style.png")
    if not os.path.exists(starry_path):
        img = Image.new("RGB", (512, 512), (15, 25, 65))
        draw = ImageDraw.Draw(img)
        # Golden stars & swirling patterns
        for _ in range(40):
            sx = int(math.sin(_) * 200 + 256)
            sy = int(math.cos(_) * 150 + 200)
            draw.ellipse([sx - 15, sy - 15, sx + 15, sy + 15], fill=(255, 215, 0))
            draw.arc([sx - 45, sy - 45, sx + 45, sy + 45], start=0, end=270, fill=(240, 180, 30), width=4)
        for y in range(0, 512, 20):
            draw.line([(0, y), (512, y + 30)], fill=(30, 70, 140), width=8)
        img = img.filter(ImageFilter.GaussianBlur(1))
        img.save(starry_path)

    # 4. Sample Style: Cyberpunk Neon
    cyber_path = os.path.join(style_dir, "cyberpunk_neon_style.png")
    if not os.path.exists(cyber_path):
        img = Image.new("RGB", (512, 512), (10, 5, 25))
        draw = ImageDraw.Draw(img)
        for i in range(0, 512, 35):
            draw.line([(0, i), (512, 512 - i)], fill=(255, 0, 128), width=4)
            draw.line([(i, 0), (512 - i, 512)], fill=(0, 240, 255), width=3)
            draw.ellipse([i, i, i + 60, i + 60], outline=(150, 0, 255), width=3)
        img.save(cyber_path)

    # 5. Sample Style: Cubism / Abstract Geometry (Picasso style)
    cubism_path = os.path.join(style_dir, "cubism_abstract_style.png")
    if not os.path.exists(cubism_path):
        img = Image.new("RGB", (512, 512), (230, 215, 195))
        draw = ImageDraw.Draw(img)
        colors = [(180, 60, 50), (60, 100, 140), (220, 160, 50), (50, 50, 50), (140, 120, 90)]
        for _ in range(25):
            x1, y1 = (_ * 37) % 512, (_ * 53) % 512
            x2, y2 = x1 + 100, y1 + 90
            x3, y3 = x1 + 50, y1 + 140
            draw.polygon([(x1, y1), (x2, y2), (x3, y3)], fill=colors[_ % len(colors)], outline=(30, 30, 30), width=3)
        img.save(cubism_path)

    return content_dir, style_dir
