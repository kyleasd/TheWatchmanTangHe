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
    ("tile_bing_plain.png", "无描边", "基线：字和格线贴在一起", "—"),
    ("tile_bing.png", "赭 #8a5a3b", "暖中间调，边缘像墨洇开", "当前"),
    ("tile_bing_dian.png", "靛 #2f4858", "冷色暗边，像环境反光", "备选"),
    ("tile_bing_paper.png", "米白 #efe6d2", "剥白边，分离最强", "备选"),
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
    S = 4
    cs = 72 * S
    gap = 40
    W = 80 * 2 + 4 * cs + 3 * gap
    H = 470
    canvas = paper((W, H))
    d = ImageDraw.Draw(canvas)
    f_title = ImageFont.truetype(FONT, 34)
    f_sub = ImageFont.truetype(FONT, 18)
    f_cap = ImageFont.truetype(FONT, 22)
    f_small = ImageFont.truetype(FONT, 16)

    d.text((56, 26), "描边色为什么是赭", font=f_title, fill=INK)
    d.text((56, 72), "墨 27 → 赭 98 → 纸 230（相对亮度）：1 px 的中间调在边缘做出一级台阶，眼睛读成「墨洇开」而不是「贴了个边」",
           font=f_sub, fill=ZHE)
    d.line([(56, 104), (W - 56, 104)], fill=ZHE, width=2)

    y0 = 126
    for i, (fn, cap, sub, tag) in enumerate(CARDS):
        x = 56 + i * (cs + gap)
        canvas.alpha_composite(load(fn, S), (x, y0))
        d.text((x, y0 + cs + 14), cap, font=f_cap, fill=INK)
        d.text((x, y0 + cs + 44), sub, font=f_small, fill=ZHE)
        d.text((x, y0 + cs + 66), tag, font=f_small, fill=ZHE)

    out = os.path.join(ART, "outline_colors.png")
    canvas.convert("RGB").save(out, quality=95)
    print(out, canvas.size)


if __name__ == "__main__":
    main()
