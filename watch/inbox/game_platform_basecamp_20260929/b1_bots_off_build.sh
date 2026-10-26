#!/bin/bash
# B1: bots module OFF for first server build. GCC 15 port of the 2022 bots code = its own lane
# (known-error ledger: TravelNode.h:294 extra qualification; LastMovementValue.h:106 rvalue ref bind;
#  Value.h instantiation errors). mangosd + realmd are the prize tonight.
set -e
cd "$HOME/mangos-wotlk/build"
cmake .. -DCMAKE_POLICY_VERSION_MINIMUM=3.5 -DCMAKE_INSTALL_PREFIX=$HOME/mangos-run -DBUILD_IKE3_BOTS=OFF 2>&1 | tail -3
make -j8 2>&1 | grep -E "error:|Error [12]|Built target (mangosd|realmd|game|scripts|shared)" | tail -12
echo "MAKE_EXIT=${PIPESTATUS[0]}"
find . -type f -executable \( -name mangosd -o -name realmd \) -exec ls -la {} \;
