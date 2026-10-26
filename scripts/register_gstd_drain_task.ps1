# Registers MagGstdDrainDaily - the standing GSTD earn loop (foundation 2).
# Daily at 08:00 local. Runs the drain with the greed law; self-heals the
# master when the excess-return mechanism walks it below the floor.
$taskName = "MagGstdDrainDaily"
$scriptPath = "C:\Users\foste\Documents\projects\local_sovereign_agent\scripts\gstd_drain_daily.ps1"
$workDir = "C:\Users\foste\Documents\projects\local_sovereign_agent"

$action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`"" `
    -WorkingDirectory $workDir
$trigger = New-ScheduledTaskTrigger -Daily -At "08:00"
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopIfGoingOnBatteries -AllowStartIfOnBatteries
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger `
    -Settings $settings -Principal $principal -Force | Out-Null
Write-Host "Registered $taskName (daily 08:00). Test run:"
Start-ScheduledTask -TaskName $taskName
Start-Sleep -Seconds 5
Get-ScheduledTask -TaskName $taskName | Select-Object TaskName, State
