--[[
    SwarmMain — PRIVLIDGE. The beat IS the ruleset.
    Server orchestrator: runway, beat-aligned hazards, per-player chains,
    progression shop, global leaderboard. Declaration order matters in Luau:
    state lives ABOVE the handlers that close over it.
]]

--!strict
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ServerStorage = game:GetService("ServerStorage")
local Workspace = game:GetService("Workspace")
local Debris = game:GetService("Debris")
local DataStoreService = game:GetService("DataStoreService")
local Lighting = game:GetService("Lighting")

local ServerModules = ServerStorage:WaitForChild("ServerModules")
local BeatClock = require(ServerModules:WaitForChild("BeatClock"))
local GrooveChain = require(ServerModules:WaitForChild("GrooveChain"))

-- ============================================================
-- CONSTANTS
-- ============================================================
local RUNWAY_LENGTH = 200
local RUNWAY_WIDTH = 40
local LANE_COUNT = 5
local LANE_WIDTH = RUNWAY_WIDTH / LANE_COUNT

local PLAYER_BAND_Z_MIN = -14
local PLAYER_BAND_Z_MAX = -4
local PLAYER_Y = 2
local PLAYER_STRAFE = 24
local JUMP_VELOCITY = 55
local GRAVITY = 140

local DRIFTER_SPEED = 16
local SWEEPER_SPEED = 45
local WALL_CLOSE_SPEED = 32
local MAX_SPEED_SCALE = 2.5
local RAMP_EVERY_STEPS = 64 -- every 8 bars

local SPAWN_PROTECT_SECONDS = 2
local RESTART_COOLDOWN = 3

-- ============================================================
-- REMOTES
-- ============================================================
local Remotes = Instance.new("Folder")
Remotes.Name = "Remotes"
Remotes.Parent = ReplicatedStorage

local function ensureRemote(name: string, class: string)
	local r = Instance.new(class)
	r.Name = name
	r.Parent = Remotes
	return r
end

local RemoteStateUpdate = ensureRemote("StateUpdate", "RemoteEvent")
local RemoteJuice = ensureRemote("Juice", "RemoteEvent")
local RemoteDeath = ensureRemote("Death", "RemoteEvent")
local RemoteScore = ensureRemote("ScoreUpdate", "RemoteEvent")
local RemoteInput = ensureRemote("Input", "RemoteEvent")
local RemoteRestart = ensureRemote("Restart", "RemoteEvent")
local RemoteShop = ensureRemote("Shop", "RemoteEvent")

-- ============================================================
-- PROFILE STORE
-- ============================================================
local scoreStore = DataStoreService:GetDataStore("PRIVLIDGE_Scores_v1")
local boardStore = DataStoreService:GetOrderedDataStore("PRIVLIDGE_Leaderboard_v1")

local SAVE_DEBOUNCE = 6 -- SetAsync quota is ~6s per key
local lastSaveAt: { [number]: number } = {}

local function defaultProfile()
	return { banked = 0, best = 0, upgrades = { speed = 0, jump = 0 } }
end

local function loadProfile(userId: number)
	local data
	local ok = false
	for _ = 1, 2 do
		local err
		ok, err = pcall(function()
			data = scoreStore:GetAsync(tostring(userId))
		end)
		if ok then break end
		warn("[PRIVLIDGE] profile load failed for " .. tostring(userId) .. ": " .. tostring(err) .. " — retrying")
		task.wait(1)
	end

	if ok and typeof(data) == "table" then
		data.upgrades = data.upgrades or { speed = 0, jump = 0 }
		data.banked = data.banked or 0
		data.best = data.best or 0
		return data
	end
	if ok then
		return defaultProfile() -- genuinely new player
	end

	-- Load failed twice: play this session read-only. NEVER overwrite
	-- possibly-real data with a default-derived profile.
	warn("[PRIVLIDGE] profile load FAILED for " .. tostring(userId) .. " — session is READ-ONLY")
	local profile = defaultProfile()
	profile.readOnly = true
	return profile
end

local function saveProfile(userId: number, profile, force: boolean?)
	if profile.readOnly then
		warn("[PRIVLIDGE] refusing to save " .. tostring(userId) .. " — load failed earlier; write would wipe data")
		return
	end
	local now = os.clock()
	if not force and now - (lastSaveAt[userId] or 0) < SAVE_DEBOUNCE then
		return -- in-game saves are best-effort; leave/shutdown force the final write
	end
	local ok, err = pcall(function()
		scoreStore:SetAsync(tostring(userId), profile)
	end)
	if ok then
		lastSaveAt[userId] = now
	else
		lastSaveAt[userId] = 0 -- allow an immediate retry on the next death
		warn("[PRIVLIDGE] profile save FAILED for " .. tostring(userId) .. ": " .. tostring(err))
	end
