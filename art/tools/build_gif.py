import os
import random
from PIL import Image

ART = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("\\", "/") + "/"
PAPER = (239, 230, 210)


def paper(size, seed=11):
    rnd = random.Random(seed)
    bg = Image.new("RGB", size, PAPER)
    px = bg.load()
    for y in range(size[1]):
        for x in range(size[0]):
            d = rnd.randint(-4, 4)
            px[x, y] = (PAPER[0] + d, PAPER[1] + d, PAPER[2] + int(d * 0.6))
    return bg


def main():
    S = 8
    gif = Image.open(ART + "_idle_1x.gif")
    frames = []
    for i in range(gif.n_frames):
        gif.seek(i)
        fr = gif.convert("RGBA")
        big = fr.resize((fr.width * S, fr.height * S), Image.NEAREST)
        bg = paper(big.size, seed=11).convert("RGBA")
        bg.alpha_composite(big)
        frames.append(bg.convert("P", palette=Image.ADAPTIVE, colors=32))
    frames[0].save(ART + "soldier_idle_x8.gif", save_all=True, append_images=frames[1:],
                   duration=380, loop=0, optimize=False, disposal=2)
    print(ART + "soldier_idle_x8.gif", len(frames))


if __name__ == "__main__":
    main()
