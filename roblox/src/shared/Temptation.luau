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
}

Temptation.PLOTS = {
	grant_of_belonging = {
		ethic = "OATH_BREAKING",
		strength = 45,
		-- positive: values that FEED the temptation; negative: values that resist
		weights = { BELONGING = 30, POWER = 10, LAW = -25, TRUTH = -25, LOYALTY = -10, WEALTH = -5 },
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
