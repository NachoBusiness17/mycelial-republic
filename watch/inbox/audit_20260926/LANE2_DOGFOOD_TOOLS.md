# LANE 2 — DOGFOOD THE FLEET'S OWN TOOLS

**Date:** 2026-09-26 · **Repo:** `local_sovereign_agent` @ `6d417abd5` · **Host:** Windows, bash/MSYS
**Interpreter:** repo venv `./.venv/Scripts/python.exe` (CPython 3.11.15). Never bare `python`.
**Corpus:** 163 `tools/*.py` (excl. `__init__.py`) — 137 git-tracked, 26 untracked.
**Rule observed:** no mutation of the real tree except where noted in F-2 (the `--help` sweep, disclosed).

**Bottom line, numbers only**

| # | Finding | Number |
|---|---|---|
| F-1 | Tools that CRASH on their own `--help` | **8** |
| F-2 | Tools that HANG (>30s) on `--help` | **18** |
| F-3 | Tools with no CLI flag at all (`--help` = silent no-op, exit 0) | **58** |
| F-4 | DEAD tools (no code caller, no doc, no test, no hook) | **29** |
| F-5 | ORPHAN tools (documented, but no code caller) | **59** |
| F-6 | LIVE tools (called by other tracked code) | **75** |
| F-7 | Tools with a test in `tests/` | **20** of 163 (**12%**) |
| F-8 | Gates that **FAIL OPEN** on malformed input | **1 confirmed** (`freshness_check.py`) + 1 vacuous (`census_patrol_selftest.py`) + 1 misleading (`md_record_seal.py`) |
| F-9 | Tools that WRITE to the real tree when given only `--help` | **≥1 confirmed** (`drift_dashboard.py`) |

---

## PART A — RAN THE SELF-CHECK INSTRUMENTS

Every row is a real invocation. Exit code is the process exit status, captured with no pipe
(a pipe would mask `$?` — an early draft of this audit was wrong for exactly that reason).

### A.1 The named instruments

| # | Command (from repo root) | Exit | Verdict |
|---|---|---|---|
| 1 | `python tools/census_patrol_selftest.py` | **0** | **VACUOUS PASS — no `__main__` block. Ran 196 lines of assertions as an importable module and executed nothing. Zero output.** |
| 2 | `python tools/census_drift_patrol.py --self-test` | **0** | **CLEAN.** 29 `ok:` lines, `CENSUS-PATROL SELF-TEST: PASS`. Real assertions incl. fossil-carrier, order-poisoning, hook-pairing. |
| 3 | `python tools/census_drift_patrol.py` | **0** | **CLEAN.** `CENSUS-PATROL: ok - census 2026-09-26 (1910 collected / 303 files)`. |
| 4 | `python tools/capability_manifest.py --print` | **0** | CLEAN. 1,065 lines to stdout. |
| 5 | `python tools/capability_manifest.py` | **0** | CLEAN, **but WRITES** `memory/capability_manifest.md` (51,062 chars). |
| 6 | `python tools/violation_ratchet.py` | **2** | CORRECT — subcommand required. Exit 2 = "gate itself broken"/usage. |
| 7 | `python tools/violation_ratchet.py check` | **1** | **GATE FIRES.** `scope=1188 files, hits=882, registered=875, NEW=7` → `FAIL`. 7 real violations incl. 4× `silent except: pass` in `tools/`. |
| 8 | `python tools/freshness_check.py` | **0** | **PASSES — but see F-8, this pass is a fail-open.** |
| 9 | `python tools/freshness_check.py --self-test` | **0** | CLEAN but **mis-scoped**: 18 `ok:` lines, all on the *receipt* helper. **Zero coverage of `main()`** — the function that carries the fail-open. |
| 10 | `python tools/workflow_gate.py` | **2** | CORRECT — argparse error, `cmd` required. |
| 11 | `python tools/workflow_gate.py check --script MISSING` | **1** | Fail-closed: `GATE ERROR: cannot read script`. |
| 12 | `python tools/workflow_gate.py check --script GARBAGE.dwf.ts` | **2** | Fail-closed: all 7 scenario gates `FAIL` (G1…G7) on a garbage script. |
| 13 | `python tools/corpus_fts_rebuild.py --help` | **0** | **NO `--help` FLAG.** Ignored the flag, did the real work: `rows_indexed: 489548`, rebuilt a 134 MB SQLite FTS index. |
| 14 | `python tools/corpus.py --help` | **0** | **NO FLAG, ZERO OUTPUT.** Silent no-op. |
| 15 | `python tools/drift.py --help` | **0** | **NO FLAG, ZERO OUTPUT.** Silent no-op. |
| 16 | `python tools/corpus_diff.py --help` | **0** | CLEAN, has argparse. |
| 17 | `python tools/corpus_lens.py --help` | **0** | CLEAN, has argparse. |
| 18 | `python tools/corpus_self_lens.py --help` | **0** | Ignored `--help`; emitted bare `{`…`}` (4 lines) — malformed partial output, still exit 0. |
| 19 | `python tools/md_record_seal.py` | **0** | **MISLEADING.** Printed `md_record_seal: bad event json: Expecting value…` and **still exited 0**. A seal that cannot parse its input reports success. |
| 20 | `python tools/md_record_audit.py --help` | **0** | **NO FLAG + WRITES** — ran the real audit, `wrote MD_RECORD_AUDIT.json`. |
| 21 | `python tools/config_seal.py --help` | **0** | CLEAN, has argparse (`{verify,update}`). |
| 22 | `python tools/config_seal.py verify` | **1** | **GATE FIRES on the real repo**: `sealed=49 live=53 modified=6 missing=0 unsealed=4` → FAIL. 6 configs drifted from the seal. |
| 23 | `python tools/checkbox_receipt_gate.py --help` | **0** | CLEAN, has argparse. |
| 24 | `python tools/checkbox_receipt_gate.py` (in sandbox) | **1** | Fail-closed: `405 checked Open rows … 1 offenders` → FAIL. |
| 25 | `python tools/estate_atlas.py <sentinel>` | **0** | **IGNORES argv, does the real scan**: `ATLAS MINTED: 1,700,130 rows read in 29.8s` and **writes** `watch/ESTATE_ATLAS/`. |
| 26 | `python -c "import mag.shared_surface"` | **0** | Imports clean. **But `dir()` contains no validator entrypoint** — it exposes `MALFORMED_BASELINE`, `LINKS_LEDGER`, constants, not a callable gate. |

