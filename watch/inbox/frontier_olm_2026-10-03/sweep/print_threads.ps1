param(
  [string]$Ids = '1wms904,1wp5668,1wnedrc,1wc6tka,1w9myqc,1wu1ugy,1wt03zh,1wv09ja',
  [int]$SelfCap = 2600,
  [int]$CommentCap = 480,
  [int]$TopComments = 8
)
$ErrorActionPreference = 'Continue'
$work = 'C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_2026-10-03\sweep'
foreach ($id in $Ids.Split(',')) {
  $file = Join-Path $work ("thread_" + $id + ".json")
  if (-not (Test-Path $file)) { Write-Output ("MISSING {0}" -f $id); continue }
  $j = Get-Content $file -Raw -Encoding UTF8 | ConvertFrom-Json
  $d = [DateTimeOffset]::FromUnixTimeSeconds([long]$j.created_utc).UtcDateTime.ToString('yyyy-MM-dd')
  Write-Output ("")
  Write-Output ("################ THREAD {0} | r/{1} | {2} | score {3} | author {4}" -f $id, $j.subreddit, $d, $j.score, $j.author)
  Write-Output ("TITLE: {0}" -f $j.title)
  Write-Output ("URL: {0}" -f $j.permalink)
  if ($j.url_out) { Write-Output ("LINKED-URL: {0}" -f $j.url_out) }
  $st = ''
  if ($j.selftext) { $st = $j.selftext }
  if ($st.Length -gt $SelfCap) { $st = $st.Substring(0,$SelfCap) + ' ...[TRUNCATED]' }
  Write-Output ("SELFTEXT:")
  Write-Output $st
  if ($j.comments) {
    $top = $j.comments | Sort-Object -Property score -Descending | Select-Object -First $TopComments
    Write-Output ("TOP {0} COMMENTS (of {1} fetched):" -f $TopComments, $j.comments.Count)
    foreach ($c in $top) {
      $b = ''
      if ($c.body) { $b = $c.body -replace "\r?\n", ' ' }
      if ($b.Length -gt $CommentCap) { $b = $b.Substring(0,$CommentCap) + ' ...[TRUNCATED]' }
      Write-Output ("  [{0}] {1} (score {2}): {3}" -f $c.id, $c.author, $c.score, $b)
    }
  } else {
    Write-Output ("COMMENTS: none fetched")
  }
}
