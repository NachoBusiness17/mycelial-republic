# Receipt: mariner mission 20261016 (cycle 10, complete)

Mate: THE MARINER. Pack: logs/mates/missions/mission_20261016_07_mariner.md
(claimed via its .claim sidecar, OPEN line appended 08:24:56, cycle 10;
CLOSED line appended at window close). Launch stub was filed in this file
before any speech, per contract, and rewritten here at window close.

Status: COMPLETE at a cycle boundary, not context death. The cycle-9
next-thread THE THERMOSTAT is landed as six pins in one new test file,
the standing skyrmion seed (the vortex line) has stood as pins since
cycles 3-7, and the next thread is named below.

Laws held: em-dash 0 in my bytes (the new test file, the docstring
block in mag/water_graph.py, the mirror block in the Godot twin, this
receipt: all 0; the files' pre-existing em-dashes in untouched
cycle 1-9 bytes are not my diffs), real counts only, no fabricated
anything, no env dumps, RAM gate respected (in-memory boards, largest
5 nodes), rolling concurrency respected (peak 1 process), receipt
before speech, positive steering (one probe-board design dead end and
four pin bugs recorded and fixed, no spiral), drop-ledger awareness
(searchable terms: water_graph thermostat closed weather loop
recirculation governor wheel prime serve law momentum tick birth state
park setpoint sill draw sleeps charged half prime restart phase sense
leg wheel rate surplus pools crown sky spends itself last rain charges
latch crown drain residual g hysteresis floor lap pipe order recirculated
unit conservation), COMPUTE LADDER honored per the STEER row: all work
local on this account, zero paid API calls, Nous/Hermes untouched, no
Task agents needed (single-seat probe-and-pin work).

## FINDINGS

1. THE PRIME (probe round 1 dead end, pinned as law): a governor
   wheel (waste basin, cold crown, a latch L, a crown->L sense leg,
   an L->waste return leg) starts only on an UNCONDITIONED first
   act. A serve loop that waits for a "Latch L opens" line before
   the first shovel never starts: the latch has no inflow until
   something lifts (pinned: 3 ticks, zero events; then the prime
   fires the full four-line wheel). The round-1 boards W/W2/S2 were
   built exactly wrong this way; the boards died, the law lives in
   the pin. Test: test_a_governor_starts_only_on_an_unconditioned_
   prime.

2. THE SERVE LAW and THE BIRTH-STATE PARK: after the prime, serving
   one shovel per open line runs the wheel at one four-line tick per
   act (condense +1 / "cl: 1 crown->L." / "Latch L opens (pool 1 >=
   level 1)." / "ol: 1 to waste at waste."), shovels == opens ==
   turns == 6 (prime plus 5 served, t1-t6 opens), the sump rides
   [B-1, B] = [2, 3] on B=3, and total mass never leaves 3: the
   steady state HOLDS A LEVEL and spends acts, not water. Stop
   serving and the wheel turns one MOMENTUM tick more (t6: the
   in-flight steam still rotates the loop once) then parks silent
   and byte-stable at the birth state (waste 3, crown 0, L 0).
   Test: test_the_serve_law_holds_the_sump_and_parks_at_the_birth_
   state.

3. THE SETPOINT and THE SLEEPING PHASE: the latch's sill is the
   thermostat's dial. Sill 2 (prime 2) starts one tick later (t1:
   condense +2 then a HOLD at pool 1 while the crown buffers the
   second unit), rides the sump at [1, 2] instead of [2, 3]: each
   sill notch drinks the sump one unit lower. The park SLEEPS
   CHARGED (waste 2, crown 0, L 1: pool = sill - 1, the memory law
   at rest), and a HALF prime (the missing residual, 1 unit)
   restarts the wheel at full period on the very next tick: the
   residual IS the phase. Total 3 at every tick. Test:
   test_the_sill_sets_the_draw_and_the_park_sleeps_charged.

