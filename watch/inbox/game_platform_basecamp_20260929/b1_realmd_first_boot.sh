#!/bin/bash
# B1: first server boot - realmd binds :3724. Account row minimal (SRP6 v/s computed client-side later = B2 lane).
set -e
mariadb realmd -e "INSERT IGNORE INTO account (username, v, s, expansion, gmlevel) VALUES ('estate', '', '', 2, 3);"
echo ACCOUNT_ROW_OK
cd ~/mangos-wotlk/build/src/realmd
timeout 15 ./realmd 2>&1 | head -30 || true
echo "REALMD_SMOKE_DONE"
