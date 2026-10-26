# ROOM STATE DOOR SPEC: the fleet lightmap promised a nightly run, none exists (locksmith, 2026-10-12)

Status: SPEC ONLY, awaiting operator mount decision. Nothing here runs on a
cadence until the operator mounts it. This file is the law-13 design-cite pass
for that mount. Companion to watch/inbox/CADENCE_DOOR_SPEC_20261010_locksmith.md
(the five meters organs; still unmounted as of this cycle, 26 Mag tasks checked).
Author seat: THE LOCKSMITH, mission_20261012_02 (receipt:
watch/inbox/mates_leave_protocol/receipts/receipt_20261012_locksmith.md).

## The door (all verified this cycle, bytes not vibes)

| Fact | Verified state this cycle |
|---|---|
| The promise | mag/room_state.py:19-20: "Night shift runs: python mag/room_state.py [--window 200]" |
| The promise's true age | dashboard/static/room_state.json carried generated=2026-09-06T04:10:08Z (file mtime 09-06 00:10, size 6,921 bytes): the seed's "stale 2026-09-27 picture" claim was itself stale; the real picture was 36 days old |
| The consumer | dashboard/static/salon_lightmap.html fetches room_state.json with cache no-store (line 366) and falls back to an inline seed wall set with a "freshness layer offline" banner (lines 393-394) when the file is missing, so staleness renders silently as truth |
| Callers | zero: no Mag scheduled task action names room_state (26 tasks dumped today), no scripts/*.ps1 mentions it (grep zero), no mag/server/tools module imports or shells it |
| The hand run (this cycle) | .venv\Scripts\python.exe mag\room_state.py --window 200: exit 0, "10 organ walls, 5 lit, 10 invariant candidates (window=200), economy: 5 JOINED, 4 ghost, 1 prune, tip=ae71aee2558f@3414"; generated=2026-10-12T12:30:40Z; the 09-06 state is now room_state.prev.json, so the cross-version invariant diff spans a real 36-day gap (all 10 walls kept label+position: 10 invariant candidates, the persistence law finally has evidence) |
| The honest prune | the fresh render puts the board wall (room.html, board.js, live.html tokens) in PRUNE: 0 fires in 72h+, last fire 2026-10-05. First real prune candidate the lightmap ever reported |

## Proposed mount (operator decision)

One line appended to an existing daily task script (candidate hosts:
scripts/estate_smith_daily.ps1 or scripts/improve_daily.ps1), or a new task
registered via the scripts/register_fts_index_task.ps1 pattern, headless via
scripts/run_hidden.vbs (wscript //B //Nologo):

```
.venv\Scripts\python.exe mag\room_state.py --window 200
```

Cost and blast radius, measured this cycle: $0, stdlib only, no daemon, no API
calls; reads memory/trajectory/steps.jsonl (81,246,148 bytes at run time) and
writes exactly two repo files (dashboard/static/room_state.json and
room_state.prev.json). RAM gate satisfied at run: 22.6 GB free, run completed
in seconds.

## Law-13 design-cite rows (corrections-design-cite)

- docker-not-desktop: CITED-WITH-EXEMPTION. The mount joins the estate's
  existing host-process daily-task fleet (26 Mag tasks, all host-process);
  containerizing a stdlib renderer that must read the repo's own trajectory
  tape in place is a different design and out of scope. No new runtime class.
- headless-only (also law 48): CITED-AND-COMPLIANT. The proposed line rides
  the existing run_hidden.vbs pattern, same as MagFtsIndexDaily and
  MagCensusPatrolDaily. No new window class.
- one-supervisor (also law 11): CITED-AND-COMPLIANT. No second supervisor: one
  line behind one existing daily script and its one existing scheduled task.
- Senses topology (watch/SELF_STEAL_MCP_TOPOLOGY_20260904.md): CITED-AND-
  COMPLIANT. room_state.py is a renderer/writer, not a sense; no MCP surface.
- Egress: none. The organ reads two local files and writes two local files.

Uncited host-spawning designs get DISPUTED and culled at census (LAW-056 gate).
This spec is the citation; the operator's mount decision completes it.

## Side finds, dated, so nobody re-hunts them

- dashboard-deploy/ is the soul_frontier Vercel project (vercel.json builds and
  routes ONLY static/games/soul_frontier/soul_frontier.html). Its static/ dir is
  a frozen 09-24 06:41 snapshot: 236 files, 44 .bak ghosts since purged from
  dashboard/static, 9 newer main files never mirrored, and an inert
  room_state.json from 09-24. The live deploy answers HTTP 200 today (root and
  the v1.2.0 URL). The game source itself (09-24 06:32) matches the deploy era.
  Verdict: do not "fix" the mirror, it is not served; the only live surface for
  the lightmap is the local dashboard/static dir.
- The five meters organs of CADENCE_DOOR_SPEC_20261010_locksmith.md remain
  unmounted: zero of 26 task actions and zero scripts/*.ps1 lines name any of
  them. logs/kpi.jsonl measured 26,109,499 bytes this cycle (receipt
  receipt_20261012_locksmith.md, COUNTS) against 17,688,381 bytes on 10-09
  (receipt_20261010_locksmith.md, COUNTS): about 8.4 MB in 2.5 days, the
  ~100 MB/month line confirmed; watch/inbox/MEMORY_GAUGE.jsonl is frozen at
  5 rows (row count read this cycle).
