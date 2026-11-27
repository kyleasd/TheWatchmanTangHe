-- ============================================================
--  文字兵 · 「兵」 — 在 Aseprite 里逐笔生成的像素字形
--  字骨：兵 = 丘（撇 + 左长竖 + 中横 + 竖 + 底横） + 八（两撇捺）
--  用法：aseprite -b --script soldier_gen.lua
--  调色板：墨 #1f1b16 / 朱 #a4322a / 赭 #8a5a3b / 靛 #2f4858 / 米白 #efe6d2
-- ============================================================
local function _dirname(p) return p:match("^(.*)[/\\][^/\\]*$") end
local _here = (debug.getinfo(1, "S").source:gsub("^@", "")):gsub("\\", "/")
local _dir = _dirname(_here)
local ART = _dir:match("(.*)/tools$") or _dir
local OUT = ART .. "/"

local W, H = 48, 56
local GY = 2 -- 字形整体上留白

local C = {
	ink   = { 31, 27, 22 },
	zhu   = { 164, 50, 42 },
	zhe   = { 138, 90, 59 },
	dian  = { 47, 72, 88 },
	paper = { 239, 230, 210 },
}
local function col(c, a) return Color{ r = c[1], g = c[2], b = c[3], a = a or 255 } end

----------------------------------------------------------------
-- 掩膜
----------------------------------------------------------------
local function newMask()
	local m = {}
	for y = 0, H - 1 do
		local row = {}
		for x = 0, W - 1 do row[x] = false end
		m[y] = row
	end
	return m
end
local function setM(m, x, y)
	if x >= 0 and y >= 0 and x < W and y < H then m[y][x] = true end
end
local function rectM(m, x0, y0, x1, y1)
	for y = y0, y1 do for x = x0, x1 do setM(m, x, y) end end
end
local function maskAt(m, x, y)
	if x < 0 or y < 0 or x >= W or y >= H then return false end
	return m[y][x]
end
-- 变宽笔触：沿线段铺一条粗细渐变的胶囊
local function segM(m, x0, y0, x1, y1, t0, t1)
	local dx, dy = x1 - x0, y1 - y0
	local L2 = dx * dx + dy * dy
	local r = math.max(t0, t1) / 2 + 1
	for yy = math.floor(math.min(y0, y1) - r), math.ceil(math.max(y0, y1) + r) do
		for xx = math.floor(math.min(x0, x1) - r), math.ceil(math.max(x0, x1) + r) do
			local u = ((xx - x0) * dx + (yy - y0) * dy) / L2
			if u < 0 then u = 0 elseif u > 1 then u = 1 end
			local d = math.sqrt((xx - (x0 + dx * u)) ^ 2 + (yy - (y0 + dy * u)) ^ 2)
			if d <= (t0 + (t1 - t0) * u) / 2 then setM(m, xx, yy) end
		end
	end
end

----------------------------------------------------------------
-- 字骨
----------------------------------------------------------------
local function buildGlyph(opt)
	opt = opt or {}
	local m = newMask()
	local B = (opt.bob or 0) + GY

	segM(m, 37, 3 + B, 16, 6 + B, 5.6, 2.4)   -- 撇（头粗尾细）
	rectM(m, 12, 6 + B, 15, 31 + B)           -- 左长竖
	rectM(m, 12, 14 + B, 40, 17 + B)          -- 中横
	rectM(m, 28, 17 + B, 31, 31 + B)          -- 竖二
	rectM(m, 3, 28 + B, 44, 31 + B)           -- 底横（字的地基）

	if opt.legs ~= false then
		segM(m, 19, 32 + B, 7, 44 + B, 5.0, 3.0) -- 八·左撇
		segM(m, 29, 32 + B, 40, 43 + B, 3.6, 5.0) -- 八·右捺
	end
	return m
end

----------------------------------------------------------------
-- 上色
----------------------------------------------------------------
local function paintInk(img, m)
	for y = 0, H - 1 do
		for x = 0, W - 1 do
			if m[y][x] then img:putPixel(x, y, col(C.ink)) end
		end
	end
end

-- 刀痕：赭腰带 + 米白干笔（默认只在墨里开口子）
local function paintMark(img, m, style, bob)
	local B = (bob or 0) + GY
	if style.belt then
		local y = 30 + B
		for x = 7, 40 do
			if maskAt(m, x, y) and maskAt(m, x, y + 1) and maskAt(m, x, y - 1) then
				img:putPixel(x, y, col(C.zhe))
			end
		end
	end
	if style.chips then
		local chips = { { 13, 25 }, { 30, 24 } }
		for _, p in ipairs(chips) do
			local x, y = p[1], p[2] + B - GY
			if maskAt(m, x, y) then img:putPixel(x, y, col(C.paper)) end
		end
	end
