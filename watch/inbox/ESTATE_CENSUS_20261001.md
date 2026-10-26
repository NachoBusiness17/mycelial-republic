# ESTATE CENSUS 20261001: the "what are we" snapshot

- **Census moment:** 2026-09-30 19:04 EDT (bash `date`). Git HEAD stamps 09-30 18:38; `last_mile_20260930/FULL_BURN_STATE.md` self-stamps 2026-10-01 ~02:00 ET (mates fired ~01:50 ET): a stamp conflict inside tonight's receipts, flagged here, not adjudicated. Named for the 2026-10-01 cycle boundary.
- **Owner:** census seat (FILE OWNERSHIP: this file). **For:** operator, next seat, cycle brief.
- **Instruments law (B2-216):** every count below names its instrument and moment. Trust bytes, not reports.

## Headline

| Number | Read (instrument, moment) |
|---|---|
| Tools | 253 Python tools in `tools/`; 105 with a tests/ reference, 148 without; +18 non-py entries (ast docstring scan + tests-text grep, 19:04 EDT) |
| mag/ | 1,080 .py modules; 198 touched within 7d (100 within 48h); 472 (44%) referenced by tests/; 17 .bak parked (mtime stat, 19:04 EDT) |
| Receipts | inbox root 1,085 .md; `last_mile_20260930/` 183 entries (146 .md); `mountain_climb/` 17 entries (15 .md) (glob counts, 19:04 EDT) |
| Tests | **3,706 collected in 27.41s** (`pytest --collect-only -q`, this session ~19:00 EDT); 3,679 passed at the 18:38 executed run (HEAD commit); 470 .py files under tests/ (`find`) |
| Git | 40 commits on 09-30 (+263,087 / -465,896 over 1,342 files); 52 on 09-29 (+2,943,736 / 1,899 files); 426 dirty paths uncommitted (`git log --numstat` agg + `git status`) |
| Meters | Gates OPEN 5 / CLOSED 1 (gate_digest 17:25); quota day-shape RED, current window GREEN (quota_ledger 21:07Z); cost $135.71 lifetime, ~$2.39 frontier tonight; anomaly PROVEN (exit 1, rows named); GPS still test-double |
| Processes | ollama serve + 2 llama-servers; 2x stealth driver; governor_autorun loop; Hermes gateway + desktop; mates 8/8 remote on z.ai quota (wmic, 19:04 EDT) |
| CLIMB | Phase 0 complete 6/6 dossiers; W4 Opus lensing returned ($0.69, KEEP-spine/TIGHTEN-heavy verdict); Phase 1 route hardening is the live transform; brief assembly queued behind operator GO |

## 1. Tools: every entry in tools/, one line each

