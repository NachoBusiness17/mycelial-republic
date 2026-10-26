$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
$work = 'C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_2026-10-03\sweep'
$ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
$subs = @('LocalLLaMA','MachineLearning','LocalLLM','ollama')

foreach ($sub in $subs) {
  $all = New-Object System.Collections.Generic.List[object]
  $before = '2026-10-03T00:00:00'
  $pages = 0
  $failed = $false
  while ($pages -lt 12) {
    $url = "https://arctic-shift.photon-reddit.com/api/posts/search?subreddit=$sub&before=$before&limit=100&sort=desc"
    try {
      $resp = Invoke-WebRequest -Uri $url -UserAgent $ua -TimeoutSec 45
      $json = $resp.Content | ConvertFrom-Json
      $posts = $json.data
      if (-not $posts -or $posts.Count -eq 0) { break }
      foreach ($p in $posts) { $all.Add($p) }
      $oldest = $posts[$posts.Count-1].created_utc
      $before = ([DateTimeOffset]::FromUnixTimeSeconds([long]$oldest).UtcDateTime.AddSeconds(1)).ToString('yyyy-MM-ddTHH:mm:ss')
      $pages++
      $oldestDate = [DateTimeOffset]::FromUnixTimeSeconds([long]$oldest).UtcDateTime
      if ($oldestDate -lt [datetime]'2026-09-03') { break }
    } catch {
      Write-Output ("SUB {0} PAGE {1} FAILED : {2}" -f $sub, $pages, $_.Exception.Message)
      $failed = $true
      break
    }
    Start-Sleep -Milliseconds 1200
  }
  # keep only last 30 days, rank by score
  $cutoff = [DateTimeOffset]::new(2026,9,3,0,0,0,[TimeSpan]::Zero).ToUnixTimeSeconds()
  $ranked = $all | Where-Object { $_.created_utc -gt $cutoff } | Sort-Object -Property score -Descending
  $file = Join-Path $work ("arctic_" + $sub + ".json")
  $ranked | Select-Object id, title, score, num_comments, created_utc, permalink, selftext, link_flair_text | ConvertTo-Json -Depth 3 | Out-File -FilePath $file -Encoding utf8
  Write-Output ("=== SUBREDDIT {0} : fetched {1} posts ({2} pages{3}), in-window {4} ===" -f $sub, $all.Count, $pages, ($(if($failed){', failed'}else{''})), $ranked.Count)
  $i = 0
  foreach ($p in $ranked) {
    $i++
    if ($i -gt 40) { break }
    $d = [DateTimeOffset]::FromUnixTimeSeconds([long]$p.created_utc).UtcDateTime.ToString('yyyy-MM-dd')
    $t = $p.title -replace "`r?`n",' '
    Write-Output ("{0} | {1} | {2}c | {3} | https://old.reddit.com{4}" -f $p.score, $d, $p.num_comments, $t, $p.permalink)
  }
  Start-Sleep -Seconds 1
}
