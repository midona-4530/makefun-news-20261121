from PIL import Image, ImageDraw, ImageFont
import os

W = H = 1024
BG = "#f3eedf"
NAVY = "#14213d"
BLUE = "#2f67c6"
RED = "#c92a2a"
GOLD = "#c99a2e"
DARK_BLUE = "#183a73"
GREEN = "#2d8b57"
INK = "#141414"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        candidates = [
            r"C:\Windows\Fonts\arial.ttf",
            r"C:\Windows\Fonts\arialbd.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
        ]
        for candidate in candidates:
            if os.path.isfile(candidate):
                return ImageFont.truetype(candidate, size)
        return ImageFont.load_default()


SANS_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
SANS_REG = r"C:\Windows\Fonts\arial.ttf"
SERIF_BOLD = r"C:\Windows\Fonts\timesbd.ttf"

bold = lambda size: font(SANS_BOLD, size)
regular = lambda size: font(SANS_REG, size)
serif = lambda size: font(SERIF_BOLD, size)


def wrap(draw, text, fnt, max_width):
    words = text.split()
    lines, line = [], ""
    for word in words:
        trial = word if not line else line + " " + word
        if draw.textbbox((0, 0), trial, font=fnt)[2] <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def fit_wrap(draw, text, fnt, max_width, max_lines, min_size=18, max_size=38):
    size = max_size
    while size >= min_size:
        trial = font(SANS_BOLD if fnt == "bold" else SANS_REG, size)
        lines = wrap(draw, text, trial, max_width)
        if len(lines) <= max_lines:
            return trial, lines
        size -= 1
    return font(SANS_BOLD if fnt == "bold" else SANS_REG, min_size), wrap(
        draw, text, font(SANS_BOLD if fnt == "bold" else SANS_REG, min_size),
        max_width
    )


def draw_missiles(draw, box):
    x, y, w, h = box
    strip_h = h - 26
    draw.rectangle((x, y, x + w, y + strip_h), fill=NAVY)
    # Stars
    for sx, sy in [(20, 18), (55, 38), (92, 16), (145, 34), (198, 13), (250, 42), (320, 19), (390, 31), (450, 18)]:
        draw.ellipse((x + sx, y + sy, x + sx + 3, y + sy + 3), fill="#d7dce8")
    # explosion stars
    cx, cy = x + w * 0.56, y + 37
    draw.ellipse((cx - 12, cy - 12, cx + 12, cy + 12), fill="#f0a32a")
    draw.ellipse((cx - 6, cy - 6, cx + 6, cy + 6), fill="#fff3b0")
    for dx, dy in [(0, -24), (20, -12), (24, 10), (9, 23), (-18, 18), (-25, -5)]:
        draw.polygon([(cx, cy), (cx + dx * 0.45, cy + dy * 0.45), (cx + dx, cy + dy)], fill="#e55431")
    # missile trails
    draw.line((x + 24, y + strip_h - 23, x + 92, y + 35), fill="#e44b44", width=3)
    draw.polygon([(x + 91, y + 33), (x + 96, y + 39), (x + 88, y + 41)], fill="#e44b44")
    draw.line((x + 155, y + strip_h - 20, x + 224, y + 29), fill="#e44b44", width=3)
    # skyline
    base = y + strip_h - 10
    draw.rectangle((x, base - 18, x + w, base), fill="#090d18")
    buildings = [28, 38, 24, 52, 30, 44, 25, 36, 48, 29]
    bx = x + 8
    for bw, bh in zip(buildings, [22, 18, 25, 30, 21, 27, 19, 23, 31, 20]):
        draw.rectangle((bx, base - bh, bx + bw, base), fill="#090d18")
        bx += bw + 5
    dome_x = x + 362
    draw.rectangle((dome_x - 8, base - 37, dome_x + 8, base), fill="#090d18")
    draw.ellipse((dome_x - 20, base - 48, dome_x + 20, base - 16), fill="#090d18")
    draw.polygon([(dome_x, base - 66), (dome_x - 5, base - 48), (dome_x + 5, base - 48)], fill="#b58a23")
    # Poland flag
    draw.rectangle((x, y + strip_h - 26, x + w, y + strip_h), fill="#ffffff")
    draw.rectangle((x, y + strip_h - 13, x + w, y + strip_h), fill="#c93439")


