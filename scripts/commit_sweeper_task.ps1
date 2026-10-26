# MagCommitSweeper - the one git writer (run every 10 minutes)
# Registered by schtasks; WindowStyle Hidden per the no-headed-surface law.
# Output APPENDS: `*>` truncated this log every run, so hours of deferrals hid
# behind a 0-byte file (diagnosed 2026-10-20). `*>>` keeps the history.
$repo = "C:\Users\foste\Documents\projects\local_sovereign_agent"
$py = Join-Path $repo ".venv\Scripts\python.exe"
$log = Join-Path $repo "logs\commit_sweeper_task.log"
Set-Location $repo
"=== $(Get-Date -Format o) sweep start ===" | Out-File -Append -Encoding utf8 $log
& $py (Join-Path $repo "tools\commit_sweeper.py") sweep 2>&1 | Out-File -Append -Encoding utf8 $log
"=== $(Get-Date -Format o) sweep exit $LASTEXITCODE ===" | Out-File -Append -Encoding utf8 $log
