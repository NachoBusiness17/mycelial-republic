# FX2 — Game surface reconcile receipt (gen-2 fix)

- Wave: wave_20260916 · Lane: FX2 (reconcile duplicate game surfaces)
- Mission: `dashboard/static/games/` is canonical (C5 deploy law); top-level `dashboard/static/*.html` game copies are DERIVED — regenerate stale copies from canonical, retarget `scripts/playtest_swarm.js`, regenerate the vislab catalog, re-run harnesses.
- Constraints: receipt first, append as gathered · no git commands · Write/Edit for source edits · `.venv\Scripts\python.exe` only · node for JS checks/harnesses.
- Inputs: G1_GAMES_AUDIT.md + G2_STATIC_INFRA_AUDIT.md (wave_20260916/receipts).
- Status: IN PROGRESS

## Step 1 — divergence verification (byte-compare, before state)

Verified with `.venv\Scripts\python.exe` (sha256 prefix16, size, CRLF flag) — G1's claim CONFIRMED:

| file | static/ (size, sha16, CRLF) | games/ (size, sha16, CRLF) | verdict |
|---|---|---|---|
| mud.html | 31,348 `da3651abdafde7cd` CRLF | 100,832 `468b884be6891a2d` LF | **DIVERGED** (stale 3× smaller) |
| swarm.html | 78,041 `91c1db9a43cc714d` CRLF | 78,041 `91c1db9a43cc714d` CRLF | IDENTICAL (today) |
| maze_arena.html | 51,645 `7d43a2eaad4e287f` LF | same | IDENTICAL (today) |
| arena_operator_field.html | 12,288 `a2517e002e2aaef3` LF | same | IDENTICAL (today) |
| arrakis.html | 11,495 `1383139718ed9c4d` LF | same | IDENTICAL (today) |
| rounds_real.json | 19,986 `2cbfef760864ccae` CRLF | same | IDENTICAL (today) |
| toy.html | MISSING | 12,919 `ca4c18beebffdb56` LF | canonical-only (correct) |
| frontier_souls.html | MISSING | 84,785 `ffa1e4dbb0cce304` LF | canonical-only (correct) |

The four "IDENTICAL today" pairs match G1's warning: accident of timing, not a rule — mud proves the drift mechanism.

## Step 2 — what live code actually loads (path census)

| surface | loads | implication |
|---|---|---|
| `scripts/playtest_swarm.js:9` | `dashboard/static/swarm.html` (STALE path) | retarget to `dashboard/static/games/swarm.html` |
| `dashboard/static/nav.js` (lines 8, 11, 17, 68, 70, 81) | `/static/maze_arena.html`, `/static/arrakis.html`, `/static/arena_operator_field.html` | top-level copies are LIVE-LINKED → must continue to exist as regenerated canonical copies (not deleted) |
| `dashboard/static/home.html` (×4) + `incident_dungeon.html` (×2) + `read_receipts.json` telemetry | `/static/maze_arena.html`, `/static/arrakis.html`, `/static/arena_operator_field.html` | same |
| top-level `/static/mud.html`, `/static/swarm.html` | **zero live links** (only prose mentions in `grounding_wave.md` evidence strings) | safe to regenerate from canonical; nobody depends on stale-mud behavior |
| `vislab/catalog.html` DEPLOYED GAMES launches | `/static/games/*` (canonical) | already canonical-facing |
| `site/build.py:29` GAMES | canonical `dashboard/static/games/<g>` → `site/dist/games/` | **GAMES list missing `toy.html` + `frontier_souls.html`** — root cause of toy's catalog absence; frontier_souls reached dist only via a manual copy (would be lost on next `site/build.py` rmtree rebuild) |
| `scripts/build_vislab_catalog.py sync_games()` | `site/dist/games/*.html` → `dashboard/static/games/` + DEPLOYED GAMES bucket | catalog entries are derived from the dist build |

Derived chain (the law in code): canonical `dashboard/static/games/` → `site/build.py` → `site/dist/games/` → `sync_games()` → canonical + catalog. Verified `site/dist/games/` is byte-identical to canonical for all 6 shared files today (mud 100,832 `468b884be6891a2d` matches) — the sync is a safe no-op byte-wise.

