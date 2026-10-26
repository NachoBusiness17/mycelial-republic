# MagGstdDrainDaily - the standing earn loop (foundation 2: runs without the operator awake)
# Chain: fresh master read -> greed law handles band checks -> drain (dry suppresses settles
# automatically since the 2026-10-13 live-fire fix) -> receipts bank to queue/gstd_tasks/DONE.
# Log: logs/gstd_drain_daily.log

$ErrorActionPreference = "Continue"
$root = "C:\Users\foste\Documents\projects\local_sovereign_agent"
$py = Join-Path $root ".venv\Scripts\python.exe"
$log = Join-Path $root "logs\gstd_drain_daily.log"
$stamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"

"[$stamp] MagGstdDrainDaily starting" | Add-Content -Path $log

# 1. fresh master read (testnet)
Push-Location (Join-Path $root "reference\gstdcoin\contracts")
$read = & npx ts-node --project tsconfig.deploy.json scripts/read-master-ton.ts 2>&1 | Select-String "MASTER_TON"
$masterTon = if ($read -match "MASTER_TON ([0-9.]+)") { [double]$Matches[1] } else { -1 }
Pop-Location

if ($masterTon -lt 0) {
    "[$stamp] master read FAILED - skipping cycle" | Add-Content -Path $log
    exit 1
}
"[$stamp] master TON: $masterTon" | Add-Content -Path $log

# 2. self-heal: below the greed floor -> top up 0.5 TON from the deployer, then re-read
if ($masterTon -lt 1.0) {
    "[$stamp] below floor (1.0) - running self-heal funding" | Add-Content -Path $log
    Push-Location (Join-Path $root "reference\gstdcoin\contracts")
    & npx ts-node --project tsconfig.deploy.json scripts/send-fund.ts 2>&1 | Select-String "FINAL_MASTER|CONFIRMED" | ForEach-Object { "[$stamp] self-heal: $_" | Add-Content -Path $log }
    Pop-Location
    Push-Location (Join-Path $root "reference\gstdcoin\contracts")
    $read2 = & npx ts-node --project tsconfig.deploy.json scripts/read-master-ton.ts 2>&1 | Select-String "MASTER_TON"
    $masterTon = if ($read2 -match "MASTER_TON ([0-9.]+)") { [double]$Matches[1] } else { $masterTon }
    Pop-Location
    "[$stamp] master TON after self-heal: $masterTon" | Add-Content -Path $log
}

# 3. the drain (greed law gates: floor 1.0, cap 10.0)
Push-Location $root
& $py tools\gstd_drain.py --master-ton $masterTon 2>&1 | ForEach-Object { "[$stamp] $_" | Add-Content -Path $log }
Pop-Location
"[$stamp] MagGstdDrainDaily complete" | Add-Content -Path $log
