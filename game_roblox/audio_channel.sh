#!/usr/bin/env bash
# audio_channel.sh — the ONE command for the shadertoy audio channel.
# Drop a track in game_roblox/audio/, run this, rojo pushes the manifest.
# Uploads fire only when configs/keys.json has roblox_opencloud.
set -uo pipefail
cd "$(dirname "$0")/.."

PCM=state/fuel/audio_channel_pcm
mkdir -p "$PCM" game_roblox/audio

shopt -s nullglob
for f in game_roblox/audio/*.mp3 game_roblox/audio/*.wav game_roblox/audio/*.ogg; do
  name=$(basename "$f")
  stem="${name%.*}"
  safe=$(printf '%s' "$stem" | tr -d "'\"/:*?<>|")
  ffmpeg -v error -ss 10 -t 150 -i "$f" -ac 1 -ar 2205 -acodec pcm_s16le "$PCM/${safe}.wav" -y 2>/dev/null \
    && echo "decoded: $name" || echo "DECODE FAIL: $name"
done

python tools/audio_channel.py
