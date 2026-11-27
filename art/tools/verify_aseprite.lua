local function _dirname(p) return p:match("^(.*)[/\\][^/\\]*$") end
local _here = (debug.getinfo(1, "S").source:gsub("^@", "")):gsub("\\", "/")
local _dir = _dirname(_here)
local ART = _dir:match("(.*)/tools$") or _dir
local OUT = ART .. "/"

local spr = app.open(OUT .. "bing_v2.aseprite")
print("frames=" .. #spr.frames .. " layers=" .. #spr.layers .. " size=" .. spr.width .. "x" .. spr.height)
for i, l in ipairs(spr.layers) do
	local c = l:cel(1)
	local n = 0
	if c then
		for y = 0, c.image.height - 1 do
			for x = 0, c.image.width - 1 do
				if app.pixelColor.rgbaA(c.image:getPixel(x, y)) > 0 then n = n + 1 end
			end
		end
	end
	print(string.format("  %d %s visible=%s pixels=%d", i, l.name, tostring(l.isVisible), n))
end
print("palette=" .. #spr.palettes[1])
print("CHECK_DONE")
