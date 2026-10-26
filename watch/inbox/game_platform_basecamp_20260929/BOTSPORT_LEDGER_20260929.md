# BOTS PORT LEDGER — GCC 15 / Boost 1.90 port of mangosbot-bots (2026-09-29)

State: the bots-fused CMaNGOS tree cannot compile bots-off (120 playerbot call sites across 40 files in src/game, zero ifdef guards — Map.cpp/Group.cpp call GetPlayerbotAI()/HasRealPlayers() unconditionally). So mangosd requires the bots port to finish. realmd (auth server) BUILT and links clean. This ledger is the resumable state for the porting lane.

## Environment (live, resumable)

- WSL Ubuntu 26.04, 12 cores: `wsl -d Ubuntu -u root`
- Build tree: `~/mangos-wotlk` (full copy incl. bots @ b685d7eb), build dir `~/mangos-wotlk/build` (CMake configured, Bots ON, flags: `-DCMAKE_POLICY_VERSION_MINIMUM=3.5 -Wno-error=template-body -Wno-error=deprecated-declarations -Wno-error=conversion-null -Wno-error=narrowing`)
- Resume: `cd ~/mangos-wotlk/build && make -j8 2>&1 | grep -E 'error:' | sort -u | head`
- Canonical patched tree: `corpus/library/mod-playerbots` (all fixes below landed there via Edit tool)
- WSL MariaDB 11.8.6 running; DBs loaded: realmd/characters/mangos(161 tbl)/playerbots(21) + world content (29,919 creature_template, 9,086 quest_template) from wotlk-db Full_DB
- Windows MariaDB also running (same loads)

## Fixes ALREADY LANDED (canonical tree, 2026-09-29)

1. CMakeLists.txt:215 — Boost `system` component removed (stub lib deleted in Boost >=1.86).
2. cmake/macros/cotire.cmake:40 — cmake_minimum_required(VERSION 2.8.12) -> 3.5 (CMake 4 removed <3.5; script-mode calls during builds bypass the cache workaround).
3. src/game/CMakeLists.txt — game tree's own include dirs made UNCONDITIONAL (upstream gated them behind BUILD_IKE3_BOTS); added `src/game/Vmap` (capital V — Linux is case-sensitive; VMapFactory.h lives there, includes say lowercase vmap).
4. src/modules/Bots/CMakeLists.txt — added `src/game/Vmap`.
5. src/shared/Network/{Socket.hpp,Listener.hpp,Socket.cpp}, src/shared/Metric/{Metric.h,Metric.cpp}, src/game/Server/{WorldSocket.h,WorldSocket.cpp}, src/mangosd/RASocket.{h,cpp}, src/realmd/AuthSocket.{h,cpp}, src/shared/Network/NetworkThread.hpp — boost::asio::io_service -> io_context (removed in Boost 1.86+); deadline_timer explicit includes added (no longer transitive); io_context::work -> executor_work_guard; io_context::post member -> free-function boost::asio::post; run(error_code&) -> run() (ec overload removed in 1.90).
6. src/shared/Util.cpp + src/shared/Network/Listener.hpp + src/game/Server/WorldSession.cpp — address::from_string / address_v4::from_string -> make_address / make_address_v4.
7. src/shared/Log.cpp — GetTimestampStr buffer 20 -> 64 (real latent overflow, glibc fortify caught it).
8. src/modules/Bots/playerbot/TravelMgr.h:280 — mem-initializer `: ObjectGuid(guid) : WorldPosition(T)` -> comma (invalid syntax upstream; MSVC-only acceptance).
9. src/modules/Bots/playerbot/strategy/Value.h — SingleCalculatedValue/MemoryCalculatedValue: this-> qualifications + CalculatedValue<T> qualified base calls (two-phase lookup).
10. src/modules/Bots/playerbot/TravelNode.h:294 — extra `TravelPath::` qualification inside class removed (MSVC-only extension).

## REMAINING ERROR LEDGER (next fixes, in first-fail order)

