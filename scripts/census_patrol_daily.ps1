# Mag daily census deep check: tools/census_drift_patrol.py --collect (B2-246, 2026-09-26).
# Mag daily dated meters: tools/meter_patrol.py (B2-469, 2026-09-26) rides this same
# scheduled surface after the census step: one dated row per institutional-cluster
# meter class (RECEIPT candidates or explicit NOBS) into watch/inbox/DATED_METERS.jsonl,
# so window scoring reads dated witness rows instead of bare archive silence.
# Register: powershell -ExecutionPolicy Bypass -File scripts\register_census_patrol_task.ps1
# Run now:  powershell -ExecutionPolicy Bypass -File scripts\census_patrol_daily.ps1
#
# The deep check needs the venv and a full `pytest --collect-only -q` pass, so it
# can never ride the default pre-push path (that block stays flag-free and
# dependency-free). This scheduled surface is its daily home; without it the
# collected-claim drift class is back to hand-catch only (B2-246 falsifier).
#
# OPERATOR RESPONSE (MagCensusPatrolDaily Last Result != 0, or this log shows a
# non-ok verdict, or an alert block landed in memory/attention.md):
#   COLLECT-DRIFT (exit 1): expected on active days, the bar of 20 crossed
#     items crosses within hours of a refresh (B2-246 measured +31 the same
#     day the B2-244 refresh landed). Respond: run
#     `.venv\Scripts\python.exe -m pytest --collect-only -q`, refresh the
#     AGENTS.md **Tests:** bullet with the real counts and today's date, and
#     name the landings that moved the count. A drift you cannot attribute to
#     known landings is a fabrication smell: investigate before refreshing.
#   STALE (exit 1): census older than 7 days while tests/ grew. Same refresh;
#     if you cite executed counts take them from a real `pytest -q` sum.
#   cannot verify (exit 2): the collection itself broke (pytest error, missing
#     venv, timeout). That is an incident, not a census problem: fix what the
#     log names. The patrol stays red until collection is whole again.
#   No START stamp for today in this log: the surface is dark (machine off,
#     logged out, task deregistered). Respond: `schtasks /Query /TN
#     MagCensusPatrolDaily`, re-register if missing, run this script by hand.
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
Set-Location $Root

$Py = Join-Path $Root ".venv\Scripts\python.exe"
$LogDir = Join-Path $Root "logs"
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir | Out-Null }
$Log = Join-Path $LogDir "census_patrol.log"
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

Write-Log "START census deep check (--collect) cwd=$Root"
# Tee-Object is not used here: in Windows PowerShell 5.1 it writes UTF-16 with
# no -Encoding flag, which mojibake'd the tool lines inside this UTF-8 log and
# blinded the Select-String verdict extraction below (B2-246 live-run defect,
# caught on the first scheduled-script run and fixed in the same lane).
& $Py tools\census_drift_patrol.py --collect 2>&1 | ForEach-Object {
    $line = "$_".TrimEnd()
    Add-Content -Path $Log -Value $line -Encoding utf8
    Write-Host $line
}
$code = $LASTEXITCODE
if ($null -eq $code) { $code = 2 }

if ($code -ne 0) {
    $verdict = (Select-String -Path $Log -Pattern "COLLECT-DRIFT|STALE|cannot verify" | Select-Object -Last 1).Line
    if (-not $verdict) { $verdict = "verdict line not found, exit $code" }
    $alert = @"

---

### Census collect patrol fired ($Stamp)

- verdict: $verdict (exit $code)
- log: `logs/census_patrol.log`
- response (exit 1): rerun `.venv/Scripts/python.exe -m pytest --collect-only -q`, refresh the AGENTS.md **Tests:** bullet with the real counts and today's date, name the landings that moved the count; an unattributable drift is a fabrication smell, investigate before refreshing.
- response (exit 2): an incident, fix the collection error the log names; the patrol stays red until collection is whole.
"@
    Add-Content -Path (Join-Path $Root "memory\attention.md") -Value $alert -Encoding utf8
    Write-Log "ALERT appended to memory/attention.md"
}

# B2-469 (2026-09-26): dated witness meters for the institutional cluster.
# Runs after the census step; exit 1 = GAP day named (never backfilled), exit 2 =
# cannot verify. Alert path mirrors the census block so a dark meter day is loud.
Write-Log "START dated meters (institutional cluster) cwd=$Root"
& $Py tools\meter_patrol.py 2>&1 | ForEach-Object {
    $line = "$_".TrimEnd()
    Add-Content -Path $Log -Value $line -Encoding utf8
    Write-Host $line
}
$meterCode = $LASTEXITCODE
if ($null -eq $meterCode) { $meterCode = 2 }

