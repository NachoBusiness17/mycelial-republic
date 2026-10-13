# MagBoxBurnNightly driver: the box-burn load curve watcher (tools/box_burn_watch.py).
# Wiring landed 2026-10-07 (queue/todo.md Stone 7 sub-item 3 rewrite, m2-todo-truths
# lane): the watcher's only prior sample window was the one-shot 09-25/09-26 night
# run and state/fuel/box_burn_watch.jsonl went dark at 2026-09-26T10:59:18Z because
# nothing owned its clock; the planned "nightly burn driver on grounding_chain"
# routing is dead too (watch/inbox/union_fullsend_20260917/grounding_chain.jsonl
# last row 2026-09-26T13:13:30Z, no scheduled trigger). This task IS the nightly
# trigger for the watcher half: fire at 22:00, the carrier self-stops at 07:00
# (the family-box law is inside the tool), rows append to
# state/fuel/box_burn_watch.jsonl. Still open (the job-firing half of sub-item 3):
# read backlogs (pile, briefs, whisper, training) -> fire top-N local jobs to a
# target utilization. This script only owns the measurement clock (MagFtsIndexDaily
# pattern: append-only log, attention.md row on nonzero exit).
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
$Py = Join-Path $Root ".venv\Scripts\python.exe"
$Carrier = Join-Path $Root "tools\box_burn_watch.py"
$Log = Join-Path $Root "logs\box_burn_nightly.log"
$Stamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

if (-not (Test-Path (Split-Path $Log -Parent))) {
    New-Item -ItemType Directory -Path (Split-Path $Log -Parent) -Force | Out-Null
}
"[$Stamp] MagBoxBurnNightly fire: $Carrier" | Out-File -FilePath $Log -Append -Encoding utf8

& $Py $Carrier --stop 07:00 --every 55 *>> $Log
$ExitCode = $LASTEXITCODE
"[$Stamp] exit $ExitCode" | Out-File -FilePath $Log -Append -Encoding utf8

if ($ExitCode -ne 0) {
    $Alert = Join-Path $Root "memory\attention.md"
    "[$Stamp] MagBoxBurnNightly exit $ExitCode - box burn watcher died mid-window; check logs/box_burn_nightly.log" | Out-File -FilePath $Alert -Append -Encoding utf8
}
exit $ExitCode
