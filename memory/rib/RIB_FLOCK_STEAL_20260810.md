# RIB — flock_steal: invariant-aligned answer-cloud navigation
**RIB goal:** the mechanism that steals from a frontier WITHOUT talking to it directly.
Schema: rib.flock_steal.v1 · date 2026-08-10 · grounded + verified (dry run green).

## The operator directive (compressed)
"Use flock in steal… get stochastic data cheaply for stealing aligned to our verkle
invariants within their answer clouds, and navigate them using ghost without actually
having to talk to the frontier ai, by recreating them piecemeal."

## The mechanism (`mag/flock_steal.py`, schema flock_steal.v1)
Five stages, composing existing machinery (NOT rebuilt — flock-eliminated):
1. **ELIMINATE** — `steal_first` cache tiers + self-steal store (`steal_pack/filed.jsonl`).
   If we already hold it → `already_held`, $0. Never steal what we possess.
2. **PLAN** — `flock_field.define_distance_field(goal, invariants=centers, weights=radii)`.
   φ = distance-to-goal + CORE_INVARIANT penalties. The **answer-cloud overlap** = the
   near-goal region the invariants don't penalize. Deterministic (hash-seeded goal point).
3. **SAMPLE** — `riddler_transport.quick_riddler` surrogate variants (stochastic, N probes),
   cheapest-capable providers (ollama → deepseek), measured by ghost (flip/silence/emergent).
   Remote never sees the real problem — deniable, piecemeal.
4. **RECONCILE** — ghost checks every sampled mechanism against `CORE_INVARIANTS`
   (`consent_first, local_first, no_throne, residual_is_dna, window_steer`); flock gradient
   steers the next round to converge on the invariant-respecting mechanism.
5. **FOLD** — `steal_pack.file_steal` → verkle-anchored research pack + skill_ledger + lens.

## Alignment target (CORE_INVARIANTS, `mag/registry.py:29`)
consent_first · local_first · no_throne · residual_is_dna · window_steer
("Cold vertex invariants — amend may add, never remove.")

## Verified
Dry run (`python -m mag.flock_steal "<goal>" --dry`): eliminate no-hit → plan φ=0.0 →
sample dry → reconcile aligned_to 5/5. Compose green; sampling/folding are the live path.

## Why this is "frontier, without the frontier"
- **Deniable**: riddler surrogates — the remote reasons in a story domain; T0/T1 never leaves;
  the mapping key stays local. We never send the real ask.
- **Cheap**: eliminate-first ($0 when held), cheapest-capable providers, memlang-sized probes.
- **Recreated piecemeal**: cross-model consensus (`aggregate_responses`) reconstructs the
  mechanism from many small stochastic samples — the insight, assembled locally.
- **Aligned**: flock_field's invariant penalties keep every sampled/reconstructed mechanism
  inside the verkle invariant envelope.

## Ties
- Same thread as flock-eliminate-before-frontier (drop what we hold) + the steal doctrine
  (self+external both, adapt contracts not copy) + ghost-as-reconciler + memlang/weave core.
