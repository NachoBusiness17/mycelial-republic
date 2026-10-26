$ErrorActionPreference = 'SilentlyContinue'
$root = 'C:\Users\foste\Documents\projects\local_sovereign_agent'
$ids = @('1wms904','1wr5ylm','1wv09ja','1wv0b24','1w9myqc','1wnedrc','1wdc1jj','1wp5668','1wc6tka','1wpodl1','1wt03zh','1wu1ugy','1wujph3','1wtg12r','1wuhtn0','1wtyc4y','1wp5668')
$phrases = @('phantom-kv','prompt lookup','opencode-cache-compact','KV cache as an agent runtime','61 days of my own transcripts','-cram','KV cache transplant','Adaptive KV-Cache Streaming','doug.sh')
$targets = @(
  (Join-Path $root 'catalog\catalog.jsonl'),
  (Join-Path $root 'watch\inbox\frontier_olm_2026-10-02'),
  (Join-Path $root 'corpus\social_archive\reddit_20261001'),
  (Join-Path $root 'docs\report_v1\sources\receipts')
)
Write-Output '=== THREAD-ID GREP (catalog.jsonl + memory top-level hits) ==='
$cat = Join-Path $root 'catalog\catalog.jsonl'
foreach ($id in ($ids | Select-Object -Unique)) {
  $hits = Select-String -Path $cat -Pattern $id -SimpleMatch -ErrorAction SilentlyContinue
  if ($hits) {
    foreach ($h in $hits) {
      $line = $h.Line
      if ($line.Length -gt 220) { $line = $line.Substring(0,220) }
      Write-Output ("CATALOG-HIT {0} at line {1}: {2}" -f $id, $h.LineNumber, $line)
    }
  } else {
    Write-Output ("CATALOG-MISS {0}" -f $id)
  }
}
Write-Output ''
Write-Output '=== PHRASE GREP in 10-02 fold + social archive + receipts (recursive, file+line) ==='
foreach ($ph in $phrases) {
  foreach ($t in ($targets | Select-Object -Skip 1)) {
    if (Test-Path $t -PathType Container) {
      $hits = Get-ChildItem -Path $t -Recurse -File -ErrorAction SilentlyContinue | Select-String -Pattern $ph -SimpleMatch -List
      foreach ($h in $hits) {
        Write-Output ("HIT '{0}' in {1}" -f $ph, $h.Path)
      }
    }
  }
  $hits2 = Select-String -Path $cat -Pattern $ph -SimpleMatch -ErrorAction SilentlyContinue
  if ($hits2) {
    foreach ($h in $hits2) {
      $line = $h.Line
      if ($line.Length -gt 200) { $line = $line.Substring(0,200) }
      Write-Output ("CATALOG-PHRASE '{0}' line {1}: {2}" -f $ph, $h.LineNumber, $line)
    }
  }
}
Write-Output ''
Write-Output '=== MEMORY/ subtree grep for the six deep-read thread ids ==='
foreach ($id in @('1wms904','1wr5ylm','1wv09ja','1wv0b24','1w9myqc','1wnedrc','1wp5668','1wc6tka','1wt03zh','1wu1ugy')) {
  $hits = Get-ChildItem -Path (Join-Path $root 'memory') -Recurse -File -ErrorAction SilentlyContinue | Select-String -Pattern $id -SimpleMatch -List
  if ($hits) {
    foreach ($h in $hits) { Write-Output ("MEM-HIT {0} in {1}" -f $id, $h.Path) }
  } else {
    Write-Output ("MEM-MISS {0}" -f $id)
  }
}
Write-Output 'DONE'
