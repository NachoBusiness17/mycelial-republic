# w3-fossil-genome: tool genome, top 20 tools/ by size

Item: w3-fossil-genome. Date: 2026-09-28. Repo: local_sovereign_agent (branch mag/run-beta1-factory-build-audi-20260806T231709Z, tree clean at start).

## Method (all commands run this pass, 2026-09-28)

1. Sizes: `find tools -maxdepth 1 -type f -printf '%s %f\n' | sort -rn | head -25`. tools/ holds 204 entries, 189 of them `.py` (`ls tools | wc -l`, `ls tools/*.py | wc -l`).
2. Imports: `grep -nE '^[[:space:]]*(import|from)[[:space:]]' tools/<file>` for each of the 20.
3. Mentions (repo-wide): `rg -n "tools[/\\.]<base>\b|(^|[^.A-Za-z0-9_])(from|import)[[:space:]]+<base>\b" -l` with self-file not reliably excluded (ripgrep prints Windows backslash paths, so the forward-slash `grep -v` filter missed it; file counts below include the tool's own file).
4. Code callers: same pattern restricted to `mag/ scripts/ tools/ tests/ configs/ githooks/ dashboard/ main.py models/ vscode-mag-map/`, per-file line evidence quoted below.
5. Tests: `rg -ln "\b<base>\b" tests/` plus `find tests -iname "*<base>*"`.
6. TOOLS.md cards: `rg -ci "\b<base>\b" TOOLS.md`.

Caveats, stated plainly:

- ripgrep was gitignore-aware; paths ignored by git (state/, logs/, etc.) were not searched, so callers living only there would be missed.
- ripgrep emitted `rg: ./nul: Incorrect function. (os error 1)` on a repo-root `nul` path; that one file is unreadable, everything else searched clean.
- "Test coverage" here means exactly what the ask asked: does a test file exist that references the tool. I did NOT execute any test suite and did NOT run any of the 20 tools.
- `tools/wandr_selfeval_task.json` (22,985 B) would rank 11 by raw bytes but is a JSON data file, not a tool; the top 20 below are the 20 largest `.py` scripts. Its one relationship (it names `tools/wandr_selfeval.py` at `tools/wandr_selfeval_task.json:138`) is recorded on the wandr row.
- A sibling lane already banked `flash50/tool_genome_data.json` (+ `tool_genome_extract.py`, `tool_genome_analyze.py`, `tool_genome_stats.py`, `deep-tool-genome.md`) in this directory; its keys are `census/genomes/removed_paths/duplicate_byte_groups`. This bank is an independent derivation and uses a distinct filename, so nothing collides.

## The table

| # | Tool (bytes) | Imports (ancestry) | Code callers (strongest first) | Files naming it (rg -l, self incl.) | Test file? |
|---|---|---|---|---|---|
| 1 | pupeteer_gauntlet.py (59,950) | stdlib + `config` (ROOT :63, ollama_base :93), `llm` :109, `langchain_ollama` :117, `mag.*` compass/job_floor/operator_inbox/pro_library/skill_ledger/spec_gate/tesuji_shell :162-168, `mag.headless` :580 | tests/test_pupeteering.py:29 + tests/test_gauntlet_sweeps.py:13 import it; mag/framework_map.py:127 tool card; mag/breakthrough_loop.py:15 (reads its log); vscode-mag-map/extension.js:145 | 43 | YES, 2 files (imports at test_pupeteering.py:29, test_gauntlet_sweeps.py:13) |
| 2 | duty_fuzz.py (53,558) | stdlib only (:97-105), deferred `subprocess` :578 | none found in code; outputs live at watch/inbox/duty_fuzz/cycle_000.jsonl, cycle_001.jsonl + manifest; carries `--selftest` :68 | 27 | none |
| 3 | seed_v2.py (53,467) | multi-script file (four `from __future__` blocks :8/:283/:333/:718): stdlib + `keys` :173, embedded `cooker` :390, `phone_relay` :422, `fastapi` :724, `cold_boot_test` :932 | tools/cold_boot_test.py:78 "Pre-zip gate for tools/seed_v2.py (build book t7 spec, t28 refire)"; no import caller found | 31 | none |
| 4 | stealth_driver.py (37,814) | stdlib + `models.env_load.load_dotenv` :58, `mag.prompt_lance.self_check` :672 | scripts/run_stealth_driver.py:18 `from stealth_driver import main`; tests/test_stealth_driver_prompt_lance.py:21 + test_stealth_driver_effort_dial.py:21 load it as a module; tests/test_selffeed_integration.py:40 imports t_selffeed | 28 | YES, 2 dedicated + 1 integration |
| 5 | wandr_selfeval.py (34,739) | stdlib only (:49-65) | none found in code; companion data file wandr_selfeval_task.json:138 names it; carries `--selftest` :42 | 54 | none |
| 6 | drift_pairs_stamp.py (30,834) | stdlib + `tools.drift.drift_check` :115 | tests/test_drift_pairs_stamp.py:35 `import tools.drift_pairs_stamp as dps`; tools/drift_dashboard.py:5,15,204 consumes its output; tools/drift.py:20 docstring (downstream stamper); tools/probe20_stamp.py:22; docs/DRIFT_BOARD_SPEC.md | 64 | YES, dedicated (test_drift_pairs_stamp.py) |
| 7 | ghost_tournament.py (27,769) | stdlib only (:22-27), deferred subprocess/urllib/concurrent.futures/argparse | none found in code; TOOLS.md 2 hits; memory/tool_manifest.json; reverse cross-ref out to steer_compare at :655 | 31 | none |
| 8 | steer_compare.py (26,550) | stdlib + `models.providers.chat_provider` :135 | main.py:4493,4498,4503,4512 `from tools.steer_compare import run_grid/print_summary/PROVIDERS/TASKS/STEERS`; mag/framework_map.py:133 card; tools/ghost_tournament.py:655 cross-ref; vscode-mag-map/extension.js:151 | 36 | none |
| 9 | quote_audit_wide.py (26,441) | stdlib only (:11-19) | none found in code; receipt watch/inbox/QUOTE_AUDIT_WIDE_20260925.md | 22 | none |
| 10 | oracle_calibration.py (24,937) | stdlib only (:42-51) | none found in code; dashboard/schemas/policy_eval.v1.schema.json:168 cites it as calibration provenance; carries `--selftest` :32 | 26 | none |
| 11 | cathedral_build.py (22,090) | stdlib only (:22-27), deferred hashlib :434 | none found in code; its output watch/inbox/cathedral_v1.html exists | 20 | none |
| 12 | census_drift_patrol.py (20,930) | stdlib + sibling `census_collect` :144, `census_patrol_selftest` :396 | githooks/pre-push:88 EXECUTES it on every push; scripts/census_patrol_daily.ps1 + register_census_patrol_task.ps1 (MagCensusPatrolDaily 08:30); tests/test_census_drift_patrol.py:36 imports; tests/hook_pairing.py:23 maps hook output; AGENTS.md census bullet | 105 | YES, dedicated (test_census_drift_patrol.py) |
| 13 | mcp_pin.py (20,471) | stdlib + `config.ROOT` :60 | configs/tools/mcp_pin.json:5 registers it as source; no import/subprocess caller found; carries `--self-test` :42 | 25 | none |
| 14 | curvature_scan.py (20,384) | stdlib + optional `numpy` :219, `matplotlib` :327-329 | tools/lattice_build.py:31 pipeline entry ("Curvature scan (topology)"); tools/meters_nightly.py:29 nightly runner | 51 | none |
| 15 | tier_probe.py (19,962) | stdlib + `config.ROOT` :52, `models.providers` get_provider/provider_base_url/provider_keys :193 | tests/test_tier_probe.py:13,72 import cost_for/score_design/score_exec; mag/framework_map.py:176 card + :534 name-match in routing regex; vscode-mag-map/extension.js:194 | 23 | YES, dedicated (test_tier_probe.py) |
| 16 | eigenmap_two_smoke.py (19,521) | stdlib only (:37-44) | no python caller; its Luau fixtures are siblings (tools/eigenmap_two_smoke.luau:4,17, eigenmap_two_smoke_env.luau:2, eigenmap_two_luau_test.luau:10); named in roblox/the_mountain.rbxlx, roblox/src/shared/CathedralMap.luau, roblox/README.md | 26 | none |
| 17 | compare_versions.py (18,890) | stdlib + guarded `config.ROOT` :22 | mag/cross_version.py:584 `from tools.compare_versions import generate_report` (with :592 not-available fallback) | 11 | none |
| 18 | build_adam_pdf.py (18,516) | `reportlab` six modules (:1-6) + `os` :7 | none found anywhere (only catalog/memory jsonl + secret_gate scan receipts) | 12 | none |
| 19 | probe20_run.py (18,261) | stdlib + `drift` :66, `probe20_tasks` TASKS :119/:121 | tools/stealth_driver.py:543 runs it via `_run_tool(["tools/probe20_run.py", "--live"], timeout=600)`; tools/probe20_stamp.py:46 `import probe20_run`; tools/probe20_tasks.py:3 (split out of it); configs/workflow_gate_scenarios/G1_multiplicity.card.json:11 cites a real gate FAIL row on it | 72 | none |
| 20 | build_aos_pdf.py (17,520) | `reportlab` seven modules (:1-7) + `os` :8 | none found anywhere (catalog/memory jsonl + receipts only) | 12 | none |

## Coverage verdict

- 4 of 20 tools have a dedicated test file named after them: stealth_driver (2: test_stealth_driver_effort_dial.py, test_stealth_driver_prompt_lance.py), drift_pairs_stamp, census_drift_patrol, tier_probe. Five dedicated files total.
- 1 more tool is imported by test files without a dedicated file: pupeteer_gauntlet (tests/test_pupeteering.py:29, tests/test_gauntlet_sweeps.py:13), plus tests/test_selffeed_integration.py:40 reaching into stealth_driver.
- 15 of 20 have ZERO references anywhere under tests/: duty_fuzz, seed_v2, wandr_selfeval, ghost_tournament, steer_compare, quote_audit_wide, oracle_calibration, cathedral_build, mcp_pin, curvature_scan, eigenmap_two_smoke, compare_versions, build_adam_pdf, probe20_run, build_aos_pdf.
- Four untested tools carry their own `--selftest`/`--self-test` flag inside the file (duty_fuzz :68, wandr_selfeval :42, oracle_calibration :32, mcp_pin :42); that is in-file self-test, not pytest coverage, and I did not run any of them.
- Existence is not health: I verified the test files exist and reference the tool by name/import; I did not execute them, so this column must not be read as "passing".

## Ancestry clusters (reading of the table)

- Repo-core dependent (import config/mag/models): pupeteer_gauntlet (heaviest: config + llm + langchain_ollama + 8 mag modules), stealth_driver, steer_compare, tier_probe, mcp_pin, compare_versions (guarded config), drift_pairs_stamp (tools.drift), census_drift_patrol (tools siblings), probe20_run (drift + probe20_tasks).
- Stdlib-isolated (nothing repo-owned): duty_fuzz, wandr_selfeval, ghost_tournament, quote_audit_wide, oracle_calibration, cathedral_build, eigenmap_two_smoke. These are also exactly the tools with no test file except none of them have one; the two heaviest stdlib-isolated tools (duty_fuzz 53.5 KB, wandr_selfeval 34.7 KB) have zero callers in code and zero tests.
- Third-party-only: build_adam_pdf, build_aos_pdf (reportlab one-shots, zero callers, zero tests; build_adam's `os` import is the only stdlib need).
- Strongest live wiring in the repo: census_drift_patrol (githooks/pre-push:88 + scheduled task), steer_compare (main.py:4493 command path), probe20_run (subprocess from stealth_driver:543), compare_versions (imported by mag/cross_version.py:584), pupeteer_gauntlet (imported by two pytest files).
- seed_v2.py is not one tool but a concatenation of several embedded scripts (four separate `from __future__ import annotations` blocks at :8, :283, :333, :718); configs/violation_baseline.json:893 already flags it "registered to keep push gate honest, flagged for future split".

## Receipt

Every cell above traces to one of the commands in Method, run in this session on this tree. The raw grep output was captured in-session; the file counts in column 5 are full `rg -l | wc -l` values (lists shown to me were head-capped at 25, the counts were not). Line references like `main.py:4493` are clickable against the current tree.
