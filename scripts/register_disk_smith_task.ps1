# Registers MagDiskSmithDaily - the Smith chart of the HDD (disk-crisis-20261008).
# Daily 08:50, after the census patrol (08:30) and longrunner patrol (08:45).
# Reads only; appends logs/disk_smith.jsonl; alerts memory/attention.md on
# free-floor breach, vhdx bloat, or pagefile balloon; exit 1 on alert.
$repo = "C:\Users\foste\Documents\projects\local_sovereign_agent"
$action = New-ScheduledTaskAction -Execute "$repo\.venv\Scripts\python.exe" `
    -Argument "-m tools.disk_smith" -WorkingDirectory $repo
$trigger = New-ScheduledTaskTrigger -Daily -At 08:50
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 30)
Register-ScheduledTask -TaskName "MagDiskSmithDaily" -Action $action -Trigger $trigger `
    -Settings $settings -Description "Smith chart of the HDD: disk growth attribution across agent seats (disk-crisis-20261008)" -Force
Write-Output "MagDiskSmithDaily registered (08:50 daily)"