end

local function paintOutline(img, m)
	for y = 0, H - 1 do
		for x = 0, W - 1 do
			if not m[y][x] then
				local near = false
				for dy = -1, 1 do
					for dx = -1, 1 do
						if maskAt(m, x + dx, y + dy) then near = true end
					end
				end
				if near then img:putPixel(x, y, col(C.paper)) end
			end
		end
	end
end

local function paintShadow(img)
	for y = 47, 51 do
		for x = 0, W - 1 do
			local dx = (x - 24) / 16.5
			local dy = (y - 49.0) / 1.9
			local d = dx * dx + dy * dy
			if d <= 1.0 then
				img:putPixel(x, y, col(C.ink, math.floor(120 - d * 60)))
			end
		end
	end
end

----------------------------------------------------------------
-- 变体对比表（1x）
----------------------------------------------------------------
local VARIANTS = {
	{ belt = false, chips = false },
	{ belt = true,  chips = false },
	{ belt = true,  chips = true },
	{ belt = false, chips = true },
}
local STEP = 50
local sheet = Sprite(#VARIANTS * STEP, H, ColorMode.RGB)
local sl = sheet:newLayer()
local simg = sheet:newCel(sl, 1).image
for i, v in ipairs(VARIANTS) do
	local tmp = Sprite(W, H, ColorMode.RGB)
	local tl = tmp:newLayer()
	local tcel = tmp:newCel(tl, 1)
	local m = buildGlyph{}
	paintInk(tcel.image, m)
	paintMark(tcel.image, m, v, 0)
	local ox = (i - 1) * STEP
	for y = 0, H - 1 do
		for x = 0, W - 1 do
			local p = tcel.image:getPixel(x, y)
			if app.pixelColor.rgbaA(p) > 0 then simg:putPixel(ox + x, y, p) end
		end
	end
end
sheet:saveCopyAs(OUT .. "_variants.png")

----------------------------------------------------------------
-- 正式资产：4 层 × 2 帧
----------------------------------------------------------------
local FINAL = { belt = true, chips = true }

local spr = Sprite(W, H, ColorMode.RGB)
for i = #spr.layers, 1, -1 do spr:deleteLayer(spr.layers[i]) end
local L = {}
-- 自下而上：影 → 描边 → 字 → 刀疤
for _, name in ipairs{ "影", "描边", "字", "刀疤" } do
	L[name] = spr:newLayer()
	L[name].name = name
end
spr:newEmptyFrame(2)
for f = 1, 2 do
	local bob = (f == 2) and -1 or 0
	local m = buildGlyph{ bob = bob }
	paintInk(spr:newCel(L["字"], f).image, m)
	paintMark(spr:newCel(L["刀疤"], f).image, m, FINAL, bob)
	paintOutline(spr:newCel(L["描边"], f).image, m)
	paintShadow(spr:newCel(L["影"], f).image)
end
L["描边"].isVisible = false
L["影"].isVisible = false

-- 把项目 5 色写进文件调色板，打开即在色板栏看到
local okPal = pcall(function()
	local pal = Palette(5)
	for i, c in ipairs{ C.ink, C.zhu, C.zhe, C.dian, C.paper } do
		pal:setColor(i - 1, col(c))
	end
	spr:setPalette(pal)
end)
print("palette ok=" .. tostring(okPal))

spr:saveAs(OUT .. "bing.aseprite")
spr:saveCopyAs(OUT .. "_idle_1x.gif")
print("aseprite saved: layers=" .. #spr.layers .. " frames=" .. #spr.frames)

----------------------------------------------------------------
-- 单帧导出
----------------------------------------------------------------
local function exportPNG(path, opt)
	opt = opt or {}
	local s = Sprite(W, H, ColorMode.RGB)
	for i = #s.layers, 1, -1 do s:deleteLayer(s.layers[i]) end
	local m = buildGlyph{ legs = opt.legs }
	if opt.shadow then paintShadow(s:newCel(s:newLayer(), 1).image) end
	if opt.outline then paintOutline(s:newCel(s:newLayer(), 1).image, m) end
	paintInk(s:newCel(s:newLayer(), 1).image, m)
	paintMark(s:newCel(s:newLayer(), 1).image, m, FINAL, 0)
	s:saveCopyAs(path)
end

exportPNG(OUT .. "bing.png", {})
exportPNG(OUT .. "qiu.png", { legs = false })
exportPNG(OUT .. "bing_wall.png", { outline = true, shadow = true })
print("OK done")
