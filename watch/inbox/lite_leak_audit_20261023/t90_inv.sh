#!/data/data/com.termux/files/usr/bin/bash
export PREFIX=/data/data/com.termux/files/usr
export HOME=/data/data/com.termux/files/home
echo ====parse.py====
cat "$HOME/lite-caller/parse.py"
echo ====heartbeat.sh====
cat "$HOME/lite-caller/heartbeat.sh"
echo ====start.sh====
cat "$HOME/lite-caller/start.sh"
echo ====BEARER_COUNT====
grep -c Bearer "$HOME/lite-caller/heartbeat.log" || true
echo ====HB_REDACT====
# redact Authorization bearer tokens and long alnum runs after Bearer
sed -E 's/(Bearer )[A-Za-z0-9._+-]{8,}/\1[REDACTED]/g' "$HOME/lite-caller/heartbeat.log"
echo ====HOME_FILES====
find "$HOME" -type f 2>/dev/null | head -300
echo ====TMP_FILES====
find "$PREFIX/tmp" -type f 2>/dev/null | head -100
echo ====PY====
which python3 python; python3 --version 2>&1; python --version 2>&1
echo ====FLASH====
ls -la "$HOME/lite-caller"/.[!.]* 2>&1 || true