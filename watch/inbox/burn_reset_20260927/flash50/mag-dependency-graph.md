# f-09 - mag/ dependency graph (census, 2026-09-28)

Item: f-09, Mag Resource Harness, flash50. Scope: every tracked Python module under `mag/`.
Companion machine-readable graph: `watch/inbox/burn_reset_20260927/flash50/f-09-graph.json`
(per-module deps, importers, evidence paths, test files, transitive dependent sets, SCC membership).
Byte-identical mirror: `watch/inbox/burn_reset_20260927/flash50/mag-dependency-graph.md`.

## 1. Instruments (commands actually run this ask)

1. `git ls-files` - tracked-file universe: **47,522 files** at run time, **3,459 tracked .py**.
2. AST pass: `.venv/Scripts/python.exe C:/Users/foste/AppData/Local/Temp/f09_depgraph.py` (script banked in %TEMP%, not the repo) -
   `ast.parse` over the strong-caller universe (**1,908 non-archive tracked .py**), extracting four import forms:
   absolute/relative `mag.*` imports, bare sibling imports inside mag/ (`import kvos_block`; valid because a mag file run as a
   script puts `mag/` at `sys.path[0]`), `import_module`-style string calls, and subprocess list literals `[..., "-m", "mag.x", ...]`.
3. Text scan: `-m mag.*` entry regex + `mag/x.py` path-form regex over **15,310 tracked text files / 315,143,130 bytes** (files <= 2MB).
4. Last modified: `git log --pretty=format:%x01%cs --name-only` over all **684 commits** on HEAD.
5. Test denominator: `.venv/Scripts/python.exe -m pytest --collect-only -q` -> **2410 tests collected in 11.69s** (2026-09-28).

Archive/scratch prefixes carrying **1,551 tracked .py** are EXCLUDED from caller evidence so that byte-copies of mag/ (dist_audit/,
attic/, corpus/, watch/, audit_prep/, phase3_*/ scratch, root tmp files) can never count as callers of live modules; `dist_audit/`
alone holds 1,076 py copies of the mag tree. `memory/*.json` state files (e.g. the generated `knowledge_graph.json`) are demoted
to weak doc evidence: they record module metadata, they invoke nothing.

## 2. Headline numbers

| metric | value |
|---|---|
| mag/ modules (tracked .py, packages count once) | **1034** |
| package `__init__.py` files | 2 (`mag`, `mag.cli`) |
| total LOC in mag/ | 295,350 |
| internal import edges (explicit, module-to-module) | 2299 (+13 bare-sibling-form edges) |
| status OK (has a non-test caller) | 704 |
| ORPHAN (zero caller evidence of any kind) | **3** |
| ENTRY (no import caller; invoked by script/config/subprocess only) | 8 |
| TEST-ONLY (only test files call it) | 42 |
| DOC-ONLY (referenced in docs/comments only, no code caller) | 277 |
| modules with >= 1 test file importing them (static map) | 321 (31.0%) |
| modules with zero test files importing them | **713** |
| strongly connected components > 1 node | 6 (sizes [298, 3, 3, 2, 2, 2]) |
| self-imports | 0 |
| modules with a last-commit date in the last 3 days (>= 2026-09-26) | 93 |
| modules untouched since before 2026-08-29 | 650 |
| modules with no resolvable commit date | 0 |

## 3. Critical path - the most depended-on modules

Transitive dependents = how many mag modules reach this one by following internal imports backward (reverse closure over the
explicit edge set). Direct importers = distinct mag modules whose code imports this one (explicit forms; package-init implicit
loads counted in the `mag` row only). `mag` itself (the package init) has 730 direct importers: any `from mag import X` that does
not resolve to a submodule binds the package instead, which is why the init is the single most imported node in the estate.

### 3a. Top 25 by transitive dependents

| # | module | transitive dependents | direct importers | test files | last modified |
|---|---|---|---|---|---|
| 1 | `mag.verkle_knot` | 560 | 57 | 5 | 2026-09-27 |
| 2 | `mag.training_events` | 544 | 66 | 13 | 2026-08-07 |
| 3 | `mag.verkle_bus` | 538 | 18 | 1 | 2026-08-14 |
| 4 | `mag.chain_query` | 533 | 20 | 0 | 2026-08-08 |
| 5 | `mag.flight_recorder` | 524 | 2 | 0 | 2026-09-25 |
| 6 | `mag.lite_guard` | 523 | 8 | 0 | 2026-09-14 |
| 7 | `mag.skill_ledger` | 522 | 24 | 8 | 2026-09-27 |
| 8 | `mag.headless` | 520 | 18 | 2 | 2026-08-19 |
| 9 | `mag.dormant` | 518 | 13 | 2 | 2026-09-27 |
| 10 | `mag.concurrency_gate` | 515 | 7 | 0 | 2026-09-14 |
| 11 | `mag.ox_seat` | 515 | 12 | 0 | 2026-08-25 |
| 12 | `mag.remedy` | 515 | 3 | 0 | 2026-08-04 |
| 13 | `mag.failure_kb` | 514 | 20 | 3 | 2026-09-27 |
| 14 | `mag.bard` | 513 | 8 | 1 | 2026-08-08 |
| 15 | `mag.destructive_receipt` | 513 | 1 | 0 | 2026-09-14 |
| 16 | `mag.fact_bus` | 513 | 1 | 0 | 2026-08-14 |
| 17 | `mag.flock_field` | 512 | 6 | 0 | 2026-08-14 |
| 18 | `mag.k8s_bridge` | 512 | 3 | 0 | 2026-08-14 |
| 19 | `mag.percolator` | 512 | 23 | 3 | 2026-09-14 |
| 20 | `mag.registry` | 512 | 16 | 1 | 2026-09-14 |
| 21 | `mag.session_card` | 512 | 2 | 0 | 2026-08-04 |
| 22 | `mag.work_contract` | 512 | 5 | 0 | 2026-09-14 |
| 23 | `mag.cache_map` | 511 | 8 | 1 | 2026-09-24 |
| 24 | `mag.gpu_k8s` | 511 | 5 | 0 | 2026-08-14 |
| 25 | `mag.idea_graph` | 511 | 6 | 1 | 2026-08-04 |

Reading: `mag.verkle_knot` is the deepest dependency root (560 of 1,034 modules transitively depend on it, 54.2 percent) while
`mag.training_events` is the most directly imported non-package module (66). `mag.dormant` is the classic fan-in leaf: 518
transitive dependents, zero outgoing deps of its own. Blast radius for any change to the top rows is over half the estate.

### 3b. Top 25 by direct importers

| # | module | direct importers | transitive dependents |
|---|---|---|---|
| 1 | `mag` | 730 | 505 |
| 2 | `mag.training_events` | 66 | 544 |
| 3 | `mag.orchestrator` | 64 | 505 |
| 4 | `mag.swarm_surface` | 63 | 505 |
| 5 | `mag.verkle_knot` | 57 | 560 |
| 6 | `mag.rib_bus` | 43 | 505 |
| 7 | `mag.operator_inbox` | 27 | 505 |
| 8 | `mag.swarm_worker` | 27 | 505 |
| 9 | `mag.skill_ledger` | 24 | 522 |
| 10 | `mag.game_world` | 23 | 510 |
| 11 | `mag.percolator` | 23 | 512 |
| 12 | `mag.chain_query` | 20 | 533 |
| 13 | `mag.failure_kb` | 20 | 514 |
| 14 | `mag.knowledge_graph` | 20 | 505 |
| 15 | `mag.memlang` | 20 | 505 |
| 16 | `mag.ghost` | 19 | 505 |
| 17 | `mag.preferences` | 19 | 507 |
| 18 | `mag.headless` | 18 | 520 |
| 19 | `mag.verkle_bus` | 18 | 538 |
| 20 | `mag.agent_knot` | 16 | 505 |
| 21 | `mag.registry` | 16 | 512 |
| 22 | `mag.seat_registry` | 16 | 505 |
| 23 | `mag.router` | 15 | 505 |
| 24 | `mag.browser_driver` | 14 | 507 |
| 25 | `mag.grok_rightsize` | 14 | 505 |

## 4. Cycles

Tarjan SCC over the explicit internal edge set (package-init implicit edges excluded from cycle detection so normal
parent/child package loads do not fabricate 2-cycles). Result: **6 SCCs with more than one node, sizes [298, 3, 3, 2, 2, 2]**; zero self-imports.

### 4a. The 298-module tangle

One giant strongly connected component of **298 modules** with **852 internal edges** holds 28.8 percent of the estate. It forms
because orchestrator-grade modules import one another through the package namespace (`from mag import X`, `from mag.y import z`),
closing loops across many hops - there is no single hub to cut (the package init itself has only 3 import lines); the verified
7-hop chain below is one instance, not a unique explanation.

Verified concrete round trip (every leg read at a real line this ask):

```
mag.abundance_rogue -> mag.knot_untangle -> mag.swarm_worker -> mag.router ->
mag.operator_inbox -> mag.ghost -> mag.republic_loop -> mag.abundance_rogue
```

Legs: `mag/abundance_rogue.py:96` `from mag import knot_untangle`; `mag/knot_untangle.py:181` `from mag import swarm_worker as sw`;
`mag/swarm_worker.py:496` `from mag.router import classify_depth`; `mag/router.py:260` `from mag.operator_inbox import status as inbox_status`;
`mag/operator_inbox.py:185` `from mag.ghost import log_frustration`; `mag/ghost.py:797` `from mag import republic_loop`;
`mag/republic_loop.py:58` `from mag import (tool_5ws, ..., abundance_rogue, ...)` (abundance_rogue named at line 72).

Membership (full, 298 modules):

```
mag, mag.abundance_rogue, mag.act, mag.adventure_moonshot, mag.afk_cadence, mag.afk_loop, mag.agent_cli,
mag.agent_desk, mag.agent_knot, mag.agent_state_router, mag.agentic_test_steal, mag.ai_landscape, mag.aos_bus_watcher,
mag.aos_grok, mag.archetype_image, mag.arrival, mag.arxiv_mine, mag.ask, mag.attractor_tools, mag.autonomous_research,
mag.autopilot, mag.autorun_common, mag.backlog_reform, mag.behavioral_synth, mag.bernaise, mag.billing_feed,
mag.biography, mag.blast, mag.bonds, mag.brief_local, mag.bus_cadence, mag.cache_watch, mag.campaign,
mag.campaign_runs, mag.cast_guard, mag.cast_server, mag.castle_foundation, mag.chain_substrate, mag.chat_source,
mag.chatgpt_bot, mag.cheap_swarm, mag.checkin_route, mag.chord_pipeline, mag.chronicle, mag.clawbot,
mag.compiler_lang, mag.compute_reconcile, mag.conductor, mag.console_render, mag.constitutional_critique,
mag.context_compression, mag.context_growth, mag.context_pack, mag.coordination, mag.copilot_bridge,
mag.corpus_ingest, mag.corpus_wave, mag.cost_ledger, mag.cost_simulator, mag.daemon, mag.data_source_watch,
mag.decision_framework, mag.deep_research_moonshot, mag.desk_dialogue, mag.desk_overseer, mag.desk_teaching,
mag.diamond_mine, mag.diary_node, mag.dirac_loop, mag.dispatch, mag.display, mag.distill, mag.doctor,
mag.dungeon_dev, mag.egregore_steal, mag.elevate, mag.emergence, mag.error_healer, mag.flock_scheduler,
mag.flock_shader, mag.flock_usage_guard, mag.free_frontend_swarm, mag.frontier_advisor, mag.frontier_council,
mag.frontier_gravity, mag.frontier_rib, mag.frontier_salon, mag.frontier_salon_cli, mag.frontier_scout,
mag.fuel_feed, mag.future_self, mag.game_battle_cycle, mag.game_brawl, mag.game_campaign, mag.game_curveball,
mag.game_dm, mag.game_dm_llm, mag.game_emulator, mag.game_entry, mag.game_flow, mag.game_freeze, mag.game_live,
mag.game_mud, mag.game_ramp, mag.game_salon, mag.game_world_render, mag.gap_frontier, mag.gap_routed_handoff,
mag.ghost, mag.ghost_cold_boot, mag.ghost_control, mag.ghost_experimenter, mag.ghost_grok_dashboard,
mag.ghost_memlance, mag.ghost_summon, mag.ghost_whisper, mag.glm_flash, mag.governance, mag.governor,
mag.governor_autorun, mag.gpu_ghost, mag.grok_bot, mag.grok_free, mag.grok_mirror, mag.grok_rightsize,
mag.grok_seat_burner, mag.grok_terminal, mag.grok_weave, mag.grokbot_cold_edges, mag.growth_cycle,
mag.guard, mag.harvest_fold, mag.health, mag.improve, mag.improve_loop, mag.intent_rightsize, mag.intention_brief,
mag.invariant, mag.invariant_lattice, mag.janitor, mag.judge, mag.knot_untangle, mag.knowledge_graph,
mag.lane_cadence, mag.lanes, mag.lattice_backfill, mag.lattice_loop, mag.law, mag.learn_rightsize,
mag.lens_chain, mag.lens_shader, mag.lifecycle, mag.live_report, mag.liveness_sense, mag.local_scheduler,
mag.loop_audit, mag.loop_doctor, mag.loop_feedback, mag.mem_invariant_map, mag.mem_ollama, mag.memlang,
mag.meta_percolate, mag.mixture_of_agents, mag.model_pick, mag.modules, mag.moonshot_engine, mag.narrative_engine,
mag.nervous_system, mag.ocean_model_mind, mag.ocean_persona, mag.operating_protocol, mag.operator_inbox,
mag.operator_os, mag.orchestrator, mag.organ_map, mag.orphan_sense, mag.osculating, mag.ox_availability,
mag.ox_fold, mag.ox_resident, mag.partner_puppet, mag.peer_handoff, mag.platform_kill, mag.ponytail_audit,
mag.popup_insights, mag.power, mag.prefix_prover, mag.press_digest, mag.primer, mag.pro_library, mag.problem_knot,
mag.process_reaper, mag.process_supervisor, mag.prompt_archaeology, mag.prospect_sim, mag.queue_gate,
mag.queue_learn, mag.queue_ops, mag.real_swarm, mag.reconstruct, mag.records, mag.refine_chain, mag.remote_control,
mag.renderman_ask, mag.republic_ambassador, mag.republic_feed, mag.republic_loop, mag.republic_os,
mag.resume_order, mag.rib_bus, mag.rib_os, mag.right_size_skills, mag.roshomon, mag.roshomon_mine,
mag.route_trace, mag.router, mag.run_trail, mag.run_worth, mag.runtime, mag.seat_availability, mag.seat_hunter,
mag.seat_registry, mag.seat_steer, mag.seats, mag.self_drive, mag.self_drive_cadence, mag.self_loop,
mag.self_steal, mag.self_train_data, mag.self_vision, mag.sentinel, mag.session_maze, mag.session_route,
mag.session_state_brief, mag.shadow_graph, mag.shadow_work, mag.shape_seed, mag.skill_pipeline, mag.skill_seat,
mag.socratic_research, mag.sovereign_dashboard, mag.sovereign_handshake, mag.spider, mag.standing_wave,
mag.steer, mag.steer_engine, mag.steer_swarm, mag.steer_telemetry, mag.steward, mag.supervisor, mag.surface_adapters,
mag.surface_instruction, mag.surface_render, mag.swarm_capacity, mag.swarm_economics, mag.swarm_emerge,
mag.swarm_health, mag.swarm_local_drain, mag.swarm_map, mag.swarm_self, mag.swarm_surface, mag.swarm_tools,
mag.swarm_worker, mag.switchboard, mag.tactical_framework, mag.temperature_stack, mag.territory_solver,
mag.throughput_model, mag.time_estimate, mag.tool_quant, mag.tool_synthesis, mag.trigger_learn, mag.tripartite,
mag.tripartite_boot, mag.trust_gate, mag.truth_audit, mag.vantage_audit, mag.verkle_audit, mag.verkle_lance,
mag.vessel_swarm, mag.visual_pack, mag.voice_dig_board, mag.voice_handoff, mag.voice_scratch, mag.voice_shadow,
mag.voice_skills, mag.voice_tasks, mag.voice_trigger, mag.voice_turn, mag.vram_memory, mag.water_computer,
mag.water_swarm, mag.wave_address, mag.wearable_swarm, mag.whisper_image, mag.word_skill_map, mag.work_loop,
mag.wow_manifest
```

