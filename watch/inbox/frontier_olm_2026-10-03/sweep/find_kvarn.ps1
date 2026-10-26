$ErrorActionPreference = 'SilentlyContinue'
$root = 'C:\Users\foste\Documents\projects\local_sovereign_agent'
$dirs = @('memory','docs','.agents','corpus','watch\inbox\frontier_olm_2026-10-03','lens')
foreach ($d in $dirs) {
  $p = Join-Path $root $d
  if (-not (Test-Path $p)) { Write-Output ("MISSING DIR: " + $d); continue }
  Get-ChildItem -Path $p -Recurse -File -Include *.md,*.json,*.jsonl,*.txt -ErrorAction SilentlyContinue |
    Select-String -Pattern 'KVarN' -SimpleMatch -List -ErrorAction SilentlyContinue |
    ForEach-Object { Write-Output ("HIT: " + $_.Path + " : line " + $_.LineNumber) }
}
Write-Output 'DONE'
