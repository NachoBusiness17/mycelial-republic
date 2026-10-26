# B2-389 Retire or collect the two script self-tests (SW-07, 2026-09-26)

## Verdict

LANDED. Chosen branch: rename out of the pytest candidate namespace (the pytest-collection half already existed via the B2-318 wrappers). tests/ack_reaper_test.py -> tests/selftests/ack_reaper_selftest.py and tests/lesson_gate_test.py -> tests/selftests/lesson_gate_selftest.py, with the pytest wrappers tests/test_ack_reaper.py / tests/test_lesson_gate.py repointed at the moved battery modules and both scripts' repo-root computations fixed for the extra directory level. Falsifier discharged: the census patrol instrument gap line now reads "instrument gap: none, every disk candidate collects items" (was 2 zero-collect candidates), both hand-run harnesses still pass standalone (21/21 and 22/22 checks), and the wrappers run green under pytest (45 passed).

## Evidence file:line quotes

- QUEUE.md row: "either rename them out of the pytest candidate namespace (scripts/selftests/ or a tests/ name matching neither test_* nor *_test.py) or convert their check() ladders into real pytest tests; falsifier: candidate_files drops by 2 or pytest collects items from them, and the patrol gap line reads zero-collect none with cause".
- Pre-move patrol: "instrument gap: 2 zero-collect candidate(s): tests/ack_reaper_test.py, tests/lesson_gate_test.py".
- Post-move patrol: "instrument gap: none, every disk candidate collects items".
- The collection half pre-existed, tests/test_ack_reaper.py:3-6: "tests/ack_reaper_test.py matched the *_test.py collection pattern but defined no test_* functions, so its 21 hand-run checks contributed zero pytest items ... These thin wrappers run the single shared battery (collect_checks())".
- Hand-run proof after the move: `python tests/selftests/ack_reaper_selftest.py` -> "ALL PASS (21 checks)"; `python tests/selftests/lesson_gate_selftest.py` -> "22/22 checks passed - ALL GREEN".
- Pytest proof: `pytest tests/test_ack_reaper.py tests/test_lesson_gate.py -q` -> "45 passed in 51.94s".

## Work done

- mkdir tests/selftests/; moved both *_test.py files to *_selftest.py inside it.
- Fixed repo-root derivations broken by the deeper path: lesson_gate_selftest REPO parents[1] -> parents[2]; ack_reaper_selftest REAPER dirname(HERE) -> dirname(dirname(HERE)), both with B2-389 cause comments.
- Repointed tests/test_ack_reaper.py and tests/test_lesson_gate.py spec_from_file_location paths to the new module locations; freshened the moved files' docstring Run lines and headers.
- One red run en route, receipted per the no-fabrication law: after the move the wrappers failed collection with ModuleNotFoundError ("No module named 'lesson_gate'") because the moved modules still derived the repo root from one directory level up; fixed by parents[2] / double-dirname with cause comments, then green.

## Falsifier

The brief's falsifier is discharged (patrol gap line reads none-with-cause; both files left the candidate namespace; pytest items already existed and pass). Reopen if: a *_test.py file reappears under tests/ top level (the naming law), or the patrol again prints a nonzero zero-collect candidate list naming these paths.

## Bibliography closed

Read: tests/ack_reaper_test.py + tests/lesson_gate_test.py (full, pre-move), tests/test_ack_reaper.py + tests/test_lesson_gate.py (wrapper headers), tools/census_drift_patrol.py --collect output pre/post, pytest runs. No external sources.
