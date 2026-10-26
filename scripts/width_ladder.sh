#!/bin/bash
# width_ladder - the width experiment: fire equal ask batches at width 2, 4, 8
# and time each. The width law's free-tier annex, measured (2026-10-16).
set -u
cd "C:/Users/foste/Documents/projects/local_sovereign_agent"
# integer-only args: kills the injection class the scanner flagged (lines 15/27)
case "${1:-50}" in ''|*[!0-9]*) echo "bad width arg"; exit 2;; esac
case "${2:-8}" in ''|*[!0-9]*) echo "bad count arg"; exit 2;; esac
PY=".venv/Scripts/python.exe"
ROOT_Q="queue/hermes_247_free_wide"

run_batch() {
  local width=$1 count=$2
  local asks=()
  for d in $(ls -d "$ROOT_Q"/H247_STACK* 2>/dev/null | grep -v _worker | head -$count); do
    asks+=("$d")
  done
  rm -rf "$ROOT_Q"/_worker*
  local w=0
  for d in "${asks[@]}"; do
    mkdir -p "$ROOT_Q/_worker$((w % width))"
    mv "$d" "$ROOT_Q/_worker$((w % width))/" 2>/dev/null
    w=$((w + 1))
  done
  local t0=$(date +%s)
  "$PY" tools/batch_fire.py --root "$ROOT_Q" --width $width > /tmp/ladder_w$width.log 2>&1
  local t1=$(date +%s)
  echo "WIDTH $width: $((t1 - t0))s for $count asks"
  find "$ROOT_Q"/_worker* -maxdepth 1 -type d -name "H247_*" -exec mv {} "$ROOT_Q"/ \; 2>/dev/null
  rm -rf "$ROOT_Q"/_worker*
}

echo "=== WIDTH 2 (8 asks) ==="
run_batch 2 8
echo "=== WIDTH 4 (8 asks) ==="
run_batch 4 8
echo "=== WIDTH 8 (8 asks) ==="
run_batch 8 8
echo "=== landed stack outputs ==="
ls watch/inbox/hermes_burn/ | grep -c "H247_STACK" | xargs echo "stack outputs:"
