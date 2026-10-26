# deep-compiler-bootstrap: the minimal kernel of a self-hosting estate

flash50 deep item, 2026-09-28. Repo: local_sovereign_agent @ branch mag/run-beta1-factory-build-audi-20260806T231709Z.

## 0. What ran here (instrument first, claims second)

Every number in this file comes from one instrument built and executed during this ask:

- Generator: `watch/inbox/burn_reset_20260927/flash50/deep_compiler_bootstrap_gen.py` (banked alongside, estate convention).
- Command: `.venv/Scripts/python.exe watch/inbox/burn_reset_20260927/flash50/deep_compiler_bootstrap_gen.py` (run twice: first pass exposed a classification bug, second pass is the recorded truth; raw stdout at `deep_compiler_bootstrap_run.log`).
- Index: `deep_compiler_bootstrap_graph.json` (26,833 bytes, full edge list + per-tool import classification).
- Method: `ast` parse of every `tools/*.py` (Python 3.11.15 venv, `sys.stdlib_module_names` for the stdlib split), plus a regex sweep for literal `tools/<name>.py` references (spawn edges), plus an upward sweep over `mag/`, `scripts/`, `githooks/`, `main.py`. Both import edges and spawn edges count: in a CLI estate the `python tools/x.py` call site is as load-bearing as the import.
- Files read in full or in the cited range: `tools/derived_dag.py`, `tools/estate_env.py`, `config.py` (all 309 lines), `tools/violation_ratchet.py:1-120`, `tools/workflow_gate.py:1-110`, `tools/config_seal.py:1-40`, `githooks/pre-push` (complete), `llm.py:1-60`, plus greps cited inline.

Headline census produced by that run:

| measure | value |
|---|---|
| python tools in tools/ (incl. index/) | 189 |
| internal edges (import + spawn) | 92 |
| tools with zero internal deps | 133 (70.4%) |
| tools never depended on by another tool | 129 (68.3%) |
| tools depended on by at least one tool | 60 |
| tools depended on by two or more (the library layer) | 25 |
| pure-stdlib, zero-internal-dep tools | 70 (37.0%), 15,210 LOC of 42,667 total (36%) |
| distinct stdlib modules used estate-wide | 56 |
| true third-party package families estate-wide | 8 (httpx, jsonschema, langchain_ollama, matplotlib, numpy, psutil, reportlab, yaml) |
| tools importing the root substrate (config, llm) | 25 |
| tools referenced from mag/, scripts/, githooks/, main.py | 38 |
| tools that spawn subprocesses | 26 |

Read the last two rows twice: the whole 42,667-line tool estate touches eight third-party families and sits on one 309-line root module.

## 1. The estate already self-hosts; the loop is visible in the hook

The ask says "seats build tools that build tools that build the estate." That is not aspiration here; it is written into the provenance comments of `githooks/pre-push` (30 PUSH-GATE lines, 22 hard exit arms). Each gate block names the earlier tool's output that generated it:

- `tools/census_drift_patrol.py` was "wired from the B2-69 census receipt" (the B2-215 block), i.e. a census tool's output became a gate.
- `tools/checkbox_receipt_gate.py` exists because the B2-251 audit (a tool run) proved a mute denominator; B2-316 wired it.
- `tools/refold_gate.py` exists because the B2-279 falsifier (a tool) executed the gap it closes.
- The caption-ledger block is wired "from the B2-244 self-feed."
- `tools/secret_gate.py` is "the wired form of the B2-73 scanner" per the 2026-09-27 operator GO.
- `tools/workflow_gate.py` self-describes as a "self steal" of the ratchet pattern (workflow_gate.py:9-11): a tool built by copying the architecture of an earlier tool.

And the kernel's shape is physically visible downstream: the ratchet's `file-too-long` rule (cap 400, violation_ratchet.py:44) has split real modules, and the children cite it in their headers: `mag/catalog_freshness.py:3`, `mag/catalog_tags.py:3`, `mag/events_scan.py:4`, `mag/frontier_salon.py:396`, `mag/frontier_salon_cli.py:3`. A gate decides how files look. That is what a kernel is.

