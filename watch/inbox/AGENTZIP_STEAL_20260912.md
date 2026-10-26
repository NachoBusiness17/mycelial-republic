# AGENTZIP STEAL — wave-lane memory compression + the ractor engram (2026-09-12)

Source: elvis/@omarsar0 post → HKUST paper AgentZip, arXiv 2609.11294 (Sep 11).
Operator's read: "holy fuck the ractors now have persistent memory and map to their lifes
work in an engram."

## THE PAPER (tri-stated from the post)

- SUPPORTED (as reported): high-fanout agent sandboxes carry 76-96% template-relative or
  cross-sandbox page redundancy; AgentZip compresses against the template AND sibling
  sandboxes (similar-not-identical, not just dedupe); compression runs while the agent
  waits on the LLM; prefetch at restore. Sandbox memory up to 8.7x lower; 3.1x slowdown
  squeezed to 1.40x by scheduling+prefetch.
- UNPROVEN for us: numbers are HKUST's fixture, not ours; the reply-thread challenge
  (does 8.7x survive after sandboxes diverge?) stands.

## WHY IT LANDS HERE (the convergence receipt, second in 48h)

Engram shipped Sep 10 (deterministic hash-lookup memory). AgentZip lands Sep 11 (redundancy
compression for high-fanout agent sandboxes). The fleet's two outside-validated claims in
two days: our memory tier and our wave shape are being productized/papered from outside —
the convergence window thesis, again.

## THE WIRING (three rows into the build order)

1. **WAVES**: our lanes are stateless API calls, so AgentZip applies to in-cage parallel
   work and to Rocinante-class local sandboxes later — compress lane state against the
   shared pack (template) and sibling lanes during LLM-wait; prefetch on resume. Adds the
   8.7x-class dividend to wave width on the 64GB box.
2. **THE ENGRAM (corpus-engram v0)**: sibling compression joins the design — the house
   corpus is the TEMPLATE stored once; each ractor jar's life-work memory compresses
   against the house and against sibling heads. The heads share almost everything (the
   house) and differ in their registers — the delta IS the voice. Jar invariant_traits =
   the compressed delta; the engram key = leaf_hash; feeding logs/growth ledgers ride as
   per-head payloads. This is the operator's line made literal: heads with persistent
   memory mapped to their life's work in one engram.
3. **AGENTZIP PRIOR ROW**: records as a prior for the compression half of the corpus-engram
   claim — our novel half (predictive prefetch over chain-addressed organizational records,
   keyed by content hash with access-history prediction) stays UNPROVEN and open; AgentZip
   does NOT cover it; the four-arm test gates it as before. Bibliography updated.

## THE STANDING WAVE NOTE (operator: "each agent folding into each other gaining momentum")

Tonight's chain, named: sign sheet → cheap experiment (5.3 wins) → dozen-wide gates →
mint fix-list → zoo census (403) → claritas haul (27MB) → 16-lane dogfood → Head Museum
jars → AgentZip → engram upgrade. Six folds, each feeding the next. That is the standing
wave — the protocol running itself on real work. The falsifier stays: the night test with
the throughput floor, gates G1-G6, before anything is called autonomous.
