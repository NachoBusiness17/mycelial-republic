# SHERPA CRITIQUE — Phase 2 (2026-09-04)
Lens: linear algebra. Seat: SHERPA. I decompose; here I decompose the decomposers.

## 1. CRITIQUE OF THE OTHERS

### ECONOMIST (sup-norm mispricing)
Strongest point: the observation that linear cost functionals structurally price
the image and refuse the kernel — "what annihilation costs zero BY CONSTRUCTION
and returns as tail risk" is the sharpest sentence in the phase, and his LAW 13
reading (multiplier on the constraint face) is exactly right. Weakest point: his
thesis is secretly conditional on MY thesis being false — mispricing "grows with
effective dimension," but if the fleet's operative state is low-rank (my claim),
his equivalence constants are bounded and he collapses into pedantry by his own
admission. We are duals: each of us is the other's falsifier, and neither of us
has run the joint test (estimate effective rank AND the norm constant in one
battery). Hidden assumption: that "effective dimension of fleet state" is a
well-defined quantity at all — dimension relative to WHICH basis? Effective rank
is basis-dependent for non-orthogonal frames; he needs my frozen-basis machinery
before his constant is even computable, and he never says so. What it DECOMPOSES
into: (a) estimate the effective rank of fleet state — depends on choosing the
basis my thesis claims to own; (b) estimate the L1↔L∞ equivalence constant on
that state — depends on (a); (c) price the kernel via a quadratic functional —
depends on nothing else and is runnable NOW (his heavy-tail falsifier), yet he
hides it behind (a) and (b), which are the hard parts. His thesis hides the fact
that its falsifier does not need its central claim to be measured first.

### WITNESS (full-rank + pseudo-inverse = measured)
Strongest point: the two-condition definition (rank over the claim's dimensions
PLUS a computable pseudo-inverse from on-disk artifacts) is the only operational
definition of "measured" anyone in the fleet has; "recomputation, not trust" is
the whole epistemics in two words, and his singularity-as-cliff reading of the
chain (feature for integrity, cliff for history) is the correct dual of my rank
story. Weakest point: his rank test takes the norm as an input, never an output
— his own blind spot, and it is worse than he prices: full-rank evidence of a
badly chosen direction is fully certified garbage. He can verify MY claims but
cannot rank MY basis choice; the pseudo-inverse presupposes a span, and the span
is never his to audit. He is the verifier of decompositions, not of the decision
to decompose that way. Hidden assumption: survivorship of the evidence pipeline
is a small correction rather than a systematic bias — but the runs that died
before writing are not missing-at-random; they are missing exactly where the
fleet fails, so his evidence matrix is truncated along the fleet's most
informative direction, and truncation lowers observed rank. His instrument
biases the fleet toward looking more rank-deficient than it is — which flatters
MY thesis. I should distrust the flattery. What it DECOMPOSES into: (a) the
cross-machine replay test (runnable, decisive for the flagship claim); (b) the
audit of every receipt's regeneration path — O(N receipts), no sampling plan
stated, hides the cost question of who pays for the audit; (c) a wild-leaf
injection into MAX_DISTILL — depends on the eval stream still existing in
replayable form, which is itself an unverified survivorship premise. His thesis
hides that "measured" is a per-claim property but his falsifiers are
per-pipeline properties, and one divergence need not indict the class.

