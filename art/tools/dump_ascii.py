import os
import sys
from PIL import Image

ART = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("\\", "/") + "/"

PAL = {
    (31, 27, 22): "#",     # 墨
    (138, 90, 59): "=",    # 赭
    (164, 50, 42): "R",    # 朱
    (239, 230, 210): ".",  # 米白
}


def classify(px):
    r, g, b, a = px
    if a < 20:
        return " "
    key = min(PAL.keys(), key=lambda k: (k[0] - r) ** 2 + (k[1] - g) ** 2 + (k[2] - b) ** 2)
    if a < 200:
        return "+"
    return PAL[key]


def dump(path):
    im = Image.open(ART + path).convert("RGBA")
    w, h = im.size
    px = im.load()
    print(f"{path}  {w}x{h}")
    print("   |" + "".join(str(x % 10) for x in range(w)))
    for y in range(h):
        print(f"{y:02d}|" + "".join(classify(px[x, y]) for x in range(w)) + "|")
    print("   |" + "".join("0" if x % 10 == 0 else " " for x in range(w)) + "|")


if __name__ == "__main__":
    dump(sys.argv[1])
