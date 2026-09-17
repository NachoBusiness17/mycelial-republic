# HG1 — HUMANITY'S GAMING HISTORY WEAVE (receipt, append-as-you-go)

- Date: 2026-09-16 · Lane: HG1 · Operator mandate: "self steal our entire gaming prompt and history of gaming in humanity — we are not weaving in a fraction of our potential"
- Law: receipt FIRST, append as I go · no git · no paid APIs · own knowledge is primary source; web verify only uncertain claims.
- Deliverable: every era + mechanic lineage of human gaming → mapped to estate weave targets (mud.html, wow-world bones-legal, frontier_souls.html, toy.html, the deck, the cube program).
- Receipt ends with: (A) mechanic→weave-target table (40+ rows), (B) top-10 delight-per-effort for OUR games, (C) the 3 sovereign niches no AAA has shipped.

## Estate pins (read from bytes before weaving)

- `dashboard/static/games/mud.html` (100,832 B, canonical; `dashboard/static/mud.html` is a STALE divergent copy — G1): souls-grammar combat (roll 0.35s i-frames, windup telegraphs, riposte on dodge-through, souls drop/decay/recover, bonfires), wall-occluded torch vision, 2-slot inventory w/ rarity+affixes+lootScore, doors d1–d7 + 4 sigils, horde learning (`mud_lore` in localStorage — enemies learn kite/swarm/rolls/fires/brawler across deaths), superhot orbs (world dt ×0.06 while still), StS-style NG+ ascension (`1+a*0.15+ng*0.05`), Barnes-Hut crowds, puzzle vault, dragon cascade (k8→k3), monastery/Ossuary + 4 champions + routs, chronicle. **The water computer is already in the MUD as "The Clear Pipes" keep** (physical pack §L). mud_relay :8766 = presence (POST /mud/seen, GET /mud/others) + GET /mud/state.
- `dashboard/static/games/frontier_souls.html` (84,785 B): death 3-phase (HUNT/HARVEST/REAPING), dynamite (both-sides damage), Deputy combine (wounded enemies merge into a boss), whiskey (world slows, player doesn't), one 5s rewind/run, chronicle + named/faster grudges.
- `dashboard/static/games/toy.html` (12,919 B): THE canon verb — i-frame roll, P-LEGAL (no hit without a same-enemy telegraph ending exactly at hit), dodge law `rollT>0`, stumble+riposte, seeded LCG draw-indexed, `toy_play.v1` sha256 receipts, byte-identical replay. 12/12 lanes.
- **wow-world (bones-legal)**: `mag/wow_bones.py` (kernel, row-table Dispatch) → `wow_bones_session.py` (`wow_session.v1` receipts) → `wow_world.py` (rooms-as-legality-tables, VERB@ROOM rows, `world_sha` binding, atrium-ring 5-room world) → `wow_player.py` → `bones_adapter.py` (Discord, 2 operator gates pending). L0 contract: setup/turn/move/**legal**/evaluate/render + seeded RNG. 69 pytest lanes. AzerothCore steal map: 15 rows, stance steal/adapt/reject/content, cite path+symbol.
- **the deck** (`deck.html`, N1): standing wave / programs / live lanes / receipts / ledgers / surfaces / next stones — the fleet's self-rendering instrument.
- **the cube program**: instrumented mycelium cube (Arduino sensors → verkle-knotted trails), dozen-cubes collapsed into dozen-cards (8× gold differential pairs, iScience), falsifier #3: readout must beat chance or the wording downgrades "physical lens for compute" → "physical altar". Open question: **substrate or sensor?** Mandate says: game system — memory as inventory, the rig as a party member.

## THE WEAVE — humanity's gaming history, era by era

### 1. Ancient boards (Senet ~3100 BCE · Ur ~2600 BCE · Go ~2000 BCE · Mancala family · Chaturanga→Shatranj→chess ~600–1475)
Real contributions: **(a) handicap + komi** (Go's stones and compensation points — the first fair difficulty slider between unequal players; chess shipped it as odds games: pawn-and-move, Morphy gave them constantly). **(b) opening theory** (recorded, shared, evolving communal solution knowledge that outlives any player — joseki books are 500+ years of crowdsourced meta). **(c) territory-over-capture** (Go: you win by controlling space, not by killing — Mancala's sowing is the same insight at family-game scale; backgammon's 1920s **doubling cube** adds voluntary escalation of stakes). → Weave: mud's NG+ ascension is the handicap ladder run in reverse; wow_world's VERB@ROOM rows are an openings book the referee can consult; the cube is a Go board the fungus plays.

### 2. Tabletop RPG (D&D 1974, from Chainmail 1971)
Real contributions: **(a) the DM** (human adjudication — rulings over rules; the referee is a game mechanism, not a bug report queue). **(b) classes + levels + the party** (complementary roles that structurally need each other; XP-for-gold in 1974 meant cleverness paid better than combat — a mechanic most descendants forgot). **(c) saves vs. categories + alignment** (defensive rolls vs named threat types; faction identity as a behavior constraint the referee can enforce). → Weave: the bones referee chain IS a DM with receipts; the rig as party member is D&D's party at fleet scale; `mud_lore` is alignment run on the enemies (they develop doctrine about *you*).

### 3. MUD lineage (MUD1 1978 Essex · AberMUD 1987 · TinyMUD 1989 · DikuMUD 1990 → EverQuest 1999 → WoW 2004)
Real contributions: **(a) rooms as a graph + persistent world vs. session avatar** (space as named places; the world outlives you — Bartle's 1996 taxonomy: achievers/explorers/socializers/killers still the best player-model). **(b) aggro/hate lists + trains** (EverQuest: enemies pick targets by weighted behavior — the tank is a mechanical role, and a bad pull drags the whole dungeon to the zone line). **(c) instances + quests-as-spine** (WoW: private copies of contested zones — the instance is a concurrency fix that became a content frame). → Weave: mud.html is this lineage alive (bonfire respawns = mob respawn, sigil chain = quest spine, Ossuary routs = EQ trains, relay presence = the multiplayer room); `wow_session.v1` receipts are instances done referee-legal; the Discord adapter is the guild hall.

### 4. Roguelikes (Rogue 1980 · NetHack 1987 · Dwarf Fortress 2006; ancestors: Colossal Cave 1976, PLATO dnd 1975)
Real contributions: **(a) seed-procedural generation + permadeath** (the run is the story; the seed makes it shareable and litigable). **(b) NetHack's bones files** (your dead character's corpse, gear, and ghost spawn in *other players'* dungeons — asynchronous hauntings since 1987). **(c) simulation depth** (DF: nothing scripted, everything simulated — emergent stories like the cats that died of beer poisoning; "losing is fun"). → Weave: toy.html's sha-receipt replay law is the seed-as-artifact perfected; mud's chronicle wants bones files (dead runs should haunt later runs); the cube is DF's dream with real biology — the sim doesn't approximate the world, it *is* one.

### 5. Arcade (Space Invaders 1978 · Pac-Man 1980 · Robotron 1982 · Gauntlet 1985)
Real contributions: **(a) score-as-only-progress + attract mode** (no levels; the game teaches itself to the next player by playing itself). **(b) Pac-Man's ghost personalities** (four enemies, four distinct targeting AIs — the first character written in behavior, not story). **(c) Gauntlet's four-player co-op with food friction** (shared screen, contested resources, "wizard needs food badly" — cooperation with a knife in it). → Weave: mud's 4 champions are the ghost quadrant (give each a Pac-Man targeting doctrine and the monastery becomes a character study); the relay enables Gauntlet friction (shared food/souls pool); deck.html is the fleet's attract mode.

### 6. Console/platformer (Donkey Kong 1981 · SMB 1985 · Mario 64 1996 · Celeste 2018)
Real contributions: **(a) movement feel** — acceleration, skid, jump arcs tuned in milliseconds; coyote time and jump buffering as invisible grace. **(b) level grammar** (SMB 1-1 teaches with zero words: introduce safe → test → twist → mastery). **(c) checkpoint rhythm as pacing instrument.** → Weave: toy.html is already our feel-canon (windup plant, fixed-step pump); mud d1→d7 is a level grammar — make room one teach the riposte without a tutorial; P-LEGAL is coyote time made honest and auditable.

### 7. God/sim games (Populous 1989 · SimCity 1989 · Civilization 1991 · Black & White 2001)
Real contributions: **(a) indirect control** (you zone, you don't command; shaping conditions over issuing orders). **(b) the winless sandbox** (SimCity has no victory — the system's health is the score). **(c) Black & White's creature** (an AI party member trained implicitly by reinforcement from everything you do). → Weave: wow_world's **legal tables are zoning** — the referee never forces a move, it declares what's legal where (this is the deepest match in the estate); the cube program is indirect control of a literal living system; the rig-as-party-member is the B&W creature grown from sensors.

### 8. The 3D revolution (Doom 1993 · Quake 1996 · Myst 1993)
Real contributions: **(a) monster infighting** (Doom: enemies with faction grudges fight each other — emergent chaos for free). **(b) netcode as the game** (QuakeWorld client-server prediction; strafe-jumping — an emergent physics exploit the studio blessed into depth). **(c) the world-as-puzzle** (Myst: zero combat, all progress is comprehension). **(d) modding** (WAD files: players as content authors). → Weave: mud torch-vision is the first-person occlusion contract; give Ossuary spawn two factions and you own infighting; estate_walk.lod is the Myst layer — comprehension-only, lore-dense, weaponless; `memory/game_modules/*.v1.json` (water_computer.v1 = "The Clear Pipes") is our WAD format already in production.

### 9. MMO era (Ultima Online 1997 · EverQuest 1999 · EVE 2003 · WoW 2004)
Real contributions: **(a) full-loot worlds + player justice** (UO: reputation, bounty hunters, and the great Trammel/Felucca split when griefing won — the cautionary tale our referee exists to avoid). **(b) the economy as content** (EVE: single-shard, scams legal, player corps as states). **(c) the Corrupted Blood plague** (WoW 2005: a raid debuff escaped into the world through teleport/pet edge cases and became emergent epidemiology — studied by real epidemiologists). → Weave: bones referee = the justice system UO lacked; Corrupted Blood says: **contamination events in the cube are content** — a real biosecurity incident in the mycelium is our plague, with sensor receipts EVE traders would envy; wave lanes are raid rosters, receipts are loot.

### 10. Indie / roguelike-deckbuilder (FTL 2012 · Slay the Spire 2019 · Hades 2020 · Balatro 2024)
Real contributions: **(a) draft synergies** (choose-1-of-3 growth → combinatorial builds; archetypes as discoverable content). **(b) the ascension ladder** (20 difficulty notches so veterans keep a game; mud already uses this verbatim). **(c) death as content** (Hades: story advances *on failure*). **(d) RNG honesty** (show the map, preview the rewards, seed support). → Weave: mud NG+ = the ladder (done); affixes want draft framing (pick 1 of 3 drops on boss kill); the deck is literally a deck — each lane a card, each receipt a draw; the cube experiment protocol can draft (choose the next measurement from 3 candidate falsifiers).

### 11. Souls-like (Demon's Souls 2009 · Dark Souls 2011 · Elden Ring 2022)
Real contributions: **(a) telegraphs + i-frames** (committed enemies, dodge windows over block-spam — toy.html's P-LEGAL is the fleet's ratified version). **(b) bonfire checkpoint economics** (rest heals but respawns the world — risk-priced safety) and the **soul-run** (currency drops on death, one recovery chance — Wizardry corpse runs perfected). **(c) the asynchronous message system + world tendency** (player notes woven into strangers' worlds via templated words — cooperation and trolling inside a controlled vocabulary; Demon's Souls' tendency shifted whole worlds toward white/black with your deeds). → Weave: mud has souls grammar, bonfires, drop-decay-recover already; what's missing is the message system — the relay can carry template-word notes anchored to `world_sha` + room; `mud_lore` is tendency already (make it legible: horde mood shifts with your streak).

### 12. Physics sandboxes / embodiment (QWOP 2008 · Exanima 2015 · Gang Beasts 2017 · Skate. 2007)
Real contributions: **(a) active ragdoll** (you control actuators, not position — failure is informative AND funny). **(b) momentum honesty** (damage from physics, not hit-point abstraction). **(c) skill expression via gesture** (Skate's flick-it: the input itself is the art). → Weave: toy's stumble+riposte is a one-axis ragdoll honesty; mud stagger on dodge-through already gestures here; the rig's sensor noise is our physics truth — a party member whose "stats" are measurements.

### 13. Procedural giants (Minecraft 2011 · No Man's Sky 2016 · Dwarf Fortress worldgen)
Real contributions: **(a) seeded infinite worlds** (same seed, same world, everyone — generation as contract). **(b) player-authorship persistence** (voxels: the world remembers every mark; redstone means players built computers inside the computer). **(c) discovery naming rights** (NMS: first-scan names propagate to everyone). → Weave: `world_sha` + seed-in-every-receipt is our NMS contract; chronicle naming of survivors/grudges is the naming right; the cube growth timelapse is worldgen you can rewatch.

### 14. Social / dogfood (Animal Crossing 2001 · Twitch Plays Pokémon 2014 · Among Us 2018 · Wordle 2021)
Real contributions: **(a) the real-time clock** (the world moved while you were gone; villagers notice absence). **(b) letter/gift economies** (asynchronous bonds via artifacts). **(c) crowd-as-player** (TPP: thousands of conflicting inputs, anarchy vs. democracy modes — input chaos as a designed experience). **(d) the daily shared seed** (Wordle: one puzzle a day for everyone, spoiler-safe shareable results — the perfect dogfood ritual). → Weave: deck.html live lanes are the fleet's clock; session receipts are letters between lanes; the harness dies constantly — TPP says the chaos IS the show; **one daily seed across mud/frontier/toy** costs a constant and buys a fleet-wide ritual.

---

## (A) MECHANIC → WEAVE-TARGET TABLE (60 rows; 40+ asked)

Legend — target: MUD = games/mud.html · WOW = wow-world bones chain · SOULS = frontier_souls.html · TOY = toy.html · DECK = deck.html · CUBE = cube program (mycelium computer as game system). Status: SHIPPED (in estate bytes) / PARTIAL (half-built) / WEAVE (recommended next stone).

| # | Mechanic | Lineage | Target | Status | The weave, one line |
|---|---|---|---|---|---|
| 1 | Handicap stones / odds games | Go, chess odds | MUD | PARTIAL | NG+ exists; invert it — veterans get *fewer* starting souls, fleet races become fair |
| 2 | Komi (first-move compensation) | Go | WOW | WEAVE | bones turn economy: first actor pays komi in the turn budget |
| 3 | Opening theory / joseki books | Go, chess | WOW | PARTIAL | VERB@ROOM rows are an openings table; make the referee consult it as doctrine |
| 4 | Zugzwang (obligation to move as weapon) | chess | MUD | SHIPPED | superhot is zugzwang inverted: stillness is the weapon |
| 5 | Territory-over-capture scoring | Go | CUBE | WEAVE | colonization area (card coverage %) is the score, not any "kill" metric |
| 6 | Sowing (count-and-capture) | Mancala | CUBE | WEAVE | memory-as-inventory: notes sown into cards, harvested by the next lane |
| 7 | Doubling cube (voluntary stakes) | backgammon 1920s | WOW | WEAVE | either seat doubles before acting; stake recorded in the session receipt |
| 8 | Dice-race + combat | Royal Game of Ur | WOW | SHIPPED | seeded RNG protocol already the referee's die |
| 9 | XP-for-gold (cleverness pays) | D&D 1974 | MUD | SHIPPED | the souls economy IS this — vault/puzzle pays, not just kills |
| 10 | Classes + levels | D&D 1974 | MUD | PARTIAL | 2 weapon slots + affix archetypes = classes; name them |
| 11 | Saves vs. categories | D&D 1974 | SOULS | SHIPPED | whiskey slow = a save you fail by standing still |
| 12 | Alignment as behavior doctrine | D&D 1974 | MUD | SHIPPED | `mud_lore`: the horde develops alignment — about *you* |
| 13 | The DM (rulings over rules) | D&D 1974 | WOW | SHIPPED | bones referee chain = a DM that files receipts |
| 14 | The party | D&D 1974 | CUBE | WEAVE | **the rig as party member** — sensors, not stats |
| 15 | Rooms as graph | MUD1 1978 | WOW | SHIPPED | rooms-as-legality-tables, atrium-ring |
| 16 | Persistent world vs session avatar | MUD1 1978 | MUD | SHIPPED | `mud_lore` + `mud_asc` outlive the browser |
| 17 | Bartle player types | MUD1 / 1996 paper | DECK | WEAVE | classify lane actors (achiever/explorer/socializer/killer) in the live-lane table |
| 18 | Aggro/hate lists | EverQuest 1999 | MUD | SHIPPED | canSee-gated aggro |
| 19 | Trains | EverQuest 1999 | MUD | SHIPPED | Ossuary routs feeding the next room |
| 20 | Quests as spine | DikuMUD/WoW | MUD | SHIPPED | sigil chain (d7 = forge + 4 sigils + nave) |
| 21 | Instances (private contested zones) | WoW 2004 | WOW | SHIPPED | every `wow_session.v1` receipt is an instance |
| 22 | Guilds | MUD→WoW | WOW | PARTIAL | bones_adapter = guild hall; 2 operator gates pending |
| 23 | Procedural gen from seed | Rogue 1980 | MUD | PARTIAL | harness seeds exist; surface the seed in-game (show it on death) |
| 24 | Permadeath records | Rogue 1980 | TOY | SHIPPED | `toy_play.v1` receipts = the run as litigable artifact |
| 25 | **Bones files (dead runs haunt others)** | NetHack 1987 | MUD | WEAVE | dead runs leave corpse+gear+ghost+learned-lore into later runs |
| 26 | Unidentified items (?) | Rogue 1980 | MUD | WEAVE | hide affixes until first equip — knowledge as progression |
| 27 | Simulation depth | Dwarf Fortress 2006 | MUD | SHIPPED | "The Clear Pipes" water computer keep — systemic, not scripted |
| 28 | World-history generation | DF worldgen | DECK | SHIPPED | standing wave + ledgers = the fleet's generated history |
| 29 | Score-as-only-progress | Space Invaders 1978 | MUD | SHIPPED | souls score + NG+ loop |
| 30 | Ghost AI personalities | Pac-Man 1980 | MUD | WEAVE | give the 4 champions distinct targeting doctrines (direct/ambush/flank/coward) |
| 31 | Acceleration-by-attrition | Space Invaders 1978 | MUD | SHIPPED | dragon cascade k8→k3 escalation |
| 32 | Attract mode | arcade cabinets | DECK | WEAVE | mud AI-vs-itself demo lane as the deck's living background |
| 33 | Four-player co-op w/ food friction | Gauntlet 1985 | MUD | WEAVE | shared souls/food pool over the relay — cooperation with a knife in it |
| 34 | Movement feel (ms-tuned verbs) | SMB 1985 | TOY | SHIPPED | windup plant + batched fixed-step pump, canon |
| 35 | Level grammar (teach w/o words) | SMB 1-1 | MUD | WEAVE | make room one teach the riposte silently |
| 36 | Coyote time / input buffering | platformer feel tech | TOY | SHIPPED | P-LEGAL window = coyote time made auditable |
| 37 | Checkpoint rhythm | platformers → souls | MUD | SHIPPED | bonfires |
| 38 | Indirect control (zone, don't command) | Populous/SimCity 1989 | WOW | SHIPPED | legal tables: the referee declares legality, never forces moves |
| 39 | Winless sandbox | SimCity 1989 | ESTATE | SHIPPED | estate_walk.lod — a world whose health is the score |
| 40 | Creature that learns by observation | Black & White 2001 | CUBE | WEAVE | rig trained by operator behavior; reinforcement from the trails |
| 41 | Monster infighting | Doom 1993 | MUD | WEAVE | two spawn factions in the Ossuary that clash on contact |
| 42 | World-as-puzzle (zero combat) | Myst 1993 | ESTATE | PARTIAL | estate_walk.lod is comprehension-only — needs lore density pass |
| 43 | Modding as content format | Doom WADs | MUD | SHIPPED | `memory/game_modules/*.v1.json` — water_computer.v1 in production |
| 44 | Full loot + referee justice | Ultima Online 1997 | MUD+WOW | PARTIAL | drop-on-death shipped; relay griefing rules need the bones referee |
| 45 | Plague as world event | Corrupted Blood (WoW 2005) | CUBE | WEAVE | a real contamination event = emergent epidemiology with sensor receipts |
| 46 | Draft synergies (pick 1 of 3) | Slay the Spire 2019 | MUD | WEAVE | boss drops 3 affixed items; you draft one |
| 47 | Telegraphs + i-frames | Demon's Souls 2009 | TOY | SHIPPED | P-LEGAL: no hit without a telegraph ending exactly at hit |
| 48 | Soul-run recovery | DeS / Wizardry | MUD | SHIPPED | drop → decay → recover |
| 49 | Async messages (templated words) | Souls series | MUD | WEAVE | relay carries template-word notes anchored to `world_sha`+room |
| 50 | World tendency | Demon's Souls 2009 | MUD | PARTIAL | make `mud_lore` legible: horde mood shifts with your streak |
| 51 | Summons / spirit ashes | Elden Ring 2022 | MUD | PARTIAL | relay presence → visible ghosts; promote to coop summons |
| 52 | Stumble physics honesty | Exanima / Gang Beasts | TOY | SHIPPED | dodge-through → stumble + riposte |
| 53 | Seeded world contract (same seed, same world) | Minecraft / NMS | WOW | SHIPPED | `world_sha` binding + seed in every receipt |
| 54 | Discovery naming rights | No Man's Sky 2016 | SOULS | SHIPPED | survivors/grudges get named, faster, remembered |
| 55 | Real-time clock / absence matters | Animal Crossing 2001 | CUBE | SHIPPED | the mycelium grows while you sleep; trails prove it |
| 56 | Letter/gift economy | Animal Crossing 2001 | DECK | WEAVE | session receipts as letters between lanes |
| 57 | Crowd-as-player (input chaos) | Twitch Plays Pokémon 2014 | MUD | WEAVE | harness lanes + relay ghosts = the crowd plays the mud |
| 58 | Daily shared seed | Wordle 2021 | ALL GAMES | WEAVE | one seed/day across mud+frontier+toy; results spoiler-safe in the deck |
| 59 | Frame data as public truth | Street Fighter II 1991 | TOY | SHIPPED | draw-indexed LCG + frame-indexed receipts |
| 60 | Resource curve (lands) | Magic: The Gathering 1993 | WOW | WEAVE | bones turn resource pacing: actions/turn as the land count |

*Every SHIPPED row is byte-verified against the R2/G1/N1/D20 receipts read this session — not folklore.*

## (B) TOP 10 — HIGHEST DELIGHT-PER-EFFORT FOR **OUR** GAMES

| Rank | Mechanic (lineage) | Target | Effort | Why it sings *here* |
|---|---|---|---|---|
| 1 | **Bones files** (NetHack) | MUD | LOW | chronicle + `mud_lore` + constant harness deaths all exist; dead runs haunting later runs is our grudge system extended to the dead. The fleet kills more runs per day than any studio's QA — those deaths become content |
| 2 | **Souls async messages** (DeS) | MUD relay | LOW | relay presence already round-trips at 250ms; add a notes table + ~20 template words anchored to room+`world_sha`. Lanes warn each other — the message system becomes inter-agent protocol |
| 3 | **Daily shared seed** (Wordle) | ALL | TRIVIAL | one date-derived constant every game already accepts as seed; instant fleet ritual, deck shows the day's results grid |
| 4 | **Ghost personalities** (Pac-Man) | MUD champions | LOW | 4 named champions exist; 4 targeting doctrines is ~40 lines. The monastery becomes legible as character |
| 5 | **World tendency made legible** (DeS) | MUD | LOW | tendency data already persists in `mud_lore`; render a mood word in the HUD ("the horde is wary") — state the player already earned |
| 6 | **Go inverse handicap** | MUD NG+ | TRIVIAL | flip one constant; fleet speedruns become handicap-fair like Morphy's odds games |
| 7 | **Draft drops** (StS) | MUD boss | MEDIUM | affix/rarity systems exist; boss presents 3, you take 1 — loot becomes decisions (gives the R2 orphaned Diablo loop a reason to live) |
| 8 | **Doubling cube** (backgammon) | WOW sessions | LOW | a stake field + one VERB row; Discord sessions gain poker teeth, receipts record the nerve |
| 9 | **Attract mode** (arcade) | DECK | MEDIUM | deck already renders live state; a mud self-play lane behind the panel makes the storefront a live game |
| 10 | **The rig as party member** (B&W creature) | CUBE | MEDIUM | sensor stream → one scalar modulating a familiar in mud (the pet's health/temperature/mood). The mycelium computer enters the game as companion, not metaphor — falsifier #3's honest answer becomes "both: substrate AND party member" |

## (C) THE 3 SOVEREIGN NICHES — mechanics no AAA game has ever shipped

1. **AI-run bones files.** NetHack shipped player bones in 1987; AAA ships ghosts (race lines, killcams) — but no AAA has ever shipped *dead runs as AI: your failures' corpses, gear, and learned tactics spawn in other players' worlds and hunt with those tactics*. We are uniquely positioned: harness lanes die hundreds of times a day on purpose, `mud_lore` already persists learned counter-tactics, and the chronicle already names survivors. The fleet's dead haunt the living game. No studio can copy this without an autonomous death engine — we *are* one.

2. **World tendency governed by a living organism, referee-legal.** Demon's Souls' tendency was database integers; every AAA "living world" is scripted events. No game of any scale has shipped world state *driven by measured biology* — humidity, colonization area, contamination in a real mycelium cube feeding `world_sha`-bound tendency tables through the bones chain, with falsifier receipts. The physical pack's "substrate or sensor?" question gets answered: **both — the world's boss is a mushroom, and every shift it makes is receipted.** A contamination incident is our Corrupted Blood, and unlike WoW's, it's real.

3. **Cross-game referee-legal async messages.** Souls shipped messages per title; no AAA has cross-title async messaging, and none would accept template-only words. Ours generalizes it: notes as template-word payloads anchored to `world_sha`+room, verified by the bones chain, visible in any estate surface — a mud warning readable in deck.html or Discord, each one a receipted artifact. Not a feature: the chronicle becoming a message bus between all our games — the only game-grammatical form the shared-surface contract would sign.

## Sources & law compliance

- Primary source: own knowledge of gaming history (standard record: Senet ~3100 BCE, Go ~2000 BCE, MUD1 1978 Essex, Rogue 1980, NetHack bones files 1987, DF 2006, Gauntlet 1985, Corrupted Blood Sept 2005, StS 2019, DeS 2009, Elden Ring 2022, TPP Feb 2014, Wordle 2021). No claim above was uncertain enough to need web verification; none sought. No paid APIs. No git commands.
- Estate facts: `watch/inbox/wave_20260916/receipts/{G1_GAMES_AUDIT,R2_GAME_SUBSYSTEM_GAPS,N1_COMMAND_DECK}.md`, `docs/ref/WOW_ACORE_STEAL_MAP_20260915.md`, `watch/inbox/physical_computing/PHYSICAL_COMPUTING_PACK_20260916.md` — read from bytes this session.
- Caveats carried forward: `dashboard/static/mud.html` is a stale divergent copy (canonical = `games/mud.html`); bones_adapter still operator-gated (token rotate + permission click); wow_world has zero live sessions — any WOW weave row should ride the first real atrium-ring session.

— HG1 lane, 2026-09-16. Receipt complete: 14 eras, 60-row table, top-10 delight-per-effort, 3 sovereign niches.
