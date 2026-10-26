$root = 'C:\Users\foste\Documents\projects\local_sovereign_agent'
$cat = Join-Path $root 'catalog\catalog.jsonl'
if (Test-Path $cat) {
  Write-Output ('CATALOG EXISTS bytes=' + (Get-Item $cat).Length)
} else {
  Write-Output 'CATALOG MISSING'
  exit 1
}
$pats = @('Auto-autoresearch','NanoChat','rekursiv','danluu','Benchmarking Local LLM Servers','inspect.aisi','AI Security Institute','Qwen3.5-4B','duane.sh','Terminal-Bench','DeepSWE','SWE-Bench Pro','sgaud.com','JevBench','Swesweep','Magnitude','Doyouok')
foreach ($p in $pats) {
  $m = Get-ChildItem -Path $cat, (Join-Path $root 'memory') -Recurse -File -ErrorAction SilentlyContinue |
       Select-String -Pattern $p -SimpleMatch -List -ErrorAction SilentlyContinue
  if ($m) {
    Write-Output ('HIT: ' + $p)
    $m | ForEach-Object { Write-Output ('  ' + $_.Path + ':' + $_.LineNumber) }
  } else {
    Write-Output ('MISS: ' + $p)
  }
}
