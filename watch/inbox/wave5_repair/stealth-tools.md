# stealth-tools receipt: wave5-repair (division B lane)

Date: 2026-09-29. Lane: stealth-tools. Owner scope honored: tools/stealth_fanout.py,
tools/stealth_driver.py, their tests. Sources read first:
watch/inbox/burn_reset_20260927/flash50/stealth-sw-03.md,
stealth-sw-15.md, _arch03_out.txt (arch-03), plus the tools themselves and
state/fuel/stealth_driver.jsonl. Raw check log:
watch/inbox/gala_20260925/wave5-repair/lanes/stealth-tools.check.txt

## Fix 1: NTFS ADS defect (fanout write site)

Defect (stealth-sw-15 finding 1, verified live): the old construction at
tools/stealth_fanout.py:135 was
`OUT_DIR / f"fan_{item_id}_{lane['model'].replace('/', '_')}.md"`, so model
`inclusionai/ling-3.0-flash-sante:free` produced `...sante:free.md`; NTFS
splits at the first colon and the lane answer landed in a `free.md`
alternate data stream on a 0-byte base file. This session's negative
control reproduced it exactly: writing the old-style name yields base file
size 0, empty content, streams `:$DATA 0` + `free.md 21`.

Fix: `slug()` at tools/stealth_fanout.py:105 replaces every NTFS-unsafe
char (`< > : " / \ | ? *`) and control char; the write site (now line 154)
is `f"fan_{slug(item_id)}_{slug(lane['model'])}.md"`. The driver got the
same law for its own write sites (its item ids come from Hermes output via
the self-feed queue): slug at tools/stealth_driver.py:126,
`_work_out_name()` at :145, used at both t_work write sites (:462 hermes
lane, :548 direct lane). The driver does NOT import through the tools
package (tools/__init__ drags the whole toolbelt plus mag.vision into this
always-on loop); both slug implementations are pinned to identical behavior
by tests/test_stealth_tools_wave5_repair.py.

Finish line A (probe A in the check log): the fixed write site round-trips
an answer through the colon model slug; filename
`fan_probe-ads_inclusionai_ling-3.0-flash-sante_free.md`, colon absent,
base file 184 bytes containing the body, stream listing shows only
`:$DATA 184`.

## Fix 2: selffeed rc=1 root cause and repair

