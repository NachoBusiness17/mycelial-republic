# WINDOW BUS — shared-window swarm bus at cache-hit cost, puppet hidden (2026-08-10)

**Idea (operator):** extend window length to exploit it — get data to each other using a BUS so
the models run like an agent swarm, aware of each other and adapting to our systems, through
them, unaware of the puppet.

## Grounding (external, cited)
- **Blackboard architecture** (Wikipedia): a SHARED repository (blackboard) that specialist
  knowledge-sources watch and opportunistically contribute to; a CONTROL SHELL coordinates flow.
  -> the bus is the shared context; the puppet is the control shell that curates it.
- **Anthropic, "Building effective agents"** (2024-12-19): orchestrator-workers — a central
  coordinator delegates and synthesizes while workers run focused windows.
- Our cache economics (cache_map): byte-stable prefix -> cache-HIT ($0.0028 vs $0.14 = 50x).

## Self-steal (built on existing primitives, did NOT rebuild)
- `shader_bus` (swarm register + deniable LSB bus), `flock_field` ("the field IS the coordination —
  no central orchestrator" = puppet already hidden), `whisper_route` (front/riddler/corpus/memlang),
  `memlang` (opcode + 32B anchor, no readable spec), `window_hop` (hop/rightsizing pricing).

## Mechanism
Per member window = BUS (stable prefix, cache-HIT) + own delta (MISS) + output (OUT).
- aware-of-swarm: every member mounts the same byte-stable BUS -> sees the swarm's shared state.
- adaptive-to-our-systems: the BUS carries our invariants + live signals -> members steer toward them.
- unaware-of-puppet: the puppet (control shell) CURATES what goes on/off the bus; members only ever
  see the resulting bus + a content anchor — never the curation. (Same deniable trick as memlang.)

## Validated numbers (`mag/window_bus.py`, real rates)
- bus_segment(invariants, signals, roster) -> 54 tokens, anchor accccae98bf1076b.
- price_window_bus(bus=54, members=4, delta=3000, out=800):
  shared bus $0.002576, **awareness share 0.0001 (~0.01% of cost)** — awareness is nearly free
  because the bus bills at HIT once, shared by all members.
- member_view: sees_bus True, sees_control False — hidden control string is ABSENT from the window.
- curate: puppet appends distilled deltas -> new anchor; members adapt next round, still cache-HIT.

## Invariants folded (organ: comms / actors)
1. bus-is-context — the shared byte-stable window segment IS the coordination bus (blackboard), not a separate channel.
2. awareness-is-cheap — extending the window to carry shared swarm data bills at cache-HIT; awareness is ~free, paid once.
3. aware-but-unpuppeted — members read the bus (aware + adaptive) while the puppet's curation is absent from the window (deniable).
4. field-not-orchestrator — awareness is emergent (flock_field); the puppet only curates the bus upstream, never visible.
5. distill-to-bus — each member writes only a distilled delta to the bus (blackboard KS / sub-agent pattern).
6. curate-advances — the puppet appends distilled deltas and re-anchors; the new bus is the next stable prefix (still hit) — awareness compounds, puppet stays hidden.

## Build
- `mag/window_bus.py` (schema window_bus.v1) — deterministic $0: bus_segment / price_window_bus /
  member_view / curate. Composes with window_hop (hop pricing) + whisper_route + flock_field.
- Steal doc: memory/steal/WINDOW_BUS_20260810.md
