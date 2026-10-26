#!/usr/bin/env bash
# Containerized build of tortoise-wow (the TurtleWoW 1.18.1 community server core).
# Operator order 2026-10-10: "self steal our wow backend... i just want this done."
# Docker route because WSL needs a sudo password we do not ask for, and the fleet
# order says these things run in docker anyway. Source mounts from the Windows
# clone; artifacts land in the named volume tortoise-build-out.
set -e
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq g++ cmake make libace-dev libmysqlclient-dev \
  libssl-dev zlib1g-dev libbz2-dev libtool automake > /dev/null
cmake -B /out -S /src -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/out-install -DTOOLS=1
echo CONFIG-OK
cmake --build /out -j"$(nproc)"
echo "BUILD-EXIT-$?"
ls -la /out/bin 2>/dev/null || true
