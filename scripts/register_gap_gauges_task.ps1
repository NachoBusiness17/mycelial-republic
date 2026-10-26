# Register Windows Task Scheduler job for the daily three-gap panel
# (tools/gap_gauges.py + its census refresh, lamplighter mate, 2026-10-09) at
# 08:20, between MagGapSentinelDaily 08:15 (writes today's snapshot this panel
# diffs) and MagCensusPatrolDaily 08:30, so the daily lanes do not overlap
# (08:00 / 08:15 / 08:20 / 08:30 / 09:00 / 09:45).
#   powershell -ExecutionPolicy Bypass -File scripts\register_gap_gauges_task.ps1
# Wrapper form from birth (no inline schtasks -Command): Windows PowerShell
# 5.1 mangles embedded double quotes in /TR - the sibling canary register
# script's inline first attempt died with schtasks exit 5 (2026-09-29). This
# copies the byte-proven register_gap_sentinel_task.ps1 pattern including the
# run_hidden.vbs launcher (bare powershell.exe task actions pop a console on
# the operator's desktop every fire, fixed 2026-10-05).
# Operator response on exit 1 (a gauge flagged): logs/gap_gauges.log and
# logs/gap_gauges/run.log carry the flags with their bytes; confirm against
# bytes before acting. Exit 2 = cannot verify: treat as an incident, inspect
# logs/gap_gauges.log.
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
$Script = Join-Path $PSScriptRoot "gap_gauges_daily.ps1"
$Log = Join-Path $Root "logs\gap_gauges.log"
$TaskName = "MagGapGaugesDaily"

if (-not (Test-Path $Script)) { Write-Error "Missing $Script"; exit 1 }
if (-not (Test-Path (Join-Path $Root "logs"))) {
    New-Item -ItemType Directory -Path (Join-Path $Root "logs") | Out-Null
}

# Delete if exists (ignore missing)
$prev = $ErrorActionPreference
$ErrorActionPreference = "SilentlyContinue"
schtasks /Delete /TN $TaskName /F 2>$null | Out-Null
$ErrorActionPreference = $prev

# Hidden launcher (2026-10-05): bare powershell.exe task actions pop a console
# on the operator's desktop every fire; run_hidden.vbs runs them windowless.
$Hidden = Join-Path $PSScriptRoot "run_hidden.vbs"
$Tr = "wscript.exe //B //Nologo `"$Hidden`" powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$Script`""
& schtasks.exe /Create /TN $TaskName /TR $Tr /SC DAILY /ST 08:20 /RL LIMITED /F
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARN: schtasks create failed (exit $LASTEXITCODE)."
    Write-Host "Create manually:"
    Write-Host "  Program: powershell.exe"
    Write-Host "  Args:    -NoProfile -ExecutionPolicy Bypass -File `"$Script`""
    Write-Host "  Start in: $Root"
    Write-Host "  Trigger: Daily 08:20"
    exit $LASTEXITCODE
}

Write-Host "OK: task '$TaskName' -> daily 08:20"
Write-Host "    script: $Script"
Write-Host "    log:    $Log"
Write-Host "Test now:  schtasks /Run /TN $TaskName"
Write-Host "Or:        powershell -ExecutionPolicy Bypass -File `"$Script`""
