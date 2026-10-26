# f-12: Mag scheduled-task census (2026-09-28 17:47 EDT)

Census method (all numbers below come from commands run this session):

- Inventory: `schtasks //Query //FO CSV //NH` -> 239 task rows machine-wide, 12 grep hits on "mag", of which 11 are true Mag-prefixed tasks (the 12th is `\Microsoft\Windows\Shell\ThemesSyncedImageDownload`, "Image" contains "mag").
- Per-task detail: `schtasks //Query //TN <name> //V //FO LIST` for all 11.
- Cross-checks: repo logs, beat ledgers, script sources, git log, all cited inline.

Verdicts: 7 ALIVE, 2 DEAD, 2 ZOMBIE (one full zombie, one alarm-leg zombie). One task was dead until repaired earlier today.

## The 11 tasks

### 1. \mag-docker-watchdog - ALIVE (quiet by design)
- Script: `wscript.exe watch\docker_watchdog.vbs` -> `powershell -File watch\docker_watchdog.ps1`
- Schedule: one-time trigger 2026-08-26 02:50, repeat every 5 minutes (schtasks: "Repeat: Every: 0 Hour(s), 5 Minute(s)")
- Last run 9/28/2026 5:40:00 PM, Last Result 0, Next 9/28/2026 5:45:00 PM
- Evidence: `watch/docker_watchdog.ps1` writes `logs/docker_watchdog.log` ONLY on RELAUNCH or DEGRADED (healthy ticks are silent by design). Log shows real work: DEGRADED storm 08-26, RELAUNCH 09-11 10:35, 09-19 18:05, 09-24 05:35. Silence since 09-24 means the engine stayed healthy. The probe rows in `logs/docker_ops.jsonl` (last 09-28 17:37:32Z) are written by something else; the ps1 names only the watchdog log (line 5), so I did not attribute those probes to this task.

### 2. \MagCensusPatrolDaily - ALIVE as of today 17:23 (was parse-dead before that)
- Script: `powershell -File scripts\census_patrol_daily.ps1`
- Schedule: daily 08:30, start 9/26/2026
- Last run 9/28/2026 8:30:01 AM, Last Result 1, Next 9/29/2026 8:30:00 AM
- Evidence: fix commit c1c0136cd landed 2026-09-28 17:23:11 -0400, i.e. AFTER the 08:30 scheduled run whose result 1 was the em-dash parse death (4 ParseFile errors per the commit message). A manual pass at 17:20:35 today ran the full body per `logs/census_patrol.log`: census COLLECT-DRIFT fired (pytest holds 2410 collected vs carrier claim 2303, delta +107, bar 20 - a true detection, not a parse failure), meter patrol 4 new 09-28 rows, task doctor named 1 unhealthy task, fossil check 0 WARN / 0 HARD / 6 registered. Exit 1 on the manual pass is the drift alarm working.

### 3. \MagCorpusRescanDaily - ALIVE
- Script: `powershell -File scripts\corpus_rescan_daily.ps1`
- Schedule: daily 03:30, start 9/26/2026
- Last run 9/28/2026 3:30:01 AM, Last Result 0, Next 9/29/2026 3:30:00 AM
- Evidence: `logs/corpus_rescan_daily.log` 09-28 run: incremental, base 561,659 rows, added 14,732, refreshed 5,086, vanished 1,710, total 581,477, exit 0 at 03:33:37. Note: the 09-27 run exited 1 with a PowerShell NativeCommandError ("module named 'mag'") - one bad day, next day clean.

### 4. \MagEndpointNewsDaily - ALIVE
- Script: `powershell -File scripts\endpoint_news_daily.ps1` -> `.venv python scripts\endpoint_news.py` (wrapper read in full)
- Schedule: daily 06:30, start 9/19/2026
- Last run 9/28/2026 6:30:01 AM, Last Result 0, Next 9/29/2026 6:30:00 AM
- Evidence: `logs/endpoint_news.log` 09-28: pass_complete true, rows 35, model_events empty. Across the log, 8 `"model_events"` lines of which 4 are empty arrays, so 4 logged passes carried real model events. Working, low volume.

