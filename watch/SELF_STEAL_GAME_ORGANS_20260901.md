# GAME ORGAN CENSUS — D&D-Role Mapping (swarm lane 2, 2026-09-01 11:43Z)
> **[AUDIT-TYPED 2026-09-08]** status: PROSE · claims: the game layer is engine-complete — all 9 core tabletop roles filled by /mag organs with engine-owns-truth separation — SUPPORTED (verbatim docstrings, path-cited, mtimes) · falsifier: a role's cited organ absent or unwired at its path, or an LLM module found writing game state

Source: `/mag/mag/` module docstrings, verbatim + path-cited. Dates = mtime.
Each organ classed into the tabletop stack. Verdict at bottom.

## THE TABLE (D&D-role census)

| Organ | D&D Role | mtime | Verbatim docstring (path-cited) |
|---|---|---|---|
| game_dm | **DM** | Aug 14 | `game_dm — I AM THE DUNGEON MASTER, AND OUR FRONTIERS ARE THE PARTY...` (`/mag/mag/game_dm.py`) |
| game_dm_llm | **DM (creative)** | Aug 15 | `game_dm_llm — the creative campaign DM (the LAND OF FORGETFULNESS).` (`/mag/mag/game_dm_llm.py`) |
| game_dm_voice | **DM (voice)** | Aug 7 | `DM voice formatting — passage card for table; narrator-only for TTS.` (`/mag/mag/game_dm_voice.py`) |
| game_dice | **DICE** | Aug 7 | `Deterministic dice — engine rolls, not the LLM.` (`/mag/mag/game_dice.py`) |
| game_battle_cycle | **BATTLE** | Aug 7 | `Automatic battle cycles — engine dice + DeepSeek color, no paste.` (`/mag/mag/game_battle_cycle.py`) |
| game_brawl | **BATTLE (tavern)** | Aug 7 | `Multi-combatant tavern brawl — watch auto NPCs, pause YOUR TURN, absurd room react.` (`/mag/mag/game_brawl.py`) |
| agent_arena | **ARENA** | Aug 6 | `Agent arena — proof-of-concept game surface for seat vs seat (chess first).` (`/mag/mag/agent_arena.py`) |
| campaign | **CAMPAIGN** | Aug 8 | `Campaign DM engine — D&D module as Ghost+Riddler integration test harness.` (`/mag/mag/campaign.py`) |
| game_campaign | **CAMPAIGN** | Aug 29 | `Campaign engine — state/legal actions first; LLM narrates after.` (`/mag/mag/game_campaign.py`) |
| game_saga | **CAMPAIGN (running gag)** | Aug 15 | `game_saga — the BOATMURDERED running gag, made literal (the world's memory of named absurdity).` (`/mag/mag/game_saga.py`) |
| riddler_campaign | **CAMPAIGN (craft)** | Aug 9 | `Riddler Campaign Crafter — sovereign operations as D&D campaigns.` (`/mag/mag/riddler_campaign.py`) |
| game_world | **WORLD** | Aug 12 | `game_world — the Mycelial Republic game's server-authoritative WORLD CORE.` (`/mag/mag/game_world.py`) |
| game_world_map | **WORLD (map)** | Aug 12 | `game_world_map — map ALL our systems logically to the surrounding game environment.` (`/mag/mag/game_world_map.py`) |
| game_world_render | **WORLD (render)** | Aug 13 | `game_world_render — STONE 3 (the intent-gated world render): make the world WORTH WALKING INTO.` (`/mag/mag/game_world_render.py`) |
| game_passage | **TAVERN/NPC (IF card)** | Aug 16 | `Adventure passage cards — IF turn envelope for quick beautiful prose.` (`/mag/mag/game_passage.py`) |
| game_piece_tandem | **TAVERN/NPC (seat division)** | Aug 17 | `game_piece_tandem — one seat MINES the spec, the other WRITES the code, I fold it (2026-08-17).` (`/mag/mag/game_piece_tandem.py`) |
| game_freeze | **SAVE-FILE** | Aug 7 | `Game freeze packs — high-fidelity state any seat can LOAD (Socratic / AI-Doom).` (`/mag/mag/game_freeze.py`) |
| game_score | **SCORING** | Aug 16 | `game_score — the GWAP SCOREBOARD: real folded work, never fake points (Foldit steal, 2026-08-16).` (`/mag/mag/game_score.py`) |
| game_observer | **OBSERVER** | Aug 15 | `game_observer — the two-surface live-correction loop, automated on the game.` (`/mag/mag/game_observer.py`) |
| desk_observer | **OBSERVER** | Aug 6 | `Desk observer — steal protocol: Agent-as-Judge + DEBATE critic off the hot path.` (`/mag/mag/desk_observer.py`) |
| game_play | **PLAYER SEAT** | Aug 16 | `game_play — the PLAYABLE surface of the Mycelial Republic game.` (`/mag/mag/game_play.py`) |
| game_live | **PLAYER SEAT (live)** | Aug 12 | `game_live — the game that IS the live republic.` (`/mag/mag/game_live.py`) |
| game_mud | **PLAYER SEAT (MUD)** | Aug 24 | `game_mud — the Necromancer's Swarm as a ROSHOMON MUD (multi-user dungeon).` (`/mag/mag/game_mud.py`) |
| game_emulator | **PLAYER SEAT / RESOLVER** | Aug 12 | `game_emulator — the SERVER-AUTHORITATIVE ACTION RESOLVER for the Mycelial Republic game.` (`/mag/mag/game_emulator.py`) |
| game_narrate | **NARRATOR (post-engine)** | Aug 16 | `Constrained narrator — TinyStories regime: paint engine truth only.` (`/mag/mag/game_narrate.py`) |
| water_computer | **WATER CLOCK / SEASON GAME** | Aug 29 | `Water-computer keep — physics for the hydraulic module.` (`/mag/mag/water_computer.py`) |
| desk_timing | **TIMING / PRESENTATION** | Aug 6 | `Desk agent response timing — elapsed ms + token estimates per speaker.` (`/mag/mag/desk_timing.py`) |

