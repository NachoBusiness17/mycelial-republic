# s2-14: census of dashboard/static/games/ (2026-09-28)

Census lane f2, item s2-14. Every number below comes from a command run during this ask
(find, wc, grep, node vm.Script compile, node JSON.parse, git ls-files / git status, cmp).
Census moment: 2026-09-28, branch mag/run-beta1-factory-build-audi-20260806T231709Z.

## 1. Inventory: 26 files / 6 dirs

`find dashboard/static/games -type f | wc -l` = 26; dirs = 6 (games/, .mimosa/,
.mimosa/hook-state/, .mimosa/hook-state/<sess>.baseline/, .vercel/, soul_frontier/).

| class | count | files |
|---|---|---|
| game pages (html) | 10 | skifree, maze_arena, ruins_go, mud, swarm, frontier_souls, toy, arena_operator_field, arrakis (top level) + soul_frontier/soul_frontier.html |
| launcher | 1 | index.html (19 lines, links 9 games, games/index.html:10-18) |
| backup copy | 1 | skifree.html.bak, byte-identical to skifree.html (`cmp` = IDENTICAL, 16,200 B each) |
| js modules | 2 | ruins_go_engine.js (417 lines, loaded), oracle_dice.js (87 lines, orphan) |
| json data | 6 | ruins_go_pack.json (1,057 lines, 33 levels), rounds_real.json (1,727 lines), dd_dragon-hoard / dd_gelatinous-cube / dd_mimic-plate / dd_riddle-door |
| tooling/metadata | 6 | .gitignore (contains only ".vercel"), 3 files under .mimosa/hook-state/, 2 under .vercel/ (Vercel project "games", prj_X4gxhiQGfhlqFgbgcLUZWanKRUvM) |

Code+data lines across the 18 html/js/json files: 13,622 (`wc -l`). Largest: mud.html 2,650
lines / 125,486 B; smallest game: arena_operator_field.html 252 lines.

Git state: `git ls-files` tracks 20 of 26 files; untracked = skifree.html.bak, 3 .mimosa
files, 2 .vercel files. Working-tree drift: mud.html has uncommitted +33/-2 (`git diff
--stat`), an FW-37 WebSocket push-socket spike (RELAY_WS at mud.html new lines: ws frames
~8Hz, 3-strike fallback to the v1 HTTP poll).

## 2. Playable: 10/10 pass the checks run; 9 reachable from the launcher

Checks run this session (node v22.23.1):

1. JS compile: every inline `<script>` block of all 11 html pages plus both .js files
   compiled with `vm.Script` (syntax check, no execution): 15 blocks total, 0 failures
   (probe `watch/inbox/burn_reset_20260927/flash50/_s2_14_jscheck.js`, re-run from its
   banked location at census time: TOTAL blocks=15 failed=0). Per page: ruins_go.html 2
   blocks (one is the
   empty src-tag body; its inline UI block compiles).
2. JSON parse: all 6 json files PARSE-OK via `node -e JSON.parse(...)` (6/6).
3. Dependency resolution: the only external script tag in the tree is
   ruins_go.html:54 `<script src="ruins_go_engine.js?v=1">` (file exists); data fetches:
   ruins_go.html:65 fetches ruins_go_pack.json (exists); maze_arena.html:764-765 fetches
   rounds_real.json from a 3-candidate chain ending in the relative in-dir path (exists;
   a byte-identical duplicate also sits at dashboard/static/rounds_real.json, `cmp`
   IDENTICAL, both 19,986 B).
4. Runtime loop: 9 of 10 games reference requestAnimationFrame (1-3 refs each); ruins_go
   is step-clock by engine law L1 (ruins_go_engine.js:6 "the world ticks exactly when the
   player displaces"), so no raf is by design.

Per-game verdicts:

| game | lines | deps | verdict |
|---|---|---|---|
| skifree.html | 570 | none | PLAYABLE, standalone |
| maze_arena.html | 865 | rounds_real.json (optional fetch chain) | PLAYABLE; errbanner self-reports runtime errors |
| ruins_go.html | 234 | ruins_go_engine.js + ruins_go_pack.json (33 levels) | PLAYABLE; html:59 reads window.RUINS_GO which the engine exports (engine:416-418) |
| mud.html | 2,650 | relay 127.0.0.1:8766 for multiplayer | PLAYABLE solo; presence needs dashboard/mud_relay.py (its PORT=8766 at line 55 matches mud.html:456); fetches are .catch-guarded |
| swarm.html | 1,734 | audio candidates ../suno/ then suno/ | PLAYABLE; audio fetch failures silent-skip to fallbackDisco synth (swarm.html:64-67) |
| frontier_souls.html | 1,995 | none | PLAYABLE, standalone |
| toy.html | 246 | none | PLAYABLE; exposes window.TOY, fleet-day seeded RNG (toy.html:17-24) |
| arena_operator_field.html | 252 | WebGL (optional) | PLAYABLE; GPU view disabled falls back to CPU/2D with a notice (lines 110-113) |
| arrakis.html | 380 | none | PLAYABLE, standalone; errbanner at line 20 |
| soul_frontier/soul_frontier.html | 1,291 | none | COMPILES+PLAYABLE but UNREACHABLE through any UI: not linked by games/index.html, zero references anywhere in dashboard/ (grep = 0 files) |

Not executed in a browser this session: playability = compile + dependency-integrity +
loop-presence evidence, not a human play test.

## 3. Bugs noted in comments

`grep -rn "TODO|FIXME" .` over the whole games tree: 0 hits (exit 1). No file notes an
unfixed bug. What the comments DO note:

Noted-and-fixed bug class (4 files):

- maze_arena.html:59 "M2 smoke hooks (BURIED-BUG LAW, Shadow Walk v1: never trust an
  unverified generator)"; :179 errbanner tripwire "field generator carved 0 cells -
  BURIED-BUG tripwire"; :632 generator pulse shown in the HUD "BURIED-BUG LAW".
