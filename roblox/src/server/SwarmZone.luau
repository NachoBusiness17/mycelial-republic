--!strict
-- SwarmZone — the bullet-hell port. Translated from dashboard/static/games/swarm.html:
-- horde density as the power fantasy, depth gates, upgrade pool with cursed picks,
-- and the 122bpm disco pulse driving the lights (SPB = 60/122/2, one 8th note).
-- Double Score pass (99R) doubles gem value; Extra Life dev product revives.
-- Q-032 flock pass: the crop is ALIVE — gems are spore fish riding shared/Flock
-- (flee/tire/rest + boids school + kill-drop toss + the stir warn), and the horde
-- steers by the pheromone trail the players lay down (fresher beats closer).

local Players = game:GetService("Players")
local Shared = game:GetService("ReplicatedStorage"):WaitForChild("Modules")
local Config = require(Shared:WaitForChild("Config"))
local Trove = require(Shared:WaitForChild("Trove"))
local Flock = require(Shared:WaitForChild("Flock"))
local Monetization = require(script.Parent:WaitForChild("Monetization"))
local ShadowLedger = require(script.Parent:WaitForChild("ShadowLedger"))

local SwarmZone = {}
local origin = Vector3.new(-120, 8, 120) -- k-space: knowledge -3, practice +4
local ARENA = 90
local pulseT = 0
local light: Part? = nil
-- the flock field: floor top (part centered at origin.Y-1, size Y 1) + the fish's
-- 0.8 half-height = the rest height; walls one stud inside the arena rim
local FLOOR_Y = origin.Y - 0.5 + 0.8
local bounds: Flock.Bounds = {
	minX = origin.X - ARENA / 2 + 1,
	maxX = origin.X + ARENA / 2 - 1,
	minZ = origin.Z - ARENA / 2 + 1,
	maxZ = origin.Z + ARENA / 2 - 1,
	floorY = FLOOR_Y,
}

export type DepthMods = { gemMul: number, enemySpd: number, enemyHp: number, take: number, spawnMul: number, rate: number }

local upgrades: { { n: string, d: string, cursed: boolean?, f: (DepthMods) -> () } } = {
	{ n = "THE CROWD", d = "more bodies, softer bodies", f = function(m: DepthMods) m.spawnMul *= 1.4; m.enemyHp *= 0.75 end },
	{ n = "GLASS JAW", d = "they die fast, you die faster", f = function(m: DepthMods) m.enemyHp *= 0.5; m.take *= 1.3 end },
	{ n = "LONG TEETH", d = "your shots punch through", f = function(m: DepthMods) m.gemMul *= 1.2 end },
	{ n = "THE MOUNTAIN", d = "CURSED: enemies 30% harder, +40% fire rate", cursed = true,
		f = function(m: DepthMods) m.spawnMul *= 1.3; m.rate *= 1.4 end },
}

local active: { [Player]: { depthMods: DepthMods, diffLevel: number, spawnT: number, kills: number, alive: boolean, streak: number } } = {}
local pellets: { BasePart } = {}
-- the crop is alive: every gem is a spore fish (visual part + Flock state);
-- trail is the pheromone field the horde steers by
local school: { { part: BasePart, f: Flock.Fish } } = {}
local trail = Flock.trailNew()
local lastPellet: { [Player]: number } = {}
local lastTrail: { [Player]: number } = {}
local fishWarned = false -- "the fish stir..." warn, once per session (swarm.html:1074)
local announcer: BillboardGui? = nil

local STREAK_LINES = {
	[5] = "the grid remembers every hit.",
	[10] = "mark, the horde scales — tell them.",
	[25] = "the maze named its depths. i named nothing.",
}

local function announce(text: string)
	if not announcer then return end
	local lbl = announcer:FindFirstChildOfClass("TextLabel")
	if lbl then
		lbl.Text = text
		task.delay(3, function()
			if lbl.Parent then lbl.Text = "SWARM · 122 BPM" end
		end)
	end
end

