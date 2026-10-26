$pats = 'Strands Decider','decision model','Jev','systemone','System One','Jeff-Code','rotational quantization','RaBitQ','VeriLoop','borgcloud','Benchmarking Local LLM Servers','Qwen3.8','Gutsy','Clef','Mistral Large 4','SoTA Feed'
$c = Get-Content catalog\catalog.jsonl
foreach ($p in $pats) {
  $m = $c | Select-String -SimpleMatch $p
  Write-Host ($p + ' => ' + $m.Count + ' rows')
  if ($m.Count -gt 0) {
    $m | Select-Object -First 2 | ForEach-Object {
      Write-Host ('  L' + $_.LineNumber + ': ' + $_.Line.Substring(0, [Math]::Min(200, $_.Line.Length)))
    }
  }
}
