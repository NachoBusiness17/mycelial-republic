# LANE 4 — TEST SUITE ROBUSTNESS AUDIT

**Date:** 2026-09-27
**Seat:** zcode (Sancho) — delegated lane
**Repo:** `C:\Users\foste\Documents\projects\local_sovereign_agent`
**Instrument:** `.venv/Scripts/python.exe` (project venv, Python 3.11), `pytest 9.1.1`
**Question:** is the suite capable of failing, and do the fleet's self-checks actually block?

> Extends lane 7's test-reality card. Where lane 7 classified, this lane
> re-derived and **corrected three classifications** — see PART A.3.

**Measured full run (this lane):**
`33 failed, 2261 passed, 9 skipped, 2 warnings in 2586.37s (0:43:06)`,
started 2026-09-27T05:32:38Z, ended 06:09:53Z, exit 1.

**The count held at 33. The SET did not.** Between lane 7's run and this one,
sibling lanes landed code into this live tree: `test_ponytail_audit`,
`test_census_drift_patrol::test_files_added_since_...` and a `test_wave_driver`
sibling dropped out; `test_frontier_council` ×2 and `test_skill_seat` ×1
arrived. A failure list in a tree with 1,832 concurrently-modified paths is a
moving target — worth knowing before anyone pins it.

---

## HEADLINE

**The suite is not theatre. The gates are.**

- **Assertion discipline is excellent.** 6,604 bare asserts across 2,124 tests.
  **Only 2 try/except-swallow sites exist in the whole suite.** Zero custom
  matchers, zero mocked gates. Nothing here is padded to pass.
- **The census gate is genuinely load-bearing.** It is the *only* one of the
  four self-checks whose blocking path is actually exercised, and it is the only
  one that killed a mutation.
- **The other three are nominal.** `config_seal`, `checkbox_receipt_gate` and
  `violation_ratchet`'s *blocking* path can each be fully disarmed with the
  suite green.
- **A fifth gate the last audit never saw** — `secret_gate.py`, wired
  2026-09-27, enforcing on **both** exit arms — has **zero tests**.
- **All three hard push gates are RED right now.** The repo is unpushable and
  the suite is green on it, because it never looks.

---

## PART A — THE 33 FAILING TESTS, CLASSIFIED

Every one of the 33 IDs was re-observed in this lane with live assertion text
(no inference). All 33 are resolved to `file:line`.

### A.1 The classification

