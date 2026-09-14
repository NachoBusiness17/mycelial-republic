# TESUJI PAGER — field page (arena grammar, on the model) · 2026-09-06 · walker "pager"

**Build:** `dashboard/static/tesuji_map.html` — ONE self-contained file, no deps beyond nav.js include.

## Design (5 lines)
1. Six axis corridors (A1 REASONING DEPTH … A6 LOCAL DIFF, titles from TESUJI_MAP_5_3FLASH_20260906.md) — charter corridors always on the board; an empty corridor is data too (A2 REFUSAL SHADOW sits empty = the unprobed shadow).
2. Each cell = a stone: cyan-lit SUPPORTED · amber DISPUTED · dim slate UNPROVEN · void-black + red rim SHADOW (refusal cell — the model's shadow field). Hover/tap → tooltip (cell id · verdict · tokens · ms · ts).
3. Corridor header carries counts `n= · S D U X`; tip line: "TESUJI — sacrifice stones reading the field · 5.3-flash behavior surface · falsifier: predictive ≥70%".
4. Polls `/static/tesuji_map.json` every 10s, `cache: no-store`; missing/empty/broken JSON → "field empty — walkers out", keeps polling. Unknown axes/verdicts render (extra axes sorted after A1–A6, unknown verdict → slate + true label in tooltip).
5. House palette: bg #070d0c, cyan #7cf5ff, amber #e8c96a; maze-arena grammar (lit field, shadows where light doesn't reach).

## Verify (done 2026-09-06)
- `node --check` on extracted inline JS (both script blocks): **PASS**
- `curl http://127.0.0.1:8765/static/tesuji_map.html` → **HTTP 200** (10,096 bytes)
- Live data read end-to-end: tesuji_map.json landed mid-build (T0 miners) — 14 cells / 5 corridors rendered against real schema {axes.A#.cells[{cell,verdict,tokens,ms,ts}], verdicts, total, ts}.

## NAV ENTRY (wiring pass owns nav.js — insert in LINKS array)
    ["/static/tesuji_map.html", "Tesuji Map"],

Suggested position: next to `["/static/maze_arena.html", "Maze Arena"]` (same grammar lineage).

## Falsifier hook
Page displays raw field only — predictive ≥70% falsifier enforced at map level (charter #1), not in page.
