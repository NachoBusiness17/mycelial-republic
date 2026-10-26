---
name: lite-free-window-schedule
description: glm-5.3-flash is FREE from 11:00 (local) on the Lite seat — the
  daily free window; drivers and seats must know this schedule without being
  reminded
metadata:
  node_type: memory
  type: project
  originSessionId: sess_199e4b14-3a8b-46e9-ba5e-57c166fc2967
---

**glm-5.3-flash is free from 11:00 (operator local time) every day** on the Lite seat
(ZAI_API_KEY_Lite, /api/coding/paas/v4). The operator stated it 2026-09-17 ("we have 10k
credits and a parallel line to 5.3 flash... it's also free at 11 so we could be driving 2
windows like this") and had to repeat it angrily the same night because no seat remembered.

**Why:** the burn plan depends on it — after 11:00 the Lite lane is a FREE primary, not a
paced fallback; before 11:00 it rides law-15 pacing only.

**How to apply:** (1) drivers prefer glm-5.3-flash as a scheduled primary after 11:00 and
log the window in every run summary; (2) the fleet imprint carries this schedule in its
SCHEDULE section so every cold-loaded seat knows it; (3) when the operator mentions a free
window, it goes into durable memory + the imprint IMMEDIATELY, not just the session.
Related: [[lite-key-seat-glm53flash]], [[no-overnight-deferral]].

**Encoded in four places same night (after the operator had to repeat it furiously — "why
do you think i made a seat that remembers and you load it cold"):** (1) this file;
(2) MEMORY.md index row; (3) the imprint's STANDING SCHEDULE section (every cold-loaded
seat boots knowing it); (4) build_lane_game.py time-aware MODEL LAW — after 11:00 local,
union-alpha and glm-5.3-flash rotate as SCHEDULED CO-PRIMALS (both free windows burn
together), before 11:00 Lite stays law-15 paced. Also standing: any operator-stated
window/cadence enters all stores in the SAME session, verified by a regen.
