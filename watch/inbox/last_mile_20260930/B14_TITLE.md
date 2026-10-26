# B14 - TITLE: the door for a first stranger (2026-09-30)

Lane: last-mile wave ("the game boots straight into the world; a stranger
needs a door"). File ownership held: `roblox_to_godot/scenes/title.gd` (new)
+ `roblox_to_godot/scenes/title.tscn` (new) + title wiring
(`roblox_to_godot/project.godot` main_scene line, `roblox_to_godot/
scripts/game.gd` door branches). No commit made by this seat.

## What landed

| Mission clause | Mechanism |
|---|---|
| Game name | "THE MOUNTAIN" centered at size 44 over a dim pure-geometry skyline ridge; tagline "a small puzzle world about water" (PLAYER_ONE.md section 1, verbatim fragment). |
| Two mode buttons | Two chamfered door panels (hud.gd `_panel` idiom): SOVEREIGN / "play alone" (teak) and AUTHORITATIVE / "join the server at" + an inset host:port field slot (amber) seeded 127.0.0.1:8800, or MOUNTAIN_SERVER when the env var is set (net_client.gd begin() grammar; the env still outranks the field at connect time). |
| Controls card | Lower-left CONTROLS panel: the six rows Mouse / SPACE / E / R / H / T with PLAYER_ONE.md section 3's wording verbatim ("wording from the game's own card"), deterministic pixel-measured greedy word wrap. |
| "verify everything" one-liner | "verify everything: check every claim yourself by running the thing. see PLAYER_ONE.md" (PLAYER_ONE.md section 1's own claim, compressed; file: `watch/inbox/mountain_climb/PLAYER_ONE.md`). |
| Keyboard nav, no mouse | UP/DOWN toggle the two rows, ENTER walks through; printable keys + BACKSPACE edit the field ONLY while the AUTHORITATIVE row is selected (ENTER/nav never type; unicode >= 33, no spaces); mouse_filter IGNORE, mouse does nothing. Headless-proof by construction. |
| ESC returns to title | game.gd `_unhandled_key_input` KEY_ESCAPE -> `change_scene_to_file("res://scenes/title.tscn")`, not won-gated (R keeps its restart role). The swap frees the whole Main tree (graph, flock, particles, net, timers) = the clean re-init; `_exit_tree` calls `net.stop()` first (the socket is not a node). |
| Mode handoff | title.gd statics: `chosen_mode` (-1 no title ran / 0 sovereign / 1 authoritative) + `join_endpoint`. game.gd `_begin_net_probe`: sovereign door -> `_fall_sovereign()` NOW, no NetClient, no 2s probe; -1 (direct scenes/main.tscn run, AC9 harness) keeps W1's auto-join bytes; authoritative door -> the field's host:port parses into net.host/net.port (env > field > compiled defaults, begin() re-reads the env). `field_text` persists across ESC walks so a typed endpoint survives. |

Pure _draw like the HUD law: one Control, drawn geometry + draw_string only
(fallback font, no themes/styleboxes/images), zero RNG, no wall clock (the
cursor blink phases off the door's own accumulated process deltas; nothing
samples the OS clock).

## Verification (byte-run 2026-09-30, Godot 4.3 console exe, headless)

- Boot smoke, final bytes: `--headless --path roblox_to_godot
  --quit-after {60,300}` -> exit 0, BANNER ONLY (the door is the main scene
  now); `MAG_HYDROLOGY=1` 60f -> exit 0 banner only.
- Probe (throwaway `b14_harness.gd`, AC9 SceneTree + inner- Probe idiom,
  real `Input.parse_input_event` keys, sim_time hook on the game host,
  deleted after): **18/20 PASS** (two consecutive identical runs):

```
B14 ck PASS boot_title sel=0 field=127.0.0.1:8800
B14 ck PASS boot_field_default 127.0.0.1:8800
B14 ck PASS nav_down sel=1
B14 ck PASS nav_up sel=0
B14 ck PASS typing_gated 127.0.0.1:8800
B14 ck PASS field_edit 127.0.0.1:9000
B14 ck PASS pre_enter_sovereign
B14 ck PASS enter_starts_game scene=Main
B14 ck PASS sovereign_now mode=2
B14 ck PASS sovereign_no_net net=<null>
B14 ck PASS sim_time_hook sim_time=0.261
B14 ck PASS sim_time_runs now=0.507 was=0.261
B14 ck PASS fresh_world total=8 score=0 won=false
B14 ck PASS esc_returns scene=Title fresh=true
B14 ck PASS title_reselects sel=0
B14 ck PASS field_persists 127.0.0.1:9000
B14 ck PASS reenter_fresh_instance id=144468608409
B14 ck PASS reenter_clean_state sim_time=0.069 won=false score=0
```

The mission's core walk is fully green: boot reaches the title (selection
0 = sovereign, default field), keyboard nav both ways, typing is gated to
the authoritative row, field edit (BACKSPACE x4 + "9000"), ENTER starts the
game as SOVEREIGN immediately (no probe window, no NetClient), the game
runs (sim_time advances; world conserves its 8 units; unwon; score 0), ESC
returns to a FRESH Title instance (different instance id, selection reset,
typed endpoint persisted via the static), walking in again re-inits clean
(new instance, sim_time restarted).

## The 2 blocked checks (not this lane's defect)

```
B14 ck FAIL auth_probes mode=0 net=false
B14 ck FAIL auth_deadline_falls_sovereign mode=0
```

Cause, bytes: sibling lane B3's in-flight `roblox_to_godot/network/
net_client.gd` (extends `scripts/net_client.gd`) redeclares `var _buf` at
its line 57 while the parent declares `var _buf := PackedByteArray()` at
line 39 -> parse error "The member \"_buf\" already exists in parent class"
-> `NetClient.new()` raises "Invalid call. Nonexistent function 'new' in
base 'GDScript'" inside game.gd `_begin_net_probe` line 266, which aborts
the function BEFORE this lane's endpoint-parse lines run and before the
W1 deadline timer is created. Unchanged on disk from 15:17 through this
lane's close (two retries). Once B3 heals their file, rerun the harness to
turn the last two checks green; the unverified links are exactly
`NetClient.new()` (B3's) and this lane's 6-line field->host/port parse
(the deadline fall itself is pre-existing W1 logic, byte-verified by
AC9's authoritative smoke).

## Defects found and fixed during the byte-runs (fix comments in file)

1. `const RIDGE := PackedVector2Array([...])` -> parse error "Assigned
   value for constant isn't a constant expression" (the constructor call is
   not a const expression in 4.3); now a var, same bytes every instance.
2. Door panel sub-label baseline +52 collided with the field slot at
   +50..+72 (the slot's opaque fill drew over the "join the server at"
   glyphs' lower half); baselines moved to +26/+44, 4 px clear.
3. Harness-only: fresh_world first asserted spring==6, but ~1s of play
   legitimately ticks p_spring (6 -> 5); the correct fresh contract is
   conservation (total 8) + unwon + score 0.

## Co-edit note (sibling lanes were live in the same tree)

game.gd was rewritten under this lane mid-session by the B2 event-ring and
B3 network lanes; this lane's wiring was re-verified present in the final
bytes after their rewrites (Title preload line 41, `_exit_tree` line 184,
door branches lines 263-288, KEY_ESCAPE line 614). A live Godot editor
session on the project caused transient hot-reload errors in probe runs;
only the `_buf` error above survived to the close.

## Files

- `roblox_to_godot/scenes/title.gd` - NEW, the whole door.
- `roblox_to_godot/scenes/title.tscn` - NEW, Control root + title.gd.
- `roblox_to_godot/project.godot` - one line: run/main_scene -> title.tscn.
- `roblox_to_godot/scripts/game.gd` - title wiring only (Title preload,
  `_begin_net_probe` door branches, KEY_ESCAPE, `_exit_tree`).
- `roblox_to_godot/b14_harness.gd` - created, run (18/20 PASS twice),
  deleted (run-then-delete law; check list preserved above).
- `watch/inbox/last_mile_20260930/B14_TITLE.md` - this receipt.

## Debts named (not smuggled)

- The AUTHORITATIVE door's endpoint-override bytes remain unproven by run
  until B3 heals `network/net_client.gd` (see blocked checks above).
- Doc drift: `roblox_to_godot/README.md` "Run it" and PLAYER_ONE.md
  section 2 still say F5 drops the stranger straight into the world; F5
  now opens this door first. Those docs are outside this lane's file
  ownership; their owner should refresh the sentence.
- The door is keyboard-only by law (no mouse dependency); a later lane may
  add click-to-select if the estate wants a mouse affordance too.
