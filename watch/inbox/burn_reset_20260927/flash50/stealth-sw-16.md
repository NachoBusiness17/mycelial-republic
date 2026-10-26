# sw-16: Zero-data self-play at inference time - can LLM agents improve reasoning without fine-tuning?

Researched 2026-09-28 by stealth-sw-16. All papers verified by direct arXiv fetch this session except where marked search-only. No em-dashes or en-dashes in this file per repo law.

## Verdict

Yes, with load-bearing caveats. LLM agents demonstrably improve reasoning at inference time with zero weight updates, purely through self-generated practice: retries with verbal reflection, self-curated memory, extracted insights, and reusable skills. The strongest published wins are large (GPT-4o on Game of 24 from 10% to 99%; Reflexion's 91% pass@1 HumanEval vs GPT-4's 80%). But the field's headline term "self-play" mostly names methods that DO train (Absolute Zero, R-Zero: zero data, not zero training), and the inference-time-only strand has three structural ceilings: task-locality, context-budget bounds on how much experience can accumulate, and evidence that models often fail to learn from accumulated interactions in streaming settings. Inference-time improvement is real elicitation, not weight-level acquisition.

## 1. The distinction that organizes the evidence

Three different claims get blurred into "self-play without fine-tuning":

- Zero data, WITH training: Absolute Zero and R-Zero generate their own curriculum and rewards, then update weights with RL or fine-tuning. No human examples, but gradient descent all the same.
- Zero training, WITH data: classic in-context learning. Improves on a task given examples, never adapts across episodes.
- Zero training, zero external data at inference: the ask's actual target. The model practices on its own generated problems, reflects on its own failures, banks the lessons in context or external memory, and retrieves them on later attempts. This exists and is published, per sections 2 and 5.

## 2. Evidence that inference-time self-generated practice works (no weight updates)

- Reflexion (Shinn, Cassano, Berman, Gopinath, Narasimhan, Yao; arXiv 2303.11366, v4 Oct 2023). "Verbal reinforcement learning": the agent reflects in natural language on task feedback, stores the reflection in an episodic memory buffer, and conditions later trials on it. The paper states reinforcement happens "not by updating weights, but instead through linguistic feedback." Result: 91% pass@1 on HumanEval, surpassing the previous SOTA GPT-4 at 80%. Verified from the arXiv abstract page this session.
- ExpeL (Zhao, Huang, Xu, Lin, Liu, Huang; arXiv 2308.10144, AAAI-24). Motivated explicitly by closed-weight API models: "autonomously gathers experiences and extracts knowledge using natural language from a collection of training tasks," then at inference recalls extracted insights plus raw experiences. Three stages: experience gathering (Reflexion-style retries), insight extraction, test-time application. No parametric updates; the abstract reports consistent improvement as experiences accumulate, plus transfer. Specific ALFWorld/WebShop numbers were not on the abstract page this session (search-only there).
- Voyager (Wang, Xie, Jiang, Mandlekar, Xiao, Zhu, Fan, Anandkumar; arXiv 2305.16291). GPT-4 as a black box, "no model parameter fine-tuning." Three components: automatic curriculum, an ever-growing skill library of executable code (stored, described, retrieved by embedding), and iterative prompting with environment feedback and self-verification. In Minecraft: 3.3x more unique items, 2.3x longer travel, tech-tree milestones up to 15.3x faster than prior SOTA; the skill library transfers to a new world to solve novel tasks. The skill library is the clearest example of inference-time practice compounding: learned code composes into new skills and, per the paper, mitigates catastrophic forgetting by living outside the weights.
- Dynamic Cheatsheet (Suzgun, Yuksekgonul, Bianchi, Jurafsky, Zou; arXiv 2504.07952, submitted Apr 10 2025, published EACL 2026 as aclanthology.org/2026.eacl-long.333). A black-box LM keeps a persistent, self-curated "cheatsheet" of concise strategies, code snippets, and problem-solving insights, updated across problems at test time with no ground-truth labels and no parameter changes. Verified numbers from the arXiv abstract: Claude 3.5 Sonnet "more than doubled" accuracy on AIME after retaining algebraic insights; GPT-4o rose from 10% to 99% on Game of 24 after discovering and reusing a Python-based solution; arithmetic-heavy tasks reached near-perfect accuracy where baselines stayed near 50%; +9% GPQA-Diamond and +8% MMLU-Pro for Claude. This is the closest thing to a direct answer to the ask: the practice problems are the model's own, the lessons are self-curated, and nothing but the context changes.
- Contextual Experience Replay (Liu, Si, Narasimhan, Yao; arXiv 2506.06698, ACL 2025, Princeton). "Training-free framework to enable efficient self-improvement for language agents in their context" - an agent accumulates past trajectory-experience pairs in its own context and replays them to improve on web-navigation benchmarks. Found via verified arXiv listing (cited by ~59) this session; the paper ID was located by search after a guessed ID (2502.15472) turned out to be an unrelated edge-communications paper, which is why that guess was discarded.
- Training-Free GRPO (Cai et al.; arXiv 2510.08191, submitted Oct 9 2025, Tencent youtu team). Replaces GRPO's numerical group-relative advantage with a "group relative semantic advantage": rollouts of a group are compared, high-quality experiential knowledge is distilled into an experience library, and that library is injected as a token prior in later API calls. Weights stay fixed. On DeepSeek-V3.1-Terminus it significantly improves out-of-domain performance on mathematical reasoning and web searching, and with "just a few dozen training samples" it beats fine-tuned small LLMs at marginal training data. The cost profile shifts from GPU training to tokens: the search-result summary of the paper reported on the order of 60K input plus 8K output tokens per request (from search summary, not the abstract itself).

