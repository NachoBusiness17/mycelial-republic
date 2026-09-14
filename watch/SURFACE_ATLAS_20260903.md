# THE SURFACE ATLAS — all 20 surfaces: structure, backends, origins (2026-09-03, deep crawl)
*Method: in-browser deep crawl (DOM + subresources + fetch/endpoint extraction), full-load
screenshots in watch/design_crawl/deep/, vision-gopher descriptions in _vision_descriptions.md.
Server: the dashboard inside mag-sovereign (routes per surface below; boot via main.py lab).*

## THE HUB
**hypervisor** ("/" — "MAG · マグ · 勾玉"): 1403 elements, 30 links, 4 version-pinned
organs (visual.js?v=tesuji9, board.js?v=hood1, windows.js?v=dashboard-nav-v37,
app.js?v=costtruth4) + /api/probe-status. THE BRIDGE: every version tag is a doctrine era
(tesuji, the hood, the nav-v37 dashboard, cost-truth). The magatama title = the soul-knot.

## THE WIIGNED SURFACES (live API backends)
- **chan** ("/keep/ — Anonymous Science"): 4 endpoints — /api/v1/chan/post, /wake,
  /catalog?n=80, /thread/. THE TAVERN: post/wake/catalog/thread = the BBS grammar.
- **castvoice** (Mag Voice): 6 voice endpoints — stt, handoff, refine, shadow, canvas, turn.
  The voice nervous system is REAL and the most API-wired surface in the fleet.
- **fleet** (Hypervisor · fleet cool/heat + real bills): /api/v1/fleet/hypervisor +
  mermaid CDN. The map and the bills.
- **health**: /api/v1-backed vitals (issues, processes, cadence, liveness, doctor).

## THE SELF-CONTAINED WORLDS (no API wiring yet — the new generation)
- **THE ROOM** (room_lightmap): 19 elements, 0 links — pure render, self-contained.
  The dungeon generation stage: needs the invariant-room feed wired.
- **maze_arena**: 18 elements, 0 links — the falsifier arena, self-contained.
  Needs: outcome logging to a jsonl (the measured experiment), agent-feed from the bay.
- These two are tonight's generation: rendered but not yet tethered to the tape.

## THE STATIC-RENDER ERA (zero-fetch boards)
- **ractor**: 1259 elements, 29,901 chars inline, meta-refresh 20s — the zero-fetch board
  built to survive the wedged webview. The static-render era began tonight.

## THE HERITAGE SURFACES (the older generations, still standing)
- **lattice** ("Conspiracy lattice"), **wave** ("standing wave"): the Aug-era verkle/wave
  projections — the architecture diagrams that became tonight's renders.
- **seat** (256 el: machine health, economy, solved cases), **shell** (the fleet sidebar),
  **table** (26KB: the RPG table), **wearable** ("Swarm HUD"), **agents**, **aos** ("loading
  the bus..."), **feed** (cost efficiency), **cast**/**cast-voice** (the fleet vehicles),
  **control** (green "Route and queue" button = the dispatch surface).

## THE SERVER
The dashboard binds 8765 inside mag-sovereign (docker proxy → container), routes per the
atlas above, static from dashboard/static, boot via main.py lab / mag.boot. Restart tonight:
docker restart mag-sovereign (dropped the wedged keep-alives; healthy).

## THE DESIGN THEORY (from the vision gopher's 20 blind readings)
- THE DARK ROOM with phosphor light: universal across all 20 — the terminal palette is law.
- THE ACCENT PAIR: cyan (cold, deterministic) + gold (warm, the operator's channel).
- PLACES NOT PAGES: the gopher kept calling surfaces rooms/halls/seats — the fleet as a
  navigable keep, not a SaaS grid.
- WHAT THE GOPHER COULDN'T SEE: each surface is a SENSE ORGAN of one organism reading one
  tape — the atlas's real subject is one nervous system with twenty eyes.

## THE GAPS THE CRAWL NAMED (the iterate list)
1. THE ROOM + arena: wire to the tape (event.v1 emission + room-state feed) — the new
   generation joins the nervous system.
2. maze_arena outcome logging (the falsifier data — jsonl per run).
3. The hypervisor's version pins should be generated from the registry (loops_registry),
   not hand-pinned.
4. chan's wake endpoint: the tavern's wake call should feed the bay share (light-to-light).
5. The nav's 19 links match 19 surfaces ✓ — but the nav lacks the API routes (the invisible
   half of the atlas): the endpoint map below is the unseen estate.
