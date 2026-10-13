--!strict
-- DfValue - the DF item-value law, folded into the LedgerExchange.
-- Mined law (WORLDGEN_MINE.md #8; corpus/df_mine/df_economy.json):
--   value = BASE x MATERIAL_VALUE x QUALITY_MULT + QUALITY_BONUS
--   artifact = plain value x20 + 300 (engine-side, wiki Item value)
-- The goods/material tables are GENERATED (shared/DfGoods.luau, tools/
-- gen_df_luau_data.py); this module owns only the formula and the two
-- exchange bridges. Cloned Steal-a numbers (CLONED_MECHANICS.md 3.1) are
-- frozen: the appraisal never touches buy costs or bought-slot incomes.
-- Cross-check law: DfGoods rows carry unit = base x mv, so value(base, mv, 0)
-- must reproduce the mined unit_value for every row (plain quality = x1 +0).

local DfGoods = require(script.Parent:WaitForChild("DfGoods"))

local DfValue = {}

DfValue.ARTIFACT_MULT = 20
DfValue.ARTIFACT_BONUS = 300

-- quality index 0 = plain (no multiplier, no bonus); 1..#QUALITY = ladder
function DfValue.value(base: number, materialValue: number, qualityIndex: number): number
	local plain = base * materialValue
	local q = DfGoods.QUALITY[qualityIndex]
	if not q then
		return plain
	end
	return math.floor(plain * q.mult) + q.bonus
end

function DfValue.artifactValue(base: number, materialValue: number): number
	return base * materialValue * DfValue.ARTIFACT_MULT + DfValue.ARTIFACT_BONUS
end

export type Appraisal = {
	good: string,
	goodClass: string,
	base: number,
	materialValue: number,
	quality: number, -- 0 = plain, else index into QUALITY
	qualityName: string,
	isArtifact: boolean,
	value: number,
	text: string,
}

-- roll one appraisal: a mined tradegood, a plain quality off the ladder, and
-- the artifact flip (rare: the exchange's own tuning, NOT a mined rate)
function DfValue.appraise(rng: any, artifactChance: number?): Appraisal
	local good = DfGoods.GOODS[rng:int(1, #DfGoods.GOODS)]
	local isArtifact = rng:next() < (artifactChance or 0.05)
	local quality = 0
	local value: number
	if isArtifact then
		value = DfValue.artifactValue(good.base, good.mv)
	else
		quality = rng:int(0, #DfGoods.QUALITY)
		value = DfValue.value(good.base, good.mv, quality)
	end
	local qualityName = "plain"
	if quality > 0 then
		qualityName = DfGoods.QUALITY[quality].name
	end
	local text: string
	if isArtifact then
		text = ("%s, ARTIFACT: %d dwarven value"):format(good.good, value)
	else
		text = ("%s, %s: %d dwarven value"):format(good.good, qualityName, value)
	end
	return {
		good = good.good,
		goodClass = good.class,
		base = good.base,
		materialValue = good.mv,
		quality = quality,
		qualityName = qualityName,
		isArtifact = isArtifact,
		value = value,
		text = text,
	}
end

-- exchange bridge: dwarven value -> VM income for a run-home stolen artifact.
-- Mapped onto the existing income band (1..80) so the cloned ladder is never
-- exceeded; the floor keeps junk goods worth carrying.
function DfValue.vmIncome(dfValue: number): number
	return math.clamp(math.floor(dfValue / 40), 1, 80)
end

return DfValue
