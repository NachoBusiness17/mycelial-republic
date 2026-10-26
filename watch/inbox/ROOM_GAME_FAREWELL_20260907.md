# FAREWELL — room_game.html (retired per orphan-salon verdict, 2026-09-07)
**Verdict: GRAVE — unanimous (groq, cerebras, openrouter, df6 audit; Astra concurred: "retire the
fork that reintroduces three fixed defects; cite that regression as its farewell").**

## THE REGRESSION IT CARRIES (why the farewell cites it)
The fork was frozen before the 09-06 fixes and reintroduces three birth defects the current
maze_arena.html healed:
1. **The sealed chamber** — center wall half-height 1.2 scaled to 3.24 in a 2.7-tall world:
   spawn chamber sealed from the cheese; walkers freeze.
2. **The wall-blind flood** — BFS y-transform `(ny+0.5)/2.7` instead of `/GH*2.7`: the lightmap
   has never respected walls in this fork's lineage.
3. **The unbounded world + inverted bounce** — dumb agents escape to negative coordinates.
Plus a dead organ: POSTs to /static/lantern_priority.json (404) every 30s, response discarded —
its field-vs-bounce falsifier reads wrong by construction.

## THE DISPOSITION
- Removed from nav.js (the mesh executed the salon verdict; file preserved at
  dashboard/static/room_game.html as forensic evidence — NOT deleted).
- If any future builder wants a second maze fork: start from maze_arena.html (the fixed form)
  and diff, never from this file. The fork is a teaching exhibit about forking.
- Cited in the orphan registry (watch/SELF_STEAL_ORPHANS_20260906.md) and the salon artifact
  (memory/runs/salons/orphans_astra_20260906/SALON_ARTIFACT.md).
