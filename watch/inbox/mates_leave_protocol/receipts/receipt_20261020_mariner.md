# Receipt: mariner mission 20261020 (cycle 13, complete)

Mate: THE MARINER. Pack: logs/mates/missions/mission_20261020_07_mariner.md
(claimed via its .claim sidecar at 08:12:02 by the static runner; the
runner appends the exit line itself, so the mate leaves the sidecar
untouched). A stub was filed in this file before any speech, per
contract, and rewritten here at window close.

Status: COMPLETE at a cycle boundary, not context death. The cycle-12
next-thread THE BANKED GOVERNOR is landed as seven laws in one new
test file (seven pins, one executing the Godot twin), and the next
thread is named below.

Resume note: the 20261019 window died at exit=1 (sidecar line
"[2026-10-19 09:36:48] mate=mariner pid=11724 exit=1") having filed
only its stub; zero bytes landed there. This window resumed cycle
12's thread from receipt_20261018_mariner.md.

Laws held: em-dash 0 in my bytes (the new docstring block in
mag/water_graph.py lines 338-390, the mirror block in the Godot twin
lines 278-307, the new test file, this receipt: all 0; the files'
pre-existing em-dashes in untouched cycle 1-12 bytes are not my
diffs), real counts only, no fabricated anything, no env dumps, RAM
gate respected (in-memory boards, largest 5 nodes; the Godot child is
the harness's own headless run), rolling concurrency respected (peak
2 processes: one pytest plus one godot child), receipt before speech,
positive steering (one pre-run table fix, one falsified parity
assumption, one test pin bug: all recorded and fixed, no spiral),
drop-ledger awareness (searchable terms: water_graph banked governor
gauge line serve unattended shovel reader open prime law floor tax
blind spot dry knock DRY_POOL rate cap ladder order meter full stream
balance split balloon backlog bank meter residue mod cap wide tap
cross-engine parity verdict rule_parity Godot twin headless crown
hostage sense leg committed landing period 2 committed), COMPUTE
LADDER honored per the STEER row: all work local on this account,
zero paid API calls, Nous/Hermes untouched, no Task agents needed
(single-seat probe-and-pin work). Consumer law: this window consumes
the engine and files tests; the consumers of my bytes are the pytest
water family floor and the pre-push gates (ratchet, citation lint),
named in COUNTS.

## FINDINGS

1. THE GAUGE-LINE SERVE (pinned end to end): one prime shovel, then
   one shovel per "Latch R opens" line, runs the wheel UNATTENDED at
   one serve per TWO ticks: the reader's verdict lag stretches the
   period but eats nothing. Bank 6, sill 1: prime at t1, reader
   opens t2,t4,t6,t8,t10,t12, chases land t3,t5,t7,t9,t11, the sink
   ends at 6, the bank is empty, silence from t13 (18-tick window
   pinned, every event list and volume table exact). The first serve
   is never eaten: the prime is unconditional; the train chases it
   at period 2. The serve trigger now lives on the gauge line (the
   cycle-10 serve law's trigger moved from the store's verdict line).
   Test: test_the_gauge_line_serve_runs_unattended.
2. THE PRIME LAW HOLDS AT THE GAUGE (pinned): a sub-level prime
   strands the bank: one shovel under a sill-2 store pools 1 and
   holds (the HOLD line), zero reader opens fire, the governor never
   starts: 7 ticks, zero serves, bank 5 stranded at the basin,
   hostage pool 1 in the store. The cycle-10 prime law survives the
   trigger move unchanged. Test: test_the_prime_law_holds_at_the_gauge.
3. THE FLOOR TAX (pinned): the primed sill-2 governor serves N-1
   and parks the level-1 blind spot in the store: bank 6, prime 2:
   five serves, the store sleeps at pool 1. The 2-prime through the
   cap-1 sense leg also parks one HOSTAGE at the crown for one tick,
   so the wheel starts at t2, not t1 (first reader open t3). The
   last serve is eaten by the store's floor, never by the lag.
   Test: test_the_floor_tax_parks_the_blind_spot.
