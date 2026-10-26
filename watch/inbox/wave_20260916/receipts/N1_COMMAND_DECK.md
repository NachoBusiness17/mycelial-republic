# N1 — COMMAND DECK (deck.html)

**Wave:** 2026-09-16 · **Lane:** N1 · **Mission:** remake the static dashboard into `deck.html` — a command deck representing what the fleet IS now, mined from real data files. Self-contained (one HTML file, embedded data, no server deps), regenerable via `scripts/build_deck.py`.

**Law compliance:** receipt filed first, appended as work proceeds. No mutating git commands. Source written via Write/Edit. Python via `.venv\Scripts\python.exe` only.

---

## PHASE 2 — SPEC (section list, written before building)

The deck renders these sections, top to bottom:

1. **STANDING WAVE** — grounding-wave verify line + wave trajectory (era, pour state).
2. **PROGRAMS** — 6 cards:
   - Referee chain (Sep-20 gates)
   - Cube program (GO-pending + stage-0 date)
   - Ractor plugin (publish checklist state)
   - Physical pack
   - World build (M0–M5)
   - Myco-memory ladder
3. **LIVE LANES** — per-lane status from `queue/lanes/*/runner_state.json` + trail tails.
4. **RECEIPTS** — latest 8 with dates.
5. **LEDGERS** — counts + claim statuses (incl. sampler = CONDITIONAL-REFUTED pending closure).
6. **SURFACES** — links to all 7 games + vislab + estate walk/lod + pipeline + catalog.
7. **NEXT STONES** — from WAVE_STATE gen-2 requeue + operator gates.

Build target: `dashboard/static/deck.html` (one file, dark instrument aesthetic consistent with estate, embedded JSON data block, zero external deps, works from `file://` AND `/static/deck.html`). Builder: `scripts/build_deck.py`, same pattern as `_build_estate_walk.py`.

---

## PHASE 1 — MINING LOG

