"""Render the profile's original neural-network animation. Requires Pillow and NumPy."""

from pathlib import Path
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
PREVIEW = ROOT / ".git" / "profile-redesign"
WIDTH, HEIGHT = 1400, 460
FRAMES, DURATION = 80, 80
CYAN = (70, 213, 255)
VIOLET = (160, 116, 255)
WHITE = (239, 246, 255)
FONTS = Path("C:/Windows/Fonts")


def font(size, bold=False, mono=False):
    name = "consola.ttf" if mono else "segoeuib.ttf" if bold else "segoeui.ttf"
    return ImageFont.truetype(str(FONTS / name), size)


def spaced(draw, xy, value, fill, size=13, spacing=3):
    x, y = xy
    face = font(size, bold=True)
    for char in value:
        draw.text((x, y), char, fill=fill, font=face)
        x += draw.textlength(char, font=face) + spacing


def background():
    y, x = np.mgrid[0:HEIGHT, 0:WIDTH]
    rgb = np.zeros((HEIGHT, WIDTH, 3), dtype=float)
    rgb[:] = (8, 12, 27)
    purple = np.exp(-(((x - 1115) / 350) ** 2 + ((y - 145) / 240) ** 2))
    blue = np.exp(-(((x - 1220) / 270) ** 2 + ((y - 420) / 200) ** 2))
    left = np.exp(-(((x - 300) / 650) ** 2 + ((y - 400) / 200) ** 2))
    rgb += purple[..., None] * np.array((27, 8, 49))
    rgb += blue[..., None] * np.array((0, 22, 37))
    rgb += left[..., None] * np.array((3, 5, 16))
    img = Image.fromarray(np.uint8(np.clip(rgb, 0, 255))).convert("RGBA")
    d = ImageDraw.Draw(img)
    for xx in range(24, WIDTH, 32):
        for yy in range(24, HEIGHT, 32):
            d.ellipse((xx, yy, xx + 1, yy + 1), fill=(41, 47, 70))
    for xx in range(750, 1900, 90):
        d.line([(1110, 205), (xx, HEIGHT)], fill=(26, 36, 57), width=1)
    for yy in [278, 293, 315, 346, 390, 449]:
        d.line([(854, yy), (WIDTH, yy)], fill=(25, 38, 59), width=1)
    d.rounded_rectangle((0, 0, WIDTH - 1, HEIGHT - 1), radius=24, outline=(48, 51, 82), width=2)
    for xx in range(80, WIDTH - 80):
        t = (xx - 80) / (WIDTH - 160)
        color = tuple(int(CYAN[k] * (1 - t) + VIOLET[k] * t) for k in range(3))
        d.line((xx, 1, xx, 3), fill=color, width=1)
    spaced(d, (68, 56), "ARTIFICIAL INTELLIGENCE", CYAN, 14, 4)
    d.text((63, 103), "Parham Kiyoumarsi", font=font(66, bold=True), fill=WHITE)
    d.text((68, 198), "Learn the theory. Build the system.", font=font(27), fill=(177, 193, 219))
    tags = [("COMPUTER VISION", 174, CYAN), ("AGENTIC AI", 136, VIOLET), ("CYBERSECURITY", 169, (234, 135, 209))]
    xx = 68
    for label, w, color in tags:
        outline = tuple(int(channel * 0.42) for channel in color)
        fill = tuple(int(channel * 0.10) for channel in color)
        d.rounded_rectangle((xx, 260, xx + w, 299), radius=9, fill=fill, outline=outline, width=1)
        face = font(13, bold=True)
        tw = d.textlength(label, font=face)
        d.text((xx + (w - tw) / 2, 270), label, font=face, fill=color)
        xx += w + 12
    d.line((68, 341, 755, 341), fill=(43, 54, 78), width=1)
    d.text((68, 363), "> learn. build. iterate.", font=font(19, mono=True), fill=(127, 153, 192))
    spaced(d, (70, 409), "COMPUTER ENGINEERING / UNIVERSITY OF ISFAHAN", (105, 126, 161), 11, 1.2)
    return img


