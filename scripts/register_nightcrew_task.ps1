# Registers MagNightCrew: the standing headless DS-overflow drain (every 30 min).
# The cron that does not wait in windows or workflows (operator ask 2026-10-10).
# Law 11 check: this is NOT a supervisor - it is a one-shot drainer that exits;
# overlaps are made safe by nightcrew's claim-then-clear inbox protocol.
$ErrorActionPreference = "Stop"
$repo = "C:\Users\foste\Documents\projects\local_sovereign_agent"
$py = "$repo\.venv\Scripts\python.exe"
$act = New-ScheduledTaskAction -Execute $py -Argument "-m tools.nightcrew" -WorkingDirectory $repo
$trg = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(2) -RepetitionInterval (New-TimeSpan -Minutes 30)
$set = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 45)
Register-ScheduledTask -TaskName "MagNightCrew" -Action $act -Trigger $trg -Settings $set -Description "Standing DS overflow queue drain; receipts to queue/ds_overflow/DONE/" -Force
Write-Output "MagNightCrew registered: every 30 min, nightcrew.py drains queue/ds_overflow/INBOX.jsonl"
