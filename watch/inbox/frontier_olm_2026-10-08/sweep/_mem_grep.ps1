$ErrorActionPreference = 'SilentlyContinue'
$scopes = @('memory\rib', 'memory\lenses', 'memory\press', 'memory\improve', 'watch\inbox\frontier_olm_2026-10-06', 'watch\inbox\frontier_olm_2026-10-07', 'watch\inbox\frontier_olm_2026-10-08', 'watch\inbox\frontier_olm_2026-10-05')
$pats = @('Escalation Signals', '2610.07354', '0.871', 'Pinned and Still Unstable', '2609.33044', 'Unanimously Wrong', 'ProbeGuard', '2610.07570', 'Conditional Accuracy Profiles', '2610.09229', 'semantic entropy', 'Uncheatable', 'Pair Difficulty', 'Maat')
foreach ($p in $pats) {
  foreach ($s in $scopes) {
    $hits = Get-ChildItem -Path $s -Recurse -File -Include *.md,*.json,*.jsonl,*.txt | Select-String -Pattern $p -SimpleMatch
    foreach ($h in ($hits | Select-Object -First 4)) {
      Write-Output ("HIT|" + $p + "|" + $h.Path + "|L" + $h.LineNumber)
    }
  }
}
Write-Output 'DONE'
