# WITNESSES — the thirteen reports behind FROM_MUD_TO_WOW_20260914.md

Condensed from the fifty-wide sweep (2026-09-14). Full verbatim reports in the session transcript. Tri-state standard: VERIFIED (file/URL opened) / PLAUSIBLE / UNVERIFIED.

## W1 — Game & engine history
- 2026-08-07: campaign engine predates the game (server-authoritative, Infocom verbs, commit e96fd62a4)
- 2026-08-11: mandate ("lead-in game… once you're a game it goes vertical with adoption") + Stone 1 persona_recall
- 2026-08-13: doctrine day — entry gate, world render, ramp, DFHack overlay, work loop; drift confessed same day
- 2026-08-14: bulk checkpoint 052732ebf (8 modules) + playable seam `main.py game`
- 2026-08-19: game_saga, game_dm_llm, invariant_npcs (8 curated + 23 auto-witnesses)
- 2026-09-14: browser MUD surfaces (d575bc168); optics steal (99826e153)
- Gaps: stones 4-5 undone; ledger only tabletop pieces; browser MUD untracked in git; dist lagged 567 lines (now worse — see W13)

## W2 — Verkle chain
- 8,247 leaves / 5.77MB JSONL; ~30,663 knot files; tip 507B
- Structure: ts, filename-as-address, leaf_hash, session_id, index, parent_verkle_root, verkle_root, amended, evidence_lost
- 2026-08-25 crisis: 1,044 dangling rows → 1,031 flagged evidence_lost (POWER_RESTORE_20260825.md, verkle_repair_state.json); single-writer lock in verkle_knot.py:37
- engram.py v0 (09-13): template + delta + payload_hash verify-on-read
- Honest: not real KZG verkle (upgrade path); no consensus/signing (single-writer lock); amendments in place; "DECLARED, not done" fanout
- Meaning for games: event-sourced authoritative world state; kifu array specced in F11_gomoku_rules_lens.md

## W3 — MUD genre lineage (web)
- MUD1 1978 Essex (Trubshaw/Bartle) → AberMUD 1988 → LPMud 1989 (world-as-live-code, LPC) → DikuMUD 1990 (classes/levels/aggro/resets/corpse runs → Merc/ROM/Circle → EQ → WoW; Koster: inheritance "completely undeniable") → TinyMUD/MOO (player construction, persistence) → Meridian 59/UO (1996/97, economy/housing/PvP) → EQ 1999 (raids) → WoW 2004 (friction removed, scaled)
- Bartle taxonomy 1996: Achievers/Explorers/Socializers/Killers; solo dev should pick Explorers + Socializers first
- Old-MUD multiplayer: telnet sockets, tick heartbeat, object DBs, wizard ladder, governance
- Top 5 steals ranked: websocket-telnet, tick, object DB, wizard ladder, Diku loop LAST

## W4 — Mechanics steals (web)
- Hades: boon draft w/ god synergy + Duo boons; Heat = voluntary difficulty-as-currency; endowed progress + loss aversion. Impl: {id,god,tags[],apply(stats)}
- Gunfire Reborn: Occult Scrolls stack with everything; elemental reaction table (corrode amps, shock disables, fire spreads). Impl: statusEffects map + pair-check tick loop
- StS: intent telegraphs (certainty loop — dying feels like YOUR error) + Ascension 0-20. Impl: intent field per enemy tick, drawn
- Vampire Survivors: auto-attack cadence, level choice per minute, weapon evolution. Impl: timer-driven fire + evolution lookup
- DF/RimWorld: emergence via event log + name generators ("the grey mushrooms remember your habit of hugging the left wall")
- Souls: one currency = XP + budget + death-stake. Impl: death drops souls where you fell
- UO/EVE: full-loot risk. Impl: tradable vault keys dropped at death
- Ranked fun-per-line: intent telegraphs, status table, boon tags/synergy, soul merge, event log + persistent horde memory

## W5 — Multi-user architecture (web + local)
- Classics: single-process select() loop, PULSE_TICK heartbeat, in-memory object DBs, player files, wizard ladder
- This week (2-8 players): ~200-line Python websocket relay on :8766 — server-authoritative G dict, 100ms snapshots, client interpolates; lan_proxy forwards unchanged; save via existing /api/v1/game (CircleMUD player files)
- Medium: Cloudflare Durable Object per room ("room:dungeon:1") — WebSocket hibernation = empty rooms cost nothing, state survives eviction; alarms = PULSE_TICK
- Honest MMO: shards/zones/instances — build NONE first; the DO room IS an instance
- Order: relay (2-3 evenings) → player files + reconnect (1-2) → DO room server (3-5)

