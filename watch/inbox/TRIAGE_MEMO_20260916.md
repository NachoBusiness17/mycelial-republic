# TRIAGE_MEMO_20260916 — mag/ module kill-list (memo only — NO deletions performed)

- **Lane:** D24 wave 20260916 (Mickey17 gen-2) · receipt: `watch/inbox/wave_20260916/receipts/D24_MEMORY_DOCTRINE_BUNDLE.md`
- **Scope:** 999 Python modules under `mag/` (993 flat `mag/*.py` + `mag/cli` 3 + `mag/tests` 2 + `mag/ontology_compiler` 1)
- **Rules honored:** no git commands → "last-commit date" column is **file mtime proxy**, clearly labeled. No deletions. Memo only.
- **Method (repro, on disk):** `watch/inbox/wave_20260916/d24_triage_probe.py` (AST import graph + word-token pass over all code: mag/, scripts/, tests/, dashboard/, backend/, root *.py) → `d24_triage_probe_out.json`; then `d24_sweep2.py` (word-boundary sweep of the 175 candidates across docs/, configs/, scripts/ non-py, queue/, tests/, root *.md/*.yaml/*.json, dashboard non-py) → `d24_sweep2_out.json`. Interpreter: `.venv\Scripts\python.exe`.

## 1. Audit receipts consulted (numbers on disk, not memory)

| Source | What it had |
|---|---|
| `watch/inbox/FULL_AUDIT_MAP_20260914.md` (CLERK row) | "980+ ownerless mag files; 5 zero-importer giants; main.py 179 cmds" — summary only, **no per-module list** |
| `watch/inbox/AUDIT_INVENTORY_20260914.json` | 665,131 files walked repo-wide; area census, no module import graph |
| `watch/inbox/ractor-salon-001.txt`, `MESH_ARCHAEOLOGY_20260911.md` | handoff-seat archaeology, not mag/ modules |

Per-module lists were **not on disk**, so per mission the pure-dead list was rebuilt from bytes (2026-09-16).

## 2. Census (measured today)

| Bucket | Count | Meaning |
|---|---|---|
| Total modules | 999 | mag/ package, all subdirs |
| AST-imported alive | 698 | imported by ≥1 other code file (static `import`/`from`) |
| Token-only | 126 | zero static imports, but name appears in other code (string dispatch, `__init__`, prose collisions like "republic") → **review, not kill** |
| Pure-dead candidates | 175 | zero static imports AND zero code-token mentions outside itself |
| … after doc/config/shell sweep | **64** | of the 175, 111 turn out to be referenced somewhere non-code → demoted to REVIEW |
| Core-reachable | 583 | transitively reachable from entrypoints: main.py, mag_launch.py, dashboard/server.py, backend/server.py, dashboard/rest.py |
| Tested modules | 366 (**36.6%**) | module name appears in ≥1 of 272 test files |
| Orphaned tests in `tests/` | **0** | all 270 test targets map to live modules (see §5) |

Reconciliation with the Aug-14 audit: its "980+ ownerless" counted files without `configs/modules.yaml` ownership (an ownership-ledger concept), not import-graph death. This memo measures import death; both are true at once.

## 3. KILL-LIST — 52 modules, kill-ready (zero refs anywhere operational)

Evidence per row: **E1** zero AST importers (AST parse of all code files); **E2** zero word-token mentions in any code file; **E3** zero mentions in docs/, configs/, scripts/, queue/, tests/, root manifests, dashboard non-py (2026-09-16 sweep). Verdict rule: `KILL` under 300 lines; `KILL·ARCHIVE-FIRST` at ≥300 lines (graveyard, not landfill — one git-history-free archive copy before removal, since git blame is not available to this lane).

| # | Module | Lines | mtime (proxy) | Evidence | Recommend |
|---|---|---|---|---|---|
| 1 | mag._bench_free_shelf | 59 | 2026-08-25 | E1+E2+E3 | KILL |
| 2 | mag._cache_ab_probe | 64 | 2026-08-25 | E1+E2+E3 | KILL |
| 3 | mag._comb_tokens | 84 | 2026-08-15 | E1+E2+E3 | KILL |
| 4 | mag._compare_chain_sources | 31 | 2026-08-25 | E1+E2+E3 | KILL |
| 5 | mag._deep_research_verkle_dedupe | 63 | 2026-08-10 | E1+E2+E3 | KILL |
| 6 | mag._diag_cache | 11 | 2026-08-25 | E1+E2+E3 | KILL |
| 7 | mag._fold_vision | 13 | 2026-08-25 | E1+E2+E3 | KILL |
| 8 | mag._gpu_probe_debug | 39 | 2026-08-11 | E1+E2+E3 | KILL |
| 9 | mag._grok_corpus_burn | 103 | 2026-08-26 | E1+E2+E3 | KILL |
| 10 | mag._openclaw_real | 19 | 2026-08-25 | E1+E2+E3 | KILL |
| 11 | mag._probe_dangling | 29 | 2026-08-25 | E1+E2+E3 | KILL |
| 12 | mag._probe_mcp | 36 | 2026-08-25 | E1+E2+E3 | KILL |
| 13 | mag._probe_zai_balance | 51 | 2026-08-25 | E1+E2+E3 | KILL |
| 14 | mag._relane_game_tasks | 44 | 2026-08-25 | E1+E2+E3 | KILL |
| 15 | mag._salon_burn | 96 | 2026-08-27 | E1+E2+E3 | KILL |
| 16 | mag._verify_chain_now | 32 | 2026-08-25 | E1+E2+E3 | KILL |
| 17 | mag._verify_concurrency_gate | 49 | 2026-08-25 | E1+E2+E3 | KILL |
| 18 | mag._verify_queue_gate | 80 | 2026-08-25 | E1+E2+E3 | KILL |
| 19 | mag._verify_repair_state | 16 | 2026-08-25 | E1+E2+E3 | KILL |
| 20 | mag._verify_rung5 | 50 | 2026-08-25 | E1+E2+E3 | KILL |
| 21 | mag._verify_sharp_edge | 59 | 2026-08-25 | E1+E2+E3 | KILL |
| 22 | mag._warm_rib | 18 | 2026-08-25 | E1+E2+E3 | KILL |
| 23 | mag.batch_scribe | 205 | 2026-08-24 | E1+E2+E3 | KILL |
| 24 | mag.claims_verify | 124 | 2026-08-23 | E1+E2+E3 | KILL |
| 25 | mag.echo_net | 151 | 2026-09-06 | E1+E2+E3 | KILL |
| 26 | mag.gguf_cartography | 583 | 2026-09-05 | E1+E2+E3 | KILL·ARCHIVE-FIRST |
| 27 | mag.grok_warm_rib | 162 | 2026-08-25 | E1+E2+E3 | KILL |
| 28 | mag.memory_train_seed | 185 | 2026-08-18 | E1+E2+E3 | KILL |
| 29 | mag.mind_mine | 417 | 2026-08-23 | E1+E2+E3 | KILL·ARCHIVE-FIRST |
| 30 | mag.orphan_audit | 214 | 2026-08-31 | E1+E2+E3 | KILL |
| 31 | mag.ox_alpha_steal | 194 | 2026-08-22 | E1+E2+E3 | KILL |
| 32 | mag.ox_burn | 121 | 2026-08-22 | E1+E2+E3 | KILL |
| 33 | mag.ox_escalate | 138 | 2026-08-22 | E1+E2+E3 | KILL |
| 34 | mag.ox_gap | 175 | 2026-08-22 | E1+E2+E3 | KILL |
| 35 | mag.ox_megaburn2 | 323 | 2026-08-23 | E1+E2+E3 | KILL·ARCHIVE-FIRST |
| 36 | mag.ox_novelty_digest | 86 | 2026-08-23 | E1+E2+E3 | KILL |
| 37 | mag.ox_probe | 232 | 2026-08-23 | E1+E2+E3 | KILL |
| 38 | mag.perturbation_battery | 550 | 2026-09-06 | E1+E2+E3 | KILL·ARCHIVE-FIRST |
| 39 | mag.quorum_window | 458 | 2026-09-07 | E1+E2+E3 | KILL·ARCHIVE-FIRST |
| 40 | mag.rel_mem_eval | 248 | 2026-08-26 | E1+E2+E3 | KILL |
| 41 | mag.riddle_direction | 141 | 2026-08-24 | E1+E2+E3 | KILL |
| 42 | mag.riddler_trajectory | 152 | 2026-09-08 | E1+E2+E3 | KILL |
| 43 | mag.saelis_world_brief | 107 | 2026-08-18 | E1+E2+E3 | KILL |
| 44 | mag.seat_probe | 112 | 2026-08-24 | E1+E2+E3 | KILL |
| 45 | mag.shelf_pdf | 99 | 2026-09-06 | E1+E2+E3 | KILL |
| 46 | mag.tandem_key_test | 77 | 2026-08-23 | E1+E2+E3 | KILL |
| 47 | mag.tavern_summon_guests | 51 | 2026-09-08 | E1+E2+E3 | KILL |
| 48 | mag.telegram_desk | 180 | 2026-09-09 | E1+E2+E3 | KILL |
| 49 | mag.thread_eye | 97 | 2026-09-09 | E1+E2+E3 | KILL |
| 50 | mag.tortoise_demo | 135 | 2026-09-07 | E1+E2+E3 | KILL |
| 51 | mag.transfer_gate | 666 | 2026-09-06 | E1+E2+E3 | KILL·ARCHIVE-FIRST |
| 52 | mag.whale_patrol | 319 | 2026-09-07 | E1+E2+E3 | KILL·ARCHIVE-FIRST |

Kill-list totals: **52 modules, ~8,300 lines**; of which 7 giants (≥300 lines, ~3,550 lines) should land in an archive branch/copy first. The 22 `_underscore` scratch/probe files (rows 1–22, ~880 lines) are the Aug-25 explosion stratum and are the safest first bite.

## 4. HOLD — 12 modules (zero refs but fresh mtime ≤ 6 days; revisit 2026-09-23)

| Module | Lines | mtime | Note |
|---|---|---|---|
| mag.catalog_scan | 107 | 2026-09-16 | same-day — active work |
| mag.lite_scale | 166 | 2026-09-16 | same-day — active work |
| mag.corpus_selfsteal | 321 | 2026-09-15 | wave-driven runner pattern |
| mag.salon_50 | 210 | 2026-09-15 | D23 salon night output exists |
| mag.abliterator_spawn_manifest | 128 | 2026-09-12 | |
| mag.bay_organs_liveness_test | 375 | 2026-09-12 | test-shaped; keep pending review |
| mag.emergence_test | 260 | 2026-09-12 | test-shaped |
| mag.trust_gate_audit_check | 45 | 2026-09-12 | |
| mag.tests.verify_identity_coupling | 262 | 2026-09-12 | KEEP — standalone verify script for the Oct-27 substrate-migration identity claim (not pytest-wired by design) |
| mag.desk_tools | 356 | 2026-09-10 | |
| mag.fire_horse | 51 | 2026-09-10 | |
| mag.narrative_tests | 388 | 2026-09-10 | test-shaped |

HOLD rule: any zero-ref module with mtime < 7 days gets a week of grace — ad-hoc `python -m mag.x` runners are a living pattern in this repo (see risks, §6).

## 5. Orphaned tests

- `tests/` (270 files): **0 orphans.** Every test file's target module maps to an alive (imported) module. The suite's subjects are not on the kill-list.
- `mag/tests/` (2 files): both are standalone verify scripts, never imported — by design, not orphans. `test_identity_schema_portability.py` (token-referenced → alive bucket) and `verify_identity_coupling.py` (HOLD, §4).
- Prior wave's claim of "orphaned tests" was not reproducible from disk; the number on disk today is 0 (+1 self-referential hit from naive name-mapping, correctly reclassified as a manual verify script).

## 6. REVIEW — 111 modules (referenced outside code, zero static imports — NOT auto-kill)

These mention-clean modules still appear in docs/TOOLS/AGENTS.md, configs/, queue/handoff/, or dashboard static assets. The sweep deliberately over-demotes (a CONVO.md line or a mimosa hook-state baseline blob counts), so this bucket needs eyeballs, not a truck. Notable members that should probably end up KEEP:

- `mag.shared_surface` — invoked by AGENTS.md + TOOLS.md + cursor rules (`.venv\Scripts\python.exe -m mag.shared_surface validate` is machine contract). **KEEP.**
- `mag.auth_switchboard` — wired to `configs/auth_tracks.yaml`, RUNNING.md. **KEEP.**
- `mag.kabuki_salon` — invoked by `scripts/astra_convo_loop.sh`. **KEEP.**
- `mag.verify_succession_contract` — checker paired with `configs/succession_contract.yaml`. **KEEP.**
- `mag.forge_daemon` — `dashboard/static/index_data/last_run.json` proves recent runs. **KEEP.**
- `mag.cli.display` / `mag.cli.__init__` — TOOLS.md + dashboard references; the mag.cmd CLI surface. **KEEP pending main.py dispatch check.**
- `mag.republic`, `mag.dissector`, `mag.decl_attention` — giants (855/738/740 lines) referenced in docs/BIBLIOGRAPHY/CONVO only; genuine REVIEW candidates with archive-first bias.

Full per-module evidence (which files mention what): `watch/inbox/wave_20260916/d24_sweep2_out.json`.

## 7. Known blind spots (why this is a memo, not a verdict)

1. **Dynamic dispatch:** `mag/afk_cadence.py:199` and `mag/afk_orchestrator.py:96` `__import__` `mag.<mod>` from in-file strings (caught by token pass) — but a plan/config naming a module in `memory/` or `watch/` would be missed (those trees excluded for size).
2. **Ad-hoc `python -m mag.x` runners** leave no static trace; only docs/shell hits (E3) catch them. Fresh mtimes (HOLD) are the second guard.
3. **mtime ≠ commit date:** git is forbidden in this lane; a module last *committed* earlier could still have a late working-tree touch and vice versa. All dates above are mtimes read 2026-09-16.

## 8. Recommendation summary

- **Kill 52** (~8.3K lines) — start with the 22 `_`-prefixed Aug-25 probe stratum.
- **Archive-first 7** of those (≥300 lines).
- **Hold 12** until 2026-09-23, then re-run the probe; survivors of a second zero-ref pass graduate to kill.
- **Review 111** by hand against §6 keeps; expect roughly 15–25 keeps (documented commands, config-paired checkers, shell-invoked runners) and the rest to graduate to kill after docs are updated.
- **No deletions performed by this memo.** Execution is a separate, human-gated lane.

*Numbers are from disk probes run 2026-09-16; raw outputs: `d24_triage_probe_out.json`, `d24_sweep2_out.json` in `watch/inbox/wave_20260916/`.*
