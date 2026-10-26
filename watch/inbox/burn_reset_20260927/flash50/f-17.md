# f-17 - root module census (repo root *.py), 2026-09-28

Item: census every Python file in the repo root (main.py, etc): lines, CLI commands exposed, actually-used evidence. Banked to watch/inbox/burn_reset_20260927/flash50/f-17.md with byte-identical mirror root-module-census.md. Census-carrier law applied: every number is command-backed this session; the instrument is named at each use. Regenerator: _f17_build.py in this directory.

## 1. Universe

- 77 .py files at repo root by os.listdir (venv python, 2026-09-28). ast.parse succeeded on all 77: 0 syntax errors.
- `ls -1 *.py | wc -l` = 70: the shell glob hides 7 dot-prefixed scratch files (.tmp_sh_dump.py, .tmp_sh_fetch.py, .tmp_sh_grep.py, .tmp_sh_grep2.py, .tmp_sh_grep3.py, .tmp_sh_grep6.py, .tmp_sh_grep7.py). Census universe is the listdir truth: 77.
- Groups: 15 named modules + 55 underscore scratch + 7 dotfile scratch = 77.
- Total lines (wc -l, uniform instrument): 12,211 = 12,042 over the 70 visible + 169 over the 7 dotfiles.
- main.py alone: 5,434 lines = 44.5 pct of all root Python lines, 236,874 bytes.

## 2. CLI surface exposed

### main.py (5,434 lines, 236,874 bytes)
- 185 add_parser registrations (AST walk): 171 top-level + 14 nested, 183 distinct command names.
- Verified three ways this session:
  1. AST extraction of every add_parser call with receiver-variable classification (sub = root group).
  2. Live `main.py --help`, rc=0: usage line lists exactly 171 top-level commands.
  3. Live nested help, all rc=0: game -> descend, map, play, render, status; usage-forecast -> calibrate, goal, queue; renderman-ask -> compact, elevate, expand; links -> add, check, dupes.
- Cross-foot: 171 + 14 = 185 registrations; 2 nested names shadow top-level names (elevate, status), so 171 + 12 = 183 distinct. Exact.
- Nested groups hang off 4 parents: game (main.py:357), usage-forecast (:977), renderman-ask (:999), links (:1322).
- AGENTS.md names 17 distinct main.py commands across its fences (ask, autorun, bonds, brief, clippy, context-pack, dashboard, doctor, improve, lab, mag, pile-classify, promote, research-pack, run, verkle-audit, watch): all exist in the parser (true), zero card rot.

### Other root files with any CLI
- mag_launch.py (710 lines): --stop / --once via sys.argv membership (mag_launch.py:614-616), no subcommands. It is the seat launcher: spawns synthesis_agent.py as Scribe (mag_launch.py:227).
- extract_wiki.py (29 lines): one positional sys.argv[1] (extract_wiki.py:16).
- _test_legibility.py (210 lines): argparse with --blueprint flag (_test_legibility.py:176).
- 26 of 77 files carry an `if __name__ == "__main__"` guard (6 named + 20 scratch); the other 51 are import-only libraries or fragments. Only 3 files accept any argument: main.py, mag_launch.py, extract_wiki.py, plus the one _test_legibility.py flag.

## 3. Actually used (main.py command space, 183 names)

Instruments, weakest to strongest (census denominator law: per-instrument counts, same tree, 2026-09-28):
- memory/ transcript echo: all 183/183 names, 88,969 mention-hits. Weakest: session tapes quote commands self-referentially (agent-state alone 60,243 hits embeds its own command line).
- corpus/ echo: 117/183 names, 34,400 main.py-style + 47,806 mag.cmd-style hits.
- docs/: 64 distinct, 306 main.py-style + 151 mag.cmd-style.
- watch/inbox receipts: 56/183 distinct (43 via main.py-style, 24 via mag.cmd-style patterns; 190 + 129 hits). String evidence, not execution traces.
- logs/ runtime logs: 35/183 distinct, 14,722 main.py-style hits. Top: autorun 6,452; agent 5,182; dashboard 1,419; ingest 602; lab 444; orchestrator 379; api 55; watch 48. This is the recurring-process core.
- scripts/ scheduled wiring: 24 distinct via main.py (lab, blast, doctor, field-steal, power, trail, build-audit, ...) + 9 via mag.cmd.

