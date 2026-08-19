# STEAL — emergent act / look hooks / Calcifer FILE speech (2026-08-14)

Broken (probed live keep_gate 2026-08-14):
- `_look_at` searched desc only. keep_gate hooks already had `Empty guard post; dice on the table.` and `A toy sword in the mud.` — look dice/sword said Nothing called X.
- `parse_player_speech` returned None for `cast fireball` / `summon familiar`. apply_action had no `act` branch. Fireball playtest died.
- `_talk_calcifer` appended verkle_lance session_ids into narrate (`rib_bus_babelfish-turtles`, `steal_pack-...`).

Organs reused (no sixth module; hang on keep_gate):
- `mag.verkle_lance.trace(noun)` on look + act key nouns (fireball, familiar, babel, calcifer, percolat)
- `mag.fish_ear.decompile` / `originate` — babel fish. Honest gap: decompile substring-replaces `fish` inside `babelfish`, so player speech uses originate/RIB not the mangled decompile
- `mag.percolator.partition` SIGNAL vs THEATER vs NOISE. `percolate()` enqueues novel — not called from keep_gate (do not enqueue)
- `mag.persona_recall.recall(archetype="trickster", region="babel")` — voice only. recount still dumps session_ids; those are theater
- FILE `memory/rib_bus/babelfish-turtles.json` invariant (fish_ear recursive translation, turtles down)
- `mag.chasm_state.persist` already runs from apply_action (liquid_familiar flag + events)
- `mag.swarm_emerge.detect()` only if act still a seam after room+lance. Never fanout. Never in narrate. No holographic_q
- Taught existing `percolator.THEATER_HINTS`: steal_pack, rib_bus_, session_id

Doctrine: no Howl plot. Calcifer = Mag hearth the player named. Babel fish = existing RIB translator. Liquid familiar = that fish in a body of work when summoned.

Proof (import-fresh, campaign gc-1b6bdffd05 keep_gate, apply_action):
- look dice -> `Empty guard post; dice on the table.`
- look sword -> `A toy sword in the mud.`
- cast fireball -> torch/Calcifer + dice hook + iron-bound gates; no fireball knot; not empty; no steal_pack / rib_bus_
- summon familiar -> liquid familiar + RIB turtles-down (babel knot found)
- talk to calcifer -> trickster voice + RIB; no steal_pack, no rib_bus_
- wink at calcifer -> not `You say: "..."`
- ast.parse mag/game_campaign.py OK

Gaps:
- No fireball knot on the chain; act still collides with room torch/dice/gates
- fish_ear.decompile is the wrong surface for player narrate (substring bug)
- persona_recall.recount still includes session_ids internally
- 8765 not restarted — code must import-fresh
