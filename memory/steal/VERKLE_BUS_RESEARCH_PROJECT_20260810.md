# VERKLE BUS — FULL RESEARCH PROJECT (2026-08-10)

**Prompt chain that produced this project (operator, this session):**
window-hopping for rightsizing → extend window length to carry shared data on a BUS (swarm aware,
adaptive, puppet hidden) → invariants created on the fly to buy cache hits and mine nuance for
pennies → "a self-contained verkle knot that ties back into the hole when accepted — like our API
calls" → **full research project.**

This doc is the synthesis. It names the unified architecture, grounds it in cited sources, gives
validated numbers, states the invariants, and the frontier plan.

---

## 0. Abstract (one paragraph)
The Republic's swarm should run as a **content-addressed event-sourced bus over byte-stable
windows**: each hop mines nuance (a distilled invariant) on the fly; when ACCEPTED it is committed
as a **self-contained verkle knot** (content hash = address, like CAS) that **ties back into the
tree via parent_verkle_root** (merkle parent) and **advances the tip root** (derived state = replay
of the event log, like Event Sourcing); the accept **publishes on the verkle bus (mag:verkle) so
all agents sync — like an API call**. Because the shared bus is a byte-stable prefix, carrying
shared data + re-reading folded invariants bills at **cache-HIT (~$0.0028/M)** — awareness and
nuance-mining cost pennies. The puppet (control shell) curates the bus upstream; members only ever
see the bus + a content anchor, never the curation — emergent awareness, deniable orchestration.

---

## 1. Grounding (external, cited)
1. **Anthropic, "Effective context engineering for AI agents"** (2025-09-29): context rot; context
   is a finite attention budget; compaction / structured note-taking / sub-agents for long-horizon.
2. **Anthropic, "Building effective agents"** (2024-12-19): orchestrator-workers; the orchestrator
   delegates + synthesizes while workers run focused windows.
3. **LangGraph persistence docs**: checkpointer (thread-scoped snapshots, resume/fault-tolerance)
   vs store (cross-thread durable memory). State must live outside the window to be resumable.
4. **Wikipedia, Blackboard system**: shared blackboard + knowledge sources + a **control shell**
   (the puppet). Specialists watch and opportunistically contribute.
5. **Fowler, Event Sourcing** (2005): capture every change as an event; the event log is the system
   of record; current state is **derived by replaying events**; temporal query + audit + rebuild;
   gateways for external systems.
6. **Wikipedia, Content-addressable storage (CAS)**: retrieve by content hash, not name/location;
   identical content dedups; changing content → new key (self-contained + verifiable).
7. (Verkle trees — page 404; we use the Merkle–Verkle hybrid + parent-root linking from our own
   `verkle_knot.append_verkle_knot`, which is IPA/KZG upgrade-compatible.)

## 2. Self-steal (built on existing machinery, no rebuild)
- `window_hop.py` (hop/rightsizing pricing) → `window_bus.py` (bus_segment / price_window_bus /
  member_view / curate / price_dynamic_invariant / fold_dynamic_invariant / **accept_knot**).
