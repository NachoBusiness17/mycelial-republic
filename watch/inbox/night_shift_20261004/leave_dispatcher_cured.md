# leave_dispatcher cured - MagLeaveProtocolDaily exit-1-every-day (night shift 2026-10-04)

Seat: night shift, free lane ($0), venv python only. Task: the scheduled task
MagLeaveProtocolDaily (08:00 daily, registered by scripts/register_leave_task.ps1)
exited 1 every day. Invocation (the /TR, two bare absolute tokens, no quotes):

    C:\Users\foste\Documents\projects\local_sovereign_agent\.venv\Scripts\python.exe C:\Users\foste\Documents\projects\local_sovereign_agent\tools\leave_dispatcher.py

## THE REAL ERROR (verbatim, from logs/mates/runs/ and logs/mates/dispatcher_*.log)

Kill mode 1 - the model wall (any runner that got past storage):

    Error: Your current subscription plan does not yet include access to GLM-5V-Turbo

Kill mode 2 - the storage lock (the rest of the runners, seconds after dispatch):

    Error: Unexpected error
    System.Management.Automation.RemoteException
    database is locked

Secondary - the shared log collision (did not set exit codes, but destroyed the
operator trail the register script points at):

    Add-Content : The process cannot access the file
    'C:\Users\foste\Documents\projects\local_sovereign_agent\logs\mates\runner_20261003.log'
    because it is being used by another process.
    Add-Content : Stream was not readable.

Historical (already cured 2026-09-30 by the AUTH FIX comment in run_mate.ps1,
listed for the arc): on 09-30 all 8 also showed

    Error: Authentication parameter not received in Header, unable to authenticate

## ROOT CAUSE

The dispatcher itself is healthy: its exit contract (tools/leave_dispatcher.py
main: return 1 if any runner nonzero else 0; exit 2 only on the argv guard)
was firing honestly. The disease was one level down, in scripts/run_mate.ps1,
with two independent kill modes splitting the 8 mates between them every day:

1. MODEL WALL. The runner invoked `opencode run $Prompt` with no model flag.
   With no default model set anywhere, opencode resolved its built-in default
   to zai/glm-5v-turbo. The z.ai coding plan does not include that model - the
   plan's models are glm-4.7 and glm-5.3 (they are the only models named in
   the opencode provider config). So every run that authenticated died on the
   subscription wall. Evidence: run_20260930_01..08 (all 8), run_20261002
   (7 of 8: 01, 02, 03, 04, 06, 07, 08), run_20261003_05_jester; the run log
   banner read `> build - glm-5v-turbo` (arrow glyph in the raw log).

2. DB LOCK. All concurrent runners (width 8) open the ONE shared opencode
   SQLite store at ~/.local/share/opencode/opencode.db - 321,089,536 bytes
   with a ~20MB WAL on this box - and the slow openers die SQLITE_BUSY two
   seconds into dispatch. Evidence: run_20261003 (7 of 8: 01, 02, 03, 04, 06,
   07, 08, all timestamped 08:00:03), run_20261002_05_jester; the shared
   db-wal mtime matches each 08:00 fire window.

Net effect across 09-30, 10-02, 10-03: 24/24 runner invocations nonzero,
DISPATCH COMPLETE: 8 invocations, 8 nonzero exits [1, 1, 1, 1, 1, 1, 1, 1]
every day, and watch/inbox/mates_leave_protocol/receipts/ is EMPTY - not one
mate receipt has ever been filed. (No dispatcher log exists for 10-01: no
fire recorded that day.)

## THE CURE (scripts/run_mate.ps1, three edits, each comment carries
cause+evidence per build discipline)