if ($meterCode -ne 0) {
    $mVerdict = (Select-String -Path $Log -Pattern "METER-PATROL: (GAP|cannot verify)" | Select-Object -Last 1).Line
    if (-not $mVerdict) { $mVerdict = "meter verdict line not found, exit $meterCode" }
    $mAlert = @"

---

### Dated meter patrol fired ($Stamp)

- verdict: $mVerdict (exit $meterCode)
- log: `logs/census_patrol.log`
- response (exit 1): the gap day(s) named in the log hold NO meter rows and are NOT backfilled (no fabrication); read watch/inbox/DATED_METERS.jsonl, then decide whether the gap days need a manual wire pull before any window scoring cites those dates.
- response (exit 2): the meter organ could not verify (missing inbox, unwritable ledger, unparsable row); fix what the log names; today's institutional-cluster witness state is unknown until then.
"@
    Add-Content -Path (Join-Path $Root "memory\attention.md") -Value $mAlert -Encoding utf8
    Write-Log "METER alert appended to memory/attention.md"
}

# Fleet task doctor (2026-09-27, from FLEET_TASK_DOCTOR_20260927): the
# instruments-built-not-run disease in scheduled-task form. One pass over the
# Mag* tasks each morning: a Ready task whose LastTaskResult is neither 0
# (ok) nor 267009 (currently running) is a failure nobody watched; a task
# stuck on 267011 (never ran) whose NextRunTime is already past is a dead
# registration. Both alert to memory/attention.md. WARN-only for the patrol
# itself: a broken doctor must never blind the census/meter steps above, so
# this block hard-catches its own errors and never raises the exit code.
Write-Log "START fleet task doctor cwd=$Root"
try {
    $badTasks = @()
    Get-ScheduledTask -TaskName "Mag*" -ErrorAction SilentlyContinue | ForEach-Object {
        if ($_.State -eq "Disabled") { return }
        $info = $_ | Get-ScheduledTaskInfo -ErrorAction SilentlyContinue
        if ($null -eq $info) { return }
        $r = $info.LastTaskResult
        if ($_.State -ne "Running" -and $r -ne 0 -and $r -ne 267009) {
            if ($r -eq 267011) {
                if ($info.NextRunTime -and ($info.NextRunTime -lt (Get-Date))) {
                    $badTasks += ("{0}: never ran AND next-run {1} is past (dead registration)" -f $_.TaskName, $info.NextRunTime)
                }
            } else {
                $badTasks += ("{0}: last result {1} at {2}" -f $_.TaskName, $r, $info.LastRunTime)
            }
        }
    }
    if ($badTasks.Count -gt 0) {
        $tAlert = @"

---

### Fleet task doctor fired ($Stamp)

$( $badTasks | ForEach-Object { "- $_" } | Out-String )
- log: `logs/census_patrol.log`
- response: a named task failed or never fired; autopsy its log (or the never-fired 267011 case: fix or delete the registration). An instrument that never runs is the elder's LIVE 4 / DECLARED 33 disease.
"@
        Add-Content -Path (Join-Path $Root "memory\attention.md") -Value $tAlert -Encoding utf8
        Write-Log ("TASK-DOCTOR: {0} unhealthy task(s) named, alert appended" -f $badTasks.Count)
    } else {
        Write-Log "TASK-DOCTOR: ok (all Mag* tasks ok, running, or not-yet-due)"
    }
} catch {
    Write-Log ("TASK-DOCTOR: self-error (warn-only, patrol continues): {0}" -f $_.Exception.Message)
}

# FOSSIL-IN-FEED arm (2026-09-27, FOSSIL_CENSUS_20260927.md P0-3): the
# thought-quantizer packs fossilized 9 days with zero alarms while the
# invariant stream grew 132->315. Registry-driven since the fossil churn
# (configs/fossil_registry.json: quantizer packs, tombstoned gene-pool
# family, jev trail watch, fixed-oracles, SEATS). WARN-only, same fail-open
# law as the doctor above: a broken check never blinds the patrol.
try {
    $fossilOut = & $Py (Join-Path $Root "tools\fossil_check.py") check 2>&1
    $fossilRc = $LASTEXITCODE
    $fossilOut | ForEach-Object { Write-Log ("FOSSIL-CHECK: {0}" -f $_) }
    if ($fossilRc -eq 1) {
        Add-Content -Path (Join-Path $Root "memory\attention.md") -Value @"

---

### Fossil check fired ($Stamp)

$($fossilOut | Select-String "WARN|HARD" | ForEach-Object { "- $_" } | Out-String)
- registry: configs/fossil_registry.json (adding artifacts = named config edit)
- law: FOSSIL_CENSUS_20260927.md  --  recompile or tombstone within the bar;
  WARN-only, enforce is operator-gated
"@ -Encoding utf8
        Write-Log "FOSSIL-CHECK: WARN alert appended"
    } elseif ($fossilRc -ge 2) {
        Write-Log "FOSSIL-CHECK: cannot-verify (exit $fossilRc) - incident per the census law"
    }
} catch {
    Write-Log ("FOSSIL-CHECK: self-error (warn-only): {0}" -f $_.Exception.Message)
}

# Worst code wins (2 cannot-verify beats 1 drift/gap beats 0 ok).
$final = $code
if ($meterCode -gt $final) { $final = $meterCode }

Write-Log "END exit=$final"
exit $final
