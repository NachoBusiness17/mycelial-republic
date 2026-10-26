foreach ($t in 'MagCensusPatrolDaily','MagFtsIndexDaily','MagImproveDaily','MagLeaveProtocolDaily') {
  Write-Output ("== " + $t)
  schtasks /Query /TN $t /V /FO LIST | Select-String -Pattern 'Task To Run','Last Run Time','Last Result','Status','Next Run Time' | ForEach-Object { $_.Line }
}
