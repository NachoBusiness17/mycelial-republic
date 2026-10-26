$ErrorActionPreference = 'SilentlyContinue'
$root = 'C:\Users\foste\Documents\projects\local_sovereign_agent'
$enc = [System.Text.Encoding]::Latin1
$patterns = @(
  'auto-autoresearch','rekursiv','NanoChat','danluu','Senior SWE-Bench',
  'Benchmarking Local LLM Servers','inspect.aisi','Qwen3.5-4B','duane.sh',
  'Terminal-Bench','DeepSWE','sgaud','JevBench','Swesweep','Magnitude',
  'doyouok','hillclimbing','deepsense','Re-Earn'
)
$files = Get-ChildItem -Path (Join-Path $root 'watch\inbox') -Recurse -File -Include *.md,*.txt,*.json
Write-Output ('inbox files scanned: ' + $files.Count)
foreach ($f in $files) {
  if ($f.Length -gt 50MB) { continue }
  $txt = $enc.GetString([System.IO.File]::ReadAllBytes($f.FullName))
  foreach ($p in $patterns) {
    $idx = $txt.IndexOf($p, [System.StringComparison]::OrdinalIgnoreCase)
    if ($idx -ge 0) {
      $line = ($txt.Substring(0, $idx) -split "`n").Count
      $start = [Math]::Max(0, $idx - 100)
      $len = [Math]::Min(260, $txt.Length - $start)
      Write-Output ('INBOX-HIT [' + $p + '] ' + $f.FullName + ':' + $line + ': ' + ($txt.Substring($start, $len) -replace '\s+', ' '))
    }
  }
}
Write-Output 'DONE'
