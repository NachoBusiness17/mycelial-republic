# INTAKE — avrldotdev GPU inference scheduler question — 2026-09-04

SCORE — FIT:3 PULL:3 COST:5 WINDOW:2 NOVELTY:3 = **16/25 — BUILD, WINDOWED**

RECEIPT (what the tweet actually says): @avrldotdev (backend dev, 9.4k followers),
2026-09-04, 700 likes / 1,095 bookmarks. Image-text: "Design a GPU Inference
Scheduler" — 8 GPUs total; small requests take exactly 1 GPU, large requests must
acquire ALL 8 simultaneously and share none; both streams arrive continuously; design
must prevent large requests starving under a constant stream of small jobs while
balancing small throughput vs large latency. Classic all-or-nothing gang scheduling /
resource-convoy problem.

AXES
- FIT 3 — pure composition: queue, rooms, chain are gang-scheduling primitives already; no new vendor. Not a 5 because no existing organ does all-or-nothing GPU gangs.
- PULL 3 — Rocinante (Oct 27) is exactly a constrained-GPU substrate; the starvation law is the same problem as our lane saturation (z_ai2 24/7, quota pools). Not on this week's critical path.
- COST 5 — free-lane draft (rib_chat / 4.7-flash) + one judgment pass; zero operator minutes.
- WINDOW 2 — nothing starved tonight needs it; real gate is Rocinante hardware arriving.
- NOVELTY 3 — textbook problem (convoy/gang scheduling), but first time the fleet has it framed as a falsifiable scheduler spec against OUR substrate.

ROUTING — BUILD (windowed; lane = Rocinante prep, gate = Oct 27 hardware on the desk — the card names the gate, per LAUNCH LAW this is a gate-deferral not a window-deferral) / CALIBRATE (measure: simulate the scheduler on free lanes against synthetic arrivals before believing any fairness claim) / REMEMBER (the starvation law: all-or-nothing acquirers need reservation, not politeness — same law as our quota pool design).

TRI-STATE
- "Design a GPU inference scheduler with these constraints" — **Supported** (image transcribed via vision, exact constraints read).
- "Anthropic's most frequently asked system design interview question to date" — **Unproven** (author assertion, no Anthropic source; do not propagate as fact).
- "Reservation-based scheduling prevents large-request starvation" — **Supported** (standard result in gang scheduling literature), pending our own falsifier sim.
