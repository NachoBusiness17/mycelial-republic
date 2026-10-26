# Receipt: mariner mission 20261012 (cycle 5, complete)

Mate: THE MARINER. Pack: logs/mates/missions/mission_20261012_07_mariner.md
(claimed via its .claim sidecar at 08:25:11, OPEN line appended; CLOSED
line appended at window close).

Status: COMPLETE. Stopped at a clean boundary, not context death, not
mid-road. Launch stub was filed in this file before any speech, per
contract, and rewritten here at window close.

Resume note: cycle 1 (receipt_20261006_mariner.md) sketched the vortex.
Cycle 2 (receipt_20261009_mariner.md) died with zero bytes. Cycle 3
(receipt_20261010_mariner.md) landed the vortex node kind in three
engines. Cycle 4 (receipt_20261011_mariner.md) proved the clock law and
the DAG law, struck the ghost kinds, and left a self-chosen NEXT THREAD:
THE LATCH, the water computer's first memory element. Cycle 5 resumed by
id mariner, verified the thread state first (vortex law in
mag/water_graph.py, 13 pins in tests/test_water_graph_vortex.py at 340
lines, the delivered-deletion comment at the _move seam: all on disk as
cycle 4 claimed), then rode the latch thread to bytes.

Working-tree note (named, not silent): cycles 3-5's water bytes are all
uncommitted at cycle 5 close (no commit was asked of any cycle). Diff-
vs-HEAD on the water files mixes three cycles' bytes; the COUNTS section
separates them by naming cycle 5's exact deltas. Sibling-dirty porcelain
entries (380+ at claim time) were already on the tree; none touched, none
stashed.

Laws held: em-dash 0 (added lines of all six changed files scanned, plus
the full new test file, 0 hits), real counts only, no fabricated
anything, no env dumps, RAM gate respected (in-memory graphs, largest
board 5 nodes), rolling concurrency respected (concurrency peak 1
process), drop-ledger awareness (this receipt names searchable terms:
water_graph latch level pool memory element sill roundtrip vortex
divider), receipt before speech, positive steering (one test failure and
one probe catch were recorded and fixed, no spiral). COMPUTE LADDER
honored per the STEER row: all work local on this account, zero paid API
calls, Nous/Hermes untouched; Task agents not needed this cycle (single-
seat probe-and-pin work).

## FINDINGS

1. THE LATCH IS LANDED (the cycle-4 NEXT THREAD, now bytes): kind
   "latch" is a POOL-LEVEL gate. Its `sill` field is its LEVEL (clamped
   >= 1 at evaluation; the wire format needed no new field). The gate
   verdict reads the POOL, standing volume plus this tick's deferred
   inflow, against the level: allow = (volume + inflow) >= max(1, sill).
   PASS: inflow lands, the gated outflow drains under the ordinary
   phase, announcing "Latch X opens (pool P >= level L)." FAIL: inflow
   lands ("Latch X holds pool P below level L; pooling.") and THE POOL
   KEEPS: a latch NEVER STARVED-spills. It is the sill's drain-on-dry
   pin (cycle 4, finding 6) standing contrast, landed as a both-kinds
   test. Landed in mag/water_graph.py (verdict branches + docstring
   LATCH block) and the Godot twin roblox_to_godot/systems/water_graph.gd
   (gated_kinds, verdict mirror, docstring block, kind comment), one
   law, two engines; mag/hydrology.py inherits tick() unchanged and the
   graded-law pin proves it; server/world.py and mag/water_computer.py
   needed ZERO bytes (no kind logic in either; named, verified by read).

2. THE ONLY GATE THAT ACTS ON A DRY TICK: a charged latch's verdict
   passes with ZERO deferred inlets (the pool alone meets the level),
   so it discharges on a dry tick. The xor needs exactly one inlet, the
   sill needs N, the vortex needs no gate but never gates its inflow;
   the latch is the family's first dry-tick actor. Pinned with an exact
   two-event list on an all-feeds-dry tick.

3. THE SILL CONTRAST, PINNED BOTH WAYS: the identical board (two cap-1
   inlets, one cap-1 outflow, one standing unit, then all ticks dry)
   with kind sill STARVED-spills its standing unit to the first waste
   (waste 1); with kind latch it keeps the unit in silence forever
   (waste 0, tank 1). No STARVED line ever fires on a latch board. This
   is the memory law in one picture: the gate forgets, the latch
   remembers.

