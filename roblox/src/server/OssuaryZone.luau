--!strict
-- OssuaryZone — THE OSSUARY: the spooky skeleton maze dungeon.
-- Clone stack (docs/CLONED_MECHANICS.md + watch/inbox intel): Exanima
-- darkness (torch radius, stacked floors), Lara-Croft-GO state changes
-- (levers shift walls, bone-key gate), weeping-angel sentinels (freeze while
-- observed, hunt while unseen), MUD law: the rooms remember (ShadowLedger).
-- Seasonal: Halloween window, pumpkin braziers, Candy Bones = VM.
-- The Sixth Candle pass (99R): wider torch radius.
--
-- Maze geometry (fixed 2026-09-25 playtest pass): cells live at ODD grid
-- coords 1..GRID, walls at EVEN coords between them. A backtracker steps ±2
-- cells and opens the wall at the integer midpoint. Wall segments not opened
-- are built; the border ring has exactly one gap per floor. worldPos maps
-- grid -> studs so every feature (sentinels, levers, braziers, candy, the
-- Court) sits at reachable cell centers, never inside rock.

local Players = game:GetService("Players")
local Lighting = game:GetService("Lighting")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ServerScriptService = game:GetService("ServerScriptService")
local Shared = ReplicatedStorage:WaitForChild("Modules")
local SeedRng = require(Shared:WaitForChild("SeedRng"))
local SectionStream = require(Shared:WaitForChild("SectionStream"))
local ShadowLedger = require(ServerScriptService:WaitForChild("ShadowLedger"))
local Worldgen = require(ReplicatedStorage:WaitForChild("Modules"):WaitForChild("Worldgen"))

local OssuaryZone = {}
local origin = Vector3.new(-60, 8, 0)
local GRID, CELL = 13, 14
local HALF = (GRID + 1) / 2 -- 7 for GRID 13: world x of grid column x = (x - HALF) * CELL
local TORCH_RADIUS = 26
local CANDLE_RADIUS = 38
local FLOORS = 3
local FLOOR_DROP = 46 -- vertical spacing between floors
-- Q-043 streamed floors: floor 1 (the arrival floor) builds eagerly at boot;
-- floors 2..FLOORS are ordered stream sections with one floor of lookahead.
-- Radius 55 vs the 46-stud drop: standing on floor N puts floor N+1's center
-- ~49 studs away (builds while you play N) and floor N+2 ~95 (stays dark).
local FLOOR_LOOKAHEAD = 55

local walls: { BasePart } = {}
local sentinels: { { part: Part, frozen: boolean } } = {}
local ossuaryModel: Model? = nil
-- Q-043 streamed floors: floors 2..FLOORS ride this ordered stream; tick
-- polls it with player root positions. floorsBuilt gates the floor-2 boulder
-- clock (no boulders into a floor that does not exist yet).
local floorsBuilt = 0
local floorStream: SectionStream.SectionStream? = nil

local function worldPos(base: Vector3, gx: number, gz: number): Vector3
	return base + Vector3.new((gx - HALF) * CELL, 0, (gz - HALF) * CELL)
end

