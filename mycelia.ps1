# Mycelia launcher - project .venv only
$ErrorActionPreference = 'Stop'
$Root = $PSScriptRoot
$Py = Join-Path $Root '.venv\Scripts\python.exe'
$Exe = Join-Path $Root '.venv\Scripts\mycelia.exe'
if (-not (Test-Path $Py)) { Write-Error 'Missing mycelial venv. Run scripts\bootstrap.ps1' }
if (Test-Path $Exe) { & $Exe @args } else { & $Py -m mycelial_republic.cli @args }
exit $LASTEXITCODE