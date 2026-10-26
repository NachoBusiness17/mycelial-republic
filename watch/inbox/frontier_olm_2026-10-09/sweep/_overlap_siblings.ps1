$ErrorActionPreference = 'SilentlyContinue'
$dirs = 'watch/inbox/frontier_olm_2026-10-05','watch/inbox/frontier_olm_2026-10-06','watch/inbox/frontier_olm_2026-10-07','watch/inbox/frontier_olm_2026-10-08','watch/inbox/frontier_olm_2026-09-30','watch/inbox/frontier_olm_2026-10-01','watch/inbox/frontier_olm_2026-10-02','watch/inbox/frontier_olm_2026-10-03','watch/inbox/frontier_olm_2026-10-04'
$pats = 'weaviate','rotational','RaBitQ','veriloop','borgcloud','SoTA Feed','mozilla','gutsy','Mistral Large 4','Le Chonk','jev-decision-index','Decision Index'
foreach ($d in $dirs) {
  $files = Get-ChildItem -Recurse $d -Include *.md -File
  foreach ($p in $pats) {
    $m = @($files | Select-String -SimpleMatch $p -ErrorAction SilentlyContinue)
    if ($m.Count -gt 0) {
      foreach ($hit in ($m | Select-Object -First 2)) {
        $rel = $hit.Path.Substring((Get-Location).Path.Length + 1)
        Write-Host ($rel + ':' + $hit.LineNumber + ' [' + $p + ']: ' + $hit.Line.Substring(0, [Math]::Min(140, $hit.Line.Length)))
      }
    }
  }
}
