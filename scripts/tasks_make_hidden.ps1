# tasks_make_hidden.ps1 — 2026-10-05
# Rewrites headed estate Task Scheduler actions to the hidden wscript launcher
# (scripts/run_hidden.vbs). Every task below ran python.exe/powershell.exe/cmd
# with LogonType Interactive, so each fire popped a console on the operator's
# desktop. New action: wscript //B //Nologo run_hidden.vbs <orig exe> <orig args>,
# WorkingDirectory preserved (repo root when the task never set one — Task
# Scheduler defaults CWD to System32). Triggers, principal, and settings pass
# through untouched via Set-ScheduledTask. Multi-action tasks (Estate Gopher)
# get every action wrapped; actions run sequentially, and wscript waits, so
# ordering and stop-on-failure semantics survive.
# Dry-run by default; -Apply to change. Idempotent: skips already-hidden tasks.
param([switch]$Apply)

$repo = "C:\Users\foste\Documents\projects\local_sovereign_agent"
$vbs = Join-Path $repo "scripts\run_hidden.vbs"
$wscript = Join-Path $env:WINDIR "System32\wscript.exe"

$generic = @(
  'Estate Cooker','Estate FullScan','Estate Gopher','Estate KeyAudit',
  'Estate LaneSupervisor','Estate Librarian','Estate Ratchet','Estate Spine Index',
  'Estate StealthSweep','EstateWalkDaily','MagCensusPatrolDaily',
  'MagCorpusRescanDaily','MagEndpointNewsDaily','MagFreeLaneFleet',
  'MagFtsIndexDaily','MagGapSentinelDaily','MagGateCanaryDaily','MagImproveDaily',
  'MagLeaveProtocolDaily','MagTipWitnessDaily','MagVisionNightly','MagXRadarDaily'
)

# Server tasks get rebuilt instead of wrapped: their `cmd /c cd /d ... && ...`
# chain cannot be tokenized, and the cd belongs in WorkingDirectory anyway.
$overrides = @{
  'MagPrivateOffice8765' = @{ wd = $repo }
  'MagLabKit8765'        = @{ wd = 'C:\Users\foste\Documents\projects\mag-sovereign-kit' }
}
$labArgs = 'main.py lab --host 127.0.0.1 --port 8765'
$labExe = Join-Path $repo '.venv\Scripts\python.exe'

function Wrap-One([string]$exe, [string[]]$argTokens, [string]$wd) {
  # Strip quotes baked into Estate Spine Index's action fields; none of the
  # estate paths contain spaces, so bare tokens are unambiguous.
  $exe = $exe.Trim('"')
  $argTokens = @($argTokens | ForEach-Object { $_.Trim('"') } | Where-Object { $_ })
  $parts = @('//B', '//Nologo', "`"$vbs`"", "`"$exe`"") + $argTokens
  New-ScheduledTaskAction -Execute $wscript -Argument ($parts -join ' ') -WorkingDirectory $wd
}

$changed = 0; $skipped = 0; $missing = 0
foreach ($name in (@($generic) + @($overrides.Keys))) {
  $t = Get-ScheduledTask -TaskName $name -ErrorAction SilentlyContinue
  if (-not $t) { Write-Output "MISSING  $name"; $missing++; continue }
  if (@($t.Actions | Where-Object { $_.Execute -notmatch 'wscript|pythonw' }).Count -eq 0) {
    Write-Output "SKIP     $name (already hidden)"; $skipped++; continue
  }

  if ($overrides.ContainsKey($name)) {
    $newActions = @(Wrap-One $labExe ($labArgs -split ' +') $overrides[$name].wd)
    Write-Output ("REBUILD  {0} (server task, cmd-chain -> WD)" -f $name)
  } else {
    $newActions = @()
    foreach ($a in @($t.Actions)) {
      $wd = $a.WorkingDirectory; if (-not $wd) { $wd = $repo }
      $tokens = @($a.Arguments -split ' +')
      Write-Output ("WRAP     {0} :: {1} {2} @ {3}" -f $name, $a.Execute, $a.Arguments, $(if ($a.WorkingDirectory) { $a.WorkingDirectory } else { '<System32 default>' }))
      $newActions += Wrap-One $a.Execute $tokens $wd
    }
  }
  if ($Apply) {
    try {
      Set-ScheduledTask -TaskName $name -Action $newActions | Out-Null
      Write-Output "APPLIED  $name"; $changed++
    } catch {
      Write-Output "FAILED   $name :: $($_.Exception.Message)"
    }
  } else { $changed++ }
}
Write-Output ("--- {0} to change ({1} applied), {2} skipped, {3} missing" -f $changed, $(if ($Apply) { $changed } else { 0 }), $skipped, $missing)
