# Open Mag OpenClaw Control UI as an app window.
# Token is read from Mag .env — never stored in the shortcut.
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$envFile = Join-Path $Root ".env"
$line = Get-Content -LiteralPath $envFile | Where-Object { $_ -match '^OPENCLAW_GATEWAY_TOKEN=' } | Select-Object -First 1
if (-not $line) { throw "OPENCLAW_GATEWAY_TOKEN missing from Mag .env" }
$token = $line.Substring($line.IndexOf("=") + 1).Trim().Trim('"').Trim("'")

$running = docker inspect -f "{{.State.Running}}" mag-openclaw 2>$null
if ($running -ne "true") {
    docker compose -f (Join-Path $Root "docker-compose.yml") up -d openclaw | Out-Null
    Start-Sleep -Seconds 5
}

$url = "http://127.0.0.1:18789/#token=$token"
$browsers = @(
    "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe",
    "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
    "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
)
$browser = $browsers | Where-Object { Test-Path $_ } | Select-Object -First 1
if ($browser) {
    Start-Process -FilePath $browser -ArgumentList @("--app=$url")
} else {
    Start-Process $url
}