1. **LastMovementValue.h:106** — `LastMovement data = LastMovement();` fails because LastMovement's copy ctor is `LastMovement(LastMovement&)` (non-const ref, cannot bind the rvalue). FIX: `LastMovement data;` (default ctor exists, calls clear()). Same pattern may recur (grep `= LastMovement()`).
2. **TravelNode.h:155/171** — `WorldPosition does not name a type` inside TravelPath/TravelNode. CAUSE (deeper): TravelMgr.h uses `Player*` METHODOLOGICAL bodies (isActive -> bot->IsActiveQuest) with Player only forward-declared — the bots headers depend on the cotire UNITY/PCH global include order (Player.h pre-included). Fix options: (a) add `#include "Player.h"` (heavy but correct) at top of TravelMgr.h, or (b) disable cotire for Bots and fix include order per-TU. Prefer (a); expect a chain of 2-5 more heavy includes (Player.h pulls Unit.h pulls Object.h).
3. **Value.h:124 LogCalculatedValue** — unqualified `MemoryCalculatedValue::UpdateChange()` / `Reset()` and `value` in dependent base -> add `<T>` + `this->` (same as the landed SingleCalculatedValue fix).
4. After the above: re-run and extend this ledger. Expect the two-phase-lookup family (`this->` fixes) to repeat across strategy/ headers; each is small.

## WHY bots-off is not a shortcut

`grep -rE "GetPlayerbotAI\(|HasRealPlayers\(" src/game/ --include="*.cpp" | wc -l` = 120 across 40 files, zero BUILD_IKE3_BOTS guards (Map.cpp:777/801, Group.cpp etc.). A stub shim would fake 40 files of API surface; the port is the honest path.

## The three rejected authorities reminder (from WOW_ACORE_STEAL_MAP)

When mangosd boots, bridge law holds: CMaNGOS = content/scale authority; bones/ledger layer (mag/wow_*) = verification authority. Wall-clock ticks, urand, and MySQL stay INSIDE the emu boundary and never leak into the verification layer.

## 2026-09-29 B1 bots-port lane: GRIND decision + 4 fix cycles (592 -> 46 unique errors)

### Decision: GRIND (keep celguar snapshot), evidence byte-backed

- Cloned `github.com/cmangos/playerbots` to `/root/playerbots-cmangos` (WSL) and inspected.
- HEAD commit is dated 2026-09-29 (same day): it targets CURRENT cmangos cores. Our fused tree is 2021-era (`git log -1` in `/root/mangos-wotlk`: "Tue Dec 28 2021 +0300 Update Bots", bots @ b685d7eb). Five years of core-API drift means the fork's ~1000 module files would compile against a 2021 core only through a fresh, unknown error mountain.
- API entry points match (PlayerbotAI::GetPlayerbotAI / IsRealPlayer / HasRealPlayerMaster identical strings in both), but the core side is heavily paired to the celguar snapshot: `src/game/Entities/Player.h:64` includes the OLD in-core `PlayerBot/Base/PlayerbotAI.h` AND forward-declares the module `class PlayerbotAI` (global scope); 120 unguarded call sites. The cmangos fork rewrote the travel system entirely (TravelMgr.cpp 2,844 lines vs celguar 4,265; no getTitle destination classes), so it is NOT a drop-in for the paired core hooks.
- The SWAP rule's condition ("declares compatibility with the mangos-wotlk era core") is NOT met: it declares compatibility with current cmangos classic/tbc/wotlk. GRIND it is.

### Cycles run (instrument: `grep 'error:' <full-sweep log> | sort -u | wc -l` after `make -k -j8`; moment = after each cycle's sync; numbers are unique LINES, cascades included)

