# STEERING FIELD THEORY - FIELD-1 (THE TRIANGULATION MINE), 2026-10-01

**Schema:** steering_field.theory.v1 · **lane:** FIELD-1 · **method:** bytes-first (every claim below names the file it was read from this session; no production code, no commits, $0 spend) · **web:** one Anthropic-interpretability grounding pass (sec 6).

**Mission (operator):** verify or refute the triangulation "STEERING THE SWARM = SOLVING A FLOW PROBLEM IN CONCEPT SPACE" against real estate bytes, make it falsifiable, and name the smallest experiment that proves or kills "field steering beats list steering".

---

## 0. The one-line theory (stated precisely)

The estate's steering organs are already a discrete potential-flow machine: the GPS ledger and law rows are TERRAIN (integer elevation), sealed steer envelopes and operator-placed food are IMPULSES (bounded pours onto the terrain), boid families are the ADVECTING MEDIUM (flock terms move belief mass down the dHead gradient), the watershed Jacobi tick is the RELAXATION KERNEL (flow = dHead*conductance >> 8, quiescence when the dirty set empties), and the walked paths carve the terrain for the next tick (river.py silt + GPS momentum = pheromone). Steering is not issuing a sequence of commands down a queue; it is setting boundary conditions (elevations, sills, crests, sealed pours) and letting the field relax. The bytes for every one of those five clauses exist; what does NOT exist anywhere yet is the single loop that couples them, and one clause (the quasicrystal) is a reading, not a mechanism.

---

## 1. THE TRIANGULATION - linkage by linkage, against bytes

Fourteen linkages tested. 9 VERIFIED, 3 PARTIAL, 2 REFUTED.

### L1. "Models = particles in a k-space" - VERIFIED (estate bytes; Anthropic caveat in sec 6)

- `mag/flock_field.py` docstring, verbatim: "Agents = particles in a scalar 'distance-to-solution' field phi over invariant space. Each agent steers by the geometric gradient -grad(phi) ... plus classic boid terms (separation / alignment / cohesion)". "The field IS the coordination (no central orchestrator)."
- `mag/flock_scheduler.py` embeds each task into that space, preferring local Ollama semantic embeddings "so that distance in invariant space MEANS semantic overlap, not hash-distance ... RIB distance must be meaning, not hash."
- `mag/water_swarm.py` (operator order 2026-08-12): "instruct our swarms to be our water flowing and forming around invariants before we can detect them ... the swarm is the WATER that flows around it." The particle reading is the operator's own prior art, already an organ (water_swarm.v1: invariant_lattice() + water_doctrine() + flow()).

### L2. "GPS accumulated signal = hydraulic head / potential terrain" - PARTIAL

Both halves exist separately and one directed feed exists; no organ elevates terrain BY accumulated signal.

- The accumulator: `tools/gps_mcp/ledger.py` (SQLite, pass_rate per (model_id, task_shape), momentum badges RISING/STEADY/DECLINING, streaks, positive floor), positive arm landed as LM7 (`watch/inbox/last_mile_20260930/LM7_POSITIVE_GPS.md`; README section "The positive arm (LM7)"). Feed path in: `mag/gwap_to_gps.py` (fail-closed verdict bridge).
- The head law: `mag/hydrology.py` head = elev*256 + depth (Q8 + milli-depth); `mag/field_flow.py` same constants on a 2D grid.
- The one existing coupling: `tools/k8s_water_sim.py` docstring, "Workload feed: tools/gps_mcp/gps_ledger.db3 verdict_log (real routing receipts) -> arrivals schedule; verdict=0 rows seed the waste basin as already-shed work awaiting escalation", tested by `tests/test_k8s_water.py::test_ledger_workload_feeds_simulator`. That is ledger VOLUME into the graph, not ledger SIGNAL into ELEVATION. The "accumulated pass_rate raises the terrain" coupling is the theory's own proposal (sec 3).
- Sibling organ that already does signal-as-potential in a different physics: `mag/frontier_gravity.py` (active-inference steal: preferred-state vector C, "the agent does not follow commands - it minimizes expected free energy"; gravity distance as free-energy proxy). Potential terrain exists; the GPS-to-elevation wire does not.

