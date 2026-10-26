# THE ESTATE'S OWN WORLD SERVER v0

The first server that is fully ours. The estate compiled CMaNGOS (a full
WoW server, roughly 2M lines) as a learning specimen, then built the five
mechanisms a world server actually needs on top of the estate's own
physics organ. Server-authoritative: the water graph runs HERE; clients
propose actions; the server validates, stages, ticks, and broadcasts.
No client ever mutates the world.

Real size (measured 2026-09-29 with wc -l, not estimated):

| file | lines | owns |
|---|---|---|
| server/__init__.py | 26 | package card |
| server/protocol.py | 108 | the wire (line-based JSON over TCP) |
| server/auth.py | 122 | v0 users file + session ids |
| server/world.py | 265 | the authoritative Mountain + event log |
| server/server.py | 390 | asyncio server, tick loop, fan-out, demo, debug client |
| total | 911 | five mechanisms, ours, including the demo driver |

The physics is not copied: server/world.py imports
`mag.water_graph.WaterGraph` (the same engine the Godot slice mirrors),
so there is one hydraulic truth in the estate, not two.

## Run

```text
.venv\Scripts\python.exe -m server.auth server\users.json add ada     # add a user
.venv\Scripts\python.exe -m server.server                             # serve 127.0.0.1:8800
.venv\Scripts\python.exe -m server.server --demo                      # 30 headless ticks, prints the WIN
.venv\Scripts\python.exe -m server.server --demo --tick-ms 80         # faster demo
.venv\Scripts\python.exe -m pytest tests/test_server_v0.py -q         # 15 passed
```

Options: `--host --port --tick-ms --users --log --ticks`. The standing
event log is `logs/world_server.jsonl` (append-only, hash-chained);
`--demo` logs to a temp dir instead unless `--log` is passed explicitly,
and grabs an ephemeral port unless `--port` is passed explicitly.

## The world

The Mountain slice's exact board (roblox_to_godot/scripts/game.gd):

- nodes: spring elev10 vol6, terrace elev6, gate1 elev5 XOR,
  hollow elev3 vol2, waste elev0, crown elev14 COLD
- pipes: p_spring spring->gate1, p_terrace terrace->gate1,
  p_out gate1->hollow, p_drain hollow->waste,
  p_bypass spring->terrace (siphon, crest 2, starts SHUT)
- WIN: crown volume >= 4. Total water in the world: 8.
- tick cadence: 800ms, driven by the server loop.

The only way uphill is the estate's steam law: boil anywhere, it
condenses at the highest cold node (the crown). Every unit that reaches
waste is gone. v0 does not freeze on WIN: the crown has no outlet, so
`winner:true` is sticky and the mountain keeps drinking.

## Protocol spec

Line-based JSON over TCP: one JSON object per `\n`-terminated UTF-8 line,
both directions, canonical encoding (sorted keys, compact). You can
drive the server from telnet. Max line 64 KiB.

C -> S:

```json
{"op":"hello","user":"ada","pass":"steam"}
{"op":"action","sid":"<64-hex>","verb":"boil|valve|join|tag|say|whisper","target":"spring|p_bypass|<text>|<user|text>","n":<monotonic int>}
```

S -> C:

```json
{"op":"welcome","sid":"<64-hex>","world":{...full snapshot...}}
{"op":"ack","verb":"boil","target":"spring","user":"ada","applies_at_tick":1}
{"op":"reject","why":"DRY_POOL","verb":"boil","target":"crown"}
{"op":"tick","n":4,"nodes":{"spring":0,"terrace":0,"gate1":0,"hollow":0,"waste":0,"crown":4},"events":["..."],"winner":true}
```

Verbs (the six-row CHAT_TABLE contract, server/protocol_table.py
CHAT_DIGEST; the offline GDScript legality mirror is
roblox_to_godot/tests/rule_parity_runner.gd — its `_validate`/
`_admit_action` reject exactly what the server rejects at receipt,
Q11 2026-10-01):

- `boil <node>`: lift 1 unit to steam (condenses at the crown).
- `valve <pipe>`: toggle a pipe open/shut (the siphon starts shut).
- `join <node>`: stand at a pool; seeds v1 interest management.
- `tag <node>`: tag a fish at a wet pool (score +1; a dry pool holds no
  fish, the school follows water).
- `say <text>` (LW6 chat v1): staged like any action, applied at the
  tick, delivered as a tick event (`user: text`); empty or >240 chars
  rejects `BAD_TEXT`.
- `whisper <user|text>` (LW6): the one receipt-time verb — mutates no
  world state, so it rides the per-session direct outbox and never
  enters tick events; malformed/over-length rejects `BAD_TEXT`, an
  unknown user rejects `UNKNOWN_TARGET`. Bots speak through the same
  channels.