1. MODEL PIN (literal, argv law intact - no new variable enters any argv):
       & $OpenCode run -m zai/glm-4.7 $Prompt 2>&1 | ForEach-Object {
   zai/glm-4.7 is the workhorse coding-plan model; a frontier swap is a
   one-literal edit to zai/glm-5.3. Both verified present in
   `opencode models zai` output.

2. STORAGE ISOLATION: after the mission claim, the runner sets
       $env:XDG_DATA_HOME = logs\mates\ocdata\<mission basename>
   so each claimed run gets its own opencode data dir and its own tiny
   opencode.db - zero contention with sibling mates and with every other
   opencode process on the box. Verified before landing: opencode honors
   XDG_DATA_HOME even on Windows (a models call with XDG_DATA_HOME overridden
   created a fresh isolated opencode.db and never touched the shared one).
   Auth is unaffected: provider keys ride {env:ZAI_API_KEY} refs in the
   opencode config, not the data-dir store. One dir per claim, and a claim is
   held by exactly one process, so the dir is single-writer by construction.

3. LOG MUTEX: Write-MateLog appends to runner_<date>.log under a named mutex
   (MagLeaveRunnerLog, session-local - all siblings share one dispatcher
   parent). AbandonedMutexException is caught-and-proceed (the mutex is
   acquired even when the previous holder died).

## PROOF RUNS (venv python, repo root, exactly as the task fires it)

Proof A - live dispatch, post-fix (2026-10-04 04:38:21 local; the clock had
rolled past midnight so fresh unclaimed 20261004 missions were written, claimed
and actually run):

    [2026-10-04 04:38:21] live dispatch: 8 invocations, width 8 (law cap 16)
    [2026-10-04 04:38:22] START mate=lamplighter mission=...\mission_20261004_06_lamplighter.md
        opencode=...data=C:\...\logs\mates\ocdata\mission_20261004_06_lamplighter pid=23600
    > build - glm-4.7
    Error: Weekly/Monthly Limit Exhausted. Your limit will reset at 2026-10-06 10:19:22
    [2026-10-04 04:43:48] DISPATCH COMPLETE: 8 invocations, 8 nonzero exits [1, 1, 1, 1, 1, 1, 1, 1]
    DISPATCHER EXIT CODE: 1

Both cures demonstrably took: every banner read `> build - glm-4.7` (was
glm-5v-turbo), every START line carried its own ocdata dir, and across 8
concurrent runners there were ZERO "database is locked" and ZERO subscription-
access errors. The only remaining failure is a new, different, honest one -
the coding plan's weekly/monthly quota is exhausted until the printed reset.
That is spend-domain truth surfacing through a correctly-working exit code,
not a harness defect. $0 spent: every API call was quota-rejected before any
token burn; no paid APIs were used.

Proof B - no-op re-run, 04:45:37 local (all 20261004 missions now claimed):

    [2026-10-04 04:45:39] no unclaimed mission for 20261004 (...) - honest no-op, exit 0
    (x8, one per runner)
    [2026-10-04 04:45:39] DISPATCH COMPLETE: 8 invocations, 0 nonzero exits []
    DISPATCHER EXIT CODE: 0

Proof C - log integrity restored: runner_20261004.log holds all 24 expected
lines (8 env-loaded + 8 START + 8 END) with zero Add-Content errors; the
pre-fix runner_20261003.log had kept only 2 lines.

Proof D - isolation on disk: each of the 8 logs/mates/ocdata/
mission_20261004_*/opencode/ dirs holds its own fresh store (e.g. a 4,096-byte
opencode.db + WAL in mission_20261004_02_locksmith/opencode/), and the shared
321MB ~/.local/share/opencode/opencode.db was not touched by the dispatch
(its mtime 04:32 predates the 04:38 run).

## TESTS

tests/test_leave_dispatcher_exit_contract.py (new, house style: module import,
tmp trees, no live opencode): 5 passed in 0.78s
(.venv\Scripts\python.exe -m pytest -q tests/test_leave_dispatcher_exit_contract.py).
Bands: source guards pinning the -m literal, the XDG_DATA_HOME isolation, and
the log mutex (regression to either kill mode fails the suite); behavior bands
pinning the exit contract (clean day 0, any-nonzero-runner day 1, dry mode
idempotent 0).

## OPEN THREADS (operator calls, not silently taken)

- Quota: the plan resets 2026-10-06 10:19:22 (API's own words). The 10-06
  08:00 fire still precedes that reset; the first unambiguously-clean live
  mate chance is the 10-07 08:00 fire. The 10-04 08:00 and 10-05 08:00 fires
  will find all missions claimed (Proof A consumed the 20261004 claims with
  verdicts recorded in the .claim sidecars) and no-op exit 0.
- The dispatcher's exit 1 on a quota-exhausted day is honest per the register
  script's own operator-response contract; do not mute it.
- steer_read WARN "malformed row line 7: missing/empty required field(s):
  mate, steer" fires 8x per dispatch: watch/inbox/STEER.md line 7 is a known
  malformed row already superseded by line 8 (st_20260930_ladder_1, which
  says so itself); left in place per the append-only law. Noise, not a defect.
- The 321MB shared opencode.db belongs to every other opencode surface on the
  box; it was not touched by this repair.

Not committed (per task order). Files touched: scripts/run_mate.ps1 (3 edits),
tests/test_leave_dispatcher_exit_contract.py (new), this receipt.
