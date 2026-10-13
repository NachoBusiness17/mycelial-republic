# dfhack_economy — FOLD for the fleet

Mined from `corpus/dfhack_full` (plugins/workflow.cpp, plugins/autolabor/*, plugins/orders.cpp,
plugins/buildingplan/*, plugins/stockpiles/*). Details + tunables: `dfhack_economy.json`.

## Fold 1 — workflow's hysteresis band → governor_autorun's queue enable/disable
workflow never toggles a job at the target; it resumes at `goal-gap` and suspends at `goal`,
with the gap defaulting to `min(5, goal/2)`. Our `governor_autorun` plan-drainer should adopt
the deadband, not a bare threshold — re-arm below target, disarm at target, hold state between.
Second steal: workflow's *recovery backoff* (retry at 1200 ticks, grow 5/3 per failure, cap 28
days) is the correct shape for retrying failed autorun jobs without hammering a dead provider.

## Fold 2 — workflow's specificity weights → Ledger Exchange arbitration
When one producer serves many constraints, workflow picks by max *specificity weight*
(subtype 10000 > exact material 5000 > category 1000 > mask 100). The Ledger Exchange should
score bid/ask matches the same way: the most narrowly-scoped rule wins ties, weights static
and comparable across rules.

## Fold 3 — orders' sort+recheck → Ledger Exchange order book
`orders sort` orders the work queue one-time → yearly → seasonal → monthly → daily so cheap
repeats never starve one-shot work; `orders recheck` flips stale-validated orders back to
Checking instead of letting them spam failures. Steal both: LIFO/high-frequency queue items
must never block one-time asks, and any order whose precondition evaporated gets re-validated,
not cancelled-and-forgotten. The JSON order libraries (basic/furnace/military) are the exact
"importable economy preset" the Exchange wants for recipes.

## Fold 4 — autolabor modern's laborer pool + starvation doubling → wave dispatchers
labormanager sizes a generalist pool as `1 + backlog/2 + n*0.25*starve_w`, ranks by
state score (idle 0 / busy 200 / exclusive 400) plus skill protection scaled by a
staffing-vs-skills slider, and doubles the weight of any labor starved 5+ cycles. Wave
dispatchers should copy all three: reserve pool sized by backlog, protect specialists with a
tunable weight, and escalate (double) anything unclaimed past a cycle count. Its
prime-tick cadence (61) desyncing from other cycles is free jitter for our pollers.

## Fold 5 — buildingplan's pickiest-first bucketing → any fleet matcher
buildingplan buckets pending work by filter pickiness (heat, material-count, full filter
serialization) and matches pickiest first, caching the count per bucket and attaching the
nearest item — so a never-matching picky filter can't block loose ones. Steal for dispatch and
validation: bucket rules by specificity, match specific→loose, cache per-bucket counts.
Stockpiles' `.dfstock` set/enable/disable import is the config-portability model for
sharing pile/governor configs across machines.
