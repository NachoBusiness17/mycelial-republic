# f-15 - test-health census of tests/ (2026-09-28)

Item f-15. Every number below came from a command run during this ask on 2026-09-28;
instruments and moments are named per the census denominator law (B2-216).

## Instruments (exact commands, this session)

1. Filesystem + git inventory: `git ls-files tests` vs `os.walk(tests)` (`.py` only, `__pycache__` excluded)
2. Collect pass (counts per file): `.venv\Scripts\python.exe -m pytest --collect-only -q -p no:cacheprovider` -> `2410 tests collected in 9.31s`, moment 2026-09-28 ~17:55 EDT
3. Execution pass (pass/fail per file): `.venv\Scripts\python.exe -m pytest tests -v --tb=no -p no:cacheprovider` -> `10 failed, 2388 passed, 12 skipped, 4 warnings in 3135.22s (0:52:15)`, moment 2026-09-28 18:05-18:57 EDT, raw log held at `%TEMP%\f15_run.log` (2452 lines, 213,617 bytes)
4. Log-evidence sweep: all 57 files in `logs/*.log` read for the string `pytest` (2 hits, below)

## Headline

| metric | value | source |
|---|---|---|
| .py files on disk under tests/ | 373 | os.walk |
| git-tracked under tests/ | 369 | git ls-files |
| untracked .py files | 4 | walk minus ls-files |
| tracked but missing on disk | 0 | set diff |
| files carrying pytest items | 368 | collect-only parse |
| files collecting zero items | 5 | collect-only parse |
| tests collected (whole suite) | 2,410 | collect summary + node parse agree exactly |
| passed (executed 2026-09-28) | 2,388 | run summary |
| failed | 10 | run summary |
| skipped | 12 | run summary |
| denominators | 2388+10+12 = 2,410 = collected | cross-check |
| suite wall time | 3,135.22 s (52:15) | run summary |

## The 10 failures (full node IDs from the verbose run log)

- `tests/test_loop_death_guards.py::test_loop_death_guard_fires_on_raise[afk_routing]`
- `tests/test_organ_map.py::test_map_and_elder_surface_callable_orphans`
- `tests/test_organ_map.py::test_map_separates_callable_from_live`
- `tests/test_organ_map.py::test_operational_graph_has_explicit_cycles_and_unverified_edges`
- `tests/test_ponytail_audit.py::test_run_audit_returns_schema`
- `tests/test_shared_surface_events.py::test_real_links_jsonl_matches_the_registered_baseline`
- `tests/test_skill_seat.py::test_ponytail_gate`
- `tests/test_swarm_quota_gate.py::test_rightsized_local_still_drains_when_remote_spent`
- `tests/test_swarm_quota_gate.py::test_run_once_skips_and_leaves_queued_when_spent`
- `tests/test_write_strip.py::test_flag_wired_through_cli_parsers`

Failure cluster: organ_map 3, swarm_quota_gate 2, loop_death_guards 1, ponytail_audit 1,
shared_surface_events 1, skill_seat 1, write_strip 1 (7 files, 10 items).
Skips (12, all reason-tagged): test_agent_arena.py 4 + test_arena_learning.py 2 +
test_desk_dialogue.py 1 = `python-chess not installed`; test_ractor_falsifier_stubs.py 5 =
`mag.ractor.engine not built yet (spec section 6 step 2)`.

## When was the last run - log evidence

Swept all 57 `logs/*.log` for `pytest`: only 2 files contain the string at all.

1. `logs/census_patrol.log` (the only pytest-adjacent scheduled instrument) is COLLECT-only,
   never executes tests. Its whole history: 2026-09-26 11:34 exit 0 (1,910 / 303 files),
   2026-09-27 08:30 exit 0 (2,303 / 352), 2026-09-28 17:20:35 exit 1 COLLECT-DRIFT
   (`pytest holds 2410 vs carrier claim 2303 (delta +107, bar 20)`, lines 34-48).
2. `logs/dashboard_sv.err.log` holds 6 lines of Mag-seat `run_shell` commands that invoke pytest
   on exactly 3 files (tests/test_tool_dispatch_shape.py, tests/test_t1_steering.py,
   tests/test_prompt_steering.py); outcomes are not in that log.
