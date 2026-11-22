#!/usr/bin/env python3
"""Build the 1024x1024 entry image for make.fun news-image-20261121.
Deterministic, offline, PIL-only. Text verified against Reuters/AP/CNN/NYT
reporting of Saturday 21 November 2026 (see SOURCES in README)."""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (247, 243, 235)      # paper
NAVY = (11, 31, 58)
GOLD = (201, 162, 39)
RED = (176, 32, 32)
TEAL = (14, 116, 110)
INK = (24, 24, 24)
GREY = (90, 90, 90)
CARD = (255, 255, 255)
LINE = (210, 205, 192)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def para(draw, x, y, text, font, color, max_w, leading):
    for ln in wrap(draw, text, font, max_w):
        draw.text((x, y), ln, font=font, fill=color)
        y += leading
    return y

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# ---- masthead ----
d.rectangle([0, 0, W, 148], fill=NAVY)
d.text((36, 28), "THE WORLD IN ONE DAY", font=F(SERIF_B, 50), fill=(255, 255, 255))
d.text((38, 96), "Saturday, 21 November 2026  •  World news in one image",
       font=F(SANS, 23), fill=(214, 196, 130))
d.rectangle([W - 236, 24, W - 36, 124], outline=GOLD, width=3)
d.text((W - 218, 34), "21 NOV", font=F(SANS_B, 30), fill=GOLD)
d.text((W - 218, 72), "2026", font=F(SANS_B, 26), fill=(255, 255, 255))

# ---- lead story: COP31 ----
y = 164
d.rectangle([36, y, W - 36, y + 140], fill=RED)
d.text((58, y + 10), "LEAD  •  CLIMATE", font=F(SANS_B, 20), fill=(255, 214, 130))
d.text((58, y + 36), "COP31 close to a climate deal",
       font=F(SERIF_B, 40), fill=(255, 255, 255))
d.text((58, y + 88), "Antalya talks run past deadline — fossil fuels and a $120bn",
       font=F(SANS, 23), fill=(255, 235, 235))
d.text((58, y + 114), "adaptation fund still deadlocked as nearly 200 nations haggle.",
       font=F(SANS, 23), fill=(255, 235, 235))
# sun/leaf mark on the lead banner
cx, cy = W - 110, y + 70
d.ellipse([cx - 42, cy - 42, cx + 42, cy + 42], outline=(255, 214, 130), width=4)
d.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=(255, 214, 130))

# ---- 2x2 cards ----
cards = [
    ("GULF CRISIS", (176, 32, 32), "Iran strikes Bahrain",
     "Tehran says its Guards hit two US bases. Bahrain reports an industrial-site fire, no injuries, and says its air defences intercepted more attacks."),
    ("MEXICO", (14, 116, 110), "‘El Chapo Isidro’ captured",
     "Mexican forces seize FBI most-wanted cartel boss Fausto Isidro Meza Flores in Sinaloa. At least 11 die as violence erupts."),
    ("UKRAINE", (11, 31, 58), "Missile hits Kryvyi Rih",
     "A Russian strike on Zelenskyy’s hometown kills a boy, 7, and a paramedic; 28 are in hospital. Missiles also stray into Poland."),
    ("BALTIC SEA", (120, 72, 20), "Russian ship ablaze",
     "Drones hit the sanctioned cargo ship Sparta II in the Gulf of Finland. The crew evacuates as the vessel burns and drifts."),
]
cw, ch, gx, gy = 466, 224, 24, 16
x0, y0 = 36, 324
for i, (kick, col, head, body) in enumerate(cards):
    x = x0 + (i % 2) * (cw + gx)
    y = y0 + (i // 2) * (ch + gy)
    d.rounded_rectangle([x, y, x + cw, y + ch], radius=10, fill=CARD, outline=LINE, width=2)
    d.rectangle([x, y, x + cw, y + 8], fill=col)
    d.text((x + 20, y + 22), kick, font=F(SANS_B, 19), fill=col)
    yy = para(d, x + 20, y + 52, head, F(SANS_B, 28), INK, cw - 40, 34)
    para(d, x + 20, yy + 8, body, F(SANS, 20), (60, 60, 60), cw - 40, 26)

# ---- bottom strip: markets / hope / summit ----
y = 804
d.rectangle([36, y, W - 36, y + 148], fill=NAVY)
cols = [
    ("MARKETS", GOLD, "Nasdaq’s worst week since March 2020 as the AI sell-off turns into a correction."),
    ("HOPE", (110, 220, 170), "Mosquitoes cut dengue in Brazilian children by about 69%."),
    ("SUMMIT", (150, 190, 255), "Trump, Xi and Putin meet in Shenzhen. Zelenskyy calls Putin a “killer”."),
]
bw = (W - 72 - 48) // 3
for i, (kick, col, txt) in enumerate(cols):
    x = 56 + i * (bw + 24)
    d.text((x, y + 16), kick, font=F(SANS_B, 20), fill=col)
    para(d, x, y + 46, txt, F(SANS, 19), (235, 235, 235), bw - 8, 25)
    if i < 2:
        d.line([x + bw + 10, y + 18, x + bw + 10, y + 130], fill=(90, 110, 140), width=2)

# ---- footer ----
d.text((36, 966), "Sources: Reuters • AP • CNN • NYT  —  21 Nov 2026",
       font=F(SANS, 18), fill=GREY)

img.save("/home/hatch/workspace/news-image-build/entry.png", optimize=True)
print("saved", img.size)
import os
print("bytes:", os.path.getsize("/home/hatch/workspace/news-image-build/entry.png"))
