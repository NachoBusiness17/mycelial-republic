$hits = Select-String -Path 'watch/inbox/frontier_olm_2026-10-03/sweep/*.md' -Pattern 'Waselnuk','Unblocked','per-task','2103156267246334157' -SimpleMatch
foreach ($h in $hits) {
  Write-Output ($h.Path + ':' + $h.LineNumber + ': ' + $h.Line.Substring(0, [Math]::Min(220, $h.Line.Length)))
}
Write-Output '=== DIR LISTING ==='
Get-ChildItem 'watch/inbox/frontier_olm_2026-10-03/sweep' | ForEach-Object { Write-Output ($_.Name + ' ' + $_.Length) }
