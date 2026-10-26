$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
$uaScript = 'windows:sweeper-kvcache:2026-10-03 (research sweep, contact: operator)'
$uaBrowser = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
$doors = @(
  @{ n='www-json'; u='https://www.reddit.com/r/LocalLLaMA/top.json?t=month&limit=10'; ua=$uaBrowser },
  @{ n='www-json-scriptua'; u='https://www.reddit.com/r/LocalLLaMA/top.json?t=month&limit=10'; ua=$uaScript },
  @{ n='api-json'; u='https://api.reddit.com/r/LocalLLaMA/top?t=month&limit=10'; ua=$uaScript },
  @{ n='old-html'; u='https://old.reddit.com/r/LocalLLaMA/top/'; ua=$uaBrowser },
  @{ n='www-html'; u='https://www.reddit.com/r/LocalLLaMA/top/?t=month'; ua=$uaBrowser }
)
foreach ($d in $doors) {
  try {
    $resp = Invoke-WebRequest -Uri $d.u -UserAgent $d.ua -TimeoutSec 30
    $head = $resp.Content
    if ($head.Length -gt 220) { $head = $head.Substring(0,220) }
    $head = ($head -replace "\r?\n", ' ')
    Write-Output ("DOOR {0} : HTTP {1} : LEN {2} : {3}" -f $d.n, $resp.StatusCode, $resp.Content.Length, $head)
  } catch {
    Write-Output ("DOOR {0} : FAILED : {1}" -f $d.n, $_.Exception.Message)
  }
  Start-Sleep -Milliseconds 1200
}
