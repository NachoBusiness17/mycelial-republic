--!strict
-- LightMazeZone — reborn as the Flicker Tower (Tower of Hell format, see
-- docs/CLONED_MECHANICS.md §3.2): NO checkpoints, shared 8:00 round timer,
-- 8 sections drawn seeded from a pool of 5, bullies (wisps) at 4:00.
-- Falls cost seconds (RespawnTime=1, set in PlayerFeel).

local Players = game:GetService("Players")
local ServerScriptService = game:GetService("ServerScriptService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Shared = ReplicatedStorage:WaitForChild("Modules")
local SeedRng = require(Shared:WaitForChild("SeedRng"))
local Trove = require(Shared:WaitForChild("Trove"))
local ShadowLedger = require(ServerScriptService:WaitForChild("ShadowLedger"))

local LightMazeZone = {}
local origin = Vector3.new(0, 40, 200)
local SECTIONS, ROUND_SECONDS, BULLY_AT = 8, 480, 240

local bridges: { { part: Part, period: number, phase: number } } = {}
local roundStart = os.clock()
local bulliesSpawned = false
local wisps: { BasePart } = {}

-- ---- the seeded section pool (the tower differs per round, replays are fair) ----
local function secLedges(base: Vector3, rng, model: Model): Vector3
	local top = base
	for i = 1, 4 do
		local p = Instance.new("Part")
		p.Anchored = true
		p.Size = Vector3.new(14, 1, 14)
		p.Position = base + Vector3.new(rng:int(-8, 8), i * 6, rng:int(-8, 8))
		p.Color = Color3.fromRGB(150, 180, 255)
		p.Material = Enum.Material.Neon
		p.Parent = model
		top = p.Position
	end
	return top + Vector3.new(0, 3, 0)
end

local function secFlickerBridges(base: Vector3, rng, model: Model): Vector3
	for i = 1, 4 do
		local b = Instance.new("Part")
		b.Anchored = true
		b.Size = Vector3.new(8, 0.5, 12)
		b.Position = base + Vector3.new(math.sin(i * 1.1) * 10, i * 6, -i * 10)
		b.Color = Color3.fromRGB(150, 180, 255)
		b.Material = Enum.Material.Neon
		b.Parent = model
		table.insert(bridges, { part = b, period = 2 + (i % 3), phase = rng:next() })
	end
	return base + Vector3.new(math.sin(4 * 1.1) * 10, 24, -40)
end

local function secSpinners(base: Vector3, rng, model: Model): Vector3
	for i = 1, 3 do
		local arm = Instance.new("Part")
		arm.Anchored = true
		arm.Size = Vector3.new(22, 1, 2)
		arm.Position = base + Vector3.new(0, i * 8, 0)
		arm.Color = Color3.fromRGB(220, 80, 90)
		arm.Material = Enum.Material.SmoothPlastic
		arm.Name = "KillArm"
		arm:SetAttribute("SpinSpeed", 40 + rng:int(0, 40))
		arm.Parent = model
		arm.Touched:Connect(function(hit)
			local plr = hit.Parent and Players:GetPlayerFromCharacter(hit.Parent)
			local hum = plr and plr.Character and plr.Character:FindFirstChildOfClass("Humanoid")
			if hum then hum.Health = 0 end -- kill bricks are honest
		end)
	end
	return base + Vector3.new(0, 27, 0)
end

local function secWallHops(base: Vector3, rng, model: Model): Vector3
	local top = base
	for i = 1, 5 do
		local w = Instance.new("Part")
		w.Anchored = true
		w.Size = Vector3.new(2, 5, 12)
		w.Position = base + Vector3.new(rng:int(-6, 6), i * 5, -i * 4)
		w.Color = Color3.fromRGB(90, 90, 110)
		w.Parent = model
		top = w.Position
	end
	return top + Vector3.new(0, 4, 0)
end

local function secThinLedges(base: Vector3, rng, model: Model): Vector3
	local top = base
	for i = 1, 6 do
		local p = Instance.new("Part")
		p.Anchored = true
		p.Size = Vector3.new(2.5, 0.7, 2.5)
		p.Position = base + Vector3.new(rng:int(-10, 10), i * 4.5, rng:int(-10, 10))
		p.Color = Color3.fromRGB(200, 220, 160)
		p.Parent = model
		top = p.Position
	end
	return top + Vector3.new(0, 3, 0)
end

local SECTION_POOL = { secLedges, secFlickerBridges, secSpinners, secWallHops, secThinLedges }

-- ---- bullies: a wisp per player after 4:00 (ToH mutators, our skin) ----
local function spawnBully(target: Player)
	local root = target.Character and target.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
	if not root then return end
	local w = Instance.new("Part")
	w.Shape = Enum.PartType.Ball
	w.Size = Vector3.new(2, 2, 2)
	w.Material = Enum.Material.Neon
	w.Color = Color3.fromRGB(140, 60, 200)
	w.Position = root.Position + Vector3.new(0, 14, 0)
	w.CanCollide = false
	w.Parent = workspace
	table.insert(wisps, w)
	-- Q-043 Trove pass: the chase is OWNED by the wisp (AttachToInstance ->
	-- Destroying -> Clean cancels the thread), not by its 60s age. The 60s
	-- cap stays as game behavior but now enforces itself by destroying the
	-- wisp (the false return then ends the thread); an early destroy cancels
	-- the chase immediately instead of leaving it polling w.Parent for up to
	-- a minute.
	local t0 = os.clock()
	local trove = Trove.new()
	trove:AttachToInstance(w)
	trove:Loop(0.1, function()
		if not w.Parent then return false end
		if os.clock() - t0 >= 60 then
			w:Destroy()
			return false
		end
		local hum = target.Character and target.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
		if hum then
			local dir = hum.Position - w.Position
			if dir.Magnitude > 2 then w.AssemblyLinearVelocity = dir.Unit * 11 end
		end
		return true
	end)
end

function LightMazeZone.build(): Model
	local model = Instance.new("Model")
	model.Name = "FlickerTower"

	-- the round seed is on the record: same seed, same tower, replayable
	local seed = tonumber(os.date("!%Y%m%d%H")) or 0
	local rng = SeedRng.new(seed)
	local cursor = origin

	for i = 1, SECTIONS do
		local builder = SECTION_POOL[rng:int(1, #SECTION_POOL)]
		cursor = builder(cursor, rng, model)
	end

	-- the summit: finishing banks into the ledger
	local summit = Instance.new("Part")
	summit.Anchored = true
	summit.Size = Vector3.new(16, 1, 16)
	summit.Position = cursor
	summit.Color = Color3.fromRGB(235, 230, 210)
	summit.Material = Enum.Material.Neon
	summit.Name = "TowerSummit"
	summit.Parent = model
	summit.Touched:Connect(function(hit)
		local plr = hit.Parent and Players:GetPlayerFromCharacter(hit.Parent)
		if plr and not plr:GetAttribute(("Summit_%d"):format(roundStart)) then
			plr:SetAttribute(("Summit_%d"):format(roundStart), true)
			local remaining = math.max(0, math.floor(ROUND_SECONDS - (os.clock() - roundStart)))
			plr:SetAttribute("VirtueMarks", tonumber((plr:GetAttribute("VirtueMarks")) or 0) + 50)
			ShadowLedger.record(plr, "LightMaze", ("topped the Flicker Tower with %ds left"):format(remaining), true)
		end
	end)

	model.Parent = workspace
	return model
end

function LightMazeZone.tick(dt: number)
	local t = os.clock()

	-- flicker bridges: solid on the lit half of the cycle
	for _, b in ipairs(bridges) do
		local lit = ((t / b.period + b.phase) % 1) < 0.6
		b.part.Transparency = lit and 0.2 or 0.95
		b.part.CanCollide = lit
	end

	-- spinners turn
	for _, arm in ipairs(workspace:GetChildren()) do
		if arm.Name == "KillArm" then
			local speed = tonumber(arm:GetAttribute("SpinSpeed")) or 40
			arm.CFrame = arm.CFrame * CFrame.Angles(0, math.rad(speed) * dt, 0)
		end
	end

	-- the shared round: reset the tower on schedule, bullies at half time
	local elapsed = t - roundStart
	if not bulliesSpawned and elapsed >= BULLY_AT then
		bulliesSpawned = true
		for _, p in ipairs(Players:GetPlayers()) do
			spawnBully(p)
		end
	end
	if elapsed >= ROUND_SECONDS then
		roundStart = t
		bulliesSpawned = false
		table.clear(wisps)
		-- sections rebuild with the new hour's seed
		local old = workspace:FindFirstChild("FlickerTower")
		if old then old:Destroy() end
		table.clear(bridges)
		LightMazeZone.build()
	end
end

return LightMazeZone