1. Cycle 1 (b1_cycle1_edits.sh): 742 -> 271. Landed: 17 case-variant include strings (`../../Travelmgr.h`, `travelMgr.h`, `../../talentspec.h`, `../value.h`, `Battleground.h/Mgr/WS`, `../../playerbotAI.h`, `BattlegroundJoinAction.h`, `BattlegroundTactics.h`, `RTSCAction.h`); TravelMgr.h std includes + `using namespace std` (module idiom, cf. PerformanceMonitor.h:12); Event.h made self-sufficient (`<string>`, WorldPacket.h, Player fwd); Value.h `Globals/ObjectMgr.h` (CreatureDataPair); Talentspec.h self-sufficient (DBCStructure.h, Entities/Player.h, targeted usings); BudgetValues.h `../Value.h`; TradeCategory.h `struct SpellEntry;` fwd; CastCustomSpellAction.h `ReagentCount[0]` (array decay in ordered compare); core Util.h toupper/tolower lambdas; TravelNode.cpp ObjectMgr.h.
2. Cycle 2 (b1_cycle2_edits.sh): 271 -> 3128 (REGRESSION, self-inflicted). TravelNode.h `using namespace ai;` (its classes are GLOBAL-scope but use ai:: names; unity context used to leak the using), TravelMgr.h PlayerbotAIConfig.h + Globals/ObjectMgr.h, Event.h `using std::string;`, ChangeTalentsAction.h extra-qualification removed, MovementActions.h `../../PlayerbotAI.h`, 6 address-of-rvalue hoists. TWO bugs: (a) Value.h bottom-include of AiObjectContext.h created a mid-parse cycle (Action.h -> Value.h -> AiObjectContext.h -> Action.h no-op => "Action does not name a type"); (b) my PlayerbotAIAware.h forward declaration landed INSIDE `namespace ai`, creating a second type `ai::PlayerbotAI` next to the real GLOBAL PlayerbotAI => ~3000 "reference to 'PlayerbotAI' is ambiguous" errors. Cycle-1 lesson also recorded: canonical files are CRLF; `$`-anchored sed patterns silently no-op.
3. Cycle 3 (Value.h bottom-include reverted; per-TU AiObjectContext.h includes for AhBot.cpp, AhBotConfig.cpp, ItemBag.cpp, CastTimeStrategy.cpp): 3128 -> 3120 (fwd-decl bomb still masked everything).
4. Cycle 4 (PlayerbotAIAware.h fwd moved to GLOBAL scope): 3120 -> 46. THE single-line root of the entire 3,120-error explosion.

### Current error state (cycle-4 log `/root/build_cycle4.log`, 46 unique lines, ~4-5 failing TUs vs 399 rebuilt this cycle)

Families, all root-caused:
1. TravelMgr.h:619 `class TravelTarget : AiObject` => AiObject not visible: add `#include "strategy/AiObject.h"` to TravelMgr.h. This also heals the `bot`-not-declared sites (bot is an AiObject protected member) in TravelMgr.cpp:1251-1311 and TravelMgr.h:641/645.
2. TravelMgr.cpp + TravelNode.cpp + WorldBuffAction.cpp: incomplete `PlayerbotAI` (ai->HasStrategy, GetBot, BOT_STATE_NON_COMBAT): add `#include "PlayerbotAI.h"` (TravelMgr.cpp, TravelNode.cpp) and `#include "../../PlayerbotAI.h"` (WorldBuffAction.cpp).
3. `insert_or_assign` x8 (TravelMgr.cpp:2028, 2042, 2055, 2084, 2092, 3262, 3468, 3502): C++17 API under `-std=c++14`. Replace with `map[key] = value;` per site (return value unused) or consider `-std=c++17` (riskier: whole tree compiled clean as C++14).
4. TravelMgr.cpp:251:47 `offset(&sTravelNodeMap.getMapOffset(getMapId()))`: address-of-rvalue; hoist `WorldPosition mapOffsetStore = ...; return offset(&mapOffsetStore);`.
5. Value.h:52 / Action.h:144-145 "incomplete ai::AiObjectContext" + AiObject.h:11 + BudgetValues.h:45/52/61 in a values/ TU: BudgetValues.h currently enters via `../Value.h` which breaks the Action.h <-> Value.h circular pair (Value.h-first entry parses Action.h mid-flight). Change BudgetValues.h to `#include "../Action.h"` (Action.h-first entry works). If any incomplete-AiObjectContext errors survive, re-attribute with `make -j1` on the specific objects; -j8 attribution is noisy.

