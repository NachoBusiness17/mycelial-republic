# NAV WIRING — 2026-09-06 — worker "wiring" (concurrency probe group 2, width 8)

**THE LAW:** served is not wired. G4 wire debt from `watch/RESEARCH_ARCHAEOLOGY_20260905.md`
named 23 unwired surfaces; on arrival, **19 were already wired** by earlier batches
(decks-daytool 09-05 + batch5/batch5-s2). This run closed the remainder.

## WIRED (4 additions — all files verified to exist before wiring)

| Label | File |
|---|---|
| Room Game | `/static/room_game.html` |
| Spore Fish | `/static/viz_spore_fish.html` |
| Clear UI | `/static/index.clear-ui.html` |
| RTFM Shell | `/static/_rtfm_graph_shell.html` |

All appended at the tail of LINKS in `dashboard/static/nav.js` (after "Armory"),
grouping/style identical to existing entries. `node --check nav.js` → OK.

## ALREADY-WIRED at run start (19 of 23, no action, additive-only respected)
arena_operator_field, arrakis, chan (route `/chan`), erosion_field, game,
grab_write, labs_map, live, maze_arena, memory_map, module_map, operator_board,
rib_toy, scout_deck, smith_chart, steal_tools, steer_field, verkle_knot_wave,
viz_3d_verkle.

## PENDING (file does not exist — not wired, per law)

| Surface | Status |
|---|---|
| salon_lightmap.html | ABSENT at end of run (checked 2x) — other worker still building (SHADERTOY B2). Wire when it lands: `["/static/salon_lightmap.html", "Salon Lightmap"]`. |
| maze_arena upgrade | maze_arena.html EXISTS and is already wired ("Maze Arena") — the upgrade mutates the same file, no new entry needed. |

## DIFF VERDICT

- Backup: `dashboard/static/nav.js.bak-nav-20260906-wiring` (59 entries, 2026-09-05 21:55)
- Current: 63 entries → **4 additions, 0 removals, 0 modifications**
- `diff backup current`: only line 62 (Armory gained trailing comma) + 4 appended lines
- Each new label greps exactly once

## ROLLBACK

```bash
cp dashboard/static/nav.js.bak-nav-20260906-wiring dashboard/static/nav.js
```

*Filed 09-06 by worker "wiring". Probe slot: codingplan.max-flash-5x.2.*
