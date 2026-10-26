# AJ5 — Adam's onboarding pack for the-mountain (2026-09-30)

Lane AJ5. Mission: sync anything new per the established vendoring pattern,
write `ONBOARDING.md` at the-mountain root for when Adam's invite lands
(LW2: not invited yet — no GitHub username on file; operator holds the
command), commit with a cold-readable message, file this receipt. MAY commit
the-mountain, NEVER push.

## Commit (the-mountain — committed, NEVER pushed)

- **Hash:** `7d5dbe275fe73ac462e0a6493391531fbd37e637` (short `7d5dbe2`)
- 12 files changed, +1,308 / −107. Working tree clean after;
  `origin/main..HEAD` = 3 (d99b9ea, cf2ec7d, 7d5dbe2 — all local-only per the
  repo's never-push law; the operator pushes when the invite lands).

## What synced (byte-identical, every copy verified by `cmp` after copy,
## re-cmp'd at the end — the twin moved mid-flight once, see incident below)

| the-mountain file | estate source | wave |
|---|---|---|
| `game/scripts/game.gd` | `roblox_to_godot/scripts/game.gd` | AD2 stubs/dim + **AJ4 playtest fix** (E-key valve cycling at shared pool dots — the siphon was unreachable under first-in-dict tie-break; exactly-once `water_event` signal replaces the saturating last_events feed poll) |
| `game/systems/water_graph.gd` | `roblox_to_godot/systems/water_graph.gd` | AD1 pipe-fracture law (full-bore stress, `120 + djb2(name) % 240`, permanent burst, spray to lowest, refused reopen, spec roundtrip) |
| `game/systems/water_particles.gd` | `roblox_to_godot/systems/water_particles.gd` | AD2 destruction visual grammar (STARVED rings, siphon kick, steam columns, crack decals + spray) + AJ4 signal-driven delivery |
| `game/systems/flock.gd` | `roblox_to_godot/systems/flock.gd` | LM9 positive mode banked (default off, threat path unchanged; estate working-tree, mtime 13:58, parse-checked clean pre-copy; nothing in game.gd sets `positive` yet) |
| `server/_vendor/water_graph.py` | `mag/water_graph.py` | AD1 fracture law in the Python engine, byte-verbatim (last refresh was AC11; AD1 landed 07:14, after AC11's 07:02) |
| `game/scripts/gravity_plane.gd` | `roblox_to_godot/scripts/gravity_plane.gd` | AD7 3D gravity volume (NEW in the-mountain) |
| `game/scripts/gravity_demo_boot.gd` | twin, same path | AH15 demo boot (NEW) |
| `game/scenes/gravity_demo.tscn` | twin, same path | AH15 demo scene (NEW) |

AJ4 note: AJ4's bytes landed in the twin DURING this lane (mtimes 14:29:15 /
14:29:42, caught by the end-of-lane re-cmp at ~14:20+). The twin was stable
75+ s and parse-clean; its own receipt (`AJ4_PLAYTEST.md`, cited in the code
comment) had NOT landed on disk at sync time — my parse-checks + smokes below
are the verification of record for the copy. Unchanged-and-verified-same:
`project.godot`, `scenes/main.tscn`, `scripts/hud.gd`, `scripts/juice.gd`,
`scripts/net_client.gd`, `scripts/player.gd`, `scripts/terrain_loader.gd`,
`systems/fish_brain.gd` (cmp SAME). The gwap/ledger `_vendor` files DIFF by
design (AD6's import-path rewrites), untouched.

## Docs landed in the-mountain

- **`ONBOARDING.md` (new, root):** what the game is (one paragraph), how to
  run (Godot 4.3+, import `game/project.godot`, F5; both modes — server
  present = AUTHORITATIVE, absent = SOVEREIGN solo after 2 s probe), the gate
  wire line, server demo commands, controls table (mouse/SPACE/E, **T**
  terrain + click-to-boil, **H** hydrology, R, the gravity demo scene), E-key
  cycling playtest note, what's next -> `docs/GAME_PLATFORM_BASECAMP.md`
  (B0/B1 done, B2+ open, near threads: positive-flock wiring, 3D controller,
  terrain content), and "how to talk to the estate" (one paragraph: a
  plain-language line in `queue/steer_agent.md` + `main.py steer-agent
  --sync`; durable asks as dated markdown receipts in `watch/inbox/`, INDEX
  first; via Mark if no estate machine access).
- `README.md` + `game/README.md`: destruction + gravity + AJ4 paragraphs,
  organs-table rows, AJ5 sync receipt, Status updated; `.gitignore` now
  blocks `.godot/` (import cache deleted after verify, AH15 idiom).

## Verification (bytes, estate Godot 4.3 console exe + estate venv, this session)

All run against the-mountain's `game/` after the FINAL (post-AJ4) copies;
import cache deleted after:

- `--headless --path game --import` → exit 0, 0 SCRIPT ERROR lines.
- `--quit-after 60` → exit 0, 0 errors; `--quit-after 300` → exit 0, 0 errors
  (no server → SOVEREIGN fallback exercised); `MAG_HYDROLOGY=1 --quit-after
  300` → exit 0, 0 errors.
- `res://scenes/gravity_demo.tscn` headless → exit 0, 0 errors, both AH15
  probes OK (plane 2 and 3: align 1, camera_align 1, reparented true, 25
  ticks — the demo's quit code carries the verdict).
- Server demo, estate venv, the-mountain cwd: `python -m server.server
  --demo` → exit 0, `THE CROWN FILLS. WIN at tick 4; boiler boiled 4, tagger
  tagged 30`, waste=4 basin visible (V5 law intact under the AD1 fracture
  vendor).
- Pre-AJ4 runs of the same three smokes were also green; AJ4's changes were
  then re-smoked (above), not trusted forward.

**Receipt law:** every exit code and error count above is from a command run
this session; no hand-counted claims.
