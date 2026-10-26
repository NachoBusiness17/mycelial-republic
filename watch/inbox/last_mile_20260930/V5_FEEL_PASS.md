# V5 — FEEL PASS (juice tiers, victory sequence, per-event audio, title entrance)

Operator ask: "the game works, now make it FEEL great ... this is the pitch a
stranger FEELS in the first 10 seconds." File ownership: `roblox_to_godot/`
feel/polish edits. Predecessor: V4_JUICE.md (shake/flash/chord/vignette).

## What changed

1. **Shake tiered by severity (fracture > boil > gate)** — `scripts/juice.gd`.
   V4's one-size shake (3 px / 10 frames) became a ladder: gate (junction
   passes/sill) 1.2 px / 6 f, STARVED 2.2 px / 8 f, boil 3.0 px / 10 f (V4
   bytes kept), siphon break rides the boil tier, fracture 7 px / 22 f.
   Routing off the existing `water_event` signal grammars (zero new sim
   surface); direction still hash -> sine-table, zero RNG.
2. **Victory sequence** — juice.gd layer-2 canvas + hud.gd. On `won`: the
   water rises (waved flood line climbs to y 430 over 3 s, cubic ease-out,
   then laps forever), the screen warms (amber wash -> 0.17 alpha over 1.4 s
   over the dark win panel), a "SUMMIT" banner drops in (ease-out-back
   overshoot, 68 px, growing underline), and the win label's score COUNTS UP
   0 -> N over 1.2 s (`hud.gd`, own post-win delta accumulator — the juice.gd
   CLOCK LAW receipt, hud edition; game.gd freezes sim_time at the win).
   Win-panel string stays byte-moved (em-dash law).
3. **Procedural audio per event type** — juice.gd. Boil: 0.5 s differentiated
   hash-noise HISS. Fracture: LOW CRACK (150->36 Hz sweep summed with a
   120 ms grit burst, one pass so they land together). Gate: soft 392 Hz
   tick. STARVED: descending 220->70 Hz "denied" womp. Win chord unchanged.
   All zero-click (sin envelope), deterministic (hash(i), no RNG), queue-cap
   law holds; headless stays silent-never-error.
4. **Title entrance** — `scenes/title.gd`. A river band flows in behind the
   name from the left over 1.4 s (leading edge cubic ease-out, chop ramps
   toward the pour front, splash droplets on sine phases while travelling),
   then the surface keeps lapping. Pure geometry + `sin(_time)`; CLOCK LAW
   and zero RNG hold.

## Concurrent-lane note (R7)

Mid-run, sibling lanes were landing R7 (game constants) and R8 (int-domain
water graph) in the same tree. game.gd came to reference `Title.DOOR_*`
statics before title.gd carried them (parse-broken window, byte-observed);
R7's own comment in game.gd declares the rename intent ("title.gd's door
lanes renamed DOOR_* — not game.gd's Mode enum"). title.gd is this lane's
file, so this lane completed it: MODE_UNCHOSEN/SOVEREIGN/AUTHORITATIVE ->
DOOR_* (values unchanged). No other title.gd semantics touched.

## Verification (byte-run 2026-09-30, Godot 4.3 console exe)

- Probe (`v5_probe.gd`, v4 run-then-delete idiom, deleted after): **22/22
  PASS, exit 0** — all four shake tiers fire with their amp/frames and decay
  to the pinned center; hiss/sweep/crack built at mix rate, first sample
  exactly 0, last inside the envelope sliver, crack peak bounded, queue cap
  1.0 s; count-up starts 0, reaches 9 (unit) and 7 (real path: crown 4 ->
  tick -> `_crown_filled`), string byte-identical, holds; post-win
  accumulator runs past frozen sim_time; flood climb settles past its 3.3 s
  window; title entrance clock crosses 1.6 s. (Probe fix noted: SHAKE tiers
  are Vector2 = float32 storage — 1.2 reads back 1.200000047 — so tier
  asserts use is_equal_approx.)
- Smoke, canonical lane command from repo root: `--headless --path
  roblox_to_godot --quit-after {60,300,900}` -> exit 0, BANNER ONLY, zero
  errors, zero warnings (all three, plus `MAG_HYDROLOGY=1` at 300f).
- Ran against the sibling-modified tree (game_constants/water_graph R8/
  net_client edits in place at smoke time) — green on the merged state.

## Files

- `roblox_to_godot/scripts/juice.gd` — tiers, voices, victory sequence.
- `roblox_to_godot/scripts/hud.gd` — win score count-up + its clock receipt.
- `roblox_to_godot/scenes/title.gd` — entrance river + the R7 DOOR_* rename
  completion.
- `roblox_to_godot/v5_probe.gd` — created, run (22/22 PASS), deleted.
- `watch/inbox/last_mile_20260930/V5_FEEL_PASS.md` — this receipt.

## Feel verdict

Ten seconds in, a stranger now feels: a river pouring in behind the title;
every verb answering through the fingers (tick / hiss / womp / crack, each
with its own weight) and the screen agreeing (1 px settle vs 7 px burst);
and a win that arrives as a moment, not a label — water climbing, light
warming, SUMMIT dropping, the score ticking up. No dead air anywhere in the first
verbs.
