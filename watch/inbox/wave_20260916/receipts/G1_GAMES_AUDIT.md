# G1 — HTML Games Audit receipt

- Wave: wave_20260916 · Lane: G1 (games audit)
- Operator order: audit only, NO fixes. Debugging/fixing deferred to gen-2.
- Constraints honored: no git commands, no paid APIs, `.venv\Scripts\python.exe` + node v22.23.1.
- Status: IN PROGRESS — findings appended below as they land.

## Inventory (dashboard/static/games/)

| File | Bytes | Kind |
|---|---|---|
| arena_operator_field.html | 12,288 | game |
| arrakis.html | 11,495 | game |
| frontier_souls.html | 84,785 | game |
| maze_arena.html | 51,645 | game |
| mud.html | 100,832 | game |
| rounds_real.json | 19,986 | data (not a game) |
| swarm.html | 78,041 | game |
| toy.html | 12,919 | game |

Harnesses located in scripts/: test_mud_fifty.js, test_frontier_souls.js, test_toy.js, playtest_swarm.js, lite_lane_probe.mjs, lite_lane_sustained.mjs.

---

## Harness results (verbatim captures)

| Harness | Target | Result | Exit |
|---|---|---|---|
| scripts/test_toy.js | games/toy.html | `12/12 lanes green` — all PASS (seed 20260916, tape A sha `678ddd9d2e189555…`, verdict win) | 0 |
| scripts/test_mud_fifty.js | games/mud.html | `51/51 lanes green` — all PASS (lanes 1–51 shown; perf lane "heavy room steps under 8ms" green) | 0 |
| scripts/test_frontier_souls.js | games/frontier_souls.html | `42/42 lanes green` — all PASS. This IS the 42-lane harness ("Adam's-laws harness"). | 0 |
| scripts/playtest_swarm.js | **dashboard/static/swarm.html (stale copy, not games/)** | `===== DOGFOOD VERDICT: 32/32 =====` all PASS | 0 |

- arena_operator_field.html, arrakis.html, maze_arena.html: **no harness exists**.
- scripts/lite_lane_probe.mjs / lite_lane_sustained.mjs: LLM API probes, not game harnesses — excluded (also honors the no-paid-APIs constraint).

## Harness-target + serving drift (defect class: BROKEN tooling / duplicate surfaces)

- `dashboard/static/` keeps a SECOND copy of 5 of the 7 games. Hash compare (md5):
  - mud.html **DIVERGED**: static/ = 31,348 B (Sep 12, stale) vs games/ = 100,832 B (Sep 15, current). Two live divergent muds.
  - swarm.html, maze_arena.html, arena_operator_field.html, arrakis.html, rounds_real.json: IDENTICAL today (accident of timing, not a rule — mud proves the drift mechanism).
- scripts/playtest_swarm.js:9 reads `dashboard/static/swarm.html` — validates the WRONG copy. If games/swarm.html changes (as mud did), the gate stays green while the deployed game rots.
- nav.js links only `/static/maze_arena.html`, `/static/arrakis.html`, `/static/arena_operator_field.html` (top-level copies). Zero links to `/static/games/*`.
- Reachability of games/ copies: estate_walk.lod.html → games/{frontier_souls, maze_arena, mud}.html; vislab/catalog.html → games/{arena_operator_field, arrakis, maze_arena, mud, swarm}.html.
- **Orphans**: toy.html — no nav link, NO vislab catalog entry, no other HTML links it. frontier_souls.html — no nav link, no vislab catalog entry (only estate_walk.lod).
- vislab/catalog.html (generated 2026-09-14) is stale: mud entry says `bytes: 33415` vs actual 100,832; missing toy + frontier entries entirely.
- swarm.html is the only file with CRLF line endings on disk (78,041 B on disk vs 76,356 B logical); all others LF.

## Structure

| Game | Bytes | Lines | Script blocks | Canvases | Math.random | localStorage |
|---|---|---|---|---|---|---|
| arena_operator_field.html | 12,288 | 226 | 1 | 1 | 2 | 0 |
| arrakis.html | 11,495 | 242 | 2 | 1 | 4 | 0 |
| frontier_souls.html | 84,785 | 1,829 | 1 | 1 | 20 | 4 |
| maze_arena.html | 51,645 | 866 | 2 | 2 | 6 | 0 |
| mud.html | 100,832 | 2,312 | 1 | 1 | 24 | 4 |
| swarm.html | 78,041 | 1,686 | 2 | 2 | 24 | 8 |
| toy.html | 12,919 | 232 | 1 | 1 | 2 | 0 |

## Static analysis findings

### The replay-law violation list (Math.random vs seeded LCG) — THE headline

**Only toy.html complies.** It is the reference implementation: seeded LCG, zero runtime Math.random (both grep hits are comments), draw-counted RNG, sha256-stamped receipts, and the harness proves byte-replay. Every other game rolls Math.random directly:

