# Register Windows Task Scheduler job for the daily X reply radar
# (.venv python -m mag.x_reply_radar run, Z16, 2026-09-30) at 08:00.
# 08:00 is the documented original time (watch/BUILD_REPORT_20260907_NIGHT.md
# "X radar 08:00"; empirical raw mtimes 08:05-08:08 = 08:00 starts). The slot
# already holds MagImproveDaily + MagLeaveProtocolDaily (proven 2-task shape).
#   powershell -ExecutionPolicy Bypass -File scripts\register_x_radar_task.ps1
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
$Script = Join-Path $PSScriptRoot "x_radar_daily.ps1"
$TaskName = "MagXRadarDaily"

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
& schtasks.exe /Create /TN $TaskName /TR $Tr /SC DAILY /ST 08:00 /RL LIMITED /F
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARN: schtasks create failed (exit $LASTEXITCODE)."
    Write-Host "Create manually:"
    Write-Host "  Program: powershell.exe"
    Write-Host "  Args:    -NoProfile -ExecutionPolicy Bypass -File `"$Script`""
    Write-Host "  Start in: $Root"
    Write-Host "  Trigger: Daily 08:00"
    exit $LASTEXITCODE
}

Write-Host "OK: task '$TaskName' -> daily 08:00"
Write-Host "    script: $Script"
Write-Host "    log:    $Root\logs\x_radar.log"
Write-Host "Test now:  schtasks /Run /TN $TaskName"
Write-Host "Or:        powershell -File `"$Script`""
