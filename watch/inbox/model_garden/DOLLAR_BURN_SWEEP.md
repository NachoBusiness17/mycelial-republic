# DOLLAR BURN SWEEP - per-file organ compliance (mass adjudication)

**Schema:** wiring.sweep.dollar_burn.v1 - **ts:** 2026-10-01 - **lane:** D1 THE DOLLAR BURN (ZCode subagent)
**Instrument:** 3 grep sets (build_targets.py) over mag/ tools/ server/ scripts/ + main.py ->
391 unique targets -> 8 file-backed ds_workhorse batches (deepseek-chat, thinking-off, retry-once)
-> 3-line verdict per file per organ, parsed by aggregate.py. Every count below is byte-derived
from results_*.jsonl at aggregation moment 2026-10-01; nothing hand-copied (B2-216 law).

**Organs** (from watch/inbox/WIRING_DEBT_CENSUS_20261001.md rows 9, 6, 3):
- a) fires LLM calls without importing mag.inference_budget
- b) fetches remote URLs without a browser User-Agent
- c) writes shared jsonl/json surfaces without atomic tmp+replace

## Headline

| organ | applicable | YES-compliant | NO-violation | NA | adjusted NO (contradictions removed) |
|---|---|---|---|---|---|
| a) inference_budget | 149 | 2 | 147 | 242 | 147 |
| b) browser UA | 153 | 31 | 122 | 238 | 122 |
| c) atomic write | 299 | 4 | 295 | 92 | 289 |

- **Files swept: 391 / 391 selected** (fire grep set 205, fetch set 182, write set 144; union 391)
- **Batches: 8, all items ok=True on attempt 1, zero empties, zero unparseable** (gopher disease absent)
- **Dollars burned: $0.5193 of the $1.50 cap** ($0.9807 headroom). Cost basis:
  usage-estimated at $0.27/M in + $1.10/M out per tools/ds_workhorse.py:65-68; avg $0.00133/file.
- **Triple violators (all three organs NO): 53 files.**
- The only organ-a compliant files remain the rib's own two: tools/hermes_burn.py, tools/model_garden.py
  (confirms census row 9: the class-kill organ is wired into 2 of the fire paths; now 2 of 149).

## Batch ledger

| batch | items | cost usd |
|---|---|---|
| results_01.jsonl | 50 | 0.0561 |
| results_02.jsonl | 50 | 0.0673 |
| results_03.jsonl | 50 | 0.0682 |
| results_04.jsonl | 50 | 0.0710 |
| results_05.jsonl | 50 | 0.0681 |
| results_06.jsonl | 50 | 0.0685 |
| results_07.jsonl | 50 | 0.0647 |
| results_08.jsonl | 41 | 0.0553 |
| **total** | **391** | **0.5193** |

## Top-10 worst files (rank: violations desc, applicable organs desc)

| # | file | a | b | c | evidence |
|---|---|---|---|---|---|
| 1 | mag/arena_bench.py | NO L376 | NO L428 | NO L494 | flash_call fires LLM without importing mag.inference_budget |
| 2 | mag/art_forge.py | NO L57 | NO L68 | NO L149 | fires LLM image API calls, no mag.inference_budget import |
| 3 | mag/arxiv_harvest.py | NO L134 | NO L71 | NO L117 | flash_call fires LLM without importing mag.inference_budget |
| 4 | mag/cache_identity.py | NO L212 | NO L180 | NO L405 | fires ollama chat via urllib, no mag.inference_budget import |
| 5 | mag/desk_dialogue.py | NO L214 | NO L292 | NO L108 | fires LLM calls via _chat_http_ex/chat without mag.inference |
| 6 | mag/desk_model_probe.py | NO L122 | NO L32 | NO L202 | fires LLM generate call, no mag.inference_budget import |
| 7 | mag/flight_recorder.py | NO L332 | NO L328 | NO L192 | fires LLM calls via urlopen, no mag.inference_budget import |
| 8 | mag/forge_daemon.py | NO L109 | NO L109 | NO L55 | fires LLM POST via urllib, no mag.inference_budget import |
| 9 | mag/gopher_lite.py | NO L142 | NO L125 | NO L111 | fires LLM calls, no mag.inference_budget import |
| 10 | mag/gpu_ghost.py | NO L213 | NO L216 | NO L284 | fires ollama LLM calls, no mag.inference_budget import |

