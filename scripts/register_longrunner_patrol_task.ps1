# Register Windows Task Scheduler job for the longrunners-caged patrol
# (tools/longrunner_patrol.py, law carrier configs/longrunner_policy.json,
# operator order 2026-10-07: "what long running processes should be in
# containers by default so we lessig this"). Daily 08:45, between census
# patrol 08:30 and FTS 09:00 so the three daily lanes do not overlap.
#   powershell -ExecutionPolicy Bypass -File scripts\register_longrunner_patrol_task.ps1
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
$Script = Join-Path $PSScriptRoot "longrunner_patrol_daily.ps1"
$TaskName = "MagLongrunnerPatrolDaily"

if (-not (Test-Path $Script)) {
    Write-Error "Missing $Script"
    exit 1
}

$prev = $ErrorActionPreference
$ErrorActionPreference = "SilentlyContinue"
schtasks /Delete /TN $TaskName /F 2>$null | Out-Null
$ErrorActionPreference = $prev

# Hidden launcher (2026-10-05 cure): windowless via run_hidden.vbs.
$Hidden = Join-Path $PSScriptRoot "run_hidden.vbs"
$Tr = "wscript.exe //B //Nologo `"$Hidden`" powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$Script`""
& schtasks.exe /Create /TN $TaskName /TR $Tr /SC DAILY /ST 08:45 /RL LIMITED /F
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARN: schtasks create failed (exit $LASTEXITCODE)."
    exit $LASTEXITCODE
}

Write-Host "OK: task '$TaskName' -> daily 08:45"
Write-Host "    policy: $Root\configs\longrunner_policy.json"
Write-Host "    log:    $Root\logs\longrunner_patrol.log"
Write-Host "Test now:  schtasks /Run /TN $TaskName"