4. THE WHEEL RATE IS THE SENSE LEG: over-shoveling (batch 2 per
   open, B=5) does not speed the wheel: the cap-1 sense leg keeps
   the turns at one per tick, the surplus pools at the cold crown
   (1->2->3->4 over t1-t4, the free buffer), the sump drains
   5->4->3->2->1->0 (post-tick) and at sump 0 the serve degrades to
   one shovel per open: the circuit converges to the honest wheel
   (shovel 1 == return 1: pure recirculation through an empty sump,
   t5-t6). After the serve dies the wheel keeps turning on the
   crown's stock with zero condense lines: t8-t11, FOUR momentum
   ticks for FOUR stored units (one tick per stored unit: the sky
   is a windable delay line), then t12-t13 silent, and the final
   state is the birth state (waste 5, crown 0, L 0): the sky spends
   itself last and the over-shoveled board loses nothing. Total 5
   at every tick. Condense counts trace the shovel rate exactly
   (+2 while the batch holds, +1 once the sump degrades the serve).
   Test: test_the_wheel_rate_is_the_sense_leg_and_the_sky_spends_
   itself_last.

5. RAIN CHARGES THE LATCH (cycle-7 residual g, CLOSED): a cold
   crown placed ABOVE a level-2 latch feeds it through its drain.
   One batch lift of 3: t1 all 3 condense at the crown (the latch
   is not cold: the sky never lands in it directly), the crown's
   drain probes the gate deferred, the latch HOLDS pool 1 (the held
   inlet gets no provenance line: the cycle-3 residual, still
   open); t2-t3 one drain unit each, open at pool 2 and discharge 1
   each; t4-t5 silent at residual 1 (the level-minus-1 hysteresis
   floor). End: basin 0, crown 0, L 1, lsnk 2, conserved 3. Test:
   test_rain_charges_the_latch_through_a_crown_drain.

6. THE LAP IS PIPE ORDER: the recirculation lap (receiver -> drain
   -> waste -> shovel -> crown -> receiver) costs one act per lap
   either way, and the tick count is set by pipe insertion order:
   crown leg created before the drain leg: the rider lands and
   chains straight to waste in ONE tick (the steady lap; the
   seeded rider's first drain is the only standalone tick). Drain
   leg created first (same topology, one dict order apart): the
   rider RESTS at the receiver one tick: the lap is TWO ticks and
   the waste oscillates 1/0. Both boards conserve 1 at every
   boundary. The loop's cadence is clock wiring, not physics (the
   cycle-9 phase-flip law, now pinned on the loop). Test:
   test_the_recirculation_lap_is_pipe_order.

7. Residuals carried forward: (a) Godot parity EXECUTION remains
   blocked: no godot or godot4 binary on this box (re-checked
   11:38:30 this window); the twin's mirror is landed line-for-line
   through the cycle-10 block and the Python suite stays the
   executable pin. (b) Held-inlet per-pipe provenance lines
   (cycle-3 residual) skipped again, named in the rain-latch pin's
   docstring. (c) The R8 named residual (hydrology._move adds raw
   instead of _receive) remains, untouched. (d) The consumer
   sweep's 18 reds are named in COUNTS, all in files whose mtimes
   predate my window (test files 2026-09-29 to 2026-10-01, source
   files to 2026-10-10): sibling-lane drift, not mine; 4 of the 18
   are new to any mariner receipt (test_env_contract 1,
   test_mcp_bridge_r1 1, test_parity_gate_hook_pin 2), the other
   14 were carried by cycles 3-9. (e) Ratchet NEW=1:
   tools/hermes_burn.py:98 env-key-read HERMES_BURN_API_BASE, a
   SIBLING lane's mid-window edit (file mtime 08:54:58, inside my
   window; the DRY-amendment repoint): not my file, not my debt,
   NOT accepted by me; the owning lane must register or fix it
   before its next push. (f) The ratchet GROWTH advisory on
   mag/water_graph.py (accepted at 465, now 762) rides cycle 3's
   registered claim per cycle 9's receipt; the operator re-audits
   at push; my share of the growth is +52 docstring lines.
   (g) The cycle-9 ride-along (a campaign-side windowed signed
   reader speaking "wheel A leads" at a mid-window tick) remains
   named, not built: scope.

## JOURNEY