3. `.pytest_cache/v/cache/lastfailed` (mtime 2026-08-05 20:29) + nodeids (2026-08-06 11:29):
   12 entries / 8 files, but paths reference the pre-restructure `memory/working/` tree -
   stale, kept as historical footnote only, not current evidence.

**Conclusion:** no per-file historical execution log exists anywhere in this estate. The daily
patrol collects and never executes; nothing else logs pytest outcomes. Therefore the
last-run evidence for every one of the 368 test-bearing files IS the 2026-09-28 full-suite run
executed for this census (2,388/10/12 above). The 5 zero-collect files were not executed by
pytest and have no run evidence: tests/conftest.py (fixtures), tests/hook_pairing.py (shared
pre-push helper, B2-363), tests/selftests/ack_reaper_selftest.py (outside the pytest candidate
namespace per B2-389; surfaced via tests/test_ack_reaper.py), tests/selftests/lesson_gate_selftest.py
(same selftest pattern), tests/test_selffeed_integration.py (2,995 bytes, 0 `def test_` -
script-style file, the patrol's named `instrument gap: 1 zero-collect candidate`).

**Mute-channel finding:** `logs/census_patrol.log` lines 8 and 48 both say `ALERT appended to
memory/attention.md`, but `memory/attention.md` contains 0 occurrences of census / patrol /
collect / drift / 2303 / 2410 (case-insensitive grep this session). Same mute pattern the
w3 theater audit banked as F6/F7.

## Drift vs the AGENTS.md carrier claim

Carrier (AGENTS.md Tests bullet): 2,303 collected / 352 files, 2026-09-27 census. Fresh collect
this session: 2,410 / 368 item-bearing files (+107 / +16). The patrol independently flagged the
same +107 delta at 2026-09-28 17:20:35 and exited 1; its fix line assigns the carrier refresh to
the operator (not done here - AGENTS.md is not a file this item may touch). Per B2-216 the two
counts are different denominators at different moments; the delta is named landings: the patrol
lists 5 files grown on 2026-09-28 (test_silentpass_batch2, test_demote_candidates,
test_router_comms_boost, test_stealth_driver_effort_dial, test_auto_promote).

## Per-file census (all 373 .py files)

tests = items collected 2026-09-28; pass/fail/skip = executed 2026-09-28 run; git = tracked in git;
last run = the 2026-09-28 census run, or `none found` (see evidence section).

| file | tests | pass | fail | skip | git | last run |
|---|---:|---:|---:|---:|---|---|
| tests/conftest.py | 0 | 0 | 0 | 0 | yes | none found |
| tests/hook_pairing.py | 0 | 0 | 0 | 0 | yes | none found |
| tests/selftests/ack_reaper_selftest.py | 0 | 0 | 0 | 0 | yes | none found |
| tests/selftests/lesson_gate_selftest.py | 0 | 0 | 0 | 0 | yes | none found |
| tests/test_abundance_rogue.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_ack_reaper.py | 22 | 22 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_adventure_moonshot.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_agent_arena.py | 5 | 1 | 0 | 4 | yes | 2026-09-28 (this census run) |
| tests/test_agent_corpus.py | 6 | 6 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_agent_desk.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_agent_desk_commit.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_agent_live.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_agent_repack.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_agent_state.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_agent_state_layers.py | 1 | 1 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_all_seat_interaction.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_api_gateway_status_route.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_arena_adapter.py | 8 | 8 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_arena_learning.py | 6 | 4 | 0 | 2 | yes | 2026-09-28 (this census run) |
| tests/test_arrival.py | 6 | 6 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_attention_ranker.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_auto_promote.py | 1 | 1 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_autorun_v1.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_b285_enum_resolution_pins.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_bard.py | 16 | 16 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_bare_numpy.py | 7 | 7 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_base_drift.py | 6 | 6 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_battery_rerun.py | 6 | 6 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_behavioral_awareness.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_bind_policy.py | 7 | 7 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_blade_plan.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_blade_templates.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_bonds_conflict_scan.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_bones_adapter.py | 17 | 17 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_brain.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_build_audit.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_build_lane_tripwire.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_cache_identity.py | 10 | 10 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_campaign.py | 27 | 27 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_canvas_bridge.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_cast_server.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_catalog_freshness.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_catalog_rescan.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_catalog_scan_junctions.py | 9 | 9 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_catalog_tags.py | 12 | 12 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_census_drift_patrol.py | 46 | 46 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_census_liveness.py | 6 | 6 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_chain_byte_exact_io.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_chan.py | 7 | 7 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_chat_source_agent_workday.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_chatgpt_bot.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_cleanup.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_clerk_route_fix.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_coding_session_loop.py | 7 | 7 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_coding_session_orchestrator.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_coding_session_runner.py | 6 | 6 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_compute_reconcile.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_conductor_eval.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_container_setup.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_context_admission.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_context_checkpoint_pack.py | 2 | 2 | 0 | 0 | NO | 2026-09-28 (this census run) |
| tests/test_context_freeze.py | 6 | 6 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_context_pack_quantized_laws.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_coordination.py | 8 | 8 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_corpus_fts.py | 11 | 11 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_corpus_path_seam.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_cost_ledger.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_cost_simulator.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_cost_truth.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_dashboard_plugin.py | 1 | 1 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_dead_hand.py | 8 | 8 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_decision_framework.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_deep_research_moonshot.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_demote_candidates.py | 1 | 1 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_description_pin.py | 8 | 8 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_desk_baseline_probe.py | 11 | 11 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_desk_conductor.py | 9 | 9 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_desk_dialogue.py | 30 | 29 | 0 | 1 | yes | 2026-09-28 (this census run) |
| tests/test_desk_local_adapter.py | 6 | 6 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_desk_observer.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_desk_orchestrator.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_desk_orchestrator_memory.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_desk_timing.py | 6 | 6 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_dirac_loop.py | 8 | 8 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_display.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_distill.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_docker_ops.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_doctor_provider_endpoints.py | 21 | 21 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_doctor_scheduled_tasks.py | 16 | 16 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_dormant_gate_b2133.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_dormant_gate_b2521.py | 1 | 1 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_drift_dashboard.py | 8 | 8 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_drift_pairs_stamp.py | 17 | 17 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_drift_patrol_prompt_copy.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_elevate.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_embassy_deliver.py | 7 | 7 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_embassy_integrity.py | 22 | 22 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_env_load_mistral_keys.py | 6 | 6 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_env_redirect_tripwire.py | 10 | 10 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_events_key_schema.py | 10 | 10 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_factory_freeze_gate.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_factory_machine.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_failure_kb.py | 10 | 10 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_falsifier_ledger.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_feature_lab.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_fork_router.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_fossil_check.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_freshness_gate.py | 31 | 31 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_frontier_advisor.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_frontier_council.py | 8 | 8 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_frontier_salon.py | 8 | 8 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_game_dfhack.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_game_dm.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_game_emulator.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_game_entry.py | 6 | 6 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_game_environment.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_game_live.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_game_piece_tandem.py | 6 | 6 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_game_play.py | 7 | 7 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_game_portal.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_game_ramp.py | 6 | 6 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_game_world_render.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_game_world_render_optics.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_gate_blocking_paths.py | 14 | 14 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_gauntlet_sweeps.py | 8 | 8 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_gemini_native.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_ghost.py | 31 | 31 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_ghost_memlance_notebook.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_ghost_spooky.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_ghost_summon.py | 6 | 6 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_governor_autorun.py | 1 | 1 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_governor_fallback.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_grave_classify.py | 44 | 44 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_grounding_chain.py | 7 | 7 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_grounding_wave_presence.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_grounding_wave_v4.py | 26 | 26 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_growth_cycle.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_gygax_steal.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_handoff_inbox.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_harvest_fold.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_headless.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_headless_law.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_healthz_status.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_honest_cache_meter.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_hood.py | 1 | 1 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_hook_prefix_pairing.py | 7 | 7 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_hunger_ledger_parity.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_hydro_xor_sim.py | 15 | 15 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_icon_drop_escape.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_icon_drop_fold.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_icon_drop_icon_thread.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_idea_graph.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_ijl.py | 10 | 10 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_improve_behavioral_scout.py | 10 | 10 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_improve_crash_scout.py | 18 | 18 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_improve_loop.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_improve_off_on.py | 6 | 6 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_improve_provider_probe.py | 17 | 17 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_improve_status_scheduled_task.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_index_fold_host.py | 27 | 27 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_intervention_gate.py | 8 | 8 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_invariant.py | 7 | 7 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_k17_holds.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_k17_pilot.py | 6 | 6 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_kv_seal.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_lab_episode.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_lane_effort.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_lane_runner_cluster.py | 27 | 27 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_lattice_distance.py | 12 | 12 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_lattice_grounding.py | 6 | 6 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_lattice_query.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_launch_pad.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_launch_topology.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_law.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_lesson_gate.py | 23 | 23 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_lifecycle.py | 10 | 10 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_line_range_and_verify.py | 11 | 11 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_link_library.py | 35 | 35 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_links_sha_ratchet.py | 10 | 10 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_live_ops_readiness.py | 1 | 1 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_lm_studio.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_local_gpu_probes.py | 8 | 8 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_local_pulse.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_local_scheduler.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_loop_audit.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_loop_breaker.py | 8 | 8 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_loop_death_guards.py | 25 | 24 | 1 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_mag_sense.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_mcp_quantized.py | 6 | 6 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_md_record_seal.py | 9 | 9 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_memlance_wave.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_memlang.py | 8 | 8 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_memory_events.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_memory_map.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_meter_patrol.py | 8 | 8 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_mimo_watch_error_capture.py | 18 | 18 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_mirror_intro.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_mirror_lens_gate.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_mirror_voice_pack.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_moonshot_engine.py | 6 | 6 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_mud_steal.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_nervous_system.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_no_win.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_null_model_refuse.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_off_hours.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_openclaw_catalog.py | 1 | 1 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_openclaw_patches.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_operating_protocol.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_operator_inbox.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_operator_mode.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_oracle.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_orchestrator_queue.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_orchestrator_reap_completed.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_organ_map.py | 3 | 0 | 3 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_osculating.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_overseer_steering_api.py | 7 | 7 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_pack_modes_steward.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_party_subchain.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_paste_pipeline_footer.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_perplexity_research.py | 15 | 15 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_phase2_surface.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_physics_steal.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_pin_law_fail_output.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_ponytail_audit.py | 3 | 2 | 1 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_power.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_pro_library.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_pro_library_eval.py | 7 | 7 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_process_supervisor.py | 11 | 11 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_prompt_lance.py | 13 | 13 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_prompt_steering.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_provider_error_tally.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_provider_gateway.py | 9 | 9 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_pupeteering.py | 6 | 6 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_q_boundaries.py | 1 | 1 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_qdrop_canonical.py | 7 | 7 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_quorum_p4_selfvote.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_quota_billable.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_quota_dormant_skip.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_quota_provider_lock.py | 7 | 7 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_quote_gate.py | 6 | 6 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_quote_hitrate.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_ractor_falsifier_stubs.py | 6 | 1 | 0 | 5 | NO | 2026-09-28 (this census run) |
| tests/test_reconnect_cage_first.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_reconstruct.py | 6 | 6 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_release_registry.py | 6 | 6 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_release_subprocess_map.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_remote_control.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_repack_integration.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_repo_readiness.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_republic_ambassador.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_republic_os.py | 8 | 8 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_republic_wave.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_research_fold.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_resume_contract.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_riddler.py | 16 | 16 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_riddler_map.py | 16 | 16 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_roadmap_gap_probe.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_roadmap_runner.py | 7 | 7 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_room_tags.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_roshomon_mine.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_route_trace.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_router.py | 11 | 11 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_router_comms_boost.py | 14 | 14 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_routing_concert.py | 1 | 1 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_routing_smoke.py | 1 | 1 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_run_worth.py | 7 | 7 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_scenarios_gate_hook_pin.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_scripts_path_pins.py | 6 | 6 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_seat_corpus.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_seat_crash_guard.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_seat_registry.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_seat_steer.py | 9 | 9 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_seed_mcp.py | 15 | 15 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_seed_paired_uplift.py | 6 | 6 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_self_steal.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_selffeed_integration.py | 0 | 0 | 0 | 0 | NO | none found |
| tests/test_sense_mcp.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_session_freeze.py | 19 | 19 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_session_route.py | 8 | 8 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_shape_seed.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_shared_surface_events.py | 23 | 22 | 1 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_shell_powershell_resolution.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_silentpass_batch2.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_skill_drop.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_skill_ledger.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_skill_ledger_outcome_vocab.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_skill_lifecycle.py | 14 | 14 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_skill_seat.py | 6 | 5 | 1 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_social_hone.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_socratic_research.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_source_trace.py | 9 | 9 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_sovereign_handshake.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_spawn_smoke.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_spec_gate_job_floor.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_spore_seed.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_stack.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_state_pile.py | 6 | 6 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_stealth_driver_effort_dial.py | 1 | 1 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_stealth_driver_prompt_lance.py | 3 | 3 | 0 | 0 | NO | 2026-09-28 (this census run) |
| tests/test_steer.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_steer_bridge.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_steer_sign.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_steward_daily.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_steward_queue_has_goal.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_substrate_identity.py | 1 | 1 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_supervision_soak.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_surface_adapters.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_surface_audit.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_surface_contract.py | 8 | 8 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_surface_instruction.py | 6 | 6 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_swarm_local_drain.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_swarm_quota_gate.py | 2 | 0 | 2 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_switchboard.py | 14 | 14 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_t1_steering.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_tactical_framework.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_tapestry_visual.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_temperature_stack.py | 9 | 9 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_tesuji_shell.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_thought_quantizer.py | 7 | 7 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_three_track.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_tier_probe.py | 7 | 7 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_tier_refuse.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_token_chain.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_tool_dispatch_shape.py | 13 | 13 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_tool_quant.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_tools_and_handoff.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_training_events.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_training_export.py | 1 | 1 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_trajectory_bounds.py | 1 | 1 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_trajectory_rib.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_transport_precheck.py | 6 | 6 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_tripartite_boot.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_union_driver_v2.py | 6 | 6 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_unsloth_seat.py | 8 | 8 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_v3_deepseek_wiring.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_v3_modules.py | 9 | 9 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_vantage_audit.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_vast_cost.py | 1 | 1 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_vast_train_dry.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_verb_stones.py | 14 | 14 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_verkle_artifact.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_verkle_audit.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_verkle_compaction.py | 9 | 9 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_verkle_lock.py | 1 | 1 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_vessel_swarm.py | 6 | 6 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_violation_ratchet.py | 7 | 7 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_virtual_desk_loop.py | 5 | 5 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_voice_dictate.py | 9 | 9 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_voice_pipeline.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_voice_scratch.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_voice_shadow.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_voice_turn.py | 7 | 7 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_vram_hologram.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_warning_monitor.py | 3 | 3 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_water_computer.py | 7 | 7 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_water_graph.py | 7 | 7 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_water_graph_campaign.py | 9 | 9 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_water_graph_starvation.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_water_swarm.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_wave_driver.py | 7 | 7 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_wireshark_steal.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_workflow_gate.py | 8 | 8 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_workflow_registry_append_only.py | 2 | 2 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_wow_bones.py | 12 | 12 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_wow_bones_session.py | 11 | 11 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_wow_family.py | 8 | 8 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_wow_manifest.py | 4 | 4 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_wow_player.py | 17 | 17 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_wow_world.py | 12 | 12 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_write_strip.py | 12 | 11 | 1 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_zai_backoff_floor.py | 13 | 13 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/test_zai_burst.py | 8 | 8 | 0 | 0 | yes | 2026-09-28 (this census run) |
| tests/wave_driver_test.py | 12 | 12 | 0 | 0 | yes | 2026-09-28 (this census run) |

## Untracked test files (4, all executed in this census run anyway)

- `tests/test_context_checkpoint_pack.py` - 2 collected, 2 pass / 0 fail / 0 skip
- `tests/test_ractor_falsifier_stubs.py` - 6 collected, 1 pass / 0 fail / 5 skip
- `tests/test_selffeed_integration.py` - 0 collected, 0 pass / 0 fail / 0 skip
- `tests/test_stealth_driver_prompt_lance.py` - 3 collected, 3 pass / 0 fail / 0 skip

## Method notes / limits

- Verbose FAILED lines in the raw log carry full node IDs; the short-summary lines truncate
  reasons, so failure REASONS above are from the short summary only (FileNotFoundError,
  TypeError, AssertionError visible in truncated form).
- The run used `-p no:cacheprovider`, so it wrote no new .pytest_cache state.
- Summary line word-for-word: `10 failed, 2388 passed, 12 skipped, 4 warnings in 3135.22s (0:52:15)`.
- No em-dash or en-dash appears in this file (machine-scanned before bank).

