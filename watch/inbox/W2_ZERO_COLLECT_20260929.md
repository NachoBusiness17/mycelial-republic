# W2 ZERO-COLLECT DETECTOR, Mickey17 Wave 2 lane receipt (2026-09-29)

Lane ownership taken: `tools/census_drift_patrol.py` (edit, the `--collect` path only) + `tests/test_census_zero_collect.py` (new). No git commit (wave law).

## Cause and evidence

Wave ledger return 7 (`watch/inbox/MICKEY17_WAVE_LEDGER_20260929.md`): zero-collect test files hide inside aggregate denominators because the census claim "N tests collected / M files" never says WHICH files carry the items; `tests/test_selffeed_integration.py` collected 0 while being counted in every file denominator. B2-247 could only NAME the gap (evidence-only, exit 0). Return 22 added the sibling fact: collection errors can mask the whole suite; both were checked live this session.

## What landed

- `tools/census_drift_patrol.py`, `--collect` deep-check path only:
  - `ZERO_COLLECT_TOLERANT` module constant: repo-relative posix paths of legitimately-empty fixtures, each entry owing a receipt. Seeded EMPTY on purpose: the only real zero-collect file found is the disease itself (`tests/test_selffeed_integration.py`, a `__main__` hermes-integration script wearing `test_*.py` naming, zero test functions; cure is rename/convert, never tolerance).
  - `zero_collect_patrol(disk_files, collected_files, tolerant)`: pure verdict core; ZERO-COLLECT = disk candidates minus collected files minus tolerant, fail-closed on the remainder, exit 1 naming each file. Empty file and collection-skipped both land in the remainder (both are "not in the collected set").
  - `run()` wiring: verdict computed after the B2-247 evidence lines (which stay byte-identical); any red of COLLECT-DRIFT / ZERO-COLLECT prints its verdict + fix line and returns 1. The tolerant list is read from the module global at call time (not a def-time default) so tests can flip it without touching the core.
- `tests/test_census_zero_collect.py` (new, 8 tests): empty file named by the detector; script-shaped disease file (main(), zero tests) named; all-populated passes; tolerant list exempts (pure + end-to-end through `run()` with monkeypatch); module seed pinned empty; CLI band pins exit 1 + gap-evidence line survival and the all-populated exit 0.

## Real run (byte truth, this session, 2026-09-29)

`pytest --collect-only -q` under the venv: exit 0, 2747 collected (first pass) then 2757 (minutes later; wave lanes landing live), NO collection errors. The 2 known errors from ledger return 22 (`test_blade_templates`, `test_bones_adapter` hard imports) are already fixed by the sibling lane, so the zero-collect list below is bytes, not a guess.

`.venv/Scripts/python.exe tools/census_drift_patrol.py --collect` exit 1:
- base gate ok (census 2026-09-29), disk candidates 396, collected 2757/396 files;
- COLLECT-DRIFT +321 vs carrier 2436 (pre-existing carrier lag since the 08:30 cron, carrier-refresh lane's business);
- **ZERO-COLLECT: 1 file, `tests/test_selffeed_integration.py`** (THE key finding); the only real zero-collect file, matching the 08:30 cron log (`logs/census_patrol.log`, "instrument gap: 1 ... tests/test_selffeed_integration.py") and ledger return 7.

## Test numbers

- `pytest tests/test_census_zero_collect.py -q` → 8 passed.
- `pytest tests/test_census_drift_patrol.py -q` → 49 passed, 1 failed: `test_cli_collect_names_the_zero_collect_instrument_gap` (line 522, `assert 1 == 0`). This pin holds the superseded B2-247 behavior (zero-collect candidate named but exit 0); its gap-naming and files-delta assertions still pass. That file is outside this lane's ownership, so it was NOT edited; cure for the owning lane: expect exit 1 plus the `ZERO-COLLECT` verdict line (or seed the tolerant list for the `*_test.py` fixture class with a receipt).

## Ratchet

`tools/violation_ratchet.py check --changed`: FAIL from 4 NEW debts on sibling lanes' changed files (`mag/physical_compute_acquire.py:606`, `mag/skills_pack.py:80`, `tools/gate_canary.py:404`, `tools/regen_front_door.py:433`), none touched by this lane. This lane's only ratchet fact: GROWTH claim `8d41e611f98d3fa5`, `tools/census_drift_patrol.py` accepted at 403 lines, now 462 (+59), non-blocking by B2-273; the B2-365 cure (split into a sibling module) was unavailable under this lane's file ownership, so the growth stands named here for the operator to re-accept or direct a split.

Em-dash count in both landed files: 0.
