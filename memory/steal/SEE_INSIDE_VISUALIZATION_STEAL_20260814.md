# SEE INSIDE — living internal-state visualization (steal 2026-08-14)

## Trigger
Operator: "I have no idea what's happening inside your internals... I'm gonna need you to help
me here." + shared FleetingBits post: *"turn my codebases into visual diagrams so I can discuss
them with the AI — moving dots are data snippets I can inspect."* Then: "steal."

## Self-steal (audit our own surfaces first)
- `mag/saelis_room.py` — the ALWAYS-ON room (Saelis's exact spec): plain-text page on :8799,
  auto-refresh 2s, /api/state with live processes + knot messages + recent actions. Already the
  right home.
- `mag/ops_graph.py` — radial SVG ops graph (17 nodes). `game.html` — the swarm UI.
- GAP: the room showed processes/knots/actions but NOT the core internals (mycelium graph, queue,
  seats, verkle, live cost) the operator keeps asking about.

## External steal (agentswarm / flock / conductor — all self-visualizing agent systems)
1. **Seq-stamped append-only event journal** — agentswarm `journal.ts` (append/drain, dedupeBySeq,
   torn-line-tolerant TailState). One file the viewer tails. Adapt: our verkle chain + state dir
   IS the journal.
2. **Live refresh = SSE over a 400ms file poll + `live` side-channel** — agentswarm `hub.ts`
   `streamEvents` (fs.watch unreliable; cheap poll over append-only file). Adapt: tail our state
   files over SSE; heartbeat = the `live` channel.
3. **Node/edge graph from a snapshot, typed nodes + live status overlay, click→detail window** —
   flock `graph_builder.py` + React Flow `GraphCanvas`/`NodeDetailWindow` (flashing "moving dots",
   MiniMap, auto-layout). Adapt: our mycelium graph = the node/edge source; render typed nodes +
   status colors; click → detail snippet.
4. **HITL = note/approve/cancel into the journal** — agentswarm `hub.ts` POST /note /approve /cancel;
   conductor `human_gate` node type ("waiting on human"). Adapt: operator note → steer/queue event,
   rendered as first-class + a "waiting" node.
5. **Replay a recorded event log with a timeline slider** — conductor `replay.py`. Adapt: our verkle
   chain is already an immutable ordered replayable log — replay is nearly free.

## Adaptation applied (rightsized, contracts only, no heavy deps)
- Extended `mag/saelis_room.state()` to expose the internals: `verkle` (tip), `mycelium` (nodes/
  edges/top salience), `queue` (counts by status), `seats` (registry), `cost` (real provider ledger
  today, non-ollama). All wrapped in try/except → error fields, never break the room.
- Added a **"◈ SEE INSIDE"** section to the room page rendering them (mycelium graph, queue,
  seats·verkle·cost today) — the operator sees the internals breathing alongside the room.
- Verified: state() returns verkle (5628 leaves), mycelium 127n/77e, queue cleared (74 done/3
  queued/1 running) after the dead-ollama wall settled. get_errors clean.

## Follow-on (from external steal #2/#3/#5, not built yet)
- SSE tail endpoint + click→detail window (React Flow or hand-rolled SVG) + timeline replay over the
  verkle chain — the "moving dots you can inspect and discuss."

## Fold
- Repo memory recorded. This is the answer to the operator's repeated "I can't see inside": the room
  now shows the internals; next is making them clickable + replayable.