Strict union of execution instruments (logs + watch/inbox, both syntaxes): 71/183 = 38.8 pct.
Adding scheduled wiring (scripts/): 78/183 = 42.6 pct.
Zero evidence in logs + receipts: 112/183. Zero in logs + receipts + wiring: 105/183 (57.4 pct of the exposed surface never appears in any execution-adjacent instrument):
add, agent-state, aos-grok, autopilot, bonds, boot-coordination, calibrate, canvas-list, canvas-sync, caveman-audit, cheap-swarm, check, cleanup, comms-trail, compact, conductor, context-growth, coordinate, cost-learn, cross-version, decide, deep-handoff, descend, diary, docker-ops, drainer-stats, dupes, elevate, embassy-publish, env, expand, extension-deploy, factory-audit, frontier-help, gap-map, ghost, ghost-summon, gpipes, grok-free, grok-mirror, grok-terminal, grove-build, ideas, janitor, job-floor, knot-evolution, lattice, lattice-backfill, lattice-query, legacy-audit, live-feed, live-ops, loop-audit, map, memlang, mycelium, ollama, operator-mode, ops-graph, org-review, orphan, plan, play, ponytail-audit, pro-library, process-supervisor, queue, queue-learn, queue-ops, quota, render, renderman-ask, republic-os, research-lens, resonance, roadmap-run, roundtable, run-worth, scheduler, scrum, self-steal, session-route, session-state-brief, skill-seat, state-brief, steer, steer-agent, steer-compare, steer-telemetry, steward, summarize-session, swarm-health, system-map, talk, tangent, tapestry, tesuji-shell, token-chain, tts, usage-forecast, virtual-desk-loop, visual, vscode-feed, warning-monitor, workshop

Guard against false positives: the raw token sweep caught prose words (and, for, that) and non-commands (morning-brief, handoff-classify, verkle-compact, probe); all rejected by intersecting with the real argparse set. The 105 is after that intersection.

## 4. Named modules (15): lines, importers, last touch

Import sweep scope: 2,256 files across mag/, tools/, tests/, scripts/, dashboard/, configs/, queue/ + root py (import-statement regex + filename refs).

| file | lines | bytes | main | CLI exposed | importers | last commit |
|---|---|---|---|---|---|---|
| audit.py | 59 | 1,507 | - | none (library) | 6 (mag/act.py, mag/agent_cli.py, mag/cli/core.py, mag/daemon.py, main.py, tests/test_resume_contract.py) | 2026-08-04 eb07ad62e |
| braid_test.py | 25 | 1,196 | - | none | 0 refs anywhere | 2026-08-19 799ddb6fe |
| config.py | 309 | 9,939 | - | none (library) | 699 importers, most-imported root module | 2026-09-16 2b84b8cce |
| conftest.py | 19 | 793 | - | none (pytest root conftest, auto-loaded) | named by mag/code_map.py, mag/verify_gate.py, scripts/_audit_modules.py, scripts/_gen_module_map.py | 2026-08-09 de29d49ea |
| extract_wiki.py | 29 | 1,184 | Y | 1 positional sys.argv[1] (extract_wiki.py:16) | 0 refs anywhere | 2026-09-27 383fed94f |
| graph.py | 113 | 3,603 | - | none (library) | 4 (mag/act.py, mag/chain_query.py, mag/cli/core.py, main.py) | 2026-08-04 eb07ad62e |
| ijl_core.py | 326 | 11,318 | - | none (library) | 5 (mag/context_pack.py, mag/governor_autorun.py, mag/router.py, mag/skill_pipeline.py, tests/test_ijl.py) | 2026-08-04 eb07ad62e |
| llm.py | 194 | 5,840 | - | none (library) | 20 (mag/blast.py, mag/ask.py, mag/arena_adapter.py, ...) | 2026-08-07 36914e134 |
| mag_launch.py | 710 | 25,912 | Y | flags --stop/--once (mag_launch.py:614-616) | 5 (mag/lifecycle.py, mag/power.py, mag/stack.py, mag/unsloth_seat.py, tests/test_launch_topology.py) | 2026-09-25 a5dd96176 |
| main.py | 5,434 | 236,874 | Y | argparse: 171 top + 14 nested = 185 registrations, 183 names | (is the CLI) | 2026-09-28 5dff72ac3 |
| simulate_crash.py | 8 | 285 | - | none | 0 refs anywhere | 2026-08-19 799ddb6fe |
| state.py | 31 | 895 | - | none (library) | 1 (graph.py) | 2026-08-04 eb07ad62e |
| synthesis_agent.py | 282 | 8,682 | Y | none | 0 importers; spawned as Scribe by mag_launch.py:227 | 2026-08-04 eb07ad62e |
| test_480_wave_temperature.py | 112 | 4,312 | Y | none (test file; NOT collected: pytest.ini:2 testpaths=tests) | 0 refs anywhere | 2026-09-14 d575bc168 |
| verify_temperature_rigidity.py | 117 | 4,004 | Y | none | 0 refs anywhere | 2026-09-14 d575bc168 |

