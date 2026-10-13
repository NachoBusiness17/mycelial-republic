# Mag corpus map freshness run (B2-104 policy): incremental rescan + tags
# re-run + manifest stamp. Fired by the MagCorpusRescanDaily scheduled task.
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
$Py = Join-Path $Root ".venv\Scripts\python.exe"
$Log = Join-Path $Root "logs\corpus_rescan_daily.log"

# 2026-09-27 autopsy fix (fleet doctor thread 8): the first fires all died
# exit 1 with ModuleNotFoundError 'mag' because python -m needs CWD = repo
# root (the mag package is not pip-installed in the venv). Both sibling
# dailies (census_patrol_daily.ps1, fts_index_daily.ps1) already do this;
# this task was registered without the line.
Set-Location $Root

if (-not (Test-Path $Py)) {
    Write-Error "Missing repo venv interpreter: $Py"
    exit 1
}

"[$(Get-Date -Format s)] incremental rescan start" | Out-File -FilePath $Log -Append -Encoding utf8
& $Py -m mag.catalog_rescan incremental 2>&1 | Out-File -FilePath $Log -Append -Encoding utf8
"[$(Get-Date -Format s)] exit $LASTEXITCODE" | Out-File -FilePath $Log -Append -Encoding utf8
exit $LASTEXITCODE