def neural_geometry():
    points = []
    count = 72
    for i in range(count):
        yy = 1 - 2 * (i + 0.5) / count
        rr = math.sqrt(1 - yy * yy)
        aa = i * math.pi * (3 - math.sqrt(5))
        points.append((rr * math.cos(aa), yy, rr * math.sin(aa)))
    pts = np.array(points)
    edges = []
    for i in range(count):
        distances = np.linalg.norm(pts - pts[i], axis=1)
        for j in np.argsort(distances)[1:5]:
            if i < j:
                edges.append((i, int(j)))
    return pts, edges


def render_frame(base, points, edges, number):
    phase = number / FRAMES * 2 * math.pi
    img = base.copy()
    overlay = Image.new("RGBA", img.size)
    d = ImageDraw.Draw(overlay)
    cx, cy, radius = 1105, 216, 163
    # Periodic rotation keeps the first and last frames visually continuous.
    angle = 0.26 * math.sin(phase)
    rotation = np.array([[math.cos(angle), 0, math.sin(angle)], [0, 1, 0], [-math.sin(angle), 0, math.cos(angle)]])
    rotated = points @ rotation.T
    projected = [(cx + p[0] * radius, cy + p[1] * radius, p[2]) for p in rotated]
    d.ellipse((cx - 191, cy - 191, cx + 191, cy + 191), outline=(125, 98, 203, 35), width=1)
    d.ellipse((cx - 177, cy - 177, cx + 177, cy + 177), outline=(79, 176, 226, 38), width=1)
    for index, (i, j) in enumerate(edges):
        a, b = projected[i], projected[j]
        depth = (a[2] + b[2] + 2) / 4
        alpha = int(24 + 62 * depth)
        color = CYAN if index % 3 else VIOLET
        d.line([a[:2], b[:2]], fill=(*color, alpha), width=1)
        if index % 4 == 0:
            progress = (number / FRAMES + index * 0.093) % 1
            px = a[0] + (b[0] - a[0]) * progress
            py = a[1] + (b[1] - a[1]) * progress
            for rr, aa in [(6, 16), (3, 50), (1.5, 235)]:
                d.ellipse((px - rr, py - rr, px + rr, py + rr), fill=(*color, aa))
    for i, (xx, yy, depth) in enumerate(projected):
        brightness = 0.5 + 0.5 * math.sin(phase * 2 + i * 0.6)
        aa = int(70 + 140 * brightness * (depth + 2) / 3)
        color = CYAN if i % 3 else VIOLET
        rr = 2.2 if depth > 0 else 1.6
        d.ellipse((xx - 6, yy - 6, xx + 6, yy + 6), fill=(*color, int(aa * 0.08)))
        d.ellipse((xx - rr, yy - rr, xx + rr, yy + rr), fill=(*color, aa))
    # The central chip remains legible while signals travel through the network.
    pulse = 0.5 + 0.5 * math.sin(phase)
    core = [(cx + 64 * math.cos(a), cy + 64 * math.sin(a)) for a in np.arange(6) * math.pi / 3 + math.pi / 6]
    d.polygon(core, fill=(11, 18, 38, 248), outline=(115, 127, 225, 175))
    inner = [(cx + 56 * math.cos(a), cy + 56 * math.sin(a)) for a in np.arange(6) * math.pi / 3 + math.pi / 6]
    d.line(inner + [inner[0]], fill=(76, 184, 241, int(85 + pulse * 85)), width=1)
    d.text((cx, cy - 3), "AI", font=font(48, bold=True), anchor="mm", fill=(*WHITE, 255))
    d.text((cx, cy + 31), "NEURAL SYSTEMS", font=font(8, mono=True), anchor="mm", fill=(130, 155, 195, 255))
    orbit = phase + 0.9
    ox, oy = cx + 191 * math.cos(orbit), cy + 191 * math.sin(orbit)
    for rr, aa in [(9, 20), (5, 55), (2.5, 245)]:
        d.ellipse((ox - rr, oy - rr, ox + rr, oy + rr), fill=(*CYAN, aa))
    for xx, yy, dx, dy in [(888, 51, 1, 1), (1322, 51, -1, 1), (888, 383, 1, -1), (1322, 383, -1, -1)]:
        d.line([(xx + dx * 19, yy), (xx, yy), (xx, yy + dy * 19)], fill=(125, 144, 189, 100), width=1)
    d.text((cx, 422), "DATA  /  MODELS  /  INTELLIGENCE", font=font(11, mono=True), fill=(123, 143, 184, 255), anchor="mm")
    if number % 20 < 12:
        d.rectangle((333, 369, 341, 388), fill=(*CYAN, 220))
    d.ellipse((44, 65, 50, 71), fill=(*CYAN, int(100 + 155 * pulse)))
    return Image.alpha_composite(img, overlay).convert("RGB")