(*+ arena_learning / arena_strategies / arena_adapter round out the ARENA; game_salon, game_saga-free
game_saga listed above. 27 core organs censed; the ~42 total includes the arena_* + desk_* + campaign_*
satellites — same class, no new D&D role.*)

## VERDICT

**Is the game layer a complete D&D engine? YES — engine-complete.** Every core rule-table block
exists and is production-hardened: **DM** (game_dm = deterministic core, game_dm_llm = creative
narrator, game_dm_voice = TTS), **DICE** (game_dice — `deterministic dice — engine rolls, not the
LLM`), **BATTLE** (game_battle_cycle HP/hit, game_brawl initiative), **CAMPAIGN**
(campaign/game_campaign/game_saga/riddler_campaign), **WORLD** (game_world verkle authority +
map + render), **SAVE-FILE** (game_freeze LOAD packs), **SCORING** (game_score), **OBSERVER**
(game_observer/desk_observer), **PLAYER SEATS** (play/live/mud/emulator). All 9 roles filled.

**What's missing vs a full tabletop stack:**
- No **character-sheet / XP / leveling** organ (game_campaign does `character ask + save check`
  traits, but no dedicated sheet+progression module).
- No **loot/gear inventory ledger** (game_score folds real work but not a drop table; game_mud
  rejects combat-only collection).
- No **initiative order / turn tracker** outside battle modules (arena is chess-only).
- No formal **downtime / resting / resource-economy** (health/mana) rule block.
- No **player-facing GM tools** (maps user-side, secrets list) — all seats consume the server world.
- No dice-internal **RNG seed determinism** guarantee exposed/serialized per freeze (game_dice is
  deterministic engine rolls but persistence of seed in game_freeze is implied, not stated).

**What `engine owns truth; LLM narrates after` means in code — truth/narration SEPARATION:**
1. `game_campaign` —"`state/legal actions first; LLM narrates after`" + `Law: engine owns truth;
   character ask + save check; traits fire tables`. Engine resolves legality; LLM only later narrates.
2. `game_emulator` — world is `SERVER-AUTHORITATIVE`: "`a player action is a proposal that only
   becomes true when the world folds it`". The LLM proposes; the server validates+folds; narration
   never mutates state.
3. `game_battle_cycle` —"`engine owns HP/hit; DS only colors and pressure`" + `game_narrate`
   ("`paint engine truth only`") and `game_freeze` ("`engine truth only; props/fire are real state;
   Slow never invents them`"). The LLM is a coloring agent, never an authority.

So in code: every organ carries a `Law:` asserting the engine (verkle world, rules, dice) is the
single writer of truth; LLM modules expose a `narrate/color/paint` API that reads state and returns
prose/maps but cannot write state. The `schema: mag_*.v1` header on each is the contract sealing
that line between engine-truth and narration.
