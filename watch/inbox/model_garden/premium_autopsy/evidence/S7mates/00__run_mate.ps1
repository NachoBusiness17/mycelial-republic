# run_mate.ps1 - per-mate static runner for the mates leave protocol (X12, 2026-09-29/30)
#
# NO PARAMETERS BY LAW. The Mimosa standoff (three hardenings, receipts in
# watch/inbox/mates_leave_protocol/REGISTER_NOTE.md 2026-09-30) ended only by
# removing every variable from the driver's subprocess argv. This file is the
# other half of that fix: tools/leave_dispatcher.py invokes
#   powershell -NoProfile -ExecutionPolicy Bypass -File <this file>
# as a fully CONSTANT argv, N times for N mates. Everything that varies
# (today's date, which mate, the prompt body) is computed HERE, inside
# PowerShell, after the gate-checked invocation: the argv is constant, only
# the mission file this runner reads varies. One fixed .ps1 per invocation
# shape; a new invocation shape means a new fixed .ps1, never a parameter.
#
# Contract:
#   - Set-Location to the repo root (this script lives in <repo>\scripts).
#   - Compute $Today via Get-Date (local date, same clock the dispatcher used).
#   - CLAIM the next unclaimed mission of today from logs\mates\missions\
#     (mission_<YYYYMMDD>_<nn>_<mate>.md). Claim = atomic CreateNew of a
#     <file>.claim sidecar; CreateNew fails if it exists, so N concurrent
#     constant-argv invocations each take a distinct mate. No unclaimed
#     mission -> honest no-op, exit 0, log line.
#   - Call `opencode run <fixed prompt template naming the claimed file>`.
#     The mate does the rest from the pack (persona, seed thread, laws,
#     STEER row, receipt contract) - the pack is the payload, the prompt
#     template never changes.
#   - Log to logs\mates\runs\run_<YYYYMMDD>_<mate>.log with Add-Content
#     -Encoding utf8 (B2-246: PS 5.1 Tee-Object writes UTF-16; never Tee).
#   - Pass opencode's exit code through; append the outcome to the .claim
#     sidecar so a crashed run is visible from the missions dir.
# No timeout on opencode: mates ride to their context edge (build-discipline
# law - no timeouts papering over sync problems).
$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
Set-Location $Root

$Today = Get-Date -Format "yyyyMMdd"
$MatesDir = Join-Path $Root "logs\mates"
$MissionsDir = Join-Path $MatesDir "missions"
$RunsDir = Join-Path $MatesDir "runs"
foreach ($d in @($MatesDir, $MissionsDir, $RunsDir)) {
    if (-not (Test-Path $d)) { New-Item -ItemType Directory -Path $d | Out-Null }
}
$DispatchLog = Join-Path $MatesDir "runner_$Today.log"

function Write-MateLog([string]$Msg) {
    $line = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $Msg"
    Add-Content -Path $DispatchLog -Value $line -Encoding utf8
    Write-Host $line
}

# AUTH FIX (2026-09-30): opencode's provider config rides {env:ZAI_API_KEY} and
# {env:ZAI_API_KEY_2} refs. A scheduled task inherits NO shell env, so the 08:00
# first fire sent an empty auth header and z.ai rejected every mate
# ("Authentication parameter not received in Header", logs/mates/runs/*).
# MINIMAL-EXPOSURE LAW (operator catch, same day): load ONLY the exact vars the
# opencode config references - never the whole .env. opencode snapshots shell
# env into its session store; every extra var would land there. Values never logged.
$EnvFile = Join-Path $Root ".env"
if (Test-Path $EnvFile) {
    $loaded = 0
    foreach ($name in @("ZAI_API_KEY", "ZAI_API_KEY_2")) {
        $line = Select-String -Path $EnvFile -Pattern ("^\s*" + $name + "=(.*)$") -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($line) {
            Set-Item -Path ("Env:" + $name) -Value $line.Matches[0].Groups[1].Value.Trim()
            $loaded++
        }
    }
    Write-MateLog ("env loaded: " + $loaded + " whitelisted var(s) for opencode auth (never full .env)")
}

# Resolve opencode: PATH first, else the known absolute install (hermes node
# bin, byte-verified 2026-09-29 via `where opencode`). Logged either way.
$cmd = Get-Command opencode -ErrorAction SilentlyContinue
if ($cmd) { $OpenCode = $cmd.Source } else { $OpenCode = "C:\Users\foste\AppData\Local\hermes\node\opencode.cmd" }

# Claim the next unclaimed mission of today (atomic CreateNew = the lock).
$Mission = $null
$pattern = Join-Path $MissionsDir "mission_$Today*.md"
foreach ($m in @(Get-ChildItem -Path $pattern -ErrorAction SilentlyContinue | Sort-Object Name)) {
    $claimPath = "$($m.FullName).claim"
    try {
        $fs = [System.IO.File]::Open($claimPath, [System.IO.FileMode]::CreateNew, [System.IO.FileAccess]::Write)
        $fs.Close()
        $Mission = $m
        break
    } catch {
        # already claimed by a sibling invocation - try the next pack
    }
}
if (-not $Mission) {
    Write-MateLog "no unclaimed mission for $Today (pattern $pattern) - honest no-op, exit 0"
    exit 0
}

$MateId = $Mission.BaseName -replace "^mission_\d{8}_\d+_", ""
$RelMission = "logs\mates\missions\$($Mission.Name)"
$RunLog = Join-Path $RunsDir "run_$($Mission.BaseName -replace '^mission_', '').log"

# THE FIXED PROMPT TEMPLATE - the only string shape this runner ever sends.
# Byte-stable except for the mission filename, which is exactly the part the
# static-runner design moved out of any argv.
$Prompt = "Read your mission pack at $RelMission and execute it in full. " +
    "You are the mate that pack names: be its persona, hunt its hunting ground, " +
    "ride its seed thread across cycles, obey its laws, and honor the STEER row it carries. " +
    "Stop only at thread exhaustion or context budget. " +
    "Before anything else and again when done, follow the pack's receipt contract: " +
    "file your receipt under watch\inbox\mates_leave_protocol\receipts\ with the JOURNEY section " +
    "(threads followed in order, dead ends named, why each turn). " +
    "No em-dashes. Real counts only. No fabricated anything."

Write-MateLog "START mate=$MateId mission=$RelMission opencode=$OpenCode pid=$PID"
& $OpenCode run $Prompt 2>&1 | ForEach-Object {
    $line = "$_".TrimEnd()
    Add-Content -Path $RunLog -Value $line -Encoding utf8
    Write-Host $line
}
$code = $LASTEXITCODE
if ($null -eq $code) { $code = 2 }

$verdict = "exit=$code"
if ($code -eq 0) { $verdict = "exit=0 (runner completed; receipt truth lives in the receipts dir, not here)" }
Add-Content -Path "$($Mission.FullName).claim" -Value "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] mate=$MateId pid=$PID $verdict" -Encoding utf8
Write-MateLog "END mate=$MateId $verdict"
exit $code
