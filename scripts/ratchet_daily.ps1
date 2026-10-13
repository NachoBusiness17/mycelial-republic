# Estate daily meters — full ratchet check + boot-freshness check.
# Register: powershell -ExecutionPolicy Bypass -File scripts\register_ratchet_task.ps1
# Exit code is the meter: 0 = all pass, 1 = stale boot docs and/or unregistered debt.
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
Set-Location $Root

$Py = Join-Path $Root ".venv\Scripts\python.exe"
$LogDir = Join-Path $Root "logs"
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir | Out-Null }
$Log = Join-Path $LogDir "ratchet_daily.log"
$Stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

function Write-Log([string]$Msg) {
    $line = "[$Stamp] $Msg"
    Add-Content -Path $Log -Value $line -Encoding utf8
    Write-Host $line
}

if (-not (Test-Path $Py)) {
    Write-Log "FAIL: missing venv python at $Py"
    exit 1
}

Write-Log "START ratchet sweep cwd=$Root"

& $Py tools\config_seal.py verify 2>&1 | Tee-Object -FilePath $Log -Append
$seal = $LASTEXITCODE
if ($null -eq $seal) { $seal = 0 }

& $Py tools\freshness_check.py 2>&1 | Tee-Object -FilePath $Log -Append
$fresh = $LASTEXITCODE
if ($null -eq $fresh) { $fresh = 0 }

& $Py tools\violation_ratchet.py check 2>&1 | Tee-Object -FilePath $Log -Append
$ratchet = $LASTEXITCODE
if ($null -eq $ratchet) { $ratchet = 0 }

Write-Log "END seal=$seal freshness=$fresh ratchet=$ratchet"
if ($seal -ne 0 -or $fresh -ne 0 -or $ratchet -ne 0) { exit 1 }
exit 0
