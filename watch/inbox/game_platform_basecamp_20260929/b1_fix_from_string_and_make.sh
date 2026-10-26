#!/bin/bash
# B1 fix 3 (2026-09-29): Boost 1.90 removed address::from_string / address_v4::from_string
# (deprecated since Boost 1.66). Modern equivalents: make_address / make_address_v4.
set -e
SRC="/mnt/c/Users/foste/Documents/projects/local_sovereign_agent/corpus/library/mod-playerbots"
DST="$HOME/mangos-wotlk"
sed -i 's/boost::asio::ip::address_v4::from_string/boost::asio::ip::make_address_v4/g' "$SRC/src/game/Server/WorldSession.cpp"
sed -i 's/boost::asio::ip::address::from_string/boost::asio::ip::make_address/g' "$SRC/src/shared/Network/Listener.hpp" "$SRC/src/shared/Util.cpp"
echo RENAMED
grep -rn "from_string" "$SRC/src/" || echo ZERO_REMAINING
cp -r "$SRC/src/." "$DST/src/"
echo SYNCED
cd "$DST/build"
make -j12 2>&1 | grep -vE "^\[|^-- " | tail -18
echo "MAKE_EXIT=${PIPESTATUS[0]}"
