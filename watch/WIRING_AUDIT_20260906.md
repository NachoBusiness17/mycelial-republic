# WIRING AUDIT 2026-09-06 — nav.js vs dashboard/static/*.html

Law executed: "served is not wired" — an html surface not linked from nav.js is an
orphan: built + receipted but unlinked = not delivered.

## Counts
- html surfaces in dashboard/static (excluding *.bak-nav): **58**
- nav.js LINKS entries before patch: **40** (incl. routes `/` → index.html and
  `/chan` → chan.html, plus non-html targets night/index.html, art/index.html,
  salons/astra/index.html, swarm_board.png — all verified to exist)
- dead links before patch: **0**
- raw orphans before patch: **24**; true orphans after route/variant adjustment: **20**
  (index.html and chan.html are wired via routes; index.clear-ui.html and
  _rtfm_graph_shell.html are internal variants, left unwired deliberately)

## Patch
- Backup first: `dashboard/static/nav.js.bak-batch5`
- Minimal additive edit: 10 entries appended at the tail of LINKS, same
  `[url, label]` shape. Nothing removed, nothing restructured, no *.bak-nav touched.
- Wired now (10): live.html (Live — carries the OVERSEER strip), operator_board.html,
  verkle_knot_wave.html, viz_3d_verkle.html, memory_map.html, module_map.html,
  labs_map.html, erosion_field.html, arena_operator_field.html, steer_field.html
- Priority basis: mtime first (09-05 → 09-04 → 09-03), this-week work named in the
  batch card maps as: overseer → live.html strip; burn_board/falsifiers/dungeon/
  calabi_yau/swarm_board were ALREADY wired; live_feed/topic_index/read_receipts are
  JSON feeds rendered inside surfaces, not standalone pages; no trajectory html exists.

## Verify
- Re-parsed patched nav.js: **50 links, 0 dead links** (every /static/ path resolves
  to an existing file). Zero dead links introduced.

## Still unwired (10, lowest value/oldest)
arrakis.html, game.html, grab_write.html, maze_arena.html, rib_toy.html,
room_game.html, scout_deck.html, smith_chart.html, steal_tools.html, viz_spore_fish.html
(maze_arena is B1 of the shadow-fields card — candidate for a follow-up wire.)

## Serving note (tri-state)
- Pages include nav via `<script src="/static/nav.js"></script>` — SUPPORTED
  (grep: control.html et al.).
- Exact static-mount line for port 8765 — UNPROVEN this pass (two greps in
  mag/api_gateway.py found no literal mount; serving is indirect). Does not affect
  the audit: the URL works in production.

Backup path: C:/Users/foste/Documents/projects/local_sovereign_agent/dashboard/static/nav.js.bak-batch5
— w2-wire, batch5, 2026-09-05/06

## batch5-s2 (2026-09-06) — the last 10 orphans
APPENDED after w2's text; nothing above edited.

### Triage (head-read + mtime each)
- WORTH WIRING (8): maze_arena.html (09-02, B1 shadow-fields — read END TO END: zero
  external fetches, zero script src, all inline; standalone PASS), arrakis.html (09-03,
  Dune-wing rider game, self-contained), game.html (09-04, "The Necromancer's Swarm",
  30K game), grab_write.html (09-04, "The Tesuji" static doctrine page, no fetches),
  rib_toy.html (09-03, RIB packet editor — only dep is the local Ollama endpoint,
  works when engine is up), scout_deck.html (09-03, baked deck, no fetches),
  smith_chart.html (09-03, "fold law" exhibit, header-declared ZERO FETCH LAW),
  steal_tools.html (09-04, "The Armory — 116 steal tools").
- LEFT UNWIRED (2): room_game.html — VARIANT: same title/skeleton as maze_arena
  (77 changed lines = playable white-lantern fork); maze_arena stays the canonical
  B1 link. viz_spore_fish.html — INTERNAL: self-labeled wrong-turn lab record,
  already embedded in viz_gallery.html as item 'fish'.

### Dep fix (additive, enables 2 of the 8)
- game.html and steal_tools.html referenced data JS at repo ROOT
  (game_verkle_knots.js, steal_tools_data.js, gen 2026-08-15) — 404 as served from
  /static/. Copied both into dashboard/static/ (byte-identical, nothing edited).
  Freshness: game knots regen via scripts/_gen_game_verkle.py — copy may drift
  until regen re-copied; noted, not blocking.

### Patch
- Backup first: dashboard/static/nav.js.bak-batch5-s2
- 8 entries appended at tail of LINKS (same [url, label] shape), nothing removed
  or reordered: Maze Arena, Arrakis, Necromancer, Grab Write, Rib Toy, Scout Deck,
  Smith Chart, Armory. ("The Game" label already taken by dungeon.html — new game
  wired as "Necromancer".)

### Verify
- node --check nav.js: SYNTAX OK. Re-parsed LINKS: **59 links total (was 51),
  0 dead** (every /static/ path resolves), 0 duplicate urls, 0 duplicate labels.
- All 10 orphans accounted for: 8 wired, 2 classified and left.

Totals now: 59 nav links / 0 dead / 60 html surfaces wired-or-accounted.
— s2-wire2, batch5 wave 3, 2026-09-06
