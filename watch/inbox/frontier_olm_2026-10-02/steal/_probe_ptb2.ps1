$ErrorActionPreference = 'SilentlyContinue'
Write-Output "--- module locations ---"
Get-ChildItem mag,tools -Recurse -Include judge.py,duel_harness.py,overmind_judge.py,percolator.py,auto_quantize.py | ForEach-Object { $_.FullName }
Write-Output "--- compass organ lines ---"
Select-String -Path 'docs\ref\MAG_MYCELIAL_REPUBLIC_COMPASS.md' -Pattern 'quantizer','percolator','sovereign mirror','water graph','gopher fleet','context pack' | Select-Object -First 20 | ForEach-Object { "{0}: {1}" -f $_.LineNumber, $_.Line.Trim() }
Write-Output "--- duel harness judge invocation (grep judge params) ---"
Select-String -Path 'mag\duel_harness.py' -Pattern 'judge','temperature','temp' | Select-Object -First 12 | ForEach-Object { "{0}: {1}" -f $_.LineNumber, $_.Line.Trim() }