### Next action (single): apply fixes 1-5 above at the canonical tree, resync (b1_cycle1_build.sh pattern), `make -k -j8`; expect libBots archive + mangosd link attempt. realmd already links (1,187,216 bytes, 2026-09-29 13:40). mangosd NOT yet produced.

### Scripts banked (watch/inbox/game_platform_basecamp_20260929/)

- b1_cycle1_edits.sh, b1_cycle2_edits.sh (canonical edit scripts, CR-safe patterns)
- b1_cycle1_build.sh, b1_cycle2_build.sh (sync+cmake+make-k patterns; cycle 3/4 variants live at /root/b1_cycle3_build.sh, /root/b1_cycle4_build.sh)
- Full-sweep logs in WSL: /root/build_full.log (742), /root/build_cycle1.log (271), /root/build_cycle2.log (3128), /root/build_cycle3.log (3120), /root/build_cycle4.log (46)
- cmangos fork reference clone: /root/playerbots-cmangos (kept for future comparison; not used in the build)

## 2026-09-29 B1 bots-port lane cycle 5-6: PORT COMPLETE, mangosd LINKED (46 -> 7 -> 0 unique errors)

### Cycle 5 (b1_cycle5_edits.sh / b1_cycle5_build.sh): ledger fix list 1-5 applied, 46 -> 7

Landed at canonical (all verified by grep after the script):

1. TravelMgr.h: added `#include "strategy/AiObject.h"` (fix 1). Healed TravelMgr.h:619/621/622/641/645 + TravelMgr.cpp:1251-1311 (`bot` is an AiObject protected member).
2. TravelNode.cpp: added `#include "PlayerbotAI.h"` before the BudgetValues.h chain (fix 2b). Healed TravelNode.cpp:63/67/150/1197/1200/1209/1416/1428 (incomplete PlayerbotAI, BOT_STATE_NON_COMBAT).
3. WorldBuffAction.cpp: added `#include "../../PlayerbotAI.h"` before WorldBuffAction.h (fix 2c). Healed WorldBuffAction.cpp:13/27.
4. Fix 2a was MOOT: TravelMgr.cpp already had PlayerbotAI.h twice (pre-existing); the cycle-4 log shows no incomplete-PlayerbotAI errors there, only AiObject-derived `bot` errors, which fix 1 heals.
5. TravelMgr.cpp: 8x insert_or_assign -> `map[key] = value;` (2028/2042/2055/2084/2092/3262/3468/3502; return value unused at every site) + line 251 address-of-rvalue hoist (`WorldPosition mapOffsetStore = sTravelNodeMap.getMapOffset(getMapId()); return offset(&mapOffsetStore);`).
6. BudgetValues.h: `../Value.h` -> `../Action.h` (fix 5, Action.h-first entry) PLUS the deeper root the ledger had not named: `strategy/AiObject.h` itself now includes `../PlayerbotAIAware.h`. AiObject derives PlayerbotAIAware but never included it; in Value.h-first TUs, AiObject.h parsed before Value.h reached its own PlayerbotAIAware.h include (AiObject.h:11 "expected class-name" -> BudgetValues.h:45/52/61 cascade).

Incident: the first cycle-5 build (make -k -j8) OOM-killed WSL (Wsl/0x8007000e, "not enough memory", exit 127) at 239 TUs compiled, zero compiler errors, remaining jobs "Hangup". Resumed make -k -j4 incrementally; objects persisted, nothing rebuilt twice.

Result (instrument: `grep 'error:' /root/build_cycle5.log | sort -u | wc -l`, log spans the killed -j8 run plus the -j4 resume): 7 unique error lines = 2 root causes, BOTH in src/game (the game lib reached full compile for the first time; earlier cycles never got past the Bots module):

- src/shared/Metric/Metric.h:126/127 `io_context::work` members (ledger fix-list-5 gap: the earlier asio sweep converted NetworkThread.hpp only, NOT Metric.h/.cpp despite the landed-fixes note claiming it)
- src/game/Server/WorldSession.cpp:1295 `address_v4::to_ulong()` (removed in newer asio)

