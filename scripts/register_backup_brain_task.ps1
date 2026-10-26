# register_backup_brain_task.ps1 - registers MagBackupBrainDaily (08:55 daily)
# The April loop, drilled daily: inventory + severed + reconnect.
# Receipt: watch/inbox/BACKUP_BRAIN_ORCHESTRATION_20261018.md

$action = New-ScheduledTaskAction -Execute 'powershell.exe' `
  -Argument '-NoProfile -ExecutionPolicy Bypass -File "C:\Users\foste\Documents\projects\local_sovereign_agent\scripts\backup_brain_daily.ps1"'
$trigger = New-ScheduledTaskTrigger -Daily -At 08:55
Register-ScheduledTask -TaskName 'MagBackupBrainDaily' -Action $action -Trigger $trigger -Force
Write-Host 'MagBackupBrainDaily registered (08:55 daily).'
