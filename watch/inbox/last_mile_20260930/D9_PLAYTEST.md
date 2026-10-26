# D9 PLAYTEST — full fresh run after tonight's landings (2026-09-30)

Lane: D9 (last_mile wave). Ownership: `roblox_to_godot/` playtest + this
receipt. No commit made by this seat (a sibling tree sweep may have carried
working-tree bytes to history mid-session, the B2 pattern; the throwaway
harnesses below were created-run-DELETED and any swept copies of them are
dead instruments, not shipped code).

## Instrument

Godot 4.3 console exe (`tools/godot/`), `--headless --path roblox_to_godot
-s <harness.gd>` (SceneTree mode, AC9 idiom). Four throwaway harnesses
(d9a v2 sovereign game, d9b authoritative, d9c fed-source destruction,
d9h probes), all deleted after their runs; check lists preserved below.
Shepherd driven by direct positions (headless ignores injected mouse
motion; AJ4 run-1 law); keys via real `Input.parse_input_event`. Server:
`-m server.server --port 8890` with temp users file (ada/steam) + temp
world log. Wall-clock ms numbers are the HARNESS's pacing instrument.
Logs: /tmp/d9a.log, /tmp/d9a2.log, /tmp/d9b.log, /tmp/d9c.log.

## HEADLINE DEFECT FOUND AND FIXED: the committed game did not boot

First run through the title door died: `scripts/game.gd` (committed in
0b846c01f) references `Title.DOOR_SOVEREIGN`/`Title.DOOR_AUTHORITATIVE`
while `scenes/title.gd` still declared `MODE_*` — parse error, Main loaded
as a scriptless Node2D, `g.mode` access failed. A half-done rename: the
same commit's `systems/game_constants.gd` documents "title.gd's DOOR_*",
so the rename intent was real but title.gd's side never landed. B2's
warning proved exactly right: the plain `--quit-after` smoke stays
banner-only through a script parse error (verified again: smoke was green
while the game was dead).

**Fix 1** (`scenes/title.gd`): constants renamed MODE_* -> DOOR_* (3
declarations + 3 internal uses), fix comment carries cause+evidence; grep
showed no other consumer of the old names (tests pin neither). A sibling
lane (V5 river entrance) landed the remaining internal renames in the
same window; final bytes coherent, verified by run (D9F 4/4) and by the
full playtest below. NOTE: every B14/B2-era "verified" receipt for the
door predates 0b846c01f; this fresh boot re-earned them.

## Playtest A — sovereign full game (23/24; the 1 FAIL is instrument math)

Boot -> title -> ENTER -> SOVEREIGN now (mode=2, no NetClient, world 8
units). Sequence and numbers, all from executed runs:

- Natural drain: spring 6 + hollow 2 -> waste 8, complete at **tick 9,
  last state change at 3.97s**; 26 events then the world is silent.
