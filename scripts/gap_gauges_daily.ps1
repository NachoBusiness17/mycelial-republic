# Mag daily three-gap panel wrapper: tools/gap_gauges.py (lamplighter mate,
# 2026-10-06; wired-ready 2026-10-09 cycle 2). Two passes in one lane:
#   1. tools/orphan_census.py  - refresh the rot gauge's input
#      (watch/inbox/ORPHAN_CENSUS.json; the 2026-10-09 cycle found it 3.0 days
#      stale by hand-run only: an unrefreshed input means the rot delta never
#      moves and the gauge reads a frozen world).
#   2. tools/gap_gauges.py     - the grow/rot/silence panel, appends
#      logs/gap_gauges/history.jsonl + run.log (its own sanctioned writers).
# The panel never writes memory/attention.md (alerts stay in the sentinel's
# lane); this wrapper only stamps the log and passes the gauge exit code
# through (0 clean / 1 flagged / 2 cannot verify).
# Register (OPERATOR-GATED, host-side task registration; this script does not
# self-register): powershell -ExecutionPolicy Bypass -File scripts\register_gap_gauges_task.ps1
# Run now:  powershell -ExecutionPolicy Bypass -File scripts\gap_gauges_daily.ps1
#
# Wrapper form (not an inline schtasks -Command) is load-bearing: Windows
# PowerShell 5.1 mangles embedded double quotes when passing /TR to
# schtasks.exe (the gap sentinel register script's first inline attempt died
# with schtasks exit 5, 2026-09-29). Copies the byte-proven
# scripts\gap_sentinel_daily.ps1 form including the Add-Content utf8 log
# (PS 5.1 Tee writes UTF-16 and mojibakes a UTF-8 log, B2-246).
#
# OPERATOR RESPONSE (MagGapGaugesDaily Last Result != 0, or no START stamp for
# today in logs/gap_gauges.log): exit 1 = a gauge flagged (GROW/SHRINK over
# bar, ROT with consumption flat, SENSOR-DARK/MISSING on the 5-sensor
# watchlist, CENSUS-DARK) - the flags print to this log and land in
# logs/gap_gauges/run.log; confirm against bytes before acting. Exit 2 = the
# census or a history row was unparsable (cannot verify): an incident, inspect
# logs/gap_gauges.log, never guess. A dark log with a Ready task is the
# instruments-built-not-run disease: schtasks /Query /TN MagGapGaugesDaily,
# re-register or run by hand.
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
Set-Location $Root

$Py = Join-Path $Root ".venv\Scripts\python.exe"
$LogDir = Join-Path $Root "logs"
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir | Out-Null }
$Log = Join-Path $LogDir "gap_gauges.log"
$Stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

function Write-Log([string]$Msg) {
    $line = "[$Stamp] $Msg"
    # Add-Content utf8, not Tee-Object: PS 5.1 Tee writes UTF-16 with no
    # -Encoding flag and mojibakes a UTF-8 log (B2-246 live-run defect).
    Add-Content -Path $Log -Value $line -Encoding utf8
    Write-Host $line
}

if (-not (Test-Path $Py)) {
    Write-Log "FAIL: missing venv python at $Py (cannot verify, exit 2)"
    exit 2
}

Write-Log "START gap gauges cwd=$Root"

# Pass 1: refresh the rot input (fail-closed: a census that cannot be rebuilt
# means pass 2 would delta against a stale world; exit through).
& $Py tools\orphan_census.py 2>&1 | ForEach-Object {
    $line = "$_".TrimEnd()
    Add-Content -Path $Log -Value $line -Encoding utf8
    Write-Host $line
}
$censusCode = $LASTEXITCODE
if ($null -eq $censusCode) { $censusCode = 2 }
if ($censusCode -ne 0) {
    Write-Log "END exit=$censusCode (orphan_census failed; gauges not run)"
    exit $censusCode
}

# Pass 2: the panel.
& $Py tools\gap_gauges.py 2>&1 | ForEach-Object {
    $line = "$_".TrimEnd()
    Add-Content -Path $Log -Value $line -Encoding utf8
    Write-Host $line
}
$code = $LASTEXITCODE
if ($null -eq $code) { $code = 2 }

Write-Log "END exit=$code"
exit $code