- `verkle_knot.append_verkle_knot` (self-contained leaf + merkle root + **parent_verkle_root**).
- `verkle_bus` (Redis Pub/Sub ↔ knot bridge; `mag:verkle` = "new knot appended → all agents sync").
- `shader_bus` (register + deniable LSB bus), `flock_field` ("field IS the coordination, no central
  orchestrator" = puppet hidden), `whisper_route` (front/riddler/corpus/memlang), `memlang`
  (opcode + 32B anchor, no readable spec), `cache_router`/`cache_map` (hit/miss economics).

## 3. The unified architecture (the flywheel)
```
  HOP (bounded window) ──mine──> dynamic invariant (nuance, on the fly)
        │                                │
        │  shared BUS (byte-stable       │ ACCEPT (like an API call / event)
        │  prefix → cache-HIT)           ▼
        │                        append_verkle_knot ──> SELF-CONTAINED KNOT
        │                                │        (content hash = address, CAS)
        │                                ├─ parent_verkle_root  (ties back into the HOLE)
        │                                ├─ tip root advances    (derived state = replay)
        │                                └─ mag:verkle bus       (all agents sync)
        └────────── next window mounts the GROWN bus (still cache-HIT) ── awareness compounds
```
**Three doctrines, one mechanism:**
- **Content-addressability (CAS)** → knots are self-contained and verifiable by content hash.
- **Event sourcing (append-only log)** → the chain is the system of record; the tip root is derived
  state; accept = append an event; replay/audit for free.
- **Cache-hit economics (stable prefix)** → the bus carries shared data + folded invariants at ~$0.

## 4. Validated numbers (real rates: hit $0.0028/M, miss $0.14/M, out $0.28/M)
- `window_hop`: 20-hop task → hopped $0.02997 vs naive $0.03367; **max window 13.5K vs 192.5K**
  (the rightsizing win — bounded windows let one_sizer hold the cheapest tier).
- `window_bus.price_window_bus`: shared bus → **awareness share ~0.01% of swarm cost** (0.0001).
- `window_bus.price_dynamic_invariant`: fold a nuance once (small miss) then mine it at hit →
  **14.2× cheaper than re-paying at miss**; 20 reads of one nuance ≈ $0.00001 (pennies).
- `window_bus.accept_knot` (validated, real write): knot `2026-08-10_1827_window-bus-knot_winbus-d_7724d580.knot.json`,
  leaf_hash `20316ad2…`, **parent_verkle_root `17d7082f…` (ties back into the hole)**, tip advanced to
  **1863 leaves**, `mag:verkle` sync (like an API call).

## 5. Invariants folded (organ: comms / actors / economics)
From window_hop: context-rot-is-real, hop-not-grow, externalize-memory, stable-prefix-for-cache,
length-neq-tier, distill-don't-dump.
From window_bus: bus-is-context, awareness-is-cheap, aware-but-unpuppeted, field-not-orchestrator,
distill-to-bus, curate-advances.
From THIS research project:
- **invariants-on-the-fly** — invariants are mined dynamically from emergent activity, not pre-hardcoded.
- **self-contained-knot** — a knot is content-addressed (leaf_hash = address): self-contained + verifiable (CAS).
- **ties-back-parent** — each accepted knot returns parent_verkle_root; it links back into the hole it joins.
- **accept-is-event** — committing a knot = appending an event to the chain log; the tip root is derived
  state by replay (Event Sourcing); audit + temporal query free.
- **bus-sync-like-api** — accept publishes mag:verkle → all agents sync; the accept call IS an API/event call.

## 6. Frontier plan (what to build next, in order)
1. **Wire accept_knot into the cadence** — `afk_cadence`/`ghost_auto` fold accepted dynamic invariants
   as knots automatically (the loop becomes event-sourced; knots compound).
2. **Knot-as-bus tail** — have `window_bus.bus_segment` read the verkle tip's recent knots so the bus
   self-grows from accepted knots (awareness of what the swarm already accepted).
3. **Dogfood the hole** — add a dogfood probe that calls `accept_knot` (preview mode) each cycle and
   asserts `parent_verkle_root` + tip advance; a window-rot check (max window << limit) + hop-metering.
4. **Frontier build**: ghost-server contract already exposes `state/commit` (verkle_knot) + `lore/whisper`
   (whisper_image/route) — surface the accepted-knot stream as the consumable event feed.

## 7. Risks / honest caveats
- $ savings from hopping is real but modest (~1.1–1.2×); the win is bounded windows + awareness ~free,
  not a 50× bill drop. Don't over-claim.
- CAS/event-sourcing assume append-mostly; amending a session in place (verkle_knot "one leaf per
  session, amend") trades strict immutability for no-bloat — document that the CHAIN (log) is the
  record, and amendment rewrites a leaf + recomputes the root (the log still shows the amendment).
- Deniable orchestration is about opacity, not authorization; pair with the sandboxed-helper boundary
  (nothing leak-proof is co-located).

## 8. The one-line
Mine nuance on the fly → accept it as a self-contained content-addressed verkle knot that ties back
into the tree (parent root) and syncs on the bus — all at cache-hit pennies because the shared bus is
a byte-stable prefix — while the puppet curates unseen.