def main():
    ASSETS.mkdir(exist_ok=True)
    PREVIEW.mkdir(parents=True, exist_ok=True)
    base = background()
    points, edges = neural_geometry()
    frames = [render_frame(base, points, edges, i) for i in range(FRAMES)]
    palette_source = Image.new("RGB", (WIDTH, HEIGHT * 4))
    for i, index in enumerate([0, 20, 40, 60]):
        palette_source.paste(frames[index], (0, i * HEIGHT))
    palette = palette_source.quantize(colors=192, method=Image.Quantize.MEDIANCUT)
    indexed = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]
    indexed[0].save(ASSETS / "neural-header.gif", save_all=True, append_images=indexed[1:], duration=DURATION, loop=0, optimize=True, disposal=1)
    frames[0].save(PREVIEW / "header-frame.png")
    frames[20].save(PREVIEW / "header-frame-20.png")
    frames[40].save(PREVIEW / "header-frame-40.png")
    print(f"Rendered {FRAMES} frames; GIF size: {(ASSETS / 'neural-header.gif').stat().st_size:,} bytes")
    render_typing()


def render_typing():
    width, height = 860, 68
    phrases = [
        "Machine Learning & Deep Learning",
        "Computer Vision & Automation",
        "Agentic AI & Research Assistants",
        "AI for Cybersecurity",
    ]
    face = font(27, mono=True)
    frames, durations = [], []

    def draw_frame(phrase, length, cursor=True, color=CYAN):
        image = Image.new("RGB", (width, height), (12, 17, 35))
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((0, 0, width - 1, height - 1), radius=12, outline=(46, 57, 86), width=1)
        full_width = draw.textlength("> " + phrase, font=face)
        x = (width - full_width) / 2
        draw.text((x, 17), "> ", font=face, fill=(125, 147, 185))
        x += draw.textlength("> ", font=face)
        visible = phrase[:length]
        draw.text((x, 17), visible, font=face, fill=color)
        if cursor:
            xx = x + draw.textlength(visible, font=face) + 3
            draw.rectangle((xx, 22, xx + 3, 45), fill=color)
        return image

    for index, phrase in enumerate(phrases):
        color = CYAN if index % 2 == 0 else (181, 151, 255)
        for length in range(len(phrase) + 1):
            frames.append(draw_frame(phrase, length, color=color))
            durations.append(65)
        for beat in range(8):
            frames.append(draw_frame(phrase, len(phrase), cursor=beat % 4 < 2, color=color))
            durations.append(150)
        for length in range(len(phrase), -1, -2):
            frames.append(draw_frame(phrase, length, color=color))
            durations.append(40)
        frames.append(draw_frame(phrase, 0, color=color))
        durations.append(200)
    palette_sample = Image.new("RGB", (width, height * 4))
    for i, phrase in enumerate(phrases):
        palette_sample.paste(draw_frame(phrase, len(phrase), color=CYAN if i % 2 == 0 else (181, 151, 255)), (0, i * height))
    palette = palette_sample.quantize(colors=96)
    indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    indexed[0].save(ASSETS / "focus-typing.gif", save_all=True, append_images=indexed[1:], duration=durations, loop=0, optimize=True, disposal=1)
    draw_frame(phrases[0], len(phrases[0])).save(PREVIEW / "typing-frame.png")
    print(f"Rendered typing animation; GIF size: {(ASSETS / 'focus-typing.gif').stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
