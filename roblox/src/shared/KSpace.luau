--!strict
-- KSpace — the shared knowledge space. Every item/room carries an address; the
-- room that remembers indexes choices by it. Mirrors the fleet catalog zones.

local KSpace = {}

export type Address = { zone: string, knowledge: number, practice: number, depth: number }

-- zone addresses: knowledge axis (what it is), practice axis (what you do there),
-- depth axis (how deep in the mountain). Basecamp is the origin.
local ZONES: { [string]: Address } = {
	["Basecamp"]              = { zone = "Basecamp", knowledge = 0, practice = 0, depth = 0 },
	["HeadMuseum"]            = { zone = "HeadMuseum", knowledge = 2, practice = 1, depth = 0 },
	["Swarm"]                 = { zone = "Swarm", knowledge = -3, practice = 4, depth = 1 },
	["RuinsGo"]               = { zone = "RuinsGo", knowledge = 4, practice = 3, depth = 2 },
	["Arrakis"]               = { zone = "Arrakis", knowledge = -2, practice = 5, depth = 2 },
	["Ski"]                   = { zone = "Ski", knowledge = -4, practice = 3, depth = 1 },
	["LightMaze"]             = { zone = "LightMaze", knowledge = 3, practice = 2, depth = 3 },
	["TheAnswer"]             = { zone = "TheAnswer", knowledge = 0, practice = 0, depth = 6 },
}

function KSpace.get(zone: string): Address?
	return ZONES[zone]
end

function KSpace.all(): { [string]: Address }
	return ZONES
end

-- nearest zone to a world position (the smart-GPS receiver: where am I in k-space?)
function KSpace.nearest(pos: Vector3): Address
	local best, bestD = ZONES.Basecamp, math.huge
	for _, a in pairs(ZONES) do
		-- world X ~ knowledge, world Z ~ -practice, world Y ~ -depth (up the mountain = depth)
		local d = (Vector3.new(a.knowledge * 40, -a.depth * 30, -a.practice * 40) - pos).Magnitude
		if d < bestD then best, bestD = a, d end
	end
	return best
end

-- drift: the difference between where the compass points and the referent.
-- GPS law: corr(dM, dR) is the instrument; here drift = angular error to the beacon,
-- corrected when the player visits a beacon (triangulation).
function KSpace.drift(from: Vector3, beaconPos: Vector3, claimedDir: Vector3): number
	local trueDir = (beaconPos - from).Unit
	local cos = math.clamp(trueDir:Dot(claimedDir.Unit), -1, 1)
	return math.deg(math.acos(cos))
end

return KSpace
