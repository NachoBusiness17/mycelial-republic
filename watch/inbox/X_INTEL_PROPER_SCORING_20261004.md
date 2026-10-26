# X INTEL: proper-scoring-rule decision models (TheVixhal / Gero-4B) (2026-10-04)

Operator drop: "https://x.com/TheVixhal/status/2106688054526427494?s=20"

## What it is, byte-verified

@TheVixhal (vixhal-baraiya, physics+AI/ML double major, builds GraphDB at
hydra_db, 23.3K followers), 2026-10-04 10:09 UTC, 38 bookmarks on 1.5K views:
an RL setup for training decision models that return calibrated probabilities
instead of text. Follow-up to his X article "Building an RL fine-tuning
platform to train JEV-like decision models" (x.com/i/article/2106424906313605120,
app-gated: both WebFetch and the reader door returned login walls - the
diagram and model card carry the content; what "JEV" means is NOT verifiable
from open bytes, noted honestly).

The diagram (banked: watch/inbox/vixhal_proper_scoring.jpg, 2000x1000,
fully legible):

- shared prefix encoder E_theta(s, q) = Qwen3-4B + LoRA -> prefix K/V
- per-option branch f_theta(h, o_i) -> score z_i -> softmax -> pi over options
- decision a* = argmax pi; confidence c = pi(a*)
- outcome rollouts y_g ~ p* where p* is a soft label FROM THE DATA - the
  diagram states verbatim: outcomes "come from the data, never from the model"
- reward per rollout: R_g = log pi(y_g) + lambda * [hit_g log c + (1-hit_g) log(1-c)]
  with hit_g = 1[y_g = a*]; loss = -mean R_g

Both reward terms are proper scoring rules (log score on the distribution,
log-Bernoulli on the stated confidence): truthful reporting of probability
AND of self-confidence is the unique optimum. Gaming is mathematically
punished, not socially discouraged.

The model (huggingface.co/vixhal-baraiya/Gero-4B, Apache 2.0, 50 downloads):

- "System One" decision model from Qwen3-4B (named for Kahneman's system;
  named Gero after Gerolamo Cardano). NO LM head: a learned linear scorer
  reads each option's final token; softmax across options.
- options scored independently - no option sees another - so no position
  bias (the architectural cure for what quiz distractor bias-checks patch
  socially); shared prefix enables prefix caching.
- question types: Choice (2-256 options), Score (2-10 ordered levels,
  probability-weighted position), Yes/No (P(yes)).
- training stages: scorer readout -> instruction/structure data (audited for
  shortcuts) -> RL for calibration mixing clear-cut and ambiguous items.
- calibration claim: probabilities at face value (0.9 right ~9/10), top of
  range slightly optimistic. No published evals on the card.
- tweet context: trained LoRA on MLX on a MacBook M5 Pro 24GB. LOCAL-FIRST.

## Estate connections (the connect step)

1. GWAP v4 DOOR - the direct hit. tools/arena_gwap.py's agreement_score is a
   fraction of declared actions the law confirmed (arena_gwap.py:13) - a raw
   hit-rate, not a proper score. A hit-rate pays nothing for calibrated doubt:
   a judge that overclaims on uncertain items scores the same as one that
   reports honest probabilities, so long as the argmax lands. The Vixhal
   reward is the upgrade class: score judges by log P(assigned to the outcome
   verification later confirms), confidence head scored by log-Bernoulli.
   Then truthful judgment is the dominant strategy and the CRJudgeBench
   finding (GLM-5.3 loses-by-6 as judge, memory index 10/2) becomes a
   trainable defect, not a fixed property.
2. QUIZ RACTIVE, UNGAMEABLE - probability-over-options answers scored by log
   score remove the distractor-bias class entirely (hedging is punished
   optimally; no answer-shape gaming). Direct input to the quiz-ractive
   steal door from X_INTEL_AIENG_SCRATCH_20261004.md and to the verification
   lanes running RIGHT NOW in the 24-wide dig (dwfrun-5e9435bb).
3. SYSTEM ONE - the estate already holds the System-One concept (the Jev
   clone verb-stack = System-One routing/guardrails, memory index 10/2) and
   the atomic-NOULs finding (control-plane beats fat choices). Gero-4B IS a
   System-One organ: branchable, sortable, no text parsing. Apache 2.0 means
   it is downloadable as a drop-in router scorer for lane routing / dumb-mesh
   MATCH confidence.
4. OUTCOMES FROM DATA, NEVER FROM THE MODEL - the diagram's rollout law is
   the estate's own trust-bytes-not-reports law in training-loop form (and
   the closed-corpus doctrine: labels from the territory). Convergence
   evidence the design is sound, from a stranger.
5. CONCEPT PREDICTOR UPGRADE PATH - the estate's concept_predictor organ
   (tests/test_concept_predictor.py, landed 09-30) outputs probabilities over
   concepts; this is its training-scheme upgrade (proper-scoring RL on
   data-derived soft labels).
6. LOCAL-FIRST TRAINING DOOR - LoRA on MLX on a 24GB MacBook = the estate's
   hardware class. The judge-calibrator the mesh needs is trainable at home
   for $0 of API spend; pairs with the Pixel-11 body / local-first doctrine.

## Steal doors, ranked

1. gwap v4: add a proper-scoring layer (log P of verified outcome + confidence
   log-Bernoulli) to the agreement engine; falsifier: judges trained/scored
   this way must beat the raw-fraction baseline on CRJudgeBench-class pairs.
2. quiz ractive v2: probability-format answers + log-score grading for estate
   skill cards and the curriculum's quiz.json contract (running workflow's
   primer cluster owes the crossover).
3. drop Gero-4B in as a System-1 router scorer (Apache 2.0): lane routing,
   mesh MATCH confidence, ask triage - anything currently parsing vibes-text.
4. local calibrator: MLX LoRA fine-tune of a small model on estate verdict
   history (failure_kb + gwap ledger as the data-derived soft labels - the
   estate already owns the p* the diagram demands).
5. honest-confidence heads on judge seats: the confidence term alone
   (lambda term) is addable to existing judge prompts' scoring before any
   training happens.

## Honest limits

Article body app-gated (JEV unexplained in open bytes). No published evals on
the model card - the calibration claim is the author's, unverified by third
parties; 50 downloads. The diagram is the strongest open evidence. No estate
action taken beyond this receipt; doors 1-2 wait on the running 24-wide
workflow's verification lanes to land first.

Writer: zcode-53-strategy-window
fetched: 2026-10-04
