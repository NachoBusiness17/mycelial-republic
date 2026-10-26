$ErrorActionPreference = 'SilentlyContinue'
$f = 'C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_2026-10-03\lens\laws.md'
Select-String -Path $f -Pattern 'stale','substrate','KV','cache' -SimpleMatch | ForEach-Object {
  Write-Output ($_.LineNumber.ToString() + ': ' + $_.Line)
}
