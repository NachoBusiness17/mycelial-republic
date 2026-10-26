$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
$ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
$doors = @(
  @{ n='mojeek'; u='https://www.mojeek.com/search?q=site%3Areddit.com%2Fr%2FLocalLLaMA+%22KV+cache%22' },
  @{ n='bing'; u='https://www.bing.com/search?q=site%3Areddit.com%2Fr%2FLocalLLaMA+%22KV+cache%22' },
  @{ n='arctic-shift'; u='https://arctic-shift.photon-reddit.com/api/posts/search?subreddit=LocalLLaMA&limit=3' },
  @{ n='redlib-catsarch'; u='https://redlib.catsarch.com/r/LocalLLaMA/top?t=month' },
  @{ n='redlib-perennialte'; u='https://redlib.perennialte.ch/r/LocalLLaMA/top?t=month' },
  @{ n='redlib-artemislena'; u='https://red.artemislena.eu/r/LocalLLaMA/top?t=month' },
  @{ n='searx-be'; u='https://searx.be/search?q=site%3Areddit.com%2Fr%2FLocalLLaMA+kv+cache' }
)
foreach ($d in $doors) {
  try {
    $resp = Invoke-WebRequest -Uri $d.u -UserAgent $ua -TimeoutSec 35
    $head = $resp.Content
    if ($head.Length -gt 260) { $head = $head.Substring(0,260) }
    $head = ($head -replace "\r?\n", ' ') -replace '\s+',' '
    Write-Output ("DOOR {0} : HTTP {1} : LEN {2} : {3}" -f $d.n, $resp.StatusCode, $resp.Content.Length, $head)
  } catch {
    Write-Output ("DOOR {0} : FAILED : {1}" -f $d.n, $_.Exception.Message)
  }
  Start-Sleep -Seconds 2
}
