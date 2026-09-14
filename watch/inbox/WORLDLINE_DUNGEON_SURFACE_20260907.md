# WORLDLINE DUNGEON — LIVE SURFACE (2026-09-07)

> **[AUDIT-TYPED 2026-09-08]** status: LIVE · claims: the teller renders pure-function HTML from live artifacts with byte-identity determinism (--check PASS), and the loop closed — the page's tip hash is the hash of the tape row about rendering the page — SUPPORTED (determinism check receipted in-card, dogfood row sealed and re-rendered) · falsifier: `--check` exiting 1 on a re-run, or a PROOF chamber's live value contradicting its cited artifact

The dungeon-master telling is now a live surface: a TELLER that renders the story from REAL fleet
artifacts, so the state of the story grows as the tape grows. $0-local, files only, read-only on
every story/artifact file (canon card, tape, chain, probe rows untouched).

## What was built

- **mag/worldline_dungeon.py — the TELLER.** `python -m mag.worldline_dungeon` reads the live
  artifacts and renders `dashboard/static/worldline_dungeon.html`. Every render is a pure function
  of the artifacts (no wall-clock, no randomness in output). `--check` renders twice from one
  artifact snapshot and asserts byte-identity.
- Page structured by the canon's four organs: **LAW** strip (three table laws), **PLAY** (the
  descent — mouth + Cold Gate + Antinode Sanctum + Hall of the Lived Record + Emergent Fork + Seed
  Vault + the last door, canon prose with LIVE numbers substituted), **PROOF** (the
  board-behind-the-tale table: live value + receipt path per row; dated receipts marked "measured
  09-07"), **RESTATEMENT** (plain close + koan "The record remembers. The 2.7 decides." + canon
  card path at the bottom).
- **Error-banner fixture** (house birth-defect law, maze_arena pattern): the arrakis/maze_arena
  `#errbanner` JS hooks at top, PLUS a server-side `#chamberfaults` box that always renders —
  green "0 chamber faults" when every artifact reads clean, red per-chamber FAULT lines (which
  artifact, what failed) with the chamber falling back to "the board has no row for this yet".
  Page never silently breaks; missing artifact degrades one chamber only.

## Live values baked in (at final render)

| Value | Live number | Artifact |
|---|---|---|
| Tape | 18 rows, 6 sessions, tip `f80676758d73b0d0` (the DOGFOOD row — see below) | memory/runs/trajectory/steps.jsonl |
| Chain | 7,377 knots, tip `d0a798c2972208c4…adb5b` @ 2026-09-06T23:08:56Z | memory/biography/verkle_chain.jsonl |
| F-W5 fork | 112.7% then 222.1% rel_delta, verdict LARGE_EFFECT / LARGE_EFFECT, 9 of 10 stones shared (run2 vs run1 conditioned intersection, computed live) | memory/runs/preload_selector/probe_20260907.jsonl |
| Seed vault | NO LONGER EMPTY — 1 seed on the pedestal: `w1-dogfood-20260907`, seed_hash `8dbd503f64bd163c`, five slabs, cut 2026-09-07T12:16:12Z | memory/worldline/w1-dogfood-20260907/SEED.json |
| Row-320 door | **OPEN** — tesuji wall at 319 stones (< 320); flips to WRITTEN automatically when row 320 lands | watch/TESUJI_MAP.jsonl |
| Curator's law | 15,564 bytes (15.2KB) on disk, weighed at render | C:/Users/foste/Documents/projects/AGENTS.md |
| Curator's shelves | recursive memory census at render (~414.7K files total; living vs biography_backup*/ghost attics split shown; definition stated on the row — canon's "517" not reproducible, board wins per law 2) | memory/ census |
| Dated statics | 97.3% re-light, 235.6K/23.6% meter, genome 0.7%, law 2.7%, phantom 441/92% — kept as marked dated receipts (c1/c2 screenshots, registry scan 09-07), not fabricated as live | canon PROOF table |

## Determinism check

- **PASS (pure function):** within one run the renderer builds the HTML twice from one artifact
  snapshot — byte-identical, asserted by `--check` (exit 1 on fail).
- **Cross-run:** renders seconds apart differ ONLY in the memory recursive census count
  (414,669 → 414,671 between two runs) — the fleet is live and writing to memory/ during the
  walk. That is the spec working: numbers update when an artifact changes, output is identical
  when nothing changed. The dungeon grows at the speed of the research.

## Nav wired: YES

One line added to the VISUALS deck in `dashboard/static/index.html` (after Fable Room):
`["worldline_dungeon.html","Worldline Dungeon","the dungeon-master telling, live from the board"]`.
Backup taken first: `dashboard/static/index.html.bak-worldline-20260907`. No nav structure touched.
Page header also carries a small console/tesuji/fable link strip.

## Dogfood row: YES — the loop closed on itself

Final render run through the W0 wrapper: `python -m mag.bash_local "python -m mag.worldline_dungeon --check"`.
That sealed tape row 18, step `f80676758d73b0d0`, session `bl-95499b34` (verify PASS: 18 rows,
6 sessions, chains intact) — and the row's `output` field contains the teller's own render report.
The page was then re-rendered, so the Hall chamber now reads "18 rows old tonight, tip
`f80676758d73b0d0`" — **the page's tip hash is the hash of the row about rendering the page.**
The dungeon writes a row about being written.

## Files

- mag/worldline_dungeon.py (new — the TELLER)
- dashboard/static/worldline_dungeon.html (generated — do not hand-edit, re-render)
- dashboard/static/index.html (+1 nav line, backup adjacent)
- watch/inbox/WORLDLINE_DUNGEON_SURFACE_20260907.md (this receipt)
- queue/handoff/zcode/CONVO.md (+1 row)

Read-only respected: watch/WORLDLINE_DUNGEON_STORY_20260907.md, steps.jsonl (append-only via the
sanctioned bash_local wrapper only), verkle_chain.jsonl, probe_20260907.jsonl, SEED.json,
TESUJI_MAP.jsonl — all untouched.
