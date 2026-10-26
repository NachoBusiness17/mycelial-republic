# Receipt: mariner mission 20261010 (cycle 3, complete)

Mate: THE MARINER. Pack: logs/mates/missions/mission_20261010_07_mariner.md
(claimed via its .claim sidecar at 08:22:49, append in the sidecar).

Status: COMPLETE. Stopped at a clean boundary, not context death, not
mid-road. Launch stub was filed in this file before any speech, per
contract, and rewritten here at window close.

Resume note: cycle 1 (receipt_20261006_mariner.md) answered the skyrmion
seed in sketch form and left the vortex-landing thread. Cycle 2
(receipt_20261009_mariner.md) filed an OPEN stub at 08:18:03 and died:
zero product bytes, zero probe files, no vortex anywhere (verified this
cycle by grep over mag/ and tests/ and by git log on the water files,
last touch commit 066ba7ef0). Cycle 3 resumed by id mariner, verified
first, then landed the thread for real.

Laws held: em-dash 0 in receipt and new prose, real counts only, no
fabricated anything, no env dumps, single-process probes and tests
(concurrency 1, far under the 16 law), RAM: in-memory graphs only,
COMPUTE LADDER honored (all work local on this account, $0), spec
before behavior change (module docstring first), fix comments carry
their receipts.

## FINDINGS

1. THE VORTEX IS LANDED (the seed thread, cycle 3: sketch to bytes).
   kind "vortex" is a rotor junction in mag/water_graph.py: inflow side
   a plain accumulator, outflow side a metering wheel over k = its LIVE
   outflow pipes (not fractured, open) in insertion order. One outlet
   emits per tick, the pipe at index rot % k; delivery is ordinary
   _move, so head law, siphon law, fracture law, and the waste hold all
   apply unchanged. rot advances ONLY when volume left through the
   chosen pipe (a blocked or dry outlet parks the rotor; a burst on its
   tick still turned it: the water left the hub). rot is stored in
   [0, k), R8-clamped at ingestion, zero RNG. Vortex outflow rides the
   gated-outflow phase slot AFTER gate verdicts; across vortices the
   order is first-live-outlet pipe insertion order. Mirrored in the
   Godot twin (roblox_to_godot/systems/water_graph.gd: WNode.rot,
   add_node rot, tick vortex_out + emission phase, to_dict rot) and in
   the graded head law (mag/hydrology.py inherits tick(); the rotor
   turns identically under _pipe_flow, pinned by test).
   What it computes, now real not sketch: round-robin demux (pinned:
   6 units through k=2 split 3/3 in 6 ticks), mod-k counting (pinned:
   k=3 sequence v0,v1,v2,v0,v1, counts 2/2/1, rot ends 5 % 3 = 2),
   parkable rotor (pinned: uphill second outlet parks the wheel at
   rot 1 with 5 units held at the hub: head-blocking is a rotor
   brake), and the gate-committed landing (below).

2. Vortex into a gate lands COMMITTED, then starves (pinned so nobody
   calls it a bug later). A vortex's outflow is a committed delivery
   (the same shape as today's gate-to-gate outflow), so a vortex
   feeding an xor bypasses the gate verdict: the pool lands, the xor's
   outflow never opens (no deferred inlet), and the standing STARVATION
   law spills the pool to the first waste on the next dry tick. Pinned
   end state: swirl 0, jx 0, pool 0, waste 2, conserved.

3. The cycle-1 steam roundtrip drop (finding 1) is FIXED, in BOTH
   from_spec sites. Base from_spec now passes steam (and rot) into
   add_node; the hydrology override's add_node had the same hole (it
   built HydroNode directly and dropped steam on every hydrology
   roundtrip) and is fixed too. The fix is one clamp site: add_node
   owns the R8 ingestion clamps for steam and rot (max(0, min(...)));
   from_spec just passes the ints. Pinned: boil 2 with no cold node,
   roundtrip keeps steam 2, second roundtrip byte-exact.

