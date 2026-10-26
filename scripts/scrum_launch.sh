#!/bin/bash
# scrum_launch - launch N headless browser instances (the scrum swarm's legs).
# Each instance: separate profile (no cookie collisions), separate debug port
# (drivable per-tab), headless. The stealth driver v2 rides these when built.
# Usage: bash scripts/scrum_launch.sh [N] [start_port]
set -u
N="${1:-4}"
PORT="${2:-9222}"
CHROME="/c/Program Files/Google/Chrome/Application/chrome.exe"
BASE="/c/Users/foste/scrum_profiles"
[ -x "$CHROME" ] || { echo "chrome not found"; exit 1; }
mkdir -p "$BASE"
launched=0
for i in $(seq 0 $((N - 1))); do
  prof="$BASE/team_$i"
  port=$((PORT + i))
  mkdir -p "$prof"
  "$CHROME" --headless=new --user-data-dir="$prof" --remote-debugging-port=$port \
    --no-first-run --no-default-browser-check --disable-gpu \
    about:blank > /dev/null 2>&1 &
  echo "team_$i: headless on debug port $port (profile $prof)"
  launched=$((launched + 1))
  sleep 1
done
echo "$launched headless legs up. Drive them via http://localhost:$PORT (CDP per tab)."
echo "Stop: powershell -Command \"Get-Process chrome | Where-Object {\$_.CommandLine -like '*scrum_profiles*'} | Stop-Process -Force\""
