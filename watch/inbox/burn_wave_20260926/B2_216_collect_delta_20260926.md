# B2-216 collected-vs-executed delta (2026-09-26)

## Verdict

landed. The 55-61 gap is real, confirmed against bytes, and attributed: mid-wave landings dominate (64 named items across 6 test files whose mtimes fall between the full runs' collection windows and the census), the residual is the collection/run artifact class (every full run carries a constant "1 error" outcome; concurrent lanes stash the shared tree mid-run) plus minute-level interleaving that no retained log can resolve. Census denominator law pinned at AGENTS.md:27. Live proof landed during this lane: the census itself moved 1,837 to 1,854 / 303 files within roughly 15 minutes of the B2-69 snapshot.

## Evidence

- Pointer receipts verified verbatim: B2_34_cluster_detectors_20260926.md:22 "38 failed / 1728 passed / 9 skipped / 1 error in 913.33s" sums 1,776; B2_51_autorun_autopsy_20260926.md:22 "1734 passed / 38 failed / 9 skipped / 1 error in 17:34" sums 1,782; B2_69_test_census_20260926.md "1837 tests collected in 2.44s", exit 0, 301 files. Gaps: 1,837 - 1,776 = 61; 1,837 - 1,782 = 55.
- Fourth datapoint discovered this lane: B2_64_drift_dashboard_20260926.md:18 "Full suite: 37 failed / 1790 passed / 9 skipped / 1 error in 19:04" sums to 1,837, exactly the census number. A same-moment executed sum can equal a collected census; comparing sums without moments misleads in both directions.
- Timeline from LEDGER ts minus suite duration (upper bounds, EDT): B2-51 collected by ~08:55 (row 13:12:32Z minus 17:34); B2-34 by ~09:07 (row 13:22:15Z minus 15:13); B2-69 census ~09:49 (row 13:51:52Z); B2-64 collected between ~09:36 and 09:49 (row 13:54:54Z minus 19:04), and its exact equality with the census pins its collection inside the quiet 09:45:56-09:49:21 window between landings.
- Landings inside the run-to-census window, file mtime + item count (pytest --collect-only -q per file, this lane, venv python): tests/test_grounding_chain.py 09:13:11 = 6; tests/test_md_record_seal.py 09:26:07 = 4; tests/test_shared_surface_events.py 09:36:26 = 14; tests/test_index_fold_host.py 09:39:44 = 18; tests/test_drift_dashboard.py 09:39:45 = 5; tests/test_drift_pairs_stamp.py 09:45:56 = 17. Sum 64 items against the 61/55 gaps.
- The 64 vs 61/55 mismatch is the honest residual, named not papered: (a) run collection moments are only upper-boundable from receipts; (b) B2_62_zai_backoff_20260926.md documents concurrent lanes stashing the shared tree mid-run ("pre-existing failures stash-proven"), so run-time tree state is not reconstructible from mtimes alone; (c) every run carries one "1 error" outcome no receipt names, and B2-64 shows 37 failed where B2-34/B2-51 show 38 with the error constant, so outcome class demonstrably slips at the error boundary.
- Fresh confirmation (~10:04 EDT, this lane): rerun `--collect-only -q` = "1854 tests collected in 2.61s", exit 0; 303 unique files collected (includes the tests/ack_reaper_test.py, lesson_gate_test.py, wave_driver_test.py trio that pytest collects by default via *_test.py, 12 items). Delta vs the 09:49 census: +17 items / +2 files, consistent with tests/test_zai_backoff_floor.py (new 09:49:21, 13 items) and tests/test_link_library.py (mtime 09:53:15) plus the 09:53:15 same-instant touch of test_process_supervisor.py and test_doctor_provider_endpoints.py; the item-level split between new-file and extended-file contributions is not byte-recoverable without a second timed census, stated as unknown.
- Run-to-run delta B2-51 vs B2-34 (1,782 vs 1,776, identical 38/9/1 columns) cannot be a pure landing delta: no tests/*.py mtime falls between 08:44:43 (test_lane_runner_cluster.py) and 09:13:11. It is the artifact class the brief names (collection errors, parametrization over live data, stash-window tree drift), unattributable further from retained bytes; no pytest run logs from the morning exist on disk.

## Work done

1. Verified all three pointer receipts against bytes (quotes above); arithmetic checked with venv python.
2. Discovered and verified the fourth datapoint: B2-64's executed sum equals the census number exactly.
3. Reran the census twice this lane (items, then unique files), both exit 0: 1,854 items / 303 files at ~10:04 EDT.
4. Counted per-file items for the six window files plus test_zai_backoff_floor (13), test_lane_runner_cluster (19), test_process_supervisor (11).
5. AGENTS.md:27 amended with the census denominator law (concurrent B2-215 tripwire sentence preserved intact; zero em-dashes introduced).
6. Self-fed B2-242 (identify the standing "1 error" module) and B2-243 (retain full-run pytest logs) to QUEUE.md Open; drafted as B2-237/238, both numbers taken by concurrent lanes mid-append, renumbered highest+1 per the B2-53 restoration precedent (the queue race fired live during this lane).
7. LEDGER row appended via venv python json.dumps; receipt registered via index_fold_host.mjs add (seq 1789823567015749425, 985 active items); `.venv\Scripts\python.exe -m mag.shared_surface validate` run after edits: 8 errors, all other lanes' bytes (concurrent receipt appends since B2-69's "6 remaining mismatches" note, plus the known LINKS.jsonl sealed-prefix debt filed owed by B2-197); zero errors name this lane's files.
8. Side finding, not owned: QUEUE.md carries two B2-216 entries (this lane's collected-vs-executed delta, and B2-62's stash-proven debt claim), the known double-spend disease with B2-53 restoration precedent already on file.

## Falsifier

- Pre-registered: if a retained per-module pytest log from any 09-26 full run ever surfaces, its per-module outcomes must reconcile the named landings to that run's executed sum on the run's own tree state; failure to close disproves this attribution.
- If a collected census ever reads LESS than a later executed sum on the same tree with no test removals, the denominator law is wrong.
- The law predicts the census keeps moving while lanes land tests: 1,837 to 1,854 is already shown; a frozen count across an mtime-proven landing disproves the mtime attribution.
- If B2-64's suite duration or ledger ts is ever corrected so its collection falls outside 09:45:56-09:49:21, the same-snapshot equality reading downgrades to coincidence and the window table must be re-derived.

## Bibliography closed

watch/inbox/burn_wave_20260926/B2_34_cluster_detectors_20260926.md:22; watch/inbox/burn_wave_20260926/B2_51_autorun_autopsy_20260926.md:22; watch/inbox/burn_wave_20260926/B2_69_test_census_20260926.md; watch/inbox/burn_wave_20260926/B2_64_drift_dashboard_20260926.md:18; watch/inbox/burn_wave_20260926/B2_62_zai_backoff_20260926.md; memory/burns/LEDGER.jsonl rows B2-51/B2-34/B2-64/B2-66/B2-69; AGENTS.md:27; watch/inbox/burn_wave_20260926/QUEUE.md; tests/ (mtimes + per-file collect counts, this lane); pytest.ini.

B2-310 ANNOTATION 2026-09-26: the side finding "QUEUE.md carries two B2-216 entries (this lane's collected-vs-executed delta, and B2-62's stash-proven debt claim)" predates the B2-255 double-spend sweep; the stash-proven debt claim is now B2-288, this lane keeps B2-216.
