---
name: games-audit-fix-wave-20260917
description: 2026-09-17 12-agent parallel audit of all games/dashboard → fix
  wave COMMITTED (161cafffe): swarm 3 crashes fixed, frontier runs persistence
  fixed, pack degenerates removed, FLEET ARCADE index built, nav link redirected;
  open items ranked (traits into step() #1, mud fork, maze_arena harness)
metadata:
  node_type: memory
  type: project
  originSessionId: sess_199e4b14-3a8b-46e9-ba5e-57c166fc2967
---

2026-09-17 — operator order "look at all our games, look at our static dashboard,
everything is a fucking mess — SELF STEAL DOGFOOD EVERYTHING, this is not a suggestion"
→ 12 parallel agents audited the entire games/dashboard surface, then a fix wave
COMMITTED (161cafffe). 9/12 agents returned before session cancel; 3 cancelled and
relaunched per Mickey-17 (bodies die, mission persists).

**Fixed and verified (commit 161cafffe):**
- swarm.html 3 game-killers: souls-NaN bank corruption (`player.souls` never initialized,
  spent at 3 sites), `G.shake` ReferenceError on hit, `spawnBoss` ReferenceError killing
  the whole loop at T=300 (Herald) — all fixed, 32/32 harness re-verified.
- frontier_souls headline mechanic UN-BROKEN: `G.runs` reset to 0 on every reload while
  `fs_souls` persisted → cross-run souls messages invisible after session 1; run counter
  now persists via SAFE_STORE (`fs_runs`), 51/51 re-verified.
- ruins_go pack 21→20: "the_passing_guard" was an exact clone of shrine_patrol with
  unreachable gem (deleted); shrine_patrol gem moved onto floor. ALL PASS.
- FLEET ARCADE built: dashboard/static/games/index.html (8 games, harness counts,
  one-line pitches) — games previously had NO index and zero inbound links.
- nav.js broken `/static/maze_arena.html` link redirected to `/static/games/`.

**Open (ranked, next fix wave):**
1. ~~D&D traits display-only~~ FIXED — vision snakes pathfind toward start+current,
   berserk lizards move twice per step. Gate 51/51, pack 25 ALL PASS. Thorns/chain
   still pending (need skip-turn flag + tick-parity offset in player state).
2. mud.html byte-identical duplicate at `dashboard/static/mud.html` — drift fork.
3. maze_arena.html unharnessed — 10 `Math.random` sites; convert to seeded stream
   + input tape (F1/F2 pattern from test_mud_replay.js).
4. mud_relay polls 8×/s with no backoff when relay is down.
5. Bred-pack difficulty hole at 10–14 moves; chapter field mixes ints and strings.
6. frontier `killFoe` splices `foes` while callers iterate — skipped foes per tick.

**Audit gems:** all 5 harnesses green under load (mud 63/63 + 41/41 replay, frontier
51/51, swarm 32/32, toy 15/15); no-harness games = arena_operator_field, arrakis,
maze_arena, ruins_go (UI only); rounds_real.json is LIVE (maze_arena ?real=1); vislab
catalog 240 entries fresh; traits provenance — mud.html BOONS L461-473 are the real
implementation, ruins_go has names only; grudge system mud-locked (frontier_souls =
cheapest transfer target); games/ undiscoverable from root (closed by arcade index).
