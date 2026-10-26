---
name: flash-lane-burn-session-20260927
description: 9/26-27 flash-lane burn session — 397 briefs through 12-lane swarm
  + dispatcher + free-lane runner, ~1.2B witnessed tokens, width-24 proven
  dynamic, all 397 landed
metadata:
  node_type: memory
  type: project
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

Flash-lane burn session 2026-09-26/27 complete. 397 briefs dispensed through a 12-lane swarm + rolling dispatcher + free-lane runner, all landed with receipts. ~1.2B witnessed agent tokens. 1302/429 experiment data at width 24. Every receipt has a 5-section file. Queue self-fed from ~40 seeds to 500+ briefs. The burn ran from ~07:00 Sep 26 to past midnight into Sep 27.

**Architecture that worked:** rolling dispatcher (every 10 min, refill to cap), 12-lane swarm (each lane owning a serial slice of 25 briefs), free-lane runner burning estate work through 8 alive external lanes in tandem. Width 10→12→24 escalated on operator GO with the envelope law re-derived as a function of window depth, not a constant.

**Key discoveries preserved elsewhere:**
- 287 absorbed 1302s invisible to surfaced counts (B2-98) → [[provider-error-silent-absorption]]
- Fold silently dropped watch/ paths, test census hand-copied (B2-02/B2-69) → [[flash-burn-structural-findings-20260927]]
- Envelope ceiling dynamic, 287 absorbed 1302s (B2-25/B2-98) → [[width24-experiment-verdict-20260926]]
- 3 fabricated research answers caught (B2-16) → [[flash-burn-structural-findings-20260927]]
- Free-lane provider roster: groq 1K req/min alive, cerebras 402 dead, nvidia 410 purged, gemini 401, mistral zero-quota (B2-04) → saved in provider health receipt

**Laws and gates built during the burn:**
- LAW-13 experiment-on-absence registered
- LAW-12 registered with scenario suite at pre-push (ENFORCING)
- B2-164 scenario suite gate wired into pre-push (ENFORCING, not WARN)
- B2-164 G1 citation tripwire fired: first genuine fleet G1 FAIL caught
- Dormant gate (mag/dormant.py) wired into 7 consumers
- Provider error tally tool (B2-98)
- B2-491 pointer-anchor law (byte anchors on file:line pointers)
- B2-338 census patrol case fix
- B2-343 restore guard (stale-base whole-file restore detection)

**Swarm completion stats (witnessed tokens per lane):** SW-00 95.1M, SW-01 81.9M, SW-02 116.0M, SW-03 69.0M, SW-05 80.1M, SW-06 0 (1302 death), SW-07 70.0M, SW-08 93.6M, SW-10 86.2M, SW-11 76.1M. Plus dispatcher-fired waves B2-01 through B2-98 and B2-100 through B2-553.

**Final counts (session close):** 506 briefs dispensed, 402 landed with receipts, 104 requeued or in flight. ~1.1B witnessed tokens across all surfaces. 240+ LEDGER rows. 550+ queue rows created by self-feeding lanes. Peak: 109.4M tok/h at width 10.

**Deep-lane tail pattern:** the last ~23 briefs are the deep, slow work (30-90 min each) while the fast lanes completed in the first 8 hours. The queue composition shifted from fast shallow work to deep slow work as the burn progressed, which is the correct direction: shallow first clears the decks, deep last does the thinking.

**Guard-pin maintenance law (B2-259, new generalizable pattern):** when a verifier's pinned constants (check7 GUARD_PINNED_ABSENT/CLAIMS) fail because a sibling lane legitimately moved the underlying rows, the landing lane must re-audit every differing row against source bytes and re-derive the pin constants from that audit named in its receipt. Never delete or weaken pins to get green. The pins are the audit's fingerprint; deleting them erases the evidence that the audit happened.

**Self-caught fabrication pattern (B2-342):** the schema registry lane caught a fabricated placeholder hash in its own first LEDGER draft draft and replaced it with the computed value before landing. The laws bite their own lanes: the same no-fabrication law that catches estate-wide fabrication also catches the seat's own shortcuts.

**Session stats through final update:** 425 dispensed, 401 landed with receipts, 24 in flight or requeued. ~1.2B witnessed tokens across all surfaces. 550+ queue rows created by self-feeding lanes. Peak: 109.4M tok/h at width 10, width-24 experiment confirmed the dynamic ceiling.
