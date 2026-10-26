$ErrorActionPreference = 'Stop'
$rows = Get-Content 'logs\duel\duels.jsonl' | ForEach-Object { $_ | ConvertFrom-Json }
Write-Output ("total rows: " + $rows.Count)
$modes = ($rows | ForEach-Object { $_.mode } | Group-Object | ForEach-Object { $_.Name + '=' + $_.Count }) -join '; '
Write-Output ("modes: " + $modes)
$alt = @($rows | Where-Object { $_.mode -eq 'altjudge' })
Write-Output ("altjudge rows: " + $alt.Count)
Write-Output ("altjudge judges: " + (($alt | ForEach-Object { $_.judge } | Sort-Object -Unique) -join '; '))
$tss = ($alt | ForEach-Object { $_.ts } | Sort-Object)
Write-Output ("altjudge ts range: " + $tss[0] + " .. " + $tss[$tss.Count - 1])
$byId = @{}
foreach ($r in $rows) { $byId[$r.ask_id] = $r }
$flips = 0; $pairs = 0
foreach ($a in $alt) {
  $orig = $byId[$a.rejudge_of]
  if ($null -eq $orig) { Write-Output ("ORPHAN: " + $a.ask_id); continue }
  $pairs++
  if ($a.winner -ne $orig.winner) {
    $flips++
    Write-Output ("FLIP: " + $a.ask_id + " orig_winner=" + $orig.winner + " alt_winner=" + $a.winner + " orig_judge=" + $orig.judge)
  }
}
Write-Output ("cross-family pairs: " + $pairs + "  flips: " + $flips)
$emberOnly = @($rows | Where-Object { ($_.mode -ne 'altjudge') -and ($_.judge -eq 'fireworks/ember-1') })
Write-Output ("ember-only rows (non-altjudge): " + $emberOnly.Count)
