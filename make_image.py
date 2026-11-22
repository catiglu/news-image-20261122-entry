"""Generate a deterministic 1024x1024 world-news poster for 22 November 2026.

No network, no randomness: the same entry.png is written on every run.
Run at build time only; the gate entry point is main.py, which copies this file.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = "#0b1220"
CARD_BG = "#1b2536"
CARD_EDGE = "#2b3a52"
ACCENT = "#f59e0b"
MUTED = "#8fa3bf"
WHITE = "#f8fafc"

FONT_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
FONT_REG = r"C:\Windows\Fonts\arial.ttf"

# (tag, color, headline) — world news reported 21-22 November 2026 (UTC).
NEWS = [
    ("MIDDLE EAST", "#f59e0b",
     "Iran strikes US bases and an industrial site in Bahrain; Houthi attacks continue"),
    ("AMERICAS", "#34d399",
     "Mexico captures top drug kingpin 'El Chapo Isidro' in a special-forces raid"),
    ("EUROPE", "#38bdf8",
     "Deadly drone barrage hits Kyiv as Russia steps up its war on Ukraine"),
    ("MARKETS", "#fb7185",
     "Nasdaq erases all 2026 gains as the AI sell-off hits Anthropic after its IPO"),
    ("CLIMATE", "#a78bfa",
     "COP31 climate talks deadlock over fossil fuels and run deep into overtime"),
    ("LAW", "#facc15",
     "UN talks fail to agree binding rules on lethal autonomous 'killer' robots"),
    ("MIDDLE EAST", "#f472b6",
     "Israeli strike kills three in a Gaza aid vehicle; Lebanon demands Israel withdraw"),
    ("AMERICAS", "#60a5fa",
     "Brazil's former president Bolsonaro in intensive care with a bowel obstruction"),
]

SOURCES = "Sources: BBC World - Reuters - AP - Al Jazeera | 21-22 November 2026"


def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def wrap(draw, text, font, max_width, max_lines):
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
    return lines


def main():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    f_title = load_font(FONT_BOLD, 76)
    f_date = load_font(FONT_REG, 34)
    f_tag = load_font(FONT_BOLD, 17)
    f_head = load_font(FONT_BOLD, 25)
    f_foot = load_font(FONT_REG, 19)

    # Header
    draw.text((64, 46), "WORLD NEWS", font=f_title, fill=WHITE)
    draw.text((66, 148), "Sunday, 22 November 2026", font=f_date, fill=ACCENT)
    draw.line([(66, 200), (W - 66, 200)], fill=CARD_EDGE, width=2)

    top = 224
    card_h = 92
    gap = 8
    left = 64
    card_w = W - 2 * left
    for i, (tag, color, title) in enumerate(NEWS):
        y0 = top + i * (card_h + gap)
        y1 = y0 + card_h
        draw.rounded_rectangle([left, y0, left + card_w, y1], radius=14, fill=CARD_BG)
        draw.rounded_rectangle([left, y0, left + 10, y1], radius=5, fill=color)
        draw.text((left + 28, y0 + 12), tag, font=f_tag, fill=color)
        lines = wrap(draw, title, f_head, card_w - 56, max_lines=2)
        ty = y0 + 40
        for ln in lines:
            draw.text((left + 28, ty), ln, font=f_head, fill=WHITE)
            ty += 29

    draw.text((64, H - 52), SOURCES, font=f_foot, fill=MUTED)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    size = os.path.getsize(out)
    assert img.size == (1024, 1024), img.size
    assert size < 1024 * 1024, size
    print("wrote", out, img.size, size, "bytes")


if __name__ == "__main__":
    main()
