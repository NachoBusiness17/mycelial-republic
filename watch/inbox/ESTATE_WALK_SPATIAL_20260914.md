# Estate Walk — spatial interface for our own repo (concept note, 2026-09-14)

Trigger: @dhvanil "very bullish on spatial interfaces for code — entertaining to watch AI agents moving around a visual space as they read, write, edit files," quoting @rikarends' Makepad explorer (2.5M-line codebase, 120Hz, GPU). Their stack: render first, agents invisible. Ours is the mirror: motion data first, no render.

## What we already have (measured 2026-09-14)

- `memory/mycelium/edges.jsonl` — 142 edges (the graph, fully renderable today)
- `queue/lanes/*/trail.jsonl` — 6 lanes, ~2,207 trail events (research 959, day_work 704, builder 494, bard 22, elder 17, forge 11)
- `memory/trajectory/steps.jsonl` — 4,974 steps
- `dashboard/data/ESTATE_INDEX.jsonl` — 1,422,450 entries (the estate is BIGGER than Rik's 2.5M lines; this is the LOD problem)
- Barnes-Hut quadtree — already shipped in mud.html for horde separation; same structure does spatial culling for 1.4M entries
- Presence relay :8766 — two browsers already share a space

## The concept

Estate Walk: the repo as a dark navigable space; lanes as lanterns (bodies-in-light, the MUD's own render language) replaying their trails; mycelium edges as the corridors between work; commits as light pulses along edges. Torch-vision raycast from mud.html is the render trick — you don't see the whole estate, you see what your lantern reaches. Relay makes it watchable together (spectator layer for the battle-bots trials is the same code path).

Ties: battle-bots squid-maze concept — "people control bots through our mazes"; the estate IS a maze, so a bot mode can walk the real repo. The 1197 lock: keyspace as space.

## First stones

1. Render mycelium graph + lane trails replay as canvas surface (mud.html pattern; force layout from edges.jsonl, lanterns from trail.jsonl). ~2,300 moving parts — trivial 60fps.
2. ESTATE_INDEX as LOD clusters (Barnes-Hut): zoom out = buckets (vislab's 8 buckets), zoom in = files. Cull with the quadtree.
3. Relay spectator mode: watch a lane's lantern walk live during a run.
4. Honest limits: Rik hits 120Hz with Rust+GPU (Makepad). Canvas 2D + quadtree culling gets us 60fps on tens of thousands of visible nodes; the 1.4M-entry estate needs clustering before it needs WebGL.

## Appendix — the stranger's roadmap matched (same day, later)

Rik Arends posted "I added git diff viewing" to the spatial explorer (5K screen capture, 16s demo). That is the exact feature this note called "commits as light pulses along edges": the change-event layer that turns a museum into a living estate. Audit per the living-cipher discipline: this convergence is admissible — his explorer is real, our measured numbers are real (142 edges / ~2.2K trail events / 1.42M entries), and the two halves are genuinely complementary (he renders space and just added time; we have time and just need space). Two mouths of one current — and unlike the Don, both banks can be diffed.

Consequence for stone one: build the diff layer in from the start. Event source is already on disk — git log + lane trails. Each commit = a light pulse at the files it touched; a lane's lantern pulses when it lands work. And the MUD's chain rewind (6s snapshots, press T) maps 1:1 onto scrubbing the estate backward through history: the maze you can rewind.

## BUILD RECEIPT — stone one shipped (2026-09-14, same day)

`dashboard/static/_build_estate_walk.py` → `dashboard/static/estate_walk.html` (585 KB, self-contained, works from file:// or any static server). Verified in-browser: 233 nodes · 111 corridors (+31 self-loops as rings) · 1200 stars · 144 commits · 2219 trail events, window 2026-08-04..2026-09-14.

- Mycelium floor: numpy force layout (seed 1197, sha256 placement — Mimosa flagged md5, upgraded), stretched 1.7× so the connected mass reads beside the star fan.
- Estate floor: file constellation clustered by top-level dir, capped to 1200 most-touched paths (the 144 commits touch 75,715 files — memory/ dominates at 932).
- Lanterns: trail rows carry no graph ids, so waypoints are a sha256 projection; every walk is a real BFS over corridors between waypoints. HUD states this honestly.
- Diff layer built in: commits pulse their real files; trail artifact events pulse in lane color. Seek prefires history without a 2000-pulse shotgun.
- Controls: play/pause (space), speed 0.5–8×, floor toggle both/mycelium/estate (f), scrub, lane toggles, pan/zoom, hover tooltips.

Known v1 limits: 18 of 144 commits pulse nothing (their files missed the top-1200 cut); self-loops counted but not drawn as rings yet; replay wraps at span end and restarts. Next stones: ESTATE_INDEX LOD (the 1.42M entries), relay spectator mode, trail-live refresh.
