$regex = 'Which Self-Improvements Should We Trust|Risk-controlled Evaluation Under Sequential|Improvement Fidelity|When Better Gets Worse|RegenHarness|Population Physics|emergence A/B|Unearned Passes|SEABench|Endogenous Misalignment|Recursive self-improvement of AI research agents'
$roots = @(
  'C:\Users\foste\Documents\projects\local_sovereign_agent\memory',
  'C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_20260928'
)
foreach ($root in $roots) {
  $files = Get-ChildItem $root -Recurse -File -ErrorAction SilentlyContinue
  foreach ($f in $files) {
    $hits = @(Select-String -Path $f.FullName -Pattern $regex -ErrorAction SilentlyContinue)
    if ($hits.Count -gt 0) {
      foreach ($h in ($hits | Select-Object -First 2)) {
        Write-Output ('FINALHIT @ ' + $f.FullName + ':' + $h.LineNumber + ' [' + $h.Matches[0].Value + ']')
      }
    }
  }
}
Write-Output 'FINAL-GREP-DONE'
