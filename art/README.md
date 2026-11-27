# art/ — 文字兵像素资产

## 现行版本：米字格底 + 像素「兵」

字用黑体 50 px 阈值化成像素；外面套一个**圆角正方形米字格**当底座，字压在格线上。
这样它不再是一坨悬空的黑字，而是一枚可点选的"活字块"。

| 文件 | 说明 |
|---|---|
| `tile/tile_bing.aseprite` | **源文件**：64 × 64，内置项目 5 色板 |
| `tile/tile_bing.png` | 兵 · 满格 |
| `tile/tile_qiu.aseprite` / `.png` | 丘 · 掉一格（同一份像素砍掉「八」，格子不动） |
| `px/bing.png` / `px/qiu.png` | 光字版（不带格），48 × 56，给别的用途 |
| `tile_preview.png` | 6× 大图 + 游戏内 2× + 1× 实际像素 |
| `pixel_bing_preview.png` | 上一版（只有字，没有格） |

**方块规格**：画布 72 × 72；格子 64 × 64（边距 4）；圆角 5；格口 1 px 淡朱 `#c0766a`（朱 62% 混纸）；
米字 1 px 淡朱 `#d2a292`（朱 38% 混纸），竖中 / 横中 / 两斜，从格口内角到对角，实线。

**字规格**：字面 44 × 42，居中（每边留 10 px），墨 `#1f1b16`，
外加 **1 px 纯白 `#ffffff` 外描边**（8 邻域外扩）。

> 纯白在 5 色主色板之外，是**按决定加入的描边/状态色**，不参与主色板推导。
> 后果要记住：地面单位白边之后，设计稿 §2.12「墙顶用米白描边」会比地面更暗——
> 上墙的靠色得改成「白边 2 px / 投影 / 字号大 1 档」，不能再用米白。

描边方案留档：`tile/tile_bing_plain.png`（无）、`tile_bing_zhe.png`（赭）、`tile_bing_paper.png`（米白）、`tile_bing_dian.png`（靛）。

`_v1/`（黑体公式填色）、`_v2/`（手排像素 + 宋刻/错版/朱缨）是前两轮，留档对照。

## 重新生成

```powershell
# 1. 字：黑体阈值化 → px/bing.png、px/qiu.png
python art/tools/pixelate.py

# 2. 套米字格 → tile/tile_bing.png、tile/tile_qiu.png
python art/tools/build_tile.py

# 3. 收进 Aseprite 文件（写入 5 色板）
& "G:\Study\Aseprite-v1.3.18.5-Source\build\bin\aseprite.exe" -b --script art/tools/package_tile.lua

# 4. 预览图
python art/tools/build_preview_tile.py

# 终端校对
python art/tools/dump_ascii.py px\bing.png
```

方块参数都在 `build_tile.py` 顶部：`TILE` / `R`（圆角）/ `FRAME_A` / `GUIDE_A`（线浓）；
描边色由 `build(..., outline=)` 决定：`ZHE`（赭，默认）/ `None`（不描）/ `PAPER`（米白）。
