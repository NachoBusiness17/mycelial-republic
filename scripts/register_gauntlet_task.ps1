# Register Windows Task Scheduler job for the cheap-seat gauntlet
# (scripts/gauntlet_free_30.ps1: gauntlet_grade + gauntlet_feed around the
# MagFreeLaneFleet drain, operator order 2026-10-06). Every 30 minutes at
# :15/:45, offset from the fleet's :03/:33 fires so each grading pass sees
# the fresh landings. LONGRUNNER POLICY R2 (2026-10-07): the clock stays
# host-side, the grading work runs inside the burners compose cage
# (docker compose run --rm --entrypoint python burners -m tools.gauntlet_*).
#   powershell -ExecutionPolicy Bypass -File scripts\register_gauntlet_task.ps1
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
$Script = Join-Path $PSScriptRoot "gauntlet_free_30.ps1"
$TaskName = "MagGauntletFree30"

if (-not (Test-Path $Script)) {
    Write-Error "Missing $Script"
    exit 1
}

# Delete if exists (ignore missing)
$prev = $ErrorActionPreference
$ErrorActionPreference = "SilentlyContinue"
schtasks /Delete /TN $TaskName /F 2>$null | Out-Null
$ErrorActionPreference = $prev

# Hidden launcher (2026-10-05 cure): windowless via run_hidden.vbs.
$Hidden = Join-Path $PSScriptRoot "run_hidden.vbs"
$Tr = "wscript.exe //B //Nologo `"$Hidden`" powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$Script`""
& schtasks.exe /Create /TN $TaskName /TR $Tr /SC MINUTE /MO 30 /ST 00:15 /RL LIMITED /F
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARN: schtasks create failed (exit $LASTEXITCODE)."
    Write-Host "Create manually:"
    Write-Host "  Program: powershell.exe"
    Write-Host "  Args:    -NoProfile -ExecutionPolicy Bypass -File `"$Script`""
    Write-Host "  Start in: $Root"
    Write-Host "  Trigger: Every 30 minutes"
    exit $LASTEXITCODE
}

Write-Host "OK: task '$TaskName' -> every 30 min at :15/:45 (offset from fleet :03/:33)"
Write-Host "    script: $Script"
Write-Host "    cage:   docker compose run --rm -T --interactive=false --entrypoint python burners -m tools.gauntlet_grade / -m tools.gauntlet_feed"
Write-Host "    queue:  $Root\watch\inbox\free_lane_queue (drained by MagFreeLaneFleet)"
Write-Host "    log:    $Root\logs\gauntlet_free.log"
Write-Host "Test now:  schtasks /Run /TN $TaskName"
