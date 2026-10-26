$hits = Select-String -Path 'watch/inbox/frontier_olm_2026-10-08/sweep/*.md' -Pattern '2603.23420','EdgeBench','Artificial Analysis','14.19','MossAI','Blackwellboy','no_stp_on_snek','EBorgnia','Relace','Waselnuk','Karpathy','GLM 5.3 Flash' -SimpleMatch
foreach ($h in $hits) {
  Write-Output ($h.Filename + ':' + $h.LineNumber + ': ' + $h.Line.Substring(0, [Math]::Min(150, $h.Line.Length)))
}
if (-not $hits) { Write-Output 'NO HITS IN TODAY SIBLINGS' }