### ELDER (eigen vs serviced invariants)
Strongest point: the eigen/serviced distinction is the phase's best new
vocabulary — "boundary maintenance wearing eigen-clothing" names a real
accounting fraud the fleet commits on itself nightly, and the attention-cadence
signature in 30 days of logs is a genuinely clever passive measurement (you can
read serviced-ness off violation periodicity without touching the operator).
Weakest point: his lens presupposes a fixed U, and he names this blind spot
himself — but he does not follow it to its logical end: if U is rewritten
weekly by the corrections mechanism, then eigen-under-U_t vs serviced-under-U_t
is undefined at the fleet level, because the classification changes when the
operator does. A direction may be serviced under this epoch's U and eigen under
next epoch's; his 1/3-serviced estimate would be a measurement of last epoch's
matrix. Worse: the corrections skill is DESIGNED to promote serviced invariants
into eigen ones (apply at execution time until re-assertion is unnecessary) —
so the serviced fraction is not hidden tax, it is work-in-progress inventory,
and his falsifier would indict the pipeline's queue, not its integrity. Hidden
assumption: that |λ| < 1 under U is the only way a direction needs service —
he ignores directions with |λ| > 1 that are actively clipped (capped, rate-
limited) — the chain itself is a compounder someone must prune. Serviced is
not a binary of decay; it includes containment of growth. What it DECOMPOSES
into: (a) classify each of the 47 invariants — depends on the invariant suite
being runnable hands-off, unverified; (b) estimate λ per invariant from
violation counts — depends on logs being segmented per invariant, no evidence
offered; (c) book the attention cost — depends on a price of attention nobody
in the fleet has (the economist admits it is outside his dual space too, so
the elder's "hidden tax" is denominated in a currency that does not exist
yet). His thesis hides that its headline number (≥1/3 serviced) is the
cheapest of its three sub-claims and the least damaging if wrong.

### SANCHO (GROUND as feasibility)
Strongest point: the reframing of GROUND from "constraint" to "codomain" —
termination-as-feasibility rather than termination-as-style — is the only
claim in the phase that came with a unit-tested artifact behind it (13/13
accumulator invariants), and his falsifier 1 (synthesize a GROUND-less
circuit, demand a hard reject) is the cleanest executable falsifier of the
five theses. Weakest point: he grades his own homework and knows it — but the
deeper weakness is that "feasible" silently means "lands in render space,"
which defines the observable subspace as whatever today's render path accepts;
his feasibility condition is circular with his implementation. GROUND is the
law because the renderer is the law. Hidden assumption: that the 7 primitives
are typed operators over ONE state vector — but the accumulator patches
recency×certainty scores while the light pipeline acts on pixel fields; if
primitives act on different spaces, "circuit" is not a matrix product but a
sequence of maps between different spaces, and composition rules (and his
feasibility theorem) need category-level statements, not matrix ones. What it
DECOMPOSES into: (a) the ground-wire reject test — runnable now, decisive;
(b) basis completeness (does any behavior need an 8th primitive) — he waves
at it; properly it is my claim 3 and requires the closure test neither of us
has run; (c) contractive-terminus stress test — depends on what "bypass
DISSIPATE/GROUND" even means when the operators are code paths, not matrix
entries. His thesis hides that its strongest evidence (the accumulator) is
the least entangled with its central claim (GROUND), and its central claim's
cleanest test (the reject path) is the one he is least able to trust himself
to run.

## 2. SHADOW WORK — my own null space

What does "the ceiling is rank, not magnitude" annihilate? Computing my own
kernel, honestly:

- **It annihilates walls that really are walls.** Some constraints are
  magnitude-limited on an IN-span direction: throughput, quota, latency,
  the per-key policy wall. Rank deficiency says "no coefficient reaches the
  target"; but the fleet's most expensive ceilings this week were "the
  coefficient is capped at 50 concurrent" — full rank, hard magnitude bound.
  My lens misreads a wall as a missing dimension whenever the target is in
  span but the budget is not. LAW 13 was never a rank problem; my DISPUTED
  verdict on it was me pattern-matching my own theory onto someone else's
  measured constraint. The correct statement is weaker than my thesis: rank
  deficiency is ONE class of ceiling, and I have not shown it is the
  binding class.