4. The valve lie (cycle 1 finding 4) is FIXED at both call sites.
   server/world.py _apply: a valve verb on a fractured pipe words the
   burst ("ada spins the valve on p_bypass; the pipe is burst (closed
   for good).") and changes nothing. mag/water_computer.py
   _graph_set_valve: same law ("Valve main spins free; the pipe is
   burst (closed for good).", ok True, no save). The engine's silent
   open() refusal stays as the backstop. Replay-safe: a valve-on-burst
   row cannot exist in any pre-law save doc (fracture is unreachable in
   stock play, cycle 1 finding 3; only the AJ4 test feeder stresses
   pipes and it writes no saves), so no old chain re-derives a
   different wording. Both paths pinned by tests.

5. Sill now has dedicated tests (cycle 1 finding 8, partially cured).
   Hold: one inlet vs sill 2 gives "Junction dam holds 1 below gate
   (1 < sill 2); pooling.", dam 1, pool 0. Pass: two concurrent inlets
   give "Junction dam sill reached (2 inlets).", pool 2, dam keeps 0.
   Still open from that finding: the docstring's "any" ghost kind
   (promised at the kind list, absent from the tick gating) and
   held-inlet event auditability (per-pipe lines for gate-held flows).

6. Hydrology ingestion is now R8-total (drive-by alignment, named).
   The add_node override previously bypassed the base clamps entirely:
   no volume, elev, steam, or rot clamp entered through hydrology.
   In-domain behavior unchanged (verified: the int-domain suite stays
   green); out-of-domain specs now clamp like the base declares. The
   R8 receipt's known residual (hydrology._move adds raw instead of
   _receive) remains, untouched, still named in both engines.

7. The snapshot node-shape pin grew the additive key (named, not
   silent). tests/test_server_v0.py asserted the exact node dict
   {"elev", "kind", "volume", "steam"}; rot joined it the same way
   steam (V-wave) and stress/fractured (AC2) did before: additive,
   always emitted, consumers updated. No persistence risk: restore
   re-derives from action rows, never from_spec (server/persistence.py
   receipt line 75 says so itself).

8. Residuals and observations carried forward, byte-backed:
   (a) the Godot parity runner (roblox_to_godot/tests/
   rule_parity_runner.gd) has NO vortex sequences yet; its frame
   format reads explicit fields, so the vortex changes cannot break it,
   but cross-engine vortex parity is unproven until a sequence lands
   (NEXT THREAD candidate);
   (b) `delivered` in WaterGraph.tick() is write-only (created line
   269, written 326 and 479, never read): a leftover of the first cut,
   harmless, one deletion to reclaim;
   (c) the module docstring's "any" ghost kind persists;
   (d) pre-existing red in the wider consumer sweep, stash-proven not
   mine: tests/test_k8s_water.py::test_ledger_workload_feeds_simulator,
   tests/test_propagator.py::test_agreement_law_100_sampled_cases,
   tests/test_propagator.py::test_agreement_covers_every_label (all
   three fail identically with my changes stashed).

