# audio_channel.ps1 — PowerShell twin of audio_channel.sh (his terminal is PS).
# Drop a track in game_roblox/audio/, run:  powershell -File game_roblox\audio_channel.ps1
# Decodes, measures BPM + energy, uploads if roblox_opencloud key exists,
# regenerates src/shared/AudioManifest.luau (rojo pushes it into the game).
$ErrorActionPreference = "Continue"
$root = Split-Path -Parent $PSScriptRoot   # estate root
$pcm = Join-Path $root "state\fuel\audio_channel_pcm"
New-Item -ItemType Directory -Force -Path $pcm | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $PSScriptRoot "audio") | Out-Null

$ffmpeg = "ffmpeg"
$exts = @("*.mp3", "*.wav", "*.ogg")
foreach ($ext in $exts) {
    Get-ChildItem -Path (Join-Path $PSScriptRoot "audio") -Filter $ext | ForEach-Object {
        $stem = [IO.Path]::GetFileNameWithoutExtension($_.Name)
        $safe = ($stem -replace "[""'/\:\*\?<>|]", "")
        $out = Join-Path $pcm "$safe.wav"
        & $ffmpeg -v error -ss 10 -t 150 -i $_.FullName -ac 1 -ar 2205 -acodec pcm_s16le $out -y 2>$null
        if ($LASTEXITCODE -eq 0) { Write-Host "decoded: $($_.Name)" } else { Write-Host "DECODE FAIL: $($_.Name)" }
    }
}

python (Join-Path $root "tools\audio_channel.py")
