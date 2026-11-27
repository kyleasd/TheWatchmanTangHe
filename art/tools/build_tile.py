import os
from PIL import Image

ART = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("\\", "/") + "/"
OUT = os.path.join(ART, "tile")
os.makedirs(OUT, exist_ok=True)

INK = (31, 27, 22)
PAPER = (239, 230, 210)
ZHU = (164, 50, 42)
ZHE = (138, 90, 59)

CANVAS = 72
TILE = 64
M = (CANVAS - TILE) // 2
R = 5

FRAME_A = 0.62
GUIDE_A = 0.38


def blend(c, paper, a):
    return tuple(int(round(c[i] * a + paper[i] * (1 - a))) for i in range(3))


FRAME = blend(ZHU, PAPER, FRAME_A)
GUIDE = blend(ZHU, PAPER, GUIDE_A)


def rounded_mask(size, radius):
    m = [[False] * size for _ in range(size)]
    for y in range(size):
        for x in range(size):
            cx = min(max(x, radius), size - 1 - radius)
            cy = min(max(y, radius), size - 1 - radius)
            dx, dy = x - cx, y - cy
            if dx * dx + dy * dy <= radius * radius + radius:
                m[y][x] = True
    return m


def outline_pts(mask, size):
    pts = set()
    for y in range(size):
        xs = [x for x in range(size) if mask[y][x]]
        if xs:
            pts.add((xs[0], y))
            pts.add((xs[-1], y))
    for x in range(size):
        ys = [y for y in range(size) if mask[y][x]]
        if ys:
            pts.add((x, ys[0]))
            pts.add((x, ys[-1]))
    return pts


def bres(x0, y0, x1, y1):
    pts = []
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    x, y = x0, y0
    while True:
        pts.append((x, y))
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy
    return pts


def build(glyph_path, out_name, outline=None):
    img = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    px = img.load()
    mask = rounded_mask(TILE, R)

    # 1. 格内纸底
    for y in range(TILE):
        for x in range(TILE):
            if mask[y][x]:
                px[M + x, M + y] = PAPER + (255,)

    # 2. 格口 1px
    for x, y in outline_pts(mask, TILE):
        px[M + x, M + y] = FRAME + (255,)

    # 3. 米字 1px
    lo, hi = 1, TILE - 2
    mid = TILE // 2
    for pts in (
        bres(mid, lo, mid, hi),
        bres(lo, mid, hi, mid),
        bres(lo, lo, hi, hi),
        bres(hi, lo, lo, hi),
    ):
        for x, y in pts:
            if mask[y][x]:
                px[M + x, M + y] = GUIDE + (255,)

    # 4. 字
    g = Image.open(glyph_path).convert("RGBA")
    g = g.crop(g.getbbox())
    gw, gh = g.size
    gp = g.load()
    gx = (CANVAS - gw) // 2
    gy = (CANVAS - gh) // 2

    def ink(x, y):
        return 0 <= x < gw and 0 <= y < gh and gp[x, y][3] > 128

    # 5. 描边（8 邻域外扩 1px）
    if outline:
        for y in range(-1, gh + 1):
            for x in range(-1, gw + 1):
                if ink(x, y):
                    continue
                hit = False
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        if ink(x + dx, y + dy):
                            hit = True
                if hit:
                    cx, cy = gx + x, gy + y
                    if 0 <= cx < CANVAS and 0 <= cy < CANVAS:
                        px[cx, cy] = outline + (255,)

    img.alpha_composite(g, (gx, gy))
    print(f"{out_name}: 字 {gw}x{gh} @ ({gx},{gy})，描边 {outline}")
    img.save(os.path.join(OUT, out_name + ".png"))
    return img


def dump(img, title=""):
    px = img.load()
    w, h = img.size
    print(f"--- {title} {w}x{h} ---")
    for y in range(h):
        row = []
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 30:
                row.append(" ")
            elif (r, g, b) == INK:
                row.append("#")
            elif (r, g, b) == PAPER:
                row.append(".")
            elif (r, g, b) == ZHE:
                row.append("+")
            elif (r, g, b) == FRAME:
                row.append("o")
            elif (r, g, b) == GUIDE:
                row.append(":")
            else:
                row.append("?")
        print("".join(row))


WHITE = (255, 255, 255)

if __name__ == "__main__":
    # 定稿：1 px 纯白描边
    bing = build(os.path.join(ART, "px", "bing.png"), "tile_bing", WHITE)
    dump(bing, "tile_bing")
    build(os.path.join(ART, "px", "qiu.png"), "tile_qiu", WHITE)

    # 留档：其他描边方案
    build(os.path.join(ART, "px", "bing.png"), "tile_bing_plain", None)
    build(os.path.join(ART, "px", "bing.png"), "tile_bing_zhe", ZHE)
    build(os.path.join(ART, "px", "bing.png"), "tile_bing_paper", PAPER)
    DIAN = (47, 72, 88)
    build(os.path.join(ART, "px", "bing.png"), "tile_bing_dian", DIAN)
