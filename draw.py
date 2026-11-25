#!/usr/bin/env python3
"""Draw the news-image-20261125 entry: a newspaper front page summing up
Wednesday, 25 November 2026, in one 1024x1024 image. Pure PIL, no network.
Run: python3 draw.py  ->  writes entry.png next to this file."""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (247, 243, 232)      # newsprint off-white
INK = (20, 20, 20)        # near-black text
RED = (178, 34, 34)       # masthead accent
GREY = (110, 108, 100)    # secondary text
RULE = (60, 60, 60)
NAVY = (26, 42, 74)
SEA = (178, 208, 228)
LAND = (214, 196, 150)
SAND = (232, 220, 180)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_font(draw, text, path, start, max_w, min_size=10):
    """Largest font size (<= start) at which text fits max_w on one line."""
    size = start
    while size > min_size:
        fnt = font(path, size)
        if draw.textlength(text, font=fnt) <= max_w:
            return fnt
        size -= 1
    return font(path, min_size)


def draw_hero_graphic(draw, x, y, w, h):
    """Stylised Strait of Hormuz: sea between two land masses, a tanker
    in the strait and a red warning burst above it."""
    draw.rectangle([x, y, x + w, y + h], fill=SEA, outline=RULE, width=2)
    # Land masses top-left and bottom-right, leaving a diagonal strait.
    draw.polygon([(x, y), (x + w * 0.62, y), (x + w * 0.30, y + h * 0.42),
                  (x, y + h * 0.55)], fill=LAND)
    draw.polygon([(x + w, y + h), (x + w * 0.42, y + h),
                  (x + w * 0.72, y + h * 0.58), (x + w, y + h * 0.45)],
                 fill=LAND)
    # Dashed shipping lane through the strait.
    cx, cy = x + w * 0.52, y + h * 0.52
    for i in range(-4, 5):
        dx = i * 26
        draw.line([cx + dx - 8, cy + dx * 0.28 - 8,
                   cx + dx + 8, cy + dx * 0.28 + 8],
                  fill=(255, 255, 255), width=3)
    # Tanker: hull + superstructure, sailing the strait.
    hx, hy = x + w * 0.30, y + h * 0.60
    draw.rectangle([hx, hy, hx + 150, hy + 22], fill=(30, 30, 30))
    draw.polygon([(hx, hy), (hx + 150, hy), (hx + 138, hy + 22),
                  (hx + 12, hy + 22)], fill=(30, 30, 30))
    draw.rectangle([hx + 96, hy - 26, hx + 138, hy], fill=(30, 30, 30))
    draw.rectangle([hx + 104, hy - 38, hx + 112, hy - 26], fill=(30, 30, 30))
    draw.rectangle([hx + 20, hy - 12, hx + 82, hy], fill=(178, 34, 34))
    # Red warning burst above the tanker.
    bx, by = x + w * 0.68, y + h * 0.22
    pts = []
    import math
    for i in range(16):
        ang = math.pi * i / 8
        r = 34 if i % 2 == 0 else 16
        pts.append((bx + r * math.cos(ang), by + r * math.sin(ang)))
    draw.polygon(pts, fill=(220, 40, 30), outline=(140, 10, 10))
    draw.text((bx, by), "!", font=font(BOLD, 34), fill=(255, 255, 255),
              anchor="mm")
    # Caption inside the panel.
    cap = font(BOLD, 17)
    draw.text((x + w / 2, y + h - 16), "THE STRAIT OF HORMUZ",
              font=cap, fill=NAVY, anchor="mb")


