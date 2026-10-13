--!strict
-- MazeArenaZone — THE STACKED ARENA (dashboard/static/games/maze_arena.html).
-- Four rounds around the cheese-light: R1 RACE TO THE CHEESE · R2 MOVING WALLS
-- (gold invariants never move; cyan bars slide to their alt) · R3 THE LIGHT
-- WALKS (beacon patrols BEACON_PATH) · R4 STAYING IS THE WIN (dwell inside the
-- beacon's 110-deg gaze scores; arrival doesn't). Six LAW_SHARDS + the red
-- assumption (the dragon that hunts in the dark) from the v1 player layer.
-- GAPS: the ray-field/BFS lightmap render, the GPS/dumb/WAY/model-seat agents,
-- the odd-eta curl, the lantern rescue field and ?real=1 constellation are
-- sim/render layers — avatars ARE the agents; round clock + wall moves shared,
-- arrival/dwell/score per player. PACING: source 60 ticks/s at 0.016 u/tick
-- (0.96 u/s) vs Roblox 16 studs/s at SCALE=100 (0.16 u/s), so durations x6 and
-- per-second speeds /6 preserve crossings-per-round; all source numbers quoted.
-- Deterministic source (fixed walls, fixed path): nothing score-bearing is
-- random — no SeedRng.

local Players = game:GetService("Players")
local ShadowLedger = require((script.Parent:FindFirstChild("ShadowLedger") or script.Parent.Parent:WaitForChild("ShadowLedger")) :: ModuleScript)

local MazeArenaZone = {}
local origin = Vector3.new(300, 8, 0)
local SCALE = 100 -- studs per maze unit (source: W=480 px for 2.0 units)
local TICK, PACING = 1 / 60, 6

