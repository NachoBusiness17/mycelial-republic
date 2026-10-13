# Register Windows Task Scheduler job MagLeaveProtocolDaily: the mates leave
# protocol (tools/leave_dispatcher.py, X12 static-runner unblock, 2026-09-29/30)
# at 08:00 daily, per the register note sanction (watch/inbox/mates_leave_protocol/
# REGISTER_NOTE.md: "schtasks MagLeaveProtocolDaily 08:00 ... When it lands: a
# register script rides with it").
#   powershell -ExecutionPolicy Bypass -File scripts\register_leave_task.ps1
#
# /TR FORM IS LOAD-BEARING (W3T defect, 2026-09-29): Windows PowerShell 5.1
# mangles embedded double quotes when passing /TR to schtasks.exe - the sibling
# canary register's inline quote form died with schtasks exit 5. The proven
# cure is a /TR with ZERO embedded quote pairs. Here the action is the venv
# python running the dispatcher by absolute path; the repo path contains no
# spaces, so the whole /TR is two bare absolute tokens and no inner quotes.
# No wrapper .ps1 is needed for logging: the dispatcher self-logs to
# logs/mates/dispatcher_<date>.log and the runner self-logs to
# logs/mates/runs/ + logs/mates/runner_<date>.log.
#
# 08:00 shares the slot with MagImproveDaily (both sanctioned at 08:00; the
# dispatcher's own work is file writes plus N light powershell spawns, and
# mate runs are opencode-bound, not CPU-bound). Lane order after this lands:
# 08:00 improve + leave protocol / 08:15 gap sentinel / 08:30 census patrol /
# 09:00 FTS index / 09:45 gate canary.
#
# OPERATOR RESPONSE (Last Result != 0, or no stamp for today in
# logs/mates/dispatcher_<date>.log): exit 1 = one or more runner invocations
# returned nonzero - read logs/mates/runner_<date>.log and the failed
# run_<date>_<nn>_<mate>.log under logs/mates/runs/, check the .claim
# sidecars in logs/mates/missions/, rerun by hand. Exit 2 = the dispatcher's
# argv guard tripped (repo moved under a frozen argv literal) or venv python
# missing - an incident, never guess. A dark log with a Ready task is the
# instruments-built-not-run disease: schtasks /Query /TN
# MagLeaveProtocolDaily, re-register or run by hand.
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
$Py = Join-Path $Root ".venv\Scripts\python.exe"
$Script = Join-Path $Root "tools\leave_dispatcher.py"
$TaskName = "MagLeaveProtocolDaily"

if (-not (Test-Path $Py)) { Write-Error "Missing venv python at $Py (run scripts\ensure_venv.ps1)"; exit 2 }
if (-not (Test-Path $Script)) { Write-Error "Missing $Script"; exit 2 }
if (-not (Test-Path (Join-Path $Root "scripts\run_mate.ps1"))) {
    Write-Error "Missing scripts\run_mate.ps1 (the dispatcher's constant argv points at it)"; exit 2
}
if (-not (Test-Path (Join-Path $Root "logs"))) {
    New-Item -ItemType Directory -Path (Join-Path $Root "logs") | Out-Null
}

# Delete if exists (ignore missing)
$prev = $ErrorActionPreference
$ErrorActionPreference = "SilentlyContinue"
schtasks /Delete /TN $TaskName /F 2>$null | Out-Null
$ErrorActionPreference = $prev

# Two bare absolute tokens, zero embedded quotes (see header: PS 5.1 mangles
# quoted /TR strings into schtasks exit 5 / -2147467259).
# Hidden launcher (2026-10-05), still zero embedded quotes (PS 5.1 /TR law above).
$Hidden = Join-Path $PSScriptRoot "run_hidden.vbs"
$Wsh = Join-Path $env:WINDIR "System32\wscript.exe"
$Tr = "$Wsh //B //Nologo $Hidden $Py $Script"
& schtasks.exe /Create /TN $TaskName /TR $Tr /SC DAILY /ST 08:00 /RL LIMITED /F
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARN: schtasks create failed (exit $LASTEXITCODE)."
    Write-Host "Create manually:"
    Write-Host "  Program: $Py"
    Write-Host "  Args:    $Script"
    Write-Host "  Trigger: Daily 08:00"
    exit $LASTEXITCODE
}

Write-Host "OK: task '$TaskName' -> daily 08:00"
Write-Host "    runs:    $Tr"
Write-Host "    logs:    logs\mates\dispatcher_<date>.log, logs\mates\runner_<date>.log"
Write-Host "Dry now:    .venv\Scripts\python.exe tools\leave_dispatcher.py --dry"
Write-Host "Live now:   .venv\Scripts\python.exe tools\leave_dispatcher.py"
Write-Host "Verify:     schtasks /Query /TN $TaskName /V /FO LIST"
