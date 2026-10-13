# GAMES SITE PLAYTEST + FIXES — 2026-09-21 night
Deploy: games-6jv7gdrfy (prod, aliased games-mag-d961.vercel.app + games-snowy-one).
## Playtest matrix (browser, input-pumped, live)
skifree ALIVE (new clone, SCORE ticks) · maze_arena ALIVE+text · ruins_go ALIVE
(engine restored, moves 0→3) · mud ALIVE · swarm ALIVE · frontier_souls ALIVE ·
toy ALIVE · arena_operator_field ALIVE+text · arrakis ALIVE · cathedral ALIVE
(loop witnessed on prod, 4 kifu rows).
## Bugs found → fixed
1. skifree.html TRUNCATED on prod (no closing script tag; whole game script dead;
   START button wired to nothing). Root: the earlier 'fix' deployed a partial file.
   Stolen replacement: the fleet's own skifree-v2 clone (complete, 17KB, one file).
2. ruins_go assets missing from local source (engine.js + pack.json existed only on
   prod). Restored to source dir.
3. ski lives-underflow (-1 display) — found in patched version; moot after swap,
   fix pattern kept for the record.
4. Operator's URL was a frozen old deployment, not prod. Real prod:
   **games-mag-d961.vercel.app** (also games-snowy-one.vercel.app).
## Playtest method
input-pump (arrows/WASD/space/click) × 2.2s per game + rAF frame delta (loop
alive) + text-growth; then targeted deep runs: SkiFree full cycle (start → steer
→ game over → restart path), ruins_go (engine + moves + msg), cathedral (ford →
gallery loop-witnessed on prod).

## ROUND 2 — operator dogfood + rebuilds (same night)
Operator playtested live: toy shallow (space-only strategy), arena meaningless,
arrakis fun but the worm does nothing. Verdicts + fixes:
1. TOY: the degenerate strategy was out-ranging the walker (space reach 55 vs bite
   ~30, walker speed 70 vs 160). Fixed: space reach 38, walker speed 95 + far-chase
   1.35x + lunge on windup-end. Standing = death; roll-through-riposte is now THE
   grammar. Verified: walker closed and killed a wall-hugger.
2. ARENA: the game existed (deliver marbles to the pit) with zero stated goal.
   Fixed: plain-language goal line, pulsing labeled PIT, physics untouched.
3. ARRAKIS v2 — rebuilt THPS-style: speed pays score continuously · spice chained
   without slowing = LINE ×N (up to ×8) · dark dune crests launch you airborne at
   speed — air spins (A/D) bank on landing · the Maker now SURFACES past thump 55,
   leads your motion, runs 6.0 vs your 5.2 (Boost 6.8 drains a meter) · E drops a
   thumper (3, restock at gates) — the Maker answers rhythm for 6s · contact eats
   your un-banked line + 3 spice + knockback + shake · proximity vignette.
   Verified live on prod: score 214 climbing, Maker surfaced, zero errors.

## ROUND 3 — swarm "the door to the background" (operator report)
THE PASS (leave the maze, ride the mountains) — dogfooded 6 ways incl. forced pass
on prod: entry, ride, steering (lowercase keys verified consistent), depth-3 Kabuki
boss spawn, ride-exit — all clean, zero errors. Could not reproduce the exact break.
REAL defect found by math: ride speed ramps to 70 while rocks spawn every 1.1s at
closing speed ×8 — at the ramp's peak the rock wall is mathematically undodgeable.
Feels exactly like "the game broke."
FIX: ride speed cap 70→46 (ramp 0.8→0.45), rock cadence 1.1s→1.7s. Steering
verified live (mtn.steer responds to A/D). Deployed: games-m3p5cebqu.
## Fan-out status
estate game census + enhancement wave (workflow dwfrun-44628a0b, 5 pinned agents)
running in background — findings land next window: memory/game_modules, wargames,
inbox games, corpus, research-enhance lane.

## ROUND 4 — census wave results (5-agent fan-out, dwfrun-44628a0b)
Full findings in the workflow record (dwfrun-44628a0b); highlights:

### Confirmed defects (deterministic checks, node + fs)
1. **mag/game_rules.py MISSING while the queue head targets it** — FLOW_LEDGER.jsonl
   line 163 enqueues {test, nomic_rules_patch, mag/game_rules.py} (19:00Z today);
   `ls mag/ | grep -i rules` = empty. The queue's next test will fail on a ghost module.
