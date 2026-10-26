#!/data/data/com.termux/files/usr/bin/bash
export PREFIX=/data/data/com.termux/files/usr
export HOME=/data/data/com.termux/files/home
LIST=$PREFIX/tmp/lkm_files.txt
: > "$LIST"
find "$HOME/lite-caller" -type f 2>/dev/null >>"$LIST"
find "$HOME" -type f \
  ! -path '*/gstdbot/node_modules/*' \
  ! -path '*/.git/*' \
  ! -name 'lkm_audit.py' \
  ! -name 'lkm_body.py' \
  ! -name 't90_inv.sh' \
  ! -name 'lkm_scan.sh' \
  ! -name 'lkm_files.txt' \
  2>/dev/null >>"$LIST"
find "$PREFIX/tmp" -type f \
  ! -name 'lkm_audit.py' ! -name 'lkm_body.py' ! -name 't90_inv.sh' ! -name 'lkm_files.txt' ! -name 'lkm_scan.sh' \
  2>/dev/null >>"$LIST"
for d in /storage/emulated/0/Download /storage/emulated/0/Documents; do
  [ -d "$d" ] && find "$d" -type f 2>/dev/null | head -5000 >>"$LIST"
done
sort -u "$LIST" -o "$LIST"
echo FILES_QUEUED $(wc -l <"$LIST")
# stdin = key line; python reads it
python3 "$PREFIX/tmp/lkm_body.py" "$LIST"
rc=$?
rm -f "$LIST"
exit $rc