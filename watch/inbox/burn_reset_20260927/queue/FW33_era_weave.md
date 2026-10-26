# FW33_era_weave: era deep-weave remainder + W8 landed (tabletop/MUD era)

**Stone:** FW-33 (FIFTY_WIDE_BOARD_20260917.md §G line 62): "Era weaves remainder: enumerate un-landed era deep-weaves from WAVE_STATE, land the next one".
**Date filed:** 2026-09-28 · **Lane:** burn_reset Q-026 · **Cost:** $0, no paid APIs, no git commands, knowledge primary (standard record; estate bytes cited by path).
**Sources read this ask:** `watch/inbox/WAVE_STATE_20260916.md` · `memory/continuity/seat_memory_20260927/gaming-weave-20260916.md` (the build-out ledger: "W8 tabletop/MUD era deep weave (1302 requeued)") · `watch/inbox/wave_20260916/receipts/W7_ERA_ANCIENT.md` (SEALED; the shape this receipt follows) · `watch/inbox/wave_20260916/receipts/W9_ERA_ROGUE_DECK.md` (FILED) · `watch/inbox/wave_20260916/receipts/HG1_GAMING_HISTORY_WEAVE.md` (the 14-era list) · `watch/inbox/THE_WEAVE_20260916.md` §1 rung law · CG2 P1-P6 rubric as restated in W9 Part 0.

## Part 0: the enumeration (what WAVE_STATE actually owes)

The weave build-out fired three era deep-weave lanes on 2026-09-16 (gaming-weave continuity record, lines 71-73). Receipt census on disk this ask (`ls watch/inbox/wave_20260916/receipts/`):

| Lane | Era | HG1 eras covered | Receipt state on disk |
|---|---|---|---|
| W7 | ancient boards | era 1 (Senet → backgammon → Tafl, 10 games) | **SEALED** (`W7_ERA_ANCIENT.md`, 146 lines) |
| W8 | tabletop + MUD | eras 2 (D&D/Chainmail) + 3 (MUD1 → WoW) | **NEVER LANDED.** No W8 file in the receipts dir; the gaming-weave record marks it "1302 requeued" (rate-limited off the 09-16 dozen-wide run). The only W8-named file in the inbox is `THE50_W8_T38_LEDGER_PUBLIC_SPEC.md`, a different board's item (THE 50 program, T38 ledger-public spec, filed 09-19), not this lane. |
| W9 | rogue/deckbuilder/souls | eras 4, 10, 11, 12 (Rogue → NetHack → DF, FTL/StS/Hades, DeS → Elden Ring, Exanima) | **FILED** (`W9_ERA_ROGUE_DECK.md`) |

**Never fired at all (HG1 eras with no deep-weave lane lit, mechanics only at table-row depth):** era 5 arcade · era 6 console/platformer · era 7 god/sim · era 8 the 3D revolution · era 9 MMO · era 13 procedural giants · era 14 social/dogfood. Their best mechanics already sit in THE_WEAVE §2 rows (several landed since: II-23 Pac-Man ghost doctrines → W4 DONE; X-1 Wordle daily seed → W1A FINAL; the Corrupted Blood plague is V-9 QUEUED), so the remainder is genuinely: **W8 (owed, requeued) + seven unlit eras.** Order of the remainder after W8 lands: MMO era (9) first: the bones-legal world is Rung IV and the MMO era is its native canon; then arcade+platformer (5+6, Rung I/II canon), god/sim (7), 3D (8), procedural (13), social/dogfood (14).

**The next one is W8. Landed below, in the W7 shape.**

---

## Part I: W8: the tabletop + MUD era, deep-unpacked for the bones-legal world

Scoring per the CG2 rubric (W9 Part 0 verbatim): P1 persistence · P2 mutation authority · P3 knowledge metagame · P4 player authorship · P5 continuation economics · P6 async co-presence. Shell `–`/`~`/`+`/`++` with one-line justification each. World being woven into: the persistent bones-legal world (rooms as legality tables, `world_sha`-bound receipts, referee-legal refusals, ghosts).

### 1. Dungeons & Dragons (1974, from Chainmail 1971; Gygax & Arneson)