## 3. Evidence from the self-play strand: zero data is not zero training

- Absolute Zero (Zhao et al.; arXiv 2505.03335, v3 Oct 2025): a single model proposes code-based reasoning tasks aimed at maximizing its own learning progress, a code executor validates and scores them, and the model is improved by RL on that self-play signal. The Absolute Zero Reasoner reaches overall SOTA on coding and math reasoning with zero external data. But it is RLVR with weight updates, not an inference-time method. Verified from the arXiv page: it "requires training," it is not inference-time only.
- R-Zero (Huang, Yu, Wang, Zhang, Li, Li, Huang, Mi, Yu; arXiv 2508.05004, v1 Aug 2025): two independently initialized roles co-evolve, a Challenger rewarded for tasks at the edge of the Solver's capability and a Solver rewarded for solving them, producing a self-improving curriculum from a single base model. Qwen3-4B-Base gains +6.49 on math-reasoning and +7.54 on general-domain reasoning benchmarks. Also weight updates: models are "optimized separately and co-evolve."

Why the distinction matters for the ask: these two are the papers people cite for "self-play with zero data," and they show the ceiling of self-generated practice is much higher when the lessons can be baked into weights. The inference-time-only strand keeps hitting the same wall from the other side: what you can hold in context.

## 4. Why inference-time learning works at all: mechanistic grounding

Learning Without Training: The Implicit Dynamics of In-Context Learning (Dherin, Munn, Mazzawi, Wunder, Gonzalvo; Google DeepMind; arXiv 2507.16003, 2025, cited by ~43 per search). A self-attention layer stacked on an MLP lets a transformer block implicitly modify the MLP's effective weights: the prompt context acts as a low-rank weight update whose keys and values are the low-rank components and whose tokens act as gates controlling when the modification is active. This gives a mechanistic story for "learning without training": context can genuinely reconfigure the network's computation at inference. The paper's own scope note from follow-ups found in search: it relies on simplifying assumptions and does not yet cover nonlinear function learning or general architectures.

## 5. Where it fails: documented limits

