# register_probe_task.ps1 - registers MagProbeCadence (every 10 min, hidden launcher
# per the no-headed-surface law; operator act to remove: schtasks /Delete /TN MagProbeCadence /F)
$action = "wscript.exe //B //Nologo C:\Users\foste\Documents\projects\local_sovereign_agent\scripts\run_hidden.vbs powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\foste\Documents\projects\local_sovereign_agent\scripts\probe_cadence.ps1"
schtasks /Create /TN "MagProbeCadence" /SC MINUTE /MO 10 /TR "$action" /F
schtasks /Query /TN "MagProbeCadence" /FO LIST
