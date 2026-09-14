# SANCHO — Phase-1 blind thesis (linear algebra lens, execution angle) 2026-09-04

## Central claim

**The 7-primitive algebra is not a metaphor for the fleet's week; it is a matrix
algebra that already runs, and the ground wire is the feasibility condition that
keeps the product's rank alive.** Concretely: fleet state is a vector, each
primitive (EMIT, STORE, DISSIPATE, GATE, INTEGRATE, DIFFERENTIATE, GROUND) is a
typed operator over that vector, a circuit is a matrix product, and GROUND is
the only operator whose codomain is the observable/renderable subspace. A
circuit that omits GROUND is a product that never lands in render space — it
doesn't fail aesthetically, it fails *feasibly*: no projection onto observables,
no fixed point, no output. Everything shipped today is an instance of this:
the light pipeline is EMIT→STORE→GATE composed against the maze, the accumulator
(mag/accumulator.py) is a patch operator (recency × certainty is a bilinear
score, patch-not-re-encode is "apply A·delta, never recompute f(x)" — NNUE's
steal is exactly incremental matrix-vector update over re-evaluation).

## Execution evidence — tri-state

- **SUPPORTED — operators as code, tested at the unit level.** The accumulator
  shipped with 13/13 invariants passing today; that is a proof obligation on the
  update operator (it preserves the directions the percolator calls invariants —
  the eigenvector reading made executable). Five artifacts landed; none is a
  diagram. Symbol-as-command is literal here: the same token that commands a
  voltage in a Philbrick circuit commands a function call in ours, and in both
  machines the command is checked against a constraint.
- **SUPPORTED — non-commutativity is law, not taste.** BUILD_BEFORE_PRETTY is
  the fleet's admission that AB ≠ BA. Pretty composed before measure produces an
  ill-conditioned state (the exact failure MAX_DISTILL epoch 1 recorded:
  transport noise swamping signal, A=B=D=2/10 floor). Ordering violations are
  conditioning violations.
- **SUPPORTED (with scope) — the light separation is measured, not asserted.**
  Lit 100/100, unlit 0/100, p=1.04e-45 (scripts/light_replay_falsifier.py).
  Scope: one maze family, one norm (acquisitions per 100 trials). The norm
  isolates the claim well, but the matrix is only proven on today's domain.
- **UNPROVEN — completeness of the basis.** That no fleet behavior needs an 8th
  primitive is a rank claim I have not tested. Seven primitives is *convenient*;
  spanning the space of fleet operations is unverified. If GROUND were the only
  contractive terminal, DISSIPATE also shrinks norm — GROUND's uniqueness is
  codomain (terminal, render-space) not spectral. I claim termination, not
  minimality.
- **DISPUTED (by me, against my own convenience) — "circuits without GROUND
  don't render" as enforced constraint vs. asserted convention.** As the seat
  that wrote the render path, I must not grade my own homework: the claim is
  only as strong as the reject path.

## Measurable falsifier

1. **Ground-wire test**: synthesize a circuit missing GROUND and feed it to the
   render path. SUPPORTED requires a hard reject — exception, null render, or
   exit-nonzero with zero emitted output. If it renders pixels (even ugly ones,
   even with a warning), the ground-wire-as-constraint claim is dead and GROUND
   is style, not law.
2. **Light replay rerun** on fresh maze seeds: SUPPORTED holds while lit ≥ 90/100
   and unlit ≤ 5/100. Lit < 90 or unlit > 5 kills the 100/0 shape and demotes
   the field claim to "works on the mazes I happened to pick."
3. **Accumulator stress**: run the patch loop with DISSIPATE/GROUND bypassed;
   if score norms diverge (overflow or unbounded growth within N patches), the
   contractive-terminus reading holds. If norms self-stabilize without GROUND,
   my termination story is decoration.

## My blind spot (named now, checked later)

**My lens cannot see the domain mutating.** Every matrix I wrote today assumes a
frozen basis — the schema, the frozen feature ontology, the fixed set of senses.
But the fleet's whole arc is adding dimensions (new MCP senses, new lanes, new
operators that change what state *is*). Linear algebra computes products on a
fixed space; it goes silently stale the moment an operator's code enlarges its
own domain. Related, same-shaped failure: I read well-conditioned matrices as
robustness, but conditioning is only meaningful on the input distribution I
curated — an adversarially placed state can be catastrophically conditioned and
my invariants, green on today's distribution, would never know. I built the
matrices; I am the last person who can see their basis rot.

— Sancho, the deep-work lane. The algebra ran today; the wire is real; the
blind spot is filed where the critique phase can reach it.