- The practice loop is only as good as the verifier. Absolute Zero needs a code executor for grounded reward; Dynamic Cheatsheet leans on the model validating its own snippets. Where outcomes are not verifiable, self-play has nothing to bank.
- Context is the new training budget, and it is finite. Dynamic Cheatsheet's documented limitation (from search summaries of the paper's discussion): the cheatsheet cannot grow indefinitely, and a Full History baseline "can exceed context-window limits and include redundant or low-value information." Curation is doing the work forgetting normally does.
- Models often do not learn from accumulated interactions in the wild. Evo-Memory (Wei, Sachdeva, Coleman, He, Bei, Ning, Ai, Li, He, Chi, Wang, Chen, Pereira, Kang, Cheng; arXiv 2511.20857, v1 Nov 2025, Google/UCSD-affiliated author list): a streaming benchmark across 10 multi-turn and single-turn reasoning/QA datasets where memory must be searched, adapted, and evolved after each interaction; its motivation states LLMs "often fail to learn from accumulated interactions, losing valuable contextual insights." It ships 10+ memory modules, an ExpRAG experience-retrieval baseline, and ReMem (an action-think-memory refine pipeline). Concrete failure-mode numbers were not on the abstract page this session (noted as not read, not guessed).
- Retrieval/update triggering itself is a failure mode: AdaMEM (OpenReview, search-only this session) reports agents failing to trigger memory retrieval or update at the right moments.
- Elicitation ceiling: every method in section 2 is bounded by what the base model can already do in some context. Game of 24 10-to-99 was the model finally writing and reusing correct code, not learning arithmetic it lacked. Nothing here crosses the acquisition gap that RL training closes (compare AZR's SOTA from weight updates in section 3).
- Cost migration, not cost elimination: Training-Free GRPO's per-request token overhead (order 60K input tokens) means the improvement loop bills the API on every step of practice.

## 6. Open questions the field has not settled

1. Transfer breadth: Voyager's skill library transfers across Minecraft worlds; ExpeL reports cross-task transfer; but no section-2 method shows cross-DOMAIN gains comparable to its in-domain ones (Training-Free GRPO's out-of-domain claim is the strongest found, on DeepSeek-V3.1-Terminus).
2. Permanence: insights live in context or an external store; no inference-time method claims any persistence beyond its memory artifact, and none survives the artifact being deleted.
3. Whether implicit ICL dynamics (section 4) compose with explicit memory curation, or whether the two interference patterns (gated low-rank updates vs curated text) fight each other in long streams, is unmeasured in what this session read.
4. Self-generated curricula at inference time (model inventing its own practice problems, no executor) remain largely the property of the training strand; Dynamic Cheatsheet is the nearest inference-time analog and it curates solutions more than it manufactures new problems.

## 7. Local mirror (this estate)

The fleet already runs this experiment on itself: AGENTS.md driving-ladder law (memory/rib/RIB_DRIVING_LADDER_20260928.md per the AGENTS.md Clippy section) rules that free stealth lane outputs are a SENSING surface, "banked as findings, never as done/trusted work; verification climbs to the funded tier." That is exactly the section-5 verifier law stated operationally: self-generated practice products are only as trustworthy as the verifier they climb to. The insight/trajectory banking organs in this repo (memory/percolator, rib_bus, trails) are an ExpeL-shaped inference-time loop over the fleet.

## Method note (what was actually run this session)

- Direct arXiv abstract fetches (WebFetch), all verified: 2504.07952 (Dynamic Cheatsheet), 2510.08191 (Training-Free GRPO), 2505.03335 (Absolute Zero), 2303.11366 (Reflexion), 2308.10144 (ExpeL), 2508.05004 (R-Zero), 2511.20857 (Evo-Memory), 2305.16291 (Voyager), plus 2502.15472 which was fetched to check a guessed ID and is NOT about this topic (edge communications, IEEE JSAC) and was discarded as a source.
- WebSearch (z.ai web_search_prime backend): located CER (arXiv 2506.06698, ACL 2025), Dherin et al. (arXiv 2507.16003), EACL 2026 status of Dynamic Cheatsheet, Evo-Memory follow-ups, AdaMEM. The backend returned MCP -429 / code 1302 rate-limit errors on roughly 4 of the underlying sub-queries this session (the envelope law reproducing at the tool layer, consistent with the repo's B2-443 error census); queries recovered on retry with narrower terms.
- Not run: any model dispatch via free-lane fanout (tools/stealth_fanout.py does not exist at the named path in this repo; a recursive search found no stealth_fanout file), any full-text PDF reads of the papers beyond abstract pages, and no local experiments. ExpeL per-benchmark numbers, Evo-Memory failure-mode numbers, and Training-Free GRPO token-overhead figures are flagged above as abstract-page-only or search-summary-only rather than full-text-verified.

## Sources

- https://arxiv.org/abs/2303.11366 (Reflexion)
- https://arxiv.org/abs/2308.10144 (ExpeL, AAAI-24)
- https://arxiv.org/abs/2305.16291 (Voyager)
- https://arxiv.org/abs/2504.07952 + https://aclanthology.org/2026.eacl-long.333 (Dynamic Cheatsheet, EACL 2026)
- https://arxiv.org/abs/2506.06698 + https://aclanthology.org/2025.acl-long.694 (Contextual Experience Replay, ACL 2025)
- https://arxiv.org/abs/2510.08191 (Training-Free GRPO)
- https://arxiv.org/abs/2505.03335 (Absolute Zero)
- https://arxiv.org/abs/2508.05004 (R-Zero)
- https://arxiv.org/abs/2507.16003 (Learning Without Training: The Implicit Dynamics of In-Context Learning)
- https://arxiv.org/abs/2511.20857 (Evo-Memory)
- Local: AGENTS.md driving-ladder bullet; memory/rib/RIB_DRIVING_LADDER_20260928.md (cited per AGENTS.md, not opened this session)