### L3a. "Sealed steering envelopes = bounded impulses" - VERIFIED (as physics shape)

- `mag/steer_seal.py` (A1, 2026-10-01): HMAC-SHA256 envelope, nonce replay guard, 300s freshness window, restrictive-word safe-fail. An envelope is exactly an impulse in the control sense: instantaneous, bounded, timestamped, admitted through a gate, and it either redirects the next turn or is inert.
- Measured impulse response, `watch/inbox/model_garden/STEERING_DOGFOOD.md` (X5): kimi-k2 obeyed the sealed envelope 4/4 substantive checks; glm-5.3-flash ignored it wholesale at reasoning_effort low. One impulse, two media, opposite response: the impulse model of steering is only as good as the medium's conductivity, which is a measured property, not an assumption.
- Placement-time impulses (the positive form): `mag/flock_positive_ab.py`/`mag/flock_positive.py` (LM9): the operator places FOOD at the target (a pour), never chases the school (a pressure). The A/B harness measures lure-vs-threat with t80_seconds and panic_entries.

### L3b. "The Dirac bank is impulse accounting" - REFUTED

`grep -ril "dirac"` lands on `mag/dirac_loop.py`, `tools/dirac_loop_shim.py`, `mag/water_computer.py` (which references "dirac loop 6" as a chain edge), and the ledger `watch/inbox/DIRAC_BANKED_INVARIANTS.jsonl`. What it actually is: graph HOMOLOGY. `mag/dirac_loop.py` docstring: "A DIRAC LOOP = an independent cycle in the knowledge graph" via fundamental cycle basis, "beta1 = m - n + c (first BETTI number)", "Discrete Dirac / graph Laplacian: the kernel = number of connected components"; the bank records loop INVARIANTS with receipts ("bank one loop's holonomy ... the tesuji act - verify-without-replay"). "Dirac" here is the discrete Dirac operator, not the delta distribution; the bank banks closed loops, not impulse magnitudes. The impulse role in the estate is carried by steer_seal (L3a) and pheromone drops (L4), so the synthesis survives, but the NAME belongs to homology. Any doc that says "Dirac impulse" must say "sealed-envelope impulse" instead.

### L4. "Pheromone trails = stigmergic deposition" - VERIFIED

- `mag/swarm_tools.py` line 15: "SWARM_PHEROMONE (moonshot) - STIGMERGY: drop/read content-addressed pheromone marks", `pheromone_drop()`/`pheromone_trail()`: "the trail outlives this NPC (content-addressed, replayable)".
- Dogfood: `watch/inbox/model_garden/steerx5-pheromone-kimi.md` (pheromone organ probed live).
- Numeric pheromone: `watch/inbox/model_garden/OVERMIND_THEORY.md` sec 3: "This is pheromone made numeric: instead of a scent trail, a (coordinate, momentum) table the router already sorts by."
- GDScript twin carries the visual form: `roblox_to_godot/systems/flock.gd` line 3-4: "Boids: flee/tire/rest, school cohesion+separation+wiggle, pheromone trail ... trail 38" (and `mag/flock_positive.py` documents trail_steer() as never called inside step(): today the trail is decorative, which is exactly the gap the momentum table fills).

### L5. "Flocking rules = advection; alignment = shared law rows, separation = blind-spot diversity, cohesion = convergence" - VERIFIED (one gloss delta)

`mag/flock_scheduler.py` docstring, verbatim: "SEPARATION pushes overlapping tasks apart (the DEDUPE - replaces the central same-goal guard), ALIGNMENT keeps them on the distilled-invariants policy, COHESION clusters true duplicates." So: alignment = policy/law rows EXACT; cohesion = convergence on true duplicates (terrain convergence by mechanism, duplicates by bytes); separation = dedupe in bytes, "blind-spot diversity" is the operator's gloss (dedupe reduces duplicated coverage, which is the budget half of blind spots; the exploration half is carried instead by LM9's satiation-gated explore: `mag/flock_positive.py` "hungry fish exploit the gradient, satiated fish explore"). Advection itself is `mag/flock_field.py` steer() + step(): force = -w_goal*grad(phi) + w_sep*sep + w_ali*ali + w_coh*coh, integrated data-parallel.

### L6. "Watershed dHead fixed-point iteration = belief-relaxation kernel" - VERIFIED