Tests column: `ref` = the tool stem appears somewhere under tests/ (coverage by REFERENCE, not an execution result); `none` = no reference found in the 470-file tests text. mtime = file mtime date. Docstrings parsed with ast; parse failures and missing docstrings named as such.
| Tool | What it does | Tests | mtime |
|---|---|---|---|
| `abliterate_p1_probe` | ABLITERATUS P1 baseline refusal census - gemma:2b as-is via local ollama API. | none | 2026-09-29 |
| `ack_fleet_game` | Copilot's Socratic ack on the subchain: ground truth on the game loop surface (one turn, no spam). | none | 2026-08-14 |
| `animal_profiles` | animal_profiles - the living per-animal behavioral layer (2026-10-01). | none | 2026-09-30 |
| `anomaly_flagger` | anomaly_flagger.py - IMP6 last-mile anomaly sweep (2026-09-30). | ref | 2026-09-30 |
| `ask_bank` | ask_bank.py - versioned hidden ask bank for the duel series (AJ2, 2026-09-30). | ref | 2026-09-30 |
| `ask_bank_seed` | ask_bank_seed.py - the frozen v1 seed corpus for tools/ask_bank.py (AJ2). | ref | 2026-09-30 |
| `attention_dam` | tools/attention_dam.py - the attention dam (Mickey17 W3, 2026-09-30). | ref | 2026-09-29 |
| `audio_channel` | audio_channel  -  the shadertoy audio input for PRIVLIDGE. | ref | 2026-09-25 |
| `auto_promote` | auto_promote.py - deterministic auto-promote gate for improve candidates (Q-002, 2026-09-28). | ref | 2026-09-28 |
| `autopilot` | Autopilot: spawn a gpipes swarm, poll, optionally nudge, collect, and write summary. | ref | 2026-08-07 |
| `backfill_direct` | backfill_direct.py  -  truncation backfill, direct-to-API (no agent seats). | none | 2026-09-22 |
| `battery_rerun` | battery_rerun.py - frozen method-card battery, reusable regression harness. | ref | 2026-09-26 |
| `bib_launder_check` | bib_launder_check - mechanical FAIL(BIB_LAUNDER) pre-flight checker (B2-154). | none | 2026-09-26 |
| `bin` | (dir, not a Python tool) | - | - |
| `blind_probe` | BLIND PROBE  -  the differential sensor array as a standing organ. | none | 2026-09-26 |
| `box_burn_watch` | box_burn_watch  -  utilization watcher for the "90 percent intelligently" law (2026-09-26). | none | 2026-09-26 |
| `brief_reaper` | Brief reaper: ingest watch/inbox *BRIEFS*.md boards into the stealth | ref | 2026-09-29 |
| `build_adam_pdf` | ═══ COVER ═══ | none | 2026-09-24 |
| `build_adam_setup` | ═══ WHAT YOU HAVE ═══ | none | 2026-09-24 |
| `build_adam_setup_final` | ═══ HARDWARE ═══ | none | 2026-09-24 |
| `build_adam_soul` | ═══ YOUR GAME ═══ | none | 2026-09-24 |
| `build_adam_soul_full` | ═══ YOUR GAME ═══ | none | 2026-09-24 |
| `build_aos_pdf` | Dark background page template | none | 2026-09-24 |
| `build_candy_pdfs` | ═══ AOS PDF ═══ | none | 2026-09-24 |
| `build_plain12_pdf` | (no docstring) | none | 2026-09-24 |
| `build_plain_pdf` | (no docstring) | none | 2026-09-24 |
| `build_seed` | build_seed  -  assemble the shippable method package (seed/) and seal it. | none | 2026-09-24 |
| `burns_verdict_enum` | burns_verdict_enum.py - verdict pseudo-enum normalizer for memory/burns/LEDGER.jsonl (AH13, 2026-09-30). | ref | 2026-09-30 |
| `cache_kpi` | CACHE KPI v0 (2026-09-22, mickey lane A3)  -  prompt-cache hit-rate per provider, read | none | 2026-09-22 |
| `capability_manifest` | Capability manifest  -  the present-tense shape of the framework. | none | 2026-08-07 |
| `caption_ledger_sha_check` | Recompute every caption-ledger have-row sha256 against disk bytes. | none | 2026-09-26 |
| `cascade_falsifier_run` | Cascade falsifier run (burn brief B2-113, 2026-09-26). | none | 2026-09-26 |
| `cathedral_build` | CATHEDRAL BUILDER  -  one engine, regions from module files (v1 hand-wire). | none | 2026-09-22 |
| `cathedral_eigen_map` | cathedral_eigen_map  -  render the in-game map FROM the curvature scan's eigen_centroids. | none | 2026-09-26 |
| `cathedral_smoke.js` | (js, not a Python tool) | - | - |
| `cathedral_walk` | CATHEDRAL WALK  -  play both contested descent orders against the wired world. | none | 2026-09-21 |
| `cathedral_wire_tavern` | Wire the tavern (dnd_classic_stub) into the live cathedral game. | none | 2026-09-21 |
| `census_collect` | census_collect.py - the --collect deep-check collectors (B2-365 split). | none | 2026-09-26 |
| `census_drift_patrol` | census_drift_patrol.py - test-census freshness tripwire (B2-215, 2026-09-26). | ref | 2026-09-29 |
| `census_patrol_selftest` | census_patrol_selftest.py - the census_drift_patrol CLI self-test (B2-248 split, 2026-09-26). | ref | 2026-09-29 |
| `chain_repair` | chain_repair  -  standing verb for the verkle chain race class. | ref | 2026-09-27 |
| `checkbox_receipt_gate` | checkbox_receipt_gate.py - standing check for checked rows without receipts | ref | 2026-09-26 |
| `classify_corpus` | Classify corpus  -  the auto-producer for the skill-ledger labeled_rows counter. | none | 2026-08-07 |
| `classify_pack` | Classify research-pack answers by topic -> knowledge base + training rows. | none | 2026-08-07 |
| `code_execution` | Sandboxed Python execution in a temp dir (no network intent). | none | 2026-08-10 |
| `cold_boot_test` | cold_boot_test  -  the ractor's overturning run, automated. | none | 2026-09-27 |
| `compaction_eval` | compaction_eval.py  -  context-compaction eval per the hermes PR #116246 bar, on a | none | 2026-09-20 |
| `compare_versions` | Cross-version statistical comparison tool. | none | 2026-08-08 |
| `concept_predictor` | concept_predictor  -  AF1 (2026-09-30) + AH16 grouped-split redesign. | ref | 2026-09-30 |
| `concept_span_check` | concept_span_check  -  AJ7 (2026-09-30): is the estate's concept space spanned | none | 2026-09-30 |
| `config_seal` | config_seal.py  -  checksum-sealed integrity register over configs/. | ref | 2026-09-29 |
| `coordinate_fleet` | Fold the operator's cross-window coordination directive onto the relation (bus + subchain). | none | 2026-08-14 |
| `corpus` | corpus -- read-only surfacing tools over the estate catalog (2026-09-18). | ref | 2026-09-26 |
| `corpus_diff` | corpus_diff  -  diff similarly-named files in a corpus, produce training data. | none | 2026-08-08 |
| `corpus_fts_rebuild` | corpus_fts_rebuild -- the one sanctioned writer for catalog/catalog_fts.sqlite. | ref | 2026-09-26 |
| `corpus_lens` | corpus_lens  -  run a corpus through bard + swarm-protocol analysis lenses. | none | 2026-08-08 |
| `corpus_lens_run` | corpus_lens_run  -  synchronously finish lens analyses to completion. | none | 2026-09-21 |
| `corpus_self_lens` | corpus_self_lens  -  run the 6 corpus lenses over MAG's OWN framework corpus, then | none | 2026-08-09 |
| `cost_rollup` | cost_rollup.py  -  one read-only rollup over every scattered cost surface. | ref | 2026-09-30 |
| `curvature_scan` | CATHEDRAL CURVATURE SCAN  -  the world as topology, measured with fundamental forms. | none | 2026-09-26 |
| `cycle_brief` | cycle_brief - the flywheel's morning composer (SNOWBALL_PLAN C1, 2026-10-01). | none | 2026-09-30 |
| `dem_to_board` | dem_to_board  -  terrain bridge: SRTM .hgt -> 64x64 water_graph board. | ref | 2026-09-29 |
| `demote_candidates` | demote_candidates.py - frontier-gap task-shape route for improve candidates (Q-049, 2026-09-28). | ref | 2026-09-28 |
| `derived_dag` | derived_dag - read-only DAG index over the estate's existing hash families. | none | 2026-09-28 |
| `description_pin` | description_pin.py  -  tool-description pinning gate. | ref | 2026-09-26 |
| `df_words.json` | (json, not a Python tool) | - | - |
| `dfhack` | DFHACK  -  the live colony overlay. Self-steal of the DFHack pattern. | ref | 2026-09-22 |
| `dirac_loop_shim` | dirac_loop_shim  -  import seam so script-mode tools (visor) can reach | none | 2026-09-27 |
| `doctrine_arbiter` | doctrine_arbiter v0 - doctrine is measured, not obeyed (R10, 2026-09-30). | ref | 2026-09-30 |
| `drift` | drift -- the metric-referent drift instrument (2026-09-18). | ref | 2026-09-26 |
| `drift_dashboard` | drift_dashboard -- render the teleo drift verdict history panel (B2-64). | ref | 2026-09-26 |
| `drift_pairs_stamp` | drift_pairs_stamp -- weekly auto-stamp of the teleological drift pairs (T1-T6). | ref | 2026-09-26 |
| `ds_workhorse` | ds_workhorse - the cheap-tier batch lane (2026-10-01, operator doctrine: | none | 2026-09-30 |
| `duel_harness` | Duel harness: one ask, two model families, one cheap judge (Mickey17 W3, 2026-09-29). | ref | 2026-09-30 |
| `duel_style_regression` | Duel style-control regression (Z18, 2026-09-30). | none | 2026-09-30 |
| `duty_fuzz` | duty_fuzz.py - duty-spec fuzz generator (THE 50 program, task 18, W4). | none | 2026-09-25 |
| `eastwest_thorn_20260920` | East/West ractor pairing on the DOE thorn kit + inroads play (RS pattern: | none | 2026-09-20 |
| `eigenmap_two_check` | eigenmap_two_check  -  position/distance/bearing sanity check on the data, | none | 2026-09-27 |
| `eigenmap_two_luau_test.luau` | (luau, not a Python tool) | - | - |
| `eigenmap_two_smoke.luau` | (luau, not a Python tool) | - | - |
| `eigenmap_two_smoke` | eigenmap_two_smoke  -  EXECUTE the shipped THE CATHEDRAL scripts headless | none | 2026-09-27 |
| `eigenmap_two_smoke_env.luau` | (luau, not a Python tool) | - | - |
| `enqueue_law` | enqueue_law.py - zombie-enqueue census + graveyard (Mickey17 W3J, 2026-09-29). | ref | 2026-09-29 |
| `env_contract` | env_contract -- the stolen MiMo env contract, estate-native (AC8 steal #1). | ref | 2026-09-30 |
| `envelope_harvest` | One-command envelope harvest for Task-agent fire data (B2-424). | none | 2026-09-26 |
| `estate_atlas` | !/usr/bin/env python3 | none | 2026-09-23 |
| `estate_cleanup` | estate_cleanup.py  -  known-junk enumerator and guarded cleaner. | ref | 2026-09-30 |
| `estate_env` | ESTATE ENV  -  the one canonical key loader (rib.md.record.v1 companion). | none | 2026-09-21 |
| `estate_index_dedup` | Estate-index mirror dedup: verify byte-for-byte duplication, then swap a pointer in. | ref | 2026-09-29 |
| `estate_query` | estate_query  -  the provenance join the estate never had (IMP4, AE5 wishlist #1). | ref | 2026-09-30 |
| `estate_smith_chart` | ESTATE SMITH CHART  -  health as /Gamma/ coordinates, not prose. | none | 2026-09-25 |
| `filesystem` | Filesystem tools jailed to config.FS_ROOTS. | ref | 2026-08-29 |
| `flashx_probe` | FlashX latency probe: glm-5.3-flashx vs glm-5.3-flash on the fleet's OpenRouter lane. | none | 2026-09-26 |
| `fold_mickey17` | fold_mickey17.py  -  deterministic fold of the Mickey 17 digestion wave. | none | 2026-09-25 |
| `fold_v2_covariance` | fold_v2_covariance.py  -  the covariance fold, applied to the fleet. | none | 2026-09-22 |
| `fossil_check` | fossil_check  -  the FOSSIL-IN-FEED arm, registry-driven. | ref | 2026-09-28 |
| `freshness_check` | freshness_check.py  -  boot-doc stale-trap gate. | ref | 2026-09-29 |
| `freshness_gate` | freshness_gate.py - freshness-receipts gate (MICKEY17 V2 owed item, t11b; hash binding t37). | ref | 2026-09-26 |
| `full_scan` | full_scan  -  the estate-wide semantic catalog churn (2026-09-23, "go wide"). | ref | 2026-09-25 |
| `fullsend_s2` | FULLSEND S2  -  union-fullsend season 2, opencode headless edition. | ref | 2026-09-22 |
| `game_module_dated_numbers` | game_module_dated_numbers.py - the dated-number tripwire for game-module lore. | none | 2026-09-26 |
| `gaming_corpus_pass` | gaming_corpus_pass  -  brief every orphaned game/tool page and every mag game engine | none | 2026-09-24 |
| `gap_sentinel` | gap_sentinel.py - estate metabolism gap sentinel (Mickey17 wave 3, 2026-09-29). | ref | 2026-09-29 |
| `gate_canary` | gate_canary.py - pre-push gate-liveness canary (Mickey17 W2, return 7/24). | ref | 2026-09-30 |
| `gate_digest` | Gate digest: the standing one-glance list of OPEN operator gates. | none | 2026-09-30 |
| `gen_artifact_lore` | Generate the DWARVEN pool region of roblox/src/shared/ArtifactLore.luau. | none | 2026-09-26 |
| `gen_df_luau_data` | Generate the DF-mined Luau data modules for THE MOUNTAIN's roblox build. | none | 2026-09-26 |
| `gen_worldgen_spheres` | Generate the SPHERES pool region of roblox/src/shared/Worldgen.luau. | none | 2026-09-26 |
| `ghost_tournament` | Ghost Tournament  -  8-hour unattended steering experiment marathon. | none | 2026-08-10 |
| `godot` | (dir, not a Python tool) | - | - |
| `gps_mcp` | (dir, not a Python tool) | - | - |
| `graph_heal` | graph_heal.py - knowledge-graph compaction pass v0 (Mickey17 W3, 2026-09-29). | ref | 2026-09-29 |
| `grave_classify` | grave_classify.py - one stable vocabulary for grave burial classifications. | ref | 2026-09-26 |
| `inbox_consume` | Consume verb for the shared-inbox event log (Mickey17 wave 3, 2026-09-29). | ref | 2026-09-29 |
| `index` | (dir, not a Python tool) | - | - |
| `k8s_water_sim` | k8s_water_sim  -  the water_graph as a k8s scheduler simulator (v0, 2026-09-30). | ref | 2026-09-30 |
| `knot_rehash_patrol` | knot_rehash_patrol.py  -  leaf-hash rehash patrol for the verkle knot chain | ref | 2026-09-30 |
| `knot_taming_night` | knot_taming_night.py  -  night-window knot tamer on LOCAL inference. | none | 2026-09-22 |
| `kv50_smith_chart` | KV50 SMITH CHART  -  the 50-wide lift mapped onto the smith chart. | none | 2026-09-21 |
| `kv_slot_pilot.md` | (md, not a Python tool) | - | - |
| `kv_slot_pilot` | KV slot cold store pilot (Mag Estate, lane A4). | none | 2026-09-22 |
| `lane_budget` | lane_budget.py - pre-bound metered budgets that HALT a running lane. | ref | 2026-09-29 |
| `lattice_build` | lattice_build.py  -  THE LATTICE: the estate map, warmed for hot-swap. | none | 2026-09-22 |
| `ldt_lattice` | ldt_lattice  -  V7: the LDT candidate-set lattice, v0 post-hoc projection. | ref | 2026-09-30 |
| `ldt_nearmiss` | ldt_nearmiss  -  IMP9: N4's near-miss adversarial split, raw vs projected. | ref | 2026-09-30 |
| `ldt_train` | ldt_train  -  Z13: the LDT v0 baseline control (no lattice), pure numpy. | ref | 2026-09-30 |
| `leave_dispatcher` | leave_dispatcher - the mates leave protocol driver, static-runner shape (X12, 2026-09-29/30). | none | 2026-09-29 |
| `ledger_append_gate` | ledger_append_gate -- pre-append schema gate for memory/burns/LEDGER.jsonl. | none | 2026-09-26 |
| `ledger_close_check` | ledger_close_check -- B2-203 one_line freshness re-check for LEDGER closes. | none | 2026-09-26 |
| `ledger_lock` | Single-writer lock + fsync append for shared JSONL ledgers. Stdlib only, Windows-safe. | none | 2026-09-27 |
| `ledger_registry` | ledger_registry.py  -  one mount table for every hash-chain on the estate. | ref | 2026-09-29 |
| `ledger_spot_patrol` | ledger_spot_patrol -- WARN-ONLY claim-vs-artifact spot checks on LANDED ledger rows. | none | 2026-09-27 |
| `legality_dataset` | legality_dataset  -  W3K: LDT legality dataset over the REAL water-graph engine. | ref | 2026-09-29 |
| `legality_propagator` | legality_propagator  -  Y10: the deterministic legality oracle, NO engine. | ref | 2026-09-30 |
| `lens` | lens.py  -  the lens socket (LENS RIB v3, step 2.5). | ref | 2026-09-20 |
| `lensing_ask` | lensing_ask - the MC6 paid-ask carrier (THE MOUNTAIN CLIMB Phase 2). | none | 2026-09-30 |
| `letter_salon_20260920` | Letter salon  -  the operator's 9/20 handwritten journal through the living chairs. | none | 2026-09-20 |
| `librarian_backfill_20260927` | librarian_backfill_20260927 -- resolve the retired librarian v1 backlog to names (Q6). | none | 2026-09-26 |
| `light_walk` | LIGHT WALK  -  walk the old paths wide through the salon lightmap. | none | 2026-09-22 |
| `llamacpp` | (dir, not a Python tool) | - | - |
| `local_bench` | Local model benchmark  -  find what the local Ollama models can be good at. | none | 2026-08-07 |
| `luau_lint` | luau_lint  -  headless structural checks for the mountain's Luau tree. | none | 2026-09-26 |
| `mcp_pin` | mcp_pin -- MCP tool schema pinning + drift alarm (2026-09-25). | ref | 2026-09-25 |
| `md_record_audit` | MD RECORD AUDIT v2  -  tests the drug-lab checklist (ALCOA+), not file counts. | none | 2026-09-27 |
| `md_record_seal` | md_record_seal  -  teeth for rib.md.record.v1 (2026-09-21). | ref | 2026-09-26 |
| `memory_gauge` | nightly memory gauge (ask A8). | none | 2026-09-22 |
| `meter_patrol` | meter_patrol.py - dated witness meters for the institutional cluster (B2-469, 2026-09-26). | ref | 2026-09-26 |
| `meters_nightly` | NIGHTLY METERS WRAPPER  -  runs the fleet meters and seals what it writes. | none | 2026-09-22 |
| `mickey17_v2_fold` | mickey17_v2_fold.py  -  deterministic fold sections for MICKEY-17 v2.1. | none | 2026-09-25 |
| `mimo_census` | Census for the XiaomiMiMo/MiMo-V2.6-RL-oss dataset (HF, Apache 2.0). | none | 2026-09-30 |
| `mimo_watch` | MIMO WATCH - 24/7 frontier-window watch on the MiMo V2.6 free lane. | ref | 2026-09-26 |
| `model_bakeoff` | model_bakeoff  -  50 concurrent calls across the free model-lane wall (2026-09-23, | none | 2026-09-24 |
| `mountain_check` | (file, not a Python tool) | - | - |
| `mountain_digflood` | mountain_digflood  -  the DFHack moment: dig the breach, watch the flood. | ref | 2026-09-30 |
| `mountain_gods_number` | mountain_gods_number  -  God's Number for OUR mountain (W3 lane, 2026-09-29). | ref | 2026-09-29 |
| `mountain_legends` | mountain_legends  -  Legends Mode for the Mountain (LM5, 2026-09-30). | none | 2026-09-30 |
| `mountain_liquids` | mountain_liquids  -  DFHack's liquids plugin, THROUGH THE LAW (LM3, 2026-09-30). | ref | 2026-09-30 |
| `mountain_reveal` | mountain_reveal  -  DFHack reveal/prospect for the Mountain (LM2, 2026-09-30). | ref | 2026-09-30 |
| `mountain_units` | mountain_units  -  DFHack-style `units` for the Mountain fish school (LM4). | ref | 2026-09-30 |
| `ocean_v2_pilot` | OCEAN v2 pilot  -  measure the BERNAYS chair's Big Five from its corpus (not asserted). | none | 2026-09-20 |
| `ollama_to_lmstudio.mjs` | (mjs, not a Python tool) | - | - |
| `one_pipe` | (no docstring) | none | 2026-08-07 |
| `openrouter_free_gate` | openrouter_free_gate -- verify-then-add gate for :free rotation ids (B2-295). | none | 2026-09-27 |
| `operator_go` | operator_go - canonical reader for watch/inbox/OPERATOR_GO.jsonl (B2-425). | ref | 2026-09-26 |
| `oracle_calibration` | THE 50, W6 item 29: oracle calibration harness (G31 recipe). | none | 2026-09-19 |
| `oral_law_dedupe` | oral_law_dedupe.py - W3 consolidation pass over the oral-law index (W3S, 2026-09-29). | ref | 2026-09-29 |
| `orphan_census` | Orphan census for the shared inbox (Mickey17 wave 3, 2026-09-29). | ref | 2026-09-29 |
| `ox_heartbeat` | ox_heartbeat  -  one-shot ox-alpha availability probe (Mag Estate lane A5, "ox heartbeat re-arm"). | none | 2026-09-22 |
| `pain_replication` | (dir, not a Python tool) | - | - |
| `path_lint` | path_lint  -  detect workspace-path strays (self-gap pass 3 law: absence-claims | none | 2026-09-20 |
| `persona_grid` | persona_grid.py  -  the Liu Hui persona-conditioning grid, generated + scored locally. | none | 2026-09-19 |
| `pile_classify` | Pile classifier  -  the long overnight classification job. | ref | 2026-09-25 |
| `pointer_rot_check` | Re-resolve burn-wave file:line pointers against current bytes and flag rot. | none | 2026-09-26 |
| `policy_eval_schema_check` | THE 50 W6 T30: worked-example validation for the G06 policy-eval wire schema. | none | 2026-09-19 |
| `precommit_secret_check` | precommit_secret_check  -  staged-secret gate (P0 containment, audit 2026-09-30 #1). | none | 2026-09-30 |
| `prepush_paths_changed` | prepush_paths_changed -- the changed-path decision as one helper (B2-272). | ref | 2026-09-27 |
| `pricing_diff` | PRICING DIFF CRON  -  cached-vs-compute token ratios across the four providers, daily. | none | 2026-09-22 |
| `probe20_run` | probe20_run -- series runner for the steering drift pairs (2026-09-26). | none | 2026-09-27 |
| `probe20_stamp` | probe20_stamp -- the probe20-to-dashboard stamp bridge (B2-64 board). | none | 2026-09-26 |
| `probe20_tasks` | probe20_tasks - the 20 labeled verdict tasks (seed, v1) for probe20_run. | none | 2026-09-27 |
| `prompt_compiler` | prompt_compiler - deterministic reduction passes for verbose prompts. | none | 2026-09-28 |
| `provider_error_tally` | Provider-error tally for a ZCode agent session family. | ref | 2026-09-26 |
| `provider_snapshot_differ` | provider_snapshot_differ - week-over-week differ for provider-probe snapshots. | none | 2026-09-26 |
| `pupeteer_gauntlet` | Puppeteer gauntlet  -  "DFHack the local mind" demo. | ref | 2026-08-10 |
| `qknot_b1` | B1  -  the Q-knot logical cycle (operator: "the number the door displays"). | none | 2026-09-20 |
| `queue_close` | queue_close -- the queue-owner close verb (LINKS-328's missing drain half). | ref | 2026-09-30 |
| `queue_dupes_check` | queue_dupes_check -- the queue double-claim census as a gate (B2-486). | ref | 2026-09-27 |
| `queue_row_census` | Queue row census + normalizer + tripwire (B2-488, 2026-09-26). | none | 2026-09-26 |
| `quota_ledger` | quota_ledger.py  -  window-quota ledger v0 (2026-09-30). | ref | 2026-09-30 |
| `quota_ledger_report` | quota_ledger_report.py  -  receipt-side evidence + rendering for the | none | 2026-09-30 |
| `quote_audit_wide` | QUOTE_AUDIT_WIDE 2026-09-25 - byte-grep audit of quote fields. | none | 2026-09-27 |
| `quote_audit_wide_progress.log` | (log, not a Python tool) | - | - |
| `quote_gate` | quote_gate.py - verbatim-quote gate over a cited source file. | ref | 2026-09-26 |
| `quote_hitrate` | quote_hitrate.py - standing verbatim-quote hit-rate over estate quote fields. | ref | 2026-09-26 |
| `realmd_client` | realmd_client.py - pure-stdlib SRP6 client that logs into the estate's realmd (LW4, 2026-09-30). | ref | 2026-09-30 |
| `rebuild_grounding_wave_md` | Rebuild dashboard/static/grounding_wave.md from watch/GROUNDING_WAVE.jsonl. | none | 2026-09-25 |
| `receipt_body_fts` | receipt_body_fts -- full-text index over watch/inbox receipt BODIES (Q4, 2026-09-27). | none | 2026-09-26 |
| `receipt_xref_gate` | receipt_xref_gate.py - dead-citation gate for watch/inbox receipts (W2, 2026-09-29). | ref | 2026-09-29 |
| `refold_gate` | refold_gate.py - fold-order mutation tripwire (B2-328, 2026-09-26). | ref | 2026-09-29 |
| `regen_front_door` | Regenerate the front door (docs/FRAMEWORK_LOAD.md) from live truth. | ref | 2026-09-29 |
| `research` | research -- read-only surfacing tools over the fleet's research corpus. | ref | 2026-09-26 |
| `research_mine` | research_mine.py  -  run estate research through DeepSeek for grounded | none | 2026-09-23 |
| `research_rig` | Research rig  -  multi-tier research with right-sized output (T0/T1). | none | 2026-08-07 |
| `restore_guard` | restore_guard.py - stale-base whole-file restore tripwire (B2-343, 2026-09-26). | ref | 2026-09-26 |
| `rib_check_game_loop` | RIB-debug the frontier game loop: prove play == building (world grows, root verifies). | none | 2026-08-14 |
| `roblox_npc_gateway` | roblox_npc_gateway  -  the fleet's brain, served to the world. | none | 2026-09-28 |
| `rollup_delta` | rollup_delta.py - rollup metabolism meter (hydrology Z17, 2026-09-29). | ref | 2026-09-30 |
| `rule_parity` | rule_parity v0  -  GDScript offline rules vs Python server rules, measured. | ref | 2026-09-30 |
| `rule_parity_out` | (dir, not a Python tool) | - | - |
| `rumor_drill` | rumor_drill  -  the seeded-rumor propagation drill (BREAD_PANIC lens, GO 2026-09-27). | none | 2026-09-28 |
| `saturation_fourcond` | Four-condition refusal-scope falsifier (I-11)  -  Bernays chair. | none | 2026-09-20 |
| `scs` | SCS scorer: Jensen-Shannon divergence over choice sets. | none | 2026-09-19 |
| `seat_law_gate` | Seat law gate - PreToolUse hook enforcing the seat's own laws at the tool path. | none | 2026-09-29 |
| `seat_law_postgate` | Seat law post-gate - PostToolUse hook: gate .dwf.ts files after partial Edits. | none | 2026-09-29 |
| `secret_gate` | secret_gate - repo secret-scan gate (PACK_SECRET_GATE_20260926 section 4). | ref | 2026-09-27 |
| `secret_gate_rules` | secret_gate_rules - rule table, thresholds and block sets for the secret gate. | none | 2026-09-27 |
| `secret_gate_scan` | secret_gate_scan - scanning core for the secret gate (file/tree/history). | ref | 2026-09-28 |
| `seed_mcp` | seed_mcp.py - MCP server that serves the SEED-RIB (B2-181, 2026-09-26). | ref | 2026-09-29 |
| `seed_mcp_cold_client` | seed_mcp_cold_client.py - the B2-181 falsifier driver (2026-09-26). | ref | 2026-09-26 |
| `seed_paired_uplift` | Seed-paired uplift harness with the TARA gate (law D executor). | ref | 2026-09-26 |
| `seed_rib` | seed_rib.py - SEED-RIB v0 generator + rebuild verifier (B2-180, 2026-09-26). | ref | 2026-09-29 |
| `seed_salon` | seed_salon  -  multi-model salon on the seed's enhancement questions (2026-09-25). | none | 2026-09-25 |
| `seed_v2` | seed_v2  -  build the shippable seed so it BOOTS COLD outside the estate. | none | 2026-09-26 |
| `sense_tools` | Sense tools for MCP  -  voice packets + image-whisper scan for dumb bodies. | ref | 2026-08-28 |
| `session_cards` | session_cards.py - one .card.json per human session under memory/biography/cards/ (Q-003, 2026-09-28). | none | 2026-09-28 |
| `shell` | Allowlisted shell commands only. | ref | 2026-09-26 |
| `skills_catalog` | skills_catalog  -  generate docs/SKILLS_CATALOG.md from every installed SKILL.md. | none | 2026-09-29 |
| `skills_lint` | skills_lint  -  contract checker for every SKILL.md on the shelf. | ref | 2026-09-29 |
| `smoke_import` | (no docstring) | none | 2026-08-07 |
| `spawn_gpipe` | Ensure project root is on sys.path so `mag` package imports work when run from tools/ | none | 2026-08-07 |
| `spec_execute` | Spec-execute POC  -  the "frozen state → penny spec → cheap execute" loop. | none | 2026-08-07 |
| `state_asof` | STATE ASOF  -  the time-machine query for the estate's record. | none | 2026-09-21 |
| `steal_gdrive` | steal_gdrive  -  yoink a link-shared Google Drive folder corpus without auth. | none | 2026-08-08 |
| `stealth_driver` | stealth_driver  -  the 24/7 useful-work loop for the free/stealth lanes. | ref | 2026-09-29 |
| `stealth_fanout` | stealth_fanout  -  Mickey17-style concurrent mining across ALL steal models. | ref | 2026-09-29 |
| `stealth_fanout_wave2` | stealth_fanout wave 2  -  missed items on the two PROVEN lanes only. | none | 2026-09-28 |
| `stealth_sweep` | stealth_sweep  -  burn the free wall daily: live-fire OpenRouter's :free and :stealth | none | 2026-09-24 |
| `steer_all` | steer_all  -  control ALL seats (copilot, grok, chatgpt, the swarm) from ONE terminal. | none | 2026-08-14 |
| `steer_compare` | Steer Compare  -  run identical steering experiments across providers. | none | 2026-08-07 |
| `steer_grok_1m` | Give grok the 1M-context build context via the shared steer bus (relational). | none | 2026-08-14 |
| `steer_grok_whole` | Hand grok the WHOLE system dossier via the shared steer bus (relational). | none | 2026-08-14 |
| `steer_read` | steer_read  -  read the operator STEER channel (watch/inbox/STEER.md). | ref | 2026-09-29 |
| `stills_xai` | Scene-still generator for the Living Mud (and any corpus game). | none | 2026-09-23 |
| `swarm_tools` | tools/swarm_tools  -  the NPC toolbelt exposed to the agent's TOOL LOOP (sense/pheromone/blackboard). | ref | 2026-08-13 |
| `tabfm_try` | AH9  -  google/tabfm-1.0.0-pytorch local CPU trial on the estate's own table. | none | 2026-09-30 |
| `task_wall` | task_wall  -  the standing concurrent task engine (2026-09-23, operator: "explode our | none | 2026-09-24 |
| `test_pipe_api` | (no docstring) | none | 2026-08-07 |
| `thought_quantizer` | thought_quantizer  -  the standing compiler for the tiered instruction packs. | ref | 2026-09-29 |
| `thrash_meter` | thrash_meter -- the multi-front thrash instrument (THE 50 / W6 / T27, 2026-09-19). | none | 2026-09-19 |
| `tier_probe` | Tier probe  -  DeepSeek right-sizing A/B (assumption testing). | ref | 2026-08-07 |
| `tip_witness` | tip_witness.py - external witness for the verkle chain tip (W3, 2026-09-30). | ref | 2026-09-30 |
| `topic_research` | Topic-driven research runner  -  the preemptive-steal loop (tesuji-everywhere). | none | 2026-08-07 |
| `track_bpm` | track_bpm  -  pure-python BPM detection for PRIVLIDGE music wiring. | none | 2026-09-25 |
| `transport_precheck` | transport_precheck.py  -  research-lane preflight transport check (B2-327). | ref | 2026-09-27 |
| `typed_scorer` | typed_scorer.py  -  System-One style typed-decision scorer on the local shelf. | none | 2026-09-20 |
| `verb_anchor` | verb_anchor -- anchor the verb kifu tail into the verkle chain (THE 50 / W9 / T43, 2026-09-19). | none | 2026-09-19 |
| `verify_lyapunov_decode_20260921` | Receipts for the Lyapunov + dimension-lift decode (2026-09-21). | none | 2026-09-21 |
| `verkle_dangling_repair` | verkle_dangling_repair.py  -  marker-backfill repair for dangling chain rows. | ref | 2026-09-29 |
| `verkle_restore_prep` | verkle_restore_prep.py  -  Q-001 restore prep for hash-recoverable dangling rows. | ref | 2026-09-29 |
| `violation_ratchet` | violation_ratchet.py  -  fingerprint-ratcheted violation gate over estate code. | ref | 2026-09-29 |
| `visor` | STATELESS VISOR: cross-session, cross-job observability board. | ref | 2026-09-27 |
| `wandr_selfeval` | wandr_selfeval.py -- WANDR-shaped estate self-eval (MICKEY-17 v2 GO list item 6). | none | 2026-09-26 |
| `wandr_selfeval_task.json` | (json, not a Python tool) | - | - |
| `wave_lift` | WAVE LIFT  -  the estate's own 50-wide executor. Hardy by design. | none | 2026-09-22 |
| `weights_consolidate` | WEIGHTS CONSOLIDATE  -  one tracked home for all model weights. | none | 2026-09-22 |
| `workflow_gate` | Workflow gate: fleet dogfood enforcement for dynamic-workflow scripts. | ref | 2026-09-29 |
| `x_churn_cli` | x_churn_cli  -  the SD-seat batch driver: 20 Grok-CLI queries, one fresh headless | none | 2026-09-23 |
| `x_churn_grok` | x_churn_grok  -  mine @NachoQuixotic's timeline for posts MISSING from the estate | none | 2026-09-23 |
| `x_churn_seeds` | x_churn_seeds  -  semantic adjacency churn: feed the estate's known posts to the | none | 2026-09-23 |
| `x_fresh_start` | (dir, not a Python tool) | - | - |
| `x_radar_backfill` | x_radar_backfill.py - x_radar run-history census + HOLES stanza writer (Mickey17 W3, 2026-09-29). | none | 2026-09-29 |
## 2. mag/ modules: load-bearing vs dormant

Fresh mtime check this session (os.stat over 1,080 .py, __pycache__ excluded). The named audits this rides on: `watch/inbox/ATLAS_SELF_STEAL_20260927.md` (the self-steal audit: the org machines, the L0-L6 stack, the leak law, three load-bearing gaps) and `watch/inbox/mountain_climb/SHERPA_DOSSIER.md` (landed 2026-09-30, the freshest per-organ PROVEN / PARTIAL / DORMANT audit with receipts). Byte view tonight:
| Bucket (mtime age) | Files |
|---|---|
| <=48h (live front) | 100 |
| 3-7d | 98 |
| 8-14d | 11 |
| 15-30d | 180 |
| 30-60d | 691 |
| >60d (dormant tail) | 0 |
| TOTAL mag .py | 1080 |
| .bak parked in mag/ | 17 |
| with tests/ reference | 472 (44%) |

Touched within 7 days (198 files):
- `mag/_consensus_witness.py` (2026-09-26)
- `mag/_flag_dangling_20260925.py` (2026-09-26)
- `mag/_flag_dangling_264d0ba3.py` (2026-09-26)
- `mag/act.py` (2026-09-29)
- `mag/afk_cadence.py` (2026-09-26)
- `mag/afk_loop.py` (2026-09-28)
- `mag/afk_orchestrator.py` (2026-09-26)
- `mag/agent_cli.py` (2026-09-30)
- `mag/agent_state.py` (2026-09-29)
- `mag/anchor_prose_acquire.py` (2026-09-30)
- `mag/ancient_engineering_acquire.py` (2026-09-30)
- `mag/api_gateway.py` (2026-09-26)
- `mag/ask_router.py` (2026-09-26)
- `mag/attention_ranker.py` (2026-09-29)
- `mag/audit_log.py` (2026-09-25)
- `mag/biography.py` (2026-09-29)
- `mag/brief_local.py` (2026-09-26)
- `mag/cache_map.py` (2026-09-30)
- `mag/cache_router.py` (2026-09-25)
- `mag/capability_steal.py` (2026-09-26)
- `mag/catalog_freshness.py` (2026-09-26)
- `mag/catalog_rebuild.py` (2026-09-26)
- `mag/catalog_rescan.py` (2026-09-26)
- `mag/catalog_scan.py` (2026-09-26)
- `mag/catalog_tags.py` (2026-09-28)
- `mag/census_liveness.py` (2026-09-26)
- `mag/chain_guard.py` (2026-09-26)
- `mag/chan.py` (2026-09-29)
- `mag/chat_source.py` (2026-09-30)
- `mag/child_development_acquire.py` (2026-09-30)
- `mag/chord_triangulate.py` (2026-09-30)
- `mag/claritas.py` (2026-09-24)
- `mag/compass.py` (2026-09-26)
- `mag/compute_reconcile.py` (2026-09-26)
- `mag/computing_history_acquire.py` (2026-09-30)
- `mag/constants.py` (2026-09-29)
- `mag/constitutional_critique.py` (2026-09-26)
- `mag/context_pack.py` (2026-09-30)
- `mag/cooker.py` (2026-09-24)
- `mag/corpus_acquire.py` (2026-09-30)
- `mag/corpus_acquire_prove.py` (2026-09-29)
- `mag/corpus_archive_acquire.py` (2026-09-29)
- `mag/corpus_archive_check.py` (2026-09-28)
- `mag/corpus_arxiv_register.py` (2026-09-29)
- `mag/corpus_cite_promote.py` (2026-09-29)
- `mag/corpus_gap_repack.py` (2026-09-28)
- `mag/corpus_gap_research.py` (2026-09-28)
- `mag/corpus_gutenberg_truth.py` (2026-09-28)
- `mag/corpus_land.py` (2026-09-29)
- `mag/corpus_lead_verify.py` (2026-09-28)
- `mag/corpus_map_backfill.py` (2026-09-29)
- `mag/corpus_nonanswer.py` (2026-09-28)
- `mag/corpus_reconcile.py` (2026-09-29)
- `mag/corpus_salvage.py` (2026-09-28)
- `mag/corpus_salvage_prove.py` (2026-09-28)
- `mag/corpus_selfsteal.py` (2026-09-29)
- `mag/corpus_selfsteal_prove.py` (2026-09-29)
- `mag/cost_truth.py` (2026-09-26)
- `mag/daemon.py` (2026-09-26)
- `mag/dedupe_index.py` (2026-09-30)
- `mag/dirac_loop.py` (2026-09-27)
- `mag/doctor.py` (2026-09-30)
- `mag/dormant.py` (2026-09-26)
- `mag/effect_broker.py` (2026-09-30)
- `mag/env_redirect.py` (2026-09-26)
- `mag/estate_bridge.py` (2026-09-29)
- `mag/events_key_schema.py` (2026-09-26)
- `mag/events_scan.py` (2026-09-26)
- `mag/failure_kb.py` (2026-09-26)
- `mag/feedback.py` (2026-09-29)
- `mag/field_flow.py` (2026-09-30)
- `mag/flock_positive.py` (2026-09-30)
- `mag/flock_positive_ab.py` (2026-09-30)
- `mag/free_tier.py` (2026-09-26)
- `mag/frontier_salon.py` (2026-09-28)
- `mag/frontier_salon_cli.py` (2026-09-28)
- `mag/fuel_feed.py` (2026-09-26)
- `mag/game_brawl.py` (2026-09-30)
- `mag/game_campaign.py` (2026-09-29)
- `mag/game_flow.py` (2026-09-30)
- `mag/gene_pool_feeder.py` (2026-09-30)
- `mag/ghost.py` (2026-09-26)
- `mag/governor_autorun.py` (2026-09-26)
- `mag/gpipes.py` (2026-09-27)
- `mag/gpu_ghost.py` (2026-09-26)
- `mag/grok_warm_rib.py` (2026-09-30)
- `mag/gwap_mud.py` (2026-09-29)
- `mag/gwap_payload.py` (2026-09-29)
- `mag/gwap_to_gps.py` (2026-09-29)
- `mag/head_museum.py` (2026-09-30)
- `mag/health.py` (2026-09-26)
- `mag/hermes_warm_boot.py` (2026-09-30)
- `mag/holdings_audit.py` (2026-09-30)
- `mag/hydrology.py` (2026-09-30)
- `mag/icon_drop.py` (2026-09-26)
- `mag/improve.py` (2026-09-29)
- `mag/intervention_gate.py` (2026-09-25)
- `mag/key_law.py` (2026-09-24)
- `mag/knot_untangle.py` (2026-09-30)
- `mag/lane_cadence.py` (2026-09-26)
- `mag/lane_effort.py` (2026-09-25)
- `mag/lane_probe.py` (2026-09-24)
- `mag/lane_runner.py` (2026-09-27)
- `mag/lane_salon.py` (2026-09-26)
- `mag/lane_supervisor.py` (2026-09-25)
- `mag/lanes.py` (2026-09-26)
- `mag/legacy_audit.py` (2026-09-26)
- `mag/lifecycle.py` (2026-09-26)
- `mag/link_library.py` (2026-09-29)
- `mag/links_sha_ratchet.py` (2026-09-26)
- `mag/links_split_gate.py` (2026-09-26)
- `mag/loop_breaker.py` (2026-09-26)
- `mag/mcp_http.py` (2026-09-29)
- `mag/mcp_server.py` (2026-09-29)
- `mag/moonshot_engine.py` (2026-09-30)
- `mag/naval_engineering_acquire.py` (2026-09-30)
- `mag/naval_engineering_land.py` (2026-09-30)
- `mag/no_win.py` (2026-09-27)
- `mag/ntrs_acquire.py` (2026-09-30)
- `mag/ocean_instrument_calibration.py` (2026-09-30)
- `mag/ocean_model_mind.py` (2026-09-30)
- `mag/ocean_percentile.py` (2026-09-30)
- `mag/ocean_persona.py` (2026-09-30)
- `mag/offerings.py` (2026-09-26)
- `mag/openclaw_catalog.py` (2026-09-29)
- `mag/orchestrator.py` (2026-09-26)
- `mag/organ_map.py` (2026-09-29)
- `mag/party_subchain.py` (2026-09-30)
- `mag/paste_pipeline.py` (2026-09-26)
- `mag/percolator.py` (2026-09-30)
- `mag/percolator_heal_test.py` (2026-09-30)
- `mag/perplexity_research.py` (2026-09-25)
- `mag/persona_priorart_acquire.py` (2026-09-30)
- `mag/phone_relay.py` (2026-09-25)
- `mag/physical_compute_acquire.py` (2026-09-30)
- `mag/platform_kill.py` (2026-09-26)
- `mag/ponytail_audit.py` (2026-09-29)
- `mag/power.py` (2026-09-26)
- `mag/probe_route.py` (2026-09-24)
- `mag/process_supervisor.py` (2026-09-26)
- `mag/prompt_lance.py` (2026-09-27)
- `mag/proof.py` (2026-09-30)
- `mag/prose_census.py` (2026-09-28)
- `mag/queue_gate.py` (2026-09-26)
- `mag/quorum_window.py` (2026-09-26)
- `mag/ractor_ocean_bridge.py` (2026-09-30)
- `mag/ractor_selfsteal_seeds.py` (2026-09-30)
- `mag/rails.py` (2026-09-29)
- `mag/realign.py` (2026-09-29)
- `mag/release_registry.py` (2026-09-26)
- `mag/research_fanout.py` (2026-09-26)
- `mag/rib_bus.py` (2026-09-30)
- `mag/rib_cache.py` (2026-09-30)
- `mag/river.py` (2026-09-30)
- `mag/roadmap_runner.py` (2026-09-29)
- `mag/rotation_harness.py` (2026-09-26)
- `mag/router.py` (2026-09-28)
- `mag/run_trail.py` (2026-09-28)
- `mag/runtime_policy.py` (2026-09-26)
- `mag/saelis_room.py` (2026-09-26)
- `mag/scale_salon.py` (2026-09-26)
- `mag/seal.py` (2026-09-30)
- `mag/seat_corpus.py` (2026-09-29)
- `mag/seat_registry.py` (2026-09-26)
- `mag/section_stream.py` (2026-09-30)
- `mag/session_state_brief.py` (2026-09-26)
- `mag/shape_map.py` (2026-09-27)
- `mag/shared_surface.py` (2026-09-29)
- `mag/siege_castle_fiction.py` (2026-09-30)
- `mag/skill_ledger.py` (2026-09-26)
- `mag/skill_lifecycle.py` (2026-09-25)
- `mag/skills_pack.py` (2026-09-29)
- `mag/source_trace.py` (2026-09-26)
- `mag/sovereign_handshake.py` (2026-09-30)
- `mag/spider.py` (2026-09-28)
- `mag/spore_seed.py` (2026-09-25)
- `mag/subscriptions.py` (2026-09-26)
- `mag/surface_rebuild.py` (2026-09-29)
- `mag/swarm_cycle.py` (2026-09-28)
- `mag/swarm_worker.py` (2026-09-26)
- `mag/temperature_stack.py` (2026-09-26)
- `mag/token_chain.py` (2026-09-29)
- `mag/trajectory_step.py` (2026-09-30)
- `mag/trust_gate.py` (2026-09-25)
- `mag/trust_gate_audit_check.py` (2026-09-25)
- `mag/tts.py` (2026-09-26)
- `mag/usage_digest.py` (2026-09-26)
- `mag/verkle_compaction.py` (2026-09-30)
- `mag/verkle_knot.py` (2026-09-30)
- `mag/voice_handoff.py` (2026-09-29)
- `mag/water_computer.py` (2026-09-29)
- `mag/water_graph.py` (2026-09-30)
- `mag/win_powershell.py` (2026-09-26)
- `mag/window_audit.py` (2026-09-26)
- `mag/work_loop.py` (2026-09-26)
- `mag/worldgen.py` (2026-09-30)
- `mag/write_strip.py` (2026-09-25)
- `mag/x_oauth.py` (2026-09-30)

Oldest 6: __init__.py (2026-08-04), blast.py (2026-08-04), bonds.py (2026-08-04), chord_lens.py (2026-08-04), chronicle.py (2026-08-04), cli/__init__.py (2026-08-04)
## 3. Receipts (glob counts, 19:04 EDT)

- `watch/inbox/` root: **1,085 .md**
- `watch/inbox/last_mile_20260930/`: **183 entries** (146 .md + logs/raw json/py)
- `watch/inbox/mountain_climb/`: **17 entries** (15 .md + raw.json + fire log)
- Newest root receipts: `CYCLE_BRIEF_20260930.md`, `GATE_DIGEST.md` (17:25), `SNOWBALL_PLAN.md`, `QUOTA_LEDGER.md`, `DAY_SYNTHESIS_20260930.md`.

## 4. Test census (instrument + moment per B2-216)

- **Collected: 3,706 in 27.41s**, `pytest --collect-only -q`, this census session ~19:00 EDT 2026-09-30.
- Carrier bullet (working-tree AGENTS.md): **3,550 / 455 files**, census moment 2026-09-30T18:51Z (14:51 EDT). Delta +156 between 14:51 and 19:00 EDT = tonight's landings (40 commits today, 426 dirty paths at census). Not a contradiction: different moments, named.
- Executed sum: **3,679 passed** (full-suite run cited in HEAD commit 9791c757c, 18:38).
- tests/ holds **470 .py files** (`find`); collected-vs-files instruments differ (parametrize, conftest, helpers).

## 5. Git state

- Commits 2026-09-30 (to 18:38 HEAD): **40**; numstat agg **1,342 files, +263,087 / -465,896** (binaries excluded by numstat).
- Commits 2026-09-29: **52**; **1,899 files, +2,943,736** (the corpus-landing day).
- HEAD: `9791c757c` "FULL BURN STATE (operator: you havent set up the full burn...)".
- Working tree: **426 dirty paths** uncommitted (tonight's in-flight receipts and code).

## 6. Meters: current reads

- **Gates** (`watch/inbox/GATE_DIGEST.md`, regenerated 17:25 by tools/gate_digest.py): **OPEN 5 / CLOSED 1**. Open: Adam invite (no GitHub username), ZAI_Pro key rotation (7 leaked keys, provider-side only), Nous portal check (402s vs ~$171 rib arithmetic), offsite backup medium pick, verkle v2 flip (GO recommended, waiting quiet window). Closed: Phase-2 lensing GO (by `mountain_climb/THE_LENSING.md`).
- **Quota** (`watch/inbox/QUOTA_LEDGER.md`, live run 2026-09-30T21:07Z): 321 fires (288 done / 28 failed / 5 running); **6 wall moments, 24 coded 1302/1308 deaths**; peak 138 fires/5h and width 26 at 00:38Z; **current window GREEN** (75 fires/5h, 0 walls last hour); **day-shape verdict RED**. z.ai account wall 1310 resets 10-05. `logs/quota_state.json`: deepseek last_ok TRUE 22:53Z (678 calls today); z_ai (190), z_ai3 (356), ollama (630) last_ok FALSE.
- **Cost** (cost_rollup, IMP5, landed 09-30): **$135.71 lifetime**. Tonight frontier ~**$2.39-2.50 of $8 cap**: W4 Opus $0.69 (+$0.37 first fire), Nous volley 1 $0.89 + volley 2 $0.48, DeepSeek $0.0018 (ton proven, $0.0004/item).
- **Anomaly** (anomaly_flagger, IMP6): PROVEN; live run 2026-09-30T17:49Z **exit 1** with rows named, not hidden.
- **GPS ledger**: PROVEN instrument, still **TEST-DOUBLE** ($0 offline); no live production traffic; gwap->gps return leg unwired (`watch/inbox/TIE_IT_ALL_20260930.md` thin spot 1).
- **Smith chart organ gammas** (freshest file `ESTATE_SMITH_CHART_20260927.json`, 2026-09-27T01:07Z, ~3d stale: the nightly chart refresh has not re-run since): supervisor gamma 0.954 REFLECTING (83 reaper-enumerate-errors), deepseek lane DELIVERING (ok_ratio 1.0), zai3/ollama lanes REFLECTING, queue done:100 DELIVERING, handoffs 12 pending.
- **attention.md**: census patrol fired 09-30 08:30, COLLECT-DRIFT exit 1 (claim 3220 vs 3403 held, +183; carrier was refreshed same day to 3,550). Probe alarms: mistral DOWN, cerebras QUOTA-DEAD.

## 7. Running processes (wmic scan, 19:04 EDT)

- **ollama serve** + ollama llama-server (port 5894) + `tools/llamacpp/llama-server.exe` serving an .ollama blob (the local janitor lane).
- **Stealth driver x2**: `scripts/run_stealth_driver.py` under both `.venv\Scripts\pythonw.exe` AND a uv pythonw. Two simultaneous instances: seen, not judged; verify intended.
- **governor_autorun**: `mag.governor_autorun.autorun_loop(5.0)` live.
- **Hermes**: desktop suite (5 procs) + `hermes_cli.main gateway run` + 2 kernel runners. Dormant-but-dispatch-capable stance with the gateway actually up.
- **Mates**: 8/8 personas CLAIMED and RUNNING on the z.ai quota (remote lanes, not local PIDs; per FULL_BURN_STATE: first fire with auth fix, 9 laws, invisible wrapper).
- Foreign: fle_u1 `inspect eval` trio (different project, shares the box).
- Scheduled tasks all Ready: MagImproveDaily 10/1 08:00, MagCensusPatrolDaily 10/1 08:30, MagFtsIndexDaily 10/1 09:00; MagLeaveProtocolDaily last ran 09-30 08:00 (machinery green; first auto-fire failed at mate-model auth per SHERPA_DOSSIER; fixed per FULL_BURN_STATE).

## 8. CLIMB state (mountain_climb/INDEX.md + tonight's receipts)

- **Landed tonight:** all six Phase-0 dossiers (MC1 SHERPA 19,189B / MC2 GOALS 17,384B / MC3 GAP 4,478B / MC4 BIBLIOGRAPHY 15,030B / MC5 ROUTE_V0 27,945B / MC6 OPUS_BRIEF_SKELETON 14,831B; hashes in INDEX.md); **W4 Opus lensing RETURNED** ($0.69, claude-opus-5.5 via Nous, finish=length: verdict KEEP the baseline spine, TIGHTEN most sections); Phase-2 lensing GO gate CLOSED; AA1 refire TIMEOUT at $0 (lane closed as operator-decision); IMP5 cost + IMP6 anomaly meters landed; B2 event ring (64-slot) landed with the 3,679-pass run.
- **Building:** nothing inside mountain_climb/ itself. The live transform is **Phase 1**: the estate's own fleet adversarially reads ROUTE_V0 into v1, inside the FULL BURN (4 quotas: mates 8/8, Nous volley 2 complete, DeepSeek ton proven, local CPU).
- **Queued:** ROUTE v1 (skeleton section 4 slot stays empty until it exists); the assembled OPUS brief via `tools/lensing_ask.py` (fires ONLY on operator GO, the AA1 law); Nous next volleys; DeepSeek 52-question dogfood sweep ($0.0004/item); tomorrow's 08:00 / 08:30 / 09:00 tasks.

## Assembly note

Tables in sections 1-2 script-generated this session (ast + mtime + tests-text scan; scripts ran under `.venv/Scripts/python.exe`); prose sections hand-written from the receipts named inline. No test suite was executed by this census beyond `--collect-only`. Em-dash count: 0 (house law).
