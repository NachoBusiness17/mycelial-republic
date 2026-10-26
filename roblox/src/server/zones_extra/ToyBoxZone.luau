--!strict
-- ToyBoxZone — THE TOY: one arena, one walker, one verb: read -> roll -> punish.
-- Quote-translated from dashboard/static/games/toy.html (souls grammar, mud
-- stripped). Dodge law: rollT > 0 (30 sta, 0.28 roll, 0.5 cd, 0.35 iframes,
-- ROLL_SPEED 420). Swing: 15 sta, cd 0.35, range 38+r+r, arc PI/2, dmg
-- 14*(0.9+0.2*rng) — the ONLY rng draw, on landed hits; punish the recovery
-- (riposte window 1.0s) and it bites double. Walker: hp 40, dmg 14, speed 95,
-- chase x1.35 past 60, plants (x0.12) while winding up 0.35s on a 1.2s cd,
-- then lunges 0.45 of the gap; roll THROUGH the bite -> it stumbles 0.8s and
-- you get the riposte. Stamina: 25/s regen, x0.5 moving / x1.5 still, gated
-- while attacking/rolling. Fleet seed law W1A: no seed -> seed = FNV-1a32 of
-- "fleet-YYYY-MM-DD" (UTC) — same day, same toy, everywhere; SeedRng stream.
-- Input law: Abil_Fire = the swing, Abil_Redirect = the roll (client courier).
-- GAPS: the sha256 play-receipt, applied-inputs tape, fixed-step 1/60 pump and
-- the source's x/y axis asymmetry (x uses chase, y plain speed — ported as the
-- intended chase on both axes) do not carry into 3D.

local Players = game:GetService("Players")
local Shared = game:GetService("ReplicatedStorage"):WaitForChild("Modules")
local SeedRng = require(Shared:WaitForChild("SeedRng"))
local ShadowLedger = require((script.Parent:FindFirstChild("ShadowLedger") or script.Parent.Parent:WaitForChild("ShadowLedger")) :: ModuleScript)

local ToyBoxZone = {}
local origin = Vector3.new(200, 8, -200)

-- source constants (toy.html, verbatim)
local SPEED, ROLL_SPEED = 160, 420
local ROLL_COST, ROLL_T, ROLL_CD, ROLL_IFRAMES = 30, 0.28, 0.5, 0.35
local SWING_COST, SWING_CD = 15, 0.35
local SWING_RANGE, SWING_ARC = 38 + 12 + 14, math.pi / 2 -- 38 + player.r + walker.r
local SWING_BASE_DMG = 14
local W_HP, W_DMG, W_SPEED, W_R = 40, 14, 95, 14
local W_WINDUP, W_CD, W_STUN, W_RIPOSTE = 0.35, 1.2, 0.8, 1.0
local ST_REGEN = 25

local function fleetSeed(): number -- FNV-1a 32 of "fleet-" .. UTC day, || 1
	local h = 2166136261
	for byte in ("fleet-" .. os.date("!%Y-%m-%d")):gmatch(".") do
		h = bit32.bxor(h, string.byte(byte))
		h = (h * 16777619) % 4294967296
	end
	return (h % 2147483646) + 1
end

local rng = SeedRng.new(fleetSeed())

type Duel = { walker: BasePart, hp: number, windup: number, attackCd: number, telegraph: number,
	stun: number, rollT: number, rollCd: number, iframes: number, riposte: number, swingCd: number }

local duels: { [Player]: Duel } = {}

local function spawnWalker(player: Player): BasePart
	local root = player.Character and player.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
	local w = Instance.new("Part")
	w.Shape = Enum.PartType.Ball
	w.Size = Vector3.new(W_R * 2, W_R * 2, W_R * 2) -- r 14
	w.Color = Color3.fromRGB(164, 68, 60) -- #a4443c
	w.Material = Enum.Material.Slate
	w.Anchored = true
	w.CanCollide = false
	w.Name = "THE WALKER"
	w.Position = (root and root.Position + Vector3.new(24, 2, 0) or origin) + Vector3.new(0, 6, 0)
	w.Parent = workspace
	return w