end

local function syncLeaderstats(player: Player, profile)
	local ls = player:FindFirstChild("leaderstats")
	if not ls then return end
	local bank = ls:FindFirstChild("Bank")
	local best = ls:FindFirstChild("Best")
	if bank then bank.Value = profile.banked end
	if best then best.Value = profile.best end
end

-- ============================================================
-- ARENA
-- ============================================================
Players.CharacterAutoLoads = false

Lighting.Ambient = Color3.fromRGB(8, 4, 20)
Lighting.OutdoorAmbient = Color3.fromRGB(4, 2, 12)
Lighting.Brightness = 0.4
Lighting.ClockTime = 0
Lighting.FogColor = Color3.fromRGB(10, 4, 24)
Lighting.FogStart = 60
Lighting.FogEnd = 260
Lighting.EnvironmentDiffuseScale = 0.2
Lighting.EnvironmentSpecularScale = 0.4

local Arena = Instance.new("Folder")
Arena.Name = "Arena"
Arena.Parent = Workspace

local function makePart(name: string, size: Vector3, cframe: CFrame, color: Color3, material: Enum.Material, parent: Instance): BasePart
	local p = Instance.new("Part")
	p.Name = name
	p.Size = size
	p.CFrame = cframe
	p.Color = color
	p.Material = material
	p.Anchored = true
	p.CanCollide = false
	p.CanQuery = false
	p.CanTouch = false
	p.Parent = parent
	return p
end

local floorPart = makePart(
	"Runway",
	Vector3.new(RUNWAY_WIDTH, 2, RUNWAY_LENGTH),
	CFrame.new(0, 1, -RUNWAY_LENGTH / 2),
	Color3.fromRGB(6, 4, 14),
	Enum.Material.SmoothPlastic,
	Arena
)
floorPart.CanCollide = true

local gridLineParts: { BasePart } = {}
local gridLineBaseColors: { [BasePart]: Color3 } = {}

local GridLines = Instance.new("Folder")
GridLines.Name = "GridLines"
GridLines.Parent = Arena

for i = 0, LANE_COUNT do
	local x = -RUNWAY_WIDTH / 2 + i * LANE_WIDTH
	local line = makePart(
		"GridLine_L_" .. i,
		Vector3.new(0.25, 0.05, RUNWAY_LENGTH),
		CFrame.new(x, 2.05, -RUNWAY_LENGTH / 2),
		Color3.fromRGB(0, 200, 255),
		Enum.Material.Neon,
		GridLines
	)
	table.insert(gridLineParts, line)
	gridLineBaseColors[line] = line.Color
end

for z = 0, RUNWAY_LENGTH, 10 do
	local line = makePart(
		"GridLine_X_" .. z,
		Vector3.new(RUNWAY_WIDTH, 0.05, 0.25),
		CFrame.new(0, 2.05, -z),
		Color3.fromRGB(255, 0, 180),
		Enum.Material.Neon,
		GridLines
	)
	table.insert(gridLineParts, line)
	gridLineBaseColors[line] = line.Color
end

local SafeLine = makePart(
	"SafeLine",
	Vector3.new(LANE_WIDTH - 0.5, 0.06, RUNWAY_LENGTH),
	CFrame.new(0, 2.08, -RUNWAY_LENGTH / 2),
	Color3.fromRGB(255, 240, 120),
	Enum.Material.Neon,
	Arena
)
SafeLine.Transparency = 0.55

-- ============================================================
-- HAZARDS / PICKUPS
-- ============================================================
local Hazards = Instance.new("Folder")
Hazards.Name = "Hazards"
Hazards.Parent = Arena

local Pickups = Instance.new("Folder")
Pickups.Name = "Pickups"
Pickups.Parent = Arena

local speedScale = 1.0

local function laneX(lane: number): number
	return -RUNWAY_WIDTH / 2 + (lane - 0.5) * LANE_WIDTH
end

local BAND_Z = (PLAYER_BAND_Z_MIN + PLAYER_BAND_Z_MAX) / 2
local SPAWN_Z = -RUNWAY_LENGTH - 10 -- off-screen behind the fog line

-- Pick a whole number of bars of travel and return the frozen speed that
-- lands the hazard on the player band exactly on a bar boundary. Speed is
-- frozen at spawn so a mid-flight ramp can't bend its arrival off-grid.
local function arrivalSpeed(distance: number, baseSpeed: number): number
	local rawSteps = distance / (baseSpeed * speedScale * BeatClock.GetSecondsPerStep())
	local steps = math.max(8, math.floor(rawSteps / 8 + 0.5) * 8)
	return distance / (steps * BeatClock.GetSecondsPerStep())
end

local function attachGlow(p: BasePart, color: Color3, range: number, brightness: number)
	local light = Instance.new("PointLight")
	light.Color = color
	light.Range = range
	light.Brightness = brightness
	light.Parent = p
