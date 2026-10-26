# Estate daily meters - full ratchet check + boot-freshness check.
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

# CHAIN_FIXES_APPLIED_20261019: sealed restore prefix (historical record; non-failing)
& $Py tools\chain_prefix_seal_check.py 2>&1 | Tee-Object -FilePath $Log -Append
$prefix = $LASTEXITCODE
if ($null -eq $prefix) { $prefix = 0 }

# CHAIN_HARDEN_ITER2_20261020: rolling no-rewrite (red only on NEW rewrite)
& $Py tools\chain_no_rewrite_check.py 2>&1 | Tee-Object -FilePath $Log -Append
$norewrite = $LASTEXITCODE
if ($null -eq $norewrite) { $norewrite = 0 }

# CHAIN_HARDEN_ITER2_20261020: lab /proc + rewrite-flag config scan
& $Py tools\chain_harden_patrol.py 2>&1 | Tee-Object -FilePath $Log -Append
$harden = $LASTEXITCODE
if ($null -eq $harden) { $harden = 0 }

Write-Log "END seal=$seal freshness=$fresh ratchet=$ratchet prefix=$prefix norewrite=$norewrite harden=$harden"
# prefix historical is informational; fail on norewrite/harden/seal/fresh/ratchet
if ($seal -ne 0 -or $fresh -ne 0 -or $ratchet -ne 0 -or $norewrite -ne 0 -or $harden -ne 0) { exit 1 }
exit 0
