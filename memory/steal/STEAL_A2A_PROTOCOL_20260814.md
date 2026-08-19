# STEAL — A2A Protocol (v1.0.0) as Mag local boundary, not a wire
**Date:** 2026-08-14
**Source:** Agent2Agent (A2A) Protocol Specification, latest released 1.0.0.
https://a2a-protocol.org/latest/specification/
https://a2a-protocol.org/latest/topics/key-concepts/
**Method:** steal the INVARIANT, not the DNA. No runtime dependency. We do NOT claim A2A wire
compatibility (JSON-RPC / gRPC / HTTP+JSON, Agent Card URLs, OAuth, webhooks).

## What the spec actually separates
Four layers Mag already named in all-seat-roundtable-001, now with their nouns:
1. Identity / capability declaration (`AgentCard`: who, skills, transports, what is optional).
2. Message: one communication turn (`role` + `parts`). Not the deliverable.
3. Task: stateful unit of work with an id, `contextId`, and a lifecycle
   (submitted/working/completed/failed/canceled/rejected; interrupted: input-required, auth-required).
4. Artifact: the tangible output of a task. Messages MUST NOT be used to deliver task outputs.
Opaque execution: collaboration does not require exposing internal state, memory, or tools.
Bindings (JSON-RPC, gRPC, REST) are Layer 3. The data model is Layer 1. Steal Layer 1. Refuse Layer 3
as Mag's public surface.

## Self-steal (what Mag already owns)
- `seat_steer.SURFACE_DRIVERS` + `SURFACE_ALIASES` + `PARTICIPANTS`: local identity and transport
  registry. That is our Agent Card, private, not `/.well-known/agent-card.json`.
- `frontier_salon.roundtable_id` + contribution `message_id`: Task + Message ids.
- `party_subchain`: the relation (append-only messages). Parent `last_leaf_hash` is context, not a
  public `contextId` service.
- Roundtable JSON under `memory/runs/frontier_salon/` + `agent_corpus`: Artifacts.
- `rib_bus`: instruction layer, not a skill listing for strangers.
- Down seats as `ok=false` rows: failed/rejected records that do not stop the table.
- Human gate on novel deltas: A2A `TASK_STATE_INPUT_REQUIRED`. Do not auto-complete doctrine.

## External-steal (adapt the contract, refuse the DNA)
TAKE:
1. Opaque seats. A participant is an adapter. No seat may demand another seat's memory, tools,
   kernel, or CDP. Mount the bus. That is the same cut as "9222 is not grok."
2. Message vs Artifact. Subchain `move` text is a Message. Steal files, roundtable JSON,
   `RIB_DOCTRINE_CANONICAL.md`, corpus hashes are Artifacts. Chat recap is not the deliverable.
3. Task lifecycle for a roundtable. `roundtable()` is one Task. Terminal after the artifact is
   written. Do not mutate that JSON in place. Further talk is a new Task in the same context
   (same parent leaf / same `roundtable_id` family), not an edit.
4. Interrupted != down. `input-required` is the human gate. `failed` is a down seat. Both are
   records. Neither is a chair.
5. Capability validation before spend. If a skill is not declared, refuse with an explicit error
   (A2A `UnsupportedOperationError`). Mag: do not call grok/supergrok unless `[priority]` or the
   participant list opted them in. Missing capability is `ok=false`, not a live CDP chase.
6. `historyLength` is Mag `transcript_limit`. Bound the attributed transcript. Do not flatten
   speakers into one advisor (A2A messages keep `role`; Mag rows keep `label`).
7. Layered spec. Frozen relation (data model) persists across bindings. Models and transports
   are interchangeable. That is the doctrine RIB in A2A nouns.

REFUSE:
1. Client/server throne. A2A is a client hitting a remote agent. Mag's bus is peers appending to
   a shared relation. Do not make salon a server that "owns" grok.
2. Public Agent Cards for ghost / memlang / riddler / verkle / swarm internals. Private machinery
   stays private. A card that lists those skills is a leak, not discovery.
3. JSON-RPC / gRPC / REST / SSE / webhook bindings as Mag's seat protocol. `seat_steer` already
   is the local binding. CDP:9222 is a transport, not a seat.
4. Push-notification webhooks to the operator. The operator is not a webhook. The bus is disk.
5. Claiming A2A wire compatibility, proto regeneration, or `A2A-Version` headers.
6. Using Messages as the durable output (their own rule). Pasting a take into chat and asking
   the human to relay is delivering an Artifact through a Message, which they forbid and we
   already named as the anti-pattern.

## Adaptation (named, not a new throne)
- Treat `roundtable()` result JSON as the Task Artifact. Subchain rows are Messages. Corpus
  hashes are Artifact ids.
- Name down-seat rows with an explicit task-state analog in `extra` (`failed` vs `rejected` vs
  `input-required`), so a down CDP is not filed as a completed grok turn.
- Participant registry (`PARTICIPANTS`) is the private Agent Card: label, surface, agent,
  version, and whether grok-spend is allowed. No well-known URL.
- Capability check in `seat_steer.send`: unknown surface or scarce grok without `[priority]`
  returns `ok=false` with a typed error, and still appends the record.
- Do not add an A2A HTTP server.

## Honesty
- Spec version stolen: 1.0.0 as published at the URLs above on 2026-08-14. Patch numbers do not
  change protocol compatibility per their own versioning section.
- We did not implement proto, JSON-RPC, or Agent Card signatures.
- A2A's enterprise auth (OAuth, mTLS, API keys) is out of scope for Mag seats talking on disk.
