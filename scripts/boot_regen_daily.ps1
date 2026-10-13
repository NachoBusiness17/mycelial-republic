# Mag daily boot-surface regen chain (ouroboros R4b move 2, 2026-10-06):
#   .venv\Scripts\python.exe -m mag.boot_regen --json
# Register: powershell -ExecutionPolicy Bypass -File scripts\register_boot_regen_task.ps1
# Run now:  powershell -ExecutionPolicy Bypass -File scripts\boot_regen_daily.ps1
#
# Why this exists (SYNTHESIS move 2 / fold finding S2,
# watch/inbox/ractor_engine/2026-10-05-ouroboros-r4-memory): organ freshness
# was READER-coupled - the regen chain fired only inside `mag.cmd
# context-pack`, a command a seat must choose to run, so a dark week with no
# seat booting silently re-staled every organ while the alarm lived inside
# the same command the absent reader never ran. This task is the clock leg.
# It also carries attribution (fold S3): MAG_BOOT_REGEN_TRIGGER rides the
# chain onto the zknot runs.jsonl receipt rows as --trigger, so regens name
# what fired them (the 2026-10-05/06 burst all read actor null, trigger
# null). The law pack itself is NOT recompiled here - MagLawPackDaily 09:30
# owns that - but boot_regen's age gate reads its stamp, so a dark law pack
# turns this task's verdict red too.
#
# EXIT-CODE CONTRACT (mag.boot_regen: 0 ok/skipped, 2 otherwise):
#   exit 0: chain fired clean (or MAG_BOOT_REGEN_SKIP skipped firing while
#     the age gate still passed). Done.
#   exit 2: a step failed (zknot exit 2 = the S1 no-silent-truncation gate;
#     the previous LATEST stays in place), an organ artifact is missing, or
#     any component is older than PACK_STALE_DAYS (7d) - the same verdict
#     that exits mag.cmd context-pack 2.
# ALERT: nonzero verdict - dated block in memory/attention.md (best-effort,
#   hot multi-writer file) and watch/inbox/boot_regen_alerts.jsonl (the
#   single-writer surface of record); the script exits nonzero so schtasks
#   Last Result carries it.
#
# OPERATOR RESPONSE (MagBootRegenDaily Last Result != 0, or no START stamp
# for today in logs/boot_regen.log): the surface is dark (machine off,
# logged out, task deregistered). Respond: schtasks /Query /TN
# MagBootRegenDaily, re-register via scripts\register_boot_regen_task.ps1,
# run this script by hand. A step-failure names the organ and its tail in
# the log; an age/missing verdict also gates mag.cmd context-pack until
# cured (cure = run the named organ by hand, or the law pack task if the
# lawpack row is the stale one).
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
Set-Location $Root

$Py = Join-Path $Root ".venv\Scripts\python.exe"
$LogDir = Join-Path $Root "logs"
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir | Out-Null }
$Log = Join-Path $LogDir "boot_regen.log"
$Stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# Log file only, no Write-Host: detached scheduled consoles hang in kernel
# waits after completed work (MagFtsIndexDaily first fire, B2-465); the
# identical code path completes in seconds by hand.
function Write-Log([string]$Msg) {
    Add-Content -Path $Log -Value ("[$Stamp] $Msg") -Encoding utf8
}

if (-not (Test-Path $Py)) {
    Write-Log "FAIL: missing venv python at $Py (exit 2)"
    exit 2
}

# attribution (fold S3): the chain stamps this trigger onto the zknot
# runs.jsonl receipt rows and onto its own report.
$env:MAG_BOOT_REGEN_TRIGGER = "MagBootRegenDaily"

Write-Log "START boot_regen chain (zknot+warm_boot+rib_boot) trigger=MagBootRegenDaily cwd=$Root"

# Tool output through an Add-Content loop, never Tee-Object: PS 5.1 Tee
# writes UTF-16 and mojibakes the log (B2-246 sibling lesson).
$sw = [System.Diagnostics.Stopwatch]::StartNew()
$out = & $Py "-m" "mag.boot_regen" "--json" 2>&1
$code = $LASTEXITCODE
if ($null -eq $code) { $code = 2 }
$sw.Stop()
foreach ($line in @($out)) { Add-Content -Path $Log -Value ("  " + "$line".TrimEnd()) -Encoding utf8 }
Write-Log ("tool -m mag.boot_regen --json -> exit=$code wall=" + [math]::Round($sw.Elapsed.TotalSeconds, 3) + "s")

$finalCode = $code
if ($finalCode -ne 0) {
    $verdict = "boot_regen chain exited $finalCode; the logged report names the step failure, missing organ, or age debt"
    $alert = @"

---

### Boot-regen daily fired ($Stamp)

- verdict: $verdict
- log: logs/boot_regen.log
- response: rerun powershell -ExecutionPolicy Bypass -File scripts\boot_regen_daily.ps1 by hand; a zknot step-failure is the S1 no-silent-truncation gate keeping the previous LATEST (inspect the log tail); an age/missing verdict names the organ to regenerate (the lawpack row belongs to MagLawPackDaily 09:30).
"@
    $AlertLog = Join-Path $Root "watch\inbox\boot_regen_alerts.jsonl"
    $alertRow = @{ ts = ((Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")); task = "MagBootRegenDaily"; verdict = $verdict; log = "logs/boot_regen.log"; exit = $finalCode } | ConvertTo-Json -Compress
    Add-Content -Path $AlertLog -Value $alertRow -Encoding utf8
    Write-Log "ALERT row appended to watch/inbox/boot_regen_alerts.jsonl"
    Add-Content -Path (Join-Path $Root "memory\attention.md") -Value $alert -Encoding utf8
    Write-Log "attention.md append attempted (best-effort, loss-prone under concurrent writers)"
}

Write-Log "END exit=$finalCode"
exit $finalCode