### 5. \MagFtsIndexDaily - ALIVE (best-in-estate self-healer)
- Script: `powershell -File scripts\fts_index_daily.ps1` -> `tools\corpus_fts_rebuild.py --check --deep`
- Schedule: daily 09:00, start 9/26/2026
- Last run 9/28/2026 9:00:01 AM, Last Result 0, Next 9/29/2026 9:00:00 AM
- Evidence: `logs/fts_index.log` 09-28 09:00:09: PRE check exit 2 (index older than catalog.jsonl), auto-rebuild through the sanctioned writer (581,477 rows, 27.7s, db 161,345,536 bytes), POST check fresh with deep sha match, exit 0. The detect-then-heal loop worked exactly as designed end to end.

### 6. \MagImproveDaily - ALIVE
- Script: `powershell -File scripts\improve_daily.ps1`
- Schedule: daily 08:00, start 9/26/2026
- Last run 9/28/2026 8:00:01 AM, Last Result 0, Next 9/29/2026 8:00:00 AM
- Evidence: `logs/improve_daily.log` END exit=0 at 08:00:01 with paths for latest.md / field_brief.md / candidates.jsonl; `memory/improve/latest.md` mtime 2026-09-28 08:01:21, `memory/improve/candidates.jsonl` mtime 2026-09-28 13:46:25. Real outputs land daily.

### 7. \MagLabKit8765 - DEAD (crash fossil)
- Script: `cmd /c cd /d C:\Users\foste\Documents\projects\mag-sovereign-kit && <repo>\.venv\Scripts\python.exe main.py lab --host 127.0.0.1 --port 8765` (points at a DIFFERENT project directory)
- Schedule: One Time Only, start date 1/1/2099
- Last run 8/1/2026 9:31:40 AM, Last Result -1, Status Disabled, Next Run N/A
- Evidence: never ran since the 08-01 crash, disabled, next run pushed to 2099. Matches theater-audit finding F3 (Aug-1 crash fossil, 0xFFFFFFFF).

### 8. \MagPrivateOffice8765 - DEAD (crash fossil, duplicate of #7)
- Script: `cmd /c cd /d <repo> && <repo>\.venv\Scripts\python.exe main.py lab --host 127.0.0.1 --port 8765`
- Schedule: One Time Only, start date 1/1/2099
- Last run 8/1/2026 9:32:40 AM, Last Result -1073741510 (= 0xC000013A STATUS_CONTROL_C_EXIT), Status Disabled, Next Run N/A
- Evidence: same fossil shape as #7, crashed 60 seconds later with Ctrl-C exit. Matches theater-audit finding F4. Both 8765 fossils should be deleted or re-armed by the operator; not done here (census only).

### 9. \MagQCaptionVerifyDaily - ALIVE
- Script: `.venv\Scripts\pythonw.exe scripts\qcaption_verify_daily.py` (windowless; receipt ledger `watch/inbox/QCAPTION_VERIFY_BEAT.jsonl`, per the script docstring, B2-271)
- Schedule: daily 07:30, start 9/26/2026
- Last run 9/28/2026 7:30:01 AM, Last Result 0, Next 9/29/2026 7:30:00 AM
- Evidence: 3 of 3 beats PASS (09-26 20:23:50Z, 09-27 11:30:02Z, 09-28 11:30:02Z; each "RESULT: PASS - 267 rows, 163 drops"). The falsifier row the design requires would be a FAIL row; none yet.

### 10. \MagSecretScanWeekly - ZOMBIE (scanner half alive, alarm leg dead)
- Script: `.venv\Scripts\pythonw.exe scripts\secret_scan_weekly.py`
- Schedule: weekly Monday 06:40, start 9/26/2026
- Last run 9/28/2026 6:40:00 AM, Last Result 0, Next 10/5/2026 6:40:00 AM
- Evidence: the scan runs and the beat lands: `watch/inbox/SECRET_SCAN_BEAT.jsonl` has 2 rows (09-26 21:13:04Z and 09-28 11:05:40Z, i.e. ~25 min after the 06:40 EDT trigger, consistent with a long corpus scan). BOTH rows report critical=1 (high=48,544 then 49,533), and the top files_with_rule_hits entry both times is `corpus/canon/x_canon_2026_fx/fx_2082662744893845828.json` - a corpus document, i.e. the critical is almost certainly a scanner false positive over owned data. The script's second leg (prepend a dated ALERT line to `memory/attention.md` when critical>0, per scripts/secret_scan_weekly.py) produced nothing: `grep "secret scan beat" memory/attention.md` = 0 hits and `grep -i secret memory/attention.md` = 0 hits at census time. So the one task whose whole point is to surface a critical finding has never surfaced it. Matches theater-audit F7 and is still true for the 09-28 run.

