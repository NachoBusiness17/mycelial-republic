# REBOOT PATCHES 2026-10-03: APPLY ORDER

Staged by Grok Bot overnight (operator-approved wave). The live tree was NOT modified:
mag/health.py, ghost.py, knot_at_close.py, verkle_knot.py, process_reaper.py and
loops_registry.py byte-match HEAD (re-checked 2026-10-04 05:00 ET).
RACTOR PASS 2026-10-04 08:35 ET (watch/inbox/ractor_engine/2026-10-04-reboot-patches/SYNTHESIS.md):
01 and 05 regenerated (two bugs fixed), apply order CHANGED (02 now goes last, after a
mag restart). Originals of 01/05/APPLY_ORDER kept in the staging worktree under
watch\inbox\ractor_engine\2026-10-04-reboot-patches\orig_20261003\.
Staging: worktree C:\Users\foste\Documents\projects\lsa_reboot_staging, branch
reboot-staging-20261003, changes staged in its index, no commits, no push.

| # | diff | files | what |
|---|------|-------|------|
| 01 | 01_janitor_limits.diff | mag/ghost.py, mag/janitor_governor.py (new), mag/loops_registry.py, tests/test_janitor_governor.py (new) | Janitor governor: stop file state\janitor.off (or MAG_JANITOR_DISABLED=1), STUCK after 3 consecutive failures (operator clear), re-arm only on a fresh recurrence, daily cap 12 (MAG_JANITOR_MAX_PER_DAY), paid providers downgraded to ollama unless MAG_JANITOR_ALLOW_PAID=1, fail closed on governor errors. Ractor fix: governor TERMINAL now includes orchestrator "died"/"stalled" (they sat pending 6 h). Mutating "verkle_audit --fix" quest removed (note-only). Loop registered in loops_registry. |
| 02 | 02_lazy_cage_doctor_reaper_linux.diff | mag/health.py, mag/process_reaper.py, tests/test_health_lazy_import.py (new) | CAGE_DOCTOR resolved lazily (cage_doctor_cmd() + module __getattr__). lifecycle.py, window_audit.py: call-time only, no change needed; guard.py broke only through health.py. Reaper Linux path via /proc (skips pid 1/self/parent); Linux live kill refused unless MAG_REAPER_LINUX_LIVE=1. |
| 03 | 03_janitor_knot_on_success.diff | mag/ghost.py, tests/test_janitor_knot_on_success.py (new) | Verkle fold moved from spawn time to janitor_governor.reconcile(): only status done AND non-empty output file. False spawn-time "autonomous_task_completed" event dropped. tension_index = full signature. Depends on 01. |
| 04 | 04_knot_at_close_dwf_filter.diff | mag/knot_at_close.py, tests/test_knot_at_close_filter.py (new) | workflow_child / dwf- sessions dropped by default (--include-workflow-children to restore). First-message query rewritten for the real schema (message.data $.role + part.data $.type/$.text); old query hit missing columns message.content/is_sidechain. No chain backup when 0 candidates. |
| 05 | 05_verkle_lock_namespace.diff | mag/verkle_knot.py, tests/test_verkle_lock.py, tests/test_verkle_lock_namespace.py (new) | Lock marker = "<pid> <ts> <host>|<pid-namespace>". PID probed only for a same-namespace marker, with psutil / OpenProcess (never os.kill on Windows). Foreign or legacy marker breaks only on 900 s mtime staleness. Ractor fix: the breaker re-reads the marker (or re-stats mtime) right before unlink, so a second waiter never deletes the lock a first waiter just re-took. |

## Before the reboot (already true)
state\knot_at_close.off exists (SYNTHESIS step 0). Leave it until step 4 verifies.

## Post-reboot steps (PowerShell, repo root)  [ORDER CHANGED 2026-10-04]
NOTE: mag/ is bind-mounted into mag-sovereign, so each apply is live in the cage at once
for NEW processes. Long-lived cage processes (ghost daemon pid 12, autorun, lane_runner)
keep the code they loaded at container start until `docker compose restart mag`.
WHY 02 MOVED LAST: the janitor loop runs inside the long-lived ghost daemon. If 02 lands
before that daemon reloads 01+03, its fresh agent children import the fixed health.py and
succeed, while the OLD in-memory loop still spawns them with no governor, no stop file
(state\janitor.off is ignored by old code), the paid deepseek tier, the verkle --fix
quest and spawn-time knots. So: 01, 03, 04, 05, operator restart, verify, then 02.
--ignore-whitespace is required for 01/02: live loops_registry.py and process_reaper.py
are CRLF while HEAD stores LF (content otherwise identical; verified byte-normalized).
MAG_JANITOR_* env switches only reach the cage ghost if set in the container env;
the stop file works on both sides (./state is bind-mounted to /app/state).

    cd C:\Users\foste\Documents\projects\local_sovereign_agent
    $P = "watch\inbox\reboot_patches_20261003"
    $py = ".venv\Scripts\python.exe"

