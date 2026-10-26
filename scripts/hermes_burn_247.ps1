# MagHermesBurn247 driver: headless Hermes burn on the standing queue.
# Operator order 2026-10-06: drive Hermes headless on the funded accounts 24/7
# ("why arent you driving hermes headless on free lanes 24/7?" + "we have 2
# hermes accounts too"). REPOINT 2026-10-16 (operator: "i dont have any more
# money in hermes but you cna drive the free lanes and stealth models through
# it"): the Nous credits are gone; this task now drives the free-lane hosts
# (openrouter.ai) through the same carrier - the env vars below pick the host
# and allow unpriced :free SKUs. The carrier (tools/hermes_burn.py) owns the law:
# claritas face, O_EXCL ask claims, REFUSED terminal markers, usage banking to
# memory/runs/hermes_burn/usage.jsonl, key_2-first with key_1 fallback.
# This script only adds the clock and the alert leg (the MagFtsIndexDaily
# pattern): hourly fire, append-only log, attention.md row on nonzero exit.
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
$Py = Join-Path $Root ".venv\Scripts\python.exe"
$Carrier = Join-Path $Root "tools\hermes_burn.py"
# 2026-10-16 repoint: free-lane asks live in their own root; the Nous-era
# root (queue\hermes_247) stays archived with its landed/terminal states.
$Queue = Join-Path $Root "queue\hermes_247_free"
$Log = Join-Path $Root "logs\hermes_burn_247.log"
$Stamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

# 2026-10-16 repoint: free-lane endpoint (full URL - the /api prefix matters,
# see the carrier docstring) + unpriced-SKU pass (see header).
$env:HERMES_BURN_API_BASE = "https://openrouter.ai/api/v1/chat/completions"
$env:HERMES_BURN_UNPRICED_OK = "1"

if (-not (Test-Path (Split-Path $Log -Parent))) {
    New-Item -ItemType Directory -Path (Split-Path $Log -Parent) -Force | Out-Null
}
"[$Stamp] MagHermesBurn247 fire: $Queue" | Out-File -FilePath $Log -Append -Encoding utf8

# THE STANDING PIPELINE (2026-10-16, operator: "standing organs that execute
# everything we feed into it via rube goldberging at our triangulation"):
# leg 1 mints from the explore backlog, leg 2 fires the wide queue at width
# 3, leg 3 runs the miner queue. One clock, three organs, the whole chain.
$Wide = Join-Path $Root "queue\hermes_247_free_wide"
& $Py (Join-Path $Root "tools\ask_minter.py") --source explore --limit 40 --budget-today 900 *>> $Log
& $Py (Join-Path $Root "tools\batch_fire.py") --root $Wide --width 3 *>> $Log

& $Py $Carrier $Queue *>> $Log
$ExitCode = $LASTEXITCODE
"[$Stamp] exit $ExitCode" | Out-File -FilePath $Log -Append -Encoding utf8

if ($ExitCode -ne 0) {
    $Alert = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    "- $Alert MagHermesBurn247 exit $ExitCode - hermes burn failed, inspect logs/hermes_burn_247.log (two consecutive failures = the free-lane host or keys hurt; check the usage ledger before refire)" |
        Out-File -FilePath (Join-Path $Root "memory\attention.md") -Append -Encoding utf8
}
exit $ExitCode
