#!/usr/bin/env python3
"""Draw entry.png: a newspaper front page summing up Tuesday 24 November 2026.

Everything is drawn with PIL in a flat newspaper style: a masthead naming
the day, a lead story, four story panels, one wide panel and an "also today"
strip. Every story is real news first reported on 24 Nov 2026, checked
against the day's summaries (dailysummaryof.com/world/2026-11-24 and
horizonapp.link/en/2026/11/24, which aggregate Reuters/AP/AFP wires):
Huawei's US jury verdict; the Houthi drone strike on Riyadh's PIF tower;
Ukraine's drone strikes on Russian ships; fourteen nations affirming the
ICJ's Myanmar genocide ruling; Nvidia reinstating Jensen Huang and the
market rally; and Iran's claim of four tankers hitting mines in Hormuz.
"""
import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 28

PAPER = (247, 243, 233)
PANEL = (255, 253, 246)
INK = (24, 30, 48)
MUTED = (96, 102, 116)
RED = (176, 32, 40)
BLUE = (31, 78, 121)
GREEN = (46, 125, 87)
ORANGE = (214, 110, 30)
GOLD = (201, 162, 39)
SKY = (168, 205, 224)

FDIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FDIR + "DejaVuSerif-Bold.ttf"
SERIF = FDIR + "DejaVuSerif.ttf"
SANS_B = FDIR + "DejaVuSans-Bold.ttf"
SANS = FDIR + "DejaVuSans.ttf"


