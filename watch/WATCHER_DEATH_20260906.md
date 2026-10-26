# WATCHER_DEATH_20260906 — the frozen heartbeat (BATCH5 wave 3, worker s4)

Written 2026-09-06Z by s4-watcher. Read-only forensics; no process started.
Evidence: host tasklist, docker ps -a, docker logs mag-sovereign, schtasks query,
repo grep. Tri-state labels on every claim.

## ITEM 1 — Who died. [SUPPORTED]

- Writer of `watch/heartbeat.json` + `watch/mag.pid` = **`mag/runtime.py`
  (`write_heartbeat`, ROOT/watch/heartbeat.json, ROOT/watch/mag.pid,
  runtime.py:18-37)**. The `watch_interval: 5.0, status: starting` shape is the
  startup write at runtime.py:129; `status` never updates afterward — "starting"
  in a frozen heartbeat is a stale label, NOT proof it died at startup.
- The process = the **integral Mag lab** (main.py lab → `run_integral`): ONE
  process owning watch-loop + Mag daemon + heartbeat (runtime.py docstring;
  mag_launch.py:243-247 slot "lab"). Last beat **2026-09-05T22:51:49Z, pid 9608**.
- **NOT the sanctioned watchdog.** `mag-docker-watchdog` scheduled task runs
  `watch/docker_watchdog.vbs` and watches Docker Desktop only. Docker never died
  (all containers "Up 22 hours"); the watchdog had nothing to flag.
- pid 9608 is absent from the host tasklist; only python.exe 13976/28164 remain
  (other organs). The lab ran on the HOST, outside any supervisor.

## ITEM 2 — Cause of death. Cause: [UNPROVEN]. Scope: [SUPPORTED].

Proven negatives:
- Host did NOT reboot or sleep through the window: mag-sovereign logged
  continuously 22:08:34Z → 23:10:24Z → 00:09:05Z → 01:08:21Z (hourly drainer
  respawns, all rc=0). Container uptime 22h.
- NOT a container death: no respawn line for lab/backend/dashboard around 22:51Z
  in `docker logs mag-sovereign`.
- NOT the watchdog's beat: Docker stayed up (watchdog watches Docker only).

Unproven: WHY host pid 9608 exited. No crash log found for the host lab; the
host has had no supervisor since the respawn law retired mag_launch/
process_supervisor, so nothing logged its death. Correlation only: the operator's
ZCode session fired its `stop` hook at 22:53Z (watch/active_session.json) — two
minutes after the last beat — suggesting operator-adjacent activity (console
close / manual quit). Marking cause **Unproven**; the *conditions* (unsupervised
host process, no auto-rearm) are Supported.

Separate casualty, in passing: `mag-ollama` Exited(255) ~26h ago — distinct from
this death, uninvestigated here.

BONUS FINDING [SUPPORTED] — the in-cage lab slot is WEDGED by mis-adoption:
container entrypoint (scripts/container/entrypoint.sh) execs mag_launch.py; at
container start 2026-09-05T03:35:20Z the supervisor logged `spawned ghost
pid=12` then `adopt lab (pid=12 still alive)` — it adopted the GHOST's pid as
the lab (mag_launch.py:342-360 `_AdoptedProc`/adopt-not-duplicate reads stale
pids from state/mag_launch.json, which is host-mounted). While ghost (pid 12)
lives, `poll()` returns None, so the supervisor will never respawn lab. That is
why the cage never took over the heartbeat when the host lab died.

## ITEM 3 — What was lost. [SUPPORTED]

Duties of the dead integral (heartbeat fields + runtime/daemon code):
- `watch/heartbeat.json` + `watch/mag.pid` liveness beacon — **ORPHANED**
  (nothing beats into it; frozen at 22:51:49Z).
- The [mag]/[assign] todo auto-assign watch loop (mag/daemon.py mag_loop,
  mag_interval 120s; last_action "assigned") — **ORPHANED** (no integral
  anywhere; the in-cage lab is wedged per ITEM 2).
- NOT lost / not its duty: `watch/active_session.json` is written by ZCode hooks
  (watch/session_end_hook.py, grok_hook.py) — event-driven, writers alive, stale
  only because no session is running. `watch/monitor_lane.state` stays fresh —
  covered by the in-cage lane_scheduler (in the mag_launch roster per
  RUNNING.md; the hand-run one-liner is SUPERSEDED). Dashboard, backend, scribe,
  ghost, drainer(autorun), api_gateway all in-cage and up.

## ITEM 4 — Re-arm. [SUPPORTED, law-cited]

- **ILLEGAL now**: host `python main.py boot --ensure` / `boot_mag.cmd` — spawns
  a second host supervisor (respawn law violation; AGENTS.md 2026-08-26).
- **Sanctioned one-liner** (cage governor re-runs the roster; stale adopted pid
  is dead after restart → dropped → fresh in-cage lab spawn; also the documented
  CAGE_RESTORE in mag/health.py):
  ```
  docker compose restart mag
  ```
- **OPERATOR HANDS recommended**: not a spend/keys gate, but it blips the live
  dashboard + gateway (:8001 MCP) for the fleet; and if the restart is done as a
  *recreate*, O4 applies (lane daemon now roster-owned, so recreates respawn it
  — RUNNING.md 2026-09-05 note). Watch the first log lines after restart for
  `spawned lab pid=…` (not `adopt lab`) to confirm the wedge cleared.
- Laws touched (law 13 cite-at-design): respawn law (container governor +
  restart policies + mag-docker-watchdog are the only supervisors); O4
  (container recreates kill roster daemons — since fixed by roster ownership);
  one-sense-one-instance (gateway blip); SACRED COWS (the host lab was a
  pre-cage residual, retired with honor — its duties move INTO the cage, not
  back onto the host).

## Receipt

BATCH5|s4|RECEIPT: dead watcher=<integral Mag lab, host pid 9608, writer mag/runtime.py>,
cause=<Unproven exit of unsupervised host process at 22:51:49Z; host+cage stayed up;
in-cage lab slot wedged by pid-12 ghost mis-adoption>, orphaned duties=[heartbeat/pid
beacon, [mag]/[assign] todo auto-assign loop], re-arm=<docker compose restart mag —
OPERATOR HANDS recommended>.
