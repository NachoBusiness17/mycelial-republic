param([string]$Query = "abs:offloading+AND+abs:inference", [string]$Out = "arxiv_fetch.xml", [int]$Max = 20)
$ProgressPreference = 'SilentlyContinue'
$uri = "https://export.arxiv.org/api/query?search_query=$Query&sortBy=submittedDate&sortOrder=descending&max_results=$Max"
try {
  $r = Invoke-WebRequest -UseBasicParsing -Uri $uri -TimeoutSec 50 -UserAgent 'mag-sweep'
  $r.Content | Out-File -Encoding utf8 $Out
  Write-Output ("OK bytes=" + $r.Content.Length)
} catch {
  Write-Output ("FETCH-FAIL: " + $_.Exception.Message)
}
