# register_steer_field_task.ps1 - registers MagSteerFieldDaily (08:40 daily)
# The cadence that keeps the vislab representative: the film is fed from real
# fleet state every morning; the exhibits fetch, they never fossilize.
# Receipt: watch/inbox/VISLAB_REPRESENTATIVE_20261018.md

$action = New-ScheduledTaskAction -Execute 'powershell.exe' `
  -Argument '-NoProfile -ExecutionPolicy Bypass -File "C:\Users\foste\Documents\projects\local_sovereign_agent\scripts\steer_field_daily.ps1"'
$trigger = New-ScheduledTaskTrigger -Daily -At 08:40
Register-ScheduledTask -TaskName 'MagSteerFieldDaily' -Action $action -Trigger $trigger -Force
Write-Host 'MagSteerFieldDaily registered (08:40 daily).'
