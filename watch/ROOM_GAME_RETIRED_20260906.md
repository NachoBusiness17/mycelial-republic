# ROOM_GAME RETIRED — 2026-09-06 (operator GO)

**Card:** room_game.html merge + retire · **Seat:** zcode Worker B "surface-fix" · **Date:** 2026-09-06
**Authority:** operator GO x4 (2026-09-06 ~11:2xZ CONVO row: "room_game removal" named in the 3-wide fan) + night 67-surface audit finding: stale fork re-teaching FIXED birth defects.

## What room_game.html was
A 09-02 fork of the arena that predated three maze_arena fixes. It kept teaching the birth
defects maze_arena had already healed:
- **unbounded world** — its `sdf()` had no outer-wall clamp (agents and player could walk the void past the room edge),
- **inverted dumb-agent bounce** — `if(sdf(nx,ny)<0.012){ this.x=nx; this.y=ny; }` moved agents INTO walls on collision,
- **flood y-transform /2.7** — lightmap row lookup used the raw `2.7` constant instead of `GH` (the exact duplicate-const class of bug fixed in arrakis),
- no error banner, no B1 shadow-field renderer, no FIELD toggle, worse GPS agent (single-ray gradient read, wall-wiggle on death).

## What was salvaged (ported into maze_arena.html, backed up first)
The fork's ONE unique asset: the **v1 THE PLAYER layer** —
- the white **lantern** (arrows/WASD, SDF-collision movement),
- six **LAW_SHARDS** (THE TAPE VERIFIES · SUBSTANCE GATE · THE PATIENCE LAW · THE MICKEY LAW · FILES ARE THE BODY · KEY LAW) with pickup flash lines,
- **the red assumption** (dragon) that wakes when you stray near and hunts in the dark,
- the lantern player drawn over the field render (frame wrapper pattern).

Ported onto the FIXED field: the player now inherits the bounded world and honest collision,
and the layer coexists with the B1 ray-field renderer (player draws after every field mode).

**Dropped in the port, on the record:** the 30s `POST /static/lantern_priority.json` beacon
("the lit quadrant steers the bay") — repo-wide search finds NO lantern_priority organ, file,
or consumer anywhere; it was a dead no-op POST, so porting it would have been faking function.
If the bay-marker organ is ever built, rebuild the beacon with it, named.

## Why retired
One build, two names, divergent truths: the fork kept teaching defects the canon had fixed.
SACRED COWS, NOT LEGACY SHIT — bones stolen (player layer), reinterpretation named (this card),
draft retired. The arena lives on at `/static/maze_arena.html` (nav: "Maze Arena").

## Disposition
- `dashboard/static/room_game.html` → `dashboard/static/attic/room_game.html.retired`
- nav.js entry removed (backup: `nav.js.bak-surface`)
- Backups: `room_game.html.bak-merge`, `maze_arena.html.bak-merge` (pre-merge state of both)
- No .jsonl chain ledger touched.
- Verified: maze_arena.html serves 200 on :8765, merged JS parses clean (node --check).
