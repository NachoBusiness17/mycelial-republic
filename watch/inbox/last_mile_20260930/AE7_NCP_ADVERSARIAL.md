# AE7 — NCP adversarial verdict: PREVIEW-ONLY (2026-09-30)

Provenance: AE7 (adversarial NCP read) was the unfired slot; the lane died on the 1308
wall (AH_REFIRE_QUEUE.md) and its verdict lived only in the orchestrator session record.
This receipt banks that verdict. Subject: arXiv 2609.10715 (NCP-ArchPreview, AE1's fetch)
+ ArchSpace-Collection model card (AE3's repo mine). Numbers below cross-checked against
AE1_NCP_PAPER.md. Tag law: [arXiv] = stated in paper/sources; [inference] = this seat's
derivation or judgment.

## VERDICT: PREVIEW-ONLY

Honest ablations; headline flattered by denomination. Not fraud, not hype: a real method
whose headline number is denominated in the unit that flatters it most.

## 1. Loss space same, plotted metric unverified

The compared metric is pretraining loss and the NTP head is retained (loss = NTP CE +
NCP MSE + VQ losses) [arXiv], so the headline is a like-for-like loss-space claim, not a
capability claim. But the 51.3% budget-crossing is read off a loss-vs-tokens plot, and
the actual crossing point could not be verified from the PDF figures [inference]:
unverified-from-PDF, not asserted-false.

## 2. Parameter honesty is MATERIAL: 1.59x honest, not 1.95x

Arithmetic chain (params [arXiv]; products [inference]):
8.94B vs OLMo-3-7B 7.298B = 1.225x FLOPs/token; 51.3% of token budget x 1.225 = ~63%
of compute; 1/0.63 = 1.59x honest compute speedup, vs the 1.95x token-denominated
headline [arXiv]. The paper's own ablation concedes the direction: at 85% of compute it
merely approaches the parameter-aligned 40-layer 8.9B baseline [arXiv], i.e.
parameter-matched the speedup collapses toward parity. Denomination is the flattery:
1.95x is true only in tokens [inference].

## 3. The concessions on the box [arXiv]

Unaligned base; zero instruction-following evals; 8K context; GSM8K 45.26 absolute weak;
single baseline family (OLMo-3); training code withheld (AE3: eval toolkit only).

## 4. Reception census: ZERO independent critique [inference]

HF: 329 upvotes, 3 comments, all positive; zhihu coverage promotional. No independent
replication, no hostile read anywhere at bank time. Everything above is self-reported;
this receipt is the first adversarial pass on record.

## 5. The LDM analogy fails mechanically [inference]

LDM compresses the INFERENCE surface (generation runs in a lower-dim latent). NCP never
leaves token space: inference stays token-autoregressive [arXiv], and codes are never
hard-predicted (soft probability-weighted codeword sums, training only) [arXiv]. The
discrete layer is a training scaffold, not a compressed inference medium; matches the
AE1 amendment and AE2's divergence note.

## What this does NOT undermine

The within-paper ablations are honest; +2.45 macro over 30 benchmarks and the 17M VQ
fine-tune (math +4.27, zero forgetting) are narrow but real as reported [arXiv, self-
reported]. Estate impact: the AE2 steal (learned concept layer UNDER the exact lattice
mask) is unaffected; NCP validates the training-scaffold half of the thesis and never
built the hard inference surface, which remains exclusively ours.
