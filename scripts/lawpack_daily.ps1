# Mag daily law-pack recompile + staleness audit (ouroboros R4-L1, 2026-10-05):
#   .venv\Scripts\python.exe tools\thought_quantizer.py --check   (0 fresh / 1 stale / 2 no report)
#   .venv\Scripts\python.exe tools\thought_quantizer.py compile   (refuses empty compiles: MIN_KEPT_LAWS)
# Register: powershell -ExecutionPolicy Bypass -File scripts\register_lawpack_task.ps1
# Run now:  powershell -ExecutionPolicy Bypass -File scripts\lawpack_daily.ps1
#
# Why this exists (SYNTHESIS move 2,
# watch/inbox/ractor_engine/2026-10-05-ouroboros-r4-memory): the pack compiled
# 2026-09-29 held 12 flash rows with zero of the week's law, and past
# PACK_STALE_DAYS (7d) the consumer hides ALL compiled law behind a debt
# pointer - a time bomb with no trigger wired to recompile it. This task is
# the trigger. mag/boot_regen.py exits context-pack 2 when this task goes
# dark and the pack ages past the bar, so darkness is loud both ways.
#
# EXIT-CODE CONTRACT (thought_quantizer: check 0 fresh / 1 stale / 2 no
# report; compile 0 ok):
#   PRE check exit 0: pack fresh. Done, nothing written.
#   PRE check exit 1 or 2: recompile through the compiler, then POST check
#     must read fresh AND the flash pack must hold at least 1 law row (the
#     min-rows assertion's read-side twin; bytes, not reports).
#   ALERT: compile failed, or POST not fresh, or flash rows 0: a dated block
#     lands in memory/attention.md (best-effort) and watch/inbox/
#     lawpack_alerts.jsonl (single-writer surface of record), and this script
#     exits nonzero so schtasks Last Result carries it.
#
# OPERATOR RESPONSE (MagLawPackDaily Last Result != 0, or an alert block in
# memory/attention.md, or no START stamp for today in logs/lawpack.log):
#   the surface is dark (machine off, task deregistered). Respond:
#   schtasks /Query /TN MagLawPackDaily, re-register via
#   scripts\register_lawpack_task.ps1, rerun this script by hand.
#   compile failed: read the tool output in the log (empty-refusal names the
#   input shape; missing venv names itself). The PREVIOUS packs keep serving
#   readers until a fresh compile lands (the compiler refuses to write empty
#   packs over good ones, R4-L1 min-rows assertion).
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
Set-Location $Root

$Py = Join-Path $Root ".venv\Scripts\python.exe"
$LogDir = Join-Path $Root "logs"
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir | Out-Null }
$Log = Join-Path $LogDir "lawpack.log"
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

Write-Log "START lawpack check cwd=$Root"

# Tool output through an Add-Content loop, never Tee-Object: PS 5.1 Tee
# writes UTF-16 and mojibakes the log (B2-246 sibling lesson).
function Invoke-Logged([string[]]$ToolArgs) {
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    $out = & $Py @ToolArgs 2>&1
    $code = $LASTEXITCODE
    if ($null -eq $code) { $code = 2 }
    $sw.Stop()
    foreach ($line in @($out)) { Add-Content -Path $Log -Value ("  " + "$line".TrimEnd()) -Encoding utf8 }
    Write-Log ("tool " + ($ToolArgs -join " ") + " -> exit=$code wall=" + [math]::Round($sw.Elapsed.TotalSeconds, 3) + "s")
    return @{ code = $code }
}

$pre = Invoke-Logged @("tools\thought_quantizer.py", "--check")
$finalCode = 0
$verdict = ""
if ($pre.code -ne 0) {
    Write-Log "STALE (exit $($pre.code)): recompiling through tools/thought_quantizer.py"
    $reb = Invoke-Logged @("tools\thought_quantizer.py", "compile")
    if ($reb.code -ne 0) {
        $finalCode = 2
        $verdict = "COMPILE FAILED exit $($reb.code); previous packs still serving (min-rows refusal keeps good packs)"
    } else {
        $post = Invoke-Logged @("tools\thought_quantizer.py", "--check")
        $flash = Join-Path $Root "memory\corpus\quantized_thought\instructions_flash.jsonl"
        $rows = 0
        if (Test-Path $flash) {
            $rows = @(Get-Content $flash -Encoding utf8 | Where-Object { $_.Trim() -ne "" }).Count
        }
        Write-Log "POST: check exit=$($post.code) flash_rows=$rows"
        if ($post.code -ne 0) {
            $finalCode = 2
            $verdict = "RECOMPILE DID NOT COME FRESH (post check exit $($post.code))"
        } elseif ($rows -lt 1) {
            $finalCode = 2
            $verdict = "FLASH PACK EMPTY (rows=0) after a green compile; an empty compile must never serve as law"
        } else {
            $verdict = "recompiled fresh; flash_rows=$rows"
        }
    }
} else {
    $verdict = "fresh, no write"
}

if ($finalCode -ne 0) {
    $alert = @"

---

### Law-pack daily fired ($Stamp)

- verdict: $verdict
- log: logs/lawpack.log
- response: rerun powershell -ExecutionPolicy Bypass -File scripts\lawpack_daily.ps1 by hand; a failed compile names its input shape in the log; context-pack exits 2 (boot_regen age gate) until a fresh pack lands.
"@
    $AlertLog = Join-Path $Root "watch\inbox\lawpack_alerts.jsonl"
    $alertRow = @{ ts = ((Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")); task = "MagLawPackDaily"; verdict = $verdict; log = "logs/lawpack.log"; exit = $finalCode } | ConvertTo-Json -Compress
    Add-Content -Path $AlertLog -Value $alertRow -Encoding utf8
    Write-Log "ALERT row appended to watch/inbox/lawpack_alerts.jsonl"
    Add-Content -Path (Join-Path $Root "memory\attention.md") -Value $alert -Encoding utf8
    Write-Log "attention.md append attempted (best-effort, loss-prone under concurrent writers)"
}

Write-Log "END exit=$finalCode verdict=$verdict"
exit $finalCode
