# INCIDENT DUNGEON — the maze-arena incident as a walkable room (2026-09-07, builder "dungeon", knockout #6)

Built: dashboard/static/incident_dungeon.html — self-contained, house dark style
(#070d0c/#7cf5ff/#e8c96a), error-banner fixture (window.onerror + unhandledrejection),
no build step, no external assets, no network, $0. Serpentine 4-room dungeon on one
canvas: R1 TL -> R2 TR -> R3 BR -> R4 BL -> exit south. Player = the white lantern,
arrows/WASD, click the glowing things, C = curator mode.

## The four rooms (defect = room, inscription = the buggy line, fix = the key)
- ROOM I THE SEAL — the full-height wall defect: inscription
  `walls: [[0.5,0.5,0.03,1.2]] .map(w=>[w[0]*2, w[1]*2.7, ...])`; click the seal ->
  read its scale math (hh 1.2x2.7 = 3.24 > world 2.7 = FULL SEAL) -> CARVE THE GAP
  (1.2 -> 0.28). The seal draws a dashed overhang past the world — geometry sized past
  its domain, made visible.
- ROOM II THE INVERTED BOUNCE — 5 orange dumb agents huddled at spawn pressing INTO the
  west wall (`if(sdf(nx,ny)<0.012){ move }`); answer >= to un-invert; they break out and
  bounce the room properly.
- ROOM III THE UNBOUNDED WORLD — ghosts drift off the left edge and pin as escaped
  (x=-71, -40, -19, -6); answer min (SDF union = min; the outer box is just one more
  primitive: Math.min(d, min(x-0.05, 1.95-x, y-0.05, 2.65-y))); the escaped snap back,
  bounded.
- ROOM IV THE BOGUS FLOOD (boss) — a live 92x48 minimap renders the LYING field
  (radial glow straight through walls — LAW-061: bogus fields look alive); boss asks
  which single character pair was missing from `(ny+0.5)/2.7` -> answer GH -> the honest
  BFS flood refills in visit order (animated), walls respected.

## Corridors = the timeline (plaques on the floor)
08-31 · the maze assembled, defects born -> 09-04 · the arena poses the falsifier ->
09-06 · "maze arena doesn't run" (the forensics). Exit door = THE RUN -> links to
/static/maze_arena.html (walk out or click).

## Curator mode (C)
Real diff hunks overlay: walls [0.50,0.50,0.03,1.20] -> 0.28; bounce <0.012 -> >=0.012;
sdf `return d;` -> `return Math.min(d, Math.min(x-0.05,1.95-x,y-0.05,2.65-y));`;
flood `(ny+0.5)/2.7` -> `(((j/GW)|0)+0.5)/GH*2.7`; post-fix receipt GPS 4/4 avg 315 vs
DUMB 2/4 avg 769-2823 (~10x). Receipt paths printed in the overlay.

## The falsifier
On the 4th solve the restatement panel opens: the player must be able to restate the
four defect classes — SCALE-PAST-WORLD / INVERTED-PREDICATE / UNBOUNDED-DOMAIN /
WRONG-TRANSFORM — that is the incident-dungeon thesis (teaching = the game). Footer
cites every inscription's receipt (CONVO.md row 09-06 ~03:0xZ, fixed arena + both
backups, state/_maze_sim_test.js, MAZE_ARENA_B1 card, orphan scan, model-cartography
card).

## Nav (wiring worker: wire, do not re-verify grammar)
["/static/incident_dungeon.html", "Incident Dungeon"] — additive, after "Maze Arena".

## Verify
node --check on extracted JS (2 script blocks, 20,780B): PASS. curl
http://127.0.0.1:8765/static/incident_dungeon.html -> HTTP 200, 25,142B. Known limits:
desktop-keyboard play assumed (no touch controls); room I interaction is click-only by
design (the seal is the interface); boss minimap is a fresh mini-maze, not the arena's
real wall list — the grammar (BFS + SDF + transforms) is the arena's, ported.
