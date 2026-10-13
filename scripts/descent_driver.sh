#!/usr/bin/env bash
# descent_driver.sh - the autonomous descent loop (2026-10-01).
# Why this exists: the descent must complete without a seat's context window
# alive. Grinds every ask dir under memory/plans/hermes_burn_* (skip = output
# exists), then any pending ds_workhorse items, in a cycle until the STOP
# file appears. Every turn banks tokens+cost in the ledger (the law's leg 8).
# The seat stages new legs into the queue dirs; the driver never invents asks.
cd "$(dirname "$0")/.." || exit 2

# PIDFILE GUARD (2026-10-02, ractor dogfood finding: two same-second twins
# double-drained the shared hermes_burn queue for 12h, no claim lock existed).
# Second instance exits loud instead of double-spending paid keys.
PIDFILE="state/descent_driver.pid"
if [ -f "$PIDFILE" ]; then
  OLDPID=$(cat "$PIDFILE" 2>/dev/null)
  if [ -n "$OLDPID" ] && kill -0 "$OLDPID" 2>/dev/null; then
    echo "DESCENT-DRIVER: instance $OLDPID already running; refusing to start." >&2
    exit 3
  fi
  echo "DESCENT-DRIVER: stale pidfile ($OLDPID dead); reclaiming." >&2
fi
echo $$ > "$PIDFILE"
trap 'rm -f "$PIDFILE"' EXIT
PY=.venv/Scripts/python.exe
STOP=memory/runs/hermes_burn/DRIVER_STOP
LOG=memory/runs/hermes_burn/driver.log
mkdir -p memory/runs/hermes_burn
cycle=0
while [ ! -f "$STOP" ]; do
  cycle=$((cycle+1))
  echo "[driver cycle $cycle $(date -u +%H:%M:%SZ)]" >> "$LOG"
  echo "BEAT $(date -u +%Y-%m-%dT%H:%M:%SZ) cycle=$cycle" >> memory/runs/hermes_burn/driver.beat
  for q in memory/plans/hermes_burn_*; do
    [ -d "$q" ] || continue
    "$PY" tools/hermes_burn.py "$q" >> "$LOG" 2>&1
  done
  if [ -f memory/runs/hermes_burn/pending_items.jsonl ]; then
    "$PY" tools/ds_workhorse.py run --in memory/runs/hermes_burn/pending_items.jsonl \
      --prompt-file memory/runs/hermes_burn/ds_baseline_prompt.md \
      --out "memory/runs/hermes_burn/pending_out_$(date -u +%H%M).jsonl" >> "$LOG" 2>&1
    mv memory/runs/hermes_burn/pending_items.jsonl memory/runs/hermes_burn/pending_last.jsonl 2>/dev/null
  fi
  sleep 45
done
echo "[driver stopped $(date -u +%H:%M:%SZ)]" >> "$LOG"