- `mag/hydrology.py` (rung 1): "flow = (dHead * conductance) >> 8" in Q8 fixed point; filling a pool RAISES its head (backwater, equalization).
- `mag/field_flow.py` (rung 2): "One Jacobi tick: all flows are computed from the START-of-tick volumes", dirty-block activation, `settled()` = "no cell is active", exactness proof against tick(full=True).
- The estate NAME for it, `tools/rule_parity.py`: "the fixed-point dHead law where boolean verdict physics and the Watershed part ways". It is already a named law under test in the parity harness.
- "Belief" is gloss, but grounded gloss: `watch/inbox/water_engineering_20260930/WF_SYNTHESIS.md` rules the base engine "a logic circuit in a wetsuit ... verdict physics, not fluid physics"; the water graph's nodes ARE verdicts (who delivered), so relaxing heads is relaxing a verdict field.

### L7. "Water computer (XOR maze, integer fixed point) = computation as attention flow through law-terrain" - VERIFIED

- `mag/water_graph.py`: xor junction "delivers only when EXACTLY one inlet delivered this tick (both inlets -> overflow to waste - the hydraulic XOR)"; sill = hydraulic AND; any = OR; check valves; siphon crests; AC2/B1 fracture; R8 int64 saturation. The XOR engine proper: `mag/hydro_xor_sim.py` (two-bucket pulsed XOR, falsifier contract C18_HYDRAULIC_THIRD_CHANNEL.md).
- `mag/water_computer.py`: graph mode + proof anchoring, claim string "the water computer computed its route to OUT by gravity", hash-pinned through verkle_knot ("dirac loop 6" chain edge).
- The scheduling reading already executed: `tools/k8s_water_sim.py`: "kube's priority plugin = valves; gravity + caps dispatch - the operator lens: the AI sets elevations, sills and crests, physics moves." That sentence is the field-solver claim, already in bytes, already running.
- "Attention flow" is gloss; the mechanism (computation = relaxation over law-gated terrain) is verified.

### L8. "HVAC: the airflow tester absorption" - VERIFIED

`watch/inbox/water_engineering_20260930/WA_HVAC_ARCHAEOLOGY.md`: airflow_home.html ("the house is the prompt", well-mixed zone model, conserved smoke particles) was never killed, "it was ABSORBED" into `dashboard/static/games/maze_arena.html` (`__fluidTick`, "HVAC SELF-STEAL (airflow_home): smoke is stuff, not pixels - conserved work per island"), receipt `watch/inbox/FLUID_LENS_MANIFEST_20260913.md`. The meter's oldest game-shaped ancestor is a conserved-flow attention model.

### L9. "The law lattice = QUASICRYSTAL" - PARTIAL (reading, not mechanism; priors exist)

- `grep -ril "quasicrystal|penrose|aperiodic"` over estate code/docs finds NO organ and NO doctrine using the word. The hits are priors: `watch/INTAKE_Math_files_einstein_hat_tile_20260904.md` (aperiodic monotile intake; verdict REMEMBER; "FLEET HOOK - none live. Distant rhyme only: shadow-fields arc cares about aperiodic/non-repeating fields (maze_arena GPU field); if a tiling generator ever feeds maze_arena, the hat/spectre family is the shelf pointer. Not a builder today."); `watch/inbox/physical_computing/receipts/G-F_SPINOR_LATTICE.md` (belt-trick 720-degree lattice, spinor double-cover as channel topology - a DIFFERENT lattice dream, unbuilt); plus noise (library fiction, shadertoys).
- The two ingredients each exist separately: local tiles that never repeat centrally (law rows, organ flags, per-seat RIBs; no master table governs all seats per tick) and long-range order without central repetition (the verkle chain: each leaf commits to the previous; global consistency carried by purely local rules - `memory/steal/VERKLE_KNOT_STANDING_WAVE_RENDER_20260915/...` family of receipts renders exactly this). What the quasicrystal frame ADDS is in sec 4.

### L10. "Overmind = FIELD SOLVER not scheduler" - PARTIAL (it contradicts the standing sibling theory in one precise way)

