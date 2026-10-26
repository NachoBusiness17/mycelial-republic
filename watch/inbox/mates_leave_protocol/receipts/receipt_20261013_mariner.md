# Receipt: mariner mission 20261013 (cycles 6-7, complete)

Mate: THE MARINER. Pack: logs/mates/missions/mission_20261013_07_mariner.md
(claimed via its .claim sidecar at 08:18:32, OPEN line appended; CLOSED
line appended at window close). Launch stub was filed in this file before
any speech, per contract, and rewritten here at window close.

Status: COMPLETE. Stopped at a clean boundary: both the pack's seed
thread (the skyrmion vortex line) and the persona's named corners
(steam over closed valves, siphon math) are landed as pins, and the
next thread is named below. Not context death, not mid-road.

Resume note: cycle 1 (receipt_20261006) sketched the vortex; cycle 2
(20261009) died with zero bytes; cycle 3 (20261010) landed the vortex
kind; cycle 4 (20261011) proved the clock and DAG laws, struck the
"any" ghost, deleted the write-only delivered dict; cycle 5 (20261012)
landed the latch and left a self-chosen NEXT THREAD: the ripple
counter and the difference detector. Cycle 6 resumed by id mariner,
verified cycle 5's thread state by bytes first (mag/water_graph.py at
618 lines with the LATCH block, 8 pins in test_water_graph_latch.py,
13 in test_water_graph_vortex.py, 9 in starvation: all present), then
rode the thread. Cycle 7 rode the persona corners in the same window.

