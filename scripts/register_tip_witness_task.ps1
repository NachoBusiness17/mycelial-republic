# Register Windows Task Scheduler job for the daily verkle tip witness
# (tools/tip_witness.py --publish --go, W3 2026-09-30) at 09:30, riding the
# daily chain AFTER MagImproveDaily 08:00, MagCensusPatrolDaily 08:30 and
# MagFtsIndexDaily 09:00. Registering this task is the operator's --go
# consent: the ratchet then advances the witness daily and refuses any
# backward/sideways move.
#   powershell -ExecutionPolicy Bypass -File scripts\register_tip_witness_task.ps1
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
$Script = Join-Path $PSScriptRoot "tip_witness_daily.ps1"
$TaskName = "MagTipWitnessDaily"

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
& schtasks.exe /Create /TN $TaskName /TR $Tr /SC DAILY /ST 09:30 /RL LIMITED /F
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARN: schtasks create failed (exit $LASTEXITCODE)."
    Write-Host "Create manually:"
    Write-Host "  Program: powershell.exe"
    Write-Host "  Args:    -NoProfile -ExecutionPolicy Bypass -File `"$Script`""
    Write-Host "  Start in: $Root"
    Write-Host "  Trigger: Daily 09:30"
    exit $LASTEXITCODE
}

Write-Host "OK: task '$TaskName' -> daily 09:30 (after FTS index 09:00)"
Write-Host "    script: $Script"
Write-Host "    log:    $Root\logs\tip_witness.log"
Write-Host "    NOTE: first run will fail exit 2 (SCOPE) until the PAT has"
Write-Host "    gist write (Account permissions -> Gists: Read and write)."
Write-Host "Test now:  schtasks /Run /TN $TaskName"
Write-Host "Or:        powershell -File `"$Script`""
