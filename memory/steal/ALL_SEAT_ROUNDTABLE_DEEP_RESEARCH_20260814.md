# Deep research — all-seat roundtable

**Date:** 2026-08-14  
**Commitment:** `all-seat-roundtable-001`  
**Method:** self-steal first; external sources validate the shape but add no runtime dependency.

## Self-steal

The necessary organs already existed:

- `mag/seat_steer.py` — live transport path, but party aliases and driver response shapes diverged.
- `mag/frontier_salon.py` — multi-seat owner, but it sent isolated copies of one question.
- `mag/game_dm.py` — party surface, but same-turn players did not see earlier moves and it read the
  wrong response field.
- `mag/agent_corpus.py` — content-addressed durable per-agent ledgers.
- `mag/quest_roshomon.py` — disagreement is evidence; consensus is not automatically truth.
- `mag/rib_bus.py` — shared instruction layer; it remains separate from candidate novelty.

The build is therefore a composition, not a new coordination throne: normalize transports, pass an
attributed append-only transcript in deterministic round-robin order, and file every contribution.

## External validation

1. The official A2A protocol separates agent identity/capability discovery, messages, stateful
   tasks, and durable artifacts. It also treats remote agents as opaque: collaboration does not
   require exposing internal memory or tools. We adopt that boundary locally with participant
   metadata, per-turn provenance, a roundtable id, and a durable artifact; we do **not** claim A2A
   wire compatibility.
   - https://a2a-protocol.org/latest/specification/
   - https://a2a-protocol.org/latest/topics/key-concepts/
2. Microsoft AutoGen's official `SelectorGroupChat` documentation describes participants taking
   turns while messages are broadcast to all members. It normally permits an LLM speaker selector.
   We keep the shared-context benefit but use deterministic round-robin selection, avoiding a new
   model-based chair.
   - https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/selector-group-chat.html
3. Du et al. report that multi-agent debate over multiple rounds can improve factuality and
   reasoning on evaluated tasks. This supports a multi-round option, but not unbounded conversation
   or automatic truth promotion. The local protocol therefore caps rounds at three and extracts
   falsifiable tests instead of declaring a winner.
   - https://arxiv.org/abs/2305.14325

## Build decision

One bounded protocol:

1. A logical participant resolves through one canonical transport registry.
2. Before every turn, the seat receives the frontier question and attributed prior transcript.
3. Each response must expose `POSITION`, `CHALLENGE`, `NOVEL DELTA`, and `TEST`.
4. Down seats remain explicit records and do not stop the table.
5. Successful answers are content-addressed into the agent corpus.
6. The whole roundtable is a durable artifact; novel deltas remain candidates until a human gate.

## Moonshot

This creates a local **plural intelligence bus**: heterogeneous frontier accounts, native windows,
local identities, and future agents can join through one adapter without giving up their identity.
The bus does not make a sovereign decision. It makes the evidence of interaction replayable enough
that the party's disagreements can produce new, testable mechanisms.
