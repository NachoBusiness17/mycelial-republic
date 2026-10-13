# MagHermesBurn247 driver: headless Hermes burn on the standing queue.
# Operator order 2026-10-06: drive Hermes headless on the funded accounts 24/7
# ("why arent you driving hermes headless on free lanes 24/7?" + "we have 2
# hermes accounts too"). The carrier (tools/hermes_burn.py) owns the law:
# claritas face, O_EXCL ask claims, REFUSED terminal markers, usage banking to
# memory/runs/hermes_burn/usage.jsonl, key_2-first with key_1 fallback.
# This script only adds the clock and the alert leg (the MagFtsIndexDaily
# pattern): hourly fire, append-only log, attention.md row on nonzero exit.
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
$Py = Join-Path $Root ".venv\Scripts\python.exe"
$Carrier = Join-Path $Root "tools\hermes_burn.py"
$Queue = Join-Path $Root "queue\hermes_247"
$Log = Join-Path $Root "logs\hermes_burn_247.log"
$Stamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

if (-not (Test-Path (Split-Path $Log -Parent))) {
    New-Item -ItemType Directory -Path (Split-Path $Log -Parent) -Force | Out-Null
}
"[$Stamp] MagHermesBurn247 fire: $Queue" | Out-File -FilePath $Log -Append -Encoding utf8

& $Py $Carrier $Queue *>> $Log
$ExitCode = $LASTEXITCODE
"[$Stamp] exit $ExitCode" | Out-File -FilePath $Log -Append -Encoding utf8

if ($ExitCode -ne 0) {
    $Alert = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    "- $Alert MagHermesBurn247 exit $ExitCode - hermes burn failed, inspect logs/hermes_burn_247.log (two consecutive failures = both funded accounts hurt; check meter before refire)" |
        Out-File -FilePath (Join-Path $Root "memory\attention.md") -Append -Encoding utf8
}
exit $ExitCode
