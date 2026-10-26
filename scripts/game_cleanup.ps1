# game_cleanup.ps1 - kill the churners: llama-server + parent, LM Studio, headless chrome fleet
$p = Get-CimInstance Win32_Process -Filter "ProcessId=58164" -ErrorAction SilentlyContinue
if ($p) {
  Write-Output ("llama-server parent: " + $p.ParentProcessId)
  $par = Get-CimInstance Win32_Process -Filter "ProcessId=$($p.ParentProcessId)" -ErrorAction SilentlyContinue
  if ($par) { Write-Output ("parent: " + $par.Name + " -> killing"); Stop-Process -Id $par.ParentProcessId -Force -ErrorAction SilentlyContinue }
  Stop-Process -Id 58164 -Force -ErrorAction SilentlyContinue
}
Get-Process | Where-Object { $_.Name -match "ollama|llama" } | ForEach-Object {
  Write-Output ("killing: " + $_.Name + " " + $_.Id)
  Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
}
Get-Process | Where-Object { $_.Name -match "LM Studio" } | ForEach-Object {
  Write-Output ("killing LM Studio: " + $_.Id)
  Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
}
$chrome = Get-CimInstance Win32_Process -Filter "Name='chrome.exe'" | Where-Object { $_.CommandLine -match "headless|scrum_profiles|remote-debugging-port" }
Write-Output ("headless chrome fleet: " + ($chrome | Measure-Object).Count)
$chrome | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
Start-Sleep 2
$lo = Get-Process | Where-Object { $_.Name -match "ollama|llama" }
$lc = Get-CimInstance Win32_Process -Filter "Name='chrome.exe'" | Where-Object { $_.CommandLine -match "headless|scrum_profiles" }
Write-Output ("remaining ollama/llama: " + ($lo | Measure-Object).Count + " | remaining headless chrome: " + ($lc | Measure-Object).Count)