Action reject codes (typed, per the v0 spec): `UNKNOWN_SID`,
`NOT_YOUR_TURN` (RESERVED, never emitted in v0; there is no turn
structure, it exists so v1 turn modes inherit the vocabulary),
`UNKNOWN_VERB`, `UNKNOWN_TARGET`, `DRY_POOL`, `BAD_TEXT` (chat v1),
plus the LW7 anti-cheat pair `RATE_CAP` (one acked action per session
per tick, whichever verb it carries) and `STALE_NONCE` (replayed
action id; the id burns at receipt even on a reject).
Transport rejects outside the action set: `BAD_AUTH` (one code for
unknown user and wrong password, so the wire does not enumerate users),
`BAD_JSON`, `UNKNOWN_OP`, the SRP6 auth pair `BAD_PROOF` /
`STALE_CHALLENGE`, and the frame-integrity code `BAD_MAC` (R3, armed
sessions only).

Semantics that matter:

- Actions are VALIDATED at receipt (reading current world state) and
  STAGED; they APPLY in arrival order at the start of the next tick,
  before the physics. The tick is the only mutator, so any (action,
  tick) interleaving is totally ordered and replays byte-identically.
- Broadcasts are encoded once per tick; every client receives the same
  bytes (test-pinned).
- The event log is append-only and hash-chained (row sha covers the row
  minus its own hash, prev links to genesis 64 zeros): in memory AND as
  JSONL on disk. Reopening a log path continues the chain and refuses
  to boot on a tampered file. No wall clock inside rows: replayability
  beats timestamps; correlate by seq/tick.

## What this borrows from the CMaNGOS lesson plan

The five mechanisms every world server needs, and where ours lives:

| mechanism | CMaNGOS | ours |
|---|---|---|
| auth | realmd SRP6 | server/auth.py: salted SHA256 file, honest that SRP6 is the lesson to port |
| session | session keys from SRP | sha256(user+salt+time+counter) sids, roster in the world |
| dispatch | packet table routing handlers | op dispatch in _handle_client, verbs validated in MountainWorld.validate |
| tick | world update loop on timers | fixed-cadence asyncio task (800ms), staged-then-tick |
| broadcast | interest-managed updates | per-client queues, one encode, fan-out to all |

Ours is 911 lines including the demo driver and a wire-level debug
client; theirs is roughly 2M. The point is not the ratio, it is that the
shape is now legible: we can read every line of our world server, and
we know exactly which parts are toys (auth) because we labeled them.

## What v1 owes

- SRP6-class auth (the realmd lesson) + TLS or an authenticated
  transport; kill plaintext passwords on the wire.
- Interest management: per-client views of the snapshot (join already
  carries position for this).
- Persistence beyond the log: restore world state on restart (the log
  chain already contains the replay).
- Match reset op (v0's WIN is sticky), rate limits, backpressure on
  broadcast queues.
- The Godot client wiring: see below.

## Wiring the Godot client (roblox_to_godot) to become the first real client

The Mountain slice already runs the same physics locally
(water_graph.gd is a line-for-line port); to become a real client it
needs to INVERT its authority:

1. Replace the local `graph.tick()` Timer with the `tick` broadcast:
   feed `nodes` volumes into the local graph view (render-only), and
   append the server `events` list to last_events.
2. Send `hello` on connect (Godot's StreamPeerTCP + a line buffer),
   keep `sid` from the welcome, and rebuild board geometry from the
   welcome snapshot instead of the hardcoded POOL_LAYOUT.
3. Convert local inputs to proposals: SPACE -> `action boil
   <nearest_pool>`, E -> `action valve <nearest_pipe_end>`; render acks
   as hints and rejects as the existing hint_text lines (map DRY_POOL
   to "the pool is dry", UNKNOWN_TARGET to "no valve within reach").
4. The flock can stay client-side for now (sensing only); `tag` actions
   already score server-side, so move the score HUD to the tick/welcome
   payload when the school becomes server-simulated.

## Tests

`tests/test_server_v0.py` (417 lines): protocol roundtrip against a
real in-process TCP server on an ephemeral port, auth accept/reject,
all action reject types, NOT_YOUR_TURN reserved-never-emitted, join/tag/
valve application at the tick boundary (including the XOR hold law),
byte-identical broadcasts to two clients, fixed-cadence tick flow,
byte-identical node-volume sequences from two fresh worlds (world-level
AND through the server path), WIN detection + stickiness, append-only
tamper-evident event log (chain continues across reopen), auth store
laws, the headless demo subprocess, graceful shutdown.

Latest measured run (2026-09-29): `15 passed in 4.29s`.
