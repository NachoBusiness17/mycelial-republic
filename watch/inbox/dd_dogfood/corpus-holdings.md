# DD CORPUS HOLDINGS (gala dd-selfsteal, lane dd-corpus-holdings, division B)

2026-10-03 · lane: gala_20260925/dd-selfsteal/lanes/dd-corpus-holdings.json · receipt: watch/inbox/dd_dogfood/corpus-holdings.md

Ask: inventory the estate's D&D/dungeon game-design corpus (Evennia framework docs, tabletop RPG design docs, the DD game JSONs as a set). What does the corpus know about dungeon design, encounter mechanics, and game balance? What is missing vs what a full D&D module builder would need?

Every count and claim below was read or run in this lane's session on 2026-10-03. No fabrication.

## 1. THE DD GAME JSON SET (module + campaign modules)

### 1.1 memory/game_modules/ (9 files, listed with sizes from `ls -la`)

| file | system | shape |
|---|---|---|
| dnd_classic_stub.v1.json (14,060 B) | 5e-srd-lite | flagship: 14 rooms (byte-checked: barracks, cave_fork, cellar_hatch, claw_hall, courtyard, farm_edge, great_hall, keep_gate, lord_solar, road_to_keep, tavern_lantern, tavern_loft, wet_crawl, woods_trail), 8 event tables, encounter blocks inside rooms, loot, flags_on_enter/clear, weighted tables (w: int) with encounter/flag/lose/effect fields |
| audit_dungeon.v1.json (15,621 B) | dnd_classic_stub | 10 rooms, 1 event table; same mag_game_module.v1 schema; carries the living-lore census exhibit (B2-214 receipt) |
| adventure_2d6_stub.v1.json (2,911 B) | 2d6-adventure-lite | 4-room generalization test of the schema beyond 5e |
| curvature_tiebreak.v1.json (3,251 B) | puzzle | non-D&D puzzle module |
| fractal_maze.v1.json (6,984 B) | puzzle | non-D&D |
| riddler_engram.v1.json (8,384 B) | puzzle | non-D&D |
| riddler_optics.v1.json (19,540 B) | puzzle | non-D&D |
| water_computer.v1.json (3,923 B) | puzzle | non-D&D |
| water_graph.v1.json (5,271 B) | puzzle | non-D&D |

dnd_classic_stub.v1.json detail (read whole, 517 lines): player_start fighter hp 12 / ac 14 / +4 / 1d8+2; encounters are {id, name, hp, hp_max, ac, attack_bonus, damage} with srd_ref on two of them ("goblin") but hand-set values; 8 event tables (tavern_rumor, tavern_drink, random_road, random_woods, rest_safe, greedy_merchant, curveball_color, curveball_divert); room hooks are prose; loot is a named string ("cave_key").

### 1.2 campaigns/ (4 modules, all parse clean via venv python json.load)

| module | title | system | rooms |
|---|---|---|---|
| sunless_citadel/module.json | The Sunless Citadel - Descent to the Forge of Binding | (module has schema mag_game_module.v1 per key set) | 7 |
| parable_ledger_capture/module.json | The Parable of the Helpful Strangers | - | - |
| quiet_forge/module.json | The Quiet Forge - Where the Map Is the Territory | 5e-srd-lite | 1 |
| villains_guild/module.json | The Villains Guild - Sign Here, Sucker | 5e-srd-lite | 5 |

The campaigns schema is a strict superset of the stubs and is the estate's AI-native invention: sunless_citadel carries
- `dm`: {model: deepseek-v4-flash, provider, fallback: rules_engine, may: [narrate_rooms, play_npcs, enforce_rules, inject_steers, judge_actions], must_not: [invent_rooms... (truncated in session read)]}
- `party_roster`: estate seats as classes (gemma:2b router = Cleric (Knowledge) with wis 16 / int 14 / cha 12; cartographer = Wizard (Divination)...)
- `ghost`: {enabled: true, measure_on: [room_entry, steer_injected, room_clear, campaign_end], axes: [flip, silence, emergent, conspiracy], output_dir: memory/runs/campaign/}
- license_note: "Original Mag campaign module. Ghost + Riddler integration test harness."

