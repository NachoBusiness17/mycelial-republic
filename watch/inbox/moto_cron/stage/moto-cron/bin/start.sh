#!/data/data/com.termux/files/usr/bin/bash
# idempotent launcher for poller + heartbeat (pidfiles)
set -u
ROOT="${HOME}/moto-cron"
BIN="${ROOT}/bin"
LOGS="${ROOT}/logs"
mkdir -p "$ROOT"/{jobs,running,done,failed,logs,bin}

if ! command -v curl >/dev/null 2>&1; then
  if command -v pkg >/dev/null 2>&1; then
    pkg install -y curl >/dev/null 2>&1 || true
  fi
fi

if command -v termux-wake-lock >/dev/null 2>&1; then
  termux-wake-lock >/dev/null 2>&1 || true
fi

start_one() {
  local name="$1" script="$2"
  local pidf="${ROOT}/${name}.pid"
  if [ -f "$pidf" ]; then
    local old
    old="$(cat "$pidf" 2>/dev/null || true)"
    if [ -n "$old" ] && kill -0 "$old" 2>/dev/null; then
      echo "[start] ${name} already running pid=${old}"
      return 0
    fi
    rm -f "$pidf"
  fi
  nohup bash "$script" >> "${LOGS}/${name}.nohup.log" 2>&1 &
  echo $! > "$pidf"
  echo "[start] ${name} pid=$(cat "$pidf")"
}

start_one poller "${BIN}/poller.sh"
start_one heartbeat "${BIN}/heartbeat.sh"
echo "[start] done $(date -u +%Y-%m-%dT%H:%M:%SZ)"