| Game | Math.random sites (line numbers) | Severity of effect |
|---|---|---|
| mud.html | 25 sites (66, 420, 432, 464, 475, 540, 623–624, 698, 758, 884, 893, 902, 1111, 1191, 1222, 1454, 1574, 1685, 1722–1728, 1752, 2212) | gameplay-critical: crits, loot rolls, spawn tables, bell trigger, ghost riposte |
| swarm.html | 31 sites (203–1150) | gameplay-critical: spawns, weather, riddles, doors, horse |
| frontier_souls.html | 21 sites (59–1024) | gameplay-critical: pack spawns, crit, 50/50 rattle kill, ambient; "seed" keywords are `seedWorld()`/`f.seed` phase offsets — NOT an LCG |
| maze_arena.html | 10 (184, 286, 291, 791, 804, 807) | agent sim: heading init + bump turns + particles |
| arrakis.html | 7 (82 x2, 126, 167 x4, 168) | 2 gameplay (randPos spawns), 5 cosmetic ornaments |
| arena_operator_field.html | 2 (161, 165) | agent heading/bump |
| toy.html | 0 runtime (lines 18, 224 are comments) | **COMPLIANT** |

Note: the 'sha' keyword hits in mud/frontier/swarm/maze are words like "shadow", NOT hashing. None of the six compute sha256 over receipts. arena_operator_field's "DIVERGENCE RECEIPT" is an in-page GPU-vs-CPU 12-point per-frame compare — ephemeral, not persisted or hashed. Receipt-schema reality: **toy is the only game with a receipt schema at all** (`{events[], sha256, verdict, hits_taken, hits_no_telegraph, duration_s}`); the others emit nothing comparable.

### localStorage / resource handling

