$ErrorActionPreference = 'SilentlyContinue'
$pats = 'Strands Decider','decision model','Jev-style','systemone','Jeff-Code','rotational quantization','VeriLoop','borgcloud','Benchmarking Local LLM Servers','Qwen3.8','qwen2.5:7b','gemma:2b'
$files = Get-ChildItem -Recurse memory -Include *.md,*.json,*.jsonl -File | Where-Object { $_.FullName -notlike '*\biography\knots\*' }
foreach ($p in $pats) {
  $m = @($files | Select-String -SimpleMatch $p -ErrorAction SilentlyContinue)
  Write-Host ($p + ' => ' + $m.Count + ' hits')
  $m | Select-Object -First 3 | ForEach-Object {
    $rel = $_.Path.Substring((Get-Location).Path.Length + 1)
    Write-Host ('  ' + $rel + ':' + $_.LineNumber + ': ' + $_.Line.Substring(0, [Math]::Min(160, $_.Line.Length)))
  }
}