end

local function startDuel(player: Player)
	if duels[player] then return end
	local hum = player.Character and player.Character:FindFirstChild("Humanoid") :: Humanoid?
	if not (hum and hum.Health > 0) then return end
	hum.MaxHealth, hum.Health = 100, 100
	hum.WalkSpeed = SPEED -- walk 160
	duels[player] = { walker = spawnWalker(player), hp = W_HP, windup = 0, attackCd = 0,
		telegraph = 0, stun = 0, rollT = 0, rollCd = 0, iframes = 0, riposte = 0, swingCd = 0 }
	ShadowLedger.record(player, "ToyBox", "faced the walker", true)
end

function ToyBoxZone.build(): Model
	local model = Instance.new("Model")
	model.Name = "ToyBox"

	local floor = Instance.new("Part")
	floor.Anchored = true
	floor.Size = Vector3.new(120, 1, 120) -- the toy box: 480x300 px felt like this in studs
	floor.Position = origin - Vector3.new(0, 1, 0)
	floor.Color = Color3.fromRGB(20, 18, 16) -- #141210
	floor.Material = Enum.Material.WoodPlanks
	floor.Parent = model

	local mat = Instance.new("Part") -- step on the mat to start the run
	mat.Anchored = true
	mat.Size = Vector3.new(12, 1, 12)
	mat.Position = origin + Vector3.new(0, 0.5, 40)
	mat.Color = Color3.fromRGB(143, 217, 143) -- #8fd98f, the roller green
	mat.Material = Enum.Material.Neon
	mat.Parent = model

	model.Parent = workspace

	mat.Touched:Connect(function(hit)
		local player = hit.Parent and Players:GetPlayerFromCharacter(hit.Parent)
		if player then startDuel(player) end
	end)

	Players.PlayerRemoving:Connect(function(p) duels[p] = nil end)
	return model
end

