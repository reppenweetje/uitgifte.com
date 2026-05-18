#!/usr/bin/env python3
"""Build og-image.png (1200x630) for uitgifte.com social previews.

Run from the uitgifte-landing/ directory:
    python3 build-og.py
"""
from PIL import Image, ImageDraw, ImageFont

# --- Brand tokens ---
PAPER = (250, 247, 238)        # #faf7ee
PAPER_SOFT = (241, 236, 224)   # #f1ece0
INK = (28, 26, 23)             # #1c1a17
INK_SOFT = (82, 77, 69)        # #524d45
INK_DIM = (160, 154, 144)      # #a09a90
LINE = (226, 220, 202)         # #e2dcca
GOLD = (176, 133, 51)          # #b08533
GOLD_SOFT = (176, 133, 51, 26) # 10% alpha
GOLD_MID = (176, 133, 51, 96)  # 38% alpha

W, H = 1200, 630

# Use HelveticaNeue.ttc on macOS — multiple weights via index
FONT_PATH = "/System/Library/Fonts/HelveticaNeue.ttc"

# Indices in HelveticaNeue.ttc (typical):
# 0=Regular, 1=Italic, 2=Bold, 3=Bold Italic, 4=Light, 5=Light Italic,
# 6=UltraLight, 7=UltraLight Italic, 8=Thin, 9=Thin Italic, 10=Medium

def font(size, weight="regular"):
    idx_map = {
        "ultralight": 6,
        "thin": 8,
        "light": 4,
        "regular": 0,
        "medium": 10,
        "bold": 2,
    }
    return ImageFont.truetype(FONT_PATH, size, index=idx_map.get(weight, 0))


# --- Canvas ---
img = Image.new("RGB", (W, H), PAPER)
draw = ImageDraw.Draw(img, "RGBA")

# Subtle dot grid background (light, every 36px)
for y in range(0, H, 36):
    for x in range(0, W, 36):
        draw.ellipse((x, y, x + 1.5, y + 1.5), fill=(28, 26, 23, 8))

# --- Frame padding ---
PAD_X = 80
PAD_Y = 72

# --- Top wordmark: UITGIFTE ◆ COM ---
wm_font = font(20, "medium")
text_uitgifte = "UITGIFTE"
text_com = "COM"
draw.text((PAD_X, PAD_Y), text_uitgifte, font=wm_font, fill=INK,
          stroke_width=0)
# spacing for tracking
uitgifte_bbox = draw.textbbox((PAD_X, PAD_Y), text_uitgifte, font=wm_font)
gap = 16
dot_x = uitgifte_bbox[2] + gap
dot_y = PAD_Y + 7
# Gold diamond (4x4 rotated 45)
diamond = [(dot_x + 5, dot_y), (dot_x + 10, dot_y + 5),
           (dot_x + 5, dot_y + 10), (dot_x, dot_y + 5)]
draw.polygon(diamond, fill=GOLD)
com_x = dot_x + 10 + gap
draw.text((com_x, PAD_Y), text_com, font=wm_font, fill=INK)

# Letter-spacing simulation via separate characters
# (PIL doesn't do letter-spacing natively — Helvetica Neue Medium gives a clean default)

# Top-right: INFO@REPP.NL
contact_text = "INFO@REPP.NL"
contact_font = font(16, "medium")
contact_bbox = draw.textbbox((0, 0), contact_text, font=contact_font)
contact_w = contact_bbox[2] - contact_bbox[0]
draw.text((W - PAD_X - contact_w, PAD_Y + 2), contact_text,
          font=contact_font, fill=INK_DIM)

# --- Hero block (left half) ---
HERO_X = PAD_X
HERO_Y = 165

# Didam-proof pill (gold border, transparent fill)
pill_text = "DIDAM-PROOF OPGEBOUWD & INGERICHT"
pill_font = font(16, "medium")
pill_text_bbox = draw.textbbox((0, 0), pill_text, font=pill_font)
pill_text_w = pill_text_bbox[2] - pill_text_bbox[0]
pill_h = 36
pill_pad_x = 22
pill_w = pill_text_w + pill_pad_x * 2 + 22  # extra for checkmark+gap
pill_x = HERO_X
pill_y = HERO_Y
# Pill outline (1px gold border, rounded)
draw.rounded_rectangle(
    (pill_x, pill_y, pill_x + pill_w, pill_y + pill_h),
    radius=pill_h // 2,
    outline=GOLD, width=1
)
# Checkmark (V) in gold inside pill
check_x = pill_x + pill_pad_x
check_y = pill_y + pill_h // 2
draw.line([(check_x, check_y), (check_x + 5, check_y + 5),
           (check_x + 12, check_y - 6)],
          fill=GOLD, width=2)
