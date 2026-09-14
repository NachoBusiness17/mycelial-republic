# WOW SURFACE INVENTORY — it already exists; one frame is empty (2026-09-11, lane 3)

Entry: dashboard/static/viz_gallery.html (4,363 B) — 12 tabs, 13 buttons (tab id 'horse' registered twice, both loading viz_horse_run.html).

| Exhibit (file) | Renders | Data source | Live/Static | One-line upgrade |
|---|---|---|---|---|
| 3D Verkle (viz_3d_verkle.html) | 260 knots on 3D golden-angle helix, three.js, hover reads tension/dirichlet/Q/residual | game_verkle_knots.js (baked) BUT polls 127.0.0.1:8765/api/v1/local-pulse every 2s — wave freq/breathing is live CPU | HYBRID | re-fetch knots from a /api/v1/verkle-knots endpoint so new chain knots append to the helix |
| Knot Wave 2D (verkle_knot_wave.html) | same 260 knots as 2D canvas spiral, residual glow, hover readout | game_verkle_knots.js only | STATIC | add the same local-pulse + knots fetch loop as its 3D twin |
| The Swarm (game.html) | swarm arena; verkle knots are collectible loot | knots baked in-page + live fetch 127.0.0.1:8799/api/saelis?q= | HYBRID | feed fleet radio/telemetry events in as swarm spawns |
| Spore fish (viz_spore_fish.html) | 10k-point closed-form fish — 'beautiful, wrong' | none (pure math) | STATIC (art) | none — kept as the honest record |
| Horse carcass (viz_horse_lane2_carcass.html) | stick-figure gallop, flash-lane wrong turn | none | STATIC (art) | none — kept as record |
| The Horse running (viz_horse_run.html) | 10k-point cloud horse: spine flex, 4-leg kinematics, mane/tail lag | none (pure math) | STATIC (art) | drive stride cadence from lane pulses |
| The Armory (steal_tools.html) | 116 steal tools as searchable wall | steal_tools_data.js (from mag/steal_tools.py) | STATIC | fetch new steals from rest.py endpoint on load |
| Memory Map (memory_map.html) | 1,572-node KG browser | memory_graph_data.js (from memory/knowledge_graph.json) | STATIC | serve KG JSON live from mag/knowledge_graph.py |
| Module Map (module_map.html) | 694 mag modules + docstrings, tier chips | module_map_data.js (from mag/_gen_module_map.py) | STATIC | regenerate on server start |
| Grab & Write (grab_write.html) | Tesuji doctrine essay | none | STATIC (text) | none — it IS the doctrine |
| Law Lattice (viz_lattice_test.html) | force-directed graph, 18 real correction laws | LAWS array copied from .agents/skills/operator-corrections/SKILL.md | STATIC | parse SKILL.md at serve-time so law edits re-lattice (NOTE: Law 20 added tonight — lattice is one law behind) |

Gallery totals: 16 files / 746,766 B (12 HTML exhibits = 106,948 B; 4 baked data JS = 639,818 B; game_verkle_knots.js 67,478 B = 260 knots / 5,767 leaves, root 3c75ffae..., last knot 2026-08-10). Not-tabbed: swarm_board.png, lattice.html (live — polls /api/v1/lattice-lab + :8743/api/health), mesh_gallery.html (.glb skinner).

## THE MISSING EXHIBIT — the LIVE STONE BOARD

One frame is empty and its data ALREADY FLOWS: dashboard/static/trailer_telemetry.json (trailer_telemetry.v1, live during runs — 3 lanes, hold_seconds, falls, docked, quota_frozen_ticks, leaderboard). No tab reads it. Build viz_stone_board.html: stone-protocol board where each lane is a stone track, stones advance per docked tick, hold_seconds is the burn timer, quota_frozen_ticks freezes a track, falls crack the stone — the 12th tab, the only exhibit live in the chain sense: rendered from telemetry the trailer produces right now. One fetch loop (setInterval + fetch('trailer_telemetry.json')) and the wow surface beats.
