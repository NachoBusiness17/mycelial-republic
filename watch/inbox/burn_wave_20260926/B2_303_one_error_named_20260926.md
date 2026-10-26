# B2-303 name the standing "1 error" module 2026-09-26

## Verdict

LANDED. The standing "1 error" is named, and it was tests/test_spore_seed.py all along: ERROR at setup of test_generate_and_validate_spore_seed, "fixture 'mocker' not found" (pytest-mock is not installed in this venv), identical on every full run because the setup error precedes any assertion. FIXED, not baseline-updated: the unused mocker parameter is removed, and two deeper defects the error had been masking are fixed in the same landing (both named in fix comments): (1) the test also called validate_spore_seed with 3 args against its current -arg signature (seat, root, timestamp) so it would have failed even with mocker present; (2) the module's tests were appending to the PRODUCTION memory/spore_seeds/testseat.jsonl on every suite run (a local reassignment of the imported SPORE_SEED_FILE name is a no-op; 12 pollution rows stood on file at fix time; the tests now monkeypatch mag.spore_seed.SPORE_SEED_FILE into tmp_path and the production file stopped growing, measured before/after). Targeted proof: pytest tests/test_spore_seed.py = 2 passed, 0 errors, production rows unchanged across the run.

## Evidence file:line quotes

- watch/inbox/burn_wave_20260926/B2_303_fullrun_errors.log (this lane's full run, 1712.75s): "=== ERRORS === / _________ ERROR at setup of test_generate_and_validate_spore_seed ___________ / file tests/test_spore_seed.py, line 8 / E fixture 'mocker' not found" and the summary "39 failed, 2164 passed, 9 skipped, 9 warnings, 1 error". This is the errors block no earlier receipt captured.
- Constant-error history verified verbatim: B2_34_cluster_detectors_20260926.md:22 and B2_51_autorun_autopsy_20260926.md:22 ("38 failed / ... / 1 error"), B2_64_drift_dashboard_20260926.md:18 ("37 failed / ... / 1 error") — the error module is now named for all four.
- tests/test_spore_seed.py:8 (pre-edit): `def test_generate_and_validate_spore_seed(mocker):` with mocker unused in the body; test 2 pre-edit reassigned the imported SPORE_SEED_FILE locally (no effect on mag.spore_seed._seed_file, which reads mag.spore_seed.SPORE_SEED_FILE at call time).
- Byte proof of production pollution: memory/spore_seeds/testseat.jsonl grew 10 -> 12 rows across this lane's pre-fix runs, every row seat_id "testseat" with a suite-run timestamp; post-fix growth = 0 (12 before, 12 after a green run).

## Work done

1. Ran the full suite once with -rE and tee'd output (the brief's ask; the B2-243 retain-logs brief has still not landed, so no retained log existed), capturing the ERRORS block and naming the module.
2. Fixed tests/test_spore_seed.py: dropped the unused mocker parameter; passed a fixed timestamp through generate into validate (the signature the module actually has); redirected both tests' log writes into tmp_path via monkeypatch on mag.spore_seed.SPORE_SEED_FILE.
3. Verified: tests/test_spore_seed.py 2 passed; production testseat.jsonl byte-count stable across a green run.
4. Owed, named: the 12 pollution rows in memory/spore_seeds/testseat.jsonl predate this fix and belong to the spore-seed owner to purge or baseline (append-only log; this lane does not delete another organ's rows).

## Falsifier

Dies if: (a) the next full-suite run still shows "1 error" (the fix regressed or a different module took up the error slot; either way the card retires and the new errors block must be filed); (b) a full run shows zero errors AND zero testseat.jsonl growth (both the fix and the pollution fix hold; the card is then fully retired as the brief's falsifier demands); (c) pytest-mock gets installed and some other test reintroduces a mocker-shaped setup error.

## Bibliography closed

Read whole: tests/test_spore_seed.py (pre/post), mag/spore_seed.py (generate/validate/_append_seed_record/_seed_file), mag/constants.py SPORE_SEED_FILE, the full-run log this lane produced, the three cited receipts' summary lines. Bytes: error block captured from a real run; production row counts measured before/after. Nothing synthesized.
