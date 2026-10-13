--!strict
-- CathedralMapHud  -  the walker-view overlay for the eigen-map (candidate
-- two). Renders THE CATHEDRAL from shared/CathedralMap (single authorship:
-- every number on this panel is computed by that module), pinned top-left
-- under the sphere chip. One compass everywhere: north = eigen -y is UP on
-- this minimap and world -Z on the plate (CathedralMap.toWorld), so the
-- bearing text you read is the direction you walk.
--
-- Standing on a region beacon, its row reads 0.0000 and the POS line equals
-- that region's centroid  -  the position sanity anchor, player-visible.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")

local Shared = ReplicatedStorage:WaitForChild("Modules")
local CathedralMap = require(Shared:WaitForChild("CathedralMap"))

local player = Players.LocalPlayer

local INK = Color3.fromRGB(230, 224, 196)
local PANEL = Color3.fromRGB(20, 18, 26)
local RUST = Color3.fromRGB(179, 86, 44)
local VIOLET = Color3.fromRGB(138, 127, 176)
local YOU = Color3.fromRGB(120, 235, 150)

local ABBREV: { [string]: string } = {
	["water_computer"] = "water",
	["fractal_maze"] = "fractal",
	["riddler_optics"] = "optics",
	["riddler_engram"] = "engram",
	["audit_dungeon"] = "audit",
}

-- ---- panel ----

local gui = Instance.new("ScreenGui")
gui.Name = "CathedralMapHud"
gui.ResetOnSpawn = false
gui.DisplayOrder = 11
gui.Parent = player:WaitForChild("PlayerGui")

local panel = Instance.new("Frame")
panel.Position = UDim2.new(0, 8, 0, 36) -- under the sphere chip (t59)
panel.Size = UDim2.new(0, 296, 0, 328)
panel.BackgroundColor3 = PANEL
panel.BackgroundTransparency = 0.25
panel.BorderSizePixel = 0
local panelCorner = Instance.new("UICorner")
panelCorner.CornerRadius = UDim.new(0, 8)
panelCorner.Parent = panel
panel.Parent = gui

local title = Instance.new("TextLabel")
title.Size = UDim2.new(1, -16, 0, 18)
title.Position = UDim2.new(0, 8, 0, 6)
title.BackgroundTransparency = 1
title.Font = Enum.Font.Garamond
title.TextSize = 14
title.TextColor3 = INK
title.TextXAlignment = Enum.TextXAlignment.Left
title.Text = "THE CATHEDRAL · eigen-map (walker view)"
title.Parent = panel

local mapFrame = Instance.new("Frame")
mapFrame.Size = UDim2.new(1, -16, 0, 176)
mapFrame.Position = UDim2.new(0, 8, 0, 26)
mapFrame.BackgroundColor3 = Color3.fromRGB(12, 11, 16)
mapFrame.BackgroundTransparency = 0.1
mapFrame.BorderSizePixel = 0
mapFrame.ClipsDescendants = true
local mapCorner = Instance.new("UICorner")
mapCorner.CornerRadius = UDim.new(0, 6)
mapCorner.Parent = mapFrame
mapFrame.Parent = panel

local layer = Instance.new("Frame")
layer.Size = UDim2.fromScale(1, 1)
layer.BackgroundTransparency = 1
layer.BorderSizePixel = 0
layer.Parent = mapFrame

local readout = Instance.new("TextLabel")
readout.Size = UDim2.new(1, -16, 0, 116)
readout.Position = UDim2.new(0, 8, 0, 206)
readout.BackgroundTransparency = 1
readout.Font = Enum.Font.Code
readout.TextSize = 11
readout.TextColor3 = INK
readout.TextXAlignment = Enum.TextXAlignment.Left
readout.TextYAlignment = Enum.TextYAlignment.Top
readout.TextWrapped = true
readout.Text = "eigen overlay: waiting for character"
readout.Parent = panel

-- ---- eigen -> pixels (one compass: -y up; NO y-flip, +ey renders south) ----

local minX, maxX, minY, maxY = CathedralMap.mapBounds(0)
local spanX, spanY = maxX - minX, maxY - minY
local mX, mY = spanX * 0.13, spanY * 0.13
local x0, x1 = minX - mX, maxX + mX
local y0, y1 = minY - mY, maxY + mY

local scale = 1.0
local offX, offY = 0.0, 0.0
local function fitCanvas()
	local w, h = mapFrame.AbsoluteSize.X, mapFrame.AbsoluteSize.Y
	if w < 8 or h < 8 then
		return
	end
	scale = math.min(w / (x1 - x0), h / (y1 - y0))
	offX = (w - (x1 - x0) * scale) / 2
	offY = (h - (y1 - y0) * scale) / 2
end
local function px(ex: number): number
	return offX + (ex - x0) * scale
end
local function py(ey: number): number
	return offY + (ey - y0) * scale -- +ey down = south; north (-y) at top
end

local function dot(x: number, y: number, size: number, color: Color3, z: number, transparency: number?): Frame
	local f = Instance.new("Frame")
	f.AnchorPoint = Vector2.new(0.5, 0.5)
	f.Position = UDim2.fromOffset(x, y)
	f.Size = UDim2.fromOffset(size, size)
	f.BackgroundColor3 = color
	f.BackgroundTransparency = transparency or 0
	f.BorderSizePixel = 0
	f.ZIndex = z
	local round = Instance.new("UICorner")
	round.CornerRadius = UDim.new(1, 0)
	round.Parent = f
	f.Parent = layer
	return f
end