- **Finite shell:** a party descends a dungeon the referee authored; rounds, hit points, saving throws; treasure is the score. The 1974 books assume Chainmail's mass-combat frame and wargame conventions throughout.
- **Infinite core: three machines.** (a) **The DM**: human adjudication as a game mechanism, not a bug queue; rulings over rules, and the ruling is the game. (b) **XP-for-gold**: the 1974 award was for treasure recovered, not monsters slain, so cleverness (routing, negotiating, avoiding) paid better than combat; most descendants quietly inverted this back to kills. (c) **The party as a legal unit**: complementary classes that structurally need each other; a party without a healer is a legal mistake, not a suboptimal one. Plus (d) **saves vs. categories**: defense is a named roll against a named threat class, legible in the record.
- **Scores:** P1 `~` (characters persist between sessions on paper; the world lived in the DM's head). P2 `++` (the DM mutates any rule at the table, instantly, and the mutation is canonical at that table; the house-rules culture is mutation authority at folk scale). P3 `+` (module and strategy corpora, Dragon magazine, ARGOT/GRODOG zines). P4 `~` (players author characters and describe actions freely, but the world is the DM's). P5 `~` (convention play, zines, and later TSR's economy; play did not pay for itself structurally). P6 `–` (in-person; async play arrived only with play-by-post).
- **The weave:** *the receipted ruling.* Every referee ruling becomes a first-class field in the session receipt (`ruling=<text>`, `bent=<rule-id>`, `why=<line>`). Modern GM modes ship dashboards, never the ruling itself as the citable artifact. The bones chain already is a DM with receipts (IV-2 SHIPPED); the weave is making the ruling row mandatory, so the chronicle learns not just what happened but which law bent and why.

### 2. MUD1 (1978, Essex University; Roy Trubshaw & Richard Bartle)

- **Finite shell:** Zork-style rooms, points for puzzles and for leveling to wizard, then "witch" status; the win state existed and was reachable.
- **Infinite core: three machines.** (a) **The world outlives the avatar, legally separated**: the land persists server-side while players are session-bound visitors; persistence is the game, not a save file. (b) **The name**: MUD1 coined the form; every roomed text world since is its descendant. (c) **Bartle's taxonomy (1996)** was distilled from MUD1's own player log: achievers, explorers, socializers, killers, the first player-model extracted from receipts rather than invented.
- **Scores:** P1 `+` (the land persisted across all sessions from day one; the original reboot-risk economy). P2 `–` (fixed content; admins only). P3 `+` (the wizard-run endgame and the community's mapped knowledge). P4 `–` (no player building). P5 `–` (a university toy; no economics). P6 `+` (co-presence at dial-up scale; the first "everyone in one world" feeling).
- **The weave:** *session-avatar/world split as the receipt boundary.* `wow_session.v1` is a session artifact; `world_sha` is the world artifact; the two hash domains must never mix (a session receipt cites the world it ran in, never mutates it directly). MUD1's P1 lesson is already our law; the weave is the discipline statement: world mutations flow only through referee-legal verbs, sessions cite `world_sha` in every receipt (already the contract, keep it asserted).

### 3. TinyMUD / MUSH lineage (1989, James Aspnes; the social MU*)

- **Finite shell:** none that matters: no points, no win, minimal combat. The shell is nearly empty on purpose.
- **Infinite core: the players build the world.** TinyMUD handed building to players: @dig, @describe, rooms and exits authored by visitors, and the referee's role shrank to keeping the peace. The MU* line (MUSH, MUCK, MUX) made player authorship the whole game: economies of *building*, social contracts, and the first large-scale experiment in what strangers build when the world is theirs. The dark lesson rode along: unwritten social law decays; the communities that lasted wrote their policies down (the first server constitutions).
- **Scores:** P1 `+` (built rooms persist for years on some MUSHes still running). P2 `+` (wizards + players both mutate content, by design). P3 `~` (building lore, not strategy). P4 `++` (THE player-authorship game; everyone is a content author). P5 `+` (idle CPU and donated servers kept worlds alive for decades at near-zero cost). P6 `+` (async co-presence in the literal sense: the world is a place people return to across time zones and years).
- **The weave:** *the AUTHOR verb.* An agent proposes a room (name, exits, legality rows, one lore line); the referee validates it against the refusal rows (typed refusals per the RS_WORLDBUILD_SALON amendments), hash-commits it into `world_sha`, and every future session inherits it. Griefing guard: the author owns their room's *lore*, the referee owns its *legality*, and the receipt records both names. This is the missing P4 in the bones-legal world (see Part IV).

### 4. DikuMUD (1990, Seifert/Hammer/Ellefsen et al.; the codebase that seeded a genre)

- **Finite shell:** levels 1-34, classes (mage/cleric/thief/warrior), zones with mobiles and resets, and the famous *tick*: the world updates on a global heartbeat rather than per-command.
- **Infinite core: the fork economy.** DikuMUD was written by students and spread as source: hundreds of codebases (Merc, ROM, Circle, SMAUG) and thousands of worlds forked from it, most with their own content and house rules. It is the clearest pre-Git proof that a good kernel plus open source beats a polished closed product: nobody remembers the "official" Diku world; everybody's cousin played a Merc MUD. Also shipped: the **reset tick** (world state is a schedule, not a diary) and **class-as-verb-set** (what you may do, not what you are).
- **Scores:** P1 `+` (persistent per-world; resets are persistence-as-schedule). P2 `++` (fork culture: mutation authority distributed to anyone with the source; thousands of legal variants). P3 `+` (builder manuals, area formats, the mort/wiz knowledge split). P4 `+` (builder ports: players became area authors under wizard review, the middle step between MUD1's fixed content and TinyMUD's open building). P5 `+` (volunteer worlds ran for decades; the codebase itself is the continuation vehicle). P6 `–`/`+` (same-dial-up co-presence as MUD1).
- **The weave:** *the reset tick as world law.* Mud already respawns the world on rest (bonfires, II-9 SHIPPED); the bones-legal world should own an explicit scheduled reset epoch in `world_sha` (world generation counter), so a room's respawn is a receipted schedule event rather than an ad-hoc side effect. And the fork lesson is the estate's own: `memory/game_modules/*.v1.json` is our area format; worlds fork as data, not code.

### 5. EverQuest (1999, Verant/989 Studios; "ever quest")

- **Finite shell:** levels, zones, camps, raids; death with an experience penalty and a naked corpse run home.
- **Infinite core: the social physics.** (a) **Aggro/hate lists**: enemies pick targets by a weighted, manipulable table; the tank is a mechanical role and *pull discipline* is a craft; a bad pull trains the whole zone and the train is everyone's problem. (b) **Camps**: content is locally scarce, so players negotiate de-facto property over spawn sites with no in-game law backing them, pure custom law. (c) **Corpse runs**: death costs real time and the recovery is a quest the world imposes.
- **Scores:** P1 `++` (the world moved with or without you; camps held while you slept, sort of; the archetypal "it's the world, not a game"). P2 `–` (live team only, and the nerf-bat was felt as distant government). P3 `++` (Allakhazam and the entire strategy-site industry; raid theory at scale). P4 `–` (player content: none). P5 `+` (subscriptions funded a decade of expansions; the camp economy ran on reputation). P6 `+` (the train warning shouted across zones is co-presence as adrenaline).
- **The weave:** *the hate table as public truth.* Mud's aggro is canSee-gated and shipped (II-5 SHIPPED); the weave is rendering the table: the rout receipt carries the hate rows (who held, who peeled, what broke), so the chronicle can litigate a rout the way a raid council replays a wipe. Frame-data-as-public-truth (I-5) applied to threat. Also: **custom camp law**: the relay's presence registry already names who is where; camp claims can be receipted soft-property (first-seen claim, honored by custom, enforced by nobody, exactly as EQ's were).

### 6. World of Warcraft (2004, Blizzard)

- **Finite shell:** levels, dungeons, raids, honor; the most polished shell of the lineage.
- **Infinite core: three machines.** (a) **Instances**: private copies of contested zones; a concurrency fix that became the content frame (IV-3 SHIPPED as `wow_session.v1` receipts: "instances as receipts"). (b) **Quests-as-spine**: the log, not the map, tells you where to go; direction as a service (II-7 SHIPPED as the sigil chain, d7 gate). (c) **The guild as a legal entity**: ranks, banks, calendars, loot rules; the first mass-scale player governance shipped as UI. And the cautionary carve: **Corrupted Blood (2005)**, the raid debuff that escaped through teleport/pet edge cases and became emergent epidemiology studied by real epidemiologists, the proof that unplanned world-plague is content gold (V-9 QUEUED: the cube's contamination incident is ours, and unlike WoW's it is real).
- **Scores:** P1 `++` (the world persisted at MMO scale; sharding made persistence affordable). P2 `+` (patches as scheduled world mutations; the patch-notes ritual). P3 `++` (theorycraft: the damage-per-second spreadsheets are a worker-owned science of the world). P4 `~` (UI addons: players author *interfaces into* the world, not the world; 2020's Classic-era restrictions showed the leash). P5 `++` (subscriptions at industrial scale). P6 `+` (LFG and guild chat; async in the weak sense).
- **The weave:** *the guild ledger.* The bones-legal world's player files are append-only ledgers (IV-6); the weave is the guild row: a named ledger shared by N player files (rank rows, loot-rule rows, a shared stake field), referee-witnessed, so agent sessions can form durable parties with governance that survives any member's death. This is D&D's party machine run at MUD1's persistence, filed as one receipt type.

### Era table

| Game | Finite shell | Infinite core | Weave target |
|---|---|---|---|
| D&D 1974 | dungeon + referee + party | the DM; XP-for-gold; party as legal unit; saves vs. categories | the receipted ruling (`ruling=`/`bent=`/`why=` in `wow_session.v1`) |
| MUD1 1978 | rooms + points + wizard | world outlives avatar; the name; Bartle's player-model from logs | session/world hash-domain separation, asserted |
| TinyMUD 1989 | almost none on purpose | players build the world; server constitutions | the AUTHOR verb (player-authored rooms under referee legality) |
| DikuMUD 1990 | levels, classes, zones, tick | the fork economy; reset tick; builder ports | reset epoch in `world_sha`; worlds fork as `game_modules/*.v1.json` data |
| EverQuest 1999 | levels, camps, corpse runs | hate lists; camp custom-law; trains | hate table rendered into rout receipts; soft camp claims on the relay |
| WoW 2004 | raids, honor, polish | instances; quests-as-spine; guild as legal entity; Corrupted Blood | the guild ledger (shared append-only governance receipt) |

Era verdict: the tabletop+MUD era invented the referee (P2 at personal scale), persistence-as-place (P1), and player authorship twice (Diku builder ports, TinyMUD open building). What it never solved is the referee at industrial scale: every large world either centralized mutation (WoW patches) or dissolved into fork clouds (Diku). The bones-legal world's bet, `world_sha` + referee-legal verbs, is exactly the missing middle: mutation authority that is distributed in *what* may change (AUTHOR, rulings) and singular in *whether* it committed (the hash).

## Part II: five mechanics no modern game ships (ranked by Discord-text + receipts fit)

The W7 discipline: per mechanic-as-law, not per flavor. Modern games ship GM modes, housing, and threat meters; none ships these as legal structure the receipts enforce.

1. **The receipted ruling.** Every referee deviation from the written rule is a receipt row: what was ruled, which rule bent, why. Modern GM tools log actions, never rulings-as-artifacts. Fit: one receipt field + one render line; the bones chain was born for this. **Ship first.**
2. **The AUTHOR verb (player-authored legality).** Players author rooms that change traversal law for everyone, under referee refusal rows. Modern housing is cosmetic instancing; TinyMUD had it in 1989 and AAA walked it back. Fit: one verb + the existing room-table machinery; the referee keeps legality, the author keeps lore.
3. **The party as a legal unit.** Content that legally requires heterogeneous roles (enter is REFUSED to a monolithic party), with a shared governance ledger. Modern games suggest roles; none requires the party's structure. Fit: a predicate on the enter verb + the guild ledger receipt.
4. **The hate table as public truth.** Threat rendered as receipted rows, litigable after the rout. Modern threat meters are client-side addons; the server's truth is never shown, let alone receipted. Fit: extend the rout receipt; zero new mechanics, pure instrumentation honesty.
5. **Reset epochs as world law.** The world's respawn is a scheduled, receipted epoch counter inside `world_sha`, not an ambient side effect. Modern respawn timers are invisible constants; none is a citable world-law field. Fit: one counter + one receipt line per epoch bump.

## Part III: the one principle the bones-legal world violates today

**Player authorship.** The world is referee-authored only. Rooms, exits, and legality rows enter the `world_sha` domain solely by hand-authored tables; no verb exists by which a session (agent or human) proposes a room, and no refusal path says "your room is illegal because row 3 grants an exit the map does not have." TinyMUD shipped player building in 1989; DikuMUD shipped reviewed building in 1990; the bones-legal world, which otherwise carries the lineage's whole legal stack, has P4 = 0. The costs are concrete: the world's room count is frozen at authorship time, agents have no channel to mark discovered territory (the chronicle remembers deaths but cannot remember *places*), and the estate's strongest existing gesture toward authorship, `memory/game_modules/*.v1.json` as a WAD format (V-3 SHIPPED), has no world-side consumer. The fix is Part II's #2: the AUTHOR verb, referee-witnessed, refusal-typed, hash-committed, with the Patolli-clause discipline W7 already filed (the referee may refuse, never silently ignore).

---

## Constraint ledger

No git commands. No paid APIs. No web calls at all this lane: the standard record for D&D/MUD1/TinyMUD/DikuMUD/EverQuest/WoW is filed from own knowledge at summary level (dates, mechanisms, and the Corrupted Blood epidemiology note are standard-record claims; per-game P-scores are this lane's own rubric application, not cited measurements). Estate claims cite byte paths read this ask. W7's own verification log is the precedent for the rubric's application, not a source for this era's facts.

**Status: RECEIPT SEALED.** W8 era deep-weave complete: enumeration filed (W7 SEALED, W9 FILED, W8 landed here, 7 eras unlit with a proposed order), 6 games deep-unpacked (shell/core/scores/weave), era table filed, 5 modern-unshipped mechanics ranked, violated principle filed (player authorship, the AUTHOR verb).

*FW-33 stone closed 2026-09-28. Receipt: `watch/inbox/burn_reset_20260927/queue/Q-026.md`.*
