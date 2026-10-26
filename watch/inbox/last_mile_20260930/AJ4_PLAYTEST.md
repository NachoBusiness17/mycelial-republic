# AJ4 — scripted playtest of the Mountain as a GAME (2026-09-30)

Lane: AJ4. Ownership held: `roblox_to_godot/` playtest tweaks + this receipt.
No commit. Throwaway harnesses `aj4_playtest.gd` / `aj4_smoke.gd` created, run,
deleted (X8/W3 idiom); `git status roblox_to_godot/` carries no probe trace
(remaining changes are this lane's four files + pre-existing sibling edits).

## Instrument

Godot 4.3 console exe, `--headless --path roblox_to_godot`. Four scripted
playtest runs (60s each: boil attempts on every pool, valve toggles incl.
tie-cycle, siphon prime -> both inlets -> XOR hold -> siphon break -> junction
STARVED, a FORCED full-bore fracture with the source held open, a win run),
then the AC9 smoke stages. Run 1 taught: headless ignores injected mouse
motion — the shepherd is driven directly (`player.set_process(false)` +
explicit positions), the documented surrogate. Logs: `/tmp/aj4_run{1..4}.log`,
`/tmp/aj4_s{1..5}_*.log`; every number below is from those bytes.

## Designer verdict

1. **Did the destruction READ? It could not — the event channel was blind.**
   All three event-driven layers (water_particles splash/fracture/starve/
   siphon parsing, hud tag popups, juice shake) read count-cursors over
   `last_events`, but game.gd appends AND trims the feed to 6 atomically, so
   from tick 3 the cursor sits at 6 == size 6 forever. Run-1 bytes: 55 ticks
   ran, the fracture physics genuinely burst p_drain (stress 283, reopen
   refused) and ZERO visuals fired — no spray, no rings; the last string any
   parser saw was tick 2's. AD2's entire destruction grammar was dead in every
   real session; its probe passed only because a fresh feed never saturates.
   A second loss stage: `_on_water_tick` sliced events to 3 BEFORE the fan-out
   (run 3: the siphon-break tick carried 4 strings; the break line was sliced
   away though `primed` had unlatched). Both fixed (below). Post-fix READ:
   distinct — fracture = 81 spray droplets arcing toward the recovery pool +
   black crack decal + dead-steel pipe stubs + the FRACTURES line in the feed;
   boil = 3-4 pale droplets rising + ring + <=3px shake + 620Hz blip. Opposite
   directions, opposite geometry. Legible. Caveat (debt): the steam column is
   thin (STEAM_RATE window ~half a tick; 4 alive at probe).
2. **Can a player reach a fracture honestly? NO — dead content on this board.**
   Thresholds: p_bypass 126, p_spring 207, p_terrace 226, p_drain 282, p_out
   292 ticks of full bore; the world holds 8 units, both sinks (waste basin,
   crown) are terminal, so max honest stress observed = 7-8. The playtest
   fracture needed a documented cheat (seed 275 + harness-fed source). The
   destruction tuning (threshold vs board water) is engine-owner territory —
   flagged, not touched.
3. **HUD "what do I do next" in 5s: was a GAP, now guided.** Standing
   mid-board the hint channel went empty (context hints only fire near a pool
   or valve); the CROWN ring gave the goal but never the verb. Fixed with an
   idle guide hint ("walk to X — SPACE boils it up to the Crown", nearest wet
   pool, crown excluded). Verified live.
4. **Win state: legible.** CROWN n/4 ring + "fill it to win" + vignette from
   crown>=3 + win panel + chord + flash. Playtest won at crown 4 with the
   panel visible and the full label intact.
5. **Siphon was structurally unreachable (fixed).** First-in-dict tie-break:
   at gate1 only p_spring could ever toggle; at spring/terrace p_bypass always
   lost its tie — the README-taught siphon (and XOR starvation behind it) was
   dead content. Valve cycling landed; the playtest then walked the whole
   taught chain live: `Siphon p_bypass primes at crest (2).` -> `Junction
   gate1 holds 2 below gate (2 inlets); pooling.` -> `Siphon p_bypass breaks
   (intake dry).` -> `Junction gate1 STARVED: 2 pooled units spilled to waste
   at waste (... boil waste to recover them).` — 12/12 harness checks green.

## What changed (the 3 polish items)

1. **Event channel fix** — game.gd `_push_event`/`_on_water_event`: every
   event string fans out on the graph's declared-but-never-emitted
   `water_event` signal (no pre-slice; the 6-slot feed stays the display
   bound). water_particles/hud/juice drop their blind cursors for the signal
   (hud's innkeeper greeting keeps feed-window rescan BY DESIGN). Files:
   `scripts/game.gd`, `scripts/hud.gd`, `scripts/juice.gd`,
   `systems/water_particles.gd`. Fix comments carry cause+evidence in-file.
2. **Valve tie cycling** — game.gd `_valve_pick`/`_valve_advance` (+2s window,
   <=24px): repeated E at a shared pipe-end cycles the tie set in insertion
   order; the hint names the pipe the NEXT E will hit. Restores p_bypass,
   p_terrace@gate1, p_drain@hollow, p_out@gate1 reachability.
3. **Idle guide hint** — game.gd `_update_hints` fallback + `_nearest_wet_pool`.

## Verification (all on final bytes)

- Playtest run 4: exit 0, 0 ERROR/WARNING lines, 50 events captured, checks
  12/12 (boil, crown_condense, fracture_event, fracture_registry, spray_alive,
  steam_alive, siphon_prime, siphon_break, xor_hold, starved, win,
  idle_guide_hint), reopen-refused held, `won=true`, crown 4/4.
- Smoke (AC9 stages): 60f exit 0 banner-only; 300f exit 0 banner-only;
  T@150 exit 0 (terrain board 25e926f0…, `load_error=''`, visible);
  H@100 exit 0 (`hydrology=true` live flip, brain_fallback=0);
  authoritative (temp users/world log, port 8800, stopped after) exit 0 both
  sides: `mode=AUTHORITATIVE` (welcomes counter was a harness race; mode 1 is
  reachable only through the welcome), 8 tick broadcasts (last n=32), client
  `tick_count=0` (server-sole-mutator held), 0 rejects, server log empty,
  world log 51 rows, listener gone.

## Named debts (not smuggled)

- Steam column density (a boil reads mostly by ring/shake/blip, not the column).
- One-shot alert ring at the fracture point (distinct ember hue) — cheap, next lane.
- Fracture thresholds vs board water: destruction needs an operator/engine-owner
  decision (caps, recirculation, or lower thresholds) to be honestly reachable.
- Server TICK_MS 800 vs client 500 feel parity (pre-existing Z14 debt).