**Flag-or-regen verdict:** no stale copy is referenced by live code with different behavior → the flag-instead-of-delete branch does NOT trigger for any of the 5. All 5 top-level game copies get regenerated from canonical; the 3 nav-linked ones must exist for nav.js/home.html/incident_dungeon.html.

## Step 3 — regeneration / flag decisions

Source edits (Write/Edit tool only):
1. `site/build.py:29` — GAMES deploy list `["maze_arena","arrakis","arena_operator_field","mud","swarm"]` → **added `"toy.html"`, `"frontier_souls.html"`**. Root-cause fix: toy could never reach the catalog (it rides canonical → `site/dist/games/` → `sync_games()` → DEPLOYED GAMES bucket), and frontier_souls only existed in dist as an untracked manual copy that the next `site/build.py` rmtree would have destroyed.
2. `scripts/playtest_swarm.js:9` — `path.join(REPO, "dashboard", "static", "swarm.html")` → `path.join(REPO, "dashboard", "static", "games", "swarm.html")`. The dogfood gate now validates canonical.

Derived-surface regeneration (plain byte copies, `.venv\Scripts\python.exe shutil.copyfile`, canonical → derived):
- `dashboard/static/{mud,swarm,maze_arena,arena_operator_field,arrakis}.html` ← `dashboard/static/games/*.html` (the 3 nav-linked ones keep working for nav.js/home.html/incident_dungeon.html; nothing depends on stale-mud behavior — verified by census).
- `dashboard/static/rounds_real.json` + `games/rounds_real.json` — synced from `site/dist/static/rounds_real.json` by `build_vislab_catalog.py sync_games()` (by-design data sync; not a catalog entry — it is data, per G1 inventory).
- `site/build.py` executed: rmtree + full rebuild of `site/dist` (14 pages, 7 games incl. toy + frontier_souls, rounds_real, suno, maze.html) — output verbatim in FINAL section.
- `scripts/build_vislab_catalog.py` executed (×3 over the lane; final at 21:13Z).

**Flagged, not fixed (out of FX2 scope, belongs to concurrent lanes):**
- CONCURRENT WRITER DETECTED: while this lane ran, another gen-2 lane edited `dashboard/static/games/swarm.html` in multiple saves (78,041 → 80,283 → 80,408 B; saves at ~17:06–17:12 EDT) implementing G1 fix-list items 1–2 (SAFE_STORAGE privacy-mode guard replacing 8 bare localStorage sites; AUDIO_BASES deploy-law audio loader so tracks resolve from `../suno/` + `suno/` under `/games/`). The same writer also edited `games/arena_operator_field.html` (12,288 `a2517e00` → 13,136 `19d54e4d`). FX2 re-synced all derived copies from the settled canonical and rebuilt downstream; the swarm lane should be told its edits were detected and honored.
- swarm gate retains PRE-EXISTING RNG flakiness (below) — G1 fix-list item 6 (seeded LCG port), not this lane.

## Step 4 — vislab catalog regen

Final `build_vislab_catalog.py` output: `catalog: 238 entries / 8 buckets / 110 health verdicts merged` — DEPLOYED GAMES bucket **5 → 7**. All 7 entries verified sha-exact against on-disk canonical (see FINAL section). mud entry fixed: was `sha:d778a7c5 / 33,415 B` (stale) → now `sha:468b884b / 100,832 B` (current). toy.html and frontier_souls.html entries now exist (`sha:ca4c18be`, `sha:ffa1e4db`).

## Step 5 — harness re-runs + syntax checks

- `node --check scripts/playtest_swarm.js` → OK (after edit).
- `.venv/Scripts/python.exe -m py_compile site/build.py` → OK (before executing it).
- `playtest_swarm.js` (canonical): 32/32 PASS ×3 on settled bytes; 1 run 31/32 (lane `necromancer raises learned dead | allies=0`) and 3 mid-edit runs 31/32 (lane `descend increments depth`) — see flakiness note in FINAL.
- `test_toy.js` 12/12 · `test_mud_fifty.js` 51/51 · `test_frontier_souls.js` 42/42 — all exit 0; toy/mud/frontier bytes unchanged since those runs (`ca4c18be`/`468b884b`/`ffa1e4db` in final snapshot match Step-1 shas), so the verdicts stand for current bytes. arena_operator_field changed under the concurrent lane and has no harness (G1 documented).

