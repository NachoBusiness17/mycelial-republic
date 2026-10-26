# THE FLASH PACE LAW + THE BILLION-TOKEN PATTERN MINE (operator order, 2026-10-11)

Operator order, verbatim components: "force flash for everything in zcode this
week. we're out of weekly resets so we gotta pace it and use our free lanes and
stealth." + "we have shown how to burn hermes and even how to burn this seat
down. our flash is now cooking down the hourly compute for the first time ever."
+ "now i want it all to work for us and learn from these billion token a day
spends. we've got 40 of them surely a pattern has emerged and a workflow can be
gleaned."

## LAW 1: FLASH-FORCED WEEK (this week, until weekly reset)

All ZCode seat work runs on GLM-5.3-Flash. Pro/reserve tiers stay untouched.
Rationale: weekly resets are exhausted; the burn must pace inside flash's hourly
compute, with overflow routed to free lanes and the stealth wall (the operator's
instance is running - the seat's probe was refused by its lock).
Seat consequence: batch depth drops, verification discipline rises - the
flash-priced pattern below. Deviation receipt required for any non-flash dispatch.

## LAW 2: THE BILLION-TOKEN PATTERN MINE (40 days x ~1B tokens/day)

The hermes_burn ledger (memory/runs/hermes_burn/usage.jsonl, 3,000+ rows) plus
the workflow REGISTRY (177 rows) plus FIRE_LEDGER are the dataset. 40 days of
billion-token burns exist; the pattern-mining seat answers one question: WHAT
SHAPE OF BURN PRODUCES LANDED VALUE PER TOKEN?

Mine design (mode 2, fires next window):
- LANE 1 (cost anatomy): per-day totals, per-model split, per-workflow-class
  split (ractor vs fill-ball vs mine vs execute vs gate-fire). Where do the
  billions actually go? Expect: sweeps (wide, cheap, repetitive) vs folds
  (narrow, expensive, decisive) vs debt (retries, 429s, refires).
- LANE 2 (landed-value join): every day's spend joined to that day's LINKS.jsonl
  rows + estate files created (git). Cost-per-landed-row by workflow class.
  Hypothesis from tonight's data: execute-burns (gstd rungs: 3 lanes, ~50M tok,
  11 proven executions) out-land audit-burns per token; sweeps out-land
  everything per token but produce volume, not decisions.
- LANE 3 (the pattern): what do the BEST days share? (multi-lane width?
  gate-first runs? the fill-ball-after-analysis pairing?) What do the WORST
  days share? (single-mega-lane burns? refire storms? the 1302 class?)
- LANE 4 (the workflow): distill the best-day shape into a saved workflow
  amendment (the pacing recipe: width, lane mix, gate placement, refire law)
  and one FLASH-PACED default (how much of a day's burn fits flash hourly
  compute vs needs the pro tier the operator is no longer buying this week).
- Falsifier: if the best days' shape is "the operator was awake and steering"
  (mode 1), the pattern is not a workflow, it is a dependency - and the honest
  output is the mode-2 seed list that substitutes for steering.

## What we already know (the night's own data points, pre-registered)

- gstd-rungs execute: 3 lanes / ~50M tok / 11 proven executions + suite green.
- event-substrate gap: 15 lanes / ~57M tok / 64 rows, 11/12 tier-2.
- The four ACCEPT folds tonight each completed on 40-180M tok.
- The dud: dwfrun-15738edf class (50-wide storm) - width without gate.
- The pattern candidate, stated for the mine to confirm or kill: narrow execute
  lanes with byte finish-lines at width 3-6 out-land wide sweeps per token by
  an order of magnitude; sweeps are for FINDING, executes are for LANDING, and
  the billion-token days that hurt were sweeps without a same-day execute.