| # | file:line | class | why |
|---|---|---|---|
| 1 | `tests/test_healthz_status.py:37` | **product bug** HIGH | `semantic_health()` returns `ok=True` for 10 `http_tool_fail` rows. The breach is invisible; `/healthz` reports healthy while failing. The test is *named* `returns_503` but only asserts the report dict — it never checks the status code. |
| 2 | `tests/test_quota_billable.py:80` | **product bug** HIGH | With `max_tokens=30,000,000` the daily budget ceiling never trips; `budget_ok` stays `True`. The spend guardrail is inert. |
| 3 | `tests/test_quota_billable.py:25` | **product bug** MED | Same root cause. The billable-vs-ledger *accounting* is correct (`usage_source`, `used_tokens` pass); only the cap pin is dead. |
| 4 | `tests/test_census_drift_patrol.py:216` | **product bug** MED | **Real TZ bug in the gate.** `census_drift_patrol.py:242` normalises commit time to **UTC** while the census day is a **local** calendar day. Between 20:00–24:00 EDT a same-local-day commit lands on the next UTC day and the gate counts it as post-census. 4 of every 24 local hours are wrong. The test is right; the gate is wrong. |
| 5 | `tests/test_organ_map.py:5` | **product bug** MED | `atlas` sits at `VERIFIED`, not `LIVE`. The map's own promotion ladder disagrees with what the test expects promotes it. |
| 6 | `tests/test_organ_map.py:39` | **product bug** LOW | `elder.audit()` still lists `ask_router` as a gap though `organ_map` calls it callable+wired. Two internal views of the same organ disagree. |
| 7 | `tests/test_supervision_soak.py:95` | **product bug** LOW | A named pipe is missing from the supervision kill list. |
| 8 | `tests/test_wave_driver.py:94` | **product bug** MED | The wave tick refuses to append: `PATH PIN REFUSED: --ground=<tmp> outside the repo root`. The pin works exactly as built; the **test** drives it out of bounds via `tmp_path`. |
| 9 | `tests/test_water_computer.py:52,59,70,83,104` | **product bug** MED | 5 of 9. Valve not refused, gravity does not move when open, bucket cheat undetected, flow does not win, cycle yields liquid not gas. Game win/cheat physics wrong. |
| 10 | `tests/test_falsifier_ledger.py:39` | **product bug** MED | Row 121 of the hash-chained grounding ledger has no `evidence` field. A broken row in a chain ledger is a writer defect, not a stale pin. |
| 11 | `tests/test_desk_baseline_probe.py:91,101,122,135,146,157` | stale pin LOW | **One root cause, six tests.** All read `dashboard/static/index.html`, which was replaced wholesale by a 16,693-byte "FLEET CONSOLE" page. The six pinned markers are absent because the file they pinned to no longer exists in that form. |
| 12 | `tests/test_mirror_intro.py:11` | stale pin LOW | **Same file as #11.** Asserts `id="mirrorGuide"` in the replaced `index.html`. |
| 13 | `tests/test_shared_surface_events.py:305` | stale pin LOW | 4 new B2-142 rows past the B2-28 marker. The append-only register is working; the marker is behind. |
| 14 | `tests/test_pack_modes_steward.py:29` | stale pin LOW | Pack text reworded; `'L2b Frozen BUILD'` / `'Do the thing'` no longer emitted. |
| 15 | `tests/test_all_seat_interaction.py:35` | stale pin LOW | `ImportError: cannot import name 'quest_party' from 'mag'` — module renamed/removed, test still names it. |
| 16 | `tests/test_no_win.py:26` | stale pin LOW | Product string is `REFRAIM[...]`; test pins `REFRAME`. One letter. **ERRATUM (2026-10-05, B7): verdict refuted - the product carried the typo, the test pin was correct per the module's own frozen spec; fixed in code, not the test (watch/inbox/burn_reset_20260927/no_win.md, commit 750259531).** |
| 17 | `tests/test_falsifier_ledger.py:68` | **missing asset** LOW | Row 104 names `dashboard/static/art/privlidge_school_receipt_20260913.png`; the PNG is not in this checkout. |
| 18 | `tests/test_ponytail_audit.py:7` | **order-dependent** LOW | **Passes in isolation, fails in the full run.** Reads live estate state; a sibling lane's concurrent writes decide the verdict. Not a reproducible defect. |
| 19 | `tests/test_loop_death_guards.py:145` | **order-dependent** LOW | **Passes in isolation, fails in the full run.** |
| 20 | `tests/test_index_fold_host.py:429,440,450,477` | **platform bug** MED | **Not a stale pin, not a product bug.** The detector fires correctly — `LIVING PREFIX MISMATCH`, `HASH MISMATCH`, `1 mismatched` are all in the output — but it prints an **absolute Windows path** where the test pins a bare filename. Passes on POSIX, fails on Windows. |
| 21 | `tests/test_substrate_identity.py:19` | **platform bug** LOW | `FileNotFoundError` on `.../projects/mag/state.py`. `Path(__file__).parents[2]` assumes `tests/` is two levels below the repo root; here it is one. Off-by-one fixture path. |
| 22 | `tests/test_census_drift_patrol.py:216` | **+time-dependent** MED | #4 again. This test carries **two** independent dependencies: a real TZ bug *and* a local-time window. It **passed** in the 05:32Z run and is absent from the final 33. |
| 23 | `tests/test_frontier_council.py` (`test_delegate_routes_and_shapes`) | stale pin LOW | **new arrival.** `assert 'deepseek' in ('chatgpt','grok_web')` — the router's lane table no longer offers deepseek on this route. |
| 24 | `tests/test_frontier_council.py` (`test_recommend_self_stolen_chain`) | stale pin LOW | **new arrival.** `assert 'cheap' == 'reasoning'` — the recommendation class changed under the pin. |
| 25 | `tests/test_skill_seat.py:25` | **order-dependent** LOW | **new arrival.** Failed in the full run with `FileNotFoundError [WinError]`, **passes in isolation** — a transient lock interaction with a concurrent lane, not a stable defect. |

