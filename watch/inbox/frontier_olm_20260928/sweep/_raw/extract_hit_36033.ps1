$line = Get-Content 'C:\Users\foste\Documents\projects\local_sovereign_agent\memory\trajectory\steps.jsonl' -TotalCount 36033 | Select-Object -Last 1
Write-Output ('LEN=' + $line.Length)
$idx = $line.IndexOf('Which Self-Improvements')
if ($idx -lt 0) { $idx = $line.IndexOf('Risk-controlled Evaluation') }
if ($idx -ge 0) {
  $start = [Math]::Max(0, $idx - 400)
  $len = [Math]::Min(1000, $line.Length - $start)
  Write-Output $line.Substring($start, $len)
} else {
  Write-Output $line.Substring(0, [Math]::Min(800, $line.Length))
}
