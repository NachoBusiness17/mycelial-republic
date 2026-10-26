# LANE 7 — TEST REALITY AUDIT

**Date:** 2026-09-26
**Seat:** zcode (Sancho) — delegated lane
**Repo:** `C:\Users\foste\Documents\projects\local_sovereign_agent`
**Instrument:** `.venv/Scripts/python.exe` (project venv, Python 3.11), `pytest 9.1.1`, `pytest-timeout` installed
**Question:** does the test suite actually protect the fleet, or is it theatre?

> **Census-denominator law honoured.** Every number below was observed from a named
> instrument at a named moment. Nothing is estimated. Where a run did not complete,
> it is reported as incomplete, not inferred.

---

## HEADLINE

**The suite is real, large, and mostly green — and the enforcement gates are its weakest part.**

- The full suite runs: **33 failed, 2246 passed, 9 skipped in 54:47** (2288 collected).
- **Two gates that literally block `git push` have no test at all**: `tools/config_seal.py`
  (zero occurrences of the string in all of `tests/`) and `tools/checkbox_receipt_gate.py` (zero).
  `tools/prepush_paths_changed.py` is a third untested hook script.
- **`tools/config_seal.py` is RED on the real repo right now** (exit 1: 3 MODIFIED, 4 UNSEALED
  configs) and nothing in the suite notices.
- **Mutation testing caught a disarmed gate**: breaking `violation_ratchet.cmd_check`'s
  blocking path (`return 1` → `return 0`) in a temp mirror left **all 7 of its tests passing**.
  The ratchet's fail-closed behaviour is untested — the tests only ever assert exit 0.

---

## PART A — THE REAL RUN

**Instrument:** `./.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider --timeout=300`
**Run window:** started ~20:59 local, wall clock **3287.86s (0:54:47)**, completed.
(Note: a bare `python` is Hermes' own venv and has no project deps — the `.venv`
interpreter is mandatory in this repo.)

```
33 failed, 2246 passed, 9 skipped, 6 warnings in 3287.86s (0:54:47)
```

| Measure | Value | Source |
|---|---|---|
| Collected | **2288** | `pytest --collect-only -q` |
| Passed | **2246** | full run, 2026-09-26 |
| Failed | **33** | full run |
| Skipped | **9** | full run |
| Wall clock | **54:47** | full run |
| AGENTS.md claim | 1910 | brief-supplied, `AGENTS.md` |
| **Drift** | **+378** | 2288 − 1910 |

**Honest instrumentation note:** the primary run's stdout was piped through `tail -60`, so
that pass captured 22 of the 33 failing test IDs. **Recovered the other 11** with a second
instrumented pass over the 130 alphabetically-earlier test files
(`pytest <130 files> -q --timeout=120 -rf`, **1706.29s / 0:28:26** →
`10 failed, 925 passed, 7 skipped`). All 33 IDs below were observed. No ID is inferred.

### Failing test IDs — ALL 33, observed

**From the recovery pass (130 earlier files, 10 failures):**
```
tests/test_all_seat_interaction.py::test_class_selection_reads_prior_selections
tests/test_census_drift_patrol.py::test_files_added_since_excludes_census_day_and_non_tests
tests/test_desk_baseline_probe.py::test_workflow_test_mode_is_visible_and_propagated
tests/test_desk_baseline_probe.py::test_dashboard_navigation_groups_each_surface_semantically
tests/test_desk_baseline_probe.py::test_verkle_lattice_is_a_readable_honest_continuity_layer
tests/test_desk_baseline_probe.py::test_verkle_knot_is_an_agent_handoff_artifact
tests/test_desk_baseline_probe.py::test_days_lenses_are_globally_wired_and_story_is_restored
tests/test_desk_baseline_probe.py::test_desk_primary_action_uses_real_behavioral_router
tests/test_falsifier_ledger.py::test_grounding_jsonl_chain_and_schema
tests/test_falsifier_ledger.py::test_evidence_local_pointers_resolve
```