1. Janitor limits, then dam the janitor
       git apply --ignore-whitespace --check "$P\01_janitor_limits.diff"; git apply --ignore-whitespace "$P\01_janitor_limits.diff"
       & $py -m pytest -q tests/test_janitor_governor.py          # expect 11 passed
       & $py -m mag.janitor_governor disable                      # creates state\janitor.off
       & $py -m mag.janitor_governor status                       # enabled=false
   Rollback: git apply -R --ignore-whitespace "$P\01_janitor_limits.diff" (only after 03 and 02 are reverted)

2. Knot at completion, success only (needs 01)
       git apply --check "$P\03_janitor_knot_on_success.diff"; git apply "$P\03_janitor_knot_on_success.diff"
       & $py -m pytest -q tests/test_janitor_knot_on_success.py tests/test_janitor_governor.py   # expect 15 passed
       & $py scripts\verify_verkle_full.py                        # 0 mismatch (53 dangling is the known baseline)
   Rollback: git apply -R "$P\03_janitor_knot_on_success.diff" (revert 03 before 01)

3. knot_at_close dwf filter + real first-message excerpt (host boot lane only)
       git apply --check "$P\04_knot_at_close_dwf_filter.diff"; git apply "$P\04_knot_at_close_dwf_filter.diff"
       & $py -m pytest -q tests/test_knot_at_close_filter.py tests/test_worldline_seed_gate.py    # expect 7 passed
       & $py mag\knot_at_close.py --skip-subagents --min-messages 5 --since 2026-09-11            # REPORT ONLY: 0 dwf candidates
       Then (operator) delete state\knot_at_close.off.
   Rollback: recreate state\knot_at_close.off; git apply -R "$P\04_knot_at_close_dwf_filter.diff"

4. Namespace-aware verkle lock
       git apply --check "$P\05_verkle_lock_namespace.diff"; git apply "$P\05_verkle_lock_namespace.diff"
       & $py -m pytest -q tests/test_verkle_lock.py tests/test_verkle_lock_namespace.py         # expect 8 passed
   Rollback: git apply -R "$P\05_verkle_lock_namespace.diff"

5. RESTART (operator call): reload 01+03+05 in the long-lived cage processes
       docker compose restart mag
       docker inspect -f '{{.State.StartedAt}}' mag-sovereign      # later than step 4 (UTC)
       docker exec -w /app mag-sovereign python -m mag.janitor_governor status   # enabled=false, why: stop file
   Do not continue to step 6 until both checks pass.

6. Lazy CAGE_DOCTOR + reaper Linux path (un-dams cage agent traffic)
       git apply --ignore-whitespace --check "$P\02_lazy_cage_doctor_reaper_linux.diff"; git apply --ignore-whitespace "$P\02_lazy_cage_doctor_reaper_linux.diff"
       & $py -m pytest -q tests/test_health_lazy_import.py        # expect 5 passed
       docker exec -w /app mag-sovereign python -c "import mag.health, mag.lifecycle, mag.window_audit, mag.guard"   # exit 0
       Then: one api agent task reaches done; reaper-enumerate-error rows per hour in logs\supervisor.jsonl fall to 0.
       EXPECT (not a regression): memory\runs\ghost\leak_report.jsonl starts getting a row per ghost
       cycle naming ~5 "leaks". Measured 2026-10-04 with the staged reaper in the cage: all six
       mag_launch children (backend.server, main.py api, mag.ghost, lane_runner, main.py
       autorun, monitor_lane) classify as leak. Report-only. NEVER set MAG_REAPER_LINUX_LIVE=1
       until the Linux classifier knows the mag_launch roster.
   Rollback: git apply -R --ignore-whitespace "$P\02_lazy_cage_doctor_reaper_linux.diff"

7. Open the governed janitor
       & $py -m mag.janitor_governor enable
       Watch one cycle: a failed task adds no autonomous- chain row; a janitor_settled row lands in
       memory\runs\ghost\autonomous_trail.jsonl when a spawned task ends.

8. & $py scripts\verify_verkle_full.py   after one concurrent host + cage write.

Full rollback: reverse order 02, 05, 04, 03, 01 with the same -R commands. NEVER leave 02
applied with 01 reverted: that is the ungoverned, un-dammed janitor. To stop the janitor
fast while 01 is live: & $py -m mag.janitor_governor disable (no restart needed).
Sequential apply 01, 03, 04, 05, 02 onto live HEAD acb1a0c1d verified clean (temp index,
2026-10-04 08:30 ET): resulting blobs identical to the staging index for all 13 files.
`git apply --check` on the live worktree (read-only): 01, 02 (--ignore-whitespace), 04, 05 clean.

