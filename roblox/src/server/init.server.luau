--!strict
-- init.server — THE MOUNTAIN. One experience:
--   Basecamp = the Roshomon MUD (the WoW mud is Basecamp, operator 2026-09-24)
--   HeadMuseum = the fleet's minds as AI NPC heads (one ractor, many faces)
--   climbs = the ports: Swarm, RuinsGo, Arrakis, Ski, LightMaze, TheAnswer
--   TheOssuary = the Halloween spearhead (spooky skeleton maze)
--   zones_extra = the wave: 12 estate games ported by fan-out agents
-- Every surface feeds the ShadowLedger (the room that remembers), every item
-- zone carries a k-space address, and the NPC heads ride the free stealth
-- lanes through the local gateway.

local RunService = game:GetService("RunService")
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Modules")
local Config = require(Shared:WaitForChild("Config"))

local MudBasecamp = require(script:WaitForChild("MudBasecamp"))
local HeadMuseum = require(script:WaitForChild("HeadMuseum"))
local ShadowLedger = require(script:WaitForChild("ShadowLedger"))
local Monetization = require(script:WaitForChild("Monetization"))
local PlayerFeel = require(script:WaitForChild("PlayerFeel"))
local AbilitySlots = require(script:WaitForChild("AbilitySlots"))
local LedgerExchange = require(script:WaitForChild("LedgerExchange"))
local SwarmZone = require(script:WaitForChild("SwarmZone"))
local RuinsGoZone = require(script:WaitForChild("RuinsGoZone"))
local ArrakisZone = require(script:WaitForChild("ArrakisZone"))
local SkiZone = require(script:WaitForChild("SkiZone"))
local LightMazeZone = require(script:WaitForChild("LightMazeZone"))
local TheAnswerBoss = require(script:WaitForChild("TheAnswerBoss"))
local OssuaryZone = require(script:WaitForChild("OssuaryZone"))
-- the cathedral eigen-map (ractor eigenmap-two, panel 2026-09-26; the sibling
-- build eigenmap-one was killed by the judge on the mirrored minimap and
-- pruned 2026-09-27, record in watch/inbox/ractor_panel_20260926/cands/):
-- the coherent-compass plate far south; see the CathedralMap.luau header
-- for the convention
local CathedralPlate = require(script:WaitForChild("CathedralPlate"))
local ZoneGate = require(script:WaitForChild("ZoneGate"))

