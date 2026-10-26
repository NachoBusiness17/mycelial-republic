$ErrorActionPreference = 'SilentlyContinue'
$root = 'C:\Users\foste\Documents\projects\local_sovereign_agent'
Get-ChildItem "$root\memory" -Recurse -File -Include *.md,*.json,*.jsonl |
  Select-String -SimpleMatch 'Jev' -List |
  ForEach-Object { $rel = $_.Path.Replace($root + '\', ''); Write-Output $rel }
