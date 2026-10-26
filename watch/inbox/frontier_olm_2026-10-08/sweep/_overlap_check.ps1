$ErrorActionPreference = 'SilentlyContinue'
$pats = @('Escalation Signals','2610.07354','0.871','semantic entropy','semantic-entropy','AutoDataBench','Uncheatable Eval','Unanimously Wrong','Pair Difficulty','Conditional Accuracy','Within-Judge','2609.33044','2609.35025','2610.07570','2609.27510','Cheap Verifier','Maat','Codoku','Five Ways to Fool','escalation signal')
foreach ($p in $pats) {
  $c = (Select-String -Path 'catalog\catalog.jsonl' -Pattern $p -SimpleMatch | Measure-Object).Count
  $m = (Get-ChildItem -Path 'memory' -Recurse -File -Include *.md,*.json,*.jsonl | Select-String -Pattern $p -SimpleMatch | Measure-Object).Count
  $w = (Get-ChildItem -Path 'watch\inbox' -Recurse -File -Include *.md,*.json,*.jsonl | Select-String -Pattern $p -SimpleMatch | Measure-Object).Count
  Write-Output ("PAT|$p|catalog=$c|memory=$m|watch=$w")
}
