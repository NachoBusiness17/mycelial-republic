$ErrorActionPreference = 'Continue'
$work = 'C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_2026-10-03\sweep'
$pattern = 'kv.?cache|kvarn|prefix cach|prompt lookup|context rot|lost in the middle|long context|context window|context length|context degrad|eviction|streamingllm|attention sink|snapkv|h2o|tool call|agent loop|memory system|compress|elid|summariz|context pack|retrieval|rag'
foreach ($sub in @('LocalLLaMA','MachineLearning','LocalLLM','ollama')) {
  $file = Join-Path $work ("arctic_" + $sub + ".json")
  if (-not (Test-Path $file)) { continue }
  $posts = Get-Content $file -Raw -Encoding UTF8 | ConvertFrom-Json
  Write-Output ("########## {0} : {1} posts loaded" -f $sub, $posts.Count)
  foreach ($p in $posts) {
    $hay = ($p.title + ' ' + $p.selftext)
    if ($hay -match $pattern) {
      $d = [DateTimeOffset]::FromUnixTimeSeconds([long]$p.created_utc).UtcDateTime.ToString('yyyy-MM-dd')
      $t = ($p.title -replace "\r?\n",' ')
      $snip = ''
      if ($p.selftext) {
        $snip = $p.selftext -replace "\r?\n",' '
        if ($snip.Length -gt 180) { $snip = $snip.Substring(0,180) }
      }
      Write-Output ("{0} | {1} | {2}c | {3} | [{4}]" -f $p.score, $d, $p.num_comments, $t, $p.id)
      if ($snip -ne '') { Write-Output ("      SNIP: {0}" -f $snip) }
    }
  }
}
