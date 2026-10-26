# genlive1-g0-3-deepseek (deepseek-chat @ deepseek, turn 1, channel: content)

DEFECT 1: `run()` computes `stale` before checking `age_days < 0`, so a future-dated census that also shrank on disk returns the STALE/exit-1 path only because `patrol()` re-checks; the dead pre-check branch `stale` built above the future guard can never be reached for negative ages, but the ordering makes the exit-2 fabrication arm dependent on `patrol()` rather than on `run()`'s own guard at line 400, which is a latent double-guard. | EVIDENCE: tools/census_drift_patrol.py:398-405 (patrol stale computed at 398, future guard at 402) | FIX: move the `age_days < 0` return above the `stale =` assignment in `patrol()` so the future arm precedes growth evaluation.

DEFECT 2: `candidate_files(root)` is called twice on the `--collect` path, once via `count_candidate_files` at line 291 and again at line 433 (`candidate_files(root)` for `disk_rel`), re-walking tests/ with two `rglob` passes per run. | EVIDENCE: tools/census_drift_patrol.py:291 and tools/census_drift_patrol.py:433 | FIX: hoist one `candidate_files(root)` set near line 289 and reuse it for both `disk_files` and `disk_rel`.

DEFECT 3: `test_files_added_since` treats any line beginning with `"20"` as a commit timestamp (`if line.startswith("20")` at line 352), so a test filename on disk beginning with "20" (e.g. `tests/2026_fixture_test.py`) in `--name-only` output is parsed as a date, sets `commit_day = None`, and silently drops the following path from growth evidence. | EVIDENCE: tools/census_drift_patrol.py:349-357 | FIX: match the ISO pattern instead, e.g. `re.match(r"^\d{4}-\d{2}-\d{2}T", line)`.

DEFECT 4: `parse_carrier` reuses `text.find("\n", match.start())` three times in the line slice at line 253, recomputing the same search per call. | EVIDENCE: tools/census_drift_patrol.py:253 | FIX: bind `nl = text.find("\n", match.start())` once and slice with `text[match.start(): nl if nl != -1 else len(text)]`.

DEFECT 5: `PatrolError` is raised only from `test_files_added_since` and `CollectError`/`TimeoutExpired` from `collect_report`; `countrye` none. Not groundable as a distinct defect line without a second site; omitted.

DEAD-CODE: `FUTURE_TOLERANCE_DAYS` is named in the comment at lines 79-80 as removed, and no live reference remains in the file; the comment documents a name with zero definition or use. | EVIDENCE: tools/census_drift_patrol.py:79-80

ONE-SITTING FIX: collapse the two `candidate_files(root)` walks on the `--collect` path into one hoisted set at the top of `run()`, removing the redundant `count_candidate_files` call in the collect block. | EVIDENCE: tools/census_drift_patrol.py:291
