# Mag daily tip witness: tools/tip_witness.py --publish --go (W3, 2026-09-30).
# Register: powershell -ExecutionPolicy Bypass -File scripts\register_tip_witness_task.ps1
# Run now:  powershell -ExecutionPolicy Bypass -File scripts\tip_witness_daily.ps1
#
# The verkle chain is writer-only tamper-evident; the gist is the external
# checkpoint that survives a writer rewrite. This scheduled publish is the
# ratchet's daily advance: the witness only ever moves FORWARD on leaf-count
# growth (tools/tip_witness.py refuses backward/sideways moves), so the
# operator's act of registering this task IS the --go consent the CLI gates on.
#
# OPERATOR RESPONSE (Last Result != 0, or an alert block landed in
# memory/attention.md):
#   DIVERGENT (exit 1): the live tip contradicts the witnessed line - chain
#     rewritten, laundering alarm. Do NOT widen scopes or re-publish to
#     "fix" it. Audit with `.venv\Scripts\python.exe main.py verkle-audit
#     --dry` and the gist revision history; the witness stays put until a
#     human explains the rewrite.
#   cannot verify (exit 2): no GITHUB_TOKEN, network down, or gist-scope
#     denial (the 2026-09-30 probe found the fine-grained PAT has gist READ
#     but gist WRITE denied - HTTP 403 on POST /gists). Fix the credential:
#     Account permissions -> Gists: Read and write, or a classic PAT with
#     the gist scope; the witness surface is dark until then.
#   No START stamp for today in this log: the surface is dark (machine off,
#     logged out, task deregistered). Respond: `schtasks /Query /TN
#     MagTipWitnessDaily`, re-register if missing, run this script by hand.
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
Set-Location $Root

$Py = Join-Path $Root ".venv\Scripts\python.exe"
$LogDir = Join-Path $Root "logs"
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir | Out-Null }
$Log = Join-Path $LogDir "tip_witness.log"
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

Write-Log "START tip witness publish cwd=$Root"
# No Tee-Object (PS 5.1 writes UTF-16, mojibakes the verdict extraction
# below - the B2-246 census-patrol defect, avoided here the same way).
& $Py tools\tip_witness.py --publish --go 2>&1 | ForEach-Object {
    $line = "$_".TrimEnd()
    Add-Content -Path $Log -Value $line -Encoding utf8
    Write-Host $line
}
$code = $LASTEXITCODE
if ($null -eq $code) { $code = 2 }

if ($code -ne 0) {
    $verdict = (Select-String -Path $Log -Pattern "WITNESS-DIVERGENT|LAUNDERING|WITNESS: cannot verify|SCOPE" | Select-Object -Last 1).Line
    if (-not $verdict) { $verdict = "verdict line not found, exit $code" }
    $alert = @"

---

### Tip witness fired ($Stamp)

- verdict: $verdict (exit $code)
- log: `logs/tip_witness.log`
- response (exit 1, DIVERGENT): chain rewrite alarm. Do NOT re-publish; audit with `main.py verkle-audit --dry` + the gist revision history. The witness never moves backward or sideways.
- response (exit 2, cannot verify): no token / network / gist-scope denial (PAT needs Gists: Read and write). The witness surface is dark until the credential is fixed.
"@
    Add-Content -Path (Join-Path $Root "memory\attention.md") -Value $alert -Encoding utf8
    Write-Log "ALERT appended to memory/attention.md"
}

Write-Log "END exit=$code"
exit $code
