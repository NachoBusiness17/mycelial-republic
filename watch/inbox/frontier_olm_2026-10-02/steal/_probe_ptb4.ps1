$ErrorActionPreference = 'SilentlyContinue'
Get-ChildItem mag,tools -Filter duel_style_regression.py -Recurse | ForEach-Object { $_.FullName }
Write-Output '--- top-level check ---'
Test-Path 'tools\duel_style_regression.py'
Test-Path 'mag\duel_style_regression.py'