4. THE DRY KNOCK (pinned on both boards): the train always asks one
   serve past the bank: the last reader open stages a shovel the
   empty basin rejects at stage time (DRY_POOL from the world
   verb's validator). Exactly 1 rejected knock on every spent bank:
   7 stage attempts, 6 acked on the sill-1 wheel, 6 acked on the
   sill-2 wheel (the 7th rejected both times). Test:
   test_the_dry_knock.
5. THE ORDER IS THE METER (pinned): on the live-wire board with a
   CAP-2 tap under the 8-unit wind, the drain-first insertion order
   keeps the balance split (4 of 8 to the sink: the drain takes its
   unit first, the tap passes min(cap, remainder): the tap cap is
   invisible behind the order), while the tap-first order meters
   the FULL stream (8 of 8) and the reader BALLOONS +1/tick while
   the wind lasts (opens read pool 2,3,4,5), draining the backlog
   1/tick after the wind dies: the reader outlives the wind by the
   whole backlog (the sink's last unit 5 ticks after the last
   served tick). Mass 8 conserved at every tick, both boards.
   Test: test_the_order_is_the_meter.
6. THE METER'S FLOOR (pinned): the store read's terminal pool is
   the first value below the level in the descent bank, bank-cap,
   bank-2cap, ...: a cap-1 tap floors at level-1 regardless of the
   bank (stored 6 reads 5: opens at 6,5,4,3,2), while a cap-2 tap
   reads past that floor to the bank's residue mod the cap (stored
   6 reads 6: opens at 6,4,2; stored 5 reads 4; stored 7 reads 6;
   the level-1 residue sleeps). The cycle-12 blind spot is a cap-1
   artifact, not a law of the store. Test: test_the_meters_floor.
7. THE CROSS-ENGINE VERDICT (pinned, EXECUTED): the banked governor
   board runs through BOTH engines via the tools/rule_parity
   harness, the Godot twin headless: 12 ticks, per-tick state
   hashes and verdict rows identical (parity true, no first
   divergence), including a reject:RATE_CAP row (the receipt
   ladder's per-tick action cap ate the SECOND staged prime) both
   engines agree on. Ladder parity holds on a composition board,
   not just the int-domain stress family. The board's schedule is
   its own (one acked prime, five acked serves at t4,t6,t8,t10,t12;
   end state waste 0, store 1, reader 1, sink 4, the fifth serve's
   unit in flight), not a transcript of the MountainWorld serve
   run, because the ladder caps differ from the raw world layer.
   Test: test_the_cross_engine_verdict.

## JOURNEY

1. Boot and claim: read the pack; read the 20261019 sidecar (exit=1,
   stub only, zero bytes) and cycle 12's full receipt for the
   thread; verified by git status that the water files carry the
   cycles 3-12 uncommitted tree (documented, not mine to stash) and
   that my edit anchors matched cycle-12 bytes exactly. Appended
   nothing to the sidecar (the runner owns it); filed this receipt's
   stub before any speech.
2. Thread intake: THE BANKED GOVERNOR in three named parts from
   cycle 12 (the unattended serve, the full-stream tap, the parity
   execution ride-along). Read mag/water_graph.py (853 lines at
   open) and server/world.py (428 lines) in full; water_computer.py
   not read this window (it delegates its graph path to this engine;
   the governor composes water_graph kinds, and the cycle-12 receipt
   holds its surface). Prior-art sweep before any probe: the
   reading-glass pin file for board grammar, the winding-clock file
   for the MountainWorld drive pattern, the int-domain file for the
   parity test shape, tools/rule_parity.py for the sequence schema
   (frames of staged acts). No unattended-serve or full-stream pins
   existed anywhere in tests/ (the serve law lived only on the
   verdict line in the thermostat file): the gaps were real.
3. Probe round 1 (one temp script, single process, in-memory):
   five probes by one driver, then a follow-up probe for the
   residue law. Engine-taught turns: (a) the P2b board starts at
   t2, not t1 (the 2-prime through the cap-1 sense leg hosts one
   unit at the crown), a shape my hand-trace missed; (b) the parity
   harness's receipt ladder rate-capped the second staged prime
   (reject:RATE_CAP at t1), falsifying my plan to mirror the
   MountainWorld run byte-for-byte: the parity board became its own
   schedule with the reject row pinned as a feature; (c) the dry
   knock appears on BOTH boards, 1 reject each, before I knew to
   look for it as a law. The residue probe (stored 5 and 7 under a
   cap-2 tap) pinned the wide tap's floor as the bank mod cap.
4. Spec-first: wrote THE BANKED GOVERNOR block into the module
   docstring BEFORE any test landed (probes done, numbers real),
   then the mirror block in the Godot twin's header (parity law
   from cycles 3-12). Engine behavior changed by zero bytes all
   window.
