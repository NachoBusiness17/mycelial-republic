# B17 — census refresh (2026-09-30, evening)

**Mission:** refresh the AGENTS.md census bullet after the day's test-file flood; carrier-shape law B2-249 preserved.

## New claim (byte truth)

```
3,550 tests collected / 455 files (2026-09-30 census
```

- **Instrument:** `.venv/Scripts/python.exe -m pytest --collect-only -q -p no:cacheprovider tests`
- **Moment:** 2026-09-30 14:51:47 EDT (18:51Z); 26.31s; zero collection errors.
- **File count (patrol's own instrument):** `rglob('test_*.py') + rglob('*_test.py')` over `tests/` = 455 (454 `test_*.py` + `wave_driver_test.py`); = 440 committed (`git ls-files`) + 15 untracked (`git status`).

## Drift attribution (from the same-day 11:46Z carrier 3,220 / 433 → 3,550 / 455; +330 collected, +22 files)

The tree was still moving at 11:46Z (that carrier said so itself). Landings after that moment:

1. **IMP+LM+AJ wave** (commit `e0ff8cec0`, 14:29 EDT): anomaly flagger, estate_query corr_id 3-way joins, LDT near-miss arc closed both directions, DFHack liquids + units. Its test files ride the working tree untracked (see 2).
2. **15 untracked working-tree test files** (`git status --porcelain tests/`, all `??`):
   `test_ah4_rib_fixes, test_ah5_warmboot, test_anomaly_flagger, test_ask_bank, test_cost_rollup, test_current_anchor_guards, test_effect_broker_ah18, test_estate_query, test_flock_positive, test_ldt_nearmiss, test_mountain_digflood, test_mountain_liquids, test_mountain_reveal, test_mountain_units, test_rib_freeze`
3. **Committed same-day waves landing after 11:46Z:** AH19 amend-perf v2 (`c1fb757da` 08:56 EDT — `test_ah19_append_leaves.py`, +14 byte-prefix no-rewrite tests), HISTORY PURGE wave (`662dc739e` 11:29 EDT — `test_ah2_proof.py`, AH2 ed25519 + seal Merkle verify), plus `test_ag5_tip_verify.py`, `test_burns_verdict_enum.py`, `test_concept_predictor.py`, `test_corr_id_ah14.py` landed 09-30.
4. Items landed **inside existing files** (parametrize/appended cases) — invisible to file-count arithmetic, covered by the +330 collected delta.

Not differenced against the 09-29 or 09-27 carriers (denominator law B2-216: never difference counts from different moments).

## Verification

```
$ .venv/Scripts/python.exe tools/census_drift_patrol.py
CENSUS-PATROL: ok - census 2026-09-30 (3550 collected / 455 files)
  disk candidate files: 455
CENSUS-PATROL: ok - census 0d old of 7d bar
PATROL_EXIT:0
```

Carrier edited in `AGENTS.md` line 27 with exact B2-249 grammar intact; prior refresh attributions (AG7 11:46Z seed → 09-29 → 09-27 → retired 1,341 headline) preserved as history inside the bullet.

— B17 lane, 2026-09-30 14:51 EDT
