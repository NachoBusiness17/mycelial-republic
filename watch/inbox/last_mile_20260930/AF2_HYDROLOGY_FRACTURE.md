# AF2_HYDROLOGY_FRACTURE — the fracture law mirrored under graded heads

**Seat:** hydrology lane (`mag/hydrology.py` + `tests/test_hydrology.py`) · **Date:** 2026-09-29 · **No commit (working tree).**
**Mission:** AD1's flag (this dir, `AD1_FRACTURE.md` § "Flagged for other owners") — hydrology's `_move` override lacked the AC2 fracture law.

## The divergence (as found)

`HydrologyGraph._move` overrides the base commit wholesale: it computes graded
flow via `_pipe_flow`, then commits (`src.volume -= flow` …) with **no call to
the base `_fracture` hook** — the landed AC2 law fires only from `WaterGraph._move`,
so a graded pipe could run full bore forever. Additionally hydrology's `from_spec`
dropped `stress`/`fractured` (and `primed`) that the base `to_spec` emits — a burst
hydrology pipe would have resurrected open through a roundtrip.

## The mirror (one law, not two copies)

- **`mag/hydrology.py` `_move`:** one insertion between flow computation and the
  volume commit — `if self._fracture(p, src, dst, flow, events): return` — the
  SAME inherited hook the boolean engine calls, at the same point in the sequence.
  No djb2 helper import needed: `name_hash`/`fracture_threshold`/`_fracture`/spray/
  event grammar all live in `mag/water_graph.py`, untouched; tick's
  `p.fractured or not p.open` skip and `open()`'s burst refusal were already
  inherited. Graded full bore (`flow == cap` under the dHead law) now stresses
  exactly like boolean full bore; gated inflow does not stress in either engine
  (probe commits in the gate phase, never `_move` — the landed shape, mirrored).
- **`mag/hydrology.py` `from_spec`:** carries `primed`/`stress`/`fractured`
  (AC2 roundtrip law + LW5 `primed`, whose base fix never reached this override).
- Docstring notes the law rides the inherited hook. 172 lines (cap 400).

## Tests (tests/test_hydrology.py, AF2 block, +3)

1. `test_graded_full_bore_stresses_partial_does_not` — graded flow saturating at
   cap accumulates stress; volume-limited partial graded flow does not.
2. `test_fracture_fires_identically_to_boolean_engine` — same shape, same pipe
   name `burst`, cap 1: graded vs boolean burst at the same tick (stress 254 =
   threshold 253 + 1), byte-identical **entire run log**, same spray to `sump`,
   same volumes (`pool == t`, `tank == 10_000 - (t+1)`).
3. `test_hydrology_spec_roundtrip_preserves_stress_and_fractured` — partial
   stress survives the hydrology.v1 roundtrip; a one-shot burst (cap = threshold+1,
   tank head engineered so the graded term saturates) survives the roundtrip
   closed, and the valve verb (`open()`) cannot resurrect it.

**Negative control (the tests bite):** with `WaterGraph._fracture` monkeypatched
to a no-op, the graded engine runs 400 ticks with **no FRACTURES event and
stress 0** (accumulation lives inside the hook) — test 2 fails on the missing
burst line. With the hook: `Pipe burst FRACTURES (stress 254): spray to sump.`,
identical to the boolean engine's own suite.

## Verification (bytes, instruments named; `pytest -q` this session)

- `tests/test_hydrology.py`: **15 passed** (12 pre-change + 3 AF2).
- `tests/test_water_graph.py`: **16 passed** (water-graph family, unchanged file).
- Adjacent sweep (11 files: water_graph, starvation, campaign, water_computer,
  k8s_water, propagator, legality_dataset, hydrology, field_flow, hydro_xor_sim,
  water_swarm): **122 passed**.
- Mission said hydrology family "was 12+43 tests": `pytest --collect-only` found
  **12** in test_hydrology.py before this lane (15 after); no 43-test hydrology
  file exists on disk (only test_hydrology.py imports HydrologyGraph) — the 43
  does not byte-match any current denominator; the executed numbers above are
  the filed truth (census denominator law: name instrument + moment).
- Ratchet `tools/violation_ratchet.py check --changed`: 0 hits on this lane
  (172/282 lines). The 1 NEW hit (`file-too-long tools/concept_predictor.py:513`)
  is the untracked AF1 sibling lane's co-tenant; debt not accepted here.

## Still flagged for the hydrology lane (pre-existing, NOT smuggled in)

- `_move`'s waste branch still early-returns **without `dst.volume += flow`** —
  the V5 waste-accumulation divergence AD1/AC5 noted. Fracture-spray into a waste
  node DOES hold (the spray path accumulates); only the direct waste delivery
  deletes. Owner: next hydrology window.
