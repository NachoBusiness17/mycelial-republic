# Mag day-end pile habit (FW-50, 2026-09-28): the session-close/overnight
# discipline mechanized instead of memory-held. Two steps, $0, local-first:
#   1. DAY-END SNAPSHOT - one capture_summary(kind="session_end", source
#      "day_end_pile.ps1") row into memory/pile/state_summaries.jsonl so the
#      day closes with a state row even when no session ran capture_summary.
#   2. PILE DRAIN - tools/pile_classify.py --limit 50 (local gemma4, free,
#      idempotent: classified ids are skipped) so the pile does not silt and
#      the classified rows keep feeding training + case law.
# Register: powershell -ExecutionPolicy Bypass -File scripts\register_day_end_task.ps1
# Run now:  powershell -ExecutionPolicy Bypass -File scripts\day_end_pile.ps1
#
# OPERATOR RESPONSE (this log shows a FAIL line, or memory/attention.md gained
# a "Day-end pile" block): step 2 exit 2 = cannot verify (ollama down, gemma4
# missing, pile unreadable) - fix what the log names; the unclassified count
# is visible via `python main.py pile-classify status` semantics in
# mag.state_snapshot.status(). Step 1 failure is WARN-only: a duplicate
# state_hash day (script ran twice) is logged, never alerted.
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
Set-Location $Root

$Py = Join-Path $Root ".venv\Scripts\python.exe"
$LogDir = Join-Path $Root "logs"
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir | Out-Null }
$Log = Join-Path $LogDir "day_end_pile.log"
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

# Step 1: the day-end snapshot (WARN-only on failure).
Write-Log "START day-end snapshot cwd=$Root"
$cap = & $Py -c "import sys; sys.path.insert(0, r'$Root'); from mag.state_snapshot import capture_summary, status; r = capture_summary(goal='day-end pile habit (FW-50): scheduled day-close capture', outcome='ok', kind='session_end', tier='scheduled', source='day_end_pile.ps1'); s = status(); print('CAPTURED', r.get('ok'), (r.get('row') or {}).get('id'), 'pile_total', s.get('pile'), 'unclassified', s.get('unclassified'))" 2>&1
$capCode = $LASTEXITCODE
$cap | ForEach-Object { Write-Log ("SNAPSHOT: {0}" -f $_) }
if ($capCode -ne 0) {
    Write-Log "WARN: snapshot step failed (exit $capCode); pile drain continues"
}

# Step 2: drain the pile (exit 0 ok, 1 = nothing drainable per tool, 2 = cannot verify).
Write-Log "START pile drain (limit 50, local model)"
& $Py tools\pile_classify.py --limit 50 2>&1 | ForEach-Object {
    $line = "$_".TrimEnd()
    Add-Content -Path $Log -Value $line -Encoding utf8
    Write-Host $line
}
$code = $LASTEXITCODE
if ($null -eq $code) { $code = 2 }

if ($code -ge 2) {
    Add-Content -Path (Join-Path $Root "memory\attention.md") -Value @"

---

### Day-end pile drain failed ($Stamp)

- exit $code from tools/pile_classify.py (cannot verify: ollama down, gemma4 missing, or pile unreadable)
- log: `logs/day_end_pile.log`
- response: fix what the log names; the pile keeps silting until the drain runs (mag.state_snapshot.status() shows the unclassified count).
"@ -Encoding utf8
    Write-Log "ALERT appended to memory/attention.md"
}

Write-Log "END exit=$code"
exit $code