## 2. The graph back to first principles

Layer 0 (first principles, not built by the estate): the CPython 3.11 interpreter, the 56 stdlib modules actually used (heavy tail: sys 160 tools, pathlib 155, json 149, datetime 96, argparse 81, re 76, hashlib 44, urllib.request 36, subprocess 26), git, the Windows/POSIX process and file layers.

Layer 0.5 (the substrate stones, outside tools/ but imported by tools through the sys.path.insert trick used by 70 tools): `config.py` (309 lines: ROOT, the FS_ROOTS jail, the SHELL_ALLOW allowlist, MAX_TOOL_OUTPUT, ollama_base; 22 tools import it directly and 844 python files repo-wide (excluding .venv/.git/watch)), `llm.py` (Ollama chat with raw-HTTP fallback), the `models/` package (model registry). These are the estate's "runtime," not its tools.

Layer 1 (the 133 leaves, zero internal deps; 70 of them pure stdlib): every one of these is rebuildable from Layer 0 + Layer 0.5 in one seat-sitting. Full list in Appendix A; the 70 pure-stdlib subset includes the entire gate family's cores: violation_ratchet, workflow_gate, config_seal, checkbox_receipt_gate, description_pin, freshness_check, quote_gate, prepush_paths_changed, derived_dag, estate_env.

Layer 2 (the 92 internal edges): full table in Appendix C. The library layer (in-degree >= 2) is 25 tools: blind_probe, census_drift_patrol, corpus, corpus_fts_rebuild, curvature_scan, drift, drift_dashboard, drift_pairs_stamp, estate_atlas, estate_env, estate_smith_chart, gen_df_luau_data, kv50_smith_chart, ledger_lock, model_bakeoff, probe20_run, quote_gate, refold_gate, secret_gate, secret_gate_rules, secret_gate_scan, seed_rib, stealth_sweep, task_wall, typed_scorer. Note what this layer is NOT: there is no parser, no interpreter, no build engine in it. The estate's shared code is measurement and locking (drift, ledger_lock, typed_scorer, census), not construction. Construction is delegated upward to Layer 3.

Layer 3 (upward wiring, 38 tools referenced from outside tools/): the decisive edges are into `githooks/pre-push` (violation_ratchet, config_seal, secret_gate, workflow_gate, census_drift_patrol, freshness_gate, refold_gate, checkbox_receipt_gate, prepush_paths_changed, description_pin) and into scheduled scripts (violation_ratchet via scripts/ratchet_daily.ps1, meter_patrol via scripts/census_patrol_daily.ps1, pile_classify via scripts/day_end_pile.ps1 and main.py). Appendix D.

So the honest global shape: a wide, flat meadow of 133 independent leaves, one thin library ridge of 25, and a narrow mountain range of 10 gates wired into the single choke point every byte must cross to become estate: the push.

## 3. The kernel question

What is the minimal kernel, the one tool you need to build everything else? Candidates, weighed against the measured graph:

1. `config.py` (root substrate). Eliminated as the kernel though it is the foundation stone: 309 lines of constants and resolvers. It is passive; it builds nothing and gates nothing. It is Layer 0.5, below kernel rank.
2. `tools/estate_env.py` (50 lines, "the one canonical key loader"). Beautiful law ("value or None. No pretending," estate_env.py:37) but in-degree 2. Locally revered, globally marginal. Not the kernel.
3. `tools/workflow_gate.py` (stdlib-only, zero internal deps, 326 lines). The GENERATION kernel: it gates the machine that spawns seats to write tools (G1 multiplicity through G7 laws, workflow_gate.py:13-20). Every flash50 fan-out, including the one that produced this item, exists under it. Strongest counter-candidate.
4. `tools/config_seal.py` (108 lines, enforcing at push, named re-seal act), census_drift_patrol (doctrine), secret_gate (secrets). These are the law, doctrine, and hygiene seals. Real, enforcing, but each covers one surface adjacent to code; none covers code itself.

