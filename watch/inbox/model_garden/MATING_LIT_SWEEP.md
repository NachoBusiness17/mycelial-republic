# MATING_LIT_SWEEP - STEAL-2 (THE PREMISE'S LITERATURE)

Lane: STEAL-2 refire (prior provider-killed lane left no partial file; this is the full sweep, not an extension).
Date: 2026-10-01. Instrument: web search + arXiv abstract fetches (urls cited per row). No local PDFs pulled;
abstract-level evidence only, flagged where deeper reading is needed.
Premise under test: population fusion of small local models. Anchor: arXiv:2508.16204 (M2N2, GECCO 2025).
Downstream consumer: memory/plans/mate_moe_v0/EXPERIMENT.md (mated-models-as-MoE export falsifier, STAGED NOT RUN),
staged from watch/inbox/hermes_burn/DG1_moe_mating_door.md.

Sweep scope: (1) merging-as-reproduction; (2) evolutionary model search at scale; (3) MoE-from-merging incl. work
since Oct 2026 began; (4) weight transfer without training across lineages; (5) mating as communication
(weights as heritable message between agents).

Counts: 34 entries swept, 24 at full-abstract depth (fetched and read), 10 lighter mentions (search-snippet depth,
marked LIGHT). Verdict vocabulary: CONFIRMS-OUR-PREMISE / EXTENDS-IT (concretely for MATE_MOE_v0) / SCOOPS-IT
(what they did first, what remains ours) / ORTHOGONAL.

## TIMELINE (earliest to newest)

Pre-window anchors (2024, already known to the estate, re-verified here):

- 2024-03  Branch-Train-MiX (BTX), Sukhbaatar et al., Meta, arXiv:2403.07816. Branch a seed, train specialists
  async, stack FFNs as MoE experts, train the router. The estate's DG1 verdict already flags it; still the root
  of the MoE-from-specialists lineage.
- 2024-03  MergeKit + mergekit-moe, Godey et al., arXiv:2403.13257 (EMNLP 2024 Industry), docs
  github.com/arcee-ai/mergekit (moe.md, evolve.md). Tooling root: dense->MoE via hidden-state gates, no router
  training required; CMA-ES merge-recipe search.
- 2024-03  Evolutionary Model Merge, Akiba et al., arXiv:2403.13187, published Nature Machine Intelligence
  (nature.com/articles/s42256-024-00975-8). Recipe-space (layer-wise coefficient) evolution across data space
  and parameter space; the mergekit-evolve lineage root.
- 2024-08  Flexible and Effective Mixing of LLMs into a Mixture of Domain Experts, Lee/Wynter/Ganti (IBM),
  arXiv:2408.17280. Toolkit building MoE-of-domains from trained models incl. without router training; the
  academic sibling of mergekit-moe.

Window (2025-2026):

- 2024-10 (ICLR 2025)  Layer Swapping, Bandarkar et al., Google DeepMind, arXiv:2410.01335. Training-free
  layer-index-granularity crossover: swap depth-banded layers between an English-finetuned model and a
  multilingual base -> zero-shot cross-lingual transfer. First mainstream LAYER-STRUCTURE crossover between
  same-family LLMs.
- 2025-01  ToMoE, Gao et al., arXiv:2501.15316 (v2 2026-01). Dense->MoE via dynamic structural pruning; MLP
  sublayers become experts inside ONE model, no permanent deletion, outperforms pruning baselines WITHOUT
  fine-tuning across Phi-2/Llama-2/Llama-3/Qwen-2.5. Self-donation, not two-parent mating.
- 2025-02  MergeME, arXiv:2502.00997, NAACL 2025 Main. Merging homogeneous and heterogeneous MoEs into one;
  parameter-interference mitigation + routing heuristics to avoid router fine-tuning. MoE->MoE direction.
- 2025-02 (ECML-PKDD 2024)  Model Fusion via Neuron Transplantation, Oez et al., arXiv:2502.06849. Prune a base
  net, transplant important neurons from all ensemble members, brief fine-tune; beats OT-fusion on fusion cost.
  Vision-ensemble scale, not LLM; neuron-granularity grafting prior art.
- 2025-03  Nature-Inspired Population-Based Evolution of LLMs (PopEvolution), Zhang et al., arXiv:2503.01155,
  ACL 2026 long (aclanthology.org/2026.acl-long.2044). THE population framing: 10 gemma-2-2b-it parents,
  populations up to 40, four operators (crossover = merging parent weights, mutation = random weight perturbation,
  selection, succession = experience transfer parent->offspring), 12 datasets, up to +54.8 pct over best initial
  parent, 200-sample adaptation, single RTX 4090, gradient-free.