5. Landed tests/test_water_graph_banked_governor.py, 7 pins, 392
   lines. Dead ends caught: (a) pre-run, my tap-first assertion
   table was hand-written wrong (t1 carries no reader open; the
   balloon pools ride 2,3,4,5 then 4,3,2,1): fixed against the
   probe trace before the first run; (b) first run failed once,
   test_the_dry_knock: I subtracted rejects from acked shovels
   when shovels already counts acked only (attempts = shovels +
   rejects = 7, both boards): fixed the pin. 7 passed / 0 failed
   (1.34s) after the fix, including the parity test executing the
   twin binary.
6. Verification turns: family floor 17 files: 162 collected / 162
   passed / 0 failed, 61.78s (cycle 12's 155 + my 7: arithmetic
   closes exactly; per-file census taken). Consumer sweep (rg
   "water_computer|water_graph|WaterGraph|MountainWorld|gravity_
   tick|sight_glass" over tests/ with the water family excluded;
   the glob let tests/test_hydrology.py through and I excluded it
   explicitly: instrument named here): 23 files, 305 collected,
   288 passed, 17 failed: identical totals and identical red set
   to cycle 12's sweep, all in files predating my window, none
   touched, no stash (sibling-dirty tree law).
7. Gates turn: ratchet PASS NEW=0 on 85 changed files, all 63 hits
   registered debt; GROWTH advisories 12 (water_graph.py 465 ->
   906 rides cycle 3's registered claim per the cycle 9-12
   receipts; my share of the growth is +53 docstring lines; the
   other 11 are sibling files). Citation lint exit ok, blocking=0,
   107 warns, zero findings on my files. Em-dash sweep of my
   bytes: py block 338-390: 0, gd block 278-307: 0, test file: 0,
   this receipt: 0 (whole-file sweeps of the two engine files show
   only pre-existing cycle 1-12 bytes).
8. Closed the loop: rewrote this receipt in full. Concurrency peak
   2 processes (pytest plus one godot child); no env vars printed;
   $0 spent; probe scripts stayed in the temp dir (2 scripts + 2
   parity files; every probe claim is re-proven by a named test
   above).

## COUNTS

- Product files changed this window: 2 (mag/water_graph.py 853 ->
  906 lines: +53, all docstring bytes: THE BANKED GOVERNOR block,
  lines 338-390; roblox_to_godot/systems/water_graph.gd 784 ->
  815: +31, header-mirror comment lines, block 278-307). Zero
  engine-behavior bytes changed in either file: the family floor's
  155 pre-existing green pins plus the consumer sweep's identical
  red set are the proof.
- Test files added: 1 (tests/test_water_graph_banked_governor.py,
  7 tests, 392 lines). Test files modified: 0.
