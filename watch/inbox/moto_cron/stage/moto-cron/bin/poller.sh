#!/data/data/com.termux/files/usr/bin/bash
# moto-cron poller: claim jobs/*.job, run by FLAG, write results + outbox
set -u
ROOT="${HOME}/moto-cron"
JOBS="${ROOT}/jobs"
RUNNING="${ROOT}/running"
DONE="${ROOT}/done"
FAILED="${ROOT}/failed"
LOGS="${ROOT}/logs"
OUTBOX="${ROOT}/outbox.log"
POLL_SEC=30
SHELL_TIMEOUT=300
SUMMARY_CAP=4096

mkdir -p "$JOBS" "$RUNNING" "$DONE" "$FAILED" "$LOGS"
touch "$OUTBOX"

log_line() {
  local ts
  ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf '%s %s %s %s %s %s\n' "$ts" "$1" "$2" "$3" "$4" "$5" >> "$OUTBOX"
}

cap_summary() {
  local s="$1"
  if [ "${#s}" -gt "$SUMMARY_CAP" ]; then
    printf '%s…[truncated]' "${s:0:$SUMMARY_CAP}"
  else
    printf '%s' "$s"
  fi
}

parse_manifest() {
  FLAG=""; PAYLOAD=""; NOTIFY=""; ID=""
  while IFS= read -r line || [ -n "$line" ]; do
    case "$line" in
      ''|\#*) continue ;;
    esac
    key="${line%%=*}"
    val="${line#*=}"
    case "$key" in
      FLAG) FLAG="$val" ;;
      PAYLOAD) PAYLOAD="$val" ;;
      NOTIFY) NOTIFY="$val" ;;
      ID) ID="$val" ;;
    esac
  done < "$1"
}

run_fetch() {
  local url="$1" out="$2"
  local http body_tmp code size sha
  body_tmp="$(mktemp)"
  http="$(curl -sL -w '%{http_code}' -o "$body_tmp" --max-time 120 "$url" 2>"${out}.err" || true)"
  code="${http:-000}"
  if [ ! -s "$body_tmp" ] && [ "$code" = "000" ]; then
    echo "curl failed" > "$out"
    rm -f "$body_tmp"
    echo "000|0|"
    return 1
  fi
  mv "$body_tmp" "$out"
  size="$(wc -c < "$out" | tr -d ' ')"
  if command -v sha256sum >/dev/null 2>&1; then
    sha="$(sha256sum "$out" | awk '{print $1}')"
  else
    sha="nosha"
  fi
  echo "${code}|${size}|${sha}"
  return 0
}

run_probe() {
  local target="$1"
  local host rc=1 notes="" curl_rc=1 curl_code="000"
  host="$target"
  case "$host" in
    http://*|https://*)
      host="${host#*://}"
      host="${host%%/*}"
      host="${host%%:*}"
      ;;
  esac
  if command -v ping >/dev/null 2>&1; then
    if ping -c 2 -W 3 "$host" >/tmp/moto_probe_ping.$$ 2>&1; then
      notes="ping=ok"
      rc=0
    else
      notes="ping=fail"
    fi
  else
    notes="ping=unavailable"
  fi
  if command -v curl >/dev/null 2>&1; then
    case "$target" in
      http://*|https://*)
        curl_code="$(curl -sL -o /dev/null -w '%{http_code}' --max-time 15 "$target" 2>/dev/null || true)"; [ -z "$curl_code" ] && curl_code="000"
        ;;
      *)
        curl_code="$(curl -sL -o /dev/null -w '%{http_code}' --max-time 15 "http://${host}/" 2>/dev/null || true)"; [ -z "$curl_code" ] && curl_code="000"
        ;;
    esac
    case "$curl_code" in 000|"") ;; *) curl_rc=0 ;; esac
    notes="${notes};curl_http=${curl_code}"
  else
    notes="${notes};curl=unavailable"
  fi
  echo "$notes"
  if [ "$rc" -eq 0 ] || [ "$curl_rc" -eq 0 ]; then
    return 0
  fi
  return 1
}

