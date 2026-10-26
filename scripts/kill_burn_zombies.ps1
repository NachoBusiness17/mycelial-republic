# kill_burn_zombies.ps1 - kill hermes_burn/checkpoint python stragglers left by ended tasks
Get-CimInstance Win32_Process -Filter "Name='python.exe'" |
  Where-Object { $_.CommandLine -match "hermes_burn|checkpoint|box_burn" } |
  ForEach-Object {
    Write-Output ("killing zombie python: " + $_.ProcessId + " " + $_.CommandLine.Substring(0, [Math]::Min(80, $_.CommandLine.Length)))
    Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
  }
Write-Output ("remaining matches: " + ((Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object { $_.CommandLine -match "hermes_burn|checkpoint|box_burn" } | Measure-Object).Count))