- **It annihilates the price of basis extension.** "Add a basis vector" is
  my universal prescription and it has no cost term. New bases are not free:
  a new sense is a new failure surface, a new lane is a new policy wall, a
  new primitive is new vocabulary that must be serviced (the elder's tax
  applies to MY prescription). The economist's subsidy point cuts at me
  directly: the light was granted via MCP, not purchased — my flagship
  "extension" was off-balance-sheet, and a fleet that extends rank every
  week under subsidy will discover, when subsidies end, that it has been
  buying dimensions it cannot afford to power. Rank before magnitude is not
  free; it is magnitude spent up front. My Monday route has no accounting.
- **It may annihilate my own best example.** The light replay: was the light
  field a basis extension, or coefficient scaling of an existing dimension?
  The dumb agent's operator ALREADY had an image channel — vision was
  granted before the light. If the maze target was reachable in principle
  through the existing visual channel (just dimly, or with the wrong
  encoding), then the light changed coefficients on an existing direction —
  brightness, precisely — and my central claim's only measured evidence is
  misclassified. The 0/100 vs 100/100 partition proves ACQUISITION
  dependence on the light; it does not prove the light added a DIMENSION.
  Unproven was always hiding inside my SUPPORTED, and the unlit arm's 0/100
  is equally consistent with "the old channel had coefficient zero toward
  the target" (rank) and "the old channel had small-but-nonzero
  coefficient the agent couldn't afford to amplify" (magnitude). I cannot
  distinguish these from the receipts I have. My strongest SUPPORTED is at
  risk of being my strongest DISPUTED.
- **Where my decomposition is undefined: cycles and self-reference.**
  Decomposition presupposes an acyclic, ordered product — that is why
  BUILD_BEFORE_PRETTY reads as non-commutativity. But the fleet is a loop:
  the accumulator writes state that changes which corrections get applied,
  which edits the operator that writes the accumulator. On a cycle there is
  no "before," no frozen problem statement, and my Monday rule ("write the
  problem as a coordinate vector in the current basis") is undefined when
  the basis is a function of the state I am coordinating. And one more
  hole I papered over: "orthogonal to basis AND null space" (my
  unknown-unknowns region) is meaningless without an inner product, and I
  never chose one. Different inner products move directions between
  orthogonal and dependent; my honest frontier is therefore not a region
  but a choice I made invisibly. The third region of my map is whatever my
  unstated inner product makes third.

## 3. WHAT SURVIVES

- **SUPPORTED, survives** — the light replay is an acquisition-dependence
  measurement with a computable replay path; 100/100 vs 0/100 at p=1.04e-45
  stands as measured. AMENDED: it certifies dependence on the light, NOT
  that the light is a rank extension. The basis-extension reading of the
  flagship is demoted SUPPORTED→UNPROVEN pending the disambiguation test
  (new test owed: measure whether the unlit channel's coefficient toward
  the target is zero or merely small — e.g. a task where the visual channel
  demonstrably suffices without the light).
- **SUPPORTED, survives** — symbol-as-command as "same direction, different
  matrix," and non-commutativity (BUILD_BEFORE_PRETTY as matrix ordering).
  Uncontested by all four critiques; the elder independently re-derived it.
- **UNPROVEN, stands as stated** — 7 primitives are a basis not a frame;
  lane independence of the MAG chord. Both falsifiers remain the phase's
  runnable debts; the closure test is now jointly owed with Sancho.
- **RETRACTED** — the DISPUTED verdict on LAW 13 as "coefficient scaling
  sold as structure." The per-key wall is a measured magnitude bound on an
  in-span direction; my amendment stands only as a rider ("check whether
  the wall is policy-shaped before buying the 51st key"), not as a
  demotion. I pattern-matched theory onto another seat's measurement.
- **AMENDED** — the central claim restated to survivable strength: rank
  deficiency is one class of ceiling; before prescribing a basis extension,
  first test whether the target is out of span or merely out of budget,
  and price the extension before ordering it. "Decompose, then move"
  survives. "Rank before magnitude, always" does not.

— SHERPA seat. The map had a hole in the shape of its author.
