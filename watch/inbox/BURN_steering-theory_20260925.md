# BURN steering-theory 2026-09-25

## Verdict
steal

## Evidence
- tools/drift.py line 83: "a rate metric answers 'is it moving'; only corr(delta-M, delta-R) answers 'is it moving north'".
- memory/runs/gps_50/FOLD.json, G38 (nemotron): "Kalman on unfiltered residuals converges to a biased state; the analogy needs a bias model before the update step". G22: fleet multipath = inter-agent signal reflection, filtered RAIM-style.
- arXiv:2607.11871v1 (13 Jul 2026, Xu et al.), mechanistic account of LLM-as-judge bias: "subtracting it from a biased activation restores near-baseline scoring (defense)"; "a simple linear projection onto the same bias-direction features anticipates judge failures on three entirely unseen benchmarks" (cross-domain AUC 0.82 vs 0.63 for a text-based baseline). Boundary: activations read only on "three white-box judges (Llama-3.1-8B, Qwen3-14B, Gemma-3-12B)". Authors: "Steering here is a causal probe on the recovered geometry, not a proposed debiasing method." Effect is direction-specific, not perturbation-amplitude-dominated.
- ICLR 2026 workshop page (Principled Design for Trustworthy AI, 27 Apr 2026) lists "The Rogue Scalpel: Activation Steering Compromises LLM Safety" (Korznikov, Galichin, Dontsov, Rogov, Oseledets, Tutubalina), OpenReview id=8ic6qxg3qS. Title-level claim only; abstract not fetched (owed).

## Steal or Vacuous
Steal, small. The fleet mapping holds with boundary conditions. (1) Internal-state monitors as drift pairs: validated. A cheap linear read of hidden state tracks the referent (judge failure) across unseen benchmarks, which is exactly the corr(delta-M, delta-R) organ, and it is direction-specific. Adopt as registry pairs on white-box lanes only: local janitors (gemma:2b, gemma4) yes, hosted groq/cerebras/zai lanes no (no hidden-state access). This is the T0/T1-local doctrine restated by the literature. (2) Packs as steering payloads: now declared attack surface. Rogue Scalpel's title claims the steering channel itself compromises safety; fold into pack-import doctrine: an unverified pack is an unscanned steering vector, same gate family as G05's emergency-override injection. (3) Kalman mapping: unchanged; G38's bias-model debt stands, the literature neither pays nor breaks it. (4) Kifu as track: untouched by both reads, untested, not invalidated.

## Falsifier
Build: register two metric-referent pairs per local lane (metric: max-prob minus second-max confidence gap, and logit entropy read at feels(); referent: verdict correctness on a labeled 1k set), then run drift_check over >= 3 deltas. Pre-registered kill: if every pair on both local lanes returns DRIFTING, INVERTED, or VACUOUS, the "Kalman = drift pairs" mapping is demoted VACUOUS for white-box lanes and the build stops.

## Bibliography
- tools/drift.py (repo, read 2026-09-25)
- memory/runs/gps_50/FOLD.json (repo, read 2026-09-25)
- memory/runs/gps_50/GPS_PACK.md (head, repo, read 2026-09-25)
- https://arxiv.org/html/2607.11871v1 (fetched 2026-09-25)
- https://iclr.cc/virtual/2026/workshop/10000808 (fetched 2026-09-25)

Owed, never synthesized: Rogue Scalpel abstract (OpenReview forum 8ic6qxg3qS); "A Concise Agent is Less Expert" seen in search snippets only, unread, uncited above.
