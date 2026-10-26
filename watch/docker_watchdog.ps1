# docker_watchdog.ps1 - the one sanctioned host-side script.
# FIX 2026-08-26 (tick): the old pipe-name check (dockerDesktopLinuxEngine) is stale in
# this Docker Desktop build - Test-Path fails while the engine is healthy (false DEGRADED
# every 5 min). Engine check now uses the docker CLI itself; relaunch logic unchanged.
$log = "C:\Users\foste\Documents\projects\local_sovereign_agent\logs\docker_watchdog.log"
$dd = "$env:LOCALAPPDATA\Programs\DockerDesktop\Docker Desktop.exe"
$engine = & docker version --format "{{.Server.Version}}" 2>$null
if (-not $engine) {
    $running = Get-Process -Name "Docker Desktop" -ErrorAction SilentlyContinue
    if (-not $running -and (Test-Path $dd)) {
        Start-Process $dd
        Add-Content $log ("{0} RELAUNCH: engine unreachable, Desktop not running -> started" -f (Get-Date -Format o))
    } else {
        Add-Content $log ("{0} DEGRADED: engine unreachable but Desktop running (engine starting or stuck)" -f (Get-Date -Format o))
    }
}
