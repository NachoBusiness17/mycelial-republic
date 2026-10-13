# Mag nightly vision batch (THE 50 W9 T44) - drains the Mr Pool vision triage
# backlog on the local sovereign lane. Idempotent: a complete corpus is an
# honest no-op; new media or error rows are drained automatically.
# Register: powershell -ExecutionPolicy Bypass -File scripts\register_vision_nightly.ps1
$ErrorActionPreference = "Stop"
$Root = Split-Path $PSScriptRoot -Parent
Set-Location $Root

$Py = Join-Path $Root ".venv\Scripts\python.exe"
$Driver = Join-Path $PSScriptRoot "vision_nightly.py"
$LogDir = Join-Path $Root "logs"
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir | Out-Null }
$Log = Join-Path $LogDir "vision_nightly.log"
$Stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

function Write-Log([string]$Msg) {
    $line = "[$Stamp] $Msg"
    Add-Content -Path $Log -Value $line -Encoding utf8
    Write-Host $line
}

if (-not (Test-Path $Py))     { Write-Log "FAIL: missing venv python at $Py"; exit 1 }
if (-not (Test-Path $Driver)) { Write-Log "FAIL: missing driver at $Driver"; exit 1 }

# The python driver owns logs\vision_nightly.log (it appends every meaningful
# line itself, including pool stdout). This wrapper only adds START/END markers
# with quick Add-Content calls: Tee-Object would hold the file open across the
# whole python run and collide with the driver's appends (2026-09-19 fix).
Write-Log "START vision_nightly (driver --run) cwd=$Root"
try {
    & $Py $Driver --run
    $code = $LASTEXITCODE
    if ($null -eq $code) { $code = 0 }
    Write-Log "END exit=$code"
    exit $code
} catch {
    Write-Log "FAIL: $_"
    exit 1
}
