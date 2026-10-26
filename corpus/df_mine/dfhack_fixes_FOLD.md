# DFHack fix taxonomy — disease families (47 cataloged)

DFHack's `fix/*` scripts, `quickfix` module, fix/tweak/preserve plugins are the community's own violation register: each entry names an engine defect, its symptom, and the repair. Full data: `dfhack_fixes.json`.

| Family | Count | Essence |
|---|---|---|
| stuck-flags | 8 | Occupancy/job/position flags desync from reality; tiles, doors, seeds, buckets, webs freeze |
| dangling-refs | 7 | References outlive their objects: dead jobs, deleted equipment, one-sided ownership claims |
| generation-defect | 6 | Wrong data written at creation: blood in manifests, glove handedness, destroyed minerals |
| lost-updates | 5 | Engine writes a value but never propagates/persists it: nicknames, room assignments, wear |
| display-defect | 5 | Cosmetic/rendering wrongness: unnamed flasks, book titles missing |
| missing-init | 4 | Field never initialized: entity race -1, site_id -1, zero-page books, undersized pop arrays |
| arrival-deadlock | 4 | Units/armies/caravans/wildlife wedged off-map, pending entry forever |
| resource-degeneration | 3 | Runaway updates or unbounded lists: temp churn FPS drain, 3000-dead migrant wall |
| unit-ai-deadlock | 3 | Per-unit loops with no exit: eternal Worship!, sleepers, NOEXERT exhaustion |
| faction-state-poisoning | 2 | Diplomacy/enemy status corrupted: loyalty cascades, civil war |

Most common family: **stuck-flags** (8) — state cached in flags drifting from ground truth, then treated as authoritative.

Also provenance: 6 retired fixes (`fix/diplomats`, `fix/feeding-timers`…) pruned when upstream fixed the bug; 3 occupancy fixes consolidated into one.

## Three ratchet folds for the fleet

1. **Our except-pass disease vs their stuck-flags disease.** DFHack's #1 family is a flag written but never reconciled (`flags.in_job`, `occupancy`, `in_building`). Ours is the swallowed exception and the stale cache later code trusts. Rule to steal: mutable state that escapes a function boundary must have a named reconciler (as `fix/occupancy` is for phantom occupancy). New unowned mutable state = new registered debt.

2. **Automatic-vs-manual is a safety dial.** DFHack marks each fix: always-on (`quickfix`), default-on periodic (`dry-buckets`, `general-strike`), opt-in (`wildlife` — NOT default because it destroys state some players want), manual-only (`stuck-merchants` — documented dangerous under `repeat`). The enablement mode lives in the register itself. Our `configs/violation_baseline.json` should do the same: every registered debt names whether a gate may auto-fix it or whether auto-fix destroys signal.

3. **Fixes retire when upstream lands.** DFHack pruned `fix/build-location` et al. when the engine fixed bugs 5991/3295/2606, and merged three overlapping occupancy fixes into one. Registered debt is not a museum: every baseline row needs an upstream condition ("delete when X") so pruning is a ledger fact. Their fix comments carry the bug number (`:bug:`11014``) — our fix comments carry the receipt the same way.