Failure shape (arch-03 plus tonight's heartbeat, cycles 149-156):
`ERR selffeed: rc=1 The system cannot find the file specified.` on every
cycle, 19+ consecutive ERRs across 2026-09-28/29.

Root cause is TWO stacked defects in `_dispatch_hermes`:

1. Wrong python. The old code set `hermes_python = sys.executable` (the
   comment claimed "Hermes Python, already on PATH"; it is the DRIVER's
   python). Under the boot lane that is the Mag venv pythonw (PID 55528)
   or a uv pythonw (PID 55068), never Hermes. Measured this session:
   hermes_cli under the Mag venv python exits rc=0 with EMPTY stdout
   (silent no-op, probe banked in wave5-repair/lanes/_probe_selffeed_repro.py),
   while Hermes's own venv python
   (C:/Users/foste/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe,
   also 3.11.15) answers `-z` with real stdout: rc=0, 'OK', 24.4s (probe
   _probe_hermes_python.py).
2. Wedged cua-driver named pipe. hermes's update.log documents the exact
   disease: "process alive but \\.\pipe\cua-driver is not accepting
   connections... MCP / CLI calls will fail with 'cannot find the file
   specified' until this process is killed". Verified live: daemon pid
   8488 alive (started 9/25/2026 11:47 PM), `Test-Path \\.\pipe\cua-driver`
   False. The per-cycle alternation (work-via-hermes succeeded at cycle
   153 the same morning selffeed ERR'd) shows the pipe failure is
   per-dispatch, not constant.

Fix (tools/stealth_driver.py):
- `_hermes_python_candidates()` :290 and `_resolve_hermes()` :312 resolve
  HERMES_PYTHON env, then `<HERMES_HOME>/hermes-agent/venv/Scripts/python.exe`,
  then `<HERMES_HOME>/tools/python-*/python.exe`; `_dispatch_hermes` :338
  refuses to spawn a python that is not Hermes and returns a loud
  `GATE-OFF hermes: ...` immediately (no 600s burn) when nothing resolves.
- `_hermes_failure_cause()` :322 names the known signatures: the
  cannot-find-the-file string maps to the wedged cua-driver pipe with the
  cure (kill stale daemon pid, restart cua-driver-serve task); rc=0 with
  empty stdout is named a silent no-op instead of passing silently.
- The selffeed gate :973-1027: after SELFFEED_GATE_AFTER=3 consecutive
  dispatch failures, t_selffeed stops burning dispatches and returns a
  loud `GATE-OFF selffeed: ...` line each cycle (streak + last cause
  persisted in WORK_STATE), with one re-probe every 36 cycles; success
  resets the streak.

Finish line B (probe B in the check log): a real selffeed dispatch cycle
through the fixed driver returned REAL OUTPUT in 42.0s:
`selffed m7: Quantify the ALLOW_RE x ENT counter-leak blast radius in the
secret ga...`; work queue rows 13 -> 14; selffeed_fail_streak after: 0.
(The proposed m7 item is real queue state, the self-feed law working as
designed.)

## Fix 3: single-instance lock

Live race evidence at session start: two driver instances, PIDs 55528
(.venv pythonw) and 55068 (uv pythonw), BOTH started 2026-09-28 11:47:55.
The heartbeat held 76 rows while its newest cycle number was 156, so
roughly half the cycles never landed a row (the two loops interleave and
skip turns). arch-03 recorded the same race the night before.

Fix: `acquire_instance_lock()` at tools/stealth_driver.py:642 (win32 named
mutex `Local\MagStealthDriverInstance`, posix flock on
state/stealth_driver.lock; both auto-release when the holder dies, so no
stale lock can exist), `InstanceLocked` :622, wired into `main()` :1082
for BOTH loop and once modes: a second instance prints
`stealth_driver: REFUSED second instance: ...` and exits 2 before running
any topic. Two handle-hygiene bugs were caught by the wave5 lock test
during development: un-typed CloseHandle truncated the 64-bit handle
through a 32-bit c_int, and the ERROR_ALREADY_EXISTS path leaked the
duplicate mutex handle; both fixed in code (typed kernel32 binding at
module level, CloseHandle before raising).

Finish line C (probe C in the check log): a holder process took the lock,
then the real `tools/stealth_driver.py once` exited rc=2 with the REFUSED
line on stdout; no topics ran.

OPERATOR NOTE: the two racing instances are still running OLD code and
hold no lock; the law takes effect on their next restart. I did not kill
them (operator call: create state/stealth_driver.off to stop both, delete
it, then start one instance via the boot lane line).

## Fix 4: mirrors.json on-change throttle (s2-10 F1)

Defect: t_roster rewrote configs/mirrors.json every cycle (fresh ts every
5 minutes). Note: the file is NOT git-tracked (`git ls-files` empty), so
this was disk churn, not git dirt. Fix: `_write_mirrors_if_changed()`
:741 compares the new hosts catalog against the file on disk and writes
atomically (tmp+replace) only on difference; t_roster reports
`mirrors: written|unchanged` in the heartbeat (:828-829).

Finish line D (probe D in the check log): against the REAL converged
mirrors.json, an identical catalog returns False with mtime and bytes
unchanged; a changed catalog on a scratch copy returns True and writes.

## Tests

tests/test_stealth_tools_wave5_repair.py (new, 8 tests): slug parity
across both tools, fanout write-site round-trip (no ADS), work_out_name
sanitization, hermes gate-off when unresolvable, failure-cause naming,
instance lock refusal + release, mirrors on-change, selffeed loud gate
with streak/reset. Ran:
`.venv/Scripts/python.exe -m pytest tests/test_stealth_tools_wave5_repair.py
tests/test_stealth_driver_effort_dial.py tests/test_stealth_driver_prompt_lance.py -q`
= 12 passed (check log). The FULL suite was not run in this lane (scope;
targeted files only). tests/test_selffeed_integration.py (live-hermes
script test, not pytest-collected as a unit) still matches t_selffeed's
success contract.

## Ratchet and an incident I caused and undid

`.venv/Scripts/python.exe tools/violation_ratchet.py check --changed`:
exit 1, FAIL. The 4 NEW hits are NOT this lane's files (mag/
corpus_gap_research.py, mag/corpus_selfsteal.py, mag/link_library.py
file-too-long; tools/fossil_check.py shell-true) - they belong to sibling
lanes' uncommitted work in the shared tree. Two advisory GROWTH lines:
mag/shared_surface.py (+21, not mine) and tools/stealth_driver.py
accepted at 753 lines, now 1108 (+355). Re-audit of my part: HEAD was
already 879 lines (so +126 predates this lane); this lane added +229
(hermes resolution block ~85, instance lock ~95, mirrors throttle ~30,
selffeed gate ~30, slug + _work_out_name ~30, net of docstring/spacing).
Re-acceptance by name is left to the operator; I did not run
baseline-update deliberately.

Incident: an exploratory `baseline-update --help` call EXECUTED the update
(the tool has no --help flag; main() runs baseline-update on any such
argv) and registered the 4 sibling NEW claims with by=operator. Undone in
the same session: the 4 fingerprints removed and
configs/violation_baseline.json restored byte-identical to HEAD
(content-equality verified before the restore: 941 claims both sides,
0 fingerprint diffs, 0 entry diffs). The ratchet now reads exactly as it
did before my session (same 4 NEW, exit 1). Logged in the check file.

## Adjacent defect flagged, NOT fixed (outside owner scope)

tools/stealth_fanout_wave2.py:39 has the identical colon defect
(`fan2_{item_id}_{lane['model'].replace('/', '_')}.md`). Not in this
lane's ownership; same one-line slug fix applies.

## Honest gaps

- The full pytest suite (2,303 collected) was not run; targeted files
  only, per lane scope.
- The cua-driver stale daemon (pid 8488) is NOT fixed: killing it needs
  admin per hermes update.log; that is a system state change outside this
  lane. Until it is cleared, hermes dispatches may still intermittently
  fail rc=1; the driver now names the cause loudly and gates selffeed
  after 3 consecutive failures instead of burning dispatches.
- The two live old-code driver instances keep selffeed-ERRing until
  restarted; restart is an operator call.
- probe20/network topics were not exercised beyond the selffeed probe.

## Decision ledger

Closes: the stealth-tools owed-work waltz of wave5-repair (ADS silent data
diversion, unnamed selffeed rc=1, driver instance race, mirrors churn).
Changes the driver's operational contract in three ways: exactly one
driver instance may run (second refuses, exit 2); hermes dispatch failures
now name their cause and gate selffeed off loudly instead of burning
600s cycles silently; mirrors.json is a change-log, not a per-cycle
snapshot. Ratchet GROWTH on stealth_driver.py (+229 this lane) is open
for operator re-acceptance by name.
