# Model mating paper dig (2026-10-01) — tweet 2105587795318411395 traced to M2N2

Sensing lane receipt. Tweet: https://x.com/thesupermannx/status/2105587795318411395
(@thesupermannx, 2026-10-01 09:17, "AI models can have babies": ATTRACTION / CROSSOVER /
COMPETITION, "better models without a single line of gradient descent"). The tweet carries
no citation; one reply names "Sakana", which is the correct breadcrumb (the code lives under
the SakanaAI org).

## 1. Paper identity (pinned, high confidence)

**"Competition and Attraction Improve Model Fusion"** — João Abrantes, Robert Tjarko Lange,
Yujin Tang. arXiv:2508.16204, submitted 2025-08-22, GECCO 2025 full paper.
Abstract: https://arxiv.org/abs/2508.16204 — full text: https://arxiv.org/html/2508.16204v1
Code (Apache-2.0, SakanaAI org): https://github.com/SakanaAI/natural_niches

Why this is THE paper (each tweet claim maps to an abstract sentence):
- Tweet "ATTRACTION: models seek out other models with complementary strengths" = paper's
  "(3) a heuristic-based attraction metric to identify the most promising pairs of models
  for fusion"; method section: "a desire to choose a model B that performs well in the data
  points where model A performs less well". Source: https://arxiv.org/html/2508.16204v1
- Tweet "CROSSOVER: internal parameters merged at flexible split points" = paper's
  "(1) dynamic adjustment of merging boundaries to progressively explore a broader range of
  parameter combinations" (vs prior fixed parameter partitions). Same source.
- Tweet "COMPETITION: the weakest get culled by a fitness function" = paper's "(2) a
  diversity preservation mechanism inspired by the competition for resources in nature"
  plus archive insertion only "if it outperforms the worst individual" (worst-member
  replacement). Same source.
- Tweet "without a single line of gradient descent" = paper's "for the first time, model
  merging can be used to evolve models entirely from scratch... MNIST classifiers from
  scratch" (evolution vs CMA-ES, both gradient-free). Same source.
- The tweet is a 14-months-late pop-sci recycle of an Aug 2025 paper; the "Sakana" reply
  matches the SakanaAI/natural_niches repo. The all-caps triad ATTRACTION/CROSSOVER/
  COMPETITION is literally the paper's title order rearranged ("Competition and Attraction").

## 2. The exact mechanism (all from https://arxiv.org/html/2508.16204v1)

**Attraction (mate choice).** Parent 1 sampled by fitness. Parent 2 sampled by attraction
score g, Eq. 4: g(A,B) = Σ_j (c_j / (z_j + ε)) · max(s(x_j|B) − s(x_j|A), 0), where s(x_j|θ)
is the per-example score of model θ on training example x_j (task correctness, reward, or
normalized CLIP similarity), c_j is a per-example resource capacity, and z_j is the whole
population's aggregate score on that example. It is complementarity with an economics
filter: B is attractive to A iff B wins exactly where A loses, and the payoff is weighted
toward high-capacity, low-competition examples (rare skills pay more than saturated ones).

**Crossover (dynamic merge boundaries).** Parameters are treated as an ordered sequence.
Sample two scalars per merge: a split position s and a mixing ratio w_m. Eq. 2:
h(A,B,w_m,s) = concat( f_{w_m}(A^{<s}, B^{<s}), f_{1−w_m}(A^{≥s}, B^{≥s}) ) where f is SLERP
between the two parents' parameter sub-arrays before the split, and the complementary mix
after it. One sampled split point per chromosome; in the diffusion experiment, attention
layers merge "independently from the other components" (a multi-chromosome analogy).
Boundaries are NOT predefined layer groups; they are re-sampled every generation, which is
the paper's stated delta over fixed-group merging.

**Competition (fitness + culling).** Implicit fitness sharing: fitness f(θ_i) =
Σ_j s(x_j|θ_i) / (z_j^α + ε) · c_j, with z_j = Σ_k s(x_j|θ_k) the population saturation on
example j, c_j = 1 for binary scores or c_j = max_i s(x_j|θ_i) for rewards in [0,1], and α
tuning competition strength (α=0 disables it, α=1 caps total extractable fitness per
example at its capacity). Culling is worst-member archive replacement: an offspring enters
the archive only if it beats the current worst individual.

## 3. Infrastructure it needs (numbers from https://arxiv.org/html/2508.16204v1)

- MNIST from scratch: 2-layer MLP, 19,210 params; archive of 20; ~1h per method on CPU
  (CMA-ES baseline ~15h). A laptop-tier budget.
