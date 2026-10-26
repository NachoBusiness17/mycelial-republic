#!/bin/bash
# B1 bots-port cycle-5 canonical edits (GRIND path), 2026-09-29.
# Ledger fix list 1-5 from cycle-4 root-cause analysis (46 unique errors).
# All edits land on the canonical corpus tree; WSL build tree synced afterward.
# CRLF law: no $-anchored patterns (canonical files are CRLF; $ silently no-ops).
set -e
C=/mnt/c/Users/foste/Documents/projects/local_sovereign_agent/corpus/library/mod-playerbots
B="$C/src/modules/Bots"
cd "$B/playerbot" || exit 1

# A. TravelMgr.h: TravelTarget : AiObject (line 619) needs its base visible.
#    Also heals 'bot'-not-declared sites (AiObject protected member) in
#    TravelMgr.cpp:1251-1311 and TravelMgr.h:641/645.  [ledger fix 1]
sed -i '/#include "Globals\/ObjectMgr.h" \/\/ B1 fix 2026-09-29: CreatureDataPair/a #include "strategy/AiObject.h" // B1 fix cycle5 2026-09-29: TravelTarget : AiObject at line 619 needs the base; also supplies the protected bot member used by TravelTarget methods' TravelMgr.h
grep -q 'strategy/AiObject.h' TravelMgr.h && echo A_TRAVELMGR_H_DONE

# B. AiObject.h: derives PlayerbotAIAware but never included it (unity-order
#    dependency). Value.h-first TUs parse AiObject.h before Value.h reaches
#    its ../PlayerbotAIAware.h include -> "expected class-name" at AiObject.h:11
#    -> BudgetValues.h:45/52/61 cascade.  [deeper root under ledger fix 5]
sed -i '/^#pragma once/a #include "../PlayerbotAIAware.h" // B1 fix cycle5 2026-09-29: AiObject derives PlayerbotAIAware; header relied on unity include order' strategy/AiObject.h
grep -q 'PlayerbotAIAware.h' strategy/AiObject.h && echo B_AIOBJECT_DONE

# C. BudgetValues.h: enter via Action.h, not Value.h.  Value.h-first entry
#    parses Action.h mid-Value.h (pragma-once no-op) so Action.h:66 sees
#    'Value' undefined.  Action.h-first lets Value.h parse completely first.
#    [ledger fix 5]
sed -i 's|#include "\.\./Value\.h" .*|#include "../Action.h" // B1 fix cycle5 2026-09-29: Action.h-first entry; Action.h includes Value.h itself - Value.h-first entry parsed Action.h mid-Value.h and broke Action.h:66|' strategy/values/BudgetValues.h
grep -q 'Action.h' strategy/values/BudgetValues.h && echo C_BUDGET_DONE

# D. TravelNode.cpp: complete PlayerbotAI (BOT_STATE_NON_COMBAT lines 1416/1428,
#    incomplete-type 63/67/150/1197-1209) + completes AiObjectContext (via
#    PlayerbotAI.h -> strategy/AiObjectContext.h) BEFORE the
#    strategy/values/BudgetValues.h chain.  [ledger fix 2b]
sed -i '/#include "TravelMgr.h"/a #include "PlayerbotAI.h" // B1 fix cycle5 2026-09-29: complete PlayerbotAI + AiObjectContext before BudgetValues.h chain' TravelNode.cpp
grep -q 'PlayerbotAI.h' TravelNode.cpp && echo D_TRAVELNODE_DONE

# E. WorldBuffAction.cpp: complete PlayerbotAI (GetFactionReaction at line 27,
#    incomplete-type at line 13) + AiObjectContext before WorldBuffAction.h ->
#    ../Action.h chain.  [ledger fix 2c]
sed -i '/#include "WorldBuffAction.h"/i #include "../../PlayerbotAI.h" // B1 fix cycle5 2026-09-29: complete PlayerbotAI (GetFactionReaction) before WorldBuffAction.h chain' strategy/actions/WorldBuffAction.cpp
grep -q 'PlayerbotAI.h' strategy/actions/WorldBuffAction.cpp && echo E_WORLDBUFF_DONE
# NOTE: TravelMgr.cpp already includes PlayerbotAI.h twice (pre-existing);
# cycle-4 log shows no incomplete-PlayerbotAI errors there - ledger fix 2a moot.

# F. insert_or_assign x8 is C++17; tree compiles -std=c++14.  Return value
#    unused at every site -> operator[] assignment.  [ledger fix 3]
sed -i 's|\([A-Za-z]\{1,\}\)\.insert_or_assign(\([^,]*\), *\([^)]*\));|\1[\2] = \3; // B1 fix cycle5: insert_or_assign is C++17, tree is C++14|' TravelMgr.cpp
echo "F_INSERT_OR_ASSIGN_REMAINING=$(grep -c insert_or_assign TravelMgr.cpp || true)"

# G. TravelMgr.cpp:251 address-of-rvalue: hoist to an lvalue.  [ledger fix 4]
sed -i 's|return offset(&sTravelNodeMap.getMapOffset(getMapId()));|WorldPosition mapOffsetStore = sTravelNodeMap.getMapOffset(getMapId()); // B1 fix cycle5: address-of-rvalue hoist\n    return offset(\&mapOffsetStore);|' TravelMgr.cpp
grep -q 'mapOffsetStore' TravelMgr.cpp && echo G_RVALUE_DONE
echo ALL_CYCLE5_EDITS_DONE
