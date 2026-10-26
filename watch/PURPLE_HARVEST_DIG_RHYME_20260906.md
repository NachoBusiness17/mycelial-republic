# PURPLE HARVEST DIG — "rhyming is not mathematical" (2026-09-06)
> **[AUDIT-TYPED 2026-09-08]** status: LIVE · claims: lexical relevance is not functional transfer; a deterministic transfer-contract gate can admit true transfers and block rhyme-traps — UNPROVEN (B6 launched same turn but the ≥9/10 falsifiers not measured in this card) · falsifier: gate admits a rhyme-trap or blocks a true transfer on the measured adversarial set (below 9/10 either side)

**Source:** x.com/LeftyHikes/status/2096615635312628114 — a reply TO @NachoQuixotic's
satellites-vs-phone-navigation post. The stranger's blocker, verbatim: "vast
differences in training data to what I want… some PhD in climate, Econ, finance
writes a paper for x reason from 1987. AI reads and incorporates that data into my
model for no reason because word search. **Rhyming is not mathematical.**"

**Commission:** iterate how to make it better, via research dig. (Operator, 09-06.)

## The problem, named

Lexical relevance ≠ functional transfer. Word-search curation admits a document
because its vocabulary rhymes with the target; the document was written to answer a
DIFFERENT question, under different assumptions, in a different regime — and poisons
the model quietly. This is LAW-061 in the data plane: retrieval passes, derivation
faked. It is also our own refeed finding (94% of input is re-fed cache reads):
motion substituting for progress, in training data.

## The art, three generations

1. **Distribution matching** (the workhorse): DSIR — importance resampling to match
   a target distribution (NeurIPS 2023, Xie et al.; neurips.cc/virtual/2023/poster/70154).
   Honest limit: it matches surface statistics to a target corpus — rhyme at n-gram
   altitude. Still cannot ask what a document is FOR.
2. **Target-task curation** (the current frontier): BETR — "Language Models Improve
   When Pretraining Data Matches Target Tasks," 2.1× compute multiplier by making the
   implicit target EXPLICIT (arXiv:2507.12466); DsDm — model-annotated selection with
   target-task documents (arXiv:2504.11393); QuRating (Princeton, multi-criteria
   rater, biases documented); DataDecide (Ai2, ICML 2025 — small-scale experiments
   predict which curated corpus wins); PreSelect (ICML 2025, contribution-predicting
   selection). Convergence: **the target must be stated, and data is admitted against
   the target, not against the words.**
3. **Claim/provenance instruments** (the seam): SciCite (citation INTENT: background
   vs uses-data vs compares; github.com/allenai/scicite), SOFT (intent ⊥ content type,
   arXiv:2601.05103), ClaimFlow (claim evolution across papers, arXiv:2603.16073),
   CiteME (claim-level attribution, NeurIPS 2024), Claimify (Microsoft — claim
   extraction from LLM outputs). **Nobody in this dig stitches claim-intent +
   assumption-carrying claims into a training-data GATE.** That is the open seam.

## What the fleet already owns (the iterate is assembly, not invention)

- Intake is already purpose-gated: every doc enters through a TRIAGE card — claims,
  tri-state verdicts, artifact, route — or it doesn't enter. **The card IS a transfer
  contract.**
- Temporal validity is chain law: a superseded 1987 claim isn't deleted, it's
  *succeeded* — v1 frozen as elder, v2 citing what it grew from. The gate always
  knows which generation is live.
- The adversarial test set already exists, measured: TRIAGE_HAUL_BOT_01's corpus
  diff found the real false friends in our own index ("EPR" hits: lineage-diff /
  RL-paint / MuseSpark — vocabulary rhyme, zero transfer).

## LAUNCHED — B6: the transfer-contract gate ("the rhyme-is-not-math filter")

Extend the intake schema with an explicit **TRANSFER CONTRACT** per card: claims
hold under assumptions A, for variable V, in regime R, as-of date D. Gate =
deterministic matcher (zero tokens, Zero-Mem law): a document is admitted to a
curriculum lane only when its contract matches the target spec. Falsifiers, on an
adversarial set built from our own measured false friends (+ true transfers: the
DA/SparDA/B3/B4 cards): gate admits true transfers ≥ 9/10 and blocks rhyme-traps
≥ 9/10, while a keyword-overlap baseline (the "rhyme" baseline, run as control)
provably fails the traps — measured, not assumed. Receipt:
watch/PURPLE_HARVEST_B6_TRANSFER_GATE_20260906.md. Builder fired same turn.

## REPLY DRAFT for @LeftyHikes (operator hand, X-register)

"It has a name: lexical relevance isn't functional transfer. Three generations of
the fix — (1) distribution matching (DSIR, NeurIPS 23): still rhyme, just at
n-gram altitude. (2) target-task curation: BETR got 2.1× compute by making the
target explicit; DsDm/QuRating/DataDecide are the toolbox. (3) the open seam:
claim-level gates — index docs by the claims they actually support and the
assumptions those claims carry (SciCite-style intent, Claimify-style extraction),
admit only what matches your model's job. A 1987 paper should enter your corpus
tagged with THEIR question, not your keywords. Rhyme is not math — make the math
the admission test."

## Doors

REPLY-SEND (his hand) · B6 verify on landing · WIRE — make TRANSFER CONTRACT a
required section on all future TRIAGE cards (seat-side, no builder needed).
