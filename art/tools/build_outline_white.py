import os
import random
from PIL import Image, ImageDraw, ImageFont

ART = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("\\", "/") + "/"
TILE = os.path.join(ART, "tile")
INK = (31, 27, 22, 255)
PAPER = (239, 230, 210, 255)
ZHE = (138, 90, 59, 255)
FONT = r"C:\Windows\Fonts\simhei.ttf"

CARDS = [
    ("tile_bing.png", "赭 #8a5a3b", "亮度 98 · 暖中间调 · 纸色之下", "质感向"),
    ("tile_bing_paper.png", "米白 #efe6d2", "亮度 230 · 等于纸 · 只在格线上现形", "干净向"),
    ("tile_bing_white.png", "纯白 #ffffff", "亮度 255 · 比纸更亮 · 泛冷光", "色板外"),
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
    S = 5
    cs = 72 * S
    gap = 46
    W = 2 * 56 + 3 * cs + 2 * gap
    H = 130 + cs + 130
    canvas = paper((W, H))
    d = ImageDraw.Draw(canvas)
    f_title = ImageFont.truetype(FONT, 36)
    f_sub = ImageFont.truetype(FONT, 18)
    f_cap = ImageFont.truetype(FONT, 24)
    f_small = ImageFont.truetype(FONT, 17)

    d.text((56, 26), "纯白描边 ＝ 把字抬到纸面之上", font=f_title, fill=INK)
    d.text((56, 76), "纸 230 已经是画面最亮的一层；255 的边比纸更亮，眼睛读成「发光 / 抠图」，不是「印刷」",
           font=f_sub, fill=ZHE)
    d.line([(56, 108), (W - 56, 108)], fill=ZHE, width=2)

    y0 = 128
    for i, (fn, cap, sub, tag) in enumerate(CARDS):
        x = 56 + i * (cs + gap)
        canvas.alpha_composite(load(fn, S), (x, y0))
        d.text((x, y0 + cs + 16), cap, font=f_cap, fill=INK)
        d.text((x, y0 + cs + 48), sub, font=f_small, fill=ZHE)
        d.text((x, y0 + cs + 72), tag, font=f_small, fill=ZHE)

    out = os.path.join(ART, "outline_white.png")
    canvas.convert("RGB").save(out, quality=95)
    print(out, canvas.size)


if __name__ == "__main__":
    main()
