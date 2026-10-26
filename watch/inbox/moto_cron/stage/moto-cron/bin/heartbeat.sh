#!/data/data/com.termux/files/usr/bin/bash
# moto-cron heartbeat: ISO ts + uptime + battery every 15 min
set -u
ROOT="${HOME}/moto-cron"
HB="${ROOT}/heartbeat"
LOGS="${ROOT}/logs"
INTERVAL=900

mkdir -p "$ROOT" "$LOGS"

write_hb() {
  local ts up batt
  ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  if [ -r /proc/uptime ]; then
    up="$(awk '{print $1}' /proc/uptime)"
  else
    up="unknown"
  fi
  batt="n/a"
  if command -v termux-battery-status >/dev/null 2>&1; then
    batt="$(termux-battery-status 2>/dev/null | tr '\n' ' ' | sed 's/  */ /g')"
    [ -z "$batt" ] && batt="n/a"
  fi
  {
    echo "ts=${ts}"
    echo "uptime_sec=${up}"
    echo "battery=${batt}"
  } > "$HB"
  echo "[heartbeat] ${ts} up=${up}" >> "${LOGS}/heartbeat.log"
}

echo "[heartbeat] start $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "${LOGS}/heartbeat.log"
while true; do
  write_hb
  sleep "$INTERVAL"
done