---

## FINAL: divergence table (before)

| file | dashboard/static/ (derived) | dashboard/static/games/ (canonical) | verdict before FX2 |
|---|---|---|---|
| mud.html | 31,348 B `da3651ab` CRLF (Sep 12) | 100,832 B `468b884b` LF (Sep 15) | **DIVERGED** — two live muds |
| swarm.html | 78,041 B `91c1db9a` | 78,041 B `91c1db9a` | IDENTICAL (timing accident) |
| maze_arena.html | 51,645 B `7d43a2ea` | same | IDENTICAL (timing accident) |
| arena_operator_field.html | 12,288 B `a2517e00` | same | IDENTICAL (timing accident) |
| arrakis.html | 11,495 B `13831397` | same | IDENTICAL (timing accident) |
| rounds_real.json | 19,986 B `2cbfef76` | same | IDENTICAL (timing accident) |
| toy.html | missing | 12,919 B `ca4c18be` | canonical-only; **no vislab entry** |
| frontier_souls.html | missing | 84,785 B `ffa1e4db` | canonical-only; **no vislab entry** |

## FINAL: regenerated vs flagged

**Regenerated (derived surfaces, plain byte copies from canonical):**
| surface | action |
|---|---|
| `dashboard/static/mud.html` | stale 31,348 B → canonical 100,832 B `468b884b` (the divergence fix) |
| `dashboard/static/swarm.html` | → canonical bytes; re-synced twice more after concurrent-writer saves; final 80,408 B `5b43a013` |
| `dashboard/static/maze_arena.html` | → canonical `7d43a2ea` (was already identical; derivation made explicit) |
| `dashboard/static/arena_operator_field.html` | → canonical `19d54e4d` 13,136 B (picked up the concurrent lane's edit) |
| `dashboard/static/arrakis.html` | → canonical `13831397` |
| `dashboard/static/{,games/}rounds_real.json` | synced via catalog builder, pair-identical `2cbfef76` |
| `site/dist/` | full `site/build.py` rebuild from canonical (now includes toy + frontier_souls in games/) |
| `vislab/catalog.{html,json}` | regenerated ×3 (final 21:13:08Z) |

**Flagged (not fixed here):**
1. Concurrent gen-2 swarm lane editing canonical `games/swarm.html` (SAFE_STORAGE + AUDIO_BASES = G1 items 1–2) and `games/arena_operator_field.html` — detected mid-lane, honored, derived surfaces re-synced to its settled output. No live code was pointed at stale behavior at any point (nav/home/incident paths all carry canonical bytes now).
2. swarm gate RNG flakiness — pre-existing G1 replay-law violation (31 unseeded Math.random sites); fix is G1 item 6 (LCG port), unchanged by FX2.
3. `vislab` health.json not re-swept (110 verdicts merged as-is) — `scripts/sweep_vislab_health.py` is a separate lane's tool.

**Edits made (source, via Write/Edit):** `site/build.py` GAMES list (+toy, +frontier_souls) · `scripts/playtest_swarm.js:9` (retarget to canonical). No deletions — all five derived copies remain because nav.js/home.html/incident_dungeon.html live-link them.

## FINAL: vislab catalog state after

```
catalog: 238 entries / 8 buckets / 110 health verdicts merged
  DEPLOYED GAMES   7        (was 5)
  ENGINE           35
  GAME DOCTRINE    12
  GAME MODULES     7
  PROMPT LIBRARY   27
  RIDDLER WING     29
  SHADERS          7
  VIZ DECKS        114
generated: 2026-09-16T21:13:08Z
```

DEPLOYED GAMES bucket, verified sha-exact against on-disk canonical:

| title | path | bytes | version | check |
|---|---|---|---|---|
| mud | dashboard/static/games/mud.html | 100,832 | sha:468b884b | OK (was stale `d778a7c5`/33,415) |
| swarm | dashboard/static/games/swarm.html | 80,408 | sha:5b43a013 | OK (post-concurrent-edit bytes) |
| maze arena | dashboard/static/games/maze_arena.html | 51,645 | sha:7d43a2ea | OK |
| arena operator field | dashboard/static/games/arena_operator_field.html | 13,136 | sha:19d54e4d | OK (post-concurrent-edit bytes) |
| arrakis | dashboard/static/games/arrakis.html | 11,495 | sha:13831397 | OK |
| **toy** | dashboard/static/games/toy.html | 12,919 | sha:ca4c18be | **NEW ENTRY** (was orphaned) |
| **frontier souls** | dashboard/static/games/frontier_souls.html | 84,785 | sha:ffa1e4db | **NEW ENTRY** (was orphaned) |

All launch paths are `/static/games/*` (canonical). rounds_real.json intentionally has no DEPLOYED GAMES entry (data, not a game — same as G1 inventory); pair-identical in both locations.

## FINAL: harness outputs verbatim

```
$ node --check scripts/playtest_swarm.js
NODE_CHECK_PLAYTEST_OK            (exit 0)

$ .venv/Scripts/python.exe -m py_compile site/build.py
PY_COMPILE_OK                     (exit 0)

$ node scripts/playtest_swarm.js        # retargeted: dashboard/static/games/swarm.html, settled bytes
=== the-pass ===
PASS  entered the pass
PASS  riding the mountains  | dist=140
PASS  pass exits to deeper maze  | state=play depth=2
PASS  pass-exit: camera locked on player  | camX=-256.2 px=410.4
PASS  pass-exit: player in world  | x=410
PASS  pass-exit: no NaN in player  | hp=99999
PASS  pass-exit: entities finite  | en=0 gems=0

=== death+bonfire+charcoal ===
PASS  death happens  | state=dead
PASS  charcoal marks the death  | 0->1
PASS  bonfire souls banked  | bank=0

===== DOGFOOD VERDICT: 32/32 =====
EXIT=0

  (repeats on settled bytes: 32/32 EXIT=0; 32/32 EXIT=0; 31/32 EXIT=1
   FAIL  necromancer raises learned dead  | allies=0   <- pre-existing RNG flake, different lane each miss)

$ node scripts/test_toy.js
12/12 lanes green
toy: 232 lines, seed 20260916, tape A sha 678ddd9d2e189555…, verdict win, duration 1.717s
EXIT=0

$ node scripts/test_mud_fifty.js
PASS 51 M: fuse replaces the champion (no double boss)
51/51 lanes green
EXIT=0

$ node scripts/test_frontier_souls.js
PASS 42 his presence withers: the timer bleeds faster in close
42/42 lanes green
EXIT=0

$ .venv/Scripts/python.exe site/build.py        (final run, tail)
built games/toy.html
built games/frontier_souls.html
built static/rounds_real.json
built suno/flat_beat_loop.mp3
built suno/gift_track.mp3
built suno/jsr_loop.mp3
built suno/hemisync_loop.mp3
built maze.html
dist ready: C:\Users\foste\Documents\projects\local_sovereign_agent\site\dist

$ .venv/Scripts/python.exe scripts/build_vislab_catalog.py
catalog: 238 entries / 8 buckets / 110 health verdicts merged
wrote ...\dashboard\static\vislab\catalog.json and ...\dashboard\static\vislab\catalog.html
```

Flakiness evidence trail (for the next lane): the three mid-edit 31/32s all failed `descend increments depth`; after the concurrent writer settled, 15/15 clean runs against the OLD pre-edit bytes (temp harness, outside repo) vs mixed results against canonical while it was being saved — i.e. the early misses were edit-contention artifacts. On final settled bytes: 3× 32/32 and 1× 31/32 with a different lane missing (`necromancer raises learned dead`) — consistent with the G1-documented 31 unseeded Math.random sites, not with the retarget (old/new paths were byte-identical when retargeted; the game JS is byte-extracted).

— FX2 lane complete. Surfaces reconciled under the C5 law (games/ canonical, static copies derived). No git commands. Receipt closed 2026-09-16.
