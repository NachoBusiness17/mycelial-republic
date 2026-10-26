# AH14 — one correlation law across the three provenance writers (AE5 wishlist #1, refire)

**2026-09-30 · owner seat: corr-id lane · status: LANDED**

## The law

`corr_id = uuid4().hex[:8]`, minted once at lane start and carried in env
`MAG_CORR_ID`. Every provenance row — trajectory steps, game-flow burns, duel
ledger — carries `corr_id` (env value, `null` when the lane set none). Absent
field on pre-AH14 rows reads as `null`; no reader changes shape.

## What landed

- **`mag/trajectory_step.py`** (canonical definition, lines ~56-73): `corr_id()`
  reads `MAG_CORR_ID` (null when unset); `make_row` stamps it on every row.
  Deliberately OUTSIDE the `step_hash` basis, so `verify` recomputes pre-AH14
  and post-AH14 rows identically (hash-clean drift-free).
- **`mag/game_flow.py`** (burns ledger writer, `FLOW_LEDGER.jsonl`): imports
  `corr_id` from trajectory_step and stamps it at the single `_log` choke
  point — every burns row joins.
- **`tools/duel_harness.py`** (`duels.jsonl`): stdlib-standalone, so the
  resolver is re-implemented with the identical env var + hex8 shape.
  `series_corr_id()`: env wins; env unset -> one uuid4-hex8 mint per series
  (process), so a series script's many duels join the same id. Additive field
  only in the row dict — the `open(out_path, "a")` one-line append semantics
  untouched (AH10 may append concurrently; no path change).
- **Backward compat**: all downstream readers (`tools/enqueue_law.py`,
  `tools/duel_style_regression.py`, `tools/tabfm_try.py`) use `json.loads` +
  `.get`/fixed keys — additive `corr_id` breaks nothing; old rows without the
  field read as null.

## Tests

`tests/test_corr_id_ah14.py` — env-set corr_id lands in fixture rows for all
three writers (trajectory "deadbeef", burns "cafe1234", duel "beef0001");
unset -> null (trajectory/burns) or per-series mint stable across the series
and hex8-shaped (duel); env wins over the mint; corr_id stays out of the
step_hash basis (`verify` reports 2/2 hash-clean); pre-AH14 row shapes still
parse with `.get("corr_id") is None`. Run: 19 passed across
test_corr_id_ah14 + test_duel_harness + test_trajectory_rib +
test_trajectory_bounds; reader sweep test_enqueue_law 8 passed. Instrument:
`.venv/Scripts/python.exe -m pytest -q`, moment 2026-09-30. Refire note: the
prior attempt's code+tests landed but died before filing this receipt; this
session verified the bytes and closed the paper trail.