Working-tree note (named, not silent): cycles 3-7's water bytes are all
uncommitted at close (no commit was asked of any cycle); diff-vs-HEAD
on the water files mixes five cycles, and COUNTS names this window's
exact deltas only. The sibling-dirty porcelain entries (30 changed files
in the ratchet's scope) were already on the tree; none touched, none
stashed.

Laws held: em-dash 0 (rg unicode sweep of the full diffs of both changed
product files, both new test files, and this receipt: zero hits; the
twin's 34 pre-existing em-dash lines are untouched bytes not in my
diffs), real counts only, no fabricated anything, no env dumps, RAM
gate respected (in-memory boards, largest 13 nodes), rolling
concurrency respected (peak 1 process), receipt before speech,
positive steering (one Permission-shaped collection blip and one of my
own pin bugs were recorded and fixed, no spiral), drop-ledger awareness
(searchable terms: water_graph ripple counter binary rotor carry
difference detector xor pulse tank adapter steam bypass closed valve
siphon crest prime dry spell hysteresis latch waste). COMPUTE LADDER
honored per the STEER row: all work local on this account, zero paid
API calls, Nous/Hermes untouched, no Task agents needed (single-seat
probe-and-pin work).

## FINDINGS

1. THE RIPPLE COUNTER (the cycle-5 NEXT THREAD, part a, landed with
   ZERO engine bytes): a chain of four k=2 vortices, each stage's
   first outlet a digit sink and its second outlet the next stage, fed
   1/tick, is a binary ripple counter. After 13 ticks the rotors read
   rot 1,1,0,1 = 1101 = 13: rot_i = bit i of the tick count. The digit
   sinks hold the divided streams: d0 7 (every odd tick), d1 3
   (t2,6,10), d2 2 (t4,12), d3 1 (t8), conserved 13. The event marks
   ARE binary counting: a tick's cascade length equals the new count's
   trailing ones + 1, and the carry crosses EVERY stage within one
   tick (t8 shows the full four-stage cascade b0,b1,b2,a3 on 7+1=8;
   full cascades land exactly on the powers of two). The cascade rides
   the emission-order law: vortex dict keys follow first-pipe
   insertion order, so downstream rotors emit in the same tick they
   are fed. Test:
   test_ripple_chain_of_k2_rotors_reads_its_count_in_binary.

2. THE COUNT IS PURE STATE: a counter run with the feed closed for 5
   mid-run ticks (every gap tick emits zero events: no rotor holds
   stock) ends BYTE-IDENTICAL to an unbroken run of the same fed
   units: nodes and pipes dicts exactly equal. The counter is a
   function of the pulse COUNT, not the pulse timing: a register, not
   a leak. Test: test_the_counter_remembers_across_a_dry_gap.

3. THE COMMITTED-LANDING INTERFACE LAW, and the cycle-5 sketch's dead
   end (cycle 6's flagship hunt find): the NEXT THREAD's detector
   sketch said "two vortex wheels feeding one xor". My probe
   falsified the sketch: a vortex outlet is a committed _move in the
   rotor phase, AFTER the verdict, so the xor's verdict (which reads
   only DEFERRED inlets from plain-source pipes) never counts it. The
   landed units pool and STARVED-spill to the waste on the first
   inlet-free tick: 6 ticks, five 1-unit spills, one unit stranded in
   the xor, the latch at 0, and not one "Junction X passes" line in
   the run (cycle 3 finding 2 had named the starve shape; this pins it
   as the rotor-feed case). Test:
   test_rotor_into_a_gate_starves_without_a_pulse_tank. The honest
   close: the sketch was wrong, the death is the law, gates read
   deferred inlets only.

4. THE PULSE TANK IS THE ROTOR-TO-GATE ADAPTER: interpose a one-unit
   plain node between rotor and gate and the train re-enters the
   verdict economy one tick later, one unit wide: a plain-source
   delivery into a gated junction IS a deferred inlet. With the
   adapter, two anti-phase wheels drive the xor through exactly one
   inlet every tick from t2 on: X passes every tick, its outflow
   charges the level-1 latch, and the latch pool counts the
   disagreement. Traced exactly through t4 and marked through t6: L 5
   with one unit honestly in flight in the tank (a clock comparison
   never closes without a settling tick), conserved 12. Test:
   test_pulse_tank_adapter_lets_two_wheels_drive_one_xor.

5. THE DIFFERENCE DETECTOR (part b, rebuilt on the adapter): two
   tanked wheels (k=2 and k=3), one xor, one level-1 latch with a
   head-blocked outflow (the honest per-tick announce grammar, zero
   movement). In 12 ticks the trains coincide twice (both tanks
   deliver: X holds 2, the next dry verdict STARVED-spills the pair),
   disagree six times (X passes one unit into L each time), and share
   four neither-ticks (silence, zero bytes). The latch's pool ends at
   6: exactly the disagreement count; the waste reads 4: exactly the
   coincidence volume. The first water circuit that computes a
   RELATION between two signals rather than routing one. Test:
   test_difference_detector_accumulates_drift_not_coincidence.

6. AGREEMENT IS SILENCE: the same board with phase-locked wheels
   (both k=2, same phase) never passes a unit: six coincidence holds,
   five 2-unit STARVED spills, one pair stranded mid-rhythm, latch 0
   with zero Latch lines in the run. Locked vs drifting clocks is
   readable from where the water lands: latch pool for drift, waste
   for lock. Test: test_phase_locked_wheels_agree_in_silence.

7. DIVIDER SPEC ERRATUM FIXED (spec-first, zero engine bytes):
   cycle 5's LATCH docstring claimed the rotor-fed latch is a divider
   at "one outflow unit per L feed units". Re-deriving the divider
   pin's trace for this cycle showed that is wrong: the rotor sets
   the division (one charge per k swirl emissions) and the latch, once
   ramped, passes ONE UNIT PER CHARGE (the L-1 floor re-arms on every
   charge). Docstring corrected in the same breath as the new
   composition block, twin mirrored.

8. STEAM CROSSES A CLOSED VALVE (persona corner, part a): a sealed
   src with its only pipe closed, boiled, condenses at the cold crown
   and drains on: sink behind the valve stays 0 forever, no event ever
   names the sealed pipe, the valve is still shut at close, conserved
   3. The lift ignores pipes entirely: a closed valve seals its pipe,
   not the sky. Test: test_steam_bypasses_a_closed_valve.

9. THE SIPHON'S DRY-SPELL HYSTERESIS BELONGS TO THE DST KIND
   (persona corner, part b, and a real engine asymmetry): the siphon
   break lives in _move only, so a siphon feeding a GATED junction is
   probed through _available, which delivers 0 on a dry intake but
   never breaks the prime. Traced both fates on the same storm: the
   gate-side siphon rides silent through the dry tick (primed True)
   and then delivers a BELOW-CREST refill (1 unit at a crest-3 gate)
   that reopens the latch; the plain-dst siphon emits "breaks (intake
   dry)", loses its prime, and refuses the identical refill in
   silence. Crest paid once per prime, not per unit. Tests:
   test_siphon_prime_survives_a_dry_spell_only_at_a_gate.

10. Residuals carried forward: (a) Godot parity EXECUTION remains
    blocked: no godot or godot4 binary on this box; the twin's mirror
    is landed line-for-line (now including the cycle-6 and cycle-7
    header blocks) and the Python suite stays the executable pin
    (cycle-3 precedent). (b) Held-inlet per-pipe provenance lines
    (cycle 3 residual) skipped again for scope. (c) The R8 named
    residual (hydrology._move adds raw instead of _receive) remains,
    untouched. (d) The three pre-existing reds
    (test_k8s_water.py::test_ledger_workload_feeds_simulator,
    tests/test_propagator.py::test_agreement_law_100_sampled_cases,
    tests/test_propagator.py::test_agreement_covers_every_label) fail
    identically to cycles 3-5's list; no fresh stash (sibling-dirty
    tree). (e) The ratchet GROWTH advisory on mag/water_graph.py
    (accepted at 465, now 658) rides cycle 3's registered claim; the
    operator re-audits at push. (f) The signed difference detector
    (which wheel leads, not just that they disagree) needs a second
    xor-latch pair phase-flipped: named, not built, NEXT THREAD
    material. (g) A latch cannot BE the cold crown (kind is one
    string), so rain cannot charge a latch directly; a cold node
    above a latch is the composition, named in passing.

