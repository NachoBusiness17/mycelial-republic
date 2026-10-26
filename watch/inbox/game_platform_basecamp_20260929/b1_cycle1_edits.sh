#!/bin/bash
# B1 bots-port cycle-1 canonical edits (GRIND path), 2026-09-29.
# All edits land on the canonical corpus tree; the WSL build tree is synced afterward.
set -e
C=/mnt/c/Users/foste/Documents/projects/local_sovereign_agent/corpus/library/mod-playerbots
B="$C/src/modules/Bots"
cd "$B/playerbot" || exit 1

# A. case-variant include fixes (Linux is case-sensitive; MSVC accepted any case)
sed -i "s|\.\./\.\./Travelmgr\.h|../../TravelMgr.h|g" \
  strategy/actions/ChooseRpgTargetAction.cpp \
  strategy/actions/ChooseTravelTargetAction.h \
  strategy/actions/ListQuestsActions.cpp \
  strategy/actions/MoveToRpgTargetAction.cpp \
  strategy/actions/MoveToTravelTargetAction.h \
  strategy/actions/QueryQuestAction.cpp \
  strategy/triggers/TravelTriggers.cpp \
  strategy/values/PossibleRpgTargetsValue.cpp
sed -i "s|\"travelMgr\.h\"|\"TravelMgr.h\"|" strategy/actions/GoAction.cpp
sed -i "s|\.\./\.\./talentspec\.h|../../Talentspec.h|g" strategy/actions/ChangeTalentsAction.cpp strategy/actions/ChangeTalentsAction.h
sed -i "s|\"\.\./value\.h\"|\"../Value.h\"|" strategy/generic/NonCombatStrategy.cpp
sed -i "s|\"Battleground\.h\"|\"BattleGround.h\"|; s|\"BattlegroundMgr\.h\"|\"BattleGroundMgr.h\"|; s|\"BattlegroundWS\.h\"|\"BattleGroundWS.h\"|" strategy/actions/LfgActions.h
sed -i "s|\.\./\.\./playerbotAI\.h|../../PlayerbotAI.h|; s|\"BattlegroundJoinAction\.h\"|\"BattleGroundJoinAction.h\"|" strategy/actions/BattleGroundJoinAction.cpp
sed -i "s|\"BattlegroundJoinAction\.h\"|\"BattleGroundJoinAction.h\"|" strategy/actions/WorldPacketActionContext.h
sed -i "s|\"BattlegroundTactics\.h\"|\"BattleGroundTactics.h\"|" strategy/actions/ActionContext.h strategy/actions/BattleGroundTactics.cpp
sed -i "s|\"RTSCAction\.h\"|\"RtscAction.h\"|" strategy/actions/ChatActionContext.h
echo A_CASE_FIXES_DONE

# B. TravelMgr.h: std includes + module-idiom using-directive after the Player.h include
sed -i '/#include "Player.h" \/\/ B1 fix/a #include <string>\n#include <vector>\n#include <sstream>\n#include <list>\n#include <map>\n#include <set>\n#include <unordered_map>\nusing namespace std; // B1 fix 2026-09-29: module idiom (cf. PerformanceMonitor.h) - headers use unqualified std names; cotire PCH supplies the headers but no using-directive' TravelMgr.h
echo B_TRAVELMGR_DONE

# C. Event.h: self-sufficiency (WorldPacket member by value, ObjectGuid, string)
sed -i '/#pragma once/a #include <string>\n#include "WorldPacket.h" // B1 fix 2026-09-29: Event holds a WorldPacket by value; header was unity-order dependent\nclass Player;' strategy/Event.h
echo C_EVENT_DONE

# D. Value.h: CreatureDataPair typedef lives in Globals/ObjectMgr.h
sed -i '/#pragma once/a #include "Globals/ObjectMgr.h" // B1 fix 2026-09-29: CreatureDataPair typedef (CDPairCalculatedValue base); unity builds pulled it in transitively' strategy/Value.h
echo D_VALUE_DONE

# E. PlayerbotAIAware.h: forward-declare PlayerbotAI (member type was undeclared in early-including TUs)
sed -i '/^namespace ai$/a\    class PlayerbotAI;' PlayerbotAIAware.h
echo E_AWARE_DONE

# F. Talentspec.h: self-sufficiency
sed -i '/#pragma once/a #include <string>\n#include <sstream>\n#include <vector>\n#include "DBCStructure.h" // B1 fix 2026-09-29: TalentEntry/TalentTabEntry are complete-type members here\n#include "Entities/Player.h" // B1 fix 2026-09-29: inline ctors call bot->getClassMask()\nusing std::string;\nusing std::ostringstream;' Talentspec.h
echo F_TALENT_DONE

# G. BudgetValues.h: include its base-class hierarchy (was zero-include unity-order header)
sed -i '/#pragma once/a #include "../Value.h" // B1 fix 2026-09-29: Uint32CalculatedValue & co. live in strategy/Value.h' strategy/values/BudgetValues.h
echo G_BUDGET_DONE

# H. CastCustomSpellAction.h:35 ReagentCount is uint32[MAX_SPELL_REAGENTS]; array decays to pointer in ordered compare
sed -i 's/pSpellInfo->ReagentCount > 0/pSpellInfo->ReagentCount[0] > 0/' strategy/actions/CastCustomSpellAction.h
echo H_CAST_DONE

# I. TradeCategory.h: forward-declare SpellEntry (overload with SpellEntry const* failed to parse)
sed -i '/#pragma once/a struct SpellEntry; // B1 fix 2026-09-29: overload IsCraftedBySpell(ItemPrototype const*, SpellEntry const*) needs the name visible' ../ahbot/TradeCategory.h
echo I_TRADECAT_DONE

# J. core Util.h: unqualified toupper/tolower is an unresolved overload under GCC 15
sed -i 's|std::transform(str.begin(), str.end(), str.begin(), toupper);|std::transform(str.begin(), str.end(), str.begin(), [](unsigned char c) { return ::toupper(c); });|' "$C/src/shared/Util.h"
sed -i 's|std::transform(str.begin(), str.end(), str.begin(), tolower);|std::transform(str.begin(), str.end(), str.begin(), [](unsigned char c) { return ::tolower(c); });|' "$C/src/shared/Util.h"
echo J_UTIL_DONE

# K. TravelNode.cpp: sObjectMgr macro needs Globals/ObjectMgr.h in this TU
sed -i '/#include "Entities\/Transports.h"/a #include "Globals/ObjectMgr.h" // B1 fix 2026-09-29: sObjectMgr (GetPlayerInfo) - unity builds pulled it in transitively' TravelNode.cpp
echo K_TRAVELNODE_DONE
echo ALL_CYCLE1_EDITS_DONE
