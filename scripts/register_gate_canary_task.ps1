# Register Windows Task Scheduler job for the daily pre-push gate-liveness
# canary (tools/gate_canary.py, Mickey17 W2 return 7/24, 2026-09-29) at
# 09:45, after MagImproveDaily 08:00, MagCensusPatrolDaily 08:30 and
# MagFtsIndexDaily 09:00 so the four daily lanes do not overlap.
#   powershell -ExecutionPolicy Bypass -File scripts\register_gate_canary_task.ps1
# Operator response on a red run (exit 1): memory/attention.md carries a
# [gate-canary] DEAD/BLIND row naming the silent gate; investigate that gate
# before trusting any push. Exit 2 = the canary itself could not verify
# (worktree setup failed or real-tree taint): treat as an incident.
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
# FIX 2026-09-29 (W3 lane): the first registration attempt used an inline
# schtasks /TR of 'powershell.exe ... -Command "& ''py'' ''tool'' *>> ''log''"'
# and died with schtasks exit 5 "Invalid argument/option" — Windows
# PowerShell 5.1 mangles embedded double quotes when passing /TR to
# schtasks.exe, so that form can never register from any console. Aligned to
# the byte-proven census pattern (register_census_patrol_task.ps1 ->
# census_patrol_daily.ps1, registered 2026-09-26, runs clean daily): a -File
# wrapper with zero embedded quote pairs in /TR. Evidence: first-failure
# bytes in watch/inbox/mates_leave_protocol/W3T_TASK_REGISTRATION.md.
$Script = Join-Path $PSScriptRoot "gate_canary_daily.ps1"
$Log = Join-Path $Root "logs\gate_canary.log"
$TaskName = "MagGateCanaryDaily"

if (-not (Test-Path $Script)) { Write-Error "Missing $Script"; exit 1 }
if (-not (Test-Path (Join-Path $Root "logs"))) {
    New-Item -ItemType Directory -Path (Join-Path $Root "logs") | Out-Null
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
& schtasks.exe /Create /TN $TaskName /TR $Tr /SC DAILY /ST 09:45 /RL LIMITED /F
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARN: schtasks create failed (exit $LASTEXITCODE)."
    Write-Host "Create manually:"
    Write-Host "  Program: powershell.exe"
    Write-Host "  Args:    -NoProfile -ExecutionPolicy Bypass -File `"$Script`""
    Write-Host "  Start in: $Root"
    Write-Host "  Trigger: Daily 09:45"
    exit $LASTEXITCODE
}

Write-Host "OK: task '$TaskName' -> daily 09:45"
Write-Host "    script: $Script"
Write-Host "    log:    $Log"
Write-Host "Test now:  schtasks /Run /TN $TaskName"
Write-Host "Or:        powershell -ExecutionPolicy Bypass -File `"$Script`""