- Siphon chain live (fresh re-enter, E-cycle at spring opens p_bypass —
  AJ4's fix verified again): `Siphon p_bypass primes`, 36 events,
  conserved 8/8.
- 60s untouched post-settle: **max pipe stress 8 (p_drain) vs the 200-400
  burst window — the fracture is NOT reachable in normal play on the
  default board.** Analytic bound agrees: 8 units, both sinks terminal,
  no recirculation back uphill (boil only moves water pool->crown), so
  total honest throughput through any pipe <= 8 volume. B1's law made
  fractures ENGINE-reachable (fed source bursts at exactly threshold+1:
  p_out 211/210, p_spring 237/236 — phase C bytes), but the board holds
  200x too little water; B1's own "board owner's lever" note stands. The
  mission's parenthetical ("should be reachable now at 211-336 ticks")
  is TRUE of the engine and FALSE of the default board.
- Hints (read via direct `_update_hints()` call — hud's one-frame
  draw-then-clear channel makes any frame-later read "" by design, D9H2
  probe): mid-board guide "walk to waste — SPACE boils it up to the
  Crown"; at-waste "SPACE — boil 1 unit at waste (it will condense at
  the Crown)". Both legible and correct.
- Valve cycling at the shared gate1 dot: p_spring -> p_terrace -> p_out
  -> p_spring. Works.
- **Win: 4 SPACE presses at waste -> crown 4/4, won=true, win panel
  visible, 159ms** from first press (one 0.5s tick to condense). The
  world then FREEZES (ticks 65 -> 65 measured) — R restarts fresh, ESC
  returns to a fresh title (sel=0, field persists), re-enter re-inits
  clean (8 units, unwon).
- Fish: tired/gold fish appear (276 gold-frames in 15s), tags land (10
  scored in a 5s deliberate chase; the catch window is real). H toggles
  the head law, T loads the St Helens terrain board.
- (v1-run bonus finding, later reproduced deliberately: a naive "boil
  whenever the hint says" loop wins in ~31s with zero understanding.)

## Playtest B — authoritative door, host field, netcode (13/15; both FAILs instrument artifacts, laws hold)

Server live on 8890. Title -> DOWN -> BACKSPACE x4 -> type "8890" ->
ENTER: **the host field works end to end** — welcome via the field's
endpoint (port 8890, not the compiled 8800), mode=AUTHORITATIVE. Played
to a **win over the wire** (4 boils, crown 4, won=true; server is sole
mutator). B3 interpolation laws, read off the live client:

- `rubber_band_frames=0`, `max_truth_error=0.0` across the whole session.
- Interpolated rendering REAL: per-frame samples of waste during a boil
  transition ramp 6.12136973 -> 6.03587 -> ... -> 6 (fractions between
  integer truths; the "frac_frames=0" FAIL was my lambda capturing the
  counter by value — GDScript capture law, the samples array is the
  truth).
- Buffer grew monotonically 1 -> 23 in a 22s probe window (the "buffered
  7 != 32" FAIL was a short session still filling the 32 ring, not a
  leak; newest_n monotone, cursor == newest).
- ESC from authoritative returns cleanly to the title; the typed field
  survives the walk ("127.0.0.1:8890").
- Rooms (B15) live-probed: hello default -> room "summit"; explicit
  "basecamp" born at hello; malformed id -> BAD_ROOM. (Client hello
  carries no room — default-room path is what players get today.)
- Server-side noise worth a line: verdict_feed logs "world verb 'say'
  has no mud mapping" every 8 ticks (fail-open by design, log spam).

## Playtest C — destruction visibility (12/13; the 1 FAIL is the same lambda artifact)

Fed-source instrument (documented cheat, AJ4/B1 lineage: inject spring
volume, drive the game's own `_on_water_tick`): **p_out burst at tick
211, p_spring at 237 — byte-exact on B1's table.** The event ring held
both `FRACTURES` lines at read time; ring held 64 with `event_dropped`
833 (the HUD's "+N dropped" tally surface); the particles fracture
registry parsed both pipes (spray budgets armed: 0.28/0.73) — the broken-
stub rendering source is live. Burst pipes refuse reopen through both
`open_pipe()` and the E verb; volume conserved through both bursts
(466 = 8 + 458 fed). **All destruction reads.** Found en route: the E
verb on a burst pipe emitted "You open p_out." while the pipe stayed
shut — the feed asserting an action that never happened.

**Fix 2** (`scripts/game.gd` `_try_valve`): a fractured pipe's E press
now emits "You try X: it FRACTURED — it stays shut forever." + a hint
line; verified by run (D9F: truthful=true, lying=false, pipe stays shut).

Fix budget: 2 of 3 used; the third withheld — the remaining pain is
board design (below), not a code defect, and B1 explicitly reserves that
lever for the board owner.

## Post-fix verification

- `pytest tests/test_event_ring.py tests/test_motion_rows.py
  tests/test_flock_positive.py tests/test_mountain_units.py
  tests/test_netcode_v0.py` -> **102 passed** (both fixes ride all
  pinned laws).
- Boot smoke through the door: D9F 4/4 PASS.

## Designer verdict — is it FUN for 10 minutes? NO. Charming for ~2.

The first 60 seconds are genuinely good: a clean door, a legible card,
water visibly running downhill, hints that walk you to the verb, a
satisfying win panel with count-up. The 10-minute question fails on
arithmetic, not polish:

1. The puzzle has ONE solution (lift 4 of 8 units to the crown) and no
   failure state: waste is a boilable basin (V5), so nothing is ever
   lost — the header's "every unit you let reach Waste is a unit you
   must boil twice as hard" is no longer true, and the whole drain/valve
   machinery is optional scenery on the beeline win.
2. **First boring moment: ~5 seconds in.** The drain spectacle completes
   at tick 9 (last state change 3.97s); from then the board is a static
   diagram whose only remaining tension is walk speed — the hint
   literally says "walk to waste, SPACE". A knowing player wins ~10s
   after the door; a reading stranger in about a minute.
3. What remains: the fish-tag chase (fun for a few minutes, uncoupled
   from the puzzle — score only decorates the win panel), the T terrain
   board (the biggest remaining toy), H (near-invisible on this board).
4. The one dramatic system tonight's wave perfected — pipe destruction —
   never happens for a real player (max honest stress 8 vs 200+). The
   spectacle the engine can now guarantee is exactly the content the
   board cannot reach.

## Named debts (not smuggled)

- **Board-side fracture lever (operator decision, third fix withheld on
  purpose):** source feed, recirculation, or crown-overflow-back — any of
  the B1-named levers. Until then destruction is dead content in normal
  play; recommend the operator pick one lever next wave.
- No-loss economy: the "twice as hard" threat text (game.gd header +
  README/PLAYER_ONE phrasing) is stale under V5; an economy tension
  decision (operator), not a playtest edit.
- Post-win freeze: the world stops ticking on win; R/ESC are the only
  exits (by design, but a "keep playing" door would stretch sessions).
- Server TICK_MS 800 vs client 500 feel parity (pre-existing Z14 debt,
  felt live: authoritative boils land noticeably slower than sovereign).
- verdict_feed say-mapping log spam every 8 ticks (fail-open, noisy).
- Fish score uncoupled from the win goal (design gap worth a lane).