## Test results (staging, Windows, .venv Python 3.11)
- Each new test was run before its patch and failed (02 reproduced the exact cage error:
  "FileNotFoundError: powershell.exe not resolvable ... (B2-375)"), then passed after.
- New tests: 01 10/10, 02 5/5, 03 4/4, 04 5/5, 05 6/6 (+ test_verkle_lock 1/1 updated).
- Ractor 2026-10-04 (staging): 01 11/11 (+ terminal-status drift test), 05 7/7 + 1/1 (+ lock
  re-take race test). All patch tests together: 35 passed. test_verkle*.py + test_ghost*.py:
  80 passed, 3 failed, all pre-existing (test_verkle_artifact x2 KeyError evidence,
  test_ghost::test_catalog_persists).
- Relevant subset (15 files): 117 passed, 2 failed, 3 errors. All 5 are pre-existing and
  identical before any patch: test_ghost::test_catalog_persists, test_reconnect_cage_first::
  test_stale_heartbeat_note_is_not_host_lab, 3x test_healthz_status AttributeError (worktree lacks runtime files).
- Verkle tests: 50 passed, 2 failed (test_verkle_artifact, KeyError 'evidence'): also fail without 05.
- Cage (read-only, staged sources piped via stdin, nothing written): live `import mag.health`
  fails with the powershell error; staged health.py imports OK; staged reaper enumerates 8 cage python procs.
- Real ZCode db (read-only): 0 dwf sessions selected; first-user excerpts 2,946 of 2,948 (was 0).
- Full suite: NOT completed under the 15-minute cap. Stopped at 05:20 ET after 15 min at 44 pct (stalled at 44 pct for 5+ min, likely a hanging test). Progress so far: 1809 passed, 39 failed, 3 errors, 21 skipped; 1 collection error (test_blade_templates: blade_buyer module absent in worktree). Failures were not triaged against a pre-patch baseline; run per-file with a timeout to localize.

## Ctrl-C lead (os.kill(pid, 0) on Windows), measured 2026-10-04
Isolated probe (prober in its own hidden console, throwaway python children only):
os.kill(child, 0) returned without error and did NOT deliver Ctrl-C, whether the child led its own
process group or not; the child ran to its timeout. os.kill(dead_pid, 0) also returned with no
error. Verdict: the "Ctrl-C common cause" (0xC000013A) is NOT supported by this mechanism. The real
defect: on Windows the old lock probe calls every dead pid ALIVE, so a dead host holder was only
ever cleared by the 900 s mtime rule. Patch 05 replaces the probe.

## Risks
- 02 un-dams all cage agent traffic (412-class). It goes LAST, after the step 5 restart
  (the old in-memory ghost loop ignores state\janitor.off). Keep the janitor off until step 7.
- 01 counts janitor "done" as success only if the output file is non-empty; the child still runs
  read_only (plan item b, pinned write path, NOT included), so expect fail_count to climb and
  signatures to go STUCK after 3. That is the intended safe state until plan b lands.
- 01 downgrades count>=10 quests from deepseek to qwen2.5-coder:7b (quality drop, $0).
- 05: a crashed cage holder blocks host writers for up to 900 s (TimeoutError after 60 s each).
  Old-code processes write untagged markers, which new code treats as foreign: restart writers.
- 02 Linux reaper classifier was written for Windows: report-only by default on purpose.
- Not included: plan items d (event triggers), f (governor_autorun dedupe), chain-backup pruning
  (operator-gated delete), read_only=False janitor seat.

## Full-suite failure triage (2026-10-04, 05:25 to 05:45 ET)
Method: mapped the -q progress characters of the stopped full run to the collection order
(deterministic: no random-order plugin) to get exact node IDs. Re-ran those IDs with
pytest-timeout 120 s in staging (patched) and in a clean detached worktree at the staging base
37e2fba7e (unpatched). Live tree not touched.

Result: NO failure is caused by any patch. No .diff changed.
- 38 IDs re-run: baseline 35 failed + 3 errors; staging 34 failed + 1 passed + 3 errors.
  FAILED/ERROR summary lines are identical on both trees except one (next item).
- tests/test_ah4_rib_fixes.py::test_warm_rib_text_live_tip_matches_the_file: ORDER/STATE-DEPENDENT,
  pre-existing. Reads memory/biography/verkle_tip.json, which a fresh worktree lacks
  (FileNotFoundError on baseline). Passes in staging only because earlier suite tests
  (rib_bus_*, memlang-*, castle-foundation, rib_os) appended 15 rows to the worktree's own chain
  during the full run. It failed in the full run itself too.
