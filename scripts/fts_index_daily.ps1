# Mag daily FTS index rebuild + deep audit (B2-465, 2026-09-26):
#   .venv\Scripts\python.exe tools\corpus_fts_rebuild.py --check --deep
# Register: powershell -ExecutionPolicy Bypass -File scripts\register_fts_index_task.ps1
# Run now:  powershell -ExecutionPolicy Bypass -File scripts\fts_index_daily.ps1
#
# Why this exists: the B2-102 freshness gate detects staleness but nothing
# rebuilt on cadence, so after the next catalog rebuild the index decayed to
# permanent scan fallback (still correct, 3.4 to 3.9s per search on the
# full-scan class, milliseconds on the fts5 path). This task is that decay's
# daily home; without it the decay is back to hand-catch only.
#
# EXIT-CODE CONTRACT (tools/corpus_fts_rebuild.py --check: 0 fresh, 2 otherwise):
#   PRE check exit 0: index fresh and the deep sha256 audit matched. Done.
#   PRE check exit 2: the JSON block logged below names the gate (mtime,
#     catalog_bytes, or deep sha256 mismatch); the rebuild runs through the
#     one sanctioned writer, then the deep check runs again. A routine day is
#     stale-then-fresh with no operator action.
#   ALERT: when the index is not fresh after the rebuild attempt, or the
#     rebuild itself exits nonzero: a dated alert block lands in
#     memory/attention.md and this script exits nonzero so schtasks Last
#     Result carries it. A catalog mtime lying in the future is the known
#     unrepairable shape (measured live, B2-465): no rebuild can make the
#     index newer than a future catalog stamp, so it alerts every cycle
#     until the mtime is fixed.
#
# OPERATOR RESPONSE (MagFtsIndexDaily Last Result != 0, or an alert block in
# memory/attention.md, or a stale verdict in this log that did not clear):
#   not fresh after a rebuild: incident. Inspect the last JSON blocks in
#     logs/fts_index.log (the note names the gate), verify the catalog is
#     whole (git status catalog/catalog.jsonl; a future mtime on
#     catalog.jsonl is the known unrepairable shape), rerun
#     powershell -ExecutionPolicy Bypass -File scripts\fts_index_daily.ps1
#     by hand. corpus_search answers on scan fallback (correct, seconds per
#     query) until an index comes fresh.
#   rebuild failed: fix what the tool output names (missing catalog.jsonl,
#     broken venv). Until a build replaces it the old index file keeps
#     serving readers (the build writes a tmp db and os.replace()s it).
#   No START stamp for today in this log: the surface is dark (machine off,
#     logged out, task deregistered). Respond: schtasks /Query /TN
#     MagFtsIndexDaily, re-register if missing, run this script by hand.
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
Set-Location $Root

$Py = Join-Path $Root ".venv\Scripts\python.exe"
$LogDir = Join-Path $Root "logs"
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir | Out-Null }
$Log = Join-Path $LogDir "fts_index.log"
$Stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# Log file only, no Write-Host: the first scheduled run of this script
# (19:27:21Z, B2-465) hung for 100+ seconds with the thread parked in a
# kernel wait after a completed rebuild, while the identical code path
# completed in 7s by hand in a visible console; the detached scheduled
# console is the one suspect, so the landed script writes nothing to it.
function Write-Log([string]$Msg) {
    Add-Content -Path $Log -Value ("[$Stamp] $Msg") -Encoding utf8
}

if (-not (Test-Path $Py)) {
    Write-Log "FAIL: missing venv python at $Py (cannot verify, exit 2)"
    exit 2
}

Write-Log "START fts index deep check (--check --deep) cwd=$Root"

# Log tool output through an Add-Content loop, never Tee-Object: in Windows
# PowerShell 5.1 Tee-Object writes UTF-16 with no -Encoding flag, which
# mojibake'd the tool lines inside the UTF-8 log and blinded the verdict
# extraction on the B2-246 sibling script's first run.
Write-Log "PRE: tools/corpus_fts_rebuild.py --check --deep"
$sw = [System.Diagnostics.Stopwatch]::StartNew()
$pre = & $Py "tools\corpus_fts_rebuild.py" --check --deep 2>&1
$preCode = $LASTEXITCODE
if ($null -eq $preCode) { $preCode = 2 }
$sw.Stop()
foreach ($line in @($pre)) { Add-Content -Path $Log -Value ("  " + "$line".TrimEnd()) -Encoding utf8 }
$preWall = [math]::Round($sw.Elapsed.TotalSeconds, 3)
Write-Log "PRE: exit=$preCode wall=${preWall}s"

$finalCode = $preCode
$verdict = ""
if ($preCode -ne 0) {
    Write-Log "STALE (exit $preCode): rebuilding through the one sanctioned writer tools/corpus_fts_rebuild.py"
    $sw.Restart()
    $reb = & $Py "tools\corpus_fts_rebuild.py" 2>&1
    $rebCode = $LASTEXITCODE
    if ($null -eq $rebCode) { $rebCode = 2 }
    $sw.Stop()
    foreach ($line in @($reb)) { Add-Content -Path $Log -Value ("  " + "$line".TrimEnd()) -Encoding utf8 }
    $rebWall = [math]::Round($sw.Elapsed.TotalSeconds, 3)
    Write-Log "REBUILD: exit=$rebCode wall=${rebWall}s"
    # The rebuild tool exits nonzero when its own post-build gate read is not
    # fresh, so a nonzero rebuild exit still gets a POST deep check: the
    # alert must name the true gate, not guess "broken catalog or venv".
    Write-Log "POST: tools/corpus_fts_rebuild.py --check --deep"
    $sw.Restart()
    $post = & $Py "tools\corpus_fts_rebuild.py" --check --deep 2>&1
    $postCode = $LASTEXITCODE
    if ($null -eq $postCode) { $postCode = 2 }
    $sw.Stop()
    foreach ($line in @($post)) { Add-Content -Path $Log -Value ("  " + "$line".TrimEnd()) -Encoding utf8 }
    $postWall = [math]::Round($sw.Elapsed.TotalSeconds, 3)
    Write-Log "POST: exit=$postCode wall=${postWall}s"
    if ($rebCode -eq 0 -and $postCode -eq 0) {
        $finalCode = 0
    } else {
        $finalCode = if ($postCode -ne 0) { $postCode } else { $rebCode }
        if ($rebCode -ne 0 -and $postCode -eq 0) {
            $verdict = "REBUILD TOOL EXIT $rebCode BUT THE POST CHECK IS FRESH; inspect logs/fts_index.log before trusting the green"
        } elseif ($rebCode -ne 0) {
            $verdict = "REBUILD DID NOT BRING THE INDEX FRESH (rebuild exit $rebCode, post exit $postCode); the log JSON names the gate"
        } else {
            $verdict = "STALE SURVIVED THE REBUILD exit $postCode; the index will not come fresh, treat as an incident (see logs/fts_index.log)"
        }
    }
}

if ($finalCode -ne 0) {
    if (-not $verdict) { $verdict = "nonzero exit $finalCode after the check-plus-rebuild cycle, see logs/fts_index.log" }
    $alert = @"

---

### FTS index daily fired ($Stamp)

- verdict: $verdict
- log: logs/fts_index.log (the JSON blocks name the gate: mtime, catalog_bytes, or deep sha256 mismatch)
- response (not fresh after a rebuild): incident. Inspect the log JSON note, verify the catalog is whole (git status catalog/catalog.jsonl; a future mtime on catalog.jsonl is the known unrepairable shape), rerun powershell -ExecutionPolicy Bypass -File scripts\fts_index_daily.ps1 by hand; corpus_search is on scan fallback (correct, seconds per query) until fresh.
- response (rebuild failed): fix what the tool output names (missing catalog.jsonl, broken venv); readers keep the old index file until a build replaces it.
"@
    # Durable alert record FIRST: watch/inbox/fts_index_alerts.jsonl has
    # exactly one writer (this script), so appends cannot race. The
    # memory/attention.md append below is best-effort operator visibility
    # only: live-measured on the first two real fires of this task
    # (19:31:31Z and 19:40:05Z 2026-09-26, B2-465), both Add-Content
    # appends returned success yet neither block survived in attention.md
    # even seconds later, because attention.md is a hot multi-writer file
    # where unsynchronized concurrent appends lose bytes. The task log and
    # this jsonl are the alert surface of record.
    $AlertLog = Join-Path $Root "watch\inbox\fts_index_alerts.jsonl"
    $alertRow = @{ ts = ((Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")); task = "MagFtsIndexDaily"; verdict = $verdict; log = "logs/fts_index.log"; exit = $finalCode } | ConvertTo-Json -Compress
    Add-Content -Path $AlertLog -Value $alertRow -Encoding utf8
    Write-Log "ALERT row appended to watch/inbox/fts_index_alerts.jsonl"
    Add-Content -Path (Join-Path $Root "memory\attention.md") -Value $alert -Encoding utf8
    Write-Log "attention.md append attempted (best-effort, loss-prone under concurrent writers)"
    Write-Log "ALERT appended to memory/attention.md"
}

Write-Log "END exit=$finalCode"
exit $finalCode
