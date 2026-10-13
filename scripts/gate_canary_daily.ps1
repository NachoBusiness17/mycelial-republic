# Mag daily gate-liveness canary wrapper: tools/gate_canary.py (Mickey17 W2
# return 7/24, 2026-09-29). The tool self-alerts DEAD/BLIND gates to
# memory/attention.md (its one sanctioned real-tree write), so this wrapper
# only stamps the log and passes the exit code through (0 ok / 1 dead-or-blind
# gate / 2 cannot verify).
# Register: powershell -ExecutionPolicy Bypass -File scripts\register_gate_canary_task.ps1
# Run now:  powershell -ExecutionPolicy Bypass -File scripts\gate_canary_daily.ps1
#
# Wrapper form (not an inline schtasks -Command) is load-bearing: Windows
# PowerShell 5.1 mangles embedded double quotes when passing /TR to
# schtasks.exe, and the first registration attempt of the inline form
# (2026-09-29, W3 lane) died with schtasks exit 5 "Invalid argument/option"
# before any task existed. The census patrol's -File wrapper
# (census_patrol_daily.ps1, registered 2026-09-26, runs clean daily) is the
# byte-proven pattern this copies.
#
# OPERATOR RESPONSE (MagGateCanaryDaily Last Result != 0, or no START stamp
# for today in logs/gate_canary.log): exit 1 = a pre-push gate was silent on
# its own known-bad — memory/attention.md carries the [gate-canary] row
# naming it; investigate that gate before trusting any push. Exit 2 = the
# canary itself could not verify (worktree setup failed or real-tree taint):
# treat as an incident. A dark log with a Ready task is the instruments-
# built-not-run disease: schtasks /Query /TN MagGateCanaryDaily, re-register
# or run by hand.
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
Set-Location $Root

$Py = Join-Path $Root ".venv\Scripts\python.exe"
$LogDir = Join-Path $Root "logs"
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir | Out-Null }
$Log = Join-Path $LogDir "gate_canary.log"
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

Write-Log "START gate canary cwd=$Root"
& $Py tools\gate_canary.py 2>&1 | ForEach-Object {
    $line = "$_".TrimEnd()
    Add-Content -Path $Log -Value $line -Encoding utf8
    Write-Host $line
}
$code = $LASTEXITCODE
if ($null -eq $code) { $code = 2 }

Write-Log "END exit=$code"
exit $code
