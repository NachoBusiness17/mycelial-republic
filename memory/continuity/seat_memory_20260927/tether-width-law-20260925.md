---
name: tether-width-law-20260925
description: Workflow crashes on tethered phone were z.ai 1302 rate-limit storm
  from 50-wide dig + carrier NAT killing streams; cap fan-out at max_concurrency
  3 on the coding-plan account
metadata:
  node_type: memory
  type: feedback
  originSessionId: sess_4ea922bc-da4d-447c-b2f9-93c5e240de7a
---

Operator reported sessions crashing with "session timeout" and "subscription error" ever since the Tree Doctrine 50-wide workflow started, from his tethered phone (2026-09-25). Byte-level cause: z.ai returned `429 code 1302 Rate limit reached` 1,838 times (workflow children get ZERO adapter retries, main sessions get 11), and carrier NAT killed idle SSE streams at 71-80s (393 network failures, spikes exactly after the 18:59Z dispatch). No 1309 expired-plan error ever fired: the "subscription error" is the 1302 family rendered by the client.

**Why:** The individual coding plan is rated for roughly one project at a time (z.ai docs, higher concurrency off-peak dynamically). A 50-wide fan-out contests the account with the operator's own foreground session and saturates a phone link, so HIS sessions are the collateral damage.

**How to apply:** Dispatch any wide workflow on `account:zai-individual-coding-plan` at `max_concurrency` 3 or less, off-peak when possible. Never amend a running workflow from a sibling session (refused: `workflow_run_not_retunable`); only the owning window can re-cap it. On flaky links: amend-resume, never rerun from zero; recommend USB tether over hotspot. Full receipt: `corpus/steal/TETHERED_LINK_STEAL_20260925.md`. Related: [[lite-free-window-schedule]], [[zcode-mobile-run-cards-20260920]], [[plain-text-status-law-20260920]].
