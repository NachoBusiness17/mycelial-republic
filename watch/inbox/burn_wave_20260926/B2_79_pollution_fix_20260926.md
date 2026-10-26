# B2-79 gap-log test pollution fix (2026-09-26)

## Verdict

The pollution is fixed at the writer: mag/temperature_stack.py routes every gap-log read and write through _gaps_log() (mag/temperature_stack.py:37), which honors the MAG_GAPS_LOG env override and otherwise keeps the production path memory/training/loop_gaps.jsonl; tests/test_temperature_stack.py::test_track_loop_gap_dedupe now points the log at tmp_path and pins that the production file keeps its byte size across both calls (tests/test_temperature_stack.py:64-91). Targeted suite 6 passed in 0.42s with the production log byte-still (312 total lines and 17 test rows before and after the run). All 17 pollution rows on disk at fix time are annotated in place with a dated pollution field; zero rows erased; the other 295 lines are byte-identical.

Amendment 2026-09-26 ~16:45Z, close-pass byte check: an 18th test row (ts 2026-09-26T16:32:38Z) landed after the annotation pass, written by a concurrent runner still on the pre-fix bytes mid-lane (this lane's own suite runs are provably clean: 313 lines and 18 test rows before and after the final run). The straggler was annotated with the same dated field (idempotent pass, only that 1 line rewritten, unannotated left 0). Final census: 313 lines, 18 test rows, 18 annotated. Verdict unchanged; writer stays decoupled.

Disclosure on the brief's count: the brief and the B2-20 receipt say 11 rows last seen 2026-09-26T10:57Z; bytes at fix time (16:28 to 16:36Z today) hold 17 rows. The extra 6 fired today at 12:59, 13:17, 13:21, 13:26, 13:41 and 13:57Z because the polluting test kept running between the B2-20 census and this landing. The annotation count is 17 at fix time and 18 at close, the numbers the bytes actually hold at each moment; nothing was removed.

## Evidence

- Byte census at fix time: memory/training/loop_gaps.jsonl 312 lines; 17 rows name test_gap_unique_xyz, all detail "unit", where "tests", dedupe c4f076b1e0205c27; span 2026-08-06T23:11:28Z (line 1) to 2026-09-26T13:57:49Z (line 312).
- Writer chain verified on bytes: tests/test_temperature_stack.py called track_loop_gap(force=True), force bypasses the dedupe gate, and the row landed through the module constant GAPS_LOG (mag/temperature_stack.py:32 pre-fix).
- Post-fix grep: the only live GAPS_LOG consumers are inside mag/temperature_stack.py (dist_audit/nacho_business_audit_20260912T214050Z holds a frozen audit copy, untouched); the use sites now call _gaps_log() at mag/temperature_stack.py:362 and :419.
- Suite: .venv/Scripts/python.exe -m pytest tests/test_temperature_stack.py -q = 6 passed in 0.42s; production log total lines and test-row count identical before and after the run.
- Annotation: 17 of 312 lines changed, each by adding one "pollution" field (dated, names the cause, no-erase law); every row still parses; zero test rows left unannotated; the 295 other lines byte-identical (string-compared before write).
- Second pollution surface found on the same writer: memory/improve/candidates.jsonl:95 carries id gap-c4f076b1e0205c27, ts 2026-08-06T23:11:28Z, claim "[loop gap] test_gap_unique_xyz: unit" (the improve side effect of the same pre-fix calls). Left in place per the no-erase law; filed as self-feed B2-330.
- The checkbox on the B2-79 row sat [x] from birth pointing at the spawning B2-20 receipt (no landing receipt existed); this landing earns it per the B2-238 law.

## Work done

1. Claimed QUEUE.md per the shared-file claim law (claim line 2026-09-26T16:28:20Z) before editing it.
2. mag/temperature_stack.py: added import os; added _gaps_log() (env MAG_GAPS_LOG, fallback GAPS_LOG) with a fix comment naming the cause and this receipt; routed _recently_tracked and track_loop_gap through it. No behavior change for production callers (no env set = same path).
3. tests/test_temperature_stack.py: test_track_loop_gap_dedupe now takes tmp_path + monkeypatch, sets MAG_GAPS_LOG to a tmp file, asserts the first call writes exactly 1 row there, the second is deduped, and the production log's size is unchanged across both calls.
4. Annotated the 17 test rows in memory/training/loop_gaps.jsonl in place with the pollution field via a .venv python script; only those 17 lines were rewritten.
5. Verified against bytes (counts above); filed self-feeds B2-330 and B2-331 under Open unchecked; appended the LEDGER row.

## Falsifier

The fix dies if any of these fails: (a) with MAG_GAPS_LOG unset, track_loop_gap still appends to memory/training/loop_gaps.jsonl (backward compat); (b) a fresh pytest run changes the production log (re-run and compare line counts, 312 vs 312 today); (c) any annotated row lost an original field or stopped parsing (parse all 312, compare field sets); (d) the test writes prod when its setenv line is removed. The no-erase claim dies if any pre-annotation non-test line differs at its position in the current file.

## Bibliography closed

tests/test_temperature_stack.py:64-91 ; mag/temperature_stack.py:32,37-49,362,419 ; memory/training/loop_gaps.jsonl (312 lines, 17 annotated) ; memory/improve/candidates.jsonl:95 ; watch/inbox/burn_wave_20260926/B2_20_loop_gaps_20260926.md ; watch/inbox/burn_wave_20260926/QUEUE.md ; memory/burns/LEDGER.jsonl.
