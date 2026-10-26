#!/bin/bash
# B1 fix 2 (2026-09-29): Boost 1.90 removed boost::asio::io_service (deprecated typedef of io_context,
# identical API for this code era). Mechanical rename across the canonical tree, full src resync, resume.
set -e
SRC="/mnt/c/Users/foste/Documents/projects/local_sovereign_agent/corpus/library/mod-playerbots"
DST="$HOME/mangos-wotlk"
grep -rl 'boost::asio::io_service' "$SRC/src/" | while read -r f; do
  sed -i 's/boost::asio::io_service/boost::asio::io_context/g' "$f"
done
echo RENAMED
grep -rc 'boost::asio::io_service' "$SRC/src/" 2>/dev/null | grep -v ':0' || echo ZERO_REMAINING
cp -r "$SRC/src/." "$DST/src/"
echo SYNCED
cd "$DST/build"
make -j12 2>&1 | tail -15
echo "MAKE_EXIT=${PIPESTATUS[0]}"
