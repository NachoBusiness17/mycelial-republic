$ErrorActionPreference = 'SilentlyContinue'
$pats = @('Escalation Signals','0.871','AutoDataBench','Uncheatable','Unanimously Wrong','Pair Difficulty','Conditional Accuracy','Within-Judge','2609.33044','2609.35025','2610.07570','2609.27510','Cheap Verifier','semantic entropy','Five Ways to Fool')
foreach ($p in $pats) {
  $hits = Select-String -Path 'catalog\catalog.jsonl' -Pattern $p -SimpleMatch
  $n = ($hits | Measure-Object).Count
  Write-Output ("CAT|$p|$n")
  if ($n -gt 0) { $hits | Select-Object -First 3 | ForEach-Object { Write-Output ("  L" + $_.LineNumber + ": " + $_.Line.Substring(0, [Math]::Min(200, $_.Line.Length))) } }
}