The kernel is `tools/violation_ratchet.py`. Four arguments, all graph- or byte-grounded:

**Position.** In a self-hosting compiler the kernel is the stage every other artifact must pass through to exist. In this estate, "existing" means "pushed," and the push has exactly one choke point: `githooks/pre-push`. Its first enforcing check is `tools/violation_ratchet.py check --changed || exit 1` over `mag/` + `tools/` (hook block 1; DEFAULT_ROOTS at violation_ratchet.py:43). It is the linker of this estate: code that does not pass it is not estate, no matter who wrote it or how good it is. The workflow_gate is subordinate in the dependency order: its own edits are re-proven at that same hook (the workflow_gate_scenarios block, enforcing exit 1), i.e. the gate that gates generation is itself gated by the ratchet's floor. In compiler terms the ratchet is the bottom of the trust chain and workflow_gate is the first tool built on top of it.

**Reflexivity.** A self-hosting kernel must be able to re-derive itself from first principles. The ratchet qualifies in the strict sense: delete `configs/violation_baseline.json`, run a scan plus `baseline-update`, and the register re-derives entirely from the tree it governs; fingerprints are `sha256(rule NUL file NUL detail)` truncated to 16 hex (violation_ratchet.py:84-85). Its input is the codebase; its output defines what counts as lawful codebase; and it includes itself in its own input (tools/ is a scan root, so `tools/violation_ratchet.py` is subject to its own rules). It also obeys its own law: the file is 351 lines against its own 400-line cap (violation_ratchet.py:44). The debt register can only grow by a named act (`baseline-update --by WHO`) and only shrinks via `prune`, whose domain rules (violation_ratchet.py:51-68) were themselves amended after a live failure (B2-95, cited in the header). A kernel that contains its own amendments is self-hosting in the Thompson sense.

**Shape-giving.** Kernels determine the shape of what is built on them. The ratchet's file-too-long law visibly split five mag modules (section 1); its fingerprint discipline (line-free details so unrelated edits do not churn the register, violation_ratchet.py:19-21) dictates how every tool's debt is named; its exit contract 0/1/2 (2 = gate broken) is the shape the workflow_gate self-stole ("exit 2 is the only hard block," workflow_gate.py:10-11). No other tool in the graph has descendants citing it in their headers as the reason for their file structure.

**Trust anchor.** Thompson's 1984 argument: a bootstrapped toolchain cannot verify itself; the trust terminates somewhere outside the system. The estate agrees and names the place: the ratchet cannot be loosened by code, only by a human-or-agent act that lands in a ledger under a name (`baseline-update --by <who>`, hook header; AGENTS.md ratchet bullet). The kernel's trusted computing base is the operator, and the act of trusting is itself receipted. That is the correct minimal answer: any "smaller" kernel (interpreter alone, config.py alone) has no such anchor and would let fabrication flow.

## 4. The full bootstrap, stated as a machine

Layer 0 (interpreter + stdlib + git) feeds Layer 0.5 (config.py jail and paths). On that, the seat (the LLM front-end, the estate's stochastic compiler) emits candidate tools. The workflow_gate (Layer 1, itself ratchet-clean) licenses the generation at fan-out width; gophers write tools plus receipts. Every push crosses violation_ratchet (the enforcing linker over code), config_seal (law), secret_gate (hygiene), census_drift_patrol (doctrine, exit 2 fail-closed). Landed tools produce audits and falsifiers; those artifacts become new gate blocks in the hook (six of the hook's blocks cite the B2 receipt that minted them). The gates then shape the next generation's file topology. The loop closes: tools -> receipts -> gates -> tools. The ratchet is the one instrument that appears in every cycle, has no instrument above it except the named operator act, and can rebuild its own state from the tree. That is the minimal kernel.

