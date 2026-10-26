# Mag endpoint_news daily fire (L0). One pass of scripts/endpoint_news.py.
# Register: powershell -ExecutionPolicy Bypass -File scripts\register_endpoint_news_task.ps1
$ErrorActionPreference = "Stop"
$Root = Split-Path $PSScriptRoot -Parent
Set-Location $Root

$Py = Join-Path $Root ".venv\Scripts\python.exe"
$LogDir = Join-Path $Root "logs"
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir | Out-Null }
$Log = Join-Path $LogDir "endpoint_news.log"
$Stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

function Write-Log([string]$Msg) {
    $line = "[$Stamp] $Msg"
    Add-Content -Path $Log -Value $line -Encoding utf8
    Write-Host $line
}

if (-not (Test-Path $Py)) {
    Write-Log "FAIL: missing venv python at $Py"
    exit 1
}

Write-Log "START endpoint_news cwd=$Root"
try {
    & $Py scripts\endpoint_news.py 2>&1 | Select-Object -Last 40 | Out-File -FilePath $Log -Append -Encoding utf8
    $code = $LASTEXITCODE
    if ($null -eq $code) { $code = 0 }
    Write-Log "END exit=$code"
    exit $code
} catch {
    Write-Log "FAIL: $_"
    exit 1
}
