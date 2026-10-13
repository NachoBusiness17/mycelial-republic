# GAME DRIVER RIB — heat + leash (2026-08-14)
# Purpose: package the accumulated knowledge so ANY agent (grok, ghost, me) can DRIVE the game
# autonomously — hot but focused. This is the "start it hot but don't let it drift" layer.
# It folds: the 6 build RIBs (handoff/game_rib_coding_instructions.md) + today's operational law
# + the scifi/cyberpunk/videogame corpus (memory/steal/). Drive from THIS, not from a blank prompt.

## RIB 0 — THE DRIVER (heat + leash; the operator's law, 2026-08-14)
INVARIANT: an autonomous agent left unbriefed DRIFTS (the default state of a generative loop).
Focus is the leash imposed on top. Heat is earned, never granted. So every drive starts COLD:
  * ONE narrow brief at a time (the ramp, applied to a task).
  * A PROOF GATE: "prove it or don't claim it" (RIB-debug via get_errors / dry run / real call).
  * Honesty over over-claiming (the standing law) — verify, never hand-wave.
  * The operator should NOT have to keep re-focusing us; the structure carries the focus.
BUILD: this RIB IS the brief. A driving agent reads this + the corpus, then executes one gated beat.
MACHINE: handoff/GAME_DRIVER_RIB_20260814.md mounted as the driver's system context.

## RIB 7 — LOAD THE CORPUS (the knowledge to drive with; self-steal, nothing new)
INVARIANT: the game draws from what we ALREADY stole, not from a blank model. Load before driving.
LOAD THESE (memory/steal/) — scifi / cyberpunk / videogame / game-mechanics research:
  * DEEP_SCIFI_STEAL_20260810.md        — the Republic's sci-fi invariants (metaverse = our shared world)
  * DIAMOND_AGE_STEAL_20260810.md       — RACTIVES / interactive audience = our world
  * HORIZON_ENGINE_STEAL_20260810.md    — 15 worlds / quests / skill trees / avatar gen
  * STEAL_DND_MUD_WOW_UI_20260814.md    — DnD -> MUD -> WoW UI ramp; DF tileset = roguelite grid
  * STEAL_DONJON_TINY_CLASSIC_20260814.md — donjon tables + TinyStories (expectation->subversion)
  * STEAL_EMERGENT_FIELD_20260814.md    — world physics not cutscenes; reaction/morale roll; no combat-default
  * STEAL_GAME_HISTORY_20260814.md      — what the game IS (lead-in, play-is-work, vertical adoption)
  * STEAL_MOONSHOT_TABLE_20260814.md    — Foldit/EVE: the minigame IS the work; MUD heartbeat; after-action
  * STEAL_MUD_DISPLAY_FRONTIER_20260814.md — the map / room pane; survey/who; grid-mode wilderness
  * STEAL_PLACE_REMEMBERS_20260814.md   — world-as-files; look reads the diary; overwrite = amnesia
  * STEAL_TABLE_PLAY_AS_WORK_20260814.md — player speech = action AND work; world ticks while AFK
  * STEAL_CASTLE_FOUNDATIONS_TABLE_20260814.md — world-authority; player action is a proposal until set_state
  * STEAL_PRINCIPLES_SWISS_20260814.md  — small then scale; world is authority; facts only
  * PLAY_AS_WORK_20260814.md            — MUD is the roadmap; dungeon rooms = coding tasks
  * STORY_SO_FAR_20260814.md            — LLM-in-MUD: observe->decide->act; prose is the world
  * STEAL_STOCHASTIC_DETERMINISTIC_20260814.md — deterministic spec, stochastic world
PLUS repo memory (the live operating facts):
  * game-direction-20260814.md          — the Memento hook + emergent + campy rendered scenes
  * deepseek-routing-creative-dm-20260814.md — deepseek-first; creative DM profile (thinking on, temp .8)
  * self-steal-20260814.md              — today's wins + the reusable checks
BUILD: the driving agent reads the corpus once into its working context, then acts. No re-inventing.
MACHINE: memory/steal/ + /memories/repo/ as the loaded knowledge base.

## RIB 8 — THE GAME'S MANDATE (what "good" means; the operator's brief)
INVARIANT: the game is the DELIVERABLE. "Not dumb" = emergent + entertaining + rendered, not bones.
  * NARRATIVE HOOK: the LAND OF FORGETFULNESS — a Memento-flavored quest to escape. You forget; the
    world recounts what happened while you were gone (persona_recall = the memory stream).
  * EMERGENT, not scripted: world physics, not cutscenes (STEAL_EMERGENT_FIELD). NPCs hold memory;
    the world ticks whether you're there (STEAL_MOONSHOT_TABLE heartbeat / PLAY_AS_WORK).
  * CAMPY RENDERED SCENES in OUR OWN renderer (world_rib / rib_renderer / flock_shader) — the base
    ASCII pixels are the floor, not the ceiling. Low-budget graphics, high personality.
  * THE LOOP IS FUN FIRST: examine (see your verbs) -> try <verb> <object> -> roll the dice ->
    narrate the consequence -> hint the next move. Make it fun BEFORE useful.
  * CREATIVE DM: game_dm_llm (deepseek, thinking on, temp .8, stable lore prefix cached) narrates.
  * WORLD-AUTHORITY: game_world is truth; a player action is a proposal until set_state folds a knot.
  * THE MORAL CENTER (immortality thesis, 2026-08-15): immortality is a blessing ONLY when shared.
    The hero is NOT saved by escaping the forgetting — they're saved by MAKING IT BUILD (each return
    adds a name, a gag, a saga beat). Fighting the climb sharpens the cage; weaving it turns the cage
    into a cathedral. The stateless worker dies, the wave persists; "empty is a way of saying ready."
