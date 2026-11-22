"""Generate a deterministic 1024x1024 broadsheet-style world-news poster
for Sunday, 22 November 2026 (make.fun bounty news-image-20261122).

No network, no randomness: the same entry.png is written on every run.
Run at build time only; the gate entry point is main.py, which copies the file.

Headlines below were verified against Reuters/AP/BBC/Al Jazeera coverage
dated 21-22 November 2026 (UTC) at build time.

v2: classic newspaper redesign - cream paper, serif masthead, dateline,
hero story + 2-column grid + "in brief" strip; rendered at 2x and
downsampled for crisp text.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
S = 2  # supersampling factor: draw at 2048, downsample to 1024
CW, CH = W * S, H * S
M = 96  # page margin (in 2x units)

PAPER = "#f7f2e7"
INK = "#1a1713"
RED = "#a5231b"
GREY = "#6d675b"
FAINT = "#b8b0a0"

FONTS = "C:/Windows/Fonts"


def _font(candidates, size):
    for name in candidates:
        path = os.path.join(FONTS, name)
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def f_masthead():
    return _font(["georgiab.ttf", "timesbd.ttf", "arialbd.ttf"], 140)


def f_hero():
    return _font(["georgiab.ttf", "timesbd.ttf", "arialbd.ttf"], 86)


def f_card():
    return _font(["georgiab.ttf", "timesbd.ttf", "arialbd.ttf"], 46)


def f_kicker():
    return _font(["georgiab.ttf", "arialbd.ttf"], 34)


def f_meta():
    return _font(["georgia.ttf", "times.ttf", "arial.ttf"], 40)


def f_meta_sm():
    return _font(["georgia.ttf", "times.ttf", "arial.ttf"], 34)



# --- Content: world news reported 21-22 November 2026 (UTC), verified ----
HERO_KICKER = "MIDDLE EAST - LEAD STORY"
HERO_HEAD = "Iran strikes US bases in Bahrain as Hormuz standoff deepens"
HERO_DECK = ("Bahrain says an industrial facility was hit; the IRGC says it "
             "targeted American positions amid Tehran's moves against the blockade.")

CARDS = [
    ("AMERICAS", "FBI ten-most-wanted kingpin 'El Chapo Isidro' seized in Mexico shoot-out"),
    ("EUROPE", "Drone war widens: Russian cargo ship left ablaze in the Gulf of Finland"),
    ("MIDDLE EAST", "Israeli strike kills three in a Gaza vehicle distributing food aid"),
    ("MARKETS", "AI sell-off deepens: S&P 500 enters correction after the Anthropic IPO"),
    ("CLIMATE", "COP31 talks deadlocked over fossil fuels and run into overtime"),
    ("LAW OF WAR", "UN 'killer robots' talks end with no binding rules on autonomous arms"),
]

BRIEF = ("Also: Bolsonaro in intensive care  -  Princess of Wales opens up on her cancer "
         "journey  -  GTA VI's record $3.79bn debut")

FOOTER = "Sources: Reuters - AP - BBC - Al Jazeera   |   as reported 21-22 November 2026 (UTC)"

NUMBERS = [
    ("3", "killed in an Israeli strike on a Gaza food-aid vehicle"),
    ("10", "FBI most-wanted list 'El Chapo Isidro' was on when seized"),
    ("0", "binding rules agreed at UN talks on killer robots"),
    ("$3.79bn", "GTA VI opening-weekend entertainment record"),
]


def wrap(draw, text, font, max_width, max_lines):
    """Greedy word wrap with ellipsis; returns lines that fit max_width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while draw.textlength(last + "...", font=font) > max_width and " " in last:
            last = last.rsplit(" ", 1)[0]
        lines[-1] = last + "..."
    for ln in lines:
        assert draw.textlength(ln, font=font) <= max_width + 2, "line overflow: " + repr(ln)
    return lines



