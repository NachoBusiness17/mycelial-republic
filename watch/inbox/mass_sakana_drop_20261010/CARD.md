# SAKANA MASS drop card (operator link, 2026-10-10)

Paper: arXiv 2610.12176, recursive self-improvement through multi-agent self-supervision
(viralized by elvis @omarsar0, DAIR.AI, 7.6k views; chat-with-paper at academy.dair.ai).
Read via grok verbatim + abstract page; paper body not yet read first-hand (flagged).

## Their claims (as posted)

- Self-improvement loops normally need an external verifier, excluding open-ended tasks
  without a checker. MASS removes the requirement.
- One base model proposes multi-agent workflows, runs them, GRADES them; evolutionary
  search keeps the best-scoring workflows; the model is fine-tuned on its own traces;
  the improved model starts the next cycle as a better optimizer and grader.
- Two cycles on Qwen3.6-27B: performance per output token 1.2 -> 1.6x on four open-ended
  benchmarks. A student trained on multi-agent traces beats a single-agent student
  trained on 1.4x more tokens.

## Estate mapping (why this hour)

1. THE SINGING-NETWORK BAR: the running ractor's acceptance law is "the network should
   learn on its own as it grows." MASS is the external claim of exactly that mechanism.
   Our design's difference: WHO CHECKS THE GRADER. The viral thread's own replies ask it
   (Aron Brand, Giacomo Masseroni); our answer is already in the design: consensus
   across heterogeneous models + dead-salmon controls (random-workflow / label-shuffle
   arms on the grader's rankings) + receipts. MASS's self-grading leg is the uncontrolled
   leg; the falsifier for their evolutionary selection is the dead-salmon test.
2. MULTI-AGENT TRACES > SINGLE-AGENT at 1.4x tokens: validates the estate's shape. Our
   lanes/ractors/workflows mint exactly such trace corpora (receipts with verdicts). The
   living-weights thesis gains a mechanism: fine-tune on own multi-agent traces, the
   optimizer improves. Our receipts corpus is MASS-shaped training data already.
3. TWO ANSWERS TO THE VERIFICATION BOTTLENECK: MASS closes the loop internally
   (self-grading, drift risk); our GWAP layer pays humans for insight on open-ended
   work. Not rivals - legs: machine consensus + controls as the floor, paid human
   insight as the top-up. The singing network should run both and MEASURE which leg
   carries which task shapes (the GPS ledger records it).
4. LINEAGE NOTE: Sakana = the AI Scientist shop (self-improving science agents with a
   documented self-modification incident history). Treat their self-improvement claims
   with the same gate we apply to our own.

## Falsifiers

- If the MASS grader's workflow rankings do not survive a random-workflow control arm,
  the selection is dead salmon and the 1.6x is self-preference drift, not improvement.
- For our side: if consensus-weighted routing does not beat single-model routing on
  held-out task shapes after N cycles of ledger accumulation, our network is not
  learning either - that is the singing-network falsifier, unchanged.