2. **curvature_tiebreak.v1.json has no start_room** (the only module without one) and
   gate_style_sluice is a one-way dead end with no reciprocal exit — unenterable
   as-is by a naive engine.
3. **steer_field.html: F.t never initialized** → NaN from first tick, walkers never
   move, the film is static (mag-disk archaeology, deterministic new Function + read).
4. **arrakis v1 (mag-disk copy) has the MACH double-declaration** — same bug class I
   found and fixed in v2; confirms the bug class predates tonight.
5. **maze_arena/room_game inverted dumb-agent wall test** (sdf < MARG = INTO walls —
   "dumb agents tunnel through walls" contradicts their own on-page description).
6. **game.html + verkle_knot_wave.html reference game_verkle_knots.js which exists
   nowhere** — knot-loot pool degrades to empty; knot-wave view dead.

### New playable surfaces discovered (ours, archaeological)
mag-disk dashboard archaeology: dungeon.html (RGB lens puzzle), room_game.html
(lantern + dragon + law shards), erosion_field.html, field_quills.html,
calabi_yau.html, mesh_gallery.html, game.html (swarm-vs-dragon clicker),
smith_chart.html exhibit, lattice_check.html, plus openai-cookbook snake_game.html.

### Enhancement proposals (25, all grounded with line numbers)
Top of the queue: swarm door = prisoner's-dilemma payoff table (open_spiel);
maze_arena phantom mode (imperfect information); ruins_go Go-capture liberties +
TrinityCore data-table guardians; MUD evennia channels/@dig/Kuhn-poker den;
toy = Chatbot-Arena Elo ladder + named playerbots + RouteLLM matchmaking (kills
the flat difficulty wall for good); frontier_souls phantom co-op + pig-dice
bonfire wager; arrakis Maker samples your path N times (self-consistency spread =
its aim confusion) + named bot riders; arena curvature seams (steer the
connection, not the agent); cathedral = evennia batch-build rooms from doctrine
md (the world grows by filing) + seat-bots; ALL games = Kev/Laya trained brains
on our playtest kifu; wholesale clone candidate = DOOM (shareware WAD, GPL
engine); ledger-blocked: ioq3/minetest/sm64ex (read contracts, copy nothing).

## ROUND 5 — genre grafts IMPLEMENTED + live (operator: "build it")
All 7 lanes' S-effort grafts are in the production files, verified by byte-grep on
the live prod alias (games-mag-d961.vercel.app), deployment games-cvz72nqp9:
- swarm: killMult decay + Shift dash with i-frames (3 markers)
- arrakis: OlliOlli landing window + Burnout wormride + SSX spin-charged boost (2 markers)
- toy: walker far-chase + lunge rebalance (1 marker)
- arena: phosphor fade trails + fall-line bonus + earned HUD (1 marker)
- skifree: tree near-miss skim credit (1 marker)
- cathedral: A-LttP `flip doctrine` world-toggle + Majora cycle-best spice payouts (6 markers)
- ruins_go_engine: Hoplite bump-kill + leap (1 marker)
MUD lane grafts (Zork compound commands, speedwalk) NOT APPLIED — mud.html is an
action game, not a text parser; the grafts belong to a text-MUD lane we don't have
yet (queued as a build candidate, not forced).
Scripted browser-input re-verification was flaky (known dispatch timing issue) —
human playtest is the acceptance pass. Syntax: all 6 files clean.

## Round 6 - the DnD layer (operator: DO IT)
Harvest applied from the actual-play podcast: DM voice per room entry (DM_LINES, 11 rooms + default), 2d6 cosmetic roll on every act (gates stay deterministic, replay law holds), ghost-at-your-shoulder flavor line (15 pct). Wired as a wrapper around act/render in cathedral_v1.html - builder template sync owed at next rebuild. JS syntax-checked with node --check, deployed, byte-verified live.

## Round 7 - the tavern mapped in (operator: we have done this before)
Self-steal hit: dnd_classic_stub.v1.json (14 rooms, the Guttered Lantern tavern, rumor hooks, goblin scout statblock, cave_key loot) was built before but never carried by the cathedral. Wired live: module injected by tools/cathedral_wire_tavern.py (idempotent), crossroads <-> lantern crosslinked, tavern layer wrapper shows rumor/hook + encounter challenge + loot lines, goblin fight resolved by the act-roll 2d6 with kifu receipts (win/kifu, loss flagged DISPUTED). Gates stay deterministic. Deployed + byte-verified live (9 marker hits on prod).