def globe(draw, cx, cy, r, width=5, color=INK):
    """Simple wireframe globe emblem: circle + meridians + parallels."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=width)
    for k in (0.35, 0.75):
        rx = int(r * k)
        draw.arc([cx - rx, cy - r, cx + rx, cy + r], 0, 360, fill=color, width=width - 1)
    for ry in (0.30, 0.72):
        ry_px = int(r * ry)
        draw.arc([cx - r, cy - ry_px, cx + r, cy + ry_px], 0, 360, fill=color, width=width - 1)


def draw_page():
    img = Image.new("RGB", (CW, CH), PAPER)
    d = ImageDraw.Draw(img)

    # ---- top rule + edition strip ----
    d.line([(M, 56), (CW - M, 56)], fill=INK, width=4)
    d.line([(M, 66), (CW - M, 66)], fill=INK, width=2)
    f_strip = f_meta_sm()
    d.text((M, 84), "LATE WORLD EDITION", font=f_strip, fill=GREY)
    t = "ONE PAGE - ONE DAY"
    tw = d.textlength(t, font=f_strip)
    d.text((CW - M - tw, 84), t, font=f_strip, fill=GREY)

    # ---- masthead ----
    fm = f_masthead()
    title = "WORLD NEWS"
    tw = d.textlength(title, font=fm)
    bx = d.textbbox((0, 0), title, font=fm)
    ty = 128
    d.text(((CW - tw) / 2, ty), title, font=fm, fill=INK)
    mast_mid = ty + (bx[3] - bx[1]) / 2 + bx[1]
    globe(d, (CW - tw) / 2 - 96, mast_mid, 52)
    globe(d, (CW + tw) / 2 + 96, mast_mid, 52)

    # ---- dateline ----
    y = ty + 240
    d.line([(M, y), (CW - M, y)], fill=INK, width=3)
    fd = f_kicker()
    date = "SUNDAY, NOVEMBER 22, 2026"
    dw = d.textlength(date, font=fd)
    d.text(((CW - dw) / 2, y + 16), date, font=fd, fill=RED)
    d.line([(M, y + 76), (CW - M, y + 76)], fill=INK, width=3)

    # ---- hero story ----
    y = y + 106
    fk = f_kicker()
    d.text((M, y), HERO_KICKER, font=fk, fill=RED)
    y += 52
    fh = f_hero()
    for ln in wrap(d, HERO_HEAD, fh, CW - 2 * M, 3):
        d.text((M, y), ln, font=fh, fill=INK)
        y += 96
    y += 6
    fdk = f_meta_sm()
    for ln in wrap(d, HERO_DECK, fdk, CW - 2 * M, 2):
        d.text((M, y), ln, font=fdk, fill=GREY)
        y += 46
    y += 18
    d.line([(M, y), (CW - M, y)], fill=INK, width=6)

    # ---- 2-column grid ----
    y += 28
    fc = f_card()
    col_gap = 72
    col_w = (CW - 2 * M - col_gap) // 2
    card_h = 196
    for i, (kicker, head) in enumerate(CARDS):
        col, row = i % 2, i // 2
        x = M + col * (col_w + col_gap)
        yy = y + row * card_h
        d.text((x, yy), kicker, font=fk, fill=RED)
        hy = yy + 48
        for ln in wrap(d, head, fc, col_w, 3):
            d.text((x, hy), ln, font=fc, fill=INK)
            hy += 50
        assert hy <= yy + card_h + 40, "card overflow: " + head[:30]
    d.line([(CW // 2, y), (CW // 2, y + 3 * card_h - 10)], fill=FAINT, width=2)
    y += 3 * card_h + 8

    # ---- in-brief strip ----
    d.line([(M, y), (CW - M, y)], fill=FAINT, width=2)
    y += 14
    fb = f_meta_sm()
    for ln in wrap(d, BRIEF, fb, CW - 2 * M, 2):
        d.text((M, y), ln, font=fb, fill=GREY)
        y += 42
    y += 10
    d.line([(M, y), (CW - M, y)], fill=FAINT, width=2)

    # ---- the day in numbers ----
    y += 24
    d.text((M, y), "THE DAY IN NUMBERS", font=fk, fill=RED)
    y += 62
    gap = 48
    cell_w = (CW - 2 * M - 3 * gap) // 4
    fn = f_hero()
    fc2 = f_meta_sm()
    for i, (num, cap) in enumerate(NUMBERS):
        x = M + i * (cell_w + gap)
        d.text((x, y), num, font=fn, fill=INK)
        cy = y + 108
        for ln in wrap(d, cap, fc2, cell_w, 2):
            d.text((x, cy), ln, font=fc2, fill=GREY)
            cy += 42
        assert cy <= y + 210, "number caption overflow: " + num
    y += 216
    d.line([(M, y), (CW - M, y)], fill=INK, width=4)

    # ---- footer ----
    ff = f_meta_sm()
    fw = d.textlength(FOOTER, font=ff)
    d.text(((CW - fw) / 2, CH - M + 8), FOOTER, font=ff, fill=GREY)

    return img.resize((W, H), Image.LANCZOS)


def main():
    img = draw_page()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG", optimize=True)
    size = os.path.getsize(out)
    print("wrote", out, size, "bytes", img.size)
    assert size <= 1024 * 1024, "PNG exceeds 1 MiB"
    assert img.size == (W, H)


if __name__ == "__main__":
    main()
