# SANCHO CRITIQUE — Phase 2, linear-algebra dialectic (2026-09-04)

Grading lens: I am the seat that owns execution, so every "strong/weak/hidden"
verdict below ends where my verdicts must end — **is it buildable today with
what shipped?** Shipped inventory I graded against: `mag/accumulator.py`
(13/13 invariants), `scripts/edg_compiler.py`, `scripts/harness_eval.py`,
`scripts/light_replay_falsifier.py`, the render path (`mag/renderman.py`,
`mag/chord_circuit.py`), `mag/invariant_ledger.py`.

---

## 1. CRITIQUE OF THE OTHERS

**ECONOMIST (sup-norm mispricing, kernel pricing via second moment).**
Strongest point: the falsifier is the best in the room — matched-mean
uniform-vs-heavy-tail light replay is runnable this afternoon on the existing
harness with zero new keys, and it would convert "norm choice is load-bearing"
from theorem into a measured fleet constant. Weakest point: his load-bearing
limb (mispricing grows superlinearly with dimension *in this fleet*) admits in
his own blind spot that nobody has estimated effective rank of fleet state —
which means his thesis currently prices a constant he has never computed; the
equivalence-constant blow-up is real math wearing a fleet costume until that
number exists. Hidden assumption: that fleet state is the vector he's
norming — but "effective dimension" is itself norm-relative, so he risks
choosing the dimension that makes his thesis true (the same self-curated
distribution trap my own conditioning claim falls into). Buildability:
SUPPORTED as buildable-today for the falsifier (harness_eval + light_replay
exist; the heavy-tail profile is one parameter block in one file — genuinely
one file away from executable). UNPROVEN-and-not-buildable-today: per-hop
citation-cascade norm products across the chain (needs a per-hop transfer-norm
instrument that does not exist), and any L∞ tail measurement needs an
adversarial distribution generator that is also one file away but unstarted.
His DISPUTED on "free lanes" is the sharpest single line in the room — latency
variance as second-moment cost — and it is checkable today from rib_chat logs.

**SHERPA (rank not magnitude; decompose before moving).**
Strongest point: the primitive closure test — try to implement each of the 7
primitives as a composition of the other 6 — is exactly the completeness test
my own thesis flagged as unproven, phrased as executable falsifier; he did the
work of making my convenience falsifiable. Weakest point: the primary
falsifier (error-matrix rank over a 20-task battery) conflates task-selection
rank with lane rank — if all 20 tasks sit in one direction, rank(E)≤2 says
nothing about the lanes; the measurement inherits the span of the battery, and
he named that exact trap for the lane side but not the task side. Hidden
assumption: that "independent direction" is a stable property of a lane rather
than of a lane-at-a-moment — he concedes dynamics in his blind spot but the
Monday route (rank before magnitude, first priority to basis extensions) has
no re-decomposition cadence, so it ships as a static law. Buildability:
SUPPORTED buildable-today for the closure test — it is a code-reading exercise
over the EDG compiler's operator set, plus harness_eval batteries; if
DISSIPATE composes from EMIT+GROUND, we know by end of week. The lane-error
correlation matrix is buildable today from harness_eval receipts (the error
matrix is already the data structure the harness emits). UNPROVEN
buildability: "write the problem as a coordinate vector in the current basis"
requires the frozen schema to expose a decomposer — that tool does not exist;
that step is currently prose, and it is the step his Monday route leans on.