- tests/test_env_load_mistral_keys.py (4 tests): NOT re-run on purpose (they read ROOT/.env;
  worktrees have no .env). Pre-existing by inspection: no patch touches env loading.
- 3 errors: tests/test_healthz_status.py (module 'server' has no attribute 'app'): pre-existing.
- Flaky: none observed (the ah4 difference repeated 2 of 2 times on each tree).

Hung test at 44 pct: tests/test_improve_loop.py::test_improve_cycle_schema. It times out at
120 s on BOTH trees: republic_loop -> rib_os.step -> flex_test -> gap_analysis full-tree file scan
(staging stack) and a live Ollama urlopen (baseline stack). Pre-existing, environment-bound.
Suggest marking it slow or adding a timeout marker so the full suite can finish.

Live HEAD moved during the night (37e2fba7e -> 059411590, 15+ commits, none touching patched files).
All five diffs re-verified: sequential apply onto 059411590 clean (temp index).

Failing node IDs (from the stopped full run):
tests/test_ah2_proof.py::test_real_newest_seal_merkle
tests/test_ah4_rib_fixes.py::test_warm_rib_text_live_tip_matches_the_file
tests/test_ask_bank.py::test_only_ask_bank_modules_touch_the_bank
tests/test_catalog_tags.py::test_run_tags_writes_owner_column
tests/test_census_drift_patrol.py::test_cli_collect_names_the_zero_collect_instrument_gap
tests/test_cialdini_scanner.py::test_x_churn_read_path_flags_payload
tests/test_cialdini_scanner.py::test_scout_queue_gate_blocks_high_risk_payload
tests/test_cialdini_scanner.py::test_scout_queue_gate_passes_clean_finding
tests/test_conductor_eval.py::test_conductor_eval_passes_without_writing
tests/test_conductor_eval.py::test_conductor_eval_files_evidence
tests/test_container_setup.py::test_compose_binds_localhost_only
tests/test_context_pack_delivery.py::test_core_sections_survive_forced_shed_ladder
tests/test_context_pack_delivery.py::test_objective_is_bounded_in_tight_mode
tests/test_coordination.py::test_coordinate_dry_classify
tests/test_coordination.py::test_rest_coordination_smoke
tests/test_decision_framework.py::test_decide_includes_route_and_interference
tests/test_doctrine_arbiter.py::TestAnomalyCountsInstrument::test_clean_streams_vindicate_zero
tests/test_doctrine_arbiter.py::TestAnomalyCountsInstrument::test_anomalous_rows_count_and_expire
tests/test_dormant_gate_b2133.py::test_no_mag_lane_list_carries_a_currently_dormant_provider
tests/test_dormant_gate_b2521.py::test_no_straggler_serves_a_currently_dormant_provider
tests/test_env_contract.py::test_run_legality_judges_emits_and_feeds
tests/test_env_load_mistral_keys.py::test_env_declares_canonical_names_only
tests/test_env_load_mistral_keys.py::test_providers_yaml_name_resolves_exact_case
tests/test_env_load_mistral_keys.py::test_keys_json_manifest_names_resolve_exact_case
tests/test_env_load_mistral_keys.py::test_load_dotenv_sets_canonical_names
tests/test_env_redirect_tripwire.py::test_doctor_examine_aggregates_redirect_warnings
tests/test_events_key_schema.py::test_real_registry_covers_every_key_in_the_real_log
tests/test_fork_router.py::test_rest_fork_detect_and_route_envelope_include_fork
tests/test_gap_sentinel.py::test_cli_exit_codes
tests/test_gate_blocking_paths.py::test_checkbox_gate_blocks_unearned_flip
tests/test_gate_blocking_paths.py::test_checkbox_gate_exit2_on_missing_queue
tests/test_gate_blocking_paths.py::test_secret_gate_blocks_provider_shaped_secret
tests/test_gate_blocking_paths.py::test_secret_gate_exempts_masked_token
tests/test_gate_blocking_paths.py::test_secret_gate_passes_clean_file
tests/test_gate_blocking_paths.py::test_secret_gate_never_prints_secret_value
tests/test_ghost.py::test_catalog_persists
tests/test_gods_number.py::test_mountain_gods_number_golden
tests/test_grounding_chain.py::test_live_dead_child_end_to_end_injected_base
tests/test_headless.py::test_canonical_python_bypasses_venv_shim
tests/test_healthz_status.py::test_status_tracks_ok_flag
tests/test_healthz_status.py::test_breach_returns_503
tests/test_healthz_status.py::test_healthy_returns_200