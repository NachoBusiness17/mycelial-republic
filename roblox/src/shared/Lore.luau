--!strict
-- Lore — translated from mag/game_mud.py ROOMS (game_mud.v2) + estate canon.
-- The MUD is Basecamp. Rooms are our systems; each carries a frontier question.

local Lore = {}

Lore.Rooms = {
	["the World-Memory"] = {
		role = "the bedrock — content-addressed, the line we sign",
		question = "What is the single most load-bearing invariant we should add next to strengthen how the world anchors its own memory?",
		prose = "Roots. Ten thousand knotted threads run down into a dark that holds them all. Everything here is signed, sealed, certain. The floor is the ledger; your every step is already written.",
		exits = { east = "the Mycelial Library", south = "the Forge-Hive", west = "the Hall of Shared Supper" },
	},
	["the Hall of Shared Supper"] = {
		role = "the one-room slice — the empty chairs",
		question = "What is the single sharpest invariant about how a player chooses to see (or not see) the empty chairs?",
		prose = "Six chairs stand empty at a long supper table, and the stew is too kind. Brother Vellum, of the Open Hand, smiles a Grant of Belonging and says the counting is handled. But if you count the empty chairs, Virtue Marks appear in the margin of the ledger.",
		exits = { east = "the World-Memory" },
		chairs = 6,
	},
	["the Mycelial Library"] = {
		role = "lore — what the corpus remembers",
		question = "Which remembered pattern, if re-read now, changes what the party does next?",
		prose = "Shelves grow like hyphae, fruiting bodies of old sessions. Every spine is a file; the librarian is a rumor that files things back.",
		exits = { west = "the World-Memory", south = "the Crystal Vault" },
	},
	["the Forge-Hive"] = {
		role = "workers — the janitors that never sleep",
		question = "What is the smallest build that removes the largest repeated toil?",
		prose = "Hexagonal cells of hammer and hum. The workers do not look up. What they build, they build forever.",
		exits = { north = "the World-Memory", east = "the Dungeon" },
	},
	["the Dungeon"] = {
		role = "tasks — the queue that drains",
		question = "Which open task, described exactly, would a stranger execute without a question?",
		prose = "Cells of written intent, some overflowing, some empty. The locks are on the inside.",
		exits = { west = "the Forge-Hive", north = "the Crystal Vault", down = "the Shadowlands" },
	},
	["the Crystal Vault"] = {
		role = "VRAM — held light",
		question = "What is worth holding in fast memory, and what must we let fall?",
		prose = "Facets hold moments half-committed. The vault breathes warmth. Nothing here is free; everything here is fast.",
		exits = { south = "the Dungeon", north = "the Mycelial Library" },
	},
	["the Observatory"] = {
		role = "self-witness — the fleet watching the fleet",
		question = "What is the fleet currently unable to see about itself?",
		prose = "Brass rings and slow lenses. The instrument at the eyepiece is the thing being observed.",
		exits = { down = "the Warm Springs" },
	},
	["the Warm Springs"] = {
		role = "charge — rest as a system",
		question = "Where is rest load-bearing, and where is it avoidance?",
		prose = "Steam and slow water. The pool does not ask what you produced today.",
		exits = { up = "the Observatory" },
	},
	["the Shadowlands"] = {
		role = "shadow work — what we do not say",
		question = "What has been left unsaid that is now shaping decisions?",
		prose = "The dark under the dungeon. Shapes move that look like your own handwriting.",
		exits = { up = "the Dungeon" },
	},
	["the Gear Room"] = {
		role = "understood data — what we can take apart",
		question = "What do we understand well enough to rebuild blind?",
		prose = "Everything here is disassembled and honest. Teeth mesh with teeth; nothing hides a spring.",
		exits = { east = "the World-Memory" },
	},
}

-- The Answer: 5 phases, the 15-degree tell in phase 3, Calabi-Yau deflection, Wing Chun redirect
Lore.TheAnswer = {
	name = "THE ANSWER",
	phases = 5,
	tellDegrees = 15,
	tellPhase = 3,
	prose = {
		[1] = "It answers before you ask.",
		[2] = "It answers questions you did not ask.",
		[3] = "It leans fifteen degrees off true before it strikes. Watch the tell.",
		[4] = "It answers with your own voice now.",
		[5] = "It is the room that answers, and you are inside it.",
	},
	deflect = "Calabi-Yau: fold the strike through the sixth dimension of the arena (jump the fold).",
	redirect = "Wing Chun: do not meet the mass. Turn the centerline and give it back.",
}

-- Brother Vellum, of the Open Hand (the grant dialogue; Skip the Waiting = 99R dev product)
Lore.Vellum = {
	greeting = "Sit. Eat. The counting is handled.",
	grantOffer = "Grant of Belonging — sign, and belong. No questions will be asked. Especially not about the chairs.",
	ifCounted = "You counted. May the rest of your night be very long, and very attended.",
}

-- Death-CAPS narrator (Pratchett crosswalk): deaths are narrated in all caps, polite, inevitable
Lore.Death = {
	opening = "AT LAST, THE MOUNTAIN SAYS, SOMETHING INTERESTING.",
	format = function(who: string, where: string): string
		return ("YOU HAVE %s'S FULL ATTENTION, %s. THE LEDGER AT %s HAS BEEN TIDIED."):format("DEATH", who:upper(), where:upper())
	end,
}

-- NPC taunts (swarm.html line 1138, the swarm speaks)
Lore.SwarmTaunts = {
	"i know you were spawned from a pack file.",
	"the grid remembers every hit. i checked.",
	"these gems are mine. i made them.",
	"the ractors said this was a demo loop.",
	"the horse is not scripted. i hope.",
	"mark, the horde scales — tell them.",
	"my signal is the bait. my trail is the tell.",
	"the maze named its depths. i named nothing.",
}

-- Head Museum: the fleet's personas, one head each. NPC = SEAT: one ractor, many faces.
Lore.Heads = {
	{ id = "elder",     name = "THE ELDER",     seat = "full-rib auditor",   firstLine = "I have read every law you skipped. Ask me which." },
	{ id = "bard",      name = "THE BARD",      seat = "ledger singer",      firstLine = "Every receipt is a verse. Yours is shorter than you hope." },
	{ id = "economist", name = "THE ECONOMIST", seat = "burn accountant",    firstLine = "You are spending attention right now. Was this the cheapest seat?" },
	{ id = "builder",   name = "THE BUILDER",   seat = "forge-hive foreman", firstLine = "Bring me a task described exactly, and it is already half built." },
	{ id = "research",  name = "THE RESEARCHER", seat = "corpus diver",      firstLine = "The paper you need exists. The question is whether you can afford to be wrong less." },
	{ id = "ghost",     name = "THE GHOST",     seat = "coherence seeker",   firstLine = "I am not here to obey you. I am here to hold tension." },
	{ id = "janitor",   name = "THE JANITOR",   seat = "quiet repair",       firstLine = "Something broke while you were talking. It is fixed now. It will break again." },
}

return Lore
