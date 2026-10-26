--!strict
-- Temptation - DF's villain law, folded onto Vellum's grant.
-- Mined law (dwarffortresswiki.org Villain, WORLDGEN_MINE.md #5): temptation
-- is checked against the target's personality and VALUES, and failure to
-- resist becomes ONGOING CORRUPTION. The act also carries an ETHIC, weighed
-- against the value it offends (DF ethics-shaped; the axes are DF value
-- tokens). The player's value profile is read at roll time from ledger facts
-- (attributes the ShadowLedger already files), so the counted chairs are the
-- spine of the resistance exactly as the hall teaches.
--   succumb iff roll(0..99) < threshold
--   threshold = plot.strength + sum(weight * value / 50), clamped 5..95

local Temptation = {}

Temptation.VALUES = { "LAW", "LOYALTY", "TRUTH", "POWER", "WEALTH", "BELONGING" }

-- the ethics chain: each plot's act weighs against one value (the pull is
-- applied through that value's weight in the plot, so profiles that hold the
-- value high resist harder, DF's values-vs-temptation shape)
Temptation.ETHICS = {
	OATH_BREAKING = { weighs = "LAW", note = "signing without counting" },
	THEFT = { weighs = "LAW", note = "stealing sacred relics or sovereign treasures" },
	TREASON = { weighs = "LOYALTY", note = "subverting sovereign rule and loyalty to the throne" },
	CORRUPTION = { weighs = "TRUTH", note = "necromantic defiance of mortality and natural order" },
	DECEIT = { weighs = "TRUTH", note = "proclaiming fabricated visions and fraudulent prophecy" },
}

export type PlotDef = {
	ethic: string,
	strength: number,
	weights: { [string]: number },
	description: string?,
}

Temptation.PLOTS = {
	grant_of_belonging = {
		ethic = "OATH_BREAKING",
		strength = 45,
		-- positive: values that FEED the temptation; negative: values that resist
		weights = { BELONGING = 30, POWER = 10, LAW = -25, TRUTH = -25, LOYALTY = -10, WEALTH = -5 },
		description = "Sign the vellum grant to buy a seat without counting",
	},
	deathless_cult = {
		ethic = "CORRUPTION",
		strength = 55,
		weights = { POWER = 35, BELONGING = 15, TRUTH = -30, LAW = -25, LOYALTY = -10, WEALTH = -5 },
		description = "Found a necromantic deathless cult to evade mortality",
	},
	artifact_theft = {
		ethic = "THEFT",
		strength = 50,
		weights = { WEALTH = 35, POWER = 15, LAW = -30, LOYALTY = -25, TRUTH = -10, BELONGING = -5 },
		description = "Steal a sacred relic of power from the mountain vault",
	},
	usurp_throne = {
		ethic = "TREASON",
		strength = 60,
		weights = { POWER = 40, WEALTH = 10, LOYALTY = -35, LAW = -30, TRUTH = -15, BELONGING = 5 },
		description = "Subvert the sovereign throne and seize dominion",
	},
	false_prophet = {
		ethic = "DECEIT",
		strength = 45,
		weights = { BELONGING = 30, POWER = 25, TRUTH = -35, LAW = -20, LOYALTY = -10, WEALTH = -5 },
		description = "Preach fabricated visions and false miracles to command devotion",
	},
}

export type Profile = { [string]: number }

-- the player's values, derived from ledger facts (never stored mutations)
function Temptation.profile(player: Player): Profile
	local counted = player:GetAttribute("CountedChairs") == true
	local rebirths = (tonumber((player:GetAttribute("Rebirths"))) or 0)
	local marks = (tonumber((player:GetAttribute("VirtueMarks"))) or 0)
	return {
		LAW = counted and 30 or 0, -- the count is an oath kept
		TRUTH = counted and 30 or 0, -- they looked at what the hall hides
		LOYALTY = counted and 10 or 0,
		POWER = math.min(rebirths * 10, 40),
		WEALTH = marks >= 1000 and 20 or 0,
		BELONGING = 20, -- everyone wants a seat; the grant says it is handled
	}
end

-- query available plot IDs (sorted for deterministic iteration)
function Temptation.listPlots(): { string }
	local ids = {}
	for id in pairs(Temptation.PLOTS) do
		table.insert(ids, id)
	end
	table.sort(ids)
	return ids
end

function Temptation.getPlot(plotId: string): PlotDef?
	return Temptation.PLOTS[plotId]
end

-- one temptation roll; returns succumbed, the roll, and the threshold it met
function Temptation.roll(rng: any, plotId: string, profile: Profile): (boolean, number, number)
	local plot = Temptation.PLOTS[plotId]
	if not plot then
		return false, 0, 0
	end
	local bias = 0
	for value, weight in pairs(plot.weights) do
		bias += weight * ((profile[value] or 0) / 50)
	end
	local roll = math.floor(rng:next() * 100)
	local threshold = math.clamp(math.floor(plot.strength + bias), 5, 95)
	return roll < threshold, roll, threshold
end

return Temptation
