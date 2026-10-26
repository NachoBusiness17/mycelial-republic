# steer_field_daily.ps1 - MagSteerFieldDaily action script (08:40 daily)
# Feeds the film: runs watch/steer_field/build.py, which reads real fleet
# state (watch/bay/state, watch/bay_share.jsonl, queue/steer_agent.md) and
# writes dashboard/static/steer_field/FIELD.json (served) + watch/steer_field/
# FIELD.json + TAILS.md. Registered by register_steer_field_task.ps1.
# Receipt: watch/inbox/VISLAB_REPRESENTATIVE_20261018.md

$repo = Split-Path -Parent $PSScriptRoot
$py = Join-Path $repo '.venv\Scripts\python.exe'
$log = Join-Path $repo 'logs\steer_field.log'
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $log) | Out-Null

"=== steer_field feed $(Get-Date -Format o) ===" | Add-Content -Path $log
& $py (Join-Path $repo 'watch\steer_field\build.py') 2>&1 | Add-Content -Path $log
"exit=$LASTEXITCODE" | Add-Content -Path $log
exit $LASTEXITCODE
