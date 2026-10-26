#!/bin/bash
# B1: full canonical -> WSL sync (src + cmake lists), reconfigure bots-ON, build, error ledger.
SRC="/mnt/c/Users/foste/Documents/projects/local_sovereign_agent/corpus/library/mod-playerbots"
DST="$HOME/mangos-wotlk"
cp -r "$SRC/src/." "$DST/src/"
cp "$SRC/CMakeLists.txt" "$DST/CMakeLists.txt"
mkdir -p "$DST/cmake/macros" && cp "$SRC/cmake/macros/cotire.cmake" "$DST/cmake/macros/cotire.cmake"
echo SYNCED
cd "$DST/build"
cmake .. -DCMAKE_POLICY_VERSION_MINIMUM=3.5 -DCMAKE_INSTALL_PREFIX=$HOME/mangos-run -DBUILD_IKE3_BOTS=ON -DCMAKE_CXX_FLAGS="-Wno-error=template-body -Wno-error=deprecated-declarations -Wno-error=conversion-null -Wno-error=narrowing" 2>&1 | tail -2
make -j8 2>&1 | grep -E "error:" | sort -u | head -12
echo "MAKE_EXIT=${PIPESTATUS[0]}"
find . -type f -executable \( -name mangosd -o -name realmd \) -exec ls -la {} \;
