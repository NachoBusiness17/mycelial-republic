# STEAL — VerkleLance: invariant-rib-builder × verkle-knot × stateless-puppeteer TIE-IN (2026-08-11)

Operator: "you need to be able to lance like 20 different spots for reference within the verkle tree
and have swarms take those shapes and then spooky shit happens and its all lanced / k8's deep dive"
+ "it's the invariant rib builder / verkle knot stateless puppeteer tie in infrastructure."

## The vision (tie-in, not a standalone tool)
VerkleLance is the JOINT between three existing pillars:
1. **verkle_lance** — lances ~20 reference spots in the verkle tree (temporal spread or by theme),
   each lance = {index, session_id, theme, root, SHAPE (theme_vector_normalized)}.
2. **invariant_lattice** (invariant RIB builder) — invariant = RIB scene; steer_ollama / dispatch_to_k8s
   / render (cheapest capable). The lanced shapes become the SEED INVARIANTS (RIB scenes).
3. **partner_puppet** (stateless puppeteer) — any actor folds invariant knots; puppet(token, execute)
   triggers from the chain. Seats are stateless readers; state lives in the chain, never the process.

Flow: lance the tree -> shapes -> invariant RIB scenes -> builder renders/dispatches to the k8s swarm
(farm) -> puppeteer steers. The flock takes the lanced shapes as seed positions (swarm takes those
shapes), converges on the lanced landscape, folds back -> emergent ("spooky shit happens").

## Built (mag/verkle_lance.py additions, verkle_lance.v1, $0)
- lance(n, mode=spread|themes)     — n reference spots + their shapes across the tree.
- shapes(n)                        — seed bundle (positions + references) the flock pods consume.
- rib_builder(n)                   — lances -> invariant RIB scenes (the invariant builder input).
- puppet_trigger(n, execute=False) — lances -> puppet tokens for partner_puppet (read-only default).
- tie_in(n, probe=True)            — the JOINT: lances -> invariant_lattice -> partner_puppet; $0 probe.

## Verified (via OUR headless runner, ghostlance surface)
- ghostlance diagnose syntax_ok.
- lance 20 spread: 20 spots across 1009 knots (indices 0..~1000), each with shape.
- rib_builder 4: 4 invariant RIB scenes (verkle_lance:<theme>:<session>:<root>), deterministic.
- tie_in 4: joint wired, puppet_wired:true, steer_bundle produced; render_probe HONEST: ollama not up
  ("start the ollama container") — no fabricated render.

## Lessons / law
- The determinism (content hash + chain index) = the temporal map; lances are just reference points on it.
- Honesty: render_probe reports the real renderer state (ollama down), never fabricates a render.
- Registered as ghost_server RESOURCE memory/verkle (the tie-in surface).
