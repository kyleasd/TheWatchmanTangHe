import os
import random
from PIL import Image, ImageDraw, ImageFont

ART = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("\\", "/") + "/"
PX = os.path.join(ART, "px")
INK = (31, 27, 22, 255)
PAPER = (239, 230, 210, 255)
ZHE = (138, 90, 59, 255)
FONT = r"C:\Windows\Fonts\simhei.ttf"

CANVAS = (48, 56)
BASELINE = 47  # 字形底边落在这一行


def paper(size, seed=7):
    rnd = random.Random(seed)
    bg = Image.new("RGBA", size, PAPER)
    px = bg.load()
    for y in range(size[1]):
        for x in range(size[0]):
            d = rnd.randint(-4, 4)
            px[x, y] = (PAPER[0] + d, PAPER[1] + d, PAPER[2] + int(d * 0.6), 255)
    return bg


def load(name, scale):
    im = Image.open(os.path.join(PX, name)).convert("RGBA")
    return im.resize((im.width * scale, im.height * scale), Image.NEAREST)


def bloodbar(d, x, y, cells, total):
    cw, chh, gap, b = 24, 10, 4, 2
    for i in range(total):
        cx = x + i * (cw + gap)
        fill = ZHE if i < cells else PAPER
        d.rectangle([cx, y, cx + cw, y + chh], fill=fill, outline=INK, width=b)


def main():
    W, H = 1400, 860
    canvas = paper((W, H))
    d = ImageDraw.Draw(canvas)
    f_title = ImageFont.truetype(FONT, 40)
    f_sub = ImageFont.truetype(FONT, 19)
    f_cap = ImageFont.truetype(FONT, 25)
    f_small = ImageFont.truetype(FONT, 17)

    d.text((58, 34), "像素兵字 · 「兵」", font=f_title, fill=INK)
    d.text((58, 88), "黑体 50 px 直接阈值化 · 去掉抗锯齿渣点与字内空缝 · 48 × 56 画布 · 墨 #1f1b16",
           font=f_sub, fill=ZHE)
    d.line([(58, 124), (W - 58, 124)], fill=ZHE, width=2)

    S = 8
    cw, ch = 48 * S, 56 * S
    x1, y0 = 120, 152
    x2 = x1 + cw + 80
    for x, fn, cap, sub in [
        (x1, "bing.png", "兵 · 2 格血", "近战 · 高攻 · 低甲 · 薄血 · 快"),
        (x2, "qiu.png", "丘 · 1 格血", "八 掉了，字矮一截，脚底还在同一条地面线"),
    ]:
        d.rectangle([x - 14, y0 - 14, x + cw + 14, y0 + ch + 14], outline=(31, 27, 22, 34), width=1)
        canvas.alpha_composite(load(fn, S), (x, y0))
        d.text((x - 4, y0 + ch + 26), cap, font=f_cap, fill=INK)
        d.text((x - 4, y0 + ch + 58), sub, font=f_small, fill=ZHE)

    # 游戏内 2× 比例
    ly = y0 + ch + 112
    d.text((58, ly), "游戏内 2×（1080p：96 × 112，字高 84）—— 同屏可读性", font=f_cap, fill=INK)
    uy = ly + 42
    row = ["bing.png"] * 3 + ["qiu.png"] + ["bing.png"] * 2
    for i, fn in enumerate(row):
        x = 58 + i * (96 + 26)
        canvas.alpha_composite(load(fn, 2), (x, uy))
        bloodbar(d, x + 18, uy + 114, 1 if fn == "qiu.png" else 2, 2)

    out = os.path.join(ART, "pixel_bing_preview.png")
    canvas.convert("RGB").save(out, quality=95)
    print(out)


if __name__ == "__main__":
    main()
