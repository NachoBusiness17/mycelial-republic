# SALON LANE A — GLM-5.3 agentic-RL invariants for steer_bus/switchboard
date: 2026-09-01 07:10Z | lane: harness/agentic lens | class: SALON-A
source: GLM53_LINEAGE_DROP_20260901.md ("Agentic RL" §103–118; "model library" §216–244); context STEERING_SYNTHESIS_20260901.md, FLEET_STRUCTURE_20260901.md
scope: board→switchboard→effect-broker→receipt (drop's own analogy, §118, ours not Z.AI's).

## 3 SHARPEST INVARIANTS TO ADOPT
**I1 — Trajectory is the first-class object, not the model response.** Drop §118 V: "both systems treat agents as workers producing auditable trajectories rather than treating a model response as the final unit of truth." Adopt: switchboard persists full trajectories (board→switchboard→effect-broker→receipt) as the audit unit; model fingerprint doubles as trajectory lineage. Load-bearing: makes receipts verifiable beyond a single turn.
**I2 — Version-pinned, stale-filtered trajectories + env-collapse drops.** Z.AI: "tracks policy versions and filters stale trajectories; drops environment-collapse failures" (§111–112). Adopt: every effect-broker receipt carries a *policy/steer version anchor*; stale-anchor receipts are filtered, not trusted; an errored/env-collapsed seat emits a *DROPPED* receipt, never PASS. This corrects STEERING_SYNTHESIS gap #6 ("dumb-seat obedience is unenforced — a silent miss produces no error").
**I3 — KV-locality routing / unified message-list as a cheap consumption contract.** Z.AI: "routes multi-turn work to preserve KV-cache locality" + "standardizes every trajectory into a unified message-list format" (§113, §115). Adopt: switchboard routes steer/receipt traffic onto F1 frozen-prefix lanes (99.6% cache-hit, $0, SWARM_DOCTRINE §3 per STEERING_SYNTHESIS) and stores *one unified row* (hint/steer/receipt) so a dumb seat consumes without re-reading the chain — mapped onto steers.jsonl/room.jsonl `{target_seat,where,why,ttl,anchor,delta}` (§1).

## THE 1 INVARIANT WE ALREADY HAVE
**Receipt/anchor tamper-evidence tied to a verkle tip.** Drop §244: build the library "around trajectory passports and receipts." Our steers/invariants already anchor to verkle_tip.json (tip index 6311, 6311/6311 chains intact, 0 orphans — STEERING_SYNTHESIS §2). Anchor-inherits-chain-integrity is the one Z.AI convergence already operational, not borrowed.

## VERDICT — does agentic-RL justify PILOT steering/abort harness as next build?
**Weak-yes — but only as the STEERING_SYNTHESIS §7 30-min $0 demo, not new org.**
Supporting: Z.AI independently validates trajectory-as-object (I1), stale/error filtering (I2), and KV-locality/unified-format (I3) — the exact rail switchboard sits on; drops residual "is this real" doubt.
Against: nothing is acquired (FLEET_STRUCTURE: STRUCTURE-OVER-ACQUISITION); all organs exist (board, steers.jsonl, verkle chain, F1/F2). The PILOT is assembly — ~$0.001/30min — and directly tests steer→claim→receipt plus the I2 abort (env-collapse→DROPPED).
Tie-break (STEERING_SYNTHESIS gap #7): scope the demo to *parallel search breadth/depth steering only*, never verdict synthesis. If the loop can't be proven at $0.001, drop it.
Alternates (probe batteries, codex Hands seat) are real but lower leverage — they don't validate the trajectory/steer/abort contract that I1–I3 name as load-bearing. PILOT first.

## HONEST STATUS
I1–I3 are **UNVERIFIED** against our cage until §7 live receipts a loop (queue UNREAD→CLAIMED→DONE, measured $≈$0, env-collapse→DROPPED). All Z.AI numbers vendor-reported; the analogy is ours (§118). No novel.