local function cellCenter(base: Vector3, rng, floorBaseY: number): Vector3
	-- odd coords only: a real cell, never rock
	local gx = 2 * rng:int(1, (GRID + 1) // 2) - 1
	local gz = 2 * rng:int(1, (GRID + 1) // 2) - 1
	return worldPos(base, gx, gz) + Vector3.new(0, floorBaseY, 0)
end

-- ---- seeded maze: recursive backtracker, odd cells / even walls ----
local function buildFloor(rng, floor: number, model: Model): Vector3
	local base = origin + Vector3.new(0, (floor - 1) * -FLOOR_DROP, 0)
	local wallColor = Color3.fromRGB(58, 54, 50)

	local slab = Instance.new("Part")
	slab.Anchored = true
	slab.Size = Vector3.new(GRID * CELL + CELL, 1, GRID * CELL + CELL)
	slab.Position = base + Vector3.new(0, -0.5, 0)
	slab.Color = Color3.fromRGB(40, 38, 42)
	slab.Material = Enum.Material.Slate
	slab.Parent = model

	local visited: { [string]: boolean } = {}
	local opened: { [string]: boolean } = {}
	local stack = { { 1, 1 } }
	visited["1,1"] = true
	while #stack > 0 do
		local cur = stack[#stack]
		local neighbors = {}
		for _, d in ipairs({ { 2, 0 }, { -2, 0 }, { 0, 2 }, { 0, -2 } }) do
			local nx, nz = cur[1] + d[1], cur[2] + d[2]
			if nx >= 1 and nx <= GRID and nz >= 1 and nz <= GRID and not visited[(nx .. "," .. nz)] then
				table.insert(neighbors, { nx, nz })
			end
		end
		if #neighbors == 0 then
			table.remove(stack)
		else
			local nxt = neighbors[rng:int(1, #neighbors)]
			visited[(nxt[1] .. "," .. nxt[2])] = true
			-- the wall between two cells: integer midpoint, direction-derived
			local mx = (cur[1] + nxt[1]) / 2
			local mz = (cur[2] + nxt[2]) / 2
			opened[(mx .. "," .. mz)] = true
			table.insert(stack, nxt)
		end
	end

	-- interior walls: at even coords between cells; skip the opened ones
	for gx = 1, GRID - 1 do
		for gz = 1, GRID do
			local isWallCoord = (gx % 2 == 0) -- vertical wall between (gx-1,gz),(gx+1,gz)... pairs
			-- vertical wall segments sit at even gx, odd gz
			if isWallCoord and gz % 2 == 1 and not opened[(gx .. "," .. gz)] then
				local w = Instance.new("Part")
				w.Anchored = true
				w.Size = Vector3.new(1.5, 9, CELL)
				w.Position = worldPos(base, gx, gz) + Vector3.new(0, 4.5, 0)
				w.Color = wallColor
				w.Material = Enum.Material.Slate
				w.Parent = model
				table.insert(walls, w)
			end
		end
	end
	for gx = 1, GRID do
		for gz = 1, GRID - 1 do
			-- horizontal wall segments sit at odd gx, even gz
			if gx % 2 == 1 and gz % 2 == 0 and not opened[(gx .. "," .. gz)] then
				local w = Instance.new("Part")
				w.Anchored = true
				w.Size = Vector3.new(CELL, 9, 1.5)
				w.Position = worldPos(base, gx, gz) + Vector3.new(0, 4.5, 0)
				w.Color = wallColor
				w.Material = Enum.Material.Slate
				w.Parent = model
				table.insert(walls, w)
			end
		end
	end

	-- border ring: solid, with exactly one gap per floor
	-- floor 1: entry gap on the +x side; floor FLOORS: court gap on the +z side
	local gapX = HALF -- world x = 0
	local gapZ = HALF -- world z = 0
	local function borderWall(pos: Vector3, size: Vector3)
		local w = Instance.new("Part")
		w.Anchored = true
		w.Size = size
		w.Position = pos
		w.Color = Color3.fromRGB(30, 28, 32)
		w.Material = Enum.Material.Slate
		w.Parent = model
		table.insert(walls, w)
	end

	for i = 0, GRID + 1, 2 do -- even coords: wall positions
		local xw = worldPos(base, i, 0)
		-- -z side (solid)
		borderWall(xw + Vector3.new(0, 5.5, 0), Vector3.new(CELL, 11, 2))
		-- +z side (gap on floor FLOORS at gx == gapX)
		if not (floor == FLOORS and i == gapX) then
			borderWall(worldPos(base, i, GRID + 1) + Vector3.new(0, 5.5, 0), Vector3.new(CELL, 11, 2))
		end
		-- -x side (solid)
		borderWall(worldPos(base, 0, i) + Vector3.new(0, 5.5, 0), Vector3.new(2, 11, CELL))
		-- +x side (gap on floor 1 at gz == gapZ)
		if not (floor == 1 and i == gapZ) then
			borderWall(worldPos(base, GRID + 1, i) + Vector3.new(0, 5.5, 0), Vector3.new(2, 11, CELL))
		end
	end

	return base
end

-- ---- skeleton sentinels: weeping angels ----
local function spawnSentinel(rng, base: Vector3, model: Model)
	local s = Instance.new("Part")
	s.Size = Vector3.new(3, 7, 3)
	s.Color = Color3.fromRGB(216, 210, 190)
	s.Material = Enum.Material.Sand
	s.Position = cellCenter(base, rng, 6.5)
	s.Name = "BoneSentinel"
	s.Parent = model
	local eye = Instance.new("PointLight")
	eye.Color = Color3.fromRGB(255, 120, 40)
	eye.Range = 8
	eye.Brightness = 2
	eye.Parent = s
	table.insert(sentinels, { part = s, frozen = true })
end

local function playerAtY(player: Player, y: number): BasePart?
	local root = player.Character and player.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
	if root and math.abs(root.Position.Y - y) < FLOOR_DROP / 2 then return root end
	return nil
end

-- ---- levers: Lara-Croft-GO state changes (two walls swap) ----
local levers: { { a: BasePart, b: BasePart } } = {}

local function makeLever(rng, base: Vector3, floorBaseY: number, model: Model)
	local floorWalls = {}
	for _, w in ipairs(walls) do
		if math.abs(w.Position.Y - (floorBaseY + 4.5)) < 2 then table.insert(floorWalls, w) end
	end
	if #floorWalls < 2 then return end
	local a = floorWalls[rng:int(1, #floorWalls)]
	local b = floorWalls[rng:int(1, #floorWalls)]
	if a == b then return end
	local lever = Instance.new("Part")
	lever.Anchored = true
	lever.Size = Vector3.new(1.5, 5, 1.5)
	lever.Color = Color3.fromRGB(200, 150, 60)
	lever.Material = Enum.Material.Wood
	lever.Position = cellCenter(base, rng, floorBaseY) + Vector3.new(0, 2.5, 0)
	lever.Name = "BoneLever"
	lever.Parent = model
	local prompt = Instance.new("ProximityPrompt")
	prompt.ActionText = "Pull the bone lever"
	prompt.ObjectText = "the walls remember"
	prompt.HoldDuration = 1
	prompt.Parent = lever
	local pair = { a = a, b = b }
	prompt.Triggered:Connect(function(player: Player)
		local pa, pb = pair.a.Position, pair.b.Position
		pair.a.Position, pair.b.Position = pb, pa -- the corridor state changes
		ShadowLedger.record(player, "Ossuary", "pulled a bone lever; the walls moved")
	end)
	table.insert(levers, pair)
end

-- ---- braziers / candy / boulders ----
local function makeBrazier(rng, base: Vector3, floorBaseY: number, model: Model)
	local b = Instance.new("Part")
	b.Shape = Enum.PartType.Ball
	b.Size = Vector3.new(2.5, 2.5, 2.5)
	b.Color = Color3.fromRGB(255, 140, 50)
	b.Material = Enum.Material.Neon
	b.Position = cellCenter(base, rng, floorBaseY) + Vector3.new(0, 1.5, 0)
	b.Name = "PumpkinBrazier"
	local light = Instance.new("PointLight")
	light.Color = Color3.fromRGB(255, 140, 50)
	light.Range = 22
	light.Brightness = 1.6
	light.Parent = b
	b.Parent = model
end

-- Per-floor daily candy cap. SEASONAL_LAUNCH.md FALSIFIERS ("cap candy per
-- floor per day if needed") named no number; the cap derives from this file's
-- own spawn math: each floor emits exactly 6 static Candy Bones at build
-- (OssuaryZone.build, 6x dropCandy per floor), so 6 candy/floor/day is the
-- least-surprising bound: a full daily sweep of every floor always pays, and
-- only overflow beyond a floor's daily spawn (the Skeleton King's 40-candy
-- shower, celebration on top of his 500 VM award) is muted. Baseline print
-- becomes max 12 VM/floor/day (36/day, 72 with the Candy Doubler) against
-- 50-3000 VM Exchange SKUs and the 5000 VM rebirth (LedgerExchange.luau), so
-- the loop is not starved.
local CANDY_PER_FLOOR_DAILY_CAP = 6

local function candyTallyAttr(floor: number): string
	return "CandyFloorTally" .. floor
end

-- true = this pickup is under the cap and may pay; burns one slot of the
-- player's per-floor daily allowance (UTC day stamp, per-player attributes,
-- the same store as VirtueDoublerUntil). Capped candy is NOT consumed: it
-- pays nothing that day and stays in the world for a later day, so there
-- are no pay-nothing pickups while the per-floor daily print stays bounded.
local function candyAllowed(plr: Player, floor: number): boolean
	local today = math.floor(os.time() / 86400)
	if plr:GetAttribute("CandyCapDay") ~= today then
		for f = 1, FLOORS do
			plr:SetAttribute(candyTallyAttr(f), 0)
		end
		plr:SetAttribute("CandyCapDay", today)
	end
	local key = candyTallyAttr(floor)
	local tally = tonumber(plr:GetAttribute(key)) or 0
	if tally >= CANDY_PER_FLOOR_DAILY_CAP then
		return false
	end
	plr:SetAttribute(key, tally + 1)
	return true
end

-- jitter (optional): explicit per-call offset replacing the internal
-- math.random(-6,6) scatter. t38 fix receipt: the seeded build loop
-- (SeedRng.new(20261031), OssuaryZone.build) called dropCandy with no way
-- to seed this scatter, so worldgen candy positions were unreplayable.
-- Callers in seeded paths must pass an explicit jitter (build passes
-- Vector3.zero; its spread is the deterministic spiral at the call site);
-- the King shower (runtime event, t29) passes nothing and keeps the
-- math.random scatter. When jitter is nil the behavior is byte-identical
-- to the pre-t38 expression.
local function dropCandy(at: Vector3, floor: number, jitter: Vector3?)
	local c = Instance.new("Part")
	c.Shape = Enum.PartType.Ball
	c.Size = Vector3.new(1.2, 1.2, 1.2)
	c.Color = Color3.fromRGB(255, 100, 160)
	c.Material = Enum.Material.Neon
	local j = jitter or Vector3.new(math.random(-6, 6), 0, math.random(-6, 6))
	c.Position = at + Vector3.new(j.X, 1.5, j.Z)
	c.Name = "CandyBone"
	c.Parent = workspace
	c.Touched:Connect(function(hit)
		local plr = hit.Parent and Players:GetPlayerFromCharacter(hit.Parent)
		if plr and candyAllowed(plr, floor) then
			-- fix receipt: this line read "CandyDoublerUntil", an attribute with
			-- zero writers (grep -rn DoublerUntil roblox/src, 2026-09-25); the
			-- 149R SKU writes VirtueDoublerUntil (Monetization.luau:46) per
			-- ROBLOX_MONETIZATION_PLAN_20260924.md "Double marks for 1 hour",
			-- so the doubler never doubled candy. Reader aligned to the writer.
			local mult = (plr:GetAttribute("VirtueDoublerUntil") and plr:GetAttribute("VirtueDoublerUntil") > os.time()) and 2 or 1
			plr:SetAttribute("VirtueMarks", tonumber((plr:GetAttribute("VirtueMarks")) or 0) + 2 * mult)
			c:Destroy()
		end
	end)
end

local function rollBoulder(base: Vector3)
	local b = Instance.new("Part")
	b.Shape = Enum.PartType.Ball
	b.Size = Vector3.new(6, 6, 6)
	b.Color = Color3.fromRGB(120, 110, 100)
	b.Material = Enum.Material.Slate
	b.Position = base + Vector3.new(0, 20, -(HALF) * CELL + 4)
	b.Name = "BoneBoulder"
	b.Parent = workspace
	b.AssemblyLinearVelocity = Vector3.new(0, -5, 40)
	b.Touched:Connect(function(hit)
		local plr = hit.Parent and Players:GetPlayerFromCharacter(hit.Parent)
		local hum = plr and plr.Character and plr.Character:FindFirstChildOfClass("Humanoid")
		if hum then hum.Health = 0 end -- honest crush
	end)
	task.delay(12, function()
		if b.Parent then b:Destroy() end
	end)
end

-- ---- the Skeleton King + Bone Key ----
local king: BasePart? = nil

local function buildCourt(base: Vector3, model: Model)
	-- the Bone Key: floor 3 antechamber, near the court gap
	local key = Instance.new("Part")
	key.Size = Vector3.new(1.2, 3, 0.4)
	key.Color = Color3.fromRGB(235, 225, 190)
	key.Material = Enum.Material.Neon
	key.Position = worldPos(base, HALF, GRID - 2) + Vector3.new(0, 2, 0)
	key.Name = "BoneKey"
	key.Parent = model
	key.Touched:Connect(function(hit)
		local plr = hit.Parent and Players:GetPlayerFromCharacter(hit.Parent)
		if plr and not plr:GetAttribute("BoneKey") then
			plr:SetAttribute("BoneKey", true)
			key:Destroy()
			ShadowLedger.record(plr, "Ossuary", "took the Bone Key", true)
		end
	end)

	-- the wooden gate sits exactly in the border gap; key-holders walk through
	local gate = Instance.new("Part")
	gate.Anchored = true
	gate.Size = Vector3.new(CELL, 11, 2)
	gate.Position = worldPos(base, HALF, GRID + 1) + Vector3.new(0, 5.5, 0)
	gate.Color = Color3.fromRGB(90, 70, 50)
	gate.Material = Enum.Material.Wood
	gate.Name = "CourtGate"
	gate.Parent = model
	gate.Touched:Connect(function(hit)
		local plr = hit.Parent and Players:GetPlayerFromCharacter(hit.Parent)
		if plr and plr:GetAttribute("BoneKey") then
			gate.CanCollide = false
			gate.Transparency = 0.85
		end
	end)

	-- the King
	local kingPart = Instance.new("Part")
	kingPart.Size = Vector3.new(6, 14, 6)
	kingPart.Color = Color3.fromRGB(226, 218, 196)
	kingPart.Material = Enum.Material.Sand
	kingPart.Position = worldPos(base, HALF, GRID - 4) + Vector3.new(0, 7, 0)
	kingPart.Name = "THE SKELETON KING"
	local crown = Instance.new("PointLight")
	crown.Color = Color3.fromRGB(255, 200, 80)
	crown.Range = 18
	crown.Brightness = 3
	crown.Parent = kingPart
	local tag = Instance.new("BillboardGui")
	tag.Size = UDim2.new(0, 260, 0, 34)
	tag.StudsOffset = Vector3.new(0, 8, 0)
	tag.AlwaysOnTop = true
	local lbl = Instance.new("TextLabel")
	lbl.Size = UDim2.fromScale(1, 1)
	lbl.BackgroundTransparency = 1
	lbl.Text = "THE SKELETON KING · he does not move while you watch"
	lbl.TextColor3 = Color3.fromRGB(255, 220, 150)
	lbl.Font = Enum.Font.Garamond
	lbl.TextSize = 16
	lbl.Parent = tag
	tag.Parent = kingPart
	kingPart.Parent = model
	king = kingPart

	kingPart.Touched:Connect(function(hit)
		local plr = hit.Parent and Players:GetPlayerFromCharacter(hit.Parent)
		if plr and plr:GetAttribute("BoneKey") and king and not king:GetAttribute("Felled") then
			king:SetAttribute("Felled", true)
			plr:SetAttribute("VirtueMarks", tonumber((plr:GetAttribute("VirtueMarks")) or 0) + 500)
			lbl.Text = "THE CROWN ROLLS. THE COURT FILES IT."
			ShadowLedger.record(plr, "Ossuary", "felled the Skeleton King with the Bone Key", true)
			for i = 1, 40 do
				-- the King stands on the top floor. t29 fix receipt: all 40 used
				-- to pass bare king.Position (one physical point; dropCandy:275
				-- still adds its own math.random(-6,6) per axis, so parts landed
				-- in a ~8.5-stud disc, stacked and intersecting). Under the
				-- per-floor 6/day cap that pile is one sweep for whoever fells
				-- him, muting the rest of the shower for that player that day.
				-- Now an index-derived Vogel spiral (golden angle; no rng
				-- instance reaches this closure, so no SeedRng and no new
				-- math.random: replay-safe by construction). Radius 4 keeps the
				-- worst-case offset (4 + sqrt(6^2+6^2) = 12.49 studs) inside the
				-- King's own cell, clear of the 14-stud wall planes minus 0.75
				-- half-thickness minus 0.6 candy radius = 12.65. Spread is
				-- positional only; the cap's muting of shower overflow stays as
				-- documented at CANDY_PER_FLOOR_DAILY_CAP (t2's stated intent).
				local r = 4 * math.sqrt(i / 40)
				local a = i * 2.399963229728653 -- golden angle, radians
				dropCandy(king.Position + Vector3.new(r * math.cos(a), 0, r * math.sin(a)), FLOORS)
			end
			task.delay(30, function()
				if king then king:SetAttribute("Felled", nil) end
			end)
		elseif plr and not plr:GetAttribute("BoneKey") then
			local hum = plr.Character and plr.Character:FindFirstChildOfClass("Humanoid")
			if hum then hum.Health = 0 end -- you brought nothing to a coronation
		end
	end)
end

-- ---- build ----
function OssuaryZone.build(): Model
	local model = Instance.new("Model")
	model.Name = "TheOssuary"

	Lighting.Brightness = 1
	Lighting.FogEnd = 90
	Lighting.FogColor = Color3.fromRGB(8, 6, 10)
	Lighting.ClockTime = 0
	local atmo = Instance.new("Atmosphere")
	atmo.Density = 0.55
	atmo.Color = Color3.fromRGB(60, 50, 70)
	atmo.Parent = Lighting

	local rng = SeedRng.new(20261031)

	-- Q-043 streamed floors (GnomeCode ep.1 pattern, ARCHITECTURE_NEXT move 1):
	-- buildFloorSection is the per-floor body of the old eager loop, UNCHANGED
	-- and in the same order, so the shared SeedRng(20261031) stream draws
	-- identically per floor. Floors build strictly in ascending order — eager
	-- floor 1 here, floors 2..FLOORS via an ORDERED SectionStream whose
	-- insertion order equals rng draw order — so the streamed world is
	-- byte-identical to the eager one, only later in time. Boot cost drops
	-- from 3 full grids to 1; the deep floors materialize around whoever
	-- descends (one floor of lookahead, FLOOR_LOOKAHEAD above).
	local function buildFloorSection(floor: number)
		local base = origin + Vector3.new(0, (floor - 1) * -FLOOR_DROP, 0)
		buildFloor(rng, floor, model)
		for _ = 1, 3 + floor do
			spawnSentinel(rng, base, model)
		end
		for _ = 1, 4 do
			makeBrazier(rng, base, 1.5, model)
		end
		if floor >= 2 then
			makeLever(rng, base, 4.5, model)
		end
		-- t38 fix receipt: this loop read "for _ = 1, 6: dropCandy(base +
		-- Vector3.new(0, 1.5, 0), floor)", stacking all 6 static candies on
		-- ONE physical point (the maze center cell, world (0, y, 0)); the
		-- only spread was dropCandy's internal math.random(-6,6) per axis,
		-- unseeded inside an otherwise seeded build (SeedRng.new(20261031)).
		-- Six 1.2-stud balls in a ~8.5-stud disc intersect into one grab
		-- sweep, and no seed reproduces their landing spots. Now the t29
		-- King-shower pattern, index-derived Vogel spiral (golden angle;
		-- zero rng draws, zero math.random in this seeded path: replay-safe
		-- by construction, and the shared 20261031 stream is untouched, so
		-- floors 1-2 maze/sentinel/brazier/lever draws are byte-identical to
		-- pre-t38). jitter=Vector3.zero suppresses dropCandy's internal
		-- scatter (nil would re-add unseeded math.random to worldgen).
		-- Geometry: center cell (grid 7,7, odd = real cell) spans +-7 studs;
		-- wall inner face at 7 - 0.75 = 6.25; candy radius 0.6 -> max safe
		-- center offset 5.65. Radius 5 keeps the outer drop 0.65 studs clear
		-- of rock; computed pair distances (python, 2026-09-25): radii
		-- 2.041/2.887/3.536/4.082/4.564/5.000, min pairwise center distance
		-- 3.270 studs vs the 1.2-stud touch threshold: no stacking, no
		-- intersection. Count unchanged: 6 per floor, CANDY_PER_FLOOR_DAILY_CAP
		-- math and the cap comment above still hold.
		for i = 1, 6 do
			local r = 5 * math.sqrt(i / 6)
			local a = i * 2.399963229728653 -- golden angle, radians (t29 constant)
			dropCandy(base + Vector3.new(r * math.cos(a), 1.5, r * math.sin(a)), floor, Vector3.zero)
		end
		if floor == FLOORS then
			buildCourt(base, model)
		end
		floorsBuilt += 1
	end

	local stream = SectionStream.new({ radius = FLOOR_LOOKAHEAD, budget = 1, ordered = true })
	for floor = 2, FLOORS do
		local f = floor
		stream:add(origin + Vector3.new(0, (f - 1) * -FLOOR_DROP, 0), function()
			buildFloorSection(f)
		end)
	end
	floorStream = stream
	buildFloorSection(1)
	-- players already in the zone when the model lands get their lookahead
	-- immediately; everyone else is covered by the tick poll below
	local bootRoots: { Vector3 } = {}
	for _, p in ipairs(Players:GetPlayers()) do
		local root = p.Character and p.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
		if root then table.insert(bootRoots, root.Position) end
	end
	stream:poll(bootRoots)

	-- carried torchlight: new joiners AND anyone already here
	local function attachTorch(player: Player)
		local function onChar(char: Model)
			local root = char:WaitForChild("HumanoidRootPart") :: BasePart
			if root:FindFirstChild("TorchLight") then return end
			local torch = Instance.new("PointLight")
			torch.Name = "TorchLight"
			torch.Color = Color3.fromRGB(255, 170, 90)
			torch.Range = player:GetAttribute("SixthCandle") and CANDLE_RADIUS or TORCH_RADIUS
			torch.Brightness = 2.2
			torch.Parent = root
		end
		player.CharacterAdded:Connect(onChar)
		if player.Character then onChar(player.Character) end
	end
	Players.PlayerAdded:Connect(attachTorch)
	for _, p in ipairs(Players:GetPlayers()) do
		attachTorch(p)
	end

	ossuaryModel = model
	model.Parent = workspace
	return model
end

-- ---- tick: sentinels hunt while unobserved, freeze while seen ----
local lastBoulder = 0

function OssuaryZone.tick(dt: number)
	-- Q-043: stream the deep floors around whoever is in the zone (GnomeCode
	-- ep.1 pattern). Ordered mode builds floors strictly 2 -> 3, keeping the
	-- shared SeedRng(20261031) draw order so the streamed world is identical
	-- to the old eager build. One floor of lookahead: standing on floor N
	-- materializes N+1, floor N+2 stays dark until N+1 is reached.
	local stream = floorStream
	if stream then
		local roots: { Vector3 } = {}
		for _, p in ipairs(Players:GetPlayers()) do
			local root = p.Character and p.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
			if root then table.insert(roots, root.Position) end
		end
		if #roots > 0 then
			stream:poll(roots)
		end
	end

	for _, s in ipairs(sentinels) do
		local part = s.part
		if not part.Parent then continue end
		local observed = false
		local hunter: Player? = nil
		for _, p in ipairs(Players:GetPlayers()) do
			local root = playerAtY(p, part.Position.Y)
			if root then
				hunter = p
				local d = (root.Position - part.Position)
				if d.Magnitude < 40 then
					local params = RaycastParams.new()
					local filter: { Instance } = { part }
					if ossuaryModel then table.insert(filter, ossuaryModel) end
					params.FilterDescendantsInstances = filter
					params.FilterType = Enum.RaycastFilterType.Exclude
					local hit = workspace:Raycast(part.Position, d.Unit * d.Magnitude, params)
					if not hit or (p.Character and hit.Instance:IsDescendantOf(p.Character)) then
						observed = true
					end
				end
			end
		end
		s.frozen = observed
		part.Color = observed and Color3.fromRGB(230, 226, 208) or Color3.fromRGB(150, 60, 50)
		if hunter then
			local root = hunter.Character and hunter.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
			if root then
				local dir = (root.Position - part.Position)
				if not observed and dir.Magnitude > 2 then
					-- hunt: glide at the player (the CFrame:Lerp instance call, fixed)
					part.CFrame = part.CFrame:Lerp(CFrame.new(root.Position - dir.Unit * 1.5), math.clamp(dt * 2.2, 0, 1))
				elseif observed and dir.Magnitude < 3 then
					local hum = hunter.Character and hunter.Character:FindFirstChildOfClass("Humanoid")
					if hum then hum.Health = 0 end -- the stare shields at distance; touch does not
				end
			end
		end
	end

	-- boulders on a slow clock, floor 2 only. Q-043: gated on floorsBuilt —
	-- the stream builds floor 2 on first descent, and a boulder rolled into
	-- a not-yet-built floor would just drop into the dark every 20s.
	lastBoulder += dt
	if lastBoulder > 20 and floorsBuilt >= 2 then
		lastBoulder = 0
		rollBoulder(origin + Vector3.new(0, -FLOOR_DROP, 0))
	end
end

return OssuaryZone
