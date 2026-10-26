# B2-267 receipt: wire the touch law into the drift-patrol prompt (2026-09-26, lane SW-03)

## Verdict

LANDED. The live drift-patrol prompt (automation-a7c71ad1 in %USERPROFILE%/.zcode/v2/tasks-index.sqlite) now carries all three B2-237 touch-law clauses (reader-open rule, size+seal-before-alarm triage rule, file-every-touch rule) as a bound TOUCH LAW block appended after the B2-199 living-law amendment, verified in the DB by readback (4,438 chars, block present exactly once, clauses 6a/6b/6c all present). A repo-side copy landed at configs/drift_patrol_prompt.txt (byte-identical to the DB), and tests/test_drift_patrol_prompt_copy.py diffs copy vs DB in the freshness_check pattern (3 tests pass; DB-unreachable machines skip, never fake-fail). The B2-222 owed state ("still no repo copy") is closed for this prompt.

## Evidence file:line quotes

- watch/inbox/burn_wave_20260926/B2_237_touch_law_20260926.md:19-21 (Work done item 1, the three clauses): "1. Readers never open registered or living-sealed logs in write-capable mode ... 2. mtime is not tamper evidence. Patrol triage checks size and prefix seal first ... never alarm, never auto-refresh. 3. A touch without a register event is still filed (paths, window, writer or 'unattributed') so repeats correlate."
- watch/inbox/burn_wave_20260926/B2_199_update_prompt.py:6-8 (the amended prompt's home and the prior amendment this builds on): "The patrol (ZCode automation automation-a7c71ad1-f43f-403d-8677-105f5176df2b in %USERPROFILE%/.zcode/v2/tasks-index.sqlite, cron 0 8 * * *, enabled)".
- DB readback (this lane): automation row prompt now 4,438 chars ending "...ats correlate. Every touch observation lands in the day's DRIFT_PATROL receipt."; count of "TOUCH LAW (B2-237" = 1; clause markers all present.
- configs/drift_patrol_prompt.txt: 4,438 bytes, byte-identical to the DB prompt (test asserts equality).
- QUEUE.md B2-267 row: "add all three law clauses to the DB prompt plus a repo-side copy diffed by a freshness_check-style test in the same lane".

## Work done

- watch/inbox/burn_wave_20260926/B2_267_update_prompt.py (new, modeled on B2_199_update_prompt.py): reads the live prompt, appends the three-clause TOUCH LAW block (em-dash guarded, idempotent via marker), writes readback-verified bytes to the DB and rewrites configs/drift_patrol_prompt.txt from the DB bytes so the copy is a readback, never a parallel hand-edit.
- One defect caught by my own readback and fixed before filing: the idempotency marker originally included a closing paren ("TOUCH LAW (B2-237)") that the block text does not contain ("TOUCH LAW (B2-237, binding on this patrol)"), so the first run's UPDATE landed but the marker assert failed; marker corrected to prefix form, rerun aborts cleanly ("already amended"), block count verified 1 (no double-append).
- configs/drift_patrol_prompt.txt (new): the repo-side copy, written from DB readback bytes.
- tests/test_drift_patrol_prompt_copy.py (new, 3 tests): copy exists and carries all three clauses; copy == live DB bytes with drift naming the repair path; DB carries the clauses when reachable. DB-unreachable machines skip.

## Falsifier

Kill conditions: (a) the DB prompt or the repo copy losing any of the three clauses (both tests red), (b) the copy drifting from the DB (equality test red, names the repair script), (c) a future prompt amendment that bypasses the repo copy (same red; the amendment lane must rerun B2_267_update_prompt.py or extend it). The patrol's next 08:00 run is the behavioral witness: its receipt should show touch observations filed under 6b/6c rather than mtime alarms; a mtime-triggered alarm on a size-stable, seal-verifying file after this landing falsifies the wiring.

## Bibliography closed

- watch/inbox/burn_wave_20260926/B2_237_touch_law_20260926.md (the three clauses, read)
- watch/inbox/burn_wave_20260926/B2_199_update_prompt.py (DB update mechanism + prompt lineage, read)
- %USERPROFILE%/.zcode/v2/tasks-index.sqlite automations row automation-a7c71ad1 (read + updated, readback verified)
- tools/freshness_check.py (the pattern whose test style this follows: bytes vs report, stale is red)
- watch/inbox/burn_wave_20260926/B2_222 owed card (the "still no repo copy" state this closes; referenced via the QUEUE B2-267 row)
