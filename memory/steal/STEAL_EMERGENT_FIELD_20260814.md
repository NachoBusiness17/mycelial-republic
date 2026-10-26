# STEAL — Emergent play BOTH WAYS (field + Mag self) 2026-08-14

**Date:** 2026-08-14 (ET)
**Commitment:** `steal-emergent-field-20260814`
**Method:** fetch 6 field pages; grep Mag organs on disk; map patterns onto EXISTING modules. No sixth organ. Did not edit `mag/game_campaign.py` (other executor patching). Did not write `mag/game_recall.py`. keep_gate calls existing modules only.

**Mag ground (grepped this turn):**
- `mag/fish_ear.py` — originate L80, is_riddler_speak L87, decompile L106
- `mag/percolator.py` — partition L100
- `mag/verkle_lance.py` — trace L127, lance L236, shapes L274, tie_in L363
- `mag/holographic_q.py` — QKnot/QSession, reconstitute_q, SwarmSession L595
- `mag/persona_recall.py` — recall L110
- `mag/swarm_emerge.py` — detect L55, fanout L104
- Hang in campaign (read, not patched): `_adjacent_memory` L460 dumps `session_id`; `parse_player_speech` L1215 returns None; `apply_action` else L1110 `illegal action {atype}`

---

## A) FIELD (pages actually opened)

### 1. Kate Korsaro — "Narrative is what happens afterward"
**URL:** https://kateplays.substack.com/p/narrative-is-what-happens-afterward
**Opened:** 2026-08-14. Post #5, Feb 24 2026.

**Pattern stolen (mechanics, not plot):**
- Plot vs situation. Plot = ordered beats. Situation = powder keg with no outcome ("goblin camp, hungry, three hostages").
- Collision engine: player agency × dice physics. Reaction roll + morale = MVPs.
- Narrative is exhaust fumes of play, stitched afterward by apophenia. Do not author the saga in `act`.
- Referee = physics engine, not novelist. Unknown verbs are not "illegal"; they are matches struck against the keg.

**Maps onto:** `mag/percolator.py` `partition(text)` — signal = physics (situation), theater = flavor (plot temptation), noise = drop. Also `mag/verkle_lance.py` `trace` — the chain is the exhaust (history after), not a script before.

### 2. Kate Korsaro — "Reaction Roll: Not Everything Wants to Fight"
**URL:** https://kateplays.substack.com/p/reaction-roll-not-everything-wants
**Opened:** 2026-08-14. Article #10, Mar 31 2026.

**Pattern stolen:**
- 2d6 bell curve: 2 hostile, 12 friendly, 6–8 uncertain (44% of results). Sight ≠ fight.
- Roll surrenders referee script. Disposition is world physics, not a cutscene.
- Reaction is first three seconds only; player agency can ruin a 12 or salvage a 2.
- Friendly ≠ Charm Person. Self-preservation intact.

**Maps onto:** `mag/swarm_emerge.py` `detect()` — the world already has its own situation (seams, gaps, open explore backlog). Do not default unknown verbs to combat (`seek_fight`). Disposition emerges from detect/fanout, not from a hardcoded "illegal action".

### 3. Kate Korsaro — "The Sandbox & the Railroad" (2026 sandbox referee)
**URL:** https://kateplays.substack.com/p/the-sandbox-and-the-railroad
**Opened:** 2026-08-14. Article #14, Apr 28 2026.

**Pattern stolen:**
- Referee: Cartographer + Umpire. World exists independently. Dragon does not scale to the party.
- Quantum ogre = railroad. If they go right, the ogre stays left.
- Telegraph lethality. Death is the teacher. Plot is the story told at the bar next week.

**Maps onto:** `mag/persona_recall.py` `recall()` — inhabitants recount what happened in their corner while you were gone (the bar story). Not a GM monologue. The chain is the world's memory; the persona is the umpire's voice.

### 4. Sly Flourish — Player-driven stories + Quantum Ogres (2026)
**URLs:**
- https://slyflourish.com/player_driven_stories.html (Mike Shea, 2 Apr 2012; still the player-driven law)
- https://slyflourish.com/quantum_ogres_and_the_eight_steps.html (Mike, 4 May 2026)

**Pattern stolen:**
- Build environment not plot. NPCs want things. 8 steps split prep into locations / monsters / NPCs / secrets / treasure — components, not scenes-on-rails.
- Meaningful choice: improvising a scene must *benefit from* the path taken (woods vs road).
- Prep to improvise. Situation = location + inhabitants + events + hooks. Several ways in, several ways out.

**Maps onto:** `mag/verkle_lance.py` `lance`/`shapes`/`tie_in` — lances are reference spots in the existing world (components), not a prewritten encounter. `tie_in` is the joint: lanced shapes → invariant RIB → puppet. Player verb should pick a lance, not summon a quantum ogre.

