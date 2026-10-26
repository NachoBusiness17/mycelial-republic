# HEADED WINDOWS CURED - 2026-10-05 (post-reboot, operator ask: "stop launching headed python windows")

## Symptom / cause
Console windows popping on the operator's desktop all day. Cause: 24 Task
Scheduler tasks (all LogonType Interactive) executed `python.exe` /
`powershell.exe` / `cmd` directly - every fire = a visible console. Worst
offender MagFreeLaneFleet (every 30 min). 6 tasks were already hidden
(pythonw/wscript precedents: MagQCaptionVerifyDaily, MagSecretScanWeekly,
mag-docker-watchdog, vast-bargain-loop, OpenClaw Gateway, cua-driver-serve).

## Cure (landed same sitting)
- `scripts/run_hidden.vbs` - generic hidden launcher: `wscript //B //Nologo
  run_hidden.vbs <exe> [args...]`, window style 0, WAITS (MultipleInstances
  policy + Last Run Result semantics survive), exit code passes through.
- `scripts/tasks_make_hidden.ps1` - idempotent migration; 24 tasks wrapped
  (incl. both Estate Gopher actions; Spine Index's embedded-quote fields
  stripped; the two retired 8765 boot tasks rebuilt cmd-chain -> WorkingDirectory).
  WorkingDirectory preserved, repo root where tasks never set one (Task
  Scheduler defaults CWD to System32). This script is the re-apply tool: run
  it after any manual `schtasks /Create` re-heads a task.
- All 13 `scripts/register_*.ps1` patched to emit the hidden wrapper
  (register_leave_task.ps1 keeps its zero-embedded-quotes PS 5.1 /TR law - no
  path contains spaces). PowerShell parser: all 13 parse clean.

## Proof (bytes, not vibes)
- Estate KeyAudit fired hidden 19:49 ET: task completed, LastTaskResult 0x1 -
  byte-identical to a direct run (orphan GROK_API_KEY finding = genuine exit,
  not launch failure). Exit-code passthrough proven.
- MagFreeLaneFleet fired hidden 19:58:58 ET: 0x0, cycle banked 10 findings
  (log 2026-10-05T23:58:54Z). Powershell-shape wrapper proven.
- 19:43 fleet "failure" 0x800710E0 = my Set-ScheduledTask racing the 19:43:43
  trigger mid-edit - one missed cycle, recovered by the 19:58 manual fire.

## Post-reboot estate state (same pass)
- Ollama UP; free-lane fleet cycling (5/7 providers healthy); docker stack UP
  via watchdog (mag-sovereign/mcp/worker/redis healthy; API door 8000 answers,
  8001 auth-gated); warm boot written (chain tip index=11355).
- Ouroboros R4: sibling seat already resumed it (dwfrun-c1ff3563 from
  dwfrun-45927560, running) - untouched here.
- Day-5 OLM mine (dwfrun-daecd119, 156.6M tok): stopped-interrupted by the
  reboot, no successor -> RESUMED from this seat 19:57 ET (operator's standing
  wide-burn order + pending doctrine-fold todo).

## Operator item EXECUTED (~20:10 ET same evening)
- 8765 UNPARKED: operator ran the admin portproxy delete ("run" = do my
  half), compose publish uncommented, `docker compose up -d mag` recreated the
  container. Byte proof: mag-sovereign healthy with
  `127.0.0.1:8765->8765/tcp` published, `curl 127.0.0.1:8765 -> 200`,
  8000/8001/9000 republished clean. Docker-first bind holds, per the 41h
  coexistence law in docker-compose.yml:41-56.
- 3 sibling git stashes still sitting (known incident, dawn list) - untouched.
