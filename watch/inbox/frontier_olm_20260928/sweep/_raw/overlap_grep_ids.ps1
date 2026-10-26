$ids = @('2609.33180','2609.26457','2609.32677','2609.27612','2609.35596','2609.34262','2609.28614','2609.33871')
$targets = @(
  'C:\Users\foste\Documents\projects\local_sovereign_agent\catalog\catalog.jsonl',
  'C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_20260928\percolator_candidates.jsonl',
  'C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_20260928\register.jsonl'
)
foreach ($t in $targets) {
  foreach ($id in $ids) {
    $hits = @(Select-String -SimpleMatch -Pattern $id -Path $t -ErrorAction SilentlyContinue | Select-Object -First 2)
    if ($hits.Count -gt 0) {
      Write-Output ('IDHIT [' + $id + '] @ ' + $t + ' line ' + (($hits | ForEach-Object { $_.LineNumber }) -join ','))
    }
  }
}
$arxivdir = 'C:\Users\foste\Documents\projects\local_sovereign_agent\state\arxiv'
if (Test-Path $arxivdir) {
  $found = @(Get-ChildItem $arxivdir -Recurse -File -ErrorAction SilentlyContinue | Where-Object { $n = $_.Name; ($ids | Where-Object { $n -like ('*' + $_ + '*') }).Count -gt 0 })
  foreach ($f in $found) { Write-Output ('IDFILE ' + $f.FullName) }
} else { Write-Output 'NO state/arxiv DIR' }
Write-Output 'ID-GREP-DONE'
