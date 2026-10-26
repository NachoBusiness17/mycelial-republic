# Register the Windows Task Scheduler job for the cadence organs daily run
# (scripts/cadence_organs_daily.ps1: the five meters organs + the room_state
# lightmap render) at 09:30 daily, after MagFtsIndexDaily 09:00 so the daily
# lanes do not overlap, exactly as proposed in
#   watch/inbox/CADENCE_DOOR_SPEC_20261010_locksmith.md
#   watch/inbox/ROOM_STATE_DOOR_SPEC_20261012_locksmith.md
# Pile rows: PROMISE_PILE_LEDGER_20261013_locksmith.md rows 3, 4, 5
# (ninth census at zero: 35 Mag tasks, 35 actions, 0 organ names, 10-23).
#
# Consumer: this script creates the task that consumes cadence_organs_daily.ps1.
# Verifier: after registration, Get-ScheduledTask MagCadenceOrgansDaily shows
#   the six organ names in its action string; the next locksmith census
#   (rows 3/4/5) reads 1 instead of 0. Test now: schtasks /Run /TN MagCadenceOrgansDaily.
#
# Law-13 design-cite: inherited from the two spec docs (the citation of
# record): docker-not-desktop exemption (existing host-process task fleet),
# headless-only compliant (run_hidden.vbs windowless launcher, 2026-10-05
# pattern), one-supervisor compliant (one task, no daemon).
#
# OPERATOR GATE: this script registers a host-side scheduled task. It is
# NEVER run by a seat; the operator runs it:
#   powershell -ExecutionPolicy Bypass -File scripts\register_cadence_organs_task.ps1
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
$Script = Join-Path $PSScriptRoot "cadence_organs_daily.ps1"
$TaskName = "MagCadenceOrgansDaily"

if (-not (Test-Path $Script)) {
    Write-Error "Missing $Script"
    exit 1
}

# Delete if exists (ignore missing)
$prev = $ErrorActionPreference
$ErrorActionPreference = "SilentlyContinue"
schtasks /Delete /TN $TaskName /F 2>$null | Out-Null
$ErrorActionPreference = $prev

# Hidden launcher (2026-10-05 pattern): bare powershell.exe task actions pop
# a console on the operator's desktop every fire; run_hidden.vbs runs them
# windowless. Same shape as MagFtsIndexDaily / MagCensusPatrolDaily.
$Hidden = Join-Path $PSScriptRoot "run_hidden.vbs"
$Tr = "wscript.exe //B //Nologo `"$Hidden`" powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$Script`""
& schtasks.exe /Create /TN $TaskName /TR $Tr /SC DAILY /ST 09:30 /RL LIMITED /F
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARN: schtasks create failed (exit $LASTEXITCODE)."
    Write-Host "Create manually:"
    Write-Host "  Program: powershell.exe"
    Write-Host "  Args:    -NoProfile -ExecutionPolicy Bypass -File `"$Script`""
    Write-Host "  Start in: $Root"
    Write-Host "  Trigger: Daily 09:30"
    exit $LASTEXITCODE
}

Write-Host "OK: task '$TaskName' -> daily 09:30"
Write-Host "    script: $Script"
Write-Host "    log:    $Root\logs\cadence_organs.log"
Write-Host "Test now:  schtasks /Run /TN $TaskName"
Write-Host "Or:        powershell -File `"$Script`""
