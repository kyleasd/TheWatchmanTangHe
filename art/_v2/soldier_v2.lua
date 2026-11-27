-- ============================================================
--  文字兵 v2 · 「兵」 — 48×56，逐行手排像素（不用公式填色）
--  字骨取楷体字面：短撇 → 左长竖 → 中横 → 竖 → 底横 → 八
--  用法：aseprite -b --script soldier_v2.lua
-- ============================================================
local OUT = "G:\\Study\\The Watchman - TangHe\\art\\"

local W, H = 48, 56

local C = {
	ink   = { 31, 27, 22 },
	zhu   = { 164, 50, 42 },
	zhe   = { 138, 90, 59 },
	dian  = { 47, 72, 88 },
	paper = { 239, 230, 210 },
}
local function col(c, a) return Color{ r = c[1], g = c[2], b = c[3], a = a or 255 } end

----------------------------------------------------------------
-- 笔画：全部写成 {y, x0, x1} 的横条，一根一根摆
----------------------------------------------------------------
-- 撇：头在字心偏右 (x24..29)，一路扫到左竖顶端 (x11..13)，笔锋渐细
local RUN_XIE = {
	{ 4, 24, 29 },
	{ 5, 23, 28 },
	{ 6, 21, 27 },
	{ 7, 19, 26 },
	{ 8, 17, 24 },
	{ 9, 15, 22 },
	{ 10, 13, 19 },
	{ 11, 11, 16 },
	{ 12, 11, 13 },
}
-- 宋版撇：头更肥（7 宽），锋更尖（2 宽）
local RUN_XIE_SONG = {
	{ 4, 23, 29 },
	{ 5, 22, 28 },
	{ 6, 20, 26 },
	{ 7, 18, 25 },
	{ 8, 16, 23 },
	{ 9, 14, 21 },
	{ 10, 12, 18 },
	{ 11, 11, 15 },
	{ 12, 11, 12 },
}
-- 盔缨（「朱缨」变体）：头顶一小簇朱
local RUN_CREST = {
	{ 0, 24, 26 },
	{ 1, 23, 27 },
	{ 2, 23, 27 },
	{ 3, 24, 27 },
}

local function newMask()
	local m = {}
	for y = 0, H - 1 do
		local row = {}
		for x = 0, W - 1 do row[x] = false end
		m[y] = row
	end
	return m
end
local function hbar(m, y, x0, x1, dy)
	for x = x0, x1 do
		local yy = y + (dy or 0)
		if x >= 0 and x < W and yy >= 0 and yy < H then m[yy][x] = true end
	end
end
local function vbar(m, x0, x1, y0, y1, dy)
	for y = y0, y1 do for x = x0, x1 do hbar(m, y, x, x, dy) end end
end

local function buildGlyph(opt)
	opt = opt or {}
	local dy = opt.bob or 0
	local song = (opt.style == "song")
	local m = newMask()
	for _, r in ipairs(song and RUN_XIE_SONG or RUN_XIE) do hbar(m, r[1], r[2], r[3], dy) end
	if song then
		vbar(m, 11, 13, 11, 35, dy) -- 左长竖 3 宽
		vbar(m, 11, 39, 18, 21, dy) -- 中横 4 厚
		vbar(m, 28, 30, 21, 35, dy) -- 竖二 3 宽
		vbar(m, 3, 44, 32, 35, dy)  -- 底横 4 厚
		-- 宋刻的顿笔：横的右端往上一挑
		hbar(m, 17, 37, 39, dy)
		hbar(m, 16, 38, 39, dy)
		hbar(m, 31, 42, 44, dy)
		hbar(m, 30, 43, 44, dy)
	else
		vbar(m, 11, 14, 11, 35, dy) -- 左长竖 4 宽
		vbar(m, 11, 39, 18, 21, dy) -- 中横
		vbar(m, 27, 30, 21, 35, dy) -- 竖二 4 宽
		vbar(m, 3, 44, 32, 35, dy)  -- 底横
	end
	if opt.legs ~= false then
		for i = 0, 11 do hbar(m, 36 + i, 16 - i, 19 - i, dy) end -- 八·左撇
		for i = 0, 8 do
			local x1 = (i >= 6) and (31 + i) or (29 + i)
			hbar(m, 36 + i, 27 + i, x1, dy) -- 八·右捺
		end
	end
	return m
