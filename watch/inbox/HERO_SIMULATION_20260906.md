# HERO SIMULATION — the salon falsifier, BASELINE run
**2026-09-06/07 · builder "hero" · falsifier: `python mag/hero_simulation.py` · receipt: `state/hero_simulation.json` · $0, no network, no daemons**

The orphans_astra salon's exit condition (memory/runs/salons/orphans_astra_20260906/SALON_ARTIFACT.md):
a fresh agent reaches every LOOT from a declared path and never reaches a GRAVE. The
six-destination re-home is not built yet, so this run simulates the walk against the CURRENT
nav wall (dashboard/static/nav.js, 80 tabs, 73 rendered entry pages) — the falsifier's first
honest reading.

## VERDICT: **FAIL** (expected — this IS the baseline reading)

| | reached | detail |
|---|---|---|
| LOOT | **0/5** | every declared path exists + loads (cards 37/37); zero have nav/link reach |
| GRAVE | **0/2** | room_game sealed in attic, zero followable links anywhere served; MEMORY.md authority unserved, unlinked — both clean |

## THE BREAKS (what the fresh agent cannot reach)
1. **b7_spectral_spec** — tier=cite: `dashboard/static/spectral_maze.html` renders the card
   path as TEXT ("card: watch/SELF_STEAL_LIGHT_MAZE_SPECTRAL_20260906.md") but nothing links it.
2. **session_maze_module** — tier=cite: memory_map.html renders the module node (via
   memory_graph_data.js); text only, no link.
3. **maze_keeper_pack** (`watch/maze_world/`) — tier=none: zero surface presence. Note: the
   "pack" currently IS one Modelfile (2.2KB) — before re-homing, the stripped prompts/laws
   the verdict promised should actually be filed into the pack.
4. **assembled_maze_0831** (`memory/graph/session_maze.json`) — tier=none: the RQ1 assembled
   arm has zero presence on any served surface.
5. **cards_37** — tier=none: 0 of 37 referenced by any nav entry or followable link.

## LIVE-FLEET DRIFT (observed during the build)
`research/orphan_registry/today_dogfood.md` §3 was amended mid-build: all 37 lines now carry
`— LINKED via cell R/linked/... #hash`. A concurrent seat's re-link pass is landing the
TESUJI LEDGER edges the salon demanded. Ledger linkage ≠ interface reachability: the
simulation measures the second and still fails. Both are required; only one is done.

## WHAT THE RE-HOME MUST CHANGE TO PASS
- **Library** must link the 37 cards (e.g. render the §3 registry or a topic_index-backed
  cards index with real hrefs) — tier must become nav/link, cite does not count.
- **Projects/History** must link `memory/graph/session_maze.json` + `mag/session_maze.py`
  as the RQ1 assembled arm + probe instrument.
- **Library** must expose `watch/maze_world/` (after the pack is actually filled).
- **B7 + session_maze**: upgrade the existing citations to followable links (the surface
  text already names both paths — wire, don't rewrite).
- **GRAVEs stay dead**: room_game remains attic-sealed with zero links (farewell citations
  like maze_arena.html's "ported from room_game.html on its retirement" are legal per the
  verdict); MEMORY.md's phantom authority stays off the nav — rebuild the live index from
  resolvable paths only.
- Acceptance: `python mag/hero_simulation.py` exits 0 (verdict PASS) after the re-home lands.