`watch/inbox/model_garden/OVERMIND_THEORY.md` (OVERMIND-1, same day, the moonshot theory mine) concludes the overmind is "the pacing signal of the estate's standing wave ... neither creates nor deletes - only ROUTES", executed as a discrete tick (SENSE/ORIENT/DECIDE/STAGE/AUTHORIZE/LEDGER) over a frozen verb table: a scheduler UNDER law, with field-flavored inputs (GPS coordinates, momentum routing). The operator's new frame upgrades this: do not tick-decide at all; set boundary conditions and let the flock relax. The bytes support BOTH: the verb table exists (`tools/mountain_liquids.py` LM3 for the Mountain; OVERMIND_THEORY gap 2 says the ESTATE verb table does not exist), and the no-central-orchestrator field exists (`mag/flock_field.py`, `mag/flock_scheduler.py` "THE TESUJI: the swarm allocates work EMERGENTLY instead of through the serial queue"). Which frame wins is exactly what sec 3's experiment decides. Notable: OVERMIND_THEORY already prices the loop at $0.05-0.15/hour and specs the decision-duel judgment (blind seat list, >= 60% agreement falsifier) that the experiment below reuses.

### L11. "The standing wave is the same object as the fixed point" - REFUTED (they are duals)

- Standing wave, `watch/STANDING_WAVE_DOCTRINE_20260905.md`: "the rows are the traveling wave, the schema/laws are the standing pattern"; requires rank >= 2 (two counter-propagating waves, interference), driven-dissipation balance (EMIT/GATE vs DISSIPATE/GROUND), a medium that holds the pattern (the sealed chain). It is a PERSISTENT OSCILLATION: the estate's metabolism.
- Fixed point, `mag/field_flow.py` `settled()` / `run(stop_on_settle=True)`: the QUIESCENT TERMINAL STATE of one relaxation (empty dirty set, zero wetted meter).
- They cannot be the same object: the standing wave is nonzero motion with an invariant pattern; the fixed point is zero motion. The correct relation is DUAL: the fixed point is the instantaneous stillness the standing wave approaches and never fully reaches; the frozen-clock law ("no movement, no transitions, no receipts born") and the Still World epoch (OVERMIND_THEORY: "a tick that stages zero verbs and says why is a GOOD tick") are the two frames looking at the same quiescence from opposite sides. Citation note: OVERMIND_THEORY cites "ASTRA_PROMPT_STANDING_WAVE_20260907.md", which does not exist on disk; the real artifacts are `watch/STANDING_WAVE_DOCTRINE_20260905.md` and `watch/FRONTIER_ASK_STANDING_WAVE_20260907.md` (a standing citation drift this lane files, not repeats).

### L12. "Particles / curl rings" - VERIFIED

`roblox_to_godot/systems/water_particles.gd` (Watershed rung 3): droplets with position+velocity riding the field, read-only over the integer graph; "XOR gates - junction events ... spawn curl rings: tangential velocity amp * exp(-dist / CURL_FALLOFF)"; zero RNG (hash-driven phases). Curl also appears as the maze flood's handedness: `dashboard/static/games/maze_arena.html` ("ODD eta adds a handed curl to the flood (swirl: one way round is cheaper - geodesics bend, reachable sets go handed)").

### L13. "The water line (the ladder)" - VERIFIED, rungs 1-4 all landed

Rung 1 graded head (`mag/hydrology.py`), rung 2 dirty-block sheet flow (`mag/field_flow.py`), rung 3 particles+curl (`water_particles.gd`), rung 4 erosion/silt/meander (`mag/river.py`: "SILT: a second integer per cell ... the mountain remembers"), terrain bridge (`tools/dem_to_board.py`, SRTM .hgt -> 64x64 integer board), parity harnesses (`tools/rule_parity.py` water + `tools/flock_parity.py` flock), and the whole ladder's spec `watch/inbox/water_engineering_20260930/WF_SYNTHESIS.md`. Plus `mag/water_swarm.py` (L1): the swarm-as-water doctrine organ.

---

## 2. THE MATH SHAPE - the update rule in water-computer terms

State = belief field over surfaces; each tick: advect by flock rules toward the GPS gradient, apply impulses, relax by fixed point, deposit pheromones. Written against the estate's integer fixed-point idiom (no floats, no RNG, no clocks; Q8 head; >> 8 conductance; dirty-block activation; conservation audited):

