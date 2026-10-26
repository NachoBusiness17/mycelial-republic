$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
$work = 'C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_2026-10-03\sweep'
$ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
$ids = @('1wv09ja','1wpodl1','1wt03zh')
foreach ($id in $ids) {
  try {
    $p = (Invoke-WebRequest -Uri "https://arctic-shift.photon-reddit.com/api/posts/ids?ids=$id" -UserAgent $ua -TimeoutSec 40).Content | ConvertFrom-Json
    $post = $p.data[0]
  } catch {
    Write-Output ("THREAD {0} : POST FETCH FAILED : {1}" -f $id, $_.Exception.Message)
    continue
  }
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
  $cc = 0
  if ($comments) { $cc = $comments.Count }
  Write-Output ("SAVED thread_{0}.json : {1} | score {2} | {3} comments | selftext len {4}" -f $id, $post.title, $post.score, $cc, ($post.selftext | ForEach-Object { $_.Length }))
  Start-Sleep -Milliseconds 1200
}