def draw_stock(draw, box):
    x, y, w, h = box
    draw.rectangle((x, y, x + w, y + h - 26), fill="#fff7f5")
    base = y + h - 38
    heights = [58, 48, 40, 31]
    xs = [x + 35, x + 155, x + 275, x + 395]
    for sx, bh in zip(xs, heights):
        draw.rectangle((sx, base - bh, sx + 70, base), fill=RED)
    points = [(x + 20, y + 18), (x + 125, y + 38), (x + 230, y + 52), (x + 345, y + 69), (x + 444, y + 78)]
    draw.line(points, fill="#8f1d1d", width=5)
    px, py = points[-1]
    draw.polygon([(px - 16, py - 11), (px + 12, py + 2), (px - 3, py + 15)], fill="#8f1d1d")
    label_box = (x + w - 118, y + h - 48, x + w - 4, y + h - 12)
    draw.rectangle(label_box, fill="#fff7f5")
    draw.text((label_box[0] + 4, label_box[1] - 2), "-3.7%", font=bold(30), fill="#8f1d1d")


def draw_scales(draw, box):
    x, y, w, h = box
    draw.rectangle((x, y, x + w, y + h - 26), fill="#fffaf0")
    cx = x + w // 2
    base = y + h - 45
    draw.line((cx, y + 18, cx, base), fill="#6c571c", width=7)
    draw.line((cx - 85, y + 30, cx + 85, y + 30), fill="#7d651d", width=6)
    draw.ellipse((cx - 12, y + 8, cx + 12, y + 32), fill=GOLD)
    for sx in (cx - 80, cx + 80):
        draw.line((cx, y + 30, sx, y + 54), fill="#6c571c", width=3)
        draw.ellipse((sx - 39, y + 50, sx + 39, y + 62), fill="#d0ad53")
        draw.polygon([(sx - 32, y + 62), (sx - 18, y + 78), (sx + 18, y + 78), (sx + 32, y + 62)], fill="#a38329")
    draw.rectangle((cx - 45, base - 8, cx + 45, base), fill="#7d651d")
    draw.polygon([(cx - 62, base), (cx + 62, base), (cx + 45, base + 12), (cx - 45, base + 12)], fill="#a38329")


def draw_eu_uk(draw, box):
    x, y, w, h = box
    draw.rectangle((x, y, x + w, y + h - 26), fill="#f5f8ff")
    eu_cx, uk_cx, cy = x + 170, x + 300, y + 58
    radius = 48
    draw.ellipse((eu_cx - radius, cy - radius, eu_cx + radius, cy + radius), fill="#1f55a4")
    # EU stars
    import math
    for i in range(12):
        a = i * math.pi / 6 - math.pi / 2
        sx = eu_cx + int(38 * math.cos(a))
        sy = cy + int(38 * math.sin(a))
        pts = []
        for j in range(10):
            r = 5 if j % 2 == 0 else 2
            aa = j * math.pi / 5 - math.pi / 2
            pts.append((sx + r * math.cos(aa), sy + r * math.sin(aa)))
        draw.polygon(pts, fill="#f4ce43")
    # UK flag clipped in a circle
    size = radius * 2
    uk = Image.new("RGBA", (size, size), "#163d86")
    ud = ImageDraw.Draw(uk)
    # straight crosses
    ud.rectangle((40, 0, 56, 96), fill="#ffffff")
    ud.rectangle((0, 40, 96, 56), fill="#ffffff")
    ud.rectangle((44, 0, 52, 96), fill="#c8102e")
    ud.rectangle((0, 44, 96, 52), fill="#c8102e")
    # diagonal white stripes
    ud.polygon([(0, 0), (13, 0), (96, 83), (96, 96), (83, 96), (0, 13)], fill="#ffffff")
    ud.polygon([(83, 0), (96, 0), (13, 96), (0, 96), (0, 83)], fill="#ffffff")
    # offset diagonal red stripes
    ud.polygon([(0, 0), (5, 0), (96, 91), (96, 96)], fill="#c8102e")
    ud.polygon([(91, 0), (96, 0), (5, 96), (0, 96)], fill="#c8102e")
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    draw._image.paste(uk, (uk_cx - radius, cy - radius), mask)
    # gold star overlap
    scx, scy = x + 235, y + 3
    pts = []
    import math
    for i in range(10):
        r = 12 if i % 2 == 0 else 5
        a = i * math.pi / 5 - math.pi / 2
        pts.append((scx + r * math.cos(a), scy + r * math.sin(a)))
    draw.polygon(pts, fill="#d6a72e")