The Bots module compiled 100% clean this cycle: libBots.a archived 44,006,598 bytes at 15:16. The bots headers now also parse clean inside game TUs (WorldSession.cpp includes PlayerbotAI.h chain; Value.h:52 incomplete-AiObjectContext is downgraded to a parse-time warning with delayed template instantiation).

OPERATIONAL LAW (new, banked): inline `wsl -- bash -c "... \$? ... \$(grep ...)"` with nested escaped expansions MANGLES through the wsl.exe command-line layer and returned a false "MAKE_EXIT=0 / 0 unique error lines" while make had actually failed with Error 2 (the Error lines sat in the log the whole time). Verification must run from a script file (`wsl -- bash /mnt/c/.../script.sh`), as b1_cycle6_build.sh does. Trust the log bytes, not the echoed readout.

### Cycle 6 (b1_cycle6_edits.sh / b1_cycle6_build.sh): 7 -> 0, mangosd LINKED

Landed at canonical:

1. Metric.h:126/127: `std::unique_ptr<boost::asio::io_context::work>` -> `std::unique_ptr<boost::asio::executor_work_guard<boost::asio::io_context::executor_type>>` (NetworkThread.hpp idiom).
2. Metric.cpp:113/114: `.reset(new io_context::work(...))` -> `.reset(new executor_work_guard<...>(make_work_guard(...)))`.
3. WorldSession.cpp:1295: `.to_ulong()` -> `.to_uint()` (same uint32 value).

Metric.h sits in the game PCH chain (pchdef.h -> ObjectAccessor.h -> Player.h -> Unit.h -> Opcodes.h -> WorldSession.h -> WorldSocket.h -> Socket.hpp -> Metric.h), so the game PCH rebuilt and the full game TU sweep reran: 1097 TUs compiled (instrument: `grep -c 'Building CXX object' /root/build_cycle6.log`), run at make -k -j6.

Result: MAKE_EXIT=0, 0 unique error lines, `[100%] Linking CXX executable mangosd`, `[100%] Built target mangosd`. Remaining log noise is deprecation warnings only (boost deadline_timer deprecated: use system_timer; non-fatal, deferred).

### Binary census (2026-09-29, stat/file in WSL; NOT executed)

- /root/mangos-wotlk/build/src/mangosd/mangosd: 37,544,048 bytes, 2026-09-29 16:10:08 EDT, ELF 64-bit LSB pie executable x86-64, dynamically linked, BuildID[sha1]=b0866273ee31b3c00addefaaacd8c1346a39c92a, not stripped
- /root/mangos-wotlk/build/src/realmd/realmd: 1,187,216 bytes, 2026-09-29 15:40:02 EDT (rel linked cycle 6), BuildID[sha1]=6c16f67de51e129ba6fd3937af5f5904b1cdb46c
- /root/mangos-wotlk/build/src/modules/Bots/libBots.a: 44,006,598 bytes, 2026-09-29 15:57:47 EDT

### Boot-attempt note (NOT attempted, by instruction)

mangosd was NOT run: no client data (DBC files, maps, vmaps, mmaps) is staged in the environment yet, and mangosd.conf does not exist (only mangosd.conf.dist in build/src/mangosd/). DBs are loaded on both MariaDB instances (realmd/characters/mangos 161 tables/playerbots 21 + wotlk-db content), so the data wall is client files + config, not SQL. First boot is a separate, deliberate step.

### Next action (single)

Stage client data (extract DBCs/maps/vmaps/mmaps from a WotLK 3.3.5a client or reuse an existing extraction), copy mangosd.conf.dist -> mangosd.conf and point DataDir at it, then first `mangosd` boot attempt in WSL with realmd already runnable; expected first-boot work is conf/DBC path fixing, not code.

### Scripts banked this session (same directory)

b1_cycle5_edits.sh, b1_cycle5_build.sh, b1_cycle6_edits.sh, b1_cycle6_build.sh; full-sweep logs in WSL: /root/build_cycle5.log (7 unique, spans OOM kill + resume), /root/build_cycle6.log (0 unique, 1097 TUs, mangosd link)

