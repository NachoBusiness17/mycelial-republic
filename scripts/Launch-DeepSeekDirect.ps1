<#
.SYNOPSIS
  Launch mag/deepseek_direct_runner.py (five grounded DeepSeek design calls, one per steal).
.DESCRIPTION
  Default: --live --steal all (needs $env:DEEPSEEK_API_KEY; its value is never echoed).
  -DryRun: packs prompts + manifest only; no key needed, no network.
  Any extra arguments pass straight through, e.g. -- --model deepseek-v4-pro --steal 3
.EXAMPLE
  .\scripts\Launch-DeepSeekDirect.ps1
  .\scripts\Launch-DeepSeekDirect.ps1 -DryRun
  .\scripts\Launch-DeepSeekDirect.ps1 --model deepseek-v4-pro --max-tokens 32000
#>
param(
    [switch]$DryRun,
    [Parameter(ValueFromRemainingArguments = $true)][string[]]$PassThru
)
$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
$py = Join-Path $repo '.venv\Scripts\python.exe'
if (-not (Test-Path $py)) { Write-Error "venv python not found: $py"; exit 2 }
Push-Location $repo
try {
    if ($DryRun) {
        & $py -m mag.deepseek_direct_runner --dry-run --steal all @PassThru
    } else {
        if ([string]::IsNullOrWhiteSpace($env:DEEPSEEK_API_KEY)) {
            Write-Host 'DEEPSEEK_API_KEY is not set in this session; refusing live run.' -ForegroundColor Red
            exit 2
        }
        & $py -m mag.deepseek_direct_runner --live --steal all @PassThru
    }
    exit $LASTEXITCODE
} finally { Pop-Location }