The seed-size comparison is instructive. live-bootstrap rebuilds the whole userspace from a few-hundred-byte hex0 monitor; this estate's rebuild seed is Layer 0 + config.py + violation_ratchet.py: an interpreter the estate did not write, 309 lines of paths and jail, and 351 lines of gate. Given those, the other 188 tools are derivable: 133 are already leaves (70 of them pure stdlib, one seat-sitting each), 56 are short compositions of the leaves and the library ridge (Appendix C, median edge count 1), and the gates re-mint the law on every push. The eighth of the estate that is third-party (8 families) is the one honest non-self-hosted strip, and it is replaceable: reportlab/matplotlib are PDF/plot sugar, langchain_ollama has an in-repo raw-HTTP fallback by design (llm.py:2-5).

## 5. Literature anchors

- Ken Thompson, "Reflections on Trusting Trust," CACM 27(8), 1984. The bootstrapped compiler as the locus of unverifiable trust. The estate's resolution is the named-act register: the kernel cannot be loosened silently, so the trust chain terminates at a receipted operator decision rather than at a binary.
- The live-bootstrap project (full-source bootstrapping from the hex0 seed, via stage0-posix to GCC). The methodological precedent for "name the smallest seed from which everything else re-derives"; section 4 applies the same discipline to a tool estate instead of a userspace.
- Wang et al., "Voyager: An Open-Ended Embodied Agent with Large Language Models," arXiv:2305.16291, 2023. The literature's closest model of seats building tools that build tools: a skill library of agent-written code, iteratively proposed, executed, and verified before storage. What Voyager lacks and this estate has is exactly the ratchet: Voyager stores skills on self-verification alone; nothing prevents silent rot of the library. The estate's contribution to that design is making accretion lawful (registered debt, named acceptance, prune) rather than merely verified-once.
- Forth and the Smalltalk image are the classical software analogues of Layer 0.5: a minimal dictionary (or image) from which the system extends itself; config.py + the ratchet play that role here, with git receipts replacing the snapshot.

## 6. The gap this design exposes

The kernel has no standing meta-check. `census_drift_patrol.py` has `census_patrol_selftest.py`; `prepush_paths_changed.py` has `--selftest`; the workflow_gate re-proves against seven scenario cards at every push. The ratchet has neither a selftest tool nor a scheduled probe (grep of violation_ratchet.py shows only `def main` at line 333; upward dependents are the hook and scripts/ratchet_daily.ps1, both of which run it as oracle, never against a known-bad fixture). Its correctness history is failure-driven (B2-95 prune gap, B2-273 growth law), which is how the census carrier rotted for 12 days before B2-215 existed. The concrete fix falls out of the bootstrap design: a `ratchet_selftest.py` that plants a known-bad file family, asserts the exact fingerprints and the exact exit contract (0 clean, 1 new debt, 2 broken gate), and is wired beside census_patrol_selftest on the daily patrol. Until then the minimal kernel is self-hosting but not self-proving, and that distinction is the estate's one open compiler-bootstrap debt.

## 7. Falsifier

This analysis is wrong if any of these fail, each checkable in minutes: (a) the hook's ratchet line is no longer enforcing (it now reads `|| true`); (b) a re-run of the generator reports violation_ratchet or workflow_gate with any internal dependency or third-party import; (c) `configs/violation_baseline.json` deleted plus one scan plus baseline-update does not re-derive a register describing the same tree (fingerprints are content-derived, so a faithful re-derivation must re-find the same claims); (d) violation_ratchet.py exceeds its own 400-line cap.