## 2026-09-29 B1 bots-port lane cycle 7: FIRST BOOT ATTEMPTED — DB wall cleared, died on missing maps (client data named)

### Binary verified (ledger census re-confirmed byte-for-byte)

/root/mangos-wotlk/build/src/mangosd/mangosd: 37,544,048 bytes, ELF 64-bit pie, BuildID[sha1]=b0866273ee31b3c00addefaaacd8c1346a39c92a — matches cycle-6 census. Port state: COMPLETE, no rebuild needed this cycle.

### mangosd.conf (b1_mangosd_boot1.sh)

- DEFAULT conf path discovery: mangosd looks for `../etc/mangosd.conf` relative to cwd, NOT `./mangosd.conf`; first invocation died in 1 line: `Could not find configuration file ../etc/mangosd.conf.` Conf therefore written to `/root/mangos-wotlk/build/src/etc/mangosd.conf` (mkdir ../etc).
- DatabaseInfo: all four -> `127.0.0.1;3306;mangos;mangos;{realmd|mangos|characters|playerbots}` (mangos MySQL user verified live over TCP; sees all four DBs). DataDir -> `/root/mangos-data` (empty placeholder, created).

### Run 1 (34-line log, banked mangosd_boot1_run1_20260929.log): db_version lineage gate

Banner + config + World DB connect OK, then: `query ERROR: Unknown column 'required_14034_01_mangos_column_fix' in 'SELECT'` — the wotlk-db Full_DB's db_version carries a DIFFERENT update lineage (required_14092_01_mangos_proc_cooldown, content_5771_c.22418) than the 2021 core's base (required_14034_01_mangos_column_fix). FIX APPLIED (b1_mangosd_boot1b.sh): swapped ONLY the `db_version` table to the core base shape (CREATE+INSERT copied from sql/base/mangos.sql lines 22-37); content tables untouched.

### Run 2 (51-line log, banked mangosd_boot1_20260929.log): the client-data wall, DELIVERABLE REACHED

ALL FOUR databases connected clean (World/Character/Playerbot/Login, 2 conns each, MariaDB 11.8.6), `Realm running as realm ID 1`, VMap+mmap paths resolved, then:

```
Check existing of map file '/root/mangos-data/maps/0004331.map': not exist!
Correct *.map files not found in path '/root/mangos-data/maps' or *.vmtree/*.vmtile files in '/root/mangos-data/vmaps'. Please place *.map and vmap files in appropriate directories or correct the DataDir value in the mangosd.conf file.
```

BOOT_EXIT=1. Note: the `.map` check fires BEFORE DBC load — DBCs were never reached this boot; maps/vmaps are the first client-data wall, DBC/ the second expected one behind it.

### What the boot error names (the exact need)

- `/root/mangos-data/maps/*.map` (first check names 0004331.map) and `/root/mangos-data/vmaps/` (*.vmtree + *.vmtile) — extract from a WotLK 3.3.5a (build 12340) client with the tree's own extractor tools (bin/ map/vmap extractors; mmaps via movemapgen for MMap pathfinding, already enabled in conf).
- DBC files (DataDir `dbc/` or client DBCs) — expected next wall once maps exist.

### State notes

- World DB is now a hybrid: wotlk-db Full_DB content tables + core-era db_version marker. If later startup hits content-schema drift (column renames in the newer Full_DB), the honest fix is loading Full_DB content INTO the core-base schema, not stretching the version gate further.
- realmd untouched this cycle (links clean; first-boot receipt is b1_realmd_first_boot.sh, earlier session).

### Scripts/logs banked this cycle (same directory)

b1_mangosd_boot1.sh, b1_mangosd_boot1b.sh; mangosd_boot1_run1_20260929.log (db_version gate), mangosd_boot1_20260929.log (maps wall). WSL copies: /root/mangosd_boot1.log (run 2), conf at /root/mangos-wotlk/build/src/etc/mangosd.conf.

### Next action (single)

Stage client data: extract maps/vmaps (+mmaps) and DBCs from a WotLK 3.3.5a client into /root/mangos-data, then boot again; expected remaining first-boot work is extractor plumbing, not code.
