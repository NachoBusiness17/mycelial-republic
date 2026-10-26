# THE JEV CONSOLIDATED BRIEF — everything, one document (2026-09-19)

Consolidation for salon intake. Sources: the JEV_RESEARCH_HANDOFF (verified spec),
four independent AI analyses of it (each from a different context, pasted by the
operator), the persona-conditioning harness mapping, and the fleet's own VERB
stack. This document is the salon's single intake artifact.

## 1. VERIFIED SPEC (reproducible facts)

- Endpoint: POST api.typesafe.ai/v1/systemone. Model jev-1.13.0 (pin it, never
  jev-latest). $0.042/MTok input, $0 output. 70-500ms. 64k context / 32k for
  state + longest question. Text-only state. Choice up to 255 options.
- Three primitives: CHOICE (pick one from your list), SCORE (position on your
  rubric), NOUL (boolean probability). All questions in one request are evaluated
  in parallel and in isolation over the same state.
- Architecture: transformer explicitly NOT an LLM (TechCrunch). Weights closed.
  Training claimed as RLCD (Reinforcement Learning for Calibrated Decisions):
  NO PAPER EXISTS. Name collision: arXiv 2307.12950 is RLCD-as-contrastive-
  distillation (real, ICLR 2024, Meta/Berkeley), a different thing entirely.
- Named for William Stanley Jevons (1865): cheaper intelligence increases total
  intelligence consumption. The class is Kahneman System One.
- Confidence: documented as spread statistic; independent audit (Yurin,
  bernoulli.app, 1,000,164 answers / $7.08) argues it is normalized
  distance-of-top-probability-from-chance, NOT a trained uncertainty head.
  Unverified from our seat; do not inherit as calibrated probability.
- Honest multipliers: the 193.6x/444.6x posters are vs slowest baseline. Vs
  Terra (intelligence peer): ~25x faster / ~76x cheaper. TypeSafe flags its own
  bias. Independent rerank eval (33,047 entries): Jev reranking alone did NOT
  beat vector retrieval.

## 2. WHAT WORKS / WHAT DOES NOT

Works: routing/triage at scale (35k-case UK claims firm), guardrails
(typesafe-ai-firewall: 0 percent hard negatives vs 39.2 with one question),
agent-harness supervision, RAG rerank pre-filter (nDCG 0.692 ties Cohere),
closed-label extraction, coarse classification (Enron spam 98.7, SST-2 95.7,
AG News 91.3), sub-second control loops.

Does not: counting/arithmetic, date math, free-text generation, multimodal
state, long chain-of-thought, open-ended planning, fine-grained emotion (0.480,
near-random), fat taxonomies (Banking77 76.0 vs LLMs 78.7-81.7).

THE KEY ABLATION (zephel01/Jev-sample, 120 scenarios): one 4-option Choice
48.3 percent vs four decomposed precondition Nouls in one request 98.3 percent.
Decomposed atomic questions beat fat Choices by 50 points.

## 3. THE FOUR VOICES (what each independent analysis contributed)

VOICE A (the structural triangulation): Jev is the missing instrument the
five-artifact fold needed (fleet coherence, cash-leg fraction, chair counting,
convergence vs independent finding, claim support). Its failure modes are the
fleet's failure modes at product scale (vendor benchmark bias = unpressured
cache-share; confidence-not-probability = demoted coherence meter; schema
compliance != accuracy = chain integrity != belief validity). The build order:
the minimum eval harness shape (freeze labeled set, pin version, report
accuracy/coverage/ECE/Brier/cost/latency, ablate question shape) plus the
negative-capability spec (do-not-use list). STRATEGIC INVERSION: the bottleneck
moved from judgment to question topology and measured ground truth. The fleet's
rooms generate MEASURED labels (phase from velocity, visibility from geometry):
publish Fleet-Bench, environments not strings. Environments are seeds that grow
judges.