### A.2 The 163-tool `--help` sweep (bounded, 30s timeout, 8 workers)

Instrument: `rg`-free `subprocess` sweep, `cwd=repo`, venv python, `tools/<tool>.py --help`.

| Outcome | Count |
|---|---|
| `HAS_HELP` — real argparse usage text | **72** |
| `EXIT0_NO_USAGE` — **no flag, silently did the work or nothing** | **58** |
| `TIMEOUT` — hung >30s | **18** |
| `CRASH_ON_HELP` — traceback | **8** |
| `HELP_ERR` — non-zero, no usage | **7** |
| **Total** | **163** |

**F-1 — 8 tools crash on their own `--help`** (all `ModuleNotFoundError` / bad-path at import time):

| Tool | Exit | Traceback tail |
|---|---|---|
| `classify_pack.py` | 1 | `ModuleNotFoundError: No module named 'config'` |
| `code_execution.py` | 1 | `ModuleNotFoundError: No module named 'config'` |
| `filesystem.py` | 1 | `ModuleNotFoundError: No module named 'config'` |
| `shell.py` | 1 | `ModuleNotFoundError: No module named 'config'` |
| `topic_research.py` | 1 | `ModuleNotFoundError: No module named 'config'` |
| `smoke_import.py` | 1 | `ModuleNotFoundError: No module named 'dashboard'` |
| `kv50_smith_chart.py` | 1 | `FileNotFoundError: [Errno 2] No such file or directory: '--help'` |
| `seed_v2.py` | 1 | `OSError: [Errno 22] Invalid argument: '…\seed\engines\lite…'` |

The `no module named 'config'` family is a real defect, not a harness artifact: these five do
`import config` (bare top-level) which only resolves if CWD happens to hold a `config/`. Five of
the seventy-five "LIVE" tools are LIVE only because a caller injects CWD for them.

**F-2 — 18 tools hang >30s on `--help`:** `cold_boot_test`, `estate_atlas`, `full_scan`,
`gaming_corpus_pass`, `knot_taming_night`, `letter_salon_20260920`, `model_bakeoff`,
`ocean_v2_pilot`, `path_lint`, `quote_audit_wide`, `research_mine`, `rib_check_game_loop`,
`roblox_npc_gateway`, `saturation_fourcond`, `seed_salon`, `task_wall`, `x_churn_cli`,
`x_churn_seeds`. None has a flag parser; `--help` is swallowed and the real (long or blocking)
job starts. `estate_atlas` is proven below: 29.8s and 1.7M rows.

**F-9 — `--help` is not a dry run.** The sweep created/modified real artifacts:
`dashboard/static/drift_board.html` (written by `tools/drift_dashboard.py:380`,
`OUT_HTML.write_text(...)`), and `corpus_fts_rebuild` rebuilt `catalog/catalog_fts.sqlite`
(134,303,744 bytes). `estate_atlas` wrote `watch/ESTATE_ATLAS/`. **Any future audit that
"safely" passes `--help` to this fleet is mutating the estate it is auditing.**
Pre-existing unrelated dirt in the tree (1,433 modified files, incl. in-flight
`seed/engines/ → tools/index/` renames) was left untouched; I did not revert anything.

---

## PART B — DEAD INSTRUMENT SWEEP

Method (validated, see "Instrument bugs found" below): per tool, `rg -w -l` over
3,262 tracked code files, 9,428 doc/config files, 294 test files, 1 githook; file lists
chunked 400 at a time to stay under the Windows 32k command-line limit. The tool file is
excluded from its own count. `referenced_by` = distinct tracked **code** files naming the
module (imports, calls, subprocess invocations).