Verdicts: LIVE (imported or wired): main.py, mag_launch.py, config.py, llm.py, audit.py, graph.py, ijl_core.py, state.py, conftest.py, synthesis_agent.py (runtime spawn). ORPHAN (zero importers, zero refs, zero receipts): braid_test.py, extract_wiki.py, simulate_crash.py, test_480_wave_temperature.py (uncollected), verify_temperature_rigidity.py.

## 5. Scratch layer (62 files: 55 underscore + 7 dotfiles)

- Lines: 4,443 total scratch (underscore + dotfile combined below).
- 20 of 62 have a main guard; none exposes subcommands; one flag total (_test_legibility.py --blueprint).
- Run receipts (verified, named artifact): 3 of 62.
  - _grok47_chore_run.py: watch/inbox/GROK47_CLI_BURN_RECEIPT_20260925.md ran it, exit 1 at 225s, $0.03970384 spent (honest failure, filed).
  - _w5_t22_verify.py: watch/inbox/MICKEY17_WAVE2_QUALITY_20260925.md ran it: 17 checks, ALL PASS, exit 0.
  - _probe_nous_search.py: watch/inbox/FASTSEARCH_STATIC_KEY_PROBE_20260925.md: 5 HTTP probes, ~$0.001, probe 4 self-reported $0.0005496.
- Inventory-only mentions (filename appears in scan receipts, not run proof): _afk_full_blast.py, _alpha_multi.py, _alpha_rar_fleet.py, _cache_mine.py, _test_legibility.py (watch/inbox/MIMOSA_SCAN_20260925.md, watch/inbox/SECRET_SCAN_BEAT.jsonl), _memlance.py (watch/inbox/FLEET_IMPRINT_20260917.md, watch/inbox/SELF_STEAL_DIRAC_MEMLANCE_20260927.md), _sweep.py (watch/inbox/CODEX_WITNESS_Manual_Audit_Evidence_20260918.json, watch/inbox/index_events.jsonl).
- Contamination note: this flash50 dir holds sibling census artifacts (lsfiles.zlist, measure_out.json, f-09-graph.json) that list every filename; those hits were excluded from evidence.
- The remaining 52 scratch files have no receipt, no importer, no ref: one-shot probes and patch scripts whose only use-record is their own mtime (Aug 13 to Sep 25).

### Per-file scratch table (wc -l, getsize)

