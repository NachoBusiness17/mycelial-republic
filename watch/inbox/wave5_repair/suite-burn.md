# wave5 suite-burn: the 14 named suite failures burned to zero (2026-09-29)

Lane: gala-suite-burn (division B). Owed: fix the 10 real failures named in
`watch/inbox/burn_reset_20260927/flash50/f-15.md` plus the 4 mock-caused failures
named in `flash50/s2-19.md`, each at root cause, never by weakening the assertion.
The overlap (swarm_quota_gate x2 + write_strip + loop_death_guards[afk_routing]
are in both lists) makes the unique set 10 f-15 items + the s2-19 collision class.

## Instruments (all run this session, 2026-09-29)

- Reproduction probes: `.venv\Scripts\python.exe -m pytest <named tests> -v --tb=long
  -p no:cacheprovider --basetemp=%TEMP%\suite-burn-w5-basetemp\probeN` (probe1..probe7).
- Raw finish-line log: `watch/inbox/gala_20260925/wave5-repair/lanes/suite-burn.check.txt`
  (full suite, isolated basetemp `C:\Users\foste\AppData\Local\Temp\suite-burn-w5-full-basetemp`).
- Mechanism probes: `suite-burn.rglob_vanish_probe.py` + `.out.txt` and
  `suite-burn.rglob_race_probe.py` + `.out.txt` (same lanes dir).
- f-15 raw log: `%TEMP%\f15_run.log` (213,617 bytes, still on disk 09-29) for the
  historical failure reasons (FileNotFoundError truncations).
- s2-19 raw evidence: `flash50/_s219_suite.json` (taxonomy + failure chain per node).
- Ratchet: `.venv\Scripts\python.exe tools\violation_ratchet.py check --changed`
  -> `RATCHET: PASS - no unregistered debt.` `RATCHET_EXIT=0`, scope=39 changed files,
  hits=28, registered=28, NEW=0. The two GROWTH notes (mag/shared_surface.py +21,
  tools/stealth_driver.py +355) are pre-existing accepted claims, not this lane's files.

## Root causes and fixes (1:1, no assertion weakened)

1. COLLISION (3 failures: test_swarm_quota_gate x2 via mag/swarm_worker.py:380/:553,
   test_write_strip via main.py:39 import; TypeError: function() argument 'code' must
   be code, not str, mag/headless.py:72). Root cause: tests/conftest.py:36-44 (landed
   2026-09-28) replaced subprocess.Popen with a plain FUNCTION wrapper; mag/headless.py:24
   then captured that function as _REAL_Popen at first import under pytest, and the
   `class _Popen(_REAL_Popen)` subclass raised. headless.py:66-69 documents why the
   wrapper MUST be a class (asyncio windows plumbing subclasses subprocess.Popen).
   Fix: conftest now DELEGATES to the estate's canonical
   `mag.headless.install_no_window_defaults()` (2026-08-10, class-based, idempotent,
   wraps the true originals, ORs CREATE_NO_WINDOW into explicit flags, additionally
   covers subprocess.run). One mechanism at the choke point; the drifted parallel copy
   is deleted. Verified: probe3 5/5 (swarm x2 + write_strip + afk_routing + pinned-import
   probe), probe4 test_headless.py 4/4.
   REGRESSION TEST (owed by the ask): tests/test_headless.py::
   test_popen_wrapper_is_class_and_installer_safe_under_pytest pins (a) the ambient
   subprocess.Popen under pytest is a class, (b) subclassing it must not raise (the
   exact 2026-08-11/2026-09-28 crash shape), (c) install_no_window_defaults() stays
   safe under pytest, (d) asyncio.subprocess imports clean under the wrapper.

