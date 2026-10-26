# Register Windows Task Scheduler job for endpoint_news (daily 06:30 local).
#   powershell -ExecutionPolicy Bypass -File scripts\register_endpoint_news_task.ps1
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
$Script = Join-Path $PSScriptRoot "endpoint_news_daily.ps1"
$TaskName = "MagEndpointNewsDaily"

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
& schtasks.exe /Create /TN $TaskName /TR $Tr /SC DAILY /ST 06:30 /RL LIMITED /F
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARN: schtasks create failed (exit $LASTEXITCODE)."
    Write-Host "Create manually:"
    Write-Host "  Program: powershell.exe"
    Write-Host "  Args:    -NoProfile -ExecutionPolicy Bypass -File `"$Script`""
    Write-Host "  Start in: $Root"
    Write-Host "  Trigger: Daily 06:30"
    exit $LASTEXITCODE
}

Write-Host "OK: task '$TaskName' -> daily 06:30"
Write-Host "    script: $Script"
Write-Host "    log:    $Root\logs\endpoint_news.log"
Write-Host "Test now:  schtasks /Run /TN $TaskName"
Write-Host "Or:        powershell -File `"$Script`""
