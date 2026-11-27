import os
from PIL import Image, ImageDraw, ImageFont

ART = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("\\", "/") + "/"
OUT = os.path.join(ART, "px")
os.makedirs(OUT, exist_ok=True)

INK = (31, 27, 22)
FONT = r"C:\Windows\Fonts\simhei.ttf"   # 黑体：横竖齐宽，缩到 44 还站得住

CANVAS = (48, 56)
MAXW, MAXH = 44, 44
BASELINE = 47


def render(ch, size):
    f = ImageFont.truetype(FONT, size)
    img = Image.new("L", (size * 3, size * 3), 0)
    ImageDraw.Draw(img).text((size, size), ch, font=f, fill=255)
    bb = img.getbbox()
    return img.crop(bb) if bb else None


def binarize(im, t=128):
    return im.point(lambda v: 255 if v >= t else 0)


def pick(ch):
    best = None
    for s in range(36, 60):
        g = render(ch, s)
        if not g:
            continue
        g = binarize(g)
        bb = g.getbbox()
        w, h = bb[2] - bb[0], bb[3] - bb[1]
        if w <= MAXW and h <= MAXH:
            best = (s, g.crop(bb))
    return best


def despeckle(im):
    px = im.load()
    w, h = im.size
    out = im.copy()
    o = out.load()
    for y in range(h):
        for x in range(w):
            if px[x, y] < 128:
                continue
            nb = 0
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and px[nx, ny] >= 128:
                    nb += 1
            if nb == 0:
                o[x, y] = 0
    return out


def squeeze_blank_rows(im):
    """删掉字内部整行空行：底横和「八」之间那 1 行缝会让腿飘起来"""
    w, h = im.size
    px = im.load()
    ink = [sum(1 for x in range(w) if px[x, y] >= 128) for y in range(h)]
    drop = {y for y in range(1, h - 1) if ink[y] == 0 and ink[y - 1] > 0 and ink[y + 1] > 0}
    if not drop:
        return im, 0
    out = Image.new("L", (w, h - len(drop)), 0)
    i = 0
    for y in range(h):
        if y in drop:
            continue
        out.paste(im.crop((0, y, w, y + 1)), (0, i))
        i += 1
    return out, len(drop)


def bar_blocks(im, frac=0.65):
    """近乎全宽的横：中横约 70% 字宽，底横 100%"""
    w, h = im.size
    px = im.load()
    rows = [y for y in range(h) if sum(1 for x in range(w) if px[x, y] >= 128) >= w * frac]
    blocks = []
    for y in rows:
        if blocks and y == blocks[-1][1] + 1:
            blocks[-1][1] = y
        else:
            blocks.append([y, y])
    return blocks


def even_bars(im, target=4):
    """横统一到 target 行厚：黑体在 50px 上会给 4/3，
    底横往下补一行时直接盖住下面那一行的笔画毛刺（八的起笔只有 1px）"""
    blocks = bar_blocks(im)
    if not blocks:
        return im, 0
    y0, y1 = blocks[-1]
    need = target - (y1 - y0 + 1)
    if need <= 0:
        return im, 0
    out = im.copy()
    strip = im.crop((0, y1, im.size[0], y1 + 1))
    for k in range(need):
        out.paste(strip, (0, y1 + 1 + k))
    return out, need


def cut_legs(im):
    """丘 = 兵砍掉「八」：以最下面那根全宽横的底边为界"""
    w, h = im.size
    blocks = bar_blocks(im, 0.9)
    if not blocks:
        return im
    return im.crop((0, 0, w, blocks[-1][1] + 1))


def to_rgba(im, baseline=BASELINE, canvas=CANVAS):
    w, h = im.size
    x = (canvas[0] - w) // 2
    y = baseline - h + 1
    out = Image.new("RGBA", canvas, (0, 0, 0, 0))
    px = im.load()
    o = out.load()
    for j in range(h):
        for i in range(w):
            if px[i, j] >= 128:
                o[x + i, y + j] = INK + (255,)
    return out


def dump(im, title=""):
    px = im.load()
    w, h = im.size
    print(f"--- {title} {w}x{h} ---")
    for y in range(h):
        print("".join("#" if px[x, y] >= 128 else "." for x in range(w)))


if __name__ == "__main__":
    size, g = pick("兵")
    g = despeckle(g)
    g, dropped = squeeze_blank_rows(g)
    g, added = even_bars(g, 4)
    print(f"bing 兵: font {size}px -> glyph {g.size[0]}x{g.size[1]} "
          f"(blank rows removed {dropped}, bottom bar +{added})")
    dump(g, "bing")
    to_rgba(g).save(os.path.join(OUT, "bing.png"))
    print()

    q = cut_legs(g)
    print(f"qiu 丘: glyph {q.size[0]}x{q.size[1]}")
    dump(q, "qiu")
    to_rgba(q).save(os.path.join(OUT, "qiu.png"))
