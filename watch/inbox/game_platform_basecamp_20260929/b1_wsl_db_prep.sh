#!/bin/bash
# B1 DB prep in WSL MariaDB (base + bots schemas; world content loaded separately)
set -e
M="mariadb"
$M -e "CREATE DATABASE IF NOT EXISTS realmd; CREATE DATABASE IF NOT EXISTS characters; CREATE DATABASE IF NOT EXISTS mangos; CREATE DATABASE IF NOT EXISTS playerbots;"
cd ~/mangos-wotlk
$M realmd < sql/base/realmd.sql
$M characters < sql/base/characters.sql
$M mangos < sql/base/mangos.sql
echo BASE_OK
mkdir -p /tmp/b1sql
for f in src/modules/Bots/sql/playerbot/playerbot.sql src/modules/Bots/sql/characters/characters.sql src/modules/Bots/sql/world/world.sql; do
  grep -viE "^(LOCK TABLES|UNLOCK TABLES)" "$f" > "/tmp/b1sql/$(basename "$f")"
done
$M characters < /tmp/b1sql/characters.sql
$M playerbots < /tmp/b1sql/playerbot.sql
$M playerbots < src/modules/Bots/sql/playerbot/ai_playerbot_weightscales_wotlk.sql
$M playerbots < src/modules/Bots/sql/playerbot/nodes_wotlk.sql
echo BOTS_OK
$M mangos < sql/base/ahbot/mangos_command_ahbot.sql
echo AHBOT_OK
$M -e "SELECT table_schema, COUNT(*) AS tbls FROM information_schema.tables WHERE table_schema IN ('mangos','realmd','characters','playerbots') GROUP BY table_schema;"
