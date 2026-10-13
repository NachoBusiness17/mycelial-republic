# Mag daily estate smith chart: python -m tools.estate_smith (lane B3, 2026-10-08).
# Spec: watch/inbox/smith_chart_estate_20261009/SPEC.md; v1 instrument home:
# watch/inbox/smith_chart_estate_20260109/estate_smith.py. Daily 09:05, after
# the disk smith 08:50 (one disk-touching process at a time, preserved by
# stagger; this tool itself never walks the disk - psutil + bounded tails).
# Register: powershell -ExecutionPolicy Bypass -File scripts\register_estate_smith_task.ps1
# Run now:  powershell -ExecutionPolicy Bypass -File scripts\estate_smith_daily.ps1
#
# The tool is the single writer: it appends its own row to
# logs/estate_smith.jsonl and its own alert lines to memory/attention.md, so
# this script never writes those surfaces - it only logs and forwards exit.
#
# OPERATOR RESPONSE (MagEstateSmithDaily Last Result != 0, or this log shows
# an ALERT line, or an alert block landed in memory/attention.md):
#   exit 1: a real threshold breach (ram avail < 8GB, disk free < 15GB, or
#     pagefile.sys file > 40GB per the last disk_smith row). The tool already
#     appended the alert lines to memory/attention.md; read the named gauge
#     and apply the relief note in the alert text. Expected to fire while the
#     founding pagefile balloon stands (63.95GB on 2026-10-09).
#   exit 2: the venv is missing - the surface is dark; fix the venv
#     (scripts\ensure_venv.ps1), no chart rows were lost (nothing ran).
#   No START stamp for today in logs/estate_smith.log: the surface is dark
#     (machine off, logged out, task deregistered). Respond:
#     schtasks /Query /TN MagEstateSmithDaily, re-register, run this by hand.
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
Set-Location $Root

$Py = Join-Path $Root ".venv\Scripts\python.exe"
$LogDir = Join-Path $Root "logs"
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir | Out-Null }
$Log = Join-Path $LogDir "estate_smith.log"
$Stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

function Write-Log([string]$Msg) {
    $line = "[$Stamp] $Msg"
    Add-Content -Path $Log -Value $line -Encoding utf8
    Write-Host $line
}

if (-not (Test-Path $Py)) {
    Write-Log "FAIL: missing venv python at $Py (cannot run, exit 2)"
    exit 2
}

Write-Log "START estate smith chart cwd=$Root"
# No Tee-Object: in Windows PowerShell 5.1 it writes UTF-16 with no -Encoding
# flag, which mojibake'd the census patrol log lines (B2-246 live-run defect);
# per-line Add-Content keeps this log UTF-8.
& $Py -m tools.estate_smith 2>&1 | ForEach-Object {
    $line = "$_".TrimEnd()
    Add-Content -Path $Log -Value $line -Encoding utf8
    Write-Host $line
}
$code = $LASTEXITCODE
if ($null -eq $code) { $code = 2 }

if ($code -eq 1) {
    Write-Log "ALERT: threshold breach fired; the tool appended its own memory/attention.md lines"
} elseif ($code -ne 0) {
    Write-Log "FAIL: estate_smith exit $code (see tool lines above)"
}
Write-Log "END exit=$code"
exit $code