# Pill text
draw.text((check_x + 20, pill_y + (pill_h - 18) // 2 + 1),
          pill_text, font=pill_font, fill=GOLD)

# Pillars eyebrow under pill
pillars_y = HERO_Y + pill_h + 22
pillars_font = font(13, "medium")
pillars_text = "PROCESBORGING   •   TRANSPARANTIE   •   GELIJKE INFORMATIE   •   DOSSIERVORMING"
draw.text((HERO_X, pillars_y), pillars_text,
          font=pillars_font, fill=INK_DIM)

# Headline (light weight, large)
headline_y = pillars_y + 24
headline_font = font(50, "light")
# Three lines for impact — kept short to avoid overlap with kavelgrid
headline_lines = [
    "Digitale",
    "infrastructuur voor",
    "transparante uitgiftes.",
]
line_h = 60
for i, line in enumerate(headline_lines):
    is_last = (i == len(headline_lines) - 1)
    if is_last:
        # Render line with gold period
        line_no_dot = line[:-1]
        draw.text((HERO_X, headline_y + i * line_h),
                  line_no_dot, font=headline_font, fill=INK)
        no_dot_bbox = draw.textbbox(
            (HERO_X, headline_y + i * line_h),
            line_no_dot, font=headline_font)
        draw.text((no_dot_bbox[2], headline_y + i * line_h),
                  ".", font=headline_font, fill=GOLD)
    else:
        draw.text((HERO_X, headline_y + i * line_h),
                  line, font=headline_font, fill=INK)

# --- Right side: abstract kavelgrid ---
GRID_X = 760
GRID_Y = 175
GRID_W = 360
GRID_H = 300

# Outer frame
draw.rectangle((GRID_X, GRID_Y, GRID_X + GRID_W, GRID_Y + GRID_H),
               outline=LINE, width=1)

# Corner ticks
tick_len = 8
for cx, cy in [(GRID_X, GRID_Y), (GRID_X + GRID_W, GRID_Y),
               (GRID_X, GRID_Y + GRID_H), (GRID_X + GRID_W, GRID_Y + GRID_H)]:
    draw.line((cx - tick_len, cy, cx + tick_len, cy), fill=INK_DIM, width=1)
    draw.line((cx, cy - tick_len, cx, cy + tick_len), fill=INK_DIM, width=1)

# Internal grid: 3 cols x 3 rows of varying sizes
col_xs = [GRID_X + 16, GRID_X + 100, GRID_X + 192, GRID_X + GRID_W - 16]
row_ys = [GRID_Y + 16, GRID_Y + 100, GRID_Y + 200, GRID_Y + GRID_H - 16]

# Kavels: (col_start, row_start, col_end, row_end, style)
kavels = [
    (0, 0, 1, 1, "line"),
    (1, 0, 2, 1, "gold-line"),
    (2, 0, 3, 1, "line"),
    (0, 1, 2, 2, "highlight"),  # KAVEL 04
    (2, 1, 3, 2, "gold-line"),
    (0, 2, 1, 3, "line"),
    (1, 2, 2, 3, "line"),
    (2, 2, 3, 3, "line"),
]

for col_s, row_s, col_e, row_e, style in kavels:
    x1, y1 = col_xs[col_s], row_ys[row_s]
    x2, y2 = col_xs[col_e], row_ys[row_e]
    if style == "highlight":
        # gold-soft fill + gold border
        draw.rectangle((x1, y1, x2, y2),
                       fill=(176, 133, 51, 28), outline=GOLD, width=1)
    elif style == "gold-line":
        draw.rectangle((x1, y1, x2, y2),
                       outline=(176, 133, 51, 105), width=1)
    else:
        draw.rectangle((x1, y1, x2, y2), outline=LINE, width=1)

# KAVEL 04 label inside highlighted kavel
label_font = font(11, "bold")
label_dim_font = font(10, "medium")
draw.text((col_xs[0] + 12, row_ys[1] + 14),
          "KAVEL 04", font=label_font, fill=GOLD)
draw.text((col_xs[0] + 12, row_ys[1] + 32),
          "1.240 m²", font=label_dim_font, fill=INK_DIM)
draw.text((col_xs[0] + 12, row_ys[1] + 48),
          "BESCHIKBAAR", font=label_dim_font, fill=INK_DIM)

# Scale indicator below grid
scale_y = GRID_Y + GRID_H + 20
draw.line((GRID_X, scale_y, GRID_X + 60, scale_y), fill=INK_DIM, width=1)
draw.line((GRID_X, scale_y - 3, GRID_X, scale_y + 3), fill=INK_DIM, width=1)
draw.line((GRID_X + 60, scale_y - 3, GRID_X + 60, scale_y + 3),
          fill=INK_DIM, width=1)
draw.text((GRID_X + 70, scale_y - 8), "20 M",
          font=font(10, "medium"), fill=INK_DIM)

# --- Footer hairline + text ---
footer_y = H - PAD_Y - 6
draw.line((PAD_X, footer_y - 24, W - PAD_X, footer_y - 24),
          fill=(176, 133, 51, 96), width=1)

footer_font = font(14, "medium")
# Gold diamond before "Een initiatief van REPP"
fd_x = PAD_X
fd_y = footer_y - 4
fd_size = 3
diamond_f = [(fd_x + fd_size, fd_y), (fd_x + fd_size * 2, fd_y + fd_size),
             (fd_x + fd_size, fd_y + fd_size * 2), (fd_x, fd_y + fd_size)]
draw.polygon(diamond_f, fill=GOLD)
draw.text((PAD_X + 16, footer_y - 14),
          "EEN INITIATIEF VAN REPP", font=footer_font, fill=INK_DIM)

# REPP.NL right
repp_text = "REPP.NL"
repp_bbox = draw.textbbox((0, 0), repp_text, font=footer_font)
repp_w = repp_bbox[2] - repp_bbox[0]
draw.text((W - PAD_X - repp_w - 18, footer_y - 14),
          repp_text, font=footer_font, fill=INK_DIM)
# Arrow up-right after repp.nl
ax = W - PAD_X - 16
ay = footer_y - 8
draw.line((ax, ay, ax + 8, ay - 8), fill=INK_DIM, width=1)
draw.line((ax + 8, ay - 8, ax + 2, ay - 8), fill=INK_DIM, width=1)
draw.line((ax + 8, ay - 8, ax + 8, ay - 2), fill=INK_DIM, width=1)

# Save
img.save("og-image.png", "PNG", optimize=True)
print(f"Wrote og-image.png ({W}x{H})")
