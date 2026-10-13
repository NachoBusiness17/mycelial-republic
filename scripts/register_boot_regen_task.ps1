# Register Windows Task Scheduler job for the daily boot-surface regen chain
# (mag.boot_regen: zknot + hermes_warm_boot + rib_boot, ouroboros R4b move 2,
# 2026-10-06) at 07:15, ahead of MagImproveDaily 08:00, MagCensusPatrolDaily
# 08:30, MagFtsIndexDaily 09:00 and MagLawPackDaily 09:30, so morning seats
# boot on organs regenerated before them and the daily lanes never overlap.
#   powershell -ExecutionPolicy Bypass -File scripts\register_boot_regen_task.ps1
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
$Script = Join-Path $PSScriptRoot "boot_regen_daily.ps1"
$TaskName = "MagBootRegenDaily"

if (-not (Test-Path $Script)) {
    Write-Error "Missing $Script"
    exit 1
}

# Delete if exists (ignore missing)
$prev = $ErrorActionPreference
$ErrorActionPreference = "SilentlyContinue"
schtasks /Delete /TN $TaskName /F 2>$null | Out-Null
$ErrorActionPreference = $prev

# Hidden launcher (2026-10-05 headed-windows cure): bare powershell.exe task
# actions pop a console on the operator's desktop every fire; run_hidden.vbs
# runs them windowless (same wrapper as MagFtsIndexDaily/MagLawPackDaily).
$Hidden = Join-Path $PSScriptRoot "run_hidden.vbs"
$Tr = "wscript.exe //B //Nologo `"$Hidden`" powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$Script`""
& schtasks.exe /Create /TN $TaskName /TR $Tr /SC DAILY /ST 07:15 /RL LIMITED /F
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARN: schtasks create failed (exit $LASTEXITCODE)."
    Write-Host "Create manually:"
    Write-Host "  Program: powershell.exe"
    Write-Host "  Args:    -NoProfile -ExecutionPolicy Bypass -File `"$Script`""
    Write-Host "  Start in: $Root"
    Write-Host "  Trigger: Daily 07:15"
    exit $LASTEXITCODE
}

Write-Host "OK: task '$TaskName' -> daily 07:15"
Write-Host "    script: $Script"
Write-Host "    log:    $Root\logs\boot_regen.log"
Write-Host "Test now:  schtasks /Run /TN $TaskName"
Write-Host "Or:        powershell -File `"$Script`""
