$ErrorActionPreference = 'SilentlyContinue'
$root = 'C:\Users\foste\Documents\projects\local_sovereign_agent'
$pats = @('When LLM judges agree','Ising','Jev','TypeSafe','Swift-Qwen','tessl','2610.03448','unintended model actions','jev-effort','effort-router','Classic ML to Cope','benchmarking-ai-decision-models','Luna 6')
$files = @("$root\catalog\catalog.jsonl")
$files += (Get-ChildItem "$root\memory" -Recurse -File -Include *.md,*.json,*.jsonl | ForEach-Object { $_.FullName })
foreach ($p in $pats) {
  $hitfiles = $files | Select-String -SimpleMatch $p -List
  $names = ($hitfiles | ForEach-Object { Split-Path $_.Path -Leaf } | Select-Object -First 3) -join ','
  Write-Output ("{0} => {1} files [{2}]" -f $p, ($hitfiles | Measure-Object).Count, $names)
}