end

local function spawnDrifter()
	local lane = math.random(1, LANE_COUNT)
	local p = Instance.new("Part")
	p.Name = "Drifter"
	p.Size = Vector3.new(3, 3, 3)
	p.Color = Color3.fromRGB(255, 40, 40)
	p.Material = Enum.Material.Neon
	p.Anchored = true
	p.CanCollide = false
	p.CanQuery = true
	p.CanTouch = false
	p:SetAttribute("Hazard", true)
	p.CFrame = CFrame.new(laneX(lane), 3.5, SPAWN_Z)
	p.Parent = Hazards
	attachGlow(p, p.Color, 12, 3)

	local speed = arrivalSpeed(math.abs(BAND_Z - SPAWN_Z), DRIFTER_SPEED)
	task.spawn(function()
		while p.Parent do
			p.CFrame = p.CFrame * CFrame.new(0, 0, speed * task.wait())
			if p.Position.Z > 20 then
				p:Destroy()
				return
			end
		end
	end)
end

local function spawnSweeper()
	-- Only the killable half of the band: |z - BAND_Z| < ~3.4
	local z = -math.random(6, 12)
	local fromLeft = math.random() > 0.5
	local startX = fromLeft and (-RUNWAY_WIDTH / 2 - 5) or (RUNWAY_WIDTH / 2 + 5)
	local dir = fromLeft and 1 or -1

	-- Telegraph: a blinking strip at the sweep line, 4 steps of warning.
	local marker = makePart(
		"SweepTelegraph",
		Vector3.new(RUNWAY_WIDTH, 0.15, 1.2),
		CFrame.new(0, 2.15, z),
		Color3.fromRGB(255, 200, 0),
		Enum.Material.Neon,
		Hazards
	)
	marker.Transparency = 0.4
	task.spawn(function()
		local on = false
		while marker.Parent do
			on = not on
			marker.Transparency = on and 0.1 or 0.7
			task.wait(BeatClock.GetSecondsPerStep())
		end
	end)

	task.delay(4 * BeatClock.GetSecondsPerStep(), function()
		if marker.Parent then marker:Destroy() end

		local p = Instance.new("Part")
		p.Name = "Sweeper"
		p.Size = Vector3.new(RUNWAY_WIDTH, 2, 2)
		p.Color = Color3.fromRGB(255, 200, 0)
		p.Material = Enum.Material.Neon
		p.Anchored = true
		p.CanCollide = false
		p.CanQuery = true
		p.CanTouch = false
		p:SetAttribute("Hazard", true)
		p.CFrame = CFrame.new(startX, 3, z)
		p.Parent = Hazards
		attachGlow(p, p.Color, 16, 4)

		local speed = SWEEPER_SPEED * speedScale
		task.spawn(function()
			while p.Parent do
				p.CFrame = p.CFrame * CFrame.new(dir * speed * task.wait(), 0, 0)
				if math.abs(p.Position.X) > RUNWAY_WIDTH / 2 + 12 then
					p:Destroy()
					return
				end
			end
		end)
	end)
end

local function spawnWall()
	local lane = math.random(1, LANE_COUNT)
	local p = Instance.new("Part")
	p.Name = "Wall"
	-- 14 studs tall: taller than max jump clearance so walls force a STRAFE
	-- while low hazards test the jump. Two verbs.
	p.Size = Vector3.new(LANE_WIDTH - 0.5, 14, 2)
	p.Color = Color3.fromRGB(180, 0, 255)
	p.Material = Enum.Material.Neon
	p.Anchored = true
	p.CanCollide = false
	p.CanQuery = true
	p.CanTouch = false
	p:SetAttribute("Hazard", true)
	p.CFrame = CFrame.new(laneX(lane), 9, SPAWN_Z)
	p.Parent = Hazards
	attachGlow(p, p.Color, 14, 3)

	local speed = arrivalSpeed(math.abs(BAND_Z - SPAWN_Z), WALL_CLOSE_SPEED)
	task.spawn(function()
		while p.Parent do
			p.CFrame = p.CFrame * CFrame.new(0, 0, speed * task.wait())
			if p.Position.Z > 20 then
				p:Destroy()
				return
			end
		end
	end)
end

