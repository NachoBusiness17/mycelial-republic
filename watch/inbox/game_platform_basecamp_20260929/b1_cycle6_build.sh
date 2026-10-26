#!/bin/bash
# B1 cycle-6 rebuild: sync canonical -> WSL, incremental make -k, census.
# NOTE: Metric.h is in the game PCH chain -> game PCH rebuilds -> full game TU sweep.
# -j6 (not -j8): the -j8 run OOM-killed WSL (0x8007000e) with the host loaded.
SRC=/mnt/c/Users/foste/Documents/projects/local_sovereign_agent/corpus/library/mod-playerbots
DST=/root/mangos-wotlk
cp -r "$SRC/src/." "$DST/src/"
cp "$SRC/CMakeLists.txt" "$DST/CMakeLists.txt"
mkdir -p "$DST/cmake/macros" && cp "$SRC/cmake/macros/cotire.cmake" "$DST/cmake/macros/cotire.cmake"
echo SYNCED
cd "$DST/build" || exit 1
make -k -j6 > /root/build_cycle6.log 2>&1
MAKE_RC=$?
echo MAKE_EXIT=$MAKE_RC
echo "unique error lines: $(grep 'error:' /root/build_cycle6.log | sort -u | wc -l)"
echo "make failure lines:"
grep -E '\*\*\*.*Error [0-9]' /root/build_cycle6.log | sort -u | head -10
echo "libBots archive:"
find "$DST/build" -name "libBots*" -exec ls -la {} \; 2>/dev/null
echo "binaries:"
find "$DST/build" -type f \( -name mangosd -o -name realmd \) -exec ls -la {} \; 2>/dev/null