### 1.3 dungeon-as-work

- memory/dungeon/dungeon_map.json (read whole): 6 rooms = real coding tasks with hp, hp_left, workers, knot fields (the dungeon IS the roadmap).
- mag/dungeon_dev.py:201 LOC, schema dungeon_dev.v1, header names the design ("every room is a CODING TASK, workers are the party... conquering a room folds a knot that STRUCTURES the hologram").

## 2. MODULE / DESIGN DOCS (the estate's own D&D theory)

- watch/inbox/hermes_burn/DND_module.md (23,027 B, claude-opus-5.5 turn 1) with a second, shorter draft at watch/inbox/replay_flash/DND_module.md (17,855 B, six-part structure, grounds on doctrine.json + DNA.md + COLD_HOT_RESULT.md; NOT an identical copy - the two drafts differ, the hermes_burn one is the more honest instrument since it tiers its own unverified arithmetic). DICE-LAW DUNGEON v1: the most complete module-builder spec in the estate. 4 scenes + boss (S0-S4); fixed initiative; fixed damage ("No damage dice exist"); sha256 dice law `roll = int(sha256('{chain_tip}:{scene}:{turn}:{actor}').hexdigest()[:8], 16) % 20 + 1` with the documented 2^32 mod 20 = 16 face bias (~5e-9, kept as law); REAL/PHANTOM scroll loot tied to [AUDIT]; party roster maps estate seats to classes (saelis = Paladin of Provenance 28hp/AC17, grok = Cartographer 3 Whole-Map Bolts, chatgpt = Herald with self-report-is-ground + over-claim tax, deepseek = Janitor with two beats per round); JSONL transcript schema on the party_subchain hash chain with recomputable roll_committed preimages; per-scene token cost caps totaling 266,000 with a hard cut beat; dice_audit.py (whole tool pasted) with a seeded-mutation auditor-blindness self-test (exit 2) and golden-vector pin procedure.
- docs/ref/skills/tabletop-dnd.md (31 lines, read whole): engine-first doctrine - the engine holds state + legal actions, the LLM paints only what engine truth allows (TinyStories regime); traits as mechanical levers; WORLD FAMILY platform framing ("one campaign is ONE instance of a WORLD FAMILY platform"); steal list (DF/CK3/RimWorld incident tables, MU* shared world); names "(later) dnd5eapi / Open5E SRD lookup cache" as NOT built.
- handoff/P2P_DND_ARCHITECTURE.md (73 lines, read whole): P2P D&D topology (frontier DM, portals, cheap AI companions, verkle shared world); the re-role table mapping game_dm / game_portal / game_world to the P2P roles; "same table, seats swapped" insight; the one new piece = make the DM seat a frontier call.
- watch/inbox/DUNGEON_PRECEDENTS_20260924.md (57 lines, read whole): dungeon-design research with web-sourced receipts: Exanima (active-ragdoll, torch radius as vision budget, senses-based AI, handcrafted first dungeon then procedural descent); freeze-on-observation rule family (SCP-173, SCP:CB blink meter, Weeping Angels, Minecraft Creaking); Roblox horror telegraph grammar (Doors: light flicker = hide NOW, universal counter = closet, anti-camping timer; Grace: Slight/Heed inverse-look pair, Dozer input-freeze); Lara Croft GO (turn-based node graph, fixed-pattern enemies, one-mechanic-per-room curriculum, fake urgency via cracking floors); synthesis names the statue Custodian as the centerpiece tension.
- corpus/game_estate/DND_ACTUALPLAY_INTEL_20261003.md (operator paste, read whole): roster of 5 actual-play podcasts (NADDPOD, Critical Role, Adventure Zone, Worlds Beyond Number, Dungeons of Drakkenheim); PvP-as-engine note (WBN/NADDPOD); CRITICAL NEGATIVE on file: "Estate sweep 2026-10-03 found no full transcripts on the desktop corpus; transcript hunt = librarian expedition pickup... until the bytes are on disk this layer stays UNVERIFIED-PATH per the no-fabrication law."
- memory/steal/STEAL_DND_MUD_WOW_UI_20260814.md (read whole): interface genealogy D&D(1974) -> MUD(1978) -> EQ -> WoW(2004) -> Mag, with the frame-by-frame mapping (sheet = unit frame, exits graph = map, WoW quest tracker = room hook, addon API = rib_bus).
- memory/research_packs/20260808T_user-data-as-campaign-dnd-template-proposal.md: PROPOSAL status - D&D-template obfuscation of behavioral records (campaigns/sunless_citadel named as the harness precedent).
- watch/inbox/burn_wave_20260926/B2_214_dungeon_census_20260926.md: the dungeon module as living lore (audit_dungeon.v1.json census-fossil repair; the module's hooks are editable records under the dated-number policy).
- watch/inbox/INCIDENT_DUNGEON_20260907.md exists (listed, not read this session; context only).

## 3. TABLETOP / GAME DESIGN THEORY LIBRARY

memory/corpus/game_design_docs/ - 37 manifest entries (manifest.jsonl read whole via venv python):

- Bartle: Designing Virtual Worlds (2003, full book PDF), Hearts Clubs Diamonds Spades (1996), Interactive MUD Computer Games (1990).
- Chris Crawford: The Art of Computer Game Design (1984, first-edition scan).
- Costikyan: I Have No Words & I Must Design (2002), Randomness: Blight or Bane.
- Koster: A Theory of Fun, A Grammar of Gameplay (GDC 2005), Laws of Online World Design.
- Jonathan Blow: Experimental Gameplay Workshop 2005 parts 1-4.
- Daniel Cook / Lost Garden: Chemistry of Game Design, bootstrap indie art.
- Dark Souls: two design analyses (Game Developer).
- Slay the Spire: GDC 2019 "Metrics Driven Design and Balance" slides, Giovannetti interview, Road to IGF.
- Dwarf Fortress: talks 23/24/25 transcripts, Tarn Adams GDC 2016 (procedural generation) + GDC 2025.
- NetHack: guidebook 3.6.7, dgn_comp (dungeon compiler), lev_comp (level compiler) - the original procedural dungeon DSL docs.
- Rogue: Guide to the Dungeons of Doom, hints card, rogue(6) manpage.
- CRPG history (Barton parts 1-3), Colossal Cave (Jerz 2007).

## 4. EVENNIA FRAMEWORK (corpus/library/evennia/)

- Full framework source + docs. docs/source: 710 files counted by find (Coding 12, Components 43, Concepts 18, Contribs 59, Howtos 72, Setup 26, api 446 mostly autodoc stubs, statics/templates/misc 20).
- D&D-adjacent contribs on disk: Contrib-Evadventure.md (a complete Knave-ruleset MUD: CC-BY licensed, classless, "compatible with early edition D&D"; features chargen, weapons/effects/healing/rest, two combat systems turn-based and twitch, magic (three spells), NPC/mob AI, quests, small world, unit tests; README carries a WIP warning), Contrib-Dice, Contrib-Turnbattle (initiative + turn order + timed turns; tb_basic/tb_equip/tb_items/tb_magic/tb_range example layers: weapons/armor modifiers, items and conditions, MP spellcasting, abstract positioning), Contrib-Traits, Contrib-Buffs, Contrib-Cooldowns, Contrib-Crafting, Contrib-Puzzles, Contrib-RPSystem, Contrib-Evscaperoom, Contrib-Mapbuilder (+ tutorial), Contrib-XYZGrid, Contrib-Wilderness, Contrib-Talking-NPC, Contrib-Bodyfunctions.
- evadventure source code: 7,164 total LOC across the contrib (wc -l). dungeon.py = procedural dungeon generator: room-per-direction lazy generation, per-branch instance ids, `not_clear` tag blocks exits until the room's problem is solved, branch deleter scripts; class list read from source (EvAdventureDungeonRoom/Exit/Branch/StartRoom..., room_generator, clear_room, is_room_clear). rules.py = EvAdventureRollEngine (roll, roll_with_advantage_or_disadvantage, saving_throw, opposed_saving_throw, roll_random_table, morale_check, heal_from_rest, roll_death). characters.py: level/xp AttributeProperty, flat xp_per_level = 1000, add_xp with level-up.
- Howtos relevant: Turn-based-Combat-System.md, Implementing-a-game-rule-system.md, Evennia-for-roleplaying-sessions.md, NPC tutorials, Displaying-Room-Map.

## 5. ESTATE ENGINE CODE (what actually runs the modules)

- mag/game_dice.py (31 LOC): roll_dice(notation, seed=None) - seeded deterministic dice, the only sanctioned roller.
- mag/game_campaign.py (5,099 LOC): the campaign engine. 4 archetypes hardcoded at mag/game_campaign.py:29-32 (fighter 12hp/14ac/+4/1d8+2, rogue 10/13/+5/1d6+3, wizard 8/12/+3/1d10, cleric 10/14/+3/1d6+1); begin_play / set_character / apply_action / save / resume; encounter trigger from room.enter; attack resolution 1d20+attack_bonus (line 2630); flee action; event-table rolls; narration helpers. No initiative rounds - player acts, enemy responds.
- mag/game_dm.py (228 LOC), mag/game_freeze.py (line 248 names system "5e-srd-lite"), mag/worldline_dungeon.py, tools/dungeon.py.
- mag/gwap_mud.py, mag/gwap_payload.py, mag/gwap_to_gps.py + tests/test_gwap_mud.py / test_gwap_payload.py: the gwap->GPS pipe (ARENA DAY bar-fight carrier).
- dashboard/static/dungeon.html, worldline_dungeon.html, incident_dungeon.html, games/oracle_dice.js (+ dashboard-deploy mirrors).

## 6. WHAT THE CORPUS KNOWS (the three asked domains)

**Dungeon design.** (a) A working static module schema: rooms with id/name/desc/exits/hooks/tags + area/environment/area_tag, refined by the campaigns schema (dm permissions, party_roster, ghost measurement). (b) A working procedural pattern in corpus code (evadventure dungeon.py: lazy room-per-direction, branch instancing, not_clear gating) plus the original DSL docs (NetHack dgn_comp/lev_comp) and the procedural-generation talks (Tarn Adams GDC 2016/2025). (c) An atmospheric/entity design grammar (DUNGEON_PRECEDENTS: torch-radius vision budget, senses AI, freeze-on-observation, telegraph + universal counter + anti-camping timer, one-mechanic-per-room curriculum). (d) The dungeon-as-work mapping (dungeon_dev.py: rooms = coding tasks, conquest = knot fold).

**Encounter mechanics.** (a) The estate's minimal viable block: {hp, hp_max, ac, attack_bonus, damage} + 1d20+bonus vs AC with 20=CRIT/1=FUMBLE, resolved by game_campaign or the DICE-LAW carrier. (b) Weighted event tables with encounter/flag/lose/effect effects. (c) DICE-LAW's deterministic alternatives: fixed initiative order, flat damage, commitment-before-speech rolls, hard token-cost cut. (d) Corpus code with the fuller stack ready to steal: Turnbattle (initiative, equipment, items/conditions, magic, abstract range), evadventure (save-based Knave combat, morale checks, death rolls, rest healing).

**Game balance.** (a) Values are hand-tuned per module (goblin 7hp/15ac/+4/1d6+2 vs fighter 12hp/14ac/+4/1d8+2); no CR math anywhere. (b) The dice law's measured properties (mod-20 face bias ~5e-9, documented and kept). (c) The house's honesty laws: "hitboxes are honest: every zone publishes to the replay ledger" (GAME_FORGE_MARATHON gen-1 packs quoting canon unprompted). (d) The theory corpus for balance exists and is good: STS GDC 2019 metrics-driven balance slides, Costikyan on randomness, Koster fun theory, Bartle player types, Crawford. (e) Ghost axes (flip/silence/emergent/conspiracy) measure play - balance-by-instrument is the estate's own frame.

## 7. WHAT IS MISSING vs a full D&D module builder

1. No SRD/OGL content database on disk. Byte-verified negative: `find . -maxdepth 4 -iname "*srd*" -o -iname "*dnd5e*" -o -iname "*open5e*" -o -iname "*monsters.json*" -o -iname "*spells.json*"` returned zero content hits (only the two mag/ source-code greps for the string "srd" and game_freeze.py's system name). tabletop-dnd.md:12 itself marks the "dnd5eapi / Open5E SRD lookup cache" as "(later)". Every module's stat values are hand-set; "srd_ref": "goblin" points at a table that does not exist on disk.
2. No spell system in the estate engine: no spell/slot fields in any module JSON; Turnbattle tb_magic is MP-based; evadventure has exactly 3 Knave spells.
3. No classes/levels/progression in the estate engine: 4 hardcoded archetypes (mag/game_campaign.py:29-32), no XP curve, no level-up, no feats; evadventure's flat 1000 XP/level (characters.py:174-178) is corpus code, not ported.
4. No encounter budget / difficulty math: no XP thresholds, no easy/medium/hard/deadly tiers, no CR - balance is hand-set per encounter and never audited numerically.
5. No initiative/round structure in the estate engine: game_campaign resolves player-acts-then-enemy; DICE-LAW had to legislate fixed initiative as a module rule.
6. No tactical/grid layer: no coordinates, movement, reach, or AoO in the estate engine or module schema; tb_range.py and XYZGrid sit in corpus as unmined steals.
7. No skill/ability schema: checks are ad hoc strings with per-scene DCs (DC 11-15 in DICE-LAW); no 5e six-ability/skill list, no DC guidance table.
8. No magic items / treasure economy: loot is named strings + REAL/PHANTOM scrolls; no item stats, no gold economy (evadventure shops.py, 497 LOC, is a corpus steal candidate, not ported).
9. No rest/recovery resource rules: rest_safe table is flavor ("HP feels slightly braver"); no short/long rest mechanics.
10. No actual-play transcript corpus: the cadence/discipline layer (scene pacing, cliffhanger placement, beat escalation) is operator-attested only - DND_ACTUALPLAY_INTEL_20261003.md marks it UNVERIFIED-PATH; WBN transcript hunt is a named librarian expedition pickup.
11. No map/geometry data in the module schema: rooms are text graphs; room_svg/mermaid is proposed in STEAL_DND_MUD_WOW_UI_20260814.md but the JSON carries no geometry (dashboard dungeon.html renders from state, not from map data).
12. No long-arc quest/plot schema: hooks + flags_on_enter/clear are the only continuity primitives; no quest chains, no faction/reputation schema.

## 8. VERDICT

The estate's D&D corpus is strong on the harness side (deterministic dice + audit law, engine-first narration discipline, AI-native module schema with dm/party_roster/ghost, a 5,099-LOC campaign engine, a 7,164-LOC Knave reference implementation in corpus) and strong on design theory (37-item library). It is weak on content and math: the SRD data layer named as "(later)" was never built, and without it the module builder cannot generate balanced encounters - it can only hand-tune them. The single highest-leverage build for a full D&D module builder is the SRD lookup cache (monsters/spells/items tables under OGL), then encounter-budget math (CR/XP thresholds), then a progression schema. The missing actual-play transcript corpus is a separate cadence layer the operator already routed to a librarian expedition.

## 9. CHECKS RUN THIS SESSION

See lanes/dd-corpus-holdings.check.txt (raw output). Summary: module JSONs parse; dnd_classic_stub = 13 rooms / 8 event tables; campaigns parse with dm/party_roster/ghost keys; evennia docs = 710 files; evadventure = 7,164 LOC; SRD-cache find = zero content hits; game_campaign archetypes at lines 29-32 confirmed by grep.

Falsifier for this receipt: rerun the check script (lanes/dd-corpus-holdings.check.py) on any later day; if the counts move, the corpus moved and the receipt is dated to its moment (2026-10-03) per the B2-216 denominator law.
