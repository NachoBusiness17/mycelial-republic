---
name: cerebras-parked-20260926
description: Operator decision 9/26 — Cerebras parked until a use is found; lane
  never worked once (zero generations ever), dormant stays true, no card attach;
  revisit trigger = B2-142/143 research
metadata:
  node_type: memory
  type: project
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

Operator asked "did cerebras ever work?" on 2026-09-26. Ledger-traced answer:
NO, not once. 9/18 scout flagged it as a candidate (1M tok/day, 8K ctx cap,
5 req/min) but the fleet never had a working key; 9/20 standing key gap; 9/21
free tier became card-gated (ALERT-CEREBRAS-CARD); 9/26 primary docs confirm
card-gated 30-day trial ($5 expiring credits, 5 RPM / 90K TPM / 1M TPD, 2
models) and the key we hold lists models but 402s on chat. Zero successful
generations in the entire record.

**Decision (operator, same hour):** "park it then. until we find a use for
it." Lane stays `dormant: true` in configs/providers.yaml (B2-36 stripped it
from the ladder and all 6 routing lists), no card attach. Decision recorded
on the queue/todo.md P0 row.

**Revisit trigger:** B2-142 community dig landed 9/26 night with findings.
Fleet-fit verdict: our short-context batch pattern fits the trial shapes
easily (B2-04 burned 6,890 tokens vs 1M TPD), but community kill-pattern is
brutal: $5 gone in 10 minutes (agentic loops) to 3 days (Llama 70B agent),
because all input including context counts toward TPM and 50k-context agent
loops die in ~2 calls. No cached-input discount (cache billed at standard).
Fleet's 97.3 pct prefix-cache engine earns zero on Cerebras. Dormant stays
correct; a GO should be a scheduled 30-day batch sprint, never a routing-list
add. Related: [[flash-lane-burn-20260926]], [[experiment-on-absence-law]].

**B2-133 consumer purge LANDED 9/26 night:** dormant flag gate wired into
7 mag/ files (fuel_feed, rotation_harness, lane_salon, quorum_window,
research_fanout, cost_truth, free_tier) via new mag/dormant.py single-reader.
Operator GO = flip one flag in providers.yaml, every gate restores with zero
code edit. Gate honestly dropped nvidia + mistral too (both dormant:true).
Live dormant roster: {saelis, gemini, mistral, cerebras, nvidia}. Remaining
stragglers (swarm_worker, _consensus_witness, scale_salon, ask_router,
subscriptions, seat_corpus, cheap_swarm nvidia default) self-fed as B2-521/
541/542/543. Cost-truth repricing (B2-522) accepted "unpriced" as honest
unknown, no frozen rate table invented.
