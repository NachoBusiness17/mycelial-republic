--!strict
-- ZoneGate: WORLDGEN_MINE.md law 4 (t35): zone access/buffs gated by
-- sphereAlliance. Each WAVE zone joins one generator_region_spheres key.
-- The region rows are GENERATED (shared/RegionSpheres.luau, df_spheres.json
-- verbatim). t67 spec: the gate owns no zone-name list. The join is
-- authored once per WAVE row as the strict-required `region` field in
-- init.server.luau, and the derived map is handed to ZoneGate.init, so a
-- zone cannot exist without a join (type error) and a join without its
-- zone cannot be written (the map is derived, not a second list; t64's
-- audit proved the old two lists were diff-identical 11 vs 11 by
-- discipline alone, the silent-drift seam this removes). The player's
-- sphere is drawn once per soul from the 130, deterministic from the
-- UserId (no UI, no DataStore, re-derivable). Portal pick per
-- Worldgen.zoneAlliance against the region's spheres (opposition outranks
-- kinship, so any opposed sphere decides):
--   allied      -> portal open + one VirtueMark per BUFF_SECONDS per zone
--   independent -> portal open, no effect (a negative is a fact)
--   opposed     -> locked door. NOT implemented: every sourced region row is
--                  unaligned spheres, so opposed is unreachable today and a
--                  dead branch would be fallback creep. If the mine ever
--                  grows an aligned region row, this is the seam that grows
--                  the lock.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Modules")
local RegionSpheres = require(Shared:WaitForChild("RegionSpheres"))
local SeedRng = require(Shared:WaitForChild("SeedRng"))
local ShadowLedger = require(script.Parent:WaitForChild("ShadowLedger"))
local Worldgen = require(Shared:WaitForChild("Worldgen"))

local ZoneGate = {}

-- t67: derived join, filled by ZoneGate.init from the WAVE rows (see
-- header spec). NONE is never picked: its row is empty, a zone joined to
-- it would carry no gate and the law would be silent furniture.
local zoneRegions: { [string]: string } = {}

local BUFF_SECONDS = 300
local REFUSAL_SECONDS = 5

-- t46 spec (WORLDGEN_MINE.md law 4, REPLICATED): the gate's verdict travels
-- to the client so the ring can be tinted without the client re-running the
-- authored join. Attribute names reject spaces, so the zone sanitizes to
-- underscores exactly like the Portal_ pad suffix is read back; one pure
-- function both sides share, values always ZoneGate.allianceFor's own.
local function gateAttr(zone: string): string
	local safe = zone:gsub("%W", "_")
	return "Gate_" .. safe
end

local lastBuff: { [string]: number } = {} -- "userId|zone" -> os.time()
local lastRefusal: { [number]: number } = {} -- userId -> os.time()

-- one sphere per soul: seeded by the UserId so the same player returns to
-- the same allegiance without any picker UI
local function ensureSphere(player: Player): string
	local existing = player:GetAttribute("Sphere")
	if typeof(existing) == "string" then
		return existing
	end
	local rng = SeedRng.new(player.UserId * 7919)
	local sphere = Worldgen.SPHERES[rng:int(1, #Worldgen.SPHERES)]
	player:SetAttribute("Sphere", sphere)
	return sphere
end

-- alliance across the region's whole sphere row: opposition outranks
-- kinship (law 4 precedence), so the first opposed sphere decides and
-- otherwise any allied sphere marks the region as kin
function ZoneGate.allianceFor(sphere: string, region: string): string
	local row = RegionSpheres.REGION_SPHERES[region]
	if not row then
		return "independent" -- unjoined region: no kin, no enmity (a fact)
	end
	local verdict = "independent"
	for _, s in ipairs(row) do
		local a = Worldgen.zoneAlliance(sphere, s)
		if a == "opposed" then
			return "opposed"
		elseif a == "allied" then
			verdict = "allied"
		end
	end
	return verdict
end

-- the portal hook: true = take the teleport, false = refused at the ring
function ZoneGate.portalGate(player: Player, zone: string): boolean
	local region = zoneRegions[zone]
	if not region then
		return true -- fixed climbs carry no join, so no gate (a fact)
	end
	local sphere = ensureSphere(player)
	local alliance = ZoneGate.allianceFor(sphere, region)
	if alliance == "opposed" then
		local now = os.time()
		if now - (lastRefusal[player.UserId] or 0) >= REFUSAL_SECONDS then
			lastRefusal[player.UserId] = now
			ShadowLedger.record(player, "Basecamp",
				("the portal to %s refuses you: your sphere %s stands opposed to the %s")
					:format(zone, sphere, region), false)
		end
		return false
	end
	if alliance == "allied" then
		local key = ("%d|%s"):format(player.UserId, zone)
		local now = os.time()
		if now - (lastBuff[key] or 0) >= BUFF_SECONDS then
			lastBuff[key] = now
			player:SetAttribute("VirtueMarks", (player:GetAttribute("VirtueMarks") or 0) + 1)
			ShadowLedger.record(player, "Basecamp",
				("the %s region welcomes a %s soul: the way is open (+1 Virtue Mark)")
					:format(region, sphere), true)
		end
	end
	return true
end

-- t67: receives the join derived from the WAVE rows; init.server.luau is
-- the single authorship site, this call is the only writer
function ZoneGate.init(regions: { [string]: string })
	zoneRegions = regions
	local function attach(player: Player)
		local sphere = ensureSphere(player)
		-- t46: stamp the same allianceFor verdict the gate enforces, once at
		-- join (sphere never changes, so the verdicts are static per soul);
		-- climb portals get no attribute, they carry no join and no tint
		for zone, region in pairs(zoneRegions) do
			player:SetAttribute(gateAttr(zone), ZoneGate.allianceFor(sphere, region))
		end
	end
	Players.PlayerAdded:Connect(attach)
	for _, p in ipairs(Players:GetPlayers()) do
		attach(p)
	end
end

return ZoneGate