function SwarmZone.build(): Part
	local floor = Instance.new("Part")
	floor.Anchored = true
	floor.Size = Vector3.new(ARENA, 1, ARENA)
	floor.Position = Vector3.new(origin.X, origin.Y - 1, origin.Z)
	floor.Color = Color3.fromRGB(18, 10, 24)
	floor.Material = Enum.Material.SmoothPlastic
	floor.Name = "SwarmArena"

	local arenaLight = Instance.new("Part")
	arenaLight.Anchored = true
	arenaLight.Size = Vector3.new(ARENA, 0.4, ARENA)
	arenaLight.Position = Vector3.new(origin.X, origin.Y + 30, origin.Z)
	arenaLight.Color = Color3.fromRGB(120, 40, 160)
	arenaLight.Material = Enum.Material.Neon
	arenaLight.Transparency = 0.6
	arenaLight.Parent = floor.Parent or workspace
	light = arenaLight

	floor.Touched:Connect(function(hit)
		local player = hit.Parent and Players:GetPlayerFromCharacter(hit.Parent)
		if player and not active[player] then
			SwarmZone.enter(player)
		end
	end)

	Players.PlayerRemoving:Connect(function(p)
		active[p] = nil
		lastPellet[p] = nil
		lastTrail[p] = nil
	end)
	return floor
end

function SwarmZone.enter(player: Player)
	active[player] = {
		depthMods = { gemMul = 1, enemySpd = 1, enemyHp = 1, take = 1, spawnMul = 1, rate = 1 },
		diffLevel = 0, spawnT = 0.4, kills = 0, streak = 0, alive = true,
	}
	player:SetAttribute("DoubleScore", Monetization.owns(player, "DoubleScore"))
	ShadowLedger.record(player, "Swarm", "entered the disco horde", true)
end