- 2025-03  A Review of Model Merging Approaches, arXiv:2503.08998. Survey; codifies that same-init branches show
  linear mode connectivity while different-pretraining-run models do not (baseline for area 4).
- 2025-05  Mergenetic, arXiv:2505.11427, ACL 2025 Demo (aclanthology.org/2025.acl-demo.55). Open-source
  evolutionary merging library; key idea: cheap partial evaluation (proxy fitness) makes the EA loop affordable.
- 2025-06 (CVPR 2025)  PLeaS - Merging Models with Permutations and Least Squares, CVPR 2025 poster 33794.
  Same-architecture merging via permutation + least-squares layer maps; area-4 alignment toolbox. LIGHT.
- 2025-08  M2N2 - Competition and Attraction Improve Model Fusion, Abrantes et al., Sakana AI, arXiv:2508.16204,
  GECCO 2025 (DOI 10.1145/3712256.3726329). OUR ANCHOR: gradient-free evolutionary fusion where merging METHODS
  compete and similar individuals cluster (attraction) before fusion.
- 2025-08  Chain of Merges (CoM), arXiv:2508.21421. Layer-wise sequential merging that preserves inter-layer
  dependency; one-shot layer-mixing breaks it. Caution tale for any layer-granularity mating.
- 2025-10  Efficient Compression of MoE via Expert Output Merging, arXiv:2510.14436. Reverse direction
  (MoE->dense via expert merging). LIGHT.
- 2025-11  A Systematic Study of In-the-Wild Model Merging, arXiv:2511.21437. Wild fine-tuned checkpoints merge
  without training; field evidence the no-training regime is real. LIGHT.
- 2026-01  ARM - Role-Conditioned Neuron Transplantation for Training-Free Generalist LLM Agent Merging,
  arXiv:2601.07309. Activation-guided, role-conditioned neuron transplant merges role-specialized agents
  (planner/coder/searcher) into one generalist, training-free; strongest balanced merge among training-free
  baselines. Merging AGENTS (their roles), not populations.
- 2026-01  A Unified Generalization Framework for Model Merging, arXiv:2601.21690. Theory. LIGHT.
- 2026-02  MERGE - Fine-Grained Model Merging via Modular Expert Recombination, Qiu/Wu/Feng/Tan,
  arXiv:2602.06552. Component-level (attention + MLP) recombination of finetuned models; bi-objective
  (accuracy vs storage) surrogate-assisted EA finds Pareto merge configs; output is a reusable modular expert
  library + lightweight routing network selecting components per input at inference. Component-mating + routing.
- 2026-03  Model Merging in the Era of LLMs (FUSE survey), Song/Zheng, arXiv:2603.09938. Foundations /
  Unification / Scenarios / Ecosystem; evolutionary optimization and MoE are now standard axes of the field.
- 2026-03  CNT - Safety-Oriented Function Reuse across LLMs via Cross-Model Neuron Transfer, arXiv:2603.18449.
  Post-hoc transfer of safety-specific neurons across different LLMs; graftable functionality at neuron
  granularity. LIGHT.
- 2026-04  BAR - Train Separately, Merge Together: Modular Post-Training with MoE, Morrison et al., Ai2,
  arXiv:2604.18473. Independently FULL-pipeline-trained experts (mid-train + SFT + RL) composed into one MoE
  with only lightweight router training at merge time; 7B, avg 49.1 over 7 categories vs monolithic retraining
  47.8 (no mid-train) / 50.5 (with); linear vs quadratic update cost; anchor-expert trick keeps experts
  heterogeneous-but-compatible. FlexOlmo lineage. STRONGEST SCOOPER of the MoE-export door.
- 2026-04  REAM - Merging Improves Pruning of Experts in LLMs, arXiv:2604.04356. Expert grouping/merging as
  compression. LIGHT.
- 2026-05  TFlow - Good Agentic Friends Do Not Just Give Verbal Advice: They Can Update Your Weights,
  Bao et al., arXiv:2605.13839. "Weight-space communication": frozen sender agents compile hidden states into
  transient, receiver-specific low-rank (LoRA-style) perturbations applied only during the receiver's generation.
  3x Qwen3-4B: up to +8.5 acc over standalone receiver, -83.27 pct tokens and 4.6x faster vs text-based
  3-agent debate. FIRST paper treating weights as a communication channel between agents.
