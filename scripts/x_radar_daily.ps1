# Mag daily X reply radar: .venv python -m mag.x_reply_radar run (Z16, 2026-09-30).
# The radar surveys last-24h X AI-thread top replies via the grok CLI ($0
# subscription lane, balance-gated) and files watch/X_REPLY_RADAR_<UTCdate>.md
# + dashboard/static/x_radar.json + memory/runs/x_reply_radar/ raws.
#
# WHY THIS TASK EXISTS (the hole): dashboard/static/x_radar_gaps.json holes[1]
# byte-proves 2026-09-22..25 as "writer never ran: zero artifacts ... no
# in-repo scheduler owns mag.x_reply_radar run". Until Z16 no scheduler ANYWHERE
# invoked it (Get-ScheduledTask sweep 2026-09-30: zero radar matches); the
# 09-11..09-29 cards were hand/seat runs at ~08:05 with gaps. This task is the
# in-repo owner the census demanded.
#
# TIME: 08:00 local, the documented original (watch/BUILD_REPORT_20260907_NIGHT.md
# "X radar 08:00"; empirical raw mtimes 08:05-08:08 = 08:00 starts). Shares the
# slot with MagImproveDaily + MagLeaveProtocolDaily, the proven 2-task shape.
#
# Register: powershell -ExecutionPolicy Bypass -File scripts\register_x_radar_task.ps1
# Run now:  powershell -ExecutionPolicy Bypass -File scripts\x_radar_daily.ps1
#
# COST LAW: the grok CLI rides a Grok Build usage balance. A 402 in
# memory/runs/x_reply_radar/err_<date>.log (or a 0-byte out_<date>.json with a
# 402 err) is the 2026-09-09..10 hole class: balance exhausted. Response is
# top-up/wait for the next firing — NEVER backfill or hand-write a card.
#
# OPERATOR RESPONSE (MagXRadarDaily Last Result != 0, or no START stamp for
# today in logs/x_radar.log):
#   exit 1 (radar failed: grok 402/timeout, no-JSON-block parse death): read
#     memory/runs/x_reply_radar/err_<date>.log named in the log; 402 = balance
#     (cost law above); parse/no-JSON = inspect out_<date>.json raw and reparse
#     with `.venv\Scripts\python.exe -m mag.x_reply_radar parse <raw>`.
#   exit 2 (cannot verify: venv python or grok CLI missing): fix the path the
#     log names; the radar stays dark until then.
#   No START stamp today: surface is dark (machine off/logged out/task
#     deregistered). `schtasks /Query /TN MagXRadarDaily`, re-register, run by
#     hand. The census patrol's fleet task doctor watches this task each
#     morning (Mag* sweep) as a second net.
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
Set-Location $Root

$Py = Join-Path $Root ".venv\Scripts\python.exe"
# 2026-10-03: grok CLI update ships grok.exe; accept it before the legacy
# no-extension name (the old single probe failed the task daily 09-30..10-03).
$Grok = Join-Path $env:USERPROFILE ".grok\bin\grok.exe"
if (-not (Test-Path $Grok)) { $Grok = Join-Path $env:USERPROFILE ".grok\bin\grok" }
$LogDir = Join-Path $Root "logs"
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir | Out-Null }
$Log = Join-Path $LogDir "x_radar.log"
$Stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

function Write-Log([string]$Msg) {
    $line = "[$Stamp] $Msg"
    Add-Content -Path $Log -Value $line -Encoding utf8
    Write-Host $line
}

if (-not (Test-Path $Py)) {
    Write-Log "FAIL: missing venv python at $Py (cannot verify, exit 2)"
    exit 2
}
if (-not (Test-Path $Grok)) {
    Write-Log "FAIL: missing grok CLI at $Grok (cannot verify, exit 2)"
    exit 2
}

Write-Log "START x reply radar (mag.x_reply_radar run) cwd=$Root"
# No Tee-Object: Windows PowerShell 5.1 writes UTF-16 without -Encoding and
# mojibake'd verdict extraction in census_patrol_daily.ps1 (B2-246 live-run
# defect). Same law here: stream line-by-line into the UTF-8 log.
& $Py -m mag.x_reply_radar run 2>&1 | ForEach-Object {
    $line = "$_".TrimEnd()
    Add-Content -Path $Log -Value $line -Encoding utf8
    Write-Host $line
}
$code = $LASTEXITCODE
if ($null -eq $code) { $code = 2 }

if ($code -ne 0) {
    $alert = @"

---

### X reply radar failed ($Stamp)

- exit: $code (1 = run failed: grok 402/timeout or no-JSON parse; 2 = cannot verify env)
- log: `logs/x_radar.log` (grok stderr: `memory/runs/x_reply_radar/err_<date>.log`)
- response (402): Grok Build balance exhausted (the 2026-09-09..10 hole class) - top-up/wait for next firing, never backfill a card.
- response (parse): reparse the raw with `.venv/Scripts/python.exe -m mag.x_reply_radar parse memory/runs/x_reply_radar/out_<date>.json`.
- response (exit 2): fix the missing venv/grok path the log names; radar dark until then.
"@
    Add-Content -Path (Join-Path $Root "memory\attention.md") -Value $alert -Encoding utf8
    Write-Log "ALERT appended to memory/attention.md"
}

Write-Log "END exit=$code"
exit $code