## Appendix A: the 133 zero-internal-dependency tools (70 pure stdlib, marked *)

  ack_fleet_game, auto_promote, autopilot, *battery_rerun, *bib_launder_check, box_burn_watch,
  build_adam_pdf, build_adam_setup, build_adam_setup_final, build_adam_soul,
  build_adam_soul_full, build_aos_pdf, build_candy_pdfs, build_plain12_pdf, build_plain_pdf,
  *cache_kpi, capability_manifest, *caption_ledger_sha_check, *cascade_falsifier_run,
  *cathedral_build, *cathedral_walk, *cathedral_wire_tavern, chain_repair,
  *checkbox_receipt_gate, classify_corpus, classify_pack, code_execution, compare_versions,
  *config_seal, coordinate_fleet, *corpus_diff, curvature_scan, *derived_dag, *description_pin,
  dfhack, dirac_loop_shim, *duty_fuzz, eastwest_thorn_20260920, *eigenmap_two_check,
  *envelope_harvest, *estate_atlas, *estate_env, estate_smith_chart, filesystem, *flashx_probe,
  *fold_mickey17, *fold_v2_covariance, *fossil_check, *freshness_check, full_scan, *fullsend_s2,
  *game_module_dated_numbers, gaming_corpus_pass, *gen_df_luau_data, *grave_classify,
  *index/projects_index, *knot_taming_night, kv50_smith_chart, *kv_slot_pilot,
  *ledger_close_check, *ledger_spot_patrol, lens, letter_salon_20260920,
  *librarian_backfill_20260927, *light_walk, local_bench, *luau_lint, mcp_pin, *md_record_audit,
  *md_record_seal, *memory_gauge, *meter_patrol, *mickey17_v2_fold, *mimo_watch, model_bakeoff,
  ocean_v2_pilot, one_pipe, *openrouter_free_gate, *operator_go, *oracle_calibration,
  ox_heartbeat, path_lint, *pointer_rot_check, policy_eval_schema_check, *prepush_paths_changed,
  *provider_error_tally, *provider_snapshot_differ, pupeteer_gauntlet, qknot_b1,
  *queue_row_census, *quote_audit_wide, *quote_gate, *rebuild_grounding_wave_md, *research,
  *research_mine, research_rig, rib_check_game_loop, *roblox_npc_gateway, saturation_fourcond,
  *scs, *seed_paired_uplift, *seed_rib, seed_salon, sense_tools, *session_cards, shell,
  *smoke_import, spawn_gpipe, *state_asof, steal_gdrive, stealth_fanout, stealth_sweep,
  steer_all, steer_compare, steer_grok_1m, steer_grok_whole, swarm_tools, task_wall,
  test_pipe_api, *thought_quantizer, tier_probe, *track_bpm, *transport_precheck, *typed_scorer,
  verb_anchor, *verify_lyapunov_decode_20260921, *violation_ratchet, *wandr_selfeval,
  *weights_consolidate, *workflow_gate, x_churn_cli, x_churn_grok, x_churn_seeds

## Appendix B: the library ridge, all 60 tools with in-degree >= 1

  drift (5)
  estate_smith_chart (4)
  drift_pairs_stamp (3)
  probe20_run (3)
  blind_probe (2)
  census_drift_patrol (2)
  corpus (2)
  corpus_fts_rebuild (2)
  curvature_scan (2)
  drift_dashboard (2)
  estate_atlas (2)
  estate_env (2)
  gen_df_luau_data (2)
  kv50_smith_chart (2)
  ledger_lock (2)
  model_bakeoff (2)
  quote_gate (2)
  refold_gate (2)
  secret_gate (2)
  secret_gate_rules (2)
  secret_gate_scan (2)
  seed_rib (2)
  stealth_sweep (2)
  task_wall (2)
  typed_scorer (2)
  auto_promote (1)
  cathedral_walk (1)
  census_collect (1)
  census_patrol_selftest (1)
  chain_repair (1)
  classify_pack (1)
  cold_boot_test (1)
  corpus_diff (1)
  corpus_lens (1)
  dirac_loop_shim (1)
  eastwest_thorn_20260920 (1)
  eigenmap_two_check (1)
  fossil_check (1)
  freshness_check (1)
  gen_artifact_lore (1)
  lattice_build (1)
  ledger_append_gate (1)
  light_walk (1)
  local_bench (1)
  meters_nightly (1)
  probe20_tasks (1)
  pupeteer_gauntlet (1)
  queue_dupes_check (1)
  research_mine (1)
  restore_guard (1)
  rumor_drill (1)
  seed_mcp (1)
  seed_v2 (1)
  steal_gdrive (1)
  stealth_fanout (1)
  steer_compare (1)
  thought_quantizer (1)
  track_bpm (1)
  wave_lift (1)
  workflow_gate (1)

