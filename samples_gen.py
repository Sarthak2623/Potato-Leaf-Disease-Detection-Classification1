"""
Generate realistic synthetic sample potato leaf images for:
1. Early Blight (Alternaria solani)
2. Late Blight (Phytophthora infestans)
3. Healthy Leaf (Solanum tuberosum)
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def create_base_leaf(size=(400, 400), health_green=(48, 128, 42)):
    """Generate a realistic ovate potato leaflet with veins on a clean neutral background."""
    w, h = size
    img = Image.new("RGB", size, (244, 246, 248))
    draw = ImageDraw.Draw(img)

    # Potato leaflet ovate curve
    cx, cy = w // 2, h // 2
    pts = []
    num_pts = 120
    for i in range(num_pts):
        theta = 2.0 * math.pi * i / num_pts
        # Ovate leaf equation
        r_base = 145.0 * (1.0 - 0.45 * math.sin(theta))
        # Small serrations / waviness
        r_serr = r_base * (1.0 + 0.025 * math.sin(theta * 18.0))
        px = cx + r_serr * math.cos(theta) * 0.72
        py = cy + r_serr * math.sin(theta) * 1.05
        pts.append((px, py))

    # Fill base leaf color
    draw.polygon(pts, fill=health_green)

    # Render fine veins
    arr = np.asarray(img, dtype=np.float32)
    # Add subtle organic noise and texture
    np.random.seed(42)
    noise = np.random.normal(0, 7.0, (h, w, 3))
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    leaf_img = Image.fromarray(arr)
    draw = ImageDraw.Draw(leaf_img)

    # Midrib (central vein)
    draw.line([(cx, cy - 130), (cx, cy + 140)], fill=(80, 160, 60), width=4)
    # Lateral secondary veins
    for y in range(int(cy - 100), int(cy + 110), 30):
        draw.line([(cx, y), (cx - 75, y - 25)], fill=(75, 155, 55), width=2)
        draw.line([(cx, y), (cx + 75, y - 25)], fill=(75, 155, 55), width=2)

    return leaf_img, pts


def generate_healthy_leaf(output_path: str):
    """Generate an immaculate healthy potato leaf."""
    leaf_img, _ = create_base_leaf(size=(400, 400), health_green=(46, 132, 45))
    # Soft leaf highlight
    leaf_img = leaf_img.filter(ImageFilter.SMOOTH_MORE)
    leaf_img.save(output_path, "JPEG", quality=95)
    print(f"Generated healthy sample: {output_path}")


def generate_early_blight_leaf(output_path: str):
    """Generate potato leaf with Early Blight (Alternaria target spots with yellow halos)."""
    leaf_img, _ = create_base_leaf(size=(400, 400), health_green=(52, 126, 48))
    draw = ImageDraw.Draw(leaf_img)

    # Target spot centers
    spots = [
        (160, 170, 36),
        (230, 230, 32),
        (220, 140, 24),
        (150, 270, 28),
        (185, 210, 20),
    ]

    for sx, sy, r in spots:
        # Chlorotic yellow halo
        halo_r = r + 16
        draw.ellipse([sx - halo_r, sy - halo_r, sx + halo_r, sy + halo_r], fill=(188, 175, 38))
        # Concentric brown rings
        for ring_r in range(r, 4, -4):
            ring_color = (88 - ring_r * 2, 48 - ring_r, 22)
            draw.ellipse([sx - ring_r, sy - ring_r, sx + ring_r, sy + ring_r], fill=ring_color)

    # Blur lesions slightly to blend organically with leaf tissue
    leaf_img = leaf_img.filter(ImageFilter.GaussianBlur(radius=1.2))
    leaf_img.save(output_path, "JPEG", quality=95)
    print(f"Generated early blight sample: {output_path}")


def generate_late_blight_leaf(output_path: str):
    """Generate potato leaf with Late Blight (water-soaked dark brown/black lesions spreading from margin)."""
    leaf_img, _ = create_base_leaf(size=(400, 400), health_green=(48, 118, 44))
    draw = ImageDraw.Draw(leaf_img)

    # Water-soaked diffuse pale green/yellow margins
    draw.polygon([(110, 140), (190, 120), (220, 190), (140, 240), (90, 190)], fill=(120, 130, 50))
    # Dark blackish-brown necrotic water-soaked center
    draw.polygon([(120, 150), (180, 130), (205, 185), (135, 225), (100, 185)], fill=(32, 24, 20))

    # Second lesion at leaf tip
    draw.polygon([(180, 70), (220, 70), (235, 115), (170, 110)], fill=(130, 135, 60))
    draw.polygon([(185, 75), (215, 75), (225, 105), (175, 105)], fill=(28, 22, 18))

    # Third lesion at lower margin
    draw.polygon([(220, 260), (275, 250), (285, 310), (210, 300)], fill=(125, 130, 55))
    draw.polygon([(230, 268), (270, 258), (278, 302), (218, 292)], fill=(30, 25, 22))

    leaf_img = leaf_img.filter(ImageFilter.GaussianBlur(radius=1.8))
    leaf_img.save(output_path, "JPEG", quality=95)
    print(f"Generated late blight sample: {output_path}")


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "samples")
    os.makedirs(out_dir, exist_ok=True)
    generate_healthy_leaf(os.path.join(out_dir, "healthy_sample.jpg"))
    generate_early_blight_leaf(os.path.join(out_dir, "early_blight_sample.jpg"))
    generate_late_blight_leaf(os.path.join(out_dir, "late_blight_sample.jpg"))

