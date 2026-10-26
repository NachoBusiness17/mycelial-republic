$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
$work = 'C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_2026-10-03\sweep'
$ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
$ids = @('1wms904','1wr5ylm','1wv0b24','1w9myqc','1wnedrc','1wdc1jj','1wp5668','1wc6tka','1wvwdn1','1wu1ugy')

foreach ($id in $ids) {
  # post
  try {
    $p = (Invoke-WebRequest -Uri "https://arctic-shift.photon-reddit.com/api/posts/ids?ids=$id" -UserAgent $ua -TimeoutSec 40).Content | ConvertFrom-Json
    $post = $p.data[0]
  } catch {
    Write-Output ("THREAD {0} : POST FETCH FAILED : {1}" -f $id, $_.Exception.Message)
    continue
  }
  # comments
  $comments = $null
  try {
    $c = (Invoke-WebRequest -Uri "https://arctic-shift.photon-reddit.com/api/comments/search?link_id=$id&limit=100&sort=desc" -UserAgent $ua -TimeoutSec 40).Content | ConvertFrom-Json
    $comments = $c.data
  } catch {
    Write-Output ("THREAD {0} : COMMENT FETCH FAILED : {1}" -f $id, $_.Exception.Message)
  }
  $out = [ordered]@{
    id = $id
    subreddit = $post.subreddit
    title = $post.title
    author = $post.author
    score = $post.score
    num_comments = $post.num_comments
    created_utc = $post.created_utc
    permalink = ("https://old.reddit.com" + $post.permalink)
    selftext = $post.selftext
    url_out = $post.url
    comments = $comments
  }
  $file = Join-Path $work ("thread_" + $id + ".json")
  $out | ConvertTo-Json -Depth 4 | Out-File -FilePath $file -Encoding utf8
  $d = [DateTimeOffset]::FromUnixTimeSeconds([long]$post.created_utc).UtcDateTime.ToString('yyyy-MM-dd')
  $cc = 0
  $topScores = ''
  if ($comments) {
    $cc = $comments.Count
    $top = $comments | Sort-Object -Property score -Descending | Select-Object -First 5
    $topScores = (($top | ForEach-Object { [string]$_.score }) -join ',')
  }
  $st = ''
  if ($post.selftext) { $st = $post.selftext; if ($st.Length -gt 200) { $st = $st.Substring(0,200) } }
  $st = $st -replace "\r?\n",' '
  Write-Output ("THREAD {0} [{1}] {2} | {3} | score {4} | {5} comments fetched (top scores {6}) | out-url: {7}" -f $id, $post.subreddit, $d, $post.title, $post.score, $cc, $topScores, $post.url)
  Write-Output ("   SELFTEXT-HEAD: {0}" -f $st)
  Start-Sleep -Milliseconds 1200
}
