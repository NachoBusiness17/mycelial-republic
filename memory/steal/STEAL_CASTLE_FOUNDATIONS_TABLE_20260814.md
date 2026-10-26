# STEAL — castle in the sky, foundations beneath (2026-08-14)

Operator: the table was a placeholder for things to come. We built the castle. Now the foundations.

## Castle (the desk)

- `dashboard/static/table.html` title still **Mag Table — system test**.
- View is `game_view` carved 23x13 box. Glyphs from campaign scene. Never calls `game_world`, `world_rib`, `wow_manifest`, `game_world_render`.
- Voice: `voice_turn` -> campaign `apply_action`. Residual speech was Stickmin curveball (patched 2026-08-14: residual = IC talk; take/grab parse; look `use_llm=False`).
- Campaign lives in campaign json. Play did not commit to the world core.

## Foundations (standing, unplugged from the table)

- `game_world`: **30 entities, 77 changes, root `89453f8ba2fc332a`**. Keys: Mirror Sea frontier seats, mud, tabletop work, two buildings in `the_mirror_sea`, dfhack test. **No `table.campaign`. No lantern room.**
- `game_world_render`: default region `mycelial-republic`. **0 buildings revealed**. Table never `walk()`.
- `world_rib`: RIB -> 2D field -> obj. The map precedes the territory. Table map is not this field.
- `wow_manifest`: six WORLD/MOD/SAVED/EVENT/EMULATOR/CONTENT invariants. Path: knot -> RIB interprets -> world_rib renders. Table does not mount `domain=wow`.
- `party_subchain`: n=60, verified, parent Verkle leaf from biography tip.
- Biography Verkle: **n_leaves=5652**, tip `c6a7a960…`, root `de658668…`. Tip still amends in place.

## The cut

Two worlds. The lantern is a campaign file. The Republic is a world core. The castle draws the first. The foundations hold the second. They do not touch.

Castles RIB was right: home/story/diary are attempts at the castle. The world is the authority. A player action is a proposal until `game_world.set_state`.

## Hang (small, this steal)

1. `apply_action` folds `table.campaign` + `table.room.<id>` into `game_world.set_state`.
2. Move calls `game_world_render.walk(player, direction, region='guttered-lantern')` — a building appears where you steer.
3. `build_view` paints the world_rib field, not the system-test box, and carries world root.
4. Table title is the lantern, not system test.

Do not call `wow_manifest()` on every turn (six new knots). The invariants already exist. Mount them by using the path.

Papers stay doctrine until play is a knot. This hang is that knot.
