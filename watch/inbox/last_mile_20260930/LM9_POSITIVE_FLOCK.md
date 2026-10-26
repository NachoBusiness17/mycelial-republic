# LM9 — POSITIVE flock: food gradients vs threat gradients (A/B verdict)

Date: 2026-09-30 · Lane: LM9 (ZCode) · Commit: NONE (uncommitted, per lane law)

## Mission (operator law 2026-09-30)

The fish behave under THREAT gradients (flee pressure, tire mechanics — V6
tuned the chase-bites). BUILD the positive mode: food-gradient reward
sources that ATTRACT; fish seek food, gain satiation, satiation modulates
explore-vs-exploit. A/B harness: same board, same seed, N ticks, THREAT
(player chases, fish flee/tire) vs POSITIVE (food placed where the operator
wants fish — luring). Metrics: time-to-target, panic-events/sec vs
calm-events/sec, cohesion. Prediction: positive mode moves the school with
fewer errors (panic state entries) than threat mode. MEASURE IT.

## The verdict (prediction CONFIRMED, both instruments)

Same board (game.gd POOL_LAYOUT, spring -> crown 892px), same seed 20260929,
same 5400 ticks (90s at the game's 60Hz), same target. Raw bytes:
`LM9_POSITIVE_FLOCK_raw.json` (this directory).

| metric | THREAT (herd) | POSITIVE (food at crown) |
|---|---|---|
| t80 (80% of school at target) | NEVER (0.0 frac at 90s) | **38.0 s** (frac 1.0) |
| panic entries (flee-state entries) | 5,530 (**61.4/s**) | **0** (0.0/s) |
| calm entries (graze-state entries) | 0 | 17,366 (193.0/s) |
| catches (fish killed) | 0 (herd) / 12 (chase) | 0 |
| cohesion (mean dist to centroid) | 38.2 px (scatter) | **13.3 px** (3x tighter) |
| school survived | 12/12 (boiled in place) | 12/12 |
| mean satiation final | 0.0 (all spent) | 1.0 (all fed) |

IN-ENGINE (the real `flock.gd`, Godot 4.3 headless probe, same board/seed/
ticks; probe created-run-deleted per the V6 pattern): positive t80 = 38.7s,
panic 0, satiation 0.9996; threat t80 = never, panic 4,133 (45.9/s), frac at
target 0.0. Cross-instrument agreement on the load-bearing numbers (t80
38.0 vs 38.7s; panic 0 vs thousands); the threat panic-rate delta (61 vs
46/s) is the two RNG streams drawing different initial jitters — same law,
different stream, both verdicts identical in shape.

### Threat policy census (no single cursor moves this school)

All four single-cursor threat policies measured (byte-backed in the raw
JSON census block; none reaches t80 in 90s):

| policy | what it does | alive | panic/s | catches |
|---|---|---|---|---|
| herd (behind rearmost) | school BOILS in place, pinned at spawn | 12 | 61.4 | 0 |
| chase (current behavior) | EXTERMINATES the school (fishing, not herding) | 0 | 8.0 | 12 |
| standoff (behind centroid) | DEADLOCK: school parks at 23.1px, just outside the 20px bubble; panic freezes | 12 | 5.0 | 0 |
| lead (walk through) | school parts around the bubble, pins | 12 | 5.0 | 0 |

The structural cause: flee is REPULSION from a point. It scatters radially;
the school (scatter 20-38px vs a 20px bubble) parts around the threat.
Every unit of school movement is purchased with panic entries, and the
purchase does not even deliver transit. The food gradient is a shared
directional attractor: the whole school glides at ~24 px/s terminal
(POOL_PULL-law) with zero panic and tightens while it goes.

## What was built (file ownership)

1. `mag/flock_positive.py` (NEW, the LAW) + `mag/flock_positive_ab.py`
   (NEW, the A/B harness; split to hold the violation-ratchet 400-line
   cap — both files ratchet-clean, and the split output is byte-faithful
   to the pre-split run): step_threat is a per-line mirror of `flock.gd`
   step() (constants cited to .gd lines; the visual-only pheromone trail
   is not mirrored — trail_steer is never called inside step);
   step_positive is the new law (nearest active source; pull beyond
   FOOD_PREF_DIST scaled by hunger = 1 - satiation; bite inside EAT_RADIUS
   only while not full; digest otherwise; fatigue rests to 0);
   run_ab() runs both arms + the 4-policy census with the verdict fields
   (fewer_panic_errors / faster_or_equal_t80 / tighter_or_equal_cohesion /
   no_threat_policy_transits). FOOD_PULL = 22.0 cites game.gd POOL_PULL —
   the positive arm holds no force advantage the game does not already use.
   CLI: `python -m mag.flock_positive_ab ab [--ticks N] [--seed S]`.
2. `roblox_to_godot/systems/flock.gd` (this lane's ownership per V6's
   precedent): positive mode LANDED, flag-gated — `var positive := false`
   default; `food` array + `add_food()`; `_step_food()` (the Python
   mirror's law, dictionaries-by-reference decrement the source); satiation
   key added to add_fish; wiggle modulated by satiation in positive mode
   (0.05 * (0.4 + 1.2*sat) — explore grows as hunger falls); catch gated on
   `not positive`. The threat path (positive = false) is byte-identical to
   V6's tuning: FLEE_RADIUS 20.0, push 6.0, tire dt/COAST_TIME, branch
   order — verified by tests/test_flock_positive.py constant-parity laws.
3. `tests/test_flock_positive.py` (NEW): 14 tests — threat-mirror constant
   parity (parse both files, numbers must be equal: the drift law), V6 push
   6.0 preserved in-game, tire law (fatigue full at ~0.8s), flag gate,
   food-attracts, feeding/depletion/full-fish-does-not-bite, digestion,
   hunger-scaled pull, satiated-explores-more, zero-panic-by-construction,
   determinism (same seed -> same bytes), and the A/B verdict law itself
   (positive beats threat on all three axes; census proves no transit;
   chase policy kills 10+).

## Verify

- `pytest tests/test_flock_positive.py -q` -> 14 passed.
- Neighborhood: `pytest tests/test_motion_rows.py tests/test_water_swarm.py
  -q` -> 55 passed (brain path untouched).
- Full suite `pytest -q --ignore=tests/test_mountain_reveal.py` (that file
  collects another lane's in-flight tools/mountain_reveal.py, currently a
  syntax error at :384 — untracked, not this lane's) ran to completion:
  .pytest_cache lastfailed records 12 failures, ALL outside this lane's
  surface (clerk routing, planner integration, cursor bridge, debug capsys,
  diag pid, memory/working/*) — none in flock/game modules; this lane's
  files are clean.
- Violation ratchet: no NEW violations in mag/flock_positive*.py (the
  first cut was 550 lines + one except-pass; fixed by the law/harness
  split, both files < 280 lines).
- In-engine probe: `Godot_v4.3-stable_win64_console.exe --headless --path
  roblox_to_godot --script res://lm9_probe.gd` -> exit 0, one JSON line,
  zero script errors; probe deleted after the run (V6 pattern).
- Headless boot smoke `--quit-after 60` -> exit 0, banner only (the
  flag-gated edit changes no default behavior).

## Handoff notes (not this lane's ownership)

- `game.gd` wiring for playing positive mode (a key to drop food at the
  cursor, flock.positive toggle, HUD food draw) belongs to the game.gd
  owner; flock.gd is ready as-is (`flock.positive = true; flock.add_food(
  pos, amount)`).
- `fish_brain.gd` still has no seek/graze verbs (its lane's MOTION_TABLE
  dialect work); the brain path is threat-only until that lane extends it —
  game.gd falls back to flock.step for positive play in the meantime.
- fish_brain.gd:30 still mirrors FLEE_RADIUS 14 (V6's handoff note stands).
