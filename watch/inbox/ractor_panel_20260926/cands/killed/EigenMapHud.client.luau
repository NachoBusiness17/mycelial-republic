--!strict
-- EigenMapHud -- the walker-view overlay: the cathedral eigen-map pinned
-- top-right, the live player position projected onto the eigen plane, and a
-- per-region distance/bearing readout in the scan's own units (milli-eigen
-- and degrees, 0 = N clockwise) plus studs. Data, transform and math live in
-- shared/EigenMap.luau (single authorship site); this file only renders.
-- Face drift to the nearest beacon rides KSpace.drift, the smart-GPS pair.
-- The readout numbers are checkable against the scan JSON directly:
-- standing on a beacon, the row for any other region equals the pair's
-- eigen distance and bearing in the data (tools/eigenmap_overlay_check.py
-- verifies the same math headless).

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")

local Shared = ReplicatedStorage:WaitForChild("Modules")
local EigenMap = require(Shared:WaitForChild("EigenMap"))
local KSpace = require(Shared:WaitForChild("KSpace"))

local player = Players.LocalPlayer

local INK = Color3.fromRGB(230, 224, 196)
local PANEL = Color3.fromRGB(20, 18, 26)
local RUST = Color3.fromRGB(179, 86, 44) -- the HTML map's chain color
local YOU = Color3.fromRGB(120, 235, 150)

local function shortName(name: string): string
	local parts = string.split(name, "_")
	if #parts > 1 then
		return ("%s_%s"):format(parts[1], string.sub(parts[2], 1, 1))
	end
	return name
end

-- ---- panel ----

local gui = Instance.new("ScreenGui")
gui.Name = "EigenMapHud"
gui.ResetOnSpawn = false
gui.DisplayOrder = 10
gui.Parent = player:WaitForChild("PlayerGui")

local panel = Instance.new("Frame")
panel.AnchorPoint = Vector2.new(1, 0)
panel.Position = UDim2.new(1, -12, 0, 12)
panel.Size = UDim2.new(0, 300, 0, 352)
panel.BackgroundColor3 = PANEL
panel.BackgroundTransparency = 0.25
panel.BorderSizePixel = 0
local corner = Instance.new("UICorner")
corner.CornerRadius = UDim.new(0, 8)
corner.Parent = panel
panel.Parent = gui

local ts, _sha = EigenMap.scanStamp()
local wired, intended = EigenMap.beta0()
local title = Instance.new("TextLabel")
title.Size = UDim2.new(1, -16, 0, 18)
title.Position = UDim2.new(0, 8, 0, 6)
title.BackgroundTransparency = 1
title.Font = Enum.Font.Garamond
title.TextSize = 14
title.TextColor3 = INK
title.TextXAlignment = Enum.TextXAlignment.Left
title.Text = ("EIGEN MAP · scan %s · water_first lean, RIB CONTESTED"):format(string.sub(ts, 1, 10))
title.Parent = panel

local mapFrame = Instance.new("Frame")
mapFrame.Size = UDim2.new(1, -16, 0, 208)
mapFrame.Position = UDim2.new(0, 8, 0, 28)
mapFrame.BackgroundColor3 = Color3.fromRGB(12, 11, 16)
mapFrame.BackgroundTransparency = 0.1
mapFrame.BorderSizePixel = 0
mapFrame.ClipsDescendants = true
local mapCorner = Instance.new("UICorner")
mapCorner.CornerRadius = UDim.new(0, 6)
mapCorner.Parent = mapFrame
mapFrame.Parent = panel

-- static layer (chain + region dots + N); redrawn if the pixel size changes
local layer = Instance.new("Frame")
layer.Size = UDim2.fromScale(1, 1)
layer.BackgroundTransparency = 1
layer.BorderSizePixel = 0
layer.Parent = mapFrame

local readout = Instance.new("TextLabel")
readout.Size = UDim2.new(1, -16, 0, 104)
readout.Position = UDim2.new(0, 8, 0, 240)
readout.BackgroundTransparency = 1
readout.Font = Enum.Font.Code
readout.TextSize = 11
readout.TextColor3 = INK
readout.TextXAlignment = Enum.TextXAlignment.Left
readout.TextYAlignment = Enum.TextYAlignment.Top
readout.TextWrapped = true
readout.Text = "eigen overlay: waiting for character"
readout.Parent = panel

-- ---- eigen plane -> map pixels ----

local ex0, ex1, ey0, ey1 = EigenMap.span()
local spanX, spanY = ex1 - ex0, ey1 - ey0
local marginX, marginY = spanX * 0.14, spanY * 0.14
local px0, px1 = ex0 - marginX, ex1 + marginX
local py0, py1 = ey0 - marginY, ey1 + marginY