function ToyBoxZone.tick(dt: number)
	for player, s in pairs(duels) do
		local char = player.Character
		local root = char and char:FindFirstChild("HumanoidRootPart") :: BasePart?
		local hum = char and char:FindFirstChild("Humanoid") :: Humanoid?
		if not (root and hum) then continue end
		if hum.Health <= 0 then
			ShadowLedger.record(player, "ToyBox", "fell to the walker", false)
			s.walker:Destroy()
			duels[player] = nil
			continue
		end

		-- timers
		s.rollCd = math.max(0, s.rollCd - dt)
		s.iframes = math.max(0, s.iframes - dt)
		s.swingCd = math.max(0, s.swingCd - dt)
		s.riposte = math.max(0, s.riposte - dt)
		local moving = Vector3.new(root.AssemblyLinearVelocity.X, 0, root.AssemblyLinearVelocity.Z).Magnitude > 4

		-- stamina law: 25/s, x0.5 active / x1.5 still, gated on attack/roll
		if s.swingCd <= 0 and s.rollT <= 0 then
			player:SetAttribute("ToyStamina", math.min(100, tonumber((player:GetAttribute("ToyStamina")) or 100) + ST_REGEN * (moving and 0.5 or 1.5) * dt))
		end

		-- the roll (Abil_Redirect): 30 sta, 0.28s, 0.5 cd, 0.35 iframes, speed 420 — the verb
		if player:GetAttribute("Abil_Redirect") == true and s.rollT <= 0 and s.rollCd <= 0
			and (player:GetAttribute("ToyStamina") :: number) >= ROLL_COST then
			player:SetAttribute("ToyStamina", (player:GetAttribute("ToyStamina") :: number) - ROLL_COST)
			s.rollT, s.rollCd, s.iframes = ROLL_T, ROLL_CD, ROLL_IFRAMES
			local look = root.CFrame.LookVector
			root.AssemblyLinearVelocity = Vector3.new(look.X, 0, look.Z).Unit * ROLL_SPEED
		end
		if s.rollT > 0 then
			s.rollT -= dt -- roll overrides walk (mud law)
			root.AssemblyLinearVelocity = Vector3.new(root.CFrame.LookVector.X, 0, root.CFrame.LookVector.Z).Unit * ROLL_SPEED
		end

		-- the swing (Abil_Fire): 15 sta, cd 0.35, range 64, arc PI/2 — riposte bites double
		if player:GetAttribute("Abil_Fire") == true and s.swingCd <= 0 and s.rollT <= 0
			and (player:GetAttribute("ToyStamina") :: number) >= SWING_COST then
			player:SetAttribute("ToyStamina", (player:GetAttribute("ToyStamina") :: number) - SWING_COST)
			s.swingCd = SWING_CD
			local d = s.walker.Position - root.Position
			local flat = Vector3.new(d.X, 0, d.Z)
			local look = root.CFrame.LookVector
			local diff = math.abs(look:Angle(flat.Magnitude > 0.01 and flat.Unit or look, Vector3.yAxis))
			if s.hp > 0 and flat.Magnitude < SWING_RANGE and diff < SWING_ARC then
				local dmg = SWING_BASE_DMG * (0.9 + 0.2 * rng:next()) -- the ONLY rng draw, on landed hits
				if s.riposte > 0 then dmg *= 2 s.riposte = 0 end -- punished the recovery
				s.hp -= dmg
				ShadowLedger.record(player, "ToyBox", s.hp <= 0 and "punished the recovery and felled the walker" or "landed a swing", true)
			end
		end

		-- the walker: chase, plant, bite — the READ is the flare
		if s.stun > 0 then
			s.stun -= dt
		else
			local toP = root.Position - s.walker.Position
			local d = Vector3.new(toP.X, 0, toP.Z)
			local len = math.max(d.Magnitude, 0.01)
			local plant = s.windup > 0 and 0.12 or 1 -- the swing winds up, the walker plants
			local chase = W_SPEED * (len > 60 and 1.35 or 1) -- closes the kite gap
			s.walker.CFrame = s.walker.CFrame + d.Unit * chase * plant * dt
			s.attackCd = math.max(0, s.attackCd - dt)
			s.telegraph = math.max(0, s.telegraph - dt)
			s.walker.Color = s.telegraph > 0 and Color3.fromRGB(255, 91, 77) or Color3.fromRGB(164, 68, 60)
			if s.windup <= 0 and s.attackCd <= 0 and len < W_R + 12 + 4 then
				s.windup, s.attackCd, s.telegraph = W_WINDUP, W_CD, W_WINDUP -- wind-up telegraph: dodgeable
			end
			if s.windup > 0 then
				s.windup -= dt
				if s.windup <= 0 then
					-- the lunge: a committed bite that closes the kite gap — dodge or bleed
					s.walker.CFrame = s.walker.CFrame + d.Unit * len * 0.45
					local d2 = (root.Position - s.walker.Position).Magnitude
					if d2 < W_R + 12 + 10 then
						if s.rollT > 0 then -- rolled THROUGH the bite — it stumbles, riposte window
							s.stun, s.riposte = W_STUN, W_RIPOSTE
							ShadowLedger.record(player, "ToyBox", "rolled through the bite — the walker stumbled", true)
						else
							hum:TakeDamage(W_DMG) -- the bite always lands unless you are mid-roll (rollT law)
						end
					end
				end
			end
		end

		if s.hp <= 0 then -- THE WALKER FALLS — the run resets into a new duel
			s.walker:Destroy()
			duels[player] = nil
			task.delay(3, function()
				if player.Parent and duels[player] == nil then -- refresh to run it again
					local fresh = spawnWalker(player)
					duels[player] = { walker = fresh, hp = W_HP, windup = 0, attackCd = 0,
						telegraph = 0, stun = 0, rollT = 0, rollCd = 0, iframes = 0, riposte = 0, swingCd = 0 }
				end
			end)
		end
	end
end

return ToyBoxZone
