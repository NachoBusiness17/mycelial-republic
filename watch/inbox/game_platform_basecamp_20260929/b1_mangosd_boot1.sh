#!/bin/bash
# B1 cycle 7: mangosd first-boot attempt (deliverable = the failure naming what's needed).
# conf from .dist: DB info -> mangos user / real DB names; DataDir -> empty placeholder.
# Expected: dies on missing client DBCs. The error text IS the deliverable.
set -u
cd /root/mangos-wotlk/build/src/mangosd || exit 1

# 1. Generate mangosd.conf from mangosd.conf.dist
# First attempt taught: mangosd's DEFAULT conf path is ../etc/mangosd.conf (install layout),
# not ./mangosd.conf — first run died "Could not find configuration file ../etc/mangosd.conf".
mkdir -p ../etc
sed -e 's|^LoginDatabaseInfo     = "127.0.0.1;3306;mangos;mangos;wotlkrealmd"|LoginDatabaseInfo     = "127.0.0.1;3306;mangos;mangos;realmd"|' \
    -e 's|^WorldDatabaseInfo     = "127.0.0.1;3306;mangos;mangos;wotlkmangos"|WorldDatabaseInfo     = "127.0.0.1;3306;mangos;mangos;mangos"|' \
    -e 's|^CharacterDatabaseInfo = "127.0.0.1;3306;mangos;mangos;wotlkcharacters"|CharacterDatabaseInfo = "127.0.0.1;3306;mangos;mangos;characters"|' \
    -e 's|^PlayerbotDatabaseInfo = "127.0.0.1;3306;mangos;mangos;wotlkplayerbots"|PlayerbotDatabaseInfo = "127.0.0.1;3306;mangos;mangos;playerbots"|' \
    -e 's|^DataDir = "\."|DataDir = "/root/mangos-data"|' \
    mangosd.conf.dist > ../etc/mangosd.conf
echo "=== conf lines ==="
grep -E '^(Login|World|Character|Playerbot)DatabaseInfo|^DataDir' ../etc/mangosd.conf

# 2. Placeholder DataDir: exists but EMPTY (no DBCs/maps staged)
mkdir -p /root/mangos-data
echo "=== DataDir contents ==="
ls -la /root/mangos-data

# 3. One boot attempt, bounded at 45s, full output banked
timeout 45 ./mangosd > /root/mangosd_boot1.log 2>&1
RC=$?
echo "BOOT_EXIT=$RC   # non-zero = died; 124 = still alive at timeout (killed)"

echo "=== boot log size ==="
wc -l /root/mangosd_boot1.log
echo "=== boot log (full) ==="
cat /root/mangosd_boot1.log

# 4. Bank the log to the shared inbox (canonical receipt surface)
cp /root/mangosd_boot1.log /mnt/c/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/game_platform_basecamp_20260929/mangosd_boot1_20260929.log
echo LOG_BANKED