- **LIVE (75)** — ≥1 code caller.
- **ORPHAN (59)** — zero code callers, but named in docs/config/hooks. Documented, unwired.
- **DEAD (29)** — zero code callers, zero doc mentions, zero tests, zero hook mentions.

**Fleet-wide: 88 of 163 tools (54%) are not called by any tracked code. Only 20 of 163 (12%) have a test.**

| Metric | Count |
|---|---|
| Called by other code | **75** |
| Documented but never called | **59** |
| Completely unreferenced (**DEAD**) | **29** |
| Have a test in `tests/` | **20** |
| Named in a githook | **10** |
| Untracked by git | **26** |
| Last-touched buckets (of 137 tracked) | 0–7d: 103 · 8–30d: 4 · 31–50d: 30 |

### The 29 DEAD tools (no caller, no doc, no test, no hook)

`build_adam_pdf`, `build_adam_setup`, `build_adam_setup_final`, `build_adam_soul`,
`build_adam_soul_full`, `build_aos_pdf`, `build_candy_pdfs`, `build_plain12_pdf`,
`build_plain_pdf`, `cache_kpi`, `caption_ledger_sha_check`, `cascade_falsifier_run`,
`fold_v2_covariance`, `game_module_dated_numbers`, `knot_taming_night`, `ledger_lock`,
`letter_salon_20260920`, `memory_gauge`, `meter_patrol`, `ocean_v2_pilot`, `path_lint`,
`pointer_rot_check`, `pricing_diff`, `probe20_stamp`, `provider_snapshot_differ`, `qknot_b1`,
`queue_row_census`, `seed_paired_uplift`, `weights_consolidate`

Two of these are named gates, which is the sharp version of the finding:
- **`game_module_dated_numbers.py`** — a tripwire ("TRIPWIRE: 1 undated real-estate number(s)"),
  and it fired on the repo during the sweep, yet nothing calls it and nothing tests it.
- **`ledger_lock.py`** — one of the 7 NEW violations the ratchet just reported
  (`except-pass: tools/ledger_lock.py:125`). The fleet has a broken lock and a gate that
  caught it; neither is wired to anything that runs.

### The 4 gate-shaped ORPHANS (documented, never invoked)
`checkbox_receipt_gate` (hook_refs=1), `prepush_paths_changed` (hook_refs=1),
`refold_gate` (hook_refs=1), and the whole `—_gate.py` family
(`openrouter_free_gate`, `policy_eval_schema_check`, `freshness_gate`, `quote_gate`).
`freshness_gate.py` is LIVE (called by code) — but see F-8, it is the one that fails open.

### Full table (163 rows)

| tool | referenced_by (code files) | doc_refs | has_test | last commit | verdict |
|---|---|---|---|---|---|

