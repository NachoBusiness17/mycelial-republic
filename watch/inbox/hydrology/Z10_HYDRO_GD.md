# Z10 HYDRO_GD — graded head ported to the Godot client (2026-09-29/30)

Lane Z10 of the hydrology wave. Spec: `watch/inbox/water_engineering_20260930/WF_SYNTHESIS.md`
rung 1 (client half); engine truth: `mag/hydrology.py` (X1). No commit (operator's push).

## What landed (files owned this lane)
- `roblox_to_godot/systems/water_graph.gd` — ADDITIVE hydrology mode:
  - `HydroNode extends WNode`: `cross_section` (default 1000, `assert >= 1` —
    Python's ValueError mirrored with add_pipe's assert idiom), computed
    `depth = volume * 1000 / cross_section` (milli-depth), `head = elev * 256 + depth` (Q8).
    Every node is a HydroNode; the boolean law never reads the geometry, so its
    behavior is unchanged (the water_graph.py regression-suite role survives).
  - `hydrology: bool` flag + `conductance: int = 8` on the graph.
  - `_pipe_flow` (new): mirrors `mag/hydrology.py _pipe_flow` line for line —
    siphons prime at crest under positive dHead then run full bore; plain pipes
    flow `mini(cap, mini(src.volume, (dHead * conductance) >> 8))`; `dHead <= 0`
    = nothing moves (check valve). GDScript `mini()` is 2-arg (Python `min` is
    variadic) — nested calls, same min of three, commented at the site.
  - `_available` / `_move`: `hydrology` branch delegates to `_pipe_flow`
    (mirrors the Python overrides incl. the siphon-prime latch and identical
    event grammar, so water_particles splash parsing does not branch); the
    boolean bodies below each branch are byte-unchanged.
  - `to_dict()` nodes carry `cross_section`/`depth`/`head` (hydrology.v1
    node-dict parity; the X1 "depth-tint reads node.depth" hook). Old keys
    untouched; game.gd's pipe-dict consumers unaffected.
- `roblox_to_godot/scripts/game.gd` — hook only: `MAG_HYDROLOGY=1|true` env sets
  the boot mode (headless smoke lane); `H` key calls `_toggle_head_law()`
  (flips `graph.hydrology` live, hint pinned 120 frames); HUD score line shows
  `law boolean|hydrology`. Header documents the Z10 law.

## Honest scope note
On this board (all pipes cap 1, cross_sections default) the graded law saturates
at cap, so both modes produce identical integer flows in play; the law
difference is proven on a cap-100 scratch graph (below) and the geometry
(depth/head) is now exposed for render rungs. Backwater/equalization needs
cross-section wiring on the board or cap > 1 to show visibly — next rung's call,
not smuggled in here.

## Verification (byte-run, Godot 4.3 console exe, current tree)
- Canonical smoke, boolean: `--headless --path roblox_to_godot --quit-after 60`
  -> exit 0, 0 errors/warnings.
- Canonical smoke, hydrology: same + `MAG_HYDROLOGY=1` -> exit 0, 0 errors/warnings.
  (400-frame hydrology rerun earlier in the lane: exit 0, 0 errors.)
- Instrumented pass (throwaway `-s` SceneTree script, run then deleted): on a
  standalone graph, elev 10 vs 0, cs 1000, src vol 100, cap 100 -> depth=100,
  head=2660, dHead=2660, graded flow `(2660*8)>>8 = 83` vs boolean 100 (exact
  mag/hydrology.py values); cs 500 -> depth 200 / head 712; backwater: dst
  raised to head 2700 -> graded 0 (never uphill) while boolean still 100;
  `to_dict` carries all three geometry keys; live board ticked one tick per
  mode, 4 events each, shared grammar; water_particles alive 220/220 droplets
  at frame 60 (renders; only headless-verified as live-step, not pixels).
- One parse bug caught and fixed by the smoke itself: 3-arg `mini()` is
  invalid GDScript (first run failed compile, cascade of Nil errors) — nested
  2-arg `mini` with a comment naming the cause.

## Sibling-lane races (byte-witnessed, not mine)
- A sibling lane landed Z3 terrain (`terrain_loader.gd`, `T` key), brain_trail,
  and probe scripts in `game.gd`/`roblox_to_godot/` DURING this lane's runs.
  One transient parse error (`_brain_trail_ok` call before its definition was
  written) raced one probe; gone on the next run. My Z10 surface verified intact
  on the post-landing tree (md5-stable across the final runs).
- The estate world server (or a sibling's) listens on 127.0.0.1:8800; with it
  reachable, every quit shows one NetClient teardown error
  (`net_socket_posix get_available_bytes !is_open`) — identical both modes,
  net code untouched by this lane. Rerun both modes with
  `MOUNTAIN_SERVER=127.0.0.1:9` (dead port, quiet refuse): exit 0, 0 errors
  both modes. Attribution: the live listener, not the hydrology port.
- A `git stash` attribution attempt bounced off a sibling's `index.lock`; no
  stash was created, working tree kept all Z10 edits (grep-verified), foreign
  pre-existing stash entries untouched.

## Next rung hooks
Board cross_sections + cap > 1 to make grading visible in play; depth-tint in
`_draw` off `to_dict()["nodes"][n]["depth"]`; water_particles `_active_flows`
still recomputes the boolean law client-side (read-only, correct on this cap-1
board; a pure `probe_flow` helper is the future fix if boards grow cap).
