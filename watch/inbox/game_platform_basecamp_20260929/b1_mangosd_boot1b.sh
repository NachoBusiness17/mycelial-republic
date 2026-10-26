#!/bin/bash
# B1 cycle 7 run 1b: first boot died on the db_version lineage gate (wotlk-db Full_DB
# db_version columns diverge from the 2021 core's expected required_14034_... column).
# Fix: swap ONLY the db_version table to the core base shape (content tables untouched),
# then boot again. Goal: reach and bank the true DBC error.
set -u
cd /root/mangos-wotlk/build/src/mangosd || exit 1
BANK=/mnt/c/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/game_platform_basecamp_20260929

# 0. Preserve run-1 bytes (byte-truth law)
cp /root/mangosd_boot1.log "$BANK/mangosd_boot1_run1_20260929.log"
echo RUN1_PRESERVED

# 1. Swap world db_version to the core's base shape (from sql/base/mangos.sql lines 22-37)
mariadb mangos <<'SQL'
DROP TABLE IF EXISTS `db_version`;
CREATE TABLE `db_version` (
  `version` varchar(120) DEFAULT NULL,
  `creature_ai_version` varchar(120) DEFAULT NULL,
  `cache_id` int(10) DEFAULT '0',
  `required_14034_01_mangos_column_fix` bit(1) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='Used DB version notes';
INSERT INTO `db_version` VALUES
('Mangos default database.','Creature EventAI not provided.',0,NULL);
SQL
echo DB_VERSION_SWAPPED
mariadb mangos -N -e 'SHOW COLUMNS FROM db_version;'

# 2. Boot attempt (run 2)
timeout 45 ./mangosd > /root/mangosd_boot1.log 2>&1
RC=$?
echo "BOOT_EXIT=$RC   # non-zero = died; 124 = still alive at timeout (killed)"

echo "=== boot log lines ==="
wc -l /root/mangosd_boot1.log
echo "=== boot log (full) ==="
cat /root/mangosd_boot1.log

# 3. Bank the definitive boot log
cp /root/mangosd_boot1.log "$BANK/mangosd_boot1_20260929.log"
echo LOG_BANKED
