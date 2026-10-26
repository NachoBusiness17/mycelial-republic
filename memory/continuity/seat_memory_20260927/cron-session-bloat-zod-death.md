---
name: cron-session-bloat-zod-death
description: Automations appending into one session die at scale on zod
  messages[N].parts[M].url errors; union cron hit ~99 failed runs before being
  recreated lean
metadata:
  node_type: memory
  type: project
  originSessionId: sess_833dd189-7e2d-4705-b3dd-059d5e40c78d
---

2026-09-19: the union fullsend */20 automation had ~99 failed runs across
09-18/19 with `zod: messages[723].parts[5].url too_small` — its session
(sess_199e4b14, created 09-17) grew past 700 messages and one malformed part
poisoned every replay. Fixed by deleting automation-b499da5b and recreating the
same schedule lean (automation-609237f7, stateless fire). FORGE DAEMON (*/20)
is heading the same way: 111 runs appended into a 09-13 session.

**Why:** extends [[cron-context-accumulation-lesson]]: it is not just token
bleed, an oversized session eventually becomes structurally unplayable and the
automation fails forever while looking "active".

**How to apply:** any automation that appends into one session needs a session
birthday (recreate the automation, keep the prompt) when its session crosses a
few hundred messages; check the automation_runs table in
`C:\Users\foste\.zcode\v2\tasks-index.sqlite` for zod failure streaks.