- **swarm.html: 8 BARE localStorage sites, ZERO try/catch** (lines 187, 208, 311, 312, 563, 873, 876, 1593). `JSON.parse(localStorage.getItem('priv_charcoal')||'[]')` runs at module top level → in privacy mode / storage-denied the game dies on load. FATAL class.
- frontier_souls (4 sites) and mud (4 sites): all wrapped in try/catch — correct pattern (lines 151–152, 326–328 / 450–451, 2221, 2246).
- mud.html line 2307: `setInterval(relayTick, 250)` — never cleared, no teardown; acceptable for a single-page game but an unclosed-resource pattern.
- mud.html line 430: `RELAY = 'http://127.0.0.1:8766'` hardcoded, plain HTTP, and both relay fetches swallow errors with `.catch(()=>{})` — silent degradation, no surfaced relay-down state.
- AudioContext: mud (line 54) + frontier (line ~59) lazy-create but never call `resume()` and have no visibilitychange handling; swarm has 1 resume. Autoplay-policy risk: audio may never start. Cosmetic.
- Dead references: getElementById — **zero dead ids in all 7 games** (every id used is defined). No TODO/FIXME/XXX in any game (0 across the board).
- **swarm.html audio is broken in its deployed location**: `new Audio('suno/gift_track.mp3')` (line 63) and the onerror fallback `new Audio('suno/flat_beat_loop.mp3')` (line 67) are RELATIVE paths. Files exist only at `dashboard/static/suno/`; `dashboard/static/games/suno/` does not exist → when served from `/static/games/swarm.html` (the vislab catalog's launch path) both primary AND fallback 404 and the game silently goes fallbackDisco. The stale top-level copy works — audio is a casualty of the rehome.
- maze_arena's fetch ladder (line 764: `/static/rounds_real.json` → `../static/rounds_real.json` → `rounds_real.json`) is defensive and resolves from BOTH locations — no defect. rounds_real.json is identical in both copies.
- Error surfacing: arrakis, maze_arena, swarm carry an identical 1-line block-0 `window.onerror → #errbanner` bootstrap (copied code, 383/383/206 chars); **mud and frontier_souls have none** — the two biggest games fail invisibly.

### Syntax check (browser-less)

All 10 extracted script blocks (7 games; arrakis/maze_arena/swarm have 2 blocks each) pass `node --check`. Temp files under `%TEMP%\g1_games_audit\` (outside the repo). **Zero syntax errors.** Exit 0.

### Cross-game duplication

- `const rnd=(a,b)=>a+Math.random()*(b-a)` duplicated byte-identical in mud (66), frontier_souls (94), swarm (203).
- localStorage `lore` IIFE + `loreSave()` pattern duplicated mud ↔ frontier_souls (keys `mud_lore` / `fs_lore`), same shape.
- onerror→errbanner bootstrap duplicated in arrakis/maze_arena/swarm (mud+frontier missing it).
- Harness-side: test_mud_fifty / test_frontier_souls / test_toy share the same DOM-shim + lane framework (fine for CI, but a shared harness lib would stop drift like the swarm retarget bug).

---

## PER-GAME SCORECARD

| Game | Harness | FATAL | BROKEN | COSMETIC | Seeded-RNG law |
|---|---|---|---|---|---|
| toy.html | 12/12 PASS (exit 0) | 0 | 0 | 0 | **COMPLIANT** (reference impl) |
| mud.html | 51/51 PASS (exit 0) | 0 | 1 (RNG law, 25 sites; no determinism lane in harness) | 3 (no errbanner, setInterval never cleared, silent relay fetch + hardcoded 127.0.0.1:8766) | VIOLATION |
| frontier_souls.html | 42/42 PASS (exit 0) | 0 | 1 (RNG law, 21 sites) | 2 (no errbanner, AudioContext no resume) | VIOLATION |
| swarm.html | 32/32 PASS — **but harness tests the stale static/ copy** | 1 (bare localStorage, load-time throw) | 2 (RNG law 31 sites; audio 404s under /static/games/) | 1 (CRLF endings) | VIOLATION |
| maze_arena.html | none exists | 0 | 1 (RNG law, 10 sites) | 0 | VIOLATION |
| arrakis.html | none exists | 0 | 1 (RNG law, 7 sites) | 0 | VIOLATION |
| arena_operator_field.html | none exists | 0 | 1 (RNG law, 2 sites) | 0 | VIOLATION |
| rounds_real.json | n/a (data) | 0 | 0 | 0 | n/a |

Pipeline/cross-game defects (not charged to a single game): playtest_swarm.js wrong target; mud.html diverged duplicate (31 KB stale vs 100 KB current); vislab catalog stale (mud bytes 33,415 vs actual 100,832) and missing toy + frontier entries; toy.html fully orphaned (no nav, no catalog); nav links only the top-level duplicates.

## TOP-10 FIX LIST (ranked, for gen-2)

1. **swarm.html — wrap all 8 localStorage sites in try/catch** (mud/frontier pattern). FATAL: privacy mode kills the game at load.
2. **swarm.html — fix audio paths** to `/static/suno/...` (absolute) or copy suno assets under games/. Audio is dead in the deployed location.
3. **scripts/playtest_swarm.js — retarget to `dashboard/static/games/swarm.html`.** The gate currently validates a stale copy; the mud divergence shows exactly how this rots.
4. **Kill the duplicate game surfaces**: make `games/` canonical, reconcile mud first (diverged), then delete/redirect `static/{mud,swarm,maze_arena,arena_operator_field,arrakis}.html`.
5. **Regenerate vislab catalog + wire nav**: stale mud entry, missing toy/frontier entries; decide toy's fate (promote to catalog or attic).
6. **Port toy.html's seeded LCG into mud + swarm + frontier_souls** (96 violation sites total across all six; these three are 77 of them) — unblocks replay receipts, which all three claim in spirit but cannot do.
7. Same LCG port for **maze_arena + arrakis + arena_operator_field** (19 sites; mechanical, small).
8. **Add the onerror→errbanner bootstrap to mud + frontier_souls** — biggest games, zero visible error surfacing.
9. **Write harnesses for the three untested games** (arena_operator_field smallest → arrakis → maze_arena) using the fifty-lane shim pattern.
10. **mud relay hygiene**: teardown/idempotency for the never-cleared `setInterval(relayTick, 250)`, surface relay-down once instead of swallowing every tick, and stop hardcoding `http://127.0.0.1:8766`.

## GEN-2 VERDICT: rewrite vs patch

| Game | Verdict | Why |
|---|---|---|
| toy.html | **PATCH** (nothing to fix) | The law's reference implementation. Only action is distribution (catalog/nav) or attic. |
| frontier_souls.html | **PATCH** | Clean structure, excellent 42-lane harness. Mechanical LCG port + errbanner. |
| maze_arena.html | **PATCH** | Sound; LCG port + first harness port. |
| arrakis.html | **PATCH** | Tiny; LCG port is ~7 lines of work. |
| arena_operator_field.html | **PATCH** | Tiny; LCG port is 2 sites. |
| mud.html | **PATCH — largest lane** | Harness (51 lanes) and structure are strong; the LCG port touches 25 sites and the relay/storage hygiene is real work. No rewrite justified. |
| swarm.html | **PATCH with a dedicated lane; rewrite only the storage+audio layer** | 32-lane playtest passes and systems are deep, but it holds the only FATAL (bare localStorage) plus broken audio plus a mistargeted gate. Rewrite the persistence/audio shell, keep the game. |

Duplicate-surface cleanup (fix list items 3–5) should be ONE ops lane in gen-2, not per-game work.

---

Audit method notes: grep in this MSYS environment silently mangles patterns starting with `/` (path conversion) — python re was used for authoritative tag counts. Syntax temp files: `C:\Users\foste\AppData\Local\Temp\g1_games_audit\` (outside repo). No fixes made. No git commands run. No APIs called.
