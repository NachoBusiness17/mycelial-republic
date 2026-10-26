# X INTEL - three-paper drop (operator, 2026-10-04 morning)

Sources: t.co/ZC280LPsV0 -> arxiv.org/abs/2609.40169; t.co/HteGrBj89J ->
academy.dair.ai explainer for arXiv:2610.01509; t.co/BKxCpfMd8L ->
arxivb.org/abs/2609.37535 (NOTE: arxivb.org is a mirror domain, NOT
arxiv.org; the paper was fetched canonically from arxiv.org/abs/2609.37535
- treat shared arxivb links as mirror-class, cite the canonical id).

## 1. ScholarEvolve - Lifelong Agent Harness Evolution (2609.40169, 09-30)

Mines the research literature itself (topic modeling over papers, per
harness MODULE) to proactively evolve agent harnesses - vs the reactive
failure-feedback meta-agents - keeping the model fixed. AppWorld
49.6 -> 63.6 (Qwen3.5-27B); Tau2-Bench 72.7 -> 81.9 (GPT-5.4-mini).

ESTATE CONNECTION: this is the estate's own program in academic form -
the OLM mine daily burn + frontier-mine + ractor arcs ARE literature-mined
harness evolution; the ribs/laws are the evolved harness. What they add
that we lack: strategy extraction is DECOMPOSED PER HARNESS MODULE before
mining (the estate's frontier-mine folds into a general digest, not per-
organ strategy slots). STEAL CANDIDATE: map frontier-mine finds onto the
organ taxonomy (the subsystems map exists) so each dig lands as a named
organ-strategy, the ScholarEvolve shape. Their "proactive vs reactive"
framing also names our split: burn-receipt cures = reactive, mine = 
proactive; the balance is a dial we already turn.

## 2. Sharpening Tax in Post-Training (2610.01509, Meta Superintelligence
Labs + UW-Madison + Stanford; via dair.ai explainer)

RL post-training "merely sharpens existing behaviors": pass@1 up, but the
set of tasks reachable under repeated sampling SHRINKS (base + minimal
harness beats post-trained at large K on BFCL v4/ACEBench/WebShop). The
tax = lost test-time scalability; grows with scale; fix = PTGS
(posterior-tempered group sampling during RL). They ask post-training
reports to carry a COVERAGE diagnostic next to accuracy.

ESTATE CONNECTION: this is the estate's swarm doctrine with a mechanism
and numbers - "the mesh reads, the frontier simulates", flash sweeping
prime, the dumb-mesh MATCH class, and above all the COLD-VERTEX
improbability drive (cold sampling = coverage-seeking by design; this
paper is its academic frame: sharpened models collapse the uncollapsed
tail the cold arm harvests). STEAL CANDIDATE (the real one): add a
coverage diagnostic to the fleet's own eval instruments - report pass@K
at large K next to pass@1 on estate ask classes (the arena/gwap batteries
measure agreement and wins, never coverage; a coverage column would have
PREDICTED the mesh-vs-frontier division of labor the estate learned by
burning dollars). Also: the dair.ai academy surface (Elvis Saravia) is a
liam.-class watch candidate for the amplification list.

## 3. Why Adaptive Optimizers Underestimate Rare Tokens (2609.37535, 09-29)

Mechanistic + closed-form: Adam/RMSProp/Lion/sign-descent systematically
under-assign probability to rare tokens (adaptive second-moment division
amplifies the rare negative gradient; tokens absent >= 2 minibatches
settle BELOW true frequency, ratio kappa/(2(e^(kappa/2)-1))); SGD/AMSGrad
and gradient-linear optimizers (incl. Shampoo, Muon) stay unbiased.

ESTATE CONNECTION (mechanism citation for existing doctrine): rare-token
underweighting is a upstream cause of the estate's closed-corpus
fabrication-frontier doctrine - models confabulate exactly where the
training distribution thins (rare facts), which is why FOG-SCAN and
byte-grounded retrieval (trust bytes not reports) are the cure, not
better prompting. Also live for any estate training leg: seed-mirror /
QLoRA small-corpus plans (Rocinante class) should prefer unbiased-
optimizer regimes or at least expect rare-vocab underfit - the paper's
fixed point says the bias is structural, not a bug to tune away.

## Doors (all free-lane, none fired)

- A: frontier-mine per-organ strategy mapping (ScholarEvolve shape) - a
  lane, not a patch.
- B: coverage diagnostic (pass@K at large K) on the arena/gwap batteries -
  instrument addition, estate-facing.
- C: arxivb.org noted as mirror-class in the link ledger; canonical
  arxiv.org ids cited for all three.

Filed by the 5.3 strategy window; fetched via the $0 surfaces (WebFetch +
the dair.ai explainer), no paid organs.

## 4. RSI-Master (arXiv 2609.35561, via @arXivBangers 06:11Z; SECOND
arxivb.org mirror link in two drops - arxivb.org is that account's
systematic habit, canonical id fetched instead; LINKS intake should
normalize arxivb.org -> arxiv.org)

Recursive self-improvement via autonomous post-training agents, with two
regularizations: anti-hacking (step-wise action regularization +
persistent traceable experiment records via an "Experiment OS") and
anti-strategy-lock-in (Reviewer-Guided Orchestration: Workers + Reviewers
in a dynamically growing research DAG, reviewers compare evidence ACROSS
related experiments to steer exploration). Results: PostTrainBench
Qwen3-4B-Base 54.49 vs 46.53 best baseline at 0.0% hacking; a 35B run
beats the human-developed Instruct model on LiveCodeBench-v6 (41.21 vs
37.36) and SciCode; nonzero on HorizonMath where frontier models score
near zero. Nothing released beyond the paper.

