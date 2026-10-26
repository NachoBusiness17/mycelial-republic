# THE WOW BACKEND SELF-STEAL + BUILD (operator order, 2026-10-10: "self steal our wow backend can we stop night crewing shit i just want this done")

## What we hold (the self-steal findings, disk-verified this sitting)

- projects/tortoise-wow = the community restoration of the FINAL Turtle-WoW server
  (1.18.1 build 7272, ported from AzerothCore + VMaNGOS; README names its own target
  client and ships a DBC verifier + SHA-256 manifest). CMake source, dep/ vendors
  fmt/re2/libmpq/recast but NOT ACE.
- C:/Games/TurtleWoW = the MATCHING CLIENT (WoW.exe + base.MPQ, dbc.MPQ, backup.MPQ,
  fonts.MPQ, Interface). The pairing is complete on disk: core + client.
- projects/azerothcore-wow = the OTHER leg (WotLK 3.3.5 core with docker compose),
  but NO 3.3.5 client exists on any local drive (searched): that leg stays parked
  until a 3.3.5 client arrives. The executable lineage tonight is TORTOISE.
- The GWAP 202/202 replay assets were not found in the quick receipt grep - their
  location stays an open item for the moat wiring later.

## The build (fired, live)

Route history, honest: WSL had the full toolchain but (a) the VM idles out between
invocations killing nohup'd builds, and (b) ACE is missing and apt needs a sudo
password we do not ask the operator for. DOCKER route chosen (also the fleet order:
these things run in docker): scripts/tortoise_docker_build.sh, container tortoise-build
on ubuntu:24.04, source mounted read-only from the Windows clone, artifacts to the
named volume tortoise-build-out, Release + TOOLS=1 (mapextractor included for DBC).
First attempt hit git-bash path mangling (/build.sh -> Program Files); fixed with
MSYS_NO_PATHCONV=1. Build log: docker logs tortoise-build.

## Done, defined (the ladder to "done" after binaries exist)

1. Binaries in tortoise-build-out volume (worldserver, realmd, mapextractor).
2. MySQL: the estate already runs docker mysql pattern (ac-database shape); create
   the DBs from sql/create_databases.sql + import the repo's sql/ dumps.
3. DBC: mapextractor against C:/Games/TurtleWoW MPQs (README: DBC-only extraction
   is the quick legal path; their dbc_verifier.py checks the versions).
4. realmd + worldserver configs, accounts, then the CLIENT CONNECT TEST - operator
   hands on the GUI (point the client's realmlist at the LAN server).

## Falsifier

If the container build fails on a missing dep beyond the installed set, the script's
apt line grows that dep - never a second container. If the client rejects the server
build (wrong DBC), the repo's own dbc_verifier is the arbiter, not eyeballs.
