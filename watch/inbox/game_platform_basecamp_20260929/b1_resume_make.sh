#!/bin/bash
# B1 generic resume: canonical src -> build tree, make -j12, show tail + real exit.
set -e
SRC="/mnt/c/Users/foste/Documents/projects/local_sovereign_agent/corpus/library/mod-playerbots"
DST="$HOME/mangos-wotlk"
cp -r "$SRC/src/." "$DST/src/"
echo SYNCED
cd "$DST/build"
make -j12 2>&1 | grep -vE "^\[|^-- " | tail -18
echo "MAKE_EXIT=${PIPESTATUS[0]}"