## Appendix C: all 92 internal edges (import I / spawn S)

  audio_channel -> track_bpm (I)
  backfill_direct -> blind_probe (S)
  blind_probe -> estate_env (I)
  build_seed -> estate_atlas (S)
  build_seed -> estate_smith_chart (S)
  build_seed -> model_bakeoff (S)
  build_seed -> stealth_sweep (S)
  build_seed -> task_wall (S)
  cathedral_eigen_map -> cathedral_walk (I)
  census_collect -> census_drift_patrol (S)
  census_drift_patrol -> census_collect (I)
  census_drift_patrol -> census_patrol_selftest (I)
  census_patrol_selftest -> census_drift_patrol (S)
  cold_boot_test -> seed_v2 (S)
  compaction_eval -> typed_scorer (I)
  corpus -> corpus_fts_rebuild (S)
  corpus_fts_rebuild -> corpus (S)
  corpus_lens -> corpus_diff (I)
  corpus_lens -> steal_gdrive (S)
  corpus_lens_run -> estate_env (I)
  corpus_self_lens -> corpus_lens (I)
  demote_candidates -> auto_promote (S)
  drift -> drift_pairs_stamp (S)
  drift_dashboard -> drift (S)
  drift_dashboard -> drift_pairs_stamp (S)
  drift_pairs_stamp -> drift (I)
  eigenmap_two_smoke -> eigenmap_two_check (S)
  freshness_gate -> freshness_check (S)
  freshness_gate -> quote_gate (S)
  freshness_gate -> workflow_gate (S)
  gen_artifact_lore -> gen_df_luau_data (S)
  gen_worldgen_spheres -> gen_artifact_lore (S)
  gen_worldgen_spheres -> gen_df_luau_data (S)
  ghost_tournament -> steer_compare (S)
  lattice_build -> blind_probe (S)
  lattice_build -> curvature_scan (S)
  lattice_build -> eastwest_thorn_20260920 (S)
  lattice_build -> estate_smith_chart (S)
  lattice_build -> kv50_smith_chart (S)
  lattice_build -> light_walk (S)
  lattice_build -> wave_lift (S)
  ledger_append_gate -> ledger_lock (S)
  ledger_lock -> ledger_append_gate (I)
  meters_nightly -> curvature_scan (S)
  meters_nightly -> estate_smith_chart (S)
  meters_nightly -> lattice_build (S)
  persona_grid -> typed_scorer (I)
  pile_classify -> pupeteer_gauntlet (I)
  pricing_diff -> meters_nightly (S)
  probe20_run -> drift (I)
  probe20_run -> probe20_tasks (I)
  probe20_stamp -> drift (S)
  probe20_stamp -> drift_dashboard (S)
  probe20_stamp -> drift_pairs_stamp (S)
  probe20_stamp -> probe20_run (I)
  probe20_tasks -> probe20_run (S)
  prompt_compiler -> thought_quantizer (S)
  queue_close -> ledger_lock (I)
  queue_dupes_check -> refold_gate (S)
  quote_hitrate -> quote_gate (I)
  receipt_body_fts -> corpus_fts_rebuild (S)
  refold_gate -> queue_dupes_check (S)
  refold_gate -> restore_guard (S)
  restore_guard -> refold_gate (S)
  rumor_drill -> corpus (I)
  secret_gate -> secret_gate_rules (I)
  secret_gate -> secret_gate_scan (I)
  secret_gate_rules -> secret_gate (S)
  secret_gate_rules -> secret_gate_scan (S)
  secret_gate_scan -> secret_gate (S)
  secret_gate_scan -> secret_gate_rules (I)
  seed_mcp -> seed_rib (I)
  seed_mcp_cold_client -> seed_mcp (S)
  seed_mcp_cold_client -> seed_rib (S)
  seed_v2 -> cold_boot_test (I)
  seed_v2 -> estate_atlas (S)
  seed_v2 -> estate_smith_chart (S)
  seed_v2 -> model_bakeoff (S)
  seed_v2 -> stealth_sweep (S)
  seed_v2 -> task_wall (S)
  spec_execute -> local_bench (S)
  stealth_driver -> chain_repair (S)
  stealth_driver -> fossil_check (S)
  stealth_driver -> probe20_run (S)
  stealth_driver -> rumor_drill (S)
  stealth_fanout_wave2 -> stealth_fanout (I)
  stills_xai -> research_mine (S)
  thrash_meter -> drift (S)
  topic_research -> classify_pack (I)
  visor -> dirac_loop_shim (I)
  visor -> drift_dashboard (S)
  wave_lift -> kv50_smith_chart (S)

