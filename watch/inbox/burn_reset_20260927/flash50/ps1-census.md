# ps1-census: every PowerShell script in scripts/ (item f-28, 2026-09-28)

Census of all 35 `.ps1` files in `scripts/` (listing: `ls -la scripts/*.ps1`, 2026-09-28).
For each: what it does, scheduled-task registration, last-run evidence, and the
Set-Location fix. All times local (EDT, UTC-4) unless stamped Z.

Method (commands run this session, 2026-09-28):

1. `ls -la scripts/*.ps1` -> 35 files, 376 B to 9,733 B, mtimes 2026-08-04 to 2026-09-28.
2. `grep -n "Set-Location" scripts/*.ps1` -> 14 files carry the cmdlet.
3. Scheduled-task sweep: PowerShell `Get-ScheduledTask` over ALL tasks, filter actions
   matching `local_sovereign_agent|\scripts\` -> 19 task rows; exactly 7 target
   `scripts\*.ps1` (two more target `scripts\*.py` via pythonw: MagQCaptionVerifyDaily,
   MagSecretScanWeekly; those are python, out of ps1 scope, noted only).
4. Per-task `schtasks /Query /TN <name> /V /FO LIST` for Last Run Time / Last Result /
   Next Run Time; `Get-ScheduledTask ... .Date` for creation stamps.
5. Log tails: `tail -3` on each script's log under `logs/` (and `watch/android_warden.log`).
6. Artifact probes for non-logging scripts: `.cursor/`, Desktop `*.lnk`, Startup folder,
   `.mag_active_env`, `../mag_test_env`, `memory/narrative_corpus/PULL_STAMP.txt`,
   `memory/_hermes_probe.txt`, `ollama list`, emulator process check (`tasklist`).
7. Fix provenance: `watch/inbox/lens_20260927/THE_LENS_20260927.md:90` and
   `watch/inbox/WINDOW_CLOSE_20260927_GATEFIX_LENS.md:103` record the root cause class:
   MagCorpusRescanDaily failed EVERY fire pre-fix because a scheduled task starts in
   `C:\Windows\System32` and `python -m mag...` needs CWD = repo root.

## Headline numbers

- 35 ps1 scripts; 7 registered as scheduled tasks; 8 are the register_* installers for
  those tasks; 20 are manual/one-shot/daemon scripts.
- All 7 task-registered scripts fired on 2026-09-28 (Last Run Times 02:30 to 09:45):
  5 exited 0, 2 exited 1 (Estate Ratchet = real config-seal debt; MagCensusPatrolDaily =
  expected COLLECT-DRIFT verdict, but its 08:30 fire left no log block, see K3).
- Set-Location fix: 14 scripts carry the literal `Set-Location` cmdlet; +2 more carry an
  equivalent (`cd $Root` in edit_env.ps1:11; `Push-Location $Root` wrappers in
  env_switch.ps1:31/50/76/102) = 16/35 with a CWD fix. 18 more need none (every path is
  `$PSScriptRoot`-derived absolute, or the script has no repo-relative file work).
  1 real gap: setup_hermes_ollama.ps1 (K6).
- 2 scripts still write UTF-16 logs via Tee-Object (improve_daily.ps1:26,
  ratchet_daily.ps1:27/31/35), the exact mojibake defect fts_index_daily.ps1:67-70 and
  census_patrol_daily.ps1:53-56 document and fixed in their own lanes (K5).

## A. Task-registered scripts (7) - all have the Set-Location fix, all fired 2026-09-28

| # | Script | Does what | Task (created) | Last run / result | Set-Location |
|---|--------|-----------|----------------|-------------------|--------------|
| 1 | ratchet_daily.ps1 | Estate daily meters: `tools/config_seal.py verify` + `tools/freshness_check.py` + `tools/violation_ratchet.py check`; exit 1 if any fail (script lines 27-41) | `\Estate Ratchet` (2026-09-25T13:33:19, daily 09:45) | 9/28/2026 9:45:02 AM, Last Result 1; log `logs/ratchet_daily.log` END 09:45:02 `seal=1 freshness=0 ratchet=0` (seal hit: GROWTH claim e066832a0b8edb5e, tools/stealth_driver.py accepted at 753 lines, now 798, +45, re-audit or re-accept by name; RATCHET PASS) | YES :6 |
| 2 | census_patrol_daily.ps1 | Census deep check (`tools/census_drift_patrol.py --collect`) + dated meters (`tools/meter_patrol.py`) + fleet task doctor + fossil_check; alerts to memory/attention.md on drift/gap (lines 57-188) | `\MagCensusPatrolDaily` (2026-09-26T11:31:00, daily 08:30) | Task says 9/28 8:30:01 AM result 1, but `logs/census_patrol.log` has NO 08:30 block for 9/28 (jumps 09-27 08:30 END exit=0 to 09-28 17:20:35); the 17:20:35 block (hand or /Run) END exit=1: `CENSUS-PATROL: COLLECT-DRIFT - pytest holds 2410 vs carrier claim 2303 (delta +107, bar 20)` | YES :33 |
| 3 | corpus_rescan_daily.ps1 | Incremental corpus rescan + tags + manifest stamp via `.venv python -m mag.catalog_rescan incremental` | `\MagCorpusRescanDaily` (2026-09-26T15:20:13, daily 03:30) | 9/28 3:30:01 AM, result 0; log END 03:33:37 exit 0 (added 14732, refreshed 5086, unchanged 550084, map_bytes 160053773) | YES :13, with the 2026-09-27 autopsy comment naming ModuleNotFoundError 'mag' (lines 8-13) |
| 4 | endpoint_news_daily.ps1 | One pass of `scripts/endpoint_news.py`, log tail 40 lines | `\MagEndpointNewsDaily` (2026-09-19T12:57:50, daily 06:30) | 9/28 6:30:01 AM, result 0; log END 06:30:01 exit=0, model_events [] | YES :5 |
| 5 | fts_index_daily.ps1 | FTS5 index `--check --deep`, rebuild through the one sanctioned writer on stale, POST re-check, alert row to watch/inbox/fts_index_alerts.jsonl on failure (lines 71-148) | `\MagFtsIndexDaily` (2026-09-26T15:26:39, daily 09:00) | 9/28 9:00:01 AM, result 0; log END 09:00:09 exit=0 (routine stale-then-rebuilt, POST exit=0 wall 0.637s) | YES :43 |
| 6 | improve_daily.ps1 | Daily scout+eval: `main.py improve --once` (L0) | `\MagImproveDaily` (2026-09-26T00:22:51, daily 08:00) | 9/28 8:00:01 AM, result 0; log END 08:00:01 exit=0 (log is UTF-16, K5) | YES :5 |
| 7 | vision_nightly.ps1 | Nightly Mr Pool vision triage drain via `scripts/vision_nightly.py --run`; wrapper only writes START/END markers (2026-09-19 Tee-collision fix, lines 25-29) | `\MagVisionNightly` (2026-09-19T13:02:48, daily 02:30) | 9/28 2:30:01 AM, result 0; log END 02:30:01 exit=0, driver no-op: coverage 1980/1980 remaining=0 corpus complete | YES :7 |

Registration action for all 7: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File
C:\...\scripts\<name>.ps1` (read off each task's Task To Run). No task registered any
other ps1 in scripts/ (full-repo task sweep, step 3 above).

## B. register_* installers (8) - each (re)creates one task via schtasks /Create /F

All 8 follow the same shape: delete task if exists, `schtasks.exe /Create /TN <name> /TR
"powershell.exe -NoProfile -ExecutionPolicy Bypass -File <abs path>" /SC DAILY /ST <hh:mm>`.
They need no Set-Location (absolute paths only). Their last-run evidence is the created
stamp on the task each one owns (a /Create /F replaces, so task Date = register script's
last successful run): register_ratchet_task.ps1 -> 09-25T13:33:19,
register_census_patrol_task.ps1 -> 09-26T11:31:00, register_corpus_rescan_task.ps1 ->
09-26T15:20:13, register_endpoint_news_task.ps1 -> 09-19T12:57:50,
register_fts_index_task.ps1 -> 09-26T15:26:39, register_improve_task.ps1 ->
09-26T00:22:51, register_vision_nightly.ps1 -> 09-19T13:02:48.
Exception, K2: register_day_end_task.ps1 (mtime Sep 28 14:59) creates `MagDayEndPileDaily`
daily 20:00, but `schtasks /Query /TN MagDayEndPileDaily` returns ERROR: The system cannot
find the file specified -> that register script has never successfully run.

## C. Manual / one-shot / daemon scripts (20)

| # | Script | Does what | Registered? | Last-run evidence | Set-Location |
|---|--------|-----------|-------------|-------------------|--------------|
| 8 | day_end_pile.ps1 | FW-50 day-end habit: `mag.state_snapshot.capture_summary(kind=session_end)` + `tools/pile_classify.py --limit 50` local drain; alerts attention.md on exit >= 2 | NO (register exists, task absent, K2) | Ran by hand today: `logs/day_end_pile.log` END 15:00:27 exit=0 (pile=144, classified_this_run=1) | YES :20 |
| 9 | android_warden.ps1 | Infinite loop keeping headless AVDs medium_phone + watcher_2 alive; logs to watch/android_warden.log; header states NOT a scheduled task by design | NO (by design) | `watch/android_warden.log` last line 2026-09-05 11:24:51 "starting watcher_2"; tasklist shows 0 emulator/qemu processes now -> not currently alive | none, CWD-safe (absolute paths, :13) |
| 10 | improve_deep.ps1 | Opt-in deep improve: `main.py improve --deep --minutes --max-tickets`; header: "Not registered as a scheduled task by default" | NO (by design) | `logs/improve_deep.log` does not exist -> no run evidence found | YES :13 |
| 11 | review_with_rope.ps1 | Grok review preamble: trail start + `context-pack --agent` + prints the /workflow review-changes line | NO | `memory/agent_preamble_latest.md` (the file this flow writes) mtime today 18:43; writer is `context-pack --agent` which the script calls, so consistent with use today but not proof the wrapper itself ran | YES :15 |
| 12 | setup_desk_gpu.ps1 | One-shot: create ollama model gemma4-desk (num_ctx 8192 GPU fit) + patch configs/lanes.yaml desk_orchestrator | NO | `ollama list` shows `gemma4-desk:latest` 9.6 GB modified "7 weeks ago" (creation ~early Aug) | none, CWD-safe (Join-Path $Root absolute) |
| 13 | setup_hermes_ollama.ps1 | One-shot Hermes setup: OLLAMA_CONTEXT_LENGTH=65536 user env, gemma4-hermes model, hermes config, LOCALAPPDATA .env keys, SOUL.md, tool probe | NO | `ollama list` shows `gemma4-hermes:latest` "2 months ago"; `memory/_hermes_probe.txt` mtime Jul 24 20:36 -> probe ran Jul 24 | NO - real gap, K6 |
| 14 | pull_narrative_corpus.ps1 | Clone 5 (+2 optional) OSS narrative/IF repos + 2 Gutenberg PD texts into mine/raw/narrative_corpus, write stamp | NO | `memory/narrative_corpus/PULL_STAMP.txt`: pulled=2026-08-06T23:57:45 (5 repos, no -All) | none, CWD-safe (derives root from $MyInvocation, Push-Location for git ops) |
| 15 | ensure_venv.ps1 | Create .venv if missing + `pip install -r requirements.txt` + langgraph/httpx/reportlab import check | NO | `.venv` exists and is used daily by every task above, but no log attributes a run to this script; no direct run evidence found | YES :4 |
| 16 | install_cursor_hooks.ps1 | Copy configs/cursor/hooks.json + mag-cursor-seat.mdc into .cursor/ | NO | `.cursor/hooks.json` Aug 4 18:48 and `.cursor/rules/mag-cursor-seat.mdc` Aug 31 06:51 exist -> ran at least to those dates | none, CWD-safe ($PSScriptRoot-absolute) |
| 17 | install_desktop_shortcuts.ps1 | Create Desktop (+Start Menu) .lnk launchers for the mag_*.cmd fleet | NO | Desktop scan today shows NO Mag*.lnk (only Bionic/Groq/Hermes/OpenCode/Roblox) -> its artifacts are absent; no current run evidence | none, CWD-safe |
| 18 | install_mag_startup.ps1 | Create Startup "MAG Start.lnk" -> boot_mag.cmd at login | NO | Startup folder has NO MAG Start.lnk (it has mag_boot_lane.cmd Sep 27, a different mechanism) -> artifact absent | none, CWD-safe |
| 19 | bootstrap_test_env.ps1 | git worktree test clone (../mag_test_env) + venv + doctor + pytest + optional lab on :8770 | NO | `../mag_test_env` not found -> no artifact; no run evidence found | YES :24 (to $TestRoot, the worktree, correct for its purpose) |
| 20 | routing_smoke.ps1 | Thin wrapper: run `scripts/routing_smoke.py` with repo venv | NO | routing_smoke.py has no log; no run evidence found | NO but verified safe: routing_smoke.py resolves ROOT from `__file__` and inserts it into sys.path (scripts/routing_smoke.py:20-22) |
| 21 | edit_env.ps1 | Open .env in notepad, then `main.py providers` | NO | .env exists (edited often); no attribution to this script possible | equivalent: `cd $Root` :11 (cd grammar, not the cmdlet) |
| 22 | env_switch.ps1 | Branch+port env tracks: list/use/status/run/sync via mag.env_registry | NO | `.mag_active_env` absent at repo root -> no track active; no run evidence today | equivalent: every python call wrapped in Push-Location $Root (:31-43, :50-63, :76-95, :102-120) |
| 23 | openclaw_dash.ps1 | Open OpenClaw UI (:18789) as browser app window with token read from .env; docker compose up openclaw if down | NO | No log; browser app windows leave no queryable trace; no run evidence found | none, CWD-safe (docker compose -f absolute) |
| 24 | mag_exec.ps1 | Run `main.py <args>` inside the mag docker container | NO | No log; no run evidence found | YES :9 |
| 25 | install.ps1 | Container-first install: docker compose up -d --build, health wait, in-container doctor, optional shortcuts | NO | No log; no run evidence found this session (docker image age not probed) | YES :17 |
| 26 | fix-wifi.ps1 | Admin one-shot: WLAN services nativewifip/Ndisuio/Netman/WlanSvc to Automatic, registry Start=2, remove phantom TP-Link USB, bounce Wi-Fi | NO | No log; no run evidence found | none, needs none (no repo-relative work) |
| 27 | blast_connect_vast.ps1 | Foreground SSH tunnel localhost:11434 -> vast-host ollama (params -HostIp/-Port/-User) | NO | Ephemeral by design; no log; no run evidence findable | none, needs none (no repo-relative work) |
| 28-35 | register_census_patrol_task.ps1, register_corpus_rescan_task.ps1, register_day_end_task.ps1, register_endpoint_news_task.ps1, register_fts_index_task.ps1, register_improve_task.ps1, register_ratchet_task.ps1, register_vision_nightly.ps1 | See section B | They ARE the registrars | See section B creation stamps | none, needs none (absolute paths) |

## Findings (K-numbered)

- K1 (green): the fix works where it matters. The script the Set-Location fix was created
  for, corpus_rescan_daily.ps1, carries it with the autopsy comment
  (scripts/corpus_rescan_daily.ps1:8-13) and has been exit-0 since: today 03:30 fire exit 0,
  14,732 rows added. All 7 task-registered scripts have the fix; all 7 fired today.
- K2 (actionable): MagDayEndPileDaily is NOT registered. day_end_pile.ps1 and
  register_day_end_task.ps1 both landed today (mtimes Sep 28 15:02 / 14:59, FW-50), the
  script ran once by hand at 15:00:27 exit 0, but `schtasks /Query /TN MagDayEndPileDaily`
  -> "The system cannot find the file specified". Tonight's 20:00 fire will not happen
  until someone runs the register script.
- K3 (anomaly, unexplained): MagCensusPatrolDaily's Task Scheduler record says Last Run
  9/28 8:30:01 AM result 1, but logs/census_patrol.log contains no 08:30 block that day
  (the previous block is 09-27 08:30:02 END exit=0; the next is 09-28 17:20:35). The
  script's first action after Set-Location is Write-Log START, so a fire that reached the
  script should have stamped the log. The 08:30 failure mode is therefore unlogged and
  unexplained here; the census does not guess it. The logged 17:20:35 run exited 1 with
  COLLECT-DRIFT: pytest holds 2410 vs the AGENTS.md carrier claim 2303 (delta +107, bar 20)
  - a real drift for the census-carrier owner to refresh, noted, not acted on (not this
  item's lane).
- K4 (red meter, real): Estate Ratchet result 1 is a genuine config-seal debt hit, not a
  harness fault: GROWTH claim e066832a0b8edb5e, tools/stealth_driver.py accepted at 753
  lines is now 798 (+45); per the log line it needs re-audit or re-accept by name.
  Freshness and the violation ratchet itself both passed (seal=1 freshness=0 ratchet=0).
- K5 (defect, known class): improve_daily.ps1:26 and ratchet_daily.ps1:27/31/35 still use
  `Tee-Object -FilePath` which in Windows PowerShell 5.1 writes UTF-16 with no -Encoding
  flag; `file` reports both logs as "data" and their tails render with per-character
  spacing. fts_index_daily.ps1:67-70 and census_patrol_daily.ps1:53-56 document this exact
  defect and avoid Tee-Object in their lanes. Exit codes are unaffected (schtasks reads
  them fine); the logs are mojibake for UTF-8 tooling.
- K6 (gap): setup_hermes_ollama.ps1 has no Set-Location and its step-7 probe runs
  `& $py -c "...from harness.hermes_cli import escalate_via_hermes..."` where $py is the
  repo venv python; `python -c` puts CWD at sys.path[0], so that import only resolves when
  the script is invoked with CWD = repo root. It is a run-once setup script (last probe
  artifact Jul 24) so the exposure is small, but it is the one script in the tree with a
  live CWD dependence and no fix.
- K7 (deployment drift): the two installer scripts whose artifacts are deletable by hand
  show absent outputs today: no Mag*.lnk on the Desktop (install_desktop_shortcuts.ps1) and
  no MAG Start.lnk in the Startup folder (install_mag_startup.ps1, whose boot_mag.cmd
  target was superseded by Startup/mag_boot_lane.cmd Sep 27). The scripts exist; their
  products are not deployed.

## Set-Location fix tally (35 total)

- Literal `Set-Location`: 14 - bootstrap_test_env:24, census_patrol_daily:33,
  corpus_rescan_daily:13, day_end_pile:20, endpoint_news_daily:5, ensure_venv:4,
  fts_index_daily:43, improve_daily:5, improve_deep:13, install:17, mag_exec:9,
  ratchet_daily:6, review_with_rope:15, vision_nightly:7.
- Equivalent fix: 2 - edit_env (`cd $Root` :11), env_switch (Push-Location $Root wrappers).
- No fix, CWD-safe by construction: 18 - android_warden, blast_connect_vast, fix-wifi,
  install_cursor_hooks, install_desktop_shortcuts, install_mag_startup, openclaw_dash,
  pull_narrative_corpus, routing_smoke, setup_desk_gpu, and the 8 register_* installers.
- No fix, real gap: 1 - setup_hermes_ollama (K6).
- 16/35 carry the fix; 7/7 task-registered scripts carry it.

## Out of ps1 scope, noted

The repo's scheduled surface also runs two python scripts via pythonw, neither ps1:
MagQCaptionVerifyDaily -> scripts/qcaption_verify_daily.py and MagSecretScanWeekly ->
scripts/secret_scan_weekly.py (read off their task actions in the sweep of step 3).
