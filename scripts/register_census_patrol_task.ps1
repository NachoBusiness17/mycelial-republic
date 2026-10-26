# Register Windows Task Scheduler job for the daily census deep check
# (tools/census_drift_patrol.py --collect, B2-246, 2026-09-26) at 08:30,
# after MagImproveDaily 08:00 so the two daily lanes do not overlap.
#   powershell -ExecutionPolicy Bypass -File scripts\register_census_patrol_task.ps1
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
$Script = Join-Path $PSScriptRoot "census_patrol_daily.ps1"
$TaskName = "MagCensusPatrolDaily"

if (-not (Test-Path $Script)) {
    Write-Error "Missing $Script"
    exit 1
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
& schtasks.exe /Create /TN $TaskName /TR $Tr /SC DAILY /ST 08:30 /RL LIMITED /F
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARN: schtasks create failed (exit $LASTEXITCODE)."
    Write-Host "Create manually:"
    Write-Host "  Program: powershell.exe"
    Write-Host "  Args:    -NoProfile -ExecutionPolicy Bypass -File `"$Script`""
    Write-Host "  Start in: $Root"
    Write-Host "  Trigger: Daily 08:30"
    exit $LASTEXITCODE
}

Write-Host "OK: task '$TaskName' → daily 08:30"
Write-Host "    script: $Script"
Write-Host "    log:    $Root\logs\census_patrol.log"
Write-Host "Test now:  schtasks /Run /TN $TaskName"
Write-Host "Or:        powershell -File `"$Script`""
