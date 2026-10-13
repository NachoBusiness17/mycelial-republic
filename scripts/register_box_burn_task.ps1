# Register Windows Task Scheduler job for the nightly box-burn load curve
# (scripts/box_burn_nightly.ps1 -> tools/box_burn_watch.py, queue/todo.md Stone 7
# sub-item 3 wiring, landed 2026-10-07 m2-todo-truths lane). Daily 22:00 fire;
# the carrier self-stops at 07:00 (family-box law), so the task runs the
# 22:00-07:00 window and then exits on its own.
#   powershell -ExecutionPolicy Bypass -File scripts\register_box_burn_task.ps1
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
$Script = Join-Path $PSScriptRoot "box_burn_nightly.ps1"
$TaskName = "MagBoxBurnNightly"

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
& schtasks.exe /Create /TN $TaskName /TR $Tr /SC DAILY /ST 22:00 /RL LIMITED /F
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARN: schtasks create failed (exit $LASTEXITCODE)."
    Write-Host "Create manually:"
    Write-Host "  Program: powershell.exe"
    Write-Host "  Args:    -NoProfile -ExecutionPolicy Bypass -File `"$Script`""
    Write-Host "  Start in: $Root"
    Write-Host "  Trigger: Daily 22:00"
    exit $LASTEXITCODE
}

Write-Host "OK: task '$TaskName' -> daily 22:00 (self-stops 07:00)"
Write-Host "    script: $Script"
Write-Host "    ledger: $Root\state\fuel\box_burn_watch.jsonl"
Write-Host "    log:    $Root\logs\box_burn_nightly.log"
Write-Host "Test now:  schtasks /Run /TN $TaskName"
Write-Host "Or:        powershell -File `"$Script`""