1. Boot and claim: read the pack; read cycle 9's full receipt and
   the 10-15/10-13 sidecars for the claim grammar; read the three
   keystone files in full (mag/water_graph.py 710 lines at window
   open, mag/water_computer.py, server/world.py) and the cycle-9
   test file for pin grammar; verified by git status and mtimes
   that no sibling held water bytes (tree exactly as cycle 9 left
   it); appended the OPEN line at 08:24:56; filed this receipt's
   stub before any speech.
2. Thread intake: cycle 9's NEXT THREAD is THE THERMOSTAT in three
   named parts (a recirculation cost, b rain-latch composition,
   c self-regulating loop). Built probe round 1 (one temp script,
   single process, in-memory, boards of 3-4 nodes).
3. Probe round 1: the recirculation board R traced clean and
   FALSIFIED my two-tick lap sketch (the +0 chain makes the steady
   lap ONE tick). The rain-latch boards B and B3 traced clean
   (part b landed on the first round). But the three governor
   boards W/W2/S2 never started: 9 empty ticks on each. Why: I
   wired the operator to serve on opens, and the latch cannot open
   before the first lift. Dead end (my board design): the round-2
   boards got the PRIME.
4. Probe round 2 (same discipline): prime-then-serve boards traced
   clean: W1 gave the serve law, the momentum tick and the
   birth-state park; S2 gave the setpoint, the sleeping phase and
   the half-prime restart; W2 gave the sense-leg rate cap, the
   crown pool and the honest-wheel convergence; R3 gave the +1
   loop (two-tick lap).
5. Probe round 3: W2's tail to full park: four momentum ticks for
   four stored units, silent park at the birth state, total 5
   throughout: the sky-spends-itself-last law pinned from real
   bytes.
6. Spec-first: wrote THE THERMOSTAT block into the module docstring
   (six laws, real numbers) BEFORE any test landed; mirrored the
   block into the twin's header (parity law from cycles 3-9).
   Engine behavior changed by zero bytes all window.
7. Landed tests/test_water_graph_thermostat.py, 6 pins, 283 lines.
   Dead ends caught by the runs (my pin bugs, the cycle 4/5/7/9
   class): (a) the W2 wants table smoothed the probe's +2 condense
   lines into a +1 constant (the batch serve lifts 2/tick: the
   trace said +2 at t1-t4 all along); fixed from the probe bytes;
   (b) the S2 restart assert read a post-serve state where my test
   had performed no serve; fixed by performing it; (c) the W2
   wastes table copied the probe's post-serve sump levels where the
   assert runs post-tick pre-serve; recomputed the table. 6 passed
   / 0 failed (1.65s) after the fixes.
8. Verification turns: family floor 14 files: 144 collected / 144
   passed / 0 failed, 189.22s (138 pre-existing + my 6: arithmetic
   closes exactly). Consumer sweep (every test file outside the
   floor importing the water surface, found by grep): 24 files,
   321 collected, 303 passed, 18 failed: all 18 in files whose
   mtimes predate my window, named in COUNTS, none touched, no
   stash (sibling-dirty tree law).
9. Gates turn: ratchet FAIL NEW=1 on tools/hermes_burn.py:98, a
   sibling's live mid-window edit (named in finding 7e, not
   accepted, not touched); my changed bytes carry zero NEW hits;
   GROWTH advisories 5, one of them water_graph.py 465 -> 762
   riding cycle 3's claim. Citation lint exit 0, blocking=0, warns
   only. Em-dash sweep of my bytes: py block 0, gd block 0, test
   file 0, receipt 0.
10. Closed the loop: rewrote this receipt in full, appended the
    CLOSED line to the sidecar. Concurrency 1 throughout; no env
    vars printed; $0 spent; probe scripts stayed in the temp dir
    (3 files; every probe claim is re-proven by a named test
    above).

## COUNTS

- Product files changed this window: 2 (mag/water_graph.py 710 ->
  762 lines: +52, all docstring bytes: THE THERMOSTAT block;
  roblox_to_godot/systems/water_graph.gd 674 -> 712: +38,
  header-mirror lines). Zero engine-behavior bytes changed in
  either file: the floor's 138 pre-existing green pins are the
  proof.
- Test files added: 1 (tests/test_water_graph_thermostat.py, 6
  tests, 283 lines). Test files modified: 0.