| Source | Live values pulled |
|---|---|
| `WAVE_STATE_20260916.md` | 60 receipts indexed (35 wave + 25 physical); gen-2 requeue §4 (G2, G3, G1, X_MINE_FIGURES verdict, 0-byte W1 draft, misfiled usage json, B13 defect, D20 gates, fossil headers, D23 50/50 fossil); salon_50 = **39/50** (fossil fix); counts §5 |
| `PHYSICAL_COMPUTING_PACK_20260916.md` | §4 falsifiers 1–4 + §4.5 (physical artifact gate); §6 folds: red-team grade A $0, free salon 25 calls, ESS probe ρ=+0.167 p=0.70 wrong-signed → replicate ρ=+0.327 n=36 p=0.052; U5 witness: **CONDITIONAL-REFUTED pending formal closure**; Landauer ceiling 1.05e13 STRUCK; C15 verdict PARTIAL-SUPPORT OPTIMISTIC-EDGE; C19 dozen-cubes → dozen-cards; Extropic Z1 140× replication seat OPEN |
| `queue/lanes/*/runner_state.json` + `trail.jsonl` | 11 lanes (table in embedded deck data); all ran 2026-09-16 except `night` (09-15 23:01, march rc=1) and `android_surface` (dormant since 09-04, no runner_state); research 1178 trail rows, day_work 849 |
| `watch/inbox/LINKS.jsonl` | **174 rows**; last 5: PMC7972235, PMC9673936, PMC10259323, seangoedecke JEV post, HN item 49717558 (matches LINKS_JEV 172→174) |
| `watch/GROUNDING_WAVE.jsonl` | 124 rows; `python -m mag.grounding_wave verify` → **FAIL row 122: prev-hash mismatch (chain broken)** |
| `memory/context_pack_latest.md` | mode=full 2026-09-16T21:20:31 · tip 7a309e6da98d… · leaves=8467 · knot 2026-09-16_2117_mag_mag-agen_06abc420 |
| `C17_CUBE_INSTRUMENT_PLAN.md` | Status: FILED 2026-09-16 — plan complete, proposal tier (two-eyes pending); echo-state FIRST, then binary discrimination vs noise (n=100, α=0.05) |
| `CUBE1_SHOPPING_LIST.md` | Stage 0 = electronics only ~$31 (ESP32 + 2×ADS1115 + Ag/AgCl electrodes); assembly proposed **2026-09-22** (fallback 09-29); stage 1 biology $20–24 only after clean floor; skeptic rider → $45–60 with defenses |
| `mag.shared_surface validate` | ok=**False** · files 444 · indexed 140 · unindexed 389 · errors 98 · warnings 1 |
| `git log -5 --oneline` | 0f34a8f3e wave checkpoint · 5305a99b1 physical pack checkpoint · 132eef87f session close · 32e2a8849 dream-rsi verified · 2b84b8cce mesh audit fixes |
| `HERMES_DIRECTIVE_BONES_REFEREE_20260916.md` | **Sep-20 gate:** BONES AS THE REFEREE — NT-ACv2 gets a game by Sep-20; end-to-end demo a stranger can watch from a phone; scope freezes: M0 only until demo ships |
| `D20_BONES_ADAPTER.md` | Sep-20 critical path; code landed, **operator-blocked**: rotate DISCORD_BOT_TOKEN + grant #game-c-overview (403 Missing Access) |
| `WOW_CLONE_BETA_BLUEPRINT_20260916.md` | M0 bones-world skeleton (LANED: W1 wow_world.py, atrium-ring) · M1 authoritative room server · M2 player files (LANED: W2 wow_player.py 17/17, byte-identical resume) · M3 zone/enemy/loot · M4 /play Discord · M5 fifty-wide playtest |
| `DESIGN_MYCO_MEMORY_20260916.md` | Pyramid: registers / VRAM (reservoir fading memory, capacity 0.048–0.209 Telhan 2026) / disk (hyphal remodeling) / archive (sclerotia); Steps 0–5: ear → read test → first write → addressing → filesystem → mount; every step fleet-consumed; retreat to "physical altar" armed |
| `P1_RACTOR_PACKAGE.md` + `U9` | Standalone repo `../ractor-salon` (plugin.json, pyproject, src, tests, CI 3.9–3.12, MCP stdio server per U9); publish checklist is **OPERATOR-executed**: venv tests → git init+tag → gh auth → repo create/push/release → catalog PR vs `NousResearch/hermes-agent` → optional PyPI + examples/ |
| `dashboard/static/games/` | exactly 7 games: arena_operator_field, arrakis, frontier_souls, maze_arena, mud, swarm, toy |
| receipts by mtime | latest 8 (excl. this one): FX2_SURFACE_RECONCILE, FX3_SHADER_FIXES, FX1_SWARM_STORAGE_AUDIO, R1_SWARM_RESEARCH, U9_UNION_MCP_SERVER, R2_GAME_SUBSYSTEM_GAPS, C17_CUBE_INSTRUMENT_PLAN, G3_SHADER_AUDIT — all 2026-09-16 |

**Note on git:** wave law says "no git" (writes); the mission's mining list explicitly asks for read-only `git log -5 --oneline`, which was run read-only. No mutating git commands used.

---

## PHASE 2 — SPEC CONFIRMED

