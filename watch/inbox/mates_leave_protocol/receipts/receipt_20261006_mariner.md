# Receipt: mariner, 20261006 (cycle 1, complete)

Mate: THE MARINER. Pack: logs/mates/missions/mission_20261006_07_mariner.md.
Cycle 1 rode in full and stopped at a clean boundary (not context death, not
mid-road). Launch stub was filed in this file before any speech, per contract.
Probe artifact: watch/inbox/mates_leave_protocol/probes/mariner_probes_20261006.py
(full JSON output from its run, 9 probe families, all green). Product files
changed this cycle: 0.

Hunting ground: mag/water_graph.py (465 lines), mag/water_computer.py (1013
lines), server/world.py (416 lines). All three read in full this cycle.

## FINDINGS

1. from_spec drops node steam (LW5-class roundtrip drop, latent, masked).
   mag/water_graph.py:429-441 (to_spec emits per-node steam) vs
   mag/water_graph.py:444-450 (from_spec passes elev/kind/sill/volume, never
   steam; Node defaults steam=0). Probe p1: graph boiled 2 units, spec carried
   steam=2, after from_spec steam=0, roundtrip not byte-exact. Masked in every
   live path today: world mode condenses steam the same tick it boils (crown
   is always present, crown volume 0 in stock play), and campaign mode maps
   the boil verb to the to_gas phase change (water_computer.py:860-864), never
   to graph.boil, so node steam never crosses a save boundary. Also masks
   tests/test_water_graph.py test_roundtrip_spec:110 (its graph holds zero
   steam, so the exactness assert passes blind). Blast radius includes
   mag/estate_bridge.py:364 (water_graph_tick roundtrips a caller-held spec
   through from_spec per call). Fix shape for next cycle: one line in
   from_spec (steam=int(n.get("steam", 0))) plus a steam-carrying roundtrip
   test; same family as the LW5 primed fix and the AC2 stress/fractured fix.

2. Gated-inlet siphons never break their prime. mag/water_graph.py:344-360
   (_available) has no break path; the break law lives only in _move
   (mag/water_graph.py:391-395), which gated inlets never reach. Probe p3:
   plain siphon primes, breaks on a dry intake ("Siphon sip breaks (intake
   dry)."), re-primes on refill; the identical siphon feeding an xor held
   primed=True through 3 observed dry ticks with zero break events, then on
   refill flowed immediately with no prime event ("sip_in: 1 tank->gate.").
   Physics consequence: a siphon into a gated junction pays its crest once and
   is then a permanent cap-1 channel across dry spells, while the same
   geometry into a plain node re-pays crest after every dry spell. One
   behavior split by destination kind; no test names it (the break test
   covers only the plain path).

3. Fracture is unreachable in world v0 stock play. Probe p4: 500 idle ticks
   on the stock Mountain board with the bypass forced open: max stress per
   pipe p_spring 3, p_terrace 3, p_out 2, p_drain 4, p_bypass 3, against
   thresholds 236 / 210 / 335 (band [200, 400]). Conservation bound: the
   world holds 8 units total, the board is a DAG with terminal sinks (crown
   has no outlet; waste holds), and no world verb adds liquid anywhere (verbs
   boil/valve/join/say/tag/whisper; steam condenses only at the crown, which
   is terminal), so no pipe can ever carry more than 8 cumulative units. The
   B1 seam fix made the artery stressable only under the AJ4 test feeder (a
   fed source refilled each tick), which the world server cannot express.
   Consequence: fracture AND finding 4 are unreachable in v0 play; both are
   reachable in campaign graph mode through seeded specs with large volumes
   (seed_graph accepts any spec).

