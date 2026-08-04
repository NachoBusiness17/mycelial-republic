# Phase 0 bootstrap — Mycelial Republic
# Always install into project .venv (never Hermes PATH python).
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

Write-Host "== Mycelial Republic bootstrap ==" -ForegroundColor Cyan
if (-not (Test-Path .venv)) {
    Write-Host "Creating .venv ..." -ForegroundColor Cyan
    if (Get-Command py -ErrorAction SilentlyContinue) {
        py -3.12 -m venv .venv
    } else {
        python -m venv .venv
    }
}
$Pip = Join-Path $Root ".venv\Scripts\pip.exe"
$Py = Join-Path $Root ".venv\Scripts\python.exe"
& $Pip install -e ".[dev]"
Write-Host "OK: editable install complete" -ForegroundColor Green
& $Py -c "import mycelial_republic; print('import OK', mycelial_republic.__file__)"
Write-Host ""
Write-Host "Launcher:  .\mycelia.ps1 --help"
Write-Host "Or:        .\.venv\Scripts\python.exe -m mycelial_republic.cli --help"
Write-Host ""
Write-Host "Next:"
Write-Host "  1. Put X archive zip in data\raw\"
Write-Host "  2. .\mycelia.ps1 prep --raw data\raw\YOUR.zip --out data\exports\posts.jsonl"
Write-Host "  3. .\mycelia.ps1 annotate --in data\exports\posts.jsonl --out data\annotated\mirror_train.jsonl --auto-heuristics"
Write-Host "  4. .\mycelia.ps1 validate --in data\annotated\mirror_train.jsonl --min 800"
Write-Host "  5. Read scaffolds\vector_scaffold_v1.md"
