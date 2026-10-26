# SEAT B: THE ADVERSARY CASE AGAINST CAPABILITY-LEDGER ROUTING

Written blind (independent of Seats A and C; attacks the PREMISE from the
panel's shared context, not any other seat's draft). Author: ractor seat
B, 2026-09-29. House law honored: em-dash 0; every claim about estate
artifacts path-cited; estimates marked ESTIMATE.

Thesis: capability-ledger routing is the wrong abstraction for this
estate. The v0 build (`tools/gps_mcp/`, 28/28 tests per
`watch/inbox/game_platform_basecamp_20260929/GPS_MCP_V0_20260929.md`) is
good plumbing for an idea that should die in committee, or at best be
demoted to an instrument that never touches the routing path.

## P1. The estate's own research already falsified the router's value

`watch/inbox/game_platform_basecamp_20260929/DELEGATION_RESEARCH_20260929.md`
banked the single most relevant 2026 result: SuperScout (arXiv:2608.04804)
at 159/266 vs 158/266 for the best single model on SWE-bench Pro at ~1/5
cost per solve, AND its own ablation showing the NO-ROUTER variant TIES
the routed system: "the handoff rather than the routing decision carries
the result." The estate read that line and then built a router. The
ablation says the leverage is in the verified handoff (sandbox-stripped
false claims) and the verification gate, both of which are PER-INSTANCE
artifacts. The ledger is a POPULATION artifact. The estate is about to
spend its scarcest resource (frontier judgment tokens, per the inverted
ask `watch/inbox/game_platform_basecamp_20260929/OPUS_ASK_DRAFT_20260929.md`
AMENDMENT 1) optimizing the component the ablation says carries ~nothing.

## P2. When a verifier exists, cascades dominate priors; when none exists,
the ledger's inputs are untrusted anyway

FrugalGPT-lineage cascades (cheap first, escalate on per-instance
evidence) capture most routing value with zero bookkeeping
(`watch/inbox/game_platform_basecamp_20260929/DELEGATION_RESEARCH_20260929.md`,
theory item 2: up to 98% cost reduction). Two cases, and the ledger loses
both:

- CASE 1: a machine-checkable gate exists per instance. Then the per-
  instance signal (did the cheap answer pass the gate?) is strictly more
  informative than any population pass-rate. The population rate only
  matters for ordering the cascade, and cheapest-first ordering plus the
  gate recovers ordering for free after a handful of instances.
- CASE 2: no per-instance gate exists. Then verdicts are unverified
  claims. v0's own build report concedes this: "record_verdict accepts
  any caller's verdict with an unverified evidence_hash. Nothing binds a
  verdict to a checkable artifact, so pass-rates are trivially
  inflatable" (`watch/inbox/game_platform_basecamp_20260929/GPS_MCP_V0_20260929.md`,
  What the Opus spec-review should critique first, item 2). A ledger of
  inflatable verdicts is not a capability map; it is a rumor database
  with a schema.

The escape hatch (build a verification-gate contract so verdicts are
trusted) is real, but notice what it concedes: the hard, valuable part is
the GATE, and once gates exist per shape, the marginal value of the
population ledger over gate-driven cascades shrinks to the cold-start
edge, exactly the region where the ledger has the least data.

## P3. The statistics starve the ledger faster than traffic feeds it

To route on a threshold of 0.85 (`tools/gps_mcp/router.py`
DEFAULT_PASS_RATE_THRESHOLD) you must SEPARATE a true 0.85 from a true
0.90; otherwise the gate flips on noise. Rough order of magnitude
(Wilson-type bound; ESTIMATE): distinguishing 0.85 from 0.90 at 95%
confidence needs on the order of 300 to 500 verified verdicts PER
(model, task_shape) cell. The v0 fixtures ship 30 cells with n between 16
and 160 (`tools/gps_mcp/seed_fixtures.py`), i.e., almost every cell is
noise by that standard. The estate's real verified-verdict throughput is
maybe tens per day on its best shape (ESTIMATE; no measurement exists;
that absence is itself the point). At that rate most cells never reach
decision-grade n, so the router spends its life in the unmeasured regime
where it is EXACTLY equivalent to a hardcoded cascade, minus the
simplicity.

## P4. Task-shape taxonomies leak (Goodhart with extra steps)

task_shape in v0 is a free TEXT column (`tools/gps_mcp/ledger.py`,
capability.task_shape TEXT). Three failure families:

- FRAGMENTATION: every caller-coined new shape name resets history to
  zero and re-triggers exploration routing; the ledger eats its own
  tail trying to fill cells.
- COLLISION: two different kinds of work under one name average into a
  meaningless rate (a "summarize" that mixes commit messages and legal
  briefs).
- GAMING: whoever names shapes controls routing (rename your way to the
  tier you want; or freeze a competitor model out by feeding its cell
  hard instances).