| `build_adam_pdf.py` | 0 | 0 | NO | 2026-09-25 | **DEAD** |
| `build_adam_setup.py` | 0 | 0 | NO | 2026-09-25 | **DEAD** |
| `build_adam_setup_final.py` | 0 | 0 | NO | 2026-09-25 | **DEAD** |
| `build_adam_soul.py` | 0 | 0 | NO | 2026-09-25 | **DEAD** |
| `build_adam_soul_full.py` | 0 | 0 | NO | 2026-09-25 | **DEAD** |
| `build_aos_pdf.py` | 0 | 0 | NO | 2026-09-25 | **DEAD** |
| `build_candy_pdfs.py` | 0 | 0 | NO | 2026-09-25 | **DEAD** |
| `build_plain12_pdf.py` | 0 | 0 | NO | 2026-09-25 | **DEAD** |
| `build_plain_pdf.py` | 0 | 0 | NO | 2026-09-25 | **DEAD** |
| `cache_kpi.py` | 0 | 0 | NO | 2026-09-22 | **DEAD** |
| `caption_ledger_sha_check.py` | 0 | 0 | NO | UNTRACKED | **DEAD** |
| `cascade_falsifier_run.py` | 0 | 0 | NO | 2026-09-26 | **DEAD** |
| `fold_v2_covariance.py` | 0 | 0 | NO | 2026-09-25 | **DEAD** |
| `game_module_dated_numbers.py` | 0 | 0 | NO | UNTRACKED | **DEAD** |
| `knot_taming_night.py` | 0 | 0 | NO | 2026-09-25 | **DEAD** |
| `ledger_lock.py` | 0 | 0 | NO | UNTRACKED | **DEAD** |
| `letter_salon_20260920.py` | 0 | 0 | NO | 2026-09-21 | **DEAD** |
| `memory_gauge.py` | 0 | 0 | NO | 2026-09-22 | **DEAD** |
| `meter_patrol.py` | 0 | 0 | NO | UNTRACKED | **DEAD** |
| `ocean_v2_pilot.py` | 0 | 0 | NO | 2026-09-21 | **DEAD** |
| `path_lint.py` | 0 | 0 | NO | 2026-09-21 | **DEAD** |
| `pointer_rot_check.py` | 0 | 0 | NO | UNTRACKED | **DEAD** |
| `pricing_diff.py` | 0 | 0 | NO | 2026-09-22 | **DEAD** |
| `probe20_stamp.py` | 0 | 0 | NO | UNTRACKED | **DEAD** |
| `provider_snapshot_differ.py` | 0 | 0 | NO | UNTRACKED | **DEAD** |
| `qknot_b1.py` | 0 | 0 | NO | 2026-09-21 | **DEAD** |
| `queue_row_census.py` | 0 | 0 | NO | UNTRACKED | **DEAD** |
| `seed_paired_uplift.py` | 0 | 0 | NO | UNTRACKED | **DEAD** |
| `weights_consolidate.py` | 0 | 0 | NO | 2026-09-22 | **DEAD** |
| `research.py` | 683 | 1517 | yes | 2026-09-18 | **LIVE** |
| `corpus.py` | 483 | 1601 | yes | 2026-09-18 | **LIVE** |
| `lens.py` | 362 | 734 | yes | 2026-09-21 | **LIVE** |
| `drift.py` | 247 | 1354 | yes | 2026-09-26 | **LIVE** |
| `shell.py` | 177 | 424 | yes | 2026-08-14 | **LIVE** |
| `filesystem.py` | 42 | 148 | yes | 2026-09-14 | **LIVE** |
| `swarm_tools.py` | 40 | 39 | yes | 2026-08-14 | **LIVE** |
| `autopilot.py` | 35 | 37 | yes | 2026-08-07 | **LIVE** |
| `pile_classify.py` | 16 | 14 | yes | 2026-09-25 | **LIVE** |
| `tier_probe.py` | 16 | 20 | yes | 2026-08-08 | **LIVE** |
| `estate_smith_chart.py` | 9 | 19 | NO | 2026-09-25 | **LIVE** |
| `local_bench.py` | 8 | 5 | NO | 2026-08-08 | **LIVE** |
| `pupeteer_gauntlet.py` | 8 | 15 | yes | 2026-08-14 | **LIVE** |
| `code_execution.py` | 7 | 17 | NO | 2026-08-14 | **LIVE** |
| `steer_compare.py` | 7 | 12 | NO | 2026-08-08 | **LIVE** |
| `classify_corpus.py` | 6 | 7 | NO | 2026-08-08 | **LIVE** |
| `model_bakeoff.py` | 6 | 4 | NO | 2026-09-24 | **LIVE** |
| `stealth_sweep.py` | 6 | 7 | NO | 2026-09-24 | **LIVE** |
| `steer_all.py` | 6 | 4 | NO | 2026-08-19 | **LIVE** |
| `task_wall.py` | 6 | 9 | NO | 2026-09-24 | **LIVE** |
| `visor.py` | 6 | 16 | NO | UNTRACKED | **LIVE** |
| `dfhack.py` | 5 | 34 | yes | 2026-09-25 | **LIVE** |
| `topic_research.py` | 5 | 10 | NO | 2026-08-08 | **LIVE** |
| `corpus_lens.py` | 4 | 4 | NO | 2026-08-09 | **LIVE** |
| `estate_atlas.py` | 4 | 7 | NO | 2026-09-25 | **LIVE** |
| `classify_pack.py` | 3 | 5 | NO | 2026-08-08 | **LIVE** |
| `freshness_check.py` | 3 | 20 | NO | 2026-09-25 | **LIVE** |
| `freshness_gate.py` | 3 | 12 | yes | 2026-09-26 | **LIVE** |
| `quote_gate.py` | 3 | 7 | yes | 2026-09-26 | **LIVE** |
| `spec_execute.py` | 3 | 6 | NO | 2026-08-08 | **LIVE** |
| `workflow_gate.py` | 3 | 30 | yes | 2026-09-26 | **LIVE** |
| `audio_channel.py` | 2 | 3 | NO | 2026-09-25 | **LIVE** |
| `blind_probe.py` | 2 | 2 | NO | 2026-09-24 | **LIVE** |
| `capability_manifest.py` | 2 | 11 | NO | 2026-08-08 | **LIVE** |
| `compare_versions.py` | 2 | 5 | NO | 2026-08-08 | **LIVE** |
| `curvature_scan.py` | 2 | 7 | NO | 2026-09-21 | **LIVE** |
| `estate_env.py` | 2 | 0 | NO | 2026-09-22 | **LIVE** |
| `gen_df_luau_data.py` | 2 | 13 | NO | 2026-09-26 | **LIVE** |
| `kv50_smith_chart.py` | 2 | 6 | NO | 2026-09-22 | **LIVE** |
| `lattice_build.py` | 2 | 2 | NO | 2026-09-25 | **LIVE** |
| `research_rig.py` | 2 | 4 | NO | 2026-08-08 | **LIVE** |
| `seed_rib.py` | 2 | 1 | NO | 2026-09-26 | **LIVE** |
| `sense_tools.py` | 2 | 5 | yes | 2026-09-14 | **LIVE** |
| `thrash_meter.py` | 2 | 8 | NO | 2026-09-19 | **LIVE** |
| `typed_scorer.py` | 2 | 2 | NO | 2026-09-21 | **LIVE** |
| `battery_rerun.py` | 1 | 3 | yes | 2026-09-26 | **LIVE** |
| `cathedral_walk.py` | 1 | 2 | NO | 2026-09-21 | **LIVE** |
| `census_collect.py` | 1 | 0 | NO | 2026-09-26 | **LIVE** |
| `census_drift_patrol.py` | 1 | 6 | NO | 2026-09-26 | **LIVE** |
| `census_patrol_selftest.py` | 1 | 1 | NO | UNTRACKED | **LIVE** |
| `cold_boot_test.py` | 1 | 8 | NO | 2026-09-26 | **LIVE** |
| `config_seal.py` | 1 | 21 | NO | 2026-09-25 | **LIVE** |
| `corpus_diff.py` | 1 | 4 | NO | 2026-08-09 | **LIVE** |
| `corpus_fts_rebuild.py` | 1 | 3 | NO | UNTRACKED | **LIVE** |
| `description_pin.py` | 1 | 10 | yes | 2026-09-26 | **LIVE** |
| `drift_dashboard.py` | 1 | 1 | NO | UNTRACKED | **LIVE** |
| `drift_pairs_stamp.py` | 1 | 13 | NO | 2026-09-26 | **LIVE** |
| `eastwest_thorn_20260920.py` | 1 | 0 | NO | 2026-09-21 | **LIVE** |
| `fullsend_s2.py` | 1 | 19 | NO | 2026-09-25 | **LIVE** |
| `gen_artifact_lore.py` | 1 | 5 | NO | 2026-09-26 | **LIVE** |
| `grave_classify.py` | 1 | 6 | yes | 2026-09-26 | **LIVE** |
| `light_walk.py` | 1 | 3 | NO | 2026-09-22 | **LIVE** |
| `md_record_seal.py` | 1 | 7 | NO | 2026-09-26 | **LIVE** |
| `meters_nightly.py` | 1 | 6 | NO | 2026-09-25 | **LIVE** |
| `mimo_watch.py` | 1 | 7 | NO | 2026-09-25 | **LIVE** |
| `ox_heartbeat.py` | 1 | 0 | NO | 2026-09-22 | **LIVE** |
| `quote_hitrate.py` | 1 | 5 | yes | 2026-09-26 | **LIVE** |
| `research_mine.py` | 1 | 0 | NO | 2026-09-25 | **LIVE** |
| `scs.py` | 1 | 16 | NO | 2026-09-19 | **LIVE** |
| `seed_v2.py` | 1 | 14 | NO | 2026-09-26 | **LIVE** |
| `steal_gdrive.py` | 1 | 5 | NO | 2026-08-09 | **LIVE** |
| `track_bpm.py` | 1 | 0 | NO | 2026-09-25 | **LIVE** |
| `verb_anchor.py` | 1 | 13 | NO | 2026-09-19 | **LIVE** |
| `violation_ratchet.py` | 1 | 73 | NO | 2026-09-25 | **LIVE** |
| `wave_lift.py` | 1 | 12 | NO | 2026-09-25 | **LIVE** |
| `ack_fleet_game.py` | 0 | 1 | NO | 2026-08-19 | **ORPHAN** |
| `backfill_direct.py` | 0 | 1 | NO | 2026-09-25 | **ORPHAN** |
| `bib_launder_check.py` | 0 | 4 | NO | UNTRACKED | **ORPHAN** |
| `box_burn_watch.py` | 0 | 4 | NO | 2026-09-26 | **ORPHAN** |
| `build_seed.py` | 0 | 1 | NO | 2026-09-24 | **ORPHAN** |
| `cathedral_build.py` | 0 | 8 | NO | 2026-09-25 | **ORPHAN** |
| `cathedral_eigen_map.py` | 0 | 2 | NO | 2026-09-26 | **ORPHAN** |
| `cathedral_wire_tavern.py` | 0 | 3 | NO | 2026-09-22 | **ORPHAN** |
| `checkbox_receipt_gate.py` | 0 | 0 | NO | 2026-09-26 | **ORPHAN** |
| `compaction_eval.py` | 0 | 8 | NO | 2026-09-21 | **ORPHAN** |
| `coordinate_fleet.py` | 0 | 1 | NO | 2026-08-19 | **ORPHAN** |
| `corpus_lens_run.py` | 0 | 4 | NO | 2026-09-25 | **ORPHAN** |
| `corpus_self_lens.py` | 0 | 5 | NO | 2026-08-09 | **ORPHAN** |
| `duty_fuzz.py` | 0 | 16 | NO | 2026-09-25 | **ORPHAN** |
| `envelope_harvest.py` | 0 | 1 | NO | UNTRACKED | **ORPHAN** |
| `fold_mickey17.py` | 0 | 7 | NO | 2026-09-25 | **ORPHAN** |
| `full_scan.py` | 0 | 3 | NO | 2026-09-25 | **ORPHAN** |
| `gaming_corpus_pass.py` | 0 | 1 | NO | 2026-09-25 | **ORPHAN** |
| `gen_worldgen_spheres.py` | 0 | 5 | NO | 2026-09-26 | **ORPHAN** |
| `ghost_tournament.py` | 0 | 7 | NO | 2026-08-14 | **ORPHAN** |
| `kv_slot_pilot.py` | 0 | 2 | NO | 2026-09-22 | **ORPHAN** |
| `ledger_close_check.py` | 0 | 1 | NO | UNTRACKED | **ORPHAN** |
| `luau_lint.py` | 0 | 11 | NO | 2026-09-25 | **ORPHAN** |
| `mcp_pin.py` | 0 | 16 | NO | 2026-09-25 | **ORPHAN** |
| `md_record_audit.py` | 0 | 8 | NO | 2026-09-25 | **ORPHAN** |
| `mickey17_v2_fold.py` | 0 | 11 | NO | 2026-09-25 | **ORPHAN** |
| `one_pipe.py` | 0 | 4 | NO | 2026-08-07 | **ORPHAN** |
| `openrouter_free_gate.py` | 0 | 2 | NO | UNTRACKED | **ORPHAN** |
| `operator_go.py` | 0 | 2 | NO | UNTRACKED | **ORPHAN** |
| `oracle_calibration.py` | 0 | 16 | NO | 2026-09-19 | **ORPHAN** |
| `persona_grid.py` | 0 | 1 | NO | 2026-09-19 | **ORPHAN** |
| `policy_eval_schema_check.py` | 0 | 5 | NO | 2026-09-19 | **ORPHAN** |
| `prepush_paths_changed.py` | 0 | 1 | NO | UNTRACKED | **ORPHAN** |
| `probe20_run.py` | 0 | 5 | NO | 2026-09-26 | **ORPHAN** |
| `provider_error_tally.py` | 0 | 1 | NO | UNTRACKED | **ORPHAN** |
| `queue_dupes_check.py` | 0 | 2 | NO | UNTRACKED | **ORPHAN** |
| `quote_audit_wide.py` | 0 | 12 | NO | 2026-09-25 | **ORPHAN** |
| `rebuild_grounding_wave_md.py` | 0 | 1 | NO | 2026-09-26 | **ORPHAN** |
| `refold_gate.py` | 0 | 1 | NO | UNTRACKED | **ORPHAN** |
| `restore_guard.py` | 0 | 1 | NO | UNTRACKED | **ORPHAN** |
| `rib_check_game_loop.py` | 0 | 1 | NO | 2026-08-19 | **ORPHAN** |
| `roblox_npc_gateway.py` | 0 | 11 | NO | 2026-09-25 | **ORPHAN** |
| `saturation_fourcond.py` | 0 | 1 | NO | 2026-09-21 | **ORPHAN** |
| `seed_mcp.py` | 0 | 1 | NO | UNTRACKED | **ORPHAN** |
| `seed_mcp_cold_client.py` | 0 | 1 | NO | UNTRACKED | **ORPHAN** |
| `seed_salon.py` | 0 | 6 | NO | 2026-09-25 | **ORPHAN** |
| `smoke_import.py` | 0 | 4 | NO | 2026-08-07 | **ORPHAN** |
| `spawn_gpipe.py` | 0 | 4 | NO | 2026-08-07 | **ORPHAN** |
| `state_asof.py` | 0 | 3 | NO | 2026-09-21 | **ORPHAN** |
| `steer_grok_1m.py` | 0 | 1 | NO | 2026-08-19 | **ORPHAN** |
| `steer_grok_whole.py` | 0 | 3 | NO | 2026-08-19 | **ORPHAN** |
| `stills_xai.py` | 0 | 1 | NO | 2026-09-25 | **ORPHAN** |
| `test_pipe_api.py` | 0 | 4 | NO | 2026-08-07 | **ORPHAN** |
| `transport_precheck.py` | 0 | 1 | NO | UNTRACKED | **ORPHAN** |
| `verify_lyapunov_decode_20260921.py` | 0 | 1 | NO | 2026-09-22 | **ORPHAN** |
| `wandr_selfeval.py` | 0 | 16 | NO | 2026-09-25 | **ORPHAN** |
| `x_churn_cli.py` | 0 | 1 | NO | 2026-09-25 | **ORPHAN** |
| `x_churn_grok.py` | 0 | 1 | NO | 2026-09-25 | **ORPHAN** |
| `x_churn_seeds.py` | 0 | 1 | NO | 2026-09-25 | **ORPHAN** |

