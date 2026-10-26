# Register Windows Task Scheduler job for the nightly vision batch
# (THE 50 W9 T44). Daily 02:30, limited run level, no admin needed.
#   powershell -ExecutionPolicy Bypass -File scripts\register_vision_nightly.ps1
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
$Script = Join-Path $PSScriptRoot "vision_nightly.ps1"
$TaskName = "MagVisionNightly"

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
& schtasks.exe /Create /TN $TaskName /TR $Tr /SC DAILY /ST 02:30 /RL LIMITED /F
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARN: schtasks create failed (exit $LASTEXITCODE)."
    Write-Host "Create manually:"
    Write-Host "  Program: powershell.exe"
    Write-Host "  Args:    -NoProfile -ExecutionPolicy Bypass -File `"$Script`""
    Write-Host "  Start in: $Root"
    Write-Host "  Trigger: Daily 02:30"
    exit $LASTEXITCODE
}

Write-Host "OK: task '$TaskName' -> daily 02:30"
Write-Host "    script: $Script"
Write-Host "    log:    $Root\logs\vision_nightly.log"
Write-Host "    receipts: watch\inbox\mrpool_export\vision_nightly_receipts.jsonl"
Write-Host "Test now:  schtasks /Run /TN $TaskName"
Write-Host "Disable:   schtasks /Change /TN $TaskName /DISABLE"
Write-Host "Dry-run:   .\.venv\Scripts\python.exe scripts\vision_nightly.py --dry-run"
Write-Host "Live probe: .\.venv\Scripts\python.exe scripts\vision_nightly.py --smoke"
