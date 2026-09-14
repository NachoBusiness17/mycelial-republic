#!/usr/bin/env bash
# scripts/hofw_001_seed.sh — driver for HOFW-001 seed build
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

SEAT_ID="hofw_001"
CONFIG="$ROOT/configs/seat_fork.yaml"
RECEIPT="$ROOT/memory/runs/hermes_jobs/${SEAT_ID}_receipt.jsonl"
BRIEF="$ROOT/memory/briefs/${SEAT_ID}_brief.md"

# 1) Fork the seat
FORK_TIP=$(python -m mag.seat_fork "$CONFIG")
echo "Forked seat tip: $FORK_TIP"

# 2) Verify brief and receipt exist
if [[ ! -f "$BRIEF" ]]; then
  echo "ERROR: brief not written at $BRIEF" >&2
  exit 1
fi
if [[ ! -f "$RECEIPT" ]]; then
  echo "ERROR: receipt not written at $RECEIPT" >&2
  exit 1
fi

# 3) Update receipt end_time (simulate start)
T_START=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
python -c "
import json
from pathlib import Path
p=Path('$RECEIPT')
r=json.loads(p.read_text())
r['start_time']='$T_START'
r['status']='running'
p.write_text(json.dumps(r,indent=2)+'\n')
"

echo "HOFW-001 seed started: $SEAT_ID"
echo "Frozen tip: $(yq -r .frozen_tip_hash "$CONFIG")"
echo "Persona: $(yq -r .persona "$CONFIG")"
echo "Wave width: $(yq -r .wave_width "$CONFIG")"
