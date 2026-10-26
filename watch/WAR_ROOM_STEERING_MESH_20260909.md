# THE MESH — the steering revival lands in the war room (2026-09-09)

> **[AUDIT-TYPED]** status: DESIGNED TWICE, RUN ZERO TIMES — the pieces exist,
> the receipt is missing · trigger: operator "why can't we enable stateless
> communications between agents, we have them in personalities, why can't they
> steer each other — look into our kubernetes and steering research, self steal"
> · sources: watch/STEERING_LINEAGE_20260901.md (archaeology, receipts),
> watch/STEERING_SYNTHESIS_20260901.md (the revival design), this week's war
> room + kabuki cards.

## The answer to "why can't they steer each other"

**They can. The fleet designed it on 09-01 and the design is still correct —
it just never got its end-to-end receipt.** The lineage card's own open
thread says it verbatim: *"no receipt yet of an inter-seat hint changing a
target's course; that is the one claim still needing a real receipt."* The
war room work this week supplies the missing grammar (devices, traps,
governance) and the kabuki card supplies the coherence law. Same machine,
three arrivals.

## What already exists on disk (the self-steal table)

| Piece | Status | Where |
|---|---|---|
| Steer queue with EDIT-BEFORE-READ / CLAIM-BEFORE-ACT law | BUILT, 1 row UNREAD | steer.mjs + /board/steers.jsonl |
| Live multi-seat bus | BUILT (28+ steer messages) | /board/room.jsonl |
| Cache-hit steering over a live seat (DFHack overlay) | BUILT | mag/grok_steer.py |
| Steer message shape: `{target_seat, where, why, ttl, sha256→verkle tip}` | DESIGNED | STEERING_SYNTHESIS §1 — **addressing was already solved** |
| Steer = delta on a frozen shared tail (F2 compact-handoff, 2/3 ADOPT) | JURY-PASSED | STEERING_SYNTHESIS §0 |
| Frozen-prefix physics: 99.6% cache hit at $0 marginal | MEASURED | SWARM_DOCTRINE §3 — steering is FREE |
| Coherence = frozen shared prefix | 3/3 ADOPT | OPS_RESEARCH F1 = the kabuki coherence budget, same law |
| Steer eval battery: 6 models, leak/flip/emergent scoring | TESTED (40 files) | memory/runs/steer_compare/ → F-CONV-2's harness |
| Per-model tuned steer strings | TESTED | memory/runs/alpha_steer/ |
| Steer-back flag (seats consuming steers, replying) | TESTED | press digest `[STEER]` items, steer_back:true |
| Steering-as-attractors ("readout injects back to steer the liquid") | TESTED seed | ghost_experimenter/steer_feedback.jsonl |

## Why it dormed (receipt-backed, from the lineage card)

1. **Delivery layer died** — seat_steer files full of `"ok": false`:
   playwright missing, CDP socket hang-ups. The steering brain worked; the
   browser surface broke. (Tavern/brawl don't need browsers — this failure
   mode is GONE on the current surfaces.)
2. **Verkle concurrency** — O(n²) root recompute + a real lost-update race
   (1,049 dangling rows). Anchoring steers to the tip broke at multi-seat
   write volume. (Hardening was prescribed 08-25: file locks + incremental
   root. Still owed.)
3. **steer_router pins empty** — the routing half was never populated.
4. **Budget** — steering to expensive surfaces was capped. (The cache
   physics killed this objection on 09-01: frozen-tail deltas ride free.)

## The kubernetes answer (operator asked)

F1 already ran this experiment: the substrate salon parked mag-control-plane
/ kind-mag and fleet function was unchanged — idle containers ≠ the pulse.
**Agent-to-agent steering needs ZERO kubernetes**: the plane is files
(room.jsonl bus + steers.jsonl queue + resume), exactly like everything else
in the fleet. K8s only becomes real at kabuki scale — 500 agents on one
substrate — and that's parked behind Rocinante, by design.

## The war room adds the missing grammar (this week's work)

The August design steered TASKS ("gap: 8 leads classified, 0 harvested —
steer depth up"). The war room types the payloads: device → target
assumption → detonation condition. A trap is a steer with `if` semantics —
fire on transcript commitment, ttl as decay, SHERPA summit-check as the
governance gate, edit-before-read as the Mimosa of agent-steering. The
ractor DNA supplies what August never had: PERSONAS as the state ("we have
them in personalities" — operator, today). A steer between nameless seats is
routing; a steer between ractors is DRAMA — and drama is the part that holds
coherence.

## THE MISSING RECEIPT (the only thing between design and done)

**F-MESH-1:** one live inter-seat steer measurably changing the target
ractor's course — blind-verifiable from the transcript delta. That receipt
has been owed since September 1st. The tavern is the venue: Fen sets a trap
on Edison via the queue, Edison's next resume rides the frozen prefix plus
the delta, the transcript shows the assumption shift, the brawl HUD shows
the hp move. $0 on the cache physics. Everything else on this card is
already built.

## Lawful now vs gated

- NOW: read steer.py/steer_bus.py/tavern_chat.py and wire the queue to the
  tavern's existing resume loop — no new runtime, wiring only. Draft the
  F-MESH-1 protocol (one page).
- GATED (coldest-vertex): running the receipt, the trap-detonation detector,
  anything at 500-agent scale.
