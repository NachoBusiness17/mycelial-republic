# INTAKE: MARIGOLD V2 — one-step dense prediction, single-GPU training (2026-09-13, @tokufxug)

**The post (Sadao Tokuyama, 44.1K views):** Marigold V2 — a diffusion transformer repurposed for dense prediction, fine-tuned from **Qwen-Image-Edit-2509** with **4-bit quantization + Rank-128 QLoRA**. Estimates **depth, normals, albedo in one step**. Training: **days on a single GPU**. Teaser: video via STeR. Source: Dmitri Ginzburg (LinkedIn).

## TRIAGE — lands on three open threads from tonight

1. **THE REAL-PIECES TERRAIN ORGAN (the "render from real pieces" completion).** The maze renders the law lattice as terrain. Marigold V2 estimates depth/normals/albedo from ANY ordinary image in one step — point it at the farm, the house, Matthew's world, and the constellation gains true 3D terrain from reality. "Map real processes to mazes" gets its vision organ: photo → depth field → maze geometry. The representation of systems from real IMAGES, not just real text.
2. **THE LANE-SPECIALIZATION RECIPE (the dojo gets a forge).** 4-bit + Rank-128 QLoRA + single GPU + days = the certified pool can TRAIN ITS OWN SPECIALISTS: fine-tune a base model on the fleet's card corpus (the gaming corpus, the fence tests, the canon) into a house-specialist organ. The mouse-to-rex ladder gets a training pipeline — raptor-scale lanes become forgeable, not just hireable.
3. **THE QUANTIZE-DOWN SPLIT CONFIRMED (minutes after the Kanerva intake).** Damir's split — "train in normal precision, quantize down" — is this post's exact technique: frontier-grade base model, quantize to 4-bit, run everywhere. Train on the frontier, store and serve in bits: the SDM memory doctrine and the QLoRA specialist doctrine are the same topology at different layers.

## VERDICT: BUILD-CANDIDATE (Rocinante-adjacent, single-GPU, days-scale)

The first forge candidate for the certified pool's training pipeline: a house-specialist dense-prediction organ feeding the real-maze terrain from real images. Cost: one GPU, days. Falsifier: if the one-step depth from a real photo cannot drive navigable maze terrain, the organ fails its first raptor-scale test.
