# INTAKE CARD — SleepFM thread, @HowToPrompt__ (2026-09-04)

**Paste**: https://x.com/HowToPrompt__/status/2095763273262264777
**Score**: 15/25 — **BUILD WINDOWED** (the steal is the probe design, not the medicine)

## Receipts vs the tweet (paper is real: Nature Medicine s41591-025-04133-4)
- Model exists, Stanford, trained on 500K+ hours PSG from ~65K patients:
  **Supported** (tweet said "nearly 600,000" — close, minor inflation).
- 130 conditions: **Supported** verbatim.
- "84% accuracy" mortality: **Misleading gloss** — the paper's number is
  AUROC 0.85 / c-index ~0.84. That is cohort risk-ranking, not "predicts
  when you'll die." The genre rule holds: real paper, absolute-number-ified
  claims. Parkinson's "89%" same class (AUC, not accuracy).
- Leave-one-out contrastive learning: **Supported** — genuinely the novel
  method (arXiv 2405.17766): hide one modality at a time during pretraining,
  force reconstruction from the rest.

## The steal (why this card isn't medicine)
Two ideas transfer to fleet health verbatim:

1. **Discordance-as-signal.** SleepFM's best predictor is not any single bad
   metric — it's cross-system desync (brain deep-asleep, heart acting alert).
   Fleet translation: our worst incidents were ALL discordance — board
   runaway (processes said fine, disk said 2.24GB), claim-organ split-brain
   (claims said success, x4), seat self-reports vs room rows. The health
   signal is BETWEEN organs, not inside any one.
2. **Leave-one-out as the probe design.** Hide one organ's report (seat
   tails, billing rows, room rows), require the remaining organs' files to
   reconstruct it. Reconstruction failure = discordance receipt = the exact
   class of bug that has bitten us three times. $0: files vs files.

## Routing
1. **BUILD WINDOWED**: `discordance_probe` v0 — pairwise cross-receipt
   consistency (room rows vs seat tails vs billing vs chain), leave-one-out
   flavor, output = tri-state discordance card. Rides behind Leg 1 organ
   fix (same neighborhood, same night window).
2. **REMEMBER**: "84% accuracy" ↔ AUROC 0.85 — the gloss taxonomy grows
   (accuracy-vs-AUC joins tweets-vs-payload, receipts-have-hypotheses).
3. **REMEMBER**: leave-one-out contrastive = alignment-by-ablation; possible
   eval shape for the tale-re-encoder corpus later (hide one wing, reconstruct).

Tri-state: paper real **Supported**; tweet's accuracy framing **Disputed**
(AUC mislabeled); fleet steal **Supported as design, Unproven until the
probe runs**.
