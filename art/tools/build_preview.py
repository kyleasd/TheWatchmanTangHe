import os
import random
from PIL import Image, ImageDraw, ImageFont

ART = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("\\", "/") + "/"
INK = (31, 27, 22, 255)
PAPER = (239, 230, 210, 255)
ZHE = (138, 90, 59, 255)
ZHU = (164, 50, 42, 255)

PALETTE = [("墨", "1f1b16", (31, 27, 22)), ("朱", "a4322a", (164, 50, 42)),
           ("赭", "8a5a3b", (138, 90, 59)), ("靛", "2f4858", (47, 72, 88)),
           ("米白", "efe6d2", (239, 230, 210))]

FONT = r"C:\Windows\Fonts\simhei.ttf"


def paper(size, seed=7):
    rnd = random.Random(seed)
    bg = Image.new("RGBA", size, PAPER)
    px = bg.load()
    for y in range(size[1]):
        for x in range(size[0]):
            d = rnd.randint(-5, 5)
            px[x, y] = (PAPER[0] + d, PAPER[1] + d, PAPER[2] + int(d * 0.6), 255)
    return bg


def load(name, scale):
    im = Image.open(ART + name).convert("RGBA")
    return im.resize((im.width * scale, im.height * scale), Image.NEAREST)


def main():
    W, H = 1400, 1010
    canvas = paper((W, H))
    d = ImageDraw.Draw(canvas)

    f_title = ImageFont.truetype(FONT, 42)
    f_sub = ImageFont.truetype(FONT, 20)
    f_cap = ImageFont.truetype(FONT, 24)
    f_small = ImageFont.truetype(FONT, 18)

    # 标题
    d.text((60, 42), "文字兵 · 「兵」", font=f_title, fill=INK)
    d.text((60, 96), "48 × 56 px  ·  5 色  ·  Aseprite 逐笔生成  ·  字骨 = 丘 + 八", font=f_sub, fill=ZHE)
    d.line([(60, 132), (W - 60, 132)], fill=ZHE, width=2)

    cards = [
        ("bing.png", "兵  ·  2 血格（满）", "近战 · 高攻 · 低甲 · 薄血 · 快"),
        ("qiu.png", "丘  ·  掉一格（兵 → 丘）", "八 两撇捺被吃掉，字还剩一半"),
        ("bing_wall.png", "墙顶态  ·  米白描边 + 脚下投影", "字号大 1 档 · 射程 +1 · 伤害 +30%"),
    ]

    S = 8
    cw, ch = 48 * S, 56 * S
    gap = 32
    x0 = 60
    y0 = 170
    for i, (fn, cap, sub) in enumerate(cards):
        x = x0 + i * (cw + gap + 16)
        sprite = load(fn, S)
        # 卡片底：极淡的墨 5% 方框
        box = [x - 14, y0 - 14, x + cw + 14, y0 + ch + 14]
        d.rectangle(box, outline=(31, 27, 22, 30), width=1)
        canvas.alpha_composite(sprite, (x, y0))
        d.text((x - 4, y0 + ch + 26), cap, font=f_cap, fill=INK)
        d.text((x - 4, y0 + ch + 58), sub, font=f_small, fill=ZHE)

    # 底部：游戏内比例
    yb = y0 + ch + 118
    d.text((60, yb), "游戏内比例 2×（1080p 基准）—— 同屏可读性", font=f_cap, fill=INK)

    y2 = yb + 44
    scale2 = 2
    sw, sh = 48 * scale2, 56 * scale2
    row = ["bing.png", "bing.png", "bing.png", "qiu.png", "bing.png", "bing.png"]
    for i, fn in enumerate(row):
        x = 60 + i * (sw + 26)
        canvas.alpha_composite(load(fn, scale2), (x, y2))

    # 调色板
    px0 = 60
    py0 = y2 + sh + 34
    d.text((px0, py0 - 30), "调色板", font=f_small, fill=ZHE)
    for i, (name, hexv, rgb) in enumerate(PALETTE):
        x = px0 + i * 120
        d.rectangle([x, py0, x + 28, py0 + 28], fill=rgb + (255,), outline=(31, 27, 22, 90))
        d.text((x + 36, py0 - 2), name, font=f_small, fill=INK)
        d.text((x + 36, py0 + 20), "#" + hexv, font=ImageFont.truetype(FONT, 14), fill=ZHE)

    out = ART + "soldier_preview.png"
    canvas.convert("RGB").save(out, quality=95)
    print(out)


if __name__ == "__main__":
    main()