def story(draw, x, y, w, tag, headline, summary):
    """One grid story: red tag, bold headline (<=2 lines), summary (<=2 lines)."""
    tag_f = font(BOLD, 16)
    draw.text((x, y), tag, font=tag_f, fill=RED)
    hy = y + 24
    head_f = font(BOLD, 25)
    lines = wrap(draw, headline, head_f, w)
    for ln in lines[:2]:
        draw.text((x, hy), ln, font=head_f, fill=INK)
        hy += 30
    sum_f = font(REG, 19)
    for ln in wrap(draw, summary, sum_f, w)[:2]:
        draw.text((x, hy), ln, font=sum_f, fill=(45, 45, 45))
        hy += 24
    return hy


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    m = 38  # margin
    cw = W - 2 * m

    # ---- Masthead ----
    title_f = fit_font(d, "THE WORLD IN ONE PICTURE", BOLD, 62, cw)
    d.text((W / 2, 34), "THE WORLD IN ONE PICTURE", font=title_f,
           fill=INK, anchor="ma")
    date_f = font(BOLD, 26)
    d.text((W / 2, 108), "WEDNESDAY, 25 NOVEMBER 2026",
           font=date_f, fill=INK, anchor="ma")
    d.text((W / 2, 140), "THE DAY'S WORLD NEWS  —  IN ONE PICTURE",
           font=font(REG, 17), fill=GREY, anchor="ma")
    d.rectangle([m, 168, W - m, 172], fill=RED)
    d.rectangle([m, 176, W - m, 178], fill=RULE)

    # ---- Hero story ----
    hy = 198
    d.text((m, hy), "TOP STORY  —  MIDDLE EAST", font=font(BOLD, 18), fill=RED)
    hero_head = ["HORMUZ ON EDGE:", "SHIPPING UNDER ATTACK"]
    head_f = font(BOLD, 42)
    yy = hy + 30
    for ln in hero_head:
        d.text((m, yy), ln, font=head_f, fill=INK)
        yy += 50
    hero_sum = ("Fresh attacks on commercial shipping in the Strait of "
                "Hormuz. Houthis threaten Saudi ports; the coalition "
                "orders Hodeidah evacuated as US\u2013Iran tensions rise.")
    sum_f = font(REG, 22)
    for ln in wrap(d, hero_sum, sum_f, 580):
        d.text((m, yy), ln, font=sum_f, fill=(45, 45, 45))
        yy += 30
    draw_hero_graphic(d, 650, 198, 336, 232)
    d.rectangle([m, 448, W - m, 450], fill=RULE)

    # ---- Six more stories, 2 columns x 3 rows ----
    stories = [
        ("TECH", "HUANG: \u2018I MADE SOME TERRIBLE MISTAKES\u2019",
         "A day after his reinstatement, Nvidia chief Jensen Huang "
         "tells staff he is in therapy."),
        ("USA", "GIULIANI AWARDED MEDAL OF FREEDOM",
         "President Trump gives Rudy Giuliani the highest honour a "
         "US civilian can receive."),
        ("USA  —  SECURITY", "UNCLASSIFIED CIA SYSTEM BREACHED",
         "Hackers break into an unclassified CIA system in the latest "
         "US cybersecurity incident."),
        ("AMERICAS", "ALL HOSTAGES FREED IN CARTAGENA",
         "Police free all hostages after a failed armoured-car raid; "
         "one captor is killed."),
        ("EUROPE", "MET POLICE \u2018STILL INSTITUTIONALLY RACIST\u2019",
         "A report finds the UK\u2019s biggest police force remains "
         "institutionally racist."),
        ("SPACE", "CHINA FLIES PAKISTAN\u2019S FIRST ASTRONAUT",
         "Shenzhou-24 carries Pakistan\u2019s first astronaut into orbit "
         "to the Tiangong space station."),
    ]
    col_w = (cw - 28) // 2
    row_y = [470, 622, 774]
    for i, (tag, head, summ) in enumerate(stories):
        x = m + (i % 2) * (col_w + 28)
        y = row_y[i // 2]
        story(d, x, y, col_w, tag, head, summ)
        if i % 2 == 0:
            d.line([x + col_w + 14, y, x + col_w + 14, y + 128],
                   fill=(200, 196, 184), width=1)

    # ---- Bottom strip: more of the day ----
    strip_y = 928
    d.rectangle([m, strip_y, W - m, strip_y + 58], fill=INK)
    strip = ("ALSO TODAY:  Hong Kong tech plunges — Hang Seng TECH \u22122.6%, "
             "Bilibili +7% on earnings  \u2022  Australia\u2013Solomon Islands "
             "sign a security treaty  \u2022  Bangladesh garment workers "
             "win a 36% pay rise")
    strip_f = font(BOLD, 16)
    lines = wrap(d, strip, strip_f, cw - 24)
    yy = strip_y + 8
    for ln in lines[:2]:
        d.text((W / 2, yy), ln, font=strip_f, fill=(255, 255, 255),
               anchor="ma")
        yy += 22

    d.text((W / 2, 1002), "All stories first reported on Wednesday, 25 November 2026.",
           font=font(REG, 14), fill=GREY, anchor="ma")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
