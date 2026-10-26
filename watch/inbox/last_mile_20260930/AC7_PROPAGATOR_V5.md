# AC7_PROPAGATOR_V5 — propagator mirrors the V5 economy law

**Seat:** legality_propagator owner (AC7). **Date:** 2026-09-29. **No commit.**
**Files owned this lane:** `tools/legality_propagator.py` + `tests/test_propagator.py`.
**Trigger:** V5 (`watch/inbox/last_mile_20260930/V5_ECONOMY.md`) changed the
engine's STARVED behavior — waste HOLDS volume, spill ROUTES to waste,
boil-from-waste recovers — and named `tools/legality_propagator.py:186`
as a stale sibling surface.

## Step 1 — read the V5 tick() changes

Two engine deltas (mag/water_graph.py, comments name the law):
`_move` into waste now accumulates (`dst.volume += flow`, basin not void);
the STARVED branch routes pooled spill to the FIRST waste node in
insertion order, or HOLDS it at the junction when no waste node exists.

## Step 2 — BEFORE sweep (instrument + moment named)

`pytest tests/test_propagator.py -q` (12 passed, incl. the 100-case
agreement law, seed 1010) + CLI `--n/--seed`: 17/5000, 99/1000, 4242/1000
— **7,100/7,100 (100.00%)**, label distribution byte-identical to Y10's
original run (dry_pool 1377 / unknown_target 1212 / unknown_verb 473 /
legal_gain 213 / legal_no_gain 1725 at seed 17). V5 moved NO sampled
verdict: the W3K generator never pre-primes siphons and pins waste at
elev 0, so held waste cannot outflow within a tick, and the STARVED spill
lands after the plain-pipe phase — verdict-invisible in this family.

## Step 3 — divergences proven anyway (bytes, hand-built boards)

1. **Verdict-level:** basin cascade `a -> waste` then a PRE-PRIMED siphon
   `waste -> crown` (later in pipe order): engine `legal_gain`, old
   oracle `legal_no_gain` (its "waste swallows" `_carry` guard deleted
   the units the siphon needed). The oracle was WRONG on a reachable
   state; the sampled family just never draws one.
2. **State-level:** pooled xor junction, no inflow: engine post-tick
   `j=0 / waste=2`, old oracle `0 / 0` (STARVED zeroing = deletion).
3. **State-level:** sill junction, no waste node: engine holds `j=2`,
   old oracle zeroed it.

## Step 4 — the fix (constraints re-derived, not copied)

- `_carry`: waste accumulates like any destination (basin law).
- `_propagate_flow`: STARVED spill routes to the first waste node in
  node insertion order (`next(... kind == "waste")`), else HELD at the
  junction — never zeroed.
- Module docstring (c) FLOW law text updated in the same change
  (spec-before-behavior); comments carry the evidence they were fixed on
  and avoid the engine-name strings the engine-free test bans.

## Step 5 — AFTER sweep (same instruments, post-fix)

- `pytest tests/test_propagator.py -q`: **15 passed** (12 + 3 new V5
  unit laws: `test_waste_basin_feeds_a_primed_siphon` (verdict-level,
  engine cross-checked), `test_starved_spill_routes_to_first_waste_basin`
  and `test_starved_without_waste_node_holds_at_junction` (state-level,
  pinned against the engine's own tick via `rebuild_graph` + a
  FLOW-phase-only helper)).
- CLI: seed 17 n=5000 → 5000/5000; seed 99 n=1000 → 1000/1000; seed
  4242 n=1000 → 1000/1000. **Total 7,100/7,100 (100.00%)**, label
  distribution unchanged (expected: the family cannot reach the changed
  laws — the new coverage is the hand-built units).
- Divergence case 1 now agrees: engine `legal_gain` == oracle `legal_gain`.

## Adjacent + gates

- `pytest tests/test_propagator.py tests/test_legality_dataset.py
  tests/test_water_graph.py tests/test_water_graph_starvation.py
  tests/test_water_graph_campaign.py -q`: **48 passed** (2026-09-29,
  this session).
- `tools/violation_ratchet.py check --changed`: 0 new hits on THIS lane's
  files. The run reports 1 NEW (file-too-long `tools/gate_canary.py:401`)
  — that file plus untracked `tools/mimo_census.py` are sibling-lane
  co-tenants in the shared working tree (git status verified); debt not
  accepted here (only its owner accepts by name).

**Agreement: before 7,100/7,100 → after 7,100/7,100; the real change is
the proven-and-fixed oracle bug (verdict-level basin cascade) + the
STARVED routing mirror, held green by 3 new state/verdict-level laws.**