## W6 — Subsystem organ map
- percolator = talent tree (109 invariants; top reinforced 184k×; no respec — GAP)
- rib_bus = broadcast creed (23 doctrine ribs, 50 channels; one-way — GAP)
- lanes = guilds (11 lanes; trails 478-926; builder lane bleeding OSError 22 — GAP)
- press = reputation/daily board (9 candidates; no persistent standing — GAP)
- warnings = debuff log (count corrected to 7,498 by B6; no severity/expiry — GAP)
- inbox = mail (420 files — healthy)
- trajectory = combat log (4,895 rows; no aggro/replay — GAP)
- events = XP log (414k+ lines; XP NEVER SPENDS — GAP)
- briefs = quest texts (3,662; no lifecycle — GAP)
- maze.jsonl = abandoned dungeon instance (67 lines, stale)
- flow ledger = tick history (newest entry a FAILED enqueue)
- biographer = character journal (no abandoned-quest resumption)
- scrum = raid scheduler (manual cadence)
- VERDICT: complete nervous system; no game layer (respawn, leveling, quest state, economy, raids) — "a server with excellent telemetry and no endgame"
- Five biggest gaps: no resurrection mechanic; XP never spends; no quest lifecycle; no economy; no raid coordination

## W7 — WoW organ gap (web)
- Organs: 13 classes/talents; quests/zones/levels; 5-man dungeons + raids (40 vanilla → Flex 10-30 → Mythic 20); loot/iLvL; professions; AH; guilds; reputation; PvP; collections; seasons
- Minimum viable versions for browser MUD: classes = 3 kits; quests = wave loop + memory; dungeons = done + 1 layout + boss room; raids = 5-10 gauntlet with roles; loot = rarity color + gate stat; AH = shared chest with price tags; guilds = persistent party channel; rep = faction number unlocking boons; PvP = duel; collections = torch familiars; seasons = weekly modifier + reset
- Cheap truth: MUD is 80% of WoW's loop (numbers and rules carry in text/canvas)
- Expensive truth: 3D world capital; persistence bills; the content treadmill
- DEFINITION: solo-dev WoW = the smallest shared world that still deserves "world" — persists (changes while logged off), shared (others' traces findable), horizon (gated somewhere you haven't earned)
- MUD is one weekly cycle + one persistent ledger from crossing the line

## W8 — Current build edge audit (the big one)
- DEPLOY DISCREPANCY: site/dist/games/mud.html = stale 920-line build; canonical = dashboard/static/games/mud.html 1,487 lines; build.py:86 copies dashboard/static/mud.html (top-level stale twin 31,348B Sep 12). Deployed site ships none of Part I.
- Vision: VERIFIED (R=270, 48 sweeps, corner ±0.0005 rad); EDGE: only ranger AI uses canSee — walkers/k8/boss chase through walls; occlusion cosmetic
- Quadtree: VERIFIED; EDGE: built from pre-move positions; own mass biases push (stale by one frame)
- SUPERHOT: VERIFIED; EDGE: spitter mine roll is per-FRAME (full rate inside frozen time) and mines tick on slowed dt
- Cascade: VERIFIED; totals k3 = (8+a)(16+2a) = 128 @ng0, 1,568 @ng20, no enemies-array cap; bonfire rest respawns the whole chain
- Ascension: VERIFIED; EDGE: G.ng uncapped past 20 (ng term keeps creeping); one-way ratchet, death locks scaled difficulty
- Lore: VERIFIED; EDGE: loreSave writes localStorage on every far kill; no reset affordance
- Classes: VERIFIED; EDGE: draw never reads e.stealth — rogues render fully; stealth is flavor unless occluded
- Boons: 12 VERIFIED; BUGS: filter `!b.max` always true (infinite stacking — torch vision multiplier esp.); Digit1/2 picks fall through to weapon swap same frame
- Puzzle: VERIFIED safe spawns; farSpot fallback can co-locate key/chest (theoretical)
- Totals: 10 enemy types, 3 projectile sources (spitter, ranger ×3, boss ×8), melee-only player, ~40 beep() sites, persistence = 2 localStorage keys only
- Top edges: Digit fall-through; dead boon filter; mines vs SUPERHOT; stale deploy; unbounded ascension × quadratic cascade