-- walls [cx,cy,hw,hh] in source maze-space (the literal already x2 / y2.7 scaled)
local WALLS = {
	{1.0, 1.35, 0.06, 0.81}, {0.5, 0.81, 0.40, 0.081}, {0.5, 1.944, 0.40, 0.081},
	{1.0, 1.35, 0.06, 0.756}, {1.5, 0.81, 0.40, 0.081}, {1.5, 1.944, 0.40, 0.081},
	{0.24, 1.404, 0.06, 0.594}, {1.76, 1.35, 0.06, 0.594},
	{1.24, 0.378, 0.06, 0.432}, {0.76, 2.376, 0.06, 0.432},
}
local MOVERS = {2, 3, 5, 6} -- source 0-based movers {1,2,4,5}
local MOVER_ALTS: {[number]: {number}} = {[2] = {0.28, 0.81}, [3] = {0.28, 1.944}, [5] = {1.72, 0.81}, [6] = {1.72, 1.944}}
local WALLS_BASE = {} -- resetWalls truth
for i, w in WALLS do WALLS_BASE[i] = {w[1], w[2], w[3], w[4]} end
local PATH = {{1.2, 1.35}, {1.9, 0.5}, {0.5, 0.5}, {0.35, 2.2}, {1.7, 2.35}} -- BEACON_PATH
local SHARDS = { -- LAW_SHARDS verbatim
	{x = 0.7, y = 0.35, law = "THE TAPE VERIFIES", sub = "every claim carries its hash"},
	{x = 1.6, y = 0.9, law = "SUBSTANCE GATE", sub = "nothing counts until it compiles"},
	{x = 0.45, y = 1.7, law = "THE PATIENCE LAW", sub = "queue is a position, the reset is the tide"},
	{x = 1.9, y = 1.9, law = "THE MICKEY LAW", sub = "die, reprint, be smarter"},
	{x = 0.3, y = 2.1, law = "FILES ARE THE BODY", sub = "the shelf outlives every seat"},
	{x = 1.1, y = 0.4, law = "KEY LAW", sub = "pool keys for programs, plans for people"},
}
-- ROUND_CFG source ticks @60fps -> seconds = ticks * TICK * PACING (90/150/150/180)
local ROUNDS: { {dur: number, label: string, moveEvery: number?, stayR: number?, gazeDeg: number?} } = {
	{dur = 900, label = "RACE TO THE CHEESE"},
	{dur = 1500, label = "MOVING WALLS", moveEvery = 210},
	{dur = 1500, label = "THE LIGHT WALKS"},
	{dur = 1800, label = "STAYING IS THE WIN", stayR = 79, gazeDeg = 55}, -- stayR: 190 px; gaze half-angle 55 (the 110-deg sector)
}
local SCAN_SPEED = 0.24 -- r1 scanSpeed 0.004 rad/tick @60fps (the gaze scans)
local BEACON_SPD = 5    -- beaconSpeed 0.005 u/tick, /6 for pacing -> studs/s
local DRAGON_SPD = 6    -- dragon speed 0.006 u/tick, /6 (source's 0.4 yaw squash dropped: world is isotropic)
local GOLD, CYAN = Color3.fromRGB(232, 201, 106), Color3.fromRGB(124, 245, 255)

local wallParts: {BasePart}, shardParts: {BasePart} = {}, {}
-- annotation exactness (t42 triage, lanes/t42.check.txt rows 2-3): both are assigned Instance.new("Part") before the Shape writes; BasePart? lacked Shape. Runtime unchanged.
local cheese: Part? = nil
local dragon: Part? = nil
local round, roundT, aim, wp = 1, 0, 0, 2
local nextMove, wallMoves, awake = 21, 0, false
local runState: {[Player]: {arrived: boolean, dwell: number, scored: number}} = {}

local function toWorld(mx: number, my: number): Vector3
	return origin + Vector3.new((mx - 1) * SCALE, 0, (my - 1.35) * SCALE)
end

local function placeWall(i: number)
	wallParts[i].CFrame = CFrame.new(toWorld(WALLS[i][1], WALLS[i][2]) + Vector3.new(0, 8, 0))
end

function MazeArenaZone.build(): Model
	local model = Instance.new("Model")
	model.Name = "StackedArena"
	local floor = Instance.new("Part")
	floor.Anchored, floor.Size = true, Vector3.new(220, 1, 290)
	floor.CFrame = CFrame.new(origin - Vector3.new(0, 0.5, 0))
	floor.Color, floor.Material = Color3.fromRGB(3, 8, 6), Enum.Material.Slate -- the page's --bg
	floor.Parent = model
	floor.Touched:Connect(function(hit)
		local player = hit.Parent and Players:GetPlayerFromCharacter(hit.Parent)
		if player and not runState[player] then
			runState[player] = {arrived = false, dwell = 0, scored = 0}
			ShadowLedger.record(player, "MazeArena", "stepped onto the stacked arena", true)
		end
	end)

	for i = 1, #WALLS do
		local w = WALLS[i]
		local p = Instance.new("Part")
		p.Anchored = true
		p.Size = Vector3.new(math.max(w[3] * 2 * SCALE, 2), 16, math.max(w[4] * 2 * SCALE, 2))
		p.Color, p.Material = GOLD, Enum.Material.Neon -- gold invariants cast the longest shadows (unmoved = gold)
		p.Name = "Wall_" .. i
		p.Parent = model
		wallParts[i] = p
		placeWall(i)
	end
	cheese = Instance.new("Part")
	cheese.Shape = Enum.PartType.Ball
	cheese.Size = Vector3.new(12, 12, 12) -- CHEESE.R = 0.06 u = 6 studs
	cheese.CFrame = CFrame.new(toWorld(1.2, 1.35) + Vector3.new(0, 7, 0)) -- CHEESE0
	cheese.Color, cheese.Material = GOLD, Enum.Material.Neon
	cheese.CanCollide, cheese.Anchored, cheese.Name = false, true, "CheeseLight"
	cheese.Parent = model
	dragon = Instance.new("Part") -- the red assumption hunts in the dark
	dragon.Shape = Enum.PartType.Ball
	dragon.Size = Vector3.new(6, 6, 6)
	dragon.CFrame = CFrame.new(toWorld(1.9, 2.2) + Vector3.new(0, 5, 0))
	dragon.Color, dragon.Material = Color3.fromRGB(255, 85, 85), Enum.Material.Neon
	dragon.CanCollide, dragon.Anchored, dragon.Name = false, true, "TheAssumption" -- phases through walls in the source too
	dragon.Parent = model
	for _, s in SHARDS do -- blue shards are real laws
		local p = Instance.new("Part")
		p.Size, p.Anchored = Vector3.new(3, 3, 3), true
		p.CFrame = CFrame.new(toWorld(s.x, s.y) + Vector3.new(0, 3, 0))
		p.Color, p.Material = CYAN, Enum.Material.Neon
		p.Parent = model
		table.insert(shardParts, p)
	end
	model.Parent = workspace
	return model
end

function MazeArenaZone.tick(dt: number)
	local c, dgn = cheese, dragon
	if not c or not dgn then return end
	local cfg = ROUNDS[round]
	roundT += dt
	if round == 1 then aim = (aim + SCAN_SPEED * dt) % (math.pi * 2) end
	if round == 2 and cfg.moveEvery and roundT >= nextMove then
		nextMove += cfg.moveEvery * TICK * PACING -- moveEvery 210 ticks = 21s paced
		local idx = MOVERS[(wallMoves % #MOVERS) + 1]
		wallMoves += 1
		local alt = MOVER_ALTS[idx]
		if alt then -- bars slide along their own axis (one alt each: once per run)
			WALLS[idx][1], WALLS[idx][2] = alt[1], alt[2]
			placeWall(idx)
			wallParts[idx].Color = CYAN
		end
	end
	if round == 3 or round == 4 then -- the light walks
		local target = toWorld(PATH[wp][1], PATH[wp][2]) + Vector3.new(0, 7, 0)
		local delta = target - c.Position
		local step = BEACON_SPD * dt
		if delta.Magnitude <= math.max(1, step * 2) then -- src: advance when d < sp*2 (two ticks of travel)
			wp = wp % #PATH + 1
		else
			c.CFrame = CFrame.new(c.Position + delta.Unit * step)
			aim = math.atan2(delta.Z, delta.X) -- the beacon faces its heading (gaze law)
		end
	end

	for plr, st in runState do
		local char = plr.Character
		local root = char and char:FindFirstChild("HumanoidRootPart") :: BasePart?
		if not root then continue end
		local off = root.Position - c.Position
		local flat = Vector3.new(off.X, 0, off.Z)
		if round <= 3 and not st.arrived and flat.Magnitude < 8 then
			st.arrived = true
			plr:SetAttribute("ArenaScore", tonumber((plr:GetAttribute("ArenaScore")) or 0) + 100)
			ShadowLedger.record(plr, "MazeArena", ("reached the cheese-light in R%d %s"):format(round, ROUNDS[round].label), true)
		end
		if round == 4 and cfg.stayR and cfg.gazeDeg and flat.Magnitude < cfg.stayR then -- STAYING IS THE WIN: dwell inside the gaze
			local ang = math.atan2(flat.Z, flat.X)
			local ad = math.abs(math.atan2(math.sin(ang - aim), math.cos(ang - aim)))
			if ad <= math.rad(cfg.gazeDeg) then
				st.dwell += dt
				plr:SetAttribute("ArenaDwell", math.floor(st.dwell))
				if st.dwell >= st.scored + 1 then -- +5 per full second held inside the gaze
					st.scored = math.floor(st.dwell)
					plr:SetAttribute("ArenaScore", tonumber((plr:GetAttribute("ArenaScore")) or 0) + 5)
				end
			end
		end
		for i, s in shardParts do
			if s.Parent and (root.Position - s.Position).Magnitude < 9 then -- src pickup < 0.08 u
				plr:SetAttribute("Laws", tonumber((plr:GetAttribute("Laws")) or 0) + 1)
				plr:SetAttribute("ArenaFlash", SHARDS[i].law .. " — " .. SHARDS[i].sub)
				s:Destroy()
				ShadowLedger.record(plr, "MazeArena", "took the law shard: " .. SHARDS[i].law, true)
			end
		end
	end

	if not awake then -- wakes in dark regions: src wakes inside 0.5 u = 50 studs
		for _, plr in Players:GetPlayers() do
			local root = plr.Character and plr.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
			if root and (root.Position - dgn.Position).Magnitude < 50 then awake = true break end
		end
	else
		local nearest: BasePart? = nil
		local nd = 1e9
		for _, plr in Players:GetPlayers() do
			local root = plr.Character and plr.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
			if root then
				local d = (root.Position - dgn.Position).Magnitude
				if d < nd then nearest, nd = root, d end
			end
		end
		if nearest then
			local dir = nearest.Position - dgn.Position
			dgn.CFrame = CFrame.new(dgn.Position + dir.Unit * math.min(DRAGON_SPD * dt, dir.Magnitude))
		end
	end

	if roundT >= cfg.dur * TICK * PACING then -- startRound(round%4+1): resetWalls + fresh cheese
		round, roundT = round % 4 + 1, 0
		nextMove, wallMoves, wp = 21, 0, 2 -- beacon at BEACON_PATH[0], bound for path[1]
		for i, w in WALLS_BASE do WALLS[i][1], WALLS[i][2] = w[1], w[2]; placeWall(i); wallParts[i].Color = GOLD end
		c.CFrame = CFrame.new(toWorld(PATH[1][1], PATH[1][2]) + Vector3.new(0, 7, 0))
		for _, st in runState do st.arrived, st.dwell, st.scored = false, 0, 0 end
	end
end

Players.PlayerRemoving:Connect(function(p) runState[p] = nil end)
return MazeArenaZone