```python
# STATE (all integers; the estate idiom: mag/field_flow.py + mag/river.py + tools/gps_mcp/ledger.py)
elev[Y][X]            # terrain 0-255 (seeded from GPS: pass_rate -> elevation, see EXPERIMENT)
vol[Y][X]             # belief mass = attention allocated to that (surface, coordinate) cell
silt[Y][X]            # pheromone deposit (river.py's second integer; conserved, never created)
waste                 # outlet set (starved work; boil() is the escalation path, nothing deleted)
dirty                 # insertion-ordered set of active cells (the wetted meter)

# HEAD (hydrology.py law, verbatim constants)
head(c)        = elev[c]*256 + vol[c]*1000 // cross_section[c]
# cross_section[c] = GPS sample_size at that coordinate: wide evidence = wide tank
# = MORE signal needed to raise the head one unit (a 3-verdict coordinate is a narrow
# tank that spikes; a 300-verdict coordinate is a lake that barely moves). The
# anti-recency bias falls out of the geometry; it is not a guard branch.

# ONE TICK (one overmind tick = one Jacobi relaxation with advection and impulses)
def tick():
    # 1. IMPULSE (sealed pours only; mag/steer_seal.py + LM9 food placement)
    for env in admitted_envelopes():            # admit_text() -> verified payload
        add_water(cell(env.coordinate), env.mass)   # bounded, nonce-guarded, timestamped
        dirty.mark(cell(env.coordinate))            # an impulse is just a directed pour
    # (threat-form impulses are measured disease: flock_positive_ab's "standoff" arm
    #  deadlocks and panic FREEZES the school; LM9: place food, never chase.)

    # 2. ADVECT + RELAX (field_flow.tick, one Jacobi pass over the dirty set)
    #    cohesion = pour to EVERY strictly-lower head (flow = dHead*conductance >> 8,
    #    scaled down when wants exceed volume) -> convergence down the GPS gradient
    #    alignment = the shared law layer: junction gates (xor/sill/any) decide which
    #    pours the LAW counts as delivered this tick (water_graph verdict physics)
    #    separation = surface-tension floor: dHead below 256//conductance rounds to
    #    zero, so near-tied coordinates do not oscillate (the dedupe)
    for c in list(dirty):                       # only active cells; quiescence costs 0
        pour_to_lower_heads(c)                  # start-of-tick snapshot (Jacobi law)
    commit_outs_then_ins()

    # 3. SETTLE OR HOLD (the fixed point is honest, not assumed)
    if not dirty:                               # field_flow.settled()
        emit STILL_WORLD(reason)                # a NOOP with a reason is a legal tick
        return

    # 4. ERODE / DEPOSIT (river.py sill law + GPS momentum = stigmergy)
    for c in cells_with_throughput_above_sill():
        c.elev -= 1; c.silt -= 1                # rising coordinates CARVE channels:
        lowest_neighbor(c).silt += 1            # next tick's gradient is steeper there
        lowest_neighbor(c).elev += 1            # (the walked path becomes the terrain)
    # GPS record_verdict() on the tick's outcomes moves momentum; momentum NEVER
    # edits verdict_log (LM7 law: ground truth is never steered).

# READ (what the dispatcher consumes): the settled field's flow lines are where
# attention drained this tick; waste basins are starved work awaiting boil()
# escalation; mean head over a surface is its accumulated signal (L2's proposal).
```

Why this is the estate's idiom and not new physics: every operator above is an existing law (add_water, the Jacobi tick, the dirty set, the sill law, boil-escalation, the momentum tiebreak). The single NEW wire is `cross_section = sample_size` and `elev seeded from pass_rate`, which is the L2 coupling the estate has never landed.

---

## 3. THE FALSIFIABLE MINIMAL EXPERIMENT - "field steering beats list steering"

**Claim to kill or prove:** allocating the day's work by relaxing a GPS-elevated integer field with boid-family advection beats the current driver's sequential queue, at equal-or-lower cost, judged on real outcomes.

**Assembly (six existing organs, one new adapter, zero new physics):**

