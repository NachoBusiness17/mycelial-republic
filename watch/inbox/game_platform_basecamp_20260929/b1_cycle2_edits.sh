#!/bin/bash
# B1 bots-port cycle-2 canonical edits (GRIND path), 2026-09-29.
# NOTE: canonical files are CRLF; avoid $-anchored sed patterns (cycle-1 lesson:
# the PlayerbotAIAware.h edit silently no-opped on a ^...$ anchor).
set -e
C=/mnt/c/Users/foste/Documents/projects/local_sovereign_agent/corpus/library/mod-playerbots
B="$C/src/modules/Bots"
cd "$B/playerbot" || exit 1

# 1. PlayerbotAI forward declaration inside namespace ai (cycle-1 edit that no-opped)
sed -i '/^namespace ai/a\    class PlayerbotAI;' PlayerbotAIAware.h
echo 1_AWARE_OK

# 2. TravelNode.h: global-scope classes use ai:: names; unity leaked 'using namespace ai'
sed -i '/#include <shared_mutex>/a using namespace ai; // B1 fix 2026-09-29: TravelNode classes are global-scope but use ai::WorldPosition etc.; unity builds leaked using namespace ai from earlier TUs' TravelNode.h
echo 2_TRAVELNODE_OK

# 3. TravelMgr.h: sPlayerbotAIConfig + CreatureDataPair/GameObjectDataPair typedefs
sed -i '/using namespace std; \/\/ B1 fix/a #include "PlayerbotAIConfig.h" // B1 fix 2026-09-29: sPlayerbotAIConfig extern\n#include "Globals/ObjectMgr.h" // B1 fix 2026-09-29: CreatureDataPair/GameObjectDataPair typedefs used by WorldPosition ctors' TravelMgr.h
echo 3_TRAVELMGR_OK

# 4. Event.h: unqualified string uses
sed -i '/^class Player;/a using std::string; // B1 fix 2026-09-29: Event members use unqualified string; unity context used to supply it' strategy/Event.h
echo 4_EVENT_OK

# 5. Value.h: complete AiObjectContext at end of header (pragma-once cycle-safe)
printf '#include "AiObjectContext.h" // B1 fix 2026-09-29: AI_VALUE macro expansions and CalculatedValue<T>::Update access context->performanceStack; TUs that never include AiObjectContext.h saw it incomplete\r\n' >> strategy/Value.h
echo 5_VALUE_OK

# 6. ChangeTalentsAction.h: MSVC-accepted extra qualification is a GCC error
sed -i 's/TalentPath\* ChangeTalentsAction::getPremadePath(int id);/TalentPath* getPremadePath(int id);/' strategy/actions/ChangeTalentsAction.h
echo 6_CHANGETALENTS_OK

# 7. MovementActions.h: inline ctor calls ai->GetBot(); needs complete PlayerbotAI
sed -i '/#include "..\/..\/PlayerbotAIConfig.h"/a #include "../../PlayerbotAI.h" // B1 fix 2026-09-29: inline MovementAction ctor calls ai->GetBot(); header was unity-order dependent' strategy/actions/MovementActions.h
echo 7_MOVEACTIONS_OK

# 8. address-of-rvalue fixes (MSVC allowed &temp; GCC errors)
for f in strategy/actions/ChooseTravelTargetAction.cpp strategy/actions/QueryQuestAction.cpp strategy/actions/GoAction.cpp strategy/actions/ListQuestsActions.cpp; do
  sed -i 's|WorldPosition\* botPos = &WorldPosition(bot);|WorldPosition botPosStore(bot); WorldPosition* botPos = \&botPosStore; // B1 fix 2026-09-29: MSVC accepted address-of-temporary; GCC rejects|g' "$f"
done
sed -i 's|this->nearestPoint(&WorldPosition(bot))|this->nearestPoint(\&botPosStore)|g' TravelMgr.cpp
sed -i 's|^            if (!this->nearestPoint(\&botPosStore)->isOverworld() \&\& !AI_VALUE|            WorldPosition botPosStore(bot); if (!this->nearestPoint(\&botPosStore)->isOverworld() \&\& !AI_VALUE|' TravelMgr.cpp
sed -i 's|^            if (!this->nearestPoint(\&botPosStore)->isOverworld())|            WorldPosition botPosStore(bot); if (!this->nearestPoint(\&botPosStore)->isOverworld())|' TravelMgr.cpp
echo 8_RVALUE_OK
echo ALL_CYCLE2_EDITS_DONE