### 4b. The small true cycles (all members listed)

- 3-cycle: `mag.agent_arena` <-> `mag.arena_adapter` <-> `mag.arena_learning`
- 3-cycle: `mag.coding_session_loop` <-> `mag.coding_session_orchestrator` <-> `mag.desk_observer`
- 2-cycle: `mag.registry` <-> `mag.session_card`
- 2-cycle: `mag.wow_bones` <-> `mag.wow_bones_session`
- 2-cycle: `mag.arxiv_harvest` <-> `mag.lane_runner`

Two of these were line-verified this ask: `mag/registry.py:456` `from mag.session_card import attach_card_to_dossier` vs
`mag/session_card.py:278` `from mag.registry import load_residual, publish_residual`; and `mag/lane_runner.py:957`
`from mag.arxiv_harvest import harvest` vs `mag/arxiv_harvest.py:134` `from mag.lane_runner import flash_call`.

## 5. Orphans (zero caller evidence anywhere)

Strict test: no AST import from any strong-universe file, no bare-sibling import, no dynamic import string, no `-m` or script-path
invocation, no doc mention in any of the 15,310 scanned files. These 3 modules are dead weight by this instrument:

| module | LOC | last modified | what it looks like |
|---|---|---|---|
| `mag._flag_dangling_20260925` | 107 | 2026-09-27 | one-shot repair script (name says so); referenced only in watch/ receipts and a comment in mag/verkle_compaction.py:232 |
| `mag.cooker` | 165 | 2026-09-24 | no `mag.cooker` import anywhere; `cooker` mentions are seed/engines/cooker.py, a different same-named module |
| `mag.lane_supervisor` | 236 | 2026-09-25 | named in tools/seed_v2.py only as a path string / cron sketch; never invoked |

Near-misses checked and EXCLUDED from the orphan list (each has a real caller or a doc mention): `mag.kvos_block` (imported by
`mag/desk_tools.py:172` as a bare sibling `import kvos_block`), `mag.catalog_rebuild` / `mag.gopher_lite` / `mag.librarian_catalog` /
`mag.steer_bus` (doc/comment mentions only, hence DOC-ONLY below, not orphans). The bare-sibling import form is invisible to a
naive `import mag` grep and silently changes orphan verdicts - the desk_tools case flipped one.

## 6. Entry-only modules (no import caller; invoked externally)

| module | evidence (files read this ask) |
|---|---|
| `mag.auth_switchboard` | `auth_status.cmd` (root) + `configs/auth_tracks.yaml` `-m mag.auth_switchboard` |
| `mag.cast_launch` | `backend/server.py:184` subprocess `[sys.executable, "-m", "mag.cast_launch", "launch", ...]` |
| `mag.kabuki_salon` | `scripts/astra_convo_loop.sh:57` `python -m mag.kabuki_salon salon ...` |
| `mag.research_worker` | `mag/orchestrator.py:861` subprocess `[..., "-m", "mag.research_worker", "--goal", goal, ...]` + `mag/swarm_worker.py` |
| `mag.seat_fork` | `scripts/hofw_001_seed.sh` `-m mag.seat_fork` |
| `mag.table_view_cache` | `dashboard/server.py:686` subprocess `[..., "-m", "mag.table_view_cache", <campaign_id>]` |
| `mag.verify_succession_contract` | `configs/succession_contract.yaml` |
| `mag.verkle_render` | `experiments/verkle_knot_standing_wave.yaml` |

These are live by invocation, not by import: they sit OUTSIDE the import graph and would not appear in a callers-only analysis.

## 7. Test-only modules (42)

Every caller is a test file. If the test suite is the only thing keeping them alive they are deletion candidates under any
production-caller standard:

```
mag._consensus_witness, mag.afk_orchestrator, mag.bare_numpy, mag.bones_adapter, mag.cache_identity, mag.capability_steal, mag.dashboard_plugin, mag.game_dfhack, mag.game_piece_tandem, mag.gygax_steal, mag.honest_cache_meter, mag.hydro_xor_sim, mag.icon_drop, mag.intervention_gate, mag.kv_seal, mag.lab_episode, mag.lane_effort, mag.lane_salon, mag.lattice_distance, mag.memory_map, mag.mud_steal, mag.no_win, mag.openclaw_catalog, mag.openclaw_patches, mag.oracle, mag.paste_pipeline, mag.perplexity_research, mag.physics_steal, mag.quest_roshomon, mag.quorum_window, mag.riddler_map, mag.rotation_harness, mag.seat_corpus, mag.skill_lifecycle, mag.social_hone, mag.spore_seed, mag.surface_steal, mag.trajectory_bounds, mag.verkle_compaction, mag.vram_hologram, mag.wireshark_steal, mag.wow_family
```

## 8. DOC-ONLY modules (277)

Referenced somewhere in tracked md/json/txt/py comments but never imported, never invoked, never tested. Full list (evidence
paths per module in the JSON, `doc_mention_files_sample`):

```
mag._bench_free_shelf, mag._cache_ab_probe, mag._codex_seat, mag._comb_tokens, mag._compare_chain_sources,
mag._conc_test_slot, mag._deep_research_verkle_dedupe, mag._demo_eyes_receipt, mag._demo_telepathy,
mag._diag_cache, mag._exp_a_cache_retrigger, mag._flag_dangling_264d0ba3, mag._gpu_probe_debug, mag._grok_corpus_burn,
mag._openclaw_real, mag._probe_burst_20260903, mag._probe_dangling, mag._probe_mcp, mag._probe_zai_balance,
mag._relane_game_tasks, mag._salon_burn, mag._verify_chain_now, mag._verify_concurrency_gate, mag._verify_queue_gate,
mag._verify_repair_state, mag._verify_rung5, mag._verify_sharp_edge, mag._verify_verkle_gate_spec,
mag._warm_rib, mag.abliterator_spawn_manifest, mag.accumulator, mag.adventure_one_shot, mag.agent_os_loop,
mag.agent_signature, mag.arena_bench, mag.auto_handoff, mag.auto_quantize, mag.autodrain, mag.autoglm,
mag.batch_scribe, mag.bay_organs_liveness_test, mag.behavior_catch, mag.board_tailer, mag.boot_check,
mag.breakthrough_loop, mag.burn_gate, mag.burn_steer, mag.cache_router, mag.cage_intake, mag.campaign_reader,
mag.campaign_simulator, mag.canon_gate, mag.canon_seal, mag.catalog, mag.catalog_rebuild, mag.chatgpt_desktop,
mag.chord, mag.chord_triangulate, mag.cites_at_birth, mag.claim_repair, mag.claims_verify, mag.cleanup_steal,
mag.cli, mag.cli.core, mag.cli.display, mag.code_map, mag.compiler_flywheel, mag.connectivity_sizer,
mag.corpus_selfsteal, mag.data_refinery, mag.decision_hook, mag.decl_attention, mag.depin, mag.disposition_sweep,
mag.dissector, mag.divergence_meter, mag.doctor_rightsize, mag.doctrine_statute, mag.dropbox_watcher,
mag.echo_net, mag.electron_seat, mag.emergence_test, mag.end_state, mag.engram, mag.epistemic_guard,
mag.falsifier_counter, mag.fanout, mag.feedback, mag.fermat_ractor, mag.final_steal, mag.fire_horse,
mag.fleet_intel, mag.flock_anim, mag.forge_daemon, mag.free_to_swarm, mag.frontier_batch, mag.frontier_intake,
mag.ga4_progression, mag.gab_seat, mag.game_produce, mag.gap_resolver, mag.gap_swarm_experiment, mag.gene_pool_feeder,
mag.gguf_cartography, mag.ghost_auto, mag.ghost_director, mag.ghost_doctor, mag.ghost_pylance, mag.ghost_server,
mag.git_divergence, mag.gopher_lite, mag.gpu_memweave, mag.grammar_transfer, mag.grok_desktop, mag.grok_hub,
mag.grok_route, mag.grok_steer, mag.hermes_warm_boot, mag.hero_simulation, mag.hf_space, mag.host_resolver,
mag.host_roundtrip, mag.hour_test, mag.interrupt_pipeline, mag.invariant_npcs, mag.invariant_surface,
mag.knot_at_close, mag.ladder, mag.lane_probe, mag.lattice_logic, mag.leaked_prompt_mine, mag.lens_tournament,
mag.librarian, mag.librarian_catalog, mag.lite_scale, mag.local_usable, mag.main_channel, mag.matrix_router,
mag.max_distill_arms, mag.maze_real, mag.mem_weave_distributor, mag.memory_consolidate, mag.memory_train_seed,
mag.mind_mine, mag.mindweave_eval, mag.mirror_control, mag.mrna_steal, mag.museum, mag.narrative_tests,
mag.north_star, mag.notion_api, mag.offline, mag.oh_fuck, mag.ontology_compiler.extract, mag.orphan_audit,
mag.overseer, mag.ox_alpha_steal, mag.ox_burn, mag.ox_escalate, mag.ox_gap, mag.ox_megaburn, mag.ox_megaburn2,
mag.ox_novelty_digest, mag.ox_probe, mag.ox_swarm, mag.p20_pending_wave, mag.pattern_mine, mag.percolator_heal_test,
mag.persistent_agent, mag.persona_direction, mag.persona_key, mag.perturbation_battery, mag.pin_audit,
mag.plan_mode, mag.play_benchmark, mag.poc_stage2, mag.portal, mag.provenance_gate, mag.race_harness,
mag.ractor_corpus, mag.read_receipts, mag.readout_controller, mag.reasoning_intake, mag.recreation_rib,
mag.refeed_guard, mag.refine_loop, mag.rel_mem_eval, mag.renderman, mag.republic, mag.research_director,
mag.rib_gif, mag.rib_k8s, mag.rib_renderer, mag.rib_store, mag.riddle_direction, mag.riddler_coherence,
mag.riddler_tap, mag.riddler_trajectory, mag.rightsize_wave, mag.room_state, mag.saelis_room, mag.saelis_world_brief,
mag.salon_50, mag.scifi_fantasy_steal, mag.scribe, mag.seat_probe, mag.seed_percolator, mag.seed_registry,
mag.self_advance, mag.self_audit, mag.self_hologram, mag.self_test, mag.session_koan, mag.session_ritual,
mag.shadow_quest, mag.shadow_slab, mag.shelf_pdf, mag.socratic_tree, mag.space_ear, mag.spawn_manifest,
mag.spine_exercise, mag.stale_sweep, mag.standing, mag.steal_lens, mag.steal_tools, mag.steer_receipt_wire,
mag.swarm_cycle, mag.swarm_quests, mag.swarm_run, mag.swarm_snapshot, mag.swarm_test, mag.table_turn_cli,
mag.tandem_key_test, mag.tavern_summon_guests, mag.team_knot, mag.telegram_desk, mag.template_invariant,
mag.tests.test_identity_schema_portability, mag.tests.verify_identity_coupling, mag.tesuji_fire, mag.thought_bank_app,
mag.thread_eye, mag.tool_lifecycle, mag.tool_retire, mag.topic_index, mag.topic_index_v3_tf_draft,
mag.tortoise_demo, mag.training_packager, mag.training_rightsize, mag.training_set, mag.trajectory_paths,
mag.trajectory_step, mag.transfer_gate, mag.trust_gate_audit_check, mag.usage_digest, mag.verify_gate,
mag.verkle_rib, mag.vertical_meter, mag.volume_fidelity, mag.vscode_seat, mag.warmed_cold_replay, mag.wave_cache,
mag.wave_fire, mag.whale_patrol, mag.whisper_route, mag.window_hop, mag.window_throttle, mag.witness_snapshot,
mag.work_tiers, mag.worldline_dungeon, mag.wow_steal, mag.x_auth_once, mag.x_chat_mine, mag.x_interceptor,
mag.x_posts_mine, mag.x_reply_radar, mag.x_surface
```

## 9. Test coverage (static import map + collect census)

Instrument and limits: coverage here = at least one tracked test file AST-imports the module. This is a STATIC map, not a
`coverage.py` execution measurement (not run; would need the full suite execution and is OWED below). The suite denominator
comes from a fresh run of `.venv/Scripts/python.exe -m pytest --collect-only -q` this ask: **2410 tests collected in 11.69s**
(2026-09-28; the AGENTS.md carrier reads 2,303 / 352 from 2026-09-27 - the collected count has drifted +107 since that
census moment; different moments, different denominators, per the census denominator law).

| metric | value |
|---|---|
| modules with >= 1 importing test file | 321 / 1034 (31.0%) |
| modules with ZERO importing test file | **713 / 1034 (69.0%)** |
| of which are ENTRY (invoked, untested by import) | 8 |
| top-tested module | `mag.orchestrator` (15 test files) |

Most-tested modules:

| module | test files importing it |
|---|---|
| `mag.orchestrator` | 15 |
| `mag.agent_cli` | 14 |
| `mag.training_events` | 13 |
| `mag.improve` | 12 |
| `mag.operator_inbox` | 10 |
| `mag.skill_ledger` | 8 |
| `mag.context_pack` | 7 |
| `mag.game_world` | 7 |
| `mag.swarm_surface` | 7 |
| `mag.doctor` | 6 |

The 713-module zero-test block includes most of the critical path's deeper rows: `mag.chain_query` (533 transitive dependents, 0 test
files), `mag.flight_recorder` (524 dependents, 0), `mag.lite_guard` (523, 0), `mag.concurrency_gate` (515, 0). The most depended-on
surface is also the least test-covered - coverage effort has clustered on tools and toys, not on load-bearing modules.

## 10. Last modified (git log, 684-commit history on HEAD)

| module | last commit date | (oldest 15) |
|---|---|---|
| `mag` | 2026-08-04 | |
| `mag.blast` | 2026-08-04 | |
| `mag.bonds` | 2026-08-04 | |
| `mag.canvas_bridge` | 2026-08-04 | |
| `mag.chat_source` | 2026-08-04 | |
| `mag.chord_lens` | 2026-08-04 | |
| `mag.chronicle` | 2026-08-04 | |
| `mag.cli` | 2026-08-04 | |
| `mag.cli.core` | 2026-08-04 | |
| `mag.cli.display` | 2026-08-04 | |
| `mag.diary` | 2026-08-04 | |
| `mag.field_steal` | 2026-08-04 | |
| `mag.idea_graph` | 2026-08-04 | |
| `mag.ingest_registry` | 2026-08-04 | |
| `mag.judge` | 2026-08-04 | |

Newest 15:

| module | last commit date |
|---|---|
| `mag.act` | 2026-09-28 |
| `mag.afk_loop` | 2026-09-28 |
| `mag.agent_cli` | 2026-09-28 |
| `mag.catalog_tags` | 2026-09-28 |
| `mag.frontier_salon` | 2026-09-28 |
| `mag.frontier_salon_cli` | 2026-09-28 |
| `mag.improve` | 2026-09-28 |
| `mag.router` | 2026-09-28 |
| `mag.spider` | 2026-09-28 |
| `mag.swarm_cycle` | 2026-09-28 |
| `mag._consensus_witness` | 2026-09-27 |
| `mag._flag_dangling_20260925` | 2026-09-27 |
| `mag._flag_dangling_264d0ba3` | 2026-09-27 |
| `mag.ask_router` | 2026-09-27 |
| `mag.brief_local` | 2026-09-27 |

650 of 1034 modules have not been touched since before 2026-08-29 (30+ days); 93 carry a commit from the last 3 days. Sample
verification: `git log -1 --format=%cs -- mag/verkle_knot.py` -> 2026-09-27, matching the JSON.

