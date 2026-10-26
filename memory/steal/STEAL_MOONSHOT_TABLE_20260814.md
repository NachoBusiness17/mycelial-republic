# STEAL_MOONSHOT_TABLE — play-as-work tabletop, both ways (2026-08-14)

Steal note only. Do not edit `game_campaign.py`. No `idle_tick.py`. No sixth organ. No `game_recall.py`. No new speaker.

Field pages fetched (6):
- Matuschak, *Exorcising us of the Primer* — https://andymatuschak.org/primer/
- Positronick DM soul — https://positronick.com/api/souls/dungeon-master.md
- Spouting Lore, PbtA conversation — https://spoutinglore.blogspot.com/2020/01/my-framework-for-gming-dungeon-world.html
- LuminariMUD heartbeat — https://luminarimud.github.io/Luminari-Source/systems/CORE_SERVER_ARCHITECTURE.md
- DF Storyteller legends API — https://dfstoryteller.com/
- Alexandrian, Blades progress clocks — https://thealexandrian.net/wordpress/40424/roleplaying-games/blades-in-the-dark-progress-clocks

Also: Diamond Age / Second Primer (already in `DIAMOND_AGE_STEAL_20260810.md`); EVE Project Discovery / Foldit (play-as-work); OSR+ downtime; OSE 2d6 reaction (search; OSE SRD fetch died).

---

## A) FIELD → MAG (existing organs only)

### 1. Play-as-work / games that do real work

**Field.** Foldit and EVE Project Discovery: the minigame *is* the lab work (protein fold, cell gating), paid in diegetic loot. Diamond Age Primer: Nell learns by living a shaped story. Matuschak invert: do not sequester learning in a fantasy book; weave support into the project that already matters. DF legends: the world writes history as files; after-action is query, not recap-by-memory. Chasm world-as-files already stolen (`STEAL_PLACE_REMEMBERS_20260814.md`).

**Mag.**
| field | organ | hang |
|---|---|---|
| world-as-files / legends after-action | `chasm_state.persist` / `chasm_state.recall` | place diary `## happened`; look reads it; overwrite is amnesia |
| Primer as holon (map→compile→play→chronicle) | `primer.primer` / `primer.play_rooms` | macro self-similar example; rooms *are* the roadmap |
| rooms = coding tasks (Foldit-in-the-dungeon) | `dungeon_dev.assign_workers` / `conquer` | party thrown at a real task; room HP = clock; enqueue only when SIGNAL says work |
| inhabitants recount while AFK | `persona_recall.recall` | stone 1; chain-grounded, attributed |

Campaign already calls persist/recall, persona_recall, fish_ear, percolator. Primer + dungeon_dev are still dark on the table.

### 2. Living world that ticks while player AFK

**Field.** MUD `heartbeat()` (Luminari: 10 Hz pulse; mobiles, weather, regen, zone reset run whether you typed). Player idle ≠ world pause. DF unpause: ticks only while unpaused; AFK fortress still burns. OSR downtime: montage/journey/faction clocks advance in abstract time. Discworld: the world may tick; *your client must not unidle you*. Mag analog: desk polls; engine does not fake a player.

**Mag.**
| field | organ | hang |
|---|---|---|
| standing pulse / copyover snapshot | `wave.snapshot` | `/wave` already is this. Desk polls it. That *is* the AFK tick. |
| recount while gone | `persona_recall.recall` | "while you were gone, in the {frame}, I saw:" |
| place still happened | `chasm_state.persist` | deeds append even if the player is elsewhere next poll |
| noise vs signal while idle | `percolator.percolate` | strip theater; novel SIGNAL queues explore; do not invent an `idle_tick.py` |

**Law:** no `idle_tick.py`. AFK = `wave.snapshot`. Do not send a fake utterance to `table_turn.handle`.

### 3. Tabletop conversation: DM narrates until player speaks; socratic GM (not quiz)

**Field.** Positronick DM: paint two strokes, end on a beat that demands a response, never decide for the PC, never wall-of-text. Spouting Lore: soft move → **"What do you do?"** (ritual, not a quiz) → resolve or say what happens → wait. Socratic GM asks to *shape direction*, not to grade. Mentzer nested reaction tables = procedural conversation; Mag must not reproduce the quiz tree.