- 2026-06  Scaling Linear Mode Connectivity to Billion-Parameter Pretrained Transformers, Li/Shen,
  arXiv:2606.23607 (code VILA-Lab/Dual-Learned-Matching). Dual-learned functionality-preserving transformations
  align INDEPENDENTLY PRETRAINED billion-param models; near-zero loss barriers along the interpolation path
  (WikiText) and small barriers for modern billion-param LLMs. Cross-pretraining-run mating is now demonstrated.
- 2026-06  HARC - When Model Merging Breaks Routing: Training-Free Calibration for MoE, Huang et al.,
  arXiv:2606.03391. Names "routing breakdown": merged routers misdispatch because softmax/Top-k routing is
  fragile under parameter perturbation; fix is training-free Hessian-aware router calibration (closed-form,
  matrix-free CG). Direct falsifier hygiene for any merged-router design.
- 2026-07  Model Merging as Probabilistic Inference in Fine-Tuning, arXiv:2607.01689. Theory. LIGHT.
- 2026-07  Co-Harness - Co-Evolving Harnesses and Model Weights for LLM Agents, arXiv:2607.22688. Jointly
  optimizes agent harness + weights in post-training; weights as co-evolving heritable trait, single-agent. LIGHT.
- 2026-07  Are we Merging the Right Models? Impact of Expert Training Duration, Kozodoi et al.,
  arXiv:2607.11997. Merge outcome depends on HOW LONG parents were trained, method-dependently: averaging
  degrades on overfit experts, sparsification-based methods (TIES-family) prefer experts trained well past the
  validation optimum (bias-variance / random-forest analogy). Parent selection is a first-class variable.