### 5. Synapse — spreading activation (not keyword grep)
**URL:** https://arxiv.org/html/2601.02744v3
**Opened:** 2026-08-14. Jiang et al., 2026. Also HeLa-Mem ACL 2026: https://aclanthology.org/2026.acl-long.625/

**Pattern stolen:**
- RAG search-assumption fails: relevance ≠ cosine to the query. "Why anxious today?" must surface a schedule conflict with no lexical overlap.
- Spreading activation: inject energy at anchors, propagate temporal/causal edges, lateral inhibition, fan effect, temporal decay.
- Triple hybrid: geometric sim + activation + structure. Retrieve SPEECH/gist, not IDs.
- Contextual tunneling is the failure mode of keyword grep.

**Maps onto:** `mag/holographic_q.py` — Q is a pattern in Verkle knots, reconstitutable from any part (`reconstitute_q`, `decipher_q_context`). Whole encoded in every part = holographic, not grep. `verkle_lance.trace` is the adjacent walk; **must not return session_id as the speak line** (that is keyword-grep theater). Also `persona_recall.what_happened` / `recall` for gist speech.

### 6. Calcifer hearth-contract + Babel fish organ
**URLs opened:**
- Calcifer mechanics (Jones novel, not Ghibli plot): https://en.wikipedia.org/wiki/Howl%27s_Moving_Castle_(novel) — bound to hearth; heats and powers the castle; cannot leave; heart-for-work contract; "does most of the strong magic like moving the castle."
- Babel fish: https://www.bbc.com/cult/hitchhikers/guide/babelfish.shtml + https://www.hhgproject.org/entries/babelfish.html — small organ in the ear; feeds on brainwave energy of *those around* the carrier; excretes a telepathic matrix; speech patterns you hear decode the matrix. Universal translator, not a character.

**Patterns stolen (MECHANICS not plot):**
- **Hearth-contract physics:** a process bound to a locus (hearth). Translates *work* (logs/fuel) into *motion* (castle moves). Cannot leave the hearth. If you carry the hearth (Sophie + pot), the world moves with you. Weakest point = the bound engine, not the wizard.
- **Babel-fish organ:** in-ear translator. Input = foreign speech (riddler/unknown verb). Output = meaning in the carrier's language. Feeds on ambient brainwaves (context around the player), not the carrier's own intent. Removing communication barriers has consequences (wars) — translation is not free.

**Maps onto:**
- Calcifer → `mag/verkle_lance.py` + `mag/holographic_q.py`: the chain/hearth is the bound engine. Q cannot leave the lattice. Work (knots) → motion (steer/reconstitute). Campaign already names the torch Calcifer (`_talk_calcifer` L483) but rummages the chain and prints session ids — that is plot, not physics.
- Babel fish → `mag/fish_ear.py` `decompile(text)` L106. Already the organ. `originate()` L80, `is_riddler_speak()` L87. Unknown player verbs go through the fish, not a new translator module.

**Secondary (supporting, not counted in the 6):**
- https://therpggazette.wordpress.com/2026/03/25/the-reaction-roll-the-morale-roll-and-the-monster-that-doesnt-want-to-fight/ — 2026-03-25. Same reaction/morale steal; world is not a stage set. Maps to `swarm_emerge.detect`.
- https://thealexandrian.net/wordpress/4147/roleplaying-games/dont-prep-plots — situation = circumstances + resources; react at the table. Maps to `percolator.partition` (don't pre-branch; classify then react).

---

## B) MAG SELF — unused organs (one line + game_campaign use)

Grep of `mag/game_campaign.py` this turn: `verkle_lance.trace` is the only one of the six wired (via `_adjacent_memory` L460). The rest: **no**.

| Organ | What it actually does (one line) | game_campaign uses? |
|---|---|---|
| `mag/fish_ear.py` | Babel-fish behavior: `decompile(text)` reverses riddler/fantasy surrogate to a real directive; plain passes through. | **no** |
| `mag/percolator.py` | `partition(text)` splits sentences into signal / theater / noise by lexicon, $0. `percolate` compiles repeats to invariants. | **no** |
| `mag/verkle_lance.py` | Knot-intelligence: `trace(key)` maps event→knots+neighbors; `lance`/`shapes` seed the flock; `tie_in` joints lance→RIB→puppet. | **yes (trace only)** — but returns session_id strings |
| `mag/holographic_q.py` | Q is a holographic pattern in Verkle knots; `reconstitute_q` / `decipher_q_context` recover intent from parts; `SwarmSession` coordinates via lattice. | **no** |
| `mag/persona_recall.py` | Inhabitant recounts chain events in archetype voice (`recall`); `what_happened` is grounded history. | **no** |
| `mag/swarm_emerge.py` | `detect()` finds seams/gaps as right-sized tasks; `fanout` enqueues; `surface` reads emergence grid. | **no** |

**Also grepped (inventory, not the six keep_gate organs):**