- LLM merging: WizardMath-7B-V1.0 x AgentEvol-7B (both Llama-2-7B architecture, 32 layers;
  same-architecture pairs required, no architecture mapper in M2N2). Archive size 15,
  1000 training evaluations total, warm-up of up to 50 random seed merges. Fitness evals:
  GSM8k (1319 train samples) and WebShop (100 train tasks, up to 7 agent steps). Hardware:
  4x H100, ~24h per method. Result: M2N2 avg 63.49 (GSM8k 40.16, WebShop 86.81) vs GA
  60.05, MAP-Elites 60.14, CMA-ES 49.06. So: on the order of a thousand merge candidates
  evaluated to bank one winner at 7B scale, with fitness cost dominating (that cost is what
  MERGE³ attacks separately, https://arxiv.org/abs/2502.10436).
- Diffusion merging: SDXL 1.0, SDXL-DPO, Juggernaut-XL-v9, JSDXL; only U-Nets merged;
  fitness = normalized CLIP similarity on COCO val with Japanese STAIR captions; M2N2 best
  on both FID (13.21) and NCS (84.85). Notably it preserved capabilities "beyond those
  explicitly optimized by the fitness function".

## 4. One-paragraph spec: mapping onto this estate

The estate's breeding pen is the same-architecture subset of the local roster in
configs/lanes.yaml: gemma:2b x another gemma-2b finetune, or (the realistic pen)
qwen2.5-coder:7b x a sibling qwen2.5-7b finetune pulled from Ollama; nomic-embed-text is
not a candidate (different organ). Attraction needs a per-example score matrix s(x_j|θ):
the estate already mints exactly that shape of data — tools/duel_harness.py writes per-ask
win/loss rows to logs/duel/duels.jsonl and tools/animal_profiles.py distills per-animal
behavior into RIB_MODEL_GATES, so fitness = a fixed ask bank (the ask_bank organ) scored
per-example, and g(A,B) = capacity-weighted "B wins where A loses" is computable from that
matrix without any new sensing surface. Merged weights live on disk, not in VRAM: pull
parents as safetensors, do the Eq. 2 split+SLERP in CPU RAM (64GB fits a streamed
per-tensor merge of 7B bf16 parents if tensors are memory-mapped mergekit-style; the RAM
gate law in configs/mates.yaml still applies, free-RAM-minus-2GB), convert the offspring to
GGUF Q4, and import it as an Ollama modelfile under a pen directory (6GB RX 5600 XT, no
CUDA, OLLAMA_MAX_LOADED_MODELS=1 means offspring evals are sequential and slow: budget the
thousand-eval loop at 2B scale first, 7B only as an overnight batch). The honest first
milestone on this box is the paper's own MNIST-from-scratch replication (archive 20, ~1h
CPU) to prove the loop, then qwen2.5-2.5B-class pairs.

## 5. Steal sentences (what M2N2 does that the estate's merge/duel/bank organs do not)

1. The duel harness verdict is terminal: A beats B, the row banks, nothing is combined.
M2N2 makes the duel generative — the per-example A/B score matrix that
logs/duel/duels.jsonl already records IS its attraction input, and the measured pair then
breeds an offspring instead of one side just losing (https://arxiv.org/html/2508.16204v1).
2. The percolator exploit (232,214 self-reinforcements, named an exploit in
configs/mates.yaml's gambiter seed) is precisely what M2N2's implicit fitness sharing caps:
an example pays out at most c_j and its payout decays as population saturation z_j grows,
so saturated examples stop feeding whoever memorized them; no estate organ has an
example-level saturation counter (https://arxiv.org/html/2508.16204v1).
3. The bank organs (mag/thought_bank.py, ask_bank) accumulate per-model performance as
sediment; M2N2's archive with worst-member replacement is the missing selection pressure
that converts banked scores into a next generation — the estate measures animal behavior
everywhere (tools/animal_profiles.py) but never lets those measurements recombine weights
(https://arxiv.org/html/2508.16204v1).

## 6. Runner-up candidates examined and rejected (discriminating evidence)

- "Darwin Family: MRI-Trust-Weighted Evolutionary Merging" arXiv:2605.14386 (2026-05-14,
  https://arxiv.org/abs/2605.14386): training-free evolutionary merging with a 14-dim merge
  genome and block-level recombination, and recursive multi-generation evolution — but no
  attraction metric (mate choice is absent from the abstract) and no from-scratch
  evolution; it is the same family, newer, not the tweeted one.
- "Nature-Inspired Population-Based Evolution of LLMs" (GENOME) arXiv:2503.01155
  (2025-03-03, https://arxiv.org/abs/2503.01155): population + weight crossover + no
  gradients, up to 40 LLMs — but crossover is plain weight merging with no dynamic split
  boundaries and no attraction pairing.
- "Mergenetic" arXiv:2505.11427 (https://arxiv.org/abs/2505.11427), "Evolutionary
  Optimization of Model Merging Recipes" (Sakana) arXiv:2403.13187
  (https://arxiv.org/abs/2403.13187), "EvoMerge" arXiv:2402.00070
  (https://arxiv.org/abs/2402.00070), "PopuLoRA" arXiv:2605.16727
  (https://arxiv.org/abs/2605.16727), "GeLaCo" arXiv:2507.10059
  (https://arxiv.org/html/2507.10059v2): each lacks at least two of the tweeted triad
  (attraction-by-complementarity, flexible split points, fitness culling without training).

## 7. Receipt

- Sensing lane, banked as findings, no done-work claim, no git commit, no INDEX.json
  promotion (promotion is the switchboard's call per watch/inbox/SHARED_SURFACE_CONTRACT.json).
- Tweet read via https://x.com/thesupermannx/status/2105587795318411395 (no citation in
  tweet or visible replies; the "Sakana" reply was the only breadcrumb).
- Every paper claim above traces to https://arxiv.org/abs/2508.16204 or
  https://arxiv.org/html/2508.16204v1; repo facts to https://github.com/SakanaAI/natural_niches.
- Estate facts trace to configs/lanes.yaml, configs/mates.yaml, tools/animal_profiles.py,
  tools/duel_harness.py, mag/thought_bank.py in this repo.
