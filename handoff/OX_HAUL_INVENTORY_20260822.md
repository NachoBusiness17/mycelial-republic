# OX-ALPHA FREE-WINDOW HAUL — buildable inventory (2026-08-22)

All captured from stealth/ox-alpha (free grok-level reasoning seat), every call $0. Banked in
handoff/. "content" = final answer; "reasoning" = the (often complete) design stream. For design
work the reasoning stream IS the deliverable.

## Batch 1 (OX_BURN_20260822T170237Z.json)
| task | result | where |
|---|---|---|
| provenance_gate | FULL spec (content 7.5k): fail-closed grounding gate, gate stamps citations, fabrication structurally impossible | json |
| swarm_free_seat_routing | FULL spec (content 4.8k): reasoning.heavy -> free seat primary, paid grok -> gated escalation (FREE_RATE_LIMITED_P1/CTX_OVERFLOW/CAPABILITY_GAP/QUALITY_GATE_FAILx2) | json |
| game_basecamp | shape (content 694): one deterministic core, many verifying renderers, verkle durable + hot channel | json |
| reasoning_ledger_impl | null content | (completed in Batch 1.5 below) |

## Batch 1.5 (OX_BURN_20260822T172429Z.json)
| task | result |
|---|---|
| game_basecamp_full | reasoning 18.7k (full basecamp/roster spec) |
| cache_meter_impl | reasoning 18.2k (honest meter impl) |

## Batch 2 (OX_BURN_20260822T171733Z.json)
| task | result |
|---|---|
| game_renderer | content 6.0k (Dverghold 3D renderer as another view over the sim core) |
| swarm_seat_scale | content 6.8k (scale escalation path into queue/drainer: quota gate, circuit breaker, defer-to-queue) |
| game_basecamp_full | content 0 (recovered in 1.5) |
| cache_meter_impl | content 0 (recovered in 1.5) |

## Batch 3 (OX_BURN_20260822T173742Z.json)
| task | result |
|---|---|
| redteam_reasoning_ledger | reasoning 20.9k (attacks + mitigations on the ledger) |
| redteam_provenance_gate | content 660 + reasoning 19.7k (bypasses + mitigations on the gate) |
| game_economics | reasoning 18.9k (economy model + anti-exploitation guardrails) |
| sovereign_mirror | reasoning 16.7k (edge-node persona spec) |

## Batch 4 (OX_BURN_20260822T174901Z.json)
| task | result |
|---|---|
| babel_fish_swarm | content 6.2k + reasoning 11.5k (stateless fleet -> one honest shared voice) |
| game_vertical | content 6.8k + reasoning 10.5k (adoption ladder + smallest launchable slice) |
| provenance_integration | content 2.5k + reasoning 14.8k (gate wraps the free seat, verkle provenance) |
| honest_billing_governor | reasoning 17.3k (per-seat real spend, rightsize routing, free-vs-paid escalation) |

## Earlier standalone artifacts
- handoff/OX_SEAT_AND_SEAT_CONTRACT_20260822.md — the seat-contract (routing/quota/reasoning-continuation/smallest slice)
- handoff/REASONING_LEDGER_DESIGN_20260822.md — the ledger schema/design
- handoff/REASONING_LEDGER_IMPL_20260822.md — the ledger build plan (invariants, file layout, 4-phase build, acceptance tests)
- handoff/ox_ledger.jsonl — live escalation ledger (deterministic + escalate + validate + commit + cache)

## Buildable priorities (from the haul)
1. **reasoning_ledger** — fully designed (design + impl + red-team): build it on the verkle/cache seam.
   Read: REASONING_LEDGER_DESIGN.md + REASONING_LEDGER_IMPL.md + redteam_reasoning_ledger (Batch 3).
2. **provenance_gate** — designed + red-teamed: build the grounding gate. Read: provenance_gate
   (Batch 1) + redteam_provenance_gate (Batch 3).
3. **swarm_free_seat_routing + swarm_seat_scale** — the free-seat routing + escalation scaling.
   Read: Batch 1 + Batch 2 swarm tasks.
4. **game** — basecamp_full (1.5) + game_renderer (2) + game_economics (3) + sovereign_mirror (3):
   the rendering-agnostic core + renderer + economy + edge nodes.

Each design is a buildable RIB. Fold into the loop / hand to the drainer when we build.
