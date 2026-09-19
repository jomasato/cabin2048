"""Draw the home-screen icons.

The wordmark on the title screen runs cool -> hot across the four digits, the
same way the tiles do as they climb. The icons repeat that so the thing on the
home screen and the thing on the title screen read as one object.

    python tools/make_icons.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = r"C:\Windows\Fonts\arialbd.ttf"

GROUND = (11, 15, 21)
DIGITS = [
    ("2", (56, 189, 248)),
    ("0", (106, 139, 255)),
    ("4", (217, 79, 176)),
    ("8", (233, 164, 65)),
]


def wordmark(size, width_ratio, rounded):
    """Ground + '2048', each digit in its own colour, optically centred."""
    scale = 4  # draw big, downsample: cheap antialiasing on the corners
    s = size * scale
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    if rounded:
        d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * 0.215), fill=GROUND)
    else:
        d.rectangle([0, 0, s - 1, s - 1], fill=GROUND)

    # find the point size that makes "2048" the requested fraction of the width
    target = s * width_ratio
    pt = int(s * 0.3)
    for _ in range(40):
        f = ImageFont.truetype(FONT, pt)
        w = d.textlength("2048", font=f)
        if w == 0:
            break
        pt = int(pt * target / w)
        if abs(w - target) < s * 0.004:
            break
    font = ImageFont.truetype(FONT, pt)

    total = d.textlength("2048", font=font)
    box = font.getbbox("2048")
    x = (s - total) / 2
    y = (s - (box[3] - box[1])) / 2 - box[1]
    for ch, colour in DIGITS:
        d.text((x, y), ch, font=font, fill=colour)
        x += d.textlength(ch, font=font)

    return img.resize((size, size), Image.LANCZOS)


def quad(size):
    """At favicon sizes '2048' is mush, so show the ramp itself."""
    scale = 4
    s = size * scale
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * 0.2), fill=GROUND)
    pad, gap = s * 0.16, s * 0.055
    cell = (s - pad * 2 - gap) / 2
    for i, (_, colour) in enumerate(DIGITS):
        cx = pad + (i % 2) * (cell + gap)
        cy = pad + (i // 2) * (cell + gap)
        d.rounded_rectangle([cx, cy, cx + cell, cy + cell], radius=int(cell * 0.22), fill=colour)
    return img.resize((size, size), Image.LANCZOS)


def out(img, name):
    path = os.path.join(HERE, name)
    img.save(path)
    print("wrote", name)


if __name__ == "__main__":
    # iOS applies its own mask to apple-touch-icon, so give it a full square.
    out(wordmark(180, 0.74, rounded=False), "icon-180.png")
    out(wordmark(192, 0.74, rounded=True), "icon-192.png")
    out(wordmark(512, 0.74, rounded=True), "icon-512.png")
    # maskable: everything important inside the middle 80%
    out(wordmark(512, 0.54, rounded=False), "icon-maskable-512.png")
    out(quad(32), "favicon-32.png")
