# NIGHT MARCH CURED - 2026-10-04 (free-lane repair, $0)

Seat: ZCode night shift, free lane. Interpreter: `.venv\Scripts\python.exe` on the
host; container python (`/usr/local/bin/python`) inside the mag-sovereign cage,
which is the interpreter the live lane daemon (pid 28, `python -m
mag.lane_runner --daemon`) already runs. No paid APIs fired; no commits made.

## 1. Real error, verbatim

Captured by hand-running the failing step in its real environment
(`docker exec mag-sovereign python /app/watch/march_228.py`, 2026-10-04T08:44Z):

```text
Traceback (most recent call last):
  File "/app/watch/march_228.py", line 24, in <module>
    for line in (ROOT / ".env").read_text(encoding="utf-8", errors="ignore").splitlines():
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/pathlib.py", line 1027, in read_text
    with self.open(mode='r', encoding=encoding, errors=errors) as f:
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/pathlib.py", line 1013, in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/app/.env'
RC=1
```

Nightly symptom (queue/lanes/night/trail.jsonl, every night since 2026-09-26
in logs/lane_scheduler.log): `night composite: monitor rc=0; march rc=1`.

## 2. Root cause

- The night lane runs inside the mag-sovereign Docker cage (docker-compose.yml
  service `mag-sovereign`; daemon confirmed as cage pid 28). Compose delivers
  `.env` via `env_file:` (environment variables only) and the volume list
  mounts queue, watch, memory, logs, state, jobs, configs, mag, dashboard,
  tools/gps_mcp, models, tests, main.py, mag_launch.py - never the `.env`
  FILE. `ls /app/.env` in the cage: `No such file or directory`.
- `watch/march_228.py` loaded its key ONLY by reading `(ROOT / ".env")` from
  disk at module level (old line 24), so in the cage it crashed before
  `__main__` - before claims, before cards, before any API call - and Python
  turned the unhandled exception into rc=1. No spend ever happened; the
  42-58 s composite duration in logs/lane_scheduler.log (research monitor
  alone measures ~40 s in the same log) confirms march died in seconds.
- The error stayed invisible for a month because `mag/lane_runner.py
  cycle_night` called `_run_script(...)` as `rc, _ =` - the captured
  stderr/stdout was discarded and only the bare rc reached the trail.
- `mag/lane_runner.py`'s own comment said "an honest rc=2 is expected until
  the operator sanctions an env door" - the code never implemented that
  expectation; a module-level crash can only ever yield rc=1.

## 3. The Errno 22 family in the same trail (state writes, second defect)

`CYCLE_FAIL EXC OSError: [Errno 22] Invalid argument:
'/app/queue/lanes/<lane>/runner_state.json'` rows (trail.jsonl; also 4,599
matching rows in logs/lane_scheduler.log, 2026-09-14 through 2026-10-04).
Mechanism: `_save_state` opened the live state file with mode 'w' (O_TRUNC)
through the Docker Desktop bind mount; host-side share-lock bursts make that
open fail intermittently. Evidence it is external and transient, not
code-side: 2026-10-04T08:38:49Z research+builder both failed, 08:40:37Z both
succeeded, and a same-mount probe (40x open-'w', read, tmp+os.replace on a
throwaway file in queue/lanes/night/) ran 40/40 clean between those moments.
Night-lane damage shape: `_save_state` sat BEFORE the CYCLE trail row inside
cycle_night, so a failed write lost the record of work that had already run
AND left `last_night` unset - the daemon then re-ran the whole composite
every ~100 s (five CYCLE_FAIL rows 2026-10-03T23:01:59Z-23:08:04Z before the
23:10:55Z success).

## 4. Cure (smallest correct; cause+evidence comments carried in-code)

1. `watch/march_228.py` - the `.env` read is guarded (`exists()`), and
   `__main__` exits rc=2 with a named `MARCH SKIP rc=2` reason when no key is
   found. Key source stays FILE-ONLY: no os.environ fallback, because the
   env door is operator-gated (lane_runner comment; recorded, never faked).
2. `mag/lane_runner.py cycle_night` - keeps march's captured output tail
   (last 180 chars) in the composite whenever rc != 0, so the next failure
   names itself in the trail instead of dying as a bare rc.
3. `mag/lane_runner.py cycle_night` - trails the CYCLE row BEFORE persisting
   `last_night`, so a failed state write can no longer hide completed work.
4. `mag/lane_runner.py _save_state` - atomic write: unique tmp dotfile in the
   lane dir, then `os.replace` over the target; never truncates the live
   file (readers see old or new inode), tmp unlinked on failure. Same
   rename-CAS pattern mag/bay_organs.py proved against win32 filter locks.
5. New tests: `tests/test_night_march_cure_20261004.py` (sandbox cage-shape
   runs, honest rc=2, no-key file, host-shape import, atomic state round-trip,
   trail-before-state ordering under a forced OSError 22, green persistence).

## 5. Proof

- Cage march standalone, post-cure: `MARCH SKIP rc=2: no key - /app/.env
  absent or carries no ZAI_API_KEY_Pro/ZAI_API_KEY (cage: .env unmounted by
  compose; no env door sanctioned)` -> `RC=2`. No traceback, no API call.
- Full lane, hand-run once in the cage (2026-10-04T08:50:01Z trail row):
  `night composite: monitor rc=0; march rc=2 :: MARCH SKIP rc=2: ...`;
  runner exit 0; queue/lanes/night/runner_state.json now carries
  `last_night: 2026-10-04`, `last_result` holding the named reason; no tmp
  dotfiles left in the lane dir. This is the honest-result green: the march
  step reports exactly what it is instead of an opaque crash.
- Tests (instrument `.venv/Scripts/python.exe -m pytest -q -p
  no:cacheprovider` over tests/test_night_march_cure_20261004.py +
  tests/test_lane_runner_cluster.py + tests/test_monitor_lane_rotation.py,
  moment 2026-10-04T08:47Z): 39 passed, 0 failed.
- Host import check (same venv): march_228 module loads with KEY present
  (host `.env` exists; behavior unchanged where the file exists) and
  `_save_state` source contains the os.replace path.
- The host-side full `--lane night --once` run was NOT fired on purpose: the
  host `.env` carries ZAI_API_KEY_Pro and memory/percolator/explore.jsonl
  holds 836 open signals (Counter over the file, 2026-10-04), so a host run
  would fire real glm-5.3-flash API calls - banned on this free-lane repair.
  The cage is the lane's real execution home, so the proof ran there.

## 6. Residuals and operator levers (no action taken, by design)

- march in-cage stays rc=2 (honest skip) until the operator sanctions an env
  door (os.environ fallback) or mounts `.env` read-only into the cage. That
  decision is the operator's; this repair records, it does not fake.
- Because the proof run set `last_night: 2026-10-04`, tonight's 23:00 UTC
  daemon cycle will answer `already-ran` - the once-per-night semantics
  doing their job after a real run.
- The Errno 22 bursts also hit research/builder/day_work state writes; the
  atomic `_save_state` removes the truncation/lost-record class for every
  lane, but the external lock source lives on the Windows host side of the
  Docker Desktop file share and is not repo-curable from this seat.
