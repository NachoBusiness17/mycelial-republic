# DRAFT - operator runs once. Hourly at :35 (clear of sweeper fires at :x9 and
# the checkpoint/hourly slots). Hidden launch per the no-headed-surface law.
$repo = "C:\Users\foste\Documents\projects\local_sovereign_agent"
$action = New-ScheduledTaskAction -Execute "C:\Windows\System32\wscript.exe" `
  -Argument "//B //Nologo `"$repo\scripts\run_hidden.vbs`" `"$repo\.venv\Scripts\pythonw.exe`" -m tools.breath_replay_check" `
  -WorkingDirectory $repo
$trigger = New-ScheduledTaskTrigger -Once -At ((Get-Date).Date.AddMinutes(35)) -RepetitionInterval (New-TimeSpan -Hours 1)
$settings = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes 30) -StartWhenAvailable
Register-ScheduledTask -TaskName "MagBreathReplayHourly" -Action $action -Trigger $trigger -Settings $settings `
  -Description "Read-only replay check of the breath chain (no git writes); appends logs/breath_replay_check.jsonl."
# Undo: Unregister-ScheduledTask -TaskName MagBreathReplayHourly -Confirm:$false