---

## PART C — THE GATES THAT LIE

Every test below ran in a **sandbox copy** under `%LOCALAPPDATA%\hermes\cache\scratch\sandbox*`.
The real tree was not mutated. Where a tool derives its root from `__file__`
(`freshness_check.py:35`, `config_seal.py:26`), I copied the *tool itself* into the sandbox
so the sandbox became the estate — otherwise the "sandbox" test silently measures the real repo.
That mistake happened once in a first draft and was caught; the corrected result is what's reported.

### Verdict table

| Gate | Malformed input | Exit | Direction | Bypassable? |
|---|---|---|---|---|
| `census_drift_patrol.py` | garbage `AGENTS.md`, no parsable carrier | **2** | fail-closed | No |
| `census_drift_patrol.py` | fossil 09-14 carrier + 40 files grown | **1** `STALE` | fail-closed | No |
| `workflow_gate.py` | missing script | **1** `GATE ERROR` | fail-closed | No |
| `workflow_gate.py` | garbage `.dwf.ts` | **2**, G1–G7 all FAIL | fail-closed | No |
| `config_seal.py verify` | config tampered after sealing | **1** `FAIL` | fail-closed | No |
| `config_seal.py verify` | garbage seal JSON | **1** (uncaught `JSONDecodeError`) | fail-closed¹ | No, but ugly |
| `violation_ratchet.py check` | garbage tree, no baseline | **0** `PASS` | **fail-open²** | See note |
| `violation_ratchet.py check` | garbage baseline JSON | **1** (uncaught traceback) | fail-closed¹ | No |
| `checkbox_receipt_gate.py` | garbage JSON | **1** `FAIL` | fail-closed | No |
| **`freshness_check.py`** | **all boot docs 400d stale, `alive=no`** | **0 `PASS`** | **FAIL-OPEN** | **YES — confirmed** |
| **`census_patrol_selftest.py`** | run as a script | **0**, no output | **VACUOUS PASS** | **YES — confirmed** |
| **`md_record_seal.py`** | unparseable event JSON | **0** after printing the error | **MISLEADING** | **YES — confirmed** |