-- Weaver: spawns at the runway end and sine-sweeps laterally as it
-- approaches — reads the lane grid as a wave, forces timing + lane reads.
local function spawnWeaver()
	local startX = laneX(math.random(2, LANE_COUNT - 1))
	local p = Instance.new("Part")
	p.Name = "Weaver"
	p.Size = Vector3.new(3, 3, 3)
	p.Color = Color3.fromRGB(0, 120, 255)
	p.Material = Enum.Material.Neon
	p.Anchored = true
	p.CanCollide = false
	p.CanQuery = true
	p.CanTouch = false
	p:SetAttribute("Hazard", true)
	p.CFrame = CFrame.new(startX, 3.5, SPAWN_Z)
	p.Parent = Hazards
	attachGlow(p, p.Color, 12, 3)

	local speed = arrivalSpeed(math.abs(BAND_Z - SPAWN_Z), DRIFTER_SPEED * 1.2)
	local phase = math.random() * math.pi * 2
	local amp = LANE_WIDTH * 1.5
	local t = 0
	task.spawn(function()
		while p.Parent do
			local dt = task.wait()
			t += dt
			p.CFrame = CFrame.new(
				math.clamp(startX + amp * math.sin(t * 4 + phase), -RUNWAY_WIDTH / 2 + 2, RUNWAY_WIDTH / 2 - 2),
				3.5,
				SPAWN_Z + speed * t
			)
			if p.Position.Z > 20 then
				p:Destroy()
				return
			end
		end
	end)
end

local function spawnPickup()
	local pos
	for _ = 1, 4 do
		local lane = math.random(1, LANE_COUNT)
		if lane ~= 3 then -- off the safe line: risk/reward
			local z = -math.random(6, 16)
			pos = Vector3.new(laneX(lane), PLAYER_Y + 1, z)
			local blocked = false
			for _, h in ipairs(Hazards:GetChildren()) do
				if h:IsA("BasePart") and h:GetAttribute("Hazard") and (h.Position - pos).Magnitude < 10 then
					blocked = true
					break
				end
			end
			if not blocked then
				for _, other in ipairs(Pickups:GetChildren()) do
					if other:IsA("BasePart") and (other.Position - pos).Magnitude < 8 then
						blocked = true
						break
					end
				end
			end
			if not blocked then break end
		end
		pos = nil
	end
	if not pos then return end

	local p = Instance.new("Part")
	p.Name = "Pickup"
	p.Shape = Enum.PartType.Ball
	p.Size = Vector3.new(2, 2, 2)
	p.Color = Color3.fromRGB(0, 255, 180)
	p.Material = Enum.Material.Neon
	p.Anchored = true
	p.CanCollide = false
	p.CanQuery = true
	p.CanTouch = false
	p.CFrame = CFrame.new(pos)
	p.Parent = Pickups
	attachGlow(p, p.Color, 12, 4)

	task.spawn(function()
		while p.Parent do
			p.CFrame = p.CFrame * CFrame.Angles(0, math.rad(120) * task.wait(), 0)
		end
	end)

	Debris:AddItem(p, 12)
end

-- ============================================================
-- PLAYER STATE (declared BEFORE the handlers that close over it)
-- ============================================================
type PlayerState = {
	player: Player,
	root: BasePart?,
	profile: any,
	runScore: number,
	alive: boolean,
	airborne: boolean,
	spin: number,
	velocityY: number,
	input: { [string]: boolean },
	grazed: { [BasePart]: boolean },
	spawnProtectUntil: number,
	lastRestart: number,
}

local playerStates: { [Player]: PlayerState } = {}

local function getState(player: Player): PlayerState?
	return playerStates[player]
end

local function fireScore(st: PlayerState)
	-- Score events are naturally sparse (landings/pickups/grazes); always
	-- deliver — dropping updates left the HUD stale between bursts.
	RemoteScore:FireClient(st.player, st.profile.banked, st.profile.best, st.runScore)
end

-- ============================================================
-- BEAT WIRING
-- ============================================================
local hazardBus = Instance.new("BindableEvent")
hazardBus.Name = "HazardBus"
hazardBus.Parent = ReplicatedStorage:WaitForChild("PRIVLIDGE_Remotes")

BeatClock.Patterns.Pulse = function(_step: number): boolean
	return true
end

