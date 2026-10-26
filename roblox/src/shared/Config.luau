--!strict
-- Config — THE MOUNTAIN: one experience, Basecamp = the Roshomon MUD, climbs = the ports.
-- Constants translated from the fleet originals (swarm.html 122bpm engine, arrakis laws,
-- skifree chase, monetization SKUs from ROBLOX_MONETIZATION_PLAN_20260924.md).

local Config = {}

-- Money (70% dev cut, DevEx $0.0035/Robux — the honest math lives in the plan doc)
Config.GamePasses = {
	DoubleScore = { id = 0, price = 99, name = "Double Score" },        -- swarm
	SaltCellarKey = { id = 0, price = 299, name = "The Salt-Cellar Key" }, -- early Cellar realm
	WatchfulEye = { id = 0, price = 199, name = "The Watchful Eye" },   -- see others' ledger disposition
	AnswersWeakness = { id = 0, price = 499, name = "The Answer's Weakness" }, -- 15-degree tell, phase 3
}
Config.DevProducts = {
	ExtraLife = { id = 0, price = 49, name = "Extra Life" },
	SkipVellum = { id = 0, price = 99, name = "Skip the Waiting" },
	VirtueDoubler = { id = 0, price = 149, name = "Virtue Mark Doubler (1h)" },
}

-- The swarm disco engine (verbatim constants from dashboard/static/games/swarm.html)
Config.Swarm = {
	BPM = 122,
	SPB = 60 / 122 / 2,          -- one 8th note
	baseSpawn = 0.55,            -- seconds between horde waves at depth 1
	spawnFloor = 0.07,
	spawnRamp = 0.07,            -- subtracted per diffLevel
	hordeCount = function(diffLevel: number, spawnMul: number): number
		return math.max(1, math.floor((1 + math.floor(diffLevel * 0.8)) * spawnMul))
	end,
}

-- Arrakis laws (verbatim spirit from arrakis.html: "speed is score ... the slow are safe and the safe are poor")
Config.Arrakis = {
	thumperCharges = 3,
	lineMultiplierStep = 1,      -- spice chained without stopping = LINE xN
	crestLaunchBoost = 1.6,
}

-- SkiFree
Config.Ski = {
	speedRampPerSec = 0.35,
	baseSpeed = 18,
	yetiTrigger = "crash",
}

-- Roshomon filter (game_mud.v2: statements agreed by >=2 witnesses = CORE = loot)
Config.Roshomon = { coreMinAgree = 2 }

-- The NPC brain bridge: local mag gateway serving the free stealth lanes
Config.Gateway = {
	url = "http://127.0.0.1:8771/npc",   -- tools/roblox_npc_gateway.py
	timeoutSec = 12,
	offline = true,                       -- fall back to canned persona lines when the bus is dark
}

-- K-space: every zone is an address in the fleet's knowledge space (catalog zones).
-- Items in-world carry these coords; the room that remembers indexes choices by them.
Config.KSpace = {
	origin = Vector3.new(0, 0, 0),        -- Basecamp center
	axes = { knowledge = "X", practice = "Z", depth = "Y" },
}

Config.Zones = {
	"Basecamp", "HeadMuseum", "Swarm", "RuinsGo", "Arrakis", "Ski", "LightMaze", "TheAnswer",
}

-- Control map (cloned standards; full table in docs/CLONED_MECHANICS.md §2)
Config.Controls = {
	sprint = "Shift",        -- x1.5 (Doors/MM2/RIVALS standard)
	dash = "Q",              -- 60 studs, 3s cd (Blox Fruits)
	airJump = "Space x2",    -- one double jump, resets on landing
	abilities = { Z = "Fire", X = "ThumperToss", C = "WingChunRedirect", V = "Count" },
	interact = "E",          -- ProximityPrompts everywhere
	reset = "Esc menu",      -- instant respawn (Tower of Hell law)
}

return Config