-- the wave: the estate's remaining games, ported by the zones_extra fan-out
-- t67 spec: each row carries its own generator_region_spheres join in the
-- strict-required `region` field, so a wave zone cannot exist without a
-- join (type error) and ZoneGate's join map is derived from these rows at
-- init, not kept as a second hand-maintained name list (t64 audit: the old
-- WAVE names and ZONE_REGION keys were diff-identical 11 vs 11 by
-- discipline alone; see ZoneGate.luau header)
type WaveZone = { name: string, region: string, module: any, pos: Vector3, color: Color3 }
local WAVE: { WaveZone } = {
	{ name = "GALLERY",         region = "LAKE",      module = require(script:WaitForChild("zones_extra"):WaitForChild("GalleryZone")),         pos = Vector3.new(0, 8, -260),    color = Color3.fromRGB(217, 164, 65) },
	{ name = "FRONTIER SOULS",  region = "GRASSLAND", module = require(script:WaitForChild("zones_extra"):WaitForChild("FrontierSoulsZone")),    pos = Vector3.new(-200, 8, -200), color = Color3.fromRGB(192, 80, 56) },
	{ name = "TOY BOX",         region = "FOREST",    module = require(script:WaitForChild("zones_extra"):WaitForChild("ToyBoxZone")),          pos = Vector3.new(200, 8, -200),  color = Color3.fromRGB(143, 217, 143) },
	{ name = "HARDWARE PRIMER", region = "DESERT",    module = require(script:WaitForChild("zones_extra"):WaitForChild("HardwarePrimerZone")),   pos = Vector3.new(220, 8, 220),   color = Color3.fromRGB(110, 198, 181) },
	{ name = "INCIDENT DUNGEON", region = "MOUNTAINS", module = require(script:WaitForChild("zones_extra"):WaitForChild("IncidentDungeonZone")), pos = Vector3.new(220, 8, -220),  color = Color3.fromRGB(124, 245, 255) },
	{ name = "MAZE ARENA",      region = "DESERT",    module = require(script:WaitForChild("zones_extra"):WaitForChild("MazeArenaZone")),       pos = Vector3.new(300, 8, 0),     color = Color3.fromRGB(124, 245, 255) },
	{ name = "SPECTRAL MAZE",   region = "SWAMP",     module = require(script:WaitForChild("zones_extra"):WaitForChild("SpectralMazeZone")),    pos = Vector3.new(-220, 8, -60),  color = Color3.fromRGB(232, 180, 90) },
	{ name = "RIDDLE MAZE",     region = "HILLS",     module = require(script:WaitForChild("zones_extra"):WaitForChild("RiddleMazeZone")),      pos = Vector3.new(300, 8, 200),   color = Color3.fromRGB(180, 140, 255) },
	{ name = "LIGHTMAP ROOMS",  region = "GLACIER",   module = require(script:WaitForChild("zones_extra"):WaitForChild("LightmapRoomsZone")),   pos = Vector3.new(-300, 8, 0),    color = Color3.fromRGB(124, 245, 255) },
	{ name = "EROSION FIELD",   region = "TUNDRA",    module = require(script:WaitForChild("zones_extra"):WaitForChild("ErosionFieldZone")),    pos = Vector3.new(0, 8, -420),    color = Color3.fromRGB(76, 106, 62) },
	{ name = "STEER FIELD",     region = "OCEAN",     module = require(script:WaitForChild("zones_extra"):WaitForChild("SteerFieldZone")),      pos = Vector3.new(-400, 8, -110), color = Color3.fromRGB(111, 216, 255) },
}

-- ---- build the world ----
Monetization.init()
MudBasecamp.build()
HeadMuseum.build()
SwarmZone.build()
RuinsGoZone.build()
ArrakisZone.build()
SkiZone.build()
LightMazeZone.build()
TheAnswerBoss.build()
OssuaryZone.build()
-- THE CATHEDRAL: beacons at the scan's eigen_centroids, one compass held in
-- map + world + bearing (north = eigen -y = world -Z); no edge anchors on
-- the DARK region; the walker HUD (client/CathedralMapHud) reads the same
-- shared module
CathedralPlate.build()
-- t67: the gate's join derives from the WAVE rows above (single authorship
-- site); ZoneGate owns no zone-name list, see ZoneGate.luau header spec
local zoneRegions: { [string]: string } = {}
for _, z in ipairs(WAVE) do
	zoneRegions[z.name] = z.region
end
ZoneGate.init(zoneRegions) -- law 4 (t35): WAVE portals gated by sphereAlliance
LedgerExchange.init()

-- wave builds are fault-isolated: one bad zone must not kill the mountain
local waveTicks: { (number) -> () } = {}
for _, z in ipairs(WAVE) do
	local ok, built = pcall(function()
		return z.module.build()
	end)
	if ok and type(built) == "table" and typeof((built :: any).tick) == "function" then
		table.insert(waveTicks, (built :: any).tick :: (number) -> ())
	elseif not ok then
		warn(("[THE MOUNTAIN] zone %s failed to build: %s"):format(z.name, tostring(built)))
	end
end

