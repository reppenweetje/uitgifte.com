#!/usr/bin/env python3
"""Build apple-touch-icon.png (180x180) for iOS home screen."""
from PIL import Image, ImageDraw

PAPER = (250, 247, 238)
GOLD = (176, 133, 51)

SIZE = 180
img = Image.new("RGB", (SIZE, SIZE), PAPER)
draw = ImageDraw.Draw(img)

# Three diamonds ◆ • ◆ pattern, REPP DNA
cx = SIZE // 2
cy = SIZE // 2
spacing = 50  # distance between diamond centers
big = 22     # half-side of big diamond
small = 6    # half-side of small middle diamond

# Left diamond
draw.polygon([
    (cx - spacing, cy - big),
    (cx - spacing + big, cy),
    (cx - spacing, cy + big),
    (cx - spacing - big, cy),
], fill=GOLD)

# Middle small diamond
draw.polygon([
    (cx, cy - small),
    (cx + small, cy),
    (cx, cy + small),
    (cx - small, cy),
], fill=GOLD)

# Right diamond
draw.polygon([
    (cx + spacing, cy - big),
    (cx + spacing + big, cy),
    (cx + spacing, cy + big),
    (cx + spacing - big, cy),
], fill=GOLD)

img.save("apple-touch-icon.png", "PNG", optimize=True)
print(f"Wrote apple-touch-icon.png ({SIZE}x{SIZE})")
