$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
$work = 'C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_2026-10-03\sweep'
$ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
$subs = @('LocalLLaMA','MachineLearning','LocalLLM','ollama')
foreach ($sub in $subs) {
  $url = "https://old.reddit.com/r/$sub/top.json?t=month&limit=100"
  try {
    $resp = Invoke-WebRequest -Uri $url -UserAgent $ua -Headers @{ 'Accept' = 'application/json' } -TimeoutSec 40
    $file = Join-Path $work ("raw_" + $sub + ".json")
    [IO.File]::WriteAllBytes($file, $resp.RawContentStream.ToArray())
    $json = $resp.Content | ConvertFrom-Json
    $children = $json.data.children
    Write-Output ("=== SUBREDDIT {0} : HTTP {1} : {2} posts ===" -f $sub, $resp.StatusCode, $children.Count)
    foreach ($c in $children) {
      $d = $c.data
      $created = [DateTimeOffset]::FromUnixTimeSeconds([long]$d.created_utc).UtcDateTime.ToString('yyyy-MM-dd')
      Write-Output ("{0} | {1} | {2} | {3} | {4} | https://old.reddit.com{5}" -f $d.score, $created, $d.num_comments, $d.title, $d.id, $d.permalink)
    }
  } catch {
    Write-Output ("=== SUBREDDIT {0} : FAILED : {1} ===" -f $sub, $_.Exception.Message)
  }
  Start-Sleep -Milliseconds 1500
}
