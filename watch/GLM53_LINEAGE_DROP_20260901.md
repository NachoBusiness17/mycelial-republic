# GLM-5.3-Flash LINEAGE DROP — operator-authored, 2026-09-01 06:47Z
authority: operator-authored (verbatim drop, primary-source bibliography attached)
purpose: full-blown salon input — lineage dissection of GLM-5.3-Flash; feeds Phase 5, probes, salon lanes A–E

## Bottom line

GLM-5.3-Flash is not publicly described as a compressed or distilled GLM-5. Z.AI says it began from a newly trained base model with a redesigned architecture and training recipe. The disclosed model is:

- 320B total parameters, 18B active
- native multimodal from pretraining
- trained on a stated 30T-token multimodal corpus
- hybrid sparse-attention + linear-attention architecture
- 1M-token context
- designed for coding, tools, agents, and lower serving cost

The exact Flash dataset mixture, optimizer schedule, teacher models, RL runs, compute budget, and safety-tuning recipe remain undisclosed. The closest detailed evidence is the GLM-5 family technical report, which should be treated as lineage evidence—not proof that every number or procedure applies identically to Flash. [Z.AI's Flash release](https://autoclaw.z.ai/blog/model/glm-5.3-flash/), [official model card](https://huggingface.co/zai-org/GLM-5.3-Flash), [GLM-5 technical report](https://arxiv.org/html/2602.15763)

## What is directly documented about Flash

Z.AI reports that Flash was trained from a new base model and that both its architecture and training recipe were redesigned for capability per unit of compute. It is the first natively multimodal model in the GLM-5 family: text, images, video, and files are trained together rather than bolted on later through a separate vision adapter. [Official Flash release](https://autoclaw.z.ai/blog/model/glm-5.3-flash/)

Its stated architecture combines:

- sparse attention for selective global access;
- linear/recurrent attention for local and state-like modeling;
- mHC, a stabilization method for deep networks;
- an indexer and `IndexPool` to compress cached key information.

Z.AI claims roughly 3× lower attention computation than GLM-5 and about 4.4× lower KV-cache usage. These are vendor-reported engineering results, not yet an independently reproduced audit. [Official Flash release](https://autoclaw.z.ai/blog/model/glm-5.3-flash/)

Z.AI also reports that an anonymous pre-release version was evaluated under real traffic as "Ox Alpha," with serving performed on Chinese AI accelerators. That is separate from GLM-5's anonymous "Pony Alpha" deployment. [Flash release](https://autoclaw.z.ai/blog/model/glm-5.3-flash/), [GLM-5 report](https://arxiv.org/html/2602.15763)

## What the training materials appear to contain

### Flash-specific evidence

The only public Flash-specific corpus statement I found is Z.AI's "latest 30T-token multimodal corpus." They do not publish its percentages, licenses, source-by-source volume, filtering rules, or exact sequence schedule. [Flash release](https://autoclaw.z.ai/blog/model/glm-5.3-flash/)

So we can safely say the material includes multimodal training data, but we cannot honestly claim that it contains a particular percentage of books, GitHub, Common Crawl, synthetic data, or proprietary conversations.

### GLM-5 family evidence

The GLM-5 report gives the nearest detailed picture of Z.AI's data engineering:

- web text filtered with quality classifiers, sentence embeddings, and a world-knowledge classifier;
- code from code-hosting snapshots, web pages containing code, and Software Heritage metadata;
- books, papers, scientific pages, and technical documents;
- long-context documents filtered for quality, deduplication, length, and knowledge coverage;
- repository-level software-engineering data linking issues, pull requests, commits, diffs, and relevant source files;
- synthetic long-context examples and agent trajectories;
- executable environments where the model must install software, use tools, edit files, run tests, and produce a verifiable result.

The report specifically describes approximately 10 million issue–PR pairs and roughly 160B unique tokens in that issue–PR component. Again, that is GLM-5-family evidence, not a Flash-specific disclosure. [GLM-5 technical report](https://arxiv.org/html/2602.15763)

## How the tuning/post-training works

The family report describes a staged pipeline:

```text
base pretraining
 ↓
mid-training / context extension / software engineering
 ↓
supervised fine-tuning
 ↓
reasoning reinforcement learning
 ↓
agentic reinforcement learning
 ↓
general reinforcement learning
 ↓
cross-stage distillation and regression checks
```

### Supervised fine-tuning

The SFT data is divided into:

- general chat: writing, translation, roleplay, multi-turn dialogue, long-context interaction;
- reasoning: mathematics, science, logic, and programming;
- coding and agents: repository work, frontend/backend development, tool calling, search, and computer-use-like tasks.

A notable design is that incorrect execution segments can be retained but masked from the loss. That teaches the model to recognize and correct bad actions without directly reinforcing them.

The report also describes preserving thinking blocks across turns and before tool calls, which is important for coding agents: the model learns that a tool invocation is part of an ongoing trajectory, not an isolated answer. [GLM-5 technical report](https://arxiv.org/html/2602.15763)

### Reasoning RL

The reasoning stage uses verifiable tasks in mathematics, science, programming, and tool use. Rewards are based on whether the outcome is correct, not merely whether the explanation sounds convincing.

The report mentions:

- GRPO-style reinforcement learning;
- IcePop-style handling of training/inference mismatch;
- open math and science datasets;
- Codeforces, TACO, and synthetic competitive-programming tasks;
- internally constructed scientific coding tasks;
- external annotation vendors;
- stronger teacher models used to identify problems that weaker GLM models fail but stronger systems can solve.

This is the "make it think better" stage, but it is not the whole agent recipe. [GLM-5 technical report](https://arxiv.org/html/2602.15763)

### Agentic RL

This is the most relevant part for our Mag/OpenClaw work. The report describes more than 10,000 real-world software, terminal, and search environments, with more than 1,000 concurrent rollouts.

The system:

- separates rollout generation from training;
- preserves exact token/action correspondence with Token-in-Token-out;
- tracks policy versions and filters stale trajectories;
- drops environment-collapse failures;
- routes multi-turn work to preserve KV-cache locality;
- uses task-specific microservices;
- standardizes every trajectory into a unified message-list format;
- monitors task progress and generation speed.

That is remarkably close to our desired "board → switchboard → effect broker → receipt" model. The analogy is ours, not Z.AI's: both systems treat agents as workers producing auditable trajectories rather than treating a model response as the final unit of truth.

### General RL

The final general-RL stage balances:

- rule-based rewards;
- outcome reward models;
- generative reward models;
- human-authored anchor responses;
- correctness, helpfulness, emotional intelligence, and style.

The use of human-written anchors is specifically intended to prevent the model from becoming excessively formulaic, verbose, or model-like. [GLM-5 technical report](https://arxiv.org/html/2602.15763)

## Previous versions and what they contributed

```text
GLM 2021
 → GLM-130B 2022
 → GLM-4.x / GLM-4.5
 → GLM-5
 → GLM-5.3-Flash
```

### GLM

The original GLM research introduced autoregressive blank infilling: instead of only predicting the next token, the model reconstructs missing spans in arbitrary orders using two-dimensional positional information. This gave the family a flexible pretraining foundation combining generative and understanding behavior. [GLM paper](https://arxiv.org/abs/2103.10360)

### GLM-130B

GLM-130B established the family as a large bilingual open model and emphasized practical quantized deployment. The paper demonstrated INT4 operation on consumer GPU configurations, which is part of the family's longer-running "large model, constrained hardware" identity. [GLM-130B paper](https://arxiv.org/abs/2210.02414)

### GLM-4.5

GLM-4.5 introduced the explicit ARC target: agentic, reasoning, and coding capabilities in one model. It used an MoE design with 355B total and 32B active parameters, multi-stage training, expert-model iteration, and reinforcement learning.

There is a small public accounting discrepancy worth preserving in our notes: the GLM-4.5 report describes 23T tokens across multi-stage training, while the Z.AI documentation summarizes 15T tokens for initial general-domain pretraining followed by targeted fine-tuning. These may refer to different stages or reporting conventions. [GLM-4.5 report](https://arxiv.org/abs/2508.06471), [Z.AI GLM-4.5 documentation](https://docs.z.ai/guides/llm/glm-4.5)

### GLM-5

GLM-5 pushed the family toward long-horizon agentic engineering:

- 744B total / 40B active parameters;
- approximately 28.5T base-training tokens;
- long-context curriculum;
- DeepSeek Sparse Attention;
- asynchronous RL;
- repository and terminal environments;
- multi-stage post-training;
- deployment on several Chinese accelerator ecosystems.

Flash appears to inherit the family's agentic objectives while radically shrinking active computation and adding native multimodality. [GLM-5 report](https://arxiv.org/html/2602.15763)

## Research inspirations and technical ancestors

| Area | Research lineage | Contribution |
|---|---|---|
| Sparse global attention | DeepSeek-V3.2 (arXiv:2512.02556) | Selective attention over long contexts |
| MoE and KV efficiency | DeepSeek-V2 (2405.04434), DeepSeek-V3 (2412.19437) | Mixture-of-experts and compressed attention ideas |
| Linear/recurrent memory | Gated Delta Networks (2412.06464) | Efficient state updates and hybrid attention |
| Long-context synthesis | NExtLong (2501.12766), EntropyLong (2510.02330) | Constructing genuine long-range dependencies |
| Reasoning RL | DeepSeekMath / GRPO (2402.03300) | Group-relative verifiable-reward training |
| Sequence-level RL | GSPO (2507.18071) | More stable optimization for long responses and MoE |
| Multi-token prediction | Gloeckle et al. (2404.19737) | Better training efficiency and speculative decoding |
| Data curation | DataComp-LM (2406.11794) | Treating dataset selection as an optimization problem |
| Quantized deployment | QuaRot (2404.00456) | Low-bit inference and rotation-based quantization |
| Large-scale infrastructure | Megatron-LM (2104.04473), ZeRO (1910.02054) | Distributed training and memory sharding |

The important distinction: the GLM-5 report explicitly cites or discusses many of these, but a citation does not prove that Flash used the technique unchanged. The safest classification is "documented influence or adjacent method," not "confirmed Flash implementation."

## The people behind it

There is no separate public Flash-only author roster that I could verify. The closest official attribution is the GLM-5 technical report from Zhipu AI and Tsinghua University.

Its listed technical leads include Aohan Zeng, Xin Lv, Zhenyu Hou, Zhengxiao Du, Qinkai Zheng, Bin Chen, and Da Yin. Advisors include Jie Tang, Yuxiao Dong, Juanzi Li, Minlie Huang, and Bin Xu. The report contains a much larger alphabetical contributor list spanning model architecture, data, RL, infrastructure, evaluation, and deployment. [GLM-5 report contributor section](https://arxiv.org/html/2602.15763)

The earlier GLM paper credits Zhengxiao Du, Yujie Qian, Xiao Liu, Ming Ding, Jiezhong Qiu, Zhilin Yang, and Jie Tang, showing that the family's core lineage runs from Tsinghua/Zhipu research on generalized pretraining into current agentic systems. [Original GLM paper](https://arxiv.org/abs/2103.10360)

## What remains unknown

Z.AI has not publicly disclosed:

- exact Flash data-source percentages;
- dataset licenses and document counts;
- deduplication and contamination thresholds;
- exact Flash pretraining/mid-training token schedule;
- teacher-model mixture;
- SFT dataset sizes;
- reward-model architecture or training data;
- number and duration of RL runs;
- total training FLOPs;
- hardware hours and energy cost;
- safety-tuning mixture;
- exact relationship between Flash checkpoints and GLM-5 checkpoints;
- detailed ablations proving which component produced each gain.

So the honest answer is: we understand the design philosophy and much of the family-level machinery, but not the proprietary recipe.

## What this means for our model library

For Mag, the valuable artifact is not merely a copy of the 321GB-class weight file. It is a model passport containing:

```text
model identity
architecture
active/total parameters
context limits
modalities
tool behavior
reasoning controls
training-lineage evidence
known benchmark claims
independent probe results
failure signatures
cost and latency
unknowns
```

That is where your "models as game worlds" idea becomes practical. We can mine the invariants without pretending the models are interchangeable:

- Flash's sparse/linear boundary is a hypothesis to probe;
- its long-context behavior should be tested at 32K, 100K, 250K, 500K, and 1M;
- its tool-use behavior should be compared against GLM-4.5 and GLM-5;
- repeated answers, refusals, verbosity, and planning failures become behavioral data;
- every probe should carry model version, settings, context size, tool trace, latency, cost, and outcome receipt.

The strongest connection to our own system is this: Z.AI's published training architecture treats trajectories, environment outcomes, stale rollouts, cache locality, and task orchestration as first-class objects. That validates building our own model library around trajectory passports and receipts rather than around vague model names.

## Curated primary bibliography

- GLM-5.3-Flash official release: https://autoclaw.z.ai/blog/model/glm-5.3-flash/
- GLM-5.3-Flash official model card: https://huggingface.co/zai-org/GLM-5.3-Flash
- GLM-5.3-Flash developer documentation: https://docs.z.ai/guides/vlm/glm-5.3-flash/
- GLM-5 technical report: https://arxiv.org/abs/2602.15763
- GLM-4.5 technical report: https://arxiv.org/abs/2508.06471
- GLM: General Language Model Pretraining: https://arxiv.org/abs/2103.10360
- GLM-130B: https://arxiv.org/abs/2210.02414
- GLM-4.5V: https://arxiv.org/abs/2507.01006
- DeepSeek-V2: https://arxiv.org/abs/2405.04434
- DeepSeek-V3: https://arxiv.org/abs/2412.19437
- DeepSeek-V3.2 and DeepSeek Sparse Attention: https://arxiv.org/abs/2512.02556
- DeepSeekMath / GRPO: https://arxiv.org/abs/2402.03300
- Gated Delta Networks: https://arxiv.org/abs/2412.06464
- NExtLong: https://arxiv.org/abs/2501.12766
- EntropyLong: https://arxiv.org/abs/2510.02330
- Multi-token prediction: https://arxiv.org/abs/2404.19737
- DataComp-LM: https://arxiv.org/abs/2406.11794
- QuaRot: https://arxiv.org/abs/2404.00456
- Group Sequence Policy Optimization: https://arxiv.org/abs/2507.18071
