if (Test-Path 'watch/inbox/frontier_olm_2026-10-08/sweep') {
  Get-ChildItem 'watch/inbox/frontier_olm_2026-10-08/sweep' | ForEach-Object { Write-Output ($_.Name + ' ' + $_.Length) }
} else {
  Write-Output 'NO SWEEP DIR YET'
}