- Family floor (my composition, named): 17 files, 162 collected /
  162 passed / 0 failed, 61.78s. Per-file collected: test_hydro_
  xor_sim 15, test_hydrology 15, test_water_computer 7, test_
  water_graph 22, test_water_graph_banked_governor 7, test_water_
  graph_boiler 7, test_water_graph_campaign 10, test_water_graph_
  int_domain 20, test_water_graph_latch 8, test_water_graph_
  reading_glass 6, test_water_graph_ripple 6, test_water_graph_
  starvation 9, test_water_graph_steam_siphon 2, test_water_graph_
  thermostat 6, test_water_graph_vortex 13, test_water_swarm 4,
  test_water_graph_winding_clock 5. (Cycle 12 claimed 155 across
  16 files; 155 + 7 = 162: arithmetic closes exactly.)
- Consumer sweep: 23 files, 305 collected, 288 passed, 17 failed.
  The 17 by group: test_verdict_feed 10, test_propagator 2,
  test_parity_gate_hook_pin 2, test_gods_number 1, test_k8s_water
  1, test_env_contract 1. Identical totals and identical set to
  cycle 12's sweep (test files 2026-09-29 to 2026-10-01). None
  mine: my bytes changed no engine behavior.
- Floor + sweep totals: 40 files, 467 collected, 450 passed, 17
  failed.
- Gates: ratchet PASS NEW=0 on 85 changed files, all 63 hits
  registered debt; GROWTH advisories 12 (water_graph.py rides
  cycle 3's claim, my share +53 docstring lines). Citation lint
  exit ok, blocking=0, warns 107, zero findings on my files.
  Em-dashes: 0 in my bytes (py block 338-390, gd block 278-307,
  new test file, this receipt); pre-existing em-dashes in
  untouched cycle 1-12 docstring bytes are not my diffs.
- Probe artifacts in the repo: 0 (2 temp probe scripts + 2 parity
  files in the temp dir, single process, in-memory; every probe
  claim pinned by a named test).
- My bugs caught and fixed this window: 1 pre-run pin table fix
  (tap-first trace hand-written wrong), 1 falsified assumption
  (the parity schedule mirroring the MountainWorld run: the
  ladder's RATE_CAP reshaped the board, and the reject row became
  a pinned feature), 1 test pin bug at first run (dry-knock
  arithmetic: shovels counts acked only; attempts = shovels +
  rejects = 7). Sketch falsifications total: 1.
- Water units conserved across all pins: totals pinned 6, 6, 6,
  8, 8, 6, 5, 7 at every tick of their boards; the parity board's
  mass rides the state-hash equality across both engines; no
  board touches the saturation port.
- Paid API calls: 0. Env vars dumped: 0. Concurrency peak: 2
  processes. RAM peak: trivial (largest board 5 nodes, in-memory).
- Godot executions: 3 subprocess runs observed in this window
  (1 by probe P5, 1 by my parity test's own run, 1 by the
  int-domain suite's parity test inside the floor run): all
  headless, all green.

## NEXT THREAD (self-chosen, for the next cycle)

THE LADDER GOVERNOR: this window's RATE_CAP discovery opens the
rung the serve law never climbed: the governor under the receipt
ladder. (a) THE CAPPED PRIME: the ladder allows one action per
sid per tick, so an unattended governor on the world ladder must
split its prime across ticks (or ride a second sid): probe the
split prime (1 shovel at t1, 1 at t2 under a sill-2 store: does
the wheel start at t3 with no hostage, and at what cost in
latency?) and the two-sid prime (two sessions stage the same
beat: the ladder admits both: does the MountainWorld run then
match the parity board?). (b) THE WIDE-PRIME START: prime 2
through a cap-2 sense leg lands both units at t1 (no crown
hostage): pin the start-at-t1 wheel and its period against the
cycle's t2-start control. (c) THE BALLOON READ-BACK: the
full-stream meter's reader balloon (pool 2,3,4,5) is readable
state: tap out of R into a second gauge and read the backlog
while it drains (the meter of the meter), pinning whether the
second tap's floor hides the backlog's last unit the way the
store's floor hides the bank's. Ride-alongs unchanged: held-inlet
per-pipe provenance lines (still deferred: the byte-exact event
pins), the R8 hydrology residual.

Resume note: no mid-road stop. Cycle 13 closed at a boundary; the
next cycle resumes by id mariner with the thread above.
