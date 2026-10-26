$f = 'watch/inbox/frontier_olm_2026-10-03/sweep/inference-efficiency-x.md'
Write-Output '=== HEADERS ==='
Select-String -Path $f -Pattern '^#' | ForEach-Object { Write-Output ($_.LineNumber.ToString() + ': ' + $_.Line) }
Write-Output '=== ITEM LINES ==='
Select-String -Path $f -Pattern '^\s*\d+\.\s+\*\*','^### ' | ForEach-Object { Write-Output ($_.LineNumber.ToString() + ': ' + $_.Line.Substring(0, [Math]::Min(180, $_.Line.Length))) }