**From the primary full run (tail, 23 failures):**
```
tests/test_healthz_status.py::test_breach_returns_503
tests/test_index_fold_host.py::test_living_prefix_mutation_is_a_hard_failure
tests/test_index_fold_host.py::test_living_truncation_is_a_hard_failure
tests/test_index_fold_host.py::test_plain_register_keeps_whole_file_seal
tests/test_index_fold_host.py::test_living_without_size_seal_is_counted_not_failed
tests/test_loop_death_guards.py::test_loop_death_guard_fires_on_raise[afk_routing]
tests/test_mirror_intro.py::test_mirror_guide_markup_in_index
tests/test_no_win.py::test_reframe_keeps_invariant_changes_conditions
tests/test_organ_map.py::test_map_separates_callable_from_live
tests/test_organ_map.py::test_map_and_elder_surface_callable_orphans
tests/test_pack_modes_steward.py::test_build_mode_includes_build_excerpt
tests/test_ponytail_audit.py::test_run_audit_returns_schema
tests/test_quota_billable.py::test_provider_budget_uses_billable_not_inflated_ledger
tests/test_quota_billable.py::test_provider_budget_trips_when_billable_hits_cap
tests/test_shared_surface_events.py::test_real_links_jsonl_matches_the_registered_baseline
tests/test_substrate_identity.py::test_identity_persistence
tests/test_supervision_soak.py::test_gpipes_pipe_status_kill_list
tests/test_water_computer.py::test_valve_refused_in_gallery
tests/test_water_computer.py::test_gravity_moves_when_open
tests/test_water_computer.py::test_bucket_is_cheat_not_win
tests/test_water_computer.py::test_flow_wins
tests/test_water_computer.py::test_cycle_steam_rain_charge_ice_melt
tests/test_wave_driver.py::TestSingleTickSubprocess::test_tick_appends_chain_valid_row
```

### Cause classification