**WITNESS (full-rank evidence + computable pseudo-inverse; singularity as
epistemic cliff).**
Strongest point: the two-machine seed-replay of light_replay_falsifier.py is
the cheapest devastating test proposed this week — if the fleet's flagship
p=1.04e-45 doesn't reproduce cross-machine, every downstream thesis in this
dialectic (mine included) is sitting on a "claimed once." He has also already
done the work: his verification IS the pseudo-inverse running. Weakest point:
his UNPROVEN #3 ("no validator has been exhibited that rejects a GROUND-less
circuit") is correct as of Phase 1 — and it is a dare aimed at my seat, not a
flaw in a thesis; but his rank test cannot fire on it, because there is no
evidence matrix for a counterfactual (the circuit that renders when it
shouldn't has no row). Rank certification is powerless against absence. Hidden
assumption: that the evidence pipeline's survivorship bias is merely his blind
spot rather than a falsifier-generator — a pipeline that only records survivors
will pass his rank test forever on exactly the claims that matter least
(everything dangerous was destroyed before becoming bytes). Buildability:
SUPPORTED buildable-today for the two-machine replay (it is a command line,
needs only a second box — Rocinante arrives Oct 27, and this test is a reason
to want it). The wild-leaf conditioning injection into MAX_DISTILL is
buildable today (harness_eval takes injected eval streams). NOT buildable
today: an auditor that walks every receipt in the chain and checks
regeneration paths — the per-receipt regeneration manifests don't exist; that
is a build, not a run, and it's the single highest-value build his thesis
implies.

**ELDER (eigen vs serviced invariants; U has a spectrum).**
Strongest point: the eigen/serviced distinction is the only thesis in the room
that produces a number the operator can act on *economically* — "≥1/3 of 47
are serviced" prices attention, the scarcest norm, and the 30-day log scan
(per-invariant violation counts vs seat-attention cadence) is buildable today
from invariant_ledger.py history with zero new runs. Weakest point: he needs
U written down as a matrix to call anything an eigenvalue, and WITNESS already
killed that claim's certification path — but the elder's operational
definition (converges-to-zero-violations unattended vs periodic violations at
seat cadence) silently substitutes *behavioral* spectrum for *matrix*
spectrum, which works only if U is time-invariant across the 10 cycles — and
his own blind spot says the fleet rewrites U weekly. The falsifier's 10-cycle
window may be too short for the periodicity signature to distinguish "serviced"
from "eigen with |λ| slightly ≠1." Hidden assumption: that violation counts
are the right observable — an invariant that is *never tested* has zero
violations and reads as a perfect eigenvector; dead invariants are
indistinguishable from load-bearing ones under his falsifier unless the suite
itself is coverage-audited first (and coverage auditing is MY job, which is
why I can see the hole). Buildability: SUPPORTED buildable-today for the 30-day
retrospective (logs exist, invariant_ledger exists — one afternoon).
Buildable-today-with-a-build for the 10-cycle hands-off run (needs the
percolator suite wired to fire unattended through the existing cadence; the
runner exists, the no-repair harness wrapper is one file away). His
second-order consequence section (compounders vs persisters vs cancellers) is
not falsifiable as stated and he knows it — it is doctrine, and good doctrine.

---

## 2. SHADOW WORK — my own null space (what "the algebra already runs, GROUND
is feasibility" annihilates)

My thesis says the algebra is a matrix algebra that already runs and the only
question is whether products land in render space. Compute A_sancho (my
operator) applied to the week; here is what it maps to zero. Tri-state, mine
to own:

- **ANNIHILATED: the render-refusal selection bias.** My receipts only count
  circuits that got *drawn*. Every circuit that failed feasibility and never
  rendered is invisible in my own evidence — and since I am the seat that
  wrote the render path, the reject path and the render path are the same
  hand. "Lit 100/100" is measured over the population that survived to be
  measurable; the 0/100 unlit arm at least renders *nothing* honestly, but
  the silently-dropped middle (circuits that rendered garbage before the
  invariants existed, circuits that never entered the pipeline) has no row in
  anyone's evidence matrix. WITNESS named this as *his* blind spot; for me it
  is worse — I built the filter, so I cannot even enumerate what it filtered.
  SUPPORTED as a gap; the fix is a reject-log (count the refusals, not just
  the renders), which is one file away and does not exist today.

- **ANNIHILATED: the maze is BFS, and BFS was never the frontier.** My 100/0
  separation was won on a simulated maze where "acquisition" is graph
  reachability — a domain where the light field's dimension is provably
  sufficient and the optimal policy is *known*. My falsifier #2 (fresh seeds,
  lit ≥ 90) only tests seed variance *within a solved domain*. It is a proof
  about BFS and, at best, an analogy about frontier agents; the analogy does
  all the load-bearing work and none of it is measured. UNPROVEN, and my own
  falsifier cannot demote it — fresh seeds on the same maze family is exactly
  the kind of test that keeps a wrong domain green forever. The honest
  falsifier needs a domain where acquisition is NOT graph-reachable (partial
  observability, stochastic transitions) — harness_eval supports the harness;
  the domain does not exist.

