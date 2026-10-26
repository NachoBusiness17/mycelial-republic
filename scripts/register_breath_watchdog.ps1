# DRAFT - run ONCE, by the operator, to register MagBreathWatchdog (every 5 min).
# Hidden via run_hidden.vbs + pythonw (the no-headed-surface law; cf. the
# MagCheckpointV2Hourly focus-steal incident 2026-10-19). Not run by any seat.
$repo = "C:\Users\foste\Documents\projects\local_sovereign_agent"
$action = New-ScheduledTaskAction -Execute "C:\Windows\System32\wscript.exe" `
  -Argument "//B //Nologo `"$repo\scripts\run_hidden.vbs`" `"$repo\.venv\Scripts\pythonw.exe`" -m tools.breath_watchdog" `
  -WorkingDirectory $repo
# Offset 3 min from MagCommitSweeper's :x9 fires so the check never races a sweep start.
$start = (Get-Date).Date.AddMinutes(2)
$trigger = New-ScheduledTaskTrigger -Once -At $start -RepetitionInterval (New-TimeSpan -Minutes 5)
$settings = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes 2) `
  -StartWhenAvailable -DontStopIfGoingOnBatteries -AllowStartIfOnBatteries
Register-ScheduledTask -TaskName "MagBreathWatchdog" -Action $action -Trigger $trigger -Settings $settings `
  -Description "Files a fleet NOTICE (lane_down) when the newest commit-sweeper breath is >15 min old; cancels on recovery."
# Undo: Unregister-ScheduledTask -TaskName MagBreathWatchdog -Confirm:$false
