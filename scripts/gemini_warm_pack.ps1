# scripts/gemini_warm_pack.ps1 - Gemini seat warm launcher (host-side).
#
# The web seat cannot mount host bytes; it can only receive pasted text. So
# "launch and be aware" composes HERE: refresh the verkle tip through the
# sanctioned writer (mag.hermes_warm_boot -> memory/warm_state.json), pull the
# newest SOAK_BEACON Position section, stamp the fixed estate-law block, put
# the pack on the clipboard. Reads exactly two known files; never globs, so
# nothing secret can ride along (secret exclusion is by construction, not by
# pattern filter). Fabricated-bootstrap guard: the 2026-10-16 Gemini-notebook
# draft (Launch-LatestVerkle.ps1) invented `python -m local_sovereign_agent`,
# --boot-source/--verkle-state/--no-secrets, MAG_VERKLE_* env vars, and a
# watch/ glob for "verkle artifacts" that would crown a random receipt json;
# none exist in this repo (verified 2026-10-16 by the ZCode seat).
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File scripts\gemini_warm_pack.ps1
#   (add -NoClipboard to skip Set-Clipboard; -OutFile <path> to also save)
[CmdletBinding()]
param(
    [string]$RepoRoot = "",
    [string]$OutFile = "",
    [switch]$NoClipboard
)
$ErrorActionPreference = "Stop"
# $PSScriptRoot is empty in param defaults on Windows PowerShell 5.1; resolve here
if (-not $RepoRoot) { $RepoRoot = Split-Path -Parent $PSScriptRoot }

$Py = Join-Path $RepoRoot ".venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $Py -PathType Leaf)) {
    throw "ESTATE_FAULT: venv python missing at $Py (scripts\ensure_venv.ps1 repairs it)"
}

# 1. refresh the tip (sanctioned writer; no other path knows the chain)
& $Py -m mag.hermes_warm_boot | Out-Null
if ($LASTEXITCODE -ne 0) { throw "ESTATE_FAULT: mag.hermes_warm_boot exited $LASTEXITCODE" }

$WarmPath = Join-Path $RepoRoot "memory\warm_state.json"
$Warm = Get-Content -LiteralPath $WarmPath -Raw | ConvertFrom-Json
if (-not $Warm.chain.ok) { throw "ESTATE_FAULT: warm boot chain not ok (see $WarmPath)" }

# 2. newest authored beacon, Position section only
$Beacon = Get-ChildItem -LiteralPath (Join-Path $RepoRoot "state") -Filter "SOAK_BEACON_*.md" -File |
    Sort-Object LastWriteTimeUtc -Descending | Select-Object -First 1
$Position = "(no beacon found)"
$BeaconName = "none"
if ($Beacon) {
    $BeaconName = $Beacon.Name
    $lines = Get-Content -LiteralPath $Beacon.FullName
    $start = -1
    for ($i = 0; $i -lt $lines.Count; $i++) { if ($lines[$i] -match '^## Position') { $start = $i; break } }
    if ($start -ge 0) {
        $end = $lines.Count
        for ($j = $start + 1; $j -lt $lines.Count; $j++) { if ($lines[$j] -match '^## ') { $end = $j; break } }
        $Position = ($lines[($start + 1)..($end - 1)] -join "`n").TrimEnd()
    }
}

# 3. compose (fixed law block; no em-dashes per house law)
$stamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
$c = $Warm.chain
$pack = @"
MAG ESTATE - WARM LAUNCH PACK (external judgment seat)
stamped $stamp UTC by scripts/gemini_warm_pack.ps1

CHAIN TIP (verkle, source memory/warm_state.json, generated $($Warm.generated)):
- index $($c.index), $($c.n_leaves) leaves
- verkle_root $($c.verkle_root)
- parent_root $($c.parent_root)
- tip moment $($c.ts), dominant theme: $($c.dominant_theme)

ESTATE POSITION (newest beacon: state/$BeaconName):
$Position

LAWS (fixed block, applies to every answer):
- Trust bytes, not reports: cite sources for every claim; a citation that does
  not resolve is marked UNVERIFIED.
- A verdict without its conditions is not a verdict: name instrument, moment,
  and assumptions for any measurement you rely on.
- No em-dashes. Plain hyphens only.
- Prefer ONE landable deliverable over a survey. Name your own deliverable's
  falsifier.
- For a substantial ask produce a self-contained structured document with
  clear markdown sections - not chat, no meta-commentary about formatting.
- You are an external surface: everything pasted here is public-safe by
  design. Never ask for host files, secrets, or context beyond this pack;
  say PACK-BOUNDED instead.

LAUNCH RECEIPT: your first reply recites the chain tip above (index + verkle_root
prefix) in one line, then awaits the ask. If you cannot recite it, you did not
load this pack - say so instead of pretending.
"@

if ($OutFile) { Set-Content -LiteralPath $OutFile -Value $pack -Encoding UTF8 }
if (-not $NoClipboard) { Set-Clipboard -Value $pack; Write-Host "pack on clipboard ($($pack.Length) chars)" }
Write-Output $pack