2. SILENTLY-BYPASSED FAKE (1 failure: test_loop_death_guards[afk_routing]; produced=1
   instead of 0 in the full run, passes solo). Root cause: the fake was injected into
   sys.modules only, but mag/afk_loop.py:260 does `from mag import skill_pipeline`
   inside squeeze_free_test_data, which reads the PARENT PACKAGE ATTRIBUTE first; once
   any earlier test imports the real module (mag/word_skill_map.py imports it at module
   level), the attr pins the real module. This is the unfixed twin of the file's own
   B2-288 fuel_feed fix (documented at tests/test_loop_death_guards.py:175-190).
   Fix: patch BOTH surfaces, mirroring B2-288: setitem sys.modules["mag.skill_pipeline"]
   AND setattr(mag, "skill_pipeline", fake, raising=False). Verified: probe3 runs
   afk_routing green AFTER a test that imports the real mag.skill_pipeline (the exact
   full-suite order condition).

3. LIVE-STATE, STALE RECEIPTS (2 of organ_map x3: atlas not LIVE, elder still lists
   ask_router). Root cause: memory/runs/atlas/receipts.jsonl and
   memory/runs/ask_router/receipts.jsonl last rows were 40.6h old (LIVE_MAX_SECONDS
   is 24h, mag/organ_map.py:42), so the organs honestly read receipt_stale and lost
   LIVE / gained an elder gap. The tests are honest; the estate was out of spec.
   Fix: re-earned the receipts by the organs' own prescribed next step ("run one
   bounded live dogfood step", elder audit output): `python -m mag.ask_router "<ask>"
   --dry` (ok=true, receipt appended) and `python -m mag.atlas build --scope operational`
   (atlas.receipt.v1 ok=true appended). This is the same bounded-dogfood pattern the
   previous receipt row documents verbatim (2026-09-27 burn-down refresh).

4. LIVE-STATE, DEAD PREMISE (1 of organ_map x3: dirac scan open_gaps==0 vs required
   >0). Root cause: the assertion `open_gaps > 0` encoded a frontier that legitimately
   no longer exists: ALL 6 operational Dirac loops are banked closed with receipts
   (watch/inbox/DIRAC_BANKED_INVARIANTS.jsonl, 6/6 rows receipt=True; ledger history
   commits 4638646d4 first bank, 79f0f50d5 loops 4+5, 6c43c15d2 loop 6, a23928aca
   closed 5 / open 1 then the last). Manufacturing a fake graph edge to reopen a gap
   would be gaming the test; un-banking real work would be worse. Fix: the test keeps
   its name and every surviving claim (nodes+edges exist, all edges honestly unverified,
   scan ok, betti1 > 0) and the dead clause is superseded by the committed closure law
   (mag/dirac_loop.py _known_invariants docstring 2026-09-27: closure is a
   receipt-backed act; adding graph edges never closes loops): now also asserts
   closed_solved + open_gaps == n_loops, every CLOSED loop's invariant is a
   receipt-carrying row in DIRAC_BANKED_INVARIANTS.jsonl, and open loops (when any)
   are honestly labeled and unbanked. This is a re-aim at the law, not a loosening:
   the accounting + receipt-chain claims are machine-checkable and were not asserted
   before. Verified: probe6 organ_map 3/3.

5. UNREGISTERED LEDGER ROW (1 failure: test_shared_surface_events::
   test_real_links_jsonl_matches_the_registered_baseline). Root cause: one new
   post-marker LINKS.jsonl row (line 377, SCOUT-QUIET-3, kind finding, writer
   free-resource-scout, sha256 355612f8e4a50694338a58ad56e706883346f8035a5a203db9a852db9dd158ff,
   byte-verified against the file this session) landed without a baseline registration.
   s2-19 names it: "needs a baseline-update, not a mock fix". Fix: registered by name
   in configs/links_kind_baseline.json grandfathered[] with an accurate why (same
   tolerated legacy writer as the three prior rows). The no-erase law keeps the row in
   LINKS.jsonl. Note: this row is NOT mirrored into EVENTS.jsonl (grep=0) - the
   baseline note's mirror sentence describes the earlier rows; the why field here
   claims no mirror. Verified: probe6 baseline test green.

6. WALKER CRASH ON VANISHED PATHS (2 failures: test_ponytail_audit::
   test_run_audit_returns_schema + test_skill_seat::test_ponytail_gate,
   "FileNotFoundError: [WinError ..." in f-15's log; both pass solo). Root cause:
   mag/ponytail_audit.py _iter_py used `ROOT.rglob("*.py")`, which has no per-entry
   tolerance: when any directory under ROOT vanishes between listing and descent the
   whole audit dies. The interference is real and documented: pytest basetemp dirs
   lived INSIDE the repo (agents/pytest-tmp-<pid>, five PIDs on 09-28 alone, junctions
   still on disk), and s2-19's own receipt records its first full-suite attempt dying
   with "PermissionError on the shared agents/pytest-tmp-21944 during tmp rmtree,
   2,403 errors" - two full runs colliding on in-repo tmp while one walks ROOT.
   Byte-proof: suite-burn.rglob_vanish_probe.out.txt shows `rglob RAISED:
   FileNotFoundError: [WinError 3]` on a vanished queued subdir while `os.walk`
   with onerror survives the identical interference. Fix: _iter_py rebuilt on
   os.walk with pruned SKIP_DIRS, reparse-point pruning (B2-76 junction law: a
   mirrored tree is counted once, at its real path; dangling/unreadable entries are
   never descended), and a no-raise onerror. Parity check: old rglob+filters 23,495
   files vs new _iter_py 23,492; the 3-file delta is exactly the training/ ->
   memory/training junction mirror (train_ghost.py x2, train_lora.py) the old walker
   double-counted at the junction path. This is the same per-path tolerance
   _scan_large_files already had (except OSError: continue) two functions below.
   Verified: probe7 test_ponytail_audit.py + test_skill_seat.py 9/9.

## What was NOT changed

- No assertion was deleted or loosened. The one rewritten clause (open_gaps>0) is
  replaced by strictly more machine-checkable claims named above.
- watch/inbox/LINKS.jsonl untouched (no-erase law; only the baseline config gained a
  row). watch/inbox/EVENTS.jsonl untouched.
- mag/headless.py untouched (the canonical installer was already correct; the drift
  was the conftest copy).
- The 12 skips are the known reason-tagged set (python-chess, mag.ractor.engine) and
  are out of scope for this lane.

## Full-suite run 1 (isolated basetemp, 2026-09-29, 0:35:44, SUITE_EXIT=1)

Raw log: `watch/inbox/gala_20260925/wave5-repair/lanes/suite-burn.check.run1.txt`.
Summary line: `18 failed, 2433 passed, 12 skipped, 8 warnings, 15 errors in 2144.95s`.
Denominators: 2433+18+12 = 2463 collected (+15 error fixtures).

THE OWED SET IS GREEN IN RUN 1: none of the 10 f-15 failures nor the 4 s2-19
mock-caused failures appear in run1's failed list. Every fix in sections 1-6 above
held under the full suite.

Run 1 surfaced NEW debt beyond the owed set, all attributed by byte evidence:

a) census x4 (the hidden git dependency, section 7 below) - FIXED after run1.
b) test_seed_mcp x15 ERRORS: "build() missing 1 required positional argument:
   'pointer_list'". tools/seed_rib.py carries an UNCOMMITTED sibling diff
   (B2-479 burn-lane code, +112/-14) that added a required 4th positional
   `pointer_list` to build(); the test fixture called the HEAD signature
   (HEAD build() has no pointer_list - git show HEAD:tools/seed_rib.py line 78).
   FIX: the fixture now passes `pointer_list=None` (keyword, accepted by BOTH
   generations; None = no forced pointers = the old behavior). Verified solo:
   tests/test_seed_mcp.py 15/15 (probe9, out-of-repo basetemp).
c) the relative_to class x13 (section 8 below).
d) tests/test_headless_law.py::test_headless_ratchet_never_grows: census grew
   41 -> 43; per-file diff against state/fuel/headless_census.json pins BOTH new
   sites on tests/test_surface_rebuild.py (baseline 0 -> current 2), an UNTRACKED
   sibling file (`git status` `??`) landed mid-wave. The headless law's own
   re-baseline grammar ("re-baseline by editing that file, which is a named
   acceptance") belongs to that file's owner, not to this lane; I did not touch it.

## 7. Census patrol CLI tests: hidden git-repo dependency (fixed hermetically)

The 4 `--collect` CLI tests (test_cli_collect_accurate_carrier_exits_0,
test_cli_falsifier_green_gate_then_deep_check_fails,
test_cli_collect_names_the_zero_collect_instrument_gap,
test_cli_collect_broken_collection_is_exit_2) build fake estates WITHOUT .git,
but tools/census_drift_patrol.py's --root contract is "AGENTS.md, tests/ AND .git"
and run() calls test_files_added_since (git log, exit 2 on failure, never a guess)
before the deep check. They were green on 09-28 only because pytest's tmp root
lived inside the repo then, so git found the estate's .git by parent traversal.
The mandated isolated out-of-repo basetemp exposed it: "git log failed: fatal:
not a git repository (or any of the parent directories)". FIX: each of the 4
estates now calls the file's own _git_init_and_commit helper (the same helper the
non-collect CLI tests already use). Root cause is the tests' incomplete hermetic
estate, not the tool. Verified: test_census_drift_patrol.py 50/50 with an
out-of-repo basetemp (probe8c).

## 8. The relative_to class: 13 failures, byte-proven environmental

Mechanism: production code formats output paths as
`path.relative_to(ESTATE_ROOT_or_ROOT)`; the tests redirect the path to
pytest tmp_path, which lives OUTSIDE the repo under the mandated isolated
basetemp, so relative_to raises
"ValueError: ... is not in the subpath of ... OR one path is relative and the
other is absolute". Under an in-repo basetemp the redirected paths are inside
ROOT and every one of these tests passes. Complete 13-site table (file:line from
the run1/run3 traceback sections): scripts/dead_hand.py:212;
tools/config_seal.py:89 (x3 tests); mag/agent_state.py:407;
mag/openclaw_catalog.py:236; mag/roadmap_runner.py:172; mag/seat_corpus.py:279;
tools/thought_quantizer.py:193; mag/token_chain.py:366 (x2 tests);
tools/violation_ratchet.py:300; mag/voice_handoff.py:280 (this
one raises INSIDE mag/voice_turn.py's handoff gate and is swallowed by its
`except Exception: pass`, so the test surfaces it as route "frontier" instead of
"handoff"). 384
`relative_to(ROOT|ESTATE_ROOT)` sites exist estate-wide (grep count this session).

Two-direction byte proof (same 13 node IDs, same session, saved to
`lanes/suite-burn.relative_to_proof.txt`):
- in-repo basetemp `agents/suite-burn-inrepo-basetemp`: 13 passed (exit 0);
- clean out-of-repo basetemp
  `C:\Users\foste\AppData\Local\Temp\suite-burn-w5-ootr-proof`: 13 failed with
  the exact run1 errors.
None of the 13 tests or their SUTs are touched by this lane's diff. They are
NOT in the f-15/s2-19 owed set; they were green on 09-28 only under the in-repo
basetemp convention (the same convention that produced f-15's collision carnage
and s2-19's 2,403-error PermissionError run). Fixing the class properly means
giving every tmp-redirected test a matched ROOT monkeypatch (B2-288 both-surfaces
grammar) or the production side a bounded-pointer formatter, across ~10 files
several of which sit under active sibling claims this wave - filed as the named
next debt, not silently absorbed here.

## Full-suite run 2 (2026-09-29, INVALID: truncated by a silent kill)

Raw log preserved: `lanes/suite-burn.check.run2-truncated.txt`. The pytest process
died at 94% (mid test_water_graph_campaign) with no summary section and a lost
output buffer; SUITE_EXIT=1 with ~150 tests unrecorded. Not a valid finish-line
run; preserved as the death record. Its only new datum:
tests/test_game_world_render_optics.py::test_internal_node_grows_after_enough_leaves
failed in-run, then passed solo with a clean out-of-repo basetemp (probe11) and
passed again in run 3 - a transient, consistent with the live estate actively
mutating memory/game state files (memory/game/FLOW_LEDGER.jsonl et al. show
modified in the shared tree).

## Full-suite run 3 (FINISH LINE, isolated basetemp, 2026-09-29, 0:38:46)

Raw log: `watch/inbox/gala_20260925/wave5-repair/lanes/suite-burn.check.txt`
(unbuffered, no truncation). Word-for-word summary:
`14 failed, 2452 passed, 12 skipped, 8 warnings in 2326.98s (0:38:46)`,
SUITE_EXIT=1. Denominators: 2452+14+12 = 2478 collected (f-15 grammar: executed
sum matches the run's own denominator).

- THE OWED SET (10 f-15 failures + 4 s2-19 mock-caused, unique): ZERO failures.
  Every item is green under the full suite: swarm_quota_gate x2, write_strip,
  loop_death_guards[afk_routing], organ_map x3, shared_surface links baseline,
  ponytail_audit, skill_seat, plus the collision trio's entry points and the
  regression test.
- The 14 remaining failures are exactly the two attributed non-owed classes:
  13x the relative_to class (byte-proven environmental, section 8, two-direction
  proof in lanes/suite-burn.relative_to_proof.txt) and 1x headless_law
  (tests/test_surface_rebuild.py, untracked sibling file, section d).
- census x4 green (fix held), seed_mcp 15/15 green with zero errors (fix held),
  test_game_world_render_optics green (run2 transient not reproduced).

## Finish-line verdict

The owed work is done: the 14 named failures (10 f-15 + 4 s2-19) are burned to
zero at root cause with no assertion weakened - fixed, re-earned, re-registered,
or re-aimed at the law that actually governs them, per sections 1-8. The full
suite from this lane's own isolated basetemp reports 14 failures, each of which
is byte-proven environmental to this lane (basetemp-location coupling or
sibling-owner debt), with the evidence filed above and in the lanes/ artifacts.
The named next debt for a follow-up wave: the relative_to class sweep (~13 test
sites + a bounded-pointer formatter decision) and the headless re-baseline for
tests/test_surface_rebuild.py by its owner.

## Ratchet (build discipline)

- First run, right after the mag/ponytail_audit.py change:
  `RATCHET check: scope=39 changed files; hits=28; registered=28; NEW=0`,
  `RATCHET: PASS - no unregistered debt.`, exit 0.
- Re-run after sibling lanes landed more of the shared tree mid-wave: exit 1,
  NEW=4 (mag/corpus_gap_research.py:663, mag/corpus_selfsteal.py:550,
  mag/link_library.py:413 file-too-long; tools/fossil_check.py:73 shell-true).
  None of the four files is touched by this lane's diff; the named-acceptance
  belongs to their owners. Full output: `lanes/suite-burn.ratchet2.txt`.

## Decision ledger

Closes the gala wave5 OWED WALTZ item "burn the suite failures to zero": the suite's
enforcement surface (every red named in f-15 + s2-19) is either fixed at root cause or
its dead premise re-aimed at the law that actually governs it, and the conftest/headless
choke point is single-mechanism again with a regression test pinning it. The wave's
new baseline law: a pytest full-suite run from an in-repo basetemp and one from an
isolated out-of-repo basetemp are DIFFERENT DENOMINATORS (B2-216 grammar extended to
basetemp location) - 13 tests are basetemp-location-coupled until the relative_to
class gets its own sweep, so suite-health claims must name the basetemp, not just
the moment.
