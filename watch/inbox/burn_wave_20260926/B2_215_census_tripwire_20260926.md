# B2-215 census freshness tripwire (2026-09-26)

## Verdict

landed. The test-count carrier is now watched by a gate of its own: `tools/census_drift_patrol.py` flags the AGENTS.md `**Tests:**` bullet as STALE when its census date is older than 7 days while `tests/` has grown (commits adding test files after the census day, or the on-disk candidate count off the carrier's own claim). Wired WARN-ONLY into `githooks/pre-push` per the t40 precedent, flip-to-enforce left as an operator call. Live repo run today: exit 0. The exact 09-14 disease reproduced in a synthetic estate: exit 1 at 12 days with the growth named. The 12-day blind spot that carried the hand-copied 1,341 headline is closed.

## Evidence

- The disease, in bytes: `watch/inbox/burn_wave_20260926/B2_69_test_census_20260926.md` records the retired "1,341 tests / 264 files" headline dated 2026-09-14 riding until 2026-09-26. `git log --diff-filter=A --name-only -- tests/` shows 31 test files added by commits dated after 2026-09-14 (including `tests/test_process_supervisor.py`, 2026-09-19T17:58-04:00, the B2-51 mid-wave landing). The pre-push hook before this lane had four blocks (ratchet, config_seal, description_pin WARN, freshness_gate WARN over inbox receipt stamps only): none read test-count carriers.
- New tool `tools/census_drift_patrol.py`: bar stated in the docstring before any read; verdict core `patrol()` is pure; STALE = age > 7d AND growth; a same-window count lag is evidence-only so a census snapshot may lag intra-day landings without crying wolf; fail-closed exit 2 on missing or unparsable `**Tests:**` line, future-dated census (freshness_gate fabrication-smell convention), or git failure. Growth measured by git bytes only; the gate never runs pytest, the collect-only rerun stays the human falsifier (B2-69 law).
- Self-test: 14/14 PASS, including the real fossil line as regression case: the retired carrier text parses to 1341 collected / 264 files / 2026-09-14 and `patrol(2026-09-14, 2026-09-26, 31, 303, 264)` returns STALE exit 1. One self-test defect found and fixed during landing: the candidate-count fixture created 2 files but asserted 3; expectation corrected by adding a `*_test.py` file so both pytest naming patterns are exercised.
- Targeted pytest: `tests/test_census_drift_patrol.py` 25 passed in 2.66s. One collection error hit and fixed during landing: a from-import of the tool's `test_files_added_since` helper dropped a `test_`-prefixed name into the test module namespace for pytest to mis-collect ("fixture 'root' not found"); switched to module import, call sites go through `cdp.`.
- Fossil-catch demo (synthetic estate, exact retired carrier text, 3 test files committed today, `--days 7`): "CENSUS-PATROL: STALE - census 2026-09-14 (1341 collected / 264 files) ... census 12d old (bar 7d) while tests/ grew: 3 test file(s) added by commits after 2026-09-14; disk holds 3 candidate files vs carrier claim 264", exit 1.
- Live repo run: "CENSUS-PATROL: ok - census 0d old of 7d bar, disk 303 vs carrier 301 (same-window lag, evidence only)", exit 0. The 303 is the honest current disk count; the carrier's 301 was this morning's collect-only figure and lanes landed test files since, exactly the intra-window lag the design tolerates without firing.
- Ratchet over changed files: `tools/violation_ratchet.py check --changed` scope 13, hits 13, registered 13, NEW=0, PASS.
- Spec first: the AGENTS.md:27 Tests bullet carries the tripwire law sentence (landed before the tool in this same lane), so the behavior has an owning spec line, not just code.

## Work done

1. Read pointers whole: `tools/freshness_check.py`, `tools/freshness_gate.py` + `tests/test_freshness_gate.py`, `githooks/pre-push`, the B2-69 census receipt, and the QUEUE brief.
2. Verified the bytes: 31 post-census test-file commits since 09-14; no pre-push block touched test-count carriers; disk count moved again today (301 at census time to 303 now), which set the same-window evidence-only rule.
3. Landed in order: AGENTS.md spec sentence, `tools/census_drift_patrol.py`, `tests/test_census_drift_patrol.py`, WARN-ONLY hook block (`sh -n` checked).
4. Verification battery: self-test 14/14, targeted pytest 25/25, live run exit 0, fossil demo exit 1, ratchet PASS with 0 new debt.
5. Filed this receipt, appended the LEDGER row via venv python json.dumps, self-fed B2-242 and B2-243 into QUEUE.md Open, and registered this receipt in the shared inbox index (writer b2-215-census-tripwire).

## Falsifier

- Break the carrier on purpose: edit AGENTS.md:27's census date to 2026-09-14, wait for or force any test-file commit after that date, rerun `.venv/Scripts/python.exe tools/census_drift_patrol.py`: it must print STALE and exit 1 (surfacing as a PUSH-GATE census WARN line, no lockout until the operator flips the block). The synthetic-estate CLI test `test_cli_stale_synthetic_estate_exits_1` pins this at 25-passing bytes.
- If pytest collection naming ever moves (`python_files` in pytest.ini), the disk-count branch silently undercounts: the git-growth branch still fires on new files, but same-file parametrize growth stays invisible (self-fed as B2-243).
- A rewrite of the bullet that drops the `**Tests:**` label makes the gate exit 2 on every push: that is the designed fail-closed alarm, never a pass. The parser also reads the first date and first "N files" match in the bullet, which is order-fragile if prose numbers ever precede the claim (self-fed as B2-242 covers the collected-count branch; the order fragility is named here as known sharp edge, not papered over).

## Bibliography closed

tools/freshness_check.py; tools/freshness_gate.py; tests/test_freshness_gate.py; githooks/pre-push; tools/violation_ratchet.py; AGENTS.md:27; pytest.ini; watch/inbox/burn_wave_20260926/B2_69_test_census_20260926.md; watch/inbox/burn_wave_20260926/QUEUE.md (## Open, B2-215 brief); tools/census_drift_patrol.py; tests/test_census_drift_patrol.py; memory/burns/LEDGER.jsonl.
