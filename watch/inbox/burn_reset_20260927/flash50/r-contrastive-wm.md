# r-contrastive-wm: Contrastive world models via mutual-information objectives (no pixel decoder)

- Item: r-contrastive-wm, banked 2026-09-28 by gopher-r-contrastive-wm (flash50, burn_reset_20260927).
- Ask: deep-dive on contrastive world models trained with mutual-information (MI) objectives, no pixel decoder; key 2024-2026 papers, method shapes, reproducibility on consumer hardware.
- Method: 6 web-search rounds plus 11 direct fetches in this session (arXiv abstract pages, one arXiv HTML full text, two arXiv API queries, three GitHub READMEs, one PMLR abstract page). Facts below are grounded in fetched pages unless flagged "snippet-only". Search-snippet claims that later contradicted fetched sources are itemized in section 8.

## 1. The problem shape

Pixel-reconstruction world models (Dreamer's RSSM: encode observation, learn forward dynamics, reconstruct observations) spend model capacity and per-step compute reproducing pixel detail irrelevant to control. The decoder-free alternative keeps the forward dynamics model and replaces the reconstruction likelihood with an objective over latent representations:

1. an MI lower bound on transition information (InfoNCE, from CPC; Deep InfoMax style scores), the "contrastive" core of this ask;
2. self-distillation latent prediction (BYOL/SPR/MPR lineage: EMA target, stop-grad predictor, no negatives);
3. prediction into a frozen pretrained feature space (DINOv2/JEPA encoders);
4. latent-space diffusion (denoising in embedding space, not pixel space);
5. the dual direction: MI *minimization* to strip action-irrelevant structure (PLSM).

Bonnie Li's August 2026 paper, literally titled "Contrastive World Models", is the most on-point publication found and is treated as the reference item (2.7).

## 2. Key papers 2024-2026 (each entry grounded in a fetched page)

### 2.1 Contrastive World Models - Bonnie Li, arXiv 2609.22175 (v1 Aug 27 2026, solo author)
The reference paper for the ask. Verified from the abstract page and the HTML v1 full text.

- Method: built on Dreamer; replaces observation reconstruction with a Deep InfoMax-style InfoNCE lower bound that maximizes MI between the global state posterior concatenated with future actions, and *local patch features of future observations*, scored with a log-bilinear function. The paper motivates the replacement by noting the observation-likelihood term equals (up to a constant) the MI between observation and state.
- Evaluation: DeepMind Control Suite only: finger-spin, cheetah-run, walker-walk; 1e6 env steps, 3 seeds; three settings of increasing visual complexity: default background, colored moving-ball distractors, Kinetics natural-video backgrounds. Baselines: Dreamer (pixel-reconstruction RSSM) and a momentum-prediction baseline (BYOL/MPR-style: EMA target encoder, cosine-similarity prediction with stop-gradients, no negatives). All three share the same RSSM backbone and actor-critic.
- Results per abstract: matches both baselines by default; substantially outperforms both once distractors or natural-video backgrounds are introduced; removing the pixel decoder makes it "consistently substantially faster in wall-clock time per training step" (qualitative claim only).
- Caveats: no GPU model, VRAM, wall-clock numbers, or parameter counts are published (abstract and HTML v1 checked); no venue listed; small-scale (3 DMC tasks). Treat as preliminary but conceptually the cleanest "contrastive MI world model, no decoder" statement in the window.

### 2.2 DINO-WM: World Models on Pre-trained Visual Features enable Zero-shot Planning - Zhou, Pan, LeCun, Pinto (NYU), arXiv 2411.04983 (v1 Nov 7 2024, v2 Feb 1 2025)
Verified from the abstract page and the GitHub README.

- Method: model visual dynamics without reconstructing the visual world: spatial patch features pre-trained with DINOv2, learn action-conditioned prediction of future patch features from offline trajectories; at test time, behavior comes from action-sequence optimization toward goal features (zero-shot planning; no expert demos, no reward model, no learned inverse model).
- Results per abstract: zero-shot behavioral solutions on six environments (arbitrarily configured mazes, push manipulation with varied object shapes, multi-particle scenarios).
- Code: MIT-licensed repo (github.com/gaoyuezhou/dino_wm) with pre-trained checkpoints and datasets on OSF; tasks shown in the repo: PointMaze, PushT (pusht_noise), Wall, deformable (granular, rope, optional PyFleX via Docker).
- Hardware: none documented (README has no VRAM/time figures; abstract has none). The frozen-encoder design implies the training cost sits in a small dynamics head, but that is design inference, not a reported number (section 7).

### 2.3 TD-MPC2: Scalable, Robust World Models for Continuous Control - Hansen, Su, Wang (UCSD), arXiv 2310.16828 (v1 Oct 25 2023, v2 Mar 21 2024); surfaced by search as ICLR 2024 (venue not shown on the abstract page)
Verified from the abstract page and the GitHub README.

- Method: "local trajectory optimization in the latent space of a learned implicit (decoder-free) world model" (the abstract's own phrasing). No reconstruction loss; latent consistency is enforced through reward and value prediction heads plus planning (MPC with terminal value).
- Scale results per abstract: 104 online RL tasks across 4 domains with one hyperparameter set; a single 317M-parameter agent trained across 80 tasks, embodiments, and action spaces.
- Hardware (README, exact quotes): "You will need a machine with a GPU and at least 12 GB of RAM for single-task online RL with TD-MPC2, and 128 GB of RAM for multi-task offline RL"; "A GPU with at least 8 GB of memory is recommended for single-task online RL and for evaluation"; "Training of the 317M parameter model requires a GPU with at least 24 GB of memory."
- Reproducibility verdict: single-task online RL runs on a consumer box today; the multi-task/offline and 317M scale-ups need server RAM/GPU.

### 2.4 DIAMOND: Diffusion for World Modeling - Alonso, Jelley, Micheli, Kanervisto, Storkey, Pearce, Fleuret, arXiv 2405.12399 (v1 May 20 2024, v2 Oct 30 2024)
Verified from the abstract page and the arXiv HTML v2 full text. Included as the pixel-space counterpoint and the best verified consumer-GPU anchor.

- Method: diffusion world model in pixel space (deliberately NOT decoder-free: the paper argues compact discrete latents discard visual details that matter for RL, and shows visual detail improves agent performance).
- Results per abstract: Atari 100k mean human-normalized score 1.46, "a new best for agents trained entirely within a world model"; also a CS:GO neural game engine trained on static gameplay.
- Hardware (HTML v2, exact quote): "Each run utilized around 12GB of VRAM and took approximately 2.9 days on a single Nvidia RTX 4090 (1.03 GPU years in total)."
- Why it matters here: it is the strongest published argument that decoder-free latent objectives discard information that can matter, and it is the only 2024-2026 entry in this survey with a fetched, verified, single-consumer-GPU wall-clock figure.

### 2.5 V-JEPA 2 (+ V-JEPA 2-AC) - Assran et al. (30 authors, Meta), arXiv 2506.09985 (Jun 11 2025)
Verified from the abstract page.

- Method: action-free joint-embedding predictive architecture (predict representations of masked spatiotemporal regions in latent space, no pixel decoding) pre-trained on over 1 million hours of internet video; a post-trained action-conditioned variant (V-JEPA 2-AC) adds control.
- Results per abstract: 77.3 top-1 on Something-Something v2, 39.7 recall-at-5 human action anticipation on Epic-Kitchens-100, 84.0 PerceptionTest video QA at 8B scale when aligned with an LLM; V-JEPA 2-AC enables zero-shot planning on Franka arms (pick-and-place toward image goals) trained on "less than 62 hours of unlabeled robot videos from the Droid dataset", with no data from the deployment labs and no task-specific training or reward.
- Hardware: no training-compute details on the abstract page. Pre-training scale (1M+ hours video) is definitionally non-consumer; the reproducible part is the recipe shape (big frozen-ish JEPA encoder + light action-conditioned post-training), not the pre-training.

### 2.6 JEDI: Joint Embedding Diffusion World Model - Lim, Shah, Ikram, Yu, Ma, Leong, Liu; arXiv 2605.13013 (May 13 2026), with an earlier version as "Performance Asymmetry in Model-Based Reinforcement Learning", arXiv 2505.19698 (v1 May 26 2025, v3 Feb 24 2026)
Verified via arXiv API query for "joint embedding diffusion".

- Method: end-to-end latent diffusion world model trained via a JEPA-style denoising loss: diffusion predicts next latents conditioned on past latents and actions, no pixel decoding.
- Claims per the API-returned abstract summaries: cuts VRAM use by 43% versus pixel diffusion while staying competitive on Atari 100k (2605.13013); identifies an Agent-Optimal vs Human-Optimal performance gap in Atari 100k and achieves SOTA on a balanced Sym-HNS metric (2505.19698).
- Hardware: no per-run GPU figures captured this session. The 43% VRAM reduction is the useful consumer-relevant number.

### 2.7 PLSM: Simplifying Latent Dynamics with Softly State-Invariant World Models - Saanum, Dayan, Schulz, arXiv 2401.17835 (v1 Jan 31 2024, v2 Nov 1 2024); surfaced by search as NeurIPS 2024 (venue not in the API abstract)
Verified via arXiv API query.

- Method (the dual direction): Parsimonious Latent Space Model regularizes latent dynamics by *minimizing* MI between latent states and action-induced state changes, making action effects more predictable; combined with prediction, planning, and model-free RL it improves accuracy, generalization, and downstream performance.
- Why it matters: 2024 evidence that the MI machinery cuts both ways: you can maximize MI between state and future observations (contrastive direction) or minimize MI between state and its action-conditional increment (parsimony direction).

### 2.8 Generalization properties of contrastive world models - Ramakrishnan, Cotton, Pitkow, Tolias, arXiv 2401.00057 (v1 Dec 29 2023); NeurIPS 2023 Workshop on Self-Supervised Learning: Theory and Practice
Verified from the abstract page.

- Content: an extensive OOD study of contrastive world models: extrapolation to new object attributes and new attribute conjunctions. Finding: the models "fail to generalize under the different OOD tests"; drops scale with OOD distance; unseen colors, shapes, or color-shape conjunctions break object-representation factorization.
- Why it matters: the sobering negative result for the whole family; contrastive/infomax objectives do not by themselves buy OOD object generalization.

### 2.9 Temporal Consistency Improves Generalization in Contextual Offline Meta Reinforcement Learning - Nakheai, Scannell, Luck, Pajarinen, arXiv 2603.02935 (v1 Mar 3 2026, v2 Sep 7 2026)
Verified from the abstract page.

- Content: for offline meta-RL task inference, critiques both contrastive learning (discriminative task representations that miss task-specific dynamics) and reconstruction (weak at long horizons); enforces multi-step latent temporal consistency, with theory on value-estimation error; MuJoCo, Contextual DeepMind Control, MetaWorld; improves zero-shot and few-shot generalization.
- Why it matters: 2026 evidence that the field is already moving past pure InfoNCE toward multi-step latent consistency objectives, which is exactly the "no pixel decoder" family.

### 2.10 MaxInfoRL: Boosting exploration in reinforcement learning through information gain maximization - Sukhija et al.; surfaced by search as ICLR 2025 (snippet-only: arXiv ID not captured)
- MI used as an exploration reward (information gain about the MDP dynamics) rather than a representation loss; entropy/information-gain interchange balances intrinsic and extrinsic reward; no-regret guarantees in bandits; continuous-control SOTA on hard exploration; JAX code (github.com/sukhijab/maxinforl_jax).
- Included as the complementary MI shape: same quantity, attached to the reward instead of the dynamics objective.

## 3. Lineage before 2024 (brief; all snippet-sourced except CVRL and IRIS/TWM)

- CPC (InfoNCE as an MI lower bound) and Deep InfoMax: the two bound shapes CWM composes.
- CVRL: Contrastive Variational Reinforcement Learning for Complex Observations - Ma, Chen, Hsu, Lee, CoRL 2020 (PMLR 155:959-972, 2021). Verified from the PMLR page: learns "a contrastive variational model by maximizing the mutual information between latent states and observations discriminatively, through contrastive learning"; matches model-based DRL on MuJoCo, outperforms on Natural MuJoCo (dynamic shadows) and box-pushing; code github.com/Yusufma03/CVRL. Note: a search snippet's "5x data efficiency vs Dreamer" claim is NOT on the fetched page; do not repeat it.
- MPR: Data-Efficient RL with Momentum Predictive Representations - Schwarzer, Anand et al., snippet-sourced as arXiv 2007.05929 (Microsoft Research page): multi-step latent self-prediction as an auxiliary loss. This is the exact "momentum prediction" baseline shape CWM (2.1) compares against.
- SPR (Schwarzer et al. 2021) and Ni et al., Understanding Self-Predictive RL, ICLR 2024 (snippet-sourced, arXiv 2306.12456): theory of what keeps self-predictive (negative-free) latent prediction from collapsing, plus a minimalist auxiliary-loss algorithm; the theory backbone for shape 2 below.
- IRIS - Micheli, Alonso, Fleuret, arXiv 2209.00588 (v2 Mar 1 2023): discrete autoencoder + autoregressive transformer world model; Atari 100k mean human-normalized 1.046 from the equivalent of two hours of gameplay (abstract-verified). No GPU model in the abstract (the "single A100" appears only in search snippets).
- TWM - Robine, Höftmann, Uelwer, Harmeling, arXiv 2303.07109 (Mar 13 2023): Transformer-XL world model over compact latents, actions, and rewards; Atari 100k gains (abstract-verified). No wall-clock figure in the abstract.
- IWM: Learning and Leveraging World Models in Visual Representation Learning - Garrido et al. (Meta), snippet-sourced, arXiv 2403.00504 (Mar 1 2024): predicts the effect of global photometric transformations in latent space (JEPA generalized beyond masking); downstream adaptation outperforms comparable masked-image-modeling baselines. The static-image sibling of the video/control entries.

## 4. Method shapes (taxonomy of the 2024-2026 field)

- Shape A, transition infomax (the ask's core): InfoNCE/Deep-InfoMax lower bound between context (state posterior + future actions) and future-observation features, negatives from the batch, log-bilinear or learned critic. Instances: CWM 2609.22175 (local-global: global posterior vs future patch features); CVRL (latent vs observation). Strength: retains predictive information while provably discarding reconstruction detail; weakness: batch-negatives and bound tightness; OOD failure evidence in 2401.00057.
- Shape B, negative-free self-distillation: EMA target encoder + stop-grad predictor, cosine/L2 on latents (MPR, SPR, V-JEPA 2 pre-training, IWM, and CWM's own baseline). Collapse control is theoretical (Ni et al. ICLR 2024) rather than MI-bounded; cheaper than contrastive (no large negative batches) but no explicit MI maximization.
- Shape C, frozen-pretrained-feature prediction: skip representation learning entirely; predict future DINOv2 patch features (DINO-WM) or post-train a huge SSL encoder lightly (V-JEPA 2-AC). The most consumer-friendly shape: the expensive part is inherited.
- Shape D, decoder-free implicit models: no reconstruction and no explicit MI term; latent consistency via reward/value heads and planning (TD-MPC2). Scales to 317M parameters; the strongest planning-first representative.
- Shape E, latent diffusion: denoise in embedding space with a JEPA-style loss (JEDI); handles multimodal futures; 43% VRAM cut vs pixel diffusion per the paper.
- Shape F, MI on the reward channel: information-gain intrinsic rewards (MaxInfoRL); orthogonal and composable with A-E.

## 5. Reproducibility on consumer hardware

Definition used here: a consumer box is a single desktop GPU in the 8-24GB range (RTX 3060 through 4090 class) with 32-128GB system RAM.

Verified hardware facts (fetched this session):

| Paper | Code | Hardware evidence | Consumer verdict |
|---|---|---|---|
| TD-MPC2 | github.com/nicklashansen/tdmpc2 | README: 8GB+ GPU and 12GB+ RAM for single-task online RL; 24GB GPU for the 317M model; 128GB RAM for multi-task offline RL | Single-task runs feasible now; multi-task/317M needs a server |
| DIAMOND | github.com/eloialonso/diamond (MIT, pretrained Atari agents on HF) | Paper v2: ~12GB VRAM, ~2.9 days per Atari 100k run on one RTX 4090 | Feasible on a 12GB+ consumer GPU; slow wall-clock |
| DINO-WM | github.com/gaoyuezhou/dino_wm (MIT, checkpoints + datasets on OSF) | No hardware figures in README or abstract | Cost likely modest (frozen encoder), but that is design inference, not a report |
| CWM (2609.22175) | none found | No hardware numbers at all; footprint is 3 DMC tasks x 1e6 steps x 3 seeds | Plausibly single-GPU by design; NOT stated: OWED |
| JEDI | not checked this session | 43% VRAM cut vs pixel diffusion (API abstract) | Direction favorable; per-run figures OWED |
| V-JEPA 2 | facebookresearch/vjepa2 (snippet-only) | 1M+ hours video pre-training | Pre-training is not consumer-reproducible; recipe shape is |

Design-level cost logic (clearly labeled inference, not reported numbers): dropping the decoder removes both the decode flops and the decoder parameters from every training step (CWM reports the qualitative speedup); moving diffusion or prediction into latent space removes the pixel-space target tensor from memory (JEDI's 43%); freezing a pretrained encoder moves representation-learning cost off your GPU bill entirely (DINO-WM).

Practical recipe for one consumer box, grounded in the above:

1. Atari-100k-scale world model today: DIAMOND is the verified anchor (12GB VRAM, 2.9 days on a 4090). If VRAM is the binding constraint, the JEDI shape (latent diffusion) claims a 43% cut.
2. Continuous control from pixels without a decoder: TD-MPC2 single-task on an 8GB GPU (README-verified), or reimplement CWM's infomax head on a small RSSM; CWM's entire evaluation footprint (3 DMC tasks, 1e6 steps, 3 seeds) is deliberately small-scale and single-GPU-plausible, but it publishes no hardware numbers.
3. Offline planning-style manipulation: DINO-WM shape: frozen DINOv2 + small dynamics head + test-time action-sequence optimization; code and checkpoints are public.
4. Do not plan to train V-JEPA-scale models locally; the consumer role there is checkpoint consumer and action-conditioned post-trainer, not pre-trainer.

## 6. Negative results worth carrying

- Contrastive world models fail systematic OOD tests (new attributes, new conjunctions); unseen colors or shapes break object factorization (arXiv 2401.00057, abstract-verified). MI retention is not OOD generalization.
- Pure contrastive task inference misses task-specific dynamics in offline meta-RL; multi-step latent temporal consistency beats it (arXiv 2603.02935, abstract-verified).
- The pixel-space counterargument is live: DIAMOND shows visual details that compact latents discard can be decision-relevant (Atari 100k MHNS 1.46, abstract + hardware-verified).
- The dual objective (minimize MI between state and action-induced change) improved accuracy and generalization in PLSM (arXiv 2401.17835, API-verified): MI maximization is not automatically the right sign for every factor of the objective.

## 7. OWED / could not verify

- CrIBo as a contrastive world-model paper: NOT FOUND. An arXiv API query for "CrIBo" returns exactly one paper: CrIBo: Self-Supervised Learning via Cross-Image Object-Level Bootstrapping (Lebailly, Stegmüller, Bozorgtabar, Thiran, Tuytelaars, arXiv 2310.07855, ICLR 2024 spotlight, github.com/tileb1/CrIBo). No world-model or contrastive-bound paper named CrIBo exists in that index. My initial recollection of a DeepMind "cross-instance bound objective" world model paper is therefore unverified memory and should be treated as wrong unless a source surfaces.
- CWM (2609.22175): no GPU model, VRAM, wall-clock, or parameter counts published; no venue. Its efficiency claims are qualitative. Hardware reproducibility: OWED.
- DINO-WM training cost on a specific GPU: OWED (nothing in README or abstract).
- V-JEPA 2 pre-training compute (GPU count, hours): OWED (not on abstract page).
- MaxInfoRL arXiv ID: not captured (search rate limits); title/venue/code are snippet-sourced.
- Not fetched, snippet-only one-liners from the final sweep: arXiv 2608.09073 (InfoNCE for action discriminability in latent WMs with monotone planning costs), arXiv 2602.06130 (Self-Improving World Modelling with Latent Actions: encourages high MI in generated futures), arXiv 2410.04940 (next-state prediction yields entangled yet interpretable representations; compares contrastive world models), arXiv 2510.06492 (MI-based diagnostic metric for latent WMs in POMDPs), and an IEEE TAI 2024 contrastive world model for drone navigation (Zhao et al.). Titles and claims unverified beyond snippets.
- Search-backend 429 rate limits hit repeatedly during two sweep rounds; coverage of mid-2025 through 2026 beyond the papers above is best-effort, not exhaustive.

## 8. Snippet-vs-source contradictions found this session (meta-finding)

- "Approximately 3.5 hours on a single RTX 4090" for DIAMOND (a search summary) is contradicted by the paper's own v2 text: about 2.9 days per run at ~12GB VRAM on one RTX 4090. Only the paper's number is real.
- A search summary attributed TWM (arXiv 2303.07109) to "Vintila, Laskin (Mila/Meta)"; the fetched abstract says Robine, Höftmann, Uelwer, Harmeling.
- IRIS's "single NVIDIA A100" appears in search summaries but not in the fetched abstract.
- CVRL's "5x data efficiency vs Dreamer" (search snippet) is absent from the fetched PMLR abstract.
- A search result framed arXiv 2603.02935 as "Contextual Latent World Models" combining InfoNCE; the fetched title is "Temporal Consistency Improves Generalization in Contextual Offline Meta Reinforcement Learning" and its abstract critiques contrastive baselines.
- Lesson (consistent with the repo's own census-denominator law): trust fetched bytes, not search prose. Every load-bearing number above comes from a fetched page.

## 9. Source log (URLs fetched this session and what each grounded)

1. https://arxiv.org/abs/2609.22175 - CWM title, author (Bonnie Li), date, abstract.
2. https://arxiv.org/html/2609.22175v1 - CWM environments (DMC finger-spin/cheetah-run/walker-walk, 1e6 steps, 3 seeds), settings (ball distractors, Kinetics backgrounds), baselines (Dreamer, momentum prediction), Deep-InfoMax-style InfoNCE detail, absence of hardware numbers.
3. https://arxiv.org/abs/2411.04983 - DINO-WM abstract (no reconstruction, DINOv2 patch features, zero-shot planning, six environments).
4. https://github.com/gaoyuezhou/dino_wm - DINO-WM code/checkpoints/tasks, no hardware info.
5. https://arxiv.org/abs/2310.16828 - TD-MPC2 abstract ("implicit (decoder-free) world model", 104 tasks, 317M agent).
6. https://github.com/nicklashansen/tdmpc2 - TD-MPC2 hardware requirements (exact quotes in 2.3).
7. https://arxiv.org/abs/2405.12399 - DIAMOND abstract (Atari 100k MHNS 1.46, CS:GO engine).
8. https://arxiv.org/html/2405.12399v2 - DIAMOND hardware quote (12GB VRAM, 2.9 days, RTX 4090).
9. https://arxiv.org/abs/2506.09985 - V-JEPA 2 abstract (1M+ hours, 62h Droid data, zero-shot Franka).
10. http://export.arxiv.org/api/query?search_query=all:%22CrIBo%22&max_results=20 - the single CrIBo paper (Lebailly et al.), resolving the CrIBo question.
11. http://export.arxiv.org/api/query?search_query=all:%22joint+embedding+diffusion%22&max_results=15 - JEDI 2605.13013 and 2505.19698 entries.
12. http://export.arxiv.org/api/query?search_query=all:%22softly+state-invariant%22&max_results=5 - PLSM 2401.17835 entry.
13. https://arxiv.org/abs/2401.00057 - contrastive world model OOD generalization study.
14. https://arxiv.org/abs/2603.02935 - temporal consistency offline meta-RL paper (true title/authors).
15. https://arxiv.org/abs/2209.00588 - IRIS abstract (MHNS 1.046, two hours of gameplay, no GPU in abstract).
16. https://arxiv.org/abs/2303.07109 - TWM abstract and true authorship.
17. https://proceedings.mlr.press/v155/ma21a.html - CVRL abstract (MI maximization, no 5x claim).
18. https://github.com/eloialonso/diamond - DIAMOND repo (no wall-clock in README; pretrained agents).