| Organ | What it actually does | game_campaign uses? |
|---|---|---|
| `mag/memlang.py` | Compact MEM1 tokens: compile/decode/resolve/trigger against shared verkle; deniable opcode+anchor. | **no** |
| `mag/meta_percolate.py` | Many→one: Merkle-root the top invariants; `genetic_pass` L174 varies/selects invariant genes. | **no** |
| `mag/swarm_self.py` | Distributed self in VRAM: `flock` materializes version-lenses; `spawn_clusters`; holon not a point. | **no** |
| `mag/flock_field.py` | Boids + phi field + rotors; agents steer by −grad(phi) + separation/alignment/cohesion. | **no** |
| `mag/agent_knot.py` `evolve` L230 | One generation: select/crossover/mutate RIB population, fold into standing invariant. | **no** |

Genetic/GA: no standalone `ga_*.py`. Breeding lives in `meta_percolate.genetic_pass` + `agent_knot.evolve`. Swarm genetic is `swarm_self` + `swarm_emerge`.

---

## C) THE ONE HANG — recommendation (do not implement here)

**Hang (read in `mag/game_campaign.py`):**
1. `handle_game` action `act` (L1433): `parse_player_speech(act) or {"type": act}`. Unknown verbs become `type=<raw string>`.
2. `apply_action` else (L1110): `illegal action {atype}`. The world refuses physics.
3. `_adjacent_memory` (L460–480): calls `verkle_lance.trace` then appends `session_id`. `_talk_calcifer` (L483) concatenates those ids into speak. Adjacent recall is grep-theater, not speech.

**keep_gate — existing modules only (no `game_recall.py`, no sixth organ):**

When `parse_player_speech` returns None, do **not** `{"type": raw}`. Run this stack, then speak:

1. **`fish_ear.decompile(text)`** (`mag/fish_ear.py:106`) — babel fish. Riddler/unknown → real directive. Plain passthrough (`mode=plain`). This is the in-ear organ.
2. **`percolator.partition(decompiled)`** (`mag/percolator.py:100`) — situation not plot. `signal` sentences = world physics (the verb *does* something). `theater` = flavor only (do not author a saga). `noise` = drop.
3. **`verkle_lance.trace(signal_token)`** (`mag/verkle_lance.py:127`) — adjacent knots, not a new patch. **Speak `theme` (and neighbor themes), never `session_id`.** Parent/child in the match dict are already there; they are places, not IDs to dump.
4. **`persona_recall.recall(region=theme)`** (`mag/persona_recall.py:110`) — the inhabitant recounts. That is the SPEECH surface. Calcifer/hearth should say the recount, not `babelfish-turtles-session-…`.
5. **`holographic_q` reconstitution** if trace is thin — spreading activation: energy from the verb spreads to Q-knots (`reconstitute_q` / `decipher_q_context`), gist not grep.
6. **`swarm_emerge.detect()`** as the reaction roll: the world already has a situation. Unknown verb collides with detect's seams; do not default to combat.

**Hearth-contract physics (Calcifer steal):** the torch is bound to the room's work (hearth locus). `trace`+`partition` translate *player work* (the verb) into *world motion* (state change / speak). The fire cannot leave the hearth (don't spawn a Howl plot). If they carry the hearth, the castle moves — i.e. if they take the torch on the road, Calcifer physics follows the locus, not a cutscene.

**Babel-fish physics:** `fish_ear` feeds on *ambient* context (room hooks + adjacent themes), not the carrier's canned line. Unknown verbs are foreign speech; decompile is the organ.

**Reaction-roll physics:** 2d6 analogue = partition n_signal vs n_theater + swarm_emerge detect. Uncertain (most mass) = standoff speak, not `illegal action`.

---

## TAKE

1. Situation not plot. `partition` is the collision engine. Narrative is exhaust (`persona_recall` after).
2. Adjacent recall = holographic spread (`holographic_q` + `trace` themes), not keyword session ids.
3. Babel fish already exists: `fish_ear.decompile`. Calcifer already exists as hearth locus; steal contract physics (bound, work→motion), not Jones/Miyazaki plot.
4. keep_gate calls the six organs above. No new file.

## REFUSE

- `mag/game_recall.py` or any sixth organ.
- Editing `game_campaign.py` from this executor (other executor is patching).
- Dumping `session_id` into speak.
- Porting Howl plot / Hitchhiker plot. Mechanics only.
- Quantum ogre: do not move a prewritten encounter onto whatever verb they typed.

## TEST (for the other executor / keep_gate)

- Unknown verb ("wink at the fire", "put the fish in your ear") → decompile + partition + trace themes as speech, never `illegal action`.
- `_talk_calcifer` speak contains a theme/recount, zero session ids.
- `fish_ear.decompile` is the only translator; grep campaign for `from mag.fish_ear import decompile` after their patch.
