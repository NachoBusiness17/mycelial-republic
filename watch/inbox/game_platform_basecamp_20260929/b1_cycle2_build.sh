#!/bin/bash
# B1 cycle-2 rebuild: sync canonical -> WSL tree, reconfigure, make -k full sweep.
SRC=/mnt/c/Users/foste/Documents/projects/local_sovereign_agent/corpus/library/mod-playerbots
DST=/root/mangos-wotlk
cp -r "$SRC/src/." "$DST/src/"
cp "$SRC/CMakeLists.txt" "$DST/CMakeLists.txt"
mkdir -p "$DST/cmake/macros" && cp "$SRC/cmake/macros/cotire.cmake" "$DST/cmake/macros/cotire.cmake"
echo SYNCED
cd "$DST/build" || exit 1
cmake .. -DCMAKE_POLICY_VERSION_MINIMUM=3.5 -DCMAKE_INSTALL_PREFIX=$HOME/mangos-run -DBUILD_IKE3_BOTS=ON -DCMAKE_CXX_FLAGS="-Wno-error=template-body -Wno-error=deprecated-declarations -Wno-error=conversion-null -Wno-error=narrowing" > /tmp/cmake_cycle2.log 2>&1
echo CMAKE_EXIT=$?
make -k -j8 > /root/build_cycle2.log 2>&1
echo MAKE_EXIT=$?
echo "unique error lines: $(grep 'error:' /root/build_cycle2.log | sort -u | wc -l)"
find . -type f \( -name mangosd -o -name realmd \) -exec ls -la {} \;