-- ---- the nervous system: input remotes (client courier -> server brain) ----
local remotes = Instance.new("Folder")
remotes.Name = "Remotes"
local movement = Instance.new("RemoteEvent")
movement.Name = "Movement"
movement.Parent = remotes
local ability = Instance.new("RemoteEvent")
ability.Name = "Ability"
ability.Parent = remotes
-- Q-037 2026-09-28: the chat relay MudBasecamp.say() promised at its old
-- stub comment — one server->client line per world-voice say()
local chat = Instance.new("RemoteEvent")
chat.Name = "Chat"
chat.Parent = remotes
remotes.Parent = ReplicatedStorage
MudBasecamp.bindChat(chat)
PlayerFeel.bind(movement)
PlayerFeel.init()
AbilitySlots.bind(ability)
AbilitySlots.init()

-- ---- portal rings: fixed climbs + the wave, all from Basecamp ----
type Portal = { to: string, pos: Vector3, color: Color3 }
local PORTALS: { Portal } = {
	{ to = "SWARM",        pos = Vector3.new(-120, 8, 120),  color = Color3.fromRGB(160, 40, 90) },
	{ to = "RUINS GO",     pos = Vector3.new(120, 8, 120),   color = Color3.fromRGB(150, 130, 80) },
	{ to = "ARRAKIS",      pos = Vector3.new(120, 8, -120),  color = Color3.fromRGB(200, 150, 60) },
	{ to = "SKI",          pos = Vector3.new(-120, 8, -120), color = Color3.fromRGB(180, 220, 240) },
	{ to = "LIGHT MAZE",   pos = Vector3.new(0, 40, 200),    color = Color3.fromRGB(150, 180, 255) },
	{ to = "THE ANSWER",   pos = Vector3.new(0, 188, 0),     color = Color3.fromRGB(220, 216, 235) },
	{ to = "THE OSSUARY",  pos = Vector3.new(-60, 8, 0),     color = Color3.fromRGB(255, 130, 40) },
}
-- the cathedral's landing is derived, never hand-set: entry() puts the
-- walker NORTH of the floor (plateCenter - (size.Z/2 + 8) on Z)
table.insert(PORTALS, { to = "THE CATHEDRAL", pos = CathedralPlate.entry(),
	color = Color3.fromRGB(91, 75, 138) })
for _, z in ipairs(WAVE) do
	table.insert(PORTALS, { to = z.name, pos = z.pos, color = z.color })
end