local function toScale(ex: number, ey: number): (number, number)
	return (ex - px0) / (px1 - px0), (py1 - ey) / (py1 - py0) -- north up
end

local function line(x1: number, y1: number, x2: number, y2: number, color: Color3,
	thickness: number, transparency: number)
	local dx, dy = x2 - x1, y2 - y1
	local len = math.sqrt(dx * dx + dy * dy)
	if len < 2 then return end
	local f = Instance.new("Frame")
	f.AnchorPoint = Vector2.new(0.5, 0.5)
	f.Position = UDim2.fromOffset((x1 + x2) / 2, (y1 + y2) / 2)
	f.Size = UDim2.fromOffset(len, thickness)
	-- screen +Y is down, GUI Rotation is clockwise: atan2(dy, dx) aims +X->target
	f.Rotation = math.deg(math.atan2(dy, dx))
	f.BackgroundColor3 = color
	f.BackgroundTransparency = transparency
	f.BorderSizePixel = 0
	f.Parent = layer
end

local youMarker = Instance.new("Frame")
youMarker.Size = UDim2.fromOffset(9, 9)
youMarker.AnchorPoint = Vector2.new(0.5, 0.5)
youMarker.BackgroundColor3 = YOU
youMarker.BorderSizePixel = 1
youMarker.BorderColor3 = Color3.new(1, 1, 1)
youMarker.ZIndex = 5
local youDot = Instance.new("UICorner")
youDot.CornerRadius = UDim.new(1, 0)
youDot.Parent = youMarker
youMarker.Parent = mapFrame

local youTag = Instance.new("TextLabel")
youTag.Size = UDim2.fromOffset(30, 12)
youTag.AnchorPoint = Vector2.new(0, 0.5)
youTag.BackgroundTransparency = 1
youTag.Font = Enum.Font.Code
youTag.TextSize = 10
youTag.TextColor3 = YOU
youTag.TextXAlignment = Enum.TextXAlignment.Left
youTag.ZIndex = 5
youTag.Text = "you"
youTag.Parent = mapFrame

local nearestLine = Instance.new("Frame")
nearestLine.AnchorPoint = Vector2.new(0.5, 0.5)
nearestLine.BackgroundColor3 = YOU
nearestLine.BackgroundTransparency = 0.55
nearestLine.BorderSizePixel = 0
nearestLine.ZIndex = 4
nearestLine.Visible = false
nearestLine.Parent = mapFrame

local drawnSize = Vector2.new(0, 0)

local function drawStatic()
	layer:ClearAllChildren()
	local w, h = layer.AbsoluteSize.X, layer.AbsoluteSize.Y
	for _, seg in ipairs(EigenMap.chain()) do
		local ra, rb = EigenMap.region(seg.a), EigenMap.region(seg.b)
		if ra and rb then
			local x1, y1 = toScale(ra.ex, ra.ey)
			local x2, y2 = toScale(rb.ex, rb.ey)
			local a1, b1, a2, b2 = x1 * w, y1 * h, x2 * w, y2 * h
			if seg.kind == "wired" then
				line(a1, b1, a2, b2, RUST, 3, 0.15)
			else
				-- dotted: the gap reads as a gap (missing stitch, build debt)
				for i = 0, 5 do
					local s, e = i / 6, (i + 0.55) / 6
					line(a1 + (a2 - a1) * s, b1 + (b2 - b1) * s,
						a1 + (a2 - a1) * e, b1 + (b2 - b1) * e, RUST, 2, 0.45)
				end
			end
		end
	end
	for _, r in ipairs(EigenMap.regions()) do
		local sx, sy = toScale(r.ex, r.ey)
		local dot = Instance.new("Frame")
		dot.AnchorPoint = Vector2.new(0.5, 0.5)
		dot.Position = UDim2.fromScale(sx, sy)
		dot.Size = UDim2.fromOffset(r.name == "water_computer" and 14 or 11, r.name == "water_computer" and 14 or 11)
		dot.BackgroundColor3 = EigenMap.classColor(r.class)
		dot.BorderSizePixel = 1
		dot.BorderColor3 = Color3.new(0, 0, 0)
		dot.ZIndex = 3
		local round = Instance.new("UICorner")
		round.CornerRadius = UDim.new(1, 0)
		round.Parent = dot
		dot.Parent = layer
		local label = Instance.new("TextLabel")
		label.AnchorPoint = Vector2.new(0, 0.5)
		label.Position = UDim2.new(sx, 9, sy, 0)
		label.Size = UDim2.fromOffset(64, 12)
		label.BackgroundTransparency = 1
		label.Font = Enum.Font.Code
		label.TextSize = 10
		label.TextColor3 = INK
		label.TextXAlignment = Enum.TextXAlignment.Left
		label.ZIndex = 3
		label.Text = shortName(r.name)
		label.Parent = layer
	end
	local north = Instance.new("TextLabel")
	north.AnchorPoint = Vector2.new(0.5, 0.5)
	north.Position = UDim2.new(0.5, 0, 0, 8)
	north.Size = UDim2.fromOffset(24, 12)
	north.BackgroundTransparency = 1
	north.Font = Enum.Font.Code
	north.TextSize = 10
	north.TextColor3 = Color3.fromRGB(160, 156, 170)
	north.Text = "N ^"
	north.Parent = layer
	drawnSize = Vector2.new(w, h)