Sections (final): STANDING WAVE · PROGRAMS (6 cards) · LIVE LANES · RECEIPTS (latest 8) · LEDGERS · SURFACES · NEXT STONES. Aesthetic mirrors estate_walk (`#07090d`, ui-monospace, muted blue-grays, lane colors from `_build_estate_walk.py`: research #6fd6ff, day_work #fff2c8, builder #8dff7a, forge #ff7a4d, bard_ledger #c98bff, elder #ffb347). Builder `scripts/build_deck.py` embeds a regenerable `window.DECK_DATA` JSON block; zero external deps; works from `file://` and `/static/deck.html`.

*(build + verification appended below)*

---

## PHASE 3 — BUILD

- **Deck:** `dashboard/static/deck.html` — **32,571 bytes** (final build 2026-09-16T21:29Z + §5-regex fix), one self-contained file, zero external deps, works from `file://` and `/static/deck.html`. Dark instrument aesthetic (estate palette: `#07090d`, ui-monospace, lane lantern colors from `_build_estate_walk.py`). All sections render client-side from an embedded `window`-independent `<script id="deck-data" type="application/json">` block (`</` escaped as `<\/` so the block can never break out).
- **Builder:** `scripts/build_deck.py` (stdlib only) — same pattern as `_build_estate_walk.py`: run it, get a fresh surface. Mines live values at build time: lane states from `queue/lanes/*/runner_state.json` + `trail.jsonl`, LINKS/GROUNDING row counts, runs `python -m mag.grounding_wave verify` and `python -m mag.shared_surface validate` as subprocesses, parses program status lines out of C17/shopping-list/blueprint/P1 receipts, latest-8 receipts by mtime, git log, context-pack tip/leaves, and existence-checks every surface link at build time (missing links render with a `MISSING` flag).
- **Bug caught during build #1:** first pass returned the HTML template before the `__DATA__` injection ran (dead code after `return`) — deck shipped with the placeholder. Fixed; rebuild verified clean.
- **Bug caught during verify #2:** WAVE_STATE §5 lines are markdown-bold (`**Receipts indexed:** 60`), so the first regex missed them and the KPI rendered "?" — regex fixed to allow `\**`, rebuild confirms `receipts_indexed: 60` + requeued summary parses clean. Post-fix re-verified: `node --check` OK, all links still resolve, verify line intact.

## PHASE 4 — VERIFICATION (real numbers)

- Builder runs clean: `deck written: …\dashboard\static\deck.html (32629 bytes) · lanes=11 receipts=8 links_rows=174 verify=FAIL row 122: prev-hash mismatch (chain broken)`
- `node --check` on the extracted inline script: **OK**
- Link resolution: every embedded game/surface/receipt/program-source path checked against disk → **NONE missing**
- Spot-checks (10) against mined values:
  1. LINKS rows = 174 ✓ (matches `wc -l`)
  2. GROUNDING verify = "FAIL row 122: prev-hash mismatch (chain broken)", rows = 124 ✓
  3. git tip = `0f34a8f3e` ✓
  4. INDEX health = ok False · 444 files · 140 indexed · 389 unindexed · 98 errors · 1 warning ✓
  5. Cube status = "FILED 2026-09-16 — plan complete, proposal tier (two-eyes pending)." ✓ (C17 line byte-match)
  6. Milestones M0–M5 parsed from blueprint ✓ · requeue rows = 10, next stones = 16 ✓
  7. Games = exactly 7 (TOY, MUD, MAZE ARENA, SWARM, ARRAKIS, FRONTIER SOULS, OPERATOR FIELD) ✓
  8. Lane states: 10 LIVE + android_surface NO-RUNNER ✓ (night borderline-live at 22.5h, by the ≤24h rule)
  9. **Liveness proof:** between my manual mining pass and the build, parallel lanes landed new receipts (G-I_PRINTABLE_FAB, G-B_SPECIES_DATA, G-F_SPINOR_LATTICE, GA_SIGNAL_MAGNITUDE, G-E_FLUID_LOGIC_LIBRARY, G-H_COCULTIVATION, G-D_WRITE_MECHANISMS, G-J_INSTRUMENT_TIER) and the context-pack tip moved (`7a309e6da98d…`/8467 leaves → `847f32689ef3…`/8468). The deck's latest-8 and standing-wave KPIs picked both up — it is a REFRESH command, not a snapshot.
- Temp verify files (`scripts/_verify_deck.py`, `scripts/_deck_verify.js`) deleted after the pass; re-verify = rebuild + `node --check`.

**Builder command:** `.venv\Scripts\python.exe scripts\build_deck.py`

---

## The one data source I wish existed (for the next fold)

**A machine-readable program-state ledger** (`watch/inbox/PROGRAMS.json` or `queue/PROGRAM_STATE.jsonl`): one row per program (referee/cube/ractor/pack/world/myco) carrying `{status, gate, updated, sources[]}` that lanes append to when a receipt moves a program. The deck's weak point is that program state lives only in prose — the builder regex-scrapes status lines out of C17, the shopping list, the blueprint, and P1 (a heading-format change silently degrades a card to "unreadable", which is at least visible). Lane liveness, ledgers, and receipts are all bytes-first; programs are the one section still mining prose. Second runner-up: a `grounding-wave repair` status the verify command exposes (row 122 is broken; nothing says who is on it).
