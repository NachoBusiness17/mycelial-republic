# AA5 — HUD: bars, ring, school panel, mode strip, tag popups (2026-09-30)

Lane: last-mile wave ("the game has all the systems but the HUD is the basic
text from the original slice"). File ownership held:
`roblox_to_godot/scripts/hud.gd` (new) + `roblox_to_godot/scripts/game.gd`
HUD wiring. No commit made by this seat.

## What landed

| Mission feature | Mechanism |
|---|---|
| Water-level bar per pool | Top-left WATER panel, one bar per pool (spring/terrace/gate1/hollow/waste), fill fraction = volume / 8 (the world total, game.gd header), colored by fill: dry amber -> deep blue (water_particles DEEP); waste lerps murky so lost water reads lost. One tick per world unit (the integer graph's granularity). Live volume as text; the wettest pool's name tinted gold (the school gathers there). |
| Crown special ring | The crown is the goal, not a pool: a progress RING (volume / WIN_CROWN 4) in the board's crown-arc grammar — dim track, cyan arc from -PI/2 (game.gd _draw "crown") — plus "CROWN n/4" and a "fill it to win" sub. |
| Fish-counter panel | Top-right SCHOOL panel: total alive (flock scan), tagged count (host.score, gold when > 0), and the innkeeper's LAST greeting IF PRESENT: LW8's bot speaks through the ordinary say channel, so its lines arrive as tick events `innkeeper: <text>` (server/world.py _apply, LW6 grammar). The panel rescans the host's 6-string feed every poll — newest wins, and the greeting drops the moment the feed scrolls it out ("if present", the mission's clause). Two-line deterministic word wrap with an overflow ellipsis. |
| Mode indicator | Top-center strip, two colors, measured and centered via font.get_string_size: SOVEREIGN (teak) / AUTHORITATIVE (amber) / PROBING (gray), then HYDROLOGY ON (cyan) / OFF (gray) — reads game.gd's mode int and graph.hydrology live (H key / MAG_HYDROLOGY boot). |
| Score popup on tag | The score number floats up 26 px over 0.9 s, quadratic alpha fade, gold. Sovereign: the flock's fish_killed signal — game.gd's _on_fish_killed increments score FIRST (connection order: _build_flock connects before _build_hud), so the popup reads the new total, at the fish's last position. Authoritative: the server's `<user> tags a fish at <pool> (score N)` event (game.gd _score_from_event grammar) spawns the popup at the pool with the SERVER's number; the signal path is suppressed there (the local kill is only a sensing proposal) so a tag never double-pops. Other players' tags pop too. |

Carried surfaces: the hint line (20,596) and the event feed (20,620, last 2
joined) keep the old positions; the one-frame hint channel (draw then clear)
is byte-moved from game.gd _update_hud into hud.gd _draw_hint — the only
host state the HUD writes, HUD channel state, never sim state. The win
overlay (ColorRect 0.88 + Label) is byte-moved from game.gd
_build_hud/_crown_filled into hud.gd (same colors, geometry, and string —
em-dash law: nothing re-authored); game.gd calls hud.show_win(score).
Layering preserved: HUD on CanvasLayer layer 1, still under juice's layer-2
win flash (the V4 draw-order law).

game.gd delta: `const Hud` preload, `var hud` replaces the six label/panel
fields, `_build_hud` rewritten (bind-before-add_child, the
water_particles/juice contract), `_update_hud` + `_mk_label` deleted, the
`_update_hud()` call dropped from `_process`, `_crown_filled` ->
`hud.show_win(score)`. Nothing else touched.

## Laws held

- Zero RNG: no RandomNumberGenerator, no randf/randf_range (grep-audited on
  the final bytes; the only "rand" match is the law-statement header).
- CLOCK LAW: every animation is a pure function of host.sim_time — popups
  key t0 off sim_time at spawn and expire by sim_time; a popup freezes with
  the world at the win, frame-replayable. No wall clock anywhere.
- Render-only: reads graph/pools/flock/score/mode/last_events/wettest;
  mutates nothing but the relocated hint_text channel.
- All four features are pure _draw() geometry + draw_string on one Control
  (mouse_filter IGNORE — the shepherd is the mouse).

## Verification (byte-run 2026-09-30, Godot 4.3 console exe)

- Canonical smoke lane, final bytes: `--headless --path roblox_to_godot
  --quit-after {60,300}` -> exit 0, BANNER ONLY, zero errors/warnings, plus
  `MAG_HYDROLOGY=1` at 300f -> exit 0 banner only.
- Probe (throwaway `hud_probe.gd`, V4 run-then-delete idiom, deleted after):
  **17/17 PASS** — mode starts PROBING; sovereign signal popup reads the
  post-increment score; authoritative suppresses the signal path and the
  event path carries the server's number; greeting captured from the feed
  and cleared when scrolled out; hydrology flag read live; win panel visible
  with the score in the label; popups expire by sim_time; wrap 1-line and
  2-line + ellipsis; hint channel cleared after the draw frame; sovereign
  popup path restored after the mode fall.

## Two real defects found and fixed by the byte-runs (fix comments in file)

1. `_wrap2` ternary backwards: `cand = line if line == "" else line + " "
   + w` assigned the EMPTY line on the first word, so no word ever landed
   and every input returned `[""]` (isolated wrap_probe: 79-char input ->
   1 empty line). The empty case must assign `w`.
2. Overflow never marked: words that kept fitting `line` AFTER the second
   line closed were silently discarded with no ellipsis — any non-empty
   leftover past two lines now sets the overflow flag.

## Files

- `roblox_to_godot/scripts/hud.gd` — NEW, the whole HUD surface.
- `roblox_to_godot/scripts/game.gd` — HUD wiring only (preload, field,
  _build_hud, _crown_filled, _process, deletions above).
- `roblox_to_godot/hud_probe.gd` + `wrap_probe.gd` — created, run
  (17/17 PASS + isolation), deleted (run-then-delete law).
- `watch/inbox/last_mile_20260930/AA5_HUD.md` — this receipt.

Debt named: the old hud_score line's "siphon primed/dry" chip has no HUD
home (the board still shows the primed dot at the siphon mid, and
water_particles rings the prime event); folding a siphon chip into the WATER
panel is a later lane's call. The siphon STATE is untouched — display only.