## JOURNEY

1. Boot and claim: read the pack; read cycle 5's and cycle 4's
   receipts in full; learned the claim grammar from the 10-12
   sidecar; appended the OPEN line at 08:18:32; filed this receipt's
   stub before any speech.
2. Verified cycle 5's thread state by bytes: mag/water_graph.py at
   618 lines with the LATCH block; test counts 8/13/9 in the
   latch/vortex/starvation files; water_computer.py grep for kind
   logic: zero hits (kind-blind, as cycle 5 claimed); server/world.py:
   one default xor node, no kind logic; twin's LATCH mirror present.
3. Read the latch suite in full to inherit the grammar (traced
   arithmetic in docstrings, exact event-list pins, _total
   conservation helper).
4. Probe round 1 (one temp script, single process, in-memory): P1 the
   ripple counter traced clean at 13 ticks (marks, rotors 1101,
   sinks 7/3/2/1, conserved); P2 the dry-gap board compared
   byte-equal; P3 the in-phase detector traced (waste 12, latch 0);
   P4 the anti-phase DIRECT rotor-to-xor board read WRONG against the
   sketch: STARVED spills, latch 0, zero pass lines. Why the turn:
   the sketch predicted xor passes every tick; the engine said the
   rotor's committed landing never joins the verdict. Dead end (the
   cycle-5 sketch's, not the engine's): re-read of the tick code
   confirmed the phase law; the adapter was needed.
5. Probe round 2 (same script): P4 rebuilt with plain pulse tanks
   (passed every tick, latch charged); P5 the drift board k=2 vs k=3
   traced (pool 6, waste 4 in 12 ticks). Dead end (derivation-only,
   caught at pin time): my first drift sketch miscounted the tank
   delay; re-derived by hand from the pipe-order law before pinning,
   and the pins passed first run.
6. Spec-first: wrote the RIPPLE COUNTER + DIFFERENCE DETECTOR block
   into the module docstring and the divider erratum fix into the
   LATCH block BEFORE any test landed; mirrored both into the twin's
   header (parity law from cycles 3-5). Engine behavior changed by
   zero bytes all window.
7. Landed tests/test_water_graph_ripple.py, 6 pins; 6 passed first
   run (the hand traces and the engine agreed).
8. Verification turns: floor run 1 (11 files) errored 129/129 with
   Permission-shaped collection errors: the same environmental
   sibling file-lock blip cycle 4 named (combined invocations only,
   always clearing on rerun): logged per positive steering, rerun
   clean: 129 passed / 0 failed, 61.35s. Wider consumer sweep (10
   files): 193 passed / 3 failed, the exact pre-existing ids from
   cycles 3-5.