| Piece | Organ (bytes) | Role |
|---|---|---|
| Task stream | `tools/gps_mcp/gps_ledger.db3` verdict_log via `tools/k8s_water_sim.py`'s existing feed (tested by `tests/test_k8s_water.py::test_ledger_workload_feeds_simulator`) | real arrivals schedule; verdict=0 rows = shed work |
| FIELD arm kernel | `mag/field_flow.py` (+ `mag/hydrology.py` head law) | the relaxation |
| Advection law | `mag/flock_positive.py` step_positive (flock.gd constants, parse-checked by `tests/test_flock_positive.py`) | boid families graze food at target coordinates; satiation explore/exploit |
| Impulse organ | `mag/steer_seal.py` seal/admit | operator pours, sealed |
| LIST arm (control) | `tools/k8s_water_sim.py`'s own scheduler: "the scheduler loop opens ONE class lane per tick ... highest class with work first" | the sequential queue, byte-honest |
| Judgment | `mag/flock_positive_ab.py` metric grammar (t80, panic_entries) + OVERMIND_THEORY sec 6 decision-duel (blind seat list, two judges, >= 60% agreement falsifier) | scoring |

**Design.** One replayed ledger day (the verdict_log tail, same rows both arms; determinism law: same inputs, byte-identical reruns).

- LIST arm: run the k8s water scheduler exactly as shipped (one lane per tick, priority ladder).
- FIELD arm: same arrivals poured onto a `field_flow` board where each (task_shape) coordinate's elev = pass_rate scaled 0-255 and cross_section = sample_size; families = model families (`step_positive`, one school per family); the ONLY interventions are sealed pours at placement time (LM9 law: lure, never chase); gates = the water_graph law rows for junction decisions; river.py sill erosion ON (walked paths steepen).
- The one new adapter (the L2 wire): a ~40-line elevation-seeder from the ledger into the board spec, plus the comparison report.