- 2026-09  The Evolution of Sex for Artificial Intelligence, Gilestro, arXiv:2609.18560 (cs.LG, cs.NE,
  q-bio.PE; code "MachineSex" on author GitLab). Population-genetics framework for multigenerational model
  populations: retraining-on-output = drift/model collapse; learner-retained-on-parent = exact Wright-Fisher;
  real data = immigration (absolute count matters, not share); output-averaging = blending inheritance
  (Jenkin's objection, kills multi-parent benefit); keeping each parent's strongest contribution = Fisher-Muller
  effect (merged LLM specialists beat every parent); lineages that learned conflicting conventions become
  REPRODUCTIVELY ISOLATED (cannot merge). Tested on exact inheritance models, RNN/FFN/VAE, and LLMs. Two weeks
  old at sweep time.
- 2026-09  From Parameters to Behaviors: A Survey of Model Fusion, Cai et al., arXiv:2609.19553, Findings of
  EMNLP 2026. Parameter-level / representation-level / behavior-level taxonomy; notes HF passed 2M models
  June 2026 (the gene pool is real and growing).
- 2026 (ICML 2026)  Skill-Based / Symbolic MoE, openreview.org/forum?id=RYrFUkraWM. Routing between existing
  pretrained LLMs. The "ensemble in disguise" form DG1 already killed for us. LIGHT.
- 2026 (ACL 2026 Industry)  Mixture of Heterogeneous Grouped Experts, aclanthology.org/2026.a-industry.20.
  Training-time heterogeneous expert sizes. LIGHT.
- 2026 (ACL 2026 Findings)  Token-Level Skill-Compositional Sparse MoE, aclanthology.org/2026.findings-acl.606.
  Independently trained experts merged into one token-level sparse MoE; BTX lineage continuation. LIGHT
  (snippet depth; read before citing in a paper).

Where OUR contribution sits on this line: the premise's three components have each been separately claimed by
2026-09: population framing (PopEvolution 2025-03, M2N2 2025-08, Evolution of Sex 2026-09), MoE-export-of-
specialists (BTX 2024-03 -> mergekit-moe 2024-03 -> BAR 2026-04 -> MERGE 2026-02), and weights-as-communication
(TFlow 2026-05, transient only). The UNOCCUPIED cell as of 2026-10-01 is their intersection under local
constraints: fitness-selected wild parents (not hand-branched specialists), TRAINING-FREE verbatim-FFN MoE export
with a router initialized from the parents' fitness tasks (selection information reused as routing calibration),
at sub-1B scale on CPU/6GB-Vulkan runtimes, with weights framed as a HERITABLE message (persistent lineage, not
TFlow's transient perturbation). Nobody in the sweep occupies that cell; BAR is one router-training step away
from it at 7B in the datacenter.

## VERDICT TABLE

| # | Paper (arXiv/venue/year) | One-line finding | Verdict |
|---|---|---|---|
| 1 | BTX (2403.07816, 2024) | Branched specialists' FFNs stack into MoE with router training; the door is pre-built | CONFIRMS-OUR-PREMISE (estate prior art, re-verified) |
| 2 | MergeKit / mergekit-moe (2403.13257, EMNLP 2024 Ind.) | Dense->MoE from same-base models via hidden-state gates, zero router training; also CMA-ES recipe evolution | CONFIRMS-OUR-PREMISE (MATE_MOE_v0's B build tool; DG1 UNVERIFIED flags now closed by docs + paper) |
| 3 | Evolutionary Model Merge (2403.13187, Nat. Mach. Intell. 2024) | EA over layer-wise merge coefficients finds cross-model compositions humans miss | CONFIRMS-OUR-PREMISE (evolution is a legitimate merge optimizer) |
| 4 | MoD toolkit (2408.17280, 2024) | MoE-of-domains from trained models incl. without router training | CONFIRMS-OUR-PREMISE |
| 5 | Layer Swapping (2410.01335, ICLR 2025) | Training-free depth-banded layer crossover transfers capability zero-shot between same-family models | EXTENDS-IT: layer-structure crossover is real prior art; MATE_MOE_v0's shared-merge of attention is a coarser cousin |
| 6 | ToMoE (2501.15316, 2025) | Dense model's own MLP sublayers become routed experts with no fine-tuning | EXTENDS-IT: proves training-free MoE conversion viable in ONE model; supports feasibility of B's no-training export |
| 7 | MergeME (2502.00997, NAACL 2025) | MoE+MoE merging needs interference mitigation and routing heuristics or routers misbehave | EXTENDS-IT: merged-router fragility is documented in the MoE-MoE direction too |
| 8 | Neuron Transplantation (2502.06849, ECML-PKDD 2024) | Prune-then-graft important neurons from ensemble members beats OT-fusion on cost | EXTENDS-IT: neuron-granularity grafting prior art (vision scale, needs brief fine-tune) |
| 9 | PopEvolution (2503.01155, ACL 2026) | LLM POPULATION evolves by weight crossover + mutation + selection + succession on one 4090 at 2B, +54.8 pct over best parent | SCOOPS-IT: they did population-evolution of small LLMs via weight crossover first. REMAINS OURS: offspring are DENSE merges (no MoE export, no structure-aware mating), no fitness-calibrated router, no local-runtime sovereignty framing, no communication semantics |
| 10 | Review of Model Merging (2503.08998, 2025) | Same-init branches are linearly mode connected; different runs are not | CONFIRMS-OUR-PREMISE (the same-base gate has a theoretical warrant) |
| 11 | Mergenetic (2505.11427, ACL 2025 Demo) | Cheap partial fitness evaluation makes evolutionary merging affordable | EXTENDS-IT: our population fitness loop should use proxy evaluation, not full benchmarks |
| 12 | PLeaS (CVPR 2025) | Permutation + least-squares layer maps merge same-arch models | EXTENDS-IT: area-4 toolbox (LIGHT) |
| 13 | M2N2 (2508.16204, GECCO 2025) ANCHOR | Method competition + attraction clustering improve gradient-free fusion | CONFIRMS-OUR-PREMISE (the estate anchor; field's own marker that fusion is evolutionary) |
| 14 | Chain of Merges (2508.21421, 2025) | Sequential layer-wise merging preserves inter-layer dependencies one-shot merging breaks | EXTENDS-IT: warns that mixing components across parents can break depth coupling; relevant to shared-attention merge in artifact A/B |
| 15 | MoE compression via expert output merging (2510.14436, 2025) | Merging experts compresses MoEs (reverse direction) | ORTHOGONAL (LIGHT) |
| 16 | In-the-Wild Merging study (2511.21437, 2025) | Wild checkpoints merge without training at scale | CONFIRMS-OUR-PREMISE (LIGHT) |
| 17 | ARM (2601.07309, 2026) | Role-specialized LLM AGENTS merge into a generalist via activation-guided neuron transplant, training-free | EXTENDS-IT: nearest neighbor to "mating agents"; ours differs by FFN-expert export + routing instead of dense transplant, and by population context |
| 18 | Unified Generalization Framework (2601.21690, 2026) | Theory unifying when merging generalizes | ORTHOGONAL (LIGHT) |
| 19 | MERGE (2602.06552, 2026) | EA finds component-level (attn+MLP) recombination; modular expert library + learned lightweight routing beats static merging | EXTENDS-IT, and partially SCOOPS the "recombination + routing" combination: theirs is component-merged library with learned routing and a storage objective. REMAINS OURS: verbatim parent FFNs (no component merging), fitness-initialized router, training-free build, population framing |
| 20 | FUSE survey (2603.09938, 2026) | Merging field consolidates; evolution and MoE are standard axes | CONFIRMS-OUR-PREMISE (field-level) |
| 21 | CNT (2603.18449, 2026) | Safety functionality transfers across DIFFERENT LLMs by moving specific neurons post-hoc | EXTENDS-IT: graftable functionality across families (LIGHT) |
| 22 | BAR (2604.18473, Ai2 2026) | Independently full-pipeline-trained experts compose into one MoE with only lightweight router training; matches monolithic retraining at 7B | SCOOPS-IT (the mated-models-as-MoE door at datacenter scale): they did specialist-models->MoE first at 7B. REMAINS OURS: training-free export (BAR trains the router + uses anchor-expert adaptation during expert training), wild fitness-selected parents vs hand-branched experts, router init from the selection fitness itself, sub-1B local CPU/6GB runtime and quantized rerun |
| 23 | REAM (2604.04356, 2026) | Merging improves expert pruning | ORTHOGONAL (compression direction, LIGHT) |
| 24 | TFlow (2605.13839, 2026) | Agents communicate by compiling sender hidden states into transient receiver-specific LoRA perturbations; big token/time savings vs text debate | SCOOPS-IT (the concept "weights as communication channel"): they named and built weight-space communication first. REMAINS OURS: HERITABILITY - theirs is transient, instance-level, sender-compiled by a learned generator with a fixed known receiver; no lineage, no generations, no population genetics, no persistent offspring |
| 25 | Scaling LMC (2606.23607, 2026) | Independently pretrained billion-param models align to near-zero loss barriers via dual-learned matching | EXTENDS-IT: the same-base gate is a TODAY constraint, not a law; cross-family mating is becoming feasible via alignment |
| 26 | HARC (2606.03391, 2026) | Merged routers suffer "routing breakdown"; training-free Hessian-aware calibration fixes it | EXTENDS-IT, falsifier-critical: our "router not specializing" KILL may be a calibration artifact with a known training-free remedy |
| 27 | Probabilistic-Inference merging (2607.01689, 2026) | Merging as inference in fine-tuning theory | ORTHOGONAL (LIGHT) |
| 28 | Co-Harness (2607.22688, 2026) | Agent harness and weights co-evolve in post-training | ORTHOGONAL-adjacent to area 5 (single-agent co-evolution, no exchange) |
| 29 | Are we Merging the Right Models? (2607.11997, 2026) | Parent training duration interacts with merge method; TIES-family wants overtrained experts | EXTENDS-IT: parent state is a first-class variable for our gate check and for interpreting A-vs-B outcomes |
| 30 | Evolution of Sex (2609.18560, 2026) | Population genetics transfers near-wholesale to model populations; Fisher-Muller confirmed for merged specialists; conflicting conventions -> reproductive isolation | CONFIRMS-OUR-PREMISE at theory level, and EXTENDS-IT: gives the MATE_MOE_v0 gate check (same-base + FFN divergence) a mechanistic justification and predicts our failure mode (isolation by convention conflict, not drift) |
| 31 | Parameters-to-Behaviors survey (2609.19553, EMNLP 2026 Find.) | Fusion field map at 3 levels; 2M+ models on HF | CONFIRMS-OUR-PREMISE (the gene pool exists and is catalogued) |
| 32 | Skill-based symbolic MoE (ICML 2026) | Routing between existing whole LLMs | ORTHOGONAL (the ensemble-in-disguise form; LIGHT) |
| 33 | Heterogeneous Grouped Experts (ACL 2026 Ind.) | Heterogeneous expert sizes at training time | ORTHOGONAL (LIGHT) |
| 34 | Token-Level Skill-Compositional Sparse MoE (ACL 2026 Find.) | Independently trained experts -> token-level sparse MoE | EXTENDS-IT (BTX lineage continuation; LIGHT, read before further use) |

## THE 3 PAPERS MATE_MOE_v0's FALSIFIER MUST ACCOUNT FOR

1. BAR (arXiv:2604.18473, Ai2, 2026-04). The door it tests is proven at 7B with one concession: lightweight
   router training. Consequence for the falsifier: MATE_MOE_v0 no longer tests "does the door exist"; it tests
   whether the TRAINING-FREE, fitness-calibrated variant holds. Account for it by (a) recording in VERDICT.md
   that a BAR-style router-training arm is the known-good fallback if the training-free router fails, and
   (b) treating "router is not specializing" as a kill of the TRAINING-FREE ROUTER INIT, not of the mating->MoE
   door itself (the door has BAR-grade evidence). DEVIATION-shaped decision for the operator at GO.
2. HARC / When Model Merging Breaks Routing (arXiv:2606.03391, 2026-06). Routing breakdown is the named,
   documented failure mode of merged routers, with a training-free second-order calibration fix. The falsifier's
   KILL "router is not specializing" can fire for a calibration reason the experiment would otherwise misread
   as a door death. Account for it by logging per-layer router-logit statistics on the eval slices (already
   implied by output_router_logits=True) and, if usage is flat, noting in the receipt that HARC-style
   recalibration is the indicated next probe before any "door dead" claim.
3. PopEvolution (arXiv:2503.01155, ACL 2026). It owns "population of small LLMs evolving by weight crossover on
   one consumer GPU" (+54.8 pct over best parent at 2B). Account for it by scoping MATE_MOE_v0's claimed novelty
   in the receipt to the EXPORT FORM (training-free FFN-verbatim MoE + fitness-initialized router + local
   quantized runtime), never to population evolution itself; and steal its operating point (2B parents, single
   4090, proxy fitness per Mergenetic) for the feed-rerun leg sizing.

Honorable mentions for the gate check (fold into step 0 reasoning, no design change): Are we Merging the Right
Models (2607.11997) - parent training state interacts with merge method; Evolution of Sex (2609.18560) -
reproductive isolation is caused by conflicting conventions, which is exactly what the FFN-cosine gate is
screening for.

## PUNCHLINES

- Timeline direction: the field is CONVERGING ON our premise, from three directions simultaneously
  (population framing: M2N2 GECCO 2025 -> PopEvolution ACL 2026 -> Evolution of Sex 2026-09; MoE-from-merging:
  BTX/mergekit-moe 2024 -> MERGE 2026-02 -> BAR 2026-04; weights-as-channel: TFlow 2026-05). Two 2026 surveys
  now list evolutionary optimization and MoE as standard merging axes. The window for "we frame model fusion as
  sex" as a novel claim closed in 2025; the window for the specific intersection (training-free, fitness-
  calibrated, local-runtime, heritable) is open but narrowing - BAR is one router-training step away at 7B.
- Weights-as-communication: exactly ONE paper does it - TFlow (2605.13839) - and it is transient, instance-level,
  and receiver-specific (sender compiles a LoRA perturbation consumed during one generation). NO paper in the
  sweep treats weight exchange as a HERITABLE message between agents (persistent offspring, lineage, generations).
  The operator's "mating as communication" framing survives TFlow precisely at the heritability boundary.
  Federated learning ships weights between parties but as transport under a global objective, not as message
  semantics between sovereign agents.

## SOURCES (primary fetches, 2026-10-01)

arxiv.org/abs/2508.16204, 2609.18560, 2502.06849, 2601.07309, 2501.15316, 2602.06552, 2603.09938, 2604.18473,
2606.03391, 2605.13839, 2503.01155, 2607.11997, 2606.23607, 2408.17280, 2609.19553, 2403.07816, 2403.13257,
2502.00997 (aclanthology.org/2025.naacl-long.117), 2505.11427 (aclanthology.org/2025.acl-demo.55),
2410.01335, 2508.21421, 2604.04356, 2510.14436, 2511.21437, 2601.21690, 2607.01689, 2607.22688, 2503.08998;
aclanthology.org/2026.acl-long.2044; openreview.net/forum?id=RYrFUkraWM; cvpr.thecvf.com/virtual/2025/poster/33794;
allenai.org/blog/bar; sakana.ai/evolutionary-model-merge and sakana.ai/m2n2; nature.com/articles/s42256-024-00975-8;
github.com/arcee-ai/mergekit (docs/moe.md, docs/evolve.md); LIGHT rows verified via search snippets only.
