---
name: openclaw-retired-20260919
description: Operator retired openclaw ("we don't even use openclaw"); the Sep-3
  engine bay, openclaw seat, and mag-openclaw container are dead machinery,
  parked 09-19
metadata:
  node_type: memory
  type: feedback
  originSessionId: sess_833dd189-7e2d-4705-b3dd-059d5e40c78d
---

Operator correction 2026-09-19: "we don't even use openclaw." The Sep-3 engine
bay (`watch/engine_spec.json`, engines A/B/E/Z mining the hermes client via the
openclaw seat and the mag-openclaw container) predates the ZCode migration and
the container no longer exists.

**Why:** the bay's queues were fossils mining a retired client; any re-arm would
dispatch into a dead seat, and openclaw dispatches surface as chat-app messages
(the old flood vector).

**How to apply:** engine_spec.json now carries all replicas 0 with a PARKED
note; do not re-arm those engines against the old queues. Treat openclaw/
opencode seats in `mag/seat_dispatch.py` as vestigial until a replacement
gateway is deliberately built. See [[migration-import-ghosts-20260919]].