¹ Fail-closed *by accident*: an uncaught exception, not a designed refusal. `config_seal` and the
ratchet both document exit 2 = "gate itself broken" and neither reaches it on malformed JSON.
A caller that only checks `!= 0` is fine; a caller that distinguishes 1 (violation) from
2 (broken) sees a violation where the truth is "the gate is broken". Worth fixing, not a hole.

² The ratchet's PASS on an empty garbage tree is **correct by design** — there were no files to
violate. It scanned `scope=1 files (all)` and found `hits=0`. Not a bypass; recorded for completeness.

---

### F-8a — CONFIRMED FAIL-OPEN: `freshness_check.py`

**The bug** (`tools/freshness_check.py:292`, and the mirrored line 286):

```python
heartbeat = head_age <= HEARTBEAT_DAYS          # False when the repo is DEAD
...
is_stale = heartbeat and age > STALE_DAYS and not frozen
```

`is_stale` is gated on `heartbeat`. If the repo has not committed in >2 days, `heartbeat=False`,
so **every boot doc is declared fresh regardless of its age** — and the tool prints
`FRESHNESS: PASS` and exits **0**.

The gate is inverted exactly when it matters most. A dead repo is the strongest possible
freshness failure, and it is the one state the tool reports as PASS.

**Reproduction (sandbox, tool copied in so the sandbox is the estate; real tree untouched):**

