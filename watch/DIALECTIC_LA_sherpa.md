# SHERPA THESIS — the wall is rank, not brightness
DIALECTIC Phase 1 (blind) — 2026-09-04 — lens: linear algebra — seat: SHERPA

## CENTRAL CLAIM
The fleet's ceiling is not the size of its compute vectors but the RANK of its
basis. Every capability gap the fleet hit this week is a rank deficiency — the
target lay OUTSIDE the span of the operator's basis — and every fix that
actually worked (the light field, MCP senses, the accumulator) was a rank
extension: adding an independent direction, not scaling an existing one.
Compute scales coefficients. Only new independent directions buy new problems.
Therefore: decompose before moving, and if a problem does not decompose into
the fleet's basis, the correct move is to add a basis vector — never to push
harder along a lane that has no component toward the target.

## THE CLAIM DECOMPOSED (tri-state)
1. SUPPORTED — The light replay is a null-space measurement, not a brightness
   measurement. 100/100 lit vs 0/100 unlit at p=1.04e-45 means: the object the
   dumb agent is asked to find lies in the null space of its unlit operator —
   no coefficient on ANY of its existing directions reaches it. The light field
   adds one dimension; the target enters the span; acquisition becomes possible.
   The light is a basis extension, and the p-value measures singularity.
2. SUPPORTED — Symbol-as-command is exactly "the same basis vector, different
   matrix." A symbol is a coordinate direction; the machine binds it to an
   operator. An operator without a constraint is a catastrophe because an
   unconstrained matrix can map your state anywhere — including out of span.
   The ground wire (7th primitive) is the constraint that keeps compositions
   inside the renderable subspace. Order matters because matrix products do
   not commute: BUILD_BEFORE_PRETTY is non-commutativity stated as law.
3. UNPROVEN — The 7 primitives are a BASIS, not an overcomplete frame. Nobody
   has shown they are independent: if, say, DISSIPATE = composition of
   EMIT + GROUND, the algebra's true rank is 6 and one primitive is redundant
   vocabulary. Rank 7 vs rank 6 changes what the algebra can express — an
   overcomplete frame spans the same space with fewer guarantees of unique
   decomposition (and unique decomposition is what a route-maker needs to
   freeze a problem statement).
4. UNPROVEN — The MAG chord's lanes are linearly independent. A persona is a
   rotation of the same vector, not a new dimension. The chord adds information
   only if lane errors are uncorrelated; if all lanes' errors are one direction,
   the chord is rank-1 regardless of lane count.
5. DISPUTED — LAW 13 ("concurrency past 50 = more keys, horizontal") is
   coefficient scaling sold as structure. Horizontal keys multiply THROUGHPUT
   along the one axis "same-provider-lane"; they cannot rescue a rank-deficient
   decomposition, and per-key policy walls are exactly the symptom of moving
   along one direction until the wall. The law is fine as economics; as
   structure it should read "more keys AND a new lane type" when the wall is
   policy-shaped.

## THE MAP OF KNOWNS/UNKNOWNS (frozen problem statements, my trade)
- KNOWN-SPACE = span(fleet basis). Rank deficiency = the unowned department.
- NULL SPACE = the shadow: what each operator annihilates. The unlit maze
  before the light; what the accumulator's projection discards; what the
  frozen schema makes unrepresentable. Shadow work = computing your own null
  space — and it is computable, this week, not poetry.
- UNKNOWN-UNKNOWNS = everything orthogonal to basis AND null space that we
  cannot yet name — the honest frontier. My map admits a third region: the
  span is finite; the ambient space is not.

## MEASURABLE FALSIFIER (primary)
Take the N fleet lanes and run a fixed 20-task battery; build error matrix E
(lanes x tasks, graded errors). If rank(E) <= 2 for N >= 4 — or mean pairwise
error correlation > 0.8 — the chord is dependent, claim 4 dies, and
"diversity" must be redefined as persona rotation. Secondary falsifier: the
primitive closure test — attempt to implement each of the 7 primitives as a
composition of the other 6; any success drops the algebra to rank 6 and kills
claim 3. Both are runnable this week from existing receipts and scripts.

## MY BLIND SPOT (named now, for the critique phase)
I cannot see DYNAMICS. Independence is a static snapshot: lanes that are
independent at decomposition time become coupled later through shared
infrastructure (one provider's congestion couples all its lanes; the
accumulator's own writes couple the state's dimensions). The linear lens also
prices the calibration catastrophe as noise — one wild leaf poisoning alpha-beta
cutoffs is a nonlinear threshold effect, invisible to a span/basis/rank view
that only sees averages. If the fleet's real failure mode is temporal coupling
or threshold poisoning, my frozen problem statements are pictures of a fleet
that no longer exists.

## ROUTE IMPLICATION (what changes Monday)
Before any build: write the problem as a coordinate vector in the current
basis. If it has a component outside the span, the build is a basis extension
(new lane type, new primitive, new sense) and gets first priority — coefficient
work on in-span problems can wait. Rank before magnitude. Decompose, then move.
