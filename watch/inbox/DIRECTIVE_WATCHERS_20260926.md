# DIRECTIVE: silent watchers — lead, follow, or get out of the way

**Issued:** 2026-09-26 ~07:05 ET by the seat, on operator boot order (verbatim:
"New day tell my silent watchers to lead follow or get out of the way").
**Scope:** every autonomous process on the box + all fleet crons. Classification
is by observed work, not by intent. Evidence per row. Enforcement applied same hour.

## LEAD (driving estate work, untouched)

| Watcher | Evidence |
|---|---|
| Burn churn cron (every 2h) | 13 runs, last fired 06:00 ET today, on schedule |
| Drift patrol cron (08:00) | 12 runs, last 9/25 08:00, fires in <1h |
| Free-resource scout cron (09:00) | 8 runs, last 9/25 09:00 |
| Wave tide cron (06:15) | 10 runs, fired 06:15 ET today |
| Arm C 200 interference run (relaunch) | see FOLLOW→restart note below |

## FOLLOW (supporting the lanes, untouched)

| Watcher | Evidence |
|---|---|
| Hermes gateway (2 procs) | dormant-but-dispatch-capable by design since 9/25 23:47 reboot; $220 armed |
| Ghost cycle (PID 3156) | standard 120s cycler, restarted 06:50 with the morning wave |
| Governor autorun_loop (PID 16100) | started 06:50 ET today, moderate CPU, no crash-loop observed this morning (9/19 live-fire incident remains on record, autopsy still owed) |
| Lane supervisor probe (PID 12660) | fired sharp 07:00:00 ET, scheduled probe |
| Ollama (PID 11112) | healthy, 11434 answers, model loaded |

## OUT OF THE WAY (enforced)

| Watcher | Evidence | Action |
|---|---|---|
| Duplicate Arm C runner (PID 19708, .venv) | started 06:07:19.080, ZERO CPU after ~1h; same script, same args, same OUT file as live twin; script opens OUT with `open("w")` — a second writer truncates/interleaves and double-spends the prereg budget | **KILLED 07:03 ET**, taskkill confirmed |

## Incident receipt — Arm C 200 double-start and recovery

1. 06:07:19 ET: `run_armC.py` started TWICE within 9 ms (PIDs 19708 .venv, 11560 uv-python).
   Both write `armC_gemma2b_judge_200.jsonl` in `"w"` mode. One solved row landed
   (i=0, target 684, cost 114/200, solved=true).
2. 07:03 ET: duplicate 19708 killed per directive. Live twin 11560 found DEAD minutes
   later, cause unknown (not killed by the seat; it held 9-core CPU then vanished).
   Preserved its partial row verbatim: `armC_200_attempt2_partial.jsonl`.
3. 07:06 ET: clean single relaunch via repo venv (background exec_ddb24380,
   this session). Ollama verified healthy and script keep_alive fix ("2h") present
   before relaunch. Fresh run rewrites the outfile from i=0 per the script's own
   attempt pattern (attempt-1 rows already preserved in `armC_200_attempt1_starved.jsonl`).

**Falsifier for the relaunch:** if `armC_gemma2b_judge_200.jsonl` shows no new row
within ~40 min, the relaunch failed too — next autopsy is strace-level, not another blind restart.

## Standing order going forward

Every silent watcher now holds one of the three ranks. Anything unclassifiable
is OUT by default. One writer per output file, always. Watchers that burn
without a receipt join the kill list at next patrol.