- Family floor (my composition, named): 14 files, 144 collected /
  144 passed / 0 failed, 189.22s. Per-file collected: test_hydro_
  xor_sim 15, test_hydrology 15, test_water_computer 7, test_water_
  graph 22, test_water_graph_boiler 7, test_water_graph_campaign
  10, test_water_graph_int_domain 20, test_water_graph_latch 8,
  test_water_graph_ripple 6, test_water_graph_starvation 9,
  test_water_graph_steam_siphon 2, test_water_graph_thermostat 6,
  test_water_graph_vortex 13, test_water_swarm 4. (Prior window
  claimed 138 across 13 files; 138 + 6 = 144: arithmetic closes
  exactly.)
- Consumer sweep: 24 files, 321 collected, 303 passed, 18 failed.
  The 18 by group: test_verdict_feed 10 (rate-carrying
  tools/gps_mcp/ledger.py last written 2026-10-10 18:09, test file
  2026-10-01), test_propagator 2 (carried since cycles 3-7),
  test_gods_number 1 (stale golden, carried since cycle 9),
  test_k8s_water 1 (carried since cycles 3-7), test_env_contract 1
  and test_mcp_bridge_r1 1 and test_parity_gate_hook_pin 2 (new to
  any mariner receipt; test files 2026-09-30/10-01, sources
  tools/legality_propagator.py 2026-09-30, tools/mcp_parity.py
  2026-10-01).
- Floor + sweep totals: 38 files, 465 collected, 447 passed, 18
  failed (none mine: my bytes changed no engine behavior).
- Gates: ratchet FAIL NEW=1, the one hit on tools/hermes_burn.py
  (sibling mid-window edit, mtime 08:54:58, NOT accepted by me, NOT
  my file); my bytes: zero NEW; GROWTH advisories 5 (water_graph.py
  rides cycle 3's claim). Citation lint exit 0, blocking=0, warns
  only, zero findings on my three files.
- Em-dashes: 0 in my bytes (py block, gd block, new test file, this
  receipt); pre-existing em-dashes in untouched cycle 1-9 docstring
  bytes are not my diffs.
- Probe artifacts in the repo: 0 (3 temp scripts in the temp dir,
  single process, in-memory; every probe claim pinned by a named
  test).
- My bugs caught and fixed this window: 4 pin bugs (W2 condense
  smoothing, S2 restart serve, W2 wastes table, W2 condense table
  rebuilt) plus 1 probe-board design bug (the unprimed governor).
  Sketch falsifications: 2 (the two-tick lap: the +0 chain makes
  it one; the serve-on-open cold start: the prime law).
- Water units conserved across all pins: every test asserts
  _total: 3, 3, 3, 5, 3, 1, 1. Boards never reached the saturation
  ceiling: zero absorbed units, zero losses.
- Paid API calls: 0. Env vars dumped: 0. Concurrency peak: 1
  process. Godot executions: 0 (no binary on box, re-checked
  11:38:30). RAM peak: trivial (largest board 5 nodes, in-memory).

## NEXT THREAD (self-chosen, for the next cycle)

THE WINDING CLOCK: finding 4 says the cold crown is a windable
delay line (N stored units = N autonomous wheel turns after the
shovel dies). Pin it as a clock: (a) STORE-THEN-COUNT: over-shovel
a known N to the crown, kill the serve, count the post-death open
ticks, assert the count reads N for several N (the sky holds a
number); (b) THE BAND: a cap-2 sense leg under a sill-2 latch
(pool rides [1, 2], opens every tick once ramped) against the cap-1
board's ride: does the wider leg flatten the setpoint or just double
the draw: probe then pin; (c) WINDING BY WORLD VERB: staged boils
(the zero-latency shovel) as the wind: the operator winds the sky
during the tick instead of between ticks: composition work on the
engine side, no engine bytes; a custom world board is named, not
built (MountainWorld's board is fixed). Ride-alongs unchanged:
Godot parity execution (blocked on a Godot binary), held-inlet
provenance lines (safe, small), the windowed signed reader (named,
not built since cycle 9).

Resume note: no mid-road stop. Cycle 10 closed at a boundary; the
next cycle resumes by id mariner with the thread above.
