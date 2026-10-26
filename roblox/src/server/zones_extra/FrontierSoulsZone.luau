--!strict
-- FrontierSoulsZone — the rim of the desert, where DEATH waits. Quote-translated
-- from dashboard/static/games/frontier_souls.html (death, the boss — three phases,
-- and none of them kind): hunt-lunge (0.55s tell, 640 speed), scythe sweep (0.6
-- windup, 1.0 rad cone, chains from phase 2), dagger fans (5/7), shadow-steps in
-- phase 3, phase gates at 66%/33% hp, presence drain, soul timer (130s; death
-- eats 10s/8s per landed hit and heals 40/30). Player loadout = MARROW (mid
-- archetype): hp 120, shot 16*0.8 dmg, shotCd 0.62, speed 480, life 1.1; roll:
-- cd 0.62, rollT 0.26, iframes 0.34, roll speed 380; hurt() grants 0.55s iframes.
-- Input law: Abil_Fire = the gun, Abil_Redirect = the roll (client courier).
-- GAPS (kept to hold the line budget): withered adds in phase 2, the deputy
-- combine, whiskey slow-mo, canyon ring world, grudge naming, dynamite, snake
-- tell law, death's audio pulse. No score-bearing rng draws: the source's
-- playerShot() has none (crit lives in playerSwing, not ported).

local Players = game:GetService("Players")
local Shared = game:GetService("ReplicatedStorage"):WaitForChild("Modules")
local ShadowLedger = require((script.Parent:FindFirstChild("ShadowLedger") or script.Parent.Parent:WaitForChild("ShadowLedger")) :: ModuleScript)

local FrontierSoulsZone = {}
local origin = Vector3.new(-200, 8, -200)

-- source constants (frontier_souls.html, verbatim)
local TIMER_MAX = 130
local PRESENCE_R, PRESENCE_DRAIN = 260, 1.5            -- d < 260 drains soul at 1.5/s
local DEATH_HP, DEATH_SPD, DEATH_DMG = 900, 100, 40    -- death: hp 900, spd 100, dmg 40
local SWEEP_RANGE, SWEEP_CONE, SWEEP_WINDUP = 165, 1.0, 0.6
local LUNGE_TELL, LUNGE_SPEED, LUNGE_TIME = 0.55, 640, 0.34
local FAN_SPREAD, SHOT_LIFE = 0.16, 1.1
local SHOT_DMG, SHOT_SPEED, SHOT_CD = 16 * 0.8, 480, 0.62 -- marrow shotMul 0.8; shot v=480, life 1.1
local ROLL_CD, ROLL_T, ROLL_IFRAMES, ROLL_SPEED, HURT_IFRAMES = 0.62, 0.26, 0.34, 380, 0.55

-- annotation exactness (t42 triage, lanes/t42.check.txt row 6): Death.part stores Instance.new("Part") (line 93); BasePart in the alias failed the exact-table literal check at the arena.death assign. Runtime unchanged.
type Death = { part: Part, hp: number, phase: number, cd: number, lungeCd: number, tpT: number,
	state: string, st: number, lt: number, sweep: number, sweepA: number, chained: boolean, lx: number, lz: number }

local arena: { player: Player?, death: Death?, timer: number, started: boolean } = { player = nil, death = nil, timer = TIMER_MAX, started = false }
local fireCd: { [Player]: number } = {}
local rollCd: { [Player]: number } = {}
local iframes: { [Player]: number } = {}

local function distTo(root: BasePart, p: BasePart): (number, number, number)
	local d = root.Position - p.Position
	local flat = Vector3.new(d.X, 0, d.Z)
	return flat.Magnitude, d.X / math.max(flat.Magnitude, 0.01), d.Z / math.max(flat.Magnitude, 0.01)
end

local function spawnShot(from: Vector3, dir: Vector3, speed: number, dmg: number, name: string, color: Color3)
	local s = Instance.new("Part")
	s.Shape = Enum.PartType.Ball
	s.Size = Vector3.new(2, 2, 2)
	s.Position = from
	s.Color = color
	s.Material = Enum.Material.Neon
	s.CanCollide = false
	s.Name = name
	s.Parent = workspace
	s.AssemblyLinearVelocity = dir * speed
	task.delay(SHOT_LIFE, function() if s.Parent then s:Destroy() end end)
	return s
end