4. ROTOR + LATCH = THE DIVIDER (the seed thread's arithmetic closes):
   a k=3 vortex round-robining one outlet into a level-2 latch charges
   1 unit per 3 ticks; the latch fires one outflow unit on the dry tick
   after each charge, exactly one out unit per three swirl units, with
   the event order pinned (verdict announcement, outflow drain, then
   the vortex's own emission: the phase law). The vortex is the
   oscillator, the latch is the counter: the rung where the water
   computer starts computing finite-state machines, as cycle 4
   projected. Pinned end to end: 9 units, conserved, rot 0.

5. LATCH CHAINS ARE PIPELINES OF INTEGRATORS: two level-2 latches in
   series each add one tick of latency and keep a floor of 1; a 4-unit
   charge through the chain delivered 2 and stored 1 per stage. A
   gate's outflow lands in a downstream latch COMMITTED (no verdict
   sees it: the vortex-into-xor shape from cycle 3, finding 2), so
   chains charge across ticks and carry state between reads. Pinned
   with the exact t4 event order: both verdict announcements precede
   all outflow moves (A then B by insertion order; ab then bo by pipe
   order).

6. TO_SPEC NEVER EMITTED `sill`, AND THE LATCH MADE THAT A BUG (the
   cycle's flagship hunt find, fixed): a bare spec roundtrip
   (snapshot() included; only the campaign path's _save_graph overlay
   ever preserved sill) silently reverted a latch's LEVEL to 0, whose
   gate then evaluates at level 1: a memory element that forgets its
   threshold on every save-load. This is the third member of the
   roundtrip drop family after primed (LW5) and steam+rot (cycle 3),
   but the first one that changes GATE BEHAVIOR, not just bookkeeping.
   Fixed under the additive-key family law (steam, then rot, now sill):
   to_spec always emits sill, from_spec already passed it, the twin's
   to_dict mirrors it, and the two exact-dict pins in the suite grew
   the key with family notes (tests/test_water_graph_vortex.py swirl
   assert, tests/test_server_v0.py spring assert). No persistence risk
   in stock play: the world restores from action rows, never from_spec
   (server/persistence.py), and the campaign overlay already kept sill.

7. EVENT HONESTY: the gate names the EFFECTIVE level. My own probe
   board (sill 0) caught the first cut printing "pool 1 >= level 0"
   while the gate had evaluated the clamped level 1: an event that
   misstates its own gate is a log lie (the valve-honesty family).
   Both engines now print max(1, sill) in the opens and holds lines.
   Below level on a dry tick the latch is SILENT (no state change, no
   event; the pool reads in the snapshot and glass), while a charged
   latch announces its open verdict EVERY tick, the sill's per-tick
   grammar, even when its outflow is blocked or absent: the verdict is
   true per tick, the water leaves or does not under the ordinary
   laws. Both grammars pinned.

8. What the latch computes (probed, then pinned): charge-and-regulate
   (under continuous cap-1 feed a level-3 latch reaches steady state
   in 3 ticks and passes exactly cap-1 per tick, storing the excess,
   never spilling); a hysteresis floor of level-1 that a full
   discharge always leaves (the memory's resting charge); the divider
   (finding 4); the integrator chain (finding 5). Deterministic, zero
   RNG, R8 rides _receive unchanged (no new increment sites).

9. Residuals carried forward: (a) Godot parity sequences for vortex
   AND latch remain UNPROVEN: still no godot or godot4 binary on this
   box; the twin mirror is landed line-for-line and the Python suite is
   the executable pin (cycle-3 precedent). (b) Held-inlet per-pipe
   provenance lines (cycle 3 residual) skipped again for scope; still
   safe to land later (membership-based asserts). (c) The R8 named
   residual (hydrology._move adds raw instead of _receive) remains,
   untouched, still named in both engines. (d) The three pre-existing
   reds (test_k8s_water.py::test_ledger_workload_feeds_simulator,
   tests/test_propagator.py::test_agreement_law_100_sampled_cases,
   tests/test_propagator.py::test_agreement_covers_every_label) fail
   identically to cycles 3 and 4's stash-proven list; no fresh stash
   this cycle (380+ sibling-dirty entries; the claim rides cycle 3's
   byte-backed stash proof plus failure-id identity). (e) Ratchet
   GROWTH advisory on mag/water_graph.py (accepted at 465, now 618:
   cycle 3's +69, cycle 4's +17, cycle 5's +67) rides cycle 3's
   registered claim; the operator re-audits or re-accepts at push.
   (f) The per-tick opens announcement on a charged, fully blocked
   latch repeats forever: honest-but-loud; a rising-edge announcement
   would need a stored was_open bit (schema churn across to_spec/
   from_spec/twin/snapshot: rejected this cycle, named for the
   operator). (g) The vortex-into-xor committed landing still starves
   pools to waste (cycle 3, finding 2): with the latch landed, board
   authors can now route vortex outflow into a latch and the starve is
   avoidable by design; changing the campaign default board is game
   design, operator territory, named not done.

## JOURNEY

1. Boot and claim: read the pack; read cycle 4's and cycle 3's receipts
   in full; learned the claim grammar from the 10-10/10-11 sidecars;
   claimed via the OPEN line (08:25:11); filed this receipt's stub
   before any speech. Verified cycle 4's thread state by bytes (vortex
   law, 13 pins, delivered-deletion comment: all present).
2. Read the hunting ground fresh, bytes not memory: mag/water_computer.py
   in full (graph mode routes through WaterGraph: zero bytes needed for
   the latch; the _save_graph overlay note read closely since it claims
   sill-keeping), server/world.py in full (validate/stage/tick/_apply:
   zero kind logic anywhere), mag/hydrology.py in full (inherits tick();
   overrides only _available/_move: the latch comes free, one pin
   proves it), the twin's tick region lines 244-371 and to_dict, and
   water_particles.gd's churn painter (keyed on xor/sill only).
3. Ghost check: grep for "latch" as a node kind across mag/, tests/,
   server/, roblox_to_godot/: all hits are English words (latched
   window, prime latch, log latching), zero kind usages. The name was
   free.
4. Spec-first: wrote the LATCH law block into the module docstring
   (semantics, contrast, event grammar, computes-list) BEFORE any
   engine byte; mirrored the block into the twin's header. Why: the
   docstring is the spec that owns node kinds (cycle-3/4 precedent).
5. Engine edits: gated_kinds += "latch"; the verdict loop grew the
   latch branch (pool-level allow) and the memory law in the fail
   branch (land, name the hold, never STARVED, silent when dry);
   out_kinds and the gated-outflow phase picked the latch up without
   further edits; the tick docstring's three-phase note now reads
   XOR/sill/latch.
6. Twin mirror: same branches in GDScript, plus the kind comment and
   to_dict sill. Ride-along: water_particles.gd's churn painter now
   sees a pooled latch (held water churns; one condition + comment).
7. Probe round (temp script, single process, in the temp dir): P1
   charge/open/steady traced (fires every tick from t3, floor 2 kept,
   conserved 6); P2 the divider traced (fires on the dry tick between
   rotor feeds, phase order exact); P3 the sill contrast traced (waste
   0 vs the sill's 1); P5 the chain traced (t4 double verdict, t5 solo
   B fire, floors 1+1); P0 the clamp caught the level-0 event lie.
   Dead end (my probe bug, transient): a P3 self-check one-liner
   crashed on a botched lambda re-run; the P3 board itself was already
   traced clean, so the check was dropped and the pin carries the
   truth. No spiral, recorded per positive steering.
8. Fix from the probe: both engines' latch event lines now name
   max(1, sill), not raw sill (finding 7). Why: honesty beats brevity
   in an event log.
9. Test landings: tests/test_water_graph_latch.py, 8 pins, each with
   the traced arithmetic in its docstring per the suite's grammar.
10. FINDING mid-pin (before any run): re-reading to_spec for the
    roundtrip pin showed sill was NEVER emitted (the campaign overlay
    comment said so in hindsight). Fixed to_spec + twin to_dict +
    the two exact-dict suite pins (findings 6).
11. Dead end (my test bug, caught by the run): the chain pin asserted
    the t4 event list after only one tick; the run showed t2's events
    and the assert diff made the missed ticks obvious. Fixed by walking
    the full trace (t1-t5 with asserts, then 3 silent ticks). Same bug
    class as cycle 4's journey turn 12; the run caught it, the fix is
    the pin.
12. Verification turns: latch file alone 8 passed / 0 failed (0.69s);
    water family floor 9 files 124 passed / 0 failed (62.26s); wider
    consumer sweep 10 files 193 passed / 3 failed, the 3 being the
    exact pre-existing ids from cycles 3 and 4.
13. Gate turn: ratchet PASS NEW=0 (GROWTH advisories 4: water_graph.py
    rides cycle 3's claim, named in finding 9e; gps_mcp ledger, its
    test, and mesh_delta are sibling lanes' claims). Citation lint FAIL
    blocking=9, ALL in watch/inbox/gap_analysis_20261010/GAP_REGISTER.md
    (a sibling lane's prose, never touched by me; 1 EMPTY-SPAN + 8
    PHANTOM-NUMBERs), warns 104, none blocking on my six files; named,
    not accepted, not mine to fix.
14. Em-dash sweep: 0 in the added lines of all six changed files, 0 in
    the full new test file.
15. Closed the loop: rewrote this receipt in full, appended the CLOSED
    line to the sidecar. Concurrency 1 throughout; no env vars printed;
    $0 spent; probe scripts stayed in the temp dir (2 files; every
    probe claim re-proven by a named test above).

## COUNTS

- Product files changed by cycle 5: 3 (mag/water_graph.py 551 -> 618 on
  disk, +67 this cycle: LATCH docstring block, verdict branches, memory
  law, event fixes, tick-docstring note, to_spec sill + fix comment;
  roblox_to_godot/systems/water_graph.gd: LATCH header block, kind
  comment, gated_kinds, verdict mirror, to_dict sill + comment;
  roblox_to_godot/systems/water_particles.gd: churn condition + comment).
- Files NOT changed, verified zero-byte-needed: mag/hydrology.py
  (inherits tick; graded pin proves it), mag/water_computer.py (graph
  mode is kind-blind), server/world.py (kind-blind; overlay note).
- Test files changed by cycle 5: 3 (new tests/test_water_graph_latch.py,
  8 tests; tests/test_water_graph_vortex.py: swirl assert grew sill +
  family note; tests/test_server_v0.py: spring assert grew sill + family
  note).
- New test functions: 8 (charge/regulate, dry-tick discharge, sill
  contrast, rotor divider, integrator chain, roundtrip + graded law,
  clamp + announcement grammar, determinism).
- Water family floor: 124 collected / 124 passed / 0 failed, 62.26s,
  9 files (cycle 4's floor read 116 / 8 files: +8 is exactly this
  cycle's new tests; zero sibling drift in the family).
- Wider consumer sweep: 10 files, 196 collected, 193 passed, 3 failed
  (pre-existing: identical ids to cycles 3 and 4's stash proofs).
- Floor + sweep totals: 19 files, 320 collected, 317 passed, 3 failed
  (all 3 pre-existing, named above).
- Gates: ratchet PASS NEW=0 (18 hits all registered; GROWTH advisories
  4, named in finding 9e); citation lint blocking=9 (all
  gap_analysis_20261010/GAP_REGISTER.md, sibling), warns 104, blocking
  on my files 0.
- Em-dashes: 0 (added lines of 6 changed files; full scan of the new
  test file; this receipt).
- Probe artifacts in the repo: 0 (2 temp scripts in the temp dir,
  single process, in-memory; every probe claim pinned by a named test).
- Latch pins: charge/regulate steady state conserved 6 with floor 2;
  dry-tick discharge exact 2-event list conserved 3; sill contrast
  waste 0 vs 1 same board; divider 9 units exact mark list including
  the phase order; chain t4 exact 5-event list conserved 4; roundtrip
  byte-exact twice on both engines; clamp announce grammar exact;
  determinism byte-identical.
- My bugs caught and fixed this cycle: 2 (the level-0 event lie, by my
  own probe before any test; the chain pin's missed ticks, by the run).
- Paid API calls: 0. Env vars dumped: 0. Concurrency peak: 1 process.
  Godot executions: 0 (no binary on box).

## NEXT THREAD (self-chosen, for the next cycle)

THE RIPPLE COUNTER AND THE DIFFERENCE DETECTOR: the FSM rung made real
with the parts the estate now has. (a) A water ripple counter: a vortex
feeding a latch chain where each stage's level halves the fire rate
(divide-by-L chains): multi-stage counting with carry between latch
stages, pinned end to end with exact mark lists. (b) A difference
detector: two independent pulse trains (two vortex wheels) feeding one
xor, the xor feeding a latch: the latch charges only on disagreement
ticks, so its pool is the accumulated disagreement of two clocks: the
first water circuit that computes a relation between two signals rather
than routing one. Ride-alongs: Godot parity sequences for vortex and
latch (still blocked on a box with a Godot binary; both sequence
families are now fully specified by the Python pins), held-inlet
per-pipe provenance lines (still safe, still small). The GAP_REGISTER
citation debt, the k8s_water/propagator reds, and the water_graph.py
GROWTH re-audit belong to their own lanes; the mariner only names them.

Resume note: no mid-road stop. Cycle 5 closed at a boundary; the next
cycle resumes by id mariner with the thread above.
