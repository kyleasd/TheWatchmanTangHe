import os
import random
from PIL import Image, ImageDraw, ImageFont

ART = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("\\", "/") + "/"
INK = (31, 27, 22, 255)
PAPER = (239, 230, 210, 255)
ZHE = (138, 90, 59, 255)
FONT = r"C:\Windows\Fonts\simhei.ttf"

PALETTE = [("墨", "1f1b16", (31, 27, 22)), ("朱", "a4322a", (164, 50, 42)),
           ("赭", "8a5a3b", (138, 90, 59)), ("靛", "2f4858", (47, 72, 88)),
           ("米白", "efe6d2", (239, 230, 210))]

CARDS = [
    ("v2_ink.png", "A · 墨", "纯墨，不施一点装饰；笔画齐宽 4 px"),
    ("v2_song.png", "B · 宋刻", "横粗竖细 + 顿笔，木刻书的味道"),
    ("v2_echo.png", "C · 错版", "赭色套印偏一格，像手工刷印的毛边"),
    ("v2_crest.png", "D · 朱缨", "头顶一簇朱，不看字也认得出是兵"),
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


def load(name, scale):
    im = Image.open(ART + name).convert("RGBA")
    return im.resize((im.width * scale, im.height * scale), Image.NEAREST)


def bloodbar(d, x, y, cells, total):
    cw, chh, gap, b = 24, 10, 4, 2
    for i in range(total):
        cx = x + i * (cw + gap)
        if i < cells:
            d.rectangle([cx, y, cx + cw, y + chh], fill=ZHE, outline=INK, width=b)
        else:
            d.rectangle([cx, y, cx + cw, y + chh], fill=PAPER, outline=INK, width=b)


def main():
    W, H = 1400, 930
    canvas = paper((W, H))
    d = ImageDraw.Draw(canvas)
    f_title = ImageFont.truetype(FONT, 40)
    f_sub = ImageFont.truetype(FONT, 19)
    f_cap = ImageFont.truetype(FONT, 25)
    f_small = ImageFont.truetype(FONT, 17)

    d.text((58, 34), "文字兵 v2 · 「兵」 四个取向", font=f_title, fill=INK)
    d.text((58, 88), "48 × 56 · 逐行手排像素 · 撇取楷体字面（头粗锋尖）· 字骨 = 丘 + 八",
           font=f_sub, fill=ZHE)
    d.line([(58, 124), (W - 58, 124)], fill=ZHE, width=2)

    S = 6
    cw, ch = 48 * S, 56 * S
    gap = 28
    x0 = (W - (4 * cw + 3 * gap)) // 2
    y0 = 148
    for i, (fn, cap, sub) in enumerate(CARDS):
        x = x0 + i * (cw + gap)
        d.rectangle([x - 14, y0 - 14, x + cw + 14, y0 + ch + 14], outline=(31, 27, 22, 34), width=1)
        canvas.alpha_composite(load(fn, S), (x, y0))
        d.text((x - 4, y0 + ch + 26), cap, font=f_cap, fill=INK)
        d.text((x - 4, y0 + ch + 58), sub, font=f_small, fill=ZHE)

    # 同屏比例
    ly = y0 + ch + 110
    d.text((58, ly), "游戏内比例 2× —— 同屏可读性 · 2 格血条对应 兵 → 丘", font=f_cap, fill=INK)

    uy = ly + 42
    row = ["v2_song.png"] * 3 + ["v2_qiu_song.png"] + ["v2_song.png"] * 2
    for i, fn in enumerate(row):
        x = 58 + i * (96 + 26)
        canvas.alpha_composite(load(fn, 2), (x, uy))
        bloodbar(d, x + 18, uy + 114, 1 if "qiu" in fn else 2, 2)

    # 色板
    py = H - 48
    for i, (name, hexv, rgb) in enumerate(PALETTE):
        x = 58 + i * 108
        d.rectangle([x, py, x + 22, py + 22], fill=rgb + (255,), outline=(31, 27, 22, 90))
        d.text((x + 30, py - 2), name, font=f_small, fill=INK)
    d.text((W - 520, py), "字形 42 × 44 · 撇 7→2 宽 · 八：左撇 4 宽 / 右捺 3→5 宽",
           font=f_small, fill=ZHE)

    out = ART + "soldier_v2_preview.png"
    canvas.convert("RGB").save(out, quality=95)
    print(out)


if __name__ == "__main__":
    main()
