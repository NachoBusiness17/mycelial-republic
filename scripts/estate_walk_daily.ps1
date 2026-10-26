# EstateWalkDaily - re-bake the estate walk tapestry (fossil-in-feed law for
# its own renderer: the bake has a cadence or it dies silently again).
# On failure: loud line to memory/attention.md (the repaired alarm channel).
#
# PATH LAW (2026-10-01 repair): Task Scheduler runs this with CWD at
# C:\Windows\System32, so every relative path silently failed - the 10-01
# 09:15 fire returned LastTaskResult=1 with no END line AND no alarm (the
# loud channel was broken by the same relative-path bug that triggered it).
# All paths are absolute now. Founding receipt: the gap-analysis audit
# (mickey17 gap-analysis lane a08, watch/inbox/gap_analysis_20261001/).
$repo = "C:\Users\foste\Documents\projects\local_sovereign_agent"
$log = Join-Path $repo "logs\estate_walk_daily.log"
$alarm = Join-Path $repo "memory\attention.md"
$stamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
$logDir = Split-Path $log
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }
& (Join-Path $repo ".venv\Scripts\python.exe") `
  (Join-Path $repo "dashboard\static\_build_estate_walk.py") >> $log 2>&1
if ($LASTEXITCODE -ne 0) {
  Add-Content -Path $alarm -Value "$stamp ESTATE-WALK-BAKE-FAILED exit=$LASTEXITCODE see logs/estate_walk_daily.log"
  exit 1
}
Add-Content -Path $log -Value "END $stamp exit=0"
exit 0
