--!strict
-- Soul — DF's unit_soul fold: the psyche as a record separate from the body.
-- Mined from DFHack (corpus/df_mine/dfhack_innerlife.json + dfhack_datamodel.json):
--   emotions are timestamped LEDGER ROWS naming their causal thought (never
--   editable scalars); stress aggregates into one signed scalar binned by the
--   exact cutoff ladder into 7 categories Miserable..Ecstatic; needs carry
--   focus_level with the -10000 unbailable pin; traits/values are static
--   multiplier lenses applied at read time, not stored mutations.
-- Two-stage law: events log first, scalars derive, thresholds gate.

local Soul = {}

export type EmotionRow = {
	thought: string,     -- the causal thought, named (DF law: rows name their cause)
	emotion: string,     -- emotion type
	strength: number,    -- 100 x factor, signed
	year: number,        -- timestamp (revocable: synthetic rows flagged, not deleted)
	synthetic: boolean,
}

export type Need = { id: string, focus: number } -- focus -999..+400; <=-10000 = unbailable pin

export type Soul = {
	emotions: { EmotionRow },
	needs: { Need },
	traits: { [string]: number },  -- static lens: multipliers at read time
	values: { [string]: number },  -- -50..+50 (the temptation weights)
	dreams: { { dream: string, accomplished: boolean } },
}

-- DF stress cutoff ladder -> 7 categories (from dfhack_innerlife mine)
local CUTOFFS: { number } = { 50000, 25000, 10000, -10000, -25000, -50000, -100000 }
local CATEGORIES: { string } = { "ecstatic", "quite cheerful", "fine", "haggard", "miserable", "wretched", "broken" }

function Soul.new(): Soul
	return { emotions = {}, needs = {}, traits = {}, values = {}, dreams = {} }
end

-- stage one: events log, naming their cause
function Soul.record(s: Soul, thought: string, emotion: string, strength: number, year: number)
	table.insert(s.emotions, { thought = thought, emotion = emotion, strength = strength, year = year, synthetic = false })
end

-- aggregate: signed scalar derived from the ledger (never stored as truth)
function Soul.stress(s: Soul): number
	local total = 0
	for _, e in ipairs(s.emotions) do
		total += e.strength
	end
	return total
end

function Soul.mood(s: Soul): string
	local stress = Soul.stress(s)
	for i, cut in ipairs(CUTOFFS) do
		if stress >= cut then
			return CATEGORIES[i]
		end
	end
	return CATEGORIES[#CATEGORIES] -- broken
end

-- needs: focus decays toward the pin; <=-10000 is unbailable (activity locks)
function Soul.addNeed(s: Soul, id: string)
	table.insert(s.needs, { id = id, focus = 0 })
end

function Soul.decayNeeds(s: Soul, rate: number)
	for _, n in ipairs(s.needs) do
		n.focus = math.max(n.focus - rate, -10000) -- the unbailable pin
	end
end

function Soul.meetNeed(s: Soul, id: string, amount: number)
	for _, n in ipairs(s.needs) do
		if n.id == id then
			n.focus = math.min(n.focus + amount, 400) -- DF focus ceiling
		end
	end
end

-- strange-mood gates (DF: stress rolls at 20000/50000/100000 -> mood types)
function Soul.moodRisk(s: Soul): string?
	local stress = Soul.stress(s)
	if stress >= 100000 then return "possessed" end
	if stress >= 50000 then return "secretive" end
	if stress >= 20000 then return "fey" end
	return nil
end

return Soul