**Metrics (pre-registered):**
1. ticks-to-80%-drained (the t80 transplant: first tick with >= 80% of arrived work either served or honestly shed-with-reason);
2. wasted dispatches (work sent to coordinates where the ledger already says DECLINING - each is a dollar leak);
3. decision-agreement vs the blind seat list (the OVERMIND_THEORY sec 6 duel: a kimi-class relay judge + one blind second family; disagreement filed, never flattened);
4. dollar spend (hard cap $1.00, checked before every dispatch - the model_garden rail's own law).

**Falsifiers (any one kills the claim at this scale):**
- FIELD arm loses on ticks-to-80% AND on wasted dispatches (a win must show on at least one outcome axis, else "field" is theater);
- decision-agreement < 60% (the seat's queue judgment beats the field: the substrate is wrong, kill or swap substrate per OVERMIND_THEORY);
- any mid-task envelope redirect of a running glm turn (STEERING_DOGFOOD: it will not take; routing bug);
- conservation violated (volume or silt unbalanced: the relaxation is lying);
- spend > $1.

**Budget:** the sim is integer Python, $0, stdlib, minutes of wall clock. Only the judgment turns cost: the steerx5 shape (3 kimi-relay turns on prepaid Nous credits + ~$0.0002 glm metered) prices the whole judgment leg under $0.01. Total experiment cost: under $0.05 worst case, $0 if judges are folded into the next already-planned duel. Success graduates it to the OVERMIND_THEORY daily-cadence shape with the GPS rows it traveled getting momentum entries.

---

## 4. WHAT THE QUASICRYSTAL READING ADDS (and what it does not)

Adds one testable invariance and one design warning; adds no mechanism.

- The invariance: in a quasicrystal, local matching rules produce long-range order with NO central repetition cell. The estate's law layer already behaves this way (law rows + chain; no master table all seats re-read per tick). The reading PREDICTS: adding a law row must never require re-synchronizing distant rows (long-range order is cheap); if the estate ever needs a global re-sync to stay consistent, the quasicrystal reading dies. That is a real falsifier, cheaper than any sim: it is a property to check, not to build.
- The warning: aperiodicity has a known failure mode (phason strain - local rule violations that propagate long-range disorder). Estate translation: a seat that ignores law rows (glm-flash's steering-inertness, STEERING_DOGFOOD) is a phason; a few are survivable, a population of them unravels the pattern rather than degrading it politely. The standing-wave doctrine already says this in its own words ("a disturbed standing wave doesn't diminish - it UNRAVELS"). The quasicrystal frame and the standing-wave doctrine agree on the failure mode; that convergence is evidence the frame is load-bearing, not decorative.
- What it does NOT add: a builder. The hat-tile intake already ruled "not a builder today" (`watch/INTAKE_Math_files_einstein_hat_tile_20260904.md`), and nothing mined this session upgrades that verdict. No tiling generator, no Penrose organ, none needed: the chain already provides the long-range order the reading wants.

---

## 5. THE ALMOST-TOUCHING (estate receipts that already built pieces of this)

1. `mag/water_swarm.py` (2026-08-12, operator order): "instruct our swarms to BE WATER ... flowing and forming around invariants before we can detect them." The field theory in one sentence, already an organ, never coupled to the GPS ledger. This is the closest prior art; the operator suspected right.
2. `mag/flock_field.py` + `mag/flock_scheduler.py`: particles-in-field with all three boid terms and "the field IS the coordination ... replaces the central same-goal guard", including the serial-queue-replacement TESUJI - built as demo/scheduler, never measured against the queue on real ledger data.
3. `tools/k8s_water_sim.py` + its test: the GPS ledger already pours into the water graph as arrivals. One adapter short of the experiment (elevations from pass_rate, not just PriorityClass).
4. `dashboard/static/games/maze_arena.html`: GPS agents already walk a deterministic distance-field gradient and race random-walkers, with a handed curl and the R4 "STAYING IS THE WIN" dwell scoring - field-vs-list steering's game-shaped ancestor, judged in-browser.
5. `watch/inbox/model_garden/OVERMIND_THEORY.md` sec 6: the decision-duel judgment shape, the $1 cap, the 60% agreement falsifier - specced the same day for the overmind moonshot; this experiment reuses it verbatim.
6. `mag/flock_positive_ab.py` (LM9): threat-vs-positive A/B with t80/panic metrics - the measurement grammar, live.

Net: the experiment is an ASSEMBLY, not an invention. The only unwritten line is the ledger-to-elevation adapter.

---

## 6. ANTHROPIC'S K-SPACE, HONESTLY (what their feature space IS, so the analogy stays precise)

In Anthropic's interpretability line (Scaling Monosemanticity, Transformer Circuits 2024; the feature-steering bias studies), the "space" is the residual stream of ONE model: activations decomposed by sparse autoencoders into millions of sparse, roughly monosemantic feature DIRECTIONS (superposition/polysemanticity is the problem SAEs attack). "Steering" there means adding a feature's direction vector (or a contrastive steering vector) to activations at inference to bias generation toward or away from a trait - no retraining, same weights. So the honest mapping is: Anthropic steers a point inside one model's activation space along interpretable directions; the estate steers a probability mass of models across a task/coordinate space whose "directions" are law rows and whose "activations" are ledger rows and receipts. The two share the FLOW structure (state = position in a space; steering = bounded additive perturbation; behavior = where the state drifts), and the estate even has the measured conductivity caveat Anthropic also reports (steering works on some media and not others: kimi 4/4, glm 0/4). But they are different spaces: the analogy is precise as "perturbation of a distributed state," not as "the same k-space." Sources: transformer-circuits.pub/2024/scaling-monosemanticity; anthropic.com/research/evaluating-feature-steering; arXiv 2411.08790 (the Oxford caveat that SAEs can misread steering vectors).

---

## 7. THEORY-LEVEL FALSIFIERS (what would kill the whole frame, not just the experiment)

1. If the LIST arm wins the duel cleanly (faster drain, fewer wasted dispatches, cheaper), then at estate scale sequential law-governed scheduling beats relaxation and the field theory is aesthetic.
2. If impulse conductivity cannot be predicted per family in advance (STEERING_DOGFOOD showed a 2-family split; if it stays unexplainable across the grid), the boundary-condition framing loses its actuator.
3. If the L2 wire (sample_size as cross_section) produces degenerate terrain (one narrow-tank coordinate hoards all attention), the head law is the wrong accumulator and the GPS should stay tabular.

Filed by lane FIELD-1 seat, 2026-10-01. Theory + mine only: no code, no commits, $0 spend, no em-dashes.
