#!/usr/bin/env python3
"""Build apple-touch-icon.png (180x180) voor het iOS-beginscherm.

Kavel-mark (vier hoek-brackets) in neon op ink, gelijk aan favicon.svg
en het uitgifte.com brandbook. Ruimere marge dan de favicon zodat de
iOS-afronding van het pictogram de brackets niet aansnijdt.
"""
from PIL import Image, ImageDraw

INK = (13, 27, 42)
NEON = (237, 255, 0)

SIZE = 180
img = Image.new("RGB", (SIZE, SIZE), INK)
draw = ImageDraw.Draw(img)

m0, m1 = 40, 140   # mark-vlak (1.8x de favicon, binnen de iOS-veilige zone)
arm = 34           # armlengte per bracket
h = 7              # halve streekdikte (streek = 14)


def bracket(cx, cy, dx, dy):
    """Eén hoek-bracket: een verticale + horizontale balk die in de
    hoek samenvallen tot een scherpe L. dx/dy geven de richting (+1/-1)."""
    # verticale balk
    vy0, vy1 = cy - dy * h, cy + dy * (arm + h)
    draw.rectangle([cx - h, min(vy0, vy1), cx + h, max(vy0, vy1)], fill=NEON)
    # horizontale balk
    hx0, hx1 = cx - dx * h, cx + dx * (arm + h)
    draw.rectangle([min(hx0, hx1), cy - h, max(hx0, hx1), cy + h], fill=NEON)


bracket(m0, m0, +1, +1)  # linksboven
bracket(m1, m0, -1, +1)  # rechtsboven
bracket(m0, m1, +1, -1)  # linksonder
bracket(m1, m1, -1, -1)  # rechtsonder

img.save("apple-touch-icon.png", "PNG", optimize=True)
print(f"Wrote apple-touch-icon.png ({SIZE}x{SIZE})")