## 11. Full inventory (1034 rows)

Columns: module / LOC / internal deps count / direct importers / test files / last modified / status. Full dep and importer
NAME LISTS live in `f-09-graph.json` (`internal_deps`, `importers_internal`, `sibling_bare_deps`, `test_files`,
`transitive_dependents_count`, `external_dep_roots`); they are not abbreviated here by hand - the table carries counts only.

| module | loc | deps | importers | tests | last mod | status |
|---|---|---|---|---|---|---|
| `mag` | 18 | 1 | 730 | 1 | 2026-08-04 | OK |
| `mag._bench_free_shelf` | 60 | 0 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag._cache_ab_probe` | 65 | 1 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag._codex_seat` | 85 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag._comb_tokens` | 85 | 0 | 0 | 0 | 2026-08-19 | DOC-ONLY |
| `mag._compare_chain_sources` | 32 | 0 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag._conc_test_slot` | 78 | 1 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag._consensus_witness` | 109 | 3 | 0 | 1 | 2026-09-27 | TEST-ONLY |
| `mag._deep_research_verkle_dedupe` | 64 | 4 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag._demo_eyes_receipt` | 117 | 2 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag._demo_telepathy` | 174 | 2 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag._diag_cache` | 12 | 1 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag._exp_a_cache_retrigger` | 69 | 1 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag._flag_dangling_20260925` | 107 | 1 | 0 | 0 | 2026-09-27 | ORPHAN |
| `mag._flag_dangling_264d0ba3` | 98 | 1 | 0 | 0 | 2026-09-27 | DOC-ONLY |
| `mag._gpu_probe_debug` | 40 | 0 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag._grok_corpus_burn` | 104 | 1 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag._openclaw_real` | 20 | 1 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag._probe_burst_20260903` | 100 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag._probe_dangling` | 30 | 0 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag._probe_mcp` | 37 | 0 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag._probe_zai_balance` | 52 | 0 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag._relane_game_tasks` | 45 | 2 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag._salon_burn` | 97 | 1 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag._verify_chain_now` | 33 | 0 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag._verify_concurrency_gate` | 50 | 1 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag._verify_queue_gate` | 81 | 2 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag._verify_repair_state` | 17 | 0 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag._verify_rung5` | 51 | 2 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag._verify_sharp_edge` | 60 | 4 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag._verify_verkle_gate_spec` | 105 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag._warm_rib` | 19 | 1 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag.abliterator_spawn_manifest` | 129 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.abundance_rogue` | 219 | 3 | 1 | 1 | 2026-08-14 | OK |
| `mag.accumulator` | 281 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.act` | 249 | 2 | 1 | 1 | 2026-09-28 | OK |
| `mag.adventure_moonshot` | 246 | 5 | 1 | 1 | 2026-08-14 | OK |
| `mag.adventure_one_shot` | 203 | 1 | 0 | 0 | 2026-08-19 | DOC-ONLY |
| `mag.afk_cadence` | 285 | 6 | 1 | 1 | 2026-09-26 | OK |
| `mag.afk_loop` | 342 | 7 | 6 | 2 | 2026-09-28 | OK |
| `mag.afk_orchestrator` | 190 | 4 | 0 | 1 | 2026-09-26 | TEST-ONLY |
| `mag.agent_arena` | 504 | 4 | 2 | 4 | 2026-08-06 | OK |
| `mag.agent_behavior` | 146 | 2 | 1 | 0 | 2026-08-14 | OK |
| `mag.agent_cli` | 3140 | 16 | 4 | 14 | 2026-09-28 | OK |
| `mag.agent_corpus` | 271 | 1 | 3 | 2 | 2026-09-14 | OK |
| `mag.agent_desk` | 258 | 1 | 10 | 4 | 2026-09-14 | OK |
| `mag.agent_knot` | 335 | 4 | 16 | 2 | 2026-08-14 | OK |
| `mag.agent_os_loop` | 109 | 2 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.agent_signature` | 221 | 0 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.agent_state` | 467 | 1 | 8 | 3 | 2026-09-14 | OK |
| `mag.agent_state_router` | 130 | 1 | 4 | 0 | 2026-08-09 | OK |
| `mag.agentic_test_steal` | 155 | 1 | 2 | 0 | 2026-08-14 | OK |
| `mag.ai_landscape` | 330 | 2 | 1 | 0 | 2026-08-14 | OK |
| `mag.amd_window_guard` | 85 | 1 | 2 | 0 | 2026-08-14 | OK |
| `mag.aos_agent` | 315 | 3 | 1 | 0 | 2026-08-25 | OK |
| `mag.aos_bus_watcher` | 337 | 3 | 1 | 0 | 2026-08-25 | OK |
| `mag.aos_grok` | 326 | 2 | 2 | 0 | 2026-08-09 | OK |
| `mag.aos_live_view` | 361 | 0 | 1 | 0 | 2026-08-25 | OK |
| `mag.api_gateway` | 768 | 2 | 2 | 2 | 2026-09-26 | OK |
| `mag.api_server` | 124 | 2 | 0 | 1 | 2026-09-14 | OK |
| `mag.arc_seed` | 182 | 0 | 1 | 0 | 2026-09-14 | OK |
| `mag.archetype_image` | 366 | 2 | 2 | 0 | 2026-08-14 | OK |
| `mag.arena_adapter` | 285 | 1 | 1 | 1 | 2026-08-06 | OK |
| `mag.arena_bench` | 598 | 1 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.arena_learning` | 457 | 2 | 4 | 2 | 2026-08-06 | OK |
| `mag.arena_strategies` | 143 | 1 | 2 | 0 | 2026-08-06 | OK |
| `mag.arrival` | 205 | 1 | 2 | 2 | 2026-08-14 | OK |
| `mag.art_forge` | 170 | 0 | 1 | 0 | 2026-09-14 | OK |
| `mag.arxiv_harvest` | 180 | 1 | 1 | 0 | 2026-09-14 | OK |
| `mag.arxiv_mine` | 243 | 1 | 2 | 0 | 2026-08-14 | OK |
| `mag.ask` | 394 | 3 | 2 | 0 | 2026-08-07 | OK |
| `mag.ask_router` | 278 | 1 | 2 | 1 | 2026-09-27 | OK |
| `mag.atlas` | 79 | 1 | 2 | 0 | 2026-09-14 | OK |
| `mag.attention_ranker` | 255 | 4 | 1 | 1 | 2026-08-06 | OK |
| `mag.attractor_tools` | 162 | 4 | 6 | 0 | 2026-08-14 | OK |
| `mag.audit_log` | 21 | 0 | 1 | 0 | 2026-09-25 | OK |
| `mag.auth_switchboard` | 293 | 0 | 0 | 0 | 2026-09-14 | ENTRY |
| `mag.auto_handoff` | 137 | 1 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.auto_quantize` | 457 | 0 | 0 | 0 | 2026-08-09 | DOC-ONLY |
| `mag.autodrain` | 215 | 4 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag.autoglm` | 168 | 0 | 0 | 0 | 2026-09-16 | DOC-ONLY |
| `mag.autonomous_research` | 590 | 6 | 2 | 0 | 2026-08-25 | OK |
| `mag.autopilot` | 114 | 4 | 2 | 1 | 2026-08-05 | OK |
| `mag.autorun_common` | 101 | 4 | 3 | 1 | 2026-09-14 | OK |
| `mag.autorun_status` | 220 | 4 | 1 | 0 | 2026-08-05 | OK |
| `mag.backlog_reform` | 144 | 2 | 3 | 0 | 2026-08-14 | OK |
| `mag.bard` | 986 | 2 | 8 | 1 | 2026-08-08 | OK |
| `mag.bare_numpy` | 149 | 0 | 0 | 1 | 2026-08-14 | TEST-ONLY |
| `mag.basecamp` | 77 | 1 | 1 | 0 | 2026-09-14 | OK |
| `mag.bash_local` | 290 | 0 | 3 | 0 | 2026-09-14 | OK |
| `mag.batch_drain` | 231 | 1 | 1 | 0 | 2026-08-25 | OK |
| `mag.batch_scribe` | 206 | 2 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag.bay_organs` | 340 | 0 | 4 | 1 | 2026-09-14 | OK |
| `mag.bay_organs_liveness_test` | 375 | 1 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.behavior_catch` | 250 | 1 | 0 | 0 | 2026-08-07 | DOC-ONLY |
| `mag.behavioral_analytics` | 317 | 1 | 3 | 0 | 2026-08-08 | OK |
| `mag.behavioral_lensing` | 487 | 1 | 1 | 0 | 2026-08-09 | OK |
| `mag.behavioral_synth` | 154 | 1 | 2 | 2 | 2026-08-07 | OK |
| `mag.bernaise` | 211 | 6 | 3 | 0 | 2026-08-09 | OK |
| `mag.billing_feed` | 274 | 3 | 2 | 0 | 2026-08-14 | OK |
| `mag.biography` | 599 | 6 | 5 | 1 | 2026-09-14 | OK |
| `mag.blade_plan` | 151 | 0 | 0 | 1 | 2026-09-14 | OK |
| `mag.blast` | 576 | 2 | 1 | 0 | 2026-08-04 | OK |
| `mag.board_directive` | 177 | 0 | 1 | 0 | 2026-09-14 | OK |
| `mag.board_tailer` | 247 | 1 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.bonds` | 486 | 2 | 4 | 1 | 2026-08-04 | OK |
| `mag.bones_adapter` | 391 | 1 | 0 | 1 | 2026-09-16 | TEST-ONLY |
| `mag.bones_read` | 142 | 0 | 1 | 0 | 2026-08-25 | OK |
| `mag.boot` | 234 | 3 | 0 | 0 | 2026-09-14 | OK |
| `mag.boot_check` | 184 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.brain` | 223 | 9 | 0 | 1 | 2026-09-14 | OK |
| `mag.breakthrough_loop` | 234 | 3 | 0 | 0 | 2026-08-09 | DOC-ONLY |
| `mag.brief_local` | 227 | 4 | 1 | 0 | 2026-09-27 | OK |
| `mag.browser_driver` | 249 | 1 | 14 | 2 | 2026-09-25 | OK |
| `mag.browser_env` | 178 | 0 | 4 | 1 | 2026-08-07 | OK |
| `mag.btw_sidechannel` | 193 | 1 | 2 | 0 | 2026-08-14 | OK |
| `mag.budget_refactor` | 165 | 0 | 5 | 0 | 2026-08-14 | OK |
| `mag.build_audit` | 145 | 1 | 1 | 1 | 2026-08-06 | OK |
| `mag.burn_gate` | 81 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.burn_steer` | 261 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.bus_cadence` | 181 | 4 | 1 | 0 | 2026-08-19 | OK |
| `mag.cache_identity` | 511 | 0 | 0 | 1 | 2026-09-14 | TEST-ONLY |
| `mag.cache_map` | 404 | 0 | 8 | 1 | 2026-09-24 | OK |
| `mag.cache_router` | 226 | 2 | 0 | 0 | 2026-09-25 | DOC-ONLY |
| `mag.cache_shard` | 107 | 0 | 2 | 0 | 2026-08-14 | OK |
| `mag.cache_watch` | 149 | 3 | 1 | 0 | 2026-09-14 | OK |
| `mag.cadence_learn` | 200 | 0 | 5 | 1 | 2026-08-25 | OK |
| `mag.cage_intake` | 333 | 1 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.campaign` | 782 | 1 | 4 | 1 | 2026-09-14 | OK |
| `mag.campaign_reader` | 152 | 0 | 0 | 0 | 2026-08-09 | DOC-ONLY |
| `mag.campaign_runs` | 146 | 2 | 1 | 0 | 2026-08-19 | OK |
| `mag.campaign_simulator` | 402 | 1 | 0 | 0 | 2026-08-09 | DOC-ONLY |
| `mag.canon_gate` | 143 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.canon_seal` | 97 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.canvas_bridge` | 461 | 0 | 0 | 1 | 2026-08-04 | OK |
| `mag.capability_steal` | 250 | 6 | 0 | 1 | 2026-09-26 | TEST-ONLY |
| `mag.capture_guard` | 138 | 0 | 1 | 0 | 2026-08-14 | OK |
| `mag.cascade_research` | 247 | 0 | 1 | 0 | 2026-09-14 | OK |
| `mag.cast_guard` | 142 | 1 | 1 | 0 | 2026-09-14 | OK |
| `mag.cast_launch` | 72 | 1 | 0 | 0 | 2026-08-14 | ENTRY |
| `mag.cast_server` | 360 | 9 | 3 | 1 | 2026-09-14 | OK |
| `mag.castle_foundation` | 167 | 4 | 2 | 0 | 2026-08-14 | OK |
| `mag.catalog` | 194 | 0 | 0 | 0 | 2026-09-16 | DOC-ONLY |
| `mag.catalog_freshness` | 94 | 0 | 1 | 1 | 2026-09-27 | OK |
| `mag.catalog_rebuild` | 151 | 1 | 0 | 0 | 2026-09-27 | DOC-ONLY |
| `mag.catalog_rescan` | 386 | 3 | 0 | 1 | 2026-09-27 | OK |
| `mag.catalog_scan` | 333 | 0 | 2 | 1 | 2026-09-27 | OK |
| `mag.catalog_tags` | 211 | 0 | 1 | 1 | 2026-09-28 | OK |
| `mag.caveman_audit` | 140 | 0 | 2 | 1 | 2026-08-05 | OK |
| `mag.cdp_runner` | 99 | 0 | 1 | 0 | 2026-08-14 | OK |
| `mag.census_liveness` | 74 | 0 | 0 | 1 | 2026-09-27 | OK |
| `mag.chain_guard` | 213 | 1 | 2 | 2 | 2026-09-27 | OK |
| `mag.chain_query` | 298 | 0 | 20 | 0 | 2026-08-08 | OK |
| `mag.chain_substrate` | 196 | 2 | 3 | 0 | 2026-08-14 | OK |
| `mag.chan` | 339 | 1 | 1 | 1 | 2026-09-14 | OK |
| `mag.chat_source` | 483 | 1 | 6 | 2 | 2026-08-04 | OK |
| `mag.chatgpt_bot` | 151 | 3 | 2 | 1 | 2026-08-14 | OK |
| `mag.chatgpt_desktop` | 197 | 2 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.cheap_swarm` | 223 | 3 | 3 | 0 | 2026-08-25 | OK |
| `mag.checkin_route` | 392 | 3 | 1 | 0 | 2026-09-14 | OK |
| `mag.chord` | 113 | 2 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.chord_circuit` | 244 | 6 | 1 | 0 | 2026-08-25 | OK |
| `mag.chord_lens` | 355 | 0 | 1 | 0 | 2026-08-04 | OK |
| `mag.chord_pipeline` | 203 | 4 | 1 | 0 | 2026-08-14 | OK |
| `mag.chord_triangulate` | 200 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.chronicle` | 133 | 2 | 3 | 2 | 2026-08-04 | OK |
| `mag.cite_gate` | 454 | 0 | 1 | 0 | 2026-09-14 | OK |
| `mag.cites_at_birth` | 104 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.claim_repair` | 472 | 1 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.claims_desk` | 191 | 0 | 1 | 0 | 2026-08-25 | OK |
| `mag.claims_verify` | 125 | 2 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag.claritas` | 65 | 0 | 0 | 0 | 2026-09-24 | OK |
| `mag.clawbot` | 198 | 2 | 1 | 0 | 2026-08-14 | OK |
| `mag.cleanup` | 149 | 1 | 1 | 1 | 2026-08-14 | OK |
| `mag.cleanup_steal` | 121 | 2 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.cli` | 27 | 3 | 0 | 0 | 2026-08-04 | DOC-ONLY |
| `mag.cli.core` | 187 | 2 | 0 | 0 | 2026-08-04 | DOC-ONLY |
| `mag.cli.display` | 129 | 0 | 0 | 0 | 2026-08-04 | DOC-ONLY |
| `mag.clippy` | 234 | 3 | 0 | 0 | 2026-08-08 | OK |
| `mag.code_map` | 219 | 1 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.codex_seat` | 152 | 0 | 1 | 0 | 2026-08-25 | OK |
| `mag.coding_session_loop` | 557 | 8 | 4 | 5 | 2026-09-14 | OK |
| `mag.coding_session_orchestrator` | 396 | 3 | 5 | 1 | 2026-08-06 | OK |
| `mag.coding_session_runner` | 403 | 3 | 1 | 1 | 2026-08-06 | OK |
| `mag.comms_trail` | 262 | 1 | 3 | 1 | 2026-09-14 | OK |
| `mag.compass` | 249 | 0 | 6 | 0 | 2026-09-27 | OK |
| `mag.compiler_flywheel` | 179 | 3 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.compiler_lang` | 278 | 8 | 1 | 0 | 2026-08-14 | OK |
| `mag.compute_reconcile` | 202 | 4 | 2 | 1 | 2026-09-27 | OK |
| `mag.concurrency_gate` | 155 | 0 | 7 | 0 | 2026-09-14 | OK |
| `mag.conductor` | 191 | 5 | 5 | 3 | 2026-08-06 | OK |
| `mag.conductor_eval` | 86 | 1 | 0 | 1 | 2026-09-14 | OK |
| `mag.connectivity_sizer` | 217 | 0 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.console_render` | 125 | 3 | 1 | 0 | 2026-08-14 | OK |
| `mag.constants` | 7 | 0 | 1 | 0 | 2026-09-14 | OK |
| `mag.constitutional_critique` | 606 | 2 | 4 | 0 | 2026-09-27 | OK |
| `mag.context_admission` | 103 | 0 | 2 | 1 | 2026-09-14 | OK |
| `mag.context_checkpoint` | 475 | 2 | 3 | 1 | 2026-09-14 | OK |
| `mag.context_compression` | 491 | 4 | 1 | 1 | 2026-09-14 | OK |
| `mag.context_growth` | 174 | 1 | 1 | 0 | 2026-08-09 | OK |
| `mag.context_pack` | 1363 | 22 | 10 | 7 | 2026-09-27 | OK |
| `mag.cooker` | 165 | 1 | 0 | 0 | 2026-09-24 | ORPHAN |
| `mag.coordination` | 391 | 5 | 9 | 2 | 2026-08-07 | OK |
| `mag.copilot_bridge` | 381 | 4 | 2 | 0 | 2026-08-09 | OK |
| `mag.corpus_expand` | 151 | 1 | 1 | 0 | 2026-08-09 | OK |
| `mag.corpus_ingest` | 208 | 2 | 1 | 0 | 2026-08-14 | OK |
| `mag.corpus_query` | 434 | 0 | 3 | 0 | 2026-08-19 | OK |
| `mag.corpus_selfsteal` | 322 | 1 | 0 | 0 | 2026-09-16 | DOC-ONLY |
| `mag.corpus_wave` | 180 | 6 | 1 | 0 | 2026-08-14 | OK |
| `mag.cost_enforcer` | 487 | 2 | 3 | 0 | 2026-08-09 | OK |
| `mag.cost_governor` | 211 | 1 | 1 | 0 | 2026-09-14 | OK |
| `mag.cost_learn` | 342 | 3 | 8 | 0 | 2026-08-14 | OK |
| `mag.cost_ledger` | 105 | 2 | 2 | 1 | 2026-09-14 | OK |
| `mag.cost_simulator` | 217 | 1 | 2 | 1 | 2026-08-05 | OK |
| `mag.cost_truth` | 598 | 4 | 2 | 2 | 2026-09-27 | OK |
| `mag.cross_version` | 629 | 1 | 0 | 0 | 2026-08-08 | OK |
| `mag.daemon` | 196 | 7 | 2 | 0 | 2026-09-26 | OK |
| `mag.dashboard_plugin` | 106 | 5 | 0 | 1 | 2026-08-07 | TEST-ONLY |
| `mag.data_refinery` | 850 | 1 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.data_source_watch` | 162 | 1 | 1 | 0 | 2026-08-09 | OK |
| `mag.decision_framework` | 323 | 9 | 5 | 1 | 2026-08-08 | OK |
| `mag.decision_hook` | 91 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.decl_attention` | 741 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.deep_research_moonshot` | 235 | 6 | 1 | 1 | 2026-08-14 | OK |
| `mag.depin` | 575 | 3 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.desk_conductor` | 780 | 5 | 1 | 1 | 2026-08-09 | OK |
| `mag.desk_dialogue` | 1358 | 11 | 12 | 3 | 2026-08-06 | OK |
| `mag.desk_local_adapter` | 175 | 0 | 7 | 1 | 2026-08-06 | OK |
| `mag.desk_local_simulator` | 30 | 0 | 1 | 0 | 2026-08-06 | OK |
| `mag.desk_model_probe` | 227 | 2 | 1 | 1 | 2026-08-06 | OK |
| `mag.desk_observer` | 354 | 6 | 2 | 1 | 2026-08-06 | OK |
| `mag.desk_ops` | 201 | 2 | 0 | 0 | 2026-08-14 | OK |
| `mag.desk_orchestrator` | 91 | 2 | 0 | 1 | 2026-08-06 | OK |
| `mag.desk_orchestrator_memory` | 221 | 3 | 1 | 1 | 2026-08-06 | OK |
| `mag.desk_overseer` | 319 | 5 | 3 | 0 | 2026-08-06 | OK |
| `mag.desk_teaching` | 304 | 5 | 1 | 0 | 2026-08-06 | OK |
| `mag.desk_timing` | 174 | 0 | 3 | 1 | 2026-08-06 | OK |
| `mag.desk_tools` | 357 | 4 | 0 | 0 | 2026-09-14 | OK |
| `mag.destructive_receipt` | 168 | 0 | 1 | 0 | 2026-09-14 | OK |
| `mag.deterministic_scanner` | 212 | 1 | 0 | 0 | 2026-08-14 | OK |
| `mag.df_tileset` | 137 | 0 | 1 | 0 | 2026-08-07 | OK |
| `mag.diamond_mine` | 167 | 2 | 3 | 0 | 2026-08-14 | OK |
| `mag.diary` | 494 | 1 | 0 | 0 | 2026-08-04 | OK |
| `mag.diary_node` | 792 | 6 | 4 | 0 | 2026-09-14 | OK |
| `mag.dirac_loop` | 349 | 2 | 3 | 2 | 2026-09-27 | OK |
| `mag.dispatch` | 397 | 7 | 4 | 1 | 2026-08-06 | OK |
| `mag.display` | 171 | 3 | 4 | 1 | 2026-09-14 | OK |
| `mag.disposition_sweep` | 89 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.dissector` | 739 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.distill` | 157 | 1 | 1 | 1 | 2026-08-14 | OK |
| `mag.divergence_meter` | 108 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.docker_ops` | 254 | 0 | 3 | 1 | 2026-08-09 | OK |
| `mag.doctor` | 1362 | 5 | 5 | 6 | 2026-09-27 | OK |
| `mag.doctor_agent` | 436 | 3 | 2 | 0 | 2026-08-14 | OK |
| `mag.doctor_rightsize` | 192 | 2 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.doctrine_statute` | 127 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.dogfood_audit` | 371 | 2 | 2 | 0 | 2026-09-14 | OK |
| `mag.dormant` | 85 | 0 | 13 | 2 | 2026-09-27 | OK |
| `mag.drainer_stats` | 194 | 3 | 0 | 0 | 2026-08-08 | OK |
| `mag.dropbox_watcher` | 283 | 1 | 0 | 0 | 2026-08-09 | DOC-ONLY |
| `mag.dspy_sovereign` | 576 | 0 | 2 | 0 | 2026-08-09 | OK |
| `mag.dungeon_dev` | 202 | 2 | 6 | 0 | 2026-08-14 | OK |
| `mag.echo_net` | 152 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.ecosystem_surface` | 339 | 3 | 1 | 0 | 2026-08-14 | OK |
| `mag.effect_broker` | 608 | 3 | 2 | 1 | 2026-09-14 | OK |
| `mag.egregore_steal` | 132 | 1 | 2 | 0 | 2026-08-14 | OK |
| `mag.elder` | 94 | 1 | 2 | 1 | 2026-09-14 | OK |
| `mag.electron_seat` | 211 | 2 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.elevate` | 159 | 3 | 1 | 1 | 2026-08-09 | OK |
| `mag.embassy_deliver` | 383 | 2 | 0 | 1 | 2026-09-14 | OK |
| `mag.embassy_integrity` | 297 | 0 | 1 | 2 | 2026-08-25 | OK |
| `mag.emergence` | 247 | 6 | 3 | 0 | 2026-08-14 | OK |
| `mag.emergence_test` | 261 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.emergent_harvest` | 317 | 3 | 2 | 0 | 2026-08-14 | OK |
| `mag.end_state` | 161 | 5 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.engram` | 136 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.env_redirect` | 117 | 0 | 2 | 1 | 2026-09-27 | OK |
| `mag.env_registry` | 263 | 0 | 4 | 0 | 2026-08-06 | OK |
| `mag.epistemic_guard` | 165 | 0 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.error_healer` | 164 | 3 | 1 | 0 | 2026-08-09 | OK |
| `mag.events_key_schema` | 106 | 0 | 2 | 0 | 2026-09-27 | OK |
| `mag.events_scan` | 48 | 1 | 1 | 0 | 2026-09-27 | OK |
| `mag.evolving_wave` | 285 | 3 | 1 | 0 | 2026-08-25 | OK |
| `mag.exit_dialogue` | 357 | 1 | 1 | 0 | 2026-08-08 | OK |
| `mag.extension_deploy` | 71 | 0 | 0 | 0 | 2026-08-08 | OK |
| `mag.fact_bus` | 150 | 2 | 1 | 0 | 2026-08-14 | OK |
| `mag.factory_gate` | 77 | 0 | 2 | 1 | 2026-08-06 | OK |
| `mag.factory_machine` | 396 | 8 | 1 | 1 | 2026-08-06 | OK |
| `mag.failure_kb` | 830 | 2 | 20 | 3 | 2026-09-27 | OK |
| `mag.falsifier_counter` | 704 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.fanout` | 108 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.feature_lab` | 204 | 3 | 0 | 1 | 2026-08-06 | OK |
| `mag.feedback` | 102 | 2 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.fermat_ractor` | 971 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.field_steal` | 345 | 0 | 1 | 0 | 2026-08-04 | OK |
| `mag.final_steal` | 179 | 5 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.fire_horse` | 52 | 1 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.fireball_cycle` | 60 | 3 | 0 | 0 | 2026-09-14 | OK |
| `mag.fish_ear` | 146 | 0 | 1 | 0 | 2026-08-14 | OK |
| `mag.fleet_intel` | 194 | 2 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.flex_test` | 139 | 2 | 1 | 0 | 2026-08-14 | OK |
| `mag.flight_recorder` | 424 | 0 | 2 | 0 | 2026-09-25 | OK |
| `mag.flock_anim` | 314 | 1 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag.flock_field` | 266 | 0 | 6 | 0 | 2026-08-14 | OK |
| `mag.flock_grid` | 97 | 0 | 1 | 0 | 2026-08-14 | OK |
| `mag.flock_job` | 172 | 1 | 1 | 0 | 2026-08-14 | OK |
| `mag.flock_scheduler` | 203 | 3 | 3 | 0 | 2026-08-14 | OK |
| `mag.flock_shader` | 336 | 1 | 4 | 0 | 2026-08-14 | OK |
| `mag.flock_steal` | 226 | 7 | 1 | 0 | 2026-08-14 | OK |
| `mag.flock_usage_guard` | 151 | 3 | 1 | 0 | 2026-08-14 | OK |
| `mag.forge_daemon` | 166 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.fork_router` | 306 | 2 | 0 | 1 | 2026-08-07 | OK |
| `mag.framework_map` | 993 | 1 | 2 | 0 | 2026-08-08 | OK |
| `mag.free_frontend_swarm` | 130 | 2 | 2 | 0 | 2026-08-14 | OK |
| `mag.free_tier` | 186 | 2 | 1 | 1 | 2026-09-27 | OK |
| `mag.free_to_swarm` | 138 | 2 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag.frontier_advisor` | 153 | 5 | 3 | 1 | 2026-08-14 | OK |
| `mag.frontier_batch` | 158 | 2 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.frontier_council` | 417 | 3 | 3 | 3 | 2026-09-14 | OK |
| `mag.frontier_game` | 238 | 6 | 0 | 1 | 2026-08-19 | OK |
| `mag.frontier_gravity` | 357 | 2 | 1 | 0 | 2026-08-14 | OK |
| `mag.frontier_help` | 173 | 2 | 1 | 0 | 2026-08-09 | OK |
| `mag.frontier_intake` | 161 | 4 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.frontier_rib` | 189 | 3 | 4 | 0 | 2026-08-14 | OK |
| `mag.frontier_salon` | 400 | 4 | 3 | 2 | 2026-09-28 | OK |
| `mag.frontier_salon_cli` | 38 | 1 | 1 | 0 | 2026-09-28 | OK |
| `mag.frontier_scout` | 571 | 1 | 5 | 0 | 2026-08-09 | OK |
| `mag.frontier_steer` | 46 | 0 | 4 | 0 | 2026-08-14 | OK |
| `mag.fuel_feed` | 706 | 6 | 10 | 2 | 2026-09-27 | OK |
| `mag.future_self` | 143 | 5 | 1 | 0 | 2026-08-14 | OK |
| `mag.ga4_progression` | 699 | 1 | 0 | 0 | 2026-08-09 | DOC-ONLY |
| `mag.gab_seat` | 268 | 5 | 0 | 0 | 2026-08-19 | DOC-ONLY |
| `mag.game_battle_cycle` | 616 | 2 | 2 | 0 | 2026-08-07 | OK |
| `mag.game_brawl` | 1669 | 8 | 3 | 0 | 2026-08-07 | OK |
| `mag.game_brawl_perspectives` | 240 | 0 | 2 | 0 | 2026-08-07 | OK |
| `mag.game_campaign` | 4839 | 21 | 12 | 2 | 2026-09-27 | OK |
| `mag.game_curveball` | 456 | 2 | 2 | 0 | 2026-08-19 | OK |
| `mag.game_dfhack` | 127 | 3 | 0 | 1 | 2026-08-14 | TEST-ONLY |
| `mag.game_dice` | 32 | 0 | 4 | 0 | 2026-08-07 | OK |
| `mag.game_dm` | 229 | 5 | 3 | 1 | 2026-08-19 | OK |
| `mag.game_dm_llm` | 154 | 1 | 3 | 0 | 2026-08-19 | OK |
| `mag.game_dm_voice` | 319 | 1 | 5 | 0 | 2026-08-07 | OK |
| `mag.game_emulator` | 221 | 3 | 1 | 1 | 2026-08-14 | OK |
| `mag.game_entry` | 241 | 2 | 1 | 1 | 2026-08-14 | OK |
| `mag.game_environment` | 168 | 0 | 1 | 1 | 2026-08-14 | OK |
| `mag.game_flow` | 170 | 1 | 1 | 0 | 2026-08-19 | OK |
| `mag.game_freeze` | 433 | 2 | 2 | 0 | 2026-08-07 | OK |
| `mag.game_live` | 160 | 3 | 1 | 1 | 2026-08-14 | OK |
| `mag.game_mud` | 558 | 3 | 3 | 0 | 2026-08-25 | OK |
| `mag.game_narrate` | 119 | 0 | 2 | 0 | 2026-08-19 | OK |
| `mag.game_observer` | 257 | 1 | 1 | 0 | 2026-08-19 | OK |
| `mag.game_passage` | 204 | 0 | 2 | 0 | 2026-08-19 | OK |
| `mag.game_piece_tandem` | 244 | 1 | 0 | 1 | 2026-08-19 | TEST-ONLY |
| `mag.game_play` | 209 | 4 | 0 | 1 | 2026-08-19 | OK |
| `mag.game_portal` | 182 | 3 | 1 | 1 | 2026-08-14 | OK |
| `mag.game_produce` | 258 | 4 | 0 | 0 | 2026-08-19 | DOC-ONLY |
| `mag.game_ramp` | 575 | 7 | 3 | 1 | 2026-09-16 | OK |
| `mag.game_saga` | 114 | 1 | 2 | 0 | 2026-08-19 | OK |
| `mag.game_salon` | 493 | 4 | 1 | 0 | 2026-08-07 | OK |
| `mag.game_score` | 102 | 3 | 2 | 0 | 2026-08-19 | OK |
| `mag.game_view` | 314 | 1 | 2 | 0 | 2026-08-19 | OK |
| `mag.game_world` | 126 | 0 | 23 | 7 | 2026-08-14 | OK |
| `mag.game_world_map` | 94 | 0 | 1 | 0 | 2026-08-14 | OK |
| `mag.game_world_render` | 302 | 3 | 2 | 2 | 2026-09-14 | OK |
| `mag.gap_analysis` | 155 | 0 | 2 | 0 | 2026-08-09 | OK |
| `mag.gap_frontier` | 171 | 6 | 6 | 0 | 2026-08-14 | OK |
| `mag.gap_map` | 166 | 0 | 5 | 0 | 2026-08-09 | OK |
| `mag.gap_resolver` | 97 | 2 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.gap_routed_handoff` | 196 | 4 | 1 | 0 | 2026-08-14 | OK |
| `mag.gap_swarm_experiment` | 538 | 2 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.gene_pool_feeder` | 347 | 1 | 0 | 0 | 2026-09-27 | DOC-ONLY |
| `mag.gguf_cartography` | 584 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.ghost` | 4243 | 61 | 19 | 2 | 2026-09-27 | OK |
| `mag.ghost_auto` | 185 | 4 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.ghost_cold_boot` | 178 | 3 | 1 | 0 | 2026-09-14 | OK |
| `mag.ghost_control` | 140 | 7 | 2 | 0 | 2026-08-09 | OK |
| `mag.ghost_cross` | 506 | 2 | 1 | 0 | 2026-08-08 | OK |
| `mag.ghost_director` | 655 | 2 | 0 | 0 | 2026-08-08 | DOC-ONLY |
| `mag.ghost_doctor` | 151 | 4 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.ghost_experimenter` | 240 | 4 | 2 | 0 | 2026-08-14 | OK |
| `mag.ghost_grok_dashboard` | 184 | 4 | 2 | 0 | 2026-08-09 | OK |
| `mag.ghost_identity` | 143 | 0 | 2 | 0 | 2026-08-08 | OK |
| `mag.ghost_leak_detector` | 1055 | 2 | 2 | 0 | 2026-08-08 | OK |
| `mag.ghost_ledger` | 274 | 2 | 2 | 0 | 2026-08-09 | OK |
| `mag.ghost_memlance` | 439 | 1 | 4 | 2 | 2026-09-14 | OK |
| `mag.ghost_nudge` | 125 | 2 | 1 | 0 | 2026-08-09 | OK |
| `mag.ghost_pylance` | 336 | 0 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.ghost_server` | 115 | 1 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.ghost_spooky` | 164 | 2 | 1 | 1 | 2026-08-14 | OK |
| `mag.ghost_summon` | 347 | 2 | 10 | 1 | 2026-08-09 | OK |
| `mag.ghost_talk` | 147 | 5 | 0 | 1 | 2026-08-09 | OK |
| `mag.ghost_whisper` | 164 | 5 | 4 | 0 | 2026-08-14 | OK |
| `mag.git_divergence` | 118 | 0 | 0 | 0 | 2026-09-15 | DOC-ONLY |
| `mag.glm_flash` | 113 | 3 | 3 | 0 | 2026-09-14 | OK |
| `mag.gopher_lite` | 252 | 2 | 0 | 0 | 2026-09-25 | DOC-ONLY |
| `mag.governance` | 215 | 8 | 3 | 0 | 2026-08-06 | OK |
| `mag.governor` | 398 | 4 | 3 | 1 | 2026-08-25 | OK |
| `mag.governor_autorun` | 2184 | 81 | 6 | 4 | 2026-09-27 | OK |
| `mag.gpipes` | 402 | 4 | 0 | 1 | 2026-08-14 | OK |
| `mag.gpu_ghost` | 310 | 5 | 8 | 0 | 2026-09-27 | OK |
| `mag.gpu_k8s` | 229 | 3 | 5 | 0 | 2026-08-14 | OK |
| `mag.gpu_lifecycle` | 139 | 1 | 9 | 0 | 2026-08-14 | OK |
| `mag.gpu_memweave` | 114 | 3 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.grammar_transfer` | 267 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.grok_bot` | 291 | 4 | 6 | 0 | 2026-08-14 | OK |
| `mag.grok_brief` | 163 | 3 | 1 | 0 | 2026-08-14 | OK |
| `mag.grok_desktop` | 166 | 1 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.grok_free` | 384 | 4 | 4 | 0 | 2026-09-14 | OK |
| `mag.grok_frontier_loop` | 271 | 4 | 1 | 0 | 2026-08-14 | OK |
| `mag.grok_gate` | 84 | 0 | 5 | 0 | 2026-08-09 | OK |
| `mag.grok_hub` | 235 | 4 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.grok_mirror` | 355 | 4 | 2 | 0 | 2026-08-14 | OK |
| `mag.grok_rightsize` | 670 | 3 | 14 | 0 | 2026-09-14 | OK |
| `mag.grok_route` | 49 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.grok_seat_burner` | 504 | 1 | 6 | 1 | 2026-09-14 | OK |
| `mag.grok_steer` | 137 | 1 | 0 | 0 | 2026-08-19 | DOC-ONLY |
| `mag.grok_tandem` | 143 | 1 | 1 | 0 | 2026-09-14 | OK |
| `mag.grok_terminal` | 362 | 6 | 3 | 0 | 2026-08-09 | OK |
| `mag.grok_warm_rib` | 163 | 2 | 0 | 0 | 2026-09-14 | OK |
| `mag.grok_weave` | 203 | 7 | 1 | 0 | 2026-08-14 | OK |
| `mag.grokbot_cold_edges` | 187 | 4 | 1 | 0 | 2026-08-14 | OK |
| `mag.grounding_wave` | 976 | 0 | 1 | 3 | 2026-09-16 | OK |
| `mag.grove` | 151 | 0 | 0 | 2 | 2026-08-05 | OK |
| `mag.growth_cycle` | 464 | 5 | 1 | 1 | 2026-08-06 | OK |
| `mag.gstd_probe` | 210 | 2 | 1 | 1 | 2026-08-06 | OK |
| `mag.guard` | 105 | 4 | 2 | 0 | 2026-09-14 | OK |
| `mag.guard_registry` | 256 | 4 | 1 | 0 | 2026-08-14 | OK |
| `mag.guardrail_sentinel` | 150 | 1 | 0 | 0 | 2026-08-14 | OK |
| `mag.gygax_steal` | 161 | 2 | 0 | 1 | 2026-08-14 | TEST-ONLY |
| `mag.hall_shared_supper` | 164 | 0 | 1 | 0 | 2026-08-25 | OK |
| `mag.handoff_inbox` | 145 | 3 | 0 | 1 | 2026-08-06 | OK |
| `mag.harness` | 736 | 3 | 2 | 0 | 2026-09-14 | OK |
| `mag.harvest_fold` | 162 | 4 | 1 | 1 | 2026-08-19 | OK |
| `mag.headless` | 204 | 0 | 18 | 2 | 2026-08-19 | OK |
| `mag.health` | 366 | 4 | 14 | 1 | 2026-09-26 | OK |
| `mag.hermes_steering` | 341 | 0 | 1 | 0 | 2026-09-14 | OK |
| `mag.hermes_warm_boot` | 125 | 0 | 0 | 0 | 2026-09-25 | DOC-ONLY |
| `mag.hero_simulation` | 396 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.hf_space` | 586 | 0 | 0 | 0 | 2026-08-08 | DOC-ONLY |
| `mag.holographic_q` | 849 | 3 | 2 | 1 | 2026-09-14 | OK |
| `mag.honest_cache_meter` | 499 | 0 | 0 | 1 | 2026-09-14 | TEST-ONLY |
| `mag.hood` | 154 | 1 | 0 | 1 | 2026-09-14 | OK |
| `mag.host_resolver` | 207 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.host_roundtrip` | 111 | 3 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.hour_test` | 118 | 1 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.hydro_xor_sim` | 295 | 0 | 0 | 1 | 2026-09-16 | TEST-ONLY |
| `mag.icon_drop` | 377 | 2 | 0 | 3 | 2026-09-27 | TEST-ONLY |
| `mag.idea_flow` | 601 | 0 | 0 | 0 | 2026-09-14 | OK |
| `mag.idea_graph` | 538 | 0 | 6 | 1 | 2026-08-04 | OK |
| `mag.improve` | 2774 | 8 | 8 | 12 | 2026-09-28 | OK |
| `mag.improve_loop` | 329 | 8 | 5 | 1 | 2026-09-14 | OK |
| `mag.ingest_registry` | 557 | 0 | 3 | 0 | 2026-08-04 | OK |
| `mag.integrity_kernel` | 300 | 0 | 4 | 0 | 2026-08-25 | OK |
| `mag.intent_rightsize` | 240 | 6 | 2 | 0 | 2026-08-14 | OK |
| `mag.intention_brief` | 291 | 1 | 2 | 0 | 2026-08-07 | OK |
| `mag.interrupt_pipeline` | 220 | 4 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.intervention_gate` | 471 | 0 | 0 | 1 | 2026-09-25 | TEST-ONLY |
| `mag.invariant` | 322 | 4 | 3 | 1 | 2026-09-14 | OK |
| `mag.invariant_lattice` | 188 | 4 | 7 | 0 | 2026-08-14 | OK |
| `mag.invariant_ledger` | 186 | 2 | 2 | 0 | 2026-08-14 | OK |
| `mag.invariant_npcs` | 253 | 3 | 0 | 0 | 2026-08-19 | DOC-ONLY |
| `mag.invariant_surface` | 259 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.janitor` | 274 | 3 | 2 | 0 | 2026-08-08 | OK |
| `mag.job_floor` | 226 | 2 | 0 | 3 | 2026-08-08 | OK |
| `mag.jones_lens` | 126 | 0 | 7 | 0 | 2026-08-14 | OK |
| `mag.judge` | 139 | 1 | 1 | 0 | 2026-08-04 | OK |
| `mag.k8s_bridge` | 165 | 1 | 3 | 0 | 2026-08-14 | OK |
| `mag.kabuki_salon` | 180 | 1 | 0 | 0 | 2026-09-14 | ENTRY |
| `mag.key_law` | 108 | 0 | 1 | 0 | 2026-09-24 | OK |
| `mag.knot_at_close` | 281 | 3 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.knot_math` | 242 | 0 | 1 | 0 | 2026-08-04 | OK |
| `mag.knot_untangle` | 233 | 3 | 2 | 0 | 2026-08-14 | OK |
| `mag.knowledge_graph` | 561 | 4 | 20 | 0 | 2026-08-19 | OK |
| `mag.kv_seal` | 143 | 0 | 0 | 1 | 2026-09-22 | TEST-ONLY |
| `mag.kvos_block` | 113 | 0 | 1 | 0 | 2026-09-14 | OK |
| `mag.lab_episode` | 494 | 4 | 0 | 1 | 2026-09-14 | TEST-ONLY |
| `mag.ladder` | 199 | 3 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag.lane_breaker` | 137 | 0 | 1 | 0 | 2026-09-14 | OK |
| `mag.lane_cadence` | 271 | 1 | 4 | 2 | 2026-09-26 | OK |
| `mag.lane_effort` | 359 | 1 | 0 | 1 | 2026-09-25 | TEST-ONLY |
| `mag.lane_probe` | 151 | 0 | 0 | 0 | 2026-09-24 | DOC-ONLY |
| `mag.lane_runner` | 1142 | 6 | 2 | 1 | 2026-09-27 | OK |
| `mag.lane_salon` | 230 | 3 | 0 | 2 | 2026-09-27 | TEST-ONLY |
| `mag.lane_supervisor` | 236 | 3 | 0 | 0 | 2026-09-25 | ORPHAN |
| `mag.lanes` | 317 | 2 | 10 | 0 | 2026-09-27 | OK |
| `mag.lattice_backfill` | 404 | 1 | 1 | 1 | 2026-08-04 | OK |
| `mag.lattice_dashboard` | 258 | 1 | 0 | 0 | 2026-08-05 | OK |
| `mag.lattice_distance` | 132 | 0 | 0 | 1 | 2026-09-14 | TEST-ONLY |
| `mag.lattice_logic` | 257 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.lattice_loop` | 804 | 2 | 2 | 1 | 2026-08-05 | OK |
| `mag.lattice_query` | 131 | 0 | 3 | 1 | 2026-08-04 | OK |
| `mag.launch_pad` | 131 | 0 | 0 | 1 | 2026-08-04 | OK |
| `mag.law` | 323 | 4 | 1 | 1 | 2026-09-14 | OK |
| `mag.leaked_prompt_mine` | 139 | 1 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.learn_rightsize` | 165 | 2 | 2 | 0 | 2026-08-09 | OK |
| `mag.legacy_audit` | 332 | 2 | 0 | 1 | 2026-09-27 | OK |
| `mag.lens_chain` | 289 | 1 | 6 | 0 | 2026-08-14 | OK |
| `mag.lens_knot` | 193 | 1 | 11 | 2 | 2026-08-14 | OK |
| `mag.lens_library` | 534 | 2 | 6 | 0 | 2026-08-09 | OK |
| `mag.lens_shader` | 199 | 1 | 3 | 0 | 2026-08-14 | OK |
| `mag.lens_tournament` | 264 | 6 | 0 | 0 | 2026-08-09 | DOC-ONLY |
| `mag.librarian` | 259 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.librarian_catalog` | 206 | 0 | 0 | 0 | 2026-09-25 | DOC-ONLY |
| `mag.lifecycle` | 917 | 7 | 4 | 4 | 2026-09-26 | OK |
| `mag.line_builder` | 141 | 0 | 2 | 0 | 2026-08-14 | OK |
| `mag.link_library` | 397 | 0 | 1 | 2 | 2026-09-27 | OK |
| `mag.links_sha_ratchet` | 153 | 0 | 1 | 1 | 2026-09-27 | OK |
| `mag.links_split_gate` | 144 | 0 | 1 | 0 | 2026-09-27 | OK |
| `mag.lite_guard` | 266 | 1 | 8 | 0 | 2026-09-14 | OK |
| `mag.lite_scale` | 167 | 4 | 0 | 0 | 2026-09-16 | DOC-ONLY |
| `mag.live_feed` | 195 | 0 | 0 | 0 | 2026-08-08 | OK |
| `mag.live_ops_readiness` | 152 | 1 | 1 | 1 | 2026-09-14 | OK |
| `mag.live_report` | 151 | 4 | 1 | 0 | 2026-09-14 | OK |
| `mag.liveness_sense` | 257 | 6 | 2 | 0 | 2026-09-14 | OK |
| `mag.lm_studio` | 123 | 0 | 1 | 1 | 2026-09-14 | OK |
| `mag.local_mode` | 44 | 0 | 2 | 0 | 2026-08-07 | OK |
| `mag.local_playbook` | 323 | 3 | 3 | 0 | 2026-08-06 | OK |
| `mag.local_pulse` | 211 | 0 | 3 | 1 | 2026-08-06 | OK |
| `mag.local_scheduler` | 459 | 5 | 3 | 1 | 2026-09-14 | OK |
| `mag.local_usable` | 515 | 0 | 0 | 0 | 2026-08-07 | DOC-ONLY |
| `mag.loop_audit` | 335 | 2 | 6 | 1 | 2026-08-05 | OK |
| `mag.loop_breaker` | 259 | 1 | 2 | 2 | 2026-09-27 | OK |
| `mag.loop_doctor` | 130 | 1 | 5 | 0 | 2026-08-14 | OK |
| `mag.loop_feedback` | 108 | 2 | 4 | 0 | 2026-08-14 | OK |
| `mag.loop_health` | 225 | 1 | 0 | 0 | 2026-08-25 | OK |
| `mag.loops_registry` | 235 | 0 | 0 | 1 | 2026-08-08 | OK |
| `mag.lora_pipeline` | 550 | 0 | 3 | 0 | 2026-08-09 | OK |
| `mag.machine_target` | 76 | 0 | 4 | 0 | 2026-08-14 | OK |
| `mag.main_channel` | 458 | 3 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.manifest` | 192 | 1 | 3 | 0 | 2026-08-25 | OK |
| `mag.matrix_router` | 175 | 2 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.max_distill` | 256 | 0 | 2 | 1 | 2026-09-14 | OK |
| `mag.max_distill_arms` | 311 | 2 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.maze_real` | 152 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.mcp_http` | 45 | 2 | 1 | 0 | 2026-09-14 | OK |
| `mag.mcp_server` | 411 | 1 | 1 | 2 | 2026-09-27 | OK |
| `mag.mem_invariant_map` | 233 | 6 | 1 | 0 | 2026-08-14 | OK |
| `mag.mem_lands` | 218 | 4 | 1 | 0 | 2026-08-14 | OK |
| `mag.mem_ollama` | 259 | 2 | 2 | 0 | 2026-08-14 | OK |
| `mag.mem_weave_distributor` | 179 | 2 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.memlang` | 443 | 14 | 20 | 1 | 2026-09-14 | OK |
| `mag.memory_consolidate` | 218 | 0 | 0 | 0 | 2026-08-19 | DOC-ONLY |
| `mag.memory_events` | 160 | 0 | 4 | 2 | 2026-08-07 | OK |
| `mag.memory_map` | 214 | 1 | 0 | 1 | 2026-08-08 | TEST-ONLY |
| `mag.memory_train_seed` | 186 | 0 | 0 | 0 | 2026-08-19 | DOC-ONLY |
| `mag.memweave` | 198 | 4 | 2 | 0 | 2026-08-25 | OK |
| `mag.meta_lattice` | 125 | 0 | 1 | 0 | 2026-08-14 | OK |
| `mag.meta_percolate` | 234 | 2 | 3 | 0 | 2026-08-14 | OK |
| `mag.mind_mine` | 418 | 1 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag.mind_window` | 475 | 0 | 1 | 0 | 2026-08-25 | OK |
| `mag.mindweave_eval` | 270 | 4 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.mine_diamonds` | 248 | 0 | 1 | 0 | 2026-08-14 | OK |
| `mag.mirror_control` | 124 | 1 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.mixture_of_agents` | 423 | 1 | 2 | 0 | 2026-08-09 | OK |
| `mag.model_health` | 151 | 2 | 2 | 0 | 2026-08-14 | OK |
| `mag.model_pick` | 88 | 2 | 5 | 0 | 2026-08-09 | OK |
| `mag.modules` | 273 | 2 | 3 | 0 | 2026-08-04 | OK |
| `mag.moonshot_engine` | 228 | 4 | 1 | 1 | 2026-08-14 | OK |
| `mag.mrna_steal` | 87 | 1 | 0 | 0 | 2026-08-19 | DOC-ONLY |
| `mag.mud_steal` | 160 | 2 | 0 | 1 | 2026-08-14 | TEST-ONLY |
| `mag.museum` | 208 | 1 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag.mycelium` | 355 | 1 | 7 | 1 | 2026-08-19 | OK |
| `mag.narrative_engine` | 846 | 2 | 2 | 0 | 2026-08-09 | OK |
| `mag.narrative_tests` | 389 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.nervous_system` | 523 | 4 | 8 | 3 | 2026-09-14 | OK |
| `mag.no_win` | 121 | 0 | 0 | 1 | 2026-09-27 | TEST-ONLY |
| `mag.north_star` | 144 | 4 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.notion_api` | 179 | 0 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag.novelty_lens` | 171 | 2 | 3 | 0 | 2026-08-14 | OK |
| `mag.ocean_model_mind` | 310 | 4 | 1 | 0 | 2026-08-25 | OK |
| `mag.ocean_persona` | 170 | 3 | 1 | 0 | 2026-08-14 | OK |
| `mag.off_hours` | 338 | 0 | 2 | 1 | 2026-09-14 | OK |
| `mag.offerings` | 234 | 0 | 2 | 0 | 2026-09-27 | OK |
| `mag.offline` | 232 | 4 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.offpeak` | 161 | 0 | 3 | 1 | 2026-08-25 | OK |
| `mag.oh_fuck` | 115 | 6 | 0 | 0 | 2026-08-09 | DOC-ONLY |
| `mag.ollama_policy` | 121 | 0 | 6 | 1 | 2026-08-06 | OK |
| `mag.one_sizer` | 129 | 0 | 6 | 0 | 2026-08-14 | OK |
| `mag.ontology_compiler.extract` | 49 | 0 | 0 | 0 | 2026-09-08 | DOC-ONLY |
| `mag.openclaw_catalog` | 253 | 0 | 0 | 1 | 2026-09-14 | TEST-ONLY |
| `mag.openclaw_patches` | 252 | 0 | 0 | 1 | 2026-09-14 | TEST-ONLY |
| `mag.operating_protocol` | 114 | 2 | 2 | 1 | 2026-08-06 | OK |
| `mag.operator_inbox` | 461 | 4 | 27 | 10 | 2026-08-14 | OK |
| `mag.operator_mode` | 183 | 0 | 9 | 1 | 2026-09-14 | OK |
| `mag.operator_os` | 295 | 5 | 1 | 0 | 2026-08-19 | OK |
| `mag.ops_graph` | 446 | 7 | 0 | 0 | 2026-08-08 | OK |
| `mag.oracle` | 189 | 1 | 0 | 1 | 2026-08-14 | TEST-ONLY |
| `mag.orchestrator` | 2057 | 24 | 64 | 15 | 2026-09-27 | OK |
| `mag.organ_map` | 702 | 6 | 3 | 1 | 2026-09-14 | OK |
| `mag.orphan_audit` | 215 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.orphan_sense` | 204 | 6 | 5 | 0 | 2026-08-19 | OK |
| `mag.orphan_timer` | 268 | 2 | 4 | 0 | 2026-08-08 | OK |
| `mag.os_v2` | 166 | 3 | 0 | 0 | 2026-09-14 | OK |
| `mag.osculating` | 252 | 2 | 1 | 1 | 2026-08-14 | OK |
| `mag.overseer` | 183 | 2 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.ox_alpha_steal` | 195 | 1 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag.ox_availability` | 155 | 2 | 1 | 0 | 2026-08-25 | OK |
| `mag.ox_burn` | 122 | 1 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag.ox_escalate` | 139 | 1 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag.ox_fold` | 258 | 1 | 2 | 0 | 2026-08-25 | OK |
| `mag.ox_gap` | 176 | 1 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag.ox_megaburn` | 561 | 1 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag.ox_megaburn2` | 324 | 1 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag.ox_megaburn3` | 248 | 1 | 4 | 0 | 2026-08-25 | OK |
| `mag.ox_novelty_digest` | 87 | 0 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag.ox_novelty_index` | 164 | 1 | 2 | 0 | 2026-08-25 | OK |
| `mag.ox_percolate` | 199 | 1 | 1 | 0 | 2026-08-25 | OK |
| `mag.ox_probe` | 233 | 0 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag.ox_resident` | 502 | 8 | 4 | 0 | 2026-08-25 | OK |
| `mag.ox_scout` | 179 | 3 | 1 | 0 | 2026-08-25 | OK |
| `mag.ox_seat` | 183 | 0 | 12 | 0 | 2026-08-25 | OK |
| `mag.ox_swarm` | 299 | 2 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag.p20_pending_wave` | 142 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.partner_puppet` | 117 | 2 | 1 | 0 | 2026-08-09 | OK |
| `mag.party_subchain` | 359 | 0 | 10 | 5 | 2026-08-19 | OK |
| `mag.paste_pipeline` | 271 | 2 | 0 | 1 | 2026-09-27 | TEST-ONLY |
| `mag.pattern_mine` | 153 | 0 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.pdf_layout` | 538 | 1 | 1 | 0 | 2026-08-04 | OK |
| `mag.peer_handoff` | 260 | 3 | 7 | 0 | 2026-09-25 | OK |
| `mag.percolator` | 385 | 3 | 23 | 3 | 2026-09-14 | OK |
| `mag.percolator_heal_test` | 157 | 1 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.perplexity_research` | 324 | 0 | 0 | 1 | 2026-09-25 | TEST-ONLY |
| `mag.persistent_agent` | 445 | 3 | 0 | 0 | 2026-08-08 | DOC-ONLY |
| `mag.persona_direction` | 184 | 2 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.persona_key` | 208 | 0 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag.persona_recall` | 156 | 1 | 3 | 0 | 2026-08-14 | OK |
| `mag.personality_substrate` | 229 | 0 | 1 | 0 | 2026-08-08 | OK |
| `mag.perturbation_battery` | 551 | 3 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.phone_door` | 77 | 0 | 1 | 0 | 2026-09-14 | OK |
| `mag.phone_relay` | 250 | 0 | 1 | 0 | 2026-09-25 | OK |
| `mag.physics_steal` | 158 | 2 | 0 | 1 | 2026-08-14 | TEST-ONLY |
| `mag.pigeonhole` | 337 | 1 | 11 | 5 | 2026-08-07 | OK |
| `mag.pin_audit` | 110 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.plan` | 204 | 0 | 2 | 0 | 2026-08-04 | OK |
| `mag.plan_mode` | 41 | 0 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag.platform_kill` | 162 | 2 | 2 | 1 | 2026-09-27 | OK |
| `mag.play_benchmark` | 392 | 1 | 0 | 0 | 2026-08-07 | DOC-ONLY |
| `mag.poc_stage2` | 142 | 3 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag.policy` | 85 | 0 | 5 | 0 | 2026-08-04 | OK |
| `mag.policy_engine` | 497 | 0 | 3 | 1 | 2026-09-16 | OK |
| `mag.ponytail_audit` | 247 | 1 | 1 | 2 | 2026-08-14 | OK |
| `mag.popup_insights` | 159 | 2 | 1 | 0 | 2026-08-14 | OK |
| `mag.portal` | 200 | 3 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.power` | 736 | 8 | 6 | 2 | 2026-09-27 | OK |
| `mag.preferences` | 142 | 0 | 19 | 3 | 2026-08-09 | OK |
| `mag.prefix_prover` | 193 | 2 | 2 | 0 | 2026-08-25 | OK |
| `mag.preflight` | 179 | 1 | 1 | 0 | 2026-08-09 | OK |
| `mag.preload_selector` | 457 | 0 | 1 | 0 | 2026-09-14 | OK |
| `mag.press_digest` | 225 | 8 | 2 | 0 | 2026-08-09 | OK |
| `mag.primer` | 180 | 6 | 1 | 0 | 2026-08-14 | OK |
| `mag.pro_library` | 393 | 3 | 10 | 2 | 2026-08-14 | OK |
| `mag.probe_route` | 195 | 0 | 2 | 0 | 2026-09-24 | OK |
| `mag.problem_knot` | 240 | 2 | 2 | 0 | 2026-08-14 | OK |
| `mag.process_reaper` | 223 | 2 | 1 | 0 | 2026-09-19 | OK |
| `mag.process_supervisor` | 500 | 4 | 8 | 1 | 2026-09-27 | OK |
| `mag.prompt_archaeology` | 499 | 1 | 1 | 0 | 2026-08-09 | OK |
| `mag.prompt_lance` | 567 | 0 | 0 | 1 | 2026-09-27 | OK |
| `mag.proof` | 170 | 1 | 5 | 0 | 2026-08-25 | OK |
| `mag.prose_census` | 156 | 0 | 1 | 0 | 2026-09-14 | OK |
| `mag.prospect_sim` | 382 | 3 | 2 | 0 | 2026-08-09 | OK |
| `mag.provenance_gate` | 234 | 0 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag.quest_roshomon` | 297 | 3 | 0 | 1 | 2026-08-19 | TEST-ONLY |
| `mag.queue_analysis` | 265 | 2 | 1 | 0 | 2026-08-19 | OK |
| `mag.queue_gate` | 389 | 4 | 3 | 1 | 2026-09-26 | OK |
| `mag.queue_learn` | 216 | 2 | 1 | 0 | 2026-08-09 | OK |
| `mag.queue_ops` | 188 | 2 | 2 | 0 | 2026-08-09 | OK |
| `mag.queue_rightsize` | 247 | 1 | 1 | 0 | 2026-08-19 | OK |
| `mag.quorum_window` | 485 | 1 | 0 | 2 | 2026-09-27 | TEST-ONLY |
| `mag.race_harness` | 183 | 1 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.ractor_corpus` | 475 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.ractor_vessels` | 142 | 0 | 1 | 0 | 2026-09-14 | OK |
| `mag.rails` | 73 | 0 | 1 | 0 | 2026-08-04 | OK |
| `mag.ram_cache` | 132 | 0 | 2 | 0 | 2026-08-25 | OK |
| `mag.read_archive` | 127 | 0 | 2 | 0 | 2026-09-14 | OK |
| `mag.read_receipts` | 126 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.readout_controller` | 128 | 3 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.real_swarm` | 244 | 3 | 2 | 1 | 2026-08-25 | OK |
| `mag.reasoning_intake` | 423 | 1 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.reconstruct` | 169 | 4 | 1 | 1 | 2026-08-14 | OK |
| `mag.records` | 262 | 2 | 4 | 0 | 2026-09-14 | OK |
| `mag.recreation_rib` | 221 | 1 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.recurrence_gate` | 241 | 1 | 1 | 0 | 2026-08-14 | OK |
| `mag.refeed_guard` | 172 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.refine_chain` | 748 | 6 | 2 | 0 | 2026-08-14 | OK |
| `mag.refine_loop` | 696 | 9 | 0 | 0 | 2026-08-09 | DOC-ONLY |
| `mag.registry` | 491 | 1 | 16 | 1 | 2026-09-14 | OK |
| `mag.rel_mem_eval` | 249 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.release_registry` | 298 | 1 | 2 | 2 | 2026-09-27 | OK |
| `mag.remedy` | 146 | 0 | 3 | 0 | 2026-08-04 | OK |
| `mag.remote_control` | 138 | 6 | 2 | 1 | 2026-08-06 | OK |
| `mag.render_brief` | 46 | 0 | 1 | 0 | 2026-09-14 | OK |
| `mag.renderman` | 848 | 1 | 0 | 0 | 2026-08-19 | DOC-ONLY |
| `mag.renderman_ask` | 209 | 2 | 2 | 0 | 2026-08-09 | OK |
| `mag.repo_readiness` | 78 | 0 | 2 | 1 | 2026-08-06 | OK |
| `mag.republic` | 856 | 1 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.republic_ambassador` | 219 | 2 | 2 | 1 | 2026-08-14 | OK |
| `mag.republic_feed` | 162 | 6 | 1 | 0 | 2026-08-14 | OK |
| `mag.republic_governance` | 381 | 1 | 1 | 0 | 2026-08-19 | OK |
| `mag.republic_loop` | 505 | 82 | 2 | 0 | 2026-09-14 | OK |
| `mag.republic_os` | 359 | 3 | 2 | 1 | 2026-08-25 | OK |
| `mag.republic_wave` | 197 | 0 | 5 | 2 | 2026-08-14 | OK |
| `mag.research_class` | 256 | 1 | 5 | 0 | 2026-08-14 | OK |
| `mag.research_director` | 812 | 4 | 0 | 0 | 2026-08-08 | DOC-ONLY |
| `mag.research_fanout` | 477 | 3 | 3 | 1 | 2026-09-27 | OK |
| `mag.research_fold` | 169 | 1 | 4 | 1 | 2026-08-09 | OK |
| `mag.research_lens` | 408 | 4 | 8 | 0 | 2026-08-09 | OK |
| `mag.research_pack` | 782 | 1 | 7 | 1 | 2026-08-04 | OK |
| `mag.research_worker` | 117 | 1 | 0 | 0 | 2026-09-14 | ENTRY |
| `mag.resonance` | 194 | 1 | 2 | 1 | 2026-08-05 | OK |
| `mag.resource_governor` | 156 | 4 | 1 | 0 | 2026-08-14 | OK |
| `mag.resume_order` | 262 | 4 | 1 | 0 | 2026-08-14 | OK |
| `mag.rib_action` | 202 | 2 | 5 | 0 | 2026-08-14 | OK |
| `mag.rib_bus` | 245 | 5 | 43 | 1 | 2026-08-14 | OK |
| `mag.rib_cache` | 143 | 3 | 5 | 0 | 2026-09-14 | OK |
| `mag.rib_gif` | 121 | 3 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.rib_k8s` | 195 | 3 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.rib_os` | 138 | 4 | 1 | 0 | 2026-08-14 | OK |
| `mag.rib_renderer` | 99 | 3 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.rib_store` | 78 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.rib_struct` | 179 | 2 | 2 | 0 | 2026-08-14 | OK |
| `mag.riddle_direction` | 142 | 2 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag.riddler` | 521 | 0 | 7 | 2 | 2026-08-14 | OK |
| `mag.riddler_campaign` | 635 | 1 | 1 | 0 | 2026-08-09 | OK |
| `mag.riddler_coherence` | 165 | 1 | 0 | 0 | 2026-08-19 | DOC-ONLY |
| `mag.riddler_map` | 300 | 1 | 0 | 1 | 2026-09-14 | TEST-ONLY |
| `mag.riddler_sanitize` | 226 | 0 | 1 | 0 | 2026-09-14 | OK |
| `mag.riddler_tap` | 216 | 3 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.riddler_trajectory` | 153 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.riddler_transport` | 462 | 3 | 3 | 0 | 2026-08-14 | OK |
| `mag.right_size_skills` | 160 | 3 | 1 | 0 | 2026-09-14 | OK |
| `mag.rightsize_all` | 163 | 2 | 1 | 0 | 2026-08-09 | OK |
| `mag.rightsize_api` | 146 | 0 | 0 | 0 | 2026-08-09 | OK |
| `mag.rightsize_wave` | 140 | 0 | 0 | 0 | 2026-08-19 | DOC-ONLY |
| `mag.roadmap_runner` | 304 | 4 | 1 | 1 | 2026-08-06 | OK |
| `mag.room_state` | 293 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.roshomon` | 365 | 4 | 9 | 0 | 2026-08-14 | OK |
| `mag.roshomon_mine` | 166 | 3 | 2 | 1 | 2026-08-14 | OK |
| `mag.rotation_harness` | 200 | 1 | 0 | 1 | 2026-09-27 | TEST-ONLY |
| `mag.route` | 171 | 3 | 0 | 2 | 2026-08-07 | OK |
| `mag.route_trace` | 176 | 3 | 1 | 1 | 2026-08-14 | OK |
| `mag.router` | 1046 | 5 | 15 | 2 | 2026-09-28 | OK |
| `mag.routing_concert` | 312 | 4 | 0 | 1 | 2026-08-07 | OK |
| `mag.run_trail` | 1021 | 3 | 8 | 2 | 2026-08-06 | OK |
| `mag.run_worth` | 556 | 4 | 2 | 1 | 2026-08-06 | OK |
| `mag.runtime` | 205 | 4 | 6 | 1 | 2026-09-14 | OK |
| `mag.runtime_policy` | 56 | 0 | 3 | 1 | 2026-09-27 | OK |
| `mag.saelis_room` | 350 | 5 | 0 | 0 | 2026-09-27 | DOC-ONLY |
| `mag.saelis_seat` | 164 | 1 | 1 | 0 | 2026-08-19 | OK |
| `mag.saelis_world_brief` | 108 | 0 | 0 | 0 | 2026-08-19 | DOC-ONLY |
| `mag.salon_50` | 211 | 2 | 0 | 0 | 2026-09-15 | DOC-ONLY |
| `mag.salon_openclaw` | 309 | 1 | 1 | 0 | 2026-09-14 | OK |
| `mag.scale_salon` | 265 | 3 | 1 | 1 | 2026-09-27 | OK |
| `mag.schema_registry` | 306 | 0 | 1 | 0 | 2026-08-14 | OK |
| `mag.scifi_fantasy_steal` | 174 | 1 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.scribe` | 132 | 2 | 0 | 0 | 2026-08-09 | DOC-ONLY |
| `mag.scrum` | 273 | 2 | 5 | 0 | 2026-08-25 | OK |
| `mag.seal` | 215 | 1 | 1 | 0 | 2026-08-25 | OK |
| `mag.seat_availability` | 177 | 4 | 2 | 0 | 2026-08-25 | OK |
| `mag.seat_corpus` | 305 | 1 | 0 | 2 | 2026-09-27 | TEST-ONLY |
| `mag.seat_dispatch` | 320 | 4 | 2 | 0 | 2026-09-14 | OK |
| `mag.seat_feed` | 158 | 0 | 2 | 2 | 2026-08-04 | OK |
| `mag.seat_fork` | 70 | 0 | 0 | 0 | 2026-09-14 | ENTRY |
| `mag.seat_guard` | 390 | 3 | 0 | 0 | 2026-08-14 | OK |
| `mag.seat_hunter` | 703 | 1 | 4 | 0 | 2026-08-25 | OK |
| `mag.seat_probe` | 113 | 2 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag.seat_registry` | 290 | 2 | 16 | 2 | 2026-09-27 | OK |
| `mag.seat_steer` | 259 | 5 | 6 | 2 | 2026-08-19 | OK |
| `mag.seats` | 393 | 1 | 1 | 0 | 2026-08-04 | OK |
| `mag.seed_chain` | 143 | 2 | 1 | 0 | 2026-08-09 | OK |
| `mag.seed_percolator` | 134 | 1 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.seed_registry` | 519 | 1 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.seeds` | 167 | 1 | 2 | 0 | 2026-08-25 | OK |
| `mag.self_advance` | 158 | 5 | 0 | 0 | 2026-08-09 | DOC-ONLY |
| `mag.self_audit` | 329 | 6 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.self_drive` | 231 | 8 | 7 | 0 | 2026-08-09 | OK |
| `mag.self_drive_cadence` | 154 | 3 | 1 | 0 | 2026-08-09 | OK |
| `mag.self_hologram` | 150 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.self_loop` | 204 | 7 | 6 | 0 | 2026-08-14 | OK |
| `mag.self_steal` | 413 | 1 | 6 | 1 | 2026-09-14 | OK |
| `mag.self_test` | 196 | 0 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag.self_train_data` | 162 | 1 | 1 | 0 | 2026-08-14 | OK |
| `mag.self_vision` | 208 | 2 | 1 | 0 | 2026-08-14 | OK |
| `mag.sense` | 78 | 1 | 1 | 1 | 2026-08-04 | OK |
| `mag.sentinel` | 154 | 1 | 1 | 0 | 2026-08-14 | OK |
| `mag.session_bridge` | 356 | 1 | 0 | 0 | 2026-09-14 | OK |
| `mag.session_card` | 289 | 1 | 2 | 0 | 2026-08-04 | OK |
| `mag.session_dossier` | 666 | 8 | 1 | 0 | 2026-08-04 | OK |
| `mag.session_freeze` | 314 | 4 | 0 | 1 | 2026-08-08 | OK |
| `mag.session_koan` | 323 | 1 | 0 | 0 | 2026-08-09 | DOC-ONLY |
| `mag.session_maze` | 288 | 3 | 5 | 0 | 2026-08-19 | OK |
| `mag.session_overseer` | 311 | 3 | 0 | 0 | 2026-08-08 | OK |
| `mag.session_rib` | 270 | 2 | 1 | 0 | 2026-09-14 | OK |
| `mag.session_ritual` | 472 | 7 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.session_route` | 192 | 3 | 3 | 1 | 2026-08-19 | OK |
| `mag.session_state_brief` | 383 | 3 | 3 | 0 | 2026-09-27 | OK |
| `mag.shader_bus` | 180 | 1 | 1 | 0 | 2026-08-14 | OK |
| `mag.shader_rib` | 218 | 1 | 1 | 0 | 2026-08-14 | OK |
| `mag.shadow_graph` | 199 | 2 | 4 | 0 | 2026-08-14 | OK |
| `mag.shadow_quest` | 161 | 4 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.shadow_slab` | 122 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.shadow_work` | 149 | 3 | 4 | 0 | 2026-08-14 | OK |
| `mag.shape_map` | 282 | 2 | 3 | 0 | 2026-09-27 | OK |
| `mag.shape_seed` | 234 | 1 | 1 | 1 | 2026-08-14 | OK |
| `mag.shared_surface` | 427 | 5 | 0 | 4 | 2026-09-27 | OK |
| `mag.shelf_pdf` | 100 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.signal_flare` | 544 | 2 | 1 | 0 | 2026-08-08 | OK |
| `mag.signals` | 165 | 0 | 1 | 0 | 2026-08-14 | OK |
| `mag.single_feed` | 83 | 0 | 1 | 0 | 2026-09-14 | OK |
| `mag.skill_drop` | 198 | 1 | 1 | 1 | 2026-08-08 | OK |
| `mag.skill_ledger` | 346 | 0 | 24 | 8 | 2026-09-27 | OK |
| `mag.skill_lifecycle` | 421 | 1 | 0 | 1 | 2026-09-25 | TEST-ONLY |
| `mag.skill_pipeline` | 359 | 4 | 7 | 0 | 2026-08-14 | OK |
| `mag.skill_seat` | 113 | 3 | 2 | 1 | 2026-08-06 | OK |
| `mag.skills_pack` | 74 | 0 | 3 | 0 | 2026-08-04 | OK |
| `mag.social_hone` | 155 | 3 | 0 | 1 | 2026-08-14 | TEST-ONLY |
| `mag.socratic` | 160 | 1 | 0 | 0 | 2026-08-04 | OK |
| `mag.socratic_research` | 143 | 3 | 2 | 1 | 2026-08-14 | OK |
| `mag.socratic_tree` | 160 | 0 | 0 | 0 | 2026-08-09 | DOC-ONLY |
| `mag.solved_surface` | 118 | 0 | 1 | 0 | 2026-08-14 | OK |
| `mag.source_trace` | 391 | 0 | 3 | 1 | 2026-09-27 | OK |
| `mag.sovereign_dashboard` | 245 | 10 | 1 | 0 | 2026-08-09 | OK |
| `mag.sovereign_handshake` | 246 | 2 | 1 | 1 | 2026-08-14 | OK |
| `mag.space_ear` | 148 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.spawn_manifest` | 343 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.spec_gate` | 201 | 0 | 2 | 2 | 2026-08-09 | OK |
| `mag.spider` | 270 | 7 | 3 | 1 | 2026-09-28 | OK |
| `mag.spine_exercise` | 152 | 6 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.spore_seed` | 196 | 2 | 0 | 1 | 2026-09-25 | TEST-ONLY |
| `mag.stack` | 553 | 12 | 0 | 2 | 2026-08-07 | OK |
| `mag.stale_sweep` | 98 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.standing` | 313 | 5 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag.standing_wave` | 282 | 1 | 1 | 0 | 2026-08-14 | OK |
| `mag.state_brief` | 260 | 3 | 0 | 0 | 2026-08-09 | OK |
| `mag.state_quantizer` | 485 | 2 | 2 | 0 | 2026-08-08 | OK |
| `mag.state_snapshot` | 153 | 0 | 4 | 1 | 2026-08-08 | OK |
| `mag.stateless_research` | 282 | 9 | 1 | 0 | 2026-08-14 | OK |
| `mag.steal_first` | 446 | 1 | 2 | 0 | 2026-08-08 | OK |
| `mag.steal_lens` | 119 | 3 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.steal_pack` | 185 | 5 | 5 | 0 | 2026-08-14 | OK |
| `mag.steal_protocol_probe` | 81 | 0 | 0 | 0 | 2026-08-06 | OK |
| `mag.steal_steer` | 188 | 1 | 6 | 0 | 2026-08-14 | OK |
| `mag.steal_tools` | 193 | 1 | 0 | 0 | 2026-08-19 | DOC-ONLY |
| `mag.steer` | 186 | 1 | 5 | 1 | 2026-08-19 | OK |
| `mag.steer_bridge` | 152 | 1 | 0 | 1 | 2026-08-08 | OK |
| `mag.steer_bus` | 76 | 0 | 1 | 0 | 2026-09-14 | OK |
| `mag.steer_engine` | 175 | 3 | 4 | 0 | 2026-08-14 | OK |
| `mag.steer_receipt_wire` | 86 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.steer_router` | 209 | 1 | 1 | 0 | 2026-08-14 | OK |
| `mag.steer_swarm` | 191 | 4 | 2 | 0 | 2026-08-14 | OK |
| `mag.steer_telemetry` | 307 | 5 | 3 | 0 | 2026-08-14 | OK |
| `mag.steiniger_lens` | 199 | 0 | 1 | 0 | 2026-08-04 | OK |
| `mag.steward` | 413 | 3 | 2 | 3 | 2026-08-06 | OK |
| `mag.story` | 494 | 1 | 0 | 0 | 2026-08-04 | OK |
| `mag.subscriptions` | 184 | 1 | 1 | 1 | 2026-09-27 | OK |
| `mag.subswarm_health` | 149 | 1 | 1 | 0 | 2026-08-14 | OK |
| `mag.suno_zeitgeist` | 125 | 0 | 1 | 0 | 2026-09-14 | OK |
| `mag.supervisor` | 209 | 2 | 1 | 1 | 2026-08-04 | OK |
| `mag.surface_adapters` | 215 | 2 | 1 | 1 | 2026-08-14 | OK |
| `mag.surface_audit` | 140 | 1 | 0 | 1 | 2026-09-14 | OK |
| `mag.surface_instruction` | 242 | 1 | 2 | 1 | 2026-08-14 | OK |
| `mag.surface_render` | 827 | 8 | 1 | 0 | 2026-08-25 | OK |
| `mag.surface_steal` | 128 | 1 | 0 | 1 | 2026-09-14 | TEST-ONLY |
| `mag.surrogate` | 387 | 1 | 1 | 0 | 2026-08-14 | OK |
| `mag.swarm_capacity` | 154 | 3 | 1 | 0 | 2026-08-14 | OK |
| `mag.swarm_control` | 139 | 0 | 3 | 0 | 2026-08-14 | OK |
| `mag.swarm_cycle` | 230 | 2 | 0 | 0 | 2026-09-28 | DOC-ONLY |
| `mag.swarm_economics` | 151 | 2 | 1 | 0 | 2026-08-14 | OK |
| `mag.swarm_emerge` | 172 | 5 | 1 | 0 | 2026-08-14 | OK |
| `mag.swarm_grok_watch` | 163 | 0 | 1 | 0 | 2026-09-25 | OK |
| `mag.swarm_health` | 258 | 7 | 7 | 0 | 2026-09-14 | OK |
| `mag.swarm_local_drain` | 249 | 1 | 2 | 1 | 2026-09-14 | OK |
| `mag.swarm_map` | 173 | 3 | 3 | 0 | 2026-08-14 | OK |
| `mag.swarm_quests` | 261 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.swarm_render` | 182 | 3 | 1 | 0 | 2026-08-14 | OK |
| `mag.swarm_rightsize` | 242 | 1 | 5 | 0 | 2026-08-14 | OK |
| `mag.swarm_run` | 156 | 2 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.swarm_self` | 295 | 5 | 3 | 0 | 2026-08-14 | OK |
| `mag.swarm_snapshot` | 299 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.swarm_surface` | 110 | 1 | 63 | 7 | 2026-09-14 | OK |
| `mag.swarm_test` | 248 | 0 | 0 | 0 | 2026-08-09 | DOC-ONLY |
| `mag.swarm_tools` | 456 | 11 | 5 | 0 | 2026-09-14 | OK |
| `mag.swarm_worker` | 702 | 8 | 27 | 2 | 2026-09-27 | OK |
| `mag.switchboard` | 829 | 7 | 7 | 2 | 2026-09-14 | OK |
| `mag.switchboard_v2` | 926 | 2 | 3 | 1 | 2026-09-16 | OK |
| `mag.system_map` | 186 | 5 | 1 | 0 | 2026-08-07 | OK |
| `mag.system_telemetry` | 175 | 1 | 1 | 0 | 2026-08-14 | OK |
| `mag.table_turn_cli` | 13 | 1 | 0 | 0 | 2026-08-19 | DOC-ONLY |
| `mag.table_view_cache` | 37 | 1 | 0 | 0 | 2026-08-19 | ENTRY |
| `mag.tactical_framework` | 153 | 1 | 1 | 1 | 2026-08-14 | OK |
| `mag.tandem_key_test` | 78 | 1 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag.tangent` | 347 | 1 | 0 | 0 | 2026-08-04 | OK |
| `mag.tapestry` | 752 | 2 | 0 | 1 | 2026-08-06 | OK |
| `mag.tapestry_visual` | 190 | 0 | 1 | 1 | 2026-08-05 | OK |
| `mag.task_router` | 282 | 3 | 3 | 0 | 2026-08-09 | OK |
| `mag.tavern_chat` | 144 | 0 | 1 | 0 | 2026-09-14 | OK |
| `mag.tavern_summon_guests` | 52 | 1 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.team_knot` | 368 | 3 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag.telegram_desk` | 181 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.temperature_stack` | 703 | 4 | 2 | 3 | 2026-09-27 | OK |
| `mag.template_invariant` | 228 | 1 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.territory_solver` | 301 | 6 | 1 | 0 | 2026-08-14 | OK |
| `mag.test_dummy` | 80 | 0 | 3 | 0 | 2026-08-09 | OK |
| `mag.test_runner` | 193 | 2 | 1 | 0 | 2026-08-25 | OK |
| `mag.tests.test_identity_schema_portability` | 159 | 3 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.tests.verify_identity_coupling` | 262 | 3 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.tesuji_fire` | 434 | 2 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.tesuji_map` | 174 | 0 | 2 | 0 | 2026-09-14 | OK |
| `mag.tesuji_probes` | 476 | 0 | 1 | 0 | 2026-09-14 | OK |
| `mag.tesuji_shell` | 264 | 2 | 12 | 3 | 2026-08-06 | OK |
| `mag.tesuji_surface` | 491 | 1 | 1 | 0 | 2026-08-09 | OK |
| `mag.the_margin` | 549 | 0 | 1 | 0 | 2026-09-14 | OK |
| `mag.thought_bank` | 56 | 0 | 1 | 0 | 2026-09-14 | OK |
| `mag.thought_bank_app` | 117 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.thread_eye` | 98 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.throughput_model` | 153 | 1 | 1 | 0 | 2026-08-14 | OK |
| `mag.time_estimate` | 134 | 3 | 1 | 0 | 2026-08-14 | OK |
| `mag.token_chain` | 398 | 0 | 1 | 1 | 2026-08-06 | OK |
| `mag.token_economy` | 205 | 0 | 3 | 0 | 2026-08-04 | OK |
| `mag.tokenomics` | 432 | 0 | 2 | 0 | 2026-08-09 | OK |
| `mag.tool_5ws` | 115 | 0 | 2 | 0 | 2026-08-14 | OK |
| `mag.tool_lifecycle` | 151 | 3 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.tool_manifest` | 217 | 0 | 1 | 0 | 2026-08-14 | OK |
| `mag.tool_quant` | 134 | 2 | 3 | 1 | 2026-08-14 | OK |
| `mag.tool_retire` | 196 | 2 | 0 | 0 | 2026-08-09 | DOC-ONLY |
| `mag.tool_synthesis` | 451 | 10 | 1 | 0 | 2026-08-14 | OK |
| `mag.top_processes` | 87 | 0 | 1 | 0 | 2026-09-14 | OK |
| `mag.topic_index` | 376 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.topic_index_v3_tf_draft` | 231 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.topic_orphan` | 121 | 1 | 1 | 0 | 2026-08-09 | OK |
| `mag.tortoise_demo` | 136 | 2 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.training_events` | 196 | 0 | 66 | 13 | 2026-08-07 | OK |
| `mag.training_packager` | 309 | 1 | 0 | 0 | 2026-08-09 | DOC-ONLY |
| `mag.training_rightsize` | 106 | 1 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.training_set` | 146 | 1 | 0 | 0 | 2026-08-09 | DOC-ONLY |
| `mag.trajectory_bounds` | 94 | 0 | 0 | 1 | 2026-09-14 | TEST-ONLY |
| `mag.trajectory_paths` | 118 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.trajectory_rib` | 191 | 1 | 0 | 1 | 2026-09-14 | OK |
| `mag.trajectory_step` | 173 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.transfer_gate` | 667 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.trigger_learn` | 245 | 3 | 2 | 0 | 2026-08-14 | OK |
| `mag.tripartite` | 282 | 5 | 4 | 0 | 2026-08-14 | OK |
| `mag.tripartite_boot` | 536 | 5 | 4 | 1 | 2026-08-06 | OK |
| `mag.trust_gate` | 258 | 2 | 3 | 0 | 2026-09-25 | OK |
| `mag.trust_gate_audit_check` | 101 | 2 | 0 | 0 | 2026-09-25 | DOC-ONLY |
| `mag.truth_audit` | 177 | 5 | 1 | 0 | 2026-09-14 | OK |
| `mag.tts` | 236 | 0 | 4 | 0 | 2026-09-27 | OK |
| `mag.unsloth_seat` | 492 | 2 | 1 | 1 | 2026-08-09 | OK |
| `mag.usage_digest` | 283 | 1 | 0 | 0 | 2026-09-27 | DOC-ONLY |
| `mag.usage_forecast` | 240 | 4 | 0 | 0 | 2026-08-09 | OK |
| `mag.usage_monitor` | 179 | 3 | 5 | 0 | 2026-08-14 | OK |
| `mag.vantage_audit` | 196 | 5 | 1 | 1 | 2026-08-14 | OK |
| `mag.vast_cost` | 336 | 1 | 2 | 1 | 2026-09-14 | OK |
| `mag.vast_launcher` | 496 | 1 | 2 | 0 | 2026-09-14 | OK |
| `mag.vast_train` | 109 | 0 | 0 | 1 | 2026-08-06 | OK |
| `mag.verb` | 513 | 0 | 0 | 1 | 2026-09-19 | OK |
| `mag.verified_clock` | 162 | 3 | 1 | 0 | 2026-08-25 | OK |
| `mag.verify_gate` | 234 | 2 | 0 | 0 | 2026-08-25 | DOC-ONLY |
| `mag.verify_succession_contract` | 150 | 0 | 0 | 0 | 2026-09-14 | ENTRY |
| `mag.verkle_artifact` | 112 | 0 | 0 | 1 | 2026-09-14 | OK |
| `mag.verkle_audit` | 440 | 4 | 2 | 1 | 2026-09-14 | OK |
| `mag.verkle_bus` | 293 | 1 | 18 | 1 | 2026-08-14 | OK |
| `mag.verkle_compaction` | 397 | 2 | 0 | 1 | 2026-09-27 | TEST-ONLY |
| `mag.verkle_knot` | 921 | 0 | 57 | 5 | 2026-09-27 | OK |
| `mag.verkle_lance` | 457 | 2 | 3 | 0 | 2026-08-14 | OK |
| `mag.verkle_render` | 117 | 0 | 0 | 0 | 2026-08-19 | ENTRY |
| `mag.verkle_rib` | 124 | 0 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.vertical_meter` | 112 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.vessel_swarm` | 222 | 2 | 1 | 1 | 2026-08-14 | OK |
| `mag.virtual_desk_loop` | 680 | 1 | 0 | 1 | 2026-08-05 | OK |
| `mag.vision` | 125 | 0 | 2 | 0 | 2026-08-25 | OK |
| `mag.visual_pack` | 609 | 2 | 2 | 0 | 2026-08-04 | OK |
| `mag.voice_dictate` | 191 | 0 | 2 | 1 | 2026-08-09 | OK |
| `mag.voice_dig_board` | 467 | 3 | 4 | 1 | 2026-08-07 | OK |
| `mag.voice_handoff` | 508 | 6 | 1 | 1 | 2026-08-07 | OK |
| `mag.voice_lanes` | 237 | 0 | 1 | 0 | 2026-08-07 | OK |
| `mag.voice_pipeline` | 336 | 0 | 1 | 1 | 2026-08-07 | OK |
| `mag.voice_scratch` | 413 | 2 | 1 | 1 | 2026-08-07 | OK |
| `mag.voice_self` | 100 | 2 | 1 | 0 | 2026-08-14 | OK |
| `mag.voice_shadow` | 242 | 1 | 1 | 1 | 2026-08-07 | OK |
| `mag.voice_skills` | 75 | 1 | 1 | 0 | 2026-09-14 | OK |
| `mag.voice_stt` | 178 | 0 | 3 | 0 | 2026-08-07 | OK |
| `mag.voice_tasks` | 264 | 2 | 2 | 0 | 2026-08-07 | OK |
| `mag.voice_trigger` | 172 | 3 | 1 | 0 | 2026-08-19 | OK |
| `mag.voice_turn` | 1778 | 21 | 5 | 1 | 2026-09-14 | OK |
| `mag.volume_fidelity` | 563 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.vram_hologram` | 205 | 1 | 0 | 1 | 2026-08-14 | TEST-ONLY |
| `mag.vram_memory` | 138 | 4 | 3 | 0 | 2026-08-19 | OK |
| `mag.vscode_feed` | 222 | 3 | 0 | 0 | 2026-08-08 | OK |
| `mag.vscode_seat` | 179 | 2 | 0 | 0 | 2026-08-19 | DOC-ONLY |
| `mag.warmed_cold_replay` | 498 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.warning_monitor` | 206 | 1 | 1 | 1 | 2026-08-08 | OK |
| `mag.water_computer` | 881 | 4 | 3 | 2 | 2026-09-27 | OK |
| `mag.water_graph` | 275 | 0 | 1 | 2 | 2026-09-27 | OK |
| `mag.water_swarm` | 129 | 4 | 1 | 1 | 2026-08-14 | OK |
| `mag.wave` | 656 | 6 | 2 | 0 | 2026-08-19 | OK |
| `mag.wave_address` | 179 | 1 | 1 | 0 | 2026-08-14 | OK |
| `mag.wave_cache` | 21 | 1 | 0 | 0 | 2026-08-19 | DOC-ONLY |
| `mag.wave_fire` | 154 | 2 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.wearable_swarm` | 208 | 5 | 1 | 0 | 2026-08-14 | OK |
| `mag.whale_patrol` | 320 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.whisper_image` | 289 | 2 | 2 | 1 | 2026-08-14 | OK |
| `mag.whisper_route` | 139 | 3 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.win_powershell` | 44 | 0 | 3 | 0 | 2026-09-26 | OK |
| `mag.window_audit` | 113 | 1 | 2 | 0 | 2026-09-26 | OK |
| `mag.window_bus` | 258 | 2 | 1 | 0 | 2026-08-14 | OK |
| `mag.window_hop` | 118 | 1 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.window_throttle` | 379 | 1 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.wireshark_steal` | 143 | 1 | 0 | 1 | 2026-08-14 | TEST-ONLY |
| `mag.witness_snapshot` | 68 | 1 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.word_skill_map` | 238 | 3 | 3 | 0 | 2026-08-09 | OK |
| `mag.work_contract` | 112 | 0 | 5 | 0 | 2026-09-14 | OK |
| `mag.work_loop` | 335 | 7 | 2 | 1 | 2026-09-26 | OK |
| `mag.work_register` | 181 | 2 | 6 | 0 | 2026-08-25 | OK |
| `mag.work_tiers` | 106 | 0 | 0 | 0 | 2026-08-09 | DOC-ONLY |
| `mag.workspace_api` | 102 | 0 | 0 | 1 | 2026-08-04 | OK |
| `mag.world_rib` | 173 | 0 | 8 | 1 | 2026-08-14 | OK |
| `mag.worldline_dungeon` | 552 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.worldline_seed` | 1073 | 2 | 2 | 0 | 2026-09-14 | OK |
| `mag.wow_bones` | 371 | 1 | 3 | 3 | 2026-09-16 | OK |
| `mag.wow_bones_session` | 272 | 1 | 3 | 3 | 2026-09-16 | OK |
| `mag.wow_family` | 325 | 0 | 0 | 1 | 2026-09-15 | TEST-ONLY |
| `mag.wow_manifest` | 115 | 3 | 1 | 1 | 2026-08-14 | OK |
| `mag.wow_player` | 434 | 0 | 0 | 1 | 2026-09-16 | OK |
| `mag.wow_steal` | 389 | 0 | 0 | 0 | 2026-09-15 | DOC-ONLY |
| `mag.wow_world` | 373 | 2 | 1 | 1 | 2026-09-16 | OK |
| `mag.write_strip` | 165 | 0 | 2 | 1 | 2026-09-25 | OK |
| `mag.x_auth_once` | 30 | 1 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.x_chat_mine` | 95 | 1 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.x_control_surface` | 678 | 1 | 2 | 0 | 2026-08-25 | OK |
| `mag.x_interceptor` | 206 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.x_oauth` | 551 | 0 | 2 | 0 | 2026-09-14 | OK |
| `mag.x_posts_mine` | 124 | 1 | 0 | 0 | 2026-08-14 | DOC-ONLY |
| `mag.x_reply_radar` | 105 | 0 | 0 | 0 | 2026-09-14 | DOC-ONLY |
| `mag.x_surface` | 132 | 2 | 0 | 0 | 2026-08-14 | DOC-ONLY |