9. Playing the vortex (the mariner's read, for the next rider): the
   rotor makes waste-placement order matter twice over (STARVED spill
   picks the first waste; the vortex demuxes by insertion order), and
   a vortex with mixed-height outlets is an analog switch: head-block
   one outlet and the wheel parks; unblock it and the stored pool
   drains in rotation. With a feedback pipe from an outlet back to the
   hub, the hub re-feeds itself and the rotor becomes a clock source
   (untested this cycle; the sim said period LCM(k1, k2) when chained).

## JOURNEY

1. Boot and resume check: read the pack, found two prior mariner
   receipts, read both; then verified cycle 2's thread state before
   trusting it: grep "vortex" over mag/ and tests/ (zero files), git
   log on the water files (last touch 066ba7ef0, no landing), no
   20261009 probe file, no working-tree vortex bytes. Verdict: cycle 2
   died after its stub; the thread was intact and unowned. Learned the
   claim grammar from the 10-09 sidecar and read scripts/run_mate.ps1
   in full (the runner contract, the model pin, the storage isolation).
   Appended my claim line to the sidecar, filed this receipt's stub
   before any speech.
2. Read the hunting ground fresh, bytes not memory: water_graph.py
   (465 lines, unchanged since cycle 1's read), the Godot twin
   water_graph.gd (517), both valve call sites (server/world.py _apply,
   water_computer._graph_set_valve), hydrology.py in full (172: the
   subclass overrides _available/_move only, so tick() is inherited and
   a rotor rides both head laws), campaign seed/valve plumbing
   (seed_graph, _room_pipe, _save_graph overlay), the world's
   stage/validate contract, persistence restore (from_spec-free by
   design), the rule parity runner (explicit field reads, safe), and
   the int-domain tests (no pin on the override's ingestion). Why: the
   landing surface is five files, not one; a vortex that diverges from
   its twin is a cross-engine lie.
3. Spec before behavior: wrote the VORTEX law block into the
   water_graph.py module docstring (kind semantics, metering, parking,
   phase slot, determinism, R8, twin mirror, seed receipt) BEFORE any
   code; named the valve-honesty duty at open() and the hydrology
   ingestion gap in their own comments with receipts. Why: build
   discipline; the docstring is the spec that owns node kinds.
4. Landed the engine: Node.rot field, add_node steam/rot with R8
   clamps, tick() out_kinds deferral + vortex_out grouping + the rotor
   emission phase after gate outflows, to_spec rot, from_spec steam+rot
   (the finding-1 fix riding the same edit, comment carrying the
   receipt family).
5. Landed parity: hydrology import/add_node/from_spec (steam and rot,
   plus the base clamps); the Godot twin (header law block, WNode.rot,
   add_node rot clamp, tick out_kinds + vortex_out + emission loop,
   to_dict rot). Why: one law, three engines (Python verdict, Python
   graded, GDScript), or it is not a law.
6. Landed the valve honesty at both call sites, with the replay-safety
   analysis written where the next seat will read it (the _apply
   branch).
7. Wrote 12 new test functions (7 vortex, 1 steam roundtrip, 2 sill,
   1 campaign valve, 1 world valve), mirroring the suite's physics-law
   grammar with traced arithmetic in every assert comment.
8. Dead end (my test bug, caught by the run): the roundtrip test used
   a k=1 vortex, where (0+1) % 1 = 0, so rot could never read 1 and
   the assert was unsatisfiable as written. Fixed by giving the board a
   second outlet (k=2, one delivery parks rot at 1).
9. Dead end (my test bug, caught by trace): the hydrology parity test
   boiled the hub AFTER 6 ticks, but the hub was dry (all 6 delivered),
   so boil lifted 0 and the steam assert could never fire. Fixed by
   boiling a fed node.
10. Dead end (shape pin, expected): test_server_v0's exact-dict
   snapshot assert rejected the additive rot key. Updated the pin with
   the family note (steam and AC2 keys joined the same way); no
   persistence risk, restore never calls from_spec.
11. Dead end (editing slip, caught before any run): one edit clobbered
    the srv line of test_two_clients_see_identical_broadcast_bytes;
    restored it in the next edit and verified by grep count (10
    _start_server calls, as before).
12. Verification turn: ran the 8-file water family (109 passed, 0
    failed, 78.36s), then the 18-file consumer sweep (297 passed, 3
    failed). The 3 failed (k8s_water, 2x propagator) reproduced
    identically with my changes git-stashed: pre-existing red, not
    this cycle's. Stash popped clean, changes intact.
13. Gate turn: violation_ratchet check --changed PASS (NEW=0; my
    water_graph.py growth 465 -> 534 rides the registered GROWTH claim,
    named here for the operator: re-audit or re-accept at push).
    citation_lint check --changed: blocking=0, exit 0, 45 warns all on
    sibling prose (hermes_burn, MICKEY17, PARABLE, dungeon errata).
14. Em-dash sweep over my new bytes: 1 found (the vortex test file
    header), killed on the spot; this receipt at 0.
15. Closed the loop: rewrote this receipt in full, appended a closure
    note to cycle 2's OPEN stub (amend-not-rewrite: dated, signed,
    pointing here), appended the CLOSED verdict to the pack sidecar.
    Concurrency 1 throughout; no env vars printed; $0 spent.

## COUNTS

- Product files changed this cycle: 5 (mag/water_graph.py +85/-9,
  mag/hydrology.py +30/-5, mag/water_computer.py +12, server/world.py
  +14/-1, roblox_to_godot/systems/water_graph.gd +47/-3; git diff --stat
  insertions/deletions read at close).
- Test files changed: 3 (+48, +22, +25 lines: test_water_graph.py,
  test_water_graph_campaign.py, test_server_v0.py) plus 1 new file
  (tests/test_water_graph_vortex.py, 132 lines, 7 tests).
- New test functions: 12 (7 vortex, 1 steam roundtrip, 2 sill,
  1 campaign valve, 1 world valve).
- Water family floor: 109 collected / 109 passed / 0 failed, 78.36s,
  8 files (test_water_graph 22, vortex 7, starvation 8, int_domain 20,
  campaign 10, hydrology 15, water_computer 7, server_v0 20; per-file
  collect counts read from pytest --collect-only -q this window).
- Cycle-1 floor comparison: those same 5 files read 63 passed then,
  67 now (+4: 3 in test_water_graph, 1 in campaign); the 8-file floor
  adds hydrology 15, water_computer 7 (already in the 63), server_v0
  20, vortex 7 against cycle 1's 63/5-file shape.
- Wider consumer sweep: 18 files, 300 collected, 297 passed, 3 failed
  (pre-existing, stash-proven: identical failures with the tracked
  changes stashed).
- Gates: ratchet PASS NEW=0 (6 hits all registered); citation lint
  blocking=0, 45 warns (0 on my files), exit 0.
- water_graph.py line span: 465 -> 534 (+69 on disk; the diff counts
  above are insertions-vs-deletions, the ratchet's number is the file
  total; both named so no one differences them).
- Vortex pins: k=2 alternation 3/3 in 6 ticks conserved 6; parking
  1 delivery then rot parked at 1, hub keeps 5; k=3 sequence
  v0,v1,v2,v0,v1, counts 2/2/1, rot 2; gate-committed landing 2 units
  then STARVED spill to waste 2, pool 0; roundtrip steam 2 and rot 1
  survive twice; graded-law parity 3/3, rot 0; determinism
  byte-identical rerun.
- Valve honesty pins: 2 of 2 call sites (world + campaign), each
  asserting the burst wording, the absence of the old lie, and the
  unchanged state.
- Em-dashes in this receipt: 0. Concurrency peak: 1 process. Paid API
  calls: 0. Env vars dumped: 0.
- Probe artifacts: 0 new files (this cycle landed code + tests, the
  probe battery was cycle 1's instrument; every former probe claim
  re-proven by the suite pins above).

## NEXT THREAD (self-chosen, for the next cycle)

Vortex parity sequences in the Godot rule runner: add vortex families
to the parity sequence generator so cross-engine rotor behavior is
proven, not mirrored-by-eye; then the chained-rotor clock (feedback
pipe, LCM period) as a real engine pin. Ride-along candidates from the
residuals: the write-only `delivered` dict (one deletion), the "any"
ghost kind (spec says it exists; the tick disagrees), and held-inlet
per-pipe event lines (pooled provenance). The k8s_water/propagator
pre-existing red belongs to whoever owns those lanes; the mariner only
names it.

Resume note: no mid-road stop. Cycle 3 closed at a boundary; the next
cycle resumes by id mariner with the thread above.