hazardBus.Event:Connect(function(name: string, step: number)
	local anyAlive = false
	for _, st in pairs(playerStates) do
		if st.alive then
			anyAlive = true
			break
		end
	end

	-- Nothing spawns or ramps for an empty server
	if not anyAlive then return end

	if name == "Drifter" then
		spawnDrifter()
	elseif name == "Sweeper" then
		spawnSweeper()
	elseif name == "Wall" then
		spawnWall()
	elseif name == "Weaver" then
		spawnWeaver()
	elseif name == "Pulse" then
		-- Once per grid step: neglected chains die
		GrooveChain.Tick()

		if step % 8 == 0 then
			-- Downbeat: the runway grid pulses with the song's measured energy
			local e = 0.5
			if activeTrack and typeof(activeTrack.energy) == "table" and #activeTrack.energy > 0 then
				local i = (step % #activeTrack.energy) + 1
				e = math.clamp(activeTrack.energy[i] / 255, 0.15, 1)
			end
			for _, line in ipairs(gridLineParts) do
				local base = gridLineBaseColors[line]
				line.Color = Color3.new(
					math.min(1, base.R + 0.5 * e),
					math.min(1, base.G + 0.5 * e),
					math.min(1, base.B + 0.5 * e)
				)
				task.delay(BeatClock.GetSecondsPerStep() * 0.7, function()
					if line.Parent then
						line.Color = base
					end
				end)
			end
		end

		if step % 8 == 4 then
			spawnPickup()
		end
		if step % RAMP_EVERY_STEPS == 0 then
			speedScale = math.min(MAX_SPEED_SCALE, speedScale + 0.1)
			RemoteJuice:FireAllClients("rampup", { scale = speedScale })
		end
	end
end)

-- ============================================================
-- AUDIO CHANNEL (shadertoy-style: the song is an input)
-- tools/audio_channel.py measures every track dropped in game_roblox/audio/
-- and regenerates ReplicatedStorage.AudioManifest (assetId, bpm, per-step
-- energy curve). This server binds a random track from the manifest each
-- boot, retunes the grid to its BPM, and ships the pick to clients.
-- Manual override: set MUSIC_ASSET_ID to pin one track.
-- assetId 0 = track measured but not uploaded yet (needs roblox_opencloud
-- key in configs/keys.json; rerun audio_channel.sh and it uploads).
-- ============================================================
local MUSIC_ASSET_ID = 0 -- manual override; 0 = let the manifest choose
local activeTrack = nil
local activeTrackIndex = 0

do
	local ok, manifest = pcall(require, ReplicatedStorage:WaitForChild("AudioManifest"))
	if ok and typeof(manifest) == "table" and #manifest > 0 then
		local playable = {}
		for i, t in ipairs(manifest) do
			if typeof(t) == "table" and t.bpm and t.energy and t.assetId and t.assetId ~= 0 then
				table.insert(playable, { index = i, track = t })
			end
		end
		if #playable > 0 then
			local pick = playable[math.random(#playable)]
			activeTrack = pick.track
			activeTrackIndex = pick.index
		end
	end
end

if MUSIC_ASSET_ID == 0 and activeTrack and activeTrack.assetId and activeTrack.assetId ~= 0 then
	MUSIC_ASSET_ID = activeTrack.assetId
end

if MUSIC_ASSET_ID ~= 0 then
	local bpm = (activeTrack and activeTrack.bpm) or 122
	if math.abs(bpm - 122) > 0.05 then
		BeatClock.SetBPM(bpm)
	end
	local music = Instance.new("Sound")
	music.Name = "PRIVLIDGE_Music"
	music.SoundId = "rbxassetid://" .. tostring(MUSIC_ASSET_ID)
	music.Looped = true
	music.Volume = 0.8
	music.Parent = Workspace
	BeatClock.BindSound(music)
	music:Play()
	print(("[PRIVLIDGE] audio channel: '%s' at %.1f BPM"):format(
		tostring(activeTrack and activeTrack.name or "override"), bpm))
else
	print("[PRIVLIDGE] audio channel: silent mode (no uploaded track yet)")
end

BeatClock:Start()

-- ============================================================
-- SKATER
-- ============================================================
local function buildSkater(player: Player): Model
	local model = Instance.new("Model")
	model.Name = player.Name .. "_Skater"

	local root = Instance.new("Part")
	root.Name = "Root"
	root.Size = Vector3.new(3, 0.6, 5)
	root.Color = Color3.fromRGB(255, 60, 200)
	root.Material = Enum.Material.Neon
	root.Anchored = true
	root.CanCollide = false
	root.CFrame = CFrame.new(0, PLAYER_Y, BAND_Z)
	root.Parent = model

	local deck = Instance.new("Part")
	deck.Name = "Deck"
	deck.Size = Vector3.new(2.4, 0.3, 4.4)
	deck.Color = Color3.fromRGB(20, 20, 30)
	deck.Material = Enum.Material.SmoothPlastic
	deck.Anchored = false
	deck.CanCollide = false
	deck.CFrame = root.CFrame * CFrame.new(0, 0.45, 0)
	deck.Parent = model

	local weld = Instance.new("WeldConstraint")
	weld.Part0 = root
	weld.Part1 = deck
	weld.Parent = root

	attachGlow(root, root.Color, 14, 2)

	model.PrimaryPart = root
	model.Parent = Workspace
	return model
end

-- ============================================================
-- DEATH / RESPAWN
-- ============================================================
local function killPlayer(player: Player, reason: string)
	local st = getState(player)
	if not st or not st.alive then return end
	st.alive = false

	st.profile.banked += st.runScore
	if st.runScore > st.profile.best then
		st.profile.best = st.runScore
	end
	syncLeaderstats(player, st.profile)
	-- Deferred: never yield the Heartbeat collision loop on a DataStore write
	task.spawn(function()
		saveProfile(player.UserId, st.profile)
		pcall(function()
			boardStore:SetAsync(tostring(player.UserId), st.profile.best)
		end)
	end)

	RemoteDeath:FireClient(player, reason, st.runScore, st.profile.banked, st.profile.best, st.profile.upgrades)
	RemoteJuice:FireClient(player, "death", {})
	GrooveChain.Reset(player)

	if st.root then
		st.root.Parent:Destroy()
		st.root = nil
	end
	st.runScore = 0
end

local function respawnPlayer(player: Player)
	local st = getState(player)
	if not st then return end

	-- World hazards are NOT wiped: they despawn naturally past the band.
	-- The respawner instead gets a short spawn-protection window.
	if st.root then st.root.Parent:Destroy() end

	local model = buildSkater(player)
	st.root = model.PrimaryPart
	st.alive = true
	st.airborne = false
	st.spin = 0
	st.velocityY = 0
	st.runScore = 0
	st.grazed = {}
	st.spawnProtectUntil = os.clock() + SPAWN_PROTECT_SECONDS
	-- NOTE: st.input intentionally NOT cleared — the physical key state on
	-- the client is unchanged and its InputEnded will still arrive.

	GrooveChain.Reset(player)

	RemoteStateUpdate:FireClient(player, {
		alive = true,
		banked = st.profile.banked,
		best = st.profile.best,
		upgrades = st.profile.upgrades,
		stepSeconds = BeatClock.GetSecondsPerStep(),
		trackIndex = activeTrackIndex,
	})
	RemoteScore:FireClient(player, st.profile.banked, st.profile.best, 0)
end

-- ============================================================
-- INPUT + SHOP
-- ============================================================
local UPGRADE_MAX = 5

local function upgradeCost(level: number): number
	return 150 * (2 ^ level)
end

RemoteShop.OnServerEvent:Connect(function(player: Player, key: string)
	local st = getState(player)
	if not st then return end
	if key ~= "speed" and key ~= "jump" then return end
	local level = st.profile.upgrades[key] or 0
	if level >= UPGRADE_MAX then return end

	local cost = upgradeCost(level)
	if st.profile.banked < cost then
		RemoteShop:FireClient(player, { key = key, ok = false, banked = st.profile.banked, level = level })
		return
	end

	st.profile.banked -= cost
	st.profile.upgrades[key] = level + 1
	task.spawn(function()
		saveProfile(player.UserId, st.profile, true)
	end)
	syncLeaderstats(player, st.profile)
	RemoteShop:FireClient(player, { key = key, ok = true, banked = st.profile.banked, level = level + 1 })
end)

local VALID_ACTIONS = { Left = true, Right = true, Jump = true }

RemoteInput.OnServerEvent:Connect(function(player: Player, action: unknown, pressed: unknown)
	if typeof(action) ~= "string" or not VALID_ACTIONS[action] then return end
	if typeof(pressed) ~= "boolean" then return end
	local st = getState(player)
	if not st then return end
	st.input[action] = pressed

	if action == "Jump" and pressed and st.alive and st.root and not st.airborne then
		st.airborne = true
		st.spin = 0
		-- Jump upgrades raise launch velocity (higher air = longer tricks)
		st.velocityY = JUMP_VELOCITY + st.profile.upgrades.jump * 4
	end
end)

RemoteRestart.OnServerEvent:Connect(function(player: Player)
	local st = getState(player)
	if not st or st.alive then return end
	local now = os.clock()
	if now - st.lastRestart < RESTART_COOLDOWN then return end
	st.lastRestart = now
	respawnPlayer(player)
end)

-- ============================================================
-- SCORING
-- ============================================================
-- Latency: the client acts on a beat it saw ~half a round-trip ago. Use the
-- platform's own per-player RTT estimate instead of a hardcoded guess.
local function judgeBeat(player: Player): string
	local comp = math.clamp(player:GetNetworkPing() / 2, 0, 0.15)
	local bd = math.max(0, BeatClock.BeatDistance() - comp)
	if bd < 0.06 then return "perfect" end
	if bd < 0.15 then return "good" end
	return "off"
end

local function awardFlat(st: PlayerState, points: number)
	st.runScore += points
	fireScore(st)
end

-- ============================================================
-- MAIN LOOP
-- ============================================================
RunService.Heartbeat:Connect(function(dt: number)
	local now = os.clock()

	for player, st in pairs(playerStates) do
		if not st.alive or not st.root then continue end
		local root = st.root
		local pos = root.Position

		-- Strafe (speed upgrades quicken lane changes)
		local strafe = 0
		if st.input["Left"] then strafe -= 1 end
		if st.input["Right"] then strafe += 1 end
		local strafeSpeed = PLAYER_STRAFE + st.profile.upgrades.speed * 2
		local newX = math.clamp(
			pos.X + strafe * strafeSpeed * dt,
			-RUNWAY_WIDTH / 2 + 2,
			RUNWAY_WIDTH / 2 - 2
		)

		-- Vertical
		local newY = pos.Y
		local landedThisFrame = false
		if st.airborne then
			st.velocityY -= GRAVITY * dt
			newY = pos.Y + st.velocityY * dt
			st.spin += dt * 360 -- one full rotation per second of air

			if newY <= PLAYER_Y then
				newY = PLAYER_Y
				st.airborne = false
				st.velocityY = 0
				landedThisFrame = true
			end
		end

		root.CFrame = CFrame.new(newX, newY, pos.Z)

		-- Landing: the beat decides the tier — perfect doubles, off breaks
		if landedThisFrame then
			local trickPoints = math.floor(st.spin / 360 * 100)
			st.spin = 0
			if trickPoints > 0 then
				local tier = judgeBeat(player)
				if tier == "perfect" then
					local awarded = GrooveChain.OnBeatAction(player, trickPoints * 2)
					st.runScore += awarded
					fireScore(st)
					RemoteJuice:FireClient(player, "trickPerfect", { points = awarded, chain = GrooveChain.GetChain(player) })
				elseif tier == "good" then
					local awarded = GrooveChain.OnBeatAction(player, trickPoints)
					st.runScore += awarded
					fireScore(st)
					RemoteJuice:FireClient(player, "trickOnBeat", { points = awarded, chain = GrooveChain.GetChain(player) })
				else
					GrooveChain.OnOffBeat(player)
					st.runScore += trickPoints
					fireScore(st)
					RemoteJuice:FireClient(player, "miss", { points = trickPoints })
				end
			end
			RemoteJuice:FireClient(player, "land", {})
		end

		local protected = now < st.spawnProtectUntil

		-- Hazard collisions + grazes (telegraph markers carry no Hazard
		-- attribute and are skipped; grazes are per-player, once each)
		for _, h in ipairs(Hazards:GetChildren()) do
			local hp = h :: BasePart
			if not hp:IsA("BasePart") then continue end
			if not hp:GetAttribute("Hazard") then continue end
			local dx = math.abs(newX - hp.Position.X)
			local dz = math.abs(pos.Z - hp.Position.Z)
			if dx > 8 or dz > 8 then continue end

			local hazardTop = hp.Position.Y + hp.Size.Y / 2
			local hitX = dx < (hp.Size.X / 2 + 1.6)
			local hitZ = dz < (hp.Size.Z / 2 + 2.4)
			local belowTop = newY - 0.3 < hazardTop

			if hitX and hitZ and belowTop then
				if not protected then
					killPlayer(player, hp.Name)
					break
				end
			elseif not st.grazed[hp] and dx < (hp.Size.X / 2 + 4.5) and dz < (hp.Size.Z / 2 + 4) then
				st.grazed[hp] = true
				awardFlat(st, 10)
				RemoteJuice:FireClient(player, "graze", { points = 10 })
			end
		end
		if not st.alive then continue end

		-- Pickups: on-beat grabs feed the chain; off-beat pays flat, no break
		for _, p in ipairs(Pickups:GetChildren()) do
			local pp = p :: BasePart
			if not pp:IsA("BasePart") then continue end
			local d = (Vector3.new(newX, newY, pos.Z) - pp.Position).Magnitude
			if d < 3.5 then
				local awarded = 0
				if judgeBeat(player) ~= "off" then
					awarded = GrooveChain.OnBeatAction(player, 25)
					st.runScore += awarded
				else
					awarded = 15
					st.runScore += 15
				end
				fireScore(st)
				RemoteJuice:FireClient(player, "collect", { points = awarded, onBeat = awarded > 15 })
				pp:Destroy()
			end
		end
	end
end)

-- ============================================================
-- LIFECYCLE
-- ============================================================
local function onPlayerAdded(player: Player)
	if playerStates[player] then return end

	local ls = Instance.new("Folder")
	ls.Name = "leaderstats"
	local bankVal = Instance.new("IntValue")
	bankVal.Name = "Bank"
	bankVal.Value = 0
	bankVal.Parent = ls
	local bestVal = Instance.new("IntValue")
	bestVal.Name = "Best"
	bestVal.Value = 0
	bestVal.Parent = ls
	ls.Parent = player

	local st: PlayerState = {
		player = player,
		root = nil,
		profile = loadProfile(player.UserId),
		runScore = 0,
		alive = false,
		airborne = false,
		spin = 0,
		velocityY = 0,
		input = {},
		grazed = {},
		spawnProtectUntil = 0,
		lastRestart = 0,
	}
	playerStates[player] = st
	GrooveChain.Register(player)
	syncLeaderstats(player, st.profile)

	RemoteScore:FireClient(player, st.profile.banked, st.profile.best, 0)
	respawnPlayer(player)
end

Players.PlayerAdded:Connect(onPlayerAdded)
for _, p in ipairs(Players:GetPlayers()) do
	task.spawn(onPlayerAdded, p)
end

Players.PlayerRemoving:Connect(function(player)
	local st = getState(player)
	if st then
		if st.alive then
			st.profile.banked += st.runScore
			if st.runScore > st.profile.best then
				st.profile.best = st.runScore
			end
		end
		saveProfile(player.UserId, st.profile, true)
		pcall(function()
			boardStore:SetAsync(tostring(player.UserId), st.profile.best)
		end)
	end
	GrooveChain.Remove(player)
	playerStates[player] = nil
end)

-- Shutdown: flush every live player's unbanked run before the server dies.
game:BindToClose(function()
	for _, player in ipairs(Players:GetPlayers()) do
		local st = getState(player)
		if st then
			if st.alive then
				st.profile.banked += st.runScore
				if st.runScore > st.profile.best then
					st.profile.best = st.runScore
				end
			end
			saveProfile(player.UserId, st.profile, true)
			pcall(function()
				boardStore:SetAsync(tostring(player.UserId), st.profile.best)
			end)
		end
	end
end)

-- ============================================================
-- GLOBAL LEADERBOARD BOARD
-- Top 10 best runs, refreshed every minute onto a board at the runway head.
-- ============================================================
local nameCache: { [number]: string } = {}

local function buildBoard(): Frame
	local boardPart = Instance.new("Part")
	boardPart.Name = "LeaderboardBoard"
	boardPart.Size = Vector3.new(16, 10, 1)
	boardPart.CFrame = CFrame.new(0, 12, -40) * CFrame.Angles(0, math.rad(180), 0)
	boardPart.Anchored = true
	boardPart.CanCollide = false
	boardPart.Color = Color3.fromRGB(10, 6, 22)
	boardPart.Material = Enum.Material.SmoothPlastic
	boardPart.Parent = Arena

	local sg = Instance.new("SurfaceGui")
	sg.Face = Enum.NormalId.Front
	sg.SizingMode = Enum.SurfaceGuiSizingMode.PixelsPerStud
	sg.PixelsPerStud = 50
	sg.Parent = boardPart

	local title = Instance.new("TextLabel")
	title.Size = UDim2.new(1, 0, 0.12, 0)
	title.BackgroundTransparency = 1
	title.Font = Enum.Font.Code
	title.TextSize = 28
	title.TextColor3 = Color3.fromRGB(255, 60, 200)
	title.Text = "PRIVLIDGE — TOP RUNS"
	title.Parent = sg

	local list = Instance.new("Frame")
	list.Name = "Rows"
	list.Size = UDim2.new(0.94, 0, 0.84, 0)
	list.Position = UDim2.new(0.03, 0, 0.14, 0)
	list.BackgroundTransparency = 1
	local layout = Instance.new("UIListLayout")
	layout.Padding = UDim.new(0, 4)
	layout.SortOrder = Enum.SortOrder.LayoutOrder
	layout.Parent = list
	list.Parent = sg

	return list
end

task.spawn(function()
	local rows = buildBoard()
	while true do
		-- One pcall around the whole refresh: a malformed entry must not
		-- kill the thread and freeze the board forever.
		pcall(function()
			local ok, pages = pcall(function()
				return boardStore:GetSortedAsync(false, 10)
			end)
			if ok and pages then
				-- Wipe only row labels — the UIListLayout must survive
				for _, child in ipairs(rows:GetChildren()) do
					if child:IsA("TextLabel") then
						child:Destroy()
					end
				end
				local page = pages:GetCurrentPage()
				for i, entry in ipairs(page) do
					local uid = tonumber(entry.key)
					local name = uid and nameCache[uid]
					if uid and not name then
						local okName, n = pcall(Players.GetNameFromUserIdAsync, Players, uid)
						name = (okName and n) or ("Player " .. tostring(uid))
						nameCache[uid] = name -- fallback cached too: no refetch spam
					end
					local row = Instance.new("TextLabel")
					row.Size = UDim2.new(1, 0, 0, 26)
					row.BackgroundTransparency = 1
					row.Font = Enum.Font.Code
					row.TextSize = 18
					row.TextXAlignment = Enum.TextXAlignment.Left
					row.TextColor3 = i == 1
						and Color3.fromRGB(255, 240, 120)
						or Color3.fromRGB(200, 200, 230)
					row.LayoutOrder = i
					row.Text = ("#%d  %s — %d"):format(i, tostring(name), entry.value)
					row.Parent = rows
				end
			end
		end)
		task.wait(60)
	end
end)
