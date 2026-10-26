# OUR SERVER v0: the estate's own world server (2026-09-29)

Seat: zcode (GLM-5.3). Build order: THE ESTATE'S OWN WORLD SERVER v0.
The estate compiled CMaNGOS as a learning specimen and decided: we build
our own. This is the first server that is fully ours. Server-authoritative:
the water graph runs on the server; clients propose actions; the server
validates, stages, ticks at a fixed 800ms cadence, and broadcasts state.

## Files (all new, em-dash count 0)

- `server/__init__.py` (26 lines): package card
- `server/protocol.py` (108): OUR wire: line-based JSON over TCP, canonical
  encode, the five action reject codes (UNKNOWN_SID, NOT_YOUR_TURN
  reserved/never emitted in v0, UNKNOWN_VERB, UNKNOWN_TARGET, DRY_POOL)
  plus transport codes (BAD_AUTH, BAD_JSON, UNKNOWN_OP)
- `server/auth.py` (122): v0 auth: JSON users file, salted SHA256, session
  ids sha256(user+salt+time+counter); honest doc that SRP6-class auth is
  the CMaNGOS realmd lesson v1 owes
- `server/world.py` (265): MountainWorld: imports mag.water_graph.WaterGraph
  (no copy; one physics truth), Mountain board verbatim from the Godot
  slice, staged-actions-then-physics tick, append-only hash-chained event
  log (memory + JSONL, chain continues across reopen, refuses tampered
  files), WIN = crown >= 4, sticky
- `server/server.py` (390): asyncio TCP server (default :8800), fixed
  cadence tick task, per-client queues, single encode per broadcast,
  graceful shutdown, wire-level debug Client, --demo (30 headless ticks,
  two simulated clients: one boils, one tags, prints the WIN)
- `tests/test_server_v0.py` (417): 15 tests (list in server/README.md)
- `server/README.md`: run instructions, full protocol spec, the CMaNGOS
  five-mechanisms table, v1 debts, Godot wiring plan

Package total: 911 lines (wc -l, 2026-09-29). The task brief guessed
"600 lines"; the real number is 911 including the demo driver and debug
client. No fabricated counts in this receipt or the README.

## Real test line

`.venv\Scripts\python.exe -m pytest tests/test_server_v0.py -q`
-> `15 passed in 4.31s` (final run, 2026-09-29).

Census note for the AGENTS.md carrier bullet: tests/ gained +1 file and
+15 collected (`pytest --collect-only -q tests/test_server_v0.py` ->
`15 tests collected in 0.41s`). Census date 2026-09-27 is 2 days fresh
(patrol threshold 7d) and the +15 drift is under the B2-244 tolerance
of 20, so no tripwire fires; the operator refreshes that bullet on the
next patrol anyway.

## Demo evidence

`python -m server.server --demo --tick-ms 60 --ticks 30` -> exit 0:

```text
tick   1: crown=1 gate1=0 hollow=2 spring=4 terrace=0 waste=0
tick   2: crown=2 gate1=0 hollow=2 spring=2 terrace=0 waste=0
tick   3: crown=3 gate1=0 hollow=2 spring=0 terrace=0 waste=0
tick   4: crown=4 gate1=0 hollow=0 spring=0 terrace=0 waste=0  WIN
...
stats: {'clients': 2, 'ticks': 30, 'actions_staged': 34}
THE CROWN FILLS. WIN at tick 4; boiler boiled 4, tagger tagged 30.
```

## The 3 design decisions

1. Import the physics, never copy it. server/world.py imports
   mag.water_graph.WaterGraph from the repo root. The Godot slice
   already mirrors that engine line for line; a second Python copy
   would be a third truth. One organ, three surfaces (server, tests,
   Godot).
2. The tick is the only mutator. Client actions are validated at
   receipt (typed ack/reject reading current state) but STAGED; they
   apply in arrival order at the start of the next tick, before the
   physics. This makes the world totally ordered and byte-replayable
   regardless of packet timing (test-pinned two ways: world-level and
   through the server path), which is the whole meaning of
   server-authoritative. Corollary: the demo drives a manually-pumped
   cadence so its wire order is deterministic and it can never race.
3. The event log is append-only and hash-chained, with no wall clock
   inside rows (seq + tick only; the wow_player/gwap house pattern,
   row sha over the row minus its own hash). Replayability beats
   timestamps; tampering with any past row refuses the boot. Reopening
   a log path continues the chain rather than truncating.

## What the Godot client needs to become the first real client

- Replace the local tick Timer with the `tick` broadcast: render from
  `nodes`, append server `events` (water_graph.gd becomes a view, not
  the authority).
- `hello` on connect (StreamPeerTCP + line buffer), keep `sid`, rebuild
  board geometry from the welcome snapshot instead of hardcoded
  POOL_LAYOUT.
- Convert inputs to proposals: SPACE -> action boil <nearest_pool>,
  E -> action valve <nearest_pipe_end>; render reject codes into the
  existing hint_text channel (DRY_POOL -> "the pool is dry").
- Flock stays client-side (sensing only) for now; `tag` already scores
  server-side, so move the score HUD onto the tick/welcome payload when
  the school becomes server-simulated.

## Honest limits (v1 owes)

SRP6-class auth + a real transport (passwords are plaintext on the wire
today; 127.0.0.1 binding is the whole security model), interest
management (join already carries position), world-state persistence
(the log already contains the replay), match reset (WIN is sticky by
design: the crown has no outlet), rate limits, backpressure.

## Verify

```text
.venv\Scripts\python.exe -m pytest tests/test_server_v0.py -q
.venv\Scripts\python.exe -m server.server --demo
```