**Mag.**
| field | organ | hang |
|---|---|---|
| player door (speech in, engine out) | `table_turn.handle` | MUD door. Channel=table. Never Voice Mag, never DeepSeek. |
| I AM THE DM — set the scene | `game_dm.dm_narrate` | room is authority. Do **not** call `game_dm.turn` / `ask_player` (those spawn frontier seats = new speakers). |
| narrator-only for TTS | `game_dm_voice.extract_narrator` | `speak_text` = ## Narrator body. Full card stays in `answer`. No sixth organ. |
| socratic, not quiz | `socratic_research.ask(enqueue=False)` | frame (5-W + lens) then **one** direction question in the narrator beat. `enqueue=False` is the contract: do not dump five swarm tasks from a table look. Honesty: `ask()` currently ignores `enqueue` and always `route_novel` — prototype must not call it until that is true, or call `socratic_research.frame()` and write one beat by hand. |

Loop: narrate → extract_narrator → **stop**. Player speaks → `table_turn.handle`. Soft lead is "What do you do?", never a multiple-choice quiz.

### 4. Attention mapping: player utterance → party tasking

**Field.** OSR 2d6 reaction: 2 attack / 3–5 hostile / 6–8 uncertain / 9–11 indifferent / 12 eager. Bell curve parks most encounters in *uncertain* — initiative stays with the player. Blades clocks: 4/6/8 segments; faction clocks tick in downtime; a filled clock *happens*. Utterance is not a verb list; it is a disposition + a clock tick.

**Mag.**
| field | organ | hang |
|---|---|---|
| utterance → real intent | `fish_ear.decompile` | riddler-speak to directive; plain passes through |
| reaction roll (signal / theater / noise) | `percolator.partition` | SIGNAL = party may task; THEATER/NOISE = strip, do not narrate steal_pack |
| clocks / room HP | `dungeon_dev` room `hp_left` | fill on SIGNAL work; conquer folds a knot. Racing clocks = in-progress vs undiscovered |
| party tasking | `dungeon_dev.assign_workers(room, enqueue=False)` until SIGNAL is a real coding room | same `enqueue=False` law as socratic: table talk does not auto-swarm |

---

## B) MAG SELF — unused by `/wave` right now

`wave.snapshot` is `/wave`. It mounts verkle_knot, party_subchain, game_world, game_view.build_view, code_team, surface_render. It does **not** import the table organs.

| organ | unused by /wave |
|---|---|
| `chasm_state.persist` / `recall` | **yes** |
| `persona_recall` | **yes** |
| `primer.py` | **yes** |
| `table_turn.handle` | **yes** (door is `/table`, not `/wave`) |
| `dungeon_dev` | **yes** |
| `fish_ear` | **yes** |
| `percolator` | **yes** |
| `game_dm` | **yes** |
| `socratic_research.ask` | **yes** |
| `wave.snapshot` | **no** (it *is* /wave) |
| `game_dm_voice.extract_narrator` | **yes** |

Five already inside campaign (do not re-invent): `chasm_state`, `persona_recall`, `fish_ear`, `percolator`, and the door `table_turn.handle`. Still dark on the table: primer, dungeon_dev, game_dm.dm_narrate, extract_narrator, socratic_research.ask(enqueue=False). `/wave` sees none of them except itself.

---

## Hang (the one the prototype should call)

**`game_dm_voice.extract_narrator`**

After `apply_action` builds the passage card (`## Narrator` then leads), call `extract_narrator(passage)` and put that in `speak_text`. Then **stop**. Wait for the player. `table_turn.handle` is already the door.

Do not: `idle_tick.py`, `game_dm.turn` / `ask_player` (new speakers), `socratic_research.ask(enqueue=True)`, `dungeon_dev.assign_workers(enqueue=True)` from table talk, a sixth organ.

AFK tick is already `wave.snapshot`. Play-as-work clocks live in `dungeon_dev` room HP, filled only when `percolator.partition` says SIGNAL after `fish_ear.decompile`.
