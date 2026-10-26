# BREAK-LOGIC pass on the logic lens (2026-10-04, eleven-doors ractor engine)

Hostile second pass over the logic lens report on the 24-wide dig's 11 remaining
build doors. Every claim below was byte-checked this session by me; commands
named inline. No em-dashes. Lens findings are numbered as given in the tasking.

## Verdicts

### Finding 1 (door 2's enforcement contract is unwired) - CONFIRMED, with two byte corrections to its own evidence

Substance verified end to end:

- Active hook confirmed: `git config --show-origin --get-all core.hooksPath` ->
  `file:.git/config githooks` (rc=0); `.git/hooks/` carries no non-sample hook,
  so githooks/pre-push is the only live pre-push surface.
- githooks/pre-push read in full (516 lines). Trigger arms are scoped to named
  files: caption (2 files), refold (3), workflow gate (1), parity (2 twins),
  golden vector (tools/dungeon.py). No arm touches mag/arena_bench.py,
  tests/test_arena_bench.py, or dashboard/static/(games/)?arrakis.html /
  dungeon.html. `grep -n pytest githooks/pre-push` -> exactly one hit, the
  comment at :201. Lens byte verified.
- The enforcement claim exists in THREE surfaces, all unwired: the receipt
  (watch/inbox/ARENA_BENCH_TRIPWIRE_20261004.md:47-49 "Pre-push now covers the
  bench"), the test docstring (tests/test_arena_bench.py:9-11; the lens cited
  :13-14, off by ~3 lines, the text is real), and the door-2 commit message
  itself (`git show --no-patch --format=%s 00cb15c77`: "4-test tripwire landed
  ... so the next move fails pre-push").
- I closed the lens's admitted gap: the four tests were never run by the lens.
  I ran `./.venv/Scripts/python.exe -m pytest tests/test_arena_bench.py -q` ->
  4 passed in 4.02s. `mag/arena_bench.py --selftest` -> rc=0 with verdict
  records present. The receipt's "4 passed" claim is now independently
  verified.
- Scheduled-task census (the lens falsifier's third arm): full schtasks name
  census this session, all Estate*/Mag* task names visible (10 Estate + 15 Mag
  tasks; none names arena/bench/test execution); `grep -ln pytest scripts/*.ps1`
  -> bootstrap_test_env.ps1, census_patrol_daily.ps1 (--collect-only via the
  patrol), restore_drill.ps1. None executes tests/test_arena_bench.py.

Two corrections the hostile pass caught in the lens's OWN evidence:

1. Its falsifier states "git remote -v shows no GitHub remote (PRIMER:108), so
   no external CI exists". FALSE today on both halves: `git remote -v` this
   session shows remote `github` -> NachoBusiness17/mycelial-republic.git, and
   `.github/workflows/ci.yml` EXISTS (landed 2026-10-01, Q51 fix). The lens
   inherited PRIMER:108's lane claim without rerunning it. The conclusion
   survives anyway because the CI is dark: `git for-each-ref refs/remotes` ->
   exactly 1 remote-tracking ref (refs/remotes/local/...), zero
   refs/remotes/github, so no push has ever reached GitHub and Actions has
   never fired; and ci.yml:45 triggers only on main (work rides mag/* branches
   per the workflow's own comment at :48-51), and its named-core pytest list at
   :84 (protocol_table + auth_srp6 + rule_parity) excludes test_arena_bench.
   No external CI executes the tripwire: right conclusion, wrong premises.
2. "pre-push ... runs ... ZERO pytest" is over-broad as a universal. The
   refold block's payload wrapper runs pytest conditionally:
   tools/refold_gate.py:167 `[sys.executable, "-m", "pytest", str(pins),
   "-q", "--no-header"]` over tests/test_index_fold_host.py when fold files
   change. Scoped truth: no hook arm ever executes any pytest on the
   arena-bench surface. Quantifier-law catch: the lens's own cited precedent
   for its move (githooks/pre-push:197-240, the refold shape) IS the
   pytest-running wrapper its universal denies.

The move (wire an arena-bench trigger in the refold shape) survives and is
correct; add the one-line rider of tests/test_arena_bench.py to ci.yml:84's
named-core list so the door's CI half is real whenever the repo lands on a host
(the workflow comment at :48-51 already anticipates that widening).

### Finding 2 (door 3 ~80 percent self-stolen, ~1h residual) - CONFIRMED, and its falsifier is now resolved AGAINST the cargo branch

All bytes verified:

- tests/test_night_march_cure_20261004.py:82-91 (atomic tmp+replace
  _save_state, no tmp dotfile) and :100-119 (trail-before-persist pin under a
  simulated OSError(22)) read this session: exact.
- mag/lane_runner.py:911-939 read whole: cycle_night gates only on
  `st.get("last_night") == today` (:919-920), never reads the trail; the
  ordering cure and the ~100s re-run history are documented at :932-936; the
  Errno-22 comment "the lock is external and transient, not code-side" is in
  _save_state at :128-132. Lens evidence byte-true throughout.
- The lens's blind spot (monitor idempotency) resolved by me:
  watch/monitor_lane.py's own docstring (:4-26) declares "Room: one row per
  run" and one poll of all three keyless APIs per run; its dedup is entirely
  state-gated (watch/monitor_lane.state seen-id lists). So a same-night re-run
  posts a fresh room row, re-polls all three sources, and if monitor's own
  state write fails in the same Errno-22 window (same host-mount class), the
  spool duplicates items. Monitor is NOT side-effect-free on re-run, so the
  "even the guard is cargo" branch of the falsifier is FALSE: the one-clause
  trail-consult guard cures real, small, live harm.
- Re-price judgment upheld: per-leg flags buy intra-cycle resume, but the
  in-cage march leg has been a deterministic rc=2 skip since the same night
  shift (test_march_no_env_file_exits_2_with_named_skip, :46-52), so there is
  no expensive second leg to resume past today. ~1h residual is the honest
  price; PRIMER:171's 2-4h priced harm the night shift already collected.

### Finding 3 (gwap re-grade adjudicator gap) - WEAKENED: one central census byte is false, and the harm is mis-scoped twice; the underlying gap is real and cheaper to cure than the lens priced

Verified true:

- mag/gwap_to_gps.py:77-78: SKIP_VERDICTS = (CHALLENGE, BLOCKED);
  VERDICT_TO_BIN = {VERIFIED_AGREE: 1, DISPUTE: 0}. feed_session's loop
  (:141-230 read) branches on verdict only; `grep -n engine
  mag/gwap_to_gps.py` -> only the demo string at :282-284. No engine-version
  gate exists. True.
- My census of memory/runs/gwap/arena-capability.jsonl: 613 rows, verdicts
  VERIFIED_AGREE 119 / CHALLENGE 204 / DISPUTE 290. Matches the lens exactly.
- GWAP_INDEPENDENT_COP_20261004.md:75-78 read: historical re-grade left as an
  operator decision. True.

False byte: "all 613 rows carry NO engine_version (counter {'<none>': 613})".
The lens's instrument read the payload top level, where engine_version never
lives; the mint itself is nested (tools/arena_gwap.py:218-224 puts
engine_version inside replay_tape_ref). My nested census
(`payload.replay_tape_ref.engine_version`): {arena-dungeon-v2: 327,
arena-tavern-v2: 286} - ALL 613 rows carry an engine stamp, every one v2.
The discriminant the lens said was absent already exists on every banked row.

Harm mis-scoped twice (this is the substantive weakening):

1. Not latent. The lens's blind spot ("whether the old 613-row file is ever
   fed to GPS is unverified") resolves against it: tools/arena_gwap.py:313
   constructs `SessionLedger("arena-capability")` whose default store is
   memory/runs/gwap/<session_id>.jsonl (mag/gwap_payload.py:30, :727), i.e.
   THE 613-row file, and :328 feeds `ledger.path` whole, with the comment at
   :320-323 saying the bridge walks the WHOLE ledger file. That is the live
   path.
2. Already banked, not future feedstock. sqlite census of
   tools/gps_mcp/gps_ledger.db3 verdict_log this session:
   arena-agreement-v1 = 351 rows = 248 verdict=0 + 103 verdict=1. The pre-v3
   DISPUTE poison is already sitting in the GPS ledger (v3 has banked zero
   rows: door-1 receipt :76-78 says the next --backfill is what banks v3). And
   feed_session's dedupe gate (model_id, task_shape, evidence_hash) means
   future refires of the same rows SKIP as duplicates - so a feed-side gate
   prevents almost nothing that has not already happened. The lens's move
   (version census in feed_session's report, dry-run default) targets the
   wrong ledger: the operator's re-grade number is the 248 zeros already in
   verdict_log, not the rows a future feed would carry.

The decay-family convergence the lens pointed at gets sharper: the already
banked 248 zeros are append-only-uncurable from the feed side; the pheromone
metabolism door (PRIMER rank 6, dispute-streak slashing + decay) is the only
door in the table whose mechanism dilutes already-banked stale verdicts without
touching the append-only bank. Finding 3's cure lives inside door 6.

### Finding 4 (EG-20) - verdict withheld as far as the input allows: the finding text was TRUNCATED in my tasking (evidence string cuts at "watch/inbox/ESTATE_GAP_DIG_20"), so I verdict only the visible evidence and the absence scope

- The visible evidence root checks out: ESTATE_GAP_DIG_20261004.md's
  enhancement table row 9 (read in the :60-82 window) is the EG-20 pass@K
  coverage column, effort 2h, success meter "column present; predicts the mesh
  vs frontier routing on one batch", self-steal source "X_INTEL_PAPERS #2;
  tools/arena_gwap.py". PRIMER:174 and :237 carry it as the runner-up with the
  same figures.
- Absence scope extended clean (lens blind spot 3): `grep -rn "EG-20|pass@K"
  watch/inbox/ queue/ state/ memory/ --include *.md,*.json,*.jsonl` (completed,
  exit 0) finds EG-20/pass@K ONLY in spec, register, intel, and lens surfaces
  (ESTATE_GAPS_20261004.json, ESTATE_GAP_DIG, X_INTEL_PAPERS_20261004.md,
  frontier_asks results, frontier_olm sweep, index_events.jsonl, LINKS.jsonl,
  PRIMER, the ractor_engine lens files). Zero hits in queue/, state/, memory/.
  No drop decision exists anywhere greppable under that instrument; the gap
  register row is the standing record. If the truncated finding claims EG-20
  remains unbuilt and unowned, my bytes support it.

## What the lens missed (additions banked below in the result)

1. The engine_version discriminant already exists on every banked row (my
   nested census) - the bridge gate is a read of an existing field, ~30min,
   not a 1-2h instrument build.
2. The GPS ledger already holds the poison: 248 arena verdict=0 rows banked
   (my sqlite census); the re-grade decision is a verdict_log census, and the
   append-only cure is decay (door 6), not a feed gate.
3. .github/workflows/ci.yml exists (2026-10-01) and the github remote is
   configured; both are dark (zero refs/remotes/github, main-only trigger,
   named-core list excludes arena_bench) - the lens's falsifier evidence was
   stale on both bytes.
4. The pre-push hook DOES conditionally run pytest via tools/refold_gate.py:167
   - the "ZERO pytest" universal is false; the lens's own precedent block is
   the counterexample.
5. Monitor is not re-run-idempotent (room row per run, 3 API polls, state-gated
   dedup) - door 3's residual guard has live harm to cure; the cargo branch of
   its falsifier is falsified.

## Honesty

- Finding 4's finding/falsifier/move fields were truncated in my tasking; I
  verdict only the visible evidence and the named blind-spot scope, not the
  unseen claim text.
- The 248-banked-zeros attribution to v2 rests on the door-1 receipt's
  statement that v3 has banked no rows yet (GWAP_INDEPENDENT_COP:76-78) plus
  the count shapes (248+103=351 fed vs 613 banked rows); I did not query
  verdict_log timestamps to date individual rows. OWED if contested: one
  `select min/max(created) from verdict_log where task_shape='arena-agreement-v1'`
  would settle it.
- The schtasks census covered task NAMES plus pytest-greps of scripts/*.ps1; I
  did not open every Estate*/Mag* task's action binary. Instrument named, scope
  named.
- Door-2 commit 00cb15c77 timestamp verified 2026-10-04 12:39:31 -0400; no
  newer door commit existed at my check (`git log -3`), so the lens's
  staleness warning about sibling landings had not materialized yet.

Writer: break-logic lens (ractor engine, 2026-10-04-eleven-doors)
fetched: 2026-10-04