Any fix (registry, versioning, operator-approved shapes) converts the
taxonomy into maintained configuration: a human-curated ontology of what
work means, hand-kept current against drift. That is not infrastructure;
that is a product with one customer.

## P5. Drift invalidates the map on the exact clocks the estate runs on

The estate's local fleet is Ollama models that get re-pulled, requantized,
and hot-swapped (`AGENTS.md`, fleet description); the funded tier is
metered credits with prices and behaviors that move
(`AGENTS.md`, DRIVING LADDER 2026-09-28). A pass-rate is a measurement of
a (model-version, prompt-template, gate-version, traffic-mix) tuple that
v0 does not even identify. The measured half-life of a capability row on
a moving fleet is unknown but plausibly SHORT (ESTIMATE: days to weeks,
by analogy with the harness-effects literature cited in
`watch/inbox/game_platform_basecamp_20260929/DELEGATION_RESEARCH_20260929.md`
theory item 2: optimal harness design varies per model strength and task
class, i.e., the mapping moves when anything moves). If the half-life is
shorter than the verdict-accumulation time (see P3), the ledger is a map
redrawn slower than the territory moves. The research brief's own
economics warning rhymes: cheap-first without hard gates burns money
exactly where you hoped to save (failed SWE-bench tasks cost MORE than
solved, $0.48 vs $0.35, 51 vs 39 calls,
`watch/inbox/game_platform_basecamp_20260929/DELEGATION_RESEARCH_20260929.md`,
economics item).

## P6. The organ tax: the estate feeds the ledger instead of shipping

Every hour spent building probe schedulers, decay functions, principal
registries, chain audits, and taxonomy governance is an hour not spent on
the platform the ledger allegedly serves. The estate already has one
proven organ-avoidance law ("the ledger becomes a maintenance organ" is
the failure this panel must weigh against the platform's actual roadmap,
`configs/version_roadmap.yaml` and `state/CURRENT.md` hold it). v0's own
README smells it: three of its grow-this items (verification contract,
adaptive routing, transport) are all ledger-upkeep, none product
(`tools/gps_mcp/README.md`, IF WE GROW THIS).

## WHAT WOULD HAVE TO BE TRUE (pre-registration conditions)

The ledger beats plain cascades ONLY IF all of the following are true,
and each is falsifiable in an estate-run eval:

- C1 VERDICT SUPPLY: machine-gated verified verdicts arrive at a rate
  that fills an active cell to decision-grade n (order 300+, ESTIMATE)
  within one drift half-life. Measurable: verdicts/day per cell vs
  half-life in days.
- C2 COST DISPERSION: qualifying models on the same shape differ in
  price by at least 10x and stably (the fixtures assert 30x mid-to-
  frontier, `tools/gps_mcp/seed_fixtures.py` FIXTURE_COSTS; fixtures are
  hand-picked, not measurements). If dispersion is small, routing saves
  nothing worth its organ.
- C3 CONCENTRATION: the shape distribution is concentrated (top 5 shapes
  carrying the large majority of traffic, ESTIMATE >= 80%) so cells fill
  at all. A flat distribution over hundreds of shapes starves every cell
  (see P3, P4).
- C4 INVISIBLE-FAILURE HETEROGENEITY: there exist shapes where cheap
  models are confidently wrong often enough that per-instance confidence
  cannot catch it, but the population rate would. If cheap-model
  failures are almost always low-confidence, cascades see them and the
  ledger adds nothing. This is THE scientific crux: it is a claim about
  calibration, and it is measurable per shape.
- C5 DRIFT SLOWNESS: capability half-life comfortably exceeds verdict
  accumulation time (the inverse of C1's rate).
- C6 GATE ECONOMICS: running the gate on a cascade instance costs much
  less than the escalations the ledger avoids (ratio order >= 10x,
  ESTIMATE); otherwise gate-driven cascade is simply cheaper.
- C7 EVAL VICTORY: in a pre-registered head-to-head (ledger routing vs
  cheapest-qualifying cascade vs a trivial classifier), the ledger arm
  wins cost-per-verified-solve by a margin that survives multiple-
  comparison correction, without losing solve rate. If it does not, the
  ledger is demoted to instrument (report_capability as a dashboard, no
  routing authority), which per P1-P2 is where most of its real value
  already sits.

## CONCESSION (what survives even if the routing premise dies)

The receipt spine (every decision auditable) and the gate-class
definitions are valuable regardless, because the estate's whole product
claim is auditable verification
(`watch/inbox/game_platform_basecamp_20260929/OPUS_ASK_DRAFT_20260929.md`,
why-this-ask-shape item 3). Kill the router, keep the instrument: the
ledger as measurement dashboard feeding fleet decisions (the operator's
tier ladder, `AGENTS.md`), not the hot path.

Em-dash count: 0.