### 11. \MagVisionNightly - ZOMBIE (pure)
- Script: `powershell -File scripts\vision_nightly.ps1`
- Schedule: daily 02:30, start 9/19/2026
- Last run 9/28/2026 2:30:01 AM, Last Result 0, Next 9/29/2026 2:30:00 AM
- Evidence: `logs/vision_nightly.log`: 12 "START mode=run" passes, 11 of them ended "no-op (0 remaining, corpus complete)" with coverage 1980/1980 since 09-25. The only END ok=1 lines in the whole log are a read-only smoke (09-19) and a dry-run (09-25). Zero inference has ever fired from the nightly; it wakes daily, exits 0, does nothing. Matches theater-audit F17 ("11 no-ops, never any work"). Candidate for schedule deletion or a completion-ratchet trigger.

## Cross-cutting finding: the attention.md alert channel is lossy

Two different tasks claimed they appended/prepended alerts to `memory/attention.md` today, and neither alert is in the file at census time (17:47 EDT):

- `scripts/census_patrol_daily.ps1:79-80` logged "ALERT appended to memory/attention.md" at 17:20:35 (COLLECT-DRIFT alert); `grep -in "COLLECT-DRIFT|CENSUS-PATROL|TASK-DOCTOR" memory/attention.md` = 0 hits.
- `scripts/secret_scan_weekly.py` should have prepended a critical alert on 09-26 and again on 09-28 (critical=1 both runs); 0 hits (see #10).
- `memory/attention.md` mtime is 2026-09-28 17:45:21, i.e. something rewrote the file AFTER the patrol's 17:20 append and the alert lines are gone.

So alerts are being written by the producers and lost before consumption. This is a separate defect from any single task; I did not fix it or chase the rewriter (census scope). The patrol log is the surviving alarm surface right now.

## Summary table

| Task | Schedule | Last result | Next run | Verdict |
|---|---|---|---|---|
| mag-docker-watchdog | every 5 min | 0 | 9/28 5:45 PM | ALIVE (quiet-by-design) |
| MagCensusPatrolDaily | daily 08:30 | 1 (pre-fix) | 9/29 8:30 AM | ALIVE (repaired 17:23 today) |
| MagCorpusRescanDaily | daily 03:30 | 0 | 9/29 3:30 AM | ALIVE |
| MagEndpointNewsDaily | daily 06:30 | 0 | 9/29 6:30 AM | ALIVE |
| MagFtsIndexDaily | daily 09:00 | 0 | 9/29 9:00 AM | ALIVE (self-healed today) |
| MagImproveDaily | daily 08:00 | 0 | 9/29 8:00 AM | ALIVE |
| MagLabKit8765 | one-time 1/1/2099 | -1 (8/1) | N/A, Disabled | DEAD fossil |
| MagPrivateOffice8765 | one-time 1/1/2099 | -1073741510 (8/1) | N/A, Disabled | DEAD fossil |
| MagQCaptionVerifyDaily | daily 07:30 | 0 | 9/29 7:30 AM | ALIVE (3/3 PASS) |
| MagSecretScanWeekly | weekly Mon 06:40 | 0 | 10/5 6:40 AM | ZOMBIE (alarm leg dead, critical is corpus FP) |
| MagVisionNightly | daily 02:30 | 0 | 9/29 2:30 AM | ZOMBIE (11 straight no-ops, zero work ever) |

Census instrument note: counts are from `schtasks //Query` at 2026-09-28 ~17:35-17:47 EDT on DESKTOP-7C70KSC, one tree, one moment. Mirror copy: `task-census.md` in this directory (byte-identical).