-- a spore fish: the visual part rides the pure Flock state (the crop is ALIVE,
-- swarm.html:949); `toss` nil spawns it resting on the school floor
local function dropFish(pos: Vector3, toss: Vector3?)
	if #school >= Flock.POP_CAP then
		return
	end
	local g = Instance.new("Part")
	g.Shape = Enum.PartType.Ball
	g.Size = Vector3.new(1.6, 1.6, 1.6)
	g.Color = Color3.fromRGB(120, 220, 160)
	g.Material = Enum.Material.Neon
	g.Name = "Gem"
	g.Anchored = true -- the flock owns the position, tick by tick
	g.CanCollide = false
	local f = Flock.newFish(pos, toss)
	g.Position = f.pos
	g.Parent = workspace
	-- the upcast matters: table.insert's read-write position wants the property
	-- EXACTLY BasePart (Part's subtype is rejected there)
	table.insert(school, { part = g :: BasePart, f = f })
	task.delay(30, function()
		g:Destroy()
	end)
end

local function killEnemy(enemy: BasePart, by: Player?, state)
	-- the crop is alive: every kill drops a fish with the toss law (swarm.html:631)
	dropFish(enemy.Position, Flock.toss())
	enemy:Destroy()
	if by and state then
		state.kills += 1
		state.streak += 1
		local line = STREAK_LINES[state.streak]
		if line then announce(line) end -- the Arsenal law: streaks self-hype
	end
end

local function firePellet(player: Player, state)
	local char = player.Character
	local root = char and char:FindFirstChild("HumanoidRootPart") :: BasePart?
	if not root then return end
	local pellet = Instance.new("Part")
	pellet.Shape = Enum.PartType.Ball
	pellet.Size = Vector3.new(1, 1, 1)
	pellet.Color = Color3.fromRGB(255, 210, 90)
	pellet.Material = Enum.Material.Neon
	pellet.CanCollide = false
	pellet.CFrame = root.CFrame
	pellet.Name = "Pellet"
	pellet.Parent = workspace
	pellet.AssemblyLinearVelocity = root.CFrame.LookVector * 120
	table.insert(pellets, pellet)
	task.delay(1.5, function()
		pellet:Destroy()
	end)
end

local function spawnEnemy(target: Player, state)
	local enemy = Instance.new("Part")
	enemy.Shape = Enum.PartType.Ball
	enemy.Size = Vector3.new(2, 2, 2)
	enemy.Color = Color3.fromRGB(220, 60, 90)
	enemy.Material = Enum.Material.Neon
	enemy.Name = "HordeUnit"
	enemy:SetAttribute("Hp", state.depthMods.enemyHp)
	enemy:SetAttribute("Owner", target.Name)
	local root = target.Character and target.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
	if not root then return end
	enemy.Position = root.Position + Vector3.new(math.random(-60, 60), 2, math.random(-60, 60))
	enemy.CanCollide = false
	enemy.Parent = workspace
	local conn
	conn = enemy.Touched:Connect(function(hit)
		local plr = hit.Parent and Players:GetPlayerFromCharacter(hit.Parent)
		if plr and active[plr] then
			active[plr].alive = false
			if plr.Character then plr.Character:BreakJoints() end
			conn:Disconnect()
			enemy:Destroy()
		end
	end)
	-- Q-043 Trove pass: the chase is OWNED by the enemy (AttachToInstance ->
	-- Destroying -> Clean cancels the thread), not by its 25s age. The 25s
	-- cap stays as game behavior but enforces itself by destroying the enemy
	-- (the false return ends the thread); the Touched kill above now cancels
	-- the chase immediately instead of leaving it polling enemy.Parent for
	-- up to 25s.
	local t0 = os.clock()
	local trove = Trove.new()
	trove:AttachToInstance(enemy)
	trove:Loop(0.08, function()
		if not enemy.Parent then return false end
		if os.clock() - t0 >= 25 then
			enemy:Destroy()
			return false
		end
		local hum = target.Character and target.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
		if hum then
			-- pheromone steering (swarm.html:842-851): the trail you left pulls
			-- them when it's fresher than you are, else they walk straight at you
			local dir = Flock.trailSteer(trail, enemy.Position, hum.Position)
			if dir.Magnitude > 1e-4 then
				enemy.AssemblyLinearVelocity = dir * (8 * state.depthMods.enemySpd)
			end
		end
		return true
	end)
end

function SwarmZone.tick(dt: number)
	-- the disco pulse: arena light breathes at 122bpm (beatPulse from the original)
	pulseT += dt
	if light then
		local beatPulse = 0.5 + 0.5 * math.sin(pulseT * (Config.Swarm.BPM / 60) * math.pi * 2)
		light.Transparency = 0.6 - 0.25 * beatPulse
	end

	-- pellets vs the horde: the Fire ability (Z) made good
	for i = #pellets, 1, -1 do
		local pellet = pellets[i]
		if not pellet.Parent then
			table.remove(pellets, i)
		else
			for _, unit in ipairs(workspace:GetChildren()) do
				if unit.Name == "HordeUnit" and unit:IsA("BasePart")
					and (unit.Position - pellet.Position).Magnitude < 3.5 then
					local ownerName = unit:GetAttribute("Owner")
					local owner = ownerName and Players:FindFirstChild(ownerName)
					killEnemy(unit, owner, owner and active[owner :: Player])
					pellet:Destroy()
					break
				end
			end
		end
	end

	-- ambient seed fish (the source's crop arrives by kills only; the port's
	-- ambient spawner keeps the zone alive solo): they spawn RESTING, so the
	-- school is visible immediately — the boids core does the rest
	if math.random() < dt * 1.2 and #school < 12 then
		dropFish(Vector3.new(
			origin.X + math.random(-ARENA / 2, ARENA / 2),
			FLOOR_Y,
			origin.Z + math.random(-ARENA / 2, ARENA / 2)
		), nil)
	end

	for player, state in pairs(active) do
		if state.alive and player.Character then
			-- the school: player touch or pet-orb proximity (the orb grinds for
			-- you). The tired ones are the catchable ones — a fleeing fish
			-- outruns the ring until it rests, exactly like the source
			local root = player.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
			if root then
				local collectRadius = player:GetAttribute("PetOrb") and 12 or 3.5
				for gi = #school, 1, -1 do
					local entry = school[gi]
					local g = entry.part
					if g.Parent and (entry.f.pos - root.Position).Magnitude < collectRadius then
						g:Destroy()
						table.remove(school, gi)
						local mult = state.depthMods.gemMul * ((player:GetAttribute("DoubleScore") and 2 or 1))
						player:SetAttribute("SwarmScore", tonumber((player:GetAttribute("SwarmScore")) or 0) + math.floor(25 * mult))
					end
				end
				-- pheromone trail: walking leaves a whisper, firing leaves a shout
				-- (swarm.html:1113-1121; the Fire pellet is the port's loud action,
				-- life 5 vs 2.5 verbatim)
				local now = os.clock()
				if now - (lastTrail[player] or 0) >= Flock.TRAIL_DROP_INTERVAL then
					lastTrail[player] = now
					Flock.trailDrop(trail, root.Position, Flock.loudTrailLife(now - (lastPellet[player] or 0) < 0.45))
				end
			end
			-- Fire ability (Z): rate-limited per player — the attribute window is
			-- 0.15s but this clock keeps it to one pellet per pull (long teeth: faster)
			if player:GetAttribute("Abil_Fire") then
				local now = os.clock()
				local gate = state.depthMods.rate > 1 and 0.18 or 0.25
				if now - (lastPellet[player] or 0) >= gate then
					lastPellet[player] = now
					firePellet(player, state)
				end
			end

			state.diffLevel += dt / 6
			-- the horde must FILL the screen (verbatim spawn curve)
			state.spawnT -= dt
			if state.spawnT <= 0 then
				local spawnMul = state.depthMods.spawnMul
				state.spawnT = math.max(Config.Swarm.spawnFloor, Config.Swarm.baseSpawn - state.diffLevel * Config.Swarm.spawnRamp) / spawnMul
				for _ = 1, Config.Swarm.hordeCount(state.diffLevel, spawnMul) do
					spawnEnemy(player, state)
				end
			end
			-- score: gems value via gemMul; Double Score pass doubles
			local mult = state.depthMods.gemMul * ((player:GetAttribute("DoubleScore") and 2 or 1))
			player:SetAttribute("SwarmScore", tonumber(math.floor((player:GetAttribute("SwarmScore")) or 0) + dt * 10 * mult))
		end
	end

	-- THE FLOCK (Q-032): airborne fish flee the nearest diver and tire; rested
	-- fish school (cohesion + separation + wiggle); the visual parts ride the
	-- pure state. trail:step ages the pheromone field for the horde's steering.
	local roots: { BasePart } = {}
	for player, state in pairs(active) do
		if state.alive and player.Character then
			local root = player.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
			if root then
				table.insert(roots, root)
			end
		end
	end
	local fishStates: { Flock.Fish } = {}
	for _, entry in school do
		table.insert(fishStates, entry.f)
	end
	for i = #school, 1, -1 do
		local entry = school[i]
		if not entry.part.Parent then
			table.remove(school, i)
			continue
		end
		local f = entry.f
		if not f.rest then
			-- flee the nearest diver (the source's single-player law, generalized
			-- to the nearest of whoever is in the arena)
			local nearest: BasePart? = nil
			local nd = math.huge
			for _, root in roots do
				local d = (root.Position - f.pos).Magnitude
				if d < nd then
					nd = d
					nearest = root
				end
			end
			if nearest then
				Flock.fleeStep(f, nearest.Position, dt, false, bounds)
				if Flock.caught(f, nearest.Position) then
					-- cornered mid-flight: the catch law (swarm.html:968 d0<15)
					entry.part:Destroy()
					table.remove(school, i)
					local owner = nearest.Parent and Players:GetPlayerFromCharacter(nearest.Parent)
					local st = owner and active[owner :: Player]
					if owner and st then
						local om = st.depthMods.gemMul * ((owner:GetAttribute("DoubleScore") and 2 or 1))
						owner:SetAttribute("SwarmScore", tonumber((owner:GetAttribute("SwarmScore")) or 0) + math.floor(25 * om))
					end
					continue
				end
			end
		else
			Flock.schoolStep(f, fishStates, pulseT, dt, FLOOR_Y)
		end
		entry.part.Position = f.pos
	end
	Flock.trailStep(trail, dt)
	-- "the fish stir..." (swarm.html:1074-1077): the crop warns before it matters
	if not fishWarned and #school >= Flock.STIR_AT then
		fishWarned = true
		announce("the fish stir...")
	end
end

return SwarmZone