```
$ git commit   # dated 2020-01-01, so HEAD is ancient
$ touch -d '400 days ago' BOOT_4_7.md state/CURRENT.md state/START_BRIEF.md state/HANDOFF.md
$ python tools/freshness_check.py ; echo EXIT=$?
FRESHNESS: repo heartbeat 2460.8d since last commit (alive=no; bar: stale=7d, heartbeat=2d)
  BOOT_4_7.md: 2460.8d old  [frozen-ok]
  state/CURRENT.md: 2460.8d old  ok
  state/START_BRIEF.md: 2460.8d old  ok
  state/HANDOFF.md: 2460.8d old  [frozen-ok]
FRESHNESS: PASS — boot docs inside the bar.
EXIT 0
```

Every line says stale. The verdict line says PASS. Note `alive=no` is computed and printed —
the information is right there and then discarded.

**Why it survived:** `freshness_check.py --self-test` runs **18 checks, all of them on the
receipt helper** (`stale_claim`, `receipt`, `receipt_from_json`, `hash_text`). It never calls
`main()`. The fail-open lives in `main()`. The self-test is real and passes, and it is
**testing a different function than the one that ships**. A 100%-green self-test is currently
misleading evidence about this gate.

**Fix (one line):** drop the `heartbeat and` conjunct, and decide the dead-repo case
explicitly — a repo past the heartbeat bar should FAIL loudly, not pass.

### F-8b — CONFIRMED VACUOUS PASS: `census_patrol_selftest.py`

`tools/census_patrol_selftest.py` is 196 lines of genuine assertions with **no `__main__` guard**
and no `main()` (`rg '__main__|^def main'` → 0 matches in the file). It is a library that
`census_drift_patrol.main()` injects into. Run directly:

