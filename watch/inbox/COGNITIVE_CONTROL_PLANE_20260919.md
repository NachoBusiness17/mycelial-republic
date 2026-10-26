# THE COGNITIVE CONTROL PLANE — Iteration 6.0 mapped to the fleet (self-steal, 2026-09-19)

Sources folded: the JEV_RESEARCH_HANDOFF (verified spec), the stevie_builds
threads, the five drops (7z, Jev tax classifier, Linear Algebra canon,
intelligence recipe, inverse-square), and the Iteration 6.0 architecture
document (the other agent's iteration incorporating Jev as decision substrate).

## The Jev ground truth, verified and locked

- Endpoint api.typesafe.ai/v1/systemone, jev-1.13.0. $0.042/MTok in, $0 out.
  70-500ms. 64k/32k context split. Text-only state. Choice up to 255 options.
- Three primitives: Choice (pick from list), Score (rubric position), Noul
  (boolean probability). Parallel, isolated, one judgment per question.
- Architecture: transformer explicitly NOT an LLM; synthetic-data-only training;
  named for William Stanley Jevons (cheaper intelligence -> more use); the class
  is Kahneman System One.
- Confidence is a spread statistic, C = (N*p_max - 1)/(N - 1), validated on 738k
  live answers. Calibration does NOT guarantee correctness: audit ECE/Brier
  locally (fleet rule: every oracle carries a calibration certificate, G44).
- Doors: Vercel typesafe-ai/jev, Netlify, OpenRouter typesafe/jev-1.13.
  On-ramps: docs.typesafe.ai/llms.txt + aliaihub/awesome-jev-usecases.
- The poster numbers (193.6x/444.6x) are vs-slowest-baseline and TypeSafe flags
  the bias itself. Vs Terra: ~25x/76x. Honest numbers on file.

## THE COGNITIVE CONTROL PLANE — what Iteration 6.0 adds and where it lands

The doc's thesis: Jev should not be another worker; it should be the measurement
and routing substrate around the workers. The fleet mapping, piece by piece:

1. DISAGREEMENT AS MEASURED PRIMITIVE: disagreement expressed in language is
   inference; it must be measured to be used. Fleet landing: salon verdicts
   become probability distributions (per-lens confidence), not prose. The
   dissensus hypergraph gets numeric edges.
2. THE QUESTION AS THE BASIC COGNITIVE UNIT (not the agent): agents become
   question-answering instruments in an epistemic graph G=(Q,H,E,D,M). Fleet
   landing: VERB feels() already is a typed question; the upgrade is the
   question GRAPH (dependencies between questions), not just the log.
3. THE DECISION SURFACE EXPOSED: answers arrive as P=.81 because Q1=.94, Q2=.77,
   Q4=.63. Then: WHICH uncertainty is controlling the decision? Fleet landing:
   drift pairs gain a dominant-uncertainty field; the cliff scalar names the
   controlling question.
4. EPISTEMIC COMPUTE ALLOCATION: low uncertainty -> cheap decision; critical ->
   human. Fleet landing: the tier packs ARE this (frontier/flash/local), plus the
   escalation ladder from the veto oracle. Formalize the thresholds.
5. THE COMPUTE GOVERNOR: debate until expected information gain falls below
   cost. Replaces fixed rounds. Fleet landing: standing drives stop on
   instrument conditions, not counters (already law); extend to salon rounds.
6. THE IGNORANCE BUDGET: the compiler's failure mode is epistemic hoarding
   (questions breeding until cost explodes). Every new distinction must answer:
   what uncertainty does it resolve, how often, what does it change, what does
   it cost. Fleet landing: the amendment gate gains the ignorance budget as the
   DISTINGUISH/compile gate. This is the cliff-scalar law applied to ontology.
7. LEVEL FOUR LEARNING: change what the system considers worth knowing. Fleet
   landing: the teleological drift pairs (referent = filed future) are exactly
   this; the instrument already exists.
8. THE FALSIFICATION EXPERIMENT: System A static / B compiler / C epistemic
   evolution, measured on tasks whose relevant distinctions were ABSENT from the
   initial ontology. Fleet landing: this is the four-condition experiment's
   sibling; pre-register it as the ontology-evolution falsifier (novelty x
   validity x generalization, plus regression rate and human-intervention count).

## What remains ours (not in any external doc)

- The append-only kifu: verb rows hash-chained, steering that cannot lie about
  its own control flow.
- The doctrine packs as satellites: grounded reads, 99 percent hit.
- The parable register as the second notation: every instrument keeps its story.
- The seal law: units grow only with verified work.

## The build order this maps to

1. VERB stone three: typed question vocabulary (Choice/Score/Noul naming
   adopted) + the silence branch (done tonight).
2. classify() pods over the riddler corpora (nedwize pattern, janitor cost).
3. Epistemic graph schema: questions as nodes with dependency edges (upgrade of
   the verb trace).
4. Ignorance budget on the amendment gate.
5. October: LLaMA-Factory is the fold pipeline; the battery drafts are the
   calibration set; the A/B/C systems are the four conditions restated.