## Appendix D: upward dependents (tools referenced from mag/, scripts/, githooks/, main.py)

  audio_channel: mag/afk_loop.py
  auto_promote: mag/improve.py
  census_drift_patrol: githooks/pre-push, scripts/census_patrol_daily.ps1, scripts/register_census_patrol_task.ps1
  checkbox_receipt_gate: githooks/pre-push
  classify_corpus: mag/framework_map.py
  code_execution: mag/framework_map.py, mag/guard_registry.py
  compare_versions: mag/cross_version.py
  config_seal: githooks/pre-push, scripts/ratchet_daily.ps1
  corpus: mag/catalog_freshness.py, scripts/build_knowledge_graph.py
  corpus_fts_rebuild: mag/catalog_rescan.py, scripts/fts_index_daily.ps1, scripts/register_fts_index_task.ps1
  corpus_lens: mag/governor_autorun.py
  description_pin: githooks/pre-push
  drift: scripts/the50_t24_symbol_correlation.py
  estate_smith_chart: mag/session_state_brief.py
  filesystem: mag/openclaw_patches.py
  fossil_check: scripts/census_patrol_daily.ps1
  freshness_check: scripts/ratchet_daily.ps1
  freshness_gate: githooks/pre-push
  lattice_build: mag/session_state_brief.py
  local_bench: mag/framework_map.py
  meter_patrol: scripts/census_patrol_daily.ps1
  pile_classify: mag/decision_framework.py, mag/framework_map.py, mag/governor_autorun.py, mag/improve_loop.py, mag/state_snapshot.py, main.py, scripts/day_end_pile.ps1
  prepush_paths_changed: githooks/pre-push
  pupeteer_gauntlet: mag/framework_map.py
  refold_gate: githooks/pre-push
  research: scripts/build_knowledge_graph.py
  secret_gate: githooks/pre-push
  shell: mag/guard_registry.py
  spec_execute: mag/framework_map.py
  stealth_sweep: mag/cooker.py
  steer_compare: mag/framework_map.py, mag/research_director.py, main.py
  swarm_tools: mag/organ_map.py
  task_wall: mag/cooker.py
  thought_quantizer: mag/context_pack.py
  tier_probe: mag/framework_map.py
  topic_research: mag/framework_map.py
  violation_ratchet: githooks/pre-push, scripts/ratchet_daily.ps1
  workflow_gate: githooks/pre-push, mag/improve.py

Banked artifacts: this file; generator `deep_compiler_bootstrap_gen.py`; index `deep_compiler_bootstrap_graph.json`; raw run log `deep_compiler_bootstrap_run.log`. All under watch/inbox/burn_reset_20260927/flash50/.