| file | lines | bytes | CLI |
|---|---|---|---|
| .tmp_sh_dump.py | 21 | 676 | none |
| .tmp_sh_fetch.py | 21 | 825 | none |
| .tmp_sh_grep.py | 9 | 295 | none |
| .tmp_sh_grep2.py | 13 | 419 | none |
| .tmp_sh_grep3.py | 13 | 412 | none |
| .tmp_sh_grep6.py | 46 | 1,585 | none |
| .tmp_sh_grep7.py | 46 | 1,605 | none |
| _afk_full_blast.py | 107 | 4,948 | none |
| _alpha_dryrun.py | 143 | 5,189 | none |
| _alpha_frontier.py | 118 | 4,503 | none |
| _alpha_multi.py | 188 | 7,109 | none |
| _alpha_rar.py | 137 | 5,545 | none |
| _alpha_rar_deepseek.py | 115 | 4,709 | none |
| _alpha_rar_fleet.py | 155 | 6,176 | none |
| _alpha_steer.py | 137 | 5,243 | none |
| _alpha_zai.py | 136 | 5,140 | none |
| _cache_mine.py | 154 | 6,580 | none |
| _cere2.py | 28 | 1,326 | none |
| _cere3.py | 30 | 1,534 | none |
| _check_and_fix.py | 10 | 283 | none |
| _dl_saelis_slow.py | 50 | 2,344 | none |
| _finish.py | 49 | 1,970 | none |
| _fix_syntax.py | 16 | 597 | none |
| _g33_deepseek_fewshot.py | 96 | 4,594 | none |
| _g42_deepseek_fewshot_v2.py | 100 | 4,920 | none |
| _g52_deepseek_v2.py | 124 | 6,931 | none |
| _g52_dump_controverted.py | 167 | 6,210 | none |
| _grok47_chore_run.py | 126 | 5,593 | none |
| _grok_business_test.py | 63 | 3,369 | none |
| _kill_dash.py | 13 | 414 | none |
| _memlance.py | 19 | 788 | none |
| _pack_mag_archaeology.py | 144 | 4,294 | none |
| _patch_canary.py | 25 | 1,133 | none |
| _patch_cheap_view.py | 83 | 3,148 | none |
| _patch_cheap_view2.py | 86 | 3,256 | none |
| _patch_table.py | 68 | 2,340 | none |
| _patch_table_is_wave.py | 21 | 1,043 | none |
| _patch_turn.py | 73 | 2,855 | none |
| _patch_view.py | 67 | 2,347 | none |
| _patch_view_cache.py | 91 | 3,595 | none |
| _patch_wave_fast.py | 162 | 6,450 | none |
| _probe_crazy.py | 36 | 1,333 | none |
| _probe_look.py | 30 | 1,316 | none |
| _probe_more.py | 43 | 1,572 | none |
| _probe_nous_search.py | 99 | 3,689 | none |
| _probe_routes.py | 22 | 674 | none |
| _probe_table.py | 10 | 428 | none |
| _probe_twice.py | 14 | 497 | none |
| _probe_view2.py | 10 | 463 | none |
| _probe_wave.py | 23 | 1,105 | none |
| _run_http.py | 2 | 77 | none |
| _stub_view.py | 53 | 1,860 | none |
| _sweep.py | 15 | 671 | none |
| _test_legibility.py | 210 | 10,013 | --blueprint flag (_test_legibility.py:176) |
| _tmp_digger_apocjn.py | 16 | 598 | none |
| _tmp_digger_hyp.py | 16 | 624 | none |
| _v41_lane2_harness.py | 157 | 5,428 | none |
| _verify_review_tier_20260925.py | 65 | 3,052 | none |
| _w5_t22_verify.py | 174 | 7,872 | none |
| _w7b_deepseek_v2.py | 126 | 7,027 | none |
| _wave_fold.py | 27 | 1,421 | none |
| _wave_fold2.py | 25 | 1,083 | none |

## 6. Not run / OWED

- No root module or scratch script was executed by this census except main.py --help (rc=0) and the four nested --help calls (rc=0). The census is static analysis plus receipt evidence, so "used" counts are mention/wiring evidence, not runtime tracing.
- Per-command counts in logs are line-mention counts from grep over 225 log files, not de-duplicated process launches.
- mag.cmd-style receipt counts include prose mentions of the form "mag <verb>" where <verb> is a real command; treated as weak evidence, used only inside unions, never as the sole basis for a used verdict.

## 7. Method receipts (commands run this session)

1. `ls -1 *.py | wc -l` -> 70; os.listdir + endswith(".py") -> 77.
2. `wc -l *.py` -> 12,042 total; `wc -l .tmp_sh_*.py` -> 169 total.
3. AST scan of all 77 (guards, argparse, add_parser, sys.argv) -> 26 guards, argparse in main.py + _test_legibility.py, 11 files touch sys.argv, 0 syntax errors.
4. `main.py --help` rc=0 -> 171-name usage line; 4 nested --help calls rc=0.
5. grep -rhoE over logs/, watch/inbox/, scripts/, docs/, memory/, corpus/, queue/ for main.py + mag.cmd invocation tokens, intersected with the real 183-name set.
6. Import sweep over 2,256 code-tree files for the 14 non-main named modules.
7. `git log -1 --format=%as %h -- <file>` per named module (dates in section 4).
8. Scratch receipt sweep over watch/inbox + logs + corpus/steal for all 62 names.
