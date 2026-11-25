#!/usr/bin/env python3
"""Draw a newspaper front page for Tuesday 24 November 2026.

One 1024x1024 image (entry.png) summarising the day's world news:
a masthead, six story panels, and an "also today" strip.
Everything is drawn with Pillow; no network, no external assets.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- canvas
PAGE_W, PAGE_H = 1024, 1024
MARGIN = 30
CONTENT_W = PAGE_W - 2 * MARGIN

PAPER = (247, 243, 232)
INK = (26, 34, 50)
RED = (179, 35, 42)
GREY = (96, 101, 114)
RULE = (26, 34, 50)
SKY = (38, 90, 140)
LEAF = (34, 120, 70)
WOOD = (122, 84, 46)
GOLD = (198, 148, 42)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def typeface(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- text flow
def split_lines(draw, text, font, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines = []
    for chunk in text.split("\n"):
        words = chunk.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = current + " " + word
            if draw.textlength(trial, font=font) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def draw_para(draw, x, y, text, font, max_width, leading, fill=INK):
    """Draw wrapped text starting at (x, y); return the y below it."""
    for line in split_lines(draw, text, font, max_width):
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def text_block_height(draw, text, font, max_width, leading):
    return len(split_lines(draw, text, font, max_width)) * leading


def centred(draw, cx, y, text, font, fill):
    w = draw.textlength(text, font=font)
    draw.text((cx - w / 2, y), text, font=font, fill=fill)
    return y + font.size


# ---------------------------------------------------------------- masthead
def draw_masthead(draw):
    y = 20
    draw.line([(MARGIN, y), (PAGE_W - MARGIN, y)], fill=RULE, width=4)
    y += 10
    title_font = typeface(SERIF, 68)
    y = centred(draw, PAGE_W / 2, y, "THE WORLD TODAY", title_font, INK)
    y += 1
    date_font = typeface(SANS_BOLD, 26)
    y = centred(draw, PAGE_W / 2, y, "TUESDAY, 24 NOVEMBER 2026",
                date_font, RED)
    y += 8
    draw.line([(MARGIN, y), (PAGE_W - MARGIN, y)], fill=RULE, width=3)
    y += 5
    draw.line([(MARGIN, y), (PAGE_W - MARGIN, y)], fill=RULE, width=1)
    return y + 10

# ---------------------------------------------------------------- pictograms
# Each icon draws inside a (x, y, size) square on the given ImageDraw.

def icon_gavel(d, x, y, s):
    """A judge's gavel: angled head and handle over a sounding block."""
    tile = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    t = ImageDraw.Draw(tile)
    t.rectangle([s * 0.30, s * 0.62, s * 0.72, s * 0.72], fill=WOOD)
    t.rectangle([s * 0.28, s * 0.72, s * 0.74, s * 0.78], fill=(94, 62, 30))
    t.line([s * 0.30, s * 0.58, s * 0.72, s * 0.30], fill=WOOD, width=max(3, s // 16))
    t.rectangle([s * 0.58, s * 0.10, s * 0.86, s * 0.24], fill=WOOD)
    t.rectangle([s * 0.62, s * 0.16, s * 0.90, s * 0.30], fill=(94, 62, 30))
    t.rectangle([s * 0.52, s * 0.06, s * 0.60, s * 0.34], fill=GOLD)
    tile = tile.rotate(38, resample=Image.BICUBIC, center=(s / 2, s / 2))
    d._image.paste(tile, (int(x), int(y)), tile)


def icon_tower(d, x, y, s):
    """A skyscraper with a small drone and a puff of smoke."""
    bx, by = x + s * 0.28, y + s * 0.30
    bw, bh = s * 0.34, s * 0.62
    d.rectangle([bx, by, bx + bw, by + bh], fill=SKY)
    d.rectangle([bx, by, bx + bw, by + s * 0.10], fill=(24, 64, 100))
    for row in range(5):
        yy = by + s * 0.16 + row * s * 0.10
        d.rectangle([bx + s * 0.05, yy, bx + bw - s * 0.05, yy + s * 0.035],
                    fill=(190, 215, 232))
    for cx, cy, r in [(x + s * 0.62, y + s * 0.12, s * 0.075),
                      (x + s * 0.72, y + s * 0.06, s * 0.06)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(170, 172, 176))
    dx, dy = x + s * 0.66, y + s * 0.30
    d.ellipse([dx - s * 0.05, dy - s * 0.05, dx + s * 0.05, dy + s * 0.05],
              fill=RED)
    d.line([dx - s * 0.13, dy, dx + s * 0.13, dy], fill=INK, width=3)
    d.line([dx - s * 0.09, dy - s * 0.06, dx + s * 0.09, dy - s * 0.06],
           fill=INK, width=2)
    d.line([dx - s * 0.24, dy + s * 0.10, dx, dy + s * 0.02], fill=RED, width=2)


def icon_ship(d, x, y, s):
    """A cargo ship on waves with a drone overhead."""
    hx0, hx1 = x + s * 0.08, x + s * 0.82
    hy = y + s * 0.52
    d.polygon([(hx0, hy), (hx1, hy), (hx1 - s * 0.10, hy + s * 0.16),
               (hx0 + s * 0.08, hy + s * 0.16)], fill=INK)
    d.rectangle([hx0 + s * 0.10, hy - s * 0.16, hx0 + s * 0.34, hy], fill=SKY)
    d.rectangle([hx0 + s * 0.38, hy - s * 0.11, hx0 + s * 0.58, hy], fill=RED)
    d.rectangle([hx0 + s * 0.60, hy - s * 0.20, hx0 + s * 0.72, hy], fill=(230, 230, 226))
    d.line([hx0 + s * 0.60, hy - s * 0.20, hx0 + s * 0.60, hy - s * 0.30],
           fill=INK, width=3)
    for wy in (y + s * 0.76, y + s * 0.86):
        pts = []
        for i in range(17):
            px = x + s * 0.05 + i * (s * 0.90 / 16)
            py = wy + math.sin(i * math.pi / 2) * s * 0.02
            pts.append((px, py))
        d.line(pts, fill=SKY, width=3)
    dx, dy = x + s * 0.78, y + s * 0.16
    d.ellipse([dx - s * 0.045, dy - s * 0.045, dx + s * 0.045, dy + s * 0.045],
              fill=RED)
    d.line([dx - s * 0.11, dy, dx + s * 0.11, dy], fill=INK, width=3)


def icon_scales(d, x, y, s):
    """Balanced scales of justice."""
    cx = x + s / 2
    top = y + s * 0.12
    d.ellipse([cx - s * 0.05, top - s * 0.05, cx + s * 0.05, top + s * 0.05],
              fill=GOLD)
    d.line([cx, top, cx, y + s * 0.72], fill=INK, width=max(3, s // 22))
    d.line([x + s * 0.10, y + s * 0.24, x + s * 0.90, y + s * 0.24],
           fill=INK, width=max(3, s // 22))
    for side in (-1, 1):
        px = cx + side * s * 0.36
        d.line([px, y + s * 0.24, px - s * 0.10, y + s * 0.50], fill=INK, width=2)
        d.line([px, y + s * 0.24, px + s * 0.10, y + s * 0.50], fill=INK, width=2)
        d.arc([px - s * 0.13, y + s * 0.44, px + s * 0.13, y + s * 0.62],
              start=0, end=180, fill=GOLD, width=max(3, s // 20))
    d.rectangle([cx - s * 0.14, y + s * 0.72, cx + s * 0.14, y + s * 0.78],
                fill=INK)


def icon_chart(d, x, y, s):
    """A rising market line with an arrowhead, over axes."""
    d.line([x + s * 0.10, y + s * 0.10, x + s * 0.10, y + s * 0.88], fill=INK,
           width=4)
    d.line([x + s * 0.10, y + s * 0.88, x + s * 0.92, y + s * 0.88], fill=INK,
           width=4)
    trail = [(x + s * 0.16, y + s * 0.70), (x + s * 0.34, y + s * 0.62),
             (x + s * 0.48, y + s * 0.66), (x + s * 0.64, y + s * 0.42),
             (x + s * 0.82, y + s * 0.22)]
    d.line(trail, fill=LEAF, width=5, joint="curve")
    tip = trail[-1]
    d.polygon([(tip[0], tip[1] - s * 0.10), (tip[0] + s * 0.10, tip[1] + s * 0.02),
               (tip[0] - s * 0.02, tip[1] + s * 0.10)], fill=LEAF)


def icon_tanker(d, x, y, s):
    """A tanker beside a spiked naval mine, on waves."""
    hx0, hx1 = x + s * 0.06, x + s * 0.58
    hy = y + s * 0.48
    d.polygon([(hx0, hy), (hx1, hy), (hx1 - s * 0.07, hy + s * 0.15),
               (hx0 + s * 0.06, hy + s * 0.15)], fill=INK)
    d.rectangle([hx0 + s * 0.06, hy - s * 0.14, hx0 + s * 0.20, hy], fill=(230, 230, 226))
    d.rectangle([hx0 + s * 0.24, hy - s * 0.09, hx0 + s * 0.42, hy], fill=RED)
    mx, my, mr = x + s * 0.76, y + s * 0.42, s * 0.11
    for k in range(8):
        ang = k * math.pi / 4
        d.line([mx + math.cos(ang) * mr * 0.8, my + math.sin(ang) * mr * 0.8,
                mx + math.cos(ang) * mr * 1.5, my + math.sin(ang) * mr * 1.5],
               fill=INK, width=3)
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=INK)
    d.ellipse([mx - mr * 0.4, my - mr * 0.4, mx + mr * 0.1, my + mr * 0.1],
              fill=(70, 76, 88))
    for wy in (y + s * 0.74, y + s * 0.84):
        pts = []
        for i in range(17):
            px = x + s * 0.04 + i * (s * 0.92 / 16)
            py = wy + math.sin(i * math.pi / 2) * s * 0.02
            pts.append((px, py))
        d.line(pts, fill=SKY, width=3)

# ---------------------------------------------------------------- stories
# (kicker, headline, body, icon, wide)
STORIES = [
    ("TECH  \u2022  NEW YORK, USA",
     "Huawei found guilty",
     "A US jury convicted Huawei on 10 of 12 counts, including conspiracy "
     "to steal trade secrets and bank fraud, but cleared it of "
     "racketeering. Huawei says it will appeal.",
     icon_gavel, True),
    ("CONFLICT  \u2022  RIYADH, SAUDI ARABIA",
     "Houthi drone hits Riyadh tower",
     "At least 11 people were wounded in the strike on the tower housing "
     "the Saudi wealth fund \u2014 hit twice in under a week.",
     icon_tower, False),
    ("CONFLICT  \u2022  GULF OF FINLAND",
     "Ukraine hits Russian ships",
     "Drones hit the cargo ship Sparta II in the Gulf of Finland and a "
     "corvette off Libya. Poland cited a new airspace violation.",
     icon_ship, False),
    ("LAW  \u2022  THE HAGUE",
     "Myanmar guilty of genocide",
     "Fourteen nations affirmed the ICJ ruling: Myanmar's forces committed "
     "genocide against the Rohingya \u2014 a first for the court.",
     icon_scales, False),
    ("ECONOMY  \u2022  MARKETS",
     "Nvidia brings back Huang",
     "Nvidia shares jumped 31% on the CEO's return; the S&P 500 rose 4.7%, "
     "the Nasdaq 6.5% and Tokyo's Nikkei 3.9%.",
     icon_chart, False),
    ("ENERGY  \u2022  STRAIT OF HORMUZ",
     "Four tankers hit mines in the strait, Iran says",
     "Iran says four tankers struck naval mines; a maritime centre says "
     "the claims are unconfirmed.",
     icon_tanker, True),
]

ALSO_TODAY = [
    "Turkish Air Force helicopter crash kills five",
    "Senegal regain Africa Cup title after court appeal",
    "Gunmen hold 25 hostages in Cartagena supermarket",
    "Zelensky urges four-way talks with Russia, US, Europe",
]


def panel_height(draw, kicker, headline, body, width, icon_size, wide):
    """Measure how tall a story panel needs to be."""
    pad = 14
    head_font = typeface(SERIF, 38 if wide else 32)
    body_font = typeface(SANS, 18)
    kicker_font = typeface(SANS_BOLD, 15)
    if wide:
        text_w = width - 2 * pad - icon_size - 14
        h = pad + 22
        h += text_block_height(draw, headline, head_font, text_w, 40)
        h += 4
        h += text_block_height(draw, body, body_font, text_w, 22)
        h += pad
        return h
    # narrow panel: headline starts beside the icon (first two lines),
    # then continues at full width; body always spans the full width.
    narrow_w = width - 2 * pad - icon_size - 10
    full_w = width - 2 * pad
    head_lines = split_lines(draw, headline, head_font, narrow_w)
    h = pad + 22
    h += min(2, len(head_lines)) * 36
    rest = " ".join(head_lines[2:])
    if rest:
        h += text_block_height(draw, rest, head_font, full_w, 36)
    h += 4
    h += text_block_height(draw, body, body_font, full_w, 22)
    h += pad
    return max(h, pad + 22 + icon_size + 8)


def draw_panel(draw, x, y, width, kicker, headline, body, icon_fn, wide):
    """Draw one bordered story panel; return the y just below it."""
    pad = 14
    icon_size = 110 if wide else 84
    height = panel_height(draw, kicker, headline, body, width, icon_size, wide)
    draw.rectangle([x, y, x + width, y + height], outline=RULE, width=2)
    kicker_font = typeface(SANS_BOLD, 15)
    head_font = typeface(SERIF, 38 if wide else 32)
    body_font = typeface(SANS, 18)
    cx = x + pad
    cy = y + pad
    draw.text((cx, cy), kicker, font=kicker_font, fill=RED)
    cy += 22
    if wide:
        # icon on the right, headline + body on the left
        icon_fn(draw, x + width - pad - icon_size, y + pad + 4, icon_size)
        text_w = width - 2 * pad - icon_size - 14
        cy = draw_para(draw, cx, cy, headline, head_font, text_w, 40)
        cy += 4
        cy = draw_para(draw, cx, cy, body, body_font, text_w, 22)
    else:
        # icon top-right; headline wraps in the space beside it
        icon_fn(draw, x + width - pad - icon_size, y + pad + 18, icon_size)
        text_w = width - 2 * pad - icon_size - 10
        head_lines = split_lines(draw, headline, head_font, text_w)
        shown = 0
        for line in head_lines:
            draw.text((cx, cy), line, font=head_font, fill=INK)
            cy += 36
            shown += 1
            if shown == 2:
                break
        rest = " ".join(head_lines[shown:])
        if rest:
            cy = draw_para(draw, cx, cy, rest, head_font,
                           width - 2 * pad, 36)
        cy += 4
        cy = draw_para(draw, cx, cy, body, body_font, width - 2 * pad, 22)
    return y + height

# ---------------------------------------------------------------- page assembly
GAP = 8
HALF_W = (CONTENT_W - GAP) // 2


def draw_also_today(draw, y):
    """Two-column bullet strip under a red heading; return y below it."""
    head_font = typeface(SANS_BOLD, 17)
    item_font = typeface(SANS, 16)
    draw.text((MARGIN, y), "ALSO TODAY", font=head_font, fill=RED)
    y += 26
    col_w = (CONTENT_W - 24) // 2
    tops = []
    for col in range(2):
        cy = y
        for item in ALSO_TODAY[col::2]:
            bullet_x = MARGIN + col * (col_w + 24)
            draw.text((bullet_x, cy), "\u2022", font=item_font, fill=INK)
            cy = draw_para(draw, bullet_x + 16, cy, item, item_font,
                           col_w - 16, 22)
            cy += 6
        tops.append(cy)
    return max(tops)


def draw_footer(draw, y):
    draw.line([(MARGIN, y), (PAGE_W - MARGIN, y)], fill=GREY, width=1)
    y += 8
    foot_font = typeface(SANS, 14)
    centred(draw, PAGE_W / 2, y,
            "All events of Tuesday 24 November 2026  \u2022  As reported that day",
            foot_font, GREY)
    return y + 20


def build_page():
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(page)
    y = draw_masthead(draw)
    # Lead story, full width.
    kicker, headline, body, icon_fn, wide = STORIES[0]
    y = draw_panel(draw, MARGIN, y, CONTENT_W, kicker, headline, body,
                   icon_fn, wide)
    y += GAP
    # Two rows of two half-width stories.
    for row in range(2):
        left = STORIES[1 + row * 2]
        right = STORIES[2 + row * 2]
        h_left = panel_height(draw, left[0], left[1], left[2], HALF_W, 84,
                              False)
        h_right = panel_height(draw, right[0], right[1], right[2], HALF_W,
                               84, False)
        row_h = max(h_left, h_right)
        draw_panel(draw, MARGIN, y, HALF_W, left[0], left[1], left[2],
                   left[3], False)
        draw_panel(draw, MARGIN + HALF_W + GAP, y, HALF_W, right[0], right[1],
                   right[2], right[3], False)
        y += row_h + GAP
    # Closing full-width story.
    kicker, headline, body, icon_fn, wide = STORIES[5]
    y = draw_panel(draw, MARGIN, y, CONTENT_W, kicker, headline, body,
                   icon_fn, wide)
    y += GAP + 2
    y = draw_also_today(draw, y)
    y += 8
    y = draw_footer(draw, y)
    if y > PAGE_H - 8:
        raise SystemExit(f"page overflow: content ends at y={y}")
    return page


def main():
    page = build_page()
    page.save(os.path.join(HERE, "entry.png"))
    print("wrote entry.png", page.size)


if __name__ == "__main__":
    main()
