# Register Windows Task Scheduler job for the headless Hermes 24/7 burn
# (scripts/hermes_burn_247.ps1 -> tools/hermes_burn.py queue/hermes_247,
# operator order 2026-10-06). Hourly cadence so the funded meters drip
# around the clock; the carrier's atomic claims make overlapping fires
# safe, and the queue is consumed not drained (empty queue = cheap no-op).
#   powershell -ExecutionPolicy Bypass -File scripts\register_hermes_burn_task.ps1
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
$Script = Join-Path $PSScriptRoot "hermes_burn_247.ps1"
$TaskName = "MagHermesBurn247"

if (-not (Test-Path $Script)) {
    Write-Error "Missing $Script"
    exit 1
}

# Delete if exists (ignore missing)
$prev = $ErrorActionPreference
$ErrorActionPreference = "SilentlyContinue"
schtasks /Delete /TN $TaskName /F 2>$null | Out-Null
$ErrorActionPreference = $prev

# Hidden launcher (2026-10-05 cure): bare task actions pop a console window
# on the operator's desktop every fire; run_hidden.vbs runs them windowless.
$Hidden = Join-Path $PSScriptRoot "run_hidden.vbs"
$Tr = "wscript.exe //B //Nologo `"$Hidden`" powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$Script`""
& schtasks.exe /Create /TN $TaskName /TR $Tr /SC HOURLY /ST 00:00 /RL LIMITED /F
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARN: schtasks create failed (exit $LASTEXITCODE)."
    Write-Host "Create manually:"
    Write-Host "  Program: powershell.exe"
    Write-Host "  Args:    -NoProfile -ExecutionPolicy Bypass -File `"$Script`""
    Write-Host "  Start in: $Root"
    Write-Host "  Trigger: Hourly"
    exit $LASTEXITCODE
}

Write-Host "OK: task '$TaskName' -> hourly (24/7)"
Write-Host "    script: $Script"
Write-Host "    queue:  $Root\queue\hermes_247"
Write-Host "    log:    $Root\logs\hermes_burn_247.log"
Write-Host "Test now:  schtasks /Run /TN $TaskName"
Write-Host "Or:        powershell -File `"$Script`""
