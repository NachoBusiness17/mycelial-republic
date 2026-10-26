# FIELD EXPERIMENT RESULT - FIELD-2 (THE FOUNDATION POUR), 2026-10-01

**Schema:** field_experiment.result.v1 · **lane:** FIELD-2 · **spec:**
watch/inbox/model_garden/STEERING_FIELD_THEORY.md sec 3 (the falsifiable
minimal experiment "field steering beats list steering") · **instrument:**
`tools/field_experiment.py` (deterministic, double-run byte-identical,
digest 1826c7cd8880089a) · **spend:** $0.0017 of the $1 hard cap.

**Claim under test:** allocating the day's work by relaxing a GPS-elevated
integer field with boid-family advection beats the current driver's
sequential queue, at equal-or-lower cost, judged on real outcomes.

## 1. SETUP (the assembly, six organs + one adapter, all imported not forked)

- Task stream: `tools/k8s_water_sim.py workload_from_ledger()` over the real
  `tools/gps_mcp/gps_ledger.db3` (242 verdict_log rows, one replayed day
  2026-09-30, 8 arrival ticks, 67 verdict=0 rows pre-shed into the waste
  basin per the feed's own law).
- Terrain: `seed_terrain()` (the ~40-line L2 adapter) -> 9 model rows x 9
  shape columns; elevation from pass_rate, per-cell cross_section from
  sample_size. Board frozen at `watch/inbox/model_garden/FIELD2_BOARD_SPEC.json`;
  column order from `mag/flock_scheduler.py plan()` (the swarm-allocation
  organ contributed the layout).
- FIELD kernel: `mag/river.py` (field_flow Jacobi sheet flow + sill erosion
  ON, silt mantle 4 so the erosion law can fire at all; 153 carve transfers
  executed).
- Advection: `mag/flock_positive.py step_positive`, one school of 12 per
  model family (9 schools, 108 fish), one 60Hz fish-second per scheduler
  tick; food = standing work volume; attendance = a fish grazing the cell
  patch (within FOOD_PREF_DIST 30, the game's own arrival radius).
- Impulse: `mag/steer_seal.py` sealed envelope minted offline and admitted
  through the single gate: authority `operator-seal`, event `sealed_admitted`,
  key_id 3e46297f84754fed, nonce 8d90dfe76d354de02bd6c14b7ce45fb3, envelope
  sha256 prefix 0ac6aedef8e5c725; payload = `mag/water_swarm.py
  water_doctrine()` + the POUR directive (lure, never chase). Placement-time
  pour of 30 food units at the `mag/flock_field.py` PhiField minimum
  (legality-propagator-v1|legality-water-graph-v1), fired tick 4. Keyfile
  OUTSIDE ROOT per the X5 precedent.
- Gates: `mag/water_graph.py` (serve pipe cap 4/tick; waste boil 1/tick;
  condensed retries re-poured onto the terrain at their historical cells).
- LIST arm (control): `tools/k8s_water_sim.py simulate()` exactly as its own
  demo ships it (classes critical/burstable 60/40, quota 2 + burst cap 2,
  escalation budget 1), max_ticks raised 24 -> 400 so both arms can drain.
- Same budget: identical arrival stream, identical 4-units/tick service cap,
  identical 400-tick ceiling. Conservation audited every tick (volume and
  silt; no leak ever fired).
- Judgment: mechanical decision-agreement vs the BLIND seat list (frozen at
  `watch/inbox/model_garden/FIELD2_SEAT_LIST.md` BEFORE either arm ran) + two
  blind judges through `tools/model_garden.py` (kimi-k2 relay + deepseek
  blind, the OVERMIND sec 6 duel shape; blind material at
  `watch/inbox/model_garden/FIELD2_ARMS_BLIND.md`, arm labels assigned by run
  digest parity: A = field).

## 2. THE TWO ARMS' SCORES (pre-registered metrics)

| metric | FIELD arm | LIST arm |
|---|---|---|
| ticks-to-80%-served (t80, primary) | **66** | 134 |
| wasted dispatches (units served at weak coordinates) | **51 / 242** | 92 / 242 |
| decision-agreement vs blind seat list (mechanical) | **7/9 = 77.8%** | 6/9 = 66.7% |
| ticks used (drain-complete) | **118** | 182 |
| units served | 242/242 | 242/242 |
| t80 literal-spec variant (served+standing-shed / arrived) | 1 | 1 |

The literal t80 variant is degenerate on this workload (the 67-unit waste
seed stands as "shed" from tick 1, so both arms read 1); the served-only
primary is reported above. Attention lag is visible and honest: the
theoretical floor at 4 units/tick is 49 ticks; the field paid 17 ticks of
medium lag (schools transit, dead-band milling), the list paid 85 ticks of
queue serialization (one class lane per tick).

Routing shape (the decision records): the field concentrated service at the
terrain's strong minima (grok-4.7|adversarial-review 35 units vs the
driver's 9; deepseek|planning 16; propagator 102) and starved the weak rows
the driver kept feeding (glm|adversarial-review 3 vs the driver's 23).

## 3. THE JUDGES' VERDICTS (blind, A = field, filed verbatim)

- kimi-k2 (relay, $0 on prepaid Nous credits): AGREEMENT_A 6/9 = 66.7%,
  AGREEMENT_B 5/9 = 55.6%, T80_WINNER A, WASTED_WINNER A, OVERALL A,
  VERDICT **A-WINS**. Rationale: "ARM A reached 80% service in 66 ticks
  versus B's 134, and served only 51 weak-coordinate units versus B's 92.
  A concentrated load on strong models; B scattered across weak coordinates
  without prioritizing seat picks." Caveat: end-of-day hindsight exploited
  more aggressively by A.
- deepseek-chat (blind, $0.0017 metered): AGREEMENT_A 5/9 = 55.6%,
  AGREEMENT_B 6/9 = 66.7%, T80_WINNER A, WASTED_WINNER A, OVERALL A,
  VERDICT **A-WINS**. Rationale: "Arm A routed the big legality block and
  most adversarial-review to strong coordinates... Arm B spread units
  across weak models in proportion to arrivals." Caveat: agreement counts
  reflect seat-following, not predictive skill.

Judge disagreement (filed, never flattened): the two judges disagree with
each other AND with the mechanical count on the agreement sub-metric (kimi
A 6/9; deepseek A 5/9; bytes A 7/9). Both agree on every outcome axis and
the overall winner. The mechanical count is the falsifier's input.

Outputs: `watch/inbox/model_garden/field2-judge-kimi.md`,
`field2-judge-deepseek.md`; usage banked in
`memory/runs/model_garden/usage.jsonl` (rows field2-judge-*: kimi 3345 in /
170 out / $0.0; deepseek 3408 in / 160 out / $0.0017).

## 4. FALSIFIER TABLE (spec sec 3, any one kills)

- FIELD loses t80 AND wasted: NO (wins both, 66 vs 134 and 51 vs 92).
- decision-agreement < 60%: NO (mechanical 77.8%; worst judge read 55.6%,
  disagreement filed above).
- mid-task envelope redirect of a running glm turn: NONE (no glm turns run
  mid-sim; the one envelope is placement-time, admitted pre-run).
- conservation violated: NO (per-tick volume and silt audits held to the
  last tick; double-run byte-identical, digest 1826c7cd8880089a).
- spend > $1: NO ($0.0017 total).

## 5. VERDICT: FIELD-WINS

At this scale (one replayed ledger day, 242 units, equal serve budget), the
GPS-elevated relaxation with boid advection beat the shipped sequential
queue on both outcome axes and on decision-agreement, at $0.0017 total
experiment cost. The theory-level falsifier 1 (LIST wins cleanly) did not
fire; the frame survives its first real-data test.

Honest limits, both judges' caveat plus the instrument's own:
- The capability table is end-of-day (mild hindsight for BOTH arms; the
  list arm ignored the signal, the field acted on it; the win measures
  acting-on-signal, not prophecy).
- Cross-shape leakage: Moore-neighbor flow can serve a unit at a different
  shape's column (world-tick column served 8 vs 4 arrivals; grading work
  drained into planning cells). Part of the field's wasted-dispatch
  advantage is terrain moving work regardless of shape; unmeasured cells at
  elev 150 form ridges that trap basins (qwen-max|adversarial-review, pass
  0.44, still drew 21 units as a local minimum).
- The seat list is one seat's rule (n>=3 evidence gate); the field has no
  such gate and trusted a 1.0/n=2 coordinate (deepseek|planning, 16 units).

## 6. NEXT ITERATION OF THE FIELD ARM

1. Aim the sealed pour at UNDER-ATTENDED strong coordinates (deep basin,
   no school in grazing range) instead of the heaviest shape's best cell,
   which was already the deepest basin (this run's lure was redundant;
   impulse fired tick 4 with no routing decision depending on it).
2. Break the basin trap: seed unmeasured cells from the model's row-mean
   pass rate (or a neutral saddle) instead of a flat 150 ridge, and test a
   sample-size-shrunk elevation (pass_rate pulled toward the global mean as
   n -> 0) so 1.0/n=2 minima stop outbidding n>=9 evidence.
3. Close the shape leak: per-column walls or shape-conditional conductance,
   then re-run; if the field still wins wasted-dispatches WITHIN shapes,
   the routing claim is stronger than this run can show.
4. Feed school state back as per-cell conductance to the served gate
   (replacing gate-priority-by-attendance), removing the dependence on the
   exact patch-arrival radius that this iteration had to fix by hand.
5. Escalation shape A/B: retry re-poured at the historical cell (this run)
   vs retry at the best-in-shape cell (k8s "retries jump to top tier"),
   measuring which retry law drains the waste basin cheaper.

## 7. DEVIATIONS (spec text vs bytes; bytes won, per lane order)

- D1 elevation polarity: spec says "elev = pass_rate scaled 0-255"; the
  downhill-only flow law would then advect work TOWARD failing coordinates,
  inverting the spec's own wasted-dispatch metric. flock_field's own law
  (phi = distance-to-solution, descent to goal) resolves it: elevation =
  4 + round((1 - pass_rate) * 200), the cost terrain.
- D2 per-cell cross_section: field_flow bytes carry one board-wide value;
  the L2 wire needs per-cell sample_size. Implemented as a `_head` override
  in FieldBoard (the river.py subclass precedent).
- D3 serve-cap shape: list arm's 4/tick is conditional (burst primes at
  crest); field arm's is a flat pipe cap 4. Same total, different shape,
  logged.
- D4 wasted-dispatch counting: list arm counts at arrival time (its
  dispatches ARE the replayed historical sends); field arm counts at
  service time (the coordinate the gate drew from, after terrain routing).
- D5 fish-layer floats: water/ledger/gate layers are integer-only; the boid
  layer rides the game organ's own float constants (LM9), determinism
  verified by same-machine double run.

Artifacts: `tools/field_experiment.py` (the instrument, rerunnable),
`FIELD2_BOARD_SPEC.json`, `FIELD2_SEAT_LIST.md`, `FIELD2_ARMS_BLIND.md`,
`field2-judge-kimi.md`, `field2-judge-deepseek.md`, ask staging under
`memory/plans/field2_judges/`. No commits; the sim is $0; only the two
judge turns spent ($0.0017).

Filed by lane FIELD-2 seat, 2026-10-01. No em-dashes.
