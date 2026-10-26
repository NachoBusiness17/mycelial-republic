#!/bin/bash
# B1: sync cotire fix + reconfigure (cotire patch changes cmake module) + build Bots then all
set -e
SRC="/mnt/c/Users/foste/Documents/projects/local_sovereign_agent/corpus/library/mod-playerbots"
DST="$HOME/mangos-wotlk"
cp "$SRC/cmake/macros/cotire.cmake" "$DST/cmake/macros/cotire.cmake"
echo SYNCED
cd "$DST/build"
cmake .. -DCMAKE_POLICY_VERSION_MINIMUM=3.5 -DCMAKE_INSTALL_PREFIX=$HOME/mangos-run -DBUILD_IKE3_BOTS=ON 2>&1 | tail -3
make -j8 2>&1 | grep -E "error|Error|Built target mangosd|Built target Bots|Built target realmd|Built target game|Built target scripts" | tail -15
echo "MAKE_EXIT=${PIPESTATUS[0]}"
find . -type f -executable \( -name mangosd -o -name realmd \) -exec ls -la {} \;
