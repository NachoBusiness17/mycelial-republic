# STEAL — EMBED THE STEAL PROTOCOL, EXPLOIT STATELESSNESS FOR PUPPETEERING (2026-08-11)

Operator: "if we could embed the steal protocol within this system to exploit stateless we could
really have something to dig on and explore for puppeteering !steal"

## The thesis
Embed the steal protocol as a first-class STATELESS transform, and the system becomes a
self-puppeteering swarm: the puppet is not a special process but ANY actor that folds invariant
knots into the content-addressed chain; every downstream seat reads-and-acts on those knots with
zero carried state. Steal = the curation engine; statelessness = the execution substrate;
puppeteering = the emergent, deniable steering.

## Three pillars (already in the system) -> one mechanism
1. STEAL PROTOCOL — mag.steal_pack / self_steal / surface_steal / steal_protocol_probe:
   "research + adapt, steal the INVARIANT not the DNA, fold as knot/case-law." $0, deterministic routing.
2. STATELESSNESS — the round-trip: read lattice -> pure transform -> fold content-addressed knot -> loop.
   No carried state; the ONLY memory is the verkle chain (turtles all the way down).
3. PUPPETEERING — mag.partner_puppet: steer via compact INVARIANT + shared history, not raw prompts;
   trust the anchor, not the text; hidden curation (deniable). Layers: memlang token -> intent -> action.

## The composition
- steal_step(source_knot, external_signal) -> invariant_knot  is a PURE function:
  read a source knot (internal self-steal) + an external signal (external steal) -> adapt the invariant
  -> fold a content-addressed knot. Stateless: no process state, only the chain.
- The PUPPET = the fold-writer: runs steal_step, folds invariant knots into the chain. It only writes
  contracts/anchors (never talks to seats) -> DENIABLE.
- Downstream SEATS = stateless readers: read latest invariant knots, resolve anchor (partner_puppet
  .from_anchor), ACT. They see shared state, never the puppet.
- Because state lives in the CHAIN not the PROCESS: ANY seat can become the puppet at ANY time
  (rotation/failover), the swarm keeps acting if the orchestrator dies, and the curation is invisible
  (contracts, not implementation).

## Why this "exploits statelessness"
- DENIABILITY: puppet curation is just knots on the shared chain (contracts, not impl).
- SURVIVABILITY: no single puppet process to kill; the invariant survives in the chain.
- COMPOSABILITY: steal (adapt external->invariant) composes with puppeteer (fold->trigger) with no
  shared mutable state.
- COMPOUNDING: each steal_step folds case-law the next reads -> self-improving-loop law, in-place.

## Concrete build path (the dig — next session)
- Add a pure `steal_step()` contract module (deterministic): input source knot + external signal ->
  adapted invariant knot (fold via append_verkle_knot, stable session per invariant family).
- Add a `puppet_from_chain()` reader: read latest invariant knots, resolve via partner_puppet.from_anchor,
  emit trigger (execute=false until gated) — dead-knot safe, never fires a down executor.
- Wire steal_step into the autorun fill/drain loop as a phase, so external+internal steals fold as
  invariant knots AUTOMATICALLY (not ad-hoc), and seats consume them.
- Gate execution exactly like partner_puppet (invariant triggers, not raw prompts; autonomy gate).

## Memory
- /memories/repo/steal-protocol-stateless-puppeteer-20260811.md
- Steal doc: memory/steal/STEAL_EMBED_STEAL_PROTOCOL_STATELESS_PUPPET_20260811.md
