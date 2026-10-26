---
name: fleet-heartbeat-20260919-evening
description: Live machine state evening 9/19 after operator asked "does this
  thing work" — dashboard 200 in 8ms, lanes heartbeating, ghost cycling, but
  governor autorun_loop CRASH-LOOPING (4 crashes 17:31Z) = the one live fire;
  autopsy offered
metadata:
  node_type: memory
  type: project
  originSessionId: sess_7d43e03e-6607-4289-a7c7-e1b173bd9cb7
---

2026-09-19 evening, operator asked "How does this fucking thing work? Does it lmao" right after the full-tree map landed. Answered from live probes, not recital: dashboard :8765 HTTP 200 in 8ms; lane runners fresh same day (research 15:13, builder + day_work 14:57 local); day_work trail heartbeat "scheduler alive, all lanes stateful" at 19:08Z; training events.jsonl last row autorun_cycle at 19:14Z (T2); ghost daemon running (PID 27908, 120s cycle); watch/inbox index registered the THE 50 fold verification receipt with sha256 (44/44 artifacts on disk).

**The one live fire: `mag.governor_autorun` autorun_loop(5.0) is crash-looping** — 4 crashes 17:31:17-17:31:18Z in memory/supervisor/state.json (PID 37172, retry scheduled), likely why the plan drainer feels dead; autopsy offered to operator, not yet run. Secondary: the ghost-daemon variant (`-m mag.ghost --daemon --port 9000`) crashed twice at 12:02Z while the plain `from mag.ghost import cycle` daemon runs fine. Also cited as known-not-working: 34 failed tests in the 2026-09-14 census and the honesty-layer pattern (elder trail filing 429 days as healthy, 79% debris unmapped until tonight). Machine verdict delivered: the loop turns and files its own paperwork; its weakest organ is self-report truth, hence "trust bytes, not reports."

Structure explained to operator in one breath (surfaces → lanes → switchboard → memory organs → governance); no new architecture facts, this memory is the heartbeat snapshot + the autorun debt. See also [[two-machine-drive-bridge-20260919]], [[host-supervisor-docker-only-split-20260919]].
