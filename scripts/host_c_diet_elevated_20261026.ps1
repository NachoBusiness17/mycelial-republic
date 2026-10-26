# host_c_diet_elevated_20261026.ps1 - ONE-CLICK C: diet (elevation required)
# Prepared 2026-10-26 by the seat boot window (parse-verified before your click,
# per the zero-blink one-UAC-click law). Non-destructive: no files deleted.
#
# What it does:
#   1. hiberfil.sys OFF        -> frees ~26.2 GB immediately (powercfg /h off).
#      Desktop; you lose Windows hibernate + fast-startup (boots marginally
#      slower, machine has 7-day uptimes anyway).
#   2. pagefile.sys 65.6GB -> fixed 32GB (64GB RAM box; 32GB is generous).
#      Takes effect at next reboot (pagefile shrinks on restart).
#   3. Reports before/after free space to scripts\host_c_diet_log.txt.
#
# What it deliberately does NOT do (separate, not this click):
#   - Docker vhdx compact: needs wsl --shutdown = kills the 8 running estate
#     containers (mag-sovereign, gstd-node, cluster-factorio...). 15.77GB of
#     build cache already pruned INSIDE the vhdx; compacting returns it to C:
#     later, fleet-down window only.
#   - Any file deletions. Zero. Cache purges already ran unelevated.
#
# Run: right-click -> Run with PowerShell as Administrator
#      (or: Start-Process powershell -Verb RunAs -ArgumentList
#        '-ExecutionPolicy Bypass -File <this path>')
# Reboot afterward to collect the pagefile half.

$ErrorActionPreference = 'Continue'
$log = Join-Path $PSScriptRoot 'host_c_diet_log.txt'
function Free-GB { [math]::Round((Get-PSDrive C).Free/1GB,1) }
$before = Free-GB
"=== host C: diet $(Get-Date -Format s)" | Tee-Object -FilePath $log -Append
"free before: $before GB" | Tee-Object -FilePath $log -Append

# --- 1. hibernation off (frees hiberfil.sys ~26 GB now)
if (Test-Path C:\hiberfil.sys) {
  powercfg /h off 2>&1 | Out-Null
  Start-Sleep -Seconds 2
  if (Test-Path C:\hiberfil.sys) {
    "hiberfil: still present after powercfg /h off (fast-startup may hold it; shrinks at reboot)" | Tee-Object -FilePath $log -Append
  } else { "hiberfil: removed (~26 GB freed)" | Tee-Object -FilePath $log -Append }
} else { "hiberfil: already absent" | Tee-Object -FilePath $log -Append }

# --- 2. pagefile: fixed 32 GB (was 65.6 GB auto/unset on a 64 GB RAM box)
$cs = Get-CimInstance Win32_ComputerSystem
if ($cs.AutomaticManagedPagefile) {
  Set-CimInstance -InputObject $cs -Property @{AutomaticManagedPagefile=$false}
  "automatic pagefile management: disabled" | Tee-Object -FilePath $log -Append
}
$pf = Get-CimInstance Win32_PageFileSetting -Filter "Name='C:\\pagefile.sys'"
if (-not $pf) {
  $pf = New-CimInstance -ClassName Win32_PageFileSetting -Property @{Name='C:\pagefile.sys'} -Key Name -ClientOnly
}
Set-CimInstance -InputObject $pf -Property @{InitialSize=32768; MaximumSize=32768}
"pagefile: set fixed 32768 MB (was 65.6 GB) - shrinks at next reboot" | Tee-Object -FilePath $log -Append

$after = Free-GB
"free after: $after GB (reboot collects the pagefile half: expect ~+30 GB more)" | Tee-Object -FilePath $log -Append
"DONE. Reboot when convenient." | Tee-Object -FilePath $log -Append
