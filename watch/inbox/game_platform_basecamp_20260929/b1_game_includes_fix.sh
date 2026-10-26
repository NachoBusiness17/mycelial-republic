#!/bin/bash
# B1: sync patched game CMakeLists, reconfigure bots-off, build everything.
set -e
SRC="/mnt/c/Users/foste/Documents/projects/local_sovereign_agent/corpus/library/mod-playerbots"
DST="$HOME/mangos-wotlk"
cp "$SRC/src/game/CMakeLists.txt" "$DST/src/game/CMakeLists.txt"
echo SYNCED
cd "$DST/build"
cmake .. -DCMAKE_POLICY_VERSION_MINIMUM=3.5 -DCMAKE_INSTALL_PREFIX=$HOME/mangos-run -DBUILD_IKE3_BOTS=OFF 2>&1 | tail -3
make -j8 2>&1 | grep -E "error:|Error [12]|Built target (mangosd|realmd|game|scripts|shared)" | tail -12
echo "MAKE_EXIT=${PIPESTATUS[0]}"
find . -type f -executable \( -name mangosd -o -name realmd \) -exec ls -la {} \;