**Totals:** 10 product bug · 6 stale pin · 1 missing asset · 2 platform bug ·
2 order-dependent (+1 dual-dependency overlap on #4). The 33 IDs collapse to
**~20 distinct defects**, and the largest single cluster (7 tests) is one
replaced HTML file.

### A.2 The one that matters most

`configs/providers.yaml:393` reads `max_tokens: 30000000` with a `note:` that
records the change as a deliberate operator supersession dated 2026-08-26
("was $1/day autorun 2026-08-12"). `tests/test_quota_billable.py` still pins
`1_000_000`. So failures #2 and #3 are **not** bugs — the ceiling was raised on
purpose and the test was never updated. Reclassified accordingly: the *product*
is at intent, the *pin* is stale, and what is genuinely broken is that a 30×
 budget increase shipped with **no test and no gate noticing**.

### A.3 Corrections to lane 7

| lane 7 said | this lane measured |
|---|---|
| `test_index_fold_host` ×4 = stale baseline pins | **Wrong.** Windows path-separator bug in the test. The product detector is correct and fires. |
| `test_census_drift_patrol` = "real bug, needs a verdict" | **Confirmed and root-caused:** a UTC-vs-local-day normalisation bug in the gate, reproducible only between 20:00 and 24:00 local. |
| `test_desk_baseline_probe` ×6 = pins on several live surfaces | **One** surface replacement (`index.html`) killing six pins — and `test_mirror_intro` shares the same file. |
| three gates have zero tests | **Five** gates have zero tests: `config_seal`, `checkbox_receipt_gate`, `secret_gate`, `prepush_paths_changed`, `freshness_check` (last one self-tests outside pytest). |

---

## PART B — ASSERTION STYLE: THE SUITE CAN FAIL

AST walk of every `test_` function in `tests/` (354 files, **2,278** test
functions), classified per-test.

| Style | Assertions | Tests dominated by it |
|---|---:|---:|
| bare `assert` | **6,604** | **2,124** |
| `unittest` `self.assertX` | 148 | 30 |
| `pytest.raises` | 54 | 13 |
| custom matchers | **0** | **0** |
| `try/except` swallow | **2** | 0 |
| mixed | — | 31 |
| no assert at all | — | **80** |

**The headline: a suite dominated by try/except swallows is a suite that cannot
fail. This is not that suite.** Exactly **2** swallow sites exist across 2,278
tests, and both are guard clauses that still carry real asserts:

- `tests/test_kv_seal.py:72` — 1 swallow, 2 asserts
- `tests/test_wow_manifest.py:45` — 1 swallow, 2 asserts

There are **no `assert_*` helper functions defined anywhere in `tests/`** — zero
custom matchers. The suite is 97% plain `assert`. 80 tests carry no assertion
construct (they fail by raising, which is legitimate); 7 resolve to zero-assert
AST and are listed in the JSON.

**Verdict: assertion discipline is the strongest thing in this audit.** Nothing
here is theatre, and no amount of gate failure should be read as a suite that
cannot fail.

---

## PART C — REAL GATE vs MOCKED GATE

**There is essentially no mocking of gates.** That is not the problem.

| Gate | Test files | Real import | Subprocess | Mocked | Verdict |
|---|---:|---:|---:|---:|---|
| `census_drift_patrol` | 5 | 0 | **5** | 0 | Real gate, real subprocess, synthetic estates |
| `workflow_gate` | 5 | **1** | 4 | 0 | Real module + LAW-12 card suite |
| `violation_ratchet` | 2 | 0 | 1 | 0 | Real module; `all_violations` monkeypatched — **the fake input never contains NEW debt** |
| `md_record_seal` | 2 | 1 | 1 | **1** | The one mock present; its integrity logic still bites |
| `config_seal` | **0** | 0 | 0 | 0 | nothing proven |
| `checkbox_receipt_gate` | **0** | 0 | 0 | 0 | nothing proven |
| `secret_gate` | **0** | 0 | 0 | 0 | nothing proven |
| `prepush_paths_changed` | **0** | 0 | 0 | 0 | nothing proven |
| `freshness_check` | 1 | 0 | 0 | 0 | real `--self-test`, outside pytest |

A test that mocks the instrument it claims to test proves nothing. In this
suite, that failure mode is **absent**. The real failure mode is the row of
zeros: four push-deciding gates have no test at all, so nothing is proven
either way.

---

## PART D — DO THE FOUR SELF-CHECKS EXERCISE THEIR BLOCKING PATH?

| Self-check | Blocking return | Hook role | Blocking path exercised? |
|---|---|---|---|
| `violation_ratchet` | `violation_ratchet.py:275` `return 1` (`:243` `return 2`) | `pre-push:10` `\|\| exit 1` **HARD** | **NO** |
| `census_drift_patrol` | `:304,309,312,318,341,349,352` `return 2`; STALE `base_exit=1` | `pre-push:96` `exit 2` **BLOCKS** | **YES — genuinely** |
| `config_seal` | `config_seal.py:71` `return 1` (`:53` `return 2`) | `pre-push:12` `\|\| exit 1` **HARD** | **NONE FOUND** |
| `checkbox_receipt_gate` | `:105` `return 1` (`:86` `return 2`) | `pre-push:113` `\|\| true` warn-only | **NONE FOUND** |

**`violation_ratchet` — nominally referenced only.** All five exit-code
assertions in `tests/test_violation_ratchet.py` are `== 0`, at lines **74, 97,
143, 161, 179**. Not one asserts `1` or `2`. The 7 tests cover
`scanner_domain`, prune bookkeeping and the `GROWTH` print — the module's
*shape*, never the decision the hook depends on.

**`census_drift_patrol` — the real thing.** Exit-code assertions at
`tests/test_census_drift_patrol.py:295, 305, 315, 328, 438, 485, 558`. Live
run: `CENSUS-PATROL SELF-TEST: PASS`. And it earned the label — it is the only
gate that killed a mutation (PART E).

**`config_seal` — nothing.** Zero occurrences of the string `config_seal` in any
file under `tests/`.

**`checkbox_receipt_gate` — nothing.** Zero occurrences.

### D.1 The gate nobody audited: `secret_gate.py`

`githooks/pre-push:324-332` wires `tools/secret_gate.py` with **both** arms
blocking:

```sh
case "$sg_rc" in
  0) echo "PUSH-GATE: secret_gate ok" ;;
  1) ... exit 1 ;;
  *) ... exit 1 ;;   # fail-closed: scanner error blocks too
esac
```

It is the only gate that can block on a **provider-shaped secret**, it is
fail-closed on scanner error, and **zero occurrences of `secret_gate` exist in
`tests/`**. It is newer than the previous audit, which is why it was missed.
It is currently the most exposed surface in the hook.

---

## PART E — MUTATION BATTERY

**Method — the real tree was never written.** Two instruments, because the
tests demand two:

- **In-memory** (`sys.modules` injection): the gate's source is read, mutated in
  memory, exec'd into a module registered under its real dotted name. The real
  test file's own `import tools.<gate> as g` picks up the neutered gate. Used
  for `violation_ratchet`, whose tests import in-process.
- **File-level in a temp mirror** at `scratch/lane4/mirror_census` (minimal:
  11 gate scripts, 6 test files, `conftest.py`, `pytest.ini`, `AGENTS.md`,
  `githooks/`, `configs/`, real `git init` + commit). Needed for
  `census_drift_patrol`, whose tests drive the tool as a **real subprocess by
  path** — an in-memory injection is invisible to that.

**The harness was validated before any verdict was believed:**

- Control 1 — invert a *success* return (`violation_ratchet` `0 → 1`):
  **KILLED**, 2 tests red. The harness can see a disarm.
- Control 2 — break the census green first-line contract: **KILLED**, 2 tests red.
- A collection gate aborts the whole battery if the mirror collects nothing. It
  fired twice during this lane and caught two broken harnesses that would
  otherwise have reported 0/6 "SURVIVED" as a finding.
- The mirror carries **15 pre-existing failures** that are mirror artifacts
  (registry jsonl / `AGENTS.md` not mirrored; `tmp_path` outside the mirror root
  trips a ratchet relpath). These are recorded as the baseline and **subtracted**;
  only *new* failures count as a kill.

### Results — 1 of 6 real disarm mutations killed

| # | Target | Hook role | Verdict |
|---|---|---|---|
| A | `violation_ratchet.cmd_check` `return 1 → 0` | `pre-push:10` `\|\| exit 1` **HARD** | **SURVIVED** — 0 new failures |
| B | `config_seal.cmd_verify` `1 → 0` and `2 → 0` | `pre-push:12` `\|\| exit 1` **HARD** | **SURVIVED** — 0 new failures |
| C | `checkbox_receipt_gate.main` `1 → 0` and `2 → 0` | `pre-push:113` warn-only | **SURVIVED** — 0 new failures |
| E | `secret_gate` `exit_code = 1 if …` → `0` | `pre-push:330-331` **both arms block** | **SURVIVED** — 0 new failures |
| D | `census_drift_patrol.run()` **every** `return 2 → 0` | `pre-push:96` `exit 2` **BLOCKS** | **KILLED** — 3 named tests |
| D2 | `census_drift_patrol` STALE `base_exit 1 → 0` | `pre-push` STALE arm | **KILLED** — 2 named tests |
| D4 | `census_drift_patrol` COLLECT-DRIFT `return deep["exit"] → 0` | the deep `--collect` check | **SURVIVED** — 0 new failures |
| — | *control* census green-contract broken | `pre-push:90` case-match | **KILLED** — 2 named tests |

**Killed (D):** `test_cli_missing_carrier_exits_2`,
`test_cli_unparsable_carrier_exits_2`, `test_cli_future_census_exits_2`.
**Killed (D2):** `test_cli_stale_synthetic_estate_exits_1`,
`test_hook_census_case_arm_replay_green_ok_arm_stale_warn_arm`.

**The sharpest single finding inside the one good gate.** `census_drift_patrol`
is killed on its STALE arm and on its cannot-verify arm, and **survives on its
COLLECT-DRIFT arm** — the `pytest --collect-only` comparison that is the gate's
*raison d'être* (the whole gate exists because the 1,910 carrier rode 12 days
stale). Disarm that arm and nothing goes red.

