$ErrorActionPreference = 'SilentlyContinue'
$pats = @('Waselnuk','getunblocked','Artificial Analysis','Coding Agent Index','Karpathy','EdgeBench','MossAI','tokens you will never see','Blackwellboy','not one number','no_stp_on_snek','preserve_thinking','GLM 5.3 Flash','GLM-5.3-Flash','Featherless','Relace','EBorgnia','loop engineering','cost per task','reasoning_effort','finish_reason')
foreach ($p in $pats) {
  $cat = Select-String -Path 'catalog/catalog.jsonl' -Pattern $p -SimpleMatch
  $rib = Select-String -Path 'memory/rib/*' -Pattern $p -SimpleMatch
  $mem = Select-String -Path 'memory/burns/LEDGER.jsonl','memory/frontier/allowance.jsonl' -Pattern $p -SimpleMatch
  Write-Output ('PAT[' + $p + '] catalog=' + (@($cat).Count) + ' rib=' + (@($rib).Count) + ' burns/frontier=' + (@($mem).Count))
  foreach ($h in @($cat | Select-Object -First 2)) { Write-Output ('  CAT: ' + $h.Line.Substring(0, [Math]::Min(180, $h.Line.Length))) }
  foreach ($h in @($rib | Select-Object -First 3)) { Write-Output ('  RIB: ' + $h.Path + ':' + $h.LineNumber + ' :: ' + $h.Line.Substring(0, [Math]::Min(160, $h.Line.Length))) }
  foreach ($h in @($mem | Select-Object -First 2)) { Write-Output ('  LED: ' + $h.Line.Substring(0, [Math]::Min(160, $h.Line.Length))) }
}