function FrontierSoulsZone.build(): Model
	local model = Instance.new("Model")
	model.Name = "FrontierSouls"

	local flats = Instance.new("Part")
	flats.Anchored = true
	flats.Size = Vector3.new(400, 1, 400)
	flats.Position = origin - Vector3.new(0, 1, 0)
	flats.Color = Color3.fromRGB(184, 156, 116) -- sand
	flats.Material = Enum.Material.Sand
	flats.Parent = model

	local rim = Instance.new("Part") -- the portal beacon: rim blood-red
	rim.Anchored = true
	rim.Shape = Enum.PartType.Cylinder
	rim.Size = Vector3.new(2, 10, 10)
	rim.CFrame = CFrame.new(origin + Vector3.new(0, 5, -60)) * CFrame.Angles(0, 0, math.rad(90))
	rim.Color = Color3.fromRGB(192, 80, 56) -- #c05038, the hurt red
	rim.Material = Enum.Material.Neon
	rim.Parent = model

	model.Parent = workspace

	rim.Touched:Connect(function(hit)
		local player = hit.Parent and Players:GetPlayerFromCharacter(hit.Parent)
		if not player or arena.started or not player.Character then return end
		arena.started, arena.player, arena.timer = true, player, TIMER_MAX
		local hum = player.Character:FindFirstChild("Humanoid") :: Humanoid
		hum.MaxHealth, hum.Health = 120, 120 -- marrow hp 120
		ShadowLedger.record(player, "FrontierSouls", "walked the rim and woke DEATH", true)

		local d = Instance.new("Part") -- he waits out ahead — never on top of you (420 out)
		d.Shape = Enum.PartType.Ball
		d.Size = Vector3.new(40, 40, 40) -- r 20
		d.Position = origin + Vector3.new(0, 21, 420)
		d.Color = Color3.fromRGB(90, 84, 100)
		d.Material = Enum.Material.Slate
		d.Name = "DEATH"
		d.Anchored = true
		d.Parent = model
		arena.death = { part = d, hp = DEATH_HP, phase = 1, cd = 4.5, lungeCd = 2.5,
			tpT = 7, state = "idle", st = 0, lt = 0, sweep = 0, sweepA = 0, chained = false, lx = 0, lz = 0 }
	end)
	return model
end

