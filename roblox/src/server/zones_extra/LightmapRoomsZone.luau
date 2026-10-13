--!strict
-- LightmapRoomsZone — THE ROOM (2026-09-02) rendered as a dungeon, ported from
-- dashboard/static/room_lightmap.html: radial lightmap, 1D distance fields per light,
-- occluders are the failure classes, lights are the engines, the center ring is the fold.
-- Exact source constants: five engine-lights A1/B1/D1/forge/harvest with their orbit
-- radii, speeds, phases and colors; motion t = now/4000, lx = r*cos(t*s+p),
-- ly = r*0.55*sin(t*s*1.3+p); scene: covenant wall rect half-extents (2.30, 1.25), the
-- four failure-class pillars r=0.09 (dead door / placeholder pass / stale row / key
-- miswire), THE FOLD ring ir=0.16 / or=0.19 at center, and the screen at (2.0, -0.9) —
-- do not look. Port note (honest): the per-pixel SDF raymarch becomes real
-- shadow-casting PointLights in a sealed dark room — same lights, same occluders, same
-- orbits, so pillar shadows are literal (Lighting global state untouched). The source
-- render has no score and no input, so none was invented; the ledger only files entering
-- the room and standing in THE FOLD. Scale: 20 studs per scene unit.

local Players = game:GetService("Players")
local ServerScriptService = game:GetService("ServerScriptService")
local ShadowLedger = require((script.Parent:FindFirstChild("ShadowLedger") or script.Parent.Parent:WaitForChild("ShadowLedger")) :: ModuleScript)

local LightmapRoomsZone = {}
local origin = Vector3.new(-300, 8, 0) -- clear of every listed zone origin
local SCALE = 20 -- studs per scene unit

type EngineDef = { c: { number }, r: number, s: number, p: number, name: string }

-- the engines, exact from LIGHTS[] (lights are the engines, wandering free)
local LIGHTS: { EngineDef } = {
	{ c = { 125, 250, 176 }, r = 0.9, s = 0.31, p = 0.0, name = "A1" },
	{ c = { 177, 140, 255 }, r = 0.75, s = 0.27, p = 2.1, name = "B1" },
	{ c = { 232, 201, 106 }, r = 0.6, s = 0.35, p = 4.2, name = "D1" },
	{ c = { 255, 157, 92 }, r = 0.5, s = 0.41, p = 1.3, name = "forge" },
	{ c = { 124, 245, 255 }, r = 0.8, s = 0.22, p = 3.3, name = "harvest" },
}

-- the four failure classes, exact from pillars[] (occluders are the failure classes)
local PILLARS: { { x: number, z: number, name: string } } = {
	{ x = -1.5, z = -0.6, name = "dead door" },
	{ x = -0.4, z = 0.75, name = "placeholder pass" },
	{ x = 0.7, z = -0.8, name = "stale row" },
	{ x = 1.7, z = 0.6, name = "key miswire" },
}

-- annotation exactness (t42 triage, lanes/t42.check.txt row 5): engines hold Instance.new("Part") orbs (line 87). Runtime unchanged.
local engines: { { orb: Part, def: EngineDef } } = {}
local entered: { [Player]: boolean } = {}
local stoodFold: { [Player]: boolean } = {}

local function sceneToWorld(sx: number, sz: number): Vector3 return origin + Vector3.new(sx * SCALE, 0, sz * SCALE) end

local function slab(parent: Instance, name: string, size: Vector3, pos: Vector3, color: Color3, mat: Enum.Material): BasePart
	local p = Instance.new("Part"); p.Anchored, p.Name, p.Size, p.Position, p.Color, p.Material, p.Parent = true, name, size, pos, color, mat, parent
	return p
end

local function label(parent: Instance, text: string, color: Color3)
	local gui = Instance.new("BillboardGui"); gui.Size, gui.StudsOffset, gui.AlwaysOnTop = UDim2.new(0, 200, 0, 30), Vector3.new(0, 3.5, 0), true
	local t = Instance.new("TextLabel"); t.Size, t.BackgroundTransparency, t.Text, t.TextColor3, t.Font, t.TextSize, t.TextWrapped, t.Parent = UDim2.fromScale(1, 1), 1, text, color, Enum.Font.Code, 12, true, gui
	gui.Parent = parent
end