## W9 — Salon (7 shapes, blind divergence)
- S1: restated ask; MUD systems Supported w/ line numbers; "WoW-like" target UNPROVEN in sources; subsystems' role in game loop Unproven
- S2 ATTACK: zero network primitives; 2 localStorage keys = "single-player diorama wearing a MUD's coat"; the ask is the confessed drift "wearing a promotion"; 10,000 words wrong deliverable — "build the second client before writing the first sentence"
- S3 SOCRATIC: 8 unasked questions (who are Adam/Melissa/Marque really; where is one logged moment of human fun; first non-operator player named+dated; article vs shipped thing; first collision; whose money; sovereignty under observation; smallest shippable = one shared room, two browsers, one torch)
- S4 COHORT: FORBIDDEN → single-writer assumption enumeration survives; PAID-RENT → 10k collapses to 3k, gap table pays; EXTENSION → first cohort of the MUD is the fleet itself; DISANALOGY → honest ancestor is 1978 MUD + a ledger, not Azeroth
- S5 SEAT-0: drift confession CONFIRMED; article = drift "wearing a promotion"; mirrors permitted if named; what earns 10k = load-bearing divergence tied to witnessed failures; commission: "a gap analysis of the gap analysis"
- S6 FOLD: 9 charter questions (concurrency, authoritative vision/BH, verkle two-writers, rib_bus streams, percolator consent, persona-recall shared authorship, solved-literature edges, minimal proof, feasibility signals); closing paragraph the article must earn
- S7 CARD: mission, 5 domains, evidence standard (VERIFIED/PLAUSIBLE/UNVERIFIED + anchors), 3 disqualifiers (unanchored, paraphrase, scope drift), one-stone culture

## W10-W13 — Sweep witnesses (lanes A-E)
- W10 (A1/A9/A10): all MUD systems verified w/ line numbers; BUG: boon filter `!b.max` dead → infinite stacking; BUG: nextLoop never calls puzzleReset — NG+ vault permanently open, key/chest/plates never respawn
- W11 (A2-A5): sibling games — swarm closest to real game (persistence, full loop, needs mp3 check); maze_arena deepest system/lab; arrakis done-but-thin; operator_field divergence-receipt pattern steal-worthy. Ramp: work() does NOT complete orchestrator items (overclaim); roguelite = depth counter; render optics real (8/8 tests) but browser MUD is a parallel universe (0 network calls, no shared math). Campaign engine: dispatch mapped; campaign model mag_game_campaign.v1; two-session capable but non-atomic write_text + latest_any fallback = lost updates under concurrency; minimal seam = atomic saves + campaign_id echo
- W12 (A6/A7): play.html works for coders, PARTIAL for non-coders (no .catch on loadModules, dev-speak errors, unescaped quote in exit chips); catalog works (embedded JSON); cascade math coherent but ng20 wall = 1,568 k3 ≈ 156k enemy HP vs 100-HP player; speed cap 220 > player 200 kills kiting by ng6-20; 3 Melissa-facing improvements (friendly server-down state, plain instructions, ng10+ softening)
- W13 (B1-B8): B1 CONFIRMED (mud untracked; engine exists; no backend link); B2 CONFIRMED (8,247 leaves; 1,031 evidence_lost documented; lock at verkle_knot.py:37); B3 CONFIRMED (DikuMUD 1990 Copenhagen, classes/aggro/resets); B4 CONFIRMED (Hades Pact); B5 CONFIRMED (ThreadingHTTPServer, /api/v1/game route, lan_proxy no-auth LAN, wrangler assets-only); B6 PARTIAL (invariants 109 with top 184,455; lanes 11 + builder Err 22 in trail; seen.json 7,498 not 477 — DISPUTED→corrected; events 414,459; steps 4,895; briefs 3,662 exact); B7 CONFIRMED (raid sizes); B8 CONFIRMED (boon filter bug; Digit1/2 fall-through; stale dist 920 vs 1,487 lines)