**Interpretation: a suite that passes on a neutered gate is not testing the
gate.** Four of the five push-deciding gates can be fully disarmed with the
suite green.

---

## PART F — WALL CLOCK AND PRE-PUSH VIABILITY

**Measured: 2586.37s = 0:43:06** for the full suite on this host.

`./.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider --timeout=300 -rf`
→ `33 failed, 2261 passed, 9 skipped, 2 warnings`, exit 1.

**Not viable as a pre-push gate**, and the estate already knows it: the hook's
own comments record the t40 lesson (2026-09-25) that a heavy new push check
locks operators out, which is why every conditional gate is narrow
changed-path rather than whole-suite. That reasoning is sound.

But the cost argument is the *wrong* thing to be looking at. The three gates
that **do** run cost about two seconds each, and they cover nothing. The
suite's 43 minutes are not the liability; the coverage of the 2-second gates is.
Buying more runtime would buy nothing — the missing tests are small.

Two operational notes from the measured run:

- Lane 7's 54:47 and this lane's 43:06 differ by 22% on the same suite. The
  variance is the suite's real-time subprocess and git work, not machine load.
- A `--timeout=300` is mandatory. Without it a single hanging subprocess turns
  a 43-minute run into an indefinite one — lane 7 hit exactly that
  (`test_coding_session_runner::test_run_until_done_preflight_fail`).