function LightmapRoomsZone.build(): Model
	local model = Instance.new("Model"); model.Name = "TheRoom"
	-- the covenant wall: the room exists because the laws bound it (rect half-extents 2.30 x 1.25)
	local RX, RZ, H = 2.3 * SCALE, 1.25 * SCALE, 26
	local wallC = Color3.fromRGB(24, 28, 30)
	slab(model, "CovenantFloor", Vector3.new(RX * 2 + 8, 1, RZ * 2 + 8), origin + Vector3.new(0, -0.5, 0), Color3.fromRGB(10, 12, 11), Enum.Material.Slate)
	slab(model, "WallN", Vector3.new(RX * 2 + 8, H, 2), origin + Vector3.new(0, H / 2, -RZ - 1), wallC, Enum.Material.Concrete)
	slab(model, "WallS", Vector3.new(RX * 2 + 8, H, 2), origin + Vector3.new(0, H / 2, RZ + 1), wallC, Enum.Material.Concrete)
	slab(model, "WallW", Vector3.new(2, H, RZ * 2 + 8), origin + Vector3.new(-RX - 1, H / 2, 0), wallC, Enum.Material.Concrete)
	slab(model, "WallE", Vector3.new(2, H, RZ * 2 + 8), origin + Vector3.new(RX + 1, H / 2, 0), wallC, Enum.Material.Concrete)
	slab(model, "CovenantCeiling", Vector3.new(RX * 2 + 8, 1, RZ * 2 + 8), origin + Vector3.new(0, H, 0), Color3.fromRGB(8, 10, 12), Enum.Material.Concrete)
	for _, pd in ipairs(PILLARS) do -- occluders glow their color at the surface (legend #ff7d7d)
		local pil = slab(model, "FailurePillar", Vector3.new(0.09 * SCALE * 2, 9, 0.09 * SCALE * 2), sceneToWorld(pd.x, pd.z) + Vector3.new(0, 4.5, 0), Color3.fromRGB(46, 26, 26), Enum.Material.Basalt)
		local glow = Instance.new("PointLight"); glow.Color, glow.Range, glow.Brightness, glow.Parent = Color3.fromRGB(255, 125, 125), 6, 0.7, pil
		label(pil, pd.name, Color3.fromRGB(255, 125, 125))
	end
	for i = 0, 7 do -- THE FOLD at center: gold ring ir=0.16 / or=0.19
		local a = math.rad(i * 45)
		local seg = slab(model, "FoldSegment", Vector3.new(1.1, 0.4, 1.7), sceneToWorld(math.cos(a) * 0.175, math.sin(a) * 0.175) + Vector3.new(0, 0.4, 0), Color3.fromRGB(232, 201, 106), Enum.Material.Neon)
		seg.CFrame = CFrame.new(seg.Position) * CFrame.Angles(0, -a, 0)
	end
	local sensor = slab(model, "FoldSensor", Vector3.new(0.32 * SCALE, 0.2, 0.32 * SCALE), origin + Vector3.new(0, 0.1, 0), Color3.fromRGB(232, 201, 106), Enum.Material.Neon)
	sensor.Transparency, sensor.CanCollide = 1, false
	label(sensor, "THE FOLD — the center ring", Color3.fromRGB(232, 201, 106))
	local scr = slab(model, "TheScreen", Vector3.new(0.8, 10, 6), sceneToWorld(2.0, -0.9) + Vector3.new(0, 5, 0), Color3.fromRGB(14, 14, 18), Enum.Material.Glass) -- the screen: do not look
	label(scr, "the screen (do not look)", Color3.fromRGB(160, 160, 185))
	for _, L in ipairs(LIGHTS) do
		local orb = Instance.new("Part"); orb.Shape, orb.Anchored, orb.Size = Enum.PartType.Ball, true, Vector3.new(2.5, 2.5, 2.5)
		orb.Color = Color3.fromRGB(L.c[1], L.c[2], L.c[3])
		orb.Material, orb.Name = Enum.Material.Neon, ("Engine_%s"):format(L.name)
		local li = Instance.new("PointLight"); li.Color, li.Range, li.Brightness, li.Shadows, li.Parent = orb.Color, 26, 2, true, orb
		label(orb, ("engine %s"):format(L.name), orb.Color)
		orb.Parent = model
		table.insert(engines, { orb = orb, def = L })
	end
	model.Parent = workspace
	return model
end

function LightmapRoomsZone.tick(_dt: number)
	local t = os.clock() / 4 -- source: t = now/4000 (ms)
	for _, e in ipairs(engines) do
		local L = e.def
		local lx = L.r * math.cos(t * L.s + L.p)
		local lz = L.r * 0.55 * math.sin(t * L.s * 1.3 + L.p)
		e.orb.Position = sceneToWorld(lx, lz) + Vector3.new(0, 6, 0)
	end
	for _, plr in ipairs(Players:GetPlayers()) do
		local root = plr.Character and plr.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
		if root and math.abs(root.Position.X - origin.X) <= 2.3 * SCALE + 4 and math.abs(root.Position.Z - origin.Z) <= 1.25 * SCALE + 4 and math.abs(root.Position.Y - origin.Y) < 14 then
			if not entered[plr] then
				entered[plr] = true
				ShadowLedger.record(plr, "LightmapRooms", "entered the room; the engines wander, the pillars stay", true)
			end
			if not stoodFold[plr] then
				local flat = Vector3.new(root.Position.X - origin.X, 0, root.Position.Z - origin.Z)
				if flat.Magnitude < 0.16 * SCALE + 1.5 then
					stoodFold[plr] = true
					ShadowLedger.record(plr, "LightmapRooms", "stood in THE FOLD, the center ring", true)
				end
			end
		end
	end
end

Players.PlayerRemoving:Connect(function(p) entered[p] = nil; stoodFold[p] = nil end)

return LightmapRoomsZone
