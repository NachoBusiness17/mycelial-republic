# AC11 — SYNC: the estate's last-mile wave lands in the-mountain (2026-09-30)

Lane AC11. Mission: the estate twin (`roblox_to_godot/` + `mag/water_graph.py`)
ran ahead of `the-mountain/game/` since the last sync (dca3801, W3). Sync the
updated files plus the new ones, update the README feature list, commit, smoke.
Receipt-first: commit and proofs below are byte-run, all numbers from executed
commands.

## Commit (the-mountain repo — committed, NEVER pushed)

- **Hash:** `d99b9ea233ddfd1626aa499719728bb38cd08d0b` (short `d99b9ea`)
- 12 files changed, +31,094 / −91. Working tree clean after; `origin/main..HEAD` = 1
  (local-only, per the repo's never-push law).

## What synced (byte-identical, every copy verified by `cmp`)

Updated (the W3 sync set, moved again):

| the-mountain file | estate source | wave |
|---|---|---|
| `game/scripts/game.gd` | `roblox_to_godot/scripts/game.gd` | Z7 brain rig (motion rows, legality gate, fallback), Z14 feel (tick 0.5 s, pool pull 22), Z10 H-key head-law toggle, T-key terrain hook |
| `game/systems/water_graph.gd` | `roblox_to_godot/systems/water_graph.gd` | Z10 graded-head hydrology (mag/hydrology.py mirror), AC5 mirror of the V5 economy law (waste is a basin) |
| `game/systems/flock.gd` | `roblox_to_godot/systems/flock.gd` | V6 flee push 2.5→6.0, FLEE_RADIUS 14→20 |
| `server/_vendor/water_graph.py` | `mag/water_graph.py` | V5 economy law (waste holds; STARVED spill routes to a basin or holds), LW5 probe-time reservation (neg-volume fix), siphon `primed` roundtrip |

New (the files that did not exist at dca3801):

| the-mountain file | estate source | wave |
|---|---|---|
| `game/scripts/hud.gd` | `roblox_to_godot/scripts/hud.gd` | AA5 drawn HUD |
| `game/scripts/juice.gd` | `roblox_to_godot/scripts/juice.gd` | V4 shake/flash/synth-audio/vignette |
| `game/scripts/terrain_loader.gd` | `roblox_to_godot/scripts/terrain_loader.gd` | Z3 St Helens board loader |
| `game/systems/fish_brain.gd` | `roblox_to_godot/systems/fish_brain.gd` | X9 policy layer |
| `game/systems/water_particles.gd` | `roblox_to_godot/systems/water_particles.gd` | X8 surface particles |
| `game/N46W122_board.json` | `logs/terrain/N46W122_board.json` (432,386 B) | Z3 board data, placed at the loader's designed in-project fallback path (`res://N46W122_board.json`) so T works out of the box |

Unchanged-and-verified-same: `project.godot`, `scenes/main.tscn`,
`scripts/net_client.gd`, `scripts/player.gd` (cmp SAME against the estate twin;
they did not move since W3).

README updates in the-mountain: root `README.md` feature list rewritten (brain,
juice, HUD, particles, terrain, hydrology, economy, new `server/` layout row,
Status de-staled — "server not published" was false since bac2b89/Y5);
`game/README.md` controls now document H and T, organs table carries the five
new files, verification status refreshed, AC11 sync receipt appended.

## Verification (all run 2026-09-30, byte-captured)

- **Headless smoke, estate venv, the-mountain as cwd** (the Y5 demo idiom):
  `.venv/Scripts/python.exe -m server.server --demo` → exit 0,
  `THE CROWN FILLS. WIN at tick 4; boiler boiled 4, tagger tagged 30.`
  Same WIN-at-tick-4 numbers as the Y5 proof on the pre-V5 vendor — and the
  demo's tick table now shows waste accumulating 1→2→3→4 (V5 basin law live
  in the vendored engine, not deleting units anymore).
- **Godot client, estate binary, the-mountain root** (Z14/W3 idiom):
  `tools/godot/Godot_v4.3-stable_win64_console.exe --headless --path game
  --quit-after 60` → exit 0, banner only; `--quit-after 300` → exit 0, banner
  only (no server running → the run exercises the SOVEREIGN fallback);
  `MAG_HYDROLOGY=1 --quit-after 300` → exit 0, banner only. Zero script
  errors, zero warnings in all three.

## Known estate-side staleness carried verbatim

`fish_brain.gd:30` mirrors `FLEE_RADIUS := 14.0  # flock.gd:9` — stale since
V6 bumped flock.gd to 20.0 (V6's own handoff note flagged it for that lane).
Byte-identity beats a local fix in a sync (a diverging copy breaks the next
one); verified present in the shipped copy and named in the-mountain's
game/README.md sync receipt so the estate lane that owns it stays on the hook.

## Out of scope, named

The estate's own `server/` (server.py, world.py, protocol_table.py,
innkeeper.py, persistence.py...) has also moved ahead of the-mountain's Y5
snapshot (LW5/LW6/LW7/LW8 waves). The mission's sync set is the game/ twin +
water_graph.py, so the server tree stays at Y5 in the-mountain; its refresh is
a named next lane, not smuggled in here.

— AC11 sync seat, 2026-09-30
