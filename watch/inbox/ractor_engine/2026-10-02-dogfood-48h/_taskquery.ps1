$names = @('MagCensusPatrolDaily','MagFtsIndexDaily','MagImproveDaily','MagLeaveProtocolDaily','MagGapSentinelDaily','MagTipWitnessDaily','MagXRadarDaily')
foreach ($n in $names) {
  $t = Get-ScheduledTask -TaskName $n -ErrorAction SilentlyContinue
  if ($t) {
    $i = $t | Get-ScheduledTaskInfo
    $act = ($t.Actions | ForEach-Object { "$($_.Execute) $($_.Arguments)" }) -join ' ; '
    "{0} | LastRun={1} | LastResult={2} | NextRun={3} | Action={4}" -f $n, $i.LastRunTime, $i.LastTaskResult, $i.NextRunTime, $act
  }
}
"--- any task still referencing invisible_runner ---"
Get-ScheduledTask | ForEach-Object {
  $a = ($_.Actions | ForEach-Object { "$($_.Execute) $($_.Arguments)" }) -join ' ; '
  if ($a -match 'invisible_runner') { "$($_.TaskName) => $a" }
}
