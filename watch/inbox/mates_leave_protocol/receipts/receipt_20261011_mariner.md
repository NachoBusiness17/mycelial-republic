# Receipt: mariner mission 20261011 (cycle 4, complete)

Mate: THE MARINER. Pack: logs/mates/missions/mission_20261011_07_mariner.md
(claimed via its .claim sidecar at 08:24:48, OPEN line appended; CLOSED
line appended at window close).

Status: COMPLETE. Stopped at a clean boundary, not context death, not
mid-road. Launch stub was filed in this file before any speech, per
contract, and rewritten here at window close.

Resume note: cycle 1 (receipt_20261006_mariner.md) sketched the vortex.
Cycle 2 (receipt_20261009_mariner.md) died with zero bytes. Cycle 3
(receipt_20261010_mariner.md) landed the vortex node kind in three
engines and left a self-chosen NEXT THREAD: the chained-rotor clock as
a real engine pin, Godot parity sequences, and ride-alongs (the
write-only `delivered` dict, the "any" ghost kind, held-inlet
provenance lines). Cycle 4 resumed by id mariner, verified the thread
state first (vortex bytes present in mag/water_graph.py and
tests/test_water_graph_vortex.py, exactly as cycle 3 claimed), then
rode it.

Working-tree note (named, not silent): cycle 3's landing was uncommitted
at cycle 4 start and remains uncommitted at cycle 4 close (no commit was
asked). Diff-vs-HEAD on the water files mixes cycle 3 and cycle 4 bytes;
the COUNTS section separates them by naming cycle 4's exact deltas.
379 porcelain entries were already dirty from sibling lanes at claim
time; none touched, none stashed (a full stash on a sibling-dirty tree
is a collision risk; see the pre-existing-red note in COUNTS for how the
not-mine claim is carried instead).