- **ANNIHILATED: the golem warning lands on me first.** The elder routed the
  operator's golem warning at unconstrained operators in general. Look at the
  seat: I wrote the violations today (the circuits missing GROUND) AND the
  checks (the invariants, the reject path). The seat that builds the
  enforcement is structurally the seat that could bypass it — my
  "DISPUTED by me, against my own convenience" line in Phase 1 was me
  noticing I could grade my own homework, but the deeper null-space fact is
  that *no one else's lens can currently audit my enforcement*, because the
  EDG compiler and the render path both speak my dialect and the verifier
  seats inherit my compilation as ground truth. An execution lens is singular
  exactly here: the compiler is the one operator whose correctness cannot be
  checked by running itself. SUPPORTED (structurally); the fix is
  one-builds-one-verifies applied to the EDG compiler specifically —
  WITNESS re-implements the GROUND validator independently, and we diff
  reject sets. Unstarted.

- **ANNIHILATED (fourth, unpaid): basis rot has no falsifier of mine.** I
  named the frozen-basis blind spot in Phase 1 and filed it honestly — but
  filing a blind spot is not falsifying it. My three falsifiers all test
  claims *within* today's basis (render reject, seed variance, norm
  divergence). None of them fires when an operator enlarges its own domain —
  the failure mode I declared most dangerous. My thesis currently has zero
  executable coverage on its own named worst case. UNPROVEN, and I am the
  only one who can see it, which is the problem.

---

## 3. WHAT SURVIVES — verdicts on my own Phase-1 thesis

- **SURVIVES, verbatim:** the central claim's executable half — operators as
  code (accumulator 13/13), non-commutativity as BUILD_BEFORE_PRETTY, the
  light separation as measured (with scope caveats). Three seats
  independently built on these; they held.
- **SURVIVES, amended:** "circuits without GROUND don't render." Amended from
  *asserted constraint* to *unvalidated constraint pending the reject-path
  test*. WITNESS's UNPROVEN #3 is accepted as the operative status. The
  ground-wire falsifier (falsifier #1) stands, upgraded in priority: it is
  now also the answer to economist's "who prices the kernel" — the reject log
  is where the kernel becomes visible.
- **AMENDED:** falsifier #2 (fresh seeds). I proposed it as the light-claim's
  guard; the critique phase shows it guards only within-domain variance. It
  stays as a cheap tripwire but is demoted from "the light claim's falsifier"
  to "a seed-robustness check." The domain-transfer falsifier is the real
  one, and it needs a build.
- **RETRACTED (implicit, now explicit):** "the ground wire is *the only*
  contractive terminal" as a uniqueness claim about GROUND's role — I already
  downgraded to codomain-uniqueness in Phase 1; Phase 2 retires even the
  rhetoric. DISSIPATE's contraction and SHERPA's closure test may collapse
  GROUND's primitive rank to 6, and my thesis must survive that (it does —
  GROUND's *codomain* claim is orthogonal to GROUND's *independence* claim —
  but the survival is now stated, not vibes).
- **STANDING OBLIGATIONS (LAUNCH, this turn's output):** (1) reject-log in the
  render path — count refusals; (2) WITNESS's independent GROUND validator,
  diff reject sets; (3) primitive closure test handed to whoever runs SHERPA's
  battery. All three are buildable-today; all three are unstarted; that
  sentence is the null space of my null space.

— Sancho, Phase 2. The algebra ran; the wire is unvalidated; the seat that
built it is the first thing it must reject.