4. Valve events can assert an open the engine refused (the hash-chain lie).
   server/world.py:363-370 (_apply valve toggle) words the event before the
   engine's verdict; mag/water_graph.py:158-164 (open) refuses a fractured
   pipe SILENTLY, so the row claims success. Probe p5a: p_spring burst first
   (probe-injected stress at threshold, then one flow tick), then a valve
   verb: the chained row reads "u1 opens p_spring." while the pipe stays
   open=False, fractured=True. Probe p5b (campaign path, same shape):
   "Valve main open." while main.open=False, main.fractured=True. Replay
   stays consistent (the refusal is deterministic, persistence re-derives the
   same state), but the log's prose is false while its state effects are
   true. Fix shape: validate() rejects a valve verb on a fractured pipe with
   its own why-code, or the event text names the burst ("the valve spins
   free; p_spring is burst"). Fix at BOTH call sites (world and campaign).

5. The starvation spill is elevation-free liquid transport (the starvation
   lift). mag/water_graph.py:320-332: the STARVED spill routes the pooled
   volume to the FIRST waste node in insertion order, no elevation rule. Probe
   p6: an xor at elevation 2 spilled 2 pooled units to a waste node at
   elevation 9 (uphill, event verbatim: "Junction gate STARVED: 2 pooled
   units spilled to waste at basin"); probe p6b: with two waste nodes (elev 9
   first-inserted, elev 0 second), the first-inserted got all 2 units, the
   lowest got 0. Play mechanic nobody has ridden: engineer one no-inflow tick
   (close both inlet valves) and a gated junction teleports its whole pool to
   whatever node sits first in the waste insertion order; boil it back from
   there. Waste placement order becomes routing power. The V5 receipt chose
   "first waste in insertion order" deliberately; the uphill consequence and
   the order-dependence were never named.

6. Steam with no cold node is a permanent parked sink. Probe p2: 3 boiled
   units, 3 ticks, steam reads 3, 3, 3, node volume 0. The module docstring
   line "falls back to its origin node when no cold node exists"
   (mag/water_graph.py:23) describes a no-op: the steam never leaves, and it
   also never condenses; the mass is unrecoverable without constructing a
   cold node after the fact. No test covers steam-without-cold.

7. SEED THREAD ANSWER: the water graph can host a vortex node, and it would
   compute the estate's first sequential primitive. Evidence chain:
   (a) the xor eats symmetric streams: probe p7a, two full cap-1 feeds into
   one xor, 8 units in, 0 reach the downstream pool, 8 pool at the junction
   (both-inlet ticks never pass; overflow is the law);
   (b) turn-taking cannot be built from existing parts: probe p7b, staggered
   crests (2 and 4) on two siphons from one fat source primed on the SAME
   tick (both probe the full source volume before the LW5 reservation), 0
   gate passes. Dead end, named;
   (c) the vortex sketch (probe p7c, clearly labeled sim, NOT mag code): a
   vortex node holds a rotation register r, emits min(cap, volume) on outlet
   r only, then advances r=(r+1)%k. k=2, two feeds: 8 units delivered in 8
   ticks, 4/4 per outlet, conserved. k=3: 3/3/2. A k-outlet vortex is a
   mod-k counter; k=2 chained with k=3 composes to period LCM(2, 3)=6.
   Design spec block for a spec-first landing next cycle:
     kind "vortex"; k = number of pipes whose src is the node (insertion
     order); field rot:int; vortex outflows ride the existing gated-out
     phase slot; delivery is ordinary _move (stress/fracture/spray laws
     apply unchanged; a k-vortex spreads full-bore wear across k pipes, 1/k
     wear rate each); to_spec/from_spec must carry rot (the LW5 one-line
     family) or the roundtrip bug class repeats; R8-safe (rot < k, tiny);
     determinism from insertion order plus rot, zero RNG; the Godot twin
     (water_graph.gd) must mirror.
   What it computes: round-robin demux (turns xor overflow into alternating
   pass), mod-k clock divider, period multiplication by chaining (LCM), and
   with a feedback pipe a self-clocking sequence source. The graph today has
   combinational gates (xor, sill), a latch (siphon prime/break), a fuse
   (fracture), and a second medium (steam); the vortex is the missing rotor.

8. Coverage blind spots in the water suite. Census: 67 test functions across
   6 water test files (grep "def test_" over tests/test_water_*.py). Named
   gaps: zero dedicated sill-gate tests (probe p9 pins the behavior by hand:
   one inlet vs sill 2 holds with event "Junction dam holds 1 below gate
   (1 < sill 2); pooling."; two CONCURRENT inlets pass with "Junction dam
   sill reached (2 inlets)." and 2 units reach the pool, dam keeps 0); the
   kind "any" promised by the module docstring (mag/water_graph.py:20) is
   absent from the Node kind list (line 107) and from the tick gating, so an
   "any" node behaves as a plain accumulator with same-tick pass-through
   (probe p9: the unit flowed sa->hub->pool in ONE tick); the roundtrip test
   is steam-blind (finding 1); held-inlet flows emit no per-pipe event lines
   (probe p4: event parse read 1 unit for p_spring while the engine's own
   stress ledger read 3, because gate-held deliveries are only summarized in
   the aggregate "holds N below gate" line), so pooled provenance is not
   auditable from the event stream alone.

9. The self-solving mountain and the drain-battery win. Probe p8: the stock
   board with ZERO valve touches fully drains in 8 ticks (every stock valve
   ships open; waste ends at 8, everything else 0), then 4 boil verbs at the
   waste basin lift 4 units to the crown and winner flips true at 12 ticks
   total, world conserved at 8 throughout. The V5 waste-hold law turned the
   sewer into a win battery: the minimal honest win rides water UP from the
   lowest node as steam. Also pins that boil-at-waste validates (volume > 0
   gate at server/world.py:258 passes on held waste).

10. Doc drift, low grade, named not fixed: the fracture class docstring says
    "at 200 + name_hash(name) % 201 it FRACTURES" while the pinned law is
    strict-greater (burst at threshold+1, tests/test_water_graph.py:228-247);
    the sill docstring says "total inflow >= a threshold" while the code
    counts INLETS, not volume (probe p9 grammar "1 < sill 2" counts pipes);
    the "any" ghost kind (finding 8).

## JOURNEY

1. Booted per pack: read the mission pack, located the three hunting-ground
   files, checked the receipts directory (empty: no prior mariner receipt,
   nothing to resume), filed the launch stub before any speech.
2. Read mag/water_graph.py, mag/water_computer.py, server/world.py in full,
   then censused 67 water test names across 6 files to map what the suite
   forces vs never forces. Why: the pack's target is physics the tests never
   touch; the census is the map of the dark.
3. Turn: read every module docstring promise against the code (steam
   fallback, the "any" kind, the fracture band, sill semantics). Why: doc vs
   code drift is where unplayed mechanics hide. This turn produced findings
   1, 6, 8, 10 on reading alone.
4. Turn: wrote the 9-family probe battery instead of trusting reads, filed
   it in the indexed world, ran it under the repo venv. Why: the mariner
   believes flows, not prose; byte truth only.
5. Dead end (mine, not the engine's): probe p5 version 1 staged the open
   verb BEFORE the burst, so the pipe legally opened and then burst in the
   same tick; the row was honest and the probe proved nothing. Fixed by
   re-sequencing (burst first, then verb); the lie then showed in both the
   world and campaign paths. Also dead-ended a sloppy one-liner rerun
   (string-replace clobbered def lines) and simply reran the whole battery.
6. Dead end (probe bug, fixed): p9 v1 starved the sill's second source
   across ticks, so the pass case never saw two concurrent inlets; and the
   "any" assert read the hub after its same-tick pass-through. Rewrote both
   cases cleanly; sill hold and pass now both pinned by hand.
7. Turn: fracture reachability. Why: the B1 receipt claims reachability via
   a test feeder; the mariner checked whether the WORLD can express that
   feeder. It cannot (finding 3): 500-tick board run plus conservation
   arithmetic. Dead end as an in-play mechanic; alive in campaign seeded
   specs, which is exactly where finding 4 lives.
8. Turn: starvation spill elevation audit. Why: V5 chose "first waste in
   insertion order" and nobody had asked what elevation does. Answer: nothing
   (finding 5): uphill spill and order-dependence both confirmed.
9. Turn: the seed thread. Why: the pack names the skyrmion steal and asks
   whether the graph can host a vortex and what it would compute. Rode it in
   three legs: xor symmetric-feed baseline (real engine: 0 of 8 delivered),
   staggered-crest alternation attempt with existing parts (dead end, named,
   same-tick priming), then the vortex sketch sim (mod-k counter, LCM 6,
   conserved 8/8). Closed the thread with the design spec block in finding 7
   so the next cycle lands code spec-first instead of re-deriving.
10. Ran the hunting ground's regression floor before claiming anything:
    63 passed in 59.58s (tests/test_water_graph.py, test_water_graph_
    starvation.py, test_water_graph_int_domain.py, test_water_graph_campaign.
    py, test_water_computer.py), zero failures.
11. Filed this receipt (drop-ledger terms: water_graph, fracture, vortex,
    sill, xor, from_spec steam, siphon prime, MountainWorld, starvation
    spill, valve event). No environment variables dumped anywhere; the probe
    file reads no env; no secrets touched.

## COUNTS

- Product files changed this cycle: 0 (probe + receipt only).
- Hunting-ground lines read in full: 1,894 (465 + 1013 + 416), plus test
  excerpts (test_water_graph.py through line 392 of 401,
  test_water_graph_int_domain.py lines 190-219 of 306).
- Water test functions censused: 67 across 6 files.
- Regression floor run today: 63 passed, 0 failed, 59.58s, 5 files.
- Probe families run: 9 (11 sub-probes counting p3a/p3b, p5a/p5b, p6/p6b,
  p7a/p7b/p7c), all green, 1 probe file, full JSON output captured.
- Fracture: stock-board max stress 4 (p_drain) vs lowest threshold 210
  (p_out); thresholds on stock pipes 236/210/335; band [200, 400]; burst law
  strictly-greater (stock threshold+1 pinned by test at stress t+1).
- Stock board conservation: 8 units total; idle 500-tick end state waste 8,
  all other nodes 0; fractured_any False.
- Valve lie: 2 of 2 paths confirmed (world row "u1 opens p_spring." with
  pipe shut; campaign "Valve main open." with pipe shut).
- Starvation lift: 2 units, gate elev 2 to waste elev 9; two-waste pick:
  first-inserted 2, lowest 0.
- Steam: roundtrip drop 2 -> 0 (probe p1); no-cold parking 3,3,3 over 3
  ticks (probe p2).
- Seed thread numbers: xor symmetric feeds 8 in / 0 downstream / 8 stuck;
  staggered siphons primed on tick 1 both, 0 gate passes; vortex sketch k=2:
  8 delivered in 8 ticks, 4/4, conserved; k=3: 3/3/2; period LCM(2,3)=6.
- Drain-battery win: 8 idle ticks to full drain + 4 boil verbs = winner at
  12 ticks, crown 4, world total 8 conserved.
- Sill probe: hold at 1 inlet ("1 < sill 2", 1 pooled); pass at 2 concurrent
  inlets (2 to pool, 0 kept).
- Concurrency this cycle: 1 (single probe process), under the 16 law. RAM:
  in-memory graphs only, far under the free-minus-2GB law.
- Em-dashes in this receipt: 0.

## NEXT THREAD (self-chosen, for the next cycle)

Vortex landing, spec-first from finding 7's block: kind "vortex" in
mag/water_graph.py + rot in to_spec/from_spec + Godot twin mirror + the
roundtrip and gate-interaction tests, riding the same wave as the one-line
from_spec steam fix (finding 1), the burst-pipe valve why-code (finding 4,
both call sites), and the sill dedicated tests (finding 8). The starvation
lift (finding 5) stays a documented play mechanic until the operator rules it
bug or feature; the mariner's vote is feature.

Resume note: no mid-road stop. Cycle 1 closed at a boundary; the next cycle
resumes by id mariner with the next thread above.