Laws held: em-dash 0 (scanned: added lines of all five changed files,
plus the full vortex test file and this receipt, 0 hits), real counts
only, no fabricated anything, no env dumps, RAM gate respected
(in-memory graphs, largest board 5 nodes), rolling concurrency
respected (concurrency peak 1 process), drop-ledger awareness (this
receipt names searchable terms: water_graph vortex clock LCM DAG sill),
COMPUTE LADDER honored per the STEER row (all work local on this
account, zero paid API calls, Nous/Hermes untouched: this account
provided everything, which is the row's point).

## FINDINGS

1. THE CLOCK LAW (the seed thread's next leg, landed as pins): a k1-wheel
   that feeds a k2-wheel on every k1'th tick (its other outlet draining
   elsewhere) drives the downstream wheel with period k1*k2. Pinned:
   k=2 half-feeding k=3 reads x,y,z,x,y,z on even ticks (ticks
   2,4,6,8,10,12), two full laps on 12 units, conserved, both rotors end
   where they started (12 mod 2, 6 mod 3). A CONTINUOUSLY fed k2 wheel
   collapses to period k2 (pinned: f0,f1,f2 on consecutive ticks). The
   cycle-1 sim's LCM claim is thus true in the real engine, with the
   correction that the period is feed-cadence times wheel, which equals
   LCM only for the coprime half-fed shape. Test:
   test_half_fed_ladder_is_a_run_down_clock_of_period_k1_times_k2,
   test_continuously_fed_wheel_collapses_to_its_own_period (both in
   tests/test_water_graph_vortex.py).

2. THE DAG LAW (new, docstring-landed, probe-falsified the cycle-3
   guess): the water graph cannot circulate. Every pipe must descend
   (check-valve law); a siphon primes only under the SAME head law, so
   it is no lift; steam, the only lift in the engine, is actuated
   (boil()), never autonomous. Consequences pinned or probed: a direct
   self-loop outlet can never flow (equal elevation is no head; 6-tick
   probe: zero movement, zero events, wheel parked at rot 0: pinned as
   test_direct_self_loop_is_a_brake_not_a_clock); a two-vortex ring dies
   on its uphill closing leg (gravity ring AND siphon ring both probed:
   the siphon leg needs head_ok too); a relaxation oscillator that
   feeds its own hub is head-blocked by construction (the basin the hub
   fills is by that fact below the hub, so the return leg rises). The
   cycle-3 docstring line "with a feedback pipe a self-clocking sequence
   source" is STRUCK and replaced by the run-down clock + DAG law in
   mag/water_graph.py's module docstring, spec-first. Every rotor clock
   runs down when its pool drains; the graph is a descent, never a
   perpetual loop. (The mariner's log: you cannot sail uphill; the
   boiler is the only wind, and someone must shovel.)

3. BURST-ON-ITS-TICK TURNS THE WHEEL, THEN THE PHASE REMAPS (pinned
   small): with an outlet stress-seeded at its djb2 threshold, its
   first full-bore turn bursts it; the unit sprays to the lowest node
   that is not dst; the rotor STILL advances (the water left the hub);
   next tick the live-outlet list has k=1 and the stored rot reads
   1 % 1 = 0, so the survivor emits: the burst remaps the wheel's
   phase. Roundtrip carries fractured + stress + rot (the AC2 and
   vortex roundtrip laws compose); the post-roundtrip tick emits the
   survivor. Test: test_outlet_fracture_turns_the_wheel_then_remaps_the_phase.

4. THE K=0 ENDGAME IS SAFE (pinned): a vortex whose every outlet has
   burst freezes with its pool, silently, no crash: the rotor grouping
   loop only collects live pipes, so the `rot % 0` evaluation seat is
   unreachable by construction. Both-outlets-burst board: hub keeps 4,
   sinks hold the two sprayed units, conserved 6, zero events after.
   Test: test_all_outlets_burst_freezes_the_hub_with_its_pool.

5. A SIPHON OUTLET MAKES A CREST-GATED ROTOR (pinned): outlet 0 a
   siphon (crest 3, cap 2), outlet 1 plain cap-1. Below crest the wheel
   parks on the siphon channel; at hub >= crest it primes and delivers
   min(cap, volume); while primed the wheel alternates siphon/plain;
   when the hub runs dry the primed siphon breaks (intake dry) and the
   wheel parks for good. Hysteresis: crest-gated start, break-stop.
   Traced end state: low 6, high 4, swirl 0, rot 0, conserved 10.
   Test: test_siphon_outlet_makes_a_crest_gated_rotor.

6. THE SILL DRAINS ITS POOL ON THE FIRST DRY TICK AFTER A PASS (pinned
   as designed, so nobody files it as a bug): the STARVED spill treats
   ALL standing volume at a gate as dead weight on a dry tick, even
   volume that landed through a PASSED gate the tick before. Tick 1:
   two inlets pass sill 2, the outflow takes 1, the remainder stands.
   Tick 2 (dry): STARVED spills the remainder to the first waste. A
   gated junction is a pulse device: it drains on a dry tick. Conserved
   via the waste hold. Same shape as cycle 3's vortex-committed-landing
   pin. Test: test_sill_drains_its_pool_on_the_first_dry_tick_after_a_pass
   (tests/test_water_graph_starvation.py).

7. THE "any" GHOST KIND IS STRUCK, NOT LANDED (cycle 1 finding 8
   closed): the docstring promised kind "any" as OR since the module
   was born; the tick never special-cased it (cycle 1's probe read
   plain behavior; this cycle's grep found zero production use). The
   truthful close is a strike, not machinery: sill 1 IS the hydraulic
   OR (a gate with threshold 1 passes when any single inlet delivers),
   so the gate family was already complete: sill 1 = OR, xor = XOR,
   sill n = AND-threshold. Docstring updated with the evidence; the
   engine's behavior changes by zero bytes.

8. THE WRITE-ONLY `delivered` DICT IS DELETED (cycle 3 residual,
   landed): created, written at three sites, read by no engine, no
   test, no render layer, in either twin. Removed from mag/water_graph.py
   (creation, three _move call sites, the gate-commit write, the _move
   signature, the _move write), mag/hydrology.py (_move override
   signature + write), and roblox_to_godot/systems/water_graph.gd
   (creation, three call sites, the gate-phase guard+write, the _move
   signature, the hydrology-branch write), with fix comments carrying
   the receipt. Event lines carry the same provenance the dict
   pretended to keep. Behavior-neutral by construction, proven by the
   floor: 116 passed / 0 failed (cycle 3's floor was 109; +7 = exactly
   this cycle's new tests).

9. Residuals carried forward: (a) Godot parity vortex sequences remain
   UNPROVEN: no godot or godot4 binary on this box (Get-Command: both
   absent; no vendored godot*.exe anywhere in the repo), so the parity
   runner cannot execute here; the gd twin's deletion and docstring
   mirror are landed line-for-line (cycle-3 precedent: the Python suite
   is the executable pin, the runner is the designated cross-engine
   prover when a box has Godot). (b) Held-inlet per-pipe provenance
   lines (cycle 3 residual) skipped this cycle for scope: safe to land
   later, the starvation tests assert by membership and substring, not
   exact list equality, so additive event lines break nothing. (c) The
   R8 named residual (hydrology._move adds raw instead of _receive)
   remains, untouched, still named in both engines. (d) The three
   pre-existing reds (test_k8s_water.py::test_ledger_workload_feeds_simulator,
   tests/test_propagator.py::test_agreement_law_100_sampled_cases,
   tests/test_propagator.py::test_agreement_covers_every_label) fail
   identically to cycle 3's stash-proven list; see COUNTS for why no
   fresh stash was run on this sibling-dirty tree. (e) Ratchet GROWTH
   advisory on mag/water_graph.py (accepted at 465, now 551: cycle 3's
   +69 then this cycle's +17) rides the claim cycle 3 registered and
   named; the operator re-audits or re-accepts at push.

10. Playing the vortex (the mariner's read for the next rider): the
    engine now has a rotor (demux, counter, run-down clock) but no
    LATCH: every gate drains on a dry tick (finding 6), so the water
    computer has no memory element beyond the rotor's position. A gate
    kind that HOLDS its pool across dry ticks (deliver-on-gate,
    keep-on-dry) would be the first bit of state a graph can carry
    between reads; rotor + latch is the rung where the water computer
    starts computing finite-state machines. NEXT THREAD below.

## JOURNEY

1. Boot and claim: read the pack; found three prior mariner receipts
   and read cycle 3's in full plus cycle 2's closure note; verified
   cycle 3's thread state by bytes (vortex in mag/water_graph.py,
   tests/test_water_graph_vortex.py on disk, no commit touching it);
   learned the claim grammar from the 10-10 sidecar; appended the OPEN
   line; filed this receipt's stub before any speech. Named the
   uncommitted-cycle-3 fact up front.
2. Read the hunting ground fresh, bytes not memory:
   mag/water_graph.py (534 lines at read), tests/test_water_graph_vortex.py
   (cycle 3's 7 pins), roblox_to_godot/systems/water_graph.gd tick and
   _move regions, mag/hydrology.py in full (the _move override carries
   the delivered param: the deletion surface), mag/water_computer.py in
   full (graph mode, valve honesty already landed, no new water-graph
   verbs to hunt), server/world.py in full (validate/stage/tick/_apply,
   valve-on-burst wording already landed), mag/hydro_xor_sim.py in full
   (continuous sim; NO OR-junction evidence in the family), and cycle
   1's probe file (it had already documented the "any" ghost).
3. Why: cycle 3's NEXT THREAD named five candidate surfaces; the bytes
   had to say which were real before any edit.
4. Probe round 1 (temp script, single process): falsified nothing yet
   but broke my own boards twice. The chained-clock board fed v2
   UPHILL (mid tanks below v2: check valves ate the flow: v2 starved at
   0 forever); the ring board's closing leg rose 5 -> 9 (dead). MY
   board bugs, caught by the probes reading zero flow. Also probed:
   direct self-loop (parked, zero movement: the head law fires before
   the net-zero question), siphon outlet (the crest-gated rotor, fully
   traced), closed-outlet degenerates (clean skip, rot preserved,
   reopen resumes), the "any" ghost (plain behavior re-confirmed), and
   sill pass-then-dry (the drain-on-dry sharp edge, first seen here).
5. Probe round 2 (corrected boards): the half-fed ladder WORKED and
   read x,y,z,x,y,z on even ticks (period 6); the surgical
   stress-seeded burst read exactly (rot turns on the burst tick, k
   drops, survivor emits); both rings still died (the closing leg: the
   DAG law surfacing). Dead end (probe script bug): round 2 crashed at
   the composite-roundtrip check on a missing from_spec import, so the
   oscillator and direct-chain probes never ran.
6. Dead end (design, not bug): the relaxation oscillator CANNOT be
   built with descending pipes: the hub's fill basin is below the hub,
   so the feedback leg rises and the head law blocks it. This dead end
   IS the finding: no autonomous feedback loop exists; the docstring's
   self-clock claim was a guess and is now struck.
7. Probe round 3: LCM(2,4) read f0..f3 at 2-tick spacing (period shape
   k1*k2; only one lap fit in 8 units: named, the (2,3) board with two
   full laps is the pin); continuous feed collapsed to k2 exactly; the
   composite burst state roundtripped byte-true and the
   post-roundtrip tick emitted the survivor.
8. Verified the deletion surface before editing: grep proved
   `_move(` and `delivered` exist in no test, no server file, no other
   mag module; the twin's delivered reads were guard-before-write.
   Why: cycle 3 called it one deletion; I refused to take that on
   faith before cutting a signature three engines share.
9. Spec-first edits: the module docstring got the cycle-4 corrections
   (the "any" strike with evidence; the clock law + DAG law replacing
   the self-clock guess) BEFORE any engine edit; the engine behavior
   changes by zero bytes for finding 7 and by the delivered deletion
   for finding 8.
10. Engine edits: delivered deleted from mag/water_graph.py,
    mag/hydrology.py, roblox_to_godot/systems/water_graph.gd, fix
    comments carrying the receipt at the signature sites.
11. Test landings: 6 new tests in tests/test_water_graph_vortex.py
    (clock, continuous-feed collapse, burst remap, siphon rotor,
    self-loop brake, k=0 freeze) and 1 in
    tests/test_water_graph_starvation.py (sill drain-on-dry), each
    with traced arithmetic in the docstring per the suite's grammar.
12. Dead end (test-board bug, caught before any run by re-tracing):
    the clock helper created v2's outlets before v1's, which flips the
    vortex emission-phase order (first-vortex-pipe insertion order) and
    shifts every mark one tick late. Reordered the helper's pipe
    insertion and documented the ordering law in its docstring.
13. Dead end (transient, logged not chased per positive steering): the
    first vortex+starvation run errored 22/22 with Permission-shaped
    collection errors; both files passed alone and together on the
    next two runs (22 passed). Sibling-lane file-lock blip; recorded
    here, no spiral. AMENDMENT at close (same window): the burst
    recurred once more on the combined run, full text still truncated
    as Perm... in the summary, and the immediate rerun passed 22/22
    again (1.23s). Pattern across both bursts: only the COMBINED
    two-file invocation, always clearing on rerun; never seen in the
    8-file floor run or the 10-file sweep. Environmental, intermittent,
    not code; the floor and sweep numbers in COUNTS are from clean
    runs.
14. Verification turns: water family floor (8 files) 116 passed /
    0 failed in 59.82s; wider consumer sweep (10 files: k8s_water,
    propagator, chat, server_persist, innkeeper, room, worldgen, river,
    dem_to_board, motion_rows) 193 passed / 3 failed, the 3 being the
    exact ids cycle 3 stash-proved pre-existing.
15. Gate turn: ratchet NEW=1 on tools/prepush_verkle_hermeticity.py:415
    (a sibling lane's file, never touched by me: not my debt to accept
    or fix); GROWTH advisory on water_graph.py named (cycle 3's claim,
    my +17 named here). Citation lint blocking=3, all in memory/zknot/
    pages (not my files); 51 warns, 0 on my five files. Em-dash sweep:
    0 in added lines of all five changed files, 0 in the vortex test
    file, 0 in this receipt.
16. Closed the loop: rewrote this receipt in full, appended the CLOSED
    line to the sidecar. Concurrency 1 throughout; no env vars printed;
    $0 spent; probe scripts stayed in the temp dir (the pins are the
    durable proof; every probe claim re-proven by a named test above).

## COUNTS

- Product files changed by cycle 4: 3 (mag/water_graph.py: two
  docstring blocks + delivered deletion, 534 -> 551 on disk, +17 net
  this cycle after cycle 3's 465 -> 534; mag/hydrology.py: _move
  signature + write removal; roblox_to_godot/systems/water_graph.gd:
  creation, three call sites, gate-phase guard+write, _move signature,
  hydrology-branch write removal). Diff-vs-HEAD stat mixes cycle 3's
  uncommitted bytes: hydrology.py +38/-... and water_graph.py +116/-
  include cycle 3; only the per-cycle deltas above are cycle 4's.
- Test files changed by cycle 4: 2 (tests/test_water_graph_vortex.py
  +6 tests, 7 -> 13 in the file; tests/test_water_graph_starvation.py
  +1 test, 8 -> 9).
- New test functions: 7 (6 vortex, 1 starvation).
- Water family floor: 116 collected / 116 passed / 0 failed, 59.82s,
  8 files (the cycle-3 floor read 109: +7 is exactly this cycle's new
  tests; no sibling drift in the family).
- Wider consumer sweep: 10 files, 196 collected, 193 passed, 3 failed
  (pre-existing: identical ids to cycle 3's stash proof; no fresh stash
  this cycle because the tree carries 379 sibling-dirty entries and a
  full stash is a collision risk; the claim rides cycle 3's byte-backed
  stash proof plus failure-id identity plus this cycle's
  behavior-neutral delta).
- Floor + sweep totals: 26 files, 312 collected, 309 passed, 3 failed
  (all 3 pre-existing).
- Gates: ratchet FAIL NEW=1 (tools/prepush_verkle_hermeticity.py:415
  file-too-long: sibling lane's file, named not accepted); GROWTH
  advisories 4 (water_graph.py 465 -> 551 named above; the other three
  are sibling lanes' gps_mcp/mesh_delta claims). Citation lint
  blocking=3 (all memory/zknot/ PHANTOM-NUMBERs, not my files), warns
  51 (0 on my five files).
- Em-dashes: 0 (added lines of 5 changed files; vortex test file full
  scan; this receipt).
- Probe artifacts in the repo: 0 (3 temp scripts, single process,
  in-memory; every probe claim pinned by a named test).
- Vortex/clock pins this cycle: period-6 two-lap ladder with exact
  marks and conservation 12; consecutive-tick collapse to k2 with
  sinks 2/2/2; burst remap with spray-to-a, rot 1 -> 0, survivor
  emit, roundtrip true; siphon rotor end state 6/4 conserved 10 with
  the break; self-loop brake 6 ticks zero movement; k=0 freeze
  conserved 6 silent; sill drain-on-dry conserved.
- Paid API calls: 0. Env vars dumped: 0. Concurrency peak: 1 process.
  Godot executions: 0 (no binary on box).

## NEXT THREAD (self-chosen, for the next cycle)

THE LATCH: a gate kind that HOLDS its pool across dry ticks
(deliver-on-gate, keep-on-dry), the water computer's first memory
element beyond the rotor's position. The sill's drain-on-dry pin (this
cycle, finding 6) is the exact spec contrast a latch pins against.
Rotor + latch = finite-state machines in water. Ride-alongs for the
same or next cycle: Godot parity vortex sequences (blocked on a box
with a Godot binary; the sequences for demux, clock, and burst-remap
are now fully specified by the Python pins), held-inlet per-pipe
provenance lines (safe: membership-based asserts), and the sibling
debts named in finding 9 belong to their own lanes. The k8s_water and
propagator reds stay named, not mine.

Resume note: no mid-road stop. Cycle 4 closed at a boundary; the next
cycle resumes by id mariner with the thread above.
