-- 把米字格方块 PNG 收进 Aseprite 文件，并写入项目 5 色板
-- 用法：aseprite -b --script package_tile.lua
local function _dirname(p) return p:match("^(.*)[/\\][^/\\]*$") end
local _here = (debug.getinfo(1, "S").source:gsub("^@", "")):gsub("\\", "/")
local _dir = _dirname(_here)
local ART = _dir:match("(.*)/tools$") or _dir
local DIR = ART .. "/tile/"

local PAL = {
	{ 31, 27, 22 },    -- 墨
	{ 164, 50, 42 },   -- 朱
	{ 138, 90, 59 },   -- 赭
	{ 47, 72, 88 },    -- 靛
	{ 239, 230, 210 }, -- 米白
}

local function make(name)
	local spr = app.open(DIR .. name .. ".png")
	local pal = Palette(5)
	for i, c in ipairs(PAL) do
		pal:setColor(i - 1, Color{ r = c[1], g = c[2], b = c[3], a = 255 })
	end
	spr:setPalette(pal)
	spr:saveAs(DIR .. name .. ".aseprite")
	print(string.format("%s: %dx%d layers=%d frames=%d", name, spr.width, spr.height, #spr.layers, #spr.frames))
end

make("tile_bing")
make("tile_qiu")
print("TILE_PACKAGE_DONE")
