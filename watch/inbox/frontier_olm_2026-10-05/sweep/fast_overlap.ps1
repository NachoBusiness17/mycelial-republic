$ErrorActionPreference = 'SilentlyContinue'
$root = 'C:\Users\foste\Documents\projects\local_sovereign_agent'
$enc = [System.Text.Encoding]::Latin1
$patterns = @(
  'Auto-autoresearch','rekursiv','NanoChat','danluu','Senior SWE-Bench',
  'Benchmarking Local LLM Servers','inspect.aisi','AI Security Institute',
  'Qwen3.5-4B','duane.sh','Terminal-Bench','DeepSWE','SWE-Bench Pro',
  'sgaud.com','JevBench','Swesweep','Magnitude','Doyouok','doyouok',
  'hillclimbing','deepsense','Re-Earn','dead man','heartbeat'
)
# One pass over catalog.jsonl
$catPath = Join-Path $root 'catalog\catalog.jsonl'
$catText = $enc.GetString([System.IO.File]::ReadAllBytes($catPath))
foreach ($p in $patterns) {
  $idx = $catText.IndexOf($p, [System.StringComparison]::OrdinalIgnoreCase)
  if ($idx -ge 0) {
    $start = [Math]::Max(0, $idx - 120)
    $len = [Math]::Min(300, $catText.Length - $start)
    Write-Output ('CAT-HIT [' + $p + '] @' + $idx + ': ' + ($catText.Substring($start, $len) -replace '\s+', ' '))
  } else {
    Write-Output ('CAT-MISS [' + $p + ']')
  }
}
Write-Output '=== MEMORY TREE ==='
# One pass over every file under memory/
$files = Get-ChildItem -Path (Join-Path $root 'memory') -Recurse -File
Write-Output ('memory files: ' + $files.Count)
foreach ($f in $files) {
  if ($f.Length -gt 400MB) { Write-Output ('SKIP TOO BIG: ' + $f.FullName); continue }
  $txt = $enc.GetString([System.IO.File]::ReadAllBytes($f.FullName))
  $lineNo = 1
  foreach ($p in $patterns) {
    $idx = $txt.IndexOf($p, [System.StringComparison]::OrdinalIgnoreCase)
    if ($idx -ge 0) {
      $line = ($txt.Substring(0, $idx) -split "`n").Count
      $start = [Math]::Max(0, $idx - 100)
      $len = [Math]::Min(260, $txt.Length - $start)
      Write-Output ('MEM-HIT [' + $p + '] ' + $f.FullName + ':' + $line + ': ' + ($txt.Substring($start, $len) -replace '\s+', ' '))
    }
  }
}
Write-Output 'DONE'