def draw_tile(draw, box, accent, headline, caption, illustration):
    x, y, w, h = box
    draw.rectangle((x, y, x + w, y + h), fill="#ffffff", outline="#252525", width=2)
    draw.rectangle((x, y, x + w, y + 9), fill=accent)
    strip_y = y + 9
    strip_h = 78
    illustration(draw, (x + 12, strip_y + 12, w - 24, strip_h))
    text_y = strip_y + 108
    headline_font, headline_lines = fit_wrap(draw, headline, "bold", w - 28, 2, 24, 34)
    for i, line in enumerate(headline_lines):
        draw.text((x + 14, text_y + i * 34), line, font=headline_font, fill=INK)
    cap_y = text_y + len(headline_lines) * 34 + 2
    caption_font, caption_lines = fit_wrap(draw, caption, "regular", w - 28, 4, 18, 21)
    for i, line in enumerate(caption_lines):
        draw.text((x + 14, cap_y + i * 22), line, font=caption_font, fill="#303030")


def draw_capsule(draw, box):
    x, y, w, h = box
    draw.rectangle((x, y, x + w, y + h), fill="#f7fbf8")
    # molecule
    dots = [(25, 29), (58, 20), (82, 48), (48, 62)]
    for i in range(len(dots) - 1):
        draw.line((x + dots[i][0], y + dots[i][1], x + dots[i + 1][0], y + dots[i + 1][1]), fill="#82a8cf", width=3)
    for dx, dy in dots:
        draw.ellipse((x + dx - 6, y + dy - 6, x + dx + 6, y + dy + 6), fill="#397bbd")
    # capsule
    cy = y + 94
    cx = x + 118
    draw.rounded_rectangle((cx - 100, cy - 35, cx + 100, cy + 35), radius=35, fill="#ffffff", outline="#19212b", width=4)
    draw.rounded_rectangle((cx, cy - 35, cx + 100, cy + 35), radius=35, fill="#d94c48")
    draw.rectangle((cx - 2, cy - 35, cx + 2, cy + 35), fill="#19212b")
    # badge
    bcx, bcy = x + w - 38, y + 35
    draw.ellipse((bcx - 25, bcy - 25, bcx + 25, bcy + 25), fill=GREEN)
    draw.rectangle((bcx - 5, bcy - 15, bcx + 5, bcy + 15), fill="#ffffff")
    draw.rectangle((bcx - 15, bcy - 5, bcx + 15, bcy + 5), fill="#ffffff")


