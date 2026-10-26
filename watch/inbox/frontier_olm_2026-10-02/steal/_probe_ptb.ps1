# probe for steal card: evals-self-improvement via x (PostTrainBench v1.2)
$ErrorActionPreference = 'SilentlyContinue'

# 1. overlap re-verify: PostTrainBench across catalog, memory, today's olm dir
$c = (Select-String -Path 'catalog\catalog.jsonl' -Pattern 'PostTrainBench' -SimpleMatch | Measure-Object).Count
Write-Output ("catalog hits: " + $c)
$m = Get-ChildItem memory -Recurse -File | Select-String -Pattern 'PostTrainBench' -SimpleMatch -List
Write-Output ("memory hits: " + (($m | ForEach-Object { $_.Path }) -join '; '))
$w = Get-ChildItem 'watch\inbox\frontier_olm_2026-10-02' -Recurse -File | Select-String -Pattern 'PostTrainBench' -SimpleMatch -List
Write-Output ("olm-2026-10-02 hits (pre-card): " + (($w | ForEach-Object { $_.Path }) -join '; '))

# 2. organ modules
Write-Output "--- organ-ish modules (mag/ and tools/) ---"
Get-ChildItem mag,tools -Filter *.py | Where-Object { $_.Name -match 'duel|judge|quant|percol|grader|improve' } | ForEach-Object { $_.Name }

# 3. organ canon lines in FRAMEWORK_LOAD
Write-Output "--- FRAMEWORK_LOAD organ lines ---"
Select-String -Path 'docs\FRAMEWORK_LOAD.md' -Pattern 'quantizer','percolator','sovereign mirror','water graph','gopher fleet','context pack' | Select-Object -First 15 | ForEach-Object { "{0}: {1}" -f $_.LineNumber, $_.Line.Trim() }

# 4. duel ledger schema peek: first row, first 600 chars
Write-Output "--- logs/duel/duels.jsonl first row (600 chars) ---"
$first = Get-Content 'logs\duel\duels.jsonl' -TotalCount 1
Write-Output ($first.Substring(0, [Math]::Min(600, $first.Length)))

# 5. does a judge2 / second-judge column already exist in any duel row? count rows mentioning 'judge2'
$j2 = (Select-String -Path 'logs\duel\duels.jsonl' -Pattern 'judge2' -SimpleMatch | Measure-Object).Count
Write-Output ("duel rows mentioning judge2: " + $j2)