## 12. Limits and OWED

- Static analysis only: no module was executed this ask. Import edges are import-time truth; lazy imports inside functions are
  included as edges (they are import-time when first called) and are labeled by nothing finer than that.
- No `coverage.py` execution run: the 31.0 percent coverage figure is a static import map over tracked test files, not executed line
  coverage. OWED: one `coverage run -m pytest -q` + `coverage json` pass to replace the static map with executed coverage.
- Test-mapping direction only: tests importing a module proves the test targets it; it does not prove the module's behavior is
  meaningfully asserted.
- `-m` regex hits inside py docstrings/comments are demoted to weak evidence (they are prose, e.g. the `mag/framework_map.py`
  command catalog); only subprocess list literals count as strong py invocation evidence. md/txt/memory/ archive mentions never
  gate a status.
- Script-path invocations (`python mag/x.py`) were scanned in shell scripts only; zero modules gained callers that way this run.
- Two strong-universe py files fail AST parse and are invisible to the import graph: `training/lora/train_ghost.py` and
  `training/vast_package/train_ghost.py` (SyntaxError line 11). Neither is under mag/; no mag/ module failed to parse.
- The 298-module SCC is a fact of the explicit edge set; which loop is 'the' root cause is a judgment call, and the verified
  7-hop chain above is one instance, not a unique explanation.
- Verkle chain tip and CURRENT.md untouched; no runtime state modified; analysis ran read-only plus this banked file set.

- f-09, flash50, 2026-09-28 -