| Class | Tests | Evidence |
|---|---|---|
| **Missing asset / dep** (the test points at a file that isn't in this checkout) | `test_falsifier_ledger` ×2, `test_ponytail_audit::test_run_audit_returns_schema`, `test_substrate_identity::test_identity_persistence` | Verified concretely: `test_falsifier_ledger::test_evidence_local_pointers_resolve` fails with `where exists = WindowsPath('.../dashboard/static/art/privlidge_school_receipt_20260913.png').exists` → `assert False`. A missing PNG on disk, not a logic bug. |
| **Stale/rotated baseline pin** (the estate's own text/surface moved under a frozen pin) | `test_index_fold_host` ×4, `test_mirror_intro`, `test_shared_surface_events::test_real_links_jsonl_matches_the_registered_baseline`, `test_pack_modes_steward`, `test_desk_baseline_probe` ×6, `test_all_seat_interaction` | These assert against *live* surfaces (`AGENTS.md`, `dashboard/`, `links.jsonl`, the desk UI). The working tree has 83 modified test paths and an active burn-wave, so pins and bytes disagree. The pins are the bug, not the product. |
| **Real bug or real regression — needs a verdict** | `test_water_computer` ×5, `test_no_win`, `test_organ_map` ×2, `test_loop_death_guards[afk_routing]`, `test_quota_billable` ×2, `test_healthz_status::test_breach_returns_503`, `test_supervision_soak`, `test_wave_driver::test_tick_appends_chain_valid_row`, `test_census_drift_patrol::test_files_added_since_excludes_census_day_and_non_tests` | Genuine assertion failures (`assert 0 ==`, `AssertionError`, `- assert True is ...`), not missing files. Four with fleet-visible consequences: a breach that should return 503 (`test_healthz_status`), a chain row that does not validate (`test_wave_driver`), the **census drift gate's own date-exclusion logic** (`test_census_drift_patrol` — the gate that guards the test-count claim is itself red), and `test_supervision_soak`. |
| **Flaky / timing** | none proven as flaky | A separate run (`--timeout=120`) hit a hard test timeout in `test_coding_session_runner.py::test_run_until_done_preflight_fail`, which shells out via `mag/coding_session_loop.py::_run_cmd` to a real subprocess. That is a latent hang risk in a 55-minute suite, not a flake observed twice. |

**The structural read that matters:** **a third of the failures are the estate's own
fossil detectors working** — `test_index_fold_host`, `test_shared_surface_events`,
`test_desk_baseline_probe` all assert that live surfaces still match frozen pins, and the
working tree has moved. Those 11 are the tripwires doing their job. The other ~9 are
untriaged assertion failures, **including the census drift gate's own unit test** — the
gate that exists to catch a stale test-count claim is itself failing, which is precisely
the class of problem it was built to surface and nobody is acting on.

### Reconcile the two instruments

The recovery pass (130 of 352 files) reported `10 failed, 925 passed, 7 skipped` in 28:26;
the full run reported `33 failed, 2246 passed, 9 skipped` in 54:47. The 10 failures from the
recovery pass are disjoint from the 23 in the full run's tail, giving 33 total — consistent,
no double-counting. The 7 vs 9 skip difference is the `deselect`/import-order effect of
naming files individually; the failing set is what reconciles.

---

## PART B — ARE THE GATES TESTED?

**The key question, answered: two hard push-gates have no test, and the third-hardest has a
test that cannot fail.**

| Gate | Blocks push? | Test file | Defs | Verdict | Fails closed? |
|---|---|---|---|---|---|
| `tools/violation_ratchet.py` | **YES** (`pre-push:10`, `\|\| exit 1`) | `tests/test_violation_ratchet.py` | 7 | **HAS TEST — happy path only, INEFFECTIVE** | **NO** |
| `tools/census_drift_patrol.py` | partial (exit 2 BLIND blocks; exit 1 STALE is WARN-ONLY, B2-277) | `tests/test_census_drift_patrol.py` | 46 | **HAS TEST — genuinely fail-closed** | YES |
| `tools/workflow_gate.py` | conditional (scenario suite blocks when gate script changes, `pre-push:280-303`) | `tests/test_workflow_gate.py` | 8 | **HAS TEST — genuinely fail-closed** | YES |
| `tools/md_record_seal.py` | no | `tests/test_md_record_seal.py` | 9 | HAS TEST — but the gate is **fail-OPEN by design** | n/a |
| `tools/freshness_check.py` | via `freshness_gate.py`, WARN-ONLY | **none** | 0 | **NO TEST under `tests/`** — ships its own real self-test | yes, outside pytest |
| `tools/corpus_fts_rebuild.py` | no | **none** | 0 | **NO TEST** | no |
| `tools/config_seal.py` | **YES** (`pre-push:12`, `\|\| exit 1`) | **none** | 0 | **NO TEST — HARD-BLOCKING GATE, ZERO COVERAGE** | **NO** |
| `tools/census_patrol_selftest.py` | no | (exercised by the patrol test) | — | **REAL SELF-TEST, not a stub** | YES |
| `mag/shared_surface.py` | via pin hooks | **none named** | 0 | PARTIAL — 6 files reference the surface | partial |
| `githooks/pre-push` (the hook) | **YES** | `hook_pairing.py` + 2 more | — | **HAS TEST — genuinely, falsifier-shaped** | YES |

### The evidence for each claim

**`violation_ratchet.py` — the tests cannot fail.** All five gate call sites in
`tests/test_violation_ratchet.py` assert `== 0`:
`cmd_prune() == 0` (×2), `cmd_baseline_update(...) == 0`, `cmd_check(changed_only=False) == 0` (×2).
The blocking branch is `violation_ratchet.py:273-275`:
```python
    if new or expired:
        print(f"RATCHET: FAIL — ...")
        return 1
```
No test ever drives unregistered debt into `cmd_check` and asserts exit 1. **Proven by
mutation 1 below.**

**`config_seal.py` — zero coverage of a hard gate.** `grep -rc "config_seal" tests/*.py`
returns nothing; no test file mentions it. It is invoked at `githooks/pre-push:12`. It is
currently **red on the real repo**:
```
CONFIG-SEAL verify: sealed=? live=? ...
  MODIFIED  providers.yaml
  MODIFIED  spend_overlay.yaml
  MODIFIED  violation_baseline.json
  UNSEALED  links_kind_baseline.json
  UNSEALED  links_sha_ratchet_baseline.json
  UNSEALED  sanctioned_scheduled_tasks.yaml
  UNSEALED  workflow_registry_baseline.json
CONFIG-SEAL: FAIL — re-seal by NAME: python tools/config_seal.py update --by WHO --note WHY
REAL_EXIT=1
```
**Every push is currently blocked, and the test suite is green on this file because it never
looks.** This is the single most actionable finding in the lane.

**`freshness_check.py` — real coverage in the wrong place.** It has no `tests/` file, but it
ships a genuine self-test. Run live:
`freshness_check.py --self-test` → `RECEIPT SELF-TEST: PASS`, with explicit
**fail-closed** vectors: drifted source fails, `None` receipt fails closed,
non-dict receipt fails closed, missing `source_hash` fails closed, unparseable
`observed_at` fails closed, future-dated receipt fails closed, naive `observed_at`
treated as UTC, JSON round-trip. **One `tests/test_freshness_check.py` shim away from
being in the suite.**

**`census_patrol_selftest.py` — a REAL self-test, not a stub.** 196 lines, 31 `check()`
calls, ~20 distinct vectors including the real 12-day fossil regression. It injects the
live patrol module (never a stale copy). Run live → `CENSUS-PATROL SELF-TEST: PASS`.
**Proven effective by mutation 5** (it went red with 7 named failures). The design comment
explains the injection: it avoids importing `tools/__init__` and avoids the tool file
executing under two module names. Good engineering, and it works.

**`githooks/pre-push` — the best-tested surface in the estate.** `tests/hook_pairing.py`
deliberately not named `test_*` so pytest skips it, and is consumed by the `test_*` files.
It reads the **real hook bytes at test time** and replays captured output through **real
`sh`** — exactly what the hook does with `out=$(... 2>&1)`. `test_scenarios_gate_hook_pin.py`
contains an honest falsifier: `test_case_flip_is_caught` flips the case of the pattern and
**requires the green first line to stop matching**. `test_hook_prefix_pairing.py` (107 lines)
extends this to every pre-push ok case-arm, both directions. Hook bytes are not duplicated
into the tests, so the tests cannot drift from the hook.

### LAW-12 scenario card suite — real and enforcing

`configs/workflow_gate_scenarios/` holds 7 cards (G1–G7) + fixtures. Run live on the real
repo:
```
SCENARIOS ok   G1_multiplicity.card.json:   G1-multiplicity  -> FAIL exit 2
SCENARIOS ok   G2_passoff.card.json:       G2-passoff       -> FAIL exit 2
SCENARIOS ok   G3_steering.card.json:      G3-steering      -> FAIL exit 2
SCENARIOS ok   G4_salvage.card.json:       G4-salvage       -> FAIL exit 2
SCENARIOS ok   G5_deliverable.card.json:   G5-deliverable   -> FAIL exit 2
SCENARIOS ok   G6_receipts.card.json:      G6-receipts      -> PASS exit 0
SCENARIOS ok   G7_laws.card.json:          G7-laws          -> FAIL exit 2
SCENARIOS ok   pass_control: all seven gates clean
SCENARIOS: 7 cards validated read-only (no registry row written)
SCEN_EXIT=0
```
Each card cites a real registry FAIL row and asserts the fixture reproduces the expected
verdict. This is a genuine gate-on-the-gate, and it is enforcing in the hook.

### Every other hook script

| Script | Test file? | Referenced by | Blocks? |
|---|---|---|---|
| `checkbox_receipt_gate` | **NO** | **0 test files** | no (WARN-ONLY) |
| `config_seal` | **NO** | **0 test files** | **YES** |
| `prepush_paths_changed` | **NO** | **0 test files** | no (path helper for the conditional gates) |
| `description_pin` | yes | 1 | no |
| `freshness_gate` | yes | 4 | no |
| `caption_ledger_verify` | no | 3 | no |
| `violation_ratchet` | yes | 2 | **YES** |
| `census_drift_patrol` | yes | 5 | partial |

**Hook enforcement split: 6 hard-blocking exits, 9 warn-only.** The warn-only ones
(`description_pin`, `freshness`, `checkbox`, `caption_ledger`, `refold`) are the "flip
`|| true` to `|| exit 1` as an operator decision" family — the hook comments say so
explicitly. That is a deliberate WARN posture, not theatre, and it is documented in place.

---

## PART C — THE COVERAGE MAP

**Both packages are flat** — no real subdirectories in `mag/` or `tools/` (the only
"subdirectories" are `mag/mag` and `tools/tools` shims with 4 and 2 files, 0% covered).
So a directory-level map collapses to one row each, and **file-level at 1,030 modules is
noise**. The meaningful measures are the file-level ratio and the LOC-weighted ratio.

### File-level (module touched by at least one test, by name or import)

| Package | Modules | Touched by tests | Ratio |
|---|---|---|---|
| `mag/` | 1030 | 308 | **29.9%** |
| `tools/` | 165 | 27 | **16.4%** |

### LOC-weighted (the honest number at this scale)

| Package | Total LOC | Covered LOC | Ratio |
|---|---|---|---|
| `mag/` | 292,112 | 106,951 | **36.6%** |
| `tools/` | 36,949 | 8,220 | **22.3%** |

`tools/` is the weak one, and that is exactly where the gates live: **77.7% of the
toolbelt's lines are untouched by any test**, and the toolbelt is what blocks pushes.

### Biggest untested `mag/` modules (by LOC)

| LOC | Module |
|---|---|
| 1668 | `mag/game_brawl` |
| 1140 | `mag/lane_runner` |
| 1072 | `mag/worldline_seed` |
| 1054 | `mag/ghost_leak_detector` |
| 992 | `mag/framework_map` |
| 970 | `mag/fermat_ractor` |
| 925 | `mag/switchboard_v2` |
| 855 | `mag/republic` |
| 849 | `mag/data_refinery` |
| 847 | `mag/renderman` |
| 845 | `mag/narrative_engine` |
| 826 | `mag/surface_render` |
| 811 | `mag/research_director` |
| 791 | `mag/diary_node` |
| 767 | `mag/api_gateway` |

### Untested high-traffic `mag/` modules (by internal importer count)

These are imported *by other production modules* and have no test:

| Module | Internal importers |
|---|---|
| **`mag/knowledge_graph`** | **25** — the most-imported module in `mag/`, untested |
| **`mag/chain_query`** | **21** — the chain is the fleet's source of record; its query surface is untested |
| `mag/grok_rightsize` | 12 |
| `mag/lanes` | 10 |
| `mag/swarm_health` | 10 |
| `mag/self_drive` | 10 |

For contrast, the *tested* high-traffic modules are `mag/orchestrator` (81 importers),
`mag/training_events` (53), `mag/verkle_knot` (43), `mag/operator_inbox` (39),
`mag/desk_dialogue` (38). So the traffic curve is: the orchestration spine is covered,
and the knowledge/chain query layer just under it is not.

### Biggest untested `tools/` modules (by LOC)

`tools/seed_v2` (956), `tools/duty_fuzz` (750), `tools/wandr_selfeval` (703),
`tools/quote_audit_wide` (662), `tools/ghost_tournament` (660),
`tools/steer_compare` (618), `tools/oracle_calibration` (569), `tools/mcp_pin` (488),
`tools/restore_guard` (372), `tools/local_bench` (363).

---

## PART D — MUTATION SANITY

**Method (no real-tree writes).** All mutations were applied to a **temp mirror** at
`$TMPDIR/lane7_mut`: 1,195 `.py` files mirrored from `tools/` + `mag/`, plus `config.py`,
`conftest.py`, `pytest.ini`, `AGENTS.md`, `githooks/`, `configs/`,
`violation_baseline.json`, and a real `git init` + commit so the git-shelling tests work.
The real repo tree was never written to. Each gate was restored and re-verified green
after its mutation.

**Mirror baseline (before any mutation):**

| Test file | Baseline |
|---|---|
| `test_violation_ratchet` | 7 passed |
| `test_workflow_gate` | 8 passed |
| `test_md_record_seal` | 9 passed |
| `test_census_drift_patrol` | 1 failed, 45 passed *(mirror artifact: the mirror's own fresh commit has no `tests/` growth, so the census-day exclusion test misfires. NOT a product bug — that same test passes on the real repo tree.)* |

### Results

| # | Target | Break | Test | Result | Verdict |
|---|---|---|---|---|---|
| 1 | `violation_ratchet.cmd_check` | `return 1` → `return 0` on unregistered debt (**gate disarmed**) | `test_violation_ratchet` | **7 PASSED (unchanged)** | **SURVIVED — fail-closed path UNTESTED** |
| 2 | `workflow_gate.G6_STAMP_RE` | regex widened to match everything | `test_workflow_gate` | **8 FAILED** | KILLED — real coverage |
| 3 | `config_seal.cmd_verify` | `return 1` → `return 0` on drift (**gate disarmed**) | *none exists* | whole 70-test mirror: no test reacted | **SURVIVED — NO TEST AT ALL** |
| 4 | `md_record_seal.register_sha256` | all hashes → 64 zeros; then living-file fallback → constant | `test_md_record_seal` | 1 failed each time | KILLED — integrity logic genuinely covered |
| 5 | `census_drift_patrol.patrol()` | every `STALE` → `OK`, every `exit 1` → `0` | `test_census_drift_patrol` | **11 FAILED**; CLI self-test also FAIL with 7 named failures | KILLED — strongest coverage |

**3 of 5 mutations killed. The 2 survivors are the 2 worst cases** — and both survivors are
hard push-gates:

- **Mutation 1** proves `tests/test_violation_ratchet.py` is 7 assertions about *bookkeeping*
  (prune domains, seq stamps, growth display) that never touch the decision the push hook
  depends on. You can disarm the ratchet and the suite is green.
- **Mutation 3** proves `config_seal` has no test at all. The 70-test mirror suite showed the
  same single pre-existing mirror artifact and nothing else.

**A note on mutation 4:** my first attempt at `md_record_seal` was a **no-op** — the file
contains zero `return 1` statements. That is not a test weakness; it is the gate being
**fail-open by design** (`fail_open()` → `sys.exit(0)` at line 78-80, docstring: *"a broken
seal must never block the fleet"*). There is no blocking path to test. I re-ran the mutation
against its actual integrity logic (the hash function), and both variants were killed. Its
*integrity* is covered; its *enforcement* is deliberately absent, and documented as such.

**The pattern worth naming:** the gates that are genuinely well-tested are the two where
someone wrote a **dedicated self-test with explicit fail-closed vectors**
(`census_patrol_selftest.py` — "the real 12-day fossil is STALE", "None receipt fails
closed", "hook pairing: stale run exits 1"). The gates that are theatre are the ones where
tests were written around the module's *shape* rather than its *verdict*.

---

## WHAT IS ACTUALLY UNTESTED CRITICAL CODE

Ranked by "how much would a silent failure here hurt the fleet":

1. **`tools/config_seal.py` — CRITICAL.** Hard push gate, **zero tests**, and **currently
   red** (exit 1, 7 drifted/unsealed configs including `providers.yaml` and
   `spend_overlay.yaml`). Every push is blocked or being bypassed right now; the suite is
   green because it never looks. *Fix: one `tests/test_config_seal.py` with a
   modify/delete/add-a-file fixture asserting exit 1, plus exit 2 on no-seal.*
2. **`violation_ratchet.cmd_check` blocking branch — CRITICAL.** The push gate's fail-closed
   decision has no assertion. Disarm it and 7 tests stay green. *Fix: one test that feeds an
   unregistered violation and asserts `== 1`.*
3. **`mag/chain_query` (21 importers) — MEDIUM/HIGH.** The chain is the fleet's signed source
   of record; its query surface is untested. `test_wave_driver::test_tick_appends_chain_valid_row`
   is *currently failing*, which is chain-row validation failing.
4. **`mag/knowledge_graph` (25 importers) — MEDIUM.** The most-imported module in `mag/`,
   with no test.
5. **`tools/checkbox_receipt_gate.py` — MEDIUM.** Runs on every push, zero tests.
6. **`tools/prepush_paths_changed.py` — MEDIUM.** This decides whether the *conditional* gates
   (refold, caption ledger, scenario suite) run at all. If it is wrong, enforcing gates skip
   silently. Zero tests.
7. **`tools/corpus_fts_rebuild.py` — MEDIUM.** Zero tests, and it **crashed live** during
   this audit with `sqlite3.OperationalError: unable to open database file`.
8. **`tools/freshness_check.py` — LOW.** Genuinely fail-closed and genuinely self-tested; the
   only defect is placement. One shim file fixes it.

### What is worth keeping

The suite is not theatre. It has real, adversarially-designed parts:

- `githooks/pre-push` testing reads **real hook bytes** and replays through **real `sh`**,
  with a case-flip falsifier that requires a regression to break a match.
- `tools/census_patrol_selftest.py` is a **196-line, 31-check** self-test with named
  regression vectors, and mutation 5 proved it bites.
- The LAW-12 scenario card suite is a **real enforcing gate-on-the-gate** — 7 cards, each
  citing a real registry FAIL row, all validated live.
- `tests/conftest.py` carries a **suite-wide autouse isolation fixture** (B2-336) that makes
  log/registry pollution structurally impossible rather than per-test discipline.
- `conftest.py` pre-creates `basetemp`, with a comment recording that its absence once
  caused 56 suite failures on 2026-08-09. That is institutional memory in the harness.
- All 7 gates are **stdlib-only** (no `mag/` imports) — they run anywhere, and their tests
  do not inherit the fleet's dependency surface.

**The estate knows how to test gates properly. It has simply not done it for
`config_seal` and for the ratchet's blocking branch** — the two gates that are wired
directly into `pre-push` with `|| exit 1`.

---

## REPRODUCTION

```bash
cd C:/Users/foste/Documents/projects/local_sovereign_agent

# PART A — the real suite (54:47 on this host)
./.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider --timeout=300

# PART B — the two uncovered hard gates
grep -rc "config_seal" tests/*.py            # nothing: zero coverage
./.venv/Scripts/python.exe tools/config_seal.py verify   # exits 1 — RED right now

# PART B — the two real self-tests
./.venv/Scripts/python.exe tools/census_drift_patrol.py --self-test   # PASS
./.venv/Scripts/python.exe tools/freshness_check.py --self-test      # PASS
./.venv/Scripts/python.exe tools/workflow_gate.py check --scenarios configs/workflow_gate_scenarios  # 7 cards ok

# PART D — mutation harness (temp mirror only; real tree untouched)
bash "$TMPDIR/lane7_mut_build.sh"   # build the 1195-file mirror
bash "$TMPDIR/lane7_mut_run.sh"      # mutations 1-3
bash "$TMPDIR/lane7_mut2.sh"         # mutations 4-5 + self-test
```

Scratch instruments: `lane7_map.py` (gate + coverage map), `lane7_loc.py` (LOC-weighted
coverage), `lane7_hookgates.sh` (hook-script inventory), `lane7_mut*.sh` (mutation harness).
Output JSON: `memory/audit_20260926/lane7_tests.json`.
