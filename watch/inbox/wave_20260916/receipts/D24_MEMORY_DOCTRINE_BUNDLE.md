# D24 — MEMORY_DOCTRINE_BUNDLE receipt

- **Wave:** 20260916 (Mickey17 gen-2)
- **Lane:** memory/doctrine bundle, fifty-wide
- **Started:** 2026-09-16 · **Closed:** 2026-09-16
- **Status:** COMPLETE
- **Constraints honored:** no git commands (mtime used as date proxy, labeled), no paid APIs, `.venv\Scripts\python.exe` only, Write tool for memo.

## Plan

1. ITEM 1 — module triage memo: locate mesh-audit receipts, extract real counts; rebuild pure-dead list from disk; write `watch/inbox/TRIAGE_MEMO_20260916.md`. Memo only — NO deletions.
2. ITEM 2 — session cards spec: read 3 `.card.json` examples + spec mentions; canonical spec below.

## Log

- Receipt filed first (gen-2 law).
- Audit receipts located: `watch/inbox/FULL_AUDIT_MAP_20260914.md` (CLERK row: "980+ ownerless mag files; 5 zero-importer giants" — summary only, **no per-module list anywhere on disk**; `AUDIT_INVENTORY_20260914.json` is a 665,131-file area census; `MESH_ARCHAEOLOGY_20260911.md` is seat archaeology, not modules). Per mission: rebuilt the lists from bytes.
- Probe 1 (`d24_triage_probe.py` → `d24_triage_probe_out.json`): AST import graph + token pass over all code. Result: **999 modules** (993 flat mag/ — matches the mission number), **698 AST-alive, 126 token-only, 175 pure-dead candidates, 583 core-reachable** (from main.py/mag_launch/dashboard/backend entrypoints), **366/999 tested = 36.6% coverage**, 272 test files, orphaned tests **0** in `tests/`.
- Probe 2 (`d24_sweep2.py` → `d24_sweep2_out.json`): swept the 175 candidates across docs/, configs/, scripts/, queue/, tests/, root manifests, dashboard non-py. **111 demoted to REVIEW** (any non-code mention blocks a kill — incl. `mag.shared_surface` which AGENTS.md itself invokes), **64 remain zero-ref**.
- Classification: **52 KILL-ready** (~8.3K lines; 7 giants archive-first; 22 `_`-probe files of the Aug-25 stratum as safest first bite), **12 HOLD** (mtime ≤ 6 days, incl. 2 same-day files and the Oct-27 identity verify script), 111 REVIEW with named likely-keeps.
- Memo written via Write tool: `watch/inbox/TRIAGE_MEMO_20260916.md`. **No deletions performed.**
- ITEM 2: read 3 real cards + stub; found writer of record (`mag/session_card.py`, schema `session_card.v1`), theme scorer (`mag/session_dossier.py` THEME_KEYS), DNA chain (`docs/DNA.md`), trail lattice (`docs/ref/run_trail_lattice.md`), registry (3,581 rows, `mag_session_registry.v1`). The `cards/` dir is a **frozen 2026-08-07 backfill projection** of 2026-07-10..21 sessions (UUIDv7-decoded); no `.card.json` writer survives in the tree. Canonical spec below.

## ITEM 2 — Session cards canonical spec (approval-ready)

### What exists on disk (measured)

- `memory/biography/cards/`: **9 files** = 8 real `{uuidv7}.card.json` (all written 2026-08-07) + `latest.card.json` stub (`session_id:"latest"`, empty themes — a pointer, not a card).
- Card schema v0 (observed, all 8): `session_id`, `title` (= session_id — never humanized), `blurb` (always ""), `themes[]` of `{id, score, keys_hit}` sorted by `-score` — exactly `mag/session_dossier.py` build_dossier theme output.
- The **canonical card** today is the embedded `session_card` object (schema **`session_card.v1`**) inside `memory/biography/residual/{sid}.json`, built by `mag/session_card.py:build_session_card` and attached at session close (`mag/biography.py:summarize_session`, SessionEnd hook → residual + card + content_commit + chain leaf, per `docs/DNA.md`). Its fields: `schema, title, one_liner, blurb, bullets[], themes[](ids), dominant_theme, ask_count`.

### Canonical spec — `bio_card.v1` (proposes unifying the two)

**Identity & links (required):**
- `session_id` — UUIDv7; the sole join key. It resolves: residual `memory/biography/residual/{sid}.json` · dossier `{sid}.dossier.json` · hot row in `memory/biography/registry.jsonl` (`mag_session_registry.v1`) · chain leaf (`content_commit` blake2b_128 + leaf_hash) · trail runs (`run.json.parent = session_id`, `trail.jsonl` under the run, per run_trail_lattice.md §4: Card↔residual at session level).
- `schema` — literal `"bio_card.v1"`.
- `content_commit` — hex copied from the residual's commit block (proves the card is pinned to the same bytes).
- `created_at`, `source` (`session_end` | `backfill` | `amend`).

**Human payload (required):**
- `title` (≤100 chars, human-phrased; never the bare session_id — v0's flaw),
- `one_liner` (≤100), `blurb` (≤600, noise-filtered per `session_card._NOISE_MARKERS`, with meta suffix "N operator turns, ~M min"),
- `bullets[]` (2–7; operator asks only, stock-dossier moves as fallback),
- `themes[]` (ids from `mag/session_dossier.py:THEME_KEYS`, ≤5, score-ordered) + `dominant_theme`, `ask_count`.

**How a session earns a card:** session closes → SessionEnd hook → `summarize_session(sid)` → residual written → `build_session_card` runs on the dossier (chord, scalar_knot, time blocks present) → card embedded in residual + hot registry row → lean-complete = residual + card + content_commit + chain leaf. Sessions with no operator asks and <2 bullets still earn a minimal card ("Session recorded" class) — no silent gaps. Amendment re-runs `attach_card_to_dossier`; amend cannot strip `core` (DNA law).

**cards/ dir rule:** `memory/biography/cards/{sid}.card.json` is a **derived projection only** (browsable one-file-per-card), regenerable from residual via `session_card.recompute_all_cards()`. It is never the sole copy (shared-surface law). The 8 frozen 2026-08-07 cards are grandfathered as historical projections; `latest.card.json` stub should be regenerated or retired. Optional: backfill projection generation for the residual sessions that lack one.

**Trail link rule:** card ↔ trail is read-only: trails (`queue/…/run.json` + `trail.jsonl`) point UP via `parent = session_id`; cards never embed run ids (keeps card immutable while trails append).

**Spec approval-ready: YES** — pending operator gate; on approval, writer lands in `mag/session_card.py` (extend `build_session_card` to emit `bio_card.v1` + projection writer), keeping `mag_session_registry.v1` untouched.

## Footer

- **Memo path:** `watch/inbox/TRIAGE_MEMO_20260916.md`
- **Card count on disk:** 9 files in `memory/biography/cards/` (8 real cards + 1 `latest.card.json` stub)
- **Spec approval-ready:** YES (operator gate pending)
- **Artifacts filed:** `watch/inbox/wave_20260916/d24_triage_probe.py` + `d24_triage_probe_out.json` · `d24_sweep2.py` + `d24_sweep2_out.json` · memo · this receipt
