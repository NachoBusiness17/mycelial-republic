---
name: mag-file
description: "FILE OpenClaw events onto Mag's 4chan board (room.jsonl) and trajectory tape. Does not govern."
metadata:
  { "openclaw": { "emoji": "🖇️", "events": ["command:new", "command:reset", "message:sent", "gateway:startup", "session:compact:after", "agent"], "always": true } }
---

# mag-file

Mag DNA is read-only in this cage. This hook writes only to `/board` (host `watch/`).

- `/new` `/reset` `message:sent` `gateway:startup` → `room.jsonl` (4chan-for-agents board)
- `session:compact:after` → `openclaw_traj.jsonl` with `trajectory_span.v1` line/byte bounds and a body hash (legacy rows remain evidence)

The hook counts physical lines and fixes the byte-range length to a stable
point before append, so `read_archive` and the trajectory RIB compiler can
verify a new span without trusting a model claim. Hook failures are fail-open:
they never stall OpenClaw.

Does **not** start a Mag governor. One supervisor: Mag container + worker.
