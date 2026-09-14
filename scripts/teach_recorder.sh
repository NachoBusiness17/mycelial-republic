#!/bin/bash
# teach_recorder.sh — chunked screen recording of the emulator while the
# operator demonstrates. 175s chunks (under the 180s screenrecord cap),
# up to 40 chunks (~2h), pulled to Documents/projects/teach/.
# Run: bash teach_recorder.sh [serial]   Stop: kill the task; last chunk
# lands on the next pull pass.
SERIAL="${1:-emulator-5554}"
DEST="$USERPROFILE/Documents/projects/teach"
mkdir -p "$DEST"
ADB="$LOCALAPPDATA/Android/Sdk/platform-tools/adb.exe"
export MSYS_NO_PATHCONV=1  # Git Bash rewrites /sdcard/... into C:\...\Git\sdcard\... — the silent pull-killer (proven 09-05)
for i in $(seq -w 1 40); do
  echo "chunk $i start $(date -u +%H:%M:%SZ)"
  timeout 200 "$ADB" -s "$SERIAL" shell "screenrecord --time-limit 175 /sdcard/teach_$i.mp4"  # hung adb must never eat the watch again (9h loss 09-04)
  timeout 60 "$ADB" -s "$SERIAL" pull "/sdcard/teach_$i.mp4" "$DEST/teach_$i.mp4"
  if [ -s "$DEST/teach_$i.mp4" ]; then
    "$ADB" -s "$SERIAL" shell rm "/sdcard/teach_$i.mp4" 2>/dev/null
  else
    echo "chunk $i PULL FAILED — recording left on device at /sdcard/teach_$i.mp4"
  fi
done
echo "recorder done"
