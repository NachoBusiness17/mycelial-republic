# PA-S7mates-grok47 (grok-4.7 @ xai, turn 1, channel: content)

A dead mate is invisible until a human opens the logs. Nothing in this runner notices.

**Dead, from outside.** Claim is created empty and closed before `opencode` starts (`run_mate.ps1:108-114`). The only finish mark is appended after the pipeline returns (`:149-154`). A hard kill of the PowerShell host (OOM, task kill) leaves `mission_*.md.claim` with no `exit=` line, a `START` in `logs\mates\runner_<YYYYMMDD>.log` (`:136`) and no matching `END` (`:153`). `opencode` dying alone still reaches `END`, because the pipe is in-process (`:140-147`). There is no timeout (`:31-32`). The RAM-gate text in `mates.yaml:31-34` is never read by this script, so a ~20GB set can swap the box and take the watcher with it. **Notice latency today: unbounded.** `leave_dispatcher.py` is named at `:9-11` and is UNVERIFIED here. Receipts are mate-written, not runner-enforced.

**Diverging.** Stuck loop: process still alive, claim still empty, `RunLog` either frozen or growing forever. A chatty loop is indistinguishable from "ride to the edge" (`:31-32`). Key leak: the runner logs a count, not values (`:62-69`), but the pipe is unredacted (`:140-144`). `$env:ZAI_API_KEY` is in the child environment (`:64-66`). Any mate `echo` of that name lands in `run_*.log` and on the console. The never-dump law (`mates.yaml:24-26`) is prose only.

**Deliverable** (emitter; notice is a second process). Falsifier: `Stop-Process -Id <runner pid> -Force`; within 90s `hb_<mate>.beat` lacks an `exit=` prefix and its unix stamp is older than 90s. A chatty loop stays fresh. This does not catch that.

```powershell
$Hb = Join-Path $RunsDir ("hb_" + $MateId + ".beat")
$hb = Start-Job -Arg $Hb -ScriptBlock { param($p)
  while ($true) { [IO.File]::WriteAllText($p, [DateTimeOffset]::UtcNow.ToUnixTimeSeconds().ToString()); Start-Sleep 30 } }
# ... existing & $OpenCode pipeline stays here ...
Stop-Job $hb -EA SilentlyContinue; Remove-Job $hb -Force -EA SilentlyContinue
[IO.File]::WriteAllText($Hb, "exit=$code")
```

Insert the `Start-Job` immediately before `:140`. Insert the stop and `exit=` write immediately after `:147`. Do not auto-respawn: `mates.yaml:20` is resume-by-id. A beat file is not a receipt.
