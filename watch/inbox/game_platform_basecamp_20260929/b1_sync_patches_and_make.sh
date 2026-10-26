#!/bin/bash
# B1: sync the four Edit-tool-patched files from the canonical repo copy into the WSL build tree, then resume make.
set -e
SRC="/mnt/c/Users/foste/Documents/projects/local_sovereign_agent/corpus/library/mod-playerbots"
DST="$HOME/mangos-wotlk"
cp "$SRC/src/shared/Network/Socket.hpp"    "$DST/src/shared/Network/Socket.hpp"
cp "$SRC/src/realmd/AuthSocket.h"          "$DST/src/realmd/AuthSocket.h"
cp "$SRC/src/shared/Metric/Metric.h"       "$DST/src/shared/Metric/Metric.h"
cp "$SRC/src/shared/Metric/Metric.cpp"     "$DST/src/shared/Metric/Metric.cpp"
echo SYNCED
cd "$DST/build"
make -j12 2>&1 | tail -15
echo "MAKE_EXIT=${PIPESTATUS[0]}"
