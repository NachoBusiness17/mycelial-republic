---
name: mesh-comms
description: Intra-agent mesh network communication — how seats, lanes, and ractors talk to each other (chan rows, rib_bus, panels, wants). Load when a seat needs another seat's verdict, handoff, or attention.
---

# MESH COMMS — the fleet's nervous system

**Grounding:** chan comms clause 11 (typed rows {from_lane, to_lane, msg, ref}
appended to `watch/room.jsonl`; the manager answers IN LINE on the chan) ·
rib_bus (`memory/rib_bus/`, doctrine + per-seat ribs) · ractor panel protocol
(folds at fixed point; nine chairs) · wants intake (WANTS.md → self-tending
tender) · mycelium edges (activation-weighted relationships).

## The four channels, and when to use each
1. **CHAN** (synchronous-ish, conversational): lane-to-lane messages as typed
   rows on watch/room.jsonl. Use for asks, handoffs, in-line answers.
2. **RIB_BUS** (doctrine/bus): publish an invariant once; every seat reads it
   at boot. Use for laws and standing facts, never chatter.
3. **PANELS** (verdicts): ractor shapes over one brief, blind divergence,
   fold at fixed point. Use for decisions that need witness diversity.
4. **WANTS/QUEUE** (asynchronous work): file a want; the tender converts it
   to queue items. Use for work, not conversation.

## Procedure
1. Pick the channel by TEMPORAL need: now → chan; always → rib_bus; decide →
   panel; later → wants.
2. Send typed, small, pointed rows — a message that needs a summary is two
   messages.
3. Fold verdicts back to the durable surface (inbox + index_events), never
   leave decisions living only in the mesh.
4. Failure mode to refuse: talking INSTEAD of doing. The mesh moves work;
   it is not the work.

**Falsifier:** a mesh message is justified iff removing it changes a file,
decision, or receipt within one window. Chatter that changes nothing is
traffic — meter it, then kill it.
