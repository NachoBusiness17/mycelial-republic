# MagLongrunnerPatrolDaily driver: the longrunners-caged law's daily tooth.
# Reads configs/longrunner_policy.json, scans the host process table for
# bare-host interpreters past the age fence outside the allowlist, alerts
# memory/attention.md, exits nonzero on findings. Never kills: killing is a
# seat or operator judgment (a live seat's work must not die to a patrol).
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
$Py = Join-Path $Root ".venv\Scripts\python.exe"
$Log = Join-Path $Root "logs\longrunner_patrol.log"
$Stamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

if (-not (Test-Path (Split-Path $Log -Parent))) {
    New-Item -ItemType Directory -Path (Split-Path $Log -Parent) -Force | Out-Null
}
"[$Stamp] MagLongrunnerPatrolDaily fire" | Out-File -FilePath $Log -Append -Encoding utf8
& $Py -m tools.longrunner_patrol 2>&1 | ForEach-Object { "$_" } |
    Out-File -FilePath $Log -Append -Encoding utf8
"[$Stamp] exit $LASTEXITCODE" | Out-File -FilePath $Log -Append -Encoding utf8
exit $LASTEXITCODE
