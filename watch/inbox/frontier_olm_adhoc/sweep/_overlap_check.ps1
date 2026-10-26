$ErrorActionPreference = 'SilentlyContinue'
$root = 'C:\Users\foste\Documents\projects\local_sovereign_agent'
$patterns = @(
  'MINDSET', 'DAEDALUS', 'GraphMemory', 'Selective Forgetting',
  'Relevance Is Not Sufficiency', 'Memento 3', 'Memento',
  'hybrid graph storage', 'GRAFT', 'MemCodex', 'TAGGRAPH', 'EMIR2', 'mem0',
  'Agent Zero Memory', 'QGMem', 'ReFold', 'MemTrial', 'SkillForge',
  'StateWise', 'PACMI', 'AECG', 'MemFit', 'PrisMem', 'MemPilot',
  'DyadMem', 'Whose Memory Is It', 'LongMemEval', 'event-centric memory',
  'schema evolution', 'property graph'
)
$catalogFile = Join-Path $root 'catalog\catalog.jsonl'
$memFiles = Get-ChildItem -Path (Join-Path $root 'memory') -Recurse -File -Include *.md,*.jsonl,*.json,*.txt
foreach ($p in $patterns) {
  $cat = Select-String -Path $catalogFile -Pattern $p -SimpleMatch
  $catN = ($cat | Measure-Object).Count
  $mem = $memFiles | Select-String -Pattern $p -SimpleMatch
  $memN = ($mem | Measure-Object).Count
  $firstPaths = ''
  if ($catN -gt 0) { $firstPaths = ($cat | Select-Object -First 1).Path }
  if ($memN -gt 0) { $mp = ($mem | Select-Object -First 2 | ForEach-Object { $_.Path }) -join ';'; $firstPaths = $firstPaths + ' | MEM: ' + $mp }
  Write-Output ("PAT: {0} | catalog={1} | memory={2} | {3}" -f $p, $catN, $memN, $firstPaths)
}
Write-Output 'DONE'
