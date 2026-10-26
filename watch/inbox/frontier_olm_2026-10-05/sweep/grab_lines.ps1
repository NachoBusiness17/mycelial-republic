$root = 'C:\Users\foste\Documents\projects\local_sovereign_agent'
$targets = @(
  @{ f = Join-Path $root 'memory\trajectory\steps.jsonl'; n = 40452 },
  @{ f = Join-Path $root 'memory\trajectory\steps.jsonl'; n = 47023 },
  @{ f = Join-Path $root 'memory\trajectory\steps.jsonl'; n = 37651 },
  @{ f = Join-Path $root 'memory\trajectory\steps.jsonl'; n = 34014 },
  @{ f = Join-Path $root 'memory\trajectory\steps.jsonl'; n = 33816 },
  @{ f = Join-Path $root 'memory\runs\gapwave\hn_x_fanout\local_serving.md'; n = 22 },
  @{ f = Join-Path $root 'memory\runs\fleet_round\burn2b_pack.md'; n = 11937 },
  @{ f = Join-Path $root 'memory\runs\fleet_round\missed_pack.md'; n = 11906 }
)
foreach ($t in $targets) {
  if (-not (Test-Path $t.f)) { Write-Output ('MISSING FILE: ' + $t.f); continue }
  $lines = [System.IO.File]::ReadAllLines($t.f)
  $i = $t.n - 1
  if ($i -lt 0 -or $i -ge $lines.Length) { Write-Output ('OUT OF RANGE: ' + $t.f + ':' + $t.n + ' (file has ' + $lines.Length + ' lines)'); continue }
  $txt = $lines[$i]
  if ($txt.Length -gt 500) { $txt = $txt.Substring(0, 500) + '...' }
  Write-Output ((Split-Path $t.f -Leaf) + ':' + $t.n + ': ' + $txt)
}
