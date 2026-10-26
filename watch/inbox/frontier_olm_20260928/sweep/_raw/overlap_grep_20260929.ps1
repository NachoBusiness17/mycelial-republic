$roots = @(
  'C:\Users\foste\Documents\projects\local_sovereign_agent\catalog\catalog.jsonl',
  'C:\Users\foste\Documents\projects\local_sovereign_agent\memory',
  'C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_20260928'
)
$pats = @(
  'Which Self-Improvements Should We Trust',
  'Risk-controlled Evaluation Under Sequential',
  'Recursive self-improvement of AI research agents',
  'Unearned Passes',
  'SEABench',
  'Endogenous Misalignment',
  'Reward Hacking Challenges Oversight',
  'Improvement Fidelity',
  'When Better Gets Worse',
  'RegenHarness',
  'Population Physics',
  'emergence A/B'
)
foreach ($root in $roots) {
  if (Test-Path $root -PathType Leaf) { $files = @($root) }
  else { $files = @(Get-ChildItem $root -Recurse -File -ErrorAction SilentlyContinue) }
  foreach ($pat in $pats) {
    $hits = @($files | Select-String -SimpleMatch -Pattern $pat -ErrorAction SilentlyContinue | Select-Object -First 3)
    if ($hits.Count -gt 0) {
      Write-Output ('HIT [' + $pat + '] @ ' + $root + ' -> ' + (($hits | ForEach-Object { $_.Path + ':' + $_.LineNumber }) -join '; '))
    }
  }
}
Write-Output 'GREP-DONE'
