# Mag daily estate metabolism gap sentinel wrapper: tools/gap_sentinel.py
# (Mickey17 W3 telemetry lane, 2026-09-29). The tool self-alerts GROWTH /
# SILENCE flags to memory/attention.md (single-writer law), so this wrapper
# only stamps the log and passes the exit code through (0 ok-or-baseline /
# 1 flagged / 2 cannot verify).
# Register: powershell -ExecutionPolicy Bypass -File scripts\register_gap_sentinel_task.ps1
# Run now:  powershell -ExecutionPolicy Bypass -File scripts\gap_sentinel_daily.ps1
#
# Wrapper form (not an inline schtasks -Command) is load-bearing: Windows
# PowerShell 5.1 mangles embedded double quotes when passing /TR to
# schtasks.exe — the sibling canary register script's first inline attempt
# (2026-09-29) died with schtasks exit 5 "Invalid argument/option". The
# census patrol's -File wrapper (registered 2026-09-26, runs clean daily) is
# the byte-proven pattern this copies.
#
# OPERATOR RESPONSE (MagGapSentinelDaily Last Result != 0, or no START stamp
# for today in logs/gap_sentinel.log): exit 1 = a project crossed the
# GROWTH bar (default 1.0 GiB/day) or a watched sensor went silent past the
# bar (default 2.0 d) — memory/attention.md carries the gap-sentinel block
# naming the project/sensor and its byte evidence; confirm against bytes
# before acting. Exit 2 = the sentinel could not verify (missing/unparsable
# rollup.json, last_run.json or history row): an incident, inspect
# logs/gap_sentinel.log, never guess. A dark log with a Ready task is the
# instruments-built-not-run disease: schtasks /Query /TN
# MagGapSentinelDaily, re-register or run by hand.
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
Set-Location $Root

$Py = Join-Path $Root ".venv\Scripts\python.exe"
$LogDir = Join-Path $Root "logs"
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir | Out-Null }
$Log = Join-Path $LogDir "gap_sentinel.log"
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

Write-Log "START gap sentinel cwd=$Root"
& $Py tools\gap_sentinel.py 2>&1 | ForEach-Object {
    $line = "$_".TrimEnd()
    Add-Content -Path $Log -Value $line -Encoding utf8
    Write-Host $line
}
$code = $LASTEXITCODE
if ($null -eq $code) { $code = 2 }

Write-Log "END exit=$code"
exit $code