end

drawStatic()
layer:GetPropertyChangedSignal("AbsoluteSize"):Connect(function()
	if math.abs(layer.AbsoluteSize.X - drawnSize.X) > 1
		or math.abs(layer.AbsoluteSize.Y - drawnSize.Y) > 1 then
		drawStatic()
	end
end)

-- ---- live overlay: position, distance, bearing ----

local studsPerMilli = EigenMap.studsPerMilli()
local lastDraw = 0.0

RunService.Heartbeat:Connect(function()
	local now = os.clock()
	if now - lastDraw < 0.15 then return end -- ~6.5 Hz, not per-frame
	lastDraw = now

	local char = player.Character
	local hrp: BasePart? = char and (char:FindFirstChild("HumanoidRootPart") :: BasePart?)
	local ex, ey
	if hrp then
		ex, ey = EigenMap.eigenFromWorld(hrp.Position.X, hrp.Position.Z)
	else
		ex, ey = EigenMap.center()
	end

	-- rows: distance + bearing from the walker to every region, data units
	local rows: { { d: number, text: string } } = {}
	for _, r in ipairs(EigenMap.regions()) do
		local d = EigenMap.distFromEigen(r.name, ex, ey)
		local brg = EigenMap.bearingFromEigen(r.name, ex, ey)
		table.insert(rows, { d = d, text = ("%-16s %6.1f deg %6.2f mE %5.0f st")
			:format(shortName(r.name), brg, d * 1000, d * studsPerMilli) })
	end
	table.sort(rows, function(a, b) return a.d < b.d end)
	local body = {}
	for _, r in ipairs(rows) do
		table.insert(body, r.text)
	end

	-- marker (clamped into the window; honest when projected outside it)
	local sx, sy = toScale(ex, ey)
	local offWindow = sx < 0 or sx > 1 or sy < 0 or sy > 1
	local cx = math.clamp(sx, 0.02, 0.98)
	local cy = math.clamp(sy, 0.02, 0.98)
	youMarker.Position = UDim2.fromScale(cx, cy)
	youTag.Position = UDim2.new(cx, 8, cy, 0)
	youMarker.Visible = hrp ~= nil
	youTag.Visible = hrp ~= nil

	local w, h = mapFrame.AbsoluteSize.X, mapFrame.AbsoluteSize.Y
	local nearestName, nearestD = EigenMap.nearestEigen(ex, ey)
	local nrow = EigenMap.region(nearestName)
	if nrow and w > 4 and h > 4 then
		local tx, ty = toScale(nrow.ex, nrow.ey)
		local x1, y1, x2, y2 = cx * w, cy * h, tx * w, ty * h
		local dx, dy = x2 - x1, y2 - y1
		local len = math.sqrt(dx * dx + dy * dy)
		nearestLine.Size = UDim2.fromOffset(len, 2)
		nearestLine.Position = UDim2.fromOffset((x1 + x2) / 2, (y1 + y2) / 2)
		nearestLine.Rotation = math.deg(math.atan2(dy, dx))
		nearestLine.Visible = hrp ~= nil and len > 8
	end

	-- face drift to the nearest beacon (KSpace smart-GPS pair)
	local driftText = ""
	if hrp and nrow then
		local drift = KSpace.drift(hrp.Position, EigenMap.worldPos(nearestName), hrp.CFrame.LookVector)
		driftText = (" · drift %.0f deg"):format(drift)
	end

	local header = ("you: eigen (%.4f, %.4f)%s · nearest %s at %.2f mE%s")
		:format(ex, ey, offWindow and " [off-window]" or "", shortName(nearestName),
			nearestD * 1000, driftText)
	table.insert(body, 1, header)
	table.insert(body, ("off-map (no centroid): %s · wired beta0 %d vs intended %d")
		:format(table.concat(EigenMap.offMap(), ", "), wired, intended))
	readout.Text = table.concat(body, "\n")
end)
