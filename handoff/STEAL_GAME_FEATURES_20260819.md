# STEAL GAME FEATURES — research + self-steal synthesis (2026-08-19)

Goal: steal the BEST features from the surfaced games, mapped onto what we ALREADY own
(self-steal audited mag/game_*), so we never rebuild what we have. Every target below is a real,
verified feature from a real game.

## The games researched (grounded)
- **Dwarf Fortress** — procedural world + history, Legends mode (browsable world history/figures),
  "Losing is fun" permadeath ethos, community saga (Boatmurdered — a fortress passed player-to-
  player, each writing a chapter).
- **RimWorld** — "story generator" with a **storyteller** algorithm that picks events based on
  player situation to craft tension; storyteller personalities (Cassandra tension-curve, Randy
  chaos). Inspired by Dwarf Fortress.
- **Façade** (Mateas & Stern) — **drama manager** that organizes events toward tension/resolution,
  over **believable agents** (natural-language characters with emotional state).
- **Left 4 Dead** — **AI Director** reacts to each player's situation/skill to place pressure
  (dynamic difficulty + procedural narrative); a separate **Music Director** personalizes tone per
  player; four-survivor co-op.
- **Middle-earth: Shadow of Mordor** — **Nemesis System**: persistent named enemies who REMEMBER
  interactions (survive -> promoted; killed you -> stronger; burned -> revenge), creating personal
  stories; inspired by pen-and-paper RPGs + sports games ("the narrative continues even when you
  lose"). Warner patented it (only Warframe's Adversary System is similar) — our build is our own,
  legally distinct.
- **Blackboard architecture** — standard game-AI tool for coordinating specialists via a shared
  workspace (the substrate).

## SELF-STEAL: what we ALREADY own (don't rebuild)
1. **Content-addressed verkle world state** (`game_world`) — immutable, replayable, server-
   authoritative. THE backbone.
2. **State-first, LLM-last engine** (`game_campaign`) — engine owns truth (dice/HP/legality/
   drama); LLM narrates after.
3. **Pals-as-XCOM-squad** — party members with stations, panic, trait-modulated DCs.
4. **Absurdity-as-legal-move** (`game_brawl`) — farce is a sanctioned mechanic.
5. **Constrained narrator w/ invent-ban** (`game_narrate`) — paints engine truth only.
6. **Two-surface live-correction loop** (`game_observer`) — one surface watches + steers the next.
7. **Two-seat mine→write→fold tandem** (`game_piece_tandem`) — structured-output codegen.
8. **Signal/meta/OOC detection in combat** (`game_battle_cycle`).
9. **GWAP honest scoreboard** (`game_score`) — score = real folded work, can't be gamed.
10. **Game-as-work ramp** (`game_ramp`) + async test→fix loop (`game_flow`).
Plus: **hero_journey** (overnight epic composer), **adventure_one_shot** (the product), **game_dm**
(DM + frontier party), **game_dm_voice** (narrator palette = a mood/music director already).

## THE STEAL MAP (game feature -> what we have -> what to steal/build)
### HIGH VALUE
- **Nemesis System (Shadow of Mordor)** — WE HAVE: verkle world (perfect persistent memory),
  game_campaign encounters. STEAL: **persistent named enemies who remember**. Enemy survives a
  fight -> promoted + remembers the player's move; killed you -> comes back stronger with a
  grudge; burned -> seeks revenge for disfigurement. Every nemesis is a verkle-committed
  character that persists and evolves across sessions. Builds the "your actions leave lasting
  enemies" layer on top of our already-persistent world. HIGH priority.
- **Legends mode (Dwarf Fortress)** — WE HAVE: verkle chain = full world history, hero_journey,
  biography, game_score. STEAL: a **browsable world history / figure ledger** — every committed
  knot is an entry; notable deeds of figures are viewable ("the fall of X, by Y's hand").
  We're closer than it looks; this is a browser/render over existing verkle history. HIGH.
- **Boatmurdered / community saga (Dwarf Fortress)** — THIS IS LITERALLY DISTRIBUTED COLLABORATIVE
  STORYTELLING. A shared persistent world passed mind-to-mind, each writing a chapter, saga
  accumulates. WE HAVE: the whole premise (shared substrate, adventure_one_shot persistence, DM
  party). STEAL: formalize a **pass-the-save / shared-campaign mode** — different minds (frontier +
  human + resident actor) take turns in the SAME persistent world and the saga accumulates as the
  durable story. Validation of the kabuki thesis + a concrete product. HIGH.

### MEDIUM VALUE
- **RimWorld storyteller personalities** — WE HAVE: game_campaign storyteller/threat_budget,
  game_dm_llm. STEAL: multiple **storyteller personalities** (tension-curve / chaos / calm) that
  pick events from the weighted tables based on LIVE state, not just a fixed budget.
- **Left 4 Dead Music Director** — WE HAVE: game_dm_voice brawl palette (calm->heating->absurd->
  aftermath) IS a mood director. STEAL: make it a first-class **mood/tone director** that reacts
  to player experience (health, tension, recent events) — not just scene-static.
- **Left 4 Dead AI Director (dynamic pressure)** — WE HAVE: storyteller threat_budget. STEAL:
  Director reacts to player SITUATION (adds/removes pressure based on skill/status) for dynamic
  difficulty. Ties into game_observer (the steer-before-next-turn loop).

### BACKLOG (from our own audit gaps — pair with game_piece_tandem STEAL_ITEMS)
- XP/levels/advancement (we flagged missing; DF/Nemesis both reward progression).
- Magic/spell resource system (wizard/cleric exist but no spell list/mana).
- Richer inventory/economy (buy/sell/equipment slots).
- Status effects (poison/burn/stun) beyond grapple.
- Death/permadeath -> meta-progression (Nemesis + DF "losing is fun" both reward the fall).

## Bottom line
Our deterministic infrastructure (verkle world authority, state-first engines, constrained
narration, honest scoring, observer loop) is the STRONGEST part and beats these games' engines on
rigor. The high-value steals are the NARRATIVE-MEMORY features these games proved players love:
**Nemesis persistent rivals** (memory shapes enemies), **Legends world-history browser** (your
deeds matter and are viewable), and **Boatmurdered shared-saga mode** (distributed collaborative
storytelling as a concrete feature). Those three slot directly onto the verkle substrate we
already hold — no new infrastructure, just the narrative layer. The games' AI director/storyteller
ideas are already half-built in game_campaign + game_observer + game_dm_voice.