for i, p in ipairs(PORTALS) do
	local pad = Instance.new("Part")
	pad.Anchored = true
	pad.Size = Vector3.new(8, 0.4, 8)
	-- two concentric rings so 18 portals fit: climbs inner, wave outer
	local angle = (i / #PORTALS) * math.pi * 2
	local radius = (i <= 7) and 30 or 46
	pad.Position = Vector3.new(math.cos(angle) * radius, 8.4, math.sin(angle) * radius)
	pad.Color = p.color
	pad.Material = Enum.Material.Neon
	pad.Name = ("Portal_%s"):format(p.to)
	pad.Parent = workspace

	local lbl = Instance.new("BillboardGui")
	lbl.Size = UDim2.new(0, 140, 0, 28)
	lbl.StudsOffset = Vector3.new(0, 3, 0)
	local t = Instance.new("TextLabel")
	t.Size = UDim2.fromScale(1, 1)
	t.BackgroundTransparency = 1
	t.Text = p.to
	t.TextColor3 = p.color
	t.Font = Enum.Font.Garamond
	t.TextSize = 18
	t.Parent = lbl
	lbl.Parent = pad

	pad.Touched:Connect(function(hit)
		local player = hit.Parent and Players:GetPlayerFromCharacter(hit.Parent)
		-- law 4 (t35): the gate answers before the pivot; a refusal is a
		-- locked door, so no teleport and no ledger line for the crossing
		if player and player.Character and ZoneGate.portalGate(player, p.to) then
			player.Character:PivotTo(CFrame.new(p.pos + Vector3.new(0, 6, 0)))
			ShadowLedger.record(player, "Basecamp", ("took the portal to %s"):format(p.to))
		end
	end)
end

-- ---- one heartbeat drives every climb ----
RunService.Heartbeat:Connect(function(dt: number)
	SwarmZone.tick(dt)
	ArrakisZone.tick(dt)
	SkiZone.tick(dt)
	LightMazeZone.tick(dt)
	OssuaryZone.tick(dt)
	LedgerExchange.tick(dt)
	CathedralPlate.tick(dt) -- the chain strips breathe (THE CATHEDRAL)
	for _, tick in ipairs(waveTicks) do
		-- fix t1b 2026-09-25: waveTicks is (number) -> (), so pcall's type was
		-- just (boolean) and `local ok, err` needed 2 values (a01 TypeError at
		-- 150,3). The ...any tail is the err channel pcall forwards on failure.
		local ok, err = pcall(function(): ...any
			tick(dt)
		end)
		if not ok then
			warn(("[THE MOUNTAIN] wave tick fault: %s"):format(tostring(err)))
		end
	end
end)

-- ---- leaderstats: the Roblox-standard visible scorecard (M-key player list) ----
local function attachLeaderstats(player: Player)
	local stats = Instance.new("Folder")
	stats.Name = "leaderstats"
	local marks = Instance.new("IntValue")
	marks.Name = "Virtue Marks"
	marks.Parent = stats
	local rebirths = Instance.new("IntValue")
	rebirths.Name = "Rebirths"
	rebirths.Parent = stats
	local invariants = Instance.new("IntValue")
	invariants.Name = "Invariants"
	invariants.Parent = stats
	local summits = Instance.new("IntValue")
	summits.Name = "Summits"
	summits.Parent = stats
	stats.Parent = player

	-- t56 2026-09-25: the 1s GetAttributes poll (t14c's stopgap) is gone;
	-- leaderstats now update on change signals. VirtueMarks/Rebirths/Invariants
	-- each bind GetAttributeChangedSignal. The Summit_ round booleans have
	-- dynamic names, so they ride the catch-all AttributeChanged event:
	-- first-time SetAttribute fires it with the new name per the official
	-- attributes doc example (SetAttribute("Grow", false) on a fresh instance
	-- "Fires Changed and AttributeChanged"). Sole Summit_ writer is the
	-- LightMazeZone.luau:156 SetAttribute (guarded at :155, once per round);
	-- t14c's finding still holds that no dedicated Summits attribute exists in
	-- src, so the scorecard counts Summit_ names instead of inventing a stat.
	-- Scripts cannot remove attributes, and the seed calls below cover values
	-- present before attach, so every case is signal-covered: no polling
	-- fallback remains.
	local function syncMarks()
		marks.Value = player:GetAttribute("VirtueMarks") or 0
	end
	local function syncRebirths()
		rebirths.Value = player:GetAttribute("Rebirths") or 0
	end
	local function syncInvariants()
		invariants.Value = player:GetAttribute("Invariants") or 0
	end
	local function syncSummits()
		local summitCount = 0
		for name in pairs(player:GetAttributes()) do
			if string.sub(name, 1, 7) == "Summit_" then
				summitCount += 1
			end
		end
		summits.Value = summitCount
	end

	syncMarks()
	syncRebirths()
	syncInvariants()
	syncSummits()

	player:GetAttributeChangedSignal("VirtueMarks"):Connect(syncMarks)
	player:GetAttributeChangedSignal("Rebirths"):Connect(syncRebirths)
	player:GetAttributeChangedSignal("Invariants"):Connect(syncInvariants)
	player.AttributeChanged:Connect(function(name: string)
		if string.sub(name, 1, 7) == "Summit_" then
			syncSummits()
		end
	end)
end
Players.PlayerAdded:Connect(attachLeaderstats)
for _, p in ipairs(Players:GetPlayers()) do
	attachLeaderstats(p)
end

local summary: string = ("%d wave zones wired, %d portals live"):format(#WAVE, #PORTALS)
	print(("[THE MOUNTAIN] built: %s. Basecamp is the mud, the heads are listening on %s.")
		:format(summary, Config.Gateway.url))