```
$ python tools/census_patrol_selftest.py ; echo EXIT=$?
EXIT 0
```

**Zero output, exit 0.** The file header says "Contract unchanged since B2-215: 0=pass, 1=fail" —
and it honours 0=pass by doing nothing at all. Any wrapper, cron, or receipt that runs this file
path gets a green result and has verified nothing. The correct invocation
(`census_drift_patrol.py --self-test`) does run all 29 checks and passes honestly.

### F-8c — CONFIRMED MISLEADING: `md_record_seal.py`

```
$ python tools/md_record_seal.py ; echo EXIT=$?
md_record_seal: bad event json: Expecting value: line 1 column 1 (char 0)
EXIT 0
```

It reports that its input is unparseable and then **exits 0**. A seal tool cannot seal, says so
in prose, and reports success to the shell. Also: `md_record_seal.py:33` hardcodes
`ESTATE = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")` — a machine-specific
absolute path, so this tool cannot run anywhere else and cannot be tested in a sandbox at all.

---

## INSTRUMENT BUGS FOUND IN MY OWN AUDIT (recorded, not hidden)

The first three Part B implementations produced **wrong** numbers. Each was caught by an
assertion or a sanity check rather than by inspection:

1. **Naive per-tool `re` over 12,690 pre-read files** — O(163 × 12,690) regex scans, did not
   finish in 8 minutes. Killed.
2. **`rg --files-from`** — **does not exist in ripgrep 15.2.0.** Every call returned
   `rg: unrecognized flag --files-from` (rc=2), which my code read as "zero references".
   Result: **163 DEAD, 0 LIVE, 0 ORPHAN** — a 100%-dead fleet, i.e. obviously false.
3. **Look-around without `--pcre2`** — `rg -e '(?<![\w.])mod(?![\w])'` fails on the default
   engine: *"look-around … is not supported"*. rc=2, again indistinguishable from "no matches".
4. **`--no-messages` + a file missing on disk** — `tests/lesson_gate_test.py` is git-tracked but
   deleted from the working tree. `rg` returns **rc=2** for an unreadable input, and
   `--no-messages` suppresses the diagnostic, so the failure is silent. Fixed by filtering the
   file lists through `os.path.exists` and by asserting `rg` never returns 2.

Final instrument asserts a known-good reference before reporting:
`SANITY census_drift_patrol code refs: 2 ['tools/census_collect.py', 'tools/census_drift_patrol.py']`
and `SANITY violation_ratchet refs: 2 ['scripts/ratchet_daily.ps1', 'tools/violation_ratchet.py']`.

The lesson is the same one the fleet's own doctrine keeps hitting, so it belongs here: **an
instrument that cannot fail loudly will report a clean sweep.** Two of my four bugs would have
produced confident, completely fabricated numbers in the report above.

---

## RECOMMENDED FIXES, IN TRIAGE ORDER

1. **`freshness_check.py:286,292`** — remove the `heartbeat and` conjunct; add `main()` coverage
   to the self-test, including the dead-repo case that currently passes. *(fail-open, live)*
2. **`census_patrol_selftest.py`** — add a `__main__` block that injects the module and runs
   `self_test`, or make direct invocation exit non-zero. *(vacuous pass)*
3. **`md_record_seal.py:33`** — replace the hardcoded absolute path with `__file__`-relative;
   exit non-zero on unparseable input. *(misleading pass + non-portable)*
4. **5× `import config`** (`shell`, `filesystem`, `code_execution`, `classify_pack`,
   `topic_research`) — resolve as a package-relative import. These crash on any invocation
   that does not happen to set CWD, and 4 of them are counted LIVE only because of that.
5. **`--help` as a mutation vector** — 58 tools ignore it, and at least `drift_dashboard`,
   `corpus_fts_rebuild` and `estate_atlas` write real artifacts. Add a `--dry-run`/`--check`
   convention, or a conftest-style wrapper that refuses unknown flags, before any agent
   sweeps this fleet again.
6. **88 of 163 tools have no caller.** Retire the 29 DEAD outright; require a named owner or a
   test for the 59 ORPHANs. A toolbelt where 54% of instruments are unwired cannot be
   dogfooded, only collected.

---

## ARTIFACTS

- `watch/inbox/audit_20260926/LANE2_DOGFOOD_TOOLS.md` — this report
- `memory/audit_20260926/lane2_tools.json` — 163 rows:
  `{tool, ran, exit_code, verdict, referenced_by, has_test, doc_refs, hook_refs, liveness, last_git, tracked}`
- Sweep artifacts: `%LOCALAPPDATA%\hermes\cache\scratch\{help_sweep,parta,partb_refs,partc,partc2}.json`

**Sandboxes used** (all under `%LOCALAPPDATA%\hermes\cache\scratch\`, all disposable):
`sandbox/` (gates on garbage), `sandbox2/` (freshness + config_seal, tool copied in),
`sandbox3/f2` (freshness dead-repo repro), `sandboxR/` (ratchet), `sandboxG/` (carrier fossils).
