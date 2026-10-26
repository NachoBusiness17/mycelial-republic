#!/bin/bash
# B1: GCC 15 -Wtemplate-body type-checks uninstantiated templates (2022 bots code assumed
# permissive two-phase lookup). Downgrade to warnings, keep everything else.
set -e
cd "$HOME/mangos-wotlk/build"
cmake .. -DCMAKE_POLICY_VERSION_MINIMUM=3.5 -DCMAKE_INSTALL_PREFIX=$HOME/mangos-run -DBUILD_IKE3_BOTS=ON -DCMAKE_CXX_FLAGS="-Wno-error=template-body -Wno-error=deprecated-declarations -Wno-error=conversion-null -Wno-error=narrowing" 2>&1 | tail -3
make -j8 2>&1 | grep -E "error:|Built target (mangosd|Bots|realmd|game|scripts)|Error [12]" | tail -15
echo "MAKE_EXIT=${PIPESTATUS[0]}"
find . -type f -executable \( -name mangosd -o -name realmd \) -exec ls -la {} \;