ESTATE CONNECTION - the estate is ALREADY running this shape, named
differently: their Experiment OS (regularized actions + persistent
traceable records) = our receipts/verkle chain/md_record autoseal + the
ratchet/citation-lint/workflow gates; their zero hacking rate is the
property our blind audits measured (96% truth-at-filing); their
Workers+Reviewers DAG = ractor lanes + arena/gwap judges over the
LINKS knowledge graph. Their anti-lock-in = our falsifier culture,
no-sacred-cows, cold-vertex two-regime steering, and tonight's
dedup-saturation rotation cure. THE STEAL (the one gap): their reviewers
compare evidence ACROSS experiments to steer the DAG - our judges grade
single asks and our synthesis lanes do cross-folding manually; a
cross-experiment evidence-comparison pass (per-organ, ScholarEvolve
slotting) is the structural version. Also banked: their 35B-beats-instruct
result is third-party proof of the estate's wire-don't-build /
tools-not-weights doctrine.

## 5. Rethinking at Fixed Points (via @huskydogewoof thread 10-02, CMU;
paper teaser + author site huskydoge.github.io; canonical id not yet
pulled - thread-class, bank the claim not the number)

Looped LMs matching standard Transformers at far fewer resources: "scale
by adding FLOPs at constant memory"; fixed-point shortcuts for
pre/post-training AND inference; learned depth prior + orthogonal
injection to shape the fixed points.

ESTATE CONNECTION: this is the operator's own steering-field vocabulary
in paper form - "dHead fixed-point = belief relaxation" (the k-space
water-computer triangulation, 2026-10-02) IS a fixed-point iteration over
model heads; the standing-wave protocol + ouroboros-GROWS verdict are
loop-first architecture claims; their "FLOPs at constant memory" is the
estate's loop economics (many cheap passes over one resident context =
the janitor/flash parliament). WATCH: pull the canonical id + read the
fixed-point shortcut for post-training (ties to the Sharpening Tax: does
looping RECOVER coverage post-sharpening? - the natural cross-paper
question).

## 6. RECURSIVE SOCIAL IMPROVEMENT (operator paste 2026-10-04, the
headline ask: "I do this manually, but it would actually be awesome to
do it autonomously!")

The recipe: (1) aggregate all agent sessions into a single db, (2) search
failure patterns across it, (3) collect pattern examples + solutions and
have an agent synthesize the traces into a skill, (4) use the skill
going forward.

ESTATE MAPPING (wire don't build - the organs exist, one is missing):
- Step 1 EXISTS scattered: trajectory tape (sealed per-session rows),
  lane trails, receipts + catalog FTS (917K rows), failure_kb.jsonl.
  Missing: the failure-centric VIEW over them (a query surface, not a
  new db - B2 verkle_vs_embedding verdict applies: no new store).
- Step 2 EXISTS per-lane: lane_runner CLUSTER_REPORT (windows,
  counts_by_class, confident_and_wrong overturns), the janitor FKB
  remedy bridge (top-5 sigs), falsifier_counter FIX/CYCLE events.
  Missing: CROSS-session global pattern roll-up.
- Step 3 is THE GAP: laws get synthesized from burn receipts (manually,
  per-window); SKILLS are not synthesized from failure traces at all -
  the ractor50 verdict named it: "waves are the fuzzer, cards are the
  commits" and the commit step is human today.
- Step 4 EXISTS with a measured bottleneck: skills dir + context pack +
  quantizer; the ouroboros F14 number (laws->ribs 4.5%) is the friction
  this recipe's step 4 always hits.
BUILD (fired): tools/social_rsi.py v0 - deterministic steps 1-2 (global
failure-pattern roll-up across trails + failure_kb, before/after example
pairs: same class failing then later green = the solution evidence),
step 3 as a synthesis PACKET per pattern (the seat or a free lane writes
the card in the winning shape), step 4 through the EXISTING human
promote gate (mag.cmd promote --apply stays the commit - autonomously
drafted, humanly promoted; the skill census law holds).
Falsifier: a session with the drafted card active fails less on that
class than without - measurable by the arena/gwap instrument.

## 7-9. the three companion links
- @ifradlin ARROW (arXiv 2610.01314): D4RT-style decoding extended to
  multi-view video + unordered image collections. The image->world stack
  (image-blaster) next rung; watch for the Mountain.
- @du_yilun finetuning-through-sampling (Harvard Kempner): SFT matching
  RL post-training, new knowledge WITHOUT forgetting. Cross-paper web:
  the Sharpening Tax measured RL shrinking coverage; this claims
  sampling-based SFT avoids the forgetting half - the estate's
  coverage doctrine now has both edges of the scissor (RL sharpens +
  shrinks; sampling-SFT adds without forgetting). Also the seed-mirror /
  Rocinante training-leg regime note, and an alternative engine for the
  RSI-Master loop.
- @matharium turnstile antenna: two crossed dipoles 90 degrees apart ->
  the field ROTATES along the mast (circular polarization, spiral
  wavefronts). THE QUADRATURE STEAL for the swarm vocabulary: the
  two-regime steering (heat-GPS dipole + cold-vertex dipole 90 degrees
  out of phase) superposed = not a standing wave but a ROTATING one - a
  helix through concept space, energy that travels instead of
  oscillating in place. "Be like water" now has an antenna diagram.
