import os
import random
from PIL import Image, ImageDraw, ImageFont

ART = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("\\", "/") + "/"
TILE = os.path.join(ART, "tile")
INK = (31, 27, 22, 255)
PAPER = (239, 230, 210, 255)
ZHE = (138, 90, 59, 255)
FONT = r"C:\Windows\Fonts\simhei.ttf"

COMPARE = [
    ("tile_bing_plain.png", "无描边"),
    ("tile_bing_zhe.png", "赭 #8a5a3b"),
    ("tile_bing.png", "纯白 #ffffff（当前）"),
    ("tile_bing_paper.png", "米白 #efe6d2"),
]


def paper(size, seed=7):
    rnd = random.Random(seed)
    bg = Image.new("RGBA", size, PAPER)
    px = bg.load()
    for y in range(size[1]):
        for x in range(size[0]):
            d = rnd.randint(-4, 4)
            px[x, y] = (PAPER[0] + d, PAPER[1] + d, PAPER[2] + int(d * 0.6), 255)
    return bg


def load(name, scale=1):
    im = Image.open(os.path.join(TILE, name)).convert("RGBA")
    return im.resize((im.width * scale, im.height * scale), Image.NEAREST)


def main():
    W, H = 1400, 1010
    canvas = paper((W, H))
    d = ImageDraw.Draw(canvas)
    f_title = ImageFont.truetype(FONT, 40)
    f_sub = ImageFont.truetype(FONT, 19)
    f_cap = ImageFont.truetype(FONT, 25)
    f_small = ImageFont.truetype(FONT, 17)

    d.text((58, 34), "文字兵 · 墨字 ＋ 1 px 纯白描边", font=f_title, fill=INK)
    d.text((58, 88), "72 × 72 · 格 64 圆角 5 · 淡朱米字格 · 字 44 × 42 留 10 px 边 · 描边走 8 邻域外扩",
           font=f_sub, fill=ZHE)
    d.line([(58, 124), (W - 58, 124)], fill=ZHE, width=2)

    S = 6
    cs = 72 * S
    y0 = 148
    for x, fn, cap, sub in [
        (80, "tile_bing.png", "兵 · 满格", "2 格血 · 近战高攻薄血"),
        (540, "tile_qiu.png", "丘 · 掉一格", "八 被吃掉，格子不动"),
    ]:
        canvas.alpha_composite(load(fn, S), (x, y0))
        d.text((x, y0 + cs + 20), cap, font=f_cap, fill=INK)
        d.text((x, y0 + cs + 52), sub, font=f_small, fill=ZHE)

    ly = y0 + cs + 112
    d.text((58, ly), "描边对比（3×）", font=f_cap, fill=INK)

    cy = ly + 44
    for i, (fn, cap) in enumerate(COMPARE):
        x = 58 + i * (216 + 52)
        canvas.alpha_composite(load(fn, 3), (x, cy))
        d.text((x, cy + 216 + 10), cap, font=f_small, fill=INK)

    out = os.path.join(ART, "tile_preview.png")
    canvas.convert("RGB").save(out, quality=95)
    print(out, canvas.size)


if __name__ == "__main__":
    main()
