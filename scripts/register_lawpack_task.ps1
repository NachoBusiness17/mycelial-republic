# Register Windows Task Scheduler job for the daily law-pack recompile +
# staleness audit (tools/thought_quantizer.py, ouroboros R4-L1, 2026-10-05) at
# 09:30, after MagImproveDaily 08:00, MagCensusPatrolDaily 08:30 and
# MagFtsIndexDaily 09:00 so the four daily lanes do not overlap.
#   powershell -ExecutionPolicy Bypass -File scripts\register_lawpack_task.ps1
# Git Bash: prefix MSYS_NO_PATHCONV=1 when passing /TN style args by hand;
# this script's own schtasks call runs under PowerShell, where no path
# mangling applies.
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
$Script = Join-Path $PSScriptRoot "lawpack_daily.ps1"
$TaskName = "MagLawPackDaily"

if (-not (Test-Path $Script)) {
    Write-Error "Missing $Script"
    exit 1
}

# Delete if exists (ignore missing)
$prev = $ErrorActionPreference
$ErrorActionPreference = "SilentlyContinue"
schtasks /Delete /TN $TaskName /F 2>$null | Out-Null
$ErrorActionPreference = $prev

# Hidden launcher: bare powershell.exe task actions pop a console on the
# operator's desktop every fire; run_hidden.vbs runs them windowless.
$Hidden = Join-Path $PSScriptRoot "run_hidden.vbs"
$Tr = "wscript.exe //B //Nologo `"$Hidden`" powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$Script`""
& schtasks.exe /Create /TN $TaskName /TR $Tr /SC DAILY /ST 09:30 /RL LIMITED /F
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARN: schtasks create failed (exit $LASTEXITCODE)."
    Write-Host "Create manually (Git Bash: prefix MSYS_NO_PATHCONV=1):"
    Write-Host "  Program: powershell.exe"
    Write-Host "  Args:    -NoProfile -ExecutionPolicy Bypass -File `"$Script`""
    Write-Host "  Start in: $Root"
    Write-Host "  Trigger: Daily 09:30"
    exit $LASTEXITCODE
}

Write-Host "OK: task '$TaskName' -> daily 09:30"
Write-Host "    script: $Script"
Write-Host "    log:    $Root\logs\lawpack.log"
Write-Host "Test now:  MSYS_NO_PATHCONV=1 schtasks /Run /TN $TaskName"
Write-Host "Or:        powershell -ExecutionPolicy Bypass -File `"$Script`""