Standing loop carriers census row 9 named, now byte-checked: lane_runner / gopher_lite / scale_salon
are triple violators; tesuji_fire + research_fanout violate a and c but DO carry a browser UA;
brain / janitor / daemon fire nothing at file scope (delegators, see delta note 2).

## Delta vs the hand census (does mass checking find what hand checking missed?)

Organ a (inference_budget):
- Census hand claim: 184 fire files in mag/+tools/, 182 unwired. Sweep semantic count:
  **130 NO-violation + 2 YES in mag/+tools/** (149 applicable across the full frame).
- **Denominator correction (mass beats hand):** 115 grep-fire hits adjudicated NA.
  Byte-proof example: mag/brain.py, which the census NAMED as a standing carrier, matches the census
  grep only via its own REST docstrings (GET /api/v1/stack, POST /api/v1/brain at brain.py:48-65);
  zero LLM client or endpoint calls in the file. The 184 headline carries this false-positive class.
- **Blind-spot catch (mass beats grep):** 59 fire files the combined grep recipe missed:
  16 localhost-ollama callers (gpu_ghost, lattice_loop, cache_identity...), provider hosts outside the
  census pattern (groq/together/nous/google), and client-library users; the census pattern
  (chat/completions|/v1/|api.openai|deepseek|anthropic|openrouter) never sees them.
- **Frame catch:** 17 organ-a violators live entirely outside the census's mag/+tools frame (scripts/, server/, main.py), e.g.
  scripts/council_runner.py, scripts/librarian.py, scripts/tide_gemma.py, scripts/provider_liveness.py.

Organ b (browser UA):
- Census hand claim: 141 fetching files in mag/+tools/, 97 bare, 44 carrying UA. Sweep:
  **103 bare / 26 carrying in mag/+tools/** (122 bare / 31 carrying overall).
- Directionally identical to the census (roughly 4 of 5 fetchers ride library defaults); mass check adds
  the per-file line evidence and extends the count to server/+scripts/.

Organ c (atomic writes):
- Census hand claim: ~15 sibling writers named by hand + 20+ files re-rolling the atomic idiom.
  Sweep: **295 raw NO-violations, 289 after removing 6 self-contradictory verdicts**
  (named: mag/agent_cli.py, mag/ai_landscape.py, mag/browser_env.py, mag/clawbot.py, mag/framework_map.py, main.py - e.g. mag/ai_landscape.py:256 writes .md, verdict said NO).
- Mode split of violators: 105 append-mode, 175 write_text, 15 plain open w. The append share matters
  on Windows (census row 3: plain one-line appends are tolerable on POSIX, must be wrapped here).
- **The sharpest catch:** 151 of the write violators are INVISIBLE to the mission's own grep
  recipe (open(...'w') with .json/.jsonl on the same line) because the path rides a variable:
  mag/cooker.py:99 `with LEDGER.open("a")`, mag/afk_cadence.py:236, mag/api_gateway.py:665,
  mag/arxiv_mine.py:65. Same-line grep structurally cannot see the writer class; the census's ~15-name
  hand list was a sample of a ~290-file population (20x wider).

Honest cost of mass checking (both directions filed):
- 6 self-contradictory organ-c verdicts (1.5% of organ-c, named above); headline uses adjusted 289.
- The file-scope contract reads delegation carriers (brain/janitor/daemon) as organ-a NA: true at file
  scope, but the census's loop-level claim (their subsystems fire) stands; a helper-import sweep is the
  follow-up instrument, not a verdict change.

## Full compliance grid (391 files)

Key: **V<line>** = NO-violation at line - **C<line>** = YES-compliant at line - **n** = organ not
applicable - **!** = verdict self-contradictory (discounted, named above) - **X** = missing verdict.
Machine copy with reasons: dollar_burn_20261001/sweep_grid.json.

| file | a) budget | b) UA | c) atomic |
|---|---|---|---|
| mag/_bench_free_shelf.py | V34 | V24 | n |
| mag/_cache_ab_probe.py | V35 | n | V63 |
| mag/_codex_seat.py | n | n | V77 |
| mag/_consensus_witness.py | V46 | n | V91 |
| mag/_demo_eyes_receipt.py | V51 | n | V106 |
| mag/_demo_telepathy.py | n | n | V96 |
| mag/_grok_corpus_burn.py | V26 | n | V94 |
| mag/_probe_burst_20260903.py | V33 | V33 | n |
| mag/_probe_zai_balance.py | n | V40 | n |
| mag/adventure_one_shot.py | n | n | V82 |
| mag/afk_cadence.py | n | n | V236 |
| mag/afk_loop.py | V111 | V98 | n |
| mag/agent_cli.py | V43 | n | !V3071 |
| mag/ai_landscape.py | n | n | !V256 |
| mag/aos_grok.py | V172 | n | V99 |
| mag/api_gateway.py | V641 | n | V665 |
| mag/arc_seed.py | n | n | V169 |
| mag/arena_bench.py | V376 | V428 | V494 |
| mag/art_forge.py | V57 | V68 | V149 |
| mag/arxiv_harvest.py | V134 | V71 | V117 |
| mag/arxiv_mine.py | n | V78 | V65 |
| mag/ask_router.py | n | n | V167 |
| mag/auth_switchboard.py | n | V115 | V150 |
| mag/autoglm.py | V134 | V129 | n |
| mag/autorun_common.py | n | n | V52 |
| mag/batch_scribe.py | V54 | n | V178 |
| mag/brain.py | n | n | n |
| mag/breakthrough_loop.py | n | n | V103 |
| mag/browser_driver.py | n | V125 | n |
| mag/browser_env.py | n | n | !V176 |
| mag/cache_identity.py | V212 | V180 | V405 |
| mag/cache_map.py | n | n | V422 |
| mag/cache_router.py | n | n | n |
| mag/campaign.py | V146 | n | V716 |
| mag/cast_launch.py | n | n | n |
| mag/cast_server.py | n | n | n |
| mag/chain_query.py | n | n | n |
| mag/checkin_route.py | n | V125 | V333 |
| mag/child_development_acquire.py | n | C72 | V304 |
| mag/chord_lens.py | n | n | n |
| mag/chord_triangulate.py | n | V45 | V193 |
| mag/clawbot.py | n | V165 | !V143 |
| mag/cleanup.py | n | n | n |
| mag/clippy.py | n | n | n |
| mag/coding_session_runner.py | n | n | V133 |
| mag/compute_reconcile.py | n | n | V173 |
| mag/computing_history_acquire.py | n | C87 | V266 |
| mag/conductor_eval.py | n | n | V82 |
| mag/console_render.py | n | n | V86 |
| mag/cooker.py | n | n | V99 |
| mag/corpus_acquire.py | n | V45 | V633 |
| mag/corpus_archive_acquire.py | n | C152 | V328 |
| mag/corpus_archive_check.py | n | V32 | V202 |
| mag/corpus_arxiv_register.py | n | C33 | V148 |
| mag/corpus_cite_promote.py | n | C56 | V344 |
| mag/corpus_gutenberg_truth.py | n | V51 | V130 |
| mag/corpus_ingest.py | n | n | V98 |
| mag/corpus_land.py | n | C59 | V178 |
| mag/corpus_lead_verify.py | n | V29 | V155 |
| mag/corpus_map_backfill.py | n | n | V90 |
| mag/corpus_nonanswer.py | n | n | V126 |
| mag/corpus_reconcile.py | n | C43 | V95 |
| mag/corpus_salvage.py | n | V53 | V273 |
| mag/corpus_selfsteal.py | n | n | V255 |
| mag/cost_enforcer.py | n | n | V80 |
| mag/cost_truth.py | n | n | n |
| mag/daemon.py | n | n | V22 |
| mag/dashboard_plugin.py | n | n | n |
| mag/decision_framework.py | n | n | n |
| mag/dedupe_index.py | n | n | V115 |
| mag/deep_research_moonshot.py | n | n | V179 |
| mag/desk_dialogue.py | V214 | V292 | V108 |
| mag/desk_model_probe.py | V122 | V32 | V202 |
| mag/desk_ops.py | n | V35 | n |
| mag/diary.py | n | n | V491 |
| mag/diary_node.py | V141 | n | V350 |
| mag/dispatch.py | V318 | n | n |
| mag/display.py | n | n | n |
| mag/docker_ops.py | n | n | V49 |
| mag/doctor.py | V93 | C249 | n |
| mag/dogfood_audit.py | n | n | V333 |
| mag/dormant.py | n | n | n |
| mag/drainer_stats.py | n | n | n |
| mag/ecosystem_surface.py | n | n | n |
| mag/effect_broker.py | V17 | n | V166 |
| mag/elevate.py | n | n | n |
| mag/embassy_deliver.py | n | V208 | n |
| mag/extension_deploy.py | n | n | n |
| mag/falsifier_counter.py | n | n | V646 |
| mag/fanout.py | V67 | V67 | n |
| mag/flex_test.py | n | n | V106 |
| mag/flight_recorder.py | V332 | V328 | V192 |
| mag/flock_scheduler.py | n | V63 | n |
| mag/forge_daemon.py | V109 | V109 | V55 |
| mag/framework_map.py | n | n | !V947 |
| mag/free_tier.py | n | n | n |
| mag/free_to_swarm.py | n | n | V69 |
| mag/frontier_salon.py | V97 | n | V320 |
| mag/fuel_feed.py | V569 | n | V294 |
| mag/game_entry.py | n | n | V204 |
| mag/game_view.py | n | n | n |
| mag/ghost.py | n | n | V77 |
| mag/ghost_control.py | n | n | n |
| mag/ghost_cross.py | V111 | n | V48 |
| mag/ghost_summon.py | V312 | n | n |
| mag/ghost_whisper.py | n | n | V87 |
| mag/gopher_lite.py | V142 | V125 | V111 |
| mag/governance.py | n | n | n |
| mag/governor_autorun.py | n | n | V70 |
| mag/gpu_ghost.py | V213 | V216 | V284 |
| mag/grok_rightsize.py | V370 | V122 | V634 |
| mag/grok_route.py | n | n | n |
| mag/growth_cycle.py | n | n | V76 |
| mag/gstd_probe.py | n | V35 | V170 |
| mag/health.py | n | V136 | n |
| mag/hermes_warm_boot.py | n | V155 | V243 |
| mag/holdings_audit.py | n | n | V198 |
| mag/idea_flow.py | n | n | n |
| mag/improve.py | n | n | V162 |
| mag/improve_loop.py | n | n | V79 |
| mag/ingest_registry.py | n | n | V453 |
| mag/janitor.py | n | n | V59 |
| mag/kabuki_salon.py | V92 | n | V141 |
| mag/knot_at_close.py | n | n | V273 |
| mag/lane_probe.py | V90 | V90 | V114 |
| mag/lane_runner.py | V1018 | V151 | V113 |
| mag/lane_salon.py | V113 | n | V193 |
| mag/lane_supervisor.py | V104 | C103 | V162 |
| mag/lattice_loop.py | V269 | n | V233 |
| mag/launch_pad.py | n | n | n |
| mag/legacy_audit.py | n | n | V266 |
| mag/lifecycle.py | n | n | V914 |
| mag/link_library.py | n | n | V338 |
| mag/lite_guard.py | n | V142 | V247 |
| mag/lite_scale.py | V84 | V82 | V154 |
| mag/lm_studio.py | V84 | V40 | n |
| mag/local_pulse.py | n | V61 | V41 |
| mag/local_scheduler.py | V205 | n | V48 |
| mag/local_usable.py | n | n | V242 |
| mag/loops_registry.py | n | n | n |
| mag/memweave.py | n | n | V94 |
| mag/mind_mine.py | n | n | V393 |
| mag/mind_window.py | n | n | V409 |
| mag/museum.py | n | n | V55 |
| mag/nervous_system.py | n | n | C242 |
| mag/notion_api.py | n | V78 | n |
| mag/ntrs_acquire.py | n | C54 | V326 |
| mag/offline.py | V126 | V50 | n |
| mag/oh_fuck.py | n | n | V96 |
| mag/ollama_policy.py | n | V27 | n |
| mag/openclaw_catalog.py | n | n | V221 |
| mag/ops_graph.py | n | n | V393 |
| mag/oracle.py | n | V76 | V114 |
| mag/orphan_timer.py | n | n | C91 |
| mag/osculating.py | n | n | V174 |
| mag/ox_alpha_steal.py | n | n | n |
| mag/ox_gap.py | V126 | n | V135 |
| mag/ox_megaburn.py | V516 | n | V461 |
| mag/ox_megaburn2.py | V250 | n | V229 |
| mag/ox_megaburn3.py | V176 | n | V155 |
| mag/ox_probe.py | V122 | V122 | V210 |
| mag/ox_resident.py | V264 | n | V247 |
| mag/ox_scout.py | V121 | n | V107 |
| mag/ox_seat.py | V129 | V129 | n |
| mag/ox_swarm.py | V133 | n | V153 |
| mag/p20_pending_wave.py | V106 | V109 | n |
| mag/partner_puppet.py | n | n | n |
| mag/paste_pipeline.py | V245 | n | V218 |
| mag/percolator_heal_test.py | n | n | V47 |
| mag/perplexity_research.py | V174 | V174 | V156 |
| mag/persona_priorart_acquire.py | n | C84 | V193 |
| mag/phone_relay.py | n | C95 | V109 |
| mag/platform_kill.py | n | n | n |
| mag/play_benchmark.py | n | n | V218 |
| mag/power.py | n | V74 | V42 |
| mag/prefix_prover.py | n | n | V173 |
| mag/preload_selector.py | V244 | V210 | V388 |
| mag/press_digest.py | n | n | V166 |
| mag/probe_route.py | V71 | V71 | V120 |
| mag/process_supervisor.py | n | V164 | V149 |
| mag/queue_gate.py | n | n | V330 |
| mag/quorum_window.py | V137 | n | V112 |
| mag/ractor_corpus.py | n | C302 | V456 |
| mag/ractor_vessels.py | V69 | n | V84 |
| mag/real_swarm.py | V130 | n | V102 |
| mag/recreation_rib.py | V181 | V142 | V133 |
| mag/refine_chain.py | V432 | n | V191 |
| mag/registry.py | n | n | V163 |
| mag/renderman_ask.py | V132 | n | V56 |
| mag/republic_feed.py | n | n | V127 |
| mag/research_fanout.py | V232 | C236 | V416 |
| mag/research_lens.py | n | n | V151 |
| mag/research_pack.py | V706 | V67 | V212 |
| mag/riddler_sanitize.py | n | n | n |
| mag/riddler_tap.py | V114 | n | V157 |
| mag/riddler_transport.py | V86 | n | n |
| mag/rightsize_api.py | n | n | V108 |
| mag/router.py | n | n | n |
| mag/saelis_room.py | V197 | n | n |
| mag/salon_50.py | V160 | n | V170 |
| mag/salon_openclaw.py | V114 | n | V44 |
| mag/scale_salon.py | V188 | V184 | V249 |
| mag/schema_registry.py | n | n | V138 |
| mag/scrum.py | n | n | V127 |
| mag/seal.py | n | n | V140 |
| mag/seat_availability.py | n | n | V130 |
| mag/seat_corpus.py | n | n | V294 |
| mag/seat_hunter.py | n | V329 | V586 |
| mag/seat_probe.py | V51 | n | V100 |
| mag/seat_registry.py | n | n | V59 |
| mag/seat_steer.py | n | n | V178 |
| mag/seats.py | n | n | n |
| mag/self_test.py | n | n | V157 |
| mag/session_dossier.py | V609 | n | V574 |
| mag/session_freeze.py | n | n | V221 |
| mag/session_maze.py | V250 | n | V160 |
| mag/session_overseer.py | n | n | V67 |
| mag/session_ritual.py | n | V358 | n |
| mag/siege_castle_fiction.py | n | C57 | V253 |
| mag/single_feed.py | n | n | V74 |
| mag/skill_ledger.py | n | n | V79 |
| mag/solved_surface.py | n | n | n |
| mag/sovereign_dashboard.py | n | n | n |
| mag/stack.py | n | n | n |
| mag/steal_first.py | n | n | n |
| mag/steer.py | n | n | V52 |
| mag/story.py | n | n | V314 |
| mag/subscriptions.py | n | n | n |
| mag/surface_adapters.py | V132 | V136 | V184 |
| mag/surface_audit.py | n | n | n |
| mag/surface_render.py | n | n | V790 |
| mag/surface_steal.py | n | n | V108 |
| mag/swarm_control.py | n | n | V87 |
| mag/swarm_local_drain.py | n | n | V211 |
| mag/swarm_map.py | n | n | V150 |
| mag/swarm_snapshot.py | V259 | V263 | n |
| mag/swarm_tools.py | n | n | V104 |
| mag/swarm_worker.py | V348 | n | V115 |
| mag/switchboard.py | n | n | V72 |
| mag/system_map.py | n | n | V131 |
| mag/tandem_key_test.py | V66 | n | V70 |
| mag/tangent.py | V204 | n | V156 |
| mag/tapestry.py | n | n | V749 |
| mag/team_knot.py | n | V70 | V149 |
| mag/telegram_desk.py | V107 | V88 | V96 |
| mag/temperature_stack.py | n | n | V338 |
| mag/test_runner.py | n | n | V136 |
| mag/tesuji_fire.py | V121 | C125 | V317 |
| mag/tesuji_surface.py | V414 | V414 | V227 |
| mag/thought_bank.py | n | n | V43 |
| mag/token_chain.py | V305 | n | V395 |
| mag/tool_manifest.py | n | n | V153 |
| mag/training_set.py | n | n | V83 |
| mag/unsloth_seat.py | n | n | V89 |
| mag/usage_digest.py | n | n | V187 |
| mag/usage_forecast.py | n | n | n |
| mag/vast_cost.py | n | V51 | V164 |
| mag/vast_launcher.py | n | V307 | n |
| mag/verb.py | V137 | C135 | V81 |
| mag/verkle_knot.py | n | n | V1094 |
| mag/vision.py | V84 | C87 | n |
| mag/vscode_feed.py | n | n | V46 |
| mag/warmed_cold_replay.py | V204 | V204 | V341 |
| mag/warning_monitor.py | n | n | V61 |
| mag/wave_fire.py | V72 | V75 | V86 |
| mag/work_loop.py | n | n | n |
| mag/worldline_seed.py | V961 | n | V950 |
| mag/x_control_surface.py | n | C167 | V102 |
| mag/x_oauth.py | n | V178 | V92 |
| main.py | n | n | !V79 |
| scripts/_bump_tesuji10.py | n | n | n |
| scripts/_patch_load_verkle.py | n | n | n |
| scripts/_survival_bag.py | n | n | V73 |
| scripts/build_lane_game.py | V641 | C257 | V671 |
| scripts/build_vislab_catalog.py | n | n | V404 |
| scripts/capacity_ladder.py | n | n | V289 |
| scripts/council_runner.py | V435 | V435 | V665 |
| scripts/desk_baseline_probe.py | n | V59 | V302 |
| scripts/dm_tools_dual_research.py | V110 | n | V185 |
| scripts/endpoint_news.py | n | V57 | V158 |
| scripts/esoteric_fills.py | n | V33 | V127 |
| scripts/fetch_founding_law.py | n | C119 | V182 |
| scripts/fetch_training_pdfs.py | n | V40 | V474 |
| scripts/garden_battery_local.py | V134 | C136 | V267 |
| scripts/garden_battery_local_refire.py | V87 | n | V146 |
| scripts/handoff_escalation_watcher.py | V206 | V86 | V171 |
| scripts/harness_eval.py | n | V201 | V254 |
| scripts/lattice_check.py | n | V165 | V206 |
| scripts/librarian.py | V52 | n | n |
| scripts/lite_fold_20260827.py | V54 | n | V74 |
| scripts/meld_claims.py | V44 | V44 | V115 |
| scripts/provider_liveness.py | V70 | n | V143 |
| scripts/roadmap_gap_probe.py | n | V28 | V255 |
| scripts/steering_suite.py | V8 | n | V1001 |
| scripts/sweep_vislab_health.py | n | V40 | V140 |
| scripts/tg_harvest.py | n | C33 | V73 |
| scripts/the50_w7_t32_gstd_probe2.py | n | V40 | V441 |
| scripts/tide_dashboard.py | n | n | V109 |
| scripts/tide_gemma.py | V84 | V56 | n |
| scripts/trailer_mode.py | n | n | V275 |
| scripts/union_fullsend_day.py | V603 | V340 | V594 |
| scripts/vast_paces.py | V57 | V50 | V43 |
| scripts/vast_paces_full.py | n | V90 | n |
| scripts/vision_bench.py | V93 | V93 | V121 |
| scripts/vision_endowment.py | V208 | n | V427 |
| scripts/vision_nightly.py | n | V87 | V71 |
| scripts/vision_triage_pool.py | V107 | C124 | V185 |
| server/identity_binding.py | n | V231 | n |
| tools/abliterate_p1_probe.py | V266 | V266 | V340 |
| tools/ack_fleet_game.py | n | n | n |
| tools/audio_channel.py | n | V90 | n |
| tools/backfill_direct.py | V102 | V56 | n |
| tools/binary_attest.py | n | V115 | V108 |
| tools/blind_probe.py | V85 | V89 | V181 |
| tools/build_adam_pdf.py | n | n | n |
| tools/build_adam_setup.py | n | n | n |
| tools/build_adam_setup_final.py | n | n | n |
| tools/build_adam_soul_full.py | n | n | n |
| tools/build_candy_pdfs.py | n | n | n |
| tools/cathedral_build.py | n | n | V432 |
| tools/cathedral_walk.py | n | n | V186 |
| tools/compaction_eval.py | V69 | n | V310 |
| tools/corpus_lens.py | n | n | V141 |
| tools/corpus_lens_run.py | V35 | n | V97 |
| tools/corpus_self_lens.py | n | n | V128 |
| tools/dem_to_board.py | n | V277 | V336 |
| tools/ds_workhorse.py | V61 | V61 | V77 |
| tools/duel_harness.py | V186 | V186 | V425 |
| tools/eastwest_thorn_20260920.py | V58 | n | n |
| tools/flashx_probe.py | V62 | V54 | n |
| tools/flock_parity.py | n | n | V923 |
| tools/full_scan.py | V87 | n | V210 |
| tools/fullsend_s2.py | V54 | n | V110 |
| tools/gaming_corpus_pass.py | V66 | n | V131 |
| tools/ghost_tournament.py | V121 | n | V315 |
| tools/gps_mcp/providers.py | V280 | V280 | n |
| tools/hermes_burn.py | C59 | V114 | V146 |
| tools/kv_slot_pilot.py | V244 | n | n |
| tools/ldt_nearmiss.py | n | n | V195 |
| tools/legality_dataset.py | n | n | V266 |
| tools/lens.py | V132 | V138 | V173 |
| tools/lensing_ask.py | V156 | V142 | V224 |
| tools/letter_salon_20260920.py | V100 | V100 | V140 |
| tools/librarian_backfill_20260927.py | n | V62 | V112 |
| tools/local_bench.py | V291 | n | V355 |
| tools/mcp_parity.py | n | V113 | n |
| tools/mickey17_v2_fold.py | n | C55 | n |
| tools/mimo_watch.py | V95 | n | V200 |
| tools/model_bakeoff.py | V85 | V82 | V104 |
| tools/model_garden.py | C56 | V172 | V203 |
| tools/mountain_selfplay.py | n | n | V824 |
| tools/ocean_v2_pilot.py | V91 | V105 | V196 |
| tools/olm_tokenizer_probe.py | V66 | V66 | n |
| tools/openrouter_free_gate.py | V69 | V56 | V141 |
| tools/pain_replication/analyze.py | n | n | V208 |
| tools/pain_replication/data/01_extract.py | n | n | V142 |
| tools/pain_replication/runner.py | n | n | V445 |
| tools/pricing_diff.py | n | C93 | V300 |
| tools/probe20_run.py | V255 | V258 | V388 |
| tools/pupeteer_gauntlet.py | V100 | V73 | V1243 |
| tools/qknot_b1.py | n | n | V68 |
| tools/queue_close.py | n | n | C195 |
| tools/queue_dupes_check.py | n | n | V87 |
| tools/research_mine.py | V62 | n | n |
| tools/research_rig.py | n | V110 | n |
| tools/reverse_map.py | V91 | V91 | V153 |
| tools/rib_check_game_loop.py | n | n | n |
| tools/roblox_npc_gateway.py | V186 | V182 | V158 |
| tools/saturation_fourcond.py | V109 | V117 | V237 |
| tools/seed_mcp_cold_client.py | n | n | V109 |
| tools/seed_salon.py | V74 | C72 | n |
| tools/seed_v2.py | n | n | V227 |
| tools/spec_execute.py | V76 | n | V158 |
| tools/steal_gdrive.py | n | C29 | V191 |
| tools/stealth_driver.py | V290 | V132 | V1405 |
| tools/stealth_fanout.py | V136 | V131 | V162 |
| tools/stealth_sweep.py | V84 | V81 | V134 |
| tools/steer_compare.py | V137 | n | V294 |
| tools/stills_xai.py | V100 | n | n |
| tools/task_wall.py | V121 | V121 | V144 |
| tools/thought_quantizer.py | n | n | V259 |
| tools/thrash_meter.py | n | n | V278 |
| tools/tier_probe.py | V200 | V208 | V366 |
| tools/tip_witness.py | n | V180 | C256 |
| tools/topic_research.py | n | n | V98 |
| tools/transport_precheck.py | n | C78 | V132 |
| tools/typed_scorer.py | V150 | V147 | n |
| tools/wandr_selfeval.py | n | C150 | V180 |
| tools/x_churn_cli.py | n | V106 | V146 |
| tools/x_churn_grok.py | V130 | C107 | V197 |
| tools/x_churn_seeds.py | V129 | V117 | V199 |

## Receipts and sidecars (all under watch/inbox/model_garden/dollar_burn_20261001/)

- build_targets.py (selection instrument) - targets.jsonl (grep sets + hit lines per file)
- prompt.txt (the ask) - manifest_01..08.jsonl (what was sent, item per file)
- results_01..08.jsonl (raw DeepSeek rows, cost per item) - aggregate.py - aggregate.json - sweep_grid.json
- Census being deltaed: watch/inbox/WIRING_DEBT_CENSUS_20261001.md (rows 9, 6, 3)
- Harness: tools/ds_workhorse.py (thinking-off, retry-once, file-backed manifests)

**Patrol hook this banks:** the census's own design section names tools/wiring_sweep.py as the
standing instrument; this sweep is its first full execution shape - grep-select, model-adjudicate,
aggregate, delta. Rerun cheaply (~$0.52 full-tree) at wave close.

