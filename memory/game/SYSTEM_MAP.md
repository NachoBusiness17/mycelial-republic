# THE LAND OF FORGETFULNESS — system mind map (Markmap / Freeplane-able outline)

## THE GAME (what it is)
- The deliverable (operator's sw27): lead-in game that funds the supercomputer
- Vertical trigger: walk in -> world recounts what happened while you were gone -> act -> a building appears
- Play IS the work (Enders Game): the dungeon rooms are real coding tasks
- "Not dumb" = emergent + campy + rendered + memorable, not bones

## THE RAMP (game_ramp — tabletop -> mud -> roguelite, master each)
- tabletop: the simplest world (a scene + a DM voice + actions) — PERFECT
- mud: navigable text world (rooms + exits on the world_rib ASCII map) — PERFECT
- roguelite: run-based dungeon (descend, permadeath, best depth) — PERFECT
- descend() -> master current tier -> next
- then scale: new games at the base level (the swarm-ramp method)

## THE ENGINE (game_campaign — the server-authoritative world)
- game_world = the authority (verkle knots; a change is a seal)
- verbs: look / examine / take / talk / use / move / rumor / drink / rest / wait / listen / sneak / work / attack / flee
- CLOCKER (Infocom): hall goblin jobs tick on look/wait; listen hears unaware; failed sneak alerts the camp; rope tugs while you stall
- examine -> command/verb reference (how to play, grounded in the room)
- try <verb> <object> -> roll dice -> success/fail -> narrate consequence -> hint next move (fun-first)
- _narrate_room / _talk_events: deterministic engine, now with creative DM opt-in (MAG_CAMPAIGN_LLM)

## THE CREATIVE DM (game_dm_llm — deepseek v4 flash)
- thinking ON (coherence) + temp 0.8 + max_tokens 2200 (was 700 -> empty-reply bug, FIXED)
- stable LORE prefix (cached, cheap) + fresh scene/action tail (novel)
- _raw_call(system, scene, history): the reusable primitive (custom system prompt)
- deepseek-first routing (was silently falling back to ollama — key-env mismatch FIXED)

## THE SAGA (game_saga — the world's memory / running gag)
- add(name, event) -> fold to game_world; recall() -> "what happened while you were gone"
- running_gags: a name that recurs becomes a running gag (the elephant, Calcifer, the mug)

## THE EGREGORES (invariant_npcs — the NPCs ARE the invariants, personified)
- 8 curated souls: Mira(Recorder) / Calcifer(Hearth) / Cartographer / Truth / Warden / Custodian / Farseer / The Tick
- auto-spawn: from_invariant_ledger() -> a "Witness of <module>" per discovered invariant (23 total)
- physical embodiment: manifest(name) — the body IS the principle (Cartographer's skin = coastline)
- egregore semantics: nourish() by attention; outlives sessions; the cast grows as invariants are discovered

## THE OVERNIGHT / NIGHT STACK (what runs while you sleep)
- campaign_runs (hourly): the swarm plays a session -> memory/game/campaign_runs/*.jsonl (the corpus)
- hero_journey (6h): reads corpus + saga + roster -> writes memory/game/hero_journey.md (5k+ epic)
- iterate-don't-repeat: seeded/shuffled sessions + near-duplicate detection -> self-heals, no repeat loops
- GOVERNOR LOOP = the thing that runs these cadences (was NOT running -> the miss; must be started via mag_up.cmd / start_everything.cmd)

## THE DRIVER RIB (handoff/GAME_DRIVER_RIB_20260814.md — the heat + leash)
- RIB 0 THE DRIVER: cold start -> one narrow brief -> PROOF GATE (prove it or don't claim it)
- RIB 7 LOAD THE CORPUS: memory/steal scifi/cyberpunk/videogame steals + repo memory
- RIB 8 THE MANDATE: emergent, campy rendered scenes, Memento hook, fun-first loop
- RIB 9 THE BOATMURDERED FUN LAW: specific/named/absurd failure, recurring gags, world ticks while away

## LESSONS (the self-steal, so it doesn't recur)
- RIB-debug EVERY finished piece: get_errors + drive the real function + read output (prove it or don't claim)
- models/ is a PYTHON PACKAGE (only models/saelis-31b/ is weights) — never blanket-dockerignore it
- mag/ + configs/ are LIVE-mounted; models/ + dashboard/ are BAKED (need rebuild)
- the governor loop is NOT the container supervisor — it's a separate process (mag_up.cmd)
- deepseek thinking-on eats max_tokens -> empty replies -> give it budget (2200+)
- verify the loop that runs a cadence is ALIVE before claiming "wired and running"

## FIELD (voxel/SDF/octree + swarm — steal, no new organ)
- The keep is a signed field. Swarm (cheap seats) walk its gradient by playing legal verbs in the current room. That is formation (shaped-swarm), not a voxel renderer.
- Hierarchical LOD is gpu_lifecycle: what sits hot in VRAM vs on disk. Same tree as the lattice/RIB.
- Incremental map (Voxblox-family) is already game_world seals + campaign JSON. Do not invent mag/voxel.py or mag/sdf.py.
- Shared worldspace overlaps = party_subchain + world_rib. Particle swarm = the caravan on the road (symptom). The field they fall into is the keep (the bug).
- Graphics demos (GDVoxelTerrain, sparse SDF raymarch) are look, not a new Mag surface. /wave is the text adventure.
