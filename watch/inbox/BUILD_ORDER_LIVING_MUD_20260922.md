# BUILD ORDER — THE LIVING MUD (beacon GWAP → AI MUD) · 2026-09-22

**Operator steering:** "our wow clone is basically the mud game... time for a
literal mud like our dnd playtests — solving puzzles using the mechanics we've
already built in our games but borrowing. Right now everything is html5 but we
have literal ai tools — image generation, 3D models — and a plan to make a wow
clone like the skyrim mod that puts ai in npcs. The idea is we are ractoring
and kabuki-ing the whole GWAP."

**The self-steal (everything already exists):**
- mud.html (124KB arcade MUD, Evennia steals: typed characters, lookable
  things, turn-based party order) — the engine lineage.
- The cathedral GWAP (6 walkable rooms, HUD, walker, minimap) — the world.
- dnd_classic_stub + tavern (14 rooms, rumors, encounters, loot) — content.
- Kabuki tavern + ractor chairs (DM_LINES per room) — the cast.
- P2P_DND_ARCHITECTURE + grokbot party-turn — the playtest pattern.
- The MiMo headless free server (:4096) — live AI dialogue for NPCs
  (the Mantella move, self-built: Skyrim's AI-NPC mod, but on OUR free lane).
- imagegen (image assets) + the deep cuts (spectral maze vision-gating,
  wipeout music-coupling) — borrowed mechanics.

## V1 — two tiers, both honest

- **LOCAL tier (the real Primer):** served from the estate, NPCs talk LIVE
  through the free headless lane — unmonitored, unlogged-permission, the
  everyman copy. Walk a room, talk to an NPC, the model answers in-character
  from the room's lore card.
- **PUBLIC tier (the beacon):** same world; NPCs speak curated lines + the
  image assets; the live-AI tier is documented as the local mode. No half-
  broken AI on the public surface — incomplete beats fake-complete.

## V1 scope (next build window)

1. Graft the MUD pane into the beacon: text-input world on the room graph
   (rooms = the 6 beacon rooms + the tavern + the dnd keep).
2. NPC layer: each NPC = a lore card (name, room, voice, secrets) + curated
   lines; LOCAL tier adds live dialogue via :4096.
3. imagegen pass: room plates + 3 NPC portraits, house palette.
4. One puzzle chain using an EXISTING mechanic (water gates or lens count) —
   borrow, don't invent.
5. Kabuki: ractor chairs cameo as NPCs (Voltaire the blade already has a seat
   in the engram room).

## The ractor gate (before V1 ships)

- **Lessig:** the public tier must be fully playable with JS on and JS off.
- **Elder:** the local tier never transmits visitor text anywhere but the
  local lane; the world's lore cards cite their knot/record sources.
- **Ponytail:** the nameplate — "the everyman Primer: a world that teaches
  back." One line on the door, that's the whole marketing.

## Standing burn (24/7, chained)

- r3 (now): untamed-knots pilot, maniclang re-seed, kev-diet pilot, cluster
  dives, watch-backlog triage — 6 lanes.
- r4: polish-verify — 9 lanes re-auditing the game polish drafts (apply /
  adjust / reject verdicts) so grafting is evidence-gated.
- r5: memory comb — biography, ghost, training, oral_history sample,
  rib_bus, agent evolution — what the revamped memory must represent.
- Fold + smith-chart on every landing; findings feed the MUD lore cards and
  the lattice.

---

## SELF-STEAL ADDENDUM (same night, pre-build inventory) — THE ARCHITECTURE ALREADY EXISTS

The estate already holds the exact engine: **mag/game_campaign.py (4,765
lines)** — "Campaign engine — state/legal actions first; LLM narrates after.
Law: engine owns truth." Character files, save checks, CK-lite trait tables,
mag_game_campaign.v1 schema. Plus:

- **mud.html (124KB)** — 34 rooms, localStorage saves, the client lineage.
- **persistent_world.html** — "THE PERSISTENT WORLD — glyph edition v0 · an
  interface to the hive."
- **fable_room.html** — "THE FABLE ROOM — room #0 · the union of story and
  record."
- **night/game_lattice.html** — "The Game Mechanics Lattice — 7 engines x 47
  rooms" (the design doctrine doc).
- **oracle_dice.js + dd_*.json** — data-driven content formats.

## THE ARCHITECTURE THIS DICTATES (revised V1)

**The engine owns truth; the LLM only narrates.** The deterministic campaign
engine resolves every action's legality; the model NEVER invents state — it
describes outcomes. This is the anti-Mantella: the Skyrim AI-NPC mod lets the
LLM improvise (hallucinated quests, broken continuity); ours resolves first
and narrates second. No hallucinated game state is possible by construction.
That is the estate's unique contribution to the AI-NPC genre — and the
riddler shape: the record is the truth; the narration is the view.

## REVISED V1 SCOPE (next build window, fresh focus)

1. JS port of the minimal campaign loop (rooms + legal actions + save) —
   engine-owns-truth in the browser, state in localStorage.
2. Narration: curated templates on the public tier; live via the :4096 lane
   on the local tier — narration only, never state.
3. Content: dnd_classic_stub + tavern + the beacon rooms as the opening
   world; one borrowed-mechanic puzzle chain (water gate or lens count).
4. imagegen pass for room plates + NPC portraits, house palette.
5. Persistent world: session closes knot into the record — the world
   remembers (the actual Primer property).

The burn waves (r3-r5) keep grinding regardless; the memory-comb and
untamed-knots findings become the MUD's lore cards directly.