-- dotted segment (no rotation math: trail of small dots, robust to rescale)
local function dotted(x1: number, y1: number, x2: number, y2: number, color: Color3, z: number, n: number, size: number, transparency: number)
	for i = 0, n do
		local t = i / n
		dot(x1 + (x2 - x1) * t, y1 + (y2 - y1) * t, size, color, z, transparency)
	end
end

local youMarker = dot(0, 0, 9, YOU, 6)
youMarker.BorderSizePixel = 1
youMarker.BorderColor3 = Color3.new(1, 1, 1)
youMarker.Parent = mapFrame

local drawnW, drawnH = 0.0, 0.0
local function drawStatic()
	layer:ClearAllChildren()
	fitCanvas()
	local chain = CathedralMap.chainEdges()
	for _, e in ipairs(chain) do
		local a = CathedralMap.centroid(e.a)
		local b = CathedralMap.centroid(e.b)
		if a and b then
			dotted(px(a[1]), py(a[2]), px(b[1]), py(b[2]), RUST, 2, 7, 3, 0.15)
		end
	end
	for _, e in ipairs(CathedralMap.hubEdges()) do
		local a = CathedralMap.centroid(e.a)
		local b = CathedralMap.centroid(e.b)
		if a and b then
			dotted(px(a[1]), py(a[2]), px(b[1]), py(b[2]), VIOLET, 1, 5, 2, 0.5)
		end
	end
	for _, region in ipairs(CathedralMap.regions()) do
		local c = CathedralMap.centroid(region)
		if c then
			local d = dot(px(c[1]), py(c[2]), region == "water_computer" and 13 or 10,
				CathedralMap.classColor(CathedralMap.class(region)), 3)
			d.BorderSizePixel = 1
			d.BorderColor3 = Color3.new(0, 0, 0)
			local t = Instance.new("TextLabel")
			t.AnchorPoint = Vector2.new(0, 0.5)
			t.Position = UDim2.fromOffset(px(c[1]) + 8, py(c[2]))
			t.Size = UDim2.fromOffset(64, 12)
			t.BackgroundTransparency = 1
			t.Font = Enum.Font.Code
			t.TextSize = 10
			t.TextColor3 = INK
			t.TextXAlignment = Enum.TextXAlignment.Left
			t.ZIndex = 4
			t.Text = ABBREV[region] or region
			t.Parent = layer
		end
	end
	local north = Instance.new("TextLabel")
	north.AnchorPoint = Vector2.new(0.5, 0.5)
	north.Position = UDim2.new(0.5, 0, 0, 9)
	north.Size = UDim2.fromOffset(36, 12)
	north.BackgroundTransparency = 1
	north.Font = Enum.Font.Code
	north.TextSize = 10
	north.TextColor3 = Color3.fromRGB(160, 156, 170)
	north.Text = "^ N (-y)"
	north.ZIndex = 4
	north.Parent = layer
	drawnW, drawnH = mapFrame.AbsoluteSize.X, mapFrame.AbsoluteSize.Y
end

drawStatic()
mapFrame:GetPropertyChangedSignal("AbsoluteSize"):Connect(function()
	if math.abs(mapFrame.AbsoluteSize.X - drawnW) > 1 or math.abs(mapFrame.AbsoluteSize.Y - drawnH) > 1 then
		drawStatic()
	end
end)

-- ---- live loop: position, distance, bearing (all from CathedralMap) ----

local lastRun = 0.0
RunService.Heartbeat:Connect(function()
	local now = os.clock()
	if now - lastRun < 0.14 then
		return
	end
	lastRun = now

	local char = player.Character
	local root = char and (char:FindFirstChild("HumanoidRootPart") :: BasePart?)
	local ex, ey
	if root then
		ex, ey = CathedralMap.worldToEigen(root.Position)
	else
		ex, ey = (maxX + minX) / 2, (maxY + minY) / 2
	end
	youMarker.Visible = root ~= nil

	-- marker clamped into the window (honest tag when projected outside)
	local sx, sy = px(ex), py(ey)
	local offWindow = sx < 0 or sx > mapFrame.AbsoluteSize.X or sy < 0 or sy > mapFrame.AbsoluteSize.Y
	youMarker.Position = UDim2.fromOffset(
		math.clamp(sx, 6, mapFrame.AbsoluteSize.X - 6),
		math.clamp(sy, 6, mapFrame.AbsoluteSize.Y - 6))

	local near = CathedralMap.nearest(ex, ey)
	local rows: { { d: number, text: string } } = {}
	for _, region in ipairs(CathedralMap.regions()) do
		local d = CathedralMap.distFrom(ex, ey, region)
		local b = CathedralMap.bearingFrom(ex, ey, region)
		local here = d < 0.0015 and "  <-- HERE" or ""
		table.insert(rows, {
			d = d,
			text = ("%-8s %7.4f  %5.1f deg %s%s"):format(ABBREV[region] or region, d, b,
				CathedralMap.compass(b), here),
		})
	end
	table.sort(rows, function(a, b)
		return a.d < b.d
	end)
	local body: { string } = {}
	for _, r in ipairs(rows) do
		table.insert(body, r.text)
	end
	table.insert(body, 1, ("POS eigen (%.4f, %.4f)%s  nearest %s")
		:format(ex, ey, offWindow and " [edge]" or "", ABBREV[near.region] or near.region))
	table.insert(body, ("scan %s · vote: chain %.3f vs star %.3f (%s lean, RIB CONTESTED)")
		:format(string.sub(CathedralMap.SCAN_TS, 1, 10), CathedralMap.VOTE.chain_len,
			CathedralMap.VOTE.star_len, CathedralMap.VOTE.shorter))
	table.insert(body, ("off-map: adventure_2d6 (stub: no centroid) · no edge on the DARK engram"))
	readout.Text = table.concat(body, "\n")
end)
