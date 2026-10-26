# STEAL — THE FUN MUD THAT TRICKS PEOPLE INTO DOING WORK (GWAP, 2026-08-16)

**Operator (2026-08-16):** "a fun mud that tricks people into doing work ... be a game company
for me not an agent ... no sacred cows look at our game look where we are going and our references
pad them out find real systems."

## THE CATEGORY IS REAL AND NAMED: GWAP (Games With A Purpose)
Luis von Ahn, CMU 2004. Human-based computation games: outsourcing steps of a computation to humans
in an ENTERTAINING way. Proof at scale: ESP game (2004) -> Google Image Labeler (2006); Foldit
(2008, 240k players, 57k credited in Nature for beating algorithms); reCAPTCHA; Duolingo; EVE
Project Discovery. "Human brains = processors in a distributed system, each doing a microtask of a
massive computation; the game is the incentive to participate."

Source: https://en.wikipedia.org/wiki/Human-based_computation_game (+ Foldit, 2026-08-16 fetch).

## THE FOUR ARCHETYPES (the real design space)
1. OUTPUT AGREEMENT — 2 strangers, same shared input, must MATCH output. Matched labels = the data.
   Vandalism is self-defeating (you can't collude with a stranger). ESP, Google Image Labeler,
   Artigo, TagATune. Anti-spam is STRUCTURAL (matching), not a filter.
2. INVERSION — describer + guesser. Describer reveals/describes until guesser reproduces the
   hidden label; the reveal-path IS the data (location info ESP couldn't get). Peekaboom, Verbosity,
   Train Robots.
3. INPUT AGREEMENT — 2 hidden inputs, tag yours so the partner can tell if they match. TagATune.
4. MACROTASK — complex expert problem gamified; players beat algorithms + TEACH the algorithm
   (foldit watches HOW humans approach it to improve the solver). Foldit, EteRNA, Phylo, EVE
   Project Discovery. Not microtask: players "explore not just the space of solutions but the
   space of SEARCH STRATEGIES."

## THE STEAL: WE ALREADY BUILT A GWAP AND DIDN'T NAME IT
Our own organs already ARE the mechanism — I was looking at the game wrong (fixing "narrate the
scene") when the POINT is the work-hiding. Both halves exist:

### Half 1 — OUTPUT AGREEMENT is already our Roshomon MUD
> `mag/game_mud.py`: "Roshomon MUD. Many seats witness one scene. **Agreement is loot. Unique
> statements are novel. Typing 'I strike' collects nothing.**"

This is von Ahn's output-agreement verbatim: agreement = loot = the data; lone/unverified claims
collect nothing (anti-spam by structure). What we steal from ESP to SHARPEN it:
- MATCHED words/claims = the value. Two independent witnesses agreeing = a folded knot (the data).
- Timed/competitive tension to keep it fun (ESP's engine).
- A "you matched a stranger" flash = the hit of dopamine that IS the reward loop.

### Half 2 — MACROTASK is already our dungeon-as-work
> `game_ramp.work()`: rooms = REAL orchestrator tasks, folded as verkle knots. "The dungeon IS the
> roadmap." `dungeon_dev`: rooms = coding tasks, room HP = clock, conquer = fold.

This is Foldit's macrotask verbatim: the minigame IS the lab work, paid in diegetic loot. What we
steal from Foldit to SHARPEN it:
- A SCORE that reflects real progress (Foldit: score = how well-folded; ours: room HP / task
  actually done) — the score must track REAL value, not fake points.
- Leaderboards + groups (Foldit: groups train new players, share solutions).
- The META-move (Foldit's real genius): WATCH how players approach the puzzle to improve the
  algorithm. Ours: how players/agents route through the dungeon -> rightsize the task router.

### The glue (from the real taxonomy + our MOONSHOT_TABLE steal)
- VERIFICATION IS STRUCTURAL (agreement), not a filter — this is the anti-hallucination guard
  turned into a game mechanic.
- AFK world ticks (LuminariMUD heartbeat; DF "fort burns whether you watch") — already ours via
  `wave.snapshot` + `chasm_state.persist`; the world produces named catastrophes (Boatmurdered)
  whether a player is watching.
- The DM paints two strokes, ends on "What do you do?", never a quiz (Positronick/Spouting Lore)
  — already ours via `game_dm_llm` (creative/playable) + `game_dm_voice` (narrator/TTS).

## THE ONE-LINE MANDATE (the game company's pitch)
**"A fun MUD where two strangers agreeing on a scene, or a party conquering a dungeon room, quietly
folds real work into the world — and the player never sees it as work."**
The fun is real (agreement = loot, dungeon = progress); the work is real (folded verkle knots =
real tasks done); the trick is that BOTH ARE THE SAME ACT. That's GWAP. That's what we already
built. Name it, sharpen it, stop pretending it's only a "narrative game."

## REFUSE
- Do NOT invent a new game/world/store/graph — the organs exist (game_world authority, game_mud
  agreement, game_ramp.work macrotask, dungeon_dev rooms).
- Do NOT make the chat the world — chat is one party seat; game_world is authority.
- Do NOT make fake points — the score must track real folded work, or it's a lie (the operator's
  honesty law).
- Do NOT over-narrate at the expense of the loop — narration is the DM flesh over a world whose
  CORE is agreement-loot + task-conquest.

## SOURCES (real, fetched 2026-08-16)
- von Ahn, "Games With A Purpose" (IEEE 2006) / "Designing Games With A Purpose" (CACM 2008)
- https://en.wikipedia.org/wiki/Human-based_computation_game
- https://en.wikipedia.org/wiki/Foldit (240k players; Nature 2010; players beat Rosetta algorithms)
- Our own: memory/steal/STEAL_GAME_HISTORY_20260814.md, STEAL_MOONSHOT_TABLE_20260814.md,
  handoff/GAME_DRIVER_RIB_20260814.md (RIB 8 fun-first + RIB 9 Boatmurdered), memory/game/STATE.md