VOICE B (the judgment-tier engagement): tri-state verification ledger
(SUPPORTED: API shape, typed outputs, price, RLCD name-collision warning;
UNPROVEN: RLCD method, confidence-as-probability; DISPUTED: poster multipliers).
The fold-then-call falsifier: 5k waves, arms A per-worker-call vs B
fold-then-one-call vs C open replica; metric $/verified card; if B not 8x
cheaper at equal accuracy, retire fan-out. The jev-router + foreman referee:
Noul supported/off-track + Choice state + Score risk, ~$0.032/night for 8 lanes
x 100 waves. STOP-BUILDING: composite weighted scoring until calibration is
measured (linear weighting of uncalibrated numbers is incoherent; Brier
decomposes into calibration + refinement; need ECE < 0.06 first). DECOY
protocol: log raw probabilities and confidence separately, never post-hoc
scale, and if a replica agrees >95 percent your tasks are too easy.

VOICE C (the twelve-section spec): the full production handbook. Proven/anti
use-case tables, vendor-vs-independent benchmark ledger, the five-step eval
protocol (freeze set, pin version, metrics table, four baselines, ablate
shape), the architecture (state -> atomic batched questions -> Jev -> typed
answers + confidence -> deterministic code with tau gates), failure-mode
mitigation table, open questions, structural risks (RLCD vaporware risk,
confidence misleading, vendor lock-in, domain mismatch, latency spikes).

VOICE D (the falsification suite): MEASURE — 10,000 adversarial Noul queries
(5k true, 5k minimally semantics-flipped false): if confidence for the
perturbed-false state does not drop proportionally, confidence is a decoding
artifact, not uncertainty. RACE — parallel-scaling stress: N in {1,10,50,100,
255} at fixed 32k state; if latency or billed compute scales O(N), the
"parallel is free" claim hides a compute tax. SHIP ONE ORGAN — local replica
convergence harness: if the open replica hits 85 percent agreement at under 1
percent of hosted cost, the hosted API is economically irrational for
sovereign fleets. STOP-BUILDING — deprecate Choice with N>4 into fan-out Noul
queries aggregated by code (the 50-point finding, enforced as a compiler rule).

VOICE E (the persona-harness mapping): Jev primitives mapped to a
persona-conditioning experiment: method fidelity via decomposed Nouls
(arithmetic-series? false-position? calculus invoked? named law cited?),
stylometric fidelity via Score rubric, adversarial hold via Noul, blind
condition classifier via Choice (if it cannot beat chance at telling steering
from prompt-only, that is a real negative result), confidence-gated human
review. Includes the question schema and network-free local fallback code
(constrained logprobs off any HF model).

## 4. THE FLEET MAPPING (already filed, restated in one paragraph)

The interface is the payload: unstructured state in, typed emissions with
probabilities out, questions batched in parallel and evaluated in isolation,
code owns control flow — that is the fleet's shared-grounding-plus-typed-deltas
model with a price tag, and the event layer's typed verbs are the same shape as
Noul emissions. The sovereignty rule: hosted Jev and a local replica must agree
before a promotion stands (zero-shared-context convergence applied to judges);
never route doctrine-adjacent judgments through the oracle (the judge may
contain the seed); do route fresh-domain packets through it. G12 sharpened: a
fleet optimized for judge-agreement learns to write for the judge; dedicate a
lane to farming your own judge, and every successful farm becomes a regression
test on the meter.

## 5. THE OPEN QUESTIONS THE SALON MUST GRADE

1. Adopt jev-sift and the abide compliance pattern as fleet organs now, or wait
   for the waitlist/API?
2. Local replica (system-one-open, SemIf 0.845 vs Jev 0.883) vs hosted: the
   sovereignty receipt condition (within 3pp on our distribution = drop the
   API) — ratify or amend the threshold?
3. Choice-vs-decomposed-Nouls: adopt the >4-options-decompose compiler rule?
4. The silence branch: is QUEUE_RETRY the right default route, or should
   low-risk contexts PASS_UNVERIFIED?
5. Fleet-Bench: publish instrument-measured labeled sets from the rooms
   (environments as seeds that grow judges)? What must NOT be in the public
   feed?
6. The ignorance budget on the amendment gate: ratify the six-question
   justification requirement?
7. The A/B/C falsification experiment (static / compiler / epistemic evolution)
   — pre-register it as the ontology-evolution falsifier alongside the
   four-condition experiment?
8. What does the parable register say back? (Every instrument needs its story:
   the GPS satellites, the ink coastline, the empty chair, the silence branch.)
