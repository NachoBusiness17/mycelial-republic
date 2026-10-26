# B2-318 pytest-named script self-tests 2026-09-26

## Verdict

Landed, port arm. Both zero-collect batteries now execute under pytest: tests/ack_reaper_test.py (21 checks) and tests/lesson_gate_test.py (22 checks) each expose one shared battery function (collect_checks()), and thin wrapper modules tests/test_ack_reaper.py + tests/test_lesson_gate.py surface every check as its own pytest item (45 wrapper items + 2 shape guards, all passing). The hand-run surface is unchanged byte-for-byte in behavior: both scripts still print the same PASS/FAIL lines and ALL PASS/22-22 summaries. The pre-registered falsifier was fired live both ways: mutating scripts/ack_reaper.py DEFAULT_REALERT_HOURS 24 -> 2400 made 3 pytest items fail (1.60s), previously ZERO items existed to fail; after byte-exact restore, 22 passed again and the script is git-clean.

## Evidence file:line quotes

- tests/ack_reaper_test.py:67 (pre-edit): the 21 checks lived only inside main() with a print-only check() closure; module defines no test_* functions, so pytest's *_test.py collection imported it and collected 0 items (the census counted a dead candidate).
- tests/lesson_gate_test.py:46 (pre-edit): same shape, module-level RESULTS + check() prints, all 22 checks inside main(); 0 collected items.
- Post-edit: tests/ack_reaper_test.py collect_checks() -> list[tuple[str, bool, str]] and tests/lesson_gate_test.py collect_checks() (RESULTS.clear() + same fixtures); main() in both is now a thin printer over the returned battery.
- scripts/ack_reaper.py:30 `DEFAULT_REALERT_HOURS = 24.0` was the mutation site; restored byte-identical, git status clean post-run.

## Work done

1. Refactored both scripts to the single-battery shape (collect_checks + thin main printer); hand-run verified unchanged: ack_reaper 21/21 ALL PASS, lesson_gate 22/22 ALL GREEN; py_compile clean.
2. Added tests/test_ack_reaper.py and tests/test_lesson_gate.py: module-scoped battery fixture (with a shape-drift guard asserting 21/22 checks), a name-uniqueness guard, and parametrized per-check items so each check fails individually with its name in the assertion.
3. Ran the pre-registered falsifier live: backup -> mutate DEFAULT_REALERT_HOURS 24->2400 -> pytest tests/test_ack_reaper.py = 3 failed / 19 passed (items 10 and siblings; before this port that mutation produced zero failures because zero items existed) -> byte-exact restore -> 22 passed, git status clean.
4. Full wrapper suites: pytest tests/test_ack_reaper.py tests/test_lesson_gate.py = 45 passed.

## Falsifier

Dies if: (a) a regression in scripts/ack_reaper.py or scripts/lesson_gate.py passes pytest -q while the hand-run battery catches it (the wrapper battery must move in lockstep, both share collect_checks()); (b) either wrapper's shape guard stops matching the script's check count without both files changing together; (c) either script's main() hand-run output changes semantics (exit code on failure, PASS/FAIL lines).

## Bibliography closed

Read whole: tests/ack_reaper_test.py, tests/lesson_gate_test.py, scripts/ack_reaper.py (mutation site + argument wiring), watch/inbox/burn_wave_20260926/B2_247_collect_gap_20260926.md pointer from the brief row (cited names verified). Bytes: hand-run outputs observed live pre/post refactor; mutation/revert observed live; git status byte-clean after restore. Nothing synthesized.