def fnt(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, max_w):
    """Greedy word wrap measured in pixels; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, font, fill, max_w, leading=None):
    """Draw wrapped text; returns the y just below the last line."""
    leading = leading or int(font.size * 1.28)
    for line in wrap(d, text, font, max_w):
        d.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def centre(d, y, text, font, fill):
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, y), text, font=font, fill=fill)
    return y + int(font.size * 1.2)


# ---------------------------------------------------------------- icons
# Each icon draws inside a square box (x, y, size). All shapes are flat.

def icon_gavel(d, x, y, s):
    # judge's gavel over a sounding block, in front of courthouse columns
    d.rectangle([x + 14, y + 16, x + 26, y + s - 30], fill=INK)
    d.rectangle([x + 28, y + 16, x + 40, y + s - 30], fill=INK)
    d.rectangle([x + 42, y + 16, x + 54, y + s - 30], fill=INK)
    # gavel head (tilted bar) and handle, drawn as a diagonal pair
    d.line([x + 62, y + 14, x + 94, y + 46], fill=(120, 84, 50), width=16)
    d.line([x + 56, y + 42, x + 92, y + 78], fill=(120, 84, 50), width=8)
    d.ellipse([x + 88, y + 40, x + 100, y + 52], fill=(120, 84, 50))
    d.rectangle([x + 52, y + s - 24, x + 92, y + s - 12], fill=(120, 84, 50),
                outline=INK, width=2)


def icon_tower(d, x, y, s):
    # a tall glass tower, smoke curling from a hit near the top
    d.rectangle([x + 30, y + 34, x + s - 30, y + s - 8], fill=BLUE, outline=INK, width=3)
    for row in range(5):
        wy = y + 44 + row * 12
        d.line([x + 34, wy, x + s - 34, wy], fill=SKY, width=3)
    d.rectangle([x + 38, y + 22, x + s - 38, y + 34], fill=INK)
    for i, (sx, sy) in enumerate(((x + 52, y + 6), (x + 66, y + 2), (x + 78, y + 10))):
        d.ellipse([sx, sy, sx + 16, sy + 12], fill=(150, 156, 168))
    d.polygon([(x + 56, y + 30), (x + 66, y + 42), (x + 76, y + 30)],
              fill=ORANGE)
    # small drone silhouette above
    d.ellipse([x + 10, y + 46, x + 20, y + 54], fill=RED)
    d.line([x + 4, y + 50, x + 10, y + 50], fill=RED, width=2)
    d.line([x + 20, y + 50, x + 26, y + 50], fill=RED, width=2)


def icon_ship(d, x, y, s):
    # a cargo ship with a drone above it, waves below
    d.polygon([(x + 8, y + 60), (x + 88, y + 52), (x + 80, y + 70),
               (x + 18, y + 72)], fill=INK)
    d.rectangle([x + 22, y + 40, x + 44, y + 58], fill=INK)
    d.rectangle([x + 48, y + 46, x + 68, y + 58], fill=INK)
    d.line([x + 30, y + 28, x + 30, y + 40], fill=INK, width=3)
    d.ellipse([x + 70, y + 10, x + 82, y + 22], fill=RED)
    d.line([x + 62, y + 16, x + 70, y + 16], fill=RED, width=2)
    d.line([x + 82, y + 16, x + 90, y + 16], fill=RED, width=2)
    for i, wy in enumerate((80, 90)):
        pts = [(x + px, y + wy + 3 * math.sin((px + i * 11) / 6.0))
               for px in range(8, 92, 4)]
        d.line(pts, fill=BLUE, width=3)


def icon_scales(d, x, y, s):
    # scales of justice
    d.line([x + s // 2, y + 12, x + s // 2, y + s - 22], fill=INK, width=4)
    d.line([x + 12, y + 22, x + s - 12, y + 22], fill=INK, width=4)
    d.ellipse([x + s // 2 - 6, y + 8, x + s // 2 + 6, y + 20], fill=GOLD)
    for sign in (-1, 1):
        cx = x + s // 2 + sign * (s // 2 - 14)
        d.line([cx, y + 22, cx, y + 48], fill=INK, width=3)
        d.line([x + s // 2 + sign * (s // 2 - 26), y + 22, cx, y + 48],
               fill=INK, width=2)
        d.line([x + s // 2 + sign * (s // 2 - 2), y + 22, cx, y + 48],
               fill=INK, width=2)
        d.pieslice([cx - 16, y + 44, cx + 16, y + 66], start=0, end=180,
                   fill=GOLD, outline=INK, width=2)
    d.rectangle([x + s // 2 - 16, y + s - 22, x + s // 2 + 16, y + s - 12],
                fill=INK)


def icon_chart(d, x, y, s):
    d.line([x + 14, y + 12, x + 14, y + s - 14], fill=INK, width=4)
    d.line([x + 14, y + s - 14, x + s - 10, y + s - 14], fill=INK, width=4)
    pts = [(x + 20, y + 72), (x + 38, y + 58), (x + 52, y + 62),
           (x + 68, y + 38), (x + 86, y + 20)]
    d.line(pts, fill=GREEN, width=6, joint="curve")
    d.polygon([(x + 86, y + 20), (x + 74, y + 18), (x + 88, y + 32),
               (x + 96, y + 16)], fill=GREEN)


def icon_tanker(d, x, y, s):
    # an oil tanker on waves with a spiked naval mine beside it
    d.polygon([(x + 6, y + 34), (x + 62, y + 34), (x + 56, y + 52),
               (x + 12, y + 52)], fill=INK)
    d.rectangle([x + 40, y + 20, x + 52, y + 34], fill=INK)
    d.line([x + 46, y + 10, x + 46, y + 20], fill=INK, width=3)
    mx, my, r = x + 70, y + 40, 10
    d.ellipse([mx - r, my - r, mx + r, my + r], fill=INK)
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        d.line([mx + int(r * 0.8 * math.cos(a)), my + int(r * 0.8 * math.sin(a)),
                mx + int((r + 5) * math.cos(a)), my + int((r + 5) * math.sin(a))],
               fill=INK, width=3)
    for i, wy in enumerate((58, 66)):
        pts = [(x + px, y + wy + 3 * math.sin((px + i * 11) / 6.0))
               for px in range(4, 96, 4)]
        d.line(pts, fill=BLUE, width=3)


# ---------------------------------------------------------------- page

def masthead(d):
    d.line([MARGIN, 30, W - MARGIN, 30], fill=INK, width=3)
    centre(d, 42, "THE WORLD TODAY", fnt(SERIF_B, 62), INK)
    centre(d, 108, "TUESDAY, 24 NOVEMBER 2026", fnt(SANS_B, 26), RED)
    d.line([MARGIN, 146, W - MARGIN, 146], fill=INK, width=3)
    d.line([MARGIN, 151, W - MARGIN, 151], fill=INK, width=1)


def lead_panel(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=INK, width=3)
    d.text((x + 18, y + 14), "TECH  •  NEW YORK, USA", font=fnt(SANS_B, 17),
           fill=RED)
    text_block(d, x + 18, y + 42, "Huawei found guilty",
               fnt(SERIF_B, 40), INK, w - 240, leading=46)
    body = ("A US jury convicted Huawei on 10 of 12 counts, including "
            "conspiracy to steal trade secrets and bank fraud, but cleared "
            "it of racketeering. Huawei says it will appeal.")
    text_block(d, x + 18, y + 100, body, fnt(SANS, 20), INK, w - 240, leading=26)
    icon_gavel(d, x + w - 195, y + 18, 170)


def story_panel(d, x, y, w, h, kicker, headline, body, icon):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=INK, width=2)
    d.text((x + 16, y + 12), kicker, font=fnt(SANS_B, 15), fill=RED)
    icon(d, x + w - 112, y + 12, 96)
    text_block(d, x + 16, y + 38, headline, fnt(SERIF_B, 29), INK,
               w - 140, leading=35)
    text_block(d, x + 16, y + 116, body, fnt(SANS, 19), INK, w - 32, leading=25)


def wide_panel(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=INK, width=2)
    icon_tanker(d, x + 14, y + 12, 68)
    d.text((x + 104, y + 12), "ENERGY  •  STRAIT OF HORMUZ", font=fnt(SANS_B, 15),
           fill=RED)
    d.text((x + 104, y + 34), "Four tankers hit mines in the strait, Iran says",
           font=fnt(SERIF_B, 25), fill=INK)
    d.text((x + 104, y + 68),
           "Iran says four tankers struck naval mines; a maritime centre says the claims are unconfirmed.",
           font=fnt(SANS, 17), fill=INK)


def also_today(d, x, y, w):
    d.text((x, y), "ALSO TODAY", font=fnt(SANS_B, 17), fill=RED)
    items = [
        "Turkish Air Force helicopter crash kills five",
        "Gunmen hold 25 hostages in Cartagena supermarket",
        "Senegal regain Africa Cup title after court appeal",
        "Zelensky urges four-way talks with Russia, US, Europe",
    ]
    half = w // 2
    yy = y + 26
    for i, item in enumerate(items):
        col = i % 2
        row = i // 2
        d.text((x + col * half, yy + row * 26), "\u2022  " + item,
               font=fnt(SANS, 16), fill=INK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    masthead(d)

    lead_panel(d, MARGIN, 164, W - 2 * MARGIN, 178)

    gx, gy = MARGIN, 356
    gw, gh = (W - 2 * MARGIN - 16) // 2, 208
    story_panel(d, gx, gy, gw, gh,
                "CONFLICT  •  RIYADH, SAUDI ARABIA",
                "Houthi drone hits Riyadh tower",
                "At least 11 people were wounded in the strike on the tower "
                "housing the Saudi wealth fund — hit twice in under a week.",
                icon_tower)
    story_panel(d, gx + gw + 16, gy, gw, gh,
                "CONFLICT  •  GULF OF FINLAND",
                "Ukraine hits Russian ships",
                "Drones hit the cargo ship Sparta II in the Gulf of "
                "Finland and a corvette off Libya. Poland cited a new "
                "airspace violation.",
                icon_ship)
    story_panel(d, gx, gy + gh + 14, gw, gh,
                "LAW  •  THE HAGUE",
                "Myanmar guilty of genocide",
                "Fourteen nations affirmed the ICJ ruling: Myanmar's "
                "forces committed genocide against the Rohingya — a first "
                "for the court.",
                icon_scales)
    story_panel(d, gx + gw + 16, gy + gh + 14, gw, gh,
                "ECONOMY  •  MARKETS",
                "Nvidia brings back Huang",
                "Nvidia shares jumped 31% on the CEO's return; the S&P 500 "
                "rose 4.7%, the Nasdaq 6.5% and Tokyo's Nikkei 3.9%.",
                icon_chart)

    wide_panel(d, MARGIN, 792, W - 2 * MARGIN, 96)
    also_today(d, MARGIN, 908, W - 2 * MARGIN)

    d.line([MARGIN, 992, W - MARGIN, 992], fill=MUTED, width=1)
    centre(d, 998, "All events of Tuesday 24 November 2026  •  As reported that day",
           fnt(SANS, 14), MUTED)

    img.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
