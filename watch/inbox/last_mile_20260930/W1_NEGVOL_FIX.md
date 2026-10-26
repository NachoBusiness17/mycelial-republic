# W1 — water_graph negative-volume fix (LW5 deferred-inflow double-count)

Date: 2026-09-29 · Owner: W1 seat (ZCode) · Files: `mag/water_graph.py`, `tests/test_water_graph.py` · No commit (operator holds the fence).

## The bug (deterministic)

`tick()` probes pipes INTO gated junctions with `_available()` — a **no-commit** probe returning `min(cap, src.volume)` without decrementing. The gate phase later decremented `src.volume -= flow` **once per deferred entry**. Two shapes double-count the same units:

1. **Shared source, two gated pipes**: volume 3 at src, two cap-3 pipes into xor/sill junctions → probes both read 3, gate commits −6 → src = **−3**.
2. **Deferred + plain from one source** (deferred first by insertion order): probe reads the full volume, plain `_move` drains what remains, then the gate commit subtracts the deferred flow again → src = **−5** (repro: tank 5, cap-5 deferred + cap-5 plain).

Reproduced before the fix: random seed 12 → `n4 volume -2`. Test-first evidence: 4 new tests red on the old cut (`4 failed, 7 passed`), green after.

## The fix (design aligned, no guard branches)

The deferred flow now **reserves at probe time**: `src.volume -= flow` inside the pipe loop, immediately after `_available` returns nonzero. Both gate branches (allow and hold) now only do `node.volume += flow`. Probe+gate becomes one atomic move split across two phases; every decrement follows a fresh `min(cap, volume)`, so negatives are impossible and insertion order stays the tiebreaker for which sibling pipe spends shared volume. The `tick()` docstring (behavior owner) was updated with the code change.

## from_spec primed drop (same landing)

`to_spec()` emitted `"primed"` but `from_spec()` never passed it and `add_pipe()` had no parameter — every spec roundtrip (incl. `estate_water_graph_tick`) silently reverted a primed siphon to unprimed. `add_pipe` gained `primed: bool = False`; `from_spec` passes `primed=bool(p.get("primed", False))`. Backward compatible (defaults unchanged for specs without the key).

## Tests amended (`tests/test_water_graph.py`, LW5 block)

- `test_shared_source_gated_inflows_never_go_negative` — minimal repro (shape 1).
- `test_deferred_then_plain_from_same_source_never_negative` — minimal repro (shape 2).
- `test_no_negative_volume_across_seeded_random_graphs` — 1000 seeded graphs (`random.Random(seed)`, seed 0–999; 3–8 nodes mixed kinds incl. xor/sill/cold/waste, 2–10 pipes, siphons, closed valves, colliding sources), 1–6 ticks each: no node volume or steam ever negative, and V5 economy conserved (volume+steam invariant through tick).
- `test_spec_roundtrip_preserves_siphon_primed_state` — primed survives roundtrip twice.

## Real pytest counts (this venv, this tree)

- `tests/test_water_graph.py` before fix: `4 failed, 7 passed` (test-first evidence).
- After fix, engine + direct consumers: `tests/test_water_graph.py tests/test_water_graph_starvation.py tests/test_water_graph_campaign.py tests/test_water_computer.py` → **35 passed**.
- Wider importers: `tests/test_dem_to_board.py tests/test_water_swarm.py tests/test_field_flow.py tests/test_hydrology.py` → **49 passed**.
- Total this change touches: **84 passed, 0 failed**.

## Observed, NOT fixed (adjacent gap, operator's call)

`to_spec()` nodes omit `sill` while `from_spec()` reads it — a sill-junction spec loses its gate threshold on to_spec→from_spec roundtrip. Same fidelity class as the primed drop but outside W1's mandate; flagged here for a follow-up landing (one word in `to_spec`, plus a roundtrip test asserting `sill=2` survives).
