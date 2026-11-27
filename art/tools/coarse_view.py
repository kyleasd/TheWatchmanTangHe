import sys
import numpy as np
from PIL import Image

path = sys.argv[1]
cols = int(sys.argv[2]) if len(sys.argv) > 2 else 100
im = Image.open(path).convert("L")
a = np.array(im)
rows = max(1, int(cols * a.shape[0] / a.shape[1] * 0.5))
sm = np.array(im.resize((cols, rows), Image.BOX)).astype(int)
ch = " .:-=+*#%@"
for row in sm:
    print("".join(ch[min(9, (255 - v) * 10 // 256)] for v in row))
