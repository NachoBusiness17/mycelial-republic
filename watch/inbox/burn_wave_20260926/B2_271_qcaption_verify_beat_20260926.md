# B2-271 Scheduled caption-ledger data-side verify beat (SW-07, 2026-09-26)

## Verdict

LANDED. The 7-check verifier now runs on a schedule independent of script changes: scripts/qcaption_verify_daily.py wraps scripts/the50_t21_q_caption_ledger_verify.py and lands one append-only row per run (schema qcaption_verify_beat.v1: ts, result PASS/FAIL, the full RESULT line, ledger row count, verifier exit) in watch/inbox/QCAPTION_VERIFY_BEAT.jsonl. Registered as schtask MagQCaptionVerifyDaily, daily 07:30 local, next run 9/27/2026 7:30 AM, Status Ready. Live fire this lane: RESULT: PASS - 267 rows, 163 drops, span 1993-06 .. 2041-12-31, beat row landed with ledger_rows 267.

## Evidence file:line quotes

- QUEUE.md row: "a hand edit of watch/inbox/qdrop_export/q_caption_ledger.jsonl, a qdrops.jsonl re-harvest, or a mid-flight concurrent regen can sit unverified indefinitely while nobody touches the two scripts; register a scheduled verify (schtasks pattern per the B2-235 filed line, or a main.py/pile-classify hook) that runs the 7-check verifier daily and lands its RESULT line plus row count in watch/inbox".
- The gap, named in scripts/qcaption_verify_daily.py header: "the B2-260 pre-push caption gate fires only when the generator or verifier script changes, so data-side rot ... sat unverified indefinitely".
- Install output: `SUCCESS: The scheduled task "MagQCaptionVerifyDaily" has successfully been created.`; query: Next Run Time 9/27/2026 7:30:00 AM, Status Ready.
- First beat row: `{"ts": "2026-09-26T20:23:50Z", "schema": "qcaption_verify_beat.v1", "result": "PASS", "result_line": "RESULT: PASS - 267 rows, 163 drops, span 1993-06 .. 2041-12-31", "ledger_rows": 267, "verifier_exit": 0}`.

## Work done

- scripts/qcaption_verify_daily.py: runs the verifier via the repo venv python, parses the RESULT line, counts ledger rows from bytes, appends the beat row, exits nonzero on FAIL (so a task-scheduler history also shows the failure).
- schtasks MagQCaptionVerifyDaily registered (daily 07:30, before the 08:00 MagImproveDaily beat).
- One live beat fired and landed.

## Falsifier

From the brief: "a hand-inserted schema-valid but pin-violating ledger row sits unflagged for more than 24h with no scheduled verify output filed" -- falsified by construction now: any pin violation fails check7 within 24h and the FAIL row lands in QCAPTION_VERIFY_BEAT.jsonl with the task history showing a nonzero exit. Reopen if: the beat file shows no new row for a calendar day while the schtask exists (task silently broken), or a FAIL row lands and nothing references it within the next session.

## Bibliography closed

Read: scripts/the50_t21_q_caption_ledger_verify.py (RESULT emission, line 480), watch/inbox/qdrop_export/q_caption_ledger.jsonl (row count), scripts/register_improve_task.ps1 (schtasks pattern), QUEUE.md B2-271 row, live verifier + beat runs. No external sources.
