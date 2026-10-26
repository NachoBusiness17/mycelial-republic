# backup_brain_daily.ps1 - MagBackupBrainDaily action script (08:55 daily)
# Proves the April loop: runs the inventory audit + both drills (severed =
# blackout half local-only; reconnect = resync surfaces fresh) and logs one
# line per drill. Never mutates live estate state. Registered by
# register_backup_brain_task.ps1. Receipt:
# watch/inbox/BACKUP_BRAIN_ORCHESTRATION_20261018.md

$repo = Split-Path -Parent $PSScriptRoot
$py = Join-Path $repo '.venv\Scripts\python.exe'
$log = Join-Path $repo 'logs\backup_brain.log'
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $log) | Out-Null

"=== backup brain drill $(Get-Date -Format o) ===" | Add-Content -Path $log
& $py (Join-Path $repo 'tools\backup_brain.py') drill --severed --reconnect 2>&1 | Add-Content -Path $log
"exit=$LASTEXITCODE" | Add-Content -Path $log
exit $LASTEXITCODE
