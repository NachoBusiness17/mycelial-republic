# driver-meter lane receipt, ball3-suite-green (2026-09-29)

Lane: driver-meter (division B). Raw check output:
`watch/inbox/gala_20260925/ball3-suite-green/lanes/driver-meter.check.txt`

## Finish line

All four targets green, live driver still running:

- CHECK 1 (check.txt): the four files, default basetemp, `35 passed`, exit 0.
- CHECK 2 (check.txt): the four files with pytest basetemp OUTSIDE the repo
  (`C:/Users/foste/AppData/Local/Temp/driver-meter-ball3-out-of-repo`),
  `35 passed`, exit 0. This is the wave5 suite-burn disease shape
  (`suite-burn-w5-full-basetemp-r3` in
  `watch/inbox/gala_20260925/wave5-repair/lanes/suite-burn.check.txt`).
- CHECK 3 (check.txt): the four named tests individually, verbose, `4 passed`.
- CHECK 4 (check.txt): production mutex `Local\MagStealthDriverInstance`
  still HELD by the live driver (probe raised InstanceLocked), driver pids
  49400 and 54484 alive (started 2026-09-29 11:29:31), heartbeat advanced
  cycle 28 (18:29Z) to cycle 30 (18:42Z) while the lane ran.
- CHECK 5 (check.txt): `tools/violation_ratchet.py check --changed` after
  the mag/+tools/ edits: `RATCHET: PASS`, exit 0, NEW=0. Two GROWTH ledger
  lines printed (mag/corpus_selfsteal.py +23, tools/stealth_driver.py +719):
  both are growths already on disk from earlier lanes' landings, not this
  lane's delta (this lane added ~30 lines to stealth_driver.py).
- CHECK 6 (check.txt): post-restore confirmation after the stash
  reproduction, `35 passed`, exit 0.

## Root causes (one per named failure)

### 1. test_instance_lock_refuses_second_acquire (tests/test_stealth_tools_wave5_repair.py)

Root cause: the LIVE stealth driver holds the production named mutex
`Local\MagStealthDriverInstance`, so the test's FIRST
`acquire_instance_lock()` was refused, not its second (the traceback named
the mutex and the driver pid pair below). The test was written to prove
second-acquire refusal; a live driver made even acquire #1 raise.

Fix: `acquire_instance_lock(namespace: str = "")` in `tools/stealth_driver.py`.
A namespace suffixes the lock into a private lock object (win32: mutex
`Local\MagStealthDriverInstance.<ns>`; posix: `state/stealth_driver.<ns>.lock`).
The test now acquires in a pid-unique namespace `ball3.<pid>` and still
proves the second acquire refuses. Production callers pass no namespace and
keep the strict shared lock (probe in CHECK 4 proves the live driver still
holds it). The posix branch of the namespace path is untested on this host
(win32 seat).

### 2. test_work_sets_tick_flag (tests/test_stealth_driver_v2.py)

Root cause: `t_work`'s mined row built `answer_file` via
`out.relative_to(ROOT)` (pre-fix `tools/stealth_driver.py:530` hermes branch
and `:625` direct-API branch). When pytest's basetemp sits outside the repo,
`WORK_OUT` is monkeypatched into a tmp_path outside ROOT and `relative_to`
raises ValueError, crashing `t_work`. Byte proof: CHECK 7 in check.txt, the
fixes git-stashed, out-of-repo basetemp,
`E ValueError: ...test_work_sets_tick_flag0\out\w1_hermes.md is not in the
subpath of ...local_sovereign_agent`. With the default in-repo basetemp
(`agents/pytest-tmp-*`) the test passed, which is why it looked intermittent
across runs.

Fix: `_rel_posix()` helper (repo-relative posix, absolute fallback). The
consumer (`impfeed`, `p = ROOT / af` at `tools/stealth_driver.py:1171`)
resolves an absolute `af` unchanged on Windows, so the fallback is safe.

### 3. test_honest_cache_meter.py::test_agent_state_commit_hash_excludes_its_own_field

Root cause: `mag/agent_state.py` commit receipts called
`fpath.relative_to(ROOT)` / `LATEST_MD.relative_to(ROOT)` (pre-fix lines
407-408), same out-of-repo tmp_path class. Byte evidence: the earlier suite
log `watch/inbox/gala_20260925/wave5-repair/lanes/suite-burn.check.txt`
failed this exact test at exactly `mag\agent_state.py:407` with the same
ValueError. The hash-exclusion invariant the test asserts was NEVER broken:
`content_commit_hex` hashes `_body_for_hash(state)` which skips
`{tip, chain_row, pack_excerpt, content_commit}` (`mag/agent_state.py:163-174`),
and the assertion passed in every run this lane made.

Fix: `_display_path()` helper (repo-relative when possible, absolute
otherwise). Display-only receipt fields; byte-identical output for the
default in-repo STATE_DIR.

### 4. test_violation_ratchet.py::test_baseline_update_stamps_accepted_lines

Root cause: the B2-273 print in `cmd_baseline_update` called
`BASELINE_PATH.relative_to(ESTATE_ROOT)` (pre-fix
`tools/violation_ratchet.py:300`), same class. Byte evidence: the same
suite log failed this test at exactly that line
(`suite-burn.check.txt`, `E ValueError: ...suite-burn-w5-full-basetemp-r3\
	est_baseline_update_stamps_ac0\violation_baseline.json ...`).

Stamp-shape census (the ask's pollution hypothesis, checked against the real
register `configs/violation_baseline.json`): 945 accepted claims; 9
file-too-long claims carry `accepted_lines` and every one was accepted by a
NAMED accepter (agent:b2-173-links-sha-ratchet, drift-patrol-cron overnight
accepts with named notes); 193 older file-too-long claims predate B2-273 and
legitimately lack the stamp; ZERO entries carry the default `"operator"`
attribution that a `--by`-less baseline-update stamps. The hypothesized
default-attribution pollution from the wave5 fold did NOT happen. The fix is
the print only (try/except to absolute path); the stamp code
(`cmd_baseline_update:292-295`) was already correct and stays.

## Live-state findings for the operator (not fixed by this lane, out of scope)

1. TWO stealth driver processes are alive: pid 49400 (Mag venv pythonw) and
   pid 54484 (uv cpython-3.11 pythonw), both running
   `scripts/run_stealth_driver.py`, both started 2026-09-29 11:29:31 (22ms
   apart). One writes the heartbeat (cycles advanced 28 to 30 during the
   lane, one coherent writer); the production mutex is held. This is the
   boot-lane double-launch disease documented in the driver header comment
   (the 09-28 pair). This lane did not kill either process; the namespace
   fix makes the test surface immune to it.
2. A one-off PermissionError storm across all 35 tests reproduced once
   mid-lane and never again: this lane's own background grep held files open
   under the pytest tmp dir during tmp cleanup (win32 open-file collision),
   not estate code. Named here so the next reader does not chase it.

## Decision ledger

Closes: the ball3 suite-green four failures (driver + meter).
Changes: (a) the instance-lock test surface is live-driver-proof by lock
namespace while the production lock stays strict; (b) the
relative_to-out-of-repo defect class is fixed at root in the three files
this lane owns (tools/stealth_driver.py, mag/agent_state.py,
tools/violation_ratchet.py); (c) the ratchet register default-attribution
pollution hypothesis is refuted by byte census.