end

----------------------------------------------------------------
-- 上色
----------------------------------------------------------------
local function paintInk(img, m)
	for y = 0, H - 1 do for x = 0, W - 1 do
		if m[y][x] then img:putPixel(x, y, col(C.ink)) end
	end end
end

-- 错版：整字往右下偏 1px 的赭影，像印偏了一道
local function paintEcho(img, m, alpha)
	for y = H - 1, 0, -1 do for x = W - 1, 0, -1 do
		if m[y][x] then img:putPixel(x + 1, y + 1, col(C.zhe, alpha or 80)) end
	end end
end

local function paintCrest(img)
	for _, r in ipairs(RUN_CREST) do
		for x = r[2], r[3] do img:putPixel(x, r[1], col(C.zhu)) end
	end
end

local function paintOutline(img, m)
	for y = 0, H - 1 do for x = 0, W - 1 do
		if not m[y][x] then
			local near = false
			for dy = -1, 1 do for dx = -1, 1 do
				local nx, ny = x + dx, y + dy
				if nx >= 0 and ny >= 0 and nx < W and ny < H and m[ny][nx] then near = true end
			end end
			if near then img:putPixel(x, y, col(C.paper)) end
		end
	end end
end

local function paintShadow(img)
	for y = 47, 51 do for x = 0, W - 1 do
		local dx = (x - 24) / 16.5
		local dy = (y - 49.0) / 1.9
		local d = dx * dx + dy * dy
		if d <= 1.0 then img:putPixel(x, y, col(C.ink, math.floor(120 - d * 60))) end
	end end
end

----------------------------------------------------------------
-- 单帧导出
----------------------------------------------------------------
local function exportPNG(path, opt)
	opt = opt or {}
	local s = Sprite(W, H, ColorMode.RGB)
	for i = #s.layers, 1, -1 do s:deleteLayer(s.layers[i]) end
	local m = buildGlyph{ legs = opt.legs, style = opt.style }
	if opt.shadow then paintShadow(s:newCel(s:newLayer(), 1).image) end
	if opt.outline then paintOutline(s:newCel(s:newLayer(), 1).image, m) end
	local img = s:newCel(s:newLayer(), 1).image
	if opt.echo then paintEcho(img, m, opt.echo) end
	paintInk(img, m)
	if opt.crest then paintCrest(img) end
	s:saveCopyAs(path)
end

exportPNG(OUT .. "v2_ink.png", {})                -- A 墨
exportPNG(OUT .. "v2_echo.png", { echo = 80 })    -- B 错版
exportPNG(OUT .. "v2_crest.png", { crest = true }) -- C 朱缨
exportPNG(OUT .. "v2_song.png", { style = "song" }) -- D 宋版
exportPNG(OUT .. "v2_qiu.png", { legs = false })  -- 拆字：丘
exportPNG(OUT .. "v2_qiu_song.png", { legs = false, style = "song" }) -- 宋版丘
exportPNG(OUT .. "v2_wall.png", { outline = true, shadow = true })

----------------------------------------------------------------
-- 正式文件（2 帧待机 + 3 图层）
----------------------------------------------------------------
local spr = Sprite(W, H, ColorMode.RGB)
for i = #spr.layers, 1, -1 do spr:deleteLayer(spr.layers[i]) end
local L = {}
for _, name in ipairs{ "影", "描边", "字" } do
	L[name] = spr:newLayer()
	L[name].name = name
end
spr:newEmptyFrame(2)
for f = 1, 2 do
	local bob = (f == 2) and -1 or 0
	local m = buildGlyph{ bob = bob }
	paintShadow(spr:newCel(L["影"], f).image)
	paintOutline(spr:newCel(L["描边"], f).image, m)
	paintInk(spr:newCel(L["字"], f).image, m)
end
L["影"].isVisible = false
L["描边"].isVisible = false

pcall(function()
	local pal = Palette(5)
	for i, c in ipairs{ C.ink, C.zhu, C.zhe, C.dian, C.paper } do pal:setColor(i - 1, col(c)) end
	spr:setPalette(pal)
end)

spr:saveAs(OUT .. "bing_v2.aseprite")
spr:saveCopyAs(OUT .. "_idle_1x.gif")
print("V2 OK: layers=" .. #spr.layers .. " frames=" .. #spr.frames)
