# MagGauntletFree30 driver: the cheap-seat gauntlet on the free-lane fleet.
# Operator order 2026-10-06: "drive the cheap seats like they're the expensive
# ones and learn the difference" - falsifier trials (dice-law honesty, kung-fu
# beat-grid alignment, dungeon metagame compliance, consensus triplets) staged
# into watch/inbox/free_lane_queue/ and drained by the MagFreeLaneFleet 24/7
# clock across all free providers + the local Ollama garden. This script adds
# the cadence and the register: grade what landed, stage the next batch.
# Fires at :15/:45, offset from the fleet's :03/:33 so grading sees the drain.
# LONGRUNNER POLICY R2 (configs/longrunner_policy.json, 2026-10-07): the clock
# stays host-side, the WORK runs inside the burners cage (docker-compose.yml
# service `burners`: cpus 2.0, mem 2g, pids 64, cap_drop ALL). Single path by
# design - no host-python fallback branch (a fallback recreates the
# bare-longrunner class the policy exists to kill). If Docker Desktop is down
# the docker error lands in this log and the patrol sees it.
# -T --interactive=false (2026-10-07 first live fire): compose run defaults to
# keeping STDIN open, and the Task Scheduler context has no usable stdin - the
# 02:42:43Z fire wedged 10+ minutes in the compose plugin before any container
# existed (killed tree: wscript 28020 -> powershell 26412 -> docker 27100 ->
# docker-compose 25648). Both flags strip the TTY/stdin attach a batch
# one-shot never needed.
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
$Compose = Join-Path $Root "docker-compose.yml"
$Log = Join-Path $Root "logs\gauntlet_free.log"
$Stamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

if (-not (Test-Path (Split-Path $Log -Parent))) {
    New-Item -ItemType Directory -Path (Split-Path $Log -Parent) -Force | Out-Null
}
"[$Stamp] MagGauntletFree30 fire" | Out-File -FilePath $Log -Append -Encoding utf8

& docker compose -f $Compose run --rm -T --interactive=false --entrypoint python burners -m tools.gauntlet_grade 2>&1 | ForEach-Object { "$_" } |
    Out-File -FilePath $Log -Append -Encoding utf8
& docker compose -f $Compose run --rm -T --interactive=false --entrypoint python burners -m tools.gauntlet_feed 2>&1 | ForEach-Object { "$_" } |
    Out-File -FilePath $Log -Append -Encoding utf8

"[$Stamp] gauntlet cycle done (exit $LASTEXITCODE)" |
    Out-File -FilePath $Log -Append -Encoding utf8
exit 0