---

## WHAT IS LOAD-BEARING AND WHAT IS THEATRE

**Load-bearing (1 of 5):**

- **`census_drift_patrol`.** 46 tests, 5 files, real subprocess against
  synthetic estates, plus a 196-line self-test with named regression vectors
  that runs live and passes. It killed 2 of 3 mutations by name. It also has a
  genuine defect the suite caught (the TZ bug) — which is the system working
  end to end. Its one hole is the COLLECT-DRIFT arm.

**Theatre (3 of 5):**

- **`config_seal` — the most actionable finding in this lane.** Hard block,
  zero tests, currently **RED with 11 problems** (6 modified, 5 unsealed,
  including `providers.yaml` and `spend_overlay.yaml`).
- **`secret_gate` — hard block on both arms, zero tests, and newer than the
  last audit.** The most exposed surface in the hook and the least examined.
- **`violation_ratchet's blocking path — 7 tests, all `== 0`.** Disarm it and
  the suite is green. The tests are about bookkeeping, not the decision.
- **`checkbox_receipt_gate` — zero tests, `|| true`, and RED right now** (1
  offender, B2-142). A dashboard, not a gate.

**Not theatre, and worth saying plainly:**

- The assertion-style census is clean: **2 swallows in 2,278 tests**.
- The hook's own test surface is the estate's best work: `tests/hook_pairing.py`
  reads the **real hook bytes** and replays through **real `sh`**, and
  `test_scenarios_gate_hook_pin.py::test_case_flip_is_caught` is an honest
  falsifier that *requires* a regression to stop matching. Hook bytes are never
  duplicated into tests, so they cannot drift.
- `tests/conftest.py` carries a suite-wide autouse isolation fixture that makes
  log pollution structurally impossible rather than per-test discipline.

**The pattern worth naming: this fleet tests that its instruments RUN, and
almost never tests that they BLOCK.** A gate's entire value is in the branch
that says no, and that branch is the untested one in every case measured here —
with `census_drift_patrol` the single exception, and even it has one uncovered
arm.

---

## LIVE GATE STATUS AT AUDIT TIME (all three hard gates RED)

| Gate | Exit | Detail |
|---|---:|---|
| `violation_ratchet check --changed` | **1** | 110 changed files, 71 hits, 64 registered, **7 NEW** |
| `config_seal verify` | **1** | sealed=49 live=54, **6 modified, 5 unsealed** |
| `checkbox_receipt_gate` | **1** | 406 checked Open rows, 69 baseline-attached, **1 offender (B2-142)** |
| `census_drift_patrol --self-test` | 0 | `CENSUS-PATROL SELF-TEST: PASS` |

**The repo is currently UNPUSHABLE** at gate 1 and gate 2. The suite is green on
all of it because it never looks.

---

## CLEANUP

- No repo file was modified. All mutation work was in-memory or inside
  `scratch/lane4/mirror_census`, outside the tree.
- `git status --porcelain | grep -i 'lane4|mutplug|mirror'` → **NONE**.
- The `agents/tmp*` entries in git status predate this lane (Sep-26 17:31) and
  belong to sibling lanes.

## RECEIPTS

- `memory/audit_20260926/lane4_robustness.json` — machine-readable, validates as JSON.
- Scratch instruments: `scratch/lane4/assertstyles.py` (assertion census),
  `zeromock.py` (zero-assert + gate/mock map), `resolve_lines.py` (33 → file:line),
  `mutate.py` / `mutate2.py` (in-memory battery + controls),
  `mutate3.py` (file-level mirror battery + collection gate).