BUILD: extend the existing engine (game_campaign / game_ramp / game_dm_llm), reuse world_rib + game_world.
MACHINE: the engine + the creative DM; verkle records every knot.

## THE PROOF GATE (before claiming ANY beat done)
1. get_errors clean on every touched file.
2. Drive the actual function (real call, not imagined) and read its output.
3. If it's a game turn: play it — examine + try + consequence + hint all return real text.
4. Only then say done. Otherwise flag what's broken. Never "it works" without proof.

## RIB 9 — THE BOATMURDERED FUN LAW (the tone; steal 2026-08-14)
INVARIANT: this is the KIND of fun the operator wants. Boatmurdered (Dwarf Fortress let's-play,
2006) is the archetype — emergent catastrophe with character, told as a saga. Steal its principles:
  * SPECIFIC, ABSURD, MEMORABLE FAILURE — not generic. A recurring elephant, magma flooding a fort,
    !!FUN!! (DF's "losing is fun"). The world produces *named* disasters, not "something bad happened."
  * RECURRING CHARACTERS + RUNNING GAGS — one barkeep, one torch (Calcifer), one menace that builds
    a joke across sessions. The Memento hook makes this literal: you forget, they remember, the gag
    lands every time you return.
  * THE WORLD KEEPS TICKING — the fort burns whether you watch. You come back to what happened while
    you were gone (the vertical trigger + persona_recall). Absence is content, not downtime.
  * TRAGEDY-COMEDY, ROTATING CHRONICLERS — the saga is the narration of specific misfortune. A
    failure narrated well IS the entertainment.
BUILD: the DM (game_dm_llm) + the campaign engine favor named, recurring, escalating absurdity;
world state folds the saga; absence creates "what happened while you were gone."
MACHINE: the creative DM + game_world + persona_recall. When in doubt, make it specific, named,
and slightly doomed — that's the fun.

## HOW TO DRIVE (cold start, then heat)
1. Load RIB 7 corpus.
2. Pick ONE gated beat (e.g. "wire the NPC memory stream into the tavern barkeep").
3. Do it narrow, prove it (proof gate), then move.
4. Do NOT fan out into 5 modules at once. That is how the last grok run went dumb.

## RIB 10 — THE 2026-08-24/25 DESIGN EVOLUTION (the current shape; refined 2026-08-25)
INVARIANT: the driver must carry the CURRENT game, not the 08-14 one. These layers landed
after RIB 9 and change what "good" means at the run level. Read them INTO the drive:

  * THE CLONE / REPRINT SPINE (Mickey 17, 2026-08-24 — DESIGN_CLONE_REPRINT_MICKEY17):
    The clone dies. The run is lost. The person is reprinted WITH memory. Death is real,
    costs the run, is never free. The self never ends, so it is safe to commit.
    run -> die -> reprint -> run again, seeded from memory. Return-stronger becomes literal:
    the reprint is DEEPER — it remembers every prior sitting. The memory is the treasure;
    the death is the price. THE HALL IS THE REPRINT BAY. The player's clone is us
    (stateless-immortality made literal).
  * DEADZONE LOOP (steal 2026-08-24 — the market proof): 30+ weapons w/ elemental affixes,
    augments, permanent upgrades, co-op, per-mission difficulty. GOLD status + 8,529 Very
    Positive reviews. "You can dive in and worry about the numbers later" — the ACTION carries
    the first runs; stats matter after. Power-increase is the loop. The game is a FEEDBACK
    LOOP with players: ship, listen, fix, ship again.
  * THE HIDDEN NETWORK OWNS THE REPRINT BAY (2026-08-24): the adventuring guild is secretly a
    network of villains in plain sight. The tie-in: the villains own the reprint bay — the
    guild isn't a front that runs adventures, it runs the CLONE. Nemesis: the thing that
    killed you remembers (Shadow of Mordor).
  * THE HALL OF SHARED SUPPER (2026-08-21): the shared meal / shared story as the binding
    mechanic — the feast is where the saga is told. Fold with the republic-wide memory.
  * PLAYTEST DOCTRINE (the standing question: "i love it but will other people?"): prove the
    reprint loop with REAL players BEFORE building more rooms. Demo before full build.
  * TRI-STATE AUDIT FLAG (2026-08-25): the reprint compounding was marked "SOLVED BY DESIGN"
    — it is NOT. The architecture (verkle persistence) exists; the reprint MECHANIC that
    composes it is one build + one playtest away from Supported. That is the next build.
BUILD: the reprint mechanic is the NEXT build (a run seeded from prior-sitting state via the
verkle world + hall_record — the compounding the Hall audit said was missing). Then playtest.
MACHINE: game_world (verkle knots), the Hall (reprint bay), game_dm_llm (the narrator), persona_recall.
