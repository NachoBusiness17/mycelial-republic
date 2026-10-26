# Register Windows Task Scheduler job for the daily estate metabolism gap
# sentinel (tools/gap_sentinel.py, Mickey17 W3 telemetry lane, 2026-09-29) at
# 08:15, between MagImproveDaily 08:00 and MagCensusPatrolDaily 08:30 so the
# daily lanes do not overlap (08:00 / 08:15 / 08:30 / 09:00 / 09:45).
#   powershell -ExecutionPolicy Bypass -File scripts\register_gap_sentinel_task.ps1
# Wrapper form from birth (no inline schtasks -Command): Windows PowerShell
# 5.1 mangles embedded double quotes in /TR — the sibling canary register
# script's inline first attempt died with schtasks exit 5 (2026-09-29). This
# copies the byte-proven census pattern (register_census_patrol_task.ps1).
# Operator response on exit 1 (GROWTH/SILENCE flags): memory/attention.md
# carries the gap-sentinel block naming the project/sensor and the bar it
# broke; confirm against bytes before acting. Exit 2 = the sentinel could
# not verify: treat as an incident, inspect logs/gap_sentinel.log.
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
$Script = Join-Path $PSScriptRoot "gap_sentinel_daily.ps1"
$Log = Join-Path $Root "logs\gap_sentinel.log"
$TaskName = "MagGapSentinelDaily"

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
& schtasks.exe /Create /TN $TaskName /TR $Tr /SC DAILY /ST 08:15 /RL LIMITED /F
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARN: schtasks create failed (exit $LASTEXITCODE)."
    Write-Host "Create manually:"
    Write-Host "  Program: powershell.exe"
    Write-Host "  Args:    -NoProfile -ExecutionPolicy Bypass -File `"$Script`""
    Write-Host "  Start in: $Root"
    Write-Host "  Trigger: Daily 08:15"
    exit $LASTEXITCODE
}

Write-Host "OK: task '$TaskName' -> daily 08:15"
Write-Host "    script: $Script"
Write-Host "    log:    $Log"
Write-Host "Test now:  schtasks /Run /TN $TaskName"
Write-Host "Or:        powershell -ExecutionPolicy Bypass -File `"$Script`""
