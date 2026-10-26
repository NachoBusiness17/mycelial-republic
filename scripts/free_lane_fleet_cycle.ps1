# free_lane_fleet_cycle.ps1 - the 24/7 free-lane burn cycle (2026-10-05).
# ABSOLUTE PATH LAW (EstateWalkDaily lesson 2026-10-03): Task Scheduler starts
# us in System32 with a stripped PATH, so every path here is absolute and the
# venv interpreter is named in full - never bare python (Hermes venv on PATH).
$py = "C:\Users\foste\Documents\projects\local_sovereign_agent\.venv\Scripts\python.exe"
$repo = "C:\Users\foste\Documents\projects\local_sovereign_agent"
$log = Join-Path $repo "logs\free_lane_fleet.log"
$stamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
try {
    Set-Location $repo  # -m needs the repo as CWD; Task Scheduler starts in System32 (caught live 2026-10-05T11:33Z: 5 dead cycles ModuleNotFoundError)
    $out = & $py -m tools.free_lane_fleet --cycle 2>&1
    if ($LASTEXITCODE -ne 0) {
        # Ouroboros r2 row 1 remainder (2026-10-05): the catch block cannot see
        # a nonzero native exit (the 13-dead-fires class ran green under
        # LastTaskResult 0), so the exit code is checked here, explicitly.
        "$stamp ERROR free_lane_fleet --cycle exited $LASTEXITCODE" | Add-Content -Encoding UTF8 $log
        "$stamp ERROR free_lane_fleet --cycle exited $LASTEXITCODE" | Add-Content -Encoding UTF8 (Join-Path $repo "memory\runs\free_lane_fleet\errors.log")
        exit 1
    }
    $outText = "$out"
    if ($outText -notmatch '^FREE-LANE CYCLE: fired \d+, banked \d+ findings, providers healthy \d+/\d+') {
        # Green-light cure, second half: a nonzero exit is not the only way a
        # cycle lies; any output that does not carry the FREE-LANE CYCLE
        # success shape is a dead loop wearing a green task.
        "$stamp ERROR unexpected cycle output shape: $outText" | Add-Content -Encoding UTF8 $log
        "$stamp ERROR unexpected cycle output shape: $outText" | Add-Content -Encoding UTF8 (Join-Path $repo "memory\runs\free_lane_fleet\errors.log")
        exit 1
    }
    "$stamp $out" | Add-Content -Encoding UTF8 $log
    # Liveness tripwire (ouroboros r2 row 1 remainder, 2026-10-05; the B2-465
    # no-START-stamp shape): a ledger older than 90 minutes while the hourly
    # task should have fired 2+ times is green-but-dead; fail loudly.
    $liveness = & $py -m tools.free_lane_fleet --check-liveness 2>&1
    if ($LASTEXITCODE -ne 0) {
        "$stamp LIVENESS-FAIL $liveness" | Add-Content -Encoding UTF8 $log
        "$stamp LIVENESS-FAIL $liveness" | Add-Content -Encoding UTF8 (Join-Path $repo "memory\runs\free_lane_fleet\errors.log")
        exit 1
    }
} catch {
    "$stamp ERROR $($_.Exception.Message)" | Add-Content -Encoding UTF8 $log
    "$stamp ERROR $($_.Exception.Message)" | Add-Content -Encoding UTF8 (Join-Path $repo "memory\runs\free_lane_fleet\errors.log")
    exit 1
}
