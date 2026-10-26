# B2-140 Arm C 200-leg close-out fold (SW-07, 2026-09-26)

## Verdict

FILED AS OWED (the brief's own condition did not fire). The brief folds the final solve count "when the leg lands" -- the leg has not landed. This lane ran the full 200-leg (run_armC.py, gemma keep_alive 2h pin, 20:04Z start) and killed it at ~21:10Z inside problem 2 with exactly 1/30 rows on disk; 66 minutes for one problem projects a multi-hour leg and the box was not left burning overnight. The honest close-out is now on the close receipt as a dated addendum: the RUNNING status is preserved with byte state, prior partials enumerated, bars stay frozen (>=15/30 secondary; trained-judge 30/30 interference reference), no claims from n=1, and the rerun is Owed for the next lane with box time.

## Evidence file:line quotes

- QUEUE.md row condition: "when the leg lands, fold the final solve count into BOOT_LANE_INTERFERENCE_BURN_CLOSE_20260926.md and correct the >=15/30 secondary reading against the trained-judge 30/30 interference reference".
- Run log tail, memory/runs/interference_replication_20260925/armC_200_run_log.txt: `budget=200 [1/30] solved=True rounds=3` (last line; no further problems in 66 minutes); armC_gemma2b_judge_200.jsonl: 1 row.
- Byte census: armC_200_attempt1_starved.jsonl, armC_200_attempt2_partial.jsonl, armC_200_attempt3_partial.jsonl each hold exactly 1 row (problem 1 solved; the attempt-3 copy was made before this lane's full run so the prior partial byte state is preserved).
- The fold, BOOT_LANE_INTERFERENCE_BURN_CLOSE_20260926.md addendum: "The leg still has NOT landed; no solve count exists and the >=15/30 secondary reading stays unmeasured ... Bars remain frozen per amendment 1 ... OWED for the next lane with box time: rerun ... run_armC.py to completion".
- The pre-addendum close text this lane preserved: "ARM C budget-200: RUNNING, 1/30 with the first problem SOLVED (n=1, no claims until the leg completes.)" (close receipt lines 13-14).

## Work done

- Preserved the prior partial as armC_200_attempt3_partial.jsonl before the full attempt (the script rewrites its output file).
- Launched and monitored the full leg; killed it at the 66-minute mark with the honest state quoted above; archived the run log inside the run directory.
- Appended the dated status addendum to BOOT_LANE_INTERFERENCE_BURN_CLOSE_20260926.md (the close receipt this brief names), carrying the frozen bars, the byte census, the rerun instruction, and the receipt pointer.

## Falsifier

The brief's fold condition fires only when the leg lands; it has not, so nothing was folded as a result. Reopen when: run_armC.py completes (then fold the final solve count against >=15/30 and the 30/30 reference, and retire this owed); or if any receipt claims a 200-leg solve count while armC_gemma2b_judge_200.jsonl holds fewer than 30 problem rows plus its summary row -- that claim would be fabrication.

## Bibliography closed

Read: watch/inbox/BOOT_LANE_INTERFERENCE_BURN_CLOSE_20260926.md (scoreboard + open items, pre/post addendum), watch/inbox/INTERFERENCE_REPLICATION_PREREG_AMENDMENT1_20260925.md:24-28 (frozen bars), memory/runs/interference_replication_20260925/run_armC.py (budgets, output path, no-resume), the four armC-200 jsonl files (byte counts), run log tail. No external sources.