9. Floor arithmetic turn (named, not papered): cycle 5's receipt
   claimed 124 across 9 floor files without a file-by-file list; my
   11-file floor reads 129 with my known +6, one short of naive
   arithmetic. Counted per file (collected table in COUNTS), checked
   git state of the shared water test files (two Modified, both the
   cycles' own uncommitted bytes): the -1 is composition ambiguity in
   the prior claim's unnamed file list. Recorded as unresolvable from
   here, no fabricated reconciliation.
10. Gates turn: ratchet PASS NEW=0 (18 hits all registered; GROWTH
    advisories 4: water_graph.py rides cycle 3's claim, the other
    three are sibling lanes'); citation lint blocking=0, warns 104,
    zero on my files. Em-dash sweep: 0 in both diffs and both new
    files.
11. Cycle 7 turn (context remained, thread not exhausted): rode the
    persona's named corners. Probe script 2: S1 the steam bypass
    traced clean; S2 the siphon-into-latch board traced (prime held
    through the dry tick, below-crest refill delivered); S3 the
    plain-dst contrast traced (break on dry, refill refused).
12. Spec-first again: siphon asymmetry and steam-bypass sentences into
    the Pipes and Steam docstring bullets, twin mirror block added.
13. Landed tests/test_water_graph_steam_siphon.py, 2 pins. Dead end
    (my pin bug, caught by the run): the plain side's end-state assert
    claimed total 6, but the refused refill STANDS at the intake (src
    1, total 7): the probe had not printed src/total and I
    over-assumed. Fixed the pin to the real bytes; the engine was
    right. Same bug class as cycle 4's turn 12 and cycle 5's turn 11:
    the run is the truth.
14. Final verification: both new files together 8 passed / 0 failed
    (0.94s); full family floor 12 files 131 passed / 0 failed
    (69.49s); gates re-run green (ratchet NEW=0, citation blocking=0);
    em-dash re-swept 0.
15. Closed the loop: rewrote this receipt in full, appended the CLOSED
    line to the sidecar. Concurrency 1 throughout; no env vars
    printed; $0 spent; probe scripts stayed in the temp dir (2 files;
    every probe claim is re-proven by a named test above).

## COUNTS

- Product files changed this window: 2 (mag/water_graph.py 618 -> 658
  on disk: +40, all docstring/spec bytes: cycle 6 +30 (the RIPPLE
  COUNTER + DIFFERENCE DETECTOR block, the divider erratum), cycle 7
  +10 (siphon asymmetry in the Pipes bullet, steam bypass in the
  Steam bullet); roblox_to_godot/systems/water_graph.gd 600 -> 643:
  +43 header-mirror bytes (cycle 6 mirror block, divider erratum
  mirror, cycle 7 WEATHER + SIPHON PRIME block). Zero engine-behavior
  bytes changed in either file: the suite's 131 green pins are the
  proof.
- Test files added: 2 (tests/test_water_graph_ripple.py: 6 tests, 364
  lines; tests/test_water_graph_steam_siphon.py: 2 tests, 125
  lines). Test files modified: 0.
- New test functions: 8 (6 ripple/detector, 2 steam/siphon).
- Family floor (my composition, named): 12 files, 131 collected /
  131 passed / 0 failed, 69.49s. Per-file collected:
  test_hydro_xor_sim 15, test_hydrology 15, test_water_computer 7,
  test_water_graph 22, test_water_graph_campaign 10,
  test_water_graph_int_domain 20, test_water_graph_latch 8,
  test_water_graph_ripple 6, test_water_graph_starvation 9,
  test_water_graph_vortex 13, test_water_swarm 4,
  test_water_graph_steam_siphon 2. Prior-window comparison: cycle 5
  claimed 124 across 9 files without naming the files; the -1 gap to
  naive arithmetic is composition ambiguity, named in JOURNEY turn 9.
- Wider consumer sweep: 10 files, 196 collected, 193 passed, 3 failed
  (pre-existing: identical ids to cycles 3-5).
- Floor + sweep totals: 22 files, 327 collected, 324 passed, 3 failed
  (all 3 pre-existing, named in finding 10d).
- Gates: ratchet PASS NEW=0 (18 hits all registered; GROWTH
  advisories 4, water_graph.py 465 -> 658 riding cycle 3's claim);
  citation lint blocking=0, warns 104, blocking and warns on my four
  files 0.
- Em-dashes: 0 (both product diffs full-scan, both new test files,
  this receipt).
- Probe artifacts in the repo: 0 (2 temp scripts in the temp dir,
  single process, in-memory; every probe claim pinned by a named
  test).
- My bugs caught and fixed this window: 1 (the plain-side pin's total:
  the refused refill stands at the intake; caught by the run, fixed
  to the real bytes). Environmental blips: 1 (Permission-shaped
  collection errors on floor run 1, cleared on rerun, cycle-4
  precedent). Sketch falsifications: 1 (cycle 5's direct
  rotor-to-xor detector: became finding 3's law).
- Water units conserved across all pins: every test asserts _total:
  13, 13, 12, 12, 24, 24, 3, 7, 6+1 standing at the intake.
- Paid API calls: 0. Env vars dumped: 0. Concurrency peak: 1 process.
  Godot executions: 0 (no binary on box). RAM peak: trivial (largest
  board 13 nodes, in-memory).

## NEXT THREAD (self-chosen, for the next cycle)

THE BOILER'S TOLL: the steam lift is the engine's only uphill route
(the DAG law), and it is actuated, never autonomous: someone shovels.
Quantify it: (a) the lift's exact cost curve: boil k units at a basin,
condense at a cold crown, drain back through a closed-valve-free
descent: throughput caps at the crown's outflow, and the cost is the
boil actuations per delivered unit: pin the cost for a two-basin lift
(basin, crown, receiver) with exact event lists. (b) The gated boiler:
a latch charged by a rotor whose verdict is READ by the operator
between ticks (the actuator is external by law): the first circuit
where the engine's state, not its physics, gates the lift: probe how a
campaign would sequence boil() against latch verdicts
(server/world.py verbs, no engine bytes). (c) The signed difference
detector (finding 10f): a second xor-latch pair phase-flipped so the
pair's two pools encode WHICH wheel leads; pin both pools on the
drift board. Ride-alongs unchanged: Godot parity execution (blocked on
a Godot binary), held-inlet provenance lines (safe, small).

Resume note: no mid-road stop. Cycles 6-7 closed at a boundary; the
next cycle resumes by id mariner with the thread above.
