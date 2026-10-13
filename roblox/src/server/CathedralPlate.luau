--!strict
-- CathedralPlate  -  THE CATHEDRAL made walkable (eigen-map card, candidate
-- two). The plate's beacon positions ARE the scan's eigen_centroids via
-- shared/CathedralMap.toWorld (single authorship: this file owns no
-- coordinates). Edge policy comes from CathedralMap.chainEdges/hubEdges: the
-- water_first chain over SADDLE-SADDLE legs only  -  no drawn edge anchors on
-- the DARK riddler_engram (referee ruling, watch/inbox/REFEREE_VERDICT_20260926.md
-- missing-edge section); the DARK anchor stands isolated by design.
-- Every beacon touch lands a ShadowLedger row with the walker's live eigen
-- position, so the walk itself files position/distance evidence.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Modules")
local CathedralMap = require(Shared:WaitForChild("CathedralMap"))
local ShadowLedger = require(script.Parent:WaitForChild("ShadowLedger"))

local CathedralPlate = {}

local FLOOR = Color3.fromRGB(28, 26, 34)
local INK = Color3.fromRGB(230, 224, 196)

local function mk(size: Vector3, pos: Vector3, color: Color3, mat: Enum.Material, collide: boolean?): Part
	local p = Instance.new("Part")
	p.Anchored = true
	p.Size = size
	p.Position = pos
	p.Color = color
	p.Material = mat
	p.CanCollide = collide ~= false
	p.TopSurface = Enum.SurfaceType.Smooth
	p.BottomSurface = Enum.SurfaceType.Smooth
	p.Parent = workspace
	return p
end

