---
name: host-supervisor-docker-only-split-20260919
description: Host process_supervisor must not spawn ghost (Docker-only law owns
  it); blind reaper (79,864 powershell errors) caused duplicate daemons, both
  fixed 09-19
metadata:
  node_type: memory
  type: project
  originSessionId: sess_833dd189-7e2d-4705-b3dd-059d5e40c78d
---

2026-09-19 cleanup: the host supervisor's ghost-daemon loop (default True)
spawned `-m mag.ghost --daemon` on the host, ghost.py's Docker-only law blocked
it instantly, and the supervisor auto-restarted it forever (crash loop, 2
respawns in 8s). The reaper that should have noticed existing daemons was blind:
79,864 `reaper-enumerate-error` rows because bare `powershell` was not on PATH
in its launch context. Result: duplicate ghost cycle loops on the host.

**Why:** double-supervision across the host/container boundary is the L8
incident family; a blind reaper turns every ambiguous liveness check into a
duplicate spawn.

**How to apply:** ghost runtime belongs to the container while
state/DOCKER_ONLY exists; host supervisor ghost-daemon default is now False in
`mag/process_supervisor.py` LOOP_DEFS. `mag/process_reaper.py` resolves
powershell via shutil.which with a System32 fallback and logs honestly when it
cannot enumerate. If a daemon shows up twice, check the reaper's error log
first. See [[migration-import-ghosts-20260919]].