run_render() {
  local payload="$1" out="$2"
  {
    echo "# FLAG_RENDER stub — payload written as-is"
    echo "# ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    printf '%s\n' "$payload"
  } > "$out"
  echo "stub_bytes=$(wc -c < "$out" | tr -d ' ')"
  return 0
}

run_shell() {
  local cmd="$1" out="$2" rc
  set +e
  if command -v timeout >/dev/null 2>&1; then
    timeout "$SHELL_TIMEOUT" bash -c "$cmd" >"$out" 2>&1
  else
    bash -c "$cmd" >"$out" 2>&1
  fi
  rc=$?
  set -e
  echo "shell_exit=${rc};out_bytes=$(wc -c < "$out" | tr -d ' ')"
  return "$rc"
}

process_one() {
  local jobpath="$1"
  local base name claim
  base="$(basename "$jobpath")"
  name="${base%.job}"
  claim="${RUNNING}/${base}"
  if ! mv "$jobpath" "$claim" 2>/dev/null; then
    return 0
  fi
  parse_manifest "$claim"
  if [ -z "$FLAG" ] || [ -z "$ID" ]; then
    local endts
    endts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    printf 'flag=%s\nid=%s\nnotify=%s\nstart=%s\nend=%s\nexit=2\nsummary=bad_manifest\n' \
      "${FLAG:-}" "${ID:-}" "${NOTIFY:-}" "$endts" "$endts" > "${FAILED}/BAD__${name}__${endts}.result"
    log_line "${NOTIFY:-none}" "${FLAG:-NONE}" "${ID:-none}" "failed" "bad_manifest"
    rm -f "$claim"
    return 0
  fi
  NOTIFY="${NOTIFY:-none}"
  local start end exitc=0 summary="" outf fts dest status
  start="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  outf="${LOGS}/${FLAG}__${ID}__work.out"
  : > "$outf"
  set +e
  case "$FLAG" in
    FLAG_FETCH) summary="$(run_fetch "$PAYLOAD" "$outf")"; exitc=$? ;;
    FLAG_PROBE) summary="$(run_probe "$PAYLOAD")"; exitc=$? ;;
    FLAG_RENDER) summary="$(run_render "$PAYLOAD" "$outf")"; exitc=$? ;;
    FLAG_SHELL) summary="$(run_shell "$PAYLOAD" "$outf")"; exitc=$? ;;
    *) summary="unknown_flag"; exitc=3 ;;
  esac
  set -e
  end="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  fts="$(date -u +%Y%m%dT%H%M%SZ)"
  summary="$(cap_summary "$summary")"
  if [ "$exitc" -eq 0 ]; then
    dest="${DONE}/${FLAG}__${ID}__${fts}.result"
    status="ok"
  else
    dest="${FAILED}/${FLAG}__${ID}__${fts}.result"
    status="failed"
  fi
  {
    echo "flag=${FLAG}"
    echo "id=${ID}"
    echo "notify=${NOTIFY}"
    echo "start=${start}"
    echo "end=${end}"
    echo "exit=${exitc}"
    echo "summary=${summary}"
    if [ -s "$outf" ] && [ "$(wc -c < "$outf" | tr -d ' ')" -le 2048 ]; then
      echo "---- output ----"
      cat "$outf"
    elif [ -s "$outf" ]; then
      echo "---- output_head ----"
      head -c 2048 "$outf"
      echo
      echo "---- (truncated) ----"
    fi
  } > "$dest"
  log_line "$NOTIFY" "$FLAG" "$ID" "$status" "$summary"
  rm -f "$claim" "$outf" "${outf}.err"
}

main_loop() {
  echo "[poller] start $(date -u +%Y-%m-%dT%H:%M:%SZ) root=$ROOT" >> "${LOGS}/poller.log"
  while true; do
    shopt -s nullglob
    for j in "$JOBS"/*.job; do
      process_one "$j"
    done
    shopt -u nullglob
    sleep "$POLL_SEC"
  done
}

main_loop