def draw_wide(draw, x, y, w, h):
    draw.rectangle((x, y, x + w, y + h), fill="#ffffff", outline="#252525", width=2)
    draw.rectangle((x, y, x + w, y + 9), fill=GREEN)
    draw.rectangle((x + 12, y + 21, x + 250, y + h - 12), fill="#f7fbf8", outline="#d2ddd5", width=1)
    draw_capsule(draw, (x + 12, y + 21, 238, h - 33))
    tx = x + 274
    tw = w - 292
    headline_font, headline_lines = fit_wrap(draw, "CANCER PILL BREAKTHROUGH", "bold", tw, 2, 25, 36)
    headline_y = y + 38
    for i, line in enumerate(headline_lines):
        draw.text((tx, headline_y + i * 36), line, font=headline_font, fill=INK)
    cap_font, cap_lines = fit_wrap(
        draw,
        "Pancreatic cancer pill daraxonrasib makes tumors undetectable in 1 in 12 trial patients",
        "regular",
        tw,
        3,
        20,
        25,
    )
    cap_y = headline_y + len(headline_lines) * 36 + 8
    for i, line in enumerate(cap_lines):
        draw.text((tx, cap_y + i * 25), line, font=cap_font, fill="#303030")


image = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(image)

# Header
draw.rectangle((0, 0, W, 128), fill="#0b0b0b")
draw.rectangle((0, 128, W, 134), fill="#cf2e2e")
masthead = "THE WORLD IN ONE DAY"
mf = serif(48)
mb = draw.textbbox((0, 0), masthead, font=mf)
draw.text(((W - (mb[2] - mb[0])) / 2, 18), masthead, font=mf, fill="#ffffff")
sub = "SATURDAY, NOVEMBER 21, 2026 · WORLD NEWS FRONT PAGE"
sf = bold(20)
sb = draw.textbbox((0, 0), sub, font=sf)
draw.text(((W - (sb[2] - sb[0])) / 2, 86), sub, font=sf, fill="#e4c35b")

# Grid
margin, gap = 28, 14
grid_y, grid_h = 145, 545
tile_w = (W - 2 * margin - gap) // 2
tile_h = (grid_h - gap) // 2
draw_tile(draw, (margin, grid_y, tile_w, tile_h), BLUE,
          "MISSILES LAND IN POLAND",
          "Russia fires 400+ drones and 110 missiles at Ukraine; two missiles come down in Poland, called a provocation",
          draw_missiles)
draw_tile(draw, (margin + tile_w + gap, grid_y, tile_w, tile_h), RED,
          "AI STOCK ROUT",
          "US stocks fall 3.7%; AI sell-off pushes the S&P 500 into correction and erases Nasdaq's 2026 gains",
          draw_stock)
draw_tile(draw, (margin, grid_y + tile_h + gap, tile_w, tile_h), GOLD,
          "MYANMAR RULING: THE FALLOUT",
          "World Court finds Myanmar responsible for genocide against the Rohingya; Myanmar dismisses the ruling",
          draw_scales)
draw_tile(draw, (margin + tile_w + gap, grid_y + tile_h + gap, tile_w, tile_h), DARK_BLUE,
          "UK–EU: BIGGEST DEAL SINCE BREXIT",
          "Britain and the EU sign major post-Brexit agreements in Brussels on food, carbon and youth mobility",
          draw_eu_uk)

# Wide tile
wide_y, wide_h = 704, 204
draw_wide(draw, margin, wide_y, W - 2 * margin, wide_h)

# Footer
draw.rectangle((0, 928, W, H), fill="#0b0b0b")
footer = "ALSO: Iran strikes US bases in Bahrain · COP31 climate talks run past deadline in Antalya · Mexico captures FBI most-wanted cartel boss 'El Chapo Isidro'"
ff = bold(20)
lines = wrap(draw, footer, ff, W - 80)
if len(lines) > 2:
    # Split defensively into exactly two balanced lines
    mid = len(lines[0]) + 1
lines = wrap(draw, footer, ff, 900)
if len(lines) == 1:
    lines = [footer[:len(footer)//2], footer[len(footer)//2:]]
start_y = 948
for i, line in enumerate(lines[:2]):
    bb = draw.textbbox((0, 0), line, font=ff)
    draw.text(((W - (bb[2] - bb[0])) / 2, start_y + i * 27), line, font=ff, fill="#ffffff")

image.save("entry.png", format="PNG", optimize=True)