local function label(part: Part, lines: { string }, color: Color3, studY: number, width: number)
	local bb = Instance.new("BillboardGui")
	bb.Size = UDim2.new(0, width, 0, 16 * #lines)
	bb.StudsOffset = Vector3.new(0, studY, 0)
	bb.AlwaysOnTop = false
	bb.MaxDistance = 220
	local prev = 0
	for _, line in ipairs(lines) do
		local t = Instance.new("TextLabel")
		t.Size = UDim2.new(1, 0, 1 / #lines, 0)
		t.Position = UDim2.new(0, 0, prev, 0)
		prev += 1 / #lines
		t.BackgroundTransparency = 1
		t.Font = Enum.Font.Code
		t.TextSize = 13
		t.TextColor3 = color
		t.Text = line
		t.Parent = bb
	end
	bb.Parent = part
end

-- strip from a to b at height y: length on the Z axis, aimed with lookAt
local function strip(a: Vector3, b: Vector3, y: number, color: Color3, w: number, h: number, transparency: number): Part
	local aa = Vector3.new(a.X, y, a.Z)
	local bb2 = Vector3.new(b.X, y, b.Z)
	local len = (bb2 - aa).Magnitude
	local s = mk(Vector3.new(w, h, len), Vector3.zero, color, Enum.Material.Neon, false)
	s.CFrame = CFrame.lookAt((aa + bb2) / 2, bb2)
	s.Transparency = transparency
	return s
end

local chainStrips: { Part } = {}
local clock = 0.0
local lastTouch: { [string]: number } = {}

-- portal landing: NORTH of the floor (derived, never hand-set)
function CathedralPlate.entry(): Vector3
	local center = CathedralMap.plateCenter()
	local size = CathedralMap.plateSize()
	return center + Vector3.new(0, 0, -(size.Z / 2 + 8))
end

function CathedralPlate.build()
	-- the floor: one plate covering every beacon + margin (geometry derived)
	local center = CathedralMap.plateCenter()
	local size = CathedralMap.plateSize()
	local floor = mk(size, center, FLOOR, Enum.Material.Slate, true)
	floor.Name = "CathedralPlate_Floor"
	label(floor, { "THE CATHEDRAL  -  the world map from eigen_centroids", "north = -Z = eigen -y · scan 2026-09-27" }, INK, 6, 420)

	-- region beacons at their eigen positions
	for _, region in ipairs(CathedralMap.regions()) do
		local pos = CathedralMap.toWorld(region)
		local cls = CathedralMap.class(region)
		local color = CathedralMap.classColor(cls)

		local plinth = mk(Vector3.new(5, 1, 5), pos + Vector3.new(0, 1, 0), FLOOR, Enum.Material.Slate, true)
		plinth.Name = ("CathedralBeacon_%s"):format(region)
		mk(Vector3.new(1.6, 12, 1.6), pos + Vector3.new(0, 7.5, 0), color, Enum.Material.Neon, false)
		local orb = Instance.new("Part")
		orb.Anchored = true
		orb.Shape = Enum.PartType.Ball
		orb.Size = Vector3.new(4, 4, 4)
		orb.Position = pos + Vector3.new(0, 16.5, 0)
		orb.Color = color
		orb.Material = Enum.Material.Neon
		orb.CanCollide = false
		orb.Parent = workspace
		orb.Name = ("CathedralOrb_%s"):format(region)

		local cos = CathedralMap.cos(region)
		local c = CathedralMap.centroid(region) or { 0, 0 }
		local cosLine = "cos null (off-manifold)"
		if cos then
			cosLine = string.format("builder cos %.3f", cos)
		end
		label(orb, {
			("%s [%s]"):format(region, cls),
			cosLine,
			string.format("eigen (%.4f, %.4f)", c[1], c[2]),
		}, color, 4, 190)

		-- the walk files its own position rows: touch = a measured arrival
		plinth.Touched:Connect(function(hit: BasePart)
			local player = hit.Parent and Players:GetPlayerFromCharacter(hit.Parent)
			if not player then
				return
			end
			local key = ("%d:%s"):format(player.UserId, region)
			local now = os.clock()
			if now - (lastTouch[key] or -math.huge) < 5 then
				return
			end
			lastTouch[key] = now
			local char = player.Character
			local root = char and char:FindFirstChild("HumanoidRootPart") :: BasePart?
			if root then
				local ex, ey = CathedralMap.worldToEigen(root.Position)
				ShadowLedger.record(player, "The Cathedral", ("reached %s [%s] from eigen (%.4f, %.4f), %.4f away, bearing %.1f")
					:format(region, cls, ex, ey, CathedralMap.distFrom(ex, ey, region),
						CathedralMap.bearingFrom(ex, ey, region)))
			end
		end)
	end

	-- chain strips (operative lean) + hub strips (contested alternate, faint)
	for _, e in ipairs(CathedralMap.chainEdges()) do
		table.insert(chainStrips, strip(CathedralMap.toWorld(e.a), CathedralMap.toWorld(e.b), 11,
			Color3.fromRGB(179, 86, 44), 1.4, 0.35, 0.1))
	end
	for _, e in ipairs(CathedralMap.hubEdges()) do
		strip(CathedralMap.toWorld(e.a), CathedralMap.toWorld(e.b), 10.4,
			Color3.fromRGB(138, 127, 176), 0.9, 0.25, 0.55)
	end

	-- entry plaque: the vote, honestly stated
	local plaque = mk(Vector3.new(10, 1, 6), center + Vector3.new(0, 1.2, size.Z / 2 - 8), FLOOR, Enum.Material.Wood, true)
	plaque.Name = "CathedralPlate_Plaque"
	label(plaque, {
		"descent vote: water_first chain 0.031 vs hub star 0.036 (eigen units)",
		"a VOTE, not a verdict  -  RIB descent-order stays CONTESTED",
		"no edge touches the DARK anchor (riddler_engram); it stands alone",
	}, INK, 5, 420)

	print(("[CathedralPlate] built: %d beacons, %d chain strips, %d hub strips")
		:format(#CathedralMap.regions(), #CathedralMap.chainEdges(), #CathedralMap.hubEdges()))
end

function CathedralPlate.tick(dt: number)
	-- the chain breathes; the hub does not (it is the contested alternate)
	clock += dt
	local pulse = 0.1 + 0.12 * (math.sin(clock * 2) + 1) / 2
	for _, s in ipairs(chainStrips) do
		s.Transparency = pulse
	end
end

return CathedralPlate
