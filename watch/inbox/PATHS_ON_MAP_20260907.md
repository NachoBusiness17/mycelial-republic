# KNOCK-OUT #7 — PATHS-ON-MAP
**2026-09-07 · builder "paths" · $0, no network, no daemons · spec: watch/SELF_STEAL_MODEL_CARTOGRAPHY_20260906.md (PATHS-ON-MAP, "trajectories are walker PATHS over the field; the envelope is the path log")**

## WHAT LANDED
1. **mag/trajectory_paths.py** — reads the LAST 500 trajectory_step.v1 rows from
   memory/trajectory/steps.jsonl, groups by session_id (the walkers), greps each step's
   command for organ tokens (tesuji/probe/distill→A1 · shadow/refusal/injection→A2 ·
   maze/arena/arrakis/swarm→A3 · lightmap/refeed/feed/rib/cache→A4 · percolator/canon/
   topic/overseer/vision/cite→A5 · gguf/quant/rocinante/studio→A6 · wave/ground→G ·
   chain/salon/riddler/x_interceptor→R), collapses consecutive same-corridor touches
   (the walk, not the noise), caps at 64 legs, colors walkers newest-first from a 15-hue
   palette → dashboard/static/trajectory_paths.json (trajectory_paths.v1).
2. **dashboard/static/tesuji_map.html** — PATHS layer over the corridor grid
   (backup: tesuji_map.html.bak-paths-20260907):
   - each walker's path draws as an SVG colored thread; x = time (left→right),
     y = the touched corridor's measured lane; touch dots (hollow = first, filled = last);
   - newest walker bright (opacity .95, 2.4px), fading with age to (.33, 1.3px);
   - toggle **P** (key or click the tip-line toggle); hover a thread → session id +
     first/last touch (ts + cell) in the existing tooltip; lanes fall back to even
     spacing when the field is empty so walkers stay visible; re-measures on every
     10s poll and on resize;
   - footer stamp: "paths = the walkers' actual traversal · source: trajectory_step.v1 ·
     the envelope made visible" + live walker/point counts.
3. **Nav**: already wired (tesuji_map.html) — no new entry, per spec.

## RECEIPTS (tri-state)
- SUPPORTED — emitter: 1,609 steps read, 500-row window → **11 walkers, 190 path points**
  from 468 raw touches (e.g. sess_b3e32cb1: A4/rib→R/chain→A3/maze→G/ground→A1/tesuji —
  a real walk, readable at a glance).
- SUPPORTED — node --check on extracted inline JS: PASS. curl 200 on
  /static/tesuji_map.html, /static/trajectory_paths.json, /static/tesuji_map.json
  (live dashboard :8000, served copy confirmed carrying the layer).
- UNPROVEN — visual render in a real browser (no GUI in this window; hover/toggle
  logic is exercised by code, not by an eyeball). First human look = the falsifier.

## FALSIFIER (inherited from LAW-060/061)
If the threads disagree with what the sessions actually did, the organ→corridor mapping
is lying — the mapping is declared in one list at the top of trajectory_paths.py and is
trivially auditable. Unvalidated-mapping paths steer exploration, never commitments.