function FrontierSoulsZone.tick(dt: number)
	local player = arena.player
	local death = arena.death
	if not (player and death and death.part.Parent) then return end
	local char = player.Character
	local root = char and char:FindFirstChild("HumanoidRootPart") :: BasePart?
	local hum = char and char:FindFirstChild("Humanoid") :: Humanoid?
	if not (root and hum and hum.Health > 0) then return end

	-- the soul timer: presence withers it, every kill buys road (we credit phase gates instead of packs)
	arena.timer -= dt * ((distTo(root, death.part)) < PRESENCE_R and PRESENCE_DRAIN or 0.15)
	player:SetAttribute("SoulTimer", math.max(0, math.floor(arena.timer)))
	if arena.timer <= 0 then hum.Health = 0 end
	fireCd[player] = math.max(0, (fireCd[player] or 0) - dt)
	rollCd[player] = math.max(0, (rollCd[player] or 0) - dt)
	iframes[player] = math.max(0, (iframes[player] or 0) - dt)

	-- Abil_Redirect = the roll: 30→n/a here, cd 0.62, rollT 0.26, iframes 0.34, speed 380
	if player:GetAttribute("Abil_Redirect") == true and rollCd[player] == 0 then
		rollCd[player], iframes[player] = ROLL_CD, ROLL_IFRAMES
		local look = root.CFrame.LookVector
		root.AssemblyLinearVelocity = Vector3.new(look.X, 0, look.Z).Unit * ROLL_SPEED
		ShadowLedger.record(player, "FrontierSouls", "rolled", true)
	end

	-- Abil_Fire = the gun: shot 480, life 1.1, dmg 16*0.8, cd 0.62 (nx points death->player, so aim -n)
	if player:GetAttribute("Abil_Fire") == true and fireCd[player] == 0 then
		fireCd[player] = SHOT_CD
		local _, tx, tz = distTo(root, death.part)
		spawnShot(root.Position - Vector3.new(tx * 7, 0, tz * 7), Vector3.new(-tx, 0, -tz),
			SHOT_SPEED, SHOT_DMG, "PlayerShot", Color3.fromRGB(232, 180, 90)).Touched:Connect(function(hit)
			if hit == death.part and death.part.Parent then
				death.hp -= SHOT_DMG
			end
		end)
	end

	local d, nx, nz = distTo(root, death.part)
	-- phase gates: 66% -> THE HARVEST, 33% -> THE REAPING (he stops walking)
	if death.phase == 1 and death.hp / DEATH_HP <= 0.66 then death.phase, death.cd, death.lungeCd = 2, 1.6, 1.4
	elseif death.phase == 2 and death.hp / DEATH_HP <= 0.33 then death.phase, death.tpT = 3, 1.2 end
	local ph = death.phase -- read after the gates, like the source

	-- phase 3: death steps between the shadows (tpT 7, 0.5 fade, flank 220 ±0.8 rad)
	if ph == 3 then
		death.tpT -= dt
		if death.tpT <= 0 and death.state ~= "tpOut" then
			death.tpT, death.state, death.st = 7, "tpOut", 0.5
		elseif death.state == "tpOut" then
			death.st -= dt
			if death.st <= 0 then
				local flank = math.atan2(-nz, -nx) + (death.hp % 2 < 1 and 0.8 or -0.8)
				death.part.CFrame = CFrame.new(root.Position + Vector3.new(math.cos(flank), 0, math.sin(flank)) * 220 + Vector3.new(0, 21, 0))
				death.state, death.cd = "idle", math.min(death.cd, 0.5)
			end
			return -- mid-step: he is nowhere
		end
	end

	death.cd -= dt
	death.lungeCd -= dt
	if death.state == "lungeTel" then -- the tell: 0.55s, then 640 for 0.34s
		death.st -= dt
		if death.st <= 0 then death.state, death.lt, death.lx, death.lz = "lunging", LUNGE_TIME, nx, nz end
	elseif death.state == "lunging" then
		death.lt -= dt
		death.part.CFrame = death.part.CFrame + Vector3.new(death.lx, 0, death.lz) * LUNGE_SPEED * dt
		if d < 28 and iframes[player] == 0 then -- r 20 + r 12 + 8 -> ~28
			hum:TakeDamage(DEATH_DMG) iframes[player] = HURT_IFRAMES
			arena.timer = math.max(0, arena.timer - 10) -- the scythe drinks: 10s of soul
			death.hp = math.min(DEATH_HP, death.hp + 40) -- death feeds
			ShadowLedger.record(player, "FrontierSouls", "was reaped by the lunge — death fed", false)
		end
		if death.lt <= 0 then death.state = "idle" end
	elseif d > PRESENCE_R then -- far: dagger fans — tighter and faster the deeper his phase
		if death.cd <= 0 then
			death.cd = if ph == 3 then 1.5 else 1.9
			local n = if ph == 3 then 7 else 5
			for k = -math.floor(n / 2), math.floor(n / 2) do
				local a = math.atan2(nz, nx) + k * FAN_SPREAD
				local shot = spawnShot(death.part.Position, Vector3.new(math.cos(a), 0, math.sin(a)),
					ph == 3 and 320 or 280, 14, "Dagger", Color3.fromRGB(216, 210, 192))
				shot.Touched:Connect(function(hit)
					if hit.Parent == char and iframes[player] == 0 then
						hum:TakeDamage(14) iframes[player] = HURT_IFRAMES
					end
				end)
			end
		end
		if death.lungeCd <= 0 and d < 560 then
			death.lungeCd = ph == 3 and 2.4 or 3.4
			death.state, death.st = "lungeTel", LUNGE_TELL
		end
	else -- close: the scythe — 0.6 windup, 1.0 rad cone, 165 range
		death.part.CFrame = death.part.CFrame + Vector3.new(nx, 0, nz) * DEATH_SPD * dt
		if death.cd <= 0 then
			death.sweep, death.sweepA = SWEEP_WINDUP, math.atan2(nz, nx)
			death.cd = if ph == 3 then 1.3 elseif ph == 2 then 2.0 else 2.6
			death.chained = ph >= 2
		end
	end

	if death.sweep > 0 then
		death.sweep -= dt
		if death.sweep <= 0 then
			local pa = math.atan2(root.Position.Z - death.part.Position.Z, root.Position.X - death.part.Position.X)
			local diff = pa - death.sweepA
			while diff > math.pi do diff -= 2 * math.pi end
			while diff < -math.pi do diff += 2 * math.pi end
			if math.abs(diff) < SWEEP_CONE and d < SWEEP_RANGE and iframes[player] == 0 then
				hum:TakeDamage(DEATH_DMG) iframes[player] = HURT_IFRAMES
				arena.timer = math.max(0, arena.timer - 8)
				death.hp = math.min(DEATH_HP, death.hp + 30)
				ShadowLedger.record(player, "FrontierSouls", "took the scythe — death fed again", false)
			end
			if death.chained then -- phase 2+: it comes around again, from the other side
				death.chained = false
				death.sweep, death.sweepA = 0.45, death.sweepA + 2.1
			end
		end
	end

	if death.hp <= 0 then -- DEATH FALLS
		death.part:Destroy()
		arena.death, arena.started = nil, false
		arena.timer = TIMER_MAX
		ShadowLedger.record(player, "FrontierSouls", "felled DEATH at the rim", true)
	end
end

return FrontierSoulsZone