- mud.html:485-487 and swarm.html:12-14 SAFE_STORAGE: localStorage "throws in private
  browsing / blocked-cookie modes and would kill the game at load"; both fixed with one
  guarded accessor falling back to in-memory storage.
- swarm.html:64-67 jukebox deploy law: a failed audio fetch "never breaks the game loop";
  candidate chain plus fallbackDisco synth.
- toy.html:9-11 editor note: "drafted by union-alpha (free window), fixed by U1 - dodge
  law rollT>0 (not iframes), stable identity across start(), seed0 vs mutated lcg,
  applied-inputs log, windup plant, browser fixed-step pump."

Stale-doc defects this census found (comments contradicted by the tree):

- oracle_dice.js:2 claims "Used by: mud.html, ruins_go.html, frontier_souls.html" -
  false: grep finds 0 references to oracle_dice anywhere in the games dir, dashboard/,
  mag/, tools/, or tests/; no script tag loads it. Orphan module.
- ruins_go_engine.js:5 claims "tests require it" - false: `grep -rln "ruins" tests/`
  returns 0 files.
- dd_riddle-door.json filename does not match content: the file's id is "DD-spear-parity"
  (Spear Parity level, "Speak only on the even breath").

Bug-visibility features (not bugs): three games install window.onerror errbanners that
print ERR/REJ lines on screen: arrakis.html:20, maze_arena.html:18, swarm.html:1.

dd_*.json disposition (node comparison vs pack): dd_gelatinous-cube.json and
dd_mimic-plate.json are folded verbatim into ruins_go_pack.json (fullEntryMatch=true both);
dd_dragon-hoard.json (id DD-hoard) and dd_riddle-door.json (id DD-spear-parity) are in
neither the pack nor any loader - standalone orphans.

## 4. Referenced by the dashboard

Per-file reference matrix (`grep -rl "games/<name>" dashboard/` over html/js/py/json,
excluding static/games/ itself and __pycache__):

| game | referencing dashboard files | refs |
|---|---|---|
| games/mud.html | deck.html:505 (card) + deck.html:664-669 (fleet.games list with frontier_souls + toy), stub dashboard/static/mud.html:3-5 (meta refresh "canonical copy lives at /static/games/mud.html"), museum/estate_walk.lod.html, vislab/catalog.html, vislab/catalog.json | 5 |
| games/maze_arena.html | deck.html:510, estate_walk.html:47, stub dashboard/static/maze_arena.html, museum/estate_walk.lod.html, vislab catalog pair | 6 |
| games/swarm.html | deck.html:515, maze.html:70 (unlock link "/games/swarm"), vislab catalog pair | 4 |
| games/frontier_souls.html | deck.html:525, museum/estate_walk.lod.html, vislab catalog pair | 4 |
| games/toy.html | deck.html:500 + :664-669 fleet list, vislab catalog pair | 3 |
| games/arena_operator_field.html | deck.html:530, stub dashboard/static/arena_operator_field.html (the nav.js "/static/arena_operator_field.html" link lands on the stub), vislab catalog pair | 4 |
| games/arrakis.html | deck.html:520, stub dashboard/static/arrakis.html (nav.js link), vislab catalog pair | 4 |
| games/skifree.html | none | 0 |
| games/ruins_go.html | none | 0 |
| games/soul_frontier.html | none (also not in the games launcher) | 0 |

Generic dashboard surfaces: dashboard/static/index.html:93-94 comment "games/* deployed
(live)" plus the liveness() rule at :118 (`name.startsWith('games/')` returns 'live') mark
the whole directory live; nav.js references the directory twice as "/static/games/"
(labeled "Maze Arena", the FW-45 2026-09-28 repair comment at nav.js:2-8 records pointing
the maze_arena entries at /static/games/); dashboard/server.py:645 serves /static/*
generically (no per-game route); dashboard/rest.py:3121-3128 mentions "games" but that is
the unrelated agent-arena chess POC, not this directory.

Support files: rounds_real.json loaded only by maze_arena.html:764; ruins_go_pack.json
only by ruins_go.html:65; ruins_go_engine.js only by ruins_go.html:54; oracle_dice.js and
all four dd_*.json loaded by nothing.

## 5. Headline counts

- Games: 10 (9 linked from games/index.html + 1 unlinked orphan, soul_frontier).
- Playable by the checks run: 10/10 compile with deps resolving; 9 reachable through the
  launcher, soul_frontier only by direct URL.
- Files with bug/caveat comments: 4 note fixed bugs (maze_arena, mud, swarm, toy); 3 carry
  stale-doc defects (oracle_dice.js header, ruins_go_engine.js header, dd_riddle-door.json
  filename); 0 TODO/FIXME; 0 unfixed-bug notes.
- Referenced by the dashboard: 7 of 10 (mud, maze_arena, swarm, frontier_souls, toy,
  arena_operator_field, arrakis). Not referenced: skifree, ruins_go, soul_frontier
  (skifree and ruins_go are launcher-only; soul_frontier is referenced by nothing).
