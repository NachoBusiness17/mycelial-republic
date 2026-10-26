# Z4 — SectionStream port (deterministic streamed world-gen)

Lane: hydrology (Y1's top port). Date: 2026-09-29.
Files: `mag/section_stream.py` (new) + `tests/test_section_stream.py` (new). No commit.

## What landed

Faithful Python port of `roblox/src/shared/SectionStream.luau` (103 lines, the GnomeCode ep.1 streamed-sections pattern): a stream holds one-shot build closures with centers; `poll(positions)` builds unbuilt sections within `radius` of any position, capped at `budget` per poll; `pending()` counts the rest. Every Luau line maps 1:1 — Vector3 → 3-tuple, `.Magnitude` → `math.dist`, `budget or math.huge` → `math.inf` default, `table.insert` → `list.append`, `predecessorsDone`'s `other == sec` table identity → `is`.

**The determinism is rng-ORDER, and the module has no rng at all.** The Luau (and the port) draw no randomness; `ordered=True` is the load-bearing mode — a section never builds before its predecessors, so insertion order equals rng draw order for closures sharing one seeded generator, making a streamed world identical to the eager one, only later in time (the Ossuary `SeedRng(20261031)` claim). Estate no-RNG law satisfied by construction; no seeded shape to port because the source holds no seed.

One adaptation beyond line-mapping (found while porting, not papered over): the Luau re-iterates its `positions` table per section — a live Python iterator would exhaust after the first section — so `poll` snapshots positions once at entry. Test `test_poll_positions_iterable_is_snapshotted` pins it with a one-shot `iter(...)`.

## Proof shape

Tests mirror the fleet's own `SeedRng.luau` xorshift32 (bit32 wrap made explicit via masks) as the shared seeded generator feeding 25 grid sections with fixed per-section draw counts:

- `ordered` streamed behind a walker that starts at the FAR corner (late radii trip first) == eager build, exactly — every `(section, int, pick)` draw equal.
- Same seed + same walk on two independent streams → identical logs.
- `ordered=False` under the same far-first walker DIVERGES from eager (all 25 still built once) — the contrast proving `ordered` is the load-bearing flag.
- The gate itself: polling the far corner alone builds 0 of 25.

## Tests (real counts)

`pytest -q tests/test_section_stream.py` → **10 passed in 0.58s** (instrument: executed).
`pytest --collect-only -q tests/test_section_stream.py` → **10 tests collected in 0.48s** (instrument: collected; same moment, delta 0 — no landings between the two runs).

Coverage: same-seed determinism, streamed-ordered == eager, unordered divergence, ordered gate hold-back, budget cap (12x2 + 1 for 25 at budget 2, then 0), `math.inf` default budget (one poll builds all), inclusive radius boundary (`|d| == radius` builds via (10,0,0) and (0,6,8); 10.000001 does not), positions snapshot, 5x5 small world walked to completion in strict insertion order, pending/add-after-poll.

Gates: `tools/violation_ratchet.py check --changed` → PASS (scope=4, hits=0, NEW=0). `py_compile` both files OK.
