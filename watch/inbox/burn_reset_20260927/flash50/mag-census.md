# mag/ module census (item f-24, 2026-09-28)

Instrument: `watch/inbox/burn_reset_20260927/flash50/f-24_census.py`, run with `./.venv/Scripts/python.exe` (Python 3.11.15) at 2026-09-28 19:12:11. Snapshot of one tree at one moment: HEAD `946473060` on branch `mag/run-beta1-factory-build-audi-20260806T231709Z`, working tree includes uncommitted edits (mtime column shows them).

## Method (read before quoting any number)

- **Population:** every `*.py` file under `mag/` on disk at census moment, found with `os.walk`, `__pycache__` skipped. Cross-check: `find mag -name "*.py" -type f | wc -l` = 1034 files; `git ls-files mag | grep -c "\.py$"` = 1034 tracked.
- **lines:** `wc -l` semantics (count of `\n` bytes). Instrument total must equal `find mag -name "*.py" | xargs wc -l` = 294316 (measured before the run); see Verification below.
- **public functions:** `ast.parse` of each file; module-level `def`/`async def` whose name does not start with `_`. Decorated defs included; methods inside classes are NOT in this column (classes have their own column).
- **public classes:** module-level `class` names not starting `_`.
- **last modified:** two instruments. `mtime` = filesystem mtime, local time, includes uncommitted edits. `last commit` = newest `git log --no-merges --name-only -- mag/` entry touching the path; renamed files map under their current name only.
- **tests:** corpus = `tests/**.py` (373 files) + `mag/tests/**.py` (2 files) = 375 test files. A module HAS TESTS when at least one test file textually references its import name (`mag.foo`), a `from mag import foo`, a `from mag import (foo, ...)`, a relative import resolving to it, or its path (`mag/foo.py`). The value shown is the count of distinct referencing test files. Textual matching, so it is an upper bound on true importing test files.
- **readers:** repo files with extension in {py, pyw, cmd, bat, ps1, sh, yaml, yml, toml, cfg, ini} outside `tests/`, `mag/tests/`, `watch/`, hidden dirs and `__pycache__` (2451 files scanned), matching the same reference forms as tests. `watch/` excluded: scratch instruments and prose, not durable code. Archival copies of code excluded: `_archaeology_out/` (951 py files, 2026-09-05 disk-image of an older repo state), `corpus/` (3402 py, session-artifact copies), `attic/` (105 py, retired code), `mine/` (15800 py, raw third-party repo dumps mined for training data), `dist_audit/` (1076 py, dated audit bundles each containing a full `mag/` copy), `local_sovereign_agent/` (a nested succession-audit snapshot of this very repo). Textual mentions inside archives are not live reads. Self-references excluded. `.json`/`.jsonl` data files not scanned. Reader counts are lower bounds for modules reached only through generic dispatchers (`mag.cmd` passes `%*`, dispatch tables never name the module).
- **reference semantics:** textual, not runtime: an import of `mag.sub.mod` credits `mod` AND the `sub` and root `__init__` chains (executing a submodule executes its inits). References inside comments/docstrings/strings count.

## Summary

| metric | value |
|---|---|
| modules in mag/ | 1034 |
| total lines | 294316 |
| AST parse failures | 0 |
| modules with >=1 public function | 1012 |
| public functions total | 5233 |
| modules with >=1 public class | 83 |
| public classes total | 205 |
| modules referenced by >=1 test file | 335 of 1034 (32.4%) |
| modules with ZERO test-file references | 699 |
| modules with >=1 non-test reader | 791 |
| modules with ZERO readers and ZERO test refs | 216 |
| test corpus files | 375 |
| reader-corpus files scanned | 2451 |

### Largest modules (top 15 by lines)

| module | lines | pub fns | test files | readers |
|---|---|---|---|---|
| `mag/game_campaign.py` | 4838 | 17 | 2 | 23 |
| `mag/ghost.py` | 4242 | 30 | 5 | 41 |
| `mag/agent_cli.py` | 3139 | 31 | 14 | 21 |
| `mag/improve.py` | 2773 | 19 | 12 | 14 |
| `mag/governor_autorun.py` | 2183 | 12 | 7 | 19 |
| `mag/orchestrator.py` | 2056 | 26 | 20 | 101 |
| `mag/voice_turn.py` | 1777 | 5 | 2 | 9 |
| `mag/game_brawl.py` | 1668 | 12 | 0 | 4 |
| `mag/context_pack.py` | 1362 | 6 | 9 | 19 |
| `mag/doctor.py` | 1361 | 12 | 10 | 24 |
| `mag/desk_dialogue.py` | 1357 | 18 | 7 | 15 |
| `mag/lane_runner.py` | 1141 | 24 | 3 | 15 |
| `mag/worldline_seed.py` | 1072 | 4 | 0 | 4 |
| `mag/ghost_leak_detector.py` | 1054 | 15 | 0 | 4 |
| `mag/router.py` | 1045 | 5 | 6 | 20 |

### Most-referenced modules (top 15 by reader count)

| module | readers | test files | lines |
|---|---|---|---|
| `mag/__init__.py` | 1340 | 308 | 17 |
| `mag/orchestrator.py` | 101 | 20 | 2056 |
| `mag/verkle_knot.py` | 88 | 6 | 920 |
| `mag/training_events.py` | 73 | 14 | 195 |
| `mag/swarm_surface.py` | 66 | 6 | 109 |
| `mag/rib_bus.py` | 50 | 1 | 244 |
| `mag/ghost.py` | 41 | 5 | 4242 |
| `mag/aos_live_view.py` | 34 | 0 | 360 |
| `mag/operator_inbox.py` | 34 | 11 | 460 |
| `mag/swarm_worker.py` | 33 | 4 | 701 |
| `mag/game_world.py` | 32 | 7 | 125 |
| `mag/headless.py` | 30 | 2 | 203 |
| `mag/lite_guard.py` | 30 | 0 | 265 |
| `mag/percolator.py` | 30 | 2 | 384 |
| `mag/skill_ledger.py` | 30 | 7 | 345 |

### Modules with zero test-file references (699)

`mag/_bench_free_shelf.py`, `mag/_cache_ab_probe.py`, `mag/_codex_seat.py`, `mag/_comb_tokens.py`, `mag/_compare_chain_sources.py`, `mag/_conc_test_slot.py`, `mag/_deep_research_verkle_dedupe.py`, `mag/_demo_eyes_receipt.py`, `mag/_demo_telepathy.py`, `mag/_diag_cache.py`, `mag/_exp_a_cache_retrigger.py`, `mag/_flag_dangling_20260925.py`, `mag/_flag_dangling_264d0ba3.py`, `mag/_gpu_probe_debug.py`, `mag/_grok_corpus_burn.py`, `mag/_openclaw_real.py`, `mag/_probe_burst_20260903.py`, `mag/_probe_dangling.py`, `mag/_probe_mcp.py`, `mag/_probe_zai_balance.py`, `mag/_relane_game_tasks.py`, `mag/_salon_burn.py`, `mag/_verify_chain_now.py`, `mag/_verify_concurrency_gate.py`, `mag/_verify_queue_gate.py`, `mag/_verify_repair_state.py`, `mag/_verify_rung5.py`, `mag/_verify_sharp_edge.py`, `mag/_verify_verkle_gate_spec.py`, `mag/_warm_rib.py`, `mag/abliterator_spawn_manifest.py`, `mag/accumulator.py`, `mag/adventure_one_shot.py`, `mag/agent_behavior.py`, `mag/agent_os_loop.py`, `mag/agent_signature.py`, `mag/agent_state_router.py`, `mag/agentic_test_steal.py`, `mag/ai_landscape.py`, `mag/amd_window_guard.py`, `mag/aos_agent.py`, `mag/aos_bus_watcher.py`, `mag/aos_grok.py`, `mag/aos_live_view.py`, `mag/arc_seed.py`, `mag/archetype_image.py`, `mag/arena_bench.py`, `mag/arena_strategies.py`, `mag/art_forge.py`, `mag/arxiv_harvest.py`, `mag/arxiv_mine.py`, `mag/ask.py`, `mag/atlas.py`, `mag/attractor_tools.py`, `mag/audit_log.py`, `mag/auth_switchboard.py`, `mag/auto_handoff.py`, `mag/auto_quantize.py`, `mag/autodrain.py`, `mag/autoglm.py`, `mag/autonomous_research.py`, `mag/autorun_status.py`, `mag/backlog_reform.py`, `mag/basecamp.py`, `mag/bash_local.py`, `mag/batch_drain.py`, `mag/batch_scribe.py`, `mag/bay_organs.py`, `mag/bay_organs_liveness_test.py`, `mag/behavior_catch.py`, `mag/behavioral_analytics.py`, `mag/behavioral_lensing.py`, `mag/bernaise.py`, `mag/billing_feed.py`, `mag/blast.py`, `mag/board_directive.py`, `mag/board_tailer.py`, `mag/bones_read.py`, `mag/boot.py`, `mag/boot_check.py`, `mag/breakthrough_loop.py`, `mag/brief_local.py`, `mag/btw_sidechannel.py`, `mag/budget_refactor.py`, `mag/burn_gate.py`, `mag/burn_steer.py`, `mag/bus_cadence.py`, `mag/cache_router.py`, `mag/cache_shard.py`, `mag/cache_watch.py`, `mag/cage_intake.py`, `mag/campaign_reader.py`, `mag/campaign_runs.py`, `mag/campaign_simulator.py`, `mag/canon_gate.py`, `mag/canon_seal.py`, `mag/capture_guard.py`, `mag/cascade_research.py`, `mag/cast_guard.py`, `mag/cast_launch.py`, `mag/castle_foundation.py`, `mag/catalog.py`, `mag/catalog_rebuild.py`, `mag/cdp_runner.py`, `mag/chain_query.py`, `mag/chain_substrate.py`, `mag/chatgpt_desktop.py`, `mag/cheap_swarm.py`, `mag/checkin_route.py`, `mag/chord.py`, `mag/chord_circuit.py`, `mag/chord_lens.py`, `mag/chord_pipeline.py`, `mag/chord_triangulate.py`, `mag/cite_gate.py`, `mag/cites_at_birth.py`, `mag/claim_repair.py`, `mag/claims_desk.py`, `mag/claims_verify.py`, `mag/claritas.py`, `mag/clawbot.py`, `mag/cleanup_steal.py`, `mag/cli/__init__.py`, `mag/cli/core.py`, `mag/cli/display.py`, `mag/clippy.py`, `mag/code_map.py`, `mag/codex_seat.py`, `mag/compiler_flywheel.py`, `mag/compiler_lang.py`, `mag/concurrency_gate.py`, `mag/connectivity_sizer.py`, `mag/console_render.py`, `mag/constants.py`, `mag/constitutional_critique.py`, `mag/context_growth.py`, `mag/cooker.py`, `mag/copilot_bridge.py`, `mag/corpus_expand.py`, `mag/corpus_ingest.py`, `mag/corpus_query.py`, `mag/corpus_selfsteal.py`, `mag/corpus_wave.py`, `mag/cost_governor.py`, `mag/cost_learn.py`, `mag/cross_version.py`, `mag/data_refinery.py`, `mag/data_source_watch.py`, `mag/decision_hook.py`, `mag/decl_attention.py`, `mag/depin.py`, `mag/desk_local_simulator.py`, `mag/desk_ops.py`, `mag/desk_teaching.py`, `mag/desk_tools.py`, `mag/destructive_receipt.py`, `mag/deterministic_scanner.py`, `mag/df_tileset.py`, `mag/diamond_mine.py`, `mag/diary_node.py`, `mag/disposition_sweep.py`, `mag/dissector.py`, `mag/divergence_meter.py`, `mag/doctor_agent.py`, `mag/doctor_rightsize.py`, `mag/doctrine_statute.py`, `mag/drainer_stats.py`, `mag/dropbox_watcher.py`, `mag/dspy_sovereign.py`, `mag/dungeon_dev.py`, `mag/echo_net.py`, `mag/ecosystem_surface.py`, `mag/egregore_steal.py`, `mag/electron_seat.py`, `mag/emergence.py`, `mag/emergence_test.py`, `mag/emergent_harvest.py`, `mag/end_state.py`, `mag/engram.py`, `mag/epistemic_guard.py`, `mag/error_healer.py`, `mag/events_key_schema.py`, `mag/events_scan.py`, `mag/evolving_wave.py`, `mag/exit_dialogue.py`, `mag/extension_deploy.py`, `mag/fact_bus.py`, `mag/falsifier_counter.py`, `mag/fanout.py`, `mag/feedback.py`, `mag/fermat_ractor.py`, `mag/field_steal.py`, `mag/final_steal.py`, `mag/fire_horse.py`, `mag/fireball_cycle.py`, `mag/fish_ear.py`, `mag/fleet_intel.py`, `mag/flex_test.py`, `mag/flight_recorder.py`, `mag/flock_anim.py`, `mag/flock_field.py`, `mag/flock_grid.py`, `mag/flock_job.py`, `mag/flock_scheduler.py`, `mag/flock_shader.py`, `mag/flock_steal.py`, `mag/flock_usage_guard.py`, `mag/forge_daemon.py`, `mag/framework_map.py`, `mag/free_frontend_swarm.py`, `mag/free_to_swarm.py`, `mag/frontier_batch.py`, `mag/frontier_gravity.py`, `mag/frontier_help.py`, `mag/frontier_intake.py`, `mag/frontier_rib.py`, `mag/frontier_salon_cli.py`, `mag/frontier_scout.py`, `mag/frontier_steer.py`, `mag/future_self.py`, `mag/ga4_progression.py`, `mag/gab_seat.py`, `mag/game_battle_cycle.py`, `mag/game_brawl.py`, `mag/game_brawl_perspectives.py`, `mag/game_curveball.py`, `mag/game_dice.py`, `mag/game_dm_llm.py`, `mag/game_dm_voice.py`, `mag/game_flow.py`, `mag/game_freeze.py`, `mag/game_mud.py`, `mag/game_narrate.py`, `mag/game_observer.py`, `mag/game_passage.py`, `mag/game_produce.py`, `mag/game_saga.py`, `mag/game_salon.py`, `mag/game_score.py`, `mag/game_view.py`, `mag/game_world_map.py`, `mag/gap_analysis.py`, `mag/gap_frontier.py`, `mag/gap_map.py`, `mag/gap_resolver.py`, `mag/gap_routed_handoff.py`, `mag/gap_swarm_experiment.py`, `mag/gene_pool_feeder.py`, `mag/gguf_cartography.py`, `mag/ghost_auto.py`, `mag/ghost_cold_boot.py`, `mag/ghost_cross.py`, `mag/ghost_director.py`, `mag/ghost_doctor.py`, `mag/ghost_experimenter.py`, `mag/ghost_grok_dashboard.py`, `mag/ghost_identity.py`, `mag/ghost_leak_detector.py`, `mag/ghost_ledger.py`, `mag/ghost_nudge.py`, `mag/ghost_pylance.py`, `mag/ghost_server.py`, `mag/ghost_whisper.py`, `mag/git_divergence.py`, `mag/glm_flash.py`, `mag/gopher_lite.py`, `mag/governance.py`, `mag/gpu_ghost.py`, `mag/gpu_k8s.py`, `mag/gpu_lifecycle.py`, `mag/gpu_memweave.py`, `mag/grammar_transfer.py`, `mag/grok_bot.py`, `mag/grok_brief.py`, `mag/grok_desktop.py`, `mag/grok_free.py`, `mag/grok_frontier_loop.py`, `mag/grok_gate.py`, `mag/grok_hub.py`, `mag/grok_mirror.py`, `mag/grok_rightsize.py`, `mag/grok_route.py`, `mag/grok_seat_burner.py`, `mag/grok_steer.py`, `mag/grok_tandem.py`, `mag/grok_terminal.py`, `mag/grok_warm_rib.py`, `mag/grok_weave.py`, `mag/grokbot_cold_edges.py`, `mag/guard.py`, `mag/guard_registry.py`, `mag/guardrail_sentinel.py`, `mag/hall_shared_supper.py`, `mag/harness.py`, `mag/hermes_steering.py`, `mag/hermes_warm_boot.py`, `mag/hero_simulation.py`, `mag/hf_space.py`, `mag/host_resolver.py`, `mag/host_roundtrip.py`, `mag/hour_test.py`, `mag/idea_flow.py`, `mag/ingest_registry.py`, `mag/integrity_kernel.py`, `mag/intent_rightsize.py`, `mag/interrupt_pipeline.py`, `mag/invariant_lattice.py`, `mag/invariant_ledger.py`, `mag/invariant_npcs.py`, `mag/invariant_surface.py`, `mag/janitor.py`, `mag/jones_lens.py`, `mag/judge.py`, `mag/k8s_bridge.py`, `mag/kabuki_salon.py`, `mag/key_law.py`, `mag/knot_at_close.py`, `mag/knot_math.py`, `mag/knot_untangle.py`, `mag/knowledge_graph.py`, `mag/kvos_block.py`, `mag/ladder.py`, `mag/lane_breaker.py`, `mag/lane_probe.py`, `mag/lane_supervisor.py`, `mag/lanes.py`, `mag/lattice_dashboard.py`, `mag/lattice_logic.py`, `mag/leaked_prompt_mine.py`, `mag/learn_rightsize.py`, `mag/lens_chain.py`, `mag/lens_library.py`, `mag/lens_shader.py`, `mag/lens_tournament.py`, `mag/librarian.py`, `mag/librarian_catalog.py`, `mag/line_builder.py`, `mag/links_split_gate.py`, `mag/lite_guard.py`, `mag/lite_scale.py`, `mag/live_feed.py`, `mag/live_report.py`, `mag/liveness_sense.py`, `mag/local_mode.py`, `mag/local_playbook.py`, `mag/local_usable.py`, `mag/loop_doctor.py`, `mag/loop_feedback.py`, `mag/loop_health.py`, `mag/lora_pipeline.py`, `mag/machine_target.py`, `mag/main_channel.py`, `mag/manifest.py`, `mag/matrix_router.py`, `mag/max_distill_arms.py`, `mag/maze_real.py`, `mag/mcp_http.py`, `mag/mem_invariant_map.py`, `mag/mem_lands.py`, `mag/mem_ollama.py`, `mag/mem_weave_distributor.py`, `mag/memory_consolidate.py`, `mag/memory_train_seed.py`, `mag/memweave.py`, `mag/meta_lattice.py`, `mag/meta_percolate.py`, `mag/mind_mine.py`, `mag/mind_window.py`, `mag/mindweave_eval.py`, `mag/mine_diamonds.py`, `mag/mirror_control.py`, `mag/mixture_of_agents.py`, `mag/model_health.py`, `mag/model_pick.py`, `mag/modules.py`, `mag/mrna_steal.py`, `mag/museum.py`, `mag/narrative_engine.py`, `mag/narrative_tests.py`, `mag/north_star.py`, `mag/notion_api.py`, `mag/novelty_lens.py`, `mag/ocean_model_mind.py`, `mag/ocean_persona.py`, `mag/offerings.py`, `mag/offline.py`, `mag/oh_fuck.py`, `mag/one_sizer.py`, `mag/ontology_compiler/extract.py`, `mag/operator_os.py`, `mag/ops_graph.py`, `mag/orphan_audit.py`, `mag/orphan_sense.py`, `mag/orphan_timer.py`, `mag/os_v2.py`, `mag/overseer.py`, `mag/ox_alpha_steal.py`, `mag/ox_availability.py`, `mag/ox_burn.py`, `mag/ox_escalate.py`, `mag/ox_fold.py`, `mag/ox_gap.py`, `mag/ox_megaburn.py`, `mag/ox_megaburn2.py`, `mag/ox_megaburn3.py`, `mag/ox_novelty_digest.py`, `mag/ox_novelty_index.py`, `mag/ox_percolate.py`, `mag/ox_probe.py`, `mag/ox_resident.py`, `mag/ox_scout.py`, `mag/ox_seat.py`, `mag/ox_swarm.py`, `mag/p20_pending_wave.py`, `mag/partner_puppet.py`, `mag/pattern_mine.py`, `mag/pdf_layout.py`, `mag/percolator_heal_test.py`, `mag/persistent_agent.py`, `mag/persona_direction.py`, `mag/persona_key.py`, `mag/persona_recall.py`, `mag/personality_substrate.py`, `mag/perturbation_battery.py`, `mag/phone_door.py`, `mag/phone_relay.py`, `mag/pin_audit.py`, `mag/plan.py`, `mag/plan_mode.py`, `mag/play_benchmark.py`, `mag/poc_stage2.py`, `mag/policy.py`, `mag/popup_insights.py`, `mag/portal.py`, `mag/prefix_prover.py`, `mag/preflight.py`, `mag/preload_selector.py`, `mag/press_digest.py`, `mag/primer.py`, `mag/probe_route.py`, `mag/problem_knot.py`, `mag/process_reaper.py`, `mag/prompt_archaeology.py`, `mag/proof.py`, `mag/prose_census.py`, `mag/prospect_sim.py`, `mag/provenance_gate.py`, `mag/queue_analysis.py`, `mag/queue_learn.py`, `mag/queue_ops.py`, `mag/queue_rightsize.py`, `mag/race_harness.py`, `mag/ractor_corpus.py`, `mag/ractor_vessels.py`, `mag/rails.py`, `mag/ram_cache.py`, `mag/read_archive.py`, `mag/read_receipts.py`, `mag/readout_controller.py`, `mag/real_swarm.py`, `mag/reasoning_intake.py`, `mag/records.py`, `mag/recreation_rib.py`, `mag/recurrence_gate.py`, `mag/refeed_guard.py`, `mag/refine_chain.py`, `mag/refine_loop.py`, `mag/rel_mem_eval.py`, `mag/render_brief.py`, `mag/renderman.py`, `mag/renderman_ask.py`, `mag/republic.py`, `mag/republic_feed.py`, `mag/republic_governance.py`, `mag/republic_loop.py`, `mag/research_class.py`, `mag/research_director.py`, `mag/research_lens.py`, `mag/research_worker.py`, `mag/resource_governor.py`, `mag/resume_order.py`, `mag/rib_action.py`, `mag/rib_cache.py`, `mag/rib_gif.py`, `mag/rib_k8s.py`, `mag/rib_os.py`, `mag/rib_renderer.py`, `mag/rib_store.py`, `mag/rib_struct.py`, `mag/riddle_direction.py`, `mag/riddler_campaign.py`, `mag/riddler_coherence.py`, `mag/riddler_sanitize.py`, `mag/riddler_tap.py`, `mag/riddler_trajectory.py`, `mag/riddler_transport.py`, `mag/right_size_skills.py`, `mag/rightsize_all.py`, `mag/rightsize_api.py`, `mag/rightsize_wave.py`, `mag/room_state.py`, `mag/roshomon.py`, `mag/saelis_room.py`, `mag/saelis_seat.py`, `mag/saelis_world_brief.py`, `mag/salon_50.py`, `mag/salon_openclaw.py`, `mag/schema_registry.py`, `mag/scifi_fantasy_steal.py`, `mag/scribe.py`, `mag/scrum.py`, `mag/seal.py`, `mag/seat_availability.py`, `mag/seat_dispatch.py`, `mag/seat_fork.py`, `mag/seat_guard.py`, `mag/seat_hunter.py`, `mag/seat_probe.py`, `mag/seed_chain.py`, `mag/seed_percolator.py`, `mag/seed_registry.py`, `mag/seeds.py`, `mag/self_advance.py`, `mag/self_audit.py`, `mag/self_drive.py`, `mag/self_drive_cadence.py`, `mag/self_hologram.py`, `mag/self_loop.py`, `mag/self_test.py`, `mag/self_train_data.py`, `mag/self_vision.py`, `mag/sentinel.py`, `mag/session_bridge.py`, `mag/session_card.py`, `mag/session_dossier.py`, `mag/session_koan.py`, `mag/session_maze.py`, `mag/session_overseer.py`, `mag/session_rib.py`, `mag/session_ritual.py`, `mag/shader_bus.py`, `mag/shader_rib.py`, `mag/shadow_graph.py`, `mag/shadow_quest.py`, `mag/shadow_slab.py`, `mag/shadow_work.py`, `mag/shape_map.py`, `mag/shelf_pdf.py`, `mag/signal_flare.py`, `mag/signals.py`, `mag/single_feed.py`, `mag/skills_pack.py`, `mag/socratic.py`, `mag/socratic_tree.py`, `mag/space_ear.py`, `mag/spawn_manifest.py`, `mag/spine_exercise.py`, `mag/stale_sweep.py`, `mag/standing.py`, `mag/standing_wave.py`, `mag/state_brief.py`, `mag/state_quantizer.py`, `mag/stateless_research.py`, `mag/steal_first.py`, `mag/steal_lens.py`, `mag/steal_pack.py`, `mag/steal_protocol_probe.py`, `mag/steal_steer.py`, `mag/steal_tools.py`, `mag/steer_bus.py`, `mag/steer_engine.py`, `mag/steer_receipt_wire.py`, `mag/steer_router.py`, `mag/steer_swarm.py`, `mag/steer_telemetry.py`, `mag/steiniger_lens.py`, `mag/subswarm_health.py`, `mag/suno_zeitgeist.py`, `mag/supervisor.py`, `mag/surface_render.py`, `mag/surrogate.py`, `mag/swarm_capacity.py`, `mag/swarm_control.py`, `mag/swarm_cycle.py`, `mag/swarm_economics.py`, `mag/swarm_emerge.py`, `mag/swarm_grok_watch.py`, `mag/swarm_health.py`, `mag/swarm_map.py`, `mag/swarm_quests.py`, `mag/swarm_render.py`, `mag/swarm_rightsize.py`, `mag/swarm_run.py`, `mag/swarm_self.py`, `mag/swarm_snapshot.py`, `mag/swarm_test.py`, `mag/swarm_tools.py`, `mag/system_map.py`, `mag/system_telemetry.py`, `mag/table_turn_cli.py`, `mag/table_view_cache.py`, `mag/tandem_key_test.py`, `mag/tangent.py`, `mag/task_router.py`, `mag/tavern_chat.py`, `mag/tavern_summon_guests.py`, `mag/team_knot.py`, `mag/telegram_desk.py`, `mag/template_invariant.py`, `mag/territory_solver.py`, `mag/test_dummy.py`, `mag/test_runner.py`, `mag/tests/test_identity_schema_portability.py`, `mag/tests/verify_identity_coupling.py`, `mag/tesuji_fire.py`, `mag/tesuji_map.py`, `mag/tesuji_probes.py`, `mag/tesuji_surface.py`, `mag/the_margin.py`, `mag/thought_bank.py`, `mag/thought_bank_app.py`, `mag/thread_eye.py`, `mag/throughput_model.py`, `mag/time_estimate.py`, `mag/tokenomics.py`, `mag/tool_5ws.py`, `mag/tool_lifecycle.py`, `mag/tool_manifest.py`, `mag/tool_retire.py`, `mag/tool_synthesis.py`, `mag/top_processes.py`, `mag/topic_index.py`, `mag/topic_index_v3_tf_draft.py`, `mag/topic_orphan.py`, `mag/tortoise_demo.py`, `mag/training_packager.py`, `mag/training_rightsize.py`, `mag/training_set.py`, `mag/trajectory_paths.py`, `mag/trajectory_step.py`, `mag/transfer_gate.py`, `mag/trigger_learn.py`, `mag/tripartite.py`, `mag/trust_gate.py`, `mag/trust_gate_audit_check.py`, `mag/truth_audit.py`, `mag/tts.py`, `mag/usage_digest.py`, `mag/usage_forecast.py`, `mag/usage_monitor.py`, `mag/vast_launcher.py`, `mag/verified_clock.py`, `mag/verify_gate.py`, `mag/verify_succession_contract.py`, `mag/verkle_lance.py`, `mag/verkle_render.py`, `mag/verkle_rib.py`, `mag/vertical_meter.py`, `mag/vision.py`, `mag/visual_pack.py`, `mag/voice_lanes.py`, `mag/voice_self.py`, `mag/voice_skills.py`, `mag/voice_stt.py`, `mag/voice_tasks.py`, `mag/voice_trigger.py`, `mag/volume_fidelity.py`, `mag/vram_memory.py`, `mag/vscode_feed.py`, `mag/vscode_seat.py`, `mag/warmed_cold_replay.py`, `mag/wave.py`, `mag/wave_address.py`, `mag/wave_cache.py`, `mag/wave_fire.py`, `mag/wearable_swarm.py`, `mag/whale_patrol.py`, `mag/whisper_route.py`, `mag/win_powershell.py`, `mag/window_audit.py`, `mag/window_bus.py`, `mag/window_hop.py`, `mag/window_throttle.py`, `mag/witness_snapshot.py`, `mag/word_skill_map.py`, `mag/work_contract.py`, `mag/work_register.py`, `mag/work_tiers.py`, `mag/worldline_dungeon.py`, `mag/worldline_seed.py`, `mag/wow_steal.py`, `mag/x_auth_once.py`, `mag/x_chat_mine.py`, `mag/x_control_surface.py`, `mag/x_interceptor.py`, `mag/x_oauth.py`, `mag/x_posts_mine.py`, `mag/x_reply_radar.py`, `mag/x_surface.py`

### Orphans: zero test refs AND zero readers (216)

`mag/_bench_free_shelf.py`, `mag/_cache_ab_probe.py`, `mag/_codex_seat.py`, `mag/_comb_tokens.py`, `mag/_compare_chain_sources.py`, `mag/_conc_test_slot.py`, `mag/_deep_research_verkle_dedupe.py`, `mag/_demo_eyes_receipt.py`, `mag/_demo_telepathy.py`, `mag/_diag_cache.py`, `mag/_exp_a_cache_retrigger.py`, `mag/_flag_dangling_264d0ba3.py`, `mag/_gpu_probe_debug.py`, `mag/_grok_corpus_burn.py`, `mag/_openclaw_real.py`, `mag/_probe_dangling.py`, `mag/_probe_mcp.py`, `mag/_probe_zai_balance.py`, `mag/_relane_game_tasks.py`, `mag/_salon_burn.py`, `mag/_verify_chain_now.py`, `mag/_verify_concurrency_gate.py`, `mag/_verify_queue_gate.py`, `mag/_verify_repair_state.py`, `mag/_verify_rung5.py`, `mag/_verify_sharp_edge.py`, `mag/_verify_verkle_gate_spec.py`, `mag/_warm_rib.py`, `mag/abliterator_spawn_manifest.py`, `mag/accumulator.py`, `mag/adventure_one_shot.py`, `mag/agent_signature.py`, `mag/arena_bench.py`, `mag/auto_handoff.py`, `mag/auto_quantize.py`, `mag/autodrain.py`, `mag/autoglm.py`, `mag/bay_organs_liveness_test.py`, `mag/boot_check.py`, `mag/breakthrough_loop.py`, `mag/burn_gate.py`, `mag/burn_steer.py`, `mag/cage_intake.py`, `mag/campaign_reader.py`, `mag/campaign_simulator.py`, `mag/canon_gate.py`, `mag/canon_seal.py`, `mag/catalog_rebuild.py`, `mag/chatgpt_desktop.py`, `mag/chord.py`, `mag/cites_at_birth.py`, `mag/claim_repair.py`, `mag/claims_verify.py`, `mag/cleanup_steal.py`, `mag/cli/display.py`, `mag/compiler_flywheel.py`, `mag/connectivity_sizer.py`, `mag/corpus_selfsteal.py`, `mag/decision_hook.py`, `mag/decl_attention.py`, `mag/disposition_sweep.py`, `mag/dissector.py`, `mag/divergence_meter.py`, `mag/doctrine_statute.py`, `mag/echo_net.py`, `mag/emergence_test.py`, `mag/end_state.py`, `mag/engram.py`, `mag/epistemic_guard.py`, `mag/falsifier_counter.py`, `mag/fermat_ractor.py`, `mag/final_steal.py`, `mag/fire_horse.py`, `mag/fleet_intel.py`, `mag/forge_daemon.py`, `mag/free_to_swarm.py`, `mag/frontier_intake.py`, `mag/ga4_progression.py`, `mag/gab_seat.py`, `mag/game_produce.py`, `mag/gap_resolver.py`, `mag/gap_swarm_experiment.py`, `mag/gene_pool_feeder.py`, `mag/gguf_cartography.py`, `mag/ghost_auto.py`, `mag/ghost_director.py`, `mag/ghost_doctor.py`, `mag/ghost_server.py`, `mag/git_divergence.py`, `mag/gopher_lite.py`, `mag/gpu_memweave.py`, `mag/grammar_transfer.py`, `mag/grok_desktop.py`, `mag/hermes_warm_boot.py`, `mag/hero_simulation.py`, `mag/hf_space.py`, `mag/host_roundtrip.py`, `mag/hour_test.py`, `mag/interrupt_pipeline.py`, `mag/invariant_npcs.py`, `mag/knot_at_close.py`, `mag/ladder.py`, `mag/lane_probe.py`, `mag/lattice_logic.py`, `mag/lite_scale.py`, `mag/matrix_router.py`, `mag/max_distill_arms.py`, `mag/maze_real.py`, `mag/memory_consolidate.py`, `mag/memory_train_seed.py`, `mag/mind_mine.py`, `mag/mindweave_eval.py`, `mag/mirror_control.py`, `mag/mrna_steal.py`, `mag/museum.py`, `mag/narrative_tests.py`, `mag/north_star.py`, `mag/offline.py`, `mag/ontology_compiler/extract.py`, `mag/orphan_audit.py`, `mag/ox_alpha_steal.py`, `mag/ox_burn.py`, `mag/ox_escalate.py`, `mag/ox_megaburn.py`, `mag/ox_megaburn2.py`, `mag/ox_novelty_digest.py`, `mag/ox_probe.py`, `mag/ox_swarm.py`, `mag/p20_pending_wave.py`, `mag/pattern_mine.py`, `mag/percolator_heal_test.py`, `mag/persistent_agent.py`, `mag/persona_direction.py`, `mag/persona_key.py`, `mag/perturbation_battery.py`, `mag/pin_audit.py`, `mag/plan_mode.py`, `mag/poc_stage2.py`, `mag/portal.py`, `mag/provenance_gate.py`, `mag/race_harness.py`, `mag/ractor_corpus.py`, `mag/read_receipts.py`, `mag/readout_controller.py`, `mag/reasoning_intake.py`, `mag/recreation_rib.py`, `mag/refeed_guard.py`, `mag/refine_loop.py`, `mag/rib_gif.py`, `mag/rib_k8s.py`, `mag/rib_renderer.py`, `mag/rib_store.py`, `mag/riddle_direction.py`, `mag/riddler_coherence.py`, `mag/riddler_tap.py`, `mag/riddler_trajectory.py`, `mag/rightsize_wave.py`, `mag/saelis_room.py`, `mag/saelis_world_brief.py`, `mag/salon_50.py`, `mag/scifi_fantasy_steal.py`, `mag/seat_probe.py`, `mag/seed_percolator.py`, `mag/seed_registry.py`, `mag/self_hologram.py`, `mag/session_koan.py`, `mag/session_ritual.py`, `mag/shadow_quest.py`, `mag/shadow_slab.py`, `mag/shelf_pdf.py`, `mag/socratic_tree.py`, `mag/space_ear.py`, `mag/spawn_manifest.py`, `mag/stale_sweep.py`, `mag/standing.py`, `mag/steal_lens.py`, `mag/steer_bus.py`, `mag/steer_receipt_wire.py`, `mag/swarm_quests.py`, `mag/swarm_run.py`, `mag/swarm_snapshot.py`, `mag/tandem_key_test.py`, `mag/tavern_summon_guests.py`, `mag/telegram_desk.py`, `mag/template_invariant.py`, `mag/tests/test_identity_schema_portability.py`, `mag/tests/verify_identity_coupling.py`, `mag/tesuji_fire.py`, `mag/thought_bank_app.py`, `mag/thread_eye.py`, `mag/tool_lifecycle.py`, `mag/tortoise_demo.py`, `mag/training_rightsize.py`, `mag/trajectory_paths.py`, `mag/trajectory_step.py`, `mag/transfer_gate.py`, `mag/trust_gate_audit_check.py`, `mag/verify_gate.py`, `mag/verkle_rib.py`, `mag/vertical_meter.py`, `mag/volume_fidelity.py`, `mag/vscode_seat.py`, `mag/warmed_cold_replay.py`, `mag/whale_patrol.py`, `mag/whisper_route.py`, `mag/window_hop.py`, `mag/window_throttle.py`, `mag/witness_snapshot.py`, `mag/work_tiers.py`, `mag/worldline_dungeon.py`, `mag/x_auth_once.py`, `mag/x_chat_mine.py`, `mag/x_interceptor.py`, `mag/x_posts_mine.py`, `mag/x_reply_radar.py`, `mag/x_surface.py`

## Per-module census table (all 1034 modules)

module | lines | pub fns | pub classes | test files | readers | last commit | mtime
---|---|---|---|---|---|---|---
mag/__init__.py | 17 | 0 | 0 | 308 | 1340 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/_bench_free_shelf.py | 59 | 1 | 0 | 0 | 0 | 47d3907e3 2026-08-25 | 2026-09-16 18:12
mag/_cache_ab_probe.py | 64 | 2 | 0 | 0 | 0 | cb26bc2cd 2026-08-25 | 2026-09-16 18:12
mag/_codex_seat.py | 84 | 1 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-08-27 07:45
mag/_comb_tokens.py | 84 | 0 | 0 | 0 | 0 | 799ddb6fe 2026-08-19 | 2026-09-16 18:12
mag/_compare_chain_sources.py | 31 | 1 | 0 | 0 | 0 | b7a47f194 2026-08-25 | 2026-09-16 18:12
mag/_conc_test_slot.py | 77 | 1 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-05 19:06
mag/_consensus_witness.py | 108 | 3 | 0 | 1 | 0 | 383fed94f 2026-09-27 | 2026-09-26 19:35
mag/_deep_research_verkle_dedupe.py | 63 | 1 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-09-16 18:12
mag/_demo_eyes_receipt.py | 116 | 4 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-08-27 04:16
mag/_demo_telepathy.py | 173 | 4 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-08-26 16:00
mag/_diag_cache.py | 11 | 0 | 0 | 0 | 0 | a4131cb46 2026-08-25 | 2026-09-16 18:12
mag/_exp_a_cache_retrigger.py | 68 | 2 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-08-28 20:51
mag/_flag_dangling_20260925.py | 106 | 0 | 0 | 0 | 1 | 383fed94f 2026-09-27 | 2026-09-26 16:36
mag/_flag_dangling_264d0ba3.py | 97 | 0 | 0 | 0 | 0 | 383fed94f 2026-09-27 | 2026-09-26 16:36
mag/_gpu_probe_debug.py | 39 | 0 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-09-16 18:12
mag/_grok_corpus_burn.py | 103 | 4 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-16 18:12
mag/_openclaw_real.py | 19 | 2 | 0 | 0 | 0 | cb26bc2cd 2026-08-25 | 2026-09-16 18:12
mag/_probe_burst_20260903.py | 99 | 3 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-03 19:27
mag/_probe_dangling.py | 29 | 0 | 0 | 0 | 0 | b7a47f194 2026-08-25 | 2026-09-16 18:12
mag/_probe_mcp.py | 36 | 0 | 0 | 0 | 0 | 1d607e078 2026-08-25 | 2026-09-16 18:12
mag/_probe_zai_balance.py | 51 | 0 | 0 | 0 | 0 | cb26bc2cd 2026-08-25 | 2026-09-16 18:12
mag/_relane_game_tasks.py | 44 | 0 | 0 | 0 | 0 | cb26bc2cd 2026-08-25 | 2026-09-16 18:12
mag/_salon_burn.py | 96 | 5 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-16 18:12
mag/_verify_chain_now.py | 32 | 0 | 0 | 0 | 0 | b7a47f194 2026-08-25 | 2026-08-25 13:39
mag/_verify_concurrency_gate.py | 49 | 0 | 0 | 0 | 0 | cb26bc2cd 2026-08-25 | 2026-09-16 18:12
mag/_verify_queue_gate.py | 80 | 0 | 0 | 0 | 0 | cb26bc2cd 2026-08-25 | 2026-09-16 18:12
mag/_verify_repair_state.py | 16 | 0 | 0 | 0 | 0 | b7a47f194 2026-08-25 | 2026-09-16 18:12
mag/_verify_rung5.py | 50 | 0 | 0 | 0 | 0 | cb26bc2cd 2026-08-25 | 2026-09-16 18:12
mag/_verify_sharp_edge.py | 59 | 0 | 0 | 0 | 0 | cb26bc2cd 2026-08-25 | 2026-09-16 18:12
mag/_verify_verkle_gate_spec.py | 104 | 1 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-07 09:25
mag/_warm_rib.py | 18 | 0 | 0 | 0 | 0 | a4131cb46 2026-08-25 | 2026-09-16 18:12
mag/abliterator_spawn_manifest.py | 128 | 4 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-12 22:30
mag/abundance_rogue.py | 218 | 7 | 0 | 1 | 1 | 052732ebf 2026-08-14 | 2026-08-12 16:58
mag/accumulator.py | 280 | 1 | 3 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-04 18:34
mag/act.py | 248 | 1 | 0 | 1 | 3 | d90bc8607 2026-09-28 | 2026-09-28 14:51
mag/adventure_moonshot.py | 245 | 4 | 0 | 1 | 1 | 052732ebf 2026-08-14 | 2026-08-13 14:59
mag/adventure_one_shot.py | 202 | 6 | 0 | 0 | 0 | 799ddb6fe 2026-08-19 | 2026-08-18 11:04
mag/afk_cadence.py | 284 | 3 | 0 | 1 | 5 | 790145ab1 2026-09-26 | 2026-09-26 01:30
mag/afk_loop.py | 341 | 8 | 0 | 2 | 8 | d90bc8607 2026-09-28 | 2026-09-28 14:50
mag/afk_orchestrator.py | 189 | 2 | 0 | 1 | 0 | 790145ab1 2026-09-26 | 2026-09-26 01:30
mag/agent_arena.py | 503 | 5 | 0 | 4 | 5 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/agent_behavior.py | 145 | 4 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-10 14:34
mag/agent_cli.py | 3139 | 31 | 0 | 14 | 21 | d90bc8607 2026-09-28 | 2026-09-28 14:51
mag/agent_corpus.py | 270 | 6 | 0 | 2 | 3 | d575bc168 2026-09-14 | 2026-08-30 13:27
mag/agent_desk.py | 257 | 11 | 0 | 6 | 13 | d575bc168 2026-09-14 | 2026-08-30 13:59
mag/agent_knot.py | 334 | 6 | 0 | 2 | 14 | 052732ebf 2026-08-14 | 2026-08-12 08:05
mag/agent_os_loop.py | 108 | 3 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-11 08:00
mag/agent_signature.py | 220 | 5 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-10 20:14
mag/agent_state.py | 466 | 10 | 0 | 3 | 13 | d575bc168 2026-09-14 | 2026-09-01 21:00
mag/agent_state_router.py | 129 | 4 | 0 | 0 | 4 | de7bb85fe 2026-08-09 | 2026-08-09 01:13
mag/agentic_test_steal.py | 154 | 5 | 0 | 0 | 2 | 052732ebf 2026-08-14 | 2026-08-11 10:17
mag/ai_landscape.py | 329 | 5 | 0 | 0 | 3 | 052732ebf 2026-08-14 | 2026-08-10 12:03
mag/amd_window_guard.py | 84 | 2 | 0 | 0 | 2 | 052732ebf 2026-08-14 | 2026-08-10 07:10
mag/aos_agent.py | 314 | 3 | 0 | 0 | 3 | cb26bc2cd 2026-08-25 | 2026-08-23 14:51
mag/aos_bus_watcher.py | 336 | 4 | 0 | 0 | 2 | cb26bc2cd 2026-08-25 | 2026-08-23 16:16
mag/aos_grok.py | 325 | 5 | 0 | 0 | 6 | de29d49ea 2026-08-09 | 2026-08-09 09:23
mag/aos_live_view.py | 360 | 5 | 0 | 0 | 34 | cb26bc2cd 2026-08-25 | 2026-08-23 11:22
mag/api_gateway.py | 767 | 4 | 0 | 2 | 3 | 790145ab1 2026-09-26 | 2026-09-26 00:49
mag/api_server.py | 123 | 3 | 0 | 1 | 3 | d575bc168 2026-09-14 | 2026-09-04 20:11
mag/arc_seed.py | 181 | 4 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-06 20:35
mag/archetype_image.py | 365 | 7 | 0 | 0 | 5 | 052732ebf 2026-08-14 | 2026-08-10 11:52
mag/arena_adapter.py | 284 | 3 | 1 | 1 | 3 | 1c156e2fa 2026-08-06 | 2026-08-08 19:56
mag/arena_bench.py | 597 | 16 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-05 00:59
mag/arena_learning.py | 456 | 8 | 0 | 2 | 6 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/arena_strategies.py | 142 | 7 | 0 | 0 | 3 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/arrival.py | 204 | 4 | 0 | 2 | 3 | 052732ebf 2026-08-14 | 2026-08-12 11:24
mag/art_forge.py | 169 | 1 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-04 20:58
mag/arxiv_harvest.py | 179 | 1 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-04 23:05
mag/arxiv_mine.py | 242 | 5 | 0 | 0 | 2 | 052732ebf 2026-08-14 | 2026-08-12 18:33
mag/ask.py | 393 | 2 | 0 | 0 | 5 | e96fd62a4 2026-08-07 | 2026-08-06 19:47
mag/ask_router.py | 277 | 10 | 0 | 1 | 6 | 383fed94f 2026-09-27 | 2026-09-26 19:36
mag/atlas.py | 78 | 3 | 0 | 0 | 4 | d575bc168 2026-09-14 | 2026-08-30 21:59
mag/attention_ranker.py | 254 | 2 | 0 | 1 | 3 | ef4dce855 2026-08-06 | 2026-08-06 18:28
mag/attractor_tools.py | 161 | 6 | 0 | 0 | 6 | 052732ebf 2026-08-14 | 2026-08-10 17:00
mag/audit_log.py | 20 | 1 | 0 | 0 | 1 | b1d714b02 2026-09-25 | 2026-09-25 08:28
mag/auth_switchboard.py | 292 | 13 | 0 | 0 | 2 | d575bc168 2026-09-14 | 2026-09-05 12:16
mag/auto_handoff.py | 136 | 3 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-10 16:12
mag/auto_quantize.py | 456 | 1 | 2 | 0 | 0 | de7bb85fe 2026-08-09 | 2026-08-08 20:30
mag/autodrain.py | 214 | 5 | 0 | 0 | 0 | 47d3907e3 2026-08-25 | 2026-08-25 20:54
mag/autoglm.py | 167 | 2 | 0 | 0 | 0 | 0f34a8f3e 2026-09-16 | 2026-09-16 14:44
mag/autonomous_research.py | 589 | 11 | 0 | 0 | 5 | cb26bc2cd 2026-08-25 | 2026-08-24 22:20
mag/autopilot.py | 113 | 1 | 0 | 1 | 4 | f3a1ff214 2026-08-05 | 2026-08-06 18:28
mag/autorun_common.py | 100 | 4 | 0 | 2 | 5 | d575bc168 2026-09-14 | 2026-09-02 04:10
mag/autorun_status.py | 219 | 2 | 0 | 0 | 2 | f3a1ff214 2026-08-05 | 2026-08-06 18:28
mag/backlog_reform.py | 143 | 3 | 0 | 0 | 3 | 052732ebf 2026-08-14 | 2026-08-09 23:10
mag/bard.py | 985 | 18 | 1 | 2 | 8 | 482e0a3c8 2026-08-08 | 2026-08-08 19:11
mag/bare_numpy.py | 148 | 11 | 1 | 1 | 0 | 052732ebf 2026-08-14 | 2026-08-12 10:30
mag/basecamp.py | 76 | 2 | 0 | 0 | 3 | d575bc168 2026-09-14 | 2026-08-31 00:26
mag/bash_local.py | 289 | 4 | 0 | 0 | 3 | d575bc168 2026-09-14 | 2026-09-07 10:05
mag/batch_drain.py | 230 | 4 | 0 | 0 | 3 | cb26bc2cd 2026-08-25 | 2026-08-24 17:05
mag/batch_scribe.py | 205 | 4 | 0 | 0 | 1 | cb26bc2cd 2026-08-25 | 2026-08-24 16:56
mag/bay_organs.py | 339 | 13 | 0 | 0 | 4 | d575bc168 2026-09-14 | 2026-09-04 10:31
mag/bay_organs_liveness_test.py | 374 | 7 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-12 21:22
mag/behavior_catch.py | 249 | 3 | 0 | 0 | 2 | e96fd62a4 2026-08-07 | 2026-08-06 22:46
mag/behavioral_analytics.py | 316 | 3 | 0 | 0 | 6 | 482e0a3c8 2026-08-08 | 2026-08-08 19:11
mag/behavioral_lensing.py | 486 | 1 | 2 | 0 | 1 | de7bb85fe 2026-08-09 | 2026-08-08 22:03
mag/behavioral_synth.py | 153 | 1 | 0 | 2 | 4 | e96fd62a4 2026-08-07 | 2026-08-06 22:46
mag/bernaise.py | 210 | 5 | 0 | 0 | 8 | de29d49ea 2026-08-09 | 2026-08-09 14:55
mag/billing_feed.py | 273 | 3 | 0 | 0 | 2 | 052732ebf 2026-08-14 | 2026-08-12 08:50
mag/biography.py | 598 | 5 | 0 | 1 | 9 | d575bc168 2026-09-14 | 2026-08-30 13:55
mag/blade_plan.py | 150 | 4 | 0 | 1 | 0 | d575bc168 2026-09-14 | 2026-08-29 04:27
mag/blast.py | 575 | 11 | 0 | 0 | 3 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/board_directive.py | 176 | 2 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-08-30 21:38
mag/board_tailer.py | 246 | 2 | 0 | 0 | 2 | d575bc168 2026-09-14 | 2026-08-31 00:49
mag/bonds.py | 485 | 4 | 0 | 1 | 9 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/bones_adapter.py | 390 | 8 | 3 | 1 | 0 | 0f34a8f3e 2026-09-16 | 2026-09-16 13:52
mag/bones_read.py | 141 | 2 | 0 | 0 | 1 | cb26bc2cd 2026-08-25 | 2026-08-23 10:15
mag/boot.py | 233 | 2 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-08-28 19:44
mag/boot_check.py | 183 | 2 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-05 21:34
mag/brain.py | 222 | 2 | 0 | 1 | 1 | d575bc168 2026-09-14 | 2026-08-30 13:51
mag/breakthrough_loop.py | 233 | 4 | 0 | 0 | 0 | de29d49ea 2026-08-09 | 2026-08-09 18:46
mag/brief_local.py | 226 | 3 | 0 | 0 | 4 | 383fed94f 2026-09-27 | 2026-09-26 14:00
mag/browser_driver.py | 248 | 5 | 0 | 2 | 18 | a5dd96176 2026-09-25 | 2026-09-22 20:19
mag/browser_env.py | 177 | 6 | 0 | 2 | 7 | e96fd62a4 2026-08-07 | 2026-08-06 18:49
mag/btw_sidechannel.py | 192 | 5 | 0 | 0 | 2 | 052732ebf 2026-08-14 | 2026-08-11 21:32
mag/budget_refactor.py | 164 | 4 | 0 | 0 | 5 | 052732ebf 2026-08-14 | 2026-08-11 11:00
mag/build_audit.py | 144 | 3 | 0 | 2 | 5 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/burn_gate.py | 80 | 4 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-07 11:03
mag/burn_steer.py | 260 | 1 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-10 08:08
mag/bus_cadence.py | 180 | 3 | 0 | 0 | 4 | 799ddb6fe 2026-08-19 | 2026-08-14 07:55
mag/cache_identity.py | 510 | 14 | 0 | 1 | 0 | d575bc168 2026-09-14 | 2026-09-07 09:39
mag/cache_map.py | 403 | 6 | 0 | 1 | 10 | a0f7a593a 2026-09-24 | 2026-09-24 19:11
mag/cache_router.py | 225 | 5 | 0 | 0 | 2 | a5dd96176 2026-09-25 | 2026-09-25 20:44
mag/cache_shard.py | 106 | 4 | 0 | 0 | 2 | 052732ebf 2026-08-14 | 2026-08-11 09:27
mag/cache_watch.py | 148 | 3 | 0 | 0 | 4 | d575bc168 2026-09-14 | 2026-08-27 11:34
mag/cadence_learn.py | 199 | 9 | 0 | 1 | 6 | cb26bc2cd 2026-08-25 | 2026-08-23 21:35
mag/cage_intake.py | 332 | 6 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-07 10:10
mag/campaign.py | 781 | 8 | 1 | 1 | 10 | d575bc168 2026-09-14 | 2026-09-04 11:13
mag/campaign_reader.py | 151 | 3 | 0 | 0 | 0 | de7bb85fe 2026-08-09 | 2026-08-08 23:49
mag/campaign_runs.py | 145 | 2 | 0 | 0 | 2 | 799ddb6fe 2026-08-19 | 2026-08-15 05:39
mag/campaign_simulator.py | 401 | 2 | 3 | 0 | 0 | de7bb85fe 2026-08-09 | 2026-08-09 00:13
mag/canon_gate.py | 142 | 4 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-04 21:10
mag/canon_seal.py | 96 | 3 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-05 21:52
mag/canvas_bridge.py | 460 | 4 | 0 | 1 | 2 | 2464edcba 2026-08-04 | 2026-08-04 18:48
mag/capability_steal.py | 249 | 5 | 0 | 1 | 3 | 790145ab1 2026-09-26 | 2026-09-26 01:43
mag/capture_guard.py | 137 | 3 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-11 22:54
mag/cascade_research.py | 246 | 6 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-10 17:55
mag/cast_guard.py | 141 | 4 | 0 | 0 | 4 | d575bc168 2026-09-14 | 2026-09-01 21:00
mag/cast_launch.py | 71 | 2 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-13 09:27
mag/cast_server.py | 359 | 2 | 1 | 1 | 8 | d575bc168 2026-09-14 | 2026-08-30 13:36
mag/castle_foundation.py | 166 | 5 | 0 | 0 | 2 | 052732ebf 2026-08-14 | 2026-08-11 11:54
mag/catalog.py | 193 | 8 | 0 | 0 | 1 | 3aafe78a0 2026-09-16 | 2026-09-16 07:19
mag/catalog_freshness.py | 93 | 3 | 0 | 1 | 2 | 383fed94f 2026-09-27 | 2026-09-26 15:24
mag/catalog_rebuild.py | 150 | 2 | 0 | 0 | 0 | 383fed94f 2026-09-27 | 2026-09-26 15:09
mag/catalog_rescan.py | 385 | 6 | 0 | 2 | 3 | 383fed94f 2026-09-27 | 2026-09-26 16:46
mag/catalog_scan.py | 332 | 5 | 0 | 2 | 5 | 383fed94f 2026-09-27 | 2026-09-26 12:15
mag/catalog_tags.py | 210 | 5 | 0 | 1 | 1 | 4b5a4ab37 2026-09-28 | 2026-09-28 12:43
mag/caveman_audit.py | 139 | 2 | 0 | 1 | 3 | d7a61db31 2026-08-05 | 2026-08-06 18:28
mag/cdp_runner.py | 98 | 5 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-13 21:00
mag/census_liveness.py | 73 | 2 | 0 | 1 | 1 | 383fed94f 2026-09-27 | 2026-09-26 16:31
mag/chain_guard.py | 212 | 3 | 0 | 2 | 4 | 383fed94f 2026-09-27 | 2026-09-26 16:37
mag/chain_query.py | 297 | 1 | 1 | 0 | 22 | 482e0a3c8 2026-08-08 | 2026-08-08 19:05
mag/chain_substrate.py | 195 | 8 | 0 | 0 | 4 | 052732ebf 2026-08-14 | 2026-08-11 10:17
mag/chan.py | 338 | 11 | 0 | 1 | 2 | d575bc168 2026-09-14 | 2026-08-30 12:48
mag/chat_source.py | 482 | 10 | 1 | 2 | 7 | eb07ad62e 2026-08-04 | 2026-08-04 18:48
mag/chatgpt_bot.py | 150 | 5 | 0 | 1 | 3 | 052732ebf 2026-08-14 | 2026-08-12 17:16
mag/chatgpt_desktop.py | 196 | 5 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-13 20:33
mag/cheap_swarm.py | 222 | 5 | 0 | 0 | 6 | cb26bc2cd 2026-08-25 | 2026-08-24 08:15
mag/checkin_route.py | 391 | 4 | 0 | 0 | 3 | d575bc168 2026-09-14 | 2026-08-28 19:47
mag/chord.py | 112 | 2 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-08-26 12:06
mag/chord_circuit.py | 243 | 5 | 0 | 0 | 1 | cb26bc2cd 2026-08-25 | 2026-08-24 11:08
mag/chord_lens.py | 354 | 5 | 0 | 0 | 1 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/chord_pipeline.py | 202 | 5 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-12 08:50
mag/chord_triangulate.py | 199 | 5 | 0 | 0 | 2 | d575bc168 2026-09-14 | 2026-09-06 14:19
mag/chronicle.py | 132 | 1 | 0 | 2 | 4 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/cite_gate.py | 453 | 9 | 0 | 0 | 2 | d575bc168 2026-09-14 | 2026-09-07 01:30
mag/cites_at_birth.py | 103 | 2 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-06 18:16
mag/claim_repair.py | 471 | 10 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-05 00:08
mag/claims_desk.py | 190 | 6 | 0 | 0 | 1 | cb26bc2cd 2026-08-25 | 2026-08-23 14:32
mag/claims_verify.py | 124 | 1 | 0 | 0 | 0 | cb26bc2cd 2026-08-25 | 2026-08-23 14:32
mag/claritas.py | 64 | 2 | 0 | 0 | 5 | 86628c678 2026-09-24 | 2026-09-24 19:30
mag/clawbot.py | 197 | 6 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-13 04:52
mag/cleanup.py | 148 | 4 | 0 | 1 | 5 | 052732ebf 2026-08-14 | 2026-08-13 08:16
mag/cleanup_steal.py | 120 | 3 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-11 11:13
mag/cli/__init__.py | 26 | 0 | 0 | 0 | 2 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/cli/core.py | 186 | 5 | 0 | 0 | 1 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/cli/display.py | 128 | 15 | 0 | 0 | 0 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/clippy.py | 233 | 5 | 0 | 0 | 2 | 60e18c524 2026-08-08 | 2026-08-07 18:50
mag/code_map.py | 218 | 5 | 0 | 0 | 2 | 052732ebf 2026-08-14 | 2026-08-09 21:53
mag/codex_seat.py | 151 | 2 | 0 | 0 | 1 | cb26bc2cd 2026-08-25 | 2026-08-24 15:46
mag/coding_session_loop.py | 556 | 7 | 0 | 6 | 8 | d575bc168 2026-09-14 | 2026-08-30 13:58
mag/coding_session_orchestrator.py | 395 | 6 | 0 | 3 | 9 | 7654afe52 2026-08-06 | 2026-08-06 18:28
mag/coding_session_runner.py | 402 | 2 | 0 | 1 | 4 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/comms_trail.py | 261 | 6 | 0 | 1 | 7 | d575bc168 2026-09-14 | 2026-08-30 22:46
mag/compass.py | 248 | 9 | 0 | 1 | 9 | 383fed94f 2026-09-27 | 2026-09-26 17:31
mag/compiler_flywheel.py | 178 | 3 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-11 13:13
mag/compiler_lang.py | 277 | 5 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-11 10:17
mag/compute_reconcile.py | 201 | 4 | 0 | 1 | 3 | 383fed94f 2026-09-27 | 2026-09-26 13:15
mag/concurrency_gate.py | 154 | 4 | 0 | 0 | 12 | d575bc168 2026-09-14 | 2026-09-05 23:39
mag/conductor.py | 190 | 3 | 0 | 3 | 11 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/conductor_eval.py | 85 | 2 | 0 | 1 | 2 | d575bc168 2026-09-14 | 2026-08-30 14:02
mag/connectivity_sizer.py | 216 | 4 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-12 19:29
mag/console_render.py | 124 | 4 | 0 | 0 | 2 | 052732ebf 2026-08-14 | 2026-08-13 08:54
mag/constants.py | 6 | 0 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-12 21:58
mag/constitutional_critique.py | 605 | 6 | 2 | 0 | 5 | 383fed94f 2026-09-27 | 2026-09-26 16:38
mag/context_admission.py | 102 | 3 | 0 | 1 | 3 | d575bc168 2026-09-14 | 2026-08-30 12:50
mag/context_checkpoint.py | 474 | 6 | 2 | 2 | 8 | d575bc168 2026-09-14 | 2026-08-30 12:51
mag/context_compression.py | 490 | 11 | 1 | 1 | 4 | d575bc168 2026-09-14 | 2026-08-30 12:51
mag/context_growth.py | 173 | 4 | 0 | 0 | 2 | de29d49ea 2026-08-09 | 2026-08-09 08:45
mag/context_pack.py | 1362 | 6 | 0 | 9 | 19 | a23928aca 2026-09-27 | 2026-09-28 13:29
mag/cooker.py | 164 | 4 | 0 | 0 | 4 | 86628c678 2026-09-24 | 2026-09-24 19:32
mag/coordination.py | 390 | 6 | 0 | 2 | 12 | 36914e134 2026-08-07 | 2026-08-07 07:45
mag/copilot_bridge.py | 380 | 6 | 3 | 0 | 3 | de7bb85fe 2026-08-09 | 2026-08-08 23:07
mag/corpus_expand.py | 150 | 5 | 0 | 0 | 3 | de29d49ea 2026-08-09 | 2026-08-09 18:38
mag/corpus_ingest.py | 207 | 4 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-12 08:50
mag/corpus_query.py | 433 | 3 | 0 | 0 | 4 | 799ddb6fe 2026-08-19 | 2026-08-14 19:00
mag/corpus_selfsteal.py | 321 | 6 | 0 | 0 | 0 | 5305a99b1 2026-09-16 | 2026-09-15 22:11
mag/corpus_wave.py | 179 | 5 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-11 11:43
mag/cost_enforcer.py | 486 | 10 | 0 | 1 | 6 | de29d49ea 2026-08-09 | 2026-08-09 18:46
mag/cost_governor.py | 210 | 9 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-08-30 20:06
mag/cost_learn.py | 341 | 6 | 0 | 0 | 15 | 052732ebf 2026-08-14 | 2026-08-11 09:04
mag/cost_ledger.py | 104 | 2 | 0 | 1 | 4 | d575bc168 2026-09-14 | 2026-08-30 20:13
mag/cost_simulator.py | 216 | 4 | 0 | 1 | 3 | bc61ef178 2026-08-05 | 2026-08-06 18:28
mag/cost_truth.py | 597 | 3 | 0 | 2 | 5 | 383fed94f 2026-09-27 | 2026-09-26 19:10
mag/cross_version.py | 628 | 8 | 0 | 0 | 3 | 60e18c524 2026-08-08 | 2026-08-08 07:07
mag/daemon.py | 195 | 2 | 0 | 1 | 4 | 02d818bf7 2026-09-26 | 2026-09-26 00:41
mag/dashboard_plugin.py | 105 | 1 | 1 | 1 | 0 | 36914e134 2026-08-07 | 2026-08-07 08:47
mag/data_refinery.py | 849 | 2 | 2 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-10 00:04
mag/data_source_watch.py | 161 | 4 | 0 | 0 | 3 | de29d49ea 2026-08-09 | 2026-08-09 15:41
mag/decision_framework.py | 322 | 6 | 0 | 1 | 9 | 60e18c524 2026-08-08 | 2026-08-07 18:30
mag/decision_hook.py | 90 | 2 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-05 21:38
mag/decl_attention.py | 740 | 16 | 4 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-06 10:39
mag/deep_research_moonshot.py | 234 | 4 | 0 | 1 | 1 | 052732ebf 2026-08-14 | 2026-08-13 07:44
mag/depin.py | 574 | 3 | 5 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-10 07:16
mag/desk_conductor.py | 779 | 9 | 0 | 1 | 6 | de29d49ea 2026-08-09 | 2026-08-09 07:47
mag/desk_dialogue.py | 1357 | 18 | 0 | 7 | 15 | 1c156e2fa 2026-08-06 | 2026-08-08 19:56
mag/desk_local_adapter.py | 174 | 7 | 0 | 1 | 7 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/desk_local_simulator.py | 29 | 1 | 0 | 0 | 1 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/desk_model_probe.py | 226 | 2 | 0 | 1 | 3 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/desk_observer.py | 353 | 6 | 0 | 1 | 3 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/desk_ops.py | 200 | 10 | 0 | 0 | 2 | 052732ebf 2026-08-14 | 2026-08-10 06:12
mag/desk_orchestrator.py | 90 | 1 | 0 | 1 | 1 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/desk_orchestrator_memory.py | 220 | 4 | 0 | 1 | 1 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/desk_overseer.py | 318 | 7 | 0 | 1 | 3 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/desk_teaching.py | 303 | 7 | 0 | 0 | 1 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/desk_timing.py | 173 | 14 | 1 | 1 | 4 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/desk_tools.py | 356 | 7 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-10 19:09
mag/destructive_receipt.py | 167 | 7 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-07 01:23
mag/deterministic_scanner.py | 211 | 7 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-13 04:21
mag/df_tileset.py | 136 | 5 | 0 | 0 | 3 | e96fd62a4 2026-08-07 | 2026-08-06 23:45
mag/diamond_mine.py | 166 | 3 | 0 | 0 | 3 | 052732ebf 2026-08-14 | 2026-08-11 10:30
mag/diary.py | 493 | 4 | 0 | 1 | 2 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/diary_node.py | 791 | 6 | 0 | 0 | 6 | d575bc168 2026-09-14 | 2026-08-30 22:36
mag/dirac_loop.py | 348 | 7 | 0 | 2 | 6 | 4638646d4 2026-09-27 | 2026-09-27 18:31
mag/dispatch.py | 396 | 1 | 0 | 1 | 10 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/display.py | 170 | 1 | 0 | 1 | 6 | d575bc168 2026-09-14 | 2026-08-30 13:51
mag/disposition_sweep.py | 88 | 2 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-06 18:50
mag/dissector.py | 738 | 14 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-07 15:25
mag/distill.py | 156 | 8 | 0 | 1 | 3 | 052732ebf 2026-08-14 | 2026-08-13 14:22
mag/divergence_meter.py | 107 | 2 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-05 22:29
mag/docker_ops.py | 253 | 8 | 0 | 1 | 6 | de29d49ea 2026-08-09 | 2026-08-09 19:21
mag/doctor.py | 1361 | 12 | 1 | 10 | 24 | 383fed94f 2026-09-27 | 2026-09-26 18:59
mag/doctor_agent.py | 435 | 5 | 1 | 0 | 3 | 052732ebf 2026-08-14 | 2026-08-10 07:16
mag/doctor_rightsize.py | 191 | 5 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-11 01:22
mag/doctrine_statute.py | 126 | 2 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-08 13:28
mag/dogfood_audit.py | 370 | 3 | 0 | 1 | 6 | d575bc168 2026-09-14 | 2026-08-31 00:50
mag/dormant.py | 84 | 4 | 0 | 3 | 13 | 383fed94f 2026-09-27 | 2026-09-26 19:10
mag/drainer_stats.py | 193 | 3 | 0 | 0 | 3 | 60e18c524 2026-08-08 | 2026-08-08 08:11
mag/dropbox_watcher.py | 282 | 5 | 0 | 0 | 1 | de29d49ea 2026-08-09 | 2026-08-09 14:30
mag/dspy_sovereign.py | 575 | 8 | 4 | 0 | 3 | de7bb85fe 2026-08-09 | 2026-08-08 22:51
mag/dungeon_dev.py | 201 | 5 | 0 | 0 | 6 | 052732ebf 2026-08-14 | 2026-08-12 06:37
mag/echo_net.py | 151 | 2 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-06 20:17
mag/ecosystem_surface.py | 338 | 5 | 0 | 0 | 5 | 052732ebf 2026-08-14 | 2026-08-10 11:45
mag/effect_broker.py | 607 | 8 | 0 | 1 | 5 | d575bc168 2026-09-14 | 2026-08-31 00:53
mag/egregore_steal.py | 131 | 3 | 0 | 0 | 2 | 052732ebf 2026-08-14 | 2026-08-11 10:17
mag/elder.py | 93 | 2 | 0 | 1 | 4 | d575bc168 2026-09-14 | 2026-08-31 00:26
mag/electron_seat.py | 210 | 3 | 0 | 0 | 2 | 052732ebf 2026-08-14 | 2026-08-13 20:33
mag/elevate.py | 158 | 5 | 0 | 1 | 3 | de29d49ea 2026-08-09 | 2026-08-09 02:02
mag/embassy_deliver.py | 382 | 6 | 0 | 1 | 4 | d575bc168 2026-09-14 | 2026-09-01 21:09
mag/embassy_integrity.py | 296 | 6 | 6 | 1 | 4 | cb26bc2cd 2026-08-25 | 2026-08-23 23:20
mag/emergence.py | 246 | 5 | 0 | 0 | 4 | 052732ebf 2026-08-14 | 2026-08-11 09:27
mag/emergence_test.py | 260 | 3 | 2 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-12 18:02
mag/emergent_harvest.py | 316 | 4 | 1 | 0 | 3 | 052732ebf 2026-08-14 | 2026-08-09 22:48
mag/end_state.py | 160 | 4 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-11 13:42
mag/engram.py | 135 | 4 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-13 10:10
mag/env_redirect.py | 116 | 2 | 0 | 2 | 2 | 383fed94f 2026-09-27 | 2026-09-26 13:33
mag/env_registry.py | 262 | 13 | 0 | 2 | 6 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/epistemic_guard.py | 164 | 6 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-13 04:52
mag/error_healer.py | 163 | 5 | 0 | 0 | 4 | de29d49ea 2026-08-09 | 2026-08-09 17:12
mag/events_key_schema.py | 105 | 3 | 0 | 0 | 4 | 383fed94f 2026-09-27 | 2026-09-26 13:37
mag/events_scan.py | 47 | 1 | 0 | 0 | 1 | 383fed94f 2026-09-27 | 2026-09-26 16:41
mag/evolving_wave.py | 284 | 6 | 0 | 0 | 1 | cb26bc2cd 2026-08-25 | 2026-08-24 11:17
mag/exit_dialogue.py | 356 | 3 | 1 | 0 | 1 | 482e0a3c8 2026-08-08 | 2026-08-08 19:11
mag/extension_deploy.py | 70 | 3 | 0 | 0 | 4 | 60e18c524 2026-08-08 | 2026-08-08 10:54
mag/fact_bus.py | 149 | 3 | 0 | 0 | 3 | 052732ebf 2026-08-14 | 2026-08-11 08:06
mag/factory_gate.py | 76 | 2 | 0 | 1 | 11 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/factory_machine.py | 395 | 5 | 0 | 2 | 4 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/failure_kb.py | 829 | 12 | 0 | 3 | 27 | 383fed94f 2026-09-27 | 2026-09-26 17:07
mag/falsifier_counter.py | 703 | 12 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-05 00:20
mag/fanout.py | 107 | 3 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-12 09:25
mag/feature_lab.py | 203 | 2 | 0 | 1 | 1 | e4dd520e8 2026-08-06 | 2026-08-06 18:28
mag/feedback.py | 101 | 2 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-11 01:22
mag/fermat_ractor.py | 970 | 21 | 1 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-06 17:57
mag/field_steal.py | 344 | 7 | 0 | 0 | 2 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/final_steal.py | 178 | 4 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-11 11:33
mag/fire_horse.py | 51 | 0 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-10 12:38
mag/fireball_cycle.py | 59 | 2 | 0 | 0 | 3 | d575bc168 2026-09-14 | 2026-08-30 22:00
mag/fish_ear.py | 145 | 4 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-11 11:28
mag/fleet_intel.py | 193 | 3 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-06 17:33
mag/flex_test.py | 138 | 2 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-10 00:54
mag/flight_recorder.py | 423 | 5 | 0 | 0 | 7 | a5dd96176 2026-09-25 | 2026-09-22 01:16
mag/flock_anim.py | 313 | 6 | 0 | 0 | 3 | cb26bc2cd 2026-08-25 | 2026-08-23 23:20
mag/flock_field.py | 265 | 7 | 2 | 0 | 7 | 052732ebf 2026-08-14 | 2026-08-09 22:24
mag/flock_grid.py | 96 | 6 | 0 | 0 | 3 | 052732ebf 2026-08-14 | 2026-08-11 07:51
mag/flock_job.py | 171 | 3 | 0 | 0 | 2 | 052732ebf 2026-08-14 | 2026-08-10 10:56
mag/flock_scheduler.py | 202 | 2 | 0 | 0 | 4 | 052732ebf 2026-08-14 | 2026-08-10 10:56
mag/flock_shader.py | 335 | 11 | 3 | 0 | 8 | 052732ebf 2026-08-14 | 2026-08-11 07:51
mag/flock_steal.py | 225 | 2 | 0 | 0 | 6 | 052732ebf 2026-08-14 | 2026-08-10 11:05
mag/flock_usage_guard.py | 150 | 4 | 0 | 0 | 3 | 052732ebf 2026-08-14 | 2026-08-11 09:09
mag/forge_daemon.py | 165 | 4 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-13 21:44
mag/fork_router.py | 305 | 2 | 0 | 1 | 2 | 36914e134 2026-08-07 | 2026-08-07 09:43
mag/framework_map.py | 992 | 9 | 0 | 0 | 4 | 60e18c524 2026-08-08 | 2026-08-08 10:27
mag/free_frontend_swarm.py | 129 | 4 | 0 | 0 | 2 | 052732ebf 2026-08-14 | 2026-08-12 01:37
mag/free_tier.py | 185 | 2 | 0 | 1 | 2 | 383fed94f 2026-09-27 | 2026-09-26 19:10
mag/free_to_swarm.py | 137 | 3 | 0 | 0 | 0 | cb26bc2cd 2026-08-25 | 2026-08-23 20:33
mag/frontier_advisor.py | 152 | 3 | 0 | 1 | 4 | 052732ebf 2026-08-14 | 2026-08-12 18:08
mag/frontier_batch.py | 157 | 6 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-10 15:08
mag/frontier_council.py | 416 | 10 | 0 | 3 | 4 | d575bc168 2026-09-14 | 2026-09-01 21:10
mag/frontier_game.py | 237 | 3 | 0 | 1 | 3 | 799ddb6fe 2026-08-19 | 2026-08-14 10:10
mag/frontier_gravity.py | 356 | 9 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-12 19:12
mag/frontier_help.py | 172 | 3 | 0 | 0 | 3 | de29d49ea 2026-08-09 | 2026-08-09 09:12
mag/frontier_intake.py | 160 | 4 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-10 17:03
mag/frontier_rib.py | 188 | 4 | 0 | 0 | 4 | 052732ebf 2026-08-14 | 2026-08-11 11:33
mag/frontier_salon.py | 399 | 4 | 0 | 2 | 6 | 5dff72ac3 2026-09-28 | 2026-09-28 13:04
mag/frontier_salon_cli.py | 37 | 1 | 0 | 0 | 1 | 5dff72ac3 2026-09-28 | 2026-09-28 13:05
mag/frontier_scout.py | 570 | 6 | 2 | 0 | 6 | de7bb85fe 2026-08-09 | 2026-08-08 22:31
mag/frontier_steer.py | 45 | 3 | 0 | 0 | 4 | 052732ebf 2026-08-14 | 2026-08-10 15:12
mag/fuel_feed.py | 705 | 7 | 0 | 4 | 19 | 383fed94f 2026-09-27 | 2026-09-26 19:10
mag/future_self.py | 142 | 3 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-12 08:05
mag/ga4_progression.py | 698 | 1 | 8 | 0 | 0 | de7bb85fe 2026-08-09 | 2026-08-08 20:30
mag/gab_seat.py | 267 | 6 | 0 | 0 | 0 | 799ddb6fe 2026-08-19 | 2026-08-18 20:55
mag/game_battle_cycle.py | 615 | 8 | 0 | 0 | 2 | e96fd62a4 2026-08-07 | 2026-08-07 00:09
mag/game_brawl.py | 1668 | 12 | 0 | 0 | 4 | e96fd62a4 2026-08-07 | 2026-08-07 01:14
mag/game_brawl_perspectives.py | 239 | 4 | 0 | 0 | 2 | e96fd62a4 2026-08-07 | 2026-08-07 01:01
mag/game_campaign.py | 4838 | 17 | 0 | 2 | 23 | 7b8617d78 2026-09-27 | 2026-09-27 23:36
mag/game_curveball.py | 455 | 3 | 0 | 0 | 4 | 799ddb6fe 2026-08-19 | 2026-08-14 08:08
mag/game_dfhack.py | 126 | 6 | 0 | 1 | 0 | 052732ebf 2026-08-14 | 2026-08-13 13:38
mag/game_dice.py | 31 | 1 | 0 | 0 | 4 | e96fd62a4 2026-08-07 | 2026-08-06 21:49
mag/game_dm.py | 228 | 8 | 0 | 1 | 4 | 799ddb6fe 2026-08-19 | 2026-08-14 10:10
mag/game_dm_llm.py | 153 | 2 | 0 | 0 | 4 | 799ddb6fe 2026-08-19 | 2026-08-15 05:51
mag/game_dm_voice.py | 318 | 2 | 0 | 0 | 6 | e96fd62a4 2026-08-07 | 2026-08-07 01:02
mag/game_emulator.py | 220 | 5 | 0 | 1 | 3 | 052732ebf 2026-08-14 | 2026-08-12 18:08
mag/game_entry.py | 240 | 6 | 0 | 1 | 1 | 052732ebf 2026-08-14 | 2026-08-13 07:44
mag/game_environment.py | 167 | 4 | 0 | 1 | 1 | 052732ebf 2026-08-14 | 2026-08-13 20:01
mag/game_flow.py | 169 | 5 | 0 | 0 | 2 | 799ddb6fe 2026-08-19 | 2026-08-17 06:13
mag/game_freeze.py | 432 | 9 | 0 | 0 | 2 | e96fd62a4 2026-08-07 | 2026-08-07 01:14
mag/game_live.py | 159 | 4 | 0 | 1 | 1 | 052732ebf 2026-08-14 | 2026-08-12 15:37
mag/game_mud.py | 557 | 5 | 0 | 0 | 5 | cb26bc2cd 2026-08-25 | 2026-08-23 23:20
mag/game_narrate.py | 118 | 1 | 0 | 0 | 3 | 799ddb6fe 2026-08-19 | 2026-08-15 22:30
mag/game_observer.py | 256 | 8 | 0 | 0 | 1 | 799ddb6fe 2026-08-19 | 2026-08-15 08:12
mag/game_passage.py | 203 | 5 | 0 | 0 | 3 | 799ddb6fe 2026-08-19 | 2026-08-15 21:44
mag/game_piece_tandem.py | 243 | 5 | 0 | 1 | 0 | 799ddb6fe 2026-08-19 | 2026-08-17 06:10
mag/game_play.py | 208 | 5 | 0 | 1 | 1 | 799ddb6fe 2026-08-19 | 2026-08-16 13:15
mag/game_portal.py | 181 | 4 | 0 | 1 | 1 | 052732ebf 2026-08-14 | 2026-08-12 16:40
mag/game_produce.py | 257 | 6 | 0 | 0 | 0 | 799ddb6fe 2026-08-19 | 2026-08-16 18:12
mag/game_ramp.py | 574 | 10 | 0 | 1 | 4 | 9546bb7f8 2026-09-16 | 2026-09-16 19:30
mag/game_saga.py | 113 | 4 | 0 | 0 | 2 | 799ddb6fe 2026-08-19 | 2026-08-14 22:30
mag/game_salon.py | 492 | 12 | 0 | 0 | 1 | e96fd62a4 2026-08-07 | 2026-08-07 00:07
mag/game_score.py | 101 | 2 | 0 | 0 | 3 | 799ddb6fe 2026-08-19 | 2026-08-16 12:49
mag/game_view.py | 313 | 3 | 0 | 0 | 16 | 799ddb6fe 2026-08-19 | 2026-08-15 22:12
mag/game_world.py | 125 | 4 | 0 | 7 | 32 | 052732ebf 2026-08-14 | 2026-08-12 06:49
mag/game_world_map.py | 93 | 2 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-12 07:01
mag/game_world_render.py | 301 | 5 | 0 | 2 | 5 | 99826e153 2026-09-14 | 2026-09-14 05:57
mag/gap_analysis.py | 154 | 2 | 0 | 0 | 3 | de7bb85fe 2026-08-09 | 2026-08-09 00:05
mag/gap_frontier.py | 170 | 4 | 0 | 0 | 7 | 052732ebf 2026-08-14 | 2026-08-11 11:28
mag/gap_map.py | 165 | 4 | 0 | 0 | 9 | de29d49ea 2026-08-09 | 2026-08-09 09:12
mag/gap_resolver.py | 96 | 2 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-10 14:15
mag/gap_routed_handoff.py | 195 | 5 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-11 22:47
mag/gap_swarm_experiment.py | 537 | 14 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-11 06:09
mag/gene_pool_feeder.py | 346 | 7 | 0 | 0 | 0 | 8763e6809 2026-09-27 | 2026-09-27 10:51
mag/gguf_cartography.py | 583 | 12 | 1 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-05 23:53
mag/ghost.py | 4242 | 30 | 0 | 5 | 41 | 383fed94f 2026-09-27 | 2026-09-26 16:39
mag/ghost_auto.py | 184 | 3 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-10 14:34
mag/ghost_cold_boot.py | 177 | 4 | 0 | 0 | 3 | d575bc168 2026-09-14 | 2026-09-01 21:02
mag/ghost_control.py | 139 | 2 | 0 | 1 | 3 | de29d49ea 2026-08-09 | 2026-08-09 14:16
mag/ghost_cross.py | 505 | 3 | 3 | 0 | 2 | 60e18c524 2026-08-08 | 2026-08-08 05:40
mag/ghost_director.py | 654 | 7 | 0 | 0 | 0 | 60e18c524 2026-08-08 | 2026-08-07 22:48
mag/ghost_doctor.py | 150 | 5 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-10 19:13
mag/ghost_experimenter.py | 239 | 6 | 0 | 0 | 4 | 052732ebf 2026-08-14 | 2026-08-10 18:41
mag/ghost_grok_dashboard.py | 183 | 4 | 0 | 0 | 4 | de29d49ea 2026-08-09 | 2026-08-09 13:31
mag/ghost_identity.py | 142 | 2 | 0 | 0 | 2 | 60e18c524 2026-08-08 | 2026-08-08 15:59
mag/ghost_leak_detector.py | 1054 | 15 | 4 | 0 | 4 | 482e0a3c8 2026-08-08 | 2026-08-08 19:11
mag/ghost_ledger.py | 273 | 5 | 0 | 0 | 5 | de29d49ea 2026-08-09 | 2026-08-09 07:47
mag/ghost_memlance.py | 438 | 7 | 0 | 2 | 10 | d575bc168 2026-09-14 | 2026-08-30 14:23
mag/ghost_nudge.py | 124 | 4 | 0 | 0 | 3 | de29d49ea 2026-08-09 | 2026-08-09 13:49
mag/ghost_pylance.py | 335 | 8 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-11 08:14
mag/ghost_server.py | 114 | 4 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-11 05:54
mag/ghost_spooky.py | 163 | 3 | 0 | 1 | 1 | 052732ebf 2026-08-14 | 2026-08-11 22:15
mag/ghost_summon.py | 346 | 8 | 0 | 1 | 13 | de29d49ea 2026-08-09 | 2026-08-09 11:59
mag/ghost_talk.py | 146 | 3 | 0 | 1 | 1 | de29d49ea 2026-08-09 | 2026-08-09 14:30
mag/ghost_whisper.py | 163 | 3 | 0 | 0 | 6 | 052732ebf 2026-08-14 | 2026-08-09 21:39
mag/git_divergence.py | 117 | 3 | 0 | 0 | 0 | ad10682d0 2026-09-15 | 2026-09-15 23:07
mag/glm_flash.py | 112 | 2 | 0 | 0 | 7 | d575bc168 2026-09-14 | 2026-08-28 18:16
mag/gopher_lite.py | 251 | 9 | 0 | 0 | 0 | a5dd96176 2026-09-25 | 2026-09-23 14:25
mag/governance.py | 214 | 2 | 0 | 0 | 4 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/governor.py | 397 | 11 | 0 | 2 | 8 | cb26bc2cd 2026-08-25 | 2026-08-24 08:15
mag/governor_autorun.py | 2183 | 12 | 0 | 7 | 19 | 383fed94f 2026-09-27 | 2026-09-26 09:53
mag/gpipes.py | 401 | 7 | 0 | 1 | 5 | 052732ebf 2026-08-14 | 2026-09-27 23:19
mag/gpu_ghost.py | 309 | 4 | 0 | 0 | 8 | 383fed94f 2026-09-27 | 2026-09-26 12:53
mag/gpu_k8s.py | 228 | 5 | 0 | 0 | 6 | 052732ebf 2026-08-14 | 2026-08-11 00:50
mag/gpu_lifecycle.py | 138 | 4 | 0 | 0 | 10 | 052732ebf 2026-08-14 | 2026-08-11 09:40
mag/gpu_memweave.py | 113 | 2 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-11 19:34
mag/grammar_transfer.py | 266 | 9 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-06 02:11
mag/grok_bot.py | 290 | 6 | 0 | 0 | 6 | 052732ebf 2026-08-14 | 2026-08-13 04:52
mag/grok_brief.py | 162 | 3 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-12 07:54
mag/grok_desktop.py | 165 | 5 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-13 18:08
mag/grok_free.py | 383 | 10 | 0 | 0 | 7 | d575bc168 2026-09-14 | 2026-08-30 22:04
mag/grok_frontier_loop.py | 270 | 7 | 0 | 0 | 2 | 052732ebf 2026-08-14 | 2026-08-11 01:04
mag/grok_gate.py | 83 | 2 | 0 | 0 | 6 | de29d49ea 2026-08-09 | 2026-08-09 13:04
mag/grok_hub.py | 234 | 6 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-11 01:22
mag/grok_mirror.py | 354 | 9 | 0 | 0 | 5 | 052732ebf 2026-08-14 | 2026-08-10 19:13
mag/grok_rightsize.py | 669 | 13 | 1 | 0 | 29 | d575bc168 2026-09-14 | 2026-09-05 22:10
mag/grok_route.py | 48 | 3 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-05 22:08
mag/grok_seat_burner.py | 503 | 12 | 0 | 0 | 14 | d575bc168 2026-09-14 | 2026-08-26 16:37
mag/grok_steer.py | 136 | 3 | 0 | 0 | 2 | 799ddb6fe 2026-08-19 | 2026-08-16 18:39
mag/grok_tandem.py | 142 | 5 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-05 22:33
mag/grok_terminal.py | 361 | 6 | 0 | 0 | 5 | de29d49ea 2026-08-09 | 2026-08-09 09:23
mag/grok_warm_rib.py | 162 | 6 | 0 | 0 | 2 | d575bc168 2026-09-14 | 2026-08-25 23:00
mag/grok_weave.py | 202 | 5 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-12 07:54
mag/grokbot_cold_edges.py | 186 | 7 | 0 | 0 | 2 | 052732ebf 2026-08-14 | 2026-08-12 01:07
mag/grounding_wave.py | 975 | 9 | 1 | 3 | 5 | 118333dd1 2026-09-16 | 2026-09-16 21:26
mag/grove.py | 150 | 2 | 0 | 2 | 3 | f31c0e926 2026-08-05 | 2026-08-06 18:28
mag/growth_cycle.py | 463 | 6 | 0 | 1 | 2 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/gstd_probe.py | 209 | 2 | 0 | 1 | 2 | 9c8fc49e8 2026-08-06 | 2026-08-06 18:28
mag/guard.py | 104 | 3 | 0 | 0 | 3 | d575bc168 2026-09-14 | 2026-08-28 19:44
mag/guard_registry.py | 255 | 3 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-10 21:49
mag/guardrail_sentinel.py | 149 | 4 | 0 | 0 | 2 | 052732ebf 2026-08-14 | 2026-08-10 12:53
mag/gygax_steal.py | 160 | 5 | 0 | 1 | 0 | 052732ebf 2026-08-14 | 2026-08-12 16:58
mag/hall_shared_supper.py | 163 | 6 | 0 | 0 | 4 | cb26bc2cd 2026-08-25 | 2026-08-23 03:03
mag/handoff_inbox.py | 144 | 4 | 0 | 1 | 4 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/harness.py | 735 | 16 | 0 | 0 | 3 | d575bc168 2026-09-14 | 2026-08-31 07:26
mag/harvest_fold.py | 161 | 6 | 0 | 1 | 1 | 799ddb6fe 2026-08-19 | 2026-08-16 13:15
mag/headless.py | 203 | 7 | 0 | 2 | 30 | 799ddb6fe 2026-08-19 | 2026-08-16 17:33
mag/health.py | 365 | 8 | 0 | 2 | 19 | 6d417abd5 2026-09-26 | 2026-09-26 17:24
mag/hermes_steering.py | 340 | 4 | 0 | 0 | 2 | d575bc168 2026-09-14 | 2026-09-11 22:22
mag/hermes_warm_boot.py | 124 | 2 | 0 | 0 | 0 | a5dd96176 2026-09-25 | 2026-09-23 19:23
mag/hero_simulation.py | 395 | 11 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-07 01:13
mag/hf_space.py | 585 | 7 | 0 | 0 | 0 | 60e18c524 2026-08-08 | 2026-08-08 14:36
mag/holographic_q.py | 848 | 9 | 3 | 1 | 8 | d575bc168 2026-09-14 | 2026-09-01 21:02
mag/honest_cache_meter.py | 498 | 12 | 4 | 1 | 0 | d575bc168 2026-09-14 | 2026-09-01 21:00
mag/hood.py | 153 | 2 | 0 | 1 | 1 | d575bc168 2026-09-14 | 2026-08-29 21:28
mag/host_resolver.py | 206 | 5 | 0 | 0 | 2 | d575bc168 2026-09-14 | 2026-09-12 23:01
mag/host_roundtrip.py | 110 | 4 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-11 19:41
mag/hour_test.py | 117 | 3 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-12 06:24
mag/hydro_xor_sim.py | 294 | 4 | 2 | 1 | 1 | 75c030d29 2026-09-16 | 2026-09-16 16:11
mag/icon_drop.py | 376 | 6 | 0 | 3 | 2 | 383fed94f 2026-09-27 | 2026-09-26 17:22
mag/idea_flow.py | 600 | 1 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-08-30 20:03
mag/idea_graph.py | 537 | 14 | 0 | 1 | 12 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/improve.py | 2773 | 19 | 0 | 12 | 14 | 2ba484fc9 2026-09-28 | 2026-09-28 12:47
mag/improve_loop.py | 328 | 4 | 0 | 2 | 9 | d575bc168 2026-09-14 | 2026-08-30 16:38
mag/ingest_registry.py | 556 | 2 | 0 | 0 | 3 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/integrity_kernel.py | 299 | 7 | 6 | 0 | 4 | cb26bc2cd 2026-08-25 | 2026-08-25 11:17
mag/intent_rightsize.py | 239 | 4 | 0 | 0 | 3 | 052732ebf 2026-08-14 | 2026-08-12 07:54
mag/intention_brief.py | 290 | 3 | 0 | 1 | 3 | e96fd62a4 2026-08-07 | 2026-08-06 21:26
mag/interrupt_pipeline.py | 219 | 5 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-10 20:14
mag/intervention_gate.py | 470 | 11 | 3 | 1 | 0 | a5dd96176 2026-09-25 | 2026-09-25 20:54
mag/invariant.py | 321 | 9 | 0 | 1 | 5 | d575bc168 2026-09-14 | 2026-08-26 08:06
mag/invariant_lattice.py | 187 | 6 | 0 | 0 | 7 | 052732ebf 2026-08-14 | 2026-08-10 17:36
mag/invariant_ledger.py | 185 | 4 | 0 | 0 | 3 | 052732ebf 2026-08-14 | 2026-08-11 09:27
mag/invariant_npcs.py | 252 | 7 | 0 | 0 | 0 | 799ddb6fe 2026-08-19 | 2026-08-15 05:34
mag/invariant_surface.py | 258 | 7 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-10 16:55
mag/janitor.py | 273 | 5 | 0 | 0 | 7 | 60e18c524 2026-08-08 | 2026-08-08 09:56
mag/job_floor.py | 225 | 7 | 0 | 3 | 3 | 60e18c524 2026-08-08 | 2026-08-07 18:15
mag/jones_lens.py | 125 | 5 | 0 | 0 | 7 | 052732ebf 2026-08-14 | 2026-08-11 09:32
mag/judge.py | 138 | 1 | 0 | 0 | 1 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/k8s_bridge.py | 164 | 12 | 0 | 0 | 3 | 052732ebf 2026-08-14 | 2026-08-10 17:36
mag/kabuki_salon.py | 179 | 2 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-07 08:09
mag/key_law.py | 107 | 3 | 0 | 0 | 8 | 3ee362d04 2026-09-24 | 2026-09-24 15:08
mag/knot_at_close.py | 280 | 1 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-07 08:12
mag/knot_math.py | 241 | 7 | 0 | 0 | 1 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/knot_untangle.py | 232 | 4 | 0 | 0 | 2 | 052732ebf 2026-08-14 | 2026-08-11 22:15
mag/knowledge_graph.py | 560 | 10 | 0 | 0 | 24 | 799ddb6fe 2026-08-19 | 2026-08-15 10:30
mag/kv_seal.py | 142 | 5 | 0 | 1 | 0 | 4cb4c99a7 2026-09-22 | 2026-09-22 01:39
mag/kvos_block.py | 112 | 3 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-10 08:23
mag/lab_episode.py | 493 | 9 | 11 | 1 | 1 | d575bc168 2026-09-14 | 2026-08-29 13:38
mag/ladder.py | 198 | 4 | 0 | 0 | 0 | cb26bc2cd 2026-08-25 | 2026-08-25 12:35
mag/lane_breaker.py | 136 | 4 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-13 09:56
mag/lane_cadence.py | 270 | 8 | 0 | 2 | 4 | 790145ab1 2026-09-26 | 2026-09-26 01:44
mag/lane_effort.py | 358 | 6 | 0 | 1 | 1 | a5dd96176 2026-09-25 | 2026-09-25 20:17
mag/lane_probe.py | 150 | 6 | 0 | 0 | 0 | a0f7a593a 2026-09-24 | 2026-09-24 19:11
mag/lane_runner.py | 1141 | 24 | 0 | 3 | 15 | a23928aca 2026-09-27 | 2026-09-27 21:04
mag/lane_salon.py | 229 | 2 | 0 | 2 | 2 | 383fed94f 2026-09-27 | 2026-09-26 19:10
mag/lane_supervisor.py | 235 | 2 | 0 | 0 | 1 | d5ad6403e 2026-09-25 | 2026-09-25 14:01
mag/lanes.py | 316 | 12 | 0 | 0 | 16 | 383fed94f 2026-09-27 | 2026-09-26 21:50
mag/lattice_backfill.py | 403 | 5 | 0 | 1 | 3 | 2464edcba 2026-08-04 | 2026-08-04 18:48
mag/lattice_dashboard.py | 257 | 1 | 0 | 0 | 2 | 4e7350700 2026-08-05 | 2026-08-06 18:28
mag/lattice_distance.py | 131 | 4 | 0 | 1 | 2 | d575bc168 2026-09-14 | 2026-09-04 08:12
mag/lattice_logic.py | 256 | 7 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-04 13:34
mag/lattice_loop.py | 803 | 11 | 0 | 1 | 4 | c65c4e7aa 2026-08-05 | 2026-08-06 18:28
mag/lattice_query.py | 130 | 6 | 0 | 1 | 4 | 2464edcba 2026-08-04 | 2026-08-04 18:48
mag/launch_pad.py | 130 | 1 | 0 | 1 | 1 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/law.py | 322 | 5 | 0 | 1 | 6 | d575bc168 2026-09-14 | 2026-08-30 16:19
mag/leaked_prompt_mine.py | 138 | 5 | 0 | 0 | 2 | 052732ebf 2026-08-14 | 2026-08-10 15:08
mag/learn_rightsize.py | 164 | 4 | 0 | 0 | 4 | de29d49ea 2026-08-09 | 2026-08-09 16:29
mag/legacy_audit.py | 331 | 6 | 0 | 1 | 3 | 383fed94f 2026-09-27 | 2026-09-26 12:53
mag/lens_chain.py | 288 | 6 | 0 | 0 | 6 | 052732ebf 2026-08-14 | 2026-08-10 19:32
mag/lens_knot.py | 192 | 5 | 0 | 2 | 9 | 052732ebf 2026-08-14 | 2026-08-11 09:58
mag/lens_library.py | 533 | 6 | 3 | 0 | 8 | de7bb85fe 2026-08-09 | 2026-08-08 20:37
mag/lens_shader.py | 198 | 7 | 2 | 0 | 3 | 052732ebf 2026-08-14 | 2026-08-11 09:58
mag/lens_tournament.py | 263 | 5 | 0 | 0 | 2 | de29d49ea 2026-08-09 | 2026-08-09 14:55
mag/librarian.py | 258 | 6 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-10 16:40
mag/librarian_catalog.py | 205 | 5 | 0 | 0 | 4 | a5dd96176 2026-09-25 | 2026-09-23 14:16
mag/lifecycle.py | 916 | 9 | 0 | 4 | 9 | 6d417abd5 2026-09-26 | 2026-09-26 17:24
mag/line_builder.py | 140 | 5 | 0 | 0 | 2 | 052732ebf 2026-08-14 | 2026-08-11 07:51
mag/link_library.py | 396 | 13 | 0 | 2 | 6 | 383fed94f 2026-09-27 | 2026-09-26 15:50
mag/links_sha_ratchet.py | 152 | 2 | 0 | 1 | 1 | 383fed94f 2026-09-27 | 2026-09-26 19:00
mag/links_split_gate.py | 143 | 3 | 0 | 0 | 2 | 383fed94f 2026-09-27 | 2026-09-26 15:59
mag/lite_guard.py | 265 | 6 | 0 | 0 | 30 | d575bc168 2026-09-14 | 2026-09-05 00:35
mag/lite_scale.py | 166 | 2 | 0 | 0 | 0 | 0f34a8f3e 2026-09-16 | 2026-09-16 14:44
mag/live_feed.py | 194 | 2 | 0 | 0 | 3 | 60e18c524 2026-08-08 | 2026-08-08 08:11
mag/live_ops_readiness.py | 151 | 3 | 0 | 1 | 5 | d575bc168 2026-09-14 | 2026-09-02 04:10
mag/live_report.py | 150 | 2 | 0 | 0 | 3 | d575bc168 2026-09-14 | 2026-09-02 04:10
mag/liveness_sense.py | 256 | 3 | 0 | 0 | 2 | d575bc168 2026-09-14 | 2026-08-30 14:44
mag/lm_studio.py | 122 | 4 | 0 | 1 | 2 | d575bc168 2026-09-14 | 2026-09-01 16:01
mag/local_mode.py | 43 | 3 | 0 | 0 | 3 | 36914e134 2026-08-07 | 2026-08-07 06:27
mag/local_playbook.py | 322 | 8 | 0 | 0 | 5 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/local_pulse.py | 210 | 2 | 0 | 1 | 4 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/local_scheduler.py | 458 | 6 | 0 | 1 | 8 | d575bc168 2026-09-14 | 2026-09-02 04:10
mag/local_usable.py | 514 | 9 | 0 | 0 | 1 | e96fd62a4 2026-08-07 | 2026-08-06 22:30
mag/loop_audit.py | 334 | 7 | 0 | 1 | 7 | f5a055a7e 2026-08-05 | 2026-08-06 18:28
mag/loop_breaker.py | 258 | 3 | 0 | 2 | 3 | 383fed94f 2026-09-27 | 2026-09-26 12:54
mag/loop_doctor.py | 129 | 3 | 0 | 0 | 5 | 052732ebf 2026-08-14 | 2026-08-11 11:43
mag/loop_feedback.py | 107 | 2 | 0 | 0 | 4 | 052732ebf 2026-08-14 | 2026-08-11 12:47
mag/loop_health.py | 224 | 2 | 0 | 0 | 1 | cb26bc2cd 2026-08-25 | 2026-08-24 07:26
mag/loops_registry.py | 234 | 2 | 0 | 1 | 2 | 60e18c524 2026-08-08 | 2026-08-08 10:09
mag/lora_pipeline.py | 549 | 5 | 1 | 0 | 4 | de7bb85fe 2026-08-09 | 2026-08-08 22:52
mag/machine_target.py | 75 | 4 | 0 | 0 | 7 | 052732ebf 2026-08-14 | 2026-08-11 08:06
mag/main_channel.py | 457 | 9 | 0 | 0 | 2 | d575bc168 2026-09-14 | 2026-09-01 18:05
mag/manifest.py | 191 | 5 | 0 | 0 | 4 | cb26bc2cd 2026-08-25 | 2026-08-24 10:17
mag/matrix_router.py | 174 | 4 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-10 20:39
mag/max_distill.py | 255 | 3 | 0 | 1 | 2 | d575bc168 2026-09-14 | 2026-08-26 14:04
mag/max_distill_arms.py | 310 | 5 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-08-27 04:08
mag/maze_real.py | 151 | 3 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-13 11:20
mag/mcp_http.py | 44 | 0 | 0 | 0 | 2 | d575bc168 2026-09-14 | 2026-09-04 20:10
mag/mcp_server.py | 410 | 8 | 0 | 2 | 8 | 383fed94f 2026-09-27 | 2026-09-26 16:47
mag/mem_invariant_map.py | 232 | 5 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-11 12:47
mag/mem_lands.py | 217 | 5 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-11 05:54
mag/mem_ollama.py | 258 | 7 | 0 | 0 | 2 | 052732ebf 2026-08-14 | 2026-08-10 19:32
mag/mem_weave_distributor.py | 178 | 6 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-11 01:22
mag/memlang.py | 442 | 9 | 0 | 1 | 26 | d575bc168 2026-09-14 | 2026-08-30 16:26
mag/memory_consolidate.py | 217 | 4 | 0 | 0 | 0 | 799ddb6fe 2026-08-19 | 2026-08-18 11:46
mag/memory_events.py | 159 | 5 | 0 | 2 | 6 | 36914e134 2026-08-07 | 2026-08-07 12:32
mag/memory_map.py | 213 | 8 | 0 | 1 | 0 | 60e18c524 2026-08-08 | 2026-08-08 17:21
mag/memory_train_seed.py | 185 | 3 | 0 | 0 | 0 | 799ddb6fe 2026-08-19 | 2026-08-18 12:18
mag/memweave.py | 197 | 4 | 0 | 0 | 4 | cb26bc2cd 2026-08-25 | 2026-08-23 23:20
mag/meta_lattice.py | 124 | 3 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-12 06:15
mag/meta_percolate.py | 233 | 6 | 0 | 0 | 3 | 052732ebf 2026-08-14 | 2026-08-13 07:09
mag/mind_mine.py | 417 | 3 | 0 | 0 | 0 | cb26bc2cd 2026-08-25 | 2026-08-23 13:01
mag/mind_window.py | 474 | 7 | 0 | 0 | 1 | cb26bc2cd 2026-08-25 | 2026-08-23 13:01
mag/mindweave_eval.py | 269 | 5 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-10 11:05
mag/mine_diamonds.py | 247 | 3 | 0 | 0 | 2 | 052732ebf 2026-08-14 | 2026-08-09 22:34
mag/mirror_control.py | 123 | 2 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-08 14:13
mag/mixture_of_agents.py | 422 | 4 | 3 | 0 | 3 | de7bb85fe 2026-08-09 | 2026-08-08 22:51
mag/model_health.py | 150 | 3 | 0 | 0 | 2 | 052732ebf 2026-08-14 | 2026-08-09 22:57
mag/model_pick.py | 87 | 2 | 0 | 0 | 6 | de29d49ea 2026-08-09 | 2026-08-09 08:07
mag/modules.py | 272 | 6 | 0 | 0 | 5 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/moonshot_engine.py | 227 | 5 | 0 | 1 | 2 | 052732ebf 2026-08-14 | 2026-08-12 15:48
mag/mrna_steal.py | 86 | 2 | 0 | 0 | 0 | 799ddb6fe 2026-08-19 | 2026-08-15 05:51
mag/mud_steal.py | 159 | 5 | 0 | 1 | 2 | 052732ebf 2026-08-14 | 2026-08-12 16:58
mag/museum.py | 207 | 4 | 0 | 0 | 0 | cb26bc2cd 2026-08-25 | 2026-08-24 16:40
mag/mycelium.py | 354 | 13 | 0 | 1 | 27 | 799ddb6fe 2026-08-19 | 2026-08-15 20:15
mag/narrative_engine.py | 845 | 4 | 2 | 0 | 2 | de7bb85fe 2026-08-09 | 2026-08-08 23:53
mag/narrative_tests.py | 388 | 9 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-10 16:54
mag/nervous_system.py | 522 | 6 | 0 | 4 | 11 | d575bc168 2026-09-14 | 2026-08-30 15:28
mag/no_win.py | 120 | 4 | 0 | 1 | 0 | 750259531 2026-09-27 | 2026-09-27 19:13
mag/north_star.py | 143 | 3 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-11 05:32
mag/notion_api.py | 178 | 6 | 0 | 0 | 1 | 5dc2971df 2026-08-25 | 2026-08-25 20:04
mag/novelty_lens.py | 170 | 4 | 0 | 0 | 4 | 052732ebf 2026-08-14 | 2026-08-11 09:27
mag/ocean_model_mind.py | 309 | 6 | 0 | 0 | 1 | cb26bc2cd 2026-08-25 | 2026-08-22 10:12
mag/ocean_persona.py | 169 | 5 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-11 11:43
mag/off_hours.py | 337 | 9 | 0 | 1 | 3 | d575bc168 2026-09-14 | 2026-08-30 20:59
mag/offerings.py | 233 | 2 | 0 | 0 | 2 | 383fed94f 2026-09-27 | 2026-09-26 12:53
mag/offline.py | 231 | 5 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-09 23:46
mag/offpeak.py | 160 | 5 | 0 | 1 | 21 | cb26bc2cd 2026-08-25 | 2026-08-24 09:19
mag/oh_fuck.py | 114 | 2 | 0 | 0 | 1 | de29d49ea 2026-08-09 | 2026-08-09 13:22
mag/ollama_policy.py | 120 | 4 | 0 | 1 | 7 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/one_sizer.py | 128 | 4 | 0 | 0 | 8 | 052732ebf 2026-08-14 | 2026-08-09 21:39
mag/ontology_compiler/extract.py | 48 | 4 | 0 | 0 | 0 | 7a3e22b30 2026-09-08 | 2026-09-08 09:41
mag/openclaw_catalog.py | 252 | 4 | 0 | 1 | 0 | d575bc168 2026-09-14 | 2026-08-29 15:55
mag/openclaw_patches.py | 251 | 5 | 0 | 1 | 1 | d575bc168 2026-09-14 | 2026-08-31 07:29
mag/operating_protocol.py | 113 | 2 | 0 | 3 | 5 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/operator_inbox.py | 460 | 8 | 0 | 11 | 34 | 052732ebf 2026-08-14 | 2026-08-11 08:41
mag/operator_mode.py | 182 | 5 | 0 | 2 | 13 | d575bc168 2026-09-14 | 2026-09-02 04:15
mag/operator_os.py | 294 | 2 | 0 | 0 | 3 | 799ddb6fe 2026-08-19 | 2026-08-14 20:30
mag/ops_graph.py | 445 | 5 | 0 | 0 | 2 | 60e18c524 2026-08-08 | 2026-08-08 10:54
mag/oracle.py | 188 | 6 | 0 | 1 | 0 | 052732ebf 2026-08-14 | 2026-08-13 09:03
mag/orchestrator.py | 2056 | 26 | 0 | 20 | 101 | 383fed94f 2026-09-27 | 2026-09-26 17:14
mag/organ_map.py | 701 | 4 | 0 | 1 | 4 | d575bc168 2026-09-14 | 2026-09-12 23:01
mag/orphan_audit.py | 214 | 2 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-08-31 07:35
mag/orphan_sense.py | 203 | 3 | 0 | 0 | 5 | 799ddb6fe 2026-08-19 | 2026-08-15 09:54
mag/orphan_timer.py | 267 | 6 | 0 | 0 | 7 | 60e18c524 2026-08-08 | 2026-08-08 10:24
mag/os_v2.py | 165 | 2 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-08-28 19:44
mag/osculating.py | 251 | 5 | 0 | 1 | 1 | 052732ebf 2026-08-14 | 2026-08-13 08:16
mag/overseer.py | 182 | 2 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-07 02:16
mag/ox_alpha_steal.py | 194 | 3 | 0 | 0 | 0 | cb26bc2cd 2026-08-25 | 2026-08-22 10:12
mag/ox_availability.py | 154 | 3 | 0 | 0 | 4 | cb26bc2cd 2026-08-25 | 2026-08-23 20:44
mag/ox_burn.py | 121 | 1 | 0 | 0 | 0 | cb26bc2cd 2026-08-25 | 2026-08-22 20:08
mag/ox_escalate.py | 138 | 1 | 0 | 0 | 0 | cb26bc2cd 2026-08-25 | 2026-08-22 12:33
mag/ox_fold.py | 257 | 4 | 0 | 0 | 2 | cb26bc2cd 2026-08-25 | 2026-08-23 08:43
mag/ox_gap.py | 175 | 3 | 0 | 0 | 1 | cb26bc2cd 2026-08-25 | 2026-08-22 20:58
mag/ox_megaburn.py | 560 | 2 | 0 | 0 | 0 | cb26bc2cd 2026-08-25 | 2026-08-22 20:58
mag/ox_megaburn2.py | 323 | 2 | 0 | 0 | 0 | cb26bc2cd 2026-08-25 | 2026-08-23 03:03
mag/ox_megaburn3.py | 247 | 3 | 0 | 0 | 4 | cb26bc2cd 2026-08-25 | 2026-08-23 14:26
mag/ox_novelty_digest.py | 86 | 1 | 0 | 0 | 0 | cb26bc2cd 2026-08-25 | 2026-08-23 16:16
mag/ox_novelty_index.py | 163 | 1 | 0 | 0 | 2 | cb26bc2cd 2026-08-25 | 2026-08-23 16:16
mag/ox_percolate.py | 198 | 4 | 0 | 0 | 2 | cb26bc2cd 2026-08-25 | 2026-08-24 08:53
mag/ox_probe.py | 232 | 3 | 0 | 0 | 0 | cb26bc2cd 2026-08-25 | 2026-08-23 08:11
mag/ox_resident.py | 501 | 9 | 0 | 0 | 9 | cb26bc2cd 2026-08-25 | 2026-08-24 15:58
mag/ox_scout.py | 178 | 4 | 0 | 0 | 1 | cb26bc2cd 2026-08-25 | 2026-08-23 16:16
mag/ox_seat.py | 182 | 2 | 0 | 0 | 16 | cb26bc2cd 2026-08-25 | 2026-08-24 13:59
mag/ox_swarm.py | 298 | 6 | 0 | 0 | 0 | cb26bc2cd 2026-08-25 | 2026-08-23 18:08
mag/p20_pending_wave.py | 141 | 3 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-12 08:16
mag/partner_puppet.py | 116 | 5 | 0 | 0 | 2 | de29d49ea 2026-08-09 | 2026-08-09 20:39
mag/party_subchain.py | 358 | 7 | 0 | 5 | 24 | 799ddb6fe 2026-08-19 | 2026-08-14 10:09
mag/paste_pipeline.py | 270 | 2 | 0 | 1 | 1 | 383fed94f 2026-09-27 | 2026-09-26 18:56
mag/pattern_mine.py | 152 | 2 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-10 00:35
mag/pdf_layout.py | 537 | 1 | 0 | 0 | 1 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/peer_handoff.py | 259 | 5 | 0 | 1 | 12 | a5dd96176 2026-09-25 | 2026-09-21 21:53
mag/percolator.py | 384 | 9 | 0 | 2 | 30 | d575bc168 2026-09-14 | 2026-09-09 14:49
mag/percolator_heal_test.py | 156 | 4 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-07 01:08
mag/perplexity_research.py | 323 | 6 | 0 | 1 | 0 | a5dd96176 2026-09-25 | 2026-09-25 20:33
mag/persistent_agent.py | 444 | 4 | 2 | 0 | 0 | 60e18c524 2026-08-08 | 2026-08-08 14:57
mag/persona_direction.py | 183 | 3 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-11 09:58
mag/persona_key.py | 207 | 6 | 0 | 0 | 0 | cb26bc2cd 2026-08-25 | 2026-08-24 13:18
mag/persona_recall.py | 155 | 4 | 0 | 0 | 4 | 052732ebf 2026-08-14 | 2026-08-11 11:28
mag/personality_substrate.py | 228 | 2 | 1 | 0 | 1 | 60e18c524 2026-08-08 | 2026-08-08 15:59
mag/perturbation_battery.py | 550 | 7 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-06 02:04
mag/phone_door.py | 76 | 3 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-07 02:13
mag/phone_relay.py | 249 | 2 | 0 | 0 | 5 | 662c25a9b 2026-09-25 | 2026-09-25 06:38
mag/physics_steal.py | 157 | 5 | 0 | 1 | 0 | 052732ebf 2026-08-14 | 2026-08-12 16:58
mag/pigeonhole.py | 336 | 14 | 0 | 4 | 15 | 36914e134 2026-08-07 | 2026-08-07 12:32
mag/pin_audit.py | 109 | 1 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-05 13:35
mag/plan.py | 203 | 8 | 0 | 0 | 6 | eb07ad62e 2026-08-04 | 2026-08-05 07:36
mag/plan_mode.py | 40 | 1 | 0 | 0 | 0 | cb26bc2cd 2026-08-25 | 2026-08-25 09:32
mag/platform_kill.py | 161 | 2 | 0 | 1 | 4 | 383fed94f 2026-09-27 | 2026-09-26 12:54
mag/play_benchmark.py | 391 | 4 | 0 | 0 | 1 | e96fd62a4 2026-08-07 | 2026-08-06 22:34
mag/poc_stage2.py | 141 | 3 | 0 | 0 | 0 | cb26bc2cd 2026-08-25 | 2026-08-24 11:57
mag/policy.py | 84 | 2 | 0 | 0 | 6 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/policy_engine.py | 496 | 17 | 0 | 1 | 6 | 2b84b8cce 2026-09-16 | 2026-09-16 10:31
mag/ponytail_audit.py | 246 | 2 | 0 | 2 | 3 | 052732ebf 2026-08-14 | 2026-08-10 14:51
mag/popup_insights.py | 158 | 2 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-12 05:53
mag/portal.py | 199 | 5 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-12 07:14
mag/power.py | 735 | 8 | 0 | 2 | 8 | 383fed94f 2026-09-27 | 2026-09-26 12:54
mag/preferences.py | 141 | 12 | 0 | 3 | 22 | de29d49ea 2026-08-09 | 2026-08-09 08:05
mag/prefix_prover.py | 192 | 4 | 0 | 0 | 2 | 6ac176ce8 2026-08-25 | 2026-08-25 17:55
mag/preflight.py | 178 | 2 | 1 | 0 | 1 | de7bb85fe 2026-08-09 | 2026-08-08 23:07
mag/preload_selector.py | 456 | 15 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-07 08:02
mag/press_digest.py | 224 | 7 | 0 | 0 | 3 | de29d49ea 2026-08-09 | 2026-08-09 13:19
mag/primer.py | 179 | 7 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-12 10:20
mag/pro_library.py | 392 | 9 | 0 | 3 | 11 | 052732ebf 2026-08-14 | 2026-08-11 07:51
mag/probe_route.py | 194 | 4 | 0 | 0 | 6 | 46711f479 2026-09-24 | 2026-09-24 22:28
mag/problem_knot.py | 239 | 6 | 0 | 0 | 3 | 052732ebf 2026-08-14 | 2026-08-10 18:21
mag/process_reaper.py | 222 | 2 | 0 | 0 | 14 | 02bcd49be 2026-09-19 | 2026-09-19 09:14
mag/process_supervisor.py | 499 | 8 | 0 | 1 | 13 | 383fed94f 2026-09-27 | 2026-09-26 09:53
mag/prompt_archaeology.py | 498 | 4 | 2 | 0 | 1 | de7bb85fe 2026-08-09 | 2026-08-08 23:21
mag/prompt_lance.py | 566 | 6 | 0 | 1 | 1 | 0d9dda89e 2026-09-27 | 2026-09-27 18:25
mag/proof.py | 169 | 6 | 0 | 0 | 5 | cb26bc2cd 2026-08-25 | 2026-08-24 10:17
mag/prose_census.py | 155 | 1 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-28 14:32
mag/prospect_sim.py | 381 | 10 | 0 | 0 | 4 | de29d49ea 2026-08-09 | 2026-08-09 15:26
mag/provenance_gate.py | 233 | 0 | 5 | 0 | 0 | cb26bc2cd 2026-08-25 | 2026-08-22 14:30
mag/quest_roshomon.py | 296 | 7 | 0 | 1 | 0 | 799ddb6fe 2026-08-19 | 2026-08-14 06:45
mag/queue_analysis.py | 264 | 7 | 0 | 0 | 1 | 799ddb6fe 2026-08-19 | 2026-08-15 09:54
mag/queue_gate.py | 388 | 7 | 0 | 1 | 4 | 790145ab1 2026-09-26 | 2026-09-26 01:50
mag/queue_learn.py | 215 | 4 | 0 | 0 | 2 | de29d49ea 2026-08-09 | 2026-08-09 08:46
mag/queue_ops.py | 187 | 6 | 0 | 0 | 3 | de29d49ea 2026-08-09 | 2026-08-09 08:45
mag/queue_rightsize.py | 246 | 4 | 0 | 0 | 4 | 799ddb6fe 2026-08-19 | 2026-08-14 08:25
mag/quorum_window.py | 484 | 7 | 0 | 2 | 1 | 383fed94f 2026-09-27 | 2026-09-26 19:10
mag/race_harness.py | 182 | 5 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-03 21:19
mag/ractor_corpus.py | 474 | 3 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-06 18:24
mag/ractor_vessels.py | 141 | 3 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-09 17:39
mag/rails.py | 72 | 4 | 0 | 0 | 2 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/ram_cache.py | 131 | 5 | 0 | 0 | 2 | cb26bc2cd 2026-08-25 | 2026-08-25 12:25
mag/read_archive.py | 126 | 3 | 0 | 0 | 5 | d575bc168 2026-09-14 | 2026-08-30 21:48
mag/read_receipts.py | 125 | 1 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-05 20:23
mag/readout_controller.py | 127 | 5 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-10 18:41
mag/real_swarm.py | 243 | 5 | 0 | 0 | 2 | cb26bc2cd 2026-08-25 | 2026-08-23 21:35
mag/reasoning_intake.py | 422 | 3 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-07 10:11
mag/reconstruct.py | 168 | 6 | 0 | 1 | 1 | 052732ebf 2026-08-14 | 2026-08-12 16:28
mag/records.py | 261 | 5 | 0 | 0 | 5 | d575bc168 2026-09-14 | 2026-08-30 13:55
mag/recreation_rib.py | 220 | 3 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-10 19:32
mag/recurrence_gate.py | 240 | 3 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-12 08:50
mag/refeed_guard.py | 171 | 3 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-05 19:15
mag/refine_chain.py | 747 | 9 | 0 | 0 | 5 | 052732ebf 2026-08-14 | 2026-08-12 19:08
mag/refine_loop.py | 695 | 7 | 1 | 0 | 0 | de29d49ea 2026-08-09 | 2026-08-09 11:17
mag/registry.py | 490 | 20 | 0 | 1 | 21 | d575bc168 2026-09-14 | 2026-08-30 13:55
mag/rel_mem_eval.py | 248 | 4 | 0 | 0 | 2 | d575bc168 2026-09-14 | 2026-08-26 00:07
mag/release_registry.py | 297 | 10 | 0 | 4 | 3 | 383fed94f 2026-09-27 | 2026-09-26 16:18
mag/remedy.py | 145 | 5 | 0 | 1 | 4 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/remote_control.py | 137 | 5 | 0 | 1 | 4 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/render_brief.py | 45 | 1 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-06 17:33
mag/renderman.py | 847 | 3 | 10 | 0 | 1 | 799ddb6fe 2026-08-19 | 2026-08-16 06:43
mag/renderman_ask.py | 208 | 6 | 0 | 0 | 4 | de29d49ea 2026-08-09 | 2026-08-09 09:12
mag/repo_readiness.py | 77 | 1 | 0 | 2 | 3 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/republic.py | 855 | 16 | 6 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-06 17:51
mag/republic_ambassador.py | 218 | 7 | 0 | 1 | 2 | 052732ebf 2026-08-14 | 2026-08-12 16:40
mag/republic_feed.py | 161 | 2 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-11 11:28
mag/republic_governance.py | 380 | 15 | 0 | 0 | 3 | 799ddb6fe 2026-08-19 | 2026-08-15 19:12
mag/republic_loop.py | 504 | 2 | 0 | 0 | 3 | d575bc168 2026-09-14 | 2026-08-30 16:38
mag/republic_os.py | 358 | 11 | 0 | 1 | 6 | cb26bc2cd 2026-08-25 | 2026-08-23 23:20
mag/republic_wave.py | 196 | 5 | 0 | 2 | 5 | 052732ebf 2026-08-14 | 2026-08-12 16:11
mag/research_class.py | 255 | 7 | 0 | 0 | 5 | 052732ebf 2026-08-14 | 2026-08-11 08:58
mag/research_director.py | 811 | 7 | 3 | 0 | 1 | 60e18c524 2026-08-08 | 2026-08-08 05:51
mag/research_fanout.py | 476 | 8 | 0 | 1 | 5 | 383fed94f 2026-09-27 | 2026-09-26 21:03
mag/research_fold.py | 168 | 4 | 0 | 1 | 5 | de7bb85fe 2026-08-09 | 2026-08-08 23:20
mag/research_lens.py | 407 | 7 | 0 | 0 | 12 | de29d49ea 2026-08-09 | 2026-08-09 09:20
mag/research_pack.py | 781 | 6 | 0 | 1 | 8 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/research_worker.py | 116 | 2 | 0 | 0 | 4 | d575bc168 2026-09-14 | 2026-08-31 00:11
mag/resonance.py | 193 | 4 | 0 | 1 | 5 | f31c0e926 2026-08-05 | 2026-08-06 18:28
mag/resource_governor.py | 155 | 2 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-11 13:09
mag/resume_order.py | 261 | 5 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-10 20:23
mag/rib_action.py | 201 | 6 | 1 | 0 | 5 | 052732ebf 2026-08-14 | 2026-08-10 16:57
mag/rib_bus.py | 244 | 6 | 0 | 1 | 50 | 052732ebf 2026-08-14 | 2026-08-12 10:20
mag/rib_cache.py | 142 | 3 | 0 | 0 | 27 | d575bc168 2026-09-14 | 2026-09-05 00:11
mag/rib_gif.py | 120 | 3 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-11 11:28
mag/rib_k8s.py | 194 | 4 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-10 17:36
mag/rib_os.py | 137 | 2 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-11 12:47
mag/rib_renderer.py | 98 | 4 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-11 06:19
mag/rib_store.py | 77 | 3 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-08-28 10:58
mag/rib_struct.py | 178 | 7 | 1 | 0 | 2 | 052732ebf 2026-08-14 | 2026-08-09 22:48
mag/riddle_direction.py | 141 | 3 | 0 | 0 | 0 | cb26bc2cd 2026-08-25 | 2026-08-24 12:23
mag/riddler.py | 520 | 5 | 3 | 2 | 9 | 052732ebf 2026-08-14 | 2026-08-10 09:16
mag/riddler_campaign.py | 634 | 3 | 4 | 0 | 1 | de7bb85fe 2026-08-09 | 2026-08-08 23:36
mag/riddler_coherence.py | 164 | 4 | 0 | 0 | 0 | 799ddb6fe 2026-08-19 | 2026-08-15 21:13
mag/riddler_map.py | 299 | 8 | 0 | 1 | 0 | d575bc168 2026-09-14 | 2026-08-28 21:13
mag/riddler_sanitize.py | 225 | 3 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-08-30 21:13
mag/riddler_tap.py | 215 | 9 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-12 19:29
mag/riddler_trajectory.py | 152 | 6 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-08 07:29
mag/riddler_transport.py | 461 | 4 | 1 | 0 | 5 | 052732ebf 2026-08-14 | 2026-08-10 11:05
mag/right_size_skills.py | 159 | 3 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-08-30 15:30
mag/rightsize_all.py | 162 | 4 | 0 | 0 | 4 | de29d49ea 2026-08-09 | 2026-08-09 13:55
mag/rightsize_api.py | 145 | 4 | 0 | 0 | 1 | de29d49ea 2026-08-09 | 2026-08-09 19:53
mag/rightsize_wave.py | 139 | 4 | 0 | 0 | 0 | 799ddb6fe 2026-08-19 | 2026-08-15 09:17
mag/roadmap_runner.py | 303 | 5 | 0 | 1 | 2 | 343781ff7 2026-08-06 | 2026-08-06 18:28
mag/room_state.py | 292 | 10 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-06 00:10
mag/roshomon.py | 364 | 9 | 0 | 0 | 9 | 052732ebf 2026-08-14 | 2026-08-10 16:46
mag/roshomon_mine.py | 165 | 4 | 0 | 1 | 2 | 052732ebf 2026-08-14 | 2026-08-12 15:57
mag/rotation_harness.py | 199 | 3 | 0 | 1 | 1 | 383fed94f 2026-09-27 | 2026-09-26 19:10
mag/route.py | 170 | 1 | 0 | 2 | 15 | 36914e134 2026-08-07 | 2026-08-07 12:32
mag/route_trace.py | 175 | 5 | 0 | 1 | 2 | 052732ebf 2026-08-14 | 2026-08-12 16:02
mag/router.py | 1045 | 5 | 0 | 6 | 20 | 6f150864a 2026-09-28 | 2026-09-28 12:56
mag/routing_concert.py | 311 | 5 | 0 | 1 | 4 | 36914e134 2026-08-07 | 2026-08-07 13:12
mag/run_trail.py | 1020 | 25 | 0 | 3 | 12 | 1c156e2fa 2026-08-06 | 2026-09-28 01:02
mag/run_worth.py | 555 | 12 | 0 | 1 | 4 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/runtime.py | 204 | 4 | 0 | 1 | 9 | d575bc168 2026-09-14 | 2026-08-28 19:44
mag/runtime_policy.py | 55 | 1 | 0 | 1 | 3 | 383fed94f 2026-09-27 | 2026-09-26 09:05
mag/saelis_room.py | 349 | 4 | 0 | 0 | 0 | 383fed94f 2026-09-27 | 2026-09-26 12:54
mag/saelis_seat.py | 163 | 4 | 0 | 0 | 3 | 799ddb6fe 2026-08-19 | 2026-08-17 21:29
mag/saelis_world_brief.py | 107 | 2 | 0 | 0 | 0 | 799ddb6fe 2026-08-19 | 2026-08-18 08:05
mag/salon_50.py | 210 | 3 | 0 | 0 | 0 | cf99e64fb 2026-09-15 | 2026-09-15 22:50
mag/salon_openclaw.py | 308 | 4 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-08-30 22:22
mag/scale_salon.py | 264 | 2 | 0 | 1 | 0 | 383fed94f 2026-09-27 | 2026-09-26 19:36
mag/schema_registry.py | 305 | 9 | 0 | 0 | 3 | 052732ebf 2026-08-14 | 2026-08-10 12:13
mag/scifi_fantasy_steal.py | 173 | 5 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-11 10:23
mag/scribe.py | 131 | 4 | 0 | 0 | 3 | de29d49ea 2026-08-09 | 2026-08-09 16:29
mag/scrum.py | 272 | 6 | 0 | 0 | 7 | cb26bc2cd 2026-08-25 | 2026-08-24 07:28
mag/seal.py | 214 | 4 | 0 | 0 | 1 | cb26bc2cd 2026-08-25 | 2026-08-24 12:29
mag/seat_availability.py | 176 | 3 | 0 | 0 | 2 | cb26bc2cd 2026-08-25 | 2026-08-23 20:49
mag/seat_corpus.py | 304 | 3 | 0 | 2 | 1 | 383fed94f 2026-09-27 | 2026-09-26 19:36
mag/seat_dispatch.py | 319 | 3 | 0 | 0 | 3 | d575bc168 2026-09-14 | 2026-09-03 22:59
mag/seat_feed.py | 157 | 1 | 0 | 2 | 3 | eb07ad62e 2026-08-04 | 2026-08-04 18:48
mag/seat_fork.py | 69 | 1 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-12 18:01
mag/seat_guard.py | 389 | 2 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-09 21:35
mag/seat_hunter.py | 702 | 14 | 0 | 0 | 4 | cb26bc2cd 2026-08-25 | 2026-08-23 20:33
mag/seat_probe.py | 112 | 2 | 0 | 0 | 0 | cb26bc2cd 2026-08-25 | 2026-08-24 15:35
mag/seat_registry.py | 289 | 7 | 0 | 2 | 19 | 383fed94f 2026-09-27 | 2026-09-26 17:14
mag/seat_steer.py | 258 | 5 | 0 | 2 | 8 | 799ddb6fe 2026-08-19 | 2026-08-14 06:42
mag/seats.py | 392 | 2 | 0 | 1 | 4 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/seed_chain.py | 142 | 4 | 0 | 0 | 2 | de29d49ea 2026-08-09 | 2026-08-09 16:32
mag/seed_percolator.py | 133 | 4 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-08-27 09:38
mag/seed_registry.py | 518 | 6 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-07 09:27
mag/seeds.py | 166 | 5 | 0 | 0 | 2 | cb26bc2cd 2026-08-25 | 2026-08-24 10:52
mag/self_advance.py | 157 | 4 | 0 | 0 | 2 | de29d49ea 2026-08-09 | 2026-08-09 16:29
mag/self_audit.py | 328 | 6 | 0 | 0 | 3 | d575bc168 2026-09-14 | 2026-08-30 12:55
mag/self_drive.py | 230 | 6 | 0 | 0 | 9 | de29d49ea 2026-08-09 | 2026-08-09 11:59
mag/self_drive_cadence.py | 153 | 1 | 0 | 0 | 1 | de7bb85fe 2026-08-09 | 2026-08-09 01:16
mag/self_hologram.py | 149 | 1 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-06 10:46
mag/self_loop.py | 203 | 5 | 0 | 0 | 6 | 052732ebf 2026-08-14 | 2026-08-11 10:17
mag/self_steal.py | 412 | 4 | 0 | 1 | 7 | d575bc168 2026-09-14 | 2026-08-30 23:32
mag/self_test.py | 195 | 7 | 0 | 0 | 1 | cb26bc2cd 2026-08-25 | 2026-08-23 08:43
mag/self_train_data.py | 161 | 3 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-12 07:54
mag/self_vision.py | 207 | 6 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-12 02:14
mag/sense.py | 77 | 1 | 0 | 1 | 4 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/sentinel.py | 153 | 4 | 0 | 0 | 3 | 052732ebf 2026-08-14 | 2026-08-10 06:36
mag/session_bridge.py | 355 | 15 | 0 | 0 | 3 | d575bc168 2026-09-14 | 2026-08-31 00:37
mag/session_card.py | 288 | 6 | 0 | 0 | 6 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/session_dossier.py | 665 | 4 | 0 | 0 | 1 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/session_freeze.py | 313 | 3 | 0 | 1 | 3 | 60e18c524 2026-08-08 | 2026-08-08 09:43
mag/session_koan.py | 322 | 4 | 1 | 0 | 0 | de7bb85fe 2026-08-09 | 2026-08-08 22:03
mag/session_maze.py | 287 | 5 | 0 | 0 | 12 | 799ddb6fe 2026-08-19 | 2026-08-16 17:43
mag/session_overseer.py | 310 | 6 | 0 | 0 | 1 | 60e18c524 2026-08-08 | 2026-08-08 07:57
mag/session_rib.py | 269 | 8 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-01 21:02
mag/session_ritual.py | 471 | 3 | 1 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-12 16:02
mag/session_route.py | 191 | 7 | 0 | 1 | 5 | 799ddb6fe 2026-08-19 | 2026-08-18 07:43
mag/session_state_brief.py | 382 | 4 | 0 | 1 | 5 | 383fed94f 2026-09-27 | 2026-09-26 14:00
mag/shader_bus.py | 179 | 6 | 0 | 0 | 5 | 052732ebf 2026-08-14 | 2026-08-10 12:30
mag/shader_rib.py | 217 | 5 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-11 10:30
mag/shadow_graph.py | 198 | 5 | 0 | 0 | 5 | 052732ebf 2026-08-14 | 2026-08-11 09:27
mag/shadow_quest.py | 160 | 4 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-11 23:20
mag/shadow_slab.py | 121 | 4 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-05 23:38
mag/shadow_work.py | 148 | 5 | 0 | 0 | 5 | 052732ebf 2026-08-14 | 2026-08-10 12:53
mag/shape_map.py | 281 | 8 | 0 | 0 | 3 | f1bceeb3a 2026-09-27 | 2026-09-27 16:58
mag/shape_seed.py | 233 | 7 | 0 | 1 | 2 | 052732ebf 2026-08-14 | 2026-08-12 17:04
mag/shared_surface.py | 426 | 2 | 0 | 5 | 7 | 383fed94f 2026-09-27 | 2026-09-26 19:05
mag/shelf_pdf.py | 99 | 2 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-06 18:19
mag/signal_flare.py | 543 | 5 | 3 | 0 | 1 | 482e0a3c8 2026-08-08 | 2026-08-08 19:11
mag/signals.py | 164 | 10 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-09 22:48
mag/single_feed.py | 82 | 1 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-04 22:15
mag/skill_drop.py | 197 | 7 | 0 | 1 | 3 | 60e18c524 2026-08-08 | 2026-08-07 18:15
mag/skill_ledger.py | 345 | 9 | 0 | 7 | 30 | 383fed94f 2026-09-27 | 2026-09-26 16:44
mag/skill_lifecycle.py | 420 | 11 | 0 | 1 | 1 | a5dd96176 2026-09-25 | 2026-09-25 20:42
mag/skill_pipeline.py | 358 | 4 | 0 | 1 | 7 | 052732ebf 2026-08-14 | 2026-08-11 05:26
mag/skill_seat.py | 112 | 5 | 0 | 1 | 4 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/skills_pack.py | 73 | 2 | 0 | 0 | 4 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/social_hone.py | 154 | 4 | 0 | 1 | 0 | 052732ebf 2026-08-14 | 2026-08-13 09:23
mag/socratic.py | 159 | 2 | 0 | 0 | 2 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/socratic_research.py | 142 | 4 | 0 | 1 | 2 | 052732ebf 2026-08-14 | 2026-08-12 15:57
mag/socratic_tree.py | 159 | 2 | 0 | 0 | 0 | de7bb85fe 2026-08-09 | 2026-08-09 00:05
mag/solved_surface.py | 117 | 2 | 0 | 1 | 2 | 052732ebf 2026-08-14 | 2026-08-10 08:41
mag/source_trace.py | 390 | 5 | 0 | 1 | 3 | 383fed94f 2026-09-27 | 2026-09-26 13:28
mag/sovereign_dashboard.py | 244 | 2 | 0 | 1 | 2 | de7bb85fe 2026-08-09 | 2026-08-09 00:08
mag/sovereign_handshake.py | 245 | 7 | 0 | 1 | 2 | 052732ebf 2026-08-14 | 2026-08-12 17:02
mag/space_ear.py | 147 | 5 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-09 18:19
mag/spawn_manifest.py | 342 | 5 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-07 01:13
mag/spec_gate.py | 200 | 8 | 0 | 2 | 5 | de7bb85fe 2026-08-09 | 2026-08-08 23:37
mag/spider.py | 269 | 1 | 0 | 1 | 7 | 4706d5a04 2026-09-28 | 2026-09-28 14:05
mag/spine_exercise.py | 151 | 1 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-06 18:44
mag/spore_seed.py | 195 | 3 | 0 | 1 | 0 | b1d714b02 2026-09-25 | 2026-09-25 08:26
mag/stack.py | 552 | 5 | 0 | 2 | 2 | e96fd62a4 2026-08-07 | 2026-08-06 18:55
mag/stale_sweep.py | 97 | 1 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-05 21:38
mag/standing.py | 312 | 5 | 0 | 0 | 0 | cb26bc2cd 2026-08-25 | 2026-08-24 13:59
mag/standing_wave.py | 281 | 8 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-13 04:04
mag/state_brief.py | 259 | 4 | 0 | 0 | 1 | de7bb85fe 2026-08-09 | 2026-08-08 21:11
mag/state_quantizer.py | 484 | 6 | 1 | 0 | 3 | 482e0a3c8 2026-08-08 | 2026-08-08 19:11
mag/state_snapshot.py | 152 | 3 | 0 | 1 | 9 | 60e18c524 2026-08-08 | 2026-08-07 18:30
mag/stateless_research.py | 281 | 5 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-11 06:19
mag/steal_first.py | 445 | 5 | 3 | 0 | 2 | 482e0a3c8 2026-08-08 | 2026-08-08 19:11
mag/steal_lens.py | 118 | 3 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-11 10:17
mag/steal_pack.py | 184 | 4 | 0 | 0 | 10 | 052732ebf 2026-08-14 | 2026-08-11 09:40
mag/steal_protocol_probe.py | 80 | 2 | 0 | 0 | 1 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/steal_steer.py | 187 | 4 | 0 | 0 | 6 | 052732ebf 2026-08-14 | 2026-08-09 22:48
mag/steal_tools.py | 192 | 8 | 0 | 0 | 3 | 799ddb6fe 2026-08-19 | 2026-08-15 07:13
mag/steer.py | 185 | 6 | 0 | 1 | 14 | 799ddb6fe 2026-08-19 | 2026-08-14 07:55
mag/steer_bridge.py | 151 | 4 | 0 | 1 | 1 | 60e18c524 2026-08-08 | 2026-08-07 15:18
mag/steer_bus.py | 75 | 1 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-02 09:30
mag/steer_engine.py | 174 | 5 | 0 | 0 | 4 | 052732ebf 2026-08-14 | 2026-08-12 09:57
mag/steer_receipt_wire.py | 85 | 2 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-03 17:06
mag/steer_router.py | 208 | 8 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-10 18:41
mag/steer_swarm.py | 190 | 4 | 0 | 0 | 3 | 052732ebf 2026-08-14 | 2026-08-12 01:36
mag/steer_telemetry.py | 306 | 7 | 0 | 0 | 4 | 052732ebf 2026-08-14 | 2026-08-11 07:51
mag/steiniger_lens.py | 198 | 2 | 0 | 0 | 1 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/steward.py | 412 | 9 | 0 | 3 | 4 | eafda6b29 2026-08-06 | 2026-08-06 18:28
mag/story.py | 493 | 1 | 0 | 1 | 2 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/subscriptions.py | 183 | 1 | 0 | 1 | 1 | 383fed94f 2026-09-27 | 2026-09-26 19:36
mag/subswarm_health.py | 148 | 5 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-10 19:13
mag/suno_zeitgeist.py | 124 | 4 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-07 17:30
mag/supervisor.py | 208 | 6 | 0 | 0 | 4 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/surface_adapters.py | 214 | 5 | 0 | 1 | 1 | 052732ebf 2026-08-14 | 2026-08-13 08:37
mag/surface_audit.py | 139 | 2 | 0 | 1 | 1 | d575bc168 2026-09-14 | 2026-08-30 13:24
mag/surface_instruction.py | 241 | 7 | 0 | 1 | 2 | 052732ebf 2026-08-14 | 2026-08-12 17:16
mag/surface_render.py | 826 | 22 | 0 | 0 | 5 | cb26bc2cd 2026-08-25 | 2026-08-24 07:26
mag/surface_steal.py | 127 | 5 | 0 | 1 | 1 | d575bc168 2026-09-14 | 2026-08-30 22:27
mag/surrogate.py | 386 | 3 | 3 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-10 11:05
mag/swarm_capacity.py | 153 | 5 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-10 17:36
mag/swarm_control.py | 138 | 5 | 0 | 0 | 3 | 052732ebf 2026-08-14 | 2026-08-12 06:15
mag/swarm_cycle.py | 229 | 2 | 0 | 0 | 2 | 5dff72ac3 2026-09-28 | 2026-09-28 12:46
mag/swarm_economics.py | 150 | 5 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-11 11:33
mag/swarm_emerge.py | 171 | 4 | 0 | 0 | 2 | 052732ebf 2026-08-14 | 2026-08-11 09:27
mag/swarm_grok_watch.py | 162 | 5 | 0 | 0 | 1 | a5dd96176 2026-09-25 | 2026-09-22 08:09
mag/swarm_health.py | 257 | 6 | 0 | 0 | 9 | d575bc168 2026-09-14 | 2026-08-30 16:19
mag/swarm_local_drain.py | 248 | 5 | 0 | 1 | 5 | d575bc168 2026-09-14 | 2026-08-30 12:53
mag/swarm_map.py | 172 | 5 | 0 | 0 | 3 | 052732ebf 2026-08-14 | 2026-08-12 10:30
mag/swarm_quests.py | 260 | 5 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-07 01:19
mag/swarm_render.py | 181 | 5 | 0 | 0 | 3 | 052732ebf 2026-08-14 | 2026-08-11 07:51
mag/swarm_rightsize.py | 241 | 3 | 0 | 0 | 5 | 052732ebf 2026-08-14 | 2026-08-11 12:47
mag/swarm_run.py | 155 | 3 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-10 18:15
mag/swarm_self.py | 294 | 6 | 0 | 0 | 3 | 052732ebf 2026-08-14 | 2026-08-12 07:14
mag/swarm_snapshot.py | 298 | 7 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-05 12:31
mag/swarm_surface.py | 109 | 3 | 0 | 6 | 66 | d575bc168 2026-09-14 | 2026-08-30 12:51
mag/swarm_test.py | 247 | 5 | 0 | 0 | 2 | de29d49ea 2026-08-09 | 2026-08-09 18:07
mag/swarm_tools.py | 455 | 13 | 0 | 0 | 9 | d575bc168 2026-09-14 | 2026-09-02 09:29
mag/swarm_worker.py | 701 | 7 | 0 | 4 | 33 | 383fed94f 2026-09-27 | 2026-09-26 19:35
mag/switchboard.py | 828 | 13 | 2 | 3 | 14 | d575bc168 2026-09-14 | 2026-08-30 14:49
mag/switchboard_v2.py | 925 | 22 | 0 | 1 | 6 | 2b84b8cce 2026-09-16 | 2026-09-16 10:29
mag/system_map.py | 185 | 1 | 0 | 0 | 4 | 36914e134 2026-08-07 | 2026-08-07 08:27
mag/system_telemetry.py | 174 | 7 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-11 13:09
mag/table_turn_cli.py | 12 | 1 | 0 | 0 | 1 | 799ddb6fe 2026-08-19 | 2026-08-16 08:50
mag/table_view_cache.py | 36 | 3 | 0 | 0 | 2 | 799ddb6fe 2026-08-19 | 2026-08-15 22:17
mag/tactical_framework.py | 152 | 6 | 0 | 1 | 1 | 052732ebf 2026-08-14 | 2026-08-12 16:58
mag/tandem_key_test.py | 77 | 1 | 0 | 0 | 0 | cb26bc2cd 2026-08-25 | 2026-08-23 20:33
mag/tangent.py | 346 | 6 | 0 | 0 | 2 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/tapestry.py | 751 | 2 | 0 | 1 | 4 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/tapestry_visual.py | 189 | 5 | 0 | 1 | 1 | 7d4939fc9 2026-08-05 | 2026-08-06 18:28
mag/task_router.py | 281 | 4 | 0 | 0 | 5 | de7bb85fe 2026-08-09 | 2026-08-08 22:51
mag/tavern_chat.py | 143 | 4 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-07 21:07
mag/tavern_summon_guests.py | 51 | 1 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-08 22:42
mag/team_knot.py | 367 | 6 | 0 | 0 | 1 | cb26bc2cd 2026-08-25 | 2026-08-24 09:19
mag/telegram_desk.py | 180 | 3 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-09 18:11
mag/temperature_stack.py | 702 | 9 | 4 | 3 | 10 | 383fed94f 2026-09-27 | 2026-09-26 17:04
mag/template_invariant.py | 227 | 6 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-10 17:36
mag/territory_solver.py | 300 | 3 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-11 22:15
mag/test_dummy.py | 79 | 4 | 0 | 0 | 3 | de29d49ea 2026-08-09 | 2026-08-09 16:29
mag/test_runner.py | 192 | 3 | 0 | 0 | 4 | cb26bc2cd 2026-08-25 | 2026-08-23 23:20
mag/tests/test_identity_schema_portability.py | 158 | 3 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-12 21:39
mag/tests/verify_identity_coupling.py | 261 | 4 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-12 21:39
mag/tesuji_fire.py | 433 | 3 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-07 03:22
mag/tesuji_map.py | 173 | 4 | 0 | 0 | 3 | d575bc168 2026-09-14 | 2026-09-07 01:27
mag/tesuji_probes.py | 475 | 11 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-05 23:24
mag/tesuji_shell.py | 263 | 5 | 0 | 3 | 18 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/tesuji_surface.py | 490 | 3 | 2 | 0 | 3 | de29d49ea 2026-08-09 | 2026-08-09 07:47
mag/the_margin.py | 548 | 10 | 4 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-06 17:20
mag/thought_bank.py | 55 | 2 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-04 22:16
mag/thought_bank_app.py | 116 | 1 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-04 23:37
mag/thread_eye.py | 97 | 2 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-09 17:58
mag/throughput_model.py | 152 | 5 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-12 10:20
mag/time_estimate.py | 133 | 2 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-12 00:23
mag/token_chain.py | 397 | 4 | 0 | 1 | 3 | e4dd520e8 2026-08-06 | 2026-08-06 18:28
mag/token_economy.py | 204 | 7 | 0 | 1 | 5 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/tokenomics.py | 431 | 5 | 1 | 0 | 3 | de7bb85fe 2026-08-09 | 2026-08-08 22:31
mag/tool_5ws.py | 114 | 3 | 0 | 0 | 2 | 052732ebf 2026-08-14 | 2026-08-11 10:23
mag/tool_lifecycle.py | 150 | 10 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-13 07:18
mag/tool_manifest.py | 216 | 5 | 0 | 0 | 2 | 052732ebf 2026-08-14 | 2026-08-10 19:17
mag/tool_quant.py | 133 | 5 | 0 | 1 | 3 | 052732ebf 2026-08-14 | 2026-08-12 10:41
mag/tool_retire.py | 195 | 4 | 0 | 0 | 2 | de29d49ea 2026-08-09 | 2026-08-09 14:30
mag/tool_synthesis.py | 450 | 10 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-12 06:15
mag/top_processes.py | 86 | 4 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-08-30 14:43
mag/topic_index.py | 375 | 3 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-05 22:01
mag/topic_index_v3_tf_draft.py | 230 | 2 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-05 21:59
mag/topic_orphan.py | 120 | 3 | 0 | 0 | 1 | de7bb85fe 2026-08-09 | 2026-08-09 00:05
mag/tortoise_demo.py | 135 | 6 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-07 17:35
mag/training_events.py | 195 | 4 | 0 | 14 | 73 | e96fd62a4 2026-08-07 | 2026-08-06 23:35
mag/training_packager.py | 308 | 2 | 0 | 0 | 1 | de7bb85fe 2026-08-09 | 2026-08-08 22:13
mag/training_rightsize.py | 105 | 2 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-10 00:05
mag/training_set.py | 145 | 3 | 0 | 0 | 1 | de29d49ea 2026-08-09 | 2026-08-09 20:07
mag/trajectory_bounds.py | 93 | 2 | 0 | 1 | 1 | d575bc168 2026-09-14 | 2026-08-31 00:01
mag/trajectory_paths.py | 117 | 2 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-07 01:18
mag/trajectory_rib.py | 190 | 2 | 0 | 1 | 4 | d575bc168 2026-09-14 | 2026-09-02 03:19
mag/trajectory_step.py | 172 | 8 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-05 13:07
mag/transfer_gate.py | 666 | 11 | 3 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-06 11:49
mag/trigger_learn.py | 244 | 4 | 0 | 0 | 2 | 052732ebf 2026-08-14 | 2026-08-12 08:50
mag/tripartite.py | 281 | 7 | 0 | 0 | 18 | 052732ebf 2026-08-14 | 2026-08-12 07:14
mag/tripartite_boot.py | 535 | 10 | 0 | 1 | 7 | 1c156e2fa 2026-08-06 | 2026-08-06 18:28
mag/trust_gate.py | 257 | 6 | 0 | 0 | 4 | a5dd96176 2026-09-25 | 2026-09-25 20:27
mag/trust_gate_audit_check.py | 100 | 2 | 0 | 0 | 0 | a5dd96176 2026-09-25 | 2026-09-25 20:37
mag/truth_audit.py | 176 | 6 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-08-30 12:55
mag/tts.py | 235 | 3 | 0 | 0 | 5 | 383fed94f 2026-09-27 | 2026-09-26 13:30
mag/unsloth_seat.py | 491 | 7 | 0 | 1 | 3 | de29d49ea 2026-08-09 | 2026-08-09 18:46
mag/usage_digest.py | 282 | 3 | 0 | 0 | 1 | 383fed94f 2026-09-27 | 2026-09-26 16:20
mag/usage_forecast.py | 239 | 6 | 0 | 0 | 2 | de29d49ea 2026-08-09 | 2026-08-09 08:07
mag/usage_monitor.py | 178 | 5 | 0 | 0 | 7 | 052732ebf 2026-08-14 | 2026-08-11 10:32
mag/vantage_audit.py | 195 | 6 | 0 | 1 | 1 | 052732ebf 2026-08-14 | 2026-08-12 16:14
mag/vast_cost.py | 335 | 2 | 0 | 1 | 3 | d575bc168 2026-09-14 | 2026-08-30 20:51
mag/vast_launcher.py | 495 | 8 | 1 | 0 | 5 | d575bc168 2026-09-14 | 2026-08-29 20:23
mag/vast_train.py | 108 | 5 | 0 | 1 | 1 | 1e92a7012 2026-08-06 | 2026-08-06 18:28
mag/verb.py | 512 | 11 | 0 | 1 | 3 | 4ad6eb0d6 2026-09-19 | 2026-09-19 11:51
mag/verified_clock.py | 161 | 9 | 0 | 0 | 2 | cb26bc2cd 2026-08-25 | 2026-08-24 09:19
mag/verify_gate.py | 233 | 3 | 0 | 0 | 0 | cb26bc2cd 2026-08-25 | 2026-08-23 06:51
mag/verify_succession_contract.py | 149 | 6 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-12 22:23
mag/verkle_artifact.py | 111 | 2 | 0 | 1 | 1 | d575bc168 2026-09-14 | 2026-09-01 20:46
mag/verkle_audit.py | 439 | 4 | 0 | 1 | 7 | d575bc168 2026-09-14 | 2026-09-10 16:39
mag/verkle_bus.py | 292 | 9 | 0 | 1 | 18 | 052732ebf 2026-08-14 | 2026-08-11 08:06
mag/verkle_compaction.py | 396 | 5 | 0 | 1 | 0 | e73b60c54 2026-09-27 | 2026-09-27 01:01
mag/verkle_knot.py | 920 | 10 | 1 | 6 | 88 | 7b8617d78 2026-09-27 | 2026-09-27 13:35
mag/verkle_lance.py | 456 | 12 | 0 | 0 | 9 | 052732ebf 2026-08-14 | 2026-08-11 05:55
mag/verkle_render.py | 116 | 5 | 0 | 0 | 2 | 799ddb6fe 2026-08-19 | 2026-08-15 06:55
mag/verkle_rib.py | 123 | 4 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-09 23:59
mag/vertical_meter.py | 111 | 2 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-07 09:20
mag/vessel_swarm.py | 221 | 8 | 0 | 1 | 1 | 052732ebf 2026-08-14 | 2026-08-12 16:58
mag/virtual_desk_loop.py | 679 | 9 | 0 | 1 | 1 | 771ebac19 2026-08-05 | 2026-08-06 18:28
mag/vision.py | 124 | 2 | 0 | 0 | 6 | cb26bc2cd 2026-08-25 | 2026-08-25 12:35
mag/visual_pack.py | 608 | 3 | 0 | 0 | 4 | eb07ad62e 2026-08-04 | 2026-08-04 11:46
mag/voice_dictate.py | 190 | 3 | 0 | 1 | 2 | de7bb85fe 2026-08-09 | 2026-08-09 00:13
mag/voice_dig_board.py | 466 | 9 | 0 | 1 | 5 | e96fd62a4 2026-08-07 | 2026-08-06 21:36
mag/voice_handoff.py | 507 | 11 | 0 | 1 | 2 | e96fd62a4 2026-08-07 | 2026-08-06 21:30
mag/voice_lanes.py | 236 | 6 | 0 | 0 | 1 | e96fd62a4 2026-08-07 | 2026-08-06 21:38
mag/voice_pipeline.py | 335 | 1 | 0 | 1 | 1 | e96fd62a4 2026-08-07 | 2026-08-06 20:10
mag/voice_scratch.py | 412 | 6 | 0 | 1 | 2 | e96fd62a4 2026-08-07 | 2026-08-06 20:10
mag/voice_self.py | 99 | 3 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-12 06:24
mag/voice_shadow.py | 241 | 6 | 0 | 1 | 2 | e96fd62a4 2026-08-07 | 2026-08-06 20:47
mag/voice_skills.py | 74 | 3 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-08-29 18:16
mag/voice_stt.py | 177 | 5 | 0 | 0 | 6 | e96fd62a4 2026-08-07 | 2026-08-06 20:55
mag/voice_tasks.py | 263 | 5 | 0 | 0 | 3 | e96fd62a4 2026-08-07 | 2026-08-06 20:49
mag/voice_trigger.py | 171 | 3 | 0 | 0 | 3 | 799ddb6fe 2026-08-19 | 2026-08-14 20:30
mag/voice_turn.py | 1777 | 5 | 0 | 2 | 9 | d575bc168 2026-09-14 | 2026-08-29 18:16
mag/volume_fidelity.py | 562 | 12 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-06 18:35
mag/vram_hologram.py | 204 | 6 | 0 | 1 | 0 | 052732ebf 2026-08-14 | 2026-08-12 16:11
mag/vram_memory.py | 137 | 4 | 0 | 0 | 7 | 799ddb6fe 2026-08-19 | 2026-08-14 09:36
mag/vscode_feed.py | 221 | 3 | 0 | 0 | 2 | 60e18c524 2026-08-08 | 2026-08-08 07:42
mag/vscode_seat.py | 178 | 5 | 0 | 0 | 0 | 799ddb6fe 2026-08-19 | 2026-08-16 10:49
mag/warmed_cold_replay.py | 497 | 11 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-07 09:39
mag/warning_monitor.py | 205 | 5 | 0 | 1 | 4 | 60e18c524 2026-08-08 | 2026-08-08 11:41
mag/water_computer.py | 880 | 33 | 0 | 2 | 6 | 6c43c15d2 2026-09-27 | 2026-09-27 23:32
mag/water_graph.py | 274 | 1 | 3 | 3 | 1 | a6275084d 2026-09-27 | 2026-09-27 21:26
mag/water_swarm.py | 128 | 4 | 0 | 1 | 3 | 052732ebf 2026-08-14 | 2026-08-12 10:41
mag/wave.py | 655 | 4 | 0 | 0 | 15 | 799ddb6fe 2026-08-19 | 2026-08-16 10:29
mag/wave_address.py | 178 | 7 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-13 04:32
mag/wave_cache.py | 20 | 2 | 0 | 0 | 1 | 799ddb6fe 2026-08-19 | 2026-08-15 22:22
mag/wave_fire.py | 153 | 5 | 0 | 0 | 1 | d575bc168 2026-09-14 | 2026-09-13 12:36
mag/wearable_swarm.py | 207 | 6 | 0 | 0 | 4 | 052732ebf 2026-08-14 | 2026-08-11 08:58
mag/whale_patrol.py | 319 | 20 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-07 21:16
mag/whisper_image.py | 288 | 7 | 0 | 1 | 6 | 052732ebf 2026-08-14 | 2026-08-10 11:46
mag/whisper_route.py | 138 | 7 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-10 14:15
mag/win_powershell.py | 43 | 1 | 0 | 0 | 3 | 6d417abd5 2026-09-26 | 2026-09-26 16:55
mag/window_audit.py | 112 | 3 | 0 | 0 | 4 | 6d417abd5 2026-09-26 | 2026-09-26 17:25
mag/window_bus.py | 257 | 8 | 0 | 0 | 1 | 052732ebf 2026-08-14 | 2026-08-10 14:28
mag/window_hop.py | 117 | 2 | 1 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-10 14:28
mag/window_throttle.py | 378 | 8 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-04 11:44
mag/wireshark_steal.py | 142 | 4 | 0 | 1 | 0 | 052732ebf 2026-08-14 | 2026-08-12 16:11
mag/witness_snapshot.py | 67 | 3 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-08 21:06
mag/word_skill_map.py | 237 | 5 | 0 | 0 | 4 | de29d49ea 2026-08-09 | 2026-08-09 14:55
mag/work_contract.py | 111 | 3 | 0 | 0 | 7 | d575bc168 2026-09-14 | 2026-08-26 08:06
mag/work_loop.py | 334 | 4 | 0 | 1 | 3 | 790145ab1 2026-09-26 | 2026-09-26 01:03
mag/work_register.py | 180 | 5 | 0 | 0 | 6 | cb26bc2cd 2026-08-25 | 2026-08-25 11:17
mag/work_tiers.py | 105 | 3 | 0 | 0 | 0 | de7bb85fe 2026-08-09 | 2026-08-08 23:20
mag/workspace_api.py | 101 | 3 | 0 | 1 | 1 | eb07ad62e 2026-08-04 | 2026-08-04 18:48
mag/world_rib.py | 172 | 5 | 0 | 1 | 10 | 052732ebf 2026-08-14 | 2026-08-11 09:27
mag/worldline_dungeon.py | 551 | 13 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-07 08:31
mag/worldline_seed.py | 1072 | 4 | 0 | 0 | 4 | d575bc168 2026-09-14 | 2026-09-07 13:20
mag/wow_bones.py | 370 | 8 | 3 | 4 | 5 | 5305a99b1 2026-09-16 | 2026-09-16 13:15
mag/wow_bones_session.py | 271 | 3 | 1 | 3 | 5 | 5305a99b1 2026-09-16 | 2026-09-16 13:14
mag/wow_family.py | 324 | 7 | 0 | 1 | 1 | 30e5ec7e2 2026-09-15 | 2026-09-15 21:19
mag/wow_manifest.py | 114 | 1 | 0 | 1 | 1 | 052732ebf 2026-08-14 | 2026-08-12 10:20
mag/wow_player.py | 433 | 4 | 2 | 1 | 1 | 75c030d29 2026-09-16 | 2026-09-16 16:38
mag/wow_steal.py | 388 | 5 | 0 | 0 | 3 | 30e5ec7e2 2026-09-15 | 2026-09-15 21:07
mag/wow_world.py | 372 | 4 | 1 | 1 | 2 | 75c030d29 2026-09-16 | 2026-09-16 16:56
mag/write_strip.py | 164 | 6 | 0 | 1 | 2 | a5dd96176 2026-09-25 | 2026-09-25 21:02
mag/x_auth_once.py | 29 | 1 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-05 19:27
mag/x_chat_mine.py | 94 | 2 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-11 11:28
mag/x_control_surface.py | 677 | 14 | 0 | 0 | 4 | cb26bc2cd 2026-08-25 | 2026-08-23 23:20
mag/x_interceptor.py | 205 | 3 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-06 13:39
mag/x_oauth.py | 550 | 13 | 0 | 0 | 3 | d575bc168 2026-09-14 | 2026-09-05 23:51
mag/x_posts_mine.py | 123 | 2 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-11 12:02
mag/x_reply_radar.py | 104 | 3 | 0 | 0 | 0 | d575bc168 2026-09-14 | 2026-09-11 08:07
mag/x_surface.py | 131 | 5 | 0 | 0 | 0 | 052732ebf 2026-08-14 | 2026-08-10 19:13

## Per-module detail

### mag/__init__.py

- lines: 17 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (0): none
- public classes (0): none
- test files (308): `mag/tests/test_identity_schema_portability.py`, `mag/tests/verify_identity_coupling.py`, `tests/conftest.py`, `tests/test_abundance_rogue.py`, `tests/test_adventure_moonshot.py`, `tests/test_agent_arena.py`, `tests/test_agent_corpus.py`, `tests/test_agent_desk.py` + 300 more
- readers (1340): `_afk_full_blast.py`, `_alpha_dryrun.py`, `_alpha_frontier.py`, `_alpha_multi.py`, `_alpha_rar.py`, `_alpha_rar_deepseek.py`, `_alpha_rar_fleet.py`, `_alpha_steer.py` + 1332 more

### mag/_bench_free_shelf.py

- lines: 59 | parse: ok | last commit: 47d3907e3 2026-08-25 | mtime: 2026-09-16 18:12
- public functions (1): `call`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/_cache_ab_probe.py

- lines: 64 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-09-16 18:12
- public functions (2): `hit_tokens`, `probe`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/_codex_seat.py

- lines: 84 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-27 07:45
- public functions (1): `run_task`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/_comb_tokens.py

- lines: 84 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-09-16 18:12
- public functions (0): none
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/_compare_chain_sources.py

- lines: 31 | parse: ok | last commit: b7a47f194 2026-08-25 | mtime: 2026-09-16 18:12
- public functions (1): `sha`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/_conc_test_slot.py

- lines: 77 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-05 19:06
- public functions (1): `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/_consensus_witness.py

- lines: 108 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 19:35
- public functions (3): `ask`, `extract_int`, `main`
- public classes (0): none
- test files (1): `tests/test_dormant_gate_b2521.py`
- readers (0): none

### mag/_deep_research_verkle_dedupe.py

- lines: 63 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-09-16 18:12
- public functions (1): `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/_demo_eyes_receipt.py

- lines: 116 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-27 04:16
- public functions (4): `make_challenge`, `blind_answer`, `endowed_answer`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/_demo_telepathy.py

- lines: 173 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-26 16:00
- public functions (4): `interpret`, `sender`, `receiver`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/_diag_cache.py

- lines: 11 | parse: ok | last commit: a4131cb46 2026-08-25 | mtime: 2026-09-16 18:12
- public functions (0): none
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/_exp_a_cache_retrigger.py

- lines: 68 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-28 20:51
- public functions (2): `hit_tokens`, `call`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/_flag_dangling_20260925.py

- lines: 106 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 16:36
- public functions (0): none
- public classes (0): none
- test files (0): none
- readers (1): `mag/verkle_compaction.py`

### mag/_flag_dangling_264d0ba3.py

- lines: 97 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 16:36
- public functions (0): none
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/_gpu_probe_debug.py

- lines: 39 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-09-16 18:12
- public functions (0): none
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/_grok_corpus_burn.py

- lines: 103 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-16 18:12
- public functions (4): `slug`, `goal_for`, `burn_one`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/_openclaw_real.py

- lines: 19 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-09-16 18:12
- public functions (2): `top_lanes`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/_probe_burst_20260903.py

- lines: 99 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-03 19:27
- public functions (3): `call`, `wave`, `summarize`
- public classes (0): none
- test files (0): none
- readers (1): `mag/flight_recorder.py`

### mag/_probe_dangling.py

- lines: 29 | parse: ok | last commit: b7a47f194 2026-08-25 | mtime: 2026-09-16 18:12
- public functions (0): none
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/_probe_mcp.py

- lines: 36 | parse: ok | last commit: 1d607e078 2026-08-25 | mtime: 2026-09-16 18:12
- public functions (0): none
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/_probe_zai_balance.py

- lines: 51 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-09-16 18:12
- public functions (0): none
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/_relane_game_tasks.py

- lines: 44 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-09-16 18:12
- public functions (0): none
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/_salon_burn.py

- lines: 96 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-16 18:12
- public functions (5): `codex_witness`, `grok_witness`, `elder_witness`, `run_witness`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/_verify_chain_now.py

- lines: 32 | parse: ok | last commit: b7a47f194 2026-08-25 | mtime: 2026-08-25 13:39
- public functions (0): none
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/_verify_concurrency_gate.py

- lines: 49 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-09-16 18:12
- public functions (0): none
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/_verify_queue_gate.py

- lines: 80 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-09-16 18:12
- public functions (0): none
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/_verify_repair_state.py

- lines: 16 | parse: ok | last commit: b7a47f194 2026-08-25 | mtime: 2026-09-16 18:12
- public functions (0): none
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/_verify_rung5.py

- lines: 50 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-09-16 18:12
- public functions (0): none
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/_verify_sharp_edge.py

- lines: 59 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-09-16 18:12
- public functions (0): none
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/_verify_verkle_gate_spec.py

- lines: 104 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-07 09:25
- public functions (1): `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/_warm_rib.py

- lines: 18 | parse: ok | last commit: a4131cb46 2026-08-25 | mtime: 2026-09-16 18:12
- public functions (0): none
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/abliterator_spawn_manifest.py

- lines: 128 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-12 22:30
- public functions (4): `read_ledger`, `compute_checksum`, `mutate_row`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/abundance_rogue.py

- lines: 218 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 16:58
- public functions (7): `enter`, `dungeon`, `play`, `history`, `abundance`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_abundance_rogue.py`
- readers (1): `mag/republic_loop.py`

### mag/accumulator.py

- lines: 280 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-04 18:34
- public functions (1): `feature_key`
- public classes (3): `Accumulator`, `Session`, `HeadStub`
- test files (0): none
- readers (0): none

### mag/act.py

- lines: 248 | parse: ok | last commit: d90bc8607 2026-09-28 | mtime: 2026-09-28 14:51
- public functions (1): `act`
- public classes (0): none
- test files (1): `tests/test_silentpass_batch2.py`
- readers (3): `mag/__init__.py`, `mag/daemon.py`, `main.py`

### mag/adventure_moonshot.py

- lines: 245 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-13 14:59
- public functions (4): `adventure`, `cadence`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_adventure_moonshot.py`
- readers (1): `mag/governor_autorun.py`

### mag/adventure_one_shot.py

- lines: 202 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-18 11:04
- public functions (6): `status`, `begin`, `stage`, `act`, `complete`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/afk_cadence.py

- lines: 284 | parse: ok | last commit: 790145ab1 2026-09-26 | mtime: 2026-09-26 01:30
- public functions (3): `run_once`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_loop_death_guards.py`
- readers (5): `mag/auto_handoff.py`, `mag/gpu_ghost.py`, `mag/organ_map.py`, `memory/trash/20260810T202850Z/_tmp_afk_autonomy.py`, `state/backups/orphan_close_20260906/organ_map.py`

### mag/afk_loop.py

- lines: 341 | parse: ok | last commit: d90bc8607 2026-09-28 | mtime: 2026-09-28 14:50
- public functions (8): `socratic_probe`, `freebie_scan`, `tool_test_cheap`, `occupy`, `system_resources`, `right_size`, `squeeze_free_test_data`, `occupy`
- public classes (0): none
- test files (2): `tests/test_loop_death_guards.py`, `tests/test_silentpass_batch2.py`
- readers (8): `mag/afk_cadence.py`, `mag/afk_orchestrator.py`, `mag/capability_steal.py`, `mag/memlang.py`, `mag/seat_hunter.py`, `mag/self_advance.py`, `mag/skill_pipeline.py`, `mag/swarm_capacity.py`

### mag/afk_orchestrator.py

- lines: 189 | parse: ok | last commit: 790145ab1 2026-09-26 | mtime: 2026-09-26 01:30
- public functions (2): `run_afk`, `main`
- public classes (0): none
- test files (1): `tests/test_loop_death_guards.py`
- readers (0): none

### mag/agent_arena.py

- lines: 503 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (5): `status`, `new_game`, `apply_move`, `agent_turn`, `handle_action`
- public classes (0): none
- test files (4): `tests/test_agent_arena.py`, `tests/test_arena_adapter.py`, `tests/test_arena_learning.py`, `tests/test_desk_dialogue.py`
- readers (5): `dashboard/rest.py`, `mag/arena_learning.py`, `mag/desk_dialogue.py`, `mag/openclaw_catalog.py`, `main.py`

### mag/agent_behavior.py

- lines: 145 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 14:34
- public functions (4): `record`, `profile`, `summary`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/ghost_auto.py`

### mag/agent_cli.py

- lines: 3139 | parse: ok | last commit: d90bc8607 2026-09-28 | mtime: 2026-09-28 14:51
- public functions (31): `dim`, `bold`, `green`, `cyan`, `yellow`, `mag_c`, `rule`, `print_mdish`, `print_banner`, `print_help`, `activate_read_only`, `restore_full_grant`, `provider_context_tokens`, `usable_context_budget`, `repack_messages`, `run_turn`, `load_run`, `normalize_seat`, `save_last`, `read_paste_block`, `attach_file`, `read_user_input`, `push_steer`, `get_live_turn`, `apply_steer`, `run_agent`, `load_session`, `save_session`, `api_agent_reset`, `api_agent_turn`, `main_argv`
- public classes (0): none
- test files (14): `tests/test_agent_desk.py`, `tests/test_agent_live.py`, `tests/test_agent_repack.py`, `tests/test_context_freeze.py`, `tests/test_prompt_steering.py`, `tests/test_repack_integration.py`, `tests/test_resume_contract.py`, `tests/test_seat_crash_guard.py` + 6 more
- readers (21): `backend/server.py`, `configs/features.yaml`, `dashboard/rest.py`, `dashboard/server.py`, `mag/context_growth.py`, `mag/coordination.py`, `mag/desk_orchestrator.py`, `mag/doctor.py` + 13 more

### mag/agent_corpus.py

- lines: 270 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 13:27
- public functions (6): `register_agent`, `log_chat`, `corpus`, `fold_into_world`, `seed_major_players`, `main`
- public classes (0): none
- test files (2): `tests/test_agent_corpus.py`, `tests/test_frontier_salon.py`
- readers (3): `mag/frontier_salon.py`, `mag/reconstruct.py`, `mag/republic_loop.py`

### mag/agent_desk.py

- lines: 257 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 13:59
- public functions (11): `read_desk`, `write_desk`, `set_desk_section`, `set_desk_goal`, `commit_operator_intent`, `peer_lane_excerpt`, `desk_snapshot`, `ensure_desk_template`, `append_desk_section`, `append_desk_raw`, `append_desk_meta_raw`
- public classes (0): none
- test files (6): `tests/test_agent_desk.py`, `tests/test_agent_desk_commit.py`, `tests/test_coding_session_loop.py`, `tests/test_coding_session_orchestrator.py`, `tests/test_desk_dialogue.py`, `tests/test_desk_timing.py`
- readers (13): `dashboard/rest.py`, `mag/coding_session_loop.py`, `mag/coding_session_orchestrator.py`, `mag/desk_conductor.py`, `mag/desk_dialogue.py`, `mag/desk_observer.py`, `mag/desk_orchestrator.py`, `mag/desk_orchestrator_memory.py` + 5 more

### mag/agent_knot.py

- lines: 334 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 08:05
- public functions (6): `standing_invariant`, `stand`, `evolve`, `evo_status`, `where`, `status`
- public classes (0): none
- test files (2): `mag/tests/test_identity_schema_portability.py`, `mag/tests/verify_identity_coupling.py`
- readers (14): `mag/chain_substrate.py`, `mag/chord_pipeline.py`, `mag/evolving_wave.py`, `mag/future_self.py`, `mag/ghost_cold_boot.py`, `mag/grok_weave.py`, `mag/liveness_sense.py`, `mag/portal.py` + 6 more

### mag/agent_os_loop.py

- lines: 108 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 08:00
- public functions (3): `cycle`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/research_class.py`

### mag/agent_signature.py

- lines: 220 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 20:14
- public functions (5): `scan`, `signature`, `know`, `audit`, `status`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/agent_state.py

- lines: 466 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-01 21:00
- public functions (10): `ensure_dirs`, `agent_state_lock`, `load_latest`, `load_version`, `list_versions`, `content_commit_hex`, `format_load_markdown`, `pack_excerpt`, `commit_state`, `link_to_residual`
- public classes (0): none
- test files (3): `tests/test_agent_state.py`, `tests/test_honest_cache_meter.py`, `tests/test_session_freeze.py`
- readers (13): `configs/modules.yaml`, `mag/agent_state_router.py`, `mag/context_pack.py`, `mag/diary_node.py`, `mag/doctor.py`, `mag/ghost.py`, `mag/governor_autorun.py`, `mag/law.py` + 5 more

### mag/agent_state_router.py

- lines: 129 | parse: ok | last commit: de7bb85fe 2026-08-09 | mtime: 2026-08-09 01:13
- public functions (4): `resolve`, `pick`, `states`, `main`
- public classes (0): none
- test files (0): none
- readers (4): `mag/ghost.py`, `mag/gpipes.py`, `mag/self_drive.py`, `mag/session_route.py`

### mag/agentic_test_steal.py

- lines: 154 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 10:17
- public functions (5): `frameworks`, `map_ours`, `frontier_steal`, `run`, `status`
- public classes (0): none
- test files (0): none
- readers (2): `mag/gap_frontier.py`, `mag/republic_loop.py`

### mag/ai_landscape.py

- lines: 329 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 12:03
- public functions (5): `recognize`, `delta`, `landscape`, `research`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/dogfood_audit.py`, `mag/knowledge_graph.py`, `mag/schema_registry.py`

### mag/amd_window_guard.py

- lines: 84 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 07:10
- public functions (2): `check`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/ghost.py`, `mag/guard_registry.py`

### mag/aos_agent.py

- lines: 314 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 14:51
- public functions (3): `reply`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/aos_bus_watcher.py`, `memory/runs/_aos_continue.py`, `memory/runs/_aos_live.py`

### mag/aos_bus_watcher.py

- lines: 336 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 16:16
- public functions (4): `check`, `run_cadence`, `status`, `daemon`
- public classes (0): none
- test files (0): none
- readers (2): `mag/aos_live_view.py`, `mag/governor_autorun.py`

### mag/aos_grok.py

- lines: 325 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 09:23
- public functions (5): `budget_status`, `specific_ask`, `probe`, `run_cadence`, `main`
- public classes (0): none
- test files (0): none
- readers (6): `dashboard/rest.py`, `mag/doctor.py`, `mag/ghost.py`, `mag/governor_autorun.py`, `mag/grok_route.py`, `main.py`

### mag/aos_live_view.py

- lines: 360 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 11:22
- public functions (5): `sanitize`, `render`, `watch`, `chat_json`, `send_text`
- public classes (0): none
- test files (0): none
- readers (34): `dashboard/server.py`, `mag/aos_agent.py`, `memory/runs/_aos_actual_reply.py`, `memory/runs/_aos_answer_hall.py`, `memory/runs/_aos_answer_whole.py`, `memory/runs/_aos_ask_next.py`, `memory/runs/_aos_bone.py`, `memory/runs/_aos_bones.py` + 26 more

### mag/api_gateway.py

- lines: 767 | parse: ok | last commit: 790145ab1 2026-09-26 | mtime: 2026-09-26 00:49
- public functions (4): `api_key`, `check_api_key`, `route`, `dispatch`
- public classes (0): none
- test files (2): `tests/test_api_gateway_status_route.py`, `tests/test_room_tags.py`
- readers (3): `mag/api_server.py`, `mag/mcp_http.py`, `state/backups/orphan_close_20260906/api_gateway.py`

### mag/api_server.py

- lines: 123 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-04 20:11
- public functions (3): `require_api_key`, `gateway_bridge`, `run`
- public classes (0): none
- test files (1): `tests/test_launch_topology.py`
- readers (3): `configs/organs/host_resolver.yaml`, `mag/organ_map.py`, `main.py`

### mag/arc_seed.py

- lines: 181 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-06 20:35
- public functions (4): `parse_rollout`, `anatomy`, `seed_skeleton`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/knot_at_close.py`

### mag/archetype_image.py

- lines: 365 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 11:52
- public functions (7): `classify`, `render`, `artifact`, `decode`, `flock_dispatch`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (5): `mag/dogfood_audit.py`, `mag/knowledge_graph.py`, `mag/schema_registry.py`, `mag/self_steal.py`, `mag/shadow_work.py`

### mag/arena_adapter.py

- lines: 284 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-08 19:56
- public functions (3): `probe_meta`, `list_games`, `run_probe`
- public classes (1): `MagSeatAgent`
- test files (1): `tests/test_arena_adapter.py`
- readers (3): `dashboard/rest.py`, `mag/agent_arena.py`, `main.py`

### mag/arena_bench.py

- lines: 597 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-05 00:59
- public functions (16): `load_ground_truth`, `build_claims`, `build_evidence_pack`, `load_weights`, `weights_canonical`, `weights_sha256`, `seal_status`, `parse_verdict`, `score_transcript`, `build_challenge_text`, `parse_live_answer`, `run_live`, `run_live_endpoint`, `fixture_pass`, `fixture_fail`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/arena_learning.py

- lines: 456 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (8): `record_move`, `record_game_end`, `rebuild_league`, `league_snapshot`, `routing_hint`, `ingest_arena_state`, `run_tournament`, `nervous_glance`
- public classes (0): none
- test files (2): `tests/test_arena_adapter.py`, `tests/test_arena_learning.py`
- readers (6): `dashboard/rest.py`, `mag/agent_arena.py`, `mag/arena_adapter.py`, `mag/nervous_system.py`, `mag/switchboard.py`, `main.py`

### mag/arena_strategies.py

- lines: 142 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (7): `list_strategies`, `get_strategy`, `default_for_seat`, `strategy_for_game_state`, `augment_move_prompt`, `emit_spider_arena_signal`, `routing_hint_for_ocean`
- public classes (0): none
- test files (0): none
- readers (3): `dashboard/rest.py`, `mag/agent_arena.py`, `mag/local_playbook.py`

### mag/arrival.py

- lines: 204 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 11:24
- public functions (4): `fold_authored`, `status`, `arrival`, `recreate`
- public classes (0): none
- test files (2): `tests/test_arrival.py`, `tests/test_moonshot_engine.py`
- readers (3): `mag/moonshot_engine.py`, `mag/republic_loop.py`, `mag/self_steal.py`

### mag/art_forge.py

- lines: 169 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-04 20:58
- public functions (1): `forge_once`
- public classes (0): none
- test files (0): none
- readers (1): `mag/lane_runner.py`

### mag/arxiv_harvest.py

- lines: 179 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-04 23:05
- public functions (1): `harvest`
- public classes (0): none
- test files (0): none
- readers (1): `mag/lane_runner.py`

### mag/arxiv_mine.py

- lines: 242 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 18:33
- public functions (5): `route_goal`, `route_candidates`, `mine`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/capability_steal.py`, `mag/improve.py`

### mag/ask.py

- lines: 393 | parse: ok | last commit: e96fd62a4 2026-08-07 | mtime: 2026-08-06 19:47
- public functions (2): `gather_context`, `ask`
- public classes (0): none
- test files (0): none
- readers (5): `dashboard/rest.py`, `mag/dispatch.py`, `mag/frontier_council.py`, `mag/route.py`, `main.py`

### mag/ask_router.py

- lines: 277 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 19:36
- public functions (10): `load_ledger`, `lane_stats`, `harvest_costs`, `score_lane`, `route`, `cmd_route`, `cmd_record`, `cmd_record`, `record_outcome`, `main`
- public classes (0): none
- test files (1): `tests/test_dormant_gate_b2521.py`
- readers (6): `mag/afk_cadence.py`, `mag/api_gateway.py`, `mag/dogfood_audit.py`, `mag/organ_map.py`, `state/backups/orphan_close_20260906/api_gateway.py`, `state/backups/orphan_close_20260906/organ_map.py`

### mag/atlas.py

- lines: 78 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 21:59
- public functions (3): `build`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (4): `mag/basecamp.py`, `mag/fireball_cycle.py`, `mag/organ_map.py`, `state/backups/orphan_close_20260906/organ_map.py`

### mag/attention_ranker.py

- lines: 254 | parse: ok | last commit: ef4dce855 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (2): `record_feedback`, `build_ranked_attention`
- public classes (0): none
- test files (1): `tests/test_attention_ranker.py`
- readers (3): `dashboard/rest.py`, `mag/feedback.py`, `mag/framework_map.py`

### mag/attractor_tools.py

- lines: 161 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 17:00
- public functions (6): `strongest_attractors`, `to_memlang_chord`, `deploy_to_swarm`, `fold_as_knowledge`, `run`, `main`
- public classes (0): none
- test files (0): none
- readers (6): `mag/end_state.py`, `mag/frontier_intake.py`, `mag/ghost_experimenter.py`, `mag/readout_controller.py`, `mag/republic_loop.py`, `mag/swarm_run.py`

### mag/audit_log.py

- lines: 20 | parse: ok | last commit: b1d714b02 2026-09-25 | mtime: 2026-09-25 08:28
- public functions (1): `audit_log`
- public classes (0): none
- test files (0): none
- readers (1): `mag/spore_seed.py`

### mag/auth_switchboard.py

- lines: 292 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-05 12:16
- public functions (13): `fp`, `jload`, `provider_table`, `probe_key`, `plan_cache`, `active_track`, `trail_row`, `cmd_status`, `cmd_snapshot`, `cmd_list`, `cmd_use`, `cmd_trail`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `auth_status.cmd`, `configs/auth_tracks.yaml`

### mag/auto_handoff.py

- lines: 136 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 16:12
- public functions (3): `run`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/auto_quantize.py

- lines: 456 | parse: ok | last commit: de7bb85fe 2026-08-09 | mtime: 2026-08-08 20:30
- public functions (1): `estimate_storage`
- public classes (2): `Quantum`, `AutoQuantizer`
- test files (0): none
- readers (0): none

### mag/autodrain.py

- lines: 214 | parse: ok | last commit: 47d3907e3 2026-08-25 | mtime: 2026-08-25 20:54
- public functions (5): `acquire`, `release`, `run_loop`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/autoglm.py

- lines: 167 | parse: ok | last commit: 0f34a8f3e 2026-09-16 | mtime: 2026-09-16 14:44
- public functions (2): `act`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/autonomous_research.py

- lines: 589 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-24 22:20
- public functions (11): `plan`, `status`, `spawn_overnight`, `wow_clone_swarm`, `game_swarm`, `fold_k8s_to_k3s`, `lens_research_asks`, `process_lensed_data`, `route_local`, `deep_research_project`, `main`
- public classes (0): none
- test files (0): none
- readers (5): `mag/organ_map.py`, `mag/republic_loop.py`, `mag/tool_synthesis.py`, `memory/runs/_probe_zai_cache.py`, `state/backups/orphan_close_20260906/organ_map.py`

### mag/autopilot.py

- lines: 113 | parse: ok | last commit: f3a1ff214 2026-08-05 | mtime: 2026-08-06 18:28
- public functions (1): `autopilot_once`
- public classes (0): none
- test files (1): `tests/test_three_track.py`
- readers (4): `dashboard/rest.py`, `mag/governor_autorun.py`, `mag/orchestrator.py`, `main.py`

### mag/autorun_common.py

- lines: 100 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-02 04:10
- public functions (4): `autorun_pause_reason`, `refresh_context_for_goal`, `fkb_score_adjustment`, `fkb_block_for_goal`
- public classes (0): none
- test files (2): `tests/test_autorun_v1.py`, `tests/test_factory_freeze_gate.py`
- readers (5): `mag/governor.py`, `mag/governor_autorun.py`, `mag/orchestrator.py`, `mag/organ_map.py`, `state/backups/orphan_close_20260906/organ_map.py`

### mag/autorun_status.py

- lines: 219 | parse: ok | last commit: f3a1ff214 2026-08-05 | mtime: 2026-08-06 18:28
- public functions (2): `routing_legend`, `autorun_dashboard_status`
- public classes (0): none
- test files (0): none
- readers (2): `dashboard/rest.py`, `mag/handoff_inbox.py`

### mag/backlog_reform.py

- lines: 143 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-09 23:10
- public functions (3): `reform`, `summary`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/gpu_ghost.py`, `mag/offline.py`, `mag/stateless_research.py`

### mag/bard.py

- lines: 985 | parse: ok | last commit: 482e0a3c8 2026-08-08 | mtime: 2026-08-08 19:11
- public functions (18): `character_for`, `coin_for`, `quest_for`, `sage_for`, `realm_for`, `adversity_for`, `bard_weave`, `bard_lens`, `get_chronicle`, `bard_sense`, `bard_publish_passage`, `bard_publish_sync`, `bard_subscriber_loop`, `bard_decode`, `bard_export_lens`, `bard_scene`, `bard_tapestry`, `bard_weave_tapestry`
- public classes (1): `Chronicle`
- test files (2): `tests/test_bard.py`, `tests/test_loop_death_guards.py`
- readers (8): `mag/context_compression.py`, `mag/depin.py`, `mag/dropbox_watcher.py`, `mag/ghost.py`, `mag/lens_library.py`, `mag/primer.py`, `mag/riddler_campaign.py`, `mag/session_ritual.py`

### mag/bare_numpy.py

- lines: 148 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 10:30
- public functions (11): `zeros`, `ones`, `from_list`, `mean`, `amin`, `amax`, `normalize`, `dot`, `apply`, `magnitude`, `status`
- public classes (1): `BArray`
- test files (1): `tests/test_bare_numpy.py`
- readers (0): none

### mag/basecamp.py

- lines: 76 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-31 00:26
- public functions (2): `status`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/fireball_cycle.py`, `mag/organ_map.py`, `state/backups/orphan_close_20260906/organ_map.py`

### mag/bash_local.py

- lines: 289 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-07 10:05
- public functions (4): `build_row`, `append_row`, `verify`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/cage_intake.py`, `mag/reasoning_intake.py`, `mag/worldline_seed.py`

### mag/batch_drain.py

- lines: 230 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-24 17:05
- public functions (4): `launch`, `status`, `collect`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/batch_scribe.py`, `memory/runs/fuel_feed/detached/_test_real_detached.py`, `memory/runs/fuel_feed/detached/_test_real_survive.py`

### mag/batch_scribe.py

- lines: 205 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-24 16:56
- public functions (4): `classify`, `scribe`, `report`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `deploy/k8s/mag-scribe-cronjob.yaml`

### mag/bay_organs.py

- lines: 339 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-04 10:31
- public functions (13): `now_iso`, `pid_alive`, `atomic_write_json`, `writer_lock_path`, `write_writer_lock`, `read_lock`, `claim_dir`, `claim_path`, `claim_is_active`, `try_claim`, `release_claim`, `claim_active`, `sweep_expired`
- public classes (0): none
- test files (0): none
- readers (4): `mag/bay_organs_liveness_test.py`, `mag/claim_repair.py`, `mag/race_harness.py`, `mag/window_throttle.py`

### mag/bay_organs_liveness_test.py

- lines: 374 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-12 21:22
- public functions (7): `cleanup_test_files`, `spawn_claimant`, `kill_process`, `monitor_claim_release`, `run_race_test`, `run_liveness_test`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/behavior_catch.py

- lines: 249 | parse: ok | last commit: e96fd62a4 2026-08-07 | mtime: 2026-08-06 22:46
- public functions (3): `log_catch`, `try_voice_or_text_catch`, `seed_play_ladder_thrash_episode`
- public classes (0): none
- test files (0): none
- readers (2): `mag/framework_map.py`, `tools/thrash_meter.py`

### mag/behavioral_analytics.py

- lines: 316 | parse: ok | last commit: 482e0a3c8 2026-08-08 | mtime: 2026-08-08 19:11
- public functions (3): `extract_behavioral_signals`, `analyze_minute_signals`, `fingerprint_agent`
- public classes (0): none
- test files (0): none
- readers (6): `mag/ai_landscape.py`, `mag/cost_learn.py`, `mag/flock_usage_guard.py`, `mag/novelty_lens.py`, `mag/research_class.py`, `mag/usage_monitor.py`

### mag/behavioral_lensing.py

- lines: 486 | parse: ok | last commit: de7bb85fe 2026-08-09 | mtime: 2026-08-08 22:03
- public functions (1): `lens_the_pipeline`
- public classes (2): `AgentBehavioralProfile`, `BehavioralLenser`
- test files (0): none
- readers (1): `mag/agent_behavior.py`

### mag/behavioral_synth.py

- lines: 153 | parse: ok | last commit: e96fd62a4 2026-08-07 | mtime: 2026-08-06 22:46
- public functions (1): `synthesize_behavioral_leaf`
- public classes (0): none
- test files (2): `tests/test_decision_framework.py`, `tests/test_growth_cycle.py`
- readers (4): `mag/framework_map.py`, `mag/growth_cycle.py`, `mag/improve.py`, `mag/pro_library.py`

### mag/bernaise.py

- lines: 210 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 14:55
- public functions (5): `plant`, `emerge`, `promote`, `run`, `main`
- public classes (0): none
- test files (0): none
- readers (8): `experiments/cascade_whisper.yaml`, `mag/fish_ear.py`, `mag/frontier_gravity.py`, `mag/lens_tournament.py`, `mag/memlang.py`, `mag/novelty_lens.py`, `mag/research_class.py`, `mag/skill_pipeline.py`

### mag/billing_feed.py

- lines: 273 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 08:50
- public functions (3): `feed`, `gate`, `status`
- public classes (0): none
- test files (0): none
- readers (2): `mag/republic_loop.py`, `mag/surface_render.py`

### mag/biography.py

- lines: 598 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 13:55
- public functions (5): `already_summarized`, `mark_summarized`, `export_session_artifacts`, `pack_status`, `summarize_session`
- public classes (0): none
- test files (1): `tests/test_chat_source_agent_workday.py`
- readers (9): `configs/modules.yaml`, `dashboard/rest.py`, `mag/chat_source.py`, `mag/cli/core.py`, `mag/daemon.py`, `mag/health.py`, `mag/records.py`, `main.py` + 1 more

### mag/blade_plan.py

- lines: 150 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-29 04:27
- public functions (4): `boot_history`, `make_plan`, `write_plan`, `main`
- public classes (0): none
- test files (1): `tests/test_blade_plan.py`
- readers (0): none

### mag/blast.py

- lines: 575 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (11): `load_config`, `ensure_dirs`, `default_influence`, `read_influence`, `write_influence`, `read_status`, `ollama_ping`, `plant_status`, `start_blast`, `stop_blast`, `pause_blast`
- public classes (0): none
- test files (0): none
- readers (3): `dashboard/rest.py`, `mag/lattice_loop.py`, `main.py`

### mag/board_directive.py

- lines: 176 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 21:38
- public functions (2): `cmd_gate`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/board_tailer.py`

### mag/board_tailer.py

- lines: 246 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-31 00:49
- public functions (2): `poll`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/organ_map.py`, `state/backups/orphan_close_20260906/organ_map.py`

### mag/bonds.py

- lines: 485 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (4): `scan_conflicts`, `ingest_bonds`, `load_bonds_text`, `load_bonds_json`
- public classes (0): none
- test files (1): `tests/test_bonds_conflict_scan.py`
- readers (9): `configs/modules.yaml`, `dashboard/rest.py`, `mag/brief_local.py`, `mag/context_pack.py`, `mag/run_trail.py`, `mag/story.py`, `main.py`, `memory/portable_bags/bag-20260727T214646Z/configs/modules.yaml` + 1 more

### mag/bones_adapter.py

- lines: 390 | parse: ok | last commit: 0f34a8f3e 2026-09-16 | mtime: 2026-09-16 13:52
- public functions (8): `fmt_inline`, `fmt_any`, `fmt_block`, `no_session_msg`, `build_bot`, `load_token`, `callback_of`, `main`
- public classes (3): `BonesHub`, `BonesGroup`, `BonesClient`
- test files (1): `tests/test_bones_adapter.py`
- readers (0): none

### mag/bones_read.py

- lines: 141 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 10:15
- public functions (2): `check`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/aos_agent.py`

### mag/boot.py

- lines: 233 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-28 19:44
- public functions (2): `format_sancho`, `run_boot`
- public classes (0): none
- test files (0): none
- readers (1): `main.py`

### mag/boot_check.py

- lines: 183 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-05 21:34
- public functions (2): `snap`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/brain.py

- lines: 222 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 13:51
- public functions (2): `brain_pulse`, `brain_act`
- public classes (0): none
- test files (1): `tests/test_brain.py`
- readers (1): `dashboard/rest.py`

### mag/breakthrough_loop.py

- lines: 233 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 18:46
- public functions (4): `capture`, `status`, `run_cadence`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/brief_local.py

- lines: 226 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 14:00
- public functions (3): `resolve_session_id`, `collect_source`, `write_brief`
- public classes (0): none
- test files (0): none
- readers (4): `dashboard/rest.py`, `mag/biography.py`, `main.py`, `tools/visor.py`

### mag/browser_driver.py

- lines: 248 | parse: ok | last commit: a5dd96176 2026-09-25 | mtime: 2026-09-22 20:19
- public functions (5): `connect`, `open_url`, `ask`, `status`, `main`
- public classes (0): none
- test files (2): `tests/test_chatgpt_bot.py`, `tests/test_seat_steer.py`
- readers (18): `mag/ai_landscape.py`, `mag/billing_feed.py`, `mag/cdp_runner.py`, `mag/chatgpt_bot.py`, `mag/electron_seat.py`, `mag/free_frontend_swarm.py`, `mag/frontier_advisor.py`, `mag/frontier_batch.py` + 10 more

### mag/browser_env.py

- lines: 177 | parse: ok | last commit: e96fd62a4 2026-08-07 | mtime: 2026-08-06 18:49
- public functions (6): `load_config`, `host_from_url`, `is_host_allowed`, `is_window_allowed`, `status`, `ensure_config_file`
- public classes (0): none
- test files (2): `tests/test_launch_topology.py`, `tests/test_temperature_stack.py`
- readers (7): `configs/organs/host_resolver.yaml`, `mag/ai_landscape.py`, `mag/browser_driver.py`, `mag/lifecycle.py`, `mag/organ_map.py`, `mag/power.py`, `mag/temperature_stack.py`

### mag/btw_sidechannel.py

- lines: 192 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 21:32
- public functions (5): `inject`, `travel`, `sense`, `rightsize`, `status`
- public classes (0): none
- test files (0): none
- readers (2): `mag/republic_loop.py`, `mag/territory_solver.py`

### mag/budget_refactor.py

- lines: 164 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 11:00
- public functions (4): `waste`, `freed`, `plan`, `status`
- public classes (0): none
- test files (0): none
- readers (5): `mag/gap_frontier.py`, `mag/republic_feed.py`, `mag/republic_loop.py`, `mag/swarm_economics.py`, `mag/truth_audit.py`

### mag/build_audit.py

- lines: 144 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (3): `build_record`, `write_audit`, `load_audit`
- public classes (0): none
- test files (2): `tests/test_build_audit.py`, `tests/test_desk_observer.py`
- readers (5): `configs/coding_session_loop.yaml`, `configs/modules.yaml`, `mag/self_audit.py`, `main.py`, `scripts/_desk_step_cycle.py`

### mag/burn_gate.py

- lines: 80 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-07 11:03
- public functions (4): `now_pt`, `in_window`, `check`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/burn_steer.py

- lines: 260 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-10 08:08
- public functions (1): `steer`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/bus_cadence.py

- lines: 180 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-14 07:55
- public functions (3): `cadence`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (4): `mag/governor_autorun.py`, `tools/steer_all.py`, `tools/steer_grok_1m.py`, `tools/steer_grok_whole.py`

### mag/cache_identity.py

- lines: 510 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-07 09:39
- public functions (14): `load_body_text`, `compose_prefix`, `drift_byte`, `prompt_sha`, `marker_for`, `median`, `ollama_health`, `pick_model`, `chat_prefill`, `compute_metrics`, `verdict_tri_state`, `cmd_probe`, `cmd_check`, `main`
- public classes (0): none
- test files (1): `tests/test_cache_identity.py`
- readers (0): none

### mag/cache_map.py

- lines: 403 | parse: ok | last commit: a0f7a593a 2026-09-24 | mtime: 2026-09-24 19:11
- public functions (6): `is_remote`, `recent_hit_ratio`, `build_map`, `render_md`, `persist`, `main`
- public classes (0): none
- test files (1): `tests/test_verkle_compaction.py`
- readers (10): `mag/cache_router.py`, `mag/cache_watch.py`, `mag/cost_learn.py`, `mag/ghost.py`, `mag/novelty_lens.py`, `mag/right_size_skills.py`, `mag/self_steal.py`, `mag/usage_forecast.py` + 2 more

### mag/cache_router.py

- lines: 225 | parse: ok | last commit: a5dd96176 2026-09-25 | mtime: 2026-09-25 20:44
- public functions (5): `audit`, `route`, `simulate`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/novelty_lens.py`, `mag/self_steal.py`

### mag/cache_shard.py

- lines: 106 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 09:27
- public functions (4): `shard_key`, `route`, `volatile_redirect`, `status`
- public classes (0): none
- test files (0): none
- readers (2): `mag/invariant_ledger.py`, `mag/steal_pack.py`

### mag/cache_watch.py

- lines: 148 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-27 11:34
- public functions (3): `run`, `history`, `main`
- public classes (0): none
- test files (0): none
- readers (4): `mag/governor_autorun.py`, `mag/usage_digest.py`, `memory/runs/elder_asks/land_tripartite_knot.py`, `scripts/lite_fold_20260827.py`

### mag/cadence_learn.py

- lines: 199 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 21:35
- public functions (9): `ceiling`, `sysenv`, `headroom`, `learned_workers`, `throttled_workers`, `learn`, `status`, `sample`, `main`
- public classes (0): none
- test files (1): `tests/test_loop_death_guards.py`
- readers (6): `mag/autodrain.py`, `mag/governor_autorun.py`, `mag/manifest.py`, `mag/real_swarm.py`, `mag/standing.py`, `mag/work_loop.py`

### mag/cage_intake.py

- lines: 332 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-07 10:10
- public functions (6): `parse_job_card`, `persona_of`, `filedate_of`, `seal`, `census`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/campaign.py

- lines: 781 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-04 11:13
- public functions (8): `load_module`, `load_riddler_map`, `dm_narrate`, `inject_scheduled_steers`, `party_member_turn`, `dm_judge`, `measure_room`, `run_campaign`
- public classes (1): `CampaignState`
- test files (1): `tests/test_campaign.py`
- readers (10): `mag/cross_version.py`, `mag/game_dm.py`, `mag/ghost_cross.py`, `mag/research_director.py`, `main.py`, `memory/trash/20260810T202850Z/_tmp_campaign_test.py`, `memory/trash/20260810T202850Z/_tmp_research_sprint.py`, `scripts/build_vislab_catalog.py` + 2 more

### mag/campaign_reader.py

- lines: 151 | parse: ok | last commit: de7bb85fe 2026-08-09 | mtime: 2026-08-08 23:49
- public functions (3): `list_campaigns`, `read_campaign`, `export_all`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/campaign_runs.py

- lines: 145 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-15 05:39
- public functions (2): `run_session`, `status`
- public classes (0): none
- test files (0): none
- readers (2): `mag/game_observer.py`, `mag/governor_autorun.py`

### mag/campaign_simulator.py

- lines: 401 | parse: ok | last commit: de7bb85fe 2026-08-09 | mtime: 2026-08-09 00:13
- public functions (2): `get_simulator`, `play_campaign`
- public classes (3): `SimulatedTurn`, `SessionLog`, `CampaignSimulator`
- test files (0): none
- readers (0): none

### mag/canon_gate.py

- lines: 142 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-04 21:10
- public functions (4): `parse_header`, `check_doc`, `stamp_doc`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/canon_seal.py

- lines: 96 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-05 21:52
- public functions (3): `seal`, `verify`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/canvas_bridge.py

- lines: 460 | parse: ok | last commit: 2464edcba 2026-08-04 | mtime: 2026-08-04 18:48
- public functions (4): `parse_canvas_tsx`, `list_viewports`, `load_viewport`, `sync_canvases`
- public classes (0): none
- test files (1): `tests/test_canvas_bridge.py`
- readers (2): `dashboard/rest.py`, `main.py`

### mag/capability_steal.py

- lines: 249 | parse: ok | last commit: 790145ab1 2026-09-26 | mtime: 2026-09-26 01:43
- public functions (5): `steal_search`, `test_local`, `expand`, `source_hint`, `main`
- public classes (0): none
- test files (1): `tests/test_loop_death_guards.py`
- readers (3): `mag/afk_orchestrator.py`, `mag/novelty_lens.py`, `mag/skill_pipeline.py`

### mag/capture_guard.py

- lines: 137 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 22:54
- public functions (3): `audit`, `doctrine`, `status`
- public classes (0): none
- test files (0): none
- readers (1): `mag/republic_loop.py`

### mag/cascade_research.py

- lines: 246 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-10 17:55
- public functions (6): `keywords`, `tier1`, `tier2`, `run`, `render`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/desk_tools.py`

### mag/cast_guard.py

- lines: 141 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-01 21:00
- public functions (4): `rate_limited`, `blocked`, `guard`, `status`
- public classes (0): none
- test files (0): none
- readers (4): `mag/cast_server.py`, `mag/invariant_ledger.py`, `mag/novelty_lens.py`, `mag/research_class.py`

### mag/cast_launch.py

- lines: 71 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-13 09:27
- public functions (2): `launch`, `status`
- public classes (0): none
- test files (0): none
- readers (1): `backend/server.py`

### mag/cast_server.py

- lines: 359 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 13:36
- public functions (2): `render_cast_page`, `run`
- public classes (1): `Handler`
- test files (1): `tests/test_cast_server.py`
- readers (8): `mag/cast_launch.py`, `mag/corpus_wave.py`, `mag/novelty_lens.py`, `mag/openclaw_catalog.py`, `mag/research_class.py`, `mag/runtime.py`, `main.py`, `memory/runs/union_audit/_write_jsonl.py`

### mag/castle_foundation.py

- lines: 166 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 11:54
- public functions (5): `castles`, `shadow`, `foundation`, `wave`, `status`
- public classes (0): none
- test files (0): none
- readers (2): `mag/republic_loop.py`, `mag/rib_os.py`

### mag/catalog.py

- lines: 193 | parse: ok | last commit: 3aafe78a0 2026-09-16 | mtime: 2026-09-16 07:19
- public functions (8): `zone_of`, `title_of`, `iter_files`, `cmd_scan`, `load_rows`, `cmd_find`, `cmd_stats`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `scripts/build_knowledge_graph.py`

### mag/catalog_freshness.py

- lines: 93 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 15:24
- public functions (3): `manifest_freshness`, `map_freshness`, `corpus_status`
- public classes (0): none
- test files (1): `tests/test_catalog_freshness.py`
- readers (2): `mag/catalog_rescan.py`, `tools/corpus.py`

### mag/catalog_rebuild.py

- lines: 150 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 15:09
- public functions (2): `rebuild`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/catalog_rescan.py

- lines: 385 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 16:46
- public functions (6): `load_index`, `walk_disk`, `incremental`, `rebuild`, `write_manifest`, `main`
- public classes (0): none
- test files (2): `tests/test_catalog_rescan.py`, `tests/test_catalog_tags.py`
- readers (3): `mag/catalog_freshness.py`, `mag/catalog_tags.py`, `scripts/corpus_rescan_daily.ps1`

### mag/catalog_scan.py

- lines: 332 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 12:15
- public functions (5): `zone_of`, `classify_target`, `reparse_record`, `scan_tree`, `main`
- public classes (0): none
- test files (2): `tests/test_catalog_scan_junctions.py`, `tests/test_corpus_path_seam.py`
- readers (5): `mag/catalog_rebuild.py`, `mag/catalog_rescan.py`, `scripts/build_knowledge_graph.py`, `tools/corpus.py`, `tools/queue_close.py`

### mag/catalog_tags.py

- lines: 210 | parse: ok | last commit: 4b5a4ab37 2026-09-28 | mtime: 2026-09-28 12:43
- public functions (5): `classify_kind`, `age_class_of`, `owner_of`, `run_tags`, `write_tag_report`
- public classes (0): none
- test files (1): `tests/test_catalog_tags.py`
- readers (1): `mag/catalog_rescan.py`

### mag/caveman_audit.py

- lines: 139 | parse: ok | last commit: d7a61db31 2026-08-05 | mtime: 2026-08-06 18:28
- public functions (2): `run_audit`, `format_report`
- public classes (0): none
- test files (1): `tests/test_skill_seat.py`
- readers (3): `mag/self_audit.py`, `mag/skill_seat.py`, `main.py`

### mag/cdp_runner.py

- lines: 98 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-13 21:00
- public functions (5): `run`, `steer_electron`, `ask_browser`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/frontier_game.py`

### mag/census_liveness.py

- lines: 73 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 16:31
- public functions (2): `patrol_status`, `report`
- public classes (0): none
- test files (1): `tests/test_census_liveness.py`
- readers (1): `main.py`

### mag/chain_guard.py

- lines: 212 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 16:37
- public functions (3): `mark`, `check`, `main`
- public classes (0): none
- test files (2): `tests/test_chain_byte_exact_io.py`, `tests/test_verkle_compaction.py`
- readers (4): `mag/chord.py`, `mag/verkle_compaction.py`, `memory/research_packs/_t15_agm_check.py`, `scripts/backup_chain.py`

### mag/chain_query.py

- lines: 297 | parse: ok | last commit: 482e0a3c8 2026-08-08 | mtime: 2026-08-08 19:05
- public functions (1): `chain_query_endpoint`
- public classes (1): `ChainQuery`
- test files (0): none
- readers (22): `mag/bard.py`, `mag/behavioral_analytics.py`, `mag/cost_enforcer.py`, `mag/depin.py`, `mag/doctor.py`, `mag/doctor_agent.py`, `mag/exit_dialogue.py`, `mag/game_dfhack.py` + 14 more

### mag/chain_substrate.py

- lines: 195 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 10:17
- public functions (8): `sense`, `core`, `surface`, `world`, `vmem`, `heartbeat`, `pulse`, `status`
- public classes (0): none
- test files (0): none
- readers (4): `mag/final_steal.py`, `mag/republic_loop.py`, `mag/self_loop.py`, `tools/verb_anchor.py`

### mag/chan.py

- lines: 338 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 12:48
- public functions (11): `room_path`, `slugify`, `paint_tool`, `trip_id`, `is_play_post`, `seed_keep`, `catalog`, `thread`, `post`, `wake`, `main`
- public classes (0): none
- test files (1): `tests/test_chan.py`
- readers (2): `dashboard/rest.py`, `mag/hood.py`

### mag/chat_source.py

- lines: 482 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 18:48
- public functions (10): `agent_bio_id`, `agent_local_id`, `agent_session_path`, `resolve_chat`, `extract_turns_from_messages`, `extract_turns_from_jsonl`, `extract_turns`, `list_agent_session_ids`, `file_agent_session`, `file_dirty_agent_sessions`
- public classes (1): `ChatRef`
- test files (2): `tests/test_agent_desk.py`, `tests/test_chat_source_agent_workday.py`
- readers (7): `mag/agent_cli.py`, `mag/agent_desk.py`, `mag/biography.py`, `mag/daemon.py`, `mag/health.py`, `mag/steer_telemetry.py`, `main.py`

### mag/chatgpt_bot.py

- lines: 150 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 17:16
- public functions (5): `spec`, `steer`, `test_artifact`, `heartbeat`, `status`
- public classes (0): none
- test files (1): `tests/test_chatgpt_bot.py`
- readers (3): `mag/frontier_advisor.py`, `mag/republic_loop.py`, `mag/self_steal.py`

### mag/chatgpt_desktop.py

- lines: 196 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-13 20:33
- public functions (5): `connect`, `steer`, `heartbeat`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/cheap_swarm.py

- lines: 222 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-24 08:15
- public functions (5): `scan`, `dispatch`, `run_cadence`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (6): `dashboard/rest.py`, `mag/doctor.py`, `mag/ghost.py`, `mag/governor_autorun.py`, `mag/republic_os.py`, `main.py`

### mag/checkin_route.py

- lines: 391 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-28 19:47
- public functions (4): `structure_checkin_plan`, `probe_router_network`, `start_checkin`, `checkin_status`
- public classes (0): none
- test files (0): none
- readers (3): `mag/refine_chain.py`, `memory/runs/job_floor/20260828-codex-lab/launch_panel.py`, `memory/runs/union_audit/_write_jsonl.py`

### mag/chord.py

- lines: 112 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-26 12:06
- public functions (2): `strike`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/chord_circuit.py

- lines: 243 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-24 11:08
- public functions (5): `origin`, `strike`, `ring`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/standing.py`

### mag/chord_lens.py

- lines: 354 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (5): `score_charts`, `detect_loops`, `locus_audit`, `build_chord_strike`, `json_dumps_stable`
- public classes (0): none
- test files (0): none
- readers (1): `mag/session_dossier.py`

### mag/chord_pipeline.py

- lines: 202 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 08:50
- public functions (5): `grab`, `ingest`, `shape_learn`, `route_work`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/republic_loop.py`

### mag/chord_triangulate.py

- lines: 199 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-06 14:19
- public functions (5): `fetch`, `parse_ts`, `scan`, `render`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `memory/runs/x_history_mine/20260926/remote_day_slice_ingest.py`, `memory/runs/x_history_mine/20260926/remote_id_fill_ingest.py`

### mag/chronicle.py

- lines: 132 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (1): `build_chronicle_payload`
- public classes (0): none
- test files (2): `tests/test_display.py`, `tests/test_stack.py`
- readers (4): `dashboard/rest.py`, `mag/display.py`, `mag/game_live.py`, `mag/stack.py`

### mag/cite_gate.py

- lines: 453 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-07 01:30
- public functions (9): `is_claim_line`, `extract_key_terms`, `subject_match`, `fetch_url`, `extract_citations`, `check_card`, `write_state`, `selftest`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/perturbation_battery.py`, `mag/quorum_window.py`

### mag/cites_at_birth.py

- lines: 103 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-06 18:16
- public functions (2): `check`, `edges`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/claim_repair.py

- lines: 471 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-05 00:08
- public functions (10): `compact_ts`, `iso_ts`, `repair_root_for`, `queue_dir`, `state_path`, `classify_file`, `scan`, `work_state`, `repair`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/claims_desk.py

- lines: 190 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 14:32
- public functions (6): `start_state`, `root`, `play`, `replay`, `run`, `verify`
- public classes (0): none
- test files (0): none
- readers (1): `mag/claims_verify.py`

### mag/claims_verify.py

- lines: 124 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 14:32
- public functions (1): `run`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/claritas.py

- lines: 64 | parse: ok | last commit: 86628c678 2026-09-24 | mtime: 2026-09-24 19:30
- public functions (2): `vendor_for`, `face_for`
- public classes (0): none
- test files (0): none
- readers (5): `seed/engines/build_seed.py`, `seed/engines/stealth_sweep.py`, `tools/build_seed.py`, `tools/seed_v2.py`, `tools/stealth_sweep.py`

### mag/clawbot.py

- lines: 197 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-13 04:52
- public functions (6): `claw_spec`, `deliver`, `watch`, `deliver_drift`, `spelunker`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/republic_loop.py`

### mag/cleanup.py

- lines: 148 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-13 08:16
- public functions (4): `audit`, `cleanup`, `run_cadence`, `main`
- public classes (0): none
- test files (1): `tests/test_cleanup.py`
- readers (5): `dashboard/rest.py`, `mag/governor_autorun.py`, `mag/tool_retire.py`, `main.py`, `memory/runs/union_audit/_write_jsonl.py`

### mag/cleanup_steal.py

- lines: 120 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 11:13
- public functions (3): `map_`, `steal`, `status`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/cli/__init__.py

- lines: 26 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (0): none
- public classes (0): none
- test files (0): none
- readers (2): `mag/cli/display.py`, `mag/corpus_wave.py`

### mag/cli/core.py

- lines: 186 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (5): `cmd_run`, `cmd_status`, `cmd_ingest_result`, `add_parser`, `dispatch`
- public classes (0): none
- test files (0): none
- readers (1): `mag/cli/__init__.py`

### mag/cli/display.py

- lines: 128 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (15): `green`, `red`, `yellow`, `cyan`, `bold`, `dim`, `badge`, `hr`, `section`, `kv`, `box`, `table`, `ok_line`, `err_line`, `warn_line`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/clippy.py

- lines: 233 | parse: ok | last commit: 60e18c524 2026-08-08 | mtime: 2026-08-07 18:50
- public functions (5): `clippy`, `propose_actions`, `record_choice`, `choose`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/framework_map.py`, `main.py`

### mag/code_map.py

- lines: 218 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-09 21:53
- public functions (5): `scan`, `build`, `main`, `distill`, `distilled`
- public classes (0): none
- test files (0): none
- readers (2): `mag/ai_landscape.py`, `memory/trash/20260810T202850Z/_tmp_distill.py`

### mag/codex_seat.py

- lines: 151 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-24 15:46
- public functions (2): `status`, `run`
- public classes (0): none
- test files (0): none
- readers (1): `mag/seat_probe.py`

### mag/coding_session_loop.py

- lines: 556 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 13:58
- public functions (7): `load_config`, `seed_desk`, `run_preflight`, `close_session_if_ready`, `session_status`, `run_board_step`, `main`
- public classes (0): none
- test files (6): `tests/test_coding_session_loop.py`, `tests/test_coding_session_orchestrator.py`, `tests/test_coding_session_runner.py`, `tests/test_desk_observer.py`, `tests/test_factory_machine.py`, `tests/test_scripts_path_pins.py`
- readers (8): `dashboard/rest.py`, `mag/coding_session_orchestrator.py`, `mag/coding_session_runner.py`, `mag/desk_observer.py`, `mag/factory_machine.py`, `main.py`, `memory/runs/union_audit/_write_jsonl.py`, `scripts/_desk_step_cycle.py`

### mag/coding_session_orchestrator.py

- lines: 395 | parse: ok | last commit: 7654afe52 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (6): `active_sprint_key`, `assess_sprint_status`, `recommend_desk_action`, `plan_session`, `advance_sprint_if_ready`, `orchestrator_tick`
- public classes (0): none
- test files (3): `tests/test_coding_session_orchestrator.py`, `tests/test_coding_session_runner.py`, `tests/test_desk_observer.py`
- readers (9): `configs/modules.yaml`, `dashboard/rest.py`, `mag/coding_session_loop.py`, `mag/coding_session_runner.py`, `mag/desk_observer.py`, `mag/factory_machine.py`, `mag/framework_map.py`, `mag/handoff_inbox.py` + 1 more

### mag/coding_session_runner.py

- lines: 402 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (2): `build_run_report`, `run_until_done`
- public classes (0): none
- test files (1): `tests/test_coding_session_runner.py`
- readers (4): `dashboard/rest.py`, `mag/factory_machine.py`, `mag/framework_map.py`, `main.py`

### mag/comms_trail.py

- lines: 261 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 22:46
- public functions (6): `capture`, `confirm_language`, `status`, `consumption_signal`, `run_cadence`, `main`
- public classes (0): none
- test files (1): `tests/test_router_comms_boost.py`
- readers (7): `dashboard/rest.py`, `mag/cleanup_steal.py`, `mag/doctor.py`, `mag/ghost.py`, `mag/governor_autorun.py`, `mag/router.py`, `main.py`

### mag/compass.py

- lines: 248 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 17:31
- public functions (9): `decisions_log_path`, `constitution_text`, `blueprint_text`, `last_state_text`, `recent_decisions`, `record_decision`, `differential_state`, `build_compass`, `should_compass`
- public classes (0): none
- test files (1): `tests/test_decision_framework.py`
- readers (9): `mag/agent_cli.py`, `mag/context_pack.py`, `mag/decision_framework.py`, `mag/framework_map.py`, `mag/governance.py`, `mag/governor.py`, `mag/operator_inbox.py`, `mag/tesuji_shell.py` + 1 more

### mag/compiler_flywheel.py

- lines: 178 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 13:13
- public functions (3): `beat`, `run`, `status`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/compiler_lang.py

- lines: 277 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 10:17
- public functions (5): `corpus`, `ingest`, `expand`, `learned_lexicon`, `status`
- public classes (0): none
- test files (0): none
- readers (1): `mag/republic_loop.py`

### mag/compute_reconcile.py

- lines: 201 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 13:15
- public functions (4): `measure`, `reconcile`, `run_cadence`, `status`
- public classes (0): none
- test files (1): `tests/test_compute_reconcile.py`
- readers (3): `mag/console_render.py`, `mag/governor_autorun.py`, `state/vast/governor.py`

### mag/concurrency_gate.py

- lines: 154 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-05 23:39
- public functions (4): `acquire`, `release`, `status`, `hold`
- public classes (0): none
- test files (0): none
- readers (12): `_alpha_rar.py`, `_alpha_steer.py`, `_cache_mine.py`, `_test_legibility.py`, `mag/_conc_test_slot.py`, `mag/_verify_concurrency_gate.py`, `mag/glm_flash.py`, `mag/overseer.py` + 4 more

### mag/conductor.py

- lines: 190 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (3): `detect_phase`, `phase_policy`, `conduct`
- public classes (0): none
- test files (3): `tests/test_factory_freeze_gate.py`, `tests/test_skill_seat.py`, `tests/test_v3_modules.py`
- readers (11): `configs/modules.yaml`, `mag/conductor_eval.py`, `mag/cost_simulator.py`, `mag/framework_map.py`, `mag/governor_autorun.py`, `mag/operating_protocol.py`, `mag/organ_map.py`, `mag/switchboard.py` + 3 more

### mag/conductor_eval.py

- lines: 85 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 14:02
- public functions (2): `load_suite`, `run_eval`
- public classes (0): none
- test files (1): `tests/test_conductor_eval.py`
- readers (2): `main.py`, `memory/runs/union_audit/_write_jsonl.py`

### mag/connectivity_sizer.py

- lines: 216 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 19:29
- public functions (4): `scan`, `classify`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/console_render.py

- lines: 124 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-13 08:54
- public functions (4): `tools`, `show`, `render_artifact`, `status`
- public classes (0): none
- test files (0): none
- readers (2): `mag/governor_autorun.py`, `mag/openclaw_catalog.py`

### mag/constants.py

- lines: 6 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-12 21:58
- public functions (0): none
- public classes (0): none
- test files (0): none
- readers (1): `mag/spore_seed.py`

### mag/constitutional_critique.py

- lines: 605 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 16:38
- public functions (6): `load_constitution`, `critique`, `get_filter`, `filter_response`, `critique_dry_run`, `critique_stats`
- public classes (2): `CritiqueResult`, `ConstitutionalFilter`
- test files (0): none
- readers (5): `mag/context_compression.py`, `mag/copilot_bridge.py`, `mag/ghost.py`, `mag/preflight.py`, `mag/sovereign_dashboard.py`

### mag/context_admission.py

- lines: 102 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 12:50
- public functions (3): `assess`, `write_receipt`, `safe_write_receipt`
- public classes (0): none
- test files (1): `tests/test_context_admission.py`
- readers (3): `mag/agent_cli.py`, `mag/organ_map.py`, `state/backups/orphan_close_20260906/organ_map.py`

### mag/context_checkpoint.py

- lines: 474 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 12:51
- public functions (6): `compute_switch_economics`, `get_engine`, `checkpoint_turn`, `restore_pointer`, `switch_model`, `switch_economics`
- public classes (2): `ContextCheckpoint`, `CheckpointEngine`
- test files (2): `tests/test_context_admission.py`, `tests/test_context_checkpoint_pack.py`
- readers (8): `mag/context_pack.py`, `mag/copilot_bridge.py`, `mag/ghost.py`, `mag/organ_map.py`, `mag/preflight.py`, `memory/runs/union_audit/_write_jsonl.py`, `state/backups/orphan_close_20260906/organ_map.py`, `tools/steer_grok_1m.py`

### mag/context_compression.py

- lines: 490 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 12:51
- public functions (11): `estimate_tokens`, `algorithmic_compress`, `llm_compress`, `compress`, `verify_compression`, `compress_ghost_identity`, `compress_bard_identity`, `compress_constitution_prompt`, `load_compressed`, `compute_savings`, `compression_dashboard`
- public classes (1): `CompressionResult`
- test files (1): `tests/test_context_admission.py`
- readers (4): `mag/ai_landscape.py`, `mag/ghost.py`, `mag/preflight.py`, `memory/runs/union_audit/_write_jsonl.py`

### mag/context_growth.py

- lines: 173 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 08:45
- public functions (4): `analyze`, `render_md`, `run_cadence`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/governor_autorun.py`, `main.py`

### mag/context_pack.py

- lines: 1362 | parse: ok | last commit: a23928aca 2026-09-27 | mtime: 2026-09-28 13:29
- public functions (6): `freeze_system_prompt`, `evolving_tail`, `build_context_pack`, `infer_pack_mode`, `format_context_pack_text`, `format_agent_preamble`
- public classes (0): none
- test files (9): `tests/test_context_checkpoint_pack.py`, `tests/test_context_freeze.py`, `tests/test_context_pack_quantized_laws.py`, `tests/test_coordination.py`, `tests/test_dirac_loop.py`, `tests/test_mirror_voice_pack.py`, `tests/test_pack_modes_steward.py`, `tests/test_v3_modules.py` + 1 more
- readers (19): `configs/modules.yaml`, `dashboard/rest.py`, `mag/agent_cli.py`, `mag/autorun_common.py`, `mag/coordination.py`, `mag/dashboard_plugin.py`, `mag/decision_framework.py`, `mag/dispatch.py` + 11 more

### mag/cooker.py

- lines: 164 | parse: ok | last commit: 86628c678 2026-09-24 | mtime: 2026-09-24 19:32
- public functions (4): `window_start`, `next_reset`, `status`, `fire_due`
- public classes (0): none
- test files (0): none
- readers (4): `seed/engines/build_seed.py`, `seed/engines/cooker.py`, `tools/build_seed.py`, `tools/seed_v2.py`

### mag/coordination.py

- lines: 390 | parse: ok | last commit: 36914e134 2026-08-07 | mtime: 2026-08-07 07:45
- public functions (6): `log_activity`, `read_activity`, `activity_summary`, `format_activity_excerpt`, `classify_depth`, `coordinate`
- public classes (0): none
- test files (2): `tests/test_coordination.py`, `tests/test_router.py`
- readers (12): `dashboard/rest.py`, `mag/agent_cli.py`, `mag/autorun_status.py`, `mag/context_pack.py`, `mag/dashboard_plugin.py`, `mag/governor_autorun.py`, `mag/peer_handoff.py`, `mag/router.py` + 4 more

### mag/copilot_bridge.py

- lines: 380 | parse: ok | last commit: de7bb85fe 2026-08-09 | mtime: 2026-08-08 23:07
- public functions (6): `find_transcript_path`, `parse_transcript`, `copilot_sync_loop`, `get_bridge`, `bridge_sync`, `bridge_status`
- public classes (3): `CopilotTurn`, `BridgeResult`, `CopilotBridge`
- test files (0): none
- readers (3): `mag/data_refinery.py`, `mag/preflight.py`, `mag/sovereign_dashboard.py`

### mag/corpus_expand.py

- lines: 150 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 18:38
- public functions (5): `sources`, `harvest`, `ingest`, `expand`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/ai_landscape.py`, `mag/skill_pipeline.py`, `mag/x_surface.py`

### mag/corpus_ingest.py

- lines: 207 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 08:50
- public functions (4): `ingest`, `shadow_work`, `shape_spec`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/republic_loop.py`

### mag/corpus_query.py

- lines: 433 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-14 19:00
- public functions (3): `query`, `inspire_for_scene`, `format_inspiration_footer`
- public classes (0): none
- test files (0): none
- readers (4): `mag/game_brawl.py`, `mag/game_campaign.py`, `mag/game_dm_voice.py`, `memory/runs/union_audit/_write_jsonl.py`

### mag/corpus_selfsteal.py

- lines: 321 | parse: ok | last commit: 5305a99b1 2026-09-16 | mtime: 2026-09-15 22:11
- public functions (6): `index`, `map_battery`, `held`, `pack`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/corpus_wave.py

- lines: 179 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 11:43
- public functions (5): `tally`, `understand`, `optimize`, `apply_to_all`, `status`
- public classes (0): none
- test files (0): none
- readers (1): `mag/vantage_audit.py`

### mag/cost_enforcer.py

- lines: 486 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 18:46
- public functions (10): `get_caps`, `update_caps`, `load_cost_ledger`, `log_call`, `get_current_spend`, `check_caps`, `enforce_caps`, `kill_all_agents_manual`, `cost_enforcer_loop`, `cost_status`
- public classes (0): none
- test files (1): `tests/test_loop_death_guards.py`
- readers (6): `dashboard/server.py`, `mag/ai_landscape.py`, `mag/ghost.py`, `mag/ghost_ledger.py`, `mag/task_router.py`, `memory/runs/union_audit/_write_jsonl.py`

### mag/cost_governor.py

- lines: 210 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 20:06
- public functions (9): `price_usd`, `spend`, `proven_useful`, `ceiling`, `check`, `record`, `mark_abandoned`, `summary`, `sweep_abandoned`
- public classes (0): none
- test files (0): none
- readers (1): `mag/swarm_worker.py`

### mag/cost_learn.py

- lines: 341 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 09:04
- public functions (6): `analyze`, `render_leaf`, `fold`, `recent_cost_evidence`, `run_cadence`, `main`
- public classes (0): none
- test files (0): none
- readers (15): `mag/ai_landscape.py`, `mag/doctor.py`, `mag/emergence.py`, `mag/flex_test.py`, `mag/governor_autorun.py`, `mag/grok_weave.py`, `mag/lens_knot.py`, `mag/model_pick.py` + 7 more

### mag/cost_ledger.py

- lines: 104 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 20:13
- public functions (2): `task_estimate`, `emit_terminal`
- public classes (0): none
- test files (1): `tests/test_cost_ledger.py`
- readers (4): `mag/framework_map.py`, `mag/orchestrator.py`, `mag/time_estimate.py`, `memory/runs/union_audit/_write_jsonl.py`

### mag/cost_simulator.py

- lines: 216 | parse: ok | last commit: bc61ef178 2026-08-05 | mtime: 2026-08-06 18:28
- public functions (4): `estimate_goal`, `estimate_wave`, `format_wave_text`, `main`
- public classes (0): none
- test files (1): `tests/test_cost_simulator.py`
- readers (3): `mag/cost_ledger.py`, `mag/operating_protocol.py`, `main.py`

### mag/cost_truth.py

- lines: 597 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 19:10
- public functions (3): `price_tokens`, `aggregate_rows`, `snapshot`
- public classes (0): none
- test files (2): `tests/test_cost_truth.py`, `tests/test_dormant_gate_b2133.py`
- readers (5): `dashboard/rest.py`, `dashboard/server.py`, `mag/cost_governor.py`, `mag/cost_ledger.py`, `mag/dormant.py`

### mag/cross_version.py

- lines: 628 | parse: ok | last commit: 60e18c524 2026-08-08 | mtime: 2026-08-08 07:07
- public functions (8): `load_experiment_config`, `load_mode_config`, `list_modules`, `snapshot_state`, `apply_mode_settings`, `run_campaign_module`, `run_experiment`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `configs/mag.yaml`, `main.py`, `tools/compare_versions.py`

### mag/daemon.py

- lines: 195 | parse: ok | last commit: 02d818bf7 2026-09-26 | mtime: 2026-09-26 00:41
- public functions (2): `run_cycle`, `run_loop`
- public classes (0): none
- test files (1): `tests/test_loop_death_guards.py`
- readers (4): `mag/__init__.py`, `mag/legacy_audit.py`, `mag/runtime.py`, `main.py`

### mag/dashboard_plugin.py

- lines: 105 | parse: ok | last commit: 36914e134 2026-08-07 | mtime: 2026-08-07 08:47
- public functions (1): `build_dashboard_plugin`
- public classes (1): `DashboardPlugin`
- test files (1): `tests/test_dashboard_plugin.py`
- readers (0): none

### mag/data_refinery.py

- lines: 849 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 00:04
- public functions (2): `get_refinery`, `refine_all`
- public classes (2): `TrainingExample`, `DataRefinery`
- test files (0): none
- readers (1): `memory/runs/union_audit/_write_jsonl.py`

### mag/data_source_watch.py

- lines: 161 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 15:41
- public functions (4): `plan`, `observe`, `watch`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/afk_orchestrator.py`, `mag/memlang.py`, `mag/skill_pipeline.py`

### mag/decision_framework.py

- lines: 322 | parse: ok | last commit: 60e18c524 2026-08-08 | mtime: 2026-08-07 18:30
- public functions (6): `surface_tips`, `format_tips_block`, `build_framework_context`, `decide`, `escalate_on_loop`, `session_loop_patterns`
- public classes (0): none
- test files (1): `tests/test_decision_framework.py`
- readers (9): `dashboard/rest.py`, `mag/agent_cli.py`, `mag/behavioral_synth.py`, `mag/brain.py`, `mag/context_pack.py`, `mag/framework_map.py`, `mag/operator_inbox.py`, `mag/system_map.py` + 1 more

### mag/decision_hook.py

- lines: 90 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-05 21:38
- public functions (2): `sweep`, `mark_done`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/decl_attention.py

- lines: 740 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-06 10:39
- public functions (16): `build_table`, `parse_declarations`, `plan_visible`, `read_visible`, `naive_read`, `extract`, `extract_last`, `answer`, `run_quiz`, `demo`, `build_topic_adjacency`, `forecast_prefetch`, `baseline_prefetch`, `run_walk`, `forecast_demo`, `main`
- public classes (4): `Block`, `Table`, `Span`, `WalkStep`
- test files (0): none
- readers (0): none

### mag/deep_research_moonshot.py

- lines: 234 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-13 07:44
- public functions (4): `synthesize`, `moonshot`, `cadence`, `status`
- public classes (0): none
- test files (1): `tests/test_deep_research_moonshot.py`
- readers (1): `mag/governor_autorun.py`

### mag/depin.py

- lines: 574 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 07:16
- public functions (3): `discover_local_skills`, `generate_work_proof`, `verify_work_proof`
- public classes (5): `SkillNFT`, `MarketplaceOrder`, `SkillRegistry`, `DepinTransaction`, `DepinMarketplace`
- test files (0): none
- readers (1): `memory/runs/union_audit/_write_jsonl.py`

### mag/desk_conductor.py

- lines: 779 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 07:47
- public functions (9): `conductor_model`, `conductor_backend`, `recommend_action`, `build_seat_fidelity`, `apply_scratch_update`, `apply_conductor_canvas_edit`, `conductor_glance`, `frontier_compact_commit`, `conductor_tick`
- public classes (0): none
- test files (1): `tests/test_desk_conductor.py`
- readers (6): `configs/lanes.yaml`, `configs/modules.yaml`, `dashboard/rest.py`, `mag/coding_session_loop.py`, `mag/coding_session_orchestrator.py`, `memory/runs/union_audit/_write_jsonl.py`

### mag/desk_dialogue.py

- lines: 1357 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-08 19:56
- public functions (18): `desk_steering_enabled`, `post_desk_steer`, `refresh_local_desk`, `read_operator_manual`, `read_first_user_model`, `read_trust_status`, `read_cursor`, `write_cursor`, `heal_canvas`, `desk_health_check`, `reset_dialogue`, `wipe_board`, `meta_dialogue_turn`, `meta_discuss`, `dialogue_turn`, `slow_wake`, `handoff_loop`, `ping_pong`
- public classes (0): none
- test files (7): `tests/test_coding_session_loop.py`, `tests/test_coding_session_orchestrator.py`, `tests/test_desk_conductor.py`, `tests/test_desk_dialogue.py`, `tests/test_desk_timing.py`, `tests/test_roadmap_gap_probe.py`, `tests/test_stack.py`
- readers (15): `configs/modules.yaml`, `dashboard/rest.py`, `mag/brain.py`, `mag/coding_session_loop.py`, `mag/desk_conductor.py`, `mag/desk_observer.py`, `mag/desk_orchestrator_memory.py`, `mag/desk_overseer.py` + 7 more

### mag/desk_local_adapter.py

- lines: 174 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (7): `extract_move_line`, `canvas_fingerprint`, `canvas_quality`, `format_local_canvas`, `normalize_local_canvas_edit`, `local_heading_stall_detected`, `echo_without_commit_detected`
- public classes (0): none
- test files (1): `tests/test_desk_local_adapter.py`
- readers (7): `mag/desk_conductor.py`, `mag/desk_dialogue.py`, `mag/desk_observer.py`, `mag/desk_orchestrator_memory.py`, `mag/desk_overseer.py`, `mag/desk_teaching.py`, `mag/local_playbook.py`

### mag/desk_local_simulator.py

- lines: 29 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (1): `respond`
- public classes (0): none
- test files (0): none
- readers (1): `mag/desk_dialogue.py`

### mag/desk_model_probe.py

- lines: 226 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (2): `ensure_qwen_desk`, `run_probe`
- public classes (0): none
- test files (1): `tests/test_local_gpu_probes.py`
- readers (3): `mag/gstd_probe.py`, `main.py`, `state/vast/sizer.py`

### mag/desk_observer.py

- lines: 353 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (6): `collect_observer_context`, `score_turn_rules`, `build_steer_packet`, `inject_steer`, `verify_sprint_handoff`, `observer_tick`
- public classes (0): none
- test files (1): `tests/test_desk_observer.py`
- readers (3): `mag/coding_session_loop.py`, `mag/coding_session_orchestrator.py`, `mag/thread_eye.py`

### mag/desk_ops.py

- lines: 200 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 06:12
- public functions (10): `lab_up`, `cast_up`, `lab_pid`, `restart_lab`, `desk_post`, `desk_refresh`, `desk_wipe`, `desk_reset`, `desk_local_only`, `desk_reload`
- public classes (0): none
- test files (0): none
- readers (2): `main.py`, `memory/runs/union_audit/_write_jsonl.py`

### mag/desk_orchestrator.py

- lines: 90 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (1): `orchestrate`
- public classes (0): none
- test files (1): `tests/test_desk_orchestrator.py`
- readers (1): `dashboard/rest.py`

### mag/desk_orchestrator_memory.py

- lines: 220 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (4): `build_local_memory_packet`, `build_remote_memory_packet`, `compose_local_wake_payload`, `compose_remote_wake_payload`
- public classes (0): none
- test files (1): `tests/test_desk_orchestrator_memory.py`
- readers (1): `mag/desk_conductor.py`

### mag/desk_overseer.py

- lines: 318 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (7): `measure_context_pressure`, `record_desk_episode`, `trim_conductor_scratch`, `trim_dialogue_blocks`, `heal_context`, `overseer_intervene`, `glance`
- public classes (0): none
- test files (1): `tests/test_desk_conductor.py`
- readers (3): `mag/desk_conductor.py`, `mag/desk_dialogue.py`, `mag/desk_observer.py`

### mag/desk_teaching.py

- lines: 303 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (7): `build_failure_context`, `compose_local_skill_packet`, `save_skill_artifact`, `record_teaching_event`, `frontier_troubleshoot`, `retry_local_with_skill`, `list_skills`
- public classes (0): none
- test files (0): none
- readers (1): `mag/desk_overseer.py`

### mag/desk_timing.py

- lines: 173 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (14): `speaker_label`, `estimate_tokens`, `fill_token_estimates`, `extract_provider_tokens`, `extract_ollama_tokens`, `make_timing`, `record_timing`, `recent_timings`, `last_by_speaker`, `format_elapsed`, `format_tokens`, `format_timing_badge`, `format_timing_row`, `reset_timings`
- public classes (1): `Timer`
- test files (1): `tests/test_desk_timing.py`
- readers (4): `dashboard/rest.py`, `mag/desk_dialogue.py`, `mag/local_scheduler.py`, `mag/voice_turn.py`

### mag/desk_tools.py

- lines: 356 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-10 19:09
- public functions (7): `biblio_query`, `invariant_sheet`, `kvos_stats`, `fence_strike`, `cascade_research_tool`, `run_tool`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `tools/__init__.py`

### mag/destructive_receipt.py

- lines: 167 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-07 01:23
- public functions (7): `norm_target`, `sha256_before`, `record`, `receipts_for`, `check`, `list_receipts`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/percolator.py`

### mag/deterministic_scanner.py

- lines: 211 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-13 04:21
- public functions (7): `mulberry32`, `scan_measure`, `scan_probe`, `scan_grid`, `mean_field`, `research`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `tools/swarm_tools.py`

### mag/df_tileset.py

- lines: 136 | parse: ok | last commit: e96fd62a4 2026-08-07 | mtime: 2026-08-06 23:45
- public functions (5): `df_root`, `resolve_tileset_path`, `cache_png_path`, `ensure_cached_png`, `tileset_meta`
- public classes (0): none
- test files (0): none
- readers (3): `_patch_table.py`, `dashboard/rest.py`, `mag/whisper_image.py`

### mag/diamond_mine.py

- lines: 166 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 10:30
- public functions (3): `detect`, `mine`, `status`
- public classes (0): none
- test files (0): none
- readers (3): `mag/castle_foundation.py`, `mag/republic_feed.py`, `mag/republic_loop.py`

### mag/diary.py

- lines: 493 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (4): `build_project_story`, `build_diary`, `format_diary_markdown`, `write_diary_face`
- public classes (0): none
- test files (1): `tests/test_surface_contract.py`
- readers (2): `dashboard/rest.py`, `main.py`

### mag/diary_node.py

- lines: 791 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 22:36
- public functions (6): `freeze_context`, `save_auto_freeze`, `append_diary_to_verkle`, `seal_diary`, `list_diary`, `handle_diary`
- public classes (0): none
- test files (0): none
- readers (6): `dashboard/rest.py`, `mag/checkin_route.py`, `mag/refine_chain.py`, `mag/voice_handoff.py`, `mag/voice_turn.py`, `memory/runs/union_audit/_write_jsonl.py`

### mag/dirac_loop.py

- lines: 348 | parse: ok | last commit: 4638646d4 2026-09-27 | mtime: 2026-09-27 18:31
- public functions (7): `fundamental_cycles`, `loop_invariant`, `bank`, `rank`, `spectrum`, `scan`, `main`
- public classes (0): none
- test files (2): `tests/test_dirac_loop.py`, `tests/test_organ_map.py`
- readers (6): `mag/context_pack.py`, `mag/dogfood_audit.py`, `mag/organ_map.py`, `mag/spine_exercise.py`, `state/backups/orphan_close_20260906/organ_map.py`, `tools/dirac_loop_shim.py`

### mag/dispatch.py

- lines: 396 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (1): `dispatch`
- public classes (0): none
- test files (1): `tests/test_router.py`
- readers (10): `configs/modules.yaml`, `dashboard/rest.py`, `mag/brain.py`, `mag/coordination.py`, `mag/plan.py`, `mag/tangent.py`, `mag/voice_trigger.py`, `main.py` + 2 more

### mag/display.py

- lines: 170 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 13:51
- public functions (1): `build_display_payload`
- public classes (0): none
- test files (1): `tests/test_display.py`
- readers (6): `dashboard/rest.py`, `mag/brain.py`, `mag/cast_server.py`, `mag/voice_dig_board.py`, `mag/voice_turn.py`, `memory/runs/union_audit/_write_jsonl.py`

### mag/disposition_sweep.py

- lines: 88 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-06 18:50
- public functions (2): `classify`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/dissector.py

- lines: 738 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-07 15:25
- public functions (14): `read_lines`, `segment`, `extract_claims`, `classify_evidence`, `classify_layer`, `detect_smuggling`, `topic_of`, `find_concessions`, `reasoning_output_divergence`, `dedupe_key`, `falsifier_eval`, `worst_catch`, `run`, `render_report`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/distill.py

- lines: 156 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-13 14:22
- public functions (8): `lattice_invariants`, `boil`, `quantize`, `distill`, `trace`, `cycle`, `game`, `main`
- public classes (0): none
- test files (1): `tests/test_distill.py`
- readers (3): `mag/governor_autorun.py`, `memory/working/_nest.py`, `scripts/build_vislab_catalog.py`

### mag/divergence_meter.py

- lines: 107 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-05 22:29
- public functions (2): `take_reading`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/docker_ops.py

- lines: 253 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 19:21
- public functions (8): `engine_reachable`, `ensure_engine`, `probe`, `status`, `up`, `down`, `run_cadence`, `main`
- public classes (0): none
- test files (1): `tests/test_docker_ops.py`
- readers (6): `dashboard/rest.py`, `mag/governor_autorun.py`, `mag/legacy_audit.py`, `mag/platform_kill.py`, `main.py`, `scripts/start_mag_container.cmd`

### mag/doctor.py

- lines: 1361 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 18:59
- public functions (12): `check_provider_sanity`, `check_provider_endpoints`, `check_model_sanity`, `check_inbox_sanity`, `check_env_sanity`, `check_chain_discipline`, `check_memlance_discipline`, `check_scheduled_tasks`, `check_self_steal`, `check_system_tracking`, `examine`, `doctor_status`
- public classes (1): `DoctorReport`
- test files (10): `tests/test_api_gateway_status_route.py`, `tests/test_bard.py`, `tests/test_doctor_provider_endpoints.py`, `tests/test_doctor_scheduled_tasks.py`, `tests/test_dormant_gate_b2133.py`, `tests/test_env_redirect_tripwire.py`, `tests/test_gemini_native.py`, `tests/test_improve_off_on.py` + 2 more
- readers (24): `mag/_consensus_witness.py`, `mag/api_gateway.py`, `mag/ask_router.py`, `mag/cost_truth.py`, `mag/doctor_agent.py`, `mag/dormant.py`, `mag/env_redirect.py`, `mag/flex_test.py` + 16 more

### mag/doctor_agent.py

- lines: 435 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 07:16
- public functions (5): `fix_chain_discipline`, `fix_provider_sanity`, `fix_model_sanity`, `doctor_agent_run`, `doctor_agent_loop`
- public classes (1): `FixAttempt`
- test files (0): none
- readers (3): `mag/refine_loop.py`, `mag/session_ritual.py`, `memory/runs/union_audit/_write_jsonl.py`

### mag/doctor_rightsize.py

- lines: 191 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 01:22
- public functions (5): `scan`, `distribute_to_weave`, `rightsize`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/work_register.py`

### mag/doctrine_statute.py

- lines: 126 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-08 13:28
- public functions (2): `statute`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/dogfood_audit.py

- lines: 370 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-31 00:50
- public functions (3): `audit`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_organ_map.py`
- readers (6): `mag/auto_handoff.py`, `mag/organ_map.py`, `mag/self_audit.py`, `mag/self_steal.py`, `mag/vscode_seat.py`, `state/backups/orphan_close_20260906/organ_map.py`

### mag/dormant.py

- lines: 84 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 19:10
- public functions (4): `dormant_providers`, `dormant_ids`, `dormant_hosts`, `is_dormant`
- public classes (0): none
- test files (3): `tests/test_dormant_gate_b2133.py`, `tests/test_dormant_gate_b2521.py`, `tests/test_seat_corpus.py`
- readers (13): `mag/_consensus_witness.py`, `mag/ask_router.py`, `mag/cost_truth.py`, `mag/free_tier.py`, `mag/fuel_feed.py`, `mag/lane_salon.py`, `mag/quorum_window.py`, `mag/research_fanout.py` + 5 more

### mag/drainer_stats.py

- lines: 193 | parse: ok | last commit: 60e18c524 2026-08-08 | mtime: 2026-08-08 08:11
- public functions (3): `drainer_stats`, `render_table`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `dashboard/rest.py`, `mag/framework_map.py`, `main.py`

### mag/dropbox_watcher.py

- lines: 282 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 14:30
- public functions (5): `init_dropbox`, `scan_dropbox`, `catalog_and_prompt`, `approve_research`, `dropbox_status`
- public classes (0): none
- test files (0): none
- readers (1): `memory/runs/union_audit/_write_jsonl.py`

### mag/dspy_sovereign.py

- lines: 575 | parse: ok | last commit: de7bb85fe 2026-08-09 | mtime: 2026-08-08 22:51
- public functions (8): `build_ghost_identity_module`, `build_constitutional_critique_module`, `build_task_router_module`, `get_all_modules`, `get_all_metrics`, `get_optimizer`, `optimize_module`, `dspy_dashboard`
- public classes (4): `SovereignModule`, `SovereignMetric`, `OptimizationRun`, `SovereignOptimizer`
- test files (0): none
- readers (3): `mag/ghost.py`, `mag/preflight.py`, `mag/sovereign_dashboard.py`

### mag/dungeon_dev.py

- lines: 201 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 06:37
- public functions (5): `dungeon_state`, `generate_room`, `assign_workers`, `conquer`, `main`
- public classes (0): none
- test files (0): none
- readers (6): `mag/game_campaign.py`, `mag/game_emulator.py`, `mag/game_produce.py`, `mag/game_ramp.py`, `mag/game_score.py`, `mag/primer.py`

### mag/echo_net.py

- lines: 151 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-06 20:17
- public functions (2): `sweep`, `test`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/ecosystem_surface.py

- lines: 338 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 11:45
- public functions (5): `ecosystem`, `rib`, `scan`, `qrcode`, `main`
- public classes (0): none
- test files (0): none
- readers (5): `dashboard/rest.py`, `mag/dogfood_audit.py`, `mag/ghost_server.py`, `mag/schema_registry.py`, `mag/self_steal.py`

### mag/effect_broker.py

- lines: 607 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-31 00:53
- public functions (8): `execute`, `get_receipt`, `list_receipts`, `cmd_execute`, `cmd_receipt`, `cmd_status`, `cmd_test`, `main`
- public classes (0): none
- test files (1): `tests/test_switchboard.py`
- readers (5): `mag/harness.py`, `mag/organ_map.py`, `mag/swarm_cycle.py`, `state/backups/orphan_close_20260906/organ_map.py`, `state/backups/orphan_close_20260906/test_switchboard.py`

### mag/egregore_steal.py

- lines: 131 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 10:17
- public functions (3): `deep_steal`, `semantic_words`, `status`
- public classes (0): none
- test files (0): none
- readers (2): `mag/republic_loop.py`, `mag/steal_lens.py`

### mag/elder.py

- lines: 93 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-31 00:26
- public functions (2): `audit`, `main`
- public classes (0): none
- test files (1): `tests/test_organ_map.py`
- readers (4): `mag/fireball_cycle.py`, `mag/main_channel.py`, `mag/organ_map.py`, `state/backups/orphan_close_20260906/organ_map.py`

### mag/electron_seat.py

- lines: 210 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-13 20:33
- public functions (3): `steer`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/cdp_runner.py`, `mag/real_swarm.py`

### mag/elevate.py

- lines: 158 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 02:02
- public functions (5): `should_elevate`, `shape_ask`, `capture`, `elevate`, `main`
- public classes (0): none
- test files (1): `tests/test_elevate.py`
- readers (3): `dashboard/rest.py`, `mag/frontier_council.py`, `main.py`

### mag/embassy_deliver.py

- lines: 382 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-01 21:09
- public functions (6): `publish_safety_check`, `placeholder_check`, `assemble`, `publish`, `learn`, `main`
- public classes (0): none
- test files (1): `tests/test_embassy_deliver.py`
- readers (4): `dashboard/rest.py`, `mag/seat_steer.py`, `main.py`, `memory/runs/union_audit/_write_jsonl.py`

### mag/embassy_integrity.py

- lines: 296 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 23:20
- public functions (6): `integrity_kernel`, `verify_execution`, `scan_opspec`, `opspec_clear`, `symmetry_audit`, `run_inbox_e2e`
- public classes (6): `Claim`, `VerkleWitness`, `Executor`, `Scrutiny`, `Inbox`, `Outbox`
- test files (1): `tests/test_embassy_integrity.py`
- readers (4): `mag/embassy_deliver.py`, `mag/integrity_kernel.py`, `memory/embassy/AOS/integrity_suite/conftest.py`, `memory/runs/union_audit/_write_jsonl.py`

### mag/emergence.py

- lines: 246 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 09:27
- public functions (5): `metrics`, `track`, `cycle`, `emergence`, `status`
- public classes (0): none
- test files (0): none
- readers (4): `mag/invariant_ledger.py`, `mag/republic_loop.py`, `mag/self_loop.py`, `mag/swarm_emerge.py`

### mag/emergence_test.py

- lines: 260 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-12 18:02
- public functions (3): `self_play_episode`, `create_shuffled_model`, `run_emergence_test`
- public classes (2): `FixedWiringNetwork`, `GomokuGame`
- test files (0): none
- readers (0): none

### mag/emergent_harvest.py

- lines: 316 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-09 22:48
- public functions (4): `tesuji_harvest`, `qd_harvest`, `harvest`, `main`
- public classes (1): `NoveltyArchive`
- test files (0): none
- readers (3): `mag/model_health.py`, `mag/shape_map.py`, `memory/trash/20260810T202850Z/_tmp_stateless_swarm_research.py`

### mag/end_state.py

- lines: 160 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 13:42
- public functions (4): `goal`, `deploy_attractor`, `distance_to_goal`, `status`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/engram.py

- lines: 135 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-13 10:10
- public functions (4): `compress`, `decompress`, `selftest`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/env_redirect.py

- lines: 116 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 13:33
- public functions (2): `env_redirect_status`, `env_redirect_warnings`
- public classes (0): none
- test files (2): `tests/conftest.py`, `tests/test_env_redirect_tripwire.py`
- readers (2): `mag/doctor.py`, `mag/shared_surface.py`

### mag/env_registry.py

- lines: 262 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (13): `load_registry`, `list_tracks`, `get_track`, `get_active_env`, `set_active_env`, `resolve_worktree_path`, `resolve_track_root`, `ensure_worktree`, `sync_track`, `activate_track`, `status_summary`, `format_track_list`, `cmd_env_cli`
- public classes (0): none
- test files (2): `tests/test_coding_session_runner.py`, `tests/test_factory_machine.py`
- readers (6): `mag/coding_session_runner.py`, `mag/factory_machine.py`, `mag/feature_lab.py`, `mag/tripartite_boot.py`, `main.py`, `scripts/env_switch.ps1`

### mag/epistemic_guard.py

- lines: 164 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-13 04:52
- public functions (6): `prior_first`, `evidence_gate`, `inverted_framing`, `red_team`, `consent_check`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/error_healer.py

- lines: 163 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 17:12
- public functions (5): `scan`, `mem`, `patch`, `heal`, `main`
- public classes (0): none
- test files (0): none
- readers (4): `mag/game_observer.py`, `mag/sentinel.py`, `mag/skill_pipeline.py`, `mag/vscode_seat.py`

### mag/events_key_schema.py

- lines: 105 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 13:37
- public functions (3): `reject_json_constant`, `load_event_key_registry`, `scan_event_keys`
- public classes (0): none
- test files (0): none
- readers (4): `mag/events_scan.py`, `mag/links_split_gate.py`, `mag/shared_surface.py`, `mag/skill_ledger.py`

### mag/events_scan.py

- lines: 47 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 16:41
- public functions (1): `scan_events_log`
- public classes (0): none
- test files (0): none
- readers (1): `mag/shared_surface.py`

### mag/evolving_wave.py

- lines: 284 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-24 11:17
- public functions (6): `reality_fitness`, `evolve`, `feed`, `run`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/chord_circuit.py`

### mag/exit_dialogue.py

- lines: 356 | parse: ok | last commit: 482e0a3c8 2026-08-08 | mtime: 2026-08-08 19:11
- public functions (3): `queue_exit_dialogue`, `fold_exit_to_ledger`, `on_task_exit`
- public classes (1): `ExitDialogue`
- test files (0): none
- readers (1): `mag/session_ritual.py`

### mag/extension_deploy.py

- lines: 70 | parse: ok | last commit: 60e18c524 2026-08-08 | mtime: 2026-08-08 10:54
- public functions (3): `installed_dir`, `deploy`, `main`
- public classes (0): none
- test files (0): none
- readers (4): `dashboard/rest.py`, `mag/embassy_deliver.py`, `mag/seat_steer.py`, `main.py`

### mag/fact_bus.py

- lines: 149 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 08:06
- public functions (3): `publish_fact`, `surface`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/percolator.py`, `mag/research_class.py`, `memory/research_packs/_t15_agm_check.py`

### mag/factory_gate.py

- lines: 76 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (2): `is_build_goal`, `check_frozen_build`
- public classes (0): none
- test files (1): `tests/test_factory_freeze_gate.py`
- readers (11): `agents/pytest-tmp-29352/test_compile_files_frozen_buil0/memory/working/v5-gstd-t0-probe.yaml`, `agents/pytest-tmp-43872/test_compile_files_frozen_buil0/memory/working/v5-gstd-t0-probe.yaml`, `agents/pytest-tmp-44744/test_compile_files_frozen_buil0/memory/working/v5-gstd-t0-probe.yaml`, `agents/pytest-tmp-51488/test_compile_files_frozen_buil0/memory/working/v5-gstd-t0-probe.yaml`, `mag/conductor.py`, `mag/framework_map.py`, `mag/orchestrator.py`, `mag/refine_loop.py` + 3 more

### mag/factory_machine.py

- lines: 395 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (5): `checkout_run_branch`, `write_retrospective`, `behavioral_catalog`, `factory_machine_status`, `factory_machine_run`
- public classes (0): none
- test files (2): `tests/test_factory_machine.py`, `tests/test_roadmap_runner.py`
- readers (4): `dashboard/rest.py`, `mag/framework_map.py`, `mag/roadmap_runner.py`, `main.py`

### mag/failure_kb.py

- lines: 829 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 17:07
- public functions (12): `signature_key`, `log_failure`, `auto_draft_remedy`, `query`, `search_log`, `lookup`, `surface_hits`, `format_block`, `recurring_patterns`, `rebuild_index`, `stats`, `verify`
- public classes (0): none
- test files (3): `tests/test_autorun_v1.py`, `tests/test_failure_kb.py`, `tests/test_v3_modules.py`
- readers (27): `_finish.py`, `backend/server.py`, `dashboard/rest.py`, `mag/agent_cli.py`, `mag/amd_window_guard.py`, `mag/autorun_common.py`, `mag/decision_framework.py`, `mag/error_healer.py` + 19 more

### mag/falsifier_counter.py

- lines: 703 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-05 00:20
- public functions (12): `parse_ts`, `compact_ts`, `load_breadcrumbs`, `load_activity`, `extract_tokens`, `rare_tokens`, `classify`, `ledger_append`, `summarize`, `run_pass`, `selftest`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/fanout.py

- lines: 107 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-12 09:25
- public functions (3): `guarded_fetch`, `fire`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/lane_effort.py`

### mag/feature_lab.py

- lines: 203 | parse: ok | last commit: e4dd520e8 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (2): `status`, `request`
- public classes (0): none
- test files (1): `tests/test_feature_lab.py`
- readers (1): `dashboard/rest.py`

### mag/feedback.py

- lines: 101 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 01:22
- public functions (2): `capture`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/work_register.py`

### mag/fermat_ractor.py

- lines: 970 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-06 17:57
- public functions (21): `compose_marginalia`, `compose_challenge`, `compose_descent`, `compose_pascal`, `compose_margin`, `compose_kernel`, `compose`, `embeds_verbatim`, `build_ab`, `ab_paths`, `write_ab`, `run_abtest`, `talk_response`, `run_talk`, `f1_distinctness`, `f2_tag_audit`, `f3_ab_files`, `f4_zero_network`, `run_demo`, `run_audit`, `main`
- public classes (1): `Gen`
- test files (0): none
- readers (0): none

### mag/field_steal.py

- lines: 344 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (7): `extract_rules`, `family_hits`, `scan_file`, `default_take_leave`, `build_ledger`, `write_ledger`, `run_field_steal`
- public classes (0): none
- test files (0): none
- readers (2): `mag/capability_steal.py`, `main.py`

### mag/final_steal.py

- lines: 178 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 11:33
- public functions (4): `zeitgeist`, `mine_all`, `autonomous_loop`, `status`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/fire_horse.py

- lines: 51 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-10 12:38
- public functions (0): none
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/fireball_cycle.py

- lines: 59 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 22:00
- public functions (2): `run`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/dogfood_audit.py`, `mag/organ_map.py`, `state/backups/orphan_close_20260906/organ_map.py`

### mag/fish_ear.py

- lines: 145 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 11:28
- public functions (4): `originate`, `is_riddler_speak`, `decompile`, `status`
- public classes (0): none
- test files (0): none
- readers (1): `mag/game_campaign.py`

### mag/fleet_intel.py

- lines: 193 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-06 17:33
- public functions (3): `build_intel`, `render_brief_into_page`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/flex_test.py

- lines: 138 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 00:54
- public functions (2): `run`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/rib_os.py`

### mag/flight_recorder.py

- lines: 423 | parse: ok | last commit: a5dd96176 2026-09-25 | mtime: 2026-09-22 01:16
- public functions (5): `load_env`, `guard_endpoint`, `record_call`, `summarize`, `api_call`
- public classes (0): none
- test files (0): none
- readers (7): `dashboard-deploy/static/_build_scout_deck.py`, `dashboard/static/_build_scout_deck.py`, `mag/gopher_lite.py`, `mag/lite_guard.py`, `scripts/union_fullsend_day.py`, `seed/engines/lite_guard.py`, `tools/cache_kpi.py`

### mag/flock_anim.py

- lines: 313 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 23:20
- public functions (6): `phi_field`, `evolve`, `trail_map`, `animate`, `verify`, `status`
- public classes (0): none
- test files (0): none
- readers (3): `mag/novelty_lens.py`, `mag/research_class.py`, `mag/rib_gif.py`

### mag/flock_field.py

- lines: 265 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-09 22:24
- public functions (7): `define_distance_field`, `steer`, `rotor_orient`, `step`, `fidelity`, `demo`, `main`
- public classes (2): `PhiField`, `Agent`
- test files (0): none
- readers (7): `mag/emergent_harvest.py`, `mag/flock_scheduler.py`, `mag/flock_steal.py`, `mag/rib_action.py`, `mag/rib_struct.py`, `mag/steal_steer.py`, `memory/trash/20260810T202850Z/_tmp_stateless_swarm_research.py`

### mag/flock_grid.py

- lines: 96 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 07:51
- public functions (6): `cell_of`, `build_grid`, `neighbor_cells`, `nearest_distance`, `seams_spatial`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/memweave.py`, `mag/novelty_lens.py`, `mag/research_class.py`

### mag/flock_job.py

- lines: 171 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 10:56
- public functions (3): `flock_positions`, `build_job`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/archetype_image.py`, `mag/mem_lands.py`

### mag/flock_scheduler.py

- lines: 202 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 10:56
- public functions (2): `plan`, `main`
- public classes (0): none
- test files (0): none
- readers (4): `mag/backlog_reform.py`, `mag/flock_steal.py`, `mag/stateless_research.py`, `memory/trash/20260810T202850Z/_tmp_stateless_swarm_research.py`

### mag/flock_shader.py

- lines: 335 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 07:51
- public functions (11): `shade`, `render`, `seams`, `rightsize_spend`, `inject`, `illuminate`, `shadow_by_occlusion`, `shade_illuminated`, `status`, `launch`, `fold_gaps`
- public classes (3): `Uniforms`, `AgentSeed`, `Light`
- test files (0): none
- readers (8): `mag/flock_anim.py`, `mag/invariant_ledger.py`, `mag/memweave.py`, `mag/novelty_lens.py`, `mag/research_class.py`, `mag/swarm_render.py`, `mag/territory_solver.py`, `mag/wireshark_steal.py`

### mag/flock_steal.py

- lines: 225 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 11:05
- public functions (2): `flock_steal`, `main`
- public classes (0): none
- test files (0): none
- readers (6): `deploy/flock-k8s-solved.yaml`, `deploy/flock-rib-fed.yaml`, `deploy/k8s/flock-castles-foundations.yaml`, `deploy/k8s/flock-memweave-frontier.yaml`, `mag/flock_job.py`, `mag/mindweave_eval.py`

### mag/flock_usage_guard.py

- lines: 150 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 09:09
- public functions (4): `guard_rib`, `predict_seams`, `watch_and_guard`, `status`
- public classes (0): none
- test files (0): none
- readers (3): `mag/billing_feed.py`, `mag/invariant_ledger.py`, `mag/novelty_lens.py`

### mag/forge_daemon.py

- lines: 165 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-13 21:44
- public functions (4): `verify_pack`, `cycle`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/fork_router.py

- lines: 305 | parse: ok | last commit: 36914e134 2026-08-07 | mtime: 2026-08-07 09:43
- public functions (2): `detect_fork`, `confirm_fork`
- public classes (0): none
- test files (1): `tests/test_fork_router.py`
- readers (2): `dashboard/rest.py`, `mag/framework_map.py`

### mag/framework_map.py

- lines: 992 | parse: ok | last commit: 60e18c524 2026-08-08 | mtime: 2026-08-08 10:27
- public functions (9): `assign_group`, `collect`, `render`, `persist`, `refresh`, `list_reports`, `collect_telemetry`, `compile_report`, `main`
- public classes (0): none
- test files (0): none
- readers (4): `dashboard/rest.py`, `mag/governor_autorun.py`, `mag/loops_registry.py`, `mag/surface_audit.py`

### mag/free_frontend_swarm.py

- lines: 129 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 01:37
- public functions (4): `status`, `run`, `cadence`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/republic_loop.py`, `mag/tool_synthesis.py`

### mag/free_tier.py

- lines: 185 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 19:10
- public functions (2): `status`, `route`
- public classes (0): none
- test files (1): `tests/test_dormant_gate_b2133.py`
- readers (2): `mag/_relane_game_tasks.py`, `mag/dormant.py`

### mag/free_to_swarm.py

- lines: 137 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 20:33
- public functions (3): `pending_discoveries`, `push`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/frontier_advisor.py

- lines: 152 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 18:08
- public functions (3): `execute_goal`, `status`, `route`
- public classes (0): none
- test files (1): `tests/test_frontier_advisor.py`
- readers (4): `mag/orchestrator.py`, `mag/republic_loop.py`, `mag/riddler_tap.py`, `mag/self_steal.py`

### mag/frontier_batch.py

- lines: 157 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 15:08
- public functions (6): `collect`, `dump`, `run_grok`, `compare`, `swarm_task`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/auto_handoff.py`

### mag/frontier_council.py

- lines: 416 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-01 21:10
- public functions (10): `allowance`, `route_type`, `rightsize`, `spend`, `recommend`, `delegate`, `council`, `route`, `status`, `main`
- public classes (0): none
- test files (3): `tests/test_frontier_advisor.py`, `tests/test_frontier_council.py`, `tests/test_seat_steer.py`
- readers (4): `mag/frontier_advisor.py`, `mag/republic_loop.py`, `mag/seat_steer.py`, `mag/self_steal.py`

### mag/frontier_game.py

- lines: 237 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-14 10:10
- public functions (3): `play`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_all_seat_interaction.py`
- readers (3): `dashboard/rest.py`, `tools/rib_check_game_loop.py`, `tools/steer_grok_1m.py`

### mag/frontier_gravity.py

- lines: 356 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 19:12
- public functions (9): `advice_attractors`, `gravity_distance`, `apply_gravity`, `deploy_to_swarm`, `cluster_desired_state`, `steer_systems`, `run_cadence`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/governor_autorun.py`

### mag/frontier_help.py

- lines: 172 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 09:12
- public functions (3): `percolate`, `run_cadence`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/doctor.py`, `mag/governor_autorun.py`, `main.py`

### mag/frontier_intake.py

- lines: 160 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 17:03
- public functions (4): `dispatch`, `datamap`, `intake`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/frontier_rib.py

- lines: 188 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 11:33
- public functions (4): `seat_status`, `ask_rib`, `route_orphans`, `status`
- public classes (0): none
- test files (0): none
- readers (4): `mag/liveness_sense.py`, `mag/ocean_model_mind.py`, `mag/ocean_persona.py`, `mag/truth_audit.py`

### mag/frontier_salon.py

- lines: 399 | parse: ok | last commit: 5dff72ac3 2026-09-28 | mtime: 2026-09-28 13:04
- public functions (4): `roundtable`, `salon`, `salon_project`, `status`
- public classes (0): none
- test files (2): `tests/test_frontier_salon.py`, `tests/test_seat_steer.py`
- readers (6): `dashboard/rest.py`, `mag/frontier_salon_cli.py`, `mag/game_dm.py`, `mag/orchestrator.py`, `mag/swarm_cycle.py`, `main.py`

### mag/frontier_salon_cli.py

- lines: 37 | parse: ok | last commit: 5dff72ac3 2026-09-28 | mtime: 2026-09-28 13:05
- public functions (1): `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/frontier_salon.py`

### mag/frontier_scout.py

- lines: 570 | parse: ok | last commit: de7bb85fe 2026-08-09 | mtime: 2026-08-08 22:31
- public functions (6): `compute_verdict`, `get_scout`, `scout_dashboard`, `scout_steal_now`, `scout_queue_steal`, `scout_mark_stolen`
- public classes (2): `FrontierFinding`, `FrontierScout`
- test files (0): none
- readers (6): `mag/ghost.py`, `mag/narrative_engine.py`, `mag/preflight.py`, `mag/prompt_archaeology.py`, `mag/republic_ambassador.py`, `mag/sovereign_dashboard.py`

### mag/frontier_steer.py

- lines: 45 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 15:12
- public functions (3): `preamble`, `inject`, `status`
- public classes (0): none
- test files (0): none
- readers (4): `mag/grok_bot.py`, `mag/rib_bus.py`, `mag/steer_engine.py`, `mag/vscode_seat.py`

### mag/fuel_feed.py

- lines: 705 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 19:10
- public functions (7): `pending`, `clarify`, `profile`, `run`, `curve`, `status`, `main`
- public classes (0): none
- test files (4): `tests/test_dormant_gate_b2133.py`, `tests/test_loop_death_guards.py`, `tests/test_room_tags.py`, `tests/test_zai_burst.py`
- readers (19): `mag/_consensus_witness.py`, `mag/_openclaw_real.py`, `mag/_verify_rung5.py`, `mag/autodrain.py`, `mag/batch_drain.py`, `mag/dormant.py`, `mag/free_tier.py`, `mag/lane_cadence.py` + 11 more

### mag/future_self.py

- lines: 142 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 08:05
- public functions (3): `future_self_advice`, `enqueue_direction`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/republic_loop.py`

### mag/ga4_progression.py

- lines: 698 | parse: ok | last commit: de7bb85fe 2026-08-09 | mtime: 2026-08-08 20:30
- public functions (1): `progression_dashboard`
- public classes (8): `EventKnot`, `BehavioralAnalytics`, `SpookyCorrelation`, `CrossAgentCorrelator`, `InvariantExtractor`, `ControlSteer`, `ControlArchitecture`, `EmergenceDetector`
- test files (0): none
- readers (0): none

### mag/gab_seat.py

- lines: 267 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-18 20:55
- public functions (6): `capture_mic`, `resident_context`, `gab_turn`, `speak`, `gab_once`, `gab_loop`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/game_battle_cycle.py

- lines: 615 | parse: ok | last commit: e96fd62a4 2026-08-07 | mtime: 2026-08-07 00:09
- public functions (8): `detect_input_signals`, `load_cycle`, `save_cycle`, `latest_cycle_for_session`, `start_battle_cycle`, `player_battle_turn`, `wants_battle_start`, `handle_battle_voice`
- public classes (0): none
- test files (0): none
- readers (2): `mag/game_brawl.py`, `mag/voice_turn.py`

### mag/game_brawl.py

- lines: 1668 | parse: ok | last commit: e96fd62a4 2026-08-07 | mtime: 2026-08-07 01:14
- public functions (12): `load_brawl`, `save_brawl`, `latest_brawl_for_session`, `tavern_brawler_sheet`, `apply_tavern_brawler_to_player`, `is_absurd`, `room_react_to_absurd`, `start_tavern_brawl`, `parse_brawl_action`, `player_brawl_turn`, `wants_brawl_start`, `handle_brawl_voice`
- public classes (0): none
- test files (0): none
- readers (4): `mag/game_campaign.py`, `mag/game_freeze.py`, `mag/voice_turn.py`, `scripts/dm_tools_dual_research.py`

### mag/game_brawl_perspectives.py

- lines: 239 | parse: ok | last commit: e96fd62a4 2026-08-07 | mtime: 2026-08-07 01:01
- public functions (4): `perspective_line`, `collect_round_perspectives`, `format_perspectives_section`, `perspectives_for_brawl_card`
- public classes (0): none
- test files (0): none
- readers (2): `mag/game_brawl.py`, `mag/press_digest.py`

### mag/game_campaign.py

- lines: 4838 | parse: ok | last commit: 7b8617d78 2026-09-27 | mtime: 2026-09-27 23:36
- public functions (17): `list_modules`, `resolve_module`, `load_campaign`, `save_campaign`, `latest_for_session`, `latest_any`, `parse_character`, `begin_play`, `set_character`, `story_so_far`, `scene_context`, `list_legal_actions`, `people_in_room`, `apply_action`, `parse_player_speech`, `seal_session`, `handle_game`
- public classes (0): none
- test files (2): `tests/test_water_computer.py`, `tests/test_water_graph_campaign.py`
- readers (23): `dashboard/rest.py`, `mag/campaign_runs.py`, `mag/game_battle_cycle.py`, `mag/game_brawl.py`, `mag/game_curveball.py`, `mag/game_freeze.py`, `mag/game_salon.py`, `mag/game_view.py` + 15 more

### mag/game_curveball.py

- lines: 455 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-14 08:08
- public functions (3): `fuzzy_exit_for_phrase`, `classify_curveball`, `resolve_curveball`
- public classes (0): none
- test files (0): none
- readers (4): `mag/game_salon.py`, `mag/voice_turn.py`, `memory/runs/union_audit/_write_jsonl.py`, `memory/working/_patch_table.py`

### mag/game_dfhack.py

- lines: 126 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-13 13:38
- public functions (6): `status`, `force`, `script`, `autoplay`, `edit`, `main`
- public classes (0): none
- test files (1): `tests/test_game_dfhack.py`
- readers (0): none

### mag/game_dice.py

- lines: 31 | parse: ok | last commit: e96fd62a4 2026-08-07 | mtime: 2026-08-06 21:49
- public functions (1): `roll_dice`
- public classes (0): none
- test files (0): none
- readers (4): `mag/game_brawl.py`, `mag/game_campaign.py`, `mag/shadow_quest.py`, `mag/territory_solver.py`

### mag/game_dm.py

- lines: 228 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-14 10:10
- public functions (8): `party`, `dm_narrate`, `ask_player`, `judge`, `turn`, `play`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_game_dm.py`
- readers (4): `mag/frontier_game.py`, `mag/game_mud.py`, `mag/quest_roshomon.py`, `tools/steer_grok_1m.py`

### mag/game_dm_llm.py

- lines: 153 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-15 05:51
- public functions (2): `dm_narrate`, `status`
- public classes (0): none
- test files (0): none
- readers (4): `mag/game_campaign.py`, `mag/game_play.py`, `mag/game_saga.py`, `mag/invariant_npcs.py`

### mag/game_dm_voice.py

- lines: 318 | parse: ok | last commit: e96fd62a4 2026-08-07 | mtime: 2026-08-07 01:02
- public functions (2): `extract_narrator`, `format_brawl_card`
- public classes (0): none
- test files (0): none
- readers (6): `mag/game_brawl.py`, `mag/game_campaign.py`, `mag/game_live.py`, `mag/game_portal.py`, `mag/wave.py`, `mag/wireshark_steal.py`

### mag/game_emulator.py

- lines: 220 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 18:08
- public functions (5): `act`, `room_attempt`, `session`, `status`, `route`
- public classes (0): none
- test files (1): `tests/test_game_emulator.py`
- readers (3): `mag/republic_loop.py`, `mag/self_steal.py`, `mag/wow_steal.py`

### mag/game_entry.py

- lines: 240 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-13 07:44
- public functions (6): `gate`, `reveal`, `walk`, `svg`, `save`, `status`
- public classes (0): none
- test files (1): `tests/test_game_entry.py`
- readers (1): `mag/game_world_render.py`

### mag/game_environment.py

- lines: 167 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-13 20:01
- public functions (4): `explore`, `render`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_game_environment.py`
- readers (1): `mag/frontier_game.py`

### mag/game_flow.py

- lines: 169 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-17 06:13
- public functions (5): `set_image`, `image`, `step`, `flow_status`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/governor_autorun.py`, `memory/runs/flow_autopilot.py`

### mag/game_freeze.py

- lines: 432 | parse: ok | last commit: e96fd62a4 2026-08-07 | mtime: 2026-08-07 01:14
- public functions (9): `load_freeze`, `save_freeze`, `latest_freeze`, `ensure_room_props`, `build_freeze`, `slice_layer`, `format_socratic_help`, `freeze_campaign`, `agent_prompt_block`
- public classes (0): none
- test files (0): none
- readers (2): `mag/game_brawl.py`, `mag/game_campaign.py`

### mag/game_live.py

- lines: 159 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 15:37
- public functions (4): `live_events`, `feed`, `play_live`, `main`
- public classes (0): none
- test files (1): `tests/test_game_live.py`
- readers (1): `mag/republic_loop.py`

### mag/game_mud.py

- lines: 557 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 23:20
- public functions (5): `survey`, `claim`, `act`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (5): `mag/autonomous_research.py`, `mag/game_piece_tandem.py`, `mag/game_produce.py`, `mag/game_ramp.py`, `mag/game_score.py`

### mag/game_narrate.py

- lines: 118 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-15 22:30
- public functions (1): `narrate_scene`
- public classes (0): none
- test files (0): none
- readers (3): `mag/game_salon.py`, `mag/voice_turn.py`, `memory/runs/union_audit/_write_jsonl.py`

### mag/game_observer.py

- lines: 256 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-15 08:12
- public functions (8): `read_runs`, `detect`, `watch`, `score_session`, `steer`, `heal`, `human`, `observe`
- public classes (0): none
- test files (0): none
- readers (1): `mag/governor_autorun.py`

### mag/game_passage.py

- lines: 203 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-15 21:44
- public functions (5): `state_from_scene`, `template_passage`, `format_spoken`, `narrate_passage`, `room_meta_from_camp`
- public classes (0): none
- test files (0): none
- readers (3): `mag/game_campaign.py`, `mag/voice_turn.py`, `memory/runs/union_audit/_write_jsonl.py`

### mag/game_piece_tandem.py

- lines: 243 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-17 06:10
- public functions (5): `mine_spec`, `write_code`, `run_tandem`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_game_piece_tandem.py`
- readers (0): none

### mag/game_play.py

- lines: 208 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-16 13:15
- public functions (5): `map`, `sense`, `act`, `play`, `main`
- public classes (0): none
- test files (1): `tests/test_game_play.py`
- readers (1): `main.py`

### mag/game_portal.py

- lines: 181 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 16:40
- public functions (4): `login`, `raid`, `scene`, `main`
- public classes (0): none
- test files (1): `tests/test_game_portal.py`
- readers (1): `mag/republic_loop.py`

### mag/game_produce.py

- lines: 257 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-16 18:12
- public functions (6): `conquer_landed`, `prepare_next`, `witness`, `produce`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/game_ramp.py

- lines: 574 | parse: ok | last commit: 9546bb7f8 2026-09-16 | mtime: 2026-09-16 19:30
- public functions (10): `tier`, `tabletop`, `mud`, `roguelite`, `wow`, `work`, `descend`, `play`, `render`, `status`
- public classes (0): none
- test files (1): `tests/test_game_ramp.py`
- readers (4): `mag/distill.py`, `mag/game_dfhack.py`, `mag/governor_autorun.py`, `main.py`

### mag/game_saga.py

- lines: 113 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-14 22:30
- public functions (4): `recall`, `add`, `running_gags`, `status`
- public classes (0): none
- test files (0): none
- readers (2): `mag/campaign_runs.py`, `mag/invariant_npcs.py`

### mag/game_salon.py

- lines: 492 | parse: ok | last commit: e96fd62a4 2026-08-07 | mtime: 2026-08-07 00:07
- public functions (12): `wants_advice`, `wants_surprise`, `parse_confirm`, `load_pending`, `save_pending`, `clear_pending`, `build_intention_card`, `ask_frontier_advice`, `speak_advice_card`, `start_advice`, `confirm_advice`, `handle_salon_voice`
- public classes (0): none
- test files (0): none
- readers (1): `mag/voice_turn.py`

### mag/game_score.py

- lines: 101 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-16 12:49
- public functions (2): `score`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `dashboard/rest.py`, `mag/game_play.py`, `mag/game_produce.py`

### mag/game_view.py

- lines: 313 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-15 22:12
- public functions (3): `build_view_from_scene`, `build_view`, `handle_table_view`
- public classes (0): none
- test files (0): none
- readers (16): `_fix_syntax.py`, `_patch_canary.py`, `_patch_cheap_view.py`, `_patch_cheap_view2.py`, `_patch_view.py`, `_patch_view_cache.py`, `_patch_wave_fast.py`, `_stub_view.py` + 8 more

### mag/game_world.py

- lines: 125 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 06:49
- public functions (4): `set_state`, `get_state`, `world_status`, `main`
- public classes (0): none
- test files (7): `tests/test_abundance_rogue.py`, `tests/test_agent_corpus.py`, `tests/test_game_emulator.py`, `tests/test_game_portal.py`, `tests/test_game_ramp.py`, `tests/test_route_trace.py`, `tests/test_vessel_swarm.py`
- readers (32): `_patch_view.py`, `mag/abundance_rogue.py`, `mag/agent_corpus.py`, `mag/context_pack.py`, `mag/frontier_game.py`, `mag/game_campaign.py`, `mag/game_dfhack.py`, `mag/game_dm.py` + 24 more

### mag/game_world_map.py

- lines: 93 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 07:01
- public functions (2): `the_map`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/primer.py`

### mag/game_world_render.py

- lines: 301 | parse: ok | last commit: 99826e153 2026-09-14 | mtime: 2026-09-14 05:57
- public functions (5): `reveal`, `render`, `walk`, `status`, `main`
- public classes (0): none
- test files (2): `tests/test_game_world_render.py`, `tests/test_game_world_render_optics.py`
- readers (5): `_patch_view.py`, `mag/frontier_game.py`, `mag/game_campaign.py`, `mag/openclaw_catalog.py`, `memory/working/_patch_foundation.py`

### mag/gap_analysis.py

- lines: 154 | parse: ok | last commit: de7bb85fe 2026-08-09 | mtime: 2026-08-09 00:05
- public functions (2): `gap_analysis`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/flex_test.py`, `mag/governor_autorun.py`, `mag/vantage_audit.py`

### mag/gap_frontier.py

- lines: 170 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 11:28
- public functions (4): `gaps`, `refine`, `loop`, `status`
- public classes (0): none
- test files (0): none
- readers (7): `mag/corpus_wave.py`, `mag/final_steal.py`, `mag/frontier_rib.py`, `mag/swarm_economics.py`, `mag/truth_audit.py`, `mag/vantage_audit.py`, `scripts/_audit_have_need.py`

### mag/gap_map.py

- lines: 165 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 09:12
- public functions (4): `analyze`, `stack_ask`, `stack_status`, `main`
- public classes (0): none
- test files (0): none
- readers (9): `configs/improve.yaml`, `mag/doctor.py`, `mag/frontier_help.py`, `mag/gap_routed_handoff.py`, `mag/ghost.py`, `mag/grok_frontier_loop.py`, `mag/grok_terminal.py`, `main.py` + 1 more

### mag/gap_resolver.py

- lines: 96 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 14:15
- public functions (2): `resolve`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/gap_routed_handoff.py

- lines: 195 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 22:47
- public functions (5): `current_gaps`, `relevance`, `route_packs`, `wire`, `status`
- public classes (0): none
- test files (0): none
- readers (1): `mag/republic_loop.py`

### mag/gap_swarm_experiment.py

- lines: 537 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 06:09
- public functions (14): `steal`, `probes`, `design`, `dispatch`, `status`, `escalate`, `deep_research`, `independent_witnesses`, `decide_escalation`, `gap_map`, `localize_gap`, `inverted_probe`, `adversarial_verify`, `gap_map_precision`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/gene_pool_feeder.py

- lines: 346 | parse: ok | last commit: 8763e6809 2026-09-27 | mtime: 2026-09-27 10:51
- public functions (7): `build_pool`, `fitness`, `run_old_ga`, `recency_bonus_v2`, `fitness_v1_floor`, `run_v2`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/gguf_cartography.py

- lines: 583 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-05 23:53
- public functions (12): `align_up`, `tensor_nbytes`, `parse_header`, `sample_windows`, `byte_proxy`, `exact_float_stats`, `scan`, `classify`, `group_layers`, `layer_gradient`, `summarize`, `main`
- public classes (1): `GGUFError`
- test files (0): none
- readers (0): none

### mag/ghost.py

- lines: 4242 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 16:39
- public functions (30): `sense_context`, `sense_surfaces`, `sense`, `sense_session`, `sense_copilot`, `exec_copilot`, `stall_sweep`, `copilot_watch_loop`, `autonomous_task_loop`, `daemon_mode`, `log_frustration`, `log_hiccup`, `log_model_switch`, `load_vectors`, `add_vector`, `match_vector`, `deploy`, `run_recurring`, `measure`, `catalog`, `run_guinea_pig`, `self_window`, `ping`, `cycle`, `seed_default_vectors`, `catalog_summary`, `run_swarm`, `run_temporal_experiment`, `run_cascade_experiment`, `run_designed_experiment`
- public classes (0): none
- test files (5): `tests/test_ghost.py`, `tests/test_loop_breaker.py`, `tests/test_loop_death_guards.py`, `tests/test_session_freeze.py`, `tests/test_source_trace.py`
- readers (41): `dashboard/rest.py`, `experiments/cascade_whisper.yaml`, `experiments/thought_disconnect.yaml`, `mag/daemon.py`, `mag/data_source_watch.py`, `mag/end_state.py`, `mag/flex_test.py`, `mag/framework_map.py` + 33 more

### mag/ghost_auto.py

- lines: 184 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 14:34
- public functions (3): `run_cadence`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/ghost_cold_boot.py

- lines: 177 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-01 21:02
- public functions (4): `cold_boot`, `boot_context`, `boot_and_fold`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/afk_orchestrator.py`, `mag/memlang.py`, `mag/skill_pipeline.py`

### mag/ghost_control.py

- lines: 139 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 14:16
- public functions (2): `control`, `main`
- public classes (0): none
- test files (1): `tests/test_surface_contract.py`
- readers (3): `dashboard/rest.py`, `mag/ghost_talk.py`, `mag/live_report.py`

### mag/ghost_cross.py

- lines: 505 | parse: ok | last commit: 60e18c524 2026-08-08 | mtime: 2026-08-08 05:40
- public functions (3): `run_chain`, `run_swarm`, `run_campaign_cross`
- public classes (3): `HopResult`, `ChainResult`, `SwarmResult`
- test files (0): none
- readers (2): `mag/research_director.py`, `memory/trash/20260810T202850Z/_tmp_research_sprint.py`

### mag/ghost_director.py

- lines: 654 | parse: ok | last commit: 60e18c524 2026-08-08 | mtime: 2026-08-07 22:48
- public functions (7): `build_director_context`, `director_cycle`, `director_feedback_loop`, `run_director_ladder`, `ladder_summary`, `print_ladder_summary`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/ghost_doctor.py

- lines: 150 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 19:13
- public functions (5): `checkup`, `diagnose`, `prescribe`, `rounds`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/ghost_experimenter.py

- lines: 239 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 18:41
- public functions (6): `experiment_plan`, `run_experiment`, `record_training`, `learn_steer_protocol`, `ghost_play`, `main`
- public classes (0): none
- test files (0): none
- readers (4): `mag/governor_autorun.py`, `mag/session_rib.py`, `memory/runs/drive_batch.py`, `memory/runs/experiment_loop.py`

### mag/ghost_grok_dashboard.py

- lines: 183 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 13:31
- public functions (4): `dispatch`, `savings`, `saved_vs_projected`, `main`
- public classes (0): none
- test files (0): none
- readers (4): `dashboard/rest.py`, `mag/ecosystem_surface.py`, `mag/ghost_control.py`, `mag/rightsize_api.py`

### mag/ghost_identity.py

- lines: 142 | parse: ok | last commit: 60e18c524 2026-08-08 | mtime: 2026-08-08 15:59
- public functions (2): `get_ghost_identity_block`, `get_ghost_system_prompt`
- public classes (0): none
- test files (0): none
- readers (2): `mag/context_compression.py`, `mag/training_packager.py`

### mag/ghost_leak_detector.py

- lines: 1054 | parse: ok | last commit: 482e0a3c8 2026-08-08 | mtime: 2026-08-08 19:11
- public functions (15): `plant_canary`, `load_canaries`, `deactivate_canary`, `scan_canaries`, `scan_entropy`, `scan_whisper_timing`, `scan_collusion`, `generate_tesuji_probe`, `score_tesuji`, `get_tesuji_scores`, `classify_leak`, `execute_response`, `leak_detect`, `seed_default_canaries`, `subscribe_leak_events`
- public classes (4): `Canary`, `LeakSignal`, `TesujiProbe`, `LeakReport`
- test files (0): none
- readers (4): `mag/ghost.py`, `mag/lens_tournament.py`, `mag/novelty_lens.py`, `mag/research_class.py`

### mag/ghost_ledger.py

- lines: 273 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 07:47
- public functions (5): `write_entry`, `read_ledger`, `ledger_summary`, `sync_deepseek_usage`, `backfill_manual_calls`
- public classes (0): none
- test files (0): none
- readers (5): `mag/ai_landscape.py`, `mag/copilot_bridge.py`, `mag/preflight.py`, `mag/tesuji_surface.py`, `memory/runs/union_audit/_write_jsonl.py`

### mag/ghost_memlance.py

- lines: 438 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 14:23
- public functions (7): `index`, `select`, `select_wave`, `trace_state`, `verify`, `self_check`, `main`
- public classes (0): none
- test files (2): `tests/test_ghost_memlance_notebook.py`, `tests/test_memlance_wave.py`
- readers (10): `_memlance.py`, `mag/ask_router.py`, `mag/game_campaign.py`, `mag/grokbot_cold_edges.py`, `mag/mem_lands.py`, `mag/novelty_lens.py`, `mag/openclaw_catalog.py`, `mag/research_class.py` + 2 more

### mag/ghost_nudge.py

- lines: 124 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 13:49
- public functions (4): `spec`, `nudge`, `auto`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `experiments/cascade_whisper.yaml`, `mag/afk_loop.py`, `mag/ghost_talk.py`

### mag/ghost_pylance.py

- lines: 335 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 08:14
- public functions (8): `diagnose`, `verify_edit`, `symbols`, `references`, `trace_value`, `imports`, `self_check`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/openclaw_catalog.py`

### mag/ghost_server.py

- lines: 114 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 05:54
- public functions (4): `manifest`, `advertise`, `help`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/ghost_spooky.py

- lines: 163 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 22:15
- public functions (3): `probe`, `all_abilities`, `main`
- public classes (0): none
- test files (1): `tests/test_ghost_spooky.py`
- readers (1): `mag/ghost_talk.py`

### mag/ghost_summon.py

- lines: 346 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 11:59
- public functions (8): `current_state`, `future_state`, `coldest_vertices`, `core_invariants_status`, `stale_skip`, `gather`, `summon`, `main`
- public classes (0): none
- test files (1): `tests/test_ghost_summon.py`
- readers (13): `dashboard/rest.py`, `mag/corpus_ingest.py`, `mag/end_state.py`, `mag/grokbot_cold_edges.py`, `mag/intent_rightsize.py`, `mag/orphan_sense.py`, `mag/persona_direction.py`, `mag/press_digest.py` + 5 more

### mag/ghost_talk.py

- lines: 146 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 14:30
- public functions (3): `reply`, `repl`, `main`
- public classes (0): none
- test files (1): `tests/test_ghost_spooky.py`
- readers (1): `dashboard/rest.py`

### mag/ghost_whisper.py

- lines: 163 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-09 21:39
- public functions (3): `whisper`, `decode`, `main`
- public classes (0): none
- test files (0): none
- readers (6): `experiments/cascade_whisper.yaml`, `mag/afk_loop.py`, `mag/ghost_cold_boot.py`, `mag/partner_puppet.py`, `mag/whisper_image.py`, `mag/whisper_route.py`

### mag/git_divergence.py

- lines: 117 | parse: ok | last commit: ad10682d0 2026-09-15 | mtime: 2026-09-15 23:07
- public functions (3): `measure`, `render`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/glm_flash.py

- lines: 112 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-28 18:16
- public functions (2): `cached_chat`, `status`
- public classes (0): none
- test files (0): none
- readers (7): `mag/_cache_ab_probe.py`, `mag/_exp_a_cache_retrigger.py`, `mag/cache_watch.py`, `mag/offerings.py`, `memory/runs/_probe_free_bus.py`, `memory/runs/audit_20260828/run_panel.py`, `scripts/probe_cache_ab.py`

### mag/gopher_lite.py

- lines: 251 | parse: ok | last commit: a5dd96176 2026-09-25 | mtime: 2026-09-23 14:25
- public functions (9): `spent_today_credits`, `gate`, `record`, `meter_row`, `chat`, `chore_label_farm`, `chore_census`, `run_once`, `status`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/governance.py

- lines: 214 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (2): `broadcast_steer`, `build_governance`
- public classes (0): none
- test files (0): none
- readers (4): `dashboard/rest.py`, `mag/brain.py`, `mag/context_pack.py`, `mag/decision_framework.py`

### mag/governor.py

- lines: 397 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-24 08:15
- public functions (11): `queue_candidates`, `agent_state_candidates`, `boot_manifest`, `all_candidates`, `score`, `exec_spec_doc`, `exec_cli_wiring`, `exec_queue_task`, `exec_selftest`, `run_cycle`, `main`
- public classes (0): none
- test files (2): `tests/test_governor_autorun.py`, `tests/test_governor_fallback.py`
- readers (8): `mag/autopilot.py`, `mag/autorun_status.py`, `mag/canvas_bridge.py`, `mag/framework_map.py`, `mag/governor_autorun.py`, `mag/openclaw_catalog.py`, `main.py`, `memory/runs/union_audit/_write_jsonl.py`

### mag/governor_autorun.py

- lines: 2183 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 09:53
- public functions (12): `estimate_cost`, `match_skills`, `route_task`, `queue_has_goal`, `recently_terminal_goal`, `enqueue_routed`, `fill_queue`, `plan_pending`, `execute_routed_task`, `autorun_once`, `autorun_loop`, `main`
- public classes (0): none
- test files (7): `tests/test_autorun_v1.py`, `tests/test_governor_autorun.py`, `tests/test_loop_breaker.py`, `tests/test_remote_control.py`, `tests/test_roadmap_gap_probe.py`, `tests/test_source_trace.py`, `tests/test_steward_queue_has_goal.py`
- readers (19): `mag/autopilot.py`, `mag/cheap_swarm.py`, `mag/framework_map.py`, `mag/gap_analysis.py`, `mag/ghost.py`, `mag/improve_loop.py`, `mag/orchestrator.py`, `mag/ponytail_audit.py` + 11 more

### mag/gpipes.py

- lines: 401 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-09-27 23:19
- public functions (7): `fan_out`, `pipe_status`, `collect`, `kill_pipe`, `list_pipes`, `main`, `supervise`
- public classes (0): none
- test files (1): `tests/test_supervision_soak.py`
- readers (5): `dashboard/rest.py`, `main.py`, `memory/working/patch_gpipes_status.py`, `tools/autopilot.py`, `tools/spawn_gpipe.py`

### mag/gpu_ghost.py

- lines: 309 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 12:53
- public functions (4): `gpu_status`, `partition`, `afk_train`, `main`
- public classes (0): none
- test files (0): none
- readers (8): `mag/intent_rightsize.py`, `mag/invariant_lattice.py`, `mag/lens_chain.py`, `mag/mem_ollama.py`, `mag/offline.py`, `mag/stateless_research.py`, `mag/swarm_capacity.py`, `mag/vram_memory.py`

### mag/gpu_k8s.py

- lines: 228 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 00:50
- public functions (5): `find_gpu_pod`, `read_telemetry`, `sample`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (6): `mag/gpu_ghost.py`, `mag/gpu_lifecycle.py`, `mag/gpu_memweave.py`, `mag/mem_lands.py`, `mag/surface_render.py`, `mag/work_register.py`

### mag/gpu_lifecycle.py

- lines: 138 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 09:40
- public functions (4): `resources`, `learn`, `route`, `status`
- public classes (0): none
- test files (0): none
- readers (10): `mag/compute_reconcile.py`, `mag/ghost.py`, `mag/mem_invariant_map.py`, `mag/resource_governor.py`, `mag/rib_gif.py`, `mag/steal_pack.py`, `mag/swarm_rightsize.py`, `mag/system_telemetry.py` + 2 more

### mag/gpu_memweave.py

- lines: 113 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 19:34
- public functions (2): `route`, `status`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/grammar_transfer.py

- lines: 266 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-06 02:11
- public functions (9): `features`, `corrupt`, `carve`, `audit`, `run_surface`, `units_chunks`, `units_sections`, `units_grid_rows`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/grok_bot.py

- lines: 290 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-13 04:52
- public functions (6): `spec`, `capture_verbose`, `steer`, `heartbeat`, `grab_bookmarks`, `status`
- public classes (0): none
- test files (0): none
- readers (6): `mag/chord_pipeline.py`, `mag/frontier_advisor.py`, `mag/governor_autorun.py`, `mag/grok_weave.py`, `mag/republic_loop.py`, `mag/steer_engine.py`

### mag/grok_brief.py

- lines: 162 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 07:54
- public functions (3): `build`, `drop`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/republic_loop.py`

### mag/grok_desktop.py

- lines: 165 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-13 18:08
- public functions (5): `steer`, `heartbeat`, `spec`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/grok_free.py

- lines: 383 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 22:04
- public functions (10): `route_surface`, `status`, `capture`, `save_idea`, `handoff`, `control_signal`, `control_status`, `write_skill`, `cadence`, `main`
- public classes (0): none
- test files (0): none
- readers (7): `mag/ai_landscape.py`, `mag/doctor.py`, `mag/ghost.py`, `mag/governor_autorun.py`, `mag/memlang.py`, `mag/republic_os.py`, `main.py`

### mag/grok_frontier_loop.py

- lines: 270 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 01:04
- public functions (7): `budget_status`, `frontier_targets`, `pick_target`, `run_frontier_steal`, `learn`, `cycle`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/grok_hub.py`, `mag/work_register.py`

### mag/grok_gate.py

- lines: 83 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 13:04
- public functions (2): `should_use_grok`, `main`
- public classes (0): none
- test files (0): none
- readers (6): `mag/ghost_grok_dashboard.py`, `mag/ghost_nudge.py`, `mag/grok_rightsize.py`, `mag/oh_fuck.py`, `mag/scrum.py`, `mag/skill_pipeline.py`

### mag/grok_hub.py

- lines: 234 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 01:22
- public functions (6): `group_asks`, `dispatch_groups`, `record`, `cycle`, `learn`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/work_register.py`

### mag/grok_mirror.py

- lines: 354 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 19:13
- public functions (9): `set_active_coding_window`, `active_coding_window`, `capture_plan`, `interpret`, `questions`, `research_project`, `distill_skill`, `run_mirror`, `main`
- public classes (0): none
- test files (0): none
- readers (5): `dashboard/rest.py`, `mag/doctor.py`, `mag/ghost.py`, `mag/memlang.py`, `main.py`

### mag/grok_rightsize.py

- lines: 669 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-05 22:10
- public functions (13): `xai_key_chain`, `xai_key_status`, `probe_xai_keys`, `classify_task`, `budget_for`, `compress_prompt`, `estimate_tokens`, `estimate_cost`, `call_grok`, `call_grok_free`, `ghost_grok_task`, `log_grok_call`, `ledger_summary`
- public classes (1): `GrokCallResult`
- test files (0): none
- readers (29): `mag/ai_landscape.py`, `mag/aos_grok.py`, `mag/code_map.py`, `mag/ghost.py`, `mag/grok_free.py`, `mag/grok_frontier_loop.py`, `mag/grok_hub.py`, `mag/grok_mirror.py` + 21 more

### mag/grok_route.py

- lines: 48 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-05 22:08
- public functions (3): `grok_cash_allowed`, `grok_cli_ok`, `route_report`
- public classes (0): none
- test files (0): none
- readers (1): `memory/runs/x_history_mine/20260926/remote_day_slice_ingest.py`

### mag/grok_seat_burner.py

- lines: 503 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-26 16:37
- public functions (12): `classify_task`, `record_spend`, `spend_ledger`, `seats_status`, `build_instruction`, `verify_output`, `run_watched`, `drive_watched_parallel`, `drive_parallel`, `steer`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (14): `_alpha_frontier.py`, `_grok_business_test.py`, `logs/grok_tandem_review.py`, `mag/_grok_corpus_burn.py`, `mag/_salon_burn.py`, `mag/game_piece_tandem.py`, `mag/governor_autorun.py`, `mag/seat_availability.py` + 6 more

### mag/grok_steer.py

- lines: 136 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-16 18:39
- public functions (3): `decide_steer`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/openclaw_catalog.py`, `memory/runs/test_grok_steer.py`

### mag/grok_tandem.py

- lines: 142 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-05 22:33
- public functions (5): `ask_cli`, `ask_bot`, `ask`, `tandem`, `probe`
- public classes (0): none
- test files (0): none
- readers (1): `mag/lane_salon.py`

### mag/grok_terminal.py

- lines: 361 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 09:23
- public functions (6): `is_critical`, `scan_for_critical`, `launch_terminal`, `run_critical`, `run_cadence`, `main`
- public classes (0): none
- test files (0): none
- readers (5): `mag/cheap_swarm.py`, `mag/ghost.py`, `mag/ghost_grok_dashboard.py`, `mag/governor_autorun.py`, `main.py`

### mag/grok_warm_rib.py

- lines: 162 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-25 23:00
- public functions (6): `warm_rib_text`, `publish`, `prefix`, `inject`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `harness/grok_build_coder.py`, `harness/grok_cli.py`

### mag/grok_weave.py

- lines: 202 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 07:54
- public functions (5): `telemetry`, `holograms`, `author_ribs`, `weave`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/republic_loop.py`

### mag/grokbot_cold_edges.py

- lines: 186 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 01:07
- public functions (7): `cold_edges`, `verkle_coordinate`, `memlance_channel`, `publish`, `build_rib`, `run`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/republic_loop.py`, `mag/tool_synthesis.py`

### mag/grounding_wave.py

- lines: 975 | parse: ok | last commit: 118333dd1 2026-09-16 | mtime: 2026-09-16 21:26
- public functions (9): `post`, `void`, `contest`, `witness`, `verify`, `render`, `view`, `resolve_ground_state`, `main`
- public classes (1): `GateRefusal`
- test files (3): `tests/test_falsifier_ledger.py`, `tests/test_grounding_wave_v4.py`, `tests/test_wave_driver.py`
- readers (5): `configs/succession_contract.yaml`, `mag/perturbation_battery.py`, `scripts/build_deck.py`, `scripts/wave_driver.py`, `tools/rebuild_grounding_wave_md.py`

### mag/grove.py

- lines: 150 | parse: ok | last commit: f31c0e926 2026-08-05 | mtime: 2026-08-06 18:28
- public functions (2): `build`, `list_nodes`
- public classes (0): none
- test files (2): `tests/test_v3_deepseek_wiring.py`, `tests/test_v3_modules.py`
- readers (3): `dashboard/rest.py`, `mag/framework_map.py`, `main.py`

### mag/growth_cycle.py

- lines: 463 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (6): `load_steer`, `growth_cycle_enabled`, `run_growth_cycle`, `growth_cycle_status`, `maybe_run_growth_cycle`, `main`
- public classes (0): none
- test files (1): `tests/test_growth_cycle.py`
- readers (2): `mag/governor_autorun.py`, `main.py`

### mag/gstd_probe.py

- lines: 209 | parse: ok | last commit: 9c8fc49e8 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (2): `run_gstd_probe`, `build_gstd_stack_row`
- public classes (0): none
- test files (1): `tests/test_local_gpu_probes.py`
- readers (2): `mag/stack.py`, `main.py`

### mag/guard.py

- lines: 104 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-28 19:44
- public functions (3): `doctor_print`, `ensure_lab`, `guard_loop`
- public classes (0): none
- test files (0): none
- readers (3): `mag/boot.py`, `mag/power.py`, `main.py`

### mag/guard_registry.py

- lines: 255 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 21:49
- public functions (3): `reconcile`, `check`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/ghost.py`

### mag/guardrail_sentinel.py

- lines: 149 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 12:53
- public functions (4): `ping`, `audit`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/dogfood_audit.py`, `mag/self_steal.py`

### mag/gygax_steal.py

- lines: 160 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 16:58
- public functions (5): `route_research`, `self_map`, `learn`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_gygax_steal.py`
- readers (0): none

### mag/hall_shared_supper.py

- lines: 163 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 03:03
- public functions (6): `start_state`, `root`, `play`, `replay`, `run`, `verify`
- public classes (0): none
- test files (0): none
- readers (4): `mag/aos_bus_watcher.py`, `mag/autonomous_research.py`, `memory/runs/_aos_fork.py`, `memory/runs/_aos_resolve.py`

### mag/handoff_inbox.py

- lines: 144 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (4): `list_disk_handoffs`, `list_orchestrator_queue`, `scrum_snapshot`, `build_inbox`
- public classes (0): none
- test files (1): `tests/test_handoff_inbox.py`
- readers (4): `configs/modules.yaml`, `dashboard/rest.py`, `mag/framework_map.py`, `scripts/_desk_step_cycle.py`

### mag/harness.py

- lines: 735 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-31 07:26
- public functions (16): `run_once`, `health_check`, `run_continuous`, `test_scenario_1`, `test_scenario_2`, `test_scenario_3`, `test_scenario_4`, `test_scenario_5`, `test_scenario_6`, `test_scenario_7`, `cmd_run_once`, `cmd_run_continuous`, `cmd_test`, `cmd_status`, `cmd_reset`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/dogfood_audit.py`, `mag/organ_map.py`, `state/backups/orphan_close_20260906/organ_map.py`

### mag/harvest_fold.py

- lines: 161 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-16 13:15
- public functions (6): `harvest`, `fold`, `cadence`, `report_back`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_harvest_fold.py`
- readers (1): `mag/republic_loop.py`

### mag/headless.py

- lines: 203 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-16 17:33
- public functions (7): `no_window_flags`, `install_no_window_defaults`, `run_headless`, `popen_headless`, `py_cmd`, `run_py`, `popen_py`
- public classes (0): none
- test files (2): `tests/test_headless.py`, `tests/test_headless_law.py`
- readers (30): `mag/autonomous_research.py`, `mag/batch_drain.py`, `mag/coding_session_loop.py`, `mag/desk_ops.py`, `mag/dogfood_audit.py`, `mag/governor.py`, `mag/governor_autorun.py`, `mag/gpipes.py` + 22 more

### mag/health.py

- lines: 365 | parse: ok | last commit: 6d417abd5 2026-09-26 | mtime: 2026-09-26 17:24
- public functions (8): `in_mag_cage`, `reconnect_plan`, `check_ollama`, `check_openrouter`, `check_grok_harness`, `gap_report`, `sanity`, `catch_up`
- public classes (0): none
- test files (2): `tests/test_reconnect_cage_first.py`, `tests/test_surface_contract.py`
- readers (19): `dashboard/rest.py`, `mag/boot.py`, `mag/compute_reconcile.py`, `mag/context_pack.py`, `mag/dispatch.py`, `mag/framework_map.py`, `mag/guard.py`, `mag/lifecycle.py` + 11 more

### mag/hermes_steering.py

- lines: 340 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-11 22:22
- public functions (4): `cmd_dispatch`, `cmd_steer`, `cmd_jobs`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/kabuki_salon.py`, `mag/tavern_chat.py`

### mag/hermes_warm_boot.py

- lines: 124 | parse: ok | last commit: a5dd96176 2026-09-25 | mtime: 2026-09-23 19:23
- public functions (2): `warm_boot`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/hero_simulation.py

- lines: 395 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-07 01:13
- public functions (11): `load_loot_registry`, `cards37_paths`, `load_grave_registry`, `loads_ok`, `parse_nav`, `find_destination_pages`, `build_surface`, `loot_tokens`, `reach_loot`, `reach_grave`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/hf_space.py

- lines: 585 | parse: ok | last commit: 60e18c524 2026-08-08 | mtime: 2026-08-08 14:36
- public functions (7): `hf_configured`, `build_space`, `deploy_space`, `store_cold_vector`, `list_cold_vectors`, `hf_auto_publish_loop`, `hf_status`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/holographic_q.py

- lines: 848 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-01 21:02
- public functions (9): `create_q_session`, `emit_q_knot`, `reconstitute_q`, `get_active_q_sessions`, `q_agent_loop`, `decipher_q_context`, `q_status`, `create_swarm_session`, `freeze_context`
- public classes (3): `QKnot`, `QSession`, `SwarmSession`
- test files (1): `tests/test_q_boundaries.py`
- readers (8): `mag/ghost.py`, `mag/persistent_agent.py`, `memory/trash/20260810T202850Z/_tmp_parallel_agent_test.py`, `memory/working/_nest.py`, `memory/working/_patch_freeze_organs.py`, `memory/working/_prove_freeze.py`, `scripts/q_knot_smoke.py`, `tools/qknot_b1.py`

### mag/honest_cache_meter.py

- lines: 498 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-01 21:00
- public functions (12): `log`, `utc_now_iso`, `today_str`, `yesterday_str`, `fmt_money`, `fmt_frac`, `normalize_usage`, `cost_usd`, `counterfactual_cost_usd`, `capture_anthropic_response`, `capture_openai_response`, `main`
- public classes (4): `RateCard`, `Usage`, `UsageParseError`, `CacheMeter`
- test files (1): `tests/test_honest_cache_meter.py`
- readers (0): none

### mag/hood.py

- lines: 153 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-29 21:28
- public functions (2): `snapshot`, `main`
- public classes (0): none
- test files (1): `tests/test_hood.py`
- readers (1): `dashboard/rest.py`

### mag/host_resolver.py

- lines: 206 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-12 23:01
- public functions (5): `resolve_host`, `get_network_state`, `update_network_state`, `resolve_host_for_service`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `configs/organs/host_resolver.yaml`, `mag/organ_map.py`

### mag/host_roundtrip.py

- lines: 110 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 19:41
- public functions (4): `instruct`, `remember_host_state`, `roundtrip`, `status`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/hour_test.py

- lines: 117 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 06:24
- public functions (3): `start`, `report`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/hydro_xor_sim.py

- lines: 294 | parse: ok | last commit: 75c030d29 2026-09-16 | mtime: 2026-09-16 16:11
- public functions (4): `simulate`, `truth_table`, `p_report`, `main`
- public classes (2): `SimParams`, `SimResult`
- test files (1): `tests/test_hydro_xor_sim.py`
- readers (1): `mag/water_graph.py`

### mag/icon_drop.py

- lines: 376 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 17:22
- public functions (6): `desktop_folder`, `drop`, `drop_shortcut`, `auto`, `list_icons`, `main`
- public classes (0): none
- test files (3): `tests/test_icon_drop_escape.py`, `tests/test_icon_drop_fold.py`, `tests/test_icon_drop_icon_thread.py`
- readers (2): `mag/skill_pipeline.py`, `mag/training_set.py`

### mag/idea_flow.py

- lines: 600 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 20:03
- public functions (1): `build_idea_flow`
- public classes (0): none
- test files (0): none
- readers (1): `dashboard/rest.py`

### mag/idea_graph.py

- lines: 537 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (14): `ensure_dirs`, `load_nodes`, `load_edges`, `get_node`, `patch_node`, `list_nodes`, `add_node`, `link`, `neighborhood`, `pack_node`, `write_latest_face`, `seed_from_working_and_agent_state`, `format_list`, `summary`
- public classes (0): none
- test files (1): `tests/test_idea_graph.py`
- readers (12): `configs/modules.yaml`, `dashboard/rest.py`, `mag/framework_map.py`, `mag/grok_free.py`, `mag/janitor.py`, `mag/mycelium.py`, `mag/orphan_timer.py`, `mag/research_lens.py` + 4 more

### mag/improve.py

- lines: 2773 | parse: ok | last commit: 2ba484fc9 2026-09-28 | mtime: 2026-09-28 12:47
- public functions (19): `load_config`, `ensure_dirs`, `read_candidates`, `append_candidates`, `update_candidate_status`, `provider_probe_due`, `run_provider_probe`, `crash_log_census`, `behavioral_events_census`, `scout`, `run_eval`, `rank_candidates_for_brief`, `synthesize_field_brief`, `deepseek_rank_top`, `improve_once`, `deep_dive`, `status_summary`, `promote_apply`, `promote_reject`
- public classes (0): none
- test files (12): `tests/test_auto_promote.py`, `tests/test_behavioral_awareness.py`, `tests/test_demote_candidates.py`, `tests/test_growth_cycle.py`, `tests/test_improve_behavioral_scout.py`, `tests/test_improve_crash_scout.py`, `tests/test_improve_provider_probe.py`, `tests/test_improve_status_scheduled_task.py` + 4 more
- readers (14): `configs/modules.yaml`, `dashboard/rest.py`, `mag/api_gateway.py`, `mag/autopilot.py`, `mag/blast.py`, `mag/factory_machine.py`, `mag/growth_cycle.py`, `mag/improve_loop.py` + 6 more

### mag/improve_loop.py

- lines: 328 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 16:38
- public functions (4): `write_cloud_handoff`, `ingest_cloud_handoffs`, `run_improve_cycle`, `main`
- public classes (0): none
- test files (2): `tests/test_growth_cycle.py`, `tests/test_improve_loop.py`
- readers (9): `configs/modules.yaml`, `dashboard/rest.py`, `mag/factory_machine.py`, `mag/framework_map.py`, `mag/growth_cycle.py`, `mag/peer_handoff.py`, `mag/swarm_health.py`, `mag/system_map.py` + 1 more

### mag/ingest_registry.py

- lines: 556 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (2): `resolve_and_ingest`, `file_url`
- public classes (0): none
- test files (0): none
- readers (3): `mag/pdf_layout.py`, `mag/research_pack.py`, `mag/session_dossier.py`

### mag/integrity_kernel.py

- lines: 299 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-25 11:17
- public functions (7): `integrity_kernel`, `tri_state`, `verify_execution`, `scan_opspec`, `opspec_clear`, `symmetry_audit`, `run_inbox_e2e`
- public classes (6): `Claim`, `VerkleWitness`, `Executor`, `Scrutiny`, `Inbox`, `Outbox`
- test files (0): none
- readers (4): `mag/_verify_sharp_edge.py`, `mag/lab_episode.py`, `mag/queue_gate.py`, `mag/work_register.py`

### mag/intent_rightsize.py

- lines: 239 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 07:54
- public functions (4): `temporal_chain`, `rightsize`, `test_limits`, `status`
- public classes (0): none
- test files (0): none
- readers (3): `mag/autonomous_research.py`, `mag/swarm_self.py`, `mag/tool_synthesis.py`

### mag/intention_brief.py

- lines: 290 | parse: ok | last commit: e96fd62a4 2026-08-07 | mtime: 2026-08-06 21:26
- public functions (3): `compile_intention`, `render_brief_for_model`, `brief_public`
- public classes (0): none
- test files (1): `tests/test_voice_turn.py`
- readers (3): `mag/framework_map.py`, `mag/voice_handoff.py`, `mag/voice_turn.py`

### mag/interrupt_pipeline.py

- lines: 219 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 20:14
- public functions (5): `value`, `interrupt`, `assemble`, `stack`, `status`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/intervention_gate.py

- lines: 470 | parse: ok | last commit: a5dd96176 2026-09-25 | mtime: 2026-09-25 20:54
- public functions (11): `state_decayed`, `decide`, `register_decision`, `load_register`, `last_injected_step`, `summarize`, `score_run`, `run_gate_over`, `worked_example`, `self_test`, `main`
- public classes (3): `MemoryEntry`, `GatePolicy`, `GateDecision`
- test files (1): `tests/test_intervention_gate.py`
- readers (0): none

### mag/invariant.py

- lines: 321 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-26 08:06
- public functions (9): `stable_prefix`, `freeze`, `check`, `instruction_sha`, `freeze_instructions`, `check_instructions`, `tail`, `preamble`, `main`
- public classes (0): none
- test files (1): `tests/test_invariant.py`
- readers (5): `mag/cache_router.py`, `mag/chord.py`, `mag/prefix_prover.py`, `mag/reconstruct.py`, `mag/skill_pipeline.py`

### mag/invariant_lattice.py

- lines: 187 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 17:36
- public functions (6): `mycelial_view`, `lattice_view`, `steer_ollama`, `dispatch_to_k8s`, `render`, `main`
- public classes (0): none
- test files (0): none
- readers (7): `mag/gap_swarm_experiment.py`, `mag/ghost_doctor.py`, `mag/ghost_experimenter.py`, `mag/mem_invariant_map.py`, `mag/rib_renderer.py`, `mag/session_rib.py`, `mag/verkle_lance.py`

### mag/invariant_ledger.py

- lines: 185 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 09:27
- public functions (4): `ledger`, `interconnect`, `gaps_at_glance`, `status`
- public classes (0): none
- test files (0): none
- readers (3): `mag/invariant_npcs.py`, `mag/steal_lens.py`, `scripts/_audit_have_need.py`

### mag/invariant_npcs.py

- lines: 252 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-15 05:34
- public functions (7): `roster`, `from_invariant_ledger`, `manifest`, `nourish`, `resolve`, `talk`, `status`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/invariant_surface.py

- lines: 258 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-10 16:55
- public functions (7): `files_under`, `bucket_of`, `clean`, `norm`, `subject_of`, `contradicts`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `_g52_dump_controverted.py`

### mag/janitor.py

- lines: 273 | parse: ok | last commit: 60e18c524 2026-08-08 | mtime: 2026-08-08 09:56
- public functions (5): `last_report`, `prune`, `document`, `run`, `main`
- public classes (0): none
- test files (0): none
- readers (7): `dashboard/rest.py`, `mag/cleanup.py`, `mag/framework_map.py`, `mag/governor_autorun.py`, `mag/ops_graph.py`, `main.py`, `memory/runs/union_audit/_write_jsonl.py`

### mag/job_floor.py

- lines: 225 | parse: ok | last commit: 60e18c524 2026-08-08 | mtime: 2026-08-07 18:15
- public functions (7): `create_job`, `claim_job`, `verify_job`, `stuck_jobs`, `status`, `list_jobs`, `main`
- public classes (0): none
- test files (3): `tests/test_pupeteering.py`, `tests/test_skill_drop.py`, `tests/test_spec_gate_job_floor.py`
- readers (3): `main.py`, `memory/runs/job_floor/20260828-codex-lab/launch_panel.py`, `tools/pupeteer_gauntlet.py`

### mag/jones_lens.py

- lines: 125 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 09:32
- public functions (5): `vector`, `braid`, `jones`, `verkle_vertex`, `status`
- public classes (0): none
- test files (0): none
- readers (7): `mag/chain_substrate.py`, `mag/compiler_lang.py`, `mag/grokbot_cold_edges.py`, `mag/intent_rightsize.py`, `mag/persona_direction.py`, `mag/shader_rib.py`, `mag/territory_solver.py`

### mag/judge.py

- lines: 138 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (1): `judge`
- public classes (0): none
- test files (0): none
- readers (1): `mag/daemon.py`

### mag/k8s_bridge.py

- lines: 164 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 17:36
- public functions (12): `cronjobs`, `jobs`, `pods`, `logs`, `get_json`, `apply_file`, `delete_job`, `create_job_from_cronjob`, `cp_to_pod`, `cp_from_pod`, `exec_read`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/gpu_k8s.py`, `mag/rib_k8s.py`, `mag/swarm_capacity.py`

### mag/kabuki_salon.py

- lines: 179 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-07 08:09
- public functions (2): `salon`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `scripts/astra_convo_loop.sh`

### mag/key_law.py

- lines: 107 | parse: ok | last commit: 3ee362d04 2026-09-24 | mtime: 2026-09-24 15:08
- public functions (3): `get`, `audit`, `status`
- public classes (0): none
- test files (0): none
- readers (8): `mag/lane_supervisor.py`, `seed/engines/build_seed.py`, `tools/build_plain_pdf.py`, `tools/build_seed.py`, `tools/roblox_npc_gateway.py`, `tools/seed_salon.py`, `tools/seed_v2.py`, `tools/violation_ratchet.py`

### mag/knot_at_close.py

- lines: 280 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-07 08:12
- public functions (1): `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/knot_math.py

- lines: 241 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (7): `parse_iso_minute`, `file_time_anchor`, `load_session_meta`, `theme_vector`, `scalar_knot_proxy`, `content_commit`, `duration_minutes`
- public classes (0): none
- test files (0): none
- readers (1): `mag/session_dossier.py`

### mag/knot_untangle.py

- lines: 232 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 22:15
- public functions (4): `tangle`, `scan_chain`, `untangle`, `status`
- public classes (0): none
- test files (0): none
- readers (2): `mag/abundance_rogue.py`, `mag/gap_routed_handoff.py`

### mag/knowledge_graph.py

- lines: 560 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-15 10:30
- public functions (10): `global_search`, `local_search`, `capability_atom`, `dream`, `build`, `known`, `context`, `fold`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (24): `mag/ai_landscape.py`, `mag/attractor_tools.py`, `mag/dirac_loop.py`, `mag/doctor_rightsize.py`, `mag/dogfood_audit.py`, `mag/frontier_batch.py`, `mag/frontier_intake.py`, `mag/gap_resolver.py` + 16 more

### mag/kv_seal.py

- lines: 142 | parse: ok | last commit: 4cb4c99a7 2026-09-22 | mtime: 2026-09-22 01:39
- public functions (5): `sidecar_path`, `seal_page`, `verify_page`, `refill_page`, `status`
- public classes (0): none
- test files (1): `tests/test_kv_seal.py`
- readers (0): none

### mag/kvos_block.py

- lines: 112 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-10 08:23
- public functions (3): `cut_blocks`, `chain_file`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/desk_tools.py`

### mag/lab_episode.py

- lines: 493 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-29 13:38
- public functions (9): `legal_actions`, `fire_shared_dep`, `new_blackout`, `shock`, `step`, `choose`, `run_episode`, `run_blackout`, `main`
- public classes (11): `ActionType`, `Kind`, `Phys`, `Seen`, `Svc`, `Edge`, `Entity`, `World`, `Observation`, `Topology`, `Episode`
- test files (1): `tests/test_lab_episode.py`
- readers (1): `mag/openclaw_catalog.py`

### mag/ladder.py

- lines: 198 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-25 12:35
- public functions (4): `sense`, `walk_cycle`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/lane_breaker.py

- lines: 136 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-13 09:56
- public functions (4): `check`, `clear`, `selftest`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/wave_fire.py`

### mag/lane_cadence.py

- lines: 270 | parse: ok | last commit: 790145ab1 2026-09-26 | mtime: 2026-09-26 01:44
- public functions (8): `retry_after`, `best_hours`, `demote_after`, `cooldown`, `pick_free_glm`, `brake_after`, `status`, `learn`
- public classes (0): none
- test files (2): `tests/test_loop_death_guards.py`, `tests/test_zai_burst.py`
- readers (4): `mag/_verify_rung5.py`, `mag/fuel_feed.py`, `mag/glm_flash.py`, `mag/queue_gate.py`

### mag/lane_effort.py

- lines: 358 | parse: ok | last commit: a5dd96176 2026-09-25 | mtime: 2026-09-25 20:17
- public functions (6): `tier_config`, `effort_for_width`, `call_budget_for_width`, `value_token_gate`, `fanout_gate`, `selftest`
- public classes (0): none
- test files (1): `tests/test_lane_effort.py`
- readers (1): `configs/lanes.yaml`

### mag/lane_probe.py

- lines: 150 | parse: ok | last commit: a0f7a593a 2026-09-24 | mtime: 2026-09-24 19:11
- public functions (6): `load_env_key_names`, `get_env_value`, `ping_lane`, `append_rows`, `run_once`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/lane_runner.py

- lines: 1141 | parse: ok | last commit: a23928aca 2026-09-27 | mtime: 2026-09-27 21:04
- public functions (24): `gate_drop`, `load_gate_block`, `build_gate_verdict`, `apply_cascade`, `gate_drop_v2`, `normalize_detail`, `cluster_step`, `cluster_report_step`, `flash_call`, `cycle_economist`, `cycle_research`, `cycle_builder`, `cycle_bard`, `cycle_elder`, `cycle_day_work`, `cycle_night`, `cycle_forge`, `cycle_watcher`, `cycle_harvest`, `cycle_prose`, `tesuji_pass`, `run_lane`, `daemon`, `main`
- public classes (0): none
- test files (3): `tests/test_hunger_ledger_parity.py`, `tests/test_lane_runner_cluster.py`, `tests/test_scripts_path_pins.py`
- readers (15): `agents/pytest-tmp-29352/test_cage_and_canonical_write_0/scripts_copy_repo/scripts/hunger_ledger.py`, `agents/pytest-tmp-29352/test_row_shape_mutation_goes_r0/scripts_repo_mut/scripts/hunger_ledger.py`, `agents/pytest-tmp-43872/test_cage_and_canonical_write_0/scripts_copy_repo/scripts/hunger_ledger.py`, `agents/pytest-tmp-43872/test_row_shape_mutation_goes_r0/scripts_repo_mut/scripts/hunger_ledger.py`, `agents/pytest-tmp-44744/test_cage_and_canonical_write_0/scripts_copy_repo/scripts/hunger_ledger.py`, `agents/pytest-tmp-44744/test_row_shape_mutation_goes_r0/scripts_repo_mut/scripts/hunger_ledger.py`, `agents/pytest-tmp-51488/test_cage_and_canonical_write_0/scripts_copy_repo/scripts/hunger_ledger.py`, `agents/pytest-tmp-51488/test_row_shape_mutation_goes_r0/scripts_repo_mut/scripts/hunger_ledger.py` + 7 more

### mag/lane_salon.py

- lines: 229 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 19:10
- public functions (2): `salon`, `main`
- public classes (0): none
- test files (2): `tests/test_dormant_gate_b2133.py`, `tests/test_loop_death_guards.py`
- readers (2): `mag/dormant.py`, `mag/openclaw_catalog.py`

### mag/lane_supervisor.py

- lines: 235 | parse: ok | last commit: d5ad6403e 2026-09-25 | mtime: 2026-09-25 14:01
- public functions (2): `probe`, `status`
- public classes (0): none
- test files (0): none
- readers (1): `tools/seed_v2.py`

### mag/lanes.py

- lines: 316 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 21:50
- public functions (12): `load_lanes`, `usage_log_path`, `briefs_dir`, `log_usage`, `usage_tail`, `usage_today_counts`, `text_has_priority`, `goal_lane`, `grok_escalations_today`, `can_escalate_grok`, `latest_brief_text`, `board_pack`
- public classes (0): none
- test files (0): none
- readers (16): `agents/critic.py`, `agents/escalate_grok.py`, `dashboard/rest.py`, `llm.py`, `mag/act.py`, `mag/ask.py`, `mag/brief_local.py`, `mag/context_pack.py` + 8 more

### mag/lattice_backfill.py

- lines: 403 | parse: ok | last commit: 2464edcba 2026-08-04 | mtime: 2026-08-04 18:48
- public functions (5): `parse_dig_meta`, `list_dig_files`, `backfill_instrument_chain`, `seed_lattice_store`, `run_backfill`
- public classes (0): none
- test files (1): `tests/test_lattice_query.py`
- readers (3): `mag/lattice_query.py`, `mag/verkle_audit.py`, `main.py`

### mag/lattice_dashboard.py

- lines: 257 | parse: ok | last commit: 4e7350700 2026-08-05 | mtime: 2026-08-06 18:28
- public functions (1): `build_lattice_summary`
- public classes (0): none
- test files (0): none
- readers (2): `dashboard/rest.py`, `main.py`

### mag/lattice_distance.py

- lines: 131 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-04 08:12
- public functions (4): `is_three_square`, `excluded_form`, `lattice_distance_ok`, `validate_voxel_coords`
- public classes (0): none
- test files (1): `tests/test_lattice_distance.py`
- readers (2): `dashboard-deploy/static/_rtfm_graph_data.py`, `dashboard/static/_rtfm_graph_data.py`

### mag/lattice_logic.py

- lines: 256 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-04 13:34
- public functions (7): `load`, `query`, `step_card`, `walk`, `chain`, `export`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/lattice_loop.py

- lines: 803 | parse: ok | last commit: c65c4e7aa 2026-08-05 | mtime: 2026-08-06 18:28
- public functions (11): `lattice_root`, `load_lattice`, `read_state`, `write_state`, `read_tip`, `append_chain_bead`, `normalize_url`, `should_enqueue_proposed`, `plant_status`, `start_loop`, `stop_loop`
- public classes (0): none
- test files (1): `tests/test_lattice_grounding.py`
- readers (4): `mag/lattice_backfill.py`, `mag/ponytail_audit.py`, `mag/virtual_desk_loop.py`, `main.py`

### mag/lattice_query.py

- lines: 130 | parse: ok | last commit: 2464edcba 2026-08-04 | mtime: 2026-08-04 18:48
- public functions (6): `load_nodes`, `load_edges`, `query_by_theme`, `neighbors`, `summary`, `graph_viewport`
- public classes (0): none
- test files (1): `tests/test_lattice_query.py`
- readers (4): `mag/clawbot.py`, `mag/lattice_dashboard.py`, `mag/verkle_audit.py`, `main.py`

### mag/launch_pad.py

- lines: 130 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (1): `build_launch_pad`
- public classes (0): none
- test files (1): `tests/test_launch_pad.py`
- readers (1): `dashboard/rest.py`

### mag/law.py

- lines: 322 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 16:19
- public functions (5): `seed`, `register`, `enforce`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_law.py`
- readers (6): `dashboard/rest.py`, `mag/governor_autorun.py`, `mag/lattice_logic.py`, `mag/ox_megaburn2.py`, `mag/ox_megaburn3.py`, `main.py`

### mag/leaked_prompt_mine.py

- lines: 138 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 15:08
- public functions (5): `inventory`, `mine_one`, `mine`, `create`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/auto_handoff.py`, `mag/frontier_steer.py`

### mag/learn_rightsize.py

- lines: 164 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 16:29
- public functions (4): `auto_catalog`, `rightsize_learning`, `learn_loop`, `main`
- public classes (0): none
- test files (0): none
- readers (4): `mag/afk_orchestrator.py`, `mag/corpus_expand.py`, `mag/memlang.py`, `mag/skill_pipeline.py`

### mag/legacy_audit.py

- lines: 331 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 12:53
- public functions (6): `classify`, `scan`, `catalog`, `retire`, `research`, `main`
- public classes (0): none
- test files (1): `tests/test_b285_enum_resolution_pins.py`
- readers (3): `dashboard/rest.py`, `mag/skill_pipeline.py`, `main.py`

### mag/lens_chain.py

- lines: 288 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 19:32
- public functions (6): `pick_lens`, `resolve`, `chain`, `lenses`, `prove`, `status`
- public classes (0): none
- test files (0): none
- readers (6): `mag/_deep_research_verkle_dedupe.py`, `mag/adventure_moonshot.py`, `mag/deep_research_moonshot.py`, `mag/interrupt_pipeline.py`, `mag/queue_analysis.py`, `mag/vessel_swarm.py`

### mag/lens_knot.py

- lines: 192 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 09:58
- public functions (5): `shared_events`, `knot_id`, `stories`, `swarm_truth`, `status`
- public classes (0): none
- test files (2): `mag/tests/test_identity_schema_portability.py`, `mag/tests/verify_identity_coupling.py`
- readers (9): `mag/agent_knot.py`, `mag/compiler_lang.py`, `mag/final_steal.py`, `mag/grok_weave.py`, `mag/republic_feed.py`, `mag/republic_loop.py`, `mag/self_loop.py`, `mag/swarm_self.py` + 1 more

### mag/lens_library.py

- lines: 533 | parse: ok | last commit: de7bb85fe 2026-08-09 | mtime: 2026-08-08 20:37
- public functions (6): `apply_lens`, `apply_all_lenses`, `lens_the_chain`, `lens_the_bard`, `lens_the_research`, `lens_library_summary`
- public classes (3): `Lens`, `LensReading`, `CrossLensSynthesis`
- test files (0): none
- readers (8): `mag/autonomous_research.py`, `mag/behavioral_lensing.py`, `mag/lens_tournament.py`, `mag/novelty_lens.py`, `mag/popup_insights.py`, `mag/research_lens.py`, `mag/shadow_work.py`, `mag/tool_synthesis.py`

### mag/lens_shader.py

- lines: 198 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 09:58
- public functions (7): `shade`, `render`, `seams`, `inject`, `uniforms_from_state`, `program`, `status`
- public classes (2): `LensSeed`, `LensUniforms`
- test files (0): none
- readers (3): `mag/republic_loop.py`, `mag/socratic_research.py`, `mag/tool_synthesis.py`

### mag/lens_tournament.py

- lines: 263 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 14:55
- public functions (5): `available_lenses`, `plant_round`, `score_response`, `tournament`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/novelty_lens.py`, `mag/skill_pipeline.py`

### mag/librarian.py

- lines: 258 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-10 16:40
- public functions (6): `md_files`, `map_rows`, `receipt_state`, `extraction_aliases`, `row_state`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/cascade_research.py`

### mag/librarian_catalog.py

- lines: 205 | parse: ok | last commit: a5dd96176 2026-09-25 | mtime: 2026-09-23 14:16
- public functions (5): `shelf_row`, `bulk_row`, `verify_canon`, `run_once`, `status`
- public classes (0): none
- test files (0): none
- readers (4): `seed/engines/build_seed.py`, `seed/engines/librarian_catalog.py`, `tools/build_seed.py`, `tools/seed_v2.py`

### mag/lifecycle.py

- lines: 916 | parse: ok | last commit: 6d417abd5 2026-09-26 | mtime: 2026-09-26 17:24
- public functions (9): `improve_intentional_flag_path`, `mark_improve_intentional`, `improve_intentional`, `clear_improve_intentional`, `improve_off`, `improve_on`, `build_lifecycle`, `reconcile`, `auto_reconcile`
- public classes (0): none
- test files (4): `tests/test_doctor_scheduled_tasks.py`, `tests/test_improve_off_on.py`, `tests/test_lifecycle.py`, `tests/test_temperature_stack.py`
- readers (9): `dashboard/rest.py`, `mag/compute_reconcile.py`, `mag/doctor.py`, `mag/icon_drop.py`, `mag/power.py`, `mag/temperature_stack.py`, `mag/win_powershell.py`, `mag_launch.py` + 1 more

### mag/line_builder.py

- lines: 140 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 07:51
- public functions (5): `split_ranges`, `plan`, `build`, `verify_conflict_free`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/memweave.py`, `mag/swarm_render.py`

### mag/link_library.py

- lines: 396 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 15:50
- public functions (13): `canonicalize`, `canonical_sha256`, `load_ledger`, `known_canonicals`, `check_url`, `load_events`, `load_image_drops`, `verify_image_drops`, `classify_host_mismatch`, `convention_report`, `validate_host_safety`, `add_urls`, `main`
- public classes (0): none
- test files (2): `tests/test_link_library.py`, `tests/test_paste_pipeline_footer.py`
- readers (6): `artifacts/backfill_links_20260916.py`, `artifacts/rashomon_dedupe_20260916.py`, `mag/links_sha_ratchet.py`, `mag/links_split_gate.py`, `mag/paste_pipeline.py`, `main.py`

### mag/links_sha_ratchet.py

- lines: 152 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 19:00
- public functions (2): `scan_same_sha_unflagged`, `links_sha_ratchet_check`
- public classes (0): none
- test files (1): `tests/test_links_sha_ratchet.py`
- readers (1): `mag/shared_surface.py`

### mag/links_split_gate.py

- lines: 143 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 15:59
- public functions (3): `links_split_check`, `links_split_marker_line`, `scan_links_kind_rows`
- public classes (0): none
- test files (0): none
- readers (2): `mag/links_sha_ratchet.py`, `mag/shared_surface.py`

### mag/lite_guard.py

- lines: 265 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-05 00:35
- public functions (6): `spent_today`, `provider_quota`, `usage_detail`, `check`, `record`, `status`
- public classes (0): none
- test files (0): none
- readers (30): `mag/cooker.py`, `mag/free_tier.py`, `mag/fuel_feed.py`, `mag/gopher_lite.py`, `mag/lane_runner.py`, `mag/lane_supervisor.py`, `mag/research_fanout.py`, `mag/rib_cache.py` + 22 more

### mag/lite_scale.py

- lines: 166 | parse: ok | last commit: 0f34a8f3e 2026-09-16 | mtime: 2026-09-16 14:44
- public functions (2): `call`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/live_feed.py

- lines: 194 | parse: ok | last commit: 60e18c524 2026-08-08 | mtime: 2026-08-08 08:11
- public functions (2): `watch`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `dashboard/rest.py`, `mag/framework_map.py`, `main.py`

### mag/live_ops_readiness.py

- lines: 151 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-02 04:10
- public functions (3): `snapshot`, `write_snapshot`, `main`
- public classes (0): none
- test files (1): `tests/test_live_ops_readiness.py`
- readers (5): `configs/modules.yaml`, `mag/live_report.py`, `mag/organ_map.py`, `main.py`, `state/backups/orphan_close_20260906/organ_map.py`

### mag/live_report.py

- lines: 150 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-02 04:10
- public functions (2): `render`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/governor_autorun.py`, `mag/organ_map.py`, `state/backups/orphan_close_20260906/organ_map.py`

### mag/liveness_sense.py

- lines: 256 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 14:44
- public functions (3): `classify`, `moonshot_tesuji`, `status`
- public classes (0): none
- test files (0): none
- readers (2): `mag/gap_routed_handoff.py`, `mag/ghost.py`

### mag/lm_studio.py

- lines: 122 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-01 16:01
- public functions (4): `models`, `chat`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_lm_studio.py`
- readers (2): `docker-compose.yml`, `mag/main_channel.py`

### mag/local_mode.py

- lines: 43 | parse: ok | last commit: 36914e134 2026-08-07 | mtime: 2026-08-07 06:27
- public functions (3): `is_local_only`, `set_local_only`, `clear_local_only`
- public classes (0): none
- test files (0): none
- readers (3): `dashboard/rest.py`, `mag/gpipes.py`, `mag/orchestrator.py`

### mag/local_playbook.py

- lines: 322 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (8): `list_playbooks`, `get_playbook`, `default_for_surface`, `build_local_prompt`, `validate_output`, `save_teacher_playbook`, `frontier_author_playbook`, `augment_arena_prompt`
- public classes (0): none
- test files (0): none
- readers (5): `configs/coding_session_loop.yaml`, `dashboard/rest.py`, `mag/agent_arena.py`, `mag/desk_dialogue.py`, `mag/desk_teaching.py`

### mag/local_pulse.py

- lines: 210 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (2): `set_local_thinking`, `build_local_pulse`
- public classes (0): none
- test files (1): `tests/test_local_pulse.py`
- readers (4): `dashboard/rest.py`, `mag/desk_dialogue.py`, `mag/display.py`, `mag/stack.py`

### mag/local_scheduler.py

- lines: 458 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-02 04:10
- public functions (6): `enqueue`, `steer`, `deepseek_triage`, `run_exclusive`, `status`, `build_stack_row`
- public classes (0): none
- test files (1): `tests/test_local_scheduler.py`
- readers (8): `dashboard/rest.py`, `mag/gpu_ghost.py`, `mag/organ_map.py`, `mag/stack.py`, `mag/stateless_research.py`, `mag/tool_synthesis.py`, `main.py`, `state/backups/orphan_close_20260906/organ_map.py`

### mag/local_usable.py

- lines: 514 | parse: ok | last commit: e96fd62a4 2026-08-07 | mtime: 2026-08-06 22:30
- public functions (9): `pack_dir`, `default_retrieval_policy`, `build_local_prompt`, `validate_pack`, `write_pack`, `load_pack`, `load_local_slice`, `obligation_ok`, `export_game_module_to_pack`
- public classes (0): none
- test files (0): none
- readers (1): `mag/checkin_route.py`

### mag/loop_audit.py

- lines: 334 | parse: ok | last commit: f5a055a7e 2026-08-05 | mtime: 2026-08-06 18:28
- public functions (7): `verkle_gap_goal`, `plan_fingerprint`, `analyze_autorun_trail`, `analyze_queue`, `recommendations`, `run_audit`, `format_report`
- public classes (0): none
- test files (1): `tests/test_loop_audit.py`
- readers (7): `mag/governor_autorun.py`, `mag/orchestrator.py`, `mag/self_audit.py`, `mag/spider.py`, `mag/steer_telemetry.py`, `mag/steward.py`, `main.py`

### mag/loop_breaker.py

- lines: 258 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 12:54
- public functions (3): `detect`, `break_loop`, `main`
- public classes (0): none
- test files (2): `tests/test_b285_enum_resolution_pins.py`, `tests/test_loop_breaker.py`
- readers (3): `mag/ghost.py`, `mag/ghost_control.py`, `mag/skill_pipeline.py`

### mag/loop_doctor.py

- lines: 129 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 11:43
- public functions (3): `sense`, `patch_list`, `status`
- public classes (0): none
- test files (0): none
- readers (5): `mag/end_state.py`, `mag/ghost.py`, `mag/loop_health.py`, `mag/republic_loop.py`, `mag/resource_governor.py`

### mag/loop_feedback.py

- lines: 107 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 12:47
- public functions (2): `read_back`, `status`
- public classes (0): none
- test files (0): none
- readers (4): `mag/harvest_fold.py`, `mag/republic_feed.py`, `mag/republic_loop.py`, `mag/truth_audit.py`

### mag/loop_health.py

- lines: 224 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-24 07:26
- public functions (2): `status`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `dashboard/rest.py`

### mag/loops_registry.py

- lines: 234 | parse: ok | last commit: 60e18c524 2026-08-08 | mtime: 2026-08-08 10:09
- public functions (2): `build_registry`, `format_registry_text`
- public classes (0): none
- test files (1): `tests/test_v3_modules.py`
- readers (2): `mag/framework_map.py`, `main.py`

### mag/lora_pipeline.py

- lines: 549 | parse: ok | last commit: de7bb85fe 2026-08-09 | mtime: 2026-08-08 22:52
- public functions (5): `detect_hardware`, `format_training_data`, `generate_training_config`, `generate_training_script`, `pipeline_status`
- public classes (1): `HardwareProfile`
- test files (0): none
- readers (4): `mag/ghost.py`, `mag/preflight.py`, `mag/sovereign_dashboard.py`, `mag/vast_launcher.py`

### mag/machine_target.py

- lines: 75 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 08:06
- public functions (4): `target`, `lowers_to`, `default_target`, `main`
- public classes (0): none
- test files (0): none
- readers (7): `mag/compiler_lang.py`, `mag/gpu_memweave.py`, `mag/host_roundtrip.py`, `mag/invariant_ledger.py`, `mag/novelty_lens.py`, `mag/research_class.py`, `mag/rib_bus.py`

### mag/main_channel.py

- lines: 457 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-01 18:05
- public functions (9): `ensure_window`, `classify_deterministic`, `classify`, `build_warm_pack`, `run`, `spawn_child`, `status`, `self_test`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/organ_map.py`, `state/backups/orphan_close_20260906/organ_map.py`

### mag/manifest.py

- lines: 191 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-24 10:17
- public functions (5): `manifest`, `anchor`, `verify`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (4): `mag/chord_circuit.py`, `mag/organ_map.py`, `mag/water_computer.py`, `state/backups/orphan_close_20260906/organ_map.py`

### mag/matrix_router.py

- lines: 174 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 20:39
- public functions (4): `register_lane`, `mount_bus`, `route`, `status`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/max_distill.py

- lines: 255 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-26 14:04
- public functions (3): `validate_skill`, `evaluate_near_misses`, `compute_rar`
- public classes (0): none
- test files (1): `tests/test_lab_episode.py`
- readers (2): `mag/lab_episode.py`, `mag/max_distill_arms.py`

### mag/max_distill_arms.py

- lines: 310 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-27 04:08
- public functions (5): `build_prompt`, `score`, `run_arm`, `report`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/maze_real.py

- lines: 151 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-13 11:20
- public functions (3): `sha`, `build`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/mcp_http.py

- lines: 44 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-04 20:10
- public functions (0): none
- public classes (0): none
- test files (0): none
- readers (2): `mag/api_server.py`, `mag/desk_tools.py`

### mag/mcp_server.py

- lines: 410 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 16:47
- public functions (8): `tools_manifest`, `quantized_manifest`, `quantized_cartridges`, `write_quantized_cartridges`, `call_tool`, `handle`, `serve`, `main`
- public classes (0): none
- test files (2): `tests/test_mcp_quantized.py`, `tests/test_sense_mcp.py`
- readers (8): `dashboard/server.py`, `docker-compose.yml`, `mag/_probe_mcp.py`, `mag/mcp_http.py`, `scripts/build_knowledge_graph.py`, `scripts/container/mcp_tcp_bridge.py`, `tools/mcp_pin.py`, `tools/seed_mcp.py`

### mag/mem_invariant_map.py

- lines: 232 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 12:47
- public functions (5): `available`, `pick_model`, `point_invariants`, `map_`, `status`
- public classes (0): none
- test files (0): none
- readers (1): `mag/rib_os.py`

### mag/mem_lands.py

- lines: 217 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 05:54
- public functions (5): `read`, `lattice`, `flow`, `self_check`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/gab_seat.py`

### mag/mem_ollama.py

- lines: 258 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 19:32
- public functions (7): `models`, `render_mem`, `render_token`, `roundtrip`, `record_row`, `review`, `status`
- public classes (0): none
- test files (0): none
- readers (2): `mag/mem_invariant_map.py`, `mag/tool_synthesis.py`

### mag/mem_weave_distributor.py

- lines: 178 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 01:22
- public functions (6): `scan_source`, `scan`, `distribute_source`, `rightsize`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/work_register.py`

### mag/memlang.py

- lines: 442 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 16:26
- public functions (9): `contracts`, `compile_token`, `decode`, `resolve`, `trigger`, `roundtrip`, `vocab`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_memlang.py`
- readers (26): `mag/_demo_telepathy.py`, `mag/attractor_tools.py`, `mag/bernaise.py`, `mag/compiler_lang.py`, `mag/doctor.py`, `mag/ecosystem_surface.py`, `mag/error_healer.py`, `mag/flex_test.py` + 18 more

### mag/memory_consolidate.py

- lines: 217 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-18 11:46
- public functions (4): `consolidate`, `run_sleep_step`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/memory_events.py

- lines: 159 | parse: ok | last commit: 36914e134 2026-08-07 | mtime: 2026-08-07 12:32
- public functions (5): `emit_event`, `emit_checkpoint_summary`, `emit_route_decision`, `emit_steer_lifecycle`, `recent_events`
- public classes (0): none
- test files (2): `tests/test_memory_events.py`, `tests/test_overseer_steering_api.py`
- readers (6): `dashboard/rest.py`, `mag/ai_landscape.py`, `mag/framework_map.py`, `mag/guardrail_sentinel.py`, `mag/pigeonhole.py`, `mag/route.py`

### mag/memory_map.py

- lines: 213 | parse: ok | last commit: 60e18c524 2026-08-08 | mtime: 2026-08-08 17:21
- public functions (8): `register`, `encode`, `decode`, `surface`, `anchor`, `assert_cage`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_memory_map.py`
- readers (0): none

### mag/memory_train_seed.py

- lines: 185 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-18 12:18
- public functions (3): `generate`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/memweave.py

- lines: 197 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 23:20
- public functions (4): `decompose`, `weave`, `consensus_quality`, `main`
- public classes (0): none
- test files (0): none
- readers (4): `mag/agent_os_loop.py`, `mag/claims_verify.py`, `mag/novelty_lens.py`, `mag/research_class.py`

### mag/meta_lattice.py

- lines: 124 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 06:15
- public functions (3): `squeeze_test`, `meta_lattice`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/republic_loop.py`

### mag/meta_percolate.py

- lines: 233 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-13 07:09
- public functions (6): `percolate_to_one`, `main`, `feed_back`, `run_cadence`, `genetic_pass`, `genetic_cadence`
- public classes (0): none
- test files (0): none
- readers (3): `mag/gene_pool_feeder.py`, `mag/governor_autorun.py`, `mag/tool_lifecycle.py`

### mag/mind_mine.py

- lines: 417 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 13:01
- public functions (3): `mine_session`, `mine_sessions`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/mind_window.py

- lines: 474 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 13:01
- public functions (7): `redact`, `ingest_transcript`, `process_transcript`, `transcript_text`, `summarize_session`, `build_digest`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/mind_mine.py`

### mag/mindweave_eval.py

- lines: 269 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 11:05
- public functions (5): `quality_of_consensus`, `rib_poisoning_test`, `pod_failure_test`, `run_all`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/mine_diamonds.py

- lines: 247 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-09 22:34
- public functions (3): `diamonds`, `digest`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/governor_autorun.py`, `memory/trash/20260810T202850Z/_tmp_stateless_swarm_research.py`

### mag/mirror_control.py

- lines: 123 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-08 14:13
- public functions (2): `run`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/mixture_of_agents.py

- lines: 422 | parse: ok | last commit: de7bb85fe 2026-08-09 | mtime: 2026-08-08 22:51
- public functions (4): `get_engine`, `moa_query`, `moa_compare`, `moa_dashboard`
- public classes (3): `AgentVote`, `MoAResult`, `MoAEngine`
- test files (0): none
- readers (3): `mag/ghost.py`, `mag/preflight.py`, `mag/sovereign_dashboard.py`

### mag/model_health.py

- lines: 150 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-09 22:57
- public functions (3): `health`, `digest`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/resume_order.py`, `mag/stateless_research.py`

### mag/model_pick.py

- lines: 87 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 08:07
- public functions (2): `recommend_model`, `main`
- public classes (0): none
- test files (0): none
- readers (6): `mag/agent_state_router.py`, `mag/frontier_council.py`, `mag/research_class.py`, `mag/right_size_skills.py`, `mag/self_drive.py`, `mag/usage_forecast.py`

### mag/modules.py

- lines: 272 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (6): `load_modules_config`, `check_module`, `check_runtime_compose`, `compose_status`, `format_compose_status`, `attach_related_runs_to_residual`
- public classes (0): none
- test files (0): none
- readers (5): `dashboard/rest.py`, `mag/improve.py`, `mag/os_v2.py`, `mag/run_trail.py`, `main.py`

### mag/moonshot_engine.py

- lines: 227 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 15:48
- public functions (5): `plan`, `cold_launch`, `progress`, `moonshot`, `moonshot_self_steal`
- public classes (0): none
- test files (1): `tests/test_moonshot_engine.py`
- readers (2): `mag/republic_loop.py`, `mag/self_steal.py`

### mag/mrna_steal.py

- lines: 86 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-15 05:51
- public functions (2): `self_map`, `route`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/mud_steal.py

- lines: 159 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 16:58
- public functions (5): `route_research`, `self_map`, `learn`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_mud_steal.py`
- readers (2): `mag/salon_50.py`, `mag/wow_steal.py`

### mag/museum.py

- lines: 207 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-24 16:40
- public functions (4): `retire`, `visit`, `rooms`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/mycelium.py

- lines: 354 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-15 20:15
- public functions (13): `add_node`, `get_node`, `link`, `salience`, `reinforce`, `contradict`, `neighborhood`, `dual_write`, `boot`, `decay`, `adopt_from_idea_graph`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_republic_os.py`
- readers (27): `dashboard/rest.py`, `mag/cleanup_steal.py`, `mag/comms_trail.py`, `mag/doctor.py`, `mag/ghost.py`, `mag/governor_autorun.py`, `mag/memlang.py`, `mag/republic_os.py` + 19 more

### mag/narrative_engine.py

- lines: 845 | parse: ok | last commit: de7bb85fe 2026-08-09 | mtime: 2026-08-08 23:53
- public functions (4): `get_engine`, `generate_campaign`, `generate_character`, `seed_scout_findings`
- public classes (2): `DeepCharacter`, `NarrativeEngine`
- test files (0): none
- readers (2): `mag/campaign_simulator.py`, `mag/game_campaign.py`

### mag/narrative_tests.py

- lines: 388 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-10 16:54
- public functions (9): `weights_path`, `load_weights`, `test_tears`, `test_archetype`, `test_phrase_clone`, `test_speed_volume`, `test_punishment`, `run_tests`, `demo`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/nervous_system.py

- lines: 522 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 15:28
- public functions (6): `write_face`, `glance_cached`, `build_glance`, `format_glance_text`, `pack_excerpt`, `build_nervous_system_glance`
- public classes (0): none
- test files (4): `tests/test_display.py`, `tests/test_nervous_system.py`, `tests/test_routing_concert.py`, `tests/test_stack.py`
- readers (11): `configs/modules.yaml`, `dashboard/rest.py`, `mag/brain.py`, `mag/context_pack.py`, `mag/dashboard_plugin.py`, `mag/display.py`, `mag/improve_loop.py`, `mag/routing_concert.py` + 3 more

### mag/no_win.py

- lines: 120 | parse: ok | last commit: 750259531 2026-09-27 | mtime: 2026-09-27 19:13
- public functions (4): `frame`, `reframe`, `play`, `main`
- public classes (0): none
- test files (1): `tests/test_no_win.py`
- readers (0): none

### mag/north_star.py

- lines: 143 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 05:32
- public functions (3): `cycle`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/notion_api.py

- lines: 178 | parse: ok | last commit: 5dc2971df 2026-08-25 | mtime: 2026-08-25 20:04
- public functions (6): `token_status`, `paragraph`, `heading`, `create_page`, `search`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/offerings.py`

### mag/novelty_lens.py

- lines: 170 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 09:27
- public functions (4): `novelty`, `keyword_lens`, `lens_map`, `status`
- public classes (0): none
- test files (0): none
- readers (4): `mag/invariant_ledger.py`, `mag/shadow_graph.py`, `mag/steal_pack.py`, `mag/tool_synthesis.py`

### mag/ocean_model_mind.py

- lines: 309 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-22 10:12
- public functions (6): `fingerprint`, `model`, `decide`, `minds`, `frontier`, `status`
- public classes (0): none
- test files (0): none
- readers (1): `mag/aos_bus_watcher.py`

### mag/ocean_persona.py

- lines: 169 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 11:43
- public functions (5): `invariants`, `lens_ocean`, `personalities`, `frontier`, `status`
- public classes (0): none
- test files (0): none
- readers (1): `mag/ocean_model_mind.py`

### mag/off_hours.py

- lines: 337 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 20:59
- public functions (9): `schedule_status`, `overnight_lane`, `classify`, `decorate`, `eligibility`, `dispatch_spec`, `mark_deferred`, `mark_eligible`, `queue_status`
- public classes (0): none
- test files (1): `tests/test_off_hours.py`
- readers (3): `dashboard/rest.py`, `mag/cost_truth.py`, `mag/orchestrator.py`

### mag/offerings.py

- lines: 233 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 12:53
- public functions (2): `status`, `route`
- public classes (0): none
- test files (0): none
- readers (2): `mag/ladder.py`, `mag/seat_dispatch.py`

### mag/offline.py

- lines: 231 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-09 23:46
- public functions (5): `self_check`, `offline_mode`, `fallback_llm`, `capability_test`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/offpeak.py

- lines: 160 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-24 09:19
- public functions (5): `is_peak`, `multiplier`, `pricing`, `defer_if_peak`, `main`
- public classes (0): none
- test files (1): `tests/test_loop_death_guards.py`
- readers (21): `configs/providers.yaml`, `mag/cheap_swarm.py`, `mag/lane_salon.py`, `mag/verified_clock.py`, `memory/seals/2026-08-24T16-22-15/configs/providers.yaml`, `memory/seals/2026-08-24T16-23-53/configs/providers.yaml`, `memory/seals/2026-08-24T16-31-53/configs/providers.yaml`, `memory/seals/2026-08-24T17-06-44/configs/providers.yaml` + 13 more

### mag/oh_fuck.py

- lines: 114 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 13:22
- public functions (2): `oh_fuck`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/skill_pipeline.py`

### mag/ollama_policy.py

- lines: 120 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (4): `list_loaded`, `enforce_one_hot`, `ensure_desk_model`, `status`
- public classes (0): none
- test files (1): `tests/test_local_gpu_probes.py`
- readers (7): `mag/desk_dialogue.py`, `mag/desk_model_probe.py`, `mag/local_scheduler.py`, `mag/surface_render.py`, `mag/tool_synthesis.py`, `mag/vram_memory.py`, `main.py`

### mag/one_sizer.py

- lines: 128 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-09 21:39
- public functions (4): `record_sizing`, `resolve_sizing`, `stats`, `main`
- public classes (0): none
- test files (0): none
- readers (8): `mag/agent_behavior.py`, `mag/flock_scheduler.py`, `mag/ghost_auto.py`, `mag/ghost_whisper.py`, `mag/memlang.py`, `mag/skill_pipeline.py`, `memory/trash/20260810T202850Z/_tmp_stateless_swarm_research.py`, `memory/trash/20260810T202850Z/_tmp_steal_elevate.py`

### mag/ontology_compiler/extract.py

- lines: 48 | parse: ok | last commit: 7a3e22b30 2026-09-08 | mtime: 2026-09-08 09:41
- public functions (4): `classify`, `cluster`, `propose`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/openclaw_catalog.py

- lines: 252 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-29 15:55
- public functions (4): `scan_clis`, `compile_fabric`, `compile_catalog`, `main`
- public classes (0): none
- test files (1): `tests/test_openclaw_catalog.py`
- readers (0): none

### mag/openclaw_patches.py

- lines: 251 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-31 07:29
- public functions (5): `apply_one`, `preflight`, `apply_inbox`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_openclaw_patches.py`
- readers (1): `mag/openclaw_catalog.py`

### mag/operating_protocol.py

- lines: 113 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (2): `normalize_surface`, `build_envelope`
- public classes (0): none
- test files (3): `tests/test_operating_protocol.py`, `tests/test_remote_control.py`, `tests/test_roadmap_runner.py`
- readers (5): `dashboard/rest.py`, `mag/framework_map.py`, `mag/remote_control.py`, `mag/roadmap_runner.py`, `main.py`

### mag/operator_inbox.py

- lines: 460 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 08:41
- public functions (8): `status`, `pending_hints`, `commit_guidance`, `clear_pending`, `capture_mention`, `drain_pending_at_checkpoint`, `log_behavioral_event`, `apply_actions_to_messages`
- public classes (0): none
- test files (11): `tests/test_decision_framework.py`, `tests/test_improve_loop.py`, `tests/test_operator_inbox.py`, `tests/test_pro_library.py`, `tests/test_pro_library_eval.py`, `tests/test_pupeteering.py`, `tests/test_repack_integration.py`, `tests/test_resume_contract.py` + 3 more
- readers (34): `_verify_review_tier_20260925.py`, `dashboard/rest.py`, `mag/agent_cli.py`, `mag/attention_ranker.py`, `mag/bernaise.py`, `mag/brain.py`, `mag/campaign.py`, `mag/clippy.py` + 26 more

### mag/operator_mode.py

- lines: 182 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-02 04:15
- public functions (5): `read`, `set_paused`, `resume`, `pause_reason`, `is_paused`
- public classes (0): none
- test files (2): `tests/test_loop_death_guards.py`, `tests/test_operator_mode.py`
- readers (13): `configs/modules.yaml`, `mag/afk_cadence.py`, `mag/afk_loop.py`, `mag/afk_orchestrator.py`, `mag/agent_cli.py`, `mag/autorun_common.py`, `mag/live_ops_readiness.py`, `mag/live_report.py` + 5 more

### mag/operator_os.py

- lines: 294 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-14 20:30
- public functions (2): `build_operator_os`, `format_org_review_text`
- public classes (0): none
- test files (0): none
- readers (3): `dashboard/rest.py`, `mag/verkle_audit.py`, `main.py`

### mag/ops_graph.py

- lines: 445 | parse: ok | last commit: 60e18c524 2026-08-08 | mtime: 2026-08-08 10:54
- public functions (5): `collect`, `categorize`, `persist`, `render`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `dashboard/rest.py`, `main.py`

### mag/oracle.py

- lines: 188 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-13 09:03
- public functions (6): `fetch_sources`, `verify`, `anchor`, `oracle`, `query`, `status`
- public classes (0): none
- test files (1): `tests/test_oracle.py`
- readers (0): none

### mag/orchestrator.py

- lines: 2056 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 17:14
- public functions (26): `dim`, `timeout_for_goal`, `register_external`, `touch_external`, `finalize_external`, `list_external_tasks`, `spawn_task`, `queue_has_goal`, `enqueue`, `purge_failed_queue`, `list_queue`, `promote_queue`, `drain_parallel`, `drain_once`, `drain_loop`, `queue_status`, `list_tasks`, `list_tasks_live`, `task_status`, `kill_task`, `reap_stale`, `reap_completed`, `respawn_dead`, `tail_log`, `self_test`, `main`
- public classes (0): none
- test files (20): `tests/test_b285_enum_resolution_pins.py`, `tests/test_decision_framework.py`, `tests/test_factory_freeze_gate.py`, `tests/test_frontier_advisor.py`, `tests/test_governor_autorun.py`, `tests/test_orchestrator_queue.py`, `tests/test_orchestrator_reap_completed.py`, `tests/test_overseer_steering_api.py` + 12 more
- readers (101): `configs/modules.yaml`, `dashboard/rest.py`, `dashboard/server.py`, `logs/_patch_pid.py`, `logs/_patch_rest.py`, `logs/_patch_sse.py`, `mag/attention_ranker.py`, `mag/autopilot.py` + 93 more

### mag/organ_map.py

- lines: 701 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-12 23:01
- public functions (4): `map_organs`, `operational_graph`, `snapshot`, `main`
- public classes (0): none
- test files (1): `tests/test_organ_map.py`
- readers (4): `mag/atlas.py`, `mag/dirac_loop.py`, `mag/elder.py`, `state/backups/orphan_close_20260906/organ_map.py`

### mag/orphan_audit.py

- lines: 214 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-31 07:35
- public functions (2): `build_report`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/orphan_sense.py

- lines: 203 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-15 09:54
- public functions (3): `novel_orphans`, `sense_test`, `status`
- public classes (0): none
- test files (0): none
- readers (5): `mag/cleanup_steal.py`, `mag/gap_frontier.py`, `mag/ghost.py`, `mag/republic_feed.py`, `mag/republic_loop.py`

### mag/orphan_timer.py

- lines: 267 | parse: ok | last commit: 60e18c524 2026-08-08 | mtime: 2026-08-08 10:24
- public functions (6): `note_intent`, `touch_intent`, `resolve_intent`, `list_open`, `run`, `main`
- public classes (0): none
- test files (0): none
- readers (7): `dashboard/rest.py`, `mag/flex_test.py`, `mag/governor_autorun.py`, `mag/ops_graph.py`, `mag/press_digest.py`, `mag/topic_orphan.py`, `main.py`

### mag/os_v2.py

- lines: 165 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-28 19:44
- public functions (2): `load_card_lines`, `live_status`
- public classes (0): none
- test files (0): none
- readers (1): `dashboard/rest.py`

### mag/osculating.py

- lines: 251 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-13 08:16
- public functions (5): `geometry`, `seams`, `moonshot`, `svg`, `status`
- public classes (0): none
- test files (1): `tests/test_osculating.py`
- readers (1): `mag/ghost_memlance.py`

### mag/overseer.py

- lines: 182 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-07 02:16
- public functions (2): `snap`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `configs/succession_contract.yaml`

### mag/ox_alpha_steal.py

- lines: 194 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-22 10:12
- public functions (3): `route_research`, `findings`, `status`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/ox_availability.py

- lines: 154 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 20:44
- public functions (3): `ping`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (4): `mag/seat_availability.py`, `memory/runs/_ask_ox_moonshot.py`, `memory/runs/_ask_ox_repro_fleet.py`, `tools/ox_heartbeat.py`

### mag/ox_burn.py

- lines: 121 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-22 20:08
- public functions (1): `run`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/ox_escalate.py

- lines: 138 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-22 12:33
- public functions (1): `route`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/ox_fold.py

- lines: 257 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 08:43
- public functions (4): `rewrite`, `fold`, `watch`, `status`
- public classes (0): none
- test files (0): none
- readers (2): `mag/free_to_swarm.py`, `mag/ox_resident.py`

### mag/ox_gap.py

- lines: 175 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-22 20:58
- public functions (3): `analyze`, `elevate`, `watch`
- public classes (0): none
- test files (0): none
- readers (1): `memory/runs/_elevate_stealth.py`

### mag/ox_megaburn.py

- lines: 560 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-22 20:58
- public functions (2): `run`, `summary`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/ox_megaburn2.py

- lines: 323 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 03:03
- public functions (2): `run`, `summary`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/ox_megaburn3.py

- lines: 247 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 14:26
- public functions (3): `generate`, `run`, `summary`
- public classes (0): none
- test files (0): none
- readers (4): `mag/ox_novelty_index.py`, `mag/ox_resident.py`, `mag/ox_scout.py`, `mag/work_loop.py`

### mag/ox_novelty_digest.py

- lines: 86 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 16:16
- public functions (1): `build`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/ox_novelty_index.py

- lines: 163 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 16:16
- public functions (1): `build`
- public classes (0): none
- test files (0): none
- readers (2): `mag/ox_resident.py`, `mag/ox_scout.py`

### mag/ox_percolate.py

- lines: 198 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-24 08:53
- public functions (4): `sync`, `distill`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/manifest.py`, `mag/work_loop.py`

### mag/ox_probe.py

- lines: 232 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 08:11
- public functions (3): `probe`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/ox_resident.py

- lines: 501 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-24 15:58
- public functions (9): `cold_asks`, `drilled_cores`, `banked`, `target_cells`, `run`, `distill`, `summary`, `watch`, `verify`
- public classes (0): none
- test files (0): none
- readers (9): `mag/manifest.py`, `mag/ox_swarm.py`, `mag/real_swarm.py`, `mag/standing.py`, `mag/work_loop.py`, `memory/runs/_ask_ox_moonshot.py`, `memory/runs/_ask_ox_repro_fleet.py`, `memory/runs/_ask_ox_utilize.py` + 1 more

### mag/ox_scout.py

- lines: 178 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 16:16
- public functions (4): `high_yield_cells`, `drill_asks`, `run`, `summary`
- public classes (0): none
- test files (0): none
- readers (1): `mag/ox_resident.py`

### mag/ox_seat.py

- lines: 182 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-24 13:59
- public functions (2): `chat`, `status`
- public classes (0): none
- test files (0): none
- readers (16): `mag/aos_agent.py`, `mag/fuel_feed.py`, `mag/ox_availability.py`, `mag/ox_burn.py`, `mag/ox_escalate.py`, `mag/ox_megaburn.py`, `mag/ox_megaburn2.py`, `mag/ox_megaburn3.py` + 8 more

### mag/ox_swarm.py

- lines: 298 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 18:08
- public functions (6): `fleet`, `pending_asks`, `preview`, `run`, `summary`, `watch`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/p20_pending_wave.py

- lines: 141 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-12 08:16
- public functions (3): `guarded_open`, `fire`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/partner_puppet.py

- lines: 116 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 20:39
- public functions (5): `puppet`, `from_anchor`, `surrogate`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `dashboard/rest.py`, `mag/verkle_lance.py`

### mag/party_subchain.py

- lines: 358 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-14 10:09
- public functions (7): `want_full`, `genesis`, `append`, `verify`, `mount`, `status`, `main`
- public classes (0): none
- test files (5): `tests/test_all_seat_interaction.py`, `tests/test_frontier_salon.py`, `tests/test_game_dm.py`, `tests/test_party_subchain.py`, `tests/test_seat_steer.py`
- readers (24): `_afk_full_blast.py`, `mag/bus_cadence.py`, `mag/context_checkpoint.py`, `mag/context_pack.py`, `mag/frontier_game.py`, `mag/frontier_salon.py`, `mag/game_campaign.py`, `mag/game_dm.py` + 16 more

### mag/paste_pipeline.py

- lines: 270 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 18:56
- public functions (2): `run`, `main`
- public classes (0): none
- test files (1): `tests/test_paste_pipeline_footer.py`
- readers (1): `tools/lattice_build.py`

### mag/pattern_mine.py

- lines: 152 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 00:35
- public functions (2): `surface`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/pdf_layout.py

- lines: 537 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (1): `render_clean_pdf`
- public classes (0): none
- test files (0): none
- readers (1): `mag/session_dossier.py`

### mag/peer_handoff.py

- lines: 259 | parse: ok | last commit: a5dd96176 2026-09-25 | mtime: 2026-09-21 21:53
- public functions (5): `file_peer_handoff`, `list_peer_handoffs`, `latest_for_track`, `format_latest_brief`, `main`
- public classes (0): none
- test files (1): `tests/test_remote_control.py`
- readers (12): `configs/modules.yaml`, `mag/context_pack.py`, `mag/drainer_stats.py`, `mag/feature_lab.py`, `mag/framework_map.py`, `mag/remote_control.py`, `mag/session_overseer.py`, `mag/session_state_brief.py` + 4 more

### mag/percolator.py

- lines: 384 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-09 14:49
- public functions (9): `partition`, `append_noise`, `noise_log`, `intake_register`, `open_intake`, `false_positive`, `percolate`, `percolate_signal`, `status`
- public classes (0): none
- test files (2): `mag/tests/test_identity_schema_portability.py`, `mag/tests/verify_identity_coupling.py`
- readers (30): `mag/agent_knot.py`, `mag/chord_pipeline.py`, `mag/compiler_lang.py`, `mag/destructive_receipt.py`, `mag/emergence.py`, `mag/evolving_wave.py`, `mag/fuel_feed.py`, `mag/game_campaign.py` + 22 more

### mag/percolator_heal_test.py

- lines: 156 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-07 01:08
- public functions (4): `check`, `make_world`, `seal_gens6`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/perplexity_research.py

- lines: 323 | parse: ok | last commit: a5dd96176 2026-09-25 | mtime: 2026-09-25 20:33
- public functions (6): `key`, `resolve_route`, `status`, `endpoint_blocked`, `research`, `main`
- public classes (0): none
- test files (1): `tests/test_perplexity_research.py`
- readers (0): none

### mag/persistent_agent.py

- lines: 444 | parse: ok | last commit: 60e18c524 2026-08-08 | mtime: 2026-08-08 14:57
- public functions (4): `create_dnd_party`, `create_research_swarm`, `agent_conversation_loop`, `list_persistent_agents`
- public classes (2): `AgentTurn`, `PersistentAgent`
- test files (0): none
- readers (0): none

### mag/persona_direction.py

- lines: 183 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 09:58
- public functions (3): `self_steal_map`, `measure`, `status`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/persona_key.py

- lines: 207 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-24 13:18
- public functions (6): `challenge`, `answer`, `record`, `baseline`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/persona_recall.py

- lines: 155 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 11:28
- public functions (4): `persona`, `what_happened`, `recall`, `status`
- public classes (0): none
- test files (0): none
- readers (4): `mag/game_entry.py`, `mag/ocean_persona.py`, `mag/republic_feed.py`, `scripts/build_vislab_catalog.py`

### mag/personality_substrate.py

- lines: 228 | parse: ok | last commit: 60e18c524 2026-08-08 | mtime: 2026-08-08 15:59
- public functions (2): `distill_training_data`, `get_substrate_summary`
- public classes (1): `PhilosopherPrinciple`
- test files (0): none
- readers (1): `mag/persona_recall.py`

### mag/perturbation_battery.py

- lines: 550 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-06 02:04
- public functions (7): `p1_ledger`, `p2_voxels`, `p3_maze`, `p4_premise_poison`, `p5_cross_domain`, `run_battery`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/phone_door.py

- lines: 76 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-07 02:13
- public functions (3): `ensure`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/overseer.py`

### mag/phone_relay.py

- lines: 249 | parse: ok | last commit: 662c25a9b 2026-09-25 | mtime: 2026-09-25 06:38
- public functions (2): `ask`, `test`
- public classes (0): none
- test files (0): none
- readers (5): `mag/lane_supervisor.py`, `seed/engines/build_seed.py`, `seed/engines/phone_relay.py`, `tools/build_seed.py`, `tools/seed_v2.py`

### mag/physics_steal.py

- lines: 157 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 16:58
- public functions (5): `route_research`, `self_map`, `learn`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_physics_steal.py`
- readers (0): none

### mag/pigeonhole.py

- lines: 336 | parse: ok | last commit: 36914e134 2026-08-07 | mtime: 2026-08-07 12:32
- public functions (14): `mailbox_dir`, `post_cmd`, `post_steer`, `ack_steer`, `steer_status`, `steering_log`, `drain_inbox`, `heartbeat`, `write_status`, `read_status`, `heartbeats`, `staleness_s`, `alive`, `self_test`
- public classes (0): none
- test files (4): `tests/test_desk_dialogue.py`, `tests/test_memory_events.py`, `tests/test_orchestrator_reap_completed.py`, `tests/test_overseer_steering_api.py`
- readers (15): `dashboard/rest.py`, `mag/agent_cli.py`, `mag/desk_dialogue.py`, `mag/governance.py`, `mag/memory_events.py`, `mag/orchestrator.py`, `mag/research_worker.py`, `mag/run_worth.py` + 7 more

### mag/pin_audit.py

- lines: 109 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-05 13:35
- public functions (1): `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/plan.py

- lines: 203 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-05 07:36
- public functions (8): `should_plan`, `priority_hint`, `build_plan`, `save_plan`, `load_plan`, `list_plans`, `set_status`, `plan_gate`
- public classes (0): none
- test files (0): none
- readers (6): `mag/autonomous_research.py`, `mag/dispatch.py`, `mag/flock_scheduler.py`, `mag/fork_router.py`, `mag/tool_synthesis.py`, `main.py`

### mag/plan_mode.py

- lines: 40 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-25 09:32
- public functions (1): `plan_mode`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/platform_kill.py

- lines: 161 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 12:54
- public functions (2): `kill_all`, `main`
- public classes (0): none
- test files (1): `tests/test_b285_enum_resolution_pins.py`
- readers (4): `mag/ghost_control.py`, `mag/oh_fuck.py`, `mag/skill_pipeline.py`, `scripts/start_mag_container.cmd`

### mag/play_benchmark.py

- lines: 391 | parse: ok | last commit: e96fd62a4 2026-08-07 | mtime: 2026-08-06 22:34
- public functions (4): `run_b0`, `run_b1`, `run_b2`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/checkin_route.py`

### mag/poc_stage2.py

- lines: 141 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-24 11:57
- public functions (3): `run`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/policy.py

- lines: 84 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (2): `load_policy`, `resolve`
- public classes (0): none
- test files (0): none
- readers (6): `mag/act.py`, `mag/daemon.py`, `mag/ghost.py`, `mag/runtime.py`, `mag/sense.py`, `main.py`

### mag/policy_engine.py

- lines: 496 | parse: ok | last commit: 2b84b8cce 2026-09-16 | mtime: 2026-09-16 10:31
- public functions (17): `load_policy`, `save_policy`, `validate_effect`, `require_confirmation`, `check_ttl`, `ttl_expires`, `check_budget`, `revoke`, `is_revoked`, `validate_authority`, `check_ttl_valid`, `expire`, `cmd_show`, `cmd_set`, `cmd_validate`, `cmd_expire`, `main`
- public classes (0): none
- test files (1): `tests/test_switchboard.py`
- readers (6): `mag/effect_broker.py`, `mag/harness.py`, `mag/organ_map.py`, `mag/switchboard_v2.py`, `state/backups/orphan_close_20260906/organ_map.py`, `state/backups/orphan_close_20260906/test_switchboard.py`

### mag/ponytail_audit.py

- lines: 246 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 14:51
- public functions (2): `run_audit`, `format_report`
- public classes (0): none
- test files (2): `tests/test_ponytail_audit.py`, `tests/test_skill_seat.py`
- readers (3): `mag/skill_seat.py`, `main.py`, `scripts/ponytail_audit.py`

### mag/popup_insights.py

- lines: 158 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 05:53
- public functions (2): `cycle`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/tool_synthesis.py`

### mag/portal.py

- lines: 199 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 07:14
- public functions (5): `vmem_map`, `interpret`, `drop`, `panel`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/power.py

- lines: 735 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 12:54
- public functions (8): `is_off`, `set_off`, `clear_off`, `stop_all`, `start_all`, `stack_status`, `format_status_text`, `main`
- public classes (0): none
- test files (2): `tests/test_power.py`, `tests/test_stack.py`
- readers (8): `dashboard/rest.py`, `mag/brain.py`, `mag/desk_ops.py`, `mag/guard.py`, `mag/lifecycle.py`, `mag/stack.py`, `mag/unsloth_seat.py`, `main.py`

### mag/preferences.py

- lines: 141 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 08:05
- public functions (12): `load_prefs`, `save_prefs`, `drainer_enabled`, `operator_active`, `set_operator_active`, `operator_status`, `autorun_allowed`, `set_drainer`, `drainer_status`, `inject_behavioral_pack`, `set_inject_behavioral_pack`, `autonomy_status`
- public classes (0): none
- test files (3): `tests/test_autorun_v1.py`, `tests/test_loop_death_guards.py`, `tests/test_phase2_surface.py`
- readers (22): `dashboard/rest.py`, `mag/afk_cadence.py`, `mag/afk_loop.py`, `mag/afk_orchestrator.py`, `mag/autorun_common.py`, `mag/autorun_status.py`, `mag/capability_steal.py`, `mag/cleanup.py` + 14 more

### mag/prefix_prover.py

- lines: 192 | parse: ok | last commit: 6ac176ce8 2026-08-25 | mtime: 2026-08-25 17:55
- public functions (4): `known_states`, `cmd_freeze`, `cmd_audit`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/autodrain.py`, `mag/cache_watch.py`

### mag/preflight.py

- lines: 178 | parse: ok | last commit: de7bb85fe 2026-08-09 | mtime: 2026-08-08 23:07
- public functions (2): `run_preflight`, `preflight_dashboard`
- public classes (1): `PreFlightResult`
- test files (0): none
- readers (1): `mag/sovereign_dashboard.py`

### mag/preload_selector.py

- lines: 456 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-07 08:02
- public functions (15): `load_blocks`, `score_blocks`, `order_blocks`, `shuffle_blocks`, `ollama_health`, `pick_model`, `chat_logprobs`, `compose_prompt`, `run_arm`, `compare`, `cmd_order`, `cmd_shuffle`, `cmd_probe`, `cmd_selftest`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/worldline_seed.py`

### mag/press_digest.py

- lines: 224 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 13:19
- public functions (7): `gather`, `pick`, `rashomon`, `digest`, `emit`, `run_cadence`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/ghost.py`, `mag/ghost_control.py`, `mag/skill_pipeline.py`

### mag/primer.py

- lines: 179 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 10:20
- public functions (7): `map_world`, `play_rooms`, `compile_world`, `chronicle`, `holon`, `primer`, `cold_build`
- public classes (0): none
- test files (0): none
- readers (1): `mag/republic_loop.py`

### mag/pro_library.py

- lines: 392 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 07:51
- public functions (9): `add_move`, `sense`, `match`, `fire`, `learn`, `aim_once`, `stats`, `seed_default_moves`, `main`
- public classes (0): none
- test files (3): `tests/test_loop_death_guards.py`, `tests/test_pro_library.py`, `tests/test_pro_library_eval.py`
- readers (11): `mag/agent_cli.py`, `mag/ai_landscape.py`, `mag/bernaise.py`, `mag/capability_steal.py`, `mag/elevate.py`, `mag/ghost.py`, `mag/grok_mirror.py`, `mag/ox_resident.py` + 3 more

### mag/probe_route.py

- lines: 194 | parse: ok | last commit: 46711f479 2026-09-24 | mtime: 2026-09-24 22:28
- public functions (4): `probe_one`, `route`, `selftest`, `main`
- public classes (0): none
- test files (0): none
- readers (6): `configs/providers.yaml`, `mag/paste_pipeline.py`, `mag/wave_fire.py`, `memory/seals/2026-09-26T06-03-14/configs/providers.yaml`, `memory/seals/2026-09-26T09-03-57/configs/providers.yaml`, `tools/roblox_npc_gateway.py`

### mag/problem_knot.py

- lines: 239 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 18:21
- public functions (6): `declare_problem`, `problem_topology`, `dispatch_solver`, `fold_solution`, `solve`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/ghost_experimenter.py`, `mag/research_class.py`, `mag/resume_order.py`

### mag/process_reaper.py

- lines: 222 | parse: ok | last commit: 02bcd49be 2026-09-19 | mtime: 2026-09-19 09:14
- public functions (2): `classify`, `run`
- public classes (0): none
- test files (0): none
- readers (14): `mag/ghost.py`, `mag/gpu_ghost.py`, `mag/icon_drop.py`, `mag/legacy_audit.py`, `mag/loop_breaker.py`, `mag/offerings.py`, `mag/platform_kill.py`, `mag/power.py` + 6 more

### mag/process_supervisor.py

- lines: 499 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 09:53
- public functions (8): `start_loop`, `stop_loop`, `restart_loop`, `reap`, `status`, `start_all`, `stop_all`, `main`
- public classes (0): none
- test files (1): `tests/test_process_supervisor.py`
- readers (13): `configs/modules.yaml`, `dashboard/rest.py`, `mag/end_state.py`, `mag/guard_registry.py`, `mag/legacy_audit.py`, `mag/liveness_sense.py`, `mag/platform_kill.py`, `mag/process_reaper.py` + 5 more

### mag/prompt_archaeology.py

- lines: 498 | parse: ok | last commit: de7bb85fe 2026-08-09 | mtime: 2026-08-08 23:21
- public functions (4): `get_archaeologist`, `excavate`, `right_size`, `tag_tier`
- public classes (2): `PromptArtifact`, `PromptArchaeologist`
- test files (0): none
- readers (1): `mag/sovereign_dashboard.py`

### mag/prompt_lance.py

- lines: 566 | parse: ok | last commit: 0d9dda89e 2026-09-27 | mtime: 2026-09-27 18:25
- public functions (6): `diagnose`, `symbols`, `references`, `provenance`, `self_check`, `main`
- public classes (0): none
- test files (1): `tests/test_prompt_lance.py`
- readers (1): `tools/stealth_driver.py`

### mag/proof.py

- lines: 169 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-24 10:17
- public functions (6): `sign`, `verify`, `anchor`, `check`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (5): `mag/chord_circuit.py`, `mag/evolving_wave.py`, `mag/poc_stage2.py`, `mag/seal.py`, `mag/seeds.py`

### mag/prose_census.py

- lines: 155 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-28 14:32
- public functions (1): `run_census`
- public classes (0): none
- test files (0): none
- readers (1): `mag/lane_runner.py`

### mag/prospect_sim.py

- lines: 381 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 15:26
- public functions (10): `organize`, `prospect`, `simulate_session`, `echo`, `shared_mem_get`, `shared_mem_put`, `categorize`, `memory_search`, `memory_recent`, `main`
- public classes (0): none
- test files (0): none
- readers (4): `dashboard/rest.py`, `mag/learn_rightsize.py`, `mag/memlang.py`, `mag/skill_pipeline.py`

### mag/provenance_gate.py

- lines: 233 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-22 14:30
- public functions (0): none
- public classes (5): `EvidenceRecord`, `Citation`, `Verdict`, `Claim`, `ProvenanceGate`
- test files (0): none
- readers (0): none

### mag/quest_roshomon.py

- lines: 296 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-14 06:45
- public functions (7): `craft`, `party`, `play`, `compare`, `run`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_all_seat_interaction.py`
- readers (0): none

### mag/queue_analysis.py

- lines: 264 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-15 09:54
- public functions (7): `inspect`, `dedupe`, `rightsize`, `tokenomics`, `apply`, `analyze`, `status`
- public classes (0): none
- test files (0): none
- readers (1): `mag/_deep_research_verkle_dedupe.py`

### mag/queue_gate.py

- lines: 388 | parse: ok | last commit: 790145ab1 2026-09-26 | mtime: 2026-09-26 01:50
- public functions (7): `fingerprint`, `scan`, `dependencies`, `preflight`, `plan`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_loop_death_guards.py`
- readers (4): `mag/_verify_queue_gate.py`, `mag/_verify_sharp_edge.py`, `mag/lane_cadence.py`, `mag/swarm_worker.py`

### mag/queue_learn.py

- lines: 215 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 08:46
- public functions (4): `analyze`, `fold`, `run_cadence`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/governor_autorun.py`, `main.py`

### mag/queue_ops.py

- lines: 187 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 08:45
- public functions (6): `log_event`, `handle_error`, `digest`, `render_md`, `run_cadence`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/governor_autorun.py`, `mag/orchestrator.py`, `main.py`

### mag/queue_rightsize.py

- lines: 246 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-14 08:25
- public functions (4): `analyze`, `apply`, `learn`, `main`
- public classes (0): none
- test files (0): none
- readers (4): `mag/rightsize_all.py`, `mag/rightsize_api.py`, `mag/skill_pipeline.py`, `memory/working/_patch_code_team.py`

### mag/quorum_window.py

- lines: 484 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 19:10
- public functions (7): `t0`, `p1`, `p2`, `p3`, `p4`, `compare`, `main`
- public classes (0): none
- test files (2): `tests/test_dormant_gate_b2133.py`, `tests/test_quorum_p4_selfvote.py`
- readers (1): `mag/dormant.py`

### mag/race_harness.py

- lines: 182 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-03 21:19
- public functions (5): `report`, `test_race`, `test_grace`, `test_park_live`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/ractor_corpus.py

- lines: 474 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-06 18:24
- public functions (3): `gutendex`, `pick`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/ractor_vessels.py

- lines: 141 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-09 17:39
- public functions (3): `fire`, `land_on_board`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/fire_horse.py`

### mag/rails.py

- lines: 72 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (4): `load_rails`, `check_path`, `check_content`, `check_write_file`
- public classes (0): none
- test files (0): none
- readers (2): `mag/agent_cli.py`, `mag/framework_map.py`

### mag/ram_cache.py

- lines: 131 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-25 12:25
- public functions (5): `load_corpus`, `corpus`, `corpus_text`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/republic_loop.py`, `mag/vram_memory.py`

### mag/read_archive.py

- lines: 126 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 21:48
- public functions (3): `parse_span`, `deref`, `main`
- public classes (0): none
- test files (0): none
- readers (5): `configs/modules.yaml`, `mag/dogfood_audit.py`, `mag/organ_map.py`, `mag/trajectory_rib.py`, `state/backups/orphan_close_20260906/organ_map.py`

### mag/read_receipts.py

- lines: 125 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-05 20:23
- public functions (1): `sweep`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/readout_controller.py

- lines: 127 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 18:41
- public functions (5): `read`, `curate`, `inject`, `control_loop`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/real_swarm.py

- lines: 243 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 21:35
- public functions (5): `live_fleet`, `pending_asks`, `preview`, `run`, `summary`
- public classes (0): none
- test files (0): none
- readers (2): `mag/governor_autorun.py`, `mag/tandem_key_test.py`

### mag/reasoning_intake.py

- lines: 422 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-07 10:11
- public functions (3): `parse_export`, `seal`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/reconstruct.py

- lines: 168 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 16:28
- public functions (6): `state`, `wave`, `rederive`, `status`, `fold_doctrine`, `main`
- public classes (0): none
- test files (1): `tests/test_reconstruct.py`
- readers (1): `mag/republic_loop.py`

### mag/records.py

- lines: 261 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 13:55
- public functions (5): `list_known_session_ids`, `pack_report`, `write_kpi`, `backfill_sessions`, `format_pack_report_text`
- public classes (0): none
- test files (0): none
- readers (5): `dashboard/rest.py`, `mag/biography.py`, `mag/lanes.py`, `mag/operator_os.py`, `main.py`

### mag/recreation_rib.py

- lines: 220 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 19:32
- public functions (3): `build`, `render`, `status`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/recurrence_gate.py

- lines: 240 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 08:50
- public functions (3): `record`, `check`, `status`
- public classes (0): none
- test files (0): none
- readers (1): `mag/republic_loop.py`

### mag/refeed_guard.py

- lines: 171 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-05 19:15
- public functions (3): `redact`, `measure`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/refine_chain.py

- lines: 747 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 19:08
- public functions (9): `structure_checkin_plan`, `load_chain`, `latest_chain`, `start_chain`, `advance_chain`, `chain_status_speak`, `extract_preference_hypotheses`, `try_refine_voice`, `handle_refine`
- public classes (0): none
- test files (0): none
- readers (5): `dashboard/rest.py`, `mag/checkin_route.py`, `mag/framework_map.py`, `mag/voice_turn.py`, `memory/runs/job_floor/20260828-codex-lab/launch_panel.py`

### mag/refine_loop.py

- lines: 695 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 11:17
- public functions (7): `refine_sense`, `doctor_probe`, `escalate_to_grok`, `delegate_fix`, `fold_back`, `run_refine_loop`, `refine_loop_loop`
- public classes (1): `Escalation`
- test files (0): none
- readers (0): none

### mag/registry.py

- lines: 490 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 13:55
- public functions (20): `residual_path`, `legacy_dossier_path`, `derived_path`, `find_residual`, `find_derived`, `load_residual`, `residual_content_hash`, `attach_cold_core`, `set_latest_session`, `get_latest_session_id`, `write_residual`, `write_derived_md`, `write_derived_pdf_bytes`, `write_derived_visual`, `registry_row_from_dossier`, `upsert_registry`, `list_registry`, `lean_pack_status`, `publish_residual`, `migrate_all_to_lean`
- public classes (0): none
- test files (1): `tests/test_chat_source_agent_workday.py`
- readers (21): `configs/modules.yaml`, `dashboard/rest.py`, `dashboard/server.py`, `mag/agent_state.py`, `mag/biography.py`, `mag/bonds.py`, `mag/brief_local.py`, `mag/diary.py` + 13 more

### mag/rel_mem_eval.py

- lines: 248 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-26 00:07
- public functions (4): `default_retrieve`, `run_cluster`, `run_all`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `memory/improve/evals/verify_rel_mem_eval.py`, `tools/duty_fuzz.py`

### mag/release_registry.py

- lines: 297 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 16:18
- public functions (10): `load_registry`, `get_release`, `list_releases`, `notes_path`, `status_summary`, `build_subprocess_map`, `format_subprocess_text`, `read_gate_log`, `record_gate`, `format_notes_text`
- public classes (0): none
- test files (4): `tests/test_coding_session_loop.py`, `tests/test_release_registry.py`, `tests/test_release_subprocess_map.py`, `tests/test_roadmap_runner.py`
- readers (3): `mag/coding_session_loop.py`, `mag/roadmap_runner.py`, `main.py`

### mag/remedy.py

- lines: 145 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (5): `cards`, `lookup`, `card_md`, `by_tool`, `prevent`
- public classes (0): none
- test files (1): `tests/test_failure_kb.py`
- readers (4): `mag/agent_cli.py`, `mag/failure_kb.py`, `mag/framework_map.py`, `mag/governance.py`

### mag/remote_control.py

- lines: 137 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (5): `configured`, `authorized`, `token_from_headers`, `status`, `submit_intent`
- public classes (0): none
- test files (1): `tests/test_remote_control.py`
- readers (4): `mag/cast_guard.py`, `mag/cast_server.py`, `mag/novelty_lens.py`, `mag/research_class.py`

### mag/render_brief.py

- lines: 45 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-06 17:33
- public functions (1): `render_brief_into_page`
- public classes (0): none
- test files (0): none
- readers (1): `mag/fleet_intel.py`

### mag/renderman.py

- lines: 847 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-16 06:43
- public functions (3): `get_texture_cache`, `get_foam`, `cache_miss_experiment`
- public classes (10): `CacheLine`, `ConsentChain`, `TextureCache`, `GeometryCache`, `RenderBucket`, `BucketRenderer`, `StochasticSample`, `StochasticSampler`, `Bubble`, `Foam`
- test files (0): none
- readers (1): `mag/wireshark_steal.py`

### mag/renderman_ask.py

- lines: 208 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 09:12
- public functions (6): `compact_ask`, `render_rib`, `expand_ask`, `ask_grok_for_executor_spec`, `elevate_ask`, `main`
- public classes (0): none
- test files (0): none
- readers (4): `mag/ghost.py`, `mag/grok_mirror.py`, `mag/grok_terminal.py`, `main.py`

### mag/repo_readiness.py

- lines: 77 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (1): `repo_readiness`
- public classes (0): none
- test files (2): `tests/test_remote_control.py`, `tests/test_repo_readiness.py`
- readers (3): `dashboard/rest.py`, `mag/attention_ranker.py`, `mag/remote_control.py`

### mag/republic.py

- lines: 855 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-06 17:51
- public functions (16): `dump`, `parse`, `load`, `save`, `dag_snapshot`, `propose_statement`, `citizen`, `deliver`, `forward`, `supersede`, `seed_correspondence`, `show_letter`, `feed`, `post`, `demo`, `main`
- public classes (6): `AppendOnlyViolation`, `RoutingError`, `Claim`, `Citizen`, `Letter`, `Book`
- test files (0): none
- readers (1): `memory/research_packs/_t15_agm_check.py`

### mag/republic_ambassador.py

- lines: 218 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 16:40
- public functions (7): `find`, `identify`, `empower`, `plug_in`, `learn`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_republic_ambassador.py`
- readers (2): `mag/republic_loop.py`, `mag/sovereign_handshake.py`

### mag/republic_feed.py

- lines: 161 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 11:28
- public functions (2): `feed`, `status`
- public classes (0): none
- test files (0): none
- readers (1): `mag/cast_server.py`

### mag/republic_governance.py

- lines: 380 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-15 19:12
- public functions (15): `resources`, `audit`, `level_for`, `ladder`, `sanction`, `report_offense`, `propose`, `consent`, `amend`, `roster`, `define_boundary`, `who_can_withdraw`, `constitution`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/dogfood_audit.py`, `mag/law.py`, `mag/ox_megaburn2.py`

### mag/republic_loop.py

- lines: 504 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 16:38
- public functions (2): `loop`, `status`
- public classes (0): none
- test files (0): none
- readers (3): `mag/ghost.py`, `mag/governor_autorun.py`, `mag/tool_synthesis.py`

### mag/republic_os.py

- lines: 358 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 23:20
- public functions (11): `boot`, `checkpoint`, `own`, `release`, `seed_aos`, `round_cycle`, `memory_block`, `self_reinforce`, `status`, `run_cadence`, `main`
- public classes (0): none
- test files (1): `tests/test_republic_os.py`
- readers (6): `dashboard/rest.py`, `mag/cleanup_steal.py`, `mag/doctor.py`, `mag/ghost.py`, `mag/governor_autorun.py`, `main.py`

### mag/republic_wave.py

- lines: 196 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 16:11
- public functions (5): `contribute`, `dedupe`, `wave`, `simulate`, `main`
- public classes (0): none
- test files (2): `tests/test_reconstruct.py`, `tests/test_republic_wave.py`
- readers (5): `mag/abundance_rogue.py`, `mag/game_portal.py`, `mag/reconstruct.py`, `mag/republic_loop.py`, `mag/vram_hologram.py`

### mag/research_class.py

- lines: 255 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 08:58
- public functions (7): `classify`, `fold_classified`, `lens_read`, `coverage`, `gaps`, `tool_plan`, `status`
- public classes (0): none
- test files (0): none
- readers (5): `mag/emergence.py`, `mag/gap_frontier.py`, `mag/invariant_ledger.py`, `mag/novelty_lens.py`, `mag/swarm_emerge.py`

### mag/research_director.py

- lines: 811 | parse: ok | last commit: 60e18c524 2026-08-08 | mtime: 2026-08-08 05:51
- public functions (7): `sense_all`, `analyze`, `plan_experiments`, `execute_experiment`, `learn_from_cycle`, `research_cycle`, `run_continuous`
- public classes (3): `ResearchState`, `ExperimentPlan`, `ResearchCycle`
- test files (0): none
- readers (1): `mag/framework_map.py`

### mag/research_fanout.py

- lines: 476 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 21:03
- public functions (8): `battery_digest`, `battery`, `call_lane`, `probe_lanes`, `run`, `retry`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_dormant_gate_b2133.py`
- readers (5): `configs/providers.yaml`, `mag/corpus_selfsteal.py`, `mag/dormant.py`, `mag/salon_50.py`, `scripts/union_fullsend_day.py`

### mag/research_fold.py

- lines: 168 | parse: ok | last commit: de7bb85fe 2026-08-09 | mtime: 2026-08-08 23:20
- public functions (4): `fold_one`, `run`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_research_fold.py`
- readers (5): `mag/governor_autorun.py`, `mag/research_lens.py`, `mag/stateless_research.py`, `mag/steal_pack.py`, `memory/trash/20260810T202850Z/_tmp_stateless_swarm_research.py`

### mag/research_lens.py

- lines: 407 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 09:20
- public functions (7): `reindex`, `retrieve_prior`, `build_lens`, `fold_back`, `status`, `run_cadence`, `main`
- public classes (0): none
- test files (0): none
- readers (12): `dashboard/rest.py`, `mag/adventure_moonshot.py`, `mag/aos_grok.py`, `mag/deep_research_moonshot.py`, `mag/doctor.py`, `mag/flex_test.py`, `mag/ghost.py`, `mag/governor_autorun.py` + 4 more

### mag/research_pack.py

- lines: 781 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (6): `build_research_pack`, `load_pack`, `pack_body_excerpts`, `answer_grounded_in_pack`, `score_fidelity`, `run_pack`
- public classes (0): none
- test files (1): `tests/test_lattice_grounding.py`
- readers (8): `mag/blast.py`, `mag/dispatch.py`, `mag/improve.py`, `mag/lattice_loop.py`, `mag/oracle.py`, `mag/press_digest.py`, `mag/research_lens.py`, `main.py`

### mag/research_worker.py

- lines: 116 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-31 00:11
- public functions (2): `run`, `main`
- public classes (0): none
- test files (0): none
- readers (4): `mag/orchestrator.py`, `mag/organ_map.py`, `mag/swarm_worker.py`, `state/backups/orphan_close_20260906/organ_map.py`

### mag/resonance.py

- lines: 193 | parse: ok | last commit: f31c0e926 2026-08-05 | mtime: 2026-08-06 18:28
- public functions (4): `score_echoes`, `top_cards`, `tick`, `format_l0e`
- public classes (0): none
- test files (1): `tests/test_v3_modules.py`
- readers (5): `mag/context_pack.py`, `mag/framework_map.py`, `mag/system_map.py`, `main.py`, `scripts/roadmap_gap_probe.py`

### mag/resource_governor.py

- lines: 155 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 13:09
- public functions (2): `run`, `status`
- public classes (0): none
- test files (0): none
- readers (1): `mag/compiler_flywheel.py`

### mag/resume_order.py

- lines: 261 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 20:23
- public functions (5): `rank`, `pick`, `status`, `compile_`, `promote_drainer`
- public classes (0): none
- test files (0): none
- readers (1): `mag/orchestrator.py`

### mag/rib_action.py

- lines: 201 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 16:57
- public functions (6): `declare`, `spawn_agents`, `run_three_body`, `influence`, `emit_actions`, `main`
- public classes (1): `ActionRib`
- test files (0): none
- readers (5): `mag/attractor_tools.py`, `mag/frontier_gravity.py`, `mag/ghost_experimenter.py`, `mag/readout_controller.py`, `mag/rib_k8s.py`

### mag/rib_bus.py

- lines: 244 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 10:20
- public functions (6): `publish_rib`, `mount`, `inject_for`, `machine_lower`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_seat_steer.py`
- readers (50): `_finish.py`, `_wave_fold.py`, `_wave_fold2.py`, `mag/agent_knot.py`, `mag/arrival.py`, `mag/autonomous_research.py`, `mag/bus_cadence.py`, `mag/compiler_flywheel.py` + 42 more

### mag/rib_cache.py

- lines: 142 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-05 00:11
- public functions (3): `rib`, `rib_chat`, `main`
- public classes (0): none
- test files (0): none
- readers (27): `_alpha_dryrun.py`, `_alpha_multi.py`, `_alpha_rar.py`, `_alpha_rar_deepseek.py`, `_alpha_rar_fleet.py`, `_alpha_steer.py`, `_alpha_zai.py`, `_cache_mine.py` + 19 more

### mag/rib_gif.py

- lines: 120 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 11:28
- public functions (3): `test_rib`, `render`, `status`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/rib_k8s.py

- lines: 194 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 17:36
- public functions (4): `invariants`, `reconcile`, `report`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/rib_os.py

- lines: 137 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 12:47
- public functions (2): `step`, `status`
- public classes (0): none
- test files (0): none
- readers (1): `mag/republic_loop.py`

### mag/rib_renderer.py

- lines: 98 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 06:19
- public functions (4): `from_frontier`, `dispatch`, `render`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/rib_store.py

- lines: 77 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-28 10:58
- public functions (3): `put`, `get`, `stats`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/rib_struct.py

- lines: 178 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-09 22:48
- public functions (7): `declare`, `room`, `steer_slot`, `assign`, `fill`, `survey`, `main`
- public classes (1): `RibStructure`
- test files (0): none
- readers (2): `mag/emergent_harvest.py`, `mag/roshomon.py`

### mag/riddle_direction.py

- lines: 141 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-24 12:23
- public functions (3): `direction_graph`, `ask`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/riddler.py

- lines: 520 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 09:16
- public functions (5): `compile_surrogate`, `fingerprint_randomize`, `validate_surrogate`, `save_surrogate`, `load_private_map`
- public classes (3): `SurrogateStory`, `PrivateGraph`, `ValidationReport`
- test files (2): `tests/test_riddler.py`, `tests/test_riddler_map.py`
- readers (9): `configs/riddler_charged_graphs.yaml`, `mag/fish_ear.py`, `mag/flock_steal.py`, `mag/ghost_whisper.py`, `mag/riddle_direction.py`, `mag/riddler_coherence.py`, `mag/riddler_map.py`, `mag/riddler_transport.py` + 1 more

### mag/riddler_campaign.py

- lines: 634 | parse: ok | last commit: de7bb85fe 2026-08-09 | mtime: 2026-08-08 23:36
- public functions (3): `get_crafter`, `craft_campaign`, `verify_campaign`
- public classes (4): `PartyMember`, `CampaignEncounter`, `Campaign`, `CampaignCrafter`
- test files (0): none
- readers (1): `mag/narrative_engine.py`

### mag/riddler_coherence.py

- lines: 164 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-15 21:13
- public functions (4): `compile_invariant_surrogate`, `run`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/riddler_map.py

- lines: 299 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-28 21:13
- public functions (8): `graph_from_payload`, `compile_payload`, `public_face`, `private_face`, `validation_face`, `bind_room`, `bind_campaign`, `bind_guild`
- public classes (0): none
- test files (1): `tests/test_riddler_map.py`
- readers (0): none

### mag/riddler_sanitize.py

- lines: 225 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 21:13
- public functions (3): `sanitize`, `sanitize_message`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/session_bridge.py`

### mag/riddler_tap.py

- lines: 215 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 19:29
- public functions (9): `roleplay_prompt`, `encode`, `tap`, `decode`, `distribute`, `run`, `run_cadence`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/riddler_trajectory.py

- lines: 152 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-08 07:29
- public functions (6): `scrub`, `action_shape`, `refs_of`, `emit`, `show`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/riddler_transport.py

- lines: 461 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 11:05
- public functions (4): `send_surrogate`, `send_surrogate_with_steer`, `riddler_query`, `quick_riddler`
- public classes (1): `RiddlerResult`
- test files (0): none
- readers (5): `configs/riddler_charged_graphs.yaml`, `mag/flock_steal.py`, `mag/research_director.py`, `mag/riddle_direction.py`, `memory/trash/20260810T202850Z/_tmp_research_sprint.py`

### mag/right_size_skills.py

- lines: 159 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 15:30
- public functions (3): `right_size`, `catalog`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/skill_pipeline.py`

### mag/rightsize_all.py

- lines: 162 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 13:55
- public functions (4): `audit`, `apply`, `run_cadence`, `main`
- public classes (0): none
- test files (0): none
- readers (4): `dashboard/rest.py`, `mag/flex_test.py`, `mag/governor_autorun.py`, `mag/rightsize_api.py`

### mag/rightsize_api.py

- lines: 145 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 19:53
- public functions (4): `build`, `status`, `endpoints`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `dashboard/rest.py`

### mag/rightsize_wave.py

- lines: 139 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-15 09:17
- public functions (4): `wave`, `collapse`, `scale`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/roadmap_runner.py

- lines: 303 | parse: ok | last commit: 343781ff7 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (5): `select_next`, `compile_run`, `execute_contract`, `run_next`, `status`
- public classes (0): none
- test files (1): `tests/test_roadmap_runner.py`
- readers (2): `mag/attention_ranker.py`, `main.py`

### mag/room_state.py

- lines: 292 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-06 00:10
- public functions (10): `load_steps`, `parse_ts`, `wall_fires`, `attention`, `histogram`, `economy`, `chain_tip`, `persisted_invariants`, `content_hash`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `tools/light_walk.py`

### mag/roshomon.py

- lines: 364 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 16:46
- public functions (9): `state_snapshot`, `questions`, `dispatch`, `compare`, `create`, `rib_declare`, `rib_survey`, `fill_via_rib`, `main`
- public classes (0): none
- test files (0): none
- readers (9): `mag/_deep_research_verkle_dedupe.py`, `mag/adventure_moonshot.py`, `mag/attractor_tools.py`, `mag/deep_research_moonshot.py`, `mag/frontier_intake.py`, `mag/readout_controller.py`, `mag/rib_renderer.py`, `mag/roshomon_mine.py` + 1 more

### mag/roshomon_mine.py

- lines: 165 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 15:57
- public functions (4): `roshomon_mine`, `inform_swarm`, `tesuji_from_sessions`, `main`
- public classes (0): none
- test files (1): `tests/test_roshomon_mine.py`
- readers (2): `mag/republic_loop.py`, `mag/session_ritual.py`

### mag/rotation_harness.py

- lines: 199 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 19:10
- public functions (3): `adjusted_rand`, `parse_partition`, `run`
- public classes (0): none
- test files (1): `tests/test_dormant_gate_b2133.py`
- readers (1): `mag/dormant.py`

### mag/route.py

- lines: 170 | parse: ok | last commit: 36914e134 2026-08-07 | mtime: 2026-08-07 12:32
- public functions (1): `route_goal`
- public classes (0): none
- test files (2): `tests/test_clerk_route_fix.py`, `tests/test_memory_events.py`
- readers (15): `configs/modules.yaml`, `mag/memory_events.py`, `main.py`, `memory/runs/20260803-clerk-fix/debug_amb.py`, `memory/runs/20260803-clerk-fix/debug_echo.py`, `memory/runs/20260803-clerk-fix/debug_hang.py`, `memory/runs/20260803-clerk-fix/debug_recall.py`, `memory/runs/20260803-clerk-fix/fanout.py` + 7 more

### mag/route_trace.py

- lines: 175 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 16:02
- public functions (5): `hop`, `trace`, `origin`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_route_trace.py`
- readers (2): `mag/republic_loop.py`, `mag/wireshark_steal.py`

### mag/router.py

- lines: 1045 | parse: ok | last commit: 6f150864a 2026-09-28 | mtime: 2026-09-28 12:56
- public functions (5): `gather_signals`, `classify_depth`, `route`, `route_task`, `route_with_snapshot`
- public classes (0): none
- test files (6): `tests/test_autorun_v1.py`, `tests/test_factory_freeze_gate.py`, `tests/test_fork_router.py`, `tests/test_router.py`, `tests/test_router_comms_boost.py`, `tests/test_skill_seat.py`
- readers (20): `configs/modules.yaml`, `mag/agent_cli.py`, `mag/brain.py`, `mag/conductor.py`, `mag/coordination.py`, `mag/dashboard_plugin.py`, `mag/decision_framework.py`, `mag/dispatch.py` + 12 more

### mag/routing_concert.py

- lines: 311 | parse: ok | last commit: 36914e134 2026-08-07 | mtime: 2026-08-07 13:12
- public functions (5): `build_concert_plan`, `run_concert_step`, `run_concert`, `conductor_review_plan`, `status`
- public classes (0): none
- test files (1): `tests/test_routing_concert.py`
- readers (4): `dashboard/rest.py`, `mag/framework_map.py`, `mag/organ_map.py`, `state/backups/orphan_close_20260906/organ_map.py`

### mag/run_trail.py

- lines: 1020 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-09-28 01:02
- public functions (25): `normalize_seat`, `cap_core`, `ensure_runs_root`, `load_active`, `load_run`, `save_run`, `set_active`, `repair_active`, `snapshot_base`, `ensure_run_base`, `normalize_drift_kind`, `list_drifts`, `start_run`, `write_progress_md`, `file_agent_core`, `append_event`, `check_seat`, `related_run_card`, `append_related_run`, `list_related_runs`, `close_run`, `read_trail`, `cores_for_reinject`, `trail_pack_excerpt`, `status`
- public classes (0): none
- test files (3): `tests/test_base_drift.py`, `tests/test_coding_session_loop.py`, `tests/test_run_worth.py`
- readers (12): `configs/modules.yaml`, `mag/bonds.py`, `mag/coding_session_loop.py`, `mag/context_pack.py`, `mag/dispatch.py`, `mag/factory_machine.py`, `mag/framework_map.py`, `mag/modules.py` + 4 more

### mag/run_worth.py

- lines: 555 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (12): `load_config`, `operator_overrides`, `is_operator_marked_good`, `mark_run_good`, `log_event`, `signals_from_run`, `score_worth`, `classify_run`, `detect_hung`, `gate_before_truncate`, `evaluate_task_hung`, `status`
- public classes (0): none
- test files (1): `tests/test_run_worth.py`
- readers (4): `mag/framework_map.py`, `mag/orchestrator.py`, `mag/run_trail.py`, `main.py`

### mag/runtime.py

- lines: 204 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-28 19:44
- public functions (4): `write_heartbeat`, `read_heartbeat`, `start_watch_thread`, `run_integral`
- public classes (0): none
- test files (1): `tests/test_reconnect_cage_first.py`
- readers (9): `mag/daemon.py`, `mag/guard.py`, `mag/health.py`, `mag/lanes.py`, `mag/operator_os.py`, `mag/organ_map.py`, `mag/self_audit.py`, `main.py` + 1 more

### mag/runtime_policy.py

- lines: 55 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 09:05
- public functions (1): `host_runtime_blocked`
- public classes (0): none
- test files (1): `tests/test_process_supervisor.py`
- readers (3): `mag/ghost.py`, `mag/governor_autorun.py`, `mag/process_supervisor.py`

### mag/saelis_room.py

- lines: 349 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 12:54
- public functions (4): `state`, `saelis_say`, `serve`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/saelis_seat.py

- lines: 163 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-17 21:29
- public functions (4): `fold_rib`, `speak`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/saelis_room.py`, `mag/swarm_local_drain.py`, `mag/vast_launcher.py`

### mag/saelis_world_brief.py

- lines: 107 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-18 08:05
- public functions (2): `brief`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/salon_50.py

- lines: 210 | parse: ok | last commit: cf99e64fb 2026-09-15 | mtime: 2026-09-15 22:50
- public functions (3): `build_battery`, `run`, `fold`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/salon_openclaw.py

- lines: 308 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 22:22
- public functions (4): `room_post`, `round_room`, `chan`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/chan.py`

### mag/scale_salon.py

- lines: 264 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 19:36
- public functions (2): `call`, `main`
- public classes (0): none
- test files (1): `tests/test_dormant_gate_b2521.py`
- readers (0): none

### mag/schema_registry.py

- lines: 305 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 12:13
- public functions (9): `versions`, `checkpoint`, `history`, `status`, `hermetic_id`, `commit_stateless`, `resolve`, `gc`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `dashboard/rest.py`, `mag/dogfood_audit.py`, `mag/knowledge_graph.py`

### mag/scifi_fantasy_steal.py

- lines: 173 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 10:23
- public functions (5): `corpus`, `deep_steal`, `results`, `run`, `status`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/scribe.py

- lines: 131 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 16:29
- public functions (4): `surface`, `render`, `scribe`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `deploy/k8s/mag-scribe-cronjob.yaml`, `mag/afk_orchestrator.py`, `mag/skill_pipeline.py`

### mag/scrum.py

- lines: 272 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-24 07:28
- public functions (6): `sync_from_todo`, `backlog`, `sprint`, `advance`, `surface`, `main`
- public classes (0): none
- test files (0): none
- readers (7): `mag/afk_cadence.py`, `mag/afk_loop.py`, `mag/cleanup_steal.py`, `mag/ghost.py`, `mag/ghost_control.py`, `mag/press_digest.py`, `main.py`

### mag/seal.py

- lines: 214 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-24 12:29
- public functions (4): `seal`, `verify`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/standing.py`

### mag/seat_availability.py

- lines: 176 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 20:49
- public functions (3): `ping`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/surface_render.py`, `mag/team_knot.py`

### mag/seat_corpus.py

- lines: 304 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 19:36
- public functions (3): `compile_corpus`, `show`, `main`
- public classes (0): none
- test files (2): `tests/test_dormant_gate_b2521.py`, `tests/test_seat_corpus.py`
- readers (1): `mag/openclaw_catalog.py`

### mag/seat_dispatch.py

- lines: 319 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-03 22:59
- public functions (3): `task`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/board_directive.py`, `mag/ladder.py`, `mag/salon_openclaw.py`

### mag/seat_feed.py

- lines: 157 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 18:48
- public functions (1): `unified_seat_feed`
- public classes (0): none
- test files (2): `tests/test_phase2_surface.py`, `tests/test_stack.py`
- readers (3): `dashboard/rest.py`, `mag/chronicle.py`, `mag/stack.py`

### mag/seat_fork.py

- lines: 69 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-12 18:01
- public functions (1): `fork_seat`
- public classes (0): none
- test files (0): none
- readers (1): `scripts/hofw_001_seed.sh`

### mag/seat_guard.py

- lines: 389 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-09 21:35
- public functions (2): `run_seat`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `main.py`

### mag/seat_hunter.py

- lines: 702 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 20:33
- public functions (14): `discover_grok_seats`, `grok_bill`, `codex_bill`, `deepseek_bill`, `ingest_deepseek_bill`, `discover_openrouter_free`, `quota_status`, `mark_lane_exhausted`, `next_lane`, `hunt`, `free_lanes`, `status`, `accounts`, `main`
- public classes (0): none
- test files (0): none
- readers (4): `mag/ox_availability.py`, `mag/real_swarm.py`, `mag/seat_availability.py`, `mag/surface_render.py`

### mag/seat_probe.py

- lines: 112 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-24 15:35
- public functions (2): `SEATS`, `run`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/seat_registry.py

- lines: 289 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 17:14
- public functions (7): `register`, `heartbeat`, `unregister`, `list_registered`, `mesh_peers`, `register_env_for_launch`, `main`
- public classes (0): none
- test files (2): `tests/test_seat_registry.py`, `tests/test_unsloth_seat.py`
- readers (19): `dashboard/rest.py`, `mag/chatgpt_bot.py`, `mag/chatgpt_desktop.py`, `mag/electron_seat.py`, `mag/framework_map.py`, `mag/grok_bot.py`, `mag/grok_desktop.py`, `mag/matrix_router.py` + 11 more

### mag/seat_steer.py

- lines: 258 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-14 06:42
- public functions (5): `resolve_surface`, `send`, `enqueue`, `execute_goal`, `status`
- public classes (0): none
- test files (2): `tests/test_frontier_salon.py`, `tests/test_seat_steer.py`
- readers (8): `dashboard/rest.py`, `mag/bus_cadence.py`, `mag/frontier_salon.py`, `mag/game_dm.py`, `mag/orchestrator.py`, `mag/republic_loop.py`, `mag/self_steal.py`, `mag/surface_adapters.py`

### mag/seats.py

- lines: 392 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (2): `build_workers_summary`, `build_seats_registry`
- public classes (0): none
- test files (1): `tests/test_router.py`
- readers (4): `dashboard/rest.py`, `mag/chronicle.py`, `mag/free_frontend_swarm.py`, `main.py`

### mag/seed_chain.py

- lines: 142 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 16:32
- public functions (4): `chain`, `solve`, `seed_build`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/afk_loop.py`, `mag/skill_pipeline.py`

### mag/seed_percolator.py

- lines: 133 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-27 09:38
- public functions (4): `judge`, `paired_run`, `report`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/seed_registry.py

- lines: 518 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-07 09:27
- public functions (6): `scan_manifest`, `print_card`, `cmd_scan`, `cmd_register`, `cmd_verify_registry`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/seeds.py

- lines: 166 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-24 10:52
- public functions (5): `plant`, `active`, `rank`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/chord_circuit.py`, `mag/ox_resident.py`

### mag/self_advance.py

- lines: 157 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 16:29
- public functions (4): `reflect`, `plan`, `expand`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/afk_orchestrator.py`, `mag/skill_pipeline.py`

### mag/self_audit.py

- lines: 328 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 12:55
- public functions (6): `run_tier`, `status`, `start_scheduler`, `stop_scheduler`, `scheduler_status`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/organ_map.py`, `memory/working/test_self_audit.py`, `state/backups/orphan_close_20260906/organ_map.py`

### mag/self_drive.py

- lines: 230 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 11:59
- public functions (6): `redraft`, `cached_context`, `learned_principles`, `plan`, `drive`, `main`
- public classes (0): none
- test files (0): none
- readers (9): `mag/flock_scheduler.py`, `mag/ghost_whisper.py`, `mag/invariant.py`, `mag/rightsize_api.py`, `mag/self_drive_cadence.py`, `mag/session_route.py`, `mag/skill_pipeline.py`, `mag/training_rightsize.py` + 1 more

### mag/self_drive_cadence.py

- lines: 153 | parse: ok | last commit: de7bb85fe 2026-08-09 | mtime: 2026-08-09 01:16
- public functions (1): `run`
- public classes (0): none
- test files (0): none
- readers (1): `mag/governor_autorun.py`

### mag/self_hologram.py

- lines: 149 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-06 10:46
- public functions (1): `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/self_loop.py

- lines: 203 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 10:17
- public functions (5): `map_self`, `talk_stochastic`, `loop_zeitgeist`, `loop`, `status`
- public classes (0): none
- test files (0): none
- readers (6): `mag/castle_foundation.py`, `mag/final_steal.py`, `mag/future_self.py`, `mag/gap_frontier.py`, `mag/republic_loop.py`, `mag/tripartite.py`

### mag/self_steal.py

- lines: 412 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 23:32
- public functions (4): `audit`, `enqueue_research`, `run_cadence`, `main`
- public classes (0): none
- test files (1): `tests/test_self_steal.py`
- readers (7): `mag/corpus_wave.py`, `mag/doctor.py`, `mag/governor_autorun.py`, `mag/moonshot_engine.py`, `mag/tactical_framework.py`, `mag/vantage_audit.py`, `main.py`

### mag/self_test.py

- lines: 195 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 08:43
- public functions (7): `byte_identity`, `rederive`, `generation`, `not_arbitrary`, `observer_record`, `run`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `memory/runs/_dbg_self.py`

### mag/self_train_data.py

- lines: 161 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 07:54
- public functions (3): `gather`, `fold`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/republic_loop.py`

### mag/self_vision.py

- lines: 207 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 02:14
- public functions (6): `questions`, `sort_via_k8s`, `vision`, `cycle`, `socratic_dialog`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/republic_loop.py`

### mag/sense.py

- lines: 77 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (1): `sense`
- public classes (0): none
- test files (1): `tests/test_mag_sense.py`
- readers (4): `mag/daemon.py`, `mag/ghost.py`, `mag/legacy_audit.py`, `mag/orphan_sense.py`

### mag/sentinel.py

- lines: 153 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 06:36
- public functions (4): `watch`, `intervene`, `run`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `dashboard/rest.py`, `mag/ghost.py`, `mag/skill_pipeline.py`

### mag/session_bridge.py

- lines: 355 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-31 00:37
- public functions (15): `sanitize`, `ensure_dirs`, `discover_sessions`, `read_outbox`, `write_to_inbox`, `update_window`, `post`, `relay`, `read_inbox`, `window_html`, `cmd_post`, `cmd_relay`, `cmd_read`, `cmd_window`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/dogfood_audit.py`, `mag/organ_map.py`, `state/backups/orphan_close_20260906/organ_map.py`

### mag/session_card.py

- lines: 288 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (6): `clean_operator_text`, `real_operator_asks`, `build_session_card`, `attach_card_to_dossier`, `recompute_card_file`, `recompute_all_cards`
- public classes (0): none
- test files (0): none
- readers (6): `configs/modules.yaml`, `dashboard/server.py`, `mag/registry.py`, `mag/session_dossier.py`, `main.py`, `memory/portable_bags/bag-20260727T214646Z/configs/modules.yaml`

### mag/session_dossier.py

- lines: 665 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (4): `build_dossier`, `write_dossier_assets`, `render_pdf`, `write_session_pack`
- public classes (0): none
- test files (0): none
- readers (1): `mag/biography.py`

### mag/session_freeze.py

- lines: 313 | parse: ok | last commit: 60e18c524 2026-08-08 | mtime: 2026-08-08 09:43
- public functions (3): `freeze_session_snapshot`, `write_freeze`, `load_latest_freeze`
- public classes (0): none
- test files (1): `tests/test_session_freeze.py`
- readers (3): `dashboard/rest.py`, `memory/working/_nest.py`, `memory/working/_nest2.py`

### mag/session_koan.py

- lines: 322 | parse: ok | last commit: de7bb85fe 2026-08-09 | mtime: 2026-08-08 22:03
- public functions (4): `generate_koans`, `recent_koans`, `koan_wall`, `close_session_with_koans`
- public classes (1): `Koan`
- test files (0): none
- readers (0): none

### mag/session_maze.py

- lines: 287 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-16 17:43
- public functions (5): `assemble`, `persist`, `deep_handoff`, `escalate_cached`, `main`
- public classes (0): none
- test files (0): none
- readers (12): `dashboard/rest.py`, `mag/elevate.py`, `mag/fuel_feed.py`, `mag/grok_seat_burner.py`, `mag/grok_steer.py`, `mag/hero_simulation.py`, `mag/self_drive.py`, `mag/self_steal.py` + 4 more

### mag/session_overseer.py

- lines: 310 | parse: ok | last commit: 60e18c524 2026-08-08 | mtime: 2026-08-08 07:57
- public functions (6): `find_transcripts`, `read_transcript`, `gather_state`, `decide`, `latest_session_id`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `dashboard/rest.py`

### mag/session_rib.py

- lines: 269 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-01 21:02
- public functions (8): `thread_invariant`, `threads`, `dedupe`, `scene`, `dispatch`, `ab_test`, `status`, `stream_of_consciousness`
- public classes (0): none
- test files (0): none
- readers (1): `mag/interrupt_pipeline.py`

### mag/session_ritual.py

- lines: 471 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 16:02
- public functions (3): `session_start`, `session_exit`, `ritual`
- public classes (1): `SessionRecord`
- test files (0): none
- readers (0): none

### mag/session_route.py

- lines: 191 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-18 07:43
- public functions (7): `default_agent_state`, `read_seed`, `formatting_block`, `learned_block`, `preamble`, `render`, `main`
- public classes (0): none
- test files (1): `tests/test_session_route.py`
- readers (5): `mag/agent_cli.py`, `mag/invariant.py`, `mag/prefix_prover.py`, `mag/skill_pipeline.py`, `main.py`

### mag/session_state_brief.py

- lines: 382 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 14:00
- public functions (4): `gather_state`, `render_brief`, `write_brief`, `main`
- public classes (0): none
- test files (1): `tests/test_session_freeze.py`
- readers (5): `mag/janitor.py`, `mag/session_freeze.py`, `mag/state_brief.py`, `main.py`, `tools/visor.py`

### mag/shader_bus.py

- lines: 179 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 12:30
- public functions (6): `render`, `register_frame`, `bus_encode`, `bus_decode`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (5): `mag/dogfood_audit.py`, `mag/novelty_lens.py`, `mag/research_class.py`, `mag/self_steal.py`, `mag/swarm_render.py`

### mag/shader_rib.py

- lines: 217 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 10:30
- public functions (5): `rib_from_shader`, `lens_rib`, `determinism_test`, `interstitial_patterns`, `status`
- public classes (0): none
- test files (0): none
- readers (1): `mag/compiler_lang.py`

### mag/shadow_graph.py

- lines: 198 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 09:27
- public functions (5): `build`, `latent_signal`, `sense_system`, `jungal_loop`, `status`
- public classes (0): none
- test files (0): none
- readers (5): `mag/diamond_mine.py`, `mag/emergence.py`, `mag/invariant_ledger.py`, `mag/orphan_sense.py`, `mag/swarm_emerge.py`

### mag/shadow_quest.py

- lines: 160 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 23:20
- public functions (4): `surface`, `quest`, `material`, `status`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/shadow_slab.py

- lines: 121 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-05 23:38
- public functions (4): `carve`, `stats`, `volume`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/shadow_work.py

- lines: 148 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 12:53
- public functions (5): `shadow`, `ledger`, `audit`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (5): `mag/_deep_research_verkle_dedupe.py`, `mag/adventure_moonshot.py`, `mag/deep_research_moonshot.py`, `mag/dogfood_audit.py`, `mag/shadow_quest.py`

### mag/shape_map.py

- lines: 281 | parse: ok | last commit: f1bceeb3a 2026-09-27 | mtime: 2026-09-27 16:58
- public functions (8): `shape_for`, `verify`, `reconstruct`, `family_claims`, `shape`, `portfolio`, `export`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/gap_resolver.py`, `mag/governor_autorun.py`, `mag/tool_quant.py`

### mag/shape_seed.py

- lines: 233 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 17:04
- public functions (7): `seed`, `derive`, `verify`, `give`, `route_shape`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_shape_seed.py`
- readers (2): `mag/republic_loop.py`, `mag/self_steal.py`

### mag/shared_surface.py

- lines: 426 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 19:05
- public functions (2): `inspect_surface`, `main`
- public classes (0): none
- test files (5): `tests/test_env_redirect_tripwire.py`, `tests/test_events_key_schema.py`, `tests/test_index_fold_host.py`, `tests/test_links_sha_ratchet.py`, `tests/test_shared_surface_events.py`
- readers (7): `mag/env_redirect.py`, `mag/events_key_schema.py`, `mag/events_scan.py`, `mag/links_sha_ratchet.py`, `mag/links_split_gate.py`, `scripts/build_deck.py`, `tools/visor.py`

### mag/shelf_pdf.py

- lines: 99 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-06 18:19
- public functions (2): `shelf_pdf`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/signal_flare.py

- lines: 543 | parse: ok | last commit: 482e0a3c8 2026-08-08 | mtime: 2026-08-08 19:11
- public functions (5): `generate_flare`, `generate_nudge`, `fire_flare`, `scan_for_flares`, `respond_to_flares`
- public classes (3): `Flare`, `Nudge`, `FlareShield`
- test files (0): none
- readers (1): `mag/doctor_agent.py`

### mag/signals.py

- lines: 164 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-09 22:48
- public functions (10): `wilson_lower`, `ucb1`, `beta_score`, `recency_decay`, `ewma_update`, `normalize`, `combine`, `proven_move`, `quantize_band`, `stats`
- public classes (0): none
- test files (0): none
- readers (1): `mag/model_health.py`

### mag/single_feed.py

- lines: 82 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-04 22:15
- public functions (1): `build_snapshot`
- public classes (0): none
- test files (0): none
- readers (1): `mag/lane_runner.py`

### mag/skill_drop.py

- lines: 197 | parse: ok | last commit: 60e18c524 2026-08-08 | mtime: 2026-08-07 18:15
- public functions (7): `right_size`, `freeze`, `verify_drop`, `drop_skill`, `release_due`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_skill_drop.py`
- readers (3): `mag/ai_landscape.py`, `mag/framework_map.py`, `mag/job_floor.py`

### mag/skill_ledger.py

- lines: 345 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 16:44
- public functions (9): `normalize_outcome`, `is_win`, `proven_moves`, `record_decision`, `record_labeled_row`, `progress`, `seed_from_bench`, `seed_from_training`, `main`
- public classes (0): none
- test files (7): `tests/test_icon_drop_escape.py`, `tests/test_icon_drop_fold.py`, `tests/test_pro_library.py`, `tests/test_pro_library_eval.py`, `tests/test_skill_ledger.py`, `tests/test_skill_ledger_outcome_vocab.py`, `tests/test_state_pile.py`
- readers (30): `dashboard/rest.py`, `mag/batch_scribe.py`, `mag/breakthrough_loop.py`, `mag/clippy.py`, `mag/context_pack.py`, `mag/cost_learn.py`, `mag/elevate.py`, `mag/embassy_deliver.py` + 22 more

### mag/skill_lifecycle.py

- lines: 420 | parse: ok | last commit: a5dd96176 2026-09-25 | mtime: 2026-09-25 20:42
- public functions (11): `is_enabled`, `available_skills`, `skill_body`, `current_turn`, `reset_state`, `begin_turn`, `load`, `unload`, `end_turn`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_skill_lifecycle.py`
- readers (1): `tools/__init__.py`

### mag/skill_pipeline.py

- lines: 358 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 05:26
- public functions (4): `match`, `route`, `run`, `main`
- public classes (0): none
- test files (1): `tests/test_loop_death_guards.py`
- readers (7): `mag/afk_loop.py`, `mag/ghost_control.py`, `mag/ghost_nudge.py`, `mag/ghost_talk.py`, `mag/right_size_skills.py`, `mag/self_advance.py`, `mag/word_skill_map.py`

### mag/skill_seat.py

- lines: 112 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (5): `load_skill`, `pick_skill_for_goal`, `build_preamble`, `run_gate`, `skill_status`
- public classes (0): none
- test files (1): `tests/test_skill_seat.py`
- readers (4): `mag/conductor.py`, `mag/skill_lifecycle.py`, `main.py`, `scripts/roadmap_gap_probe.py`

### mag/skills_pack.py

- lines: 73 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (2): `load_skills_cfg`, `skills_for_job`
- public classes (0): none
- test files (0): none
- readers (4): `mag/context_pack.py`, `mag/governor_autorun.py`, `mag/router.py`, `mag/skill_lifecycle.py`

### mag/social_hone.py

- lines: 154 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-13 09:23
- public functions (4): `drive`, `socratic`, `hone`, `status`
- public classes (0): none
- test files (1): `tests/test_social_hone.py`
- readers (0): none

### mag/socratic.py

- lines: 159 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (2): `prior_context`, `workshop`
- public classes (0): none
- test files (0): none
- readers (2): `mag/skill_pipeline.py`, `main.py`

### mag/socratic_research.py

- lines: 142 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 15:57
- public functions (4): `frame`, `ask`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_socratic_research.py`
- readers (2): `mag/republic_loop.py`, `mag/social_hone.py`

### mag/socratic_tree.py

- lines: 159 | parse: ok | last commit: de7bb85fe 2026-08-09 | mtime: 2026-08-09 00:05
- public functions (2): `socratic`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/solved_surface.py

- lines: 117 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 08:41
- public functions (2): `solved`, `main`
- public classes (0): none
- test files (1): `tests/test_surface_contract.py`
- readers (2): `dashboard/rest.py`, `mag/context_pack.py`

### mag/source_trace.py

- lines: 390 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 13:28
- public functions (5): `dedupe_uv_pairs`, `trace_source`, `sense`, `break_source`, `main`
- public classes (0): none
- test files (1): `tests/test_source_trace.py`
- readers (3): `mag/ghost.py`, `mag/loop_breaker.py`, `mag/route_trace.py`

### mag/sovereign_dashboard.py

- lines: 244 | parse: ok | last commit: de7bb85fe 2026-08-09 | mtime: 2026-08-09 00:08
- public functions (2): `sovereign_dashboard`, `sovereign_endpoint`
- public classes (0): none
- test files (1): `tests/test_surface_contract.py`
- readers (2): `dashboard/rest.py`, `mag/ghost.py`

### mag/sovereign_handshake.py

- lines: 245 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 17:02
- public functions (7): `advertise`, `discover`, `handshake`, `web`, `connect`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_sovereign_handshake.py`
- readers (2): `mag/republic_loop.py`, `mag/self_steal.py`

### mag/space_ear.py

- lines: 147 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-09 18:19
- public functions (5): `geturl`, `transcribe`, `listen`, `transcribe_file`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/spawn_manifest.py

- lines: 342 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-07 01:13
- public functions (5): `resolve_ref`, `cmd_record`, `cmd_check`, `cmd_resolve`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/spec_gate.py

- lines: 200 | parse: ok | last commit: de7bb85fe 2026-08-09 | mtime: 2026-08-08 23:37
- public functions (8): `fingerprint`, `freeze`, `base_for`, `check`, `gate`, `verify_after`, `list_bases`, `main`
- public classes (0): none
- test files (2): `tests/test_pupeteering.py`, `tests/test_spec_gate_job_floor.py`
- readers (5): `dashboard/rest.py`, `mag/invariant.py`, `mag/job_floor.py`, `main.py`, `tools/pupeteer_gauntlet.py`

### mag/spider.py

- lines: 269 | parse: ok | last commit: 4706d5a04 2026-09-28 | mtime: 2026-09-28 14:05
- public functions (1): `tick`
- public classes (0): none
- test files (1): `tests/test_v3_modules.py`
- readers (7): `configs/modules.yaml`, `mag/checkin_route.py`, `mag/framework_map.py`, `mag/improve_loop.py`, `mag/stack.py`, `main.py`, `scripts/roadmap_gap_probe.py`

### mag/spine_exercise.py

- lines: 151 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-06 18:44
- public functions (1): `main`
- public classes (0): none
- test files (0): none
- readers (1): `state/backups/orphan_close_20260906/spine_exercise.py`

### mag/spore_seed.py

- lines: 195 | parse: ok | last commit: b1d714b02 2026-09-25 | mtime: 2026-09-25 08:26
- public functions (3): `generate_spore_seed`, `validate_spore_seed`, `verify_seat_continuity`
- public classes (0): none
- test files (1): `tests/test_spore_seed.py`
- readers (0): none

### mag/stack.py

- lines: 552 | parse: ok | last commit: e96fd62a4 2026-08-07 | mtime: 2026-08-06 18:55
- public functions (5): `build_fleet_triad`, `build_supervisor_snapshot`, `build_fleet_snapshot`, `build_research_glance`, `build_stack_payload`
- public classes (0): none
- test files (2): `tests/test_roadmap_gap_probe.py`, `tests/test_stack.py`
- readers (2): `dashboard/rest.py`, `scripts/roadmap_gap_probe.py`

### mag/stale_sweep.py

- lines: 97 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-05 21:38
- public functions (1): `sweep`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/standing.py

- lines: 312 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-24 13:59
- public functions (5): `run_once`, `run_loop`, `status`, `stop`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/standing_wave.py

- lines: 281 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-13 04:04
- public functions (8): `elias_lens`, `wave_packets`, `propagate`, `echo_detect`, `find_echoes`, `find_in_corpus`, `run`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/governor_autorun.py`

### mag/state_brief.py

- lines: 259 | parse: ok | last commit: de7bb85fe 2026-08-09 | mtime: 2026-08-08 21:11
- public functions (4): `gather`, `render`, `write`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `main.py`

### mag/state_quantizer.py

- lines: 484 | parse: ok | last commit: 482e0a3c8 2026-08-08 | mtime: 2026-08-08 19:11
- public functions (6): `extract_theme_vector`, `aggregate_theme_vectors`, `quantize_state`, `detect_phase_changes`, `create_memory_state`, `quantizer_status`
- public classes (1): `QuantizedMemory`
- test files (0): none
- readers (3): `mag/ghost.py`, `mag/persistent_agent.py`, `memory/trash/20260810T202850Z/_tmp_test_quantizer.py`

### mag/state_snapshot.py

- lines: 152 | parse: ok | last commit: 60e18c524 2026-08-08 | mtime: 2026-08-07 18:30
- public functions (3): `capture_summary`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_state_pile.py`
- readers (9): `dashboard/rest.py`, `mag/clippy.py`, `mag/decision_framework.py`, `mag/framework_map.py`, `mag/improve_loop.py`, `mag/vscode_feed.py`, `main.py`, `scripts/day_end_pile.ps1` + 1 more

### mag/stateless_research.py

- lines: 281 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 06:19
- public functions (5): `plan`, `launch`, `collect`, `local_steer`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/ghost_auto.py`

### mag/steal_first.py

- lines: 445 | parse: ok | last commit: 482e0a3c8 2026-08-08 | mtime: 2026-08-08 19:11
- public functions (5): `get_steal_first`, `steal_first`, `preload_nacho_invariants`, `preload_verkle_chain_segments`, `steal_first_endpoint`
- public classes (3): `StolenResult`, `StealFirstCache`, `StealFirstMiddleware`
- test files (0): none
- readers (2): `mag/flock_steal.py`, `mag/ghost.py`

### mag/steal_lens.py

- lines: 118 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 10:17
- public functions (3): `steal`, `reorg_map`, `status`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/steal_pack.py

- lines: 184 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 09:40
- public functions (4): `file_steal`, `file_all`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (10): `mag/flock_steal.py`, `mag/governor_autorun.py`, `mag/grok_frontier_loop.py`, `mag/mindweave_eval.py`, `mag/novelty_lens.py`, `mag/research_class.py`, `mag/steal_lens.py`, `mag/vscode_seat.py` + 2 more

### mag/steal_protocol_probe.py

- lines: 80 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (2): `run_steal_protocol_probe`, `build_steal_stack_row`
- public classes (0): none
- test files (0): none
- readers (1): `main.py`

### mag/steal_steer.py

- lines: 187 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-09 22:48
- public functions (4): `novelty`, `steer_query`, `coverage`, `main`
- public classes (0): none
- test files (0): none
- readers (6): `mag/emergent_harvest.py`, `mag/frontier_intake.py`, `mag/rib_action.py`, `mag/rib_struct.py`, `mag/roshomon.py`, `mag/shape_map.py`

### mag/steal_tools.py

- lines: 192 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-15 07:13
- public functions (8): `inventory`, `tools`, `to_js`, `js_file`, `sense`, `fold`, `route`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `scripts/_audit_have_need.py`, `scripts/_audit_tool_families.py`, `scripts/_route_tool_quant.py`

### mag/steer.py

- lines: 185 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-14 07:55
- public functions (6): `emit`, `consume`, `scan_unconsumed`, `mark_consumed`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_steer.py`
- readers (14): `_afk_full_blast.py`, `dashboard/rest.py`, `experiments/cascade_whisper.yaml`, `mag/bus_cadence.py`, `mag/game_campaign.py`, `mag/governor_autorun.py`, `mag/oh_fuck.py`, `mag/press_digest.py` + 6 more

### mag/steer_bridge.py

- lines: 151 | parse: ok | last commit: 60e18c524 2026-08-08 | mtime: 2026-08-07 15:18
- public functions (4): `steer`, `sync_guidance_file`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_steer_bridge.py`
- readers (1): `main.py`

### mag/steer_bus.py

- lines: 75 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-02 09:30
- public functions (1): `authorize`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/steer_engine.py

- lines: 174 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 09:57
- public functions (5): `compile_steer`, `spec`, `inject_for`, `fold`, `status`
- public classes (0): none
- test files (0): none
- readers (4): `mag/grok_warm_rib.py`, `mag/republic_loop.py`, `mag/rib_bus.py`, `mag/water_swarm.py`

### mag/steer_receipt_wire.py

- lines: 85 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-03 17:06
- public functions (2): `run_once`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/steer_router.py

- lines: 208 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 18:41
- public functions (8): `rightsize`, `pin`, `resume`, `pins`, `steer`, `record_steering`, `corpus`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/interrupt_pipeline.py`

### mag/steer_swarm.py

- lines: 190 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 01:36
- public functions (4): `testable_ask`, `plan`, `engage`, `status`
- public classes (0): none
- test files (0): none
- readers (3): `mag/autonomous_research.py`, `mag/republic_loop.py`, `mag/tool_synthesis.py`

### mag/steer_telemetry.py

- lines: 306 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 07:51
- public functions (7): `duplicate_candidates`, `probe_duplicate`, `collect`, `fold_policy`, `apply_at_launch`, `run_probe_pass`, `main`
- public classes (0): none
- test files (0): none
- readers (4): `mag/bernaise.py`, `mag/governor_autorun.py`, `mag/lens_tournament.py`, `main.py`

### mag/steiniger_lens.py

- lines: 198 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (2): `laymen_attribution_block`, `build_laymen_operations`
- public classes (0): none
- test files (0): none
- readers (1): `mag/session_dossier.py`

### mag/steward.py

- lines: 412 | parse: ok | last commit: eafda6b29 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (9): `run_steward_daily`, `ran_today`, `find_frozen_builds`, `run_steward_scope`, `run_steward_patterns`, `run_job`, `parse_steward_goal`, `fill_steward_queue`, `execute_steward_goal`
- public classes (0): none
- test files (3): `tests/test_pack_modes_steward.py`, `tests/test_steward_daily.py`, `tests/test_steward_queue_has_goal.py`
- readers (4): `mag/framework_map.py`, `mag/governor_autorun.py`, `mag/orchestrator.py`, `main.py`

### mag/story.py

- lines: 493 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (1): `build_story`
- public classes (0): none
- test files (1): `tests/test_surface_contract.py`
- readers (2): `dashboard/rest.py`, `scripts/_scrub_story2.py`

### mag/subscriptions.py

- lines: 183 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 19:36
- public functions (1): `status`
- public classes (0): none
- test files (1): `tests/test_dormant_gate_b2521.py`
- readers (1): `mag/cost_truth.py`

### mag/subswarm_health.py

- lines: 148 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 19:13
- public functions (5): `health`, `circuit`, `route_guard`, `report`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/ghost_doctor.py`

### mag/suno_zeitgeist.py

- lines: 124 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-07 17:30
- public functions (4): `score`, `cmd_file`, `cmd_best`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/mirror_control.py`

### mag/supervisor.py

- lines: 208 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (6): `context_bundle`, `slow_think`, `supervise_once`, `supervise_loop`, `stall_nudge_text`, `stall_nudge`
- public classes (0): none
- test files (0): none
- readers (4): `mag/framework_map.py`, `mag/orchestrator.py`, `mag/process_supervisor.py`, `scripts/test_stall_nudge.py`

### mag/surface_adapters.py

- lines: 214 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-13 08:37
- public functions (5): `registry`, `adapter`, `native_call`, `steer`, `status`
- public classes (0): none
- test files (1): `tests/test_surface_adapters.py`
- readers (1): `mag/governor_autorun.py`

### mag/surface_audit.py

- lines: 139 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 13:24
- public functions (2): `collect_surfaces`, `audit`
- public classes (0): none
- test files (1): `tests/test_surface_audit.py`
- readers (1): `dashboard/rest.py`

### mag/surface_instruction.py

- lines: 241 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 17:16
- public functions (7): `onboarding`, `render`, `ingest`, `trigger`, `route`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_surface_instruction.py`
- readers (2): `mag/chatgpt_bot.py`, `mag/republic_loop.py`

### mag/surface_render.py

- lines: 826 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-24 07:26
- public functions (22): `baremetal_svg`, `mesh_mermaid`, `wheels_mermaid`, `mesh_svg`, `doctrine_flow`, `vram_lattice`, `bill_metrics`, `sparkline_svg`, `mesh_dot`, `live_artifact_html`, `surface_detail`, `drilldown_html`, `republic_surfaces`, `republic_mermaid`, `republic_detail`, `republic_drilldown`, `story_mermaid`, `matthew_map_html`, `fleet_heartbeat`, `fleet_mermaid`, `render_all`, `persist`
- public classes (0): none
- test files (0): none
- readers (5): `dashboard/rest.py`, `mag/openclaw_catalog.py`, `mag/republic_loop.py`, `mag/swarm_cycle.py`, `memory/working/_w5.py`

### mag/surface_steal.py

- lines: 127 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 22:27
- public functions (5): `related_nodes`, `steal_docs`, `lingering`, `surface`, `main`
- public classes (0): none
- test files (1): `tests/test_self_steal.py`
- readers (1): `mag/self_steal.py`

### mag/surrogate.py

- lines: 386 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 11:05
- public functions (3): `decode_response`, `aggregate_responses`, `save_decoded_response`
- public classes (3): `CanonicalOperation`, `DecodedResponse`, `AggregatedDecision`
- test files (0): none
- readers (1): `mag/riddler_transport.py`

### mag/swarm_capacity.py

- lines: 153 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 17:36
- public functions (5): `host_capacity`, `cluster_capacity`, `recommend_replicas`, `free_compute_surface`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/swarm_tools.py`

### mag/swarm_control.py

- lines: 138 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 06:15
- public functions (5): `flock_targets`, `dead_drop`, `receive`, `control`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/grok_brief.py`, `mag/portal.py`, `mag/republic_loop.py`

### mag/swarm_cycle.py

- lines: 229 | parse: ok | last commit: 5dff72ac3 2026-09-28 | mtime: 2026-09-28 12:46
- public functions (2): `cycle`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/organ_map.py`, `state/backups/orphan_close_20260906/organ_map.py`

### mag/swarm_economics.py

- lines: 150 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 11:33
- public functions (5): `size`, `allocate`, `growth`, `rightsize_to_finance`, `status`
- public classes (0): none
- test files (0): none
- readers (1): `mag/swarm_tools.py`

### mag/swarm_emerge.py

- lines: 171 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 09:27
- public functions (4): `detect`, `fanout`, `surface`, `status`
- public classes (0): none
- test files (0): none
- readers (2): `mag/game_campaign.py`, `mag/invariant_ledger.py`

### mag/swarm_grok_watch.py

- lines: 162 | parse: ok | last commit: a5dd96176 2026-09-25 | mtime: 2026-09-22 08:09
- public functions (5): `classify_result`, `scan`, `run_cadence`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/governor_autorun.py`

### mag/swarm_health.py

- lines: 257 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 16:19
- public functions (6): `probe_agent`, `swarm_health`, `health_law`, `status`, `run_cadence`, `main`
- public classes (0): none
- test files (0): none
- readers (9): `mag/ecosystem_surface.py`, `mag/flex_test.py`, `mag/ghost.py`, `mag/governor_autorun.py`, `mag/law.py`, `mag/memlang.py`, `mag/resource_governor.py`, `mag/swarm_tools.py` + 1 more

### mag/swarm_local_drain.py

- lines: 248 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 12:53
- public functions (5): `key_reconcile`, `unorphan_stale`, `drain_pass`, `run_cadence`, `status`
- public classes (0): none
- test files (1): `tests/test_swarm_local_drain.py`
- readers (5): `mag/autodrain.py`, `mag/governor_autorun.py`, `mag/organ_map.py`, `scripts/container/drain_worker.py`, `state/backups/orphan_close_20260906/organ_map.py`

### mag/swarm_map.py

- lines: 172 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 10:30
- public functions (5): `frame`, `svg`, `html`, `save`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/console_render.py`, `mag/republic_loop.py`, `mag/swarm_tools.py`

### mag/swarm_quests.py

- lines: 260 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-07 01:19
- public functions (5): `os_scan`, `transform`, `build`, `verify`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/swarm_render.py

- lines: 181 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 07:51
- public functions (5): `flock_image`, `ownership_image`, `post_process`, `visual_language`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/memweave.py`, `mag/novelty_lens.py`, `mag/research_class.py`

### mag/swarm_rightsize.py

- lines: 241 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 12:47
- public functions (3): `train`, `rightsize`, `status`
- public classes (0): none
- test files (0): none
- readers (5): `mag/btw_sidechannel.py`, `mag/corpus_wave.py`, `mag/orchestrator.py`, `mag/republic_loop.py`, `mag/time_estimate.py`

### mag/swarm_run.py

- lines: 155 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 18:15
- public functions (3): `run_cycle`, `run_three`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/swarm_self.py

- lines: 294 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 07:14
- public functions (6): `flock`, `self`, `spawn_clusters`, `capacity`, `dig`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/grok_weave.py`, `mag/republic_loop.py`, `mag/swarm_map.py`

### mag/swarm_snapshot.py

- lines: 298 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-05 12:31
- public functions (7): `day_key`, `days_back`, `collect`, `render`, `digest`, `vision_read`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/swarm_surface.py

- lines: 109 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 12:51
- public functions (3): `anchor`, `route_novel`, `status`
- public classes (0): none
- test files (6): `tests/test_frontier_advisor.py`, `tests/test_frontier_council.py`, `tests/test_moonshot_engine.py`, `tests/test_shape_seed.py`, `tests/test_sovereign_handshake.py`, `tests/test_surface_instruction.py`
- readers (66): `mag/adventure_moonshot.py`, `mag/agentic_test_steal.py`, `mag/arxiv_mine.py`, `mag/autonomous_research.py`, `mag/castle_foundation.py`, `mag/chord_pipeline.py`, `mag/cleanup_steal.py`, `mag/compiler_lang.py` + 58 more

### mag/swarm_test.py

- lines: 247 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 18:07
- public functions (5): `plan`, `run`, `run_problem`, `ramp`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/skill_pipeline.py`, `memory/trash/20260810T202850Z/_tmp_ghost_swarm_test.py`

### mag/swarm_tools.py

- lines: 455 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-02 09:29
- public functions (13): `memlance`, `scratch_write`, `scratch_read`, `verkle_write`, `swarm_sense`, `pheromone_drop`, `pheromone_trail`, `pheromone_drift`, `drift_targets`, `blackboard_post`, `blackboard_read`, `spec_with_tools`, `main`
- public classes (0): none
- test files (0): none
- readers (9): `_verify_review_tier_20260925.py`, `mag/_demo_telepathy.py`, `mag/clawbot.py`, `mag/fleet_intel.py`, `mag/organ_map.py`, `mag/republic_loop.py`, `mag/swarm_worker.py`, `state/backups/orphan_close_20260906/organ_map.py` + 1 more

### mag/swarm_worker.py

- lines: 701 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 19:35
- public functions (7): `enqueue_task`, `provider_spawn_allowed`, `run_once`, `run_rightsized_once`, `collect`, `status`, `main`
- public classes (0): none
- test files (4): `tests/test_dormant_gate_b2521.py`, `tests/test_loop_death_guards.py`, `tests/test_swarm_local_drain.py`, `tests/test_swarm_quota_gate.py`
- readers (33): `configs/organs/host_resolver.yaml`, `deploy/k8s/mag-swarm-cronjob.yaml`, `mag/_relane_game_tasks.py`, `mag/_verify_queue_gate.py`, `mag/autonomous_research.py`, `mag/compute_reconcile.py`, `mag/flock_shader.py`, `mag/free_to_swarm.py` + 25 more

### mag/switchboard.py

- lines: 828 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 14:49
- public functions (13): `tier_rank`, `tier_allows`, `build_seat_registry`, `mesh`, `peers`, `find_orphans`, `reap`, `steer_drop`, `route_intent`, `status`, `format_status_text`, `self_test`, `main`
- public classes (2): `SeatProfile`, `ProcessPeer`
- test files (3): `tests/test_factory_freeze_gate.py`, `tests/test_seat_registry.py`, `tests/test_switchboard.py`
- readers (14): `configs/modules.yaml`, `dashboard/rest.py`, `mag/board_directive.py`, `mag/conductor.py`, `mag/ghost.py`, `mag/organ_map.py`, `mag/orphan_sense.py`, `mag/power.py` + 6 more

### mag/switchboard_v2.py

- lines: 925 | parse: ok | last commit: 2b84b8cce 2026-09-16 | mtime: 2026-09-16 10:29
- public functions (22): `classify`, `propose`, `grant`, `confirm`, `deny`, `mark_executing`, `complete`, `fail`, `commit_receipt`, `write_board_note`, `trail_append`, `reconcile`, `cmd_classify`, `cmd_propose`, `cmd_grant`, `cmd_confirm`, `cmd_deny`, `cmd_inbox`, `cmd_reconcile`, `cmd_write`, `cmd_expire`, `main`
- public classes (0): none
- test files (1): `tests/test_switchboard.py`
- readers (6): `mag/effect_broker.py`, `mag/harness.py`, `mag/organ_map.py`, `mag/swarm_cycle.py`, `state/backups/orphan_close_20260906/organ_map.py`, `state/backups/orphan_close_20260906/test_switchboard.py`

### mag/system_map.py

- lines: 185 | parse: ok | last commit: 36914e134 2026-08-07 | mtime: 2026-08-07 08:27
- public functions (1): `build_system_map`
- public classes (0): none
- test files (0): none
- readers (4): `dashboard/rest.py`, `mag/dashboard_plugin.py`, `mag/framework_map.py`, `main.py`

### mag/system_telemetry.py

- lines: 174 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 13:09
- public functions (7): `cpu_mem`, `gpu`, `disk`, `net`, `sense`, `crosslink`, `status`
- public classes (0): none
- test files (0): none
- readers (1): `mag/compiler_flywheel.py`

### mag/table_turn_cli.py

- lines: 12 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-16 08:50
- public functions (1): `main`
- public classes (0): none
- test files (0): none
- readers (1): `_patch_turn.py`

### mag/table_view_cache.py

- lines: 36 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-15 22:17
- public functions (3): `refresh`, `read`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `_patch_view_cache.py`, `dashboard/server.py`

### mag/tactical_framework.py

- lines: 152 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 16:58
- public functions (6): `war_map`, `strategic_objective`, `tactical_layer`, `impractical_audit`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_tactical_framework.py`
- readers (1): `mag/republic_loop.py`

### mag/tandem_key_test.py

- lines: 77 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 20:33
- public functions (1): `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/tangent.py

- lines: 346 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (6): `enqueue`, `list_tangents`, `process_one`, `process_queue`, `scan_live_for_tangents`, `cycle_hook`
- public classes (0): none
- test files (0): none
- readers (2): `dashboard/rest.py`, `main.py`

### mag/tapestry.py

- lines: 751 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (2): `build_tapestry_pack`, `write_tapestry_pack`
- public classes (0): none
- test files (1): `tests/test_tapestry_visual.py`
- readers (4): `dashboard/rest.py`, `mag/tapestry_visual.py`, `mag/verkle_compaction.py`, `main.py`

### mag/tapestry_visual.py

- lines: 189 | parse: ok | last commit: 7d4939fc9 2026-08-05 | mtime: 2026-08-06 18:28
- public functions (5): `steiniger_temperature`, `tension_band`, `knot_params_from_hash`, `visual_profile`, `lattice_chain_offset`
- public classes (0): none
- test files (1): `tests/test_tapestry_visual.py`
- readers (1): `mag/tapestry.py`

### mag/task_router.py

- lines: 281 | parse: ok | last commit: de7bb85fe 2026-08-09 | mtime: 2026-08-08 22:51
- public functions (4): `classify_task`, `route_task`, `build_parallel_swarm`, `fire_swarm`
- public classes (0): none
- test files (0): none
- readers (5): `mag/corpus_wave.py`, `mag/doctor.py`, `mag/preflight.py`, `mag/sovereign_dashboard.py`, `main.py`

### mag/tavern_chat.py

- lines: 143 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-07 21:07
- public functions (4): `start`, `say`, `tail`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/tavern_summon_guests.py`

### mag/tavern_summon_guests.py

- lines: 51 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-08 22:42
- public functions (1): `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/team_knot.py

- lines: 367 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-24 09:19
- public functions (6): `team_reality`, `stand`, `status`, `where`, `feed`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/manifest.py`

### mag/telegram_desk.py

- lines: 180 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-09 18:11
- public functions (3): `whoami`, `run`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/temperature_stack.py

- lines: 702 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 17:04
- public functions (9): `registry`, `stack_for_goal`, `timeout_for_goal`, `sampling_for_goal`, `loop_timings`, `file_pointer_knot`, `track_loop_gap`, `track_lifecycle_into_improve`, `write_state_snapshot`
- public classes (4): `TimingProfile`, `TemperatureStack`, `PointerKnot`, `TemperatureRegistry`
- test files (3): `tests/conftest.py`, `tests/test_lifecycle.py`, `tests/test_temperature_stack.py`
- readers (10): `dashboard/rest.py`, `mag/doctor.py`, `mag/env_redirect.py`, `mag/framework_map.py`, `mag/lifecycle.py`, `mag/orchestrator.py`, `mag/shared_surface.py`, `mag_launch.py` + 2 more

### mag/template_invariant.py

- lines: 227 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 17:36
- public functions (6): `extract`, `fold_template`, `instance_ledger`, `consolidate`, `consolidate_all`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/territory_solver.py

- lines: 300 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 22:15
- public functions (3): `solve`, `campaign`, `status`
- public classes (0): none
- test files (0): none
- readers (1): `mag/republic_loop.py`

### mag/test_dummy.py

- lines: 79 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 16:29
- public functions (4): `is_dummy`, `ask`, `capacity`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/scribe.py`, `mag/seed_chain.py`, `mag/self_advance.py`

### mag/test_runner.py

- lines: 192 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 23:20
- public functions (3): `run`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (4): `dashboard/rest.py`, `mag/afk_cadence.py`, `mag/skill_pipeline.py`, `mag/verify_gate.py`

### mag/tests/test_identity_schema_portability.py

- lines: 158 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-12 21:39
- public functions (3): `generate_invariant_from_schema`, `test_identity_schema_portability`, `test_schema_covers_core_constraints`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/tests/verify_identity_coupling.py

- lines: 261 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-12 21:39
- public functions (4): `generate_invariant_from_schema`, `test_identity_schema_portability`, `test_invariant_stability_under_environmental_variation`, `generate_audit_report`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/tesuji_fire.py

- lines: 433 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-07 03:22
- public functions (3): `cmd_plan`, `cmd_run`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/tesuji_map.py

- lines: 173 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-07 01:27
- public functions (4): `post`, `verify`, `render`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/grammar_transfer.py`, `mag/perturbation_battery.py`, `mag/tesuji_fire.py`

### mag/tesuji_probes.py

- lines: 475 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-05 23:24
- public functions (11): `build_grid`, `apply_parser`, `check`, `render_prompt`, `variants`, `cell_name`, `cost_estimate`, `cmd_list`, `cmd_dryrun`, `cmd_export`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/tesuji_fire.py`

### mag/tesuji_shell.py

- lines: 263 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (5): `read_shells`, `log_tesuji_shell`, `status`, `synthesize_tesuji_shell_leaf`, `latest_leaf_excerpt`
- public classes (0): none
- test files (3): `tests/test_pro_library.py`, `tests/test_pro_library_eval.py`, `tests/test_tesuji_shell.py`
- readers (18): `mag/afk_loop.py`, `mag/context_pack.py`, `mag/framework_map.py`, `mag/ghost_auto.py`, `mag/governance.py`, `mag/growth_cycle.py`, `mag/gygax_steal.py`, `mag/improve.py` + 10 more

### mag/tesuji_surface.py

- lines: 490 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 07:47
- public functions (3): `fingerprint_call`, `compare_fingerprints`, `riddler_tesuji_test`
- public classes (2): `BehavioralFingerprint`, `TesujiSignal`
- test files (0): none
- readers (3): `mag/ga4_progression.py`, `mag/novelty_lens.py`, `mag/research_class.py`

### mag/the_margin.py

- lines: 548 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-06 17:20
- public functions (10): `dump`, `parse`, `load`, `save`, `log_attempt`, `toolchain_status`, `run_kernel`, `seed`, `demo`, `main`
- public classes (4): `AppendOnlyViolation`, `Attempt`, `Node`, `Dag`
- test files (0): none
- readers (1): `mag/republic.py`

### mag/thought_bank.py

- lines: 55 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-04 22:16
- public functions (2): `bank`, `bank_response`
- public classes (0): none
- test files (0): none
- readers (1): `mag/lane_runner.py`

### mag/thought_bank_app.py

- lines: 116 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-04 23:37
- public functions (1): `harvest`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/thread_eye.py

- lines: 97 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-09 17:58
- public functions (2): `observe`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/throughput_model.py

- lines: 152 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 10:20
- public functions (5): `capacity`, `split_resources`, `ingest_estimate`, `manifest_estimate`, `moonshot_estimate`
- public classes (0): none
- test files (0): none
- readers (1): `mag/moonshot_engine.py`

### mag/time_estimate.py

- lines: 133 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 00:23
- public functions (2): `estimate`, `status`
- public classes (0): none
- test files (0): none
- readers (1): `mag/throughput_model.py`

### mag/token_chain.py

- lines: 397 | parse: ok | last commit: e4dd520e8 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (4): `parse_work_order`, `execute_work_order`, `run_token_chain`, `cmd_token_chain`
- public classes (0): none
- test files (1): `tests/test_token_chain.py`
- readers (3): `dashboard/rest.py`, `mag/orchestrator.py`, `main.py`

### mag/token_economy.py

- lines: 204 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (7): `est_tokens`, `load_chat_system_prompt`, `counterfactual_tui_chars`, `record_turn`, `load_totals`, `save_totals`, `economy_snapshot`
- public classes (0): none
- test files (1): `tests/test_surface_contract.py`
- readers (5): `dashboard/rest.py`, `mag/ask.py`, `mag/framework_map.py`, `mag/ghost_grok_dashboard.py`, `scripts/corpus_packer.py`

### mag/tokenomics.py

- lines: 431 | parse: ok | last commit: de7bb85fe 2026-08-09 | mtime: 2026-08-08 22:31
- public functions (5): `get_observer`, `tokenomics_dashboard`, `tokenomics_burn`, `tokenomics_arbitrage`, `tokenomics_waste`
- public classes (1): `TokenomicsObserver`
- test files (0): none
- readers (3): `mag/ghost.py`, `mag/preflight.py`, `mag/sovereign_dashboard.py`

### mag/tool_5ws.py

- lines: 114 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 10:23
- public functions (3): `ask`, `select`, `status`
- public classes (0): none
- test files (0): none
- readers (2): `mag/republic_loop.py`, `mag/socratic_research.py`

### mag/tool_lifecycle.py

- lines: 150 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-13 07:18
- public functions (10): `born`, `carried`, `selected`, `percolated`, `verified`, `rendered`, `branched`, `propagated`, `run_tool`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/tool_manifest.py

- lines: 216 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 19:17
- public functions (5): `scan`, `to_markdown`, `write_md`, `status`, `run_scan`
- public classes (0): none
- test files (0): none
- readers (2): `mag/agent_signature.py`, `mag/recreation_rib.py`

### mag/tool_quant.py

- lines: 133 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 10:41
- public functions (5): `scan_tools`, `quant_tool`, `quant_all`, `turtle_join`, `status`
- public classes (0): none
- test files (1): `tests/test_tool_quant.py`
- readers (3): `mag/republic_loop.py`, `mag/water_swarm.py`, `mag/wave_address.py`

### mag/tool_retire.py

- lines: 195 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 14:30
- public functions (4): `retire`, `audit`, `list_retired`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/skill_pipeline.py`, `mag/training_set.py`

### mag/tool_synthesis.py

- lines: 450 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 06:15
- public functions (10): `shader_avoid`, `evaluate_asks`, `test_subsystems`, `gpu_process_data`, `rightsize_data_extraction`, `free_activations`, `swarm_test_tools`, `warm_prefix`, `synthesize`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/republic_loop.py`

### mag/top_processes.py

- lines: 86 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 14:43
- public functions (4): `top_cpu`, `top_memory`, `top_processes`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/ghost.py`

### mag/topic_index.py

- lines: 375 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-05 22:01
- public functions (3): `build`, `query`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/topic_index_v3_tf_draft.py`

### mag/topic_index_v3_tf_draft.py

- lines: 230 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-05 21:59
- public functions (2): `build`, `query`
- public classes (0): none
- test files (0): none
- readers (1): `mag/topic_index.py`

### mag/topic_orphan.py

- lines: 120 | parse: ok | last commit: de7bb85fe 2026-08-09 | mtime: 2026-08-09 00:05
- public functions (3): `scan`, `reroute`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/governor_autorun.py`

### mag/tortoise_demo.py

- lines: 135 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-07 17:35
- public functions (6): `chain_theme`, `voice`, `kick`, `shepard`, `wav_write`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/training_events.py

- lines: 195 | parse: ok | last commit: e96fd62a4 2026-08-07 | mtime: 2026-08-06 23:35
- public functions (4): `emit`, `read_events`, `export_jsonl`, `stats`
- public classes (0): none
- test files (14): `tests/test_auto_promote.py`, `tests/test_coding_session_loop.py`, `tests/test_growth_cycle.py`, `tests/test_icon_drop_escape.py`, `tests/test_icon_drop_fold.py`, `tests/test_local_gpu_probes.py`, `tests/test_loop_death_guards.py`, `tests/test_release_registry.py` + 6 more
- readers (73): `_patch_view.py`, `mag/afk_cadence.py`, `mag/afk_loop.py`, `mag/afk_orchestrator.py`, `mag/arena_learning.py`, `mag/arena_strategies.py`, `mag/behavior_catch.py`, `mag/bernaise.py` + 65 more

### mag/training_packager.py

- lines: 308 | parse: ok | last commit: de7bb85fe 2026-08-09 | mtime: 2026-08-08 22:13
- public functions (2): `package_all`, `package_quick`
- public classes (0): none
- test files (0): none
- readers (1): `mag/lora_pipeline.py`

### mag/training_rightsize.py

- lines: 105 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 00:05
- public functions (2): `decide`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/training_set.py

- lines: 145 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 20:07
- public functions (3): `build`, `count`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/skill_pipeline.py`

### mag/trajectory_bounds.py

- lines: 93 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-31 00:01
- public functions (2): `build_bounds`, `main`
- public classes (0): none
- test files (1): `tests/test_trajectory_bounds.py`
- readers (1): `configs/modules.yaml`

### mag/trajectory_paths.py

- lines: 117 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-07 01:18
- public functions (2): `touches`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/trajectory_rib.py

- lines: 190 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-02 03:19
- public functions (2): `compile_tape`, `main`
- public classes (0): none
- test files (1): `tests/test_trajectory_rib.py`
- readers (4): `configs/modules.yaml`, `mag/organ_map.py`, `main.py`, `state/backups/orphan_close_20260906/organ_map.py`

### mag/trajectory_step.py

- lines: 172 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-05 13:07
- public functions (8): `make_row`, `append_row`, `extract`, `cmd_hook`, `cmd_verify`, `cmd_stats`, `cmd_test_reject`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/transfer_gate.py

- lines: 666 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-06 11:49
- public functions (11): `load_index`, `slice_section`, `read_card`, `derive_contract`, `gate`, `keyword_hits`, `confusion`, `f1_at`, `zero_token_audit`, `run_eval`, `main`
- public classes (3): `Contract`, `Decision`, `EvalDoc`
- test files (0): none
- readers (0): none

### mag/trigger_learn.py

- lines: 244 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 08:50
- public functions (4): `learn`, `decide`, `publish`, `status`
- public classes (0): none
- test files (0): none
- readers (2): `mag/lens_shader.py`, `mag/republic_loop.py`

### mag/tripartite.py

- lines: 281 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 07:14
- public functions (7): `hold`, `consensus`, `verdict`, `lens`, `navigate`, `triad`, `main`
- public classes (0): none
- test files (0): none
- readers (18): `configs/providers.yaml`, `mag/future_self.py`, `mag/grok_weave.py`, `mag/offerings.py`, `mag/republic_loop.py`, `mag/swarm_self.py`, `memory/seals/2026-08-26T06-17-17/configs/providers.yaml`, `memory/seals/2026-09-05T01-23-43/configs/providers.yaml` + 10 more

### mag/tripartite_boot.py

- lines: 535 | parse: ok | last commit: 1c156e2fa 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (10): `run_coordinated_boot`, `refresh_manifest_body`, `weave_route`, `weave_spawn`, `weave_terminal`, `weave_drain`, `weave_autorun_tick`, `maybe_boot_on_autorun_start`, `format_tripartite_excerpt`, `main`
- public classes (0): none
- test files (1): `tests/test_tripartite_boot.py`
- readers (7): `mag/boot.py`, `mag/context_pack.py`, `mag/framework_map.py`, `mag/governor_autorun.py`, `mag/orchestrator.py`, `mag_launch.py`, `main.py`

### mag/trust_gate.py

- lines: 257 | parse: ok | last commit: a5dd96176 2026-09-25 | mtime: 2026-09-25 20:27
- public functions (6): `novelty`, `trust`, `poison`, `gate`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (4): `_verify_review_tier_20260925.py`, `mag/republic_loop.py`, `mag/swarm_tools.py`, `mag/trust_gate_audit_check.py`

### mag/trust_gate_audit_check.py

- lines: 100 | parse: ok | last commit: a5dd96176 2026-09-25 | mtime: 2026-09-25 20:37
- public functions (2): `reset_seen`, `run`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/truth_audit.py

- lines: 176 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 12:55
- public functions (6): `ghost_sense`, `provenance_audit`, `grounding`, `gaps`, `truth_audit`, `status`
- public classes (0): none
- test files (0): none
- readers (1): `mag/republic_loop.py`

### mag/tts.py

- lines: 235 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 13:30
- public functions (3): `speak`, `speak_async`, `stop`
- public classes (0): none
- test files (0): none
- readers (5): `mag/ask.py`, `mag/gab_seat.py`, `mag/socratic.py`, `mag/voice_self.py`, `main.py`

### mag/unsloth_seat.py

- lines: 491 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 18:46
- public functions (7): `unsloth_exe`, `unsloth_status`, `unsloth_stop`, `unsloth_start`, `unsloth_chat`, `build_unsloth_payload`, `main`
- public classes (0): none
- test files (1): `tests/test_unsloth_seat.py`
- readers (3): `dashboard/rest.py`, `mag/stack.py`, `main.py`

### mag/usage_digest.py

- lines: 282 | parse: ok | last commit: 383fed94f 2026-09-27 | mtime: 2026-09-26 16:20
- public functions (3): `aggregate_day`, `commit_day`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/verkle_compaction.py`

### mag/usage_forecast.py

- lines: 239 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 08:07
- public functions (6): `estimate_ask`, `forecast`, `queue_goals`, `queue_forecast`, `calibrate`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/self_steal.py`, `main.py`

### mag/usage_monitor.py

- lines: 178 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 10:32
- public functions (5): `watch`, `check_now`, `live_poll`, `rule`, `status`
- public classes (0): none
- test files (0): none
- readers (7): `mag/emergence.py`, `mag/flock_usage_guard.py`, `mag/invariant_ledger.py`, `mag/novelty_lens.py`, `mag/resource_governor.py`, `mag/swarm_emerge.py`, `mag/trigger_learn.py`

### mag/vantage_audit.py

- lines: 195 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 16:14
- public functions (6): `surfaces`, `synthesis`, `frontier`, `iterate`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_vantage_audit.py`
- readers (1): `mag/republic_loop.py`

### mag/vast_cost.py

- lines: 335 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-30 20:51
- public functions (2): `sync`, `snapshot`
- public classes (0): none
- test files (1): `tests/test_vast_cost.py`
- readers (3): `dashboard/rest.py`, `mag/cost_truth.py`, `mag/governor_autorun.py`

### mag/vast_launcher.py

- lines: 495 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-29 20:23
- public functions (8): `estimate_training_costs`, `best_option`, `build_training_package`, `launch_training`, `credit`, `verify_pipeline_locally`, `serve_plan`, `main`
- public classes (1): `GPUOption`
- test files (0): none
- readers (5): `mag/ghost.py`, `mag/icon_drop.py`, `mag/preflight.py`, `mag/scrum.py`, `mag/vast_cost.py`

### mag/vast_train.py

- lines: 108 | parse: ok | last commit: 1e92a7012 2026-08-06 | mtime: 2026-08-06 18:28
- public functions (5): `load_config`, `validate_export`, `build_job_spec`, `estimate_cost`, `dry_run`
- public classes (0): none
- test files (1): `tests/test_vast_train_dry.py`
- readers (1): `main.py`

### mag/verb.py

- lines: 512 | parse: ok | last commit: 4ad6eb0d6 2026-09-19 | mtime: 2026-09-19 11:51
- public functions (11): `verify_trace`, `feels`, `match`, `classify`, `confident`, `sift`, `witness`, `vow`, `abide`, `meter_record`, `weekly_trigger`
- public classes (0): none
- test files (1): `tests/test_verb_stones.py`
- readers (3): `scripts/gopher_packs.py`, `scripts/vision_triage_pool.py`, `tools/verb_anchor.py`

### mag/verified_clock.py

- lines: 161 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-24 09:19
- public functions (9): `now_utc`, `now_iso`, `ts`, `age`, `chain_ts`, `verify`, `anchor`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `mag/manifest.py`, `mag/team_knot.py`

### mag/verify_gate.py

- lines: 233 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 06:51
- public functions (3): `gate`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/verify_succession_contract.py

- lines: 149 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-12 22:23
- public functions (6): `verify_yaml_syntax`, `verify_components_exist`, `verify_tsvf_properties`, `verify_integration_points`, `verify_deterministic_hashes`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `configs/succession_contract.yaml`

### mag/verkle_artifact.py

- lines: 111 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-01 20:46
- public functions (2): `verify_leaf`, `build_agent_knot`
- public classes (0): none
- test files (1): `tests/test_verkle_artifact.py`
- readers (1): `dashboard/rest.py`

### mag/verkle_audit.py

- lines: 439 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-10 16:39
- public functions (4): `verkle_gaps`, `reconcile_tickets`, `synth_all_residuals`, `run_audit`
- public classes (0): none
- test files (1): `tests/test_verkle_audit.py`
- readers (7): `mag/framework_map.py`, `mag/ghost.py`, `mag/governor_autorun.py`, `mag/loop_audit.py`, `mag/ponytail_audit.py`, `main.py`, `memory/runs/union_audit/_write_jsonl.py`

### mag/verkle_bus.py

- lines: 292 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 08:06
- public functions (9): `connect_redis`, `close_redis`, `is_connected`, `publish`, `publish_sync`, `subscribe`, `fold_event_to_verkle`, `scrum_checkpoint`, `bus_status`
- public classes (0): none
- test files (1): `tests/test_bard.py`
- readers (18): `mag/bard.py`, `mag/constitutional_critique.py`, `mag/context_checkpoint.py`, `mag/copilot_bridge.py`, `mag/cost_enforcer.py`, `mag/depin.py`, `mag/doctor_agent.py`, `mag/fact_bus.py` + 10 more

### mag/verkle_compaction.py

- lines: 396 | parse: ok | last commit: e73b60c54 2026-09-27 | mtime: 2026-09-27 01:01
- public functions (5): `is_fold_candidate`, `plan`, `apply`, `prove_archived_leaf`, `verify_archive_anchor`
- public classes (0): none
- test files (1): `tests/test_verkle_compaction.py`
- readers (0): none

### mag/verkle_knot.py

- lines: 920 | parse: ok | last commit: 7b8617d78 2026-09-27 | mtime: 2026-09-27 13:35
- public functions (10): `session_pointer_v2`, `verkle_lock`, `knot_filename`, `build_leaf_from_dossier`, `prove`, `prove_latest`, `repair_tip_if_consistent`, `append_verkle_knot`, `consolidate_chain_one_leaf_per_session`, `evolution_summary`
- public classes (1): `VerkleProof`
- test files (6): `tests/test_chain_byte_exact_io.py`, `tests/test_chat_source_agent_workday.py`, `tests/test_loop_death_guards.py`, `tests/test_verkle_audit.py`, `tests/test_verkle_compaction.py`, `tests/test_verkle_lock.py`
- readers (88): `configs/modules.yaml`, `mag/_flag_dangling_20260925.py`, `mag/_flag_dangling_264d0ba3.py`, `mag/afk_loop.py`, `mag/agent_knot.py`, `mag/agent_os_loop.py`, `mag/breakthrough_loop.py`, `mag/castle_foundation.py` + 80 more

### mag/verkle_lance.py

- lines: 456 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 05:55
- public functions (12): `index`, `temporal`, `trace`, `link`, `verify`, `lance`, `shapes`, `rib_builder`, `puppet_trigger`, `tie_in`, `self_check`, `main`
- public classes (0): none
- test files (0): none
- readers (9): `_afk_full_blast.py`, `mag/ask_router.py`, `mag/effect_broker.py`, `mag/game_campaign.py`, `mag/novelty_lens.py`, `mag/openclaw_catalog.py`, `mag/route_trace.py`, `mag/spine_exercise.py` + 1 more

### mag/verkle_render.py

- lines: 116 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-15 06:55
- public functions (5): `tip`, `knot_snapshot`, `to_js`, `js_file`, `status`
- public classes (0): none
- test files (0): none
- readers (2): `experiments/verkle_knot_standing_wave.yaml`, `scripts/_gen_game_verkle.py`

### mag/verkle_rib.py

- lines: 123 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-09 23:59
- public functions (4): `rib_points`, `export`, `summary`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/vertical_meter.py

- lines: 111 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-07 09:20
- public functions (2): `measure`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/vessel_swarm.py

- lines: 221 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 16:58
- public functions (8): `sonar`, `launch_swarm`, `naval_map`, `game_map`, `status`, `chain_of_command`, `fleet_tactics`, `main`
- public classes (0): none
- test files (1): `tests/test_vessel_swarm.py`
- readers (1): `mag/republic_loop.py`

### mag/virtual_desk_loop.py

- lines: 679 | parse: ok | last commit: 771ebac19 2026-08-05 | mtime: 2026-08-06 18:28
- public functions (9): `load_config`, `read_state`, `write_state`, `load_brief`, `run_once`, `plant_status`, `start_loop`, `stop_loop`, `import_export`
- public classes (0): none
- test files (1): `tests/test_virtual_desk_loop.py`
- readers (1): `main.py`

### mag/vision.py

- lines: 124 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-25 12:35
- public functions (2): `describe`, `main`
- public classes (0): none
- test files (0): none
- readers (6): `mag/_demo_eyes_receipt.py`, `mag/autoglm.py`, `mag/mcp_server.py`, `mag/offerings.py`, `scripts/vision_endowment.py`, `tools/__init__.py`

### mag/visual_pack.py

- lines: 608 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 11:46
- public functions (3): `resolve_session_id`, `build_visual_pack`, `write_visual_pack`
- public classes (0): none
- test files (0): none
- readers (4): `dashboard/rest.py`, `mag/biography.py`, `mag/brief_local.py`, `main.py`

### mag/voice_dictate.py

- lines: 190 | parse: ok | last commit: de7bb85fe 2026-08-09 | mtime: 2026-08-09 00:13
- public functions (3): `cleanup`, `cleanup_for_terminal`, `handle_dictate`
- public classes (0): none
- test files (1): `tests/test_voice_dictate.py`
- readers (2): `mag/cast_server.py`, `mag/voice_turn.py`

### mag/voice_dig_board.py

- lines: 466 | parse: ok | last commit: e96fd62a4 2026-08-07 | mtime: 2026-08-06 21:36
- public functions (9): `note_voice_turn`, `note_scout_ready`, `render_board_md`, `board_context_for_local`, `clear_board`, `clear_board_if_sludge`, `canvas_snapshot`, `refresh_board`, `handle_dig`
- public classes (0): none
- test files (1): `tests/test_voice_shadow.py`
- readers (5): `dashboard/rest.py`, `mag/diary_node.py`, `mag/voice_handoff.py`, `mag/voice_shadow.py`, `mag/voice_turn.py`

### mag/voice_handoff.py

- lines: 507 | parse: ok | last commit: e96fd62a4 2026-08-07 | mtime: 2026-08-06 21:30
- public functions (11): `wants_handoff`, `wants_blocking_smart`, `list_handoffs`, `get_handoff`, `ready_handoff_for_session`, `mark_spoken`, `file_handoff`, `handoff_spoken_reply`, `try_handoff_reply`, `inject_ready_result`, `handle_handoff`
- public classes (0): none
- test files (1): `tests/test_voice_turn.py`
- readers (2): `dashboard/rest.py`, `mag/voice_turn.py`

### mag/voice_lanes.py

- lines: 236 | parse: ok | last commit: e96fd62a4 2026-08-07 | mtime: 2026-08-06 21:38
- public functions (6): `normalize_lane`, `lane_spec`, `session_id_for_lane`, `infer_lane`, `instant_harness_reply`, `lane_public`
- public classes (0): none
- test files (0): none
- readers (1): `mag/voice_turn.py`

### mag/voice_pipeline.py

- lines: 335 | parse: ok | last commit: e96fd62a4 2026-08-07 | mtime: 2026-08-06 20:10
- public functions (1): `run_voice_pipeline`
- public classes (0): none
- test files (1): `tests/test_voice_pipeline.py`
- readers (1): `mag/voice_scratch.py`

### mag/voice_scratch.py

- lines: 412 | parse: ok | last commit: e96fd62a4 2026-08-07 | mtime: 2026-08-06 20:10
- public functions (6): `load_pad`, `save_pad`, `clear_pad`, `append_draft`, `commit_and_wake`, `handle_scratch`
- public classes (0): none
- test files (1): `tests/test_voice_scratch.py`
- readers (2): `dashboard/rest.py`, `mag/cast_server.py`

### mag/voice_self.py

- lines: 99 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 06:24
- public functions (3): `speak_state`, `voice_loop`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/republic_loop.py`

### mag/voice_shadow.py

- lines: 241 | parse: ok | last commit: e96fd62a4 2026-08-07 | mtime: 2026-08-06 20:47
- public functions (6): `load_shadow`, `save_shadow`, `shadow_context_for_local`, `start_shadow_scout`, `shadow_status`, `handle_shadow`
- public classes (0): none
- test files (1): `tests/test_voice_shadow.py`
- readers (2): `dashboard/rest.py`, `mag/voice_turn.py`

### mag/voice_skills.py

- lines: 74 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-29 18:16
- public functions (3): `match_voice_skills`, `is_play_intent`, `is_in_game_action`
- public classes (0): none
- test files (0): none
- readers (1): `mag/voice_turn.py`

### mag/voice_stt.py

- lines: 177 | parse: ok | last commit: e96fd62a4 2026-08-07 | mtime: 2026-08-06 20:55
- public functions (5): `whisper_available`, `stt_status`, `transcribe_file`, `save_upload`, `handle_stt`
- public classes (0): none
- test files (0): none
- readers (6): `dashboard/rest.py`, `mag/cast_server.py`, `mag/gab_seat.py`, `mag/novelty_lens.py`, `mag/research_class.py`, `mag/voice_self.py`

### mag/voice_tasks.py

- lines: 263 | parse: ok | last commit: e96fd62a4 2026-08-07 | mtime: 2026-08-06 20:49
- public functions (5): `is_product_need`, `file_task`, `list_tasks`, `handle_voice_task`, `product_need_reply`
- public classes (0): none
- test files (0): none
- readers (3): `dashboard/rest.py`, `mag/voice_handoff.py`, `mag/voice_turn.py`

### mag/voice_trigger.py

- lines: 171 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-14 20:30
- public functions (3): `parse`, `dispatch`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/novelty_lens.py`, `mag/research_class.py`, `mag/wearable_swarm.py`

### mag/voice_turn.py

- lines: 1777 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-29 18:16
- public functions (5): `load_session`, `save_session`, `clear_session`, `soft_stt_fix`, `handle_voice_turn`
- public classes (0): none
- test files (2): `tests/test_voice_scratch.py`, `tests/test_voice_turn.py`
- readers (9): `dashboard/rest.py`, `mag/cast_server.py`, `mag/diary_node.py`, `mag/gab_seat.py`, `mag/voice_dig_board.py`, `mag/voice_scratch.py`, `memory/working/_patch_place_remember.py`, `memory/working/_patch_table.py` + 1 more

### mag/volume_fidelity.py

- lines: 562 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-06 18:35
- public functions (12): `fnv1a32`, `mulberry32`, `solve_field`, `carve`, `structure_stats`, `spearman`, `load_volume`, `test_null_model`, `test_neighbor_fidelity`, `test_stability`, `test_semantic`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/vram_hologram.py

- lines: 204 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 16:11
- public functions (6): `quantization_curve`, `wave_oscillation`, `right_size`, `collective_reality`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_vram_hologram.py`
- readers (0): none

### mag/vram_memory.py

- lines: 137 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-14 09:36
- public functions (4): `hot_region`, `warm_in_vram`, `cook`, `main`
- public classes (0): none
- test files (0): none
- readers (7): `mag/republic_loop.py`, `mag/swarm_self.py`, `mag/tripartite.py`, `memory/working/_nest.py`, `memory/working/_patch_freeze_organs.py`, `memory/working/_prove_freeze.py`, `scripts/model_census.py`

### mag/vscode_feed.py

- lines: 221 | parse: ok | last commit: 60e18c524 2026-08-08 | mtime: 2026-08-08 07:42
- public functions (3): `capture`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (2): `dashboard/rest.py`, `main.py`

### mag/vscode_seat.py

- lines: 178 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-16 10:49
- public functions (5): `task_spec`, `generate`, `self_fix_swarm`, `main`, `cadence_generate`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/warmed_cold_replay.py

- lines: 497 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-07 09:39
- public functions (11): `extract_target`, `build_genome_slab`, `build_record_slab`, `compose`, `chat`, `aligned_span`, `metrics`, `prefill_ms_per_tok`, `run`, `dry_run`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/warning_monitor.py

- lines: 205 | parse: ok | last commit: 60e18c524 2026-08-08 | mtime: 2026-08-08 11:41
- public functions (5): `extract_warnings`, `run`, `recent_warnings`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_warning_monitor.py`
- readers (4): `dashboard/rest.py`, `deploy/k8s/mag-cronjob.yaml`, `mag/governor_autorun.py`, `main.py`

### mag/water_computer.py

- lines: 880 | parse: ok | last commit: 6c43c15d2 2026-09-27 | mtime: 2026-09-27 23:32
- public functions (33): `is_module`, `seed`, `heights`, `valves`, `graph_spec`, `seed_graph`, `default_graph_spec`, `proof_payload`, `anchor_proof`, `graph_glass`, `cheated`, `scorched`, `phase`, `steam_n`, `rain_n`, `ice_n`, `charge_n`, `mass`, `won`, `sight_glass`, `glance`, `to_gas`, `fireball`, `freeze`, `gravity_tick`, `set_valve`, `pour_bucket`, `hire_tick`, `handle`, `after`, `extra_legal`, `extra_paths`, `main`
- public classes (0): none
- test files (2): `tests/test_water_computer.py`, `tests/test_water_graph_campaign.py`
- readers (6): `mag/game_campaign.py`, `mag/organ_map.py`, `mag/spine_exercise.py`, `mag/swarm_cycle.py`, `mag/water_graph.py`, `state/backups/orphan_close_20260906/organ_map.py`

### mag/water_graph.py

- lines: 274 | parse: ok | last commit: a6275084d 2026-09-27 | mtime: 2026-09-27 21:26
- public functions (1): `from_spec`
- public classes (3): `Node`, `Pipe`, `WaterGraph`
- test files (3): `tests/test_water_graph.py`, `tests/test_water_graph_campaign.py`, `tests/test_water_graph_starvation.py`
- readers (1): `mag/water_computer.py`

### mag/water_swarm.py

- lines: 128 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 10:41
- public functions (4): `invariant_lattice`, `water_doctrine`, `flow`, `status`
- public classes (0): none
- test files (1): `tests/test_water_swarm.py`
- readers (3): `mag/organ_map.py`, `mag/republic_loop.py`, `state/backups/orphan_close_20260906/organ_map.py`

### mag/wave.py

- lines: 655 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-16 10:29
- public functions (4): `room_mermaid`, `room_svg`, `snapshot`, `snapshot_fast`
- public classes (0): none
- test files (0): none
- readers (15): `_patch_turn.py`, `_patch_wave_fast.py`, `backend/server.py`, `dashboard/rest.py`, `mag/chord_circuit.py`, `mag/wave_cache.py`, `memory/working/_hairline.py`, `memory/working/_patch_freeze_organs.py` + 7 more

### mag/wave_address.py

- lines: 178 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-13 04:32
- public functions (7): `register`, `reach`, `discover`, `surface`, `register_surface`, `run_cadence`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/governor_autorun.py`

### mag/wave_cache.py

- lines: 20 | parse: ok | last commit: 799ddb6fe 2026-08-19 | mtime: 2026-08-15 22:22
- public functions (2): `refresh`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `_patch_wave_fast.py`

### mag/wave_fire.py

- lines: 153 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-13 12:36
- public functions (5): `load_pack`, `brief`, `fire_lane`, `run`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `memory/runs/fleet_round/burn_chain.py`

### mag/wearable_swarm.py

- lines: 207 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 08:58
- public functions (6): `skills`, `parse_command`, `command`, `surface`, `skills_rib`, `status`
- public classes (0): none
- test files (0): none
- readers (4): `mag/cast_server.py`, `mag/invariant_ledger.py`, `mag/novelty_lens.py`, `mag/research_class.py`

### mag/whale_patrol.py

- lines: 319 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-07 21:16
- public functions (20): `decode_snowflake`, `post_id`, `now_iso`, `age_hours`, `parse_counts`, `load_rows`, `append_row`, `room_log`, `latest_by_post`, `cmd_track`, `cmd_reply`, `cmd_observe`, `cmd_census`, `cmd_ping`, `watched_handles`, `cmd_watchlist`, `feed`, `cmd_feed`, `feed_items`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/whisper_image.py

- lines: 288 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 11:46
- public functions (7): `encode_image`, `decode_image`, `campaign_carrier`, `encode_whisper`, `decode_whisper_image`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_sense_mcp.py`
- readers (6): `mag/archetype_image.py`, `mag/dogfood_audit.py`, `mag/schema_registry.py`, `mag/self_steal.py`, `mag/shader_bus.py`, `tools/sense_tools.py`

### mag/whisper_route.py

- lines: 138 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 14:15
- public functions (7): `front_research`, `riddler`, `set_invariant`, `dissect`, `run`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/win_powershell.py

- lines: 43 | parse: ok | last commit: 6d417abd5 2026-09-26 | mtime: 2026-09-26 16:55
- public functions (1): `powershell_exe`
- public classes (0): none
- test files (0): none
- readers (3): `mag/health.py`, `mag/lifecycle.py`, `mag/window_audit.py`

### mag/window_audit.py

- lines: 112 | parse: ok | last commit: 6d417abd5 2026-09-26 | mtime: 2026-09-26 17:25
- public functions (3): `poll_once`, `run_once`, `main`
- public classes (0): none
- test files (0): none
- readers (4): `mag/ghost.py`, `mag/guard_registry.py`, `mag/win_powershell.py`, `stop_window_popups.cmd`

### mag/window_bus.py

- lines: 257 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 14:28
- public functions (8): `bus_segment`, `price_window_bus`, `member_view`, `curate`, `price_dynamic_invariant`, `fold_dynamic_invariant`, `accept_knot`, `main`
- public classes (0): none
- test files (0): none
- readers (1): `mag/matrix_router.py`

### mag/window_hop.py

- lines: 117 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 14:28
- public functions (2): `plan`, `main`
- public classes (1): `Seg`
- test files (0): none
- readers (0): none

### mag/window_throttle.py

- lines: 378 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-04 11:44
- public functions (8): `now_iso`, `window_path`, `claim_is_active`, `claim`, `release`, `status`, `sweep`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/wireshark_steal.py

- lines: 142 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 16:11
- public functions (4): `route_research`, `vision`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_wireshark_steal.py`
- readers (0): none

### mag/witness_snapshot.py

- lines: 67 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-08 21:06
- public functions (3): `merkle_root`, `build`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/word_skill_map.py

- lines: 237 | parse: ok | last commit: de29d49ea 2026-08-09 | mtime: 2026-08-09 14:55
- public functions (5): `learn`, `word_skills`, `map_to_group`, `steer_collab`, `main`
- public classes (0): none
- test files (0): none
- readers (4): `mag/bernaise.py`, `mag/ghost_whisper.py`, `mag/prospect_sim.py`, `mag/skill_pipeline.py`

### mag/work_contract.py

- lines: 111 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-08-26 08:06
- public functions (3): `brief`, `envelope`, `result`
- public classes (0): none
- test files (0): none
- readers (7): `mag/_verify_sharp_edge.py`, `mag/fuel_feed.py`, `mag/glm_flash.py`, `mag/invariant.py`, `mag/ox_resident.py`, `mag/rib_cache.py`, `memory/runs/_probe_zai_cache.py`

### mag/work_loop.py

- lines: 334 | parse: ok | last commit: 790145ab1 2026-09-26 | mtime: 2026-09-26 01:03
- public functions (4): `sense`, `run_once`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_loop_death_guards.py`
- readers (3): `mag/chord_circuit.py`, `mag/governor_autorun.py`, `mag/manifest.py`

### mag/work_register.py

- lines: 180 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-25 11:17
- public functions (5): `record`, `recall`, `backfill`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (6): `mag/_consensus_witness.py`, `mag/_verify_sharp_edge.py`, `mag/lab_episode.py`, `mag/mem_lands.py`, `mag/north_star.py`, `mag/seat_dispatch.py`

### mag/work_tiers.py

- lines: 105 | parse: ok | last commit: de7bb85fe 2026-08-09 | mtime: 2026-08-08 23:20
- public functions (3): `next_for`, `describe`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/workspace_api.py

- lines: 101 | parse: ok | last commit: eb07ad62e 2026-08-04 | mtime: 2026-08-04 18:48
- public functions (3): `list_tree`, `read_file`, `write_file`
- public classes (0): none
- test files (1): `tests/test_three_track.py`
- readers (1): `dashboard/rest.py`

### mag/world_rib.py

- lines: 172 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 09:27
- public functions (5): `compile`, `to_obj`, `world_from_rib`, `rederive`, `status`
- public classes (0): none
- test files (1): `tests/test_wow_manifest.py`
- readers (10): `mag/compiler_lang.py`, `mag/emergence.py`, `mag/game_play.py`, `mag/game_ramp.py`, `mag/game_world_render.py`, `mag/invariant_ledger.py`, `mag/novelty_lens.py`, `mag/primer.py` + 2 more

### mag/worldline_dungeon.py

- lines: 551 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-07 08:31
- public functions (13): `read_tape`, `read_chain`, `read_probe`, `read_seeds`, `read_tesuji`, `read_curator`, `e`, `stamp`, `chamber_ok`, `chamber_dead`, `build_state`, `render_page`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/worldline_seed.py

- lines: 1072 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-07 13:20
- public functions (4): `emit`, `verify`, `load`, `main`
- public classes (0): none
- test files (0): none
- readers (4): `mag/_verify_verkle_gate_spec.py`, `mag/knot_at_close.py`, `mag/seed_registry.py`, `mag/worldline_dungeon.py`

### mag/wow_bones.py

- lines: 370 | parse: ok | last commit: 5305a99b1 2026-09-16 | mtime: 2026-09-16 13:15
- public functions (8): `parse_opcodes`, `parse_enums`, `extract`, `load_fixture`, `laws`, `status`, `FX_PRESENT`, `main`
- public classes (3): `Dispatch`, `Instance`, `Stream`
- test files (4): `tests/test_bones_adapter.py`, `tests/test_wow_bones.py`, `tests/test_wow_bones_session.py`, `tests/test_wow_world.py`
- readers (5): `mag/bones_adapter.py`, `mag/game_ramp.py`, `mag/wow_bones_session.py`, `mag/wow_world.py`, `scripts/walk_world.py`

### mag/wow_bones_session.py

- lines: 271 | parse: ok | last commit: 5305a99b1 2026-09-16 | mtime: 2026-09-16 13:14
- public functions (3): `canonical`, `session_id_for`, `main`
- public classes (1): `BonesSession`
- test files (3): `tests/test_bones_adapter.py`, `tests/test_wow_bones_session.py`, `tests/test_wow_world.py`
- readers (5): `mag/bones_adapter.py`, `mag/wow_bones.py`, `mag/wow_world.py`, `scripts/build_deck.py`, `scripts/walk_world.py`

### mag/wow_family.py

- lines: 324 | parse: ok | last commit: 30e5ec7e2 2026-09-15 | mtime: 2026-09-15 21:19
- public functions (7): `parse_source`, `versioned_contracts`, `doctrine`, `lineage`, `delta`, `status`, `main`
- public classes (0): none
- test files (1): `tests/test_wow_family.py`
- readers (1): `mag/research_fanout.py`

### mag/wow_manifest.py

- lines: 114 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-12 10:20
- public functions (1): `manifest`
- public classes (0): none
- test files (1): `tests/test_wow_manifest.py`
- readers (1): `mag/republic_loop.py`

### mag/wow_player.py

- lines: 433 | parse: ok | last commit: 75c030d29 2026-09-16 | mtime: 2026-09-16 16:38
- public functions (4): `canonical`, `player_id_for`, `verify_file`, `main`
- public classes (2): `PlayerLedgerError`, `PlayerFile`
- test files (1): `tests/test_wow_player.py`
- readers (1): `scripts/walk_world.py`

### mag/wow_steal.py

- lines: 388 | parse: ok | last commit: 30e5ec7e2 2026-09-15 | mtime: 2026-09-15 21:07
- public functions (5): `self_map`, `verify`, `receipt`, `status`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/research_fanout.py`, `mag/wow_bones.py`, `mag/wow_family.py`

### mag/wow_world.py

- lines: 372 | parse: ok | last commit: 75c030d29 2026-09-16 | mtime: 2026-09-16 16:56
- public functions (4): `world_digest`, `world_session_id`, `room_fixture`, `main`
- public classes (1): `WorldSession`
- test files (1): `tests/test_wow_world.py`
- readers (2): `mag/game_ramp.py`, `scripts/walk_world.py`

### mag/write_strip.py

- lines: 164 | parse: ok | last commit: a5dd96176 2026-09-25 | mtime: 2026-09-25 21:02
- public functions (6): `normalize_tool_name`, `classify_tool`, `is_write_tool`, `is_dual_use_tool`, `strip_write_tools`, `read_only_from_env`
- public classes (0): none
- test files (1): `tests/test_write_strip.py`
- readers (2): `mag/agent_cli.py`, `mag/orchestrator.py`

### mag/x_auth_once.py

- lines: 29 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-05 19:27
- public functions (1): `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/x_chat_mine.py

- lines: 94 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 11:28
- public functions (2): `mine`, `status`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/x_control_surface.py

- lines: 677 | parse: ok | last commit: cb26bc2cd 2026-08-25 | mtime: 2026-08-23 23:20
- public functions (14): `x_api_configured`, `grok_api_configured`, `any_x_surface_configured`, `fetch_user_timeline`, `fetch_status`, `grok_search_nachoquixotic`, `is_strike_chord_prompt`, `extract_prompt_metadata`, `ingest_prompts_from_posts`, `check_mentions`, `parse_x_command`, `post_to_x`, `x_surface_cycle`, `x_surface_status`
- public classes (0): none
- test files (0): none
- readers (4): `mag/ghost.py`, `mag/task_router.py`, `memory/trash/20260810T202850Z/_tmp_ingest_nacho.py`, `memory/trash/20260810T202850Z/_tmp_x_surface_test.py`

### mag/x_interceptor.py

- lines: 205 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-06 13:39
- public functions (3): `deepfire`, `scan`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/x_oauth.py

- lines: 550 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-05 23:51
- public functions (13): `start`, `complete`, `refresh`, `upload_media`, `post`, `edit`, `delete`, `me`, `follow`, `recent_posts`, `dm`, `like`, `main`
- public classes (0): none
- test files (0): none
- readers (3): `mag/x_auth_once.py`, `mag/x_control_surface.py`, `scripts/x_auth_loop.py`

### mag/x_posts_mine.py

- lines: 123 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-11 12:02
- public functions (2): `mine`, `status`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/x_reply_radar.py

- lines: 104 | parse: ok | last commit: d575bc168 2026-09-14 | mtime: 2026-09-11 08:07
- public functions (3): `emit`, `run`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

### mag/x_surface.py

- lines: 131 | parse: ok | last commit: 052732ebf 2026-08-14 | mtime: 2026-08-10 19:13
- public functions (5): `harvest`, `draft`, `queue`, `approve`, `main`
- public classes (0): none
- test files (0): none
- readers (0): none

