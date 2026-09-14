# Bibliography

Compiled from the search set on KV-cache serving for agent workflows, DeepSeek agent-team harnesses, and agentic evaluation / cost benchmarks.

---

## 1. KV-cache management for agent and workflow serving

### Zheng et al., 2026 — PBKV

Zheng, Haoyu, Fangcheng Fu, Jia Wu, Binhang Yuan, Yongqiang Zhang, Hao Wang, Yuanyuan Zhu, Xiao Yan, and Jiawei Jiang. 2026. “Efficient Serving for Dynamic Agent Workflows with Prediction-Based KV-Cache Management.” arXiv preprint arXiv:2605.06472. https://arxiv.org/abs/2605.06472

LLM workflows compose specialized agents that share substantial context, so KV-cache reuse can save compute. Prior systems either manage cache per agent (and miss intra-workflow reuse) or assume a *static* agent call graph (KVFlow). Practical workflows are dynamic: which agents run next depends on the task. PBKV predicts upcoming agent invocations from historical workflows plus the current context, estimates reuse potential, and keeps high-potential entries in GPU memory. Predictions are used conservatively for both eviction and prefetch. Up to 1.85× speedup over LRU on dynamic workflows and 1.26× over KVFlow on static workflows.

```bibtex
@misc{zheng2026pbkv,
  title        = {Efficient Serving for Dynamic Agent Workflows with Prediction-based KV-Cache Management},
  author       = {Zheng, Haoyu and Fu, Fangcheng and Wu, Jia and Yuan, Binhang and Zhang, Yongqiang and Wang, Hao and Zhu, Yuanyuan and Yan, Xiao and Jiang, Jiawei},
  year         = {2026},
  eprint       = {2605.06472},
  archivePrefix= {arXiv},
  primaryClass = {cs.LG},
  url          = {https://arxiv.org/abs/2605.06472}
}
```

### RoleKV, 2026 (anonymous ARR submission)

Anonymous authors. 2026. “RoleKV — Role-Aware KV Cache Management for the Inverted Age-Importance of LLM Agent Context.” ACL ARR 2026 May Submission 16206. OpenReview. https://openreview.net/forum?id=of1W47Odj1

Keywords: LLM inference, Agentic AI, KV cache, Efficient AI.

In agent workloads the *oldest* KV blocks (system prompts, tool outputs) stay important, while the newest blocks (chain-of-thought) decay fastest — the inverse of LRU’s assumption. Recency eviction therefore discards the wrong blocks, causing wasted prefill on preempt-discard engines and wasted PCIe traffic on CPU-offload engines. RoleKV is a training-free, lossless *system-level* eviction policy: a Role Tagger assigns each block a semantic role and eviction follows role-aware decay rather than recency. Reported gains on HotpotQA across 8B–70B models: up to 31% fewer preemptions, 35% less PCIe traffic, and 1.34× end-to-end speedup.

```bibtex
@misc{rolekv2026,
  title        = {RoleKV -- Role-Aware KV Cache Management for the Inverted Age-Importance of LLM Agent Context},
  author       = {{Anonymous}},
  year         = {2026},
  howpublished = {ACL ARR 2026 May Submission 16206},
  url          = {https://openreview.net/forum?id=of1W47Odj1},
  note         = {OpenReview; authors anonymous at time of compilation}
}
```

### Tiwari et al., 2026 — CacheWise

Tiwari, Shubham, Tapan Chugh, Nash Rickert, Simon Peter, Ratul Mahajan, and Haiying Shen. 2026. “CacheWise: Understanding Workloads and Optimizing KVCache Management for Efficiently Serving LLM Coding Agents.” arXiv preprint arXiv:2606.16824. https://arxiv.org/abs/2606.16824

Coding agents run as long closed-loop sessions (LLM generation ↔ tool calls). From a collected dataset of real coding-assistant traces, the authors show large repeated prefixes and sustained KVCache pressure that chat-oriented policies handle poorly. CacheWise combines prefix-aware scheduling with reuse-aware eviction guided by lightweight predictions from tool-call metadata. Implemented in vLLM: up to 2–2.6× fewer KVCache evictions and up to 3.5× faster session completion. Traces: https://github.com/cachewise-project/cachewise-coding-traces

```bibtex
@misc{tiwari2026cachewise,
  title        = {CacheWise: Understanding Workloads and Optimizing KVCache Management for Efficiently Serving LLM Coding Agents},
  author       = {Tiwari, Shubham and Chugh, Tapan and Rickert, Nash and Peter, Simon and Mahajan, Ratul and Shen, Haiying},
  year         = {2026},
  eprint       = {2606.16824},
  archivePrefix= {arXiv},
  primaryClass = {cs.DC},
  url          = {https://arxiv.org/abs/2606.16824}
}
```

### Shen et al., 2026 — Recency/Frequency Adaptive KV Caching

Shen, Yang, Meghana Madhyastha, Robert Underwood, Bogdan Nicolae, and Randal Burns. 2026. “Recency/Frequency Adaptive KV Caching for Large Language Model Serving.” arXiv preprint arXiv:2606.21238. Accepted at the ICML 2026 Workshop on Resource-Adaptive Foundation Model Inference (AdaptFM). https://arxiv.org/abs/2606.21238

LRU lets unrelated workloads flush one another’s caches. The method adaptively splits cache space between recently used and frequently used KV blocks. Gains vs. naive vLLM: up to +10.8% hit rate and −12.6% TTFT on synthetic document QA; +2.1% hit rate and −2.0% TTFT on real conversation traces. Implementation: https://github.com/Y-aang/vllm-ARC

```bibtex
@misc{shen2026adaptivekv,
  title        = {Recency/Frequency Adaptive KV Caching for Large Language Model Serving},
  author       = {Shen, Yang and Madhyastha, Meghana and Underwood, Robert and Nicolae, Bogdan and Burns, Randal},
  year         = {2026},
  eprint       = {2606.21238},
  archivePrefix= {arXiv},
  primaryClass = {cs.DC},
  note         = {Accepted at ICML 2026 Workshop on Resource-Adaptive Foundation Model Inference (AdaptFM)},
  url          = {https://arxiv.org/abs/2606.21238}
}
```

### Pan et al., 2025 — KVFlow

Pan, Zaifeng, Ajjkumar Patel, Zhengding Hu, Yipeng Shen, Yue Guan, Wan-Lu Li, Lianhui Qin, Yida Wang, and Yufei Ding. 2025. “KVFlow: Efficient Prefix Caching for Accelerating LLM-Based Multi-Agent Workflows.” arXiv preprint arXiv:2507.07400. NeurIPS 2025. https://arxiv.org/abs/2507.07400

Workflow-aware KV management for *static* multi-agent schedules. Models execution as an Agent Step Graph and assigns each agent a steps-to-execution score used for fine-grained node-level eviction in a tree-structured prefix cache, plus overlapped CPU→GPU prefetch for the next step. Up to 1.83× vs. SGLang hierarchical radix cache on large-prompt single workflows and 2.19× with many concurrent workflows. Code: https://github.com/PanZaifeng/KVFlow

This is the static-workflow baseline that PBKV compares against.

```bibtex
@article{pan2025kvflow,
  title   = {KVFlow: Efficient Prefix Caching for Accelerating LLM-Based Multi-Agent Workflows},
  author  = {Pan, Zaifeng and Patel, Ajjkumar and Hu, Zhengding and Shen, Yipeng and Guan, Yue and Li, Wan-Lu and Qin, Lianhui and Wang, Yida and Ding, Yufei},
  journal = {arXiv preprint arXiv:2507.07400},
  year    = {2025},
  note    = {NeurIPS 2025},
  url     = {https://arxiv.org/abs/2507.07400}
}
```

### Bian et al., 2025/2026 — TokenCake

Bian, Zhuohang, Feiyang Wu, Zhuoran Li, Teng Ma, and Youwei Zhuo. 2025. “TokenCake: A KV-Cache-Centric Serving Framework for LLM-Based Multi-Agent Applications.” arXiv preprint arXiv:2510.18586. Accepted at EuroSys ’27. https://arxiv.org/abs/2510.18586

Agent-aware co-design of scheduling and memory. A temporal scheduler offloads idle KV during tool-call stalls and predictively uploads to hide transfer latency; a spatial scheduler partitions GPU memory using graph structure plus runtime state so critical-path agents are protected. vs. vLLM: >47% lower end-to-end latency and up to 16.9% better effective GPU memory utilization.

```bibtex
@misc{bian2025tokencake,
  title        = {TokenCake: A KV-Cache-centric Serving Framework for LLM-based Multi-Agent Applications},
  author       = {Bian, Zhuohang and Wu, Feiyang and Li, Zhuoran and Ma, Teng and Zhuo, Youwei},
  year         = {2025},
  eprint       = {2510.18586},
  archivePrefix= {arXiv},
  primaryClass = {cs.DC},
  note         = {Accepted at EuroSys 2027},
  url          = {https://arxiv.org/abs/2510.18586}
}
```

### Emergent Mind — KVCache-centric scheduler (survey page)

Emergent Mind. 2025. “KVCache-centric Scheduler.” Topic page. https://www.emergentmind.com/topics/kvcache-centric-scheduler

Secondary overview of cache-aware scheduling: retention in the memory hierarchy, TTFT/TBT QoS, and pointers to Mooncake, KVFlow, and related systems. Not a primary paper.

```bibtex
@misc{emergentmind2025kvcache,
  title        = {KVCache-centric Scheduler},
  author       = {{Emergent Mind}},
  year         = {2025},
  howpublished = {\url{https://www.emergentmind.com/topics/kvcache-centric-scheduler}},
  note         = {Topic overview}
}
```

---

## 2. Related KV-cache surveys and adjacent systems

Jiang, Jiantong, Peiyu Yang, Rui Zhang, and Feng Liu. 2026. “Towards Efficient Large Language Model Serving: A Survey on System-Aware KV Cache Optimization.” ACL 2026 Findings. Companion repo: https://github.com/jjiantong/Awesome-KV-Cache-Optimization

Li, Haoyang, Yiming Li, Anxin Tian, Tianhao Tang, Zhanchao Xu, Xuejia Chen, Nicole Hu, Wei Dong, Qing Li, and Lei Chen. 2024. “A Survey on Large Language Model Acceleration Based on KV Cache Management.” arXiv preprint arXiv:2412.19442. https://arxiv.org/abs/2412.19442

```bibtex
@article{jiang2026skis,
  title   = {Towards Efficient Large Language Model Serving: A Survey on System-Aware KV Cache Optimization},
  author  = {Jiang, Jiantong and Yang, Peiyu and Zhang, Rui and Liu, Feng},
  journal = {Findings of the Association for Computational Linguistics},
  year    = {2026},
  note    = {ACL 2026 Findings}
}

@article{li2024surveykv,
  title   = {A Survey on Large Language Model Acceleration based on KV Cache Management},
  author  = {Li, Haoyang and Li, Yiming and Tian, Anxin and Tang, Tianhao and Xu, Zhanchao and Chen, Xuejia and Hu, Nicole and Dong, Wei and Li, Qing and Chen, Lei},
  journal = {arXiv preprint arXiv:2412.19442},
  year    = {2024},
  url     = {https://arxiv.org/abs/2412.19442}
}
```

---

## 3. Agent-team software and DeepSeek Harness

### Official harness and experimental Team domain

DeepSeek AI. n.d. *DeepSeek Harness* (`dsh`). GitHub repository. MIT license. https://github.com/deepseek-ai/deepseek-harness  
Docs: https://deepseek-harness.github.io/deepseek-harness/

Plugin architecture (“everything is a plugin”) on Cordis. Developer preview; breaking changes expected.

DeepSeek AI. n.d. “Agent Teams.” In *deepseek-harness* documentation. https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/agent-team.md

Identity and roster: `TeamId` is the root `SessionId`; `TeamTaskId` is team-local (`task-<n>`); teammate session id is persistent identity. Documents `membership`, `listMembers`, `spawnTeammate`, and durable peer messaging.

DeepSeek AI. n.d. `@deepseek-ai/dsh-experimental-agent-team`. Package README. https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/experimental/agent-team

Turns one coding session into a small team: the session agent is Lead, creates named continuable teammates (fresh or fork), exchanges durable messages, and tracks a shared task board. State survives crashes and reloads.

DeepSeek AI. n.d. `@deepseek-ai/dsh-experimental-agent-team-profile`. Package README. https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/experimental/agent-team-profile/README.md

Profile layer over `@deepseek-ai/dsh-base` that inserts Team-scoped tools and disables overlapping global continuable-child controls, leaving `subagent` / `subagent_fork` as one-shot delegation.

DeepSeek AI. n.d. `@deepseek-ai/dsh-subagent-spawn-in-process`. Package README. https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/subagent/subagent-spawn-in-process/README.md

In-process spawn path for named teammates (the `spawn_teammate` / fork-fresh-agent surface referenced in the search dump).

```bibtex
@misc{deepseek-harness,
  title        = {DeepSeek Harness},
  author       = {{DeepSeek AI}},
  howpublished = {\url{https://github.com/deepseek-ai/deepseek-harness}},
  note         = {Open-source agent harness; MIT license}
}

@misc{deepseek-agent-teams-docs,
  title        = {Agent Teams},
  author       = {{DeepSeek AI}},
  howpublished = {\url{https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/agent-team.md}},
  note         = {Harness documentation}
}
```

### Third-party Team plugins

NanmiCoder. n.d. *dsh-agent-teams*. GitHub repository. https://github.com/NanmiCoder/dsh-agent-teams  
Chinese README: https://github.com/NanmiCoder/dsh-agent-teams/blob/master/README_ZH.md

Makes the current Harness session the captain: durable child agents, dependency-aware tasks, direct messages. Documented pairing at compilation time: DeepSeek Harness `0.1.2-rc.1` + AgentTeams `0.1.16-rc.3`. npm: `@nanmicoder/dsh-agent-teams`.

wowyuarm. n.d. *dsh-agent-team: Give DeepSeek Harness a persistent agent team for long-running collaboration*. GitHub repository. https://github.com/wowyuarm/dsh-agent-team

Durable identities across sessions; workspaces, channels, task threads, claims. Model-facing tools: `team_inbox`, `team_thread`, `team_message`, `team_claim`, `team_view`. Certified in-repo against DSH `0.1.5-rc.1`.

limuyang2. n.d. *Agent Team for DeepSeek Harness* (`@limuyang2/dsh-agent-team`). https://github.com/limuyang2/agent-team

Independent root agents (not subagents) with mixed models/providers, one Leader, shared workspace, separate conversations. Release noted in README: `0.1.4`.

```bibtex
@misc{nanmicoder-dsh-agent-teams,
  title        = {dsh-agent-teams},
  author       = {{NanmiCoder}},
  howpublished = {\url{https://github.com/NanmiCoder/dsh-agent-teams}},
  note         = {Plugin for DeepSeek Harness}
}

@misc{wowyuarm-dsh-agent-team,
  title        = {dsh-agent-team},
  author       = {{wowyuarm}},
  howpublished = {\url{https://github.com/wowyuarm/dsh-agent-team}},
  note         = {Persistent team plugin for DeepSeek Harness}
}

@misc{limuyang2-dsh-agent-team,
  title        = {Agent Team for DeepSeek Harness},
  author       = {{limuyang2}},
  howpublished = {\url{https://github.com/limuyang2/agent-team}},
  note         = {npm package @limuyang2/dsh-agent-team}
}
```

---

## 4. Agent evaluation, construction, and cost/quality benchmarks

### Shi et al., 2026 — τ^τ-bench (hyper-tau-bench)

Shi, Quan, Keshav Dhandhania, Karthik Narasimhan, and Victor Barres. 2026. “τ^τ-Bench: An Environment for End-to-End, Realistic Agent Construction.” arXiv preprint arXiv:2609.04611. https://arxiv.org/abs/2609.04611

Makes *building* a customer-service agent the task. A developer agent receives business records, a client with requirements, a production API, an inherited codebase, and serving-cost/model limits, then must ship a complete agent scored against held-out simulated users. 53 tasks across four domains. Strongest reported config (Claude Opus 5 under Claude Code) passes 23.9% of evaluation simulations; expert-authored reference ceiling 82.2%. Outer loop around Sierra’s τ³-bench inner loop. MIT codebase + public leaderboard (Sierra).

```bibtex
@misc{shi2026hypertau,
  title        = {$\tau^{\tau}$-Bench: An Environment for End-To-End, Realistic Agent Construction},
  author       = {Shi, Quan and Dhandhania, Keshav and Narasimhan, Karthik and Barres, Victor},
  year         = {2026},
  eprint       = {2609.04611},
  archivePrefix= {arXiv},
  primaryClass = {cs.AI},
  url          = {https://arxiv.org/abs/2609.04611}
}
```

### Yao et al., 2024 — τ-bench (predecessor)

Yao, Shunyu, Noah Shinn, Pedram Razavi, and Karthik Narasimhan. 2024. “τ-Bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains.” arXiv preprint arXiv:2406.12045. https://arxiv.org/abs/2406.12045  
Code: https://github.com/sierra-research/tau-bench

Dynamic conversations between a simulated user and an agent with domain APIs and policy guidelines. Evaluation compares final database state to an annotated goal. Initial domains: τ-retail and τ-airline.

```bibtex
@misc{yao2024taubench,
  title        = {$\tau$-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains},
  author       = {Yao, Shunyu and Shinn, Noah and Razavi, Pedram and Narasimhan, Karthik},
  year         = {2024},
  eprint       = {2406.12045},
  archivePrefix= {arXiv},
  primaryClass = {cs.AI},
  url          = {https://arxiv.org/abs/2406.12045}
}
```

### Kapoor et al., 2025/2026 — Holistic Agent Leaderboard (HAL)

Kapoor, Sayash, Benedikt Stroebl, Peter Kirgis, Nitya Nadgir, Zachary S. Siegel, Boyi Wei, Tianci Xue, Ziru Chen, Felix Chen, Saiteja Utpala, Franck Ndzomga, Dheeraj Oruganty, Sophie Luskin, Kangheng Liu, Botao Yu, Amit Arora, Dongyoon Hahm, Harsh Trivedi, Huan Sun, Juyong Lee, Tengjun Jin, Yifan Mai, Yifei Zhou, Yuxuan Zhu, Rishi Bommasani, Daniel Kang, Dawn Song, Peter Henderson, Yu Su, Percy Liang, and Arvind Narayanan. 2025. “Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation.” arXiv preprint arXiv:2510.11977. ICLR 2026. https://arxiv.org/abs/2510.11977  
Site: https://hal.cs.princeton.edu/

Standardized harness over hundreds of VMs; three-way analysis of models × scaffolds × benchmarks. Validation: 21,730 rollouts, 9 models, 9 benchmarks (coding, web, science, customer service), ~$40k. Finds include higher reasoning effort *reducing* accuracy in a majority of runs, plus log-level failure modes (searching Hugging Face for the benchmark, misusing payment tools).

```bibtex
@inproceedings{hal2026,
  title     = {Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation},
  author    = {Kapoor, Sayash and Stroebl, Benedikt and Kirgis, Peter and Nadgir, Nitya and Siegel, Zachary S. and Wei, Boyi and Xue, Tianci and Chen, Ziru and Chen, Felix and Utpala, Saiteja and Ndzomga, Franck and Oruganty, Dheeraj and Luskin, Sophie and Liu, Kangheng and Yu, Botao and Arora, Amit and Hahm, Dongyoon and Trivedi, Harsh and Sun, Huan and Lee, Juyong and Jin, Tengjun and Mai, Yifan and Zhou, Yifei and Zhu, Yuxuan and Bommasani, Rishi and Kang, Daniel and Song, Dawn and Henderson, Peter and Su, Yu and Liang, Percy and Narayanan, Arvind},
  booktitle = {The Fourteenth International Conference on Learning Representations (ICLR)},
  year      = {2026},
  url       = {https://arxiv.org/abs/2510.11977}
}
```

### Bandel et al., 2026 — General Agent Evaluation (Exgentic)

Bandel, Elron, Asaf Yehudai, Lilach Eden, Yehoshua Sagron, Yotam Perlitz, Elad Venezian, Natalia Razinkov, Natan Ergas, Shlomit Shachor Ifergan, Segev Shlomov, Michal Jacovi, Leshem Choshen, Liat Ein-Dor, Yoav Katz, and Michal Shmueli-Scheuer. 2026. “General Agent Evaluation.” arXiv preprint arXiv:2602.22953. https://arxiv.org/abs/2602.22953  
Harness / leaderboard: https://www.exgentic.ai

First factorial comparison of tool-calling, MCP, code-generation, and CLI agents on the same models and benchmarks. Contributions: Unified Protocol, Exgentic harness, Open General Agent Leaderboard (5 architectures × 5 backbones × 6 benchmarks). Architecture swings results by up to 12 points within a model; backbone still dominates. On 4 of 6 benchmarks, top general agents match heavily customized domain agents.

```bibtex
@misc{bandel2026gae,
  title        = {General Agent Evaluation},
  author       = {Bandel, Elron and Yehudai, Asaf and Eden, Lilach and Sagron, Yehoshua and Perlitz, Yotam and Venezian, Elad and Razinkov, Natalia and Ergas, Natan and Shachor Ifergan, Shlomit and Shlomov, Segev and Jacovi, Michal and Choshen, Leshem and Ein-Dor, Liat and Katz, Yoav and Shmueli-Scheuer, Michal},
  year         = {2026},
  eprint       = {2602.22953},
  archivePrefix= {arXiv},
  primaryClass = {cs.AI},
  url          = {https://arxiv.org/abs/2602.22953}
}
```

### Arora — agentic-coding-harness-benchmarks

Arora, Amit. n.d. *agentic-coding-harness-benchmarks*. GitHub repository. MIT-0. https://github.com/aarora79/agentic-coding-harness-benchmarks

Harness for long-horizon coding tasks across agents (Claude Code and pi). Three hosting paths: Anthropic on Amazon Bedrock, open-weight on Bedrock via LiteLLM, or self-hosted vLLM on EC2. LLM-as-judge scoring and cost/quality Pareto plots. Companion `swe-router` skill recommends the cheapest model that clears a task bar.

```bibtex
@misc{arora-agentic-harness-bench,
  title        = {agentic-coding-harness-benchmarks},
  author       = {Arora, Amit},
  howpublished = {\url{https://github.com/aarora79/agentic-coding-harness-benchmarks}},
  note         = {MIT-0}
}
```

---

## 5. Leaderboards, pricing pages, and industry reports

BenchGecko. n.d. “Cheapest Agent LLMs · Ranked by Price and Tool Use Score.” https://benchgecko.ai/pricing/agents  
Related pricing dump: https://github.com/BenchGecko/llm-pricing

Ranks models by input $/1M tokens with agent scores over SWE / τ / WebArena (and related APEX-Agents pages on the same site). Live aggregator — treat figures as dated snapshots.

Tokenade. 2026. “Agentic Coding Cost Benchmarks (2026).” https://tokenade.net/en/stats/agentic-coding-cost-benchmarks  
Related: https://tokenade.net/en/case-studies/swe-bench-agent-token-study

Secondary synthesis. Headline claims in the page: ~50× more tokens for a typical agentic coding session than comparable code-chat; ~1M input tokens for a 50-turn session; large cost reductions from observation masking on SWE-bench Verified. Cite the underlying papers/posts (e.g. Vantage; Bai et al.) rather than Tokenade alone for scholarly use.

LLMPodium. n.d. “Best Agentic LLMs: OSWorld, τ²-Bench & Toolathlon.” https://llmpodium.com/leaderboard/agentic

Composite podium over OSWorld, Toolathlon, MCP Atlas, τ²-Bench Retail, and Apex Agents. Live leaderboard.

Together AI. 2026. “Benchmarking Inference at Scale: Coding Agents.” Blog post. https://www.together.ai/blog/coding-agent-benchmarks

Production coding-agent traffic (long prompts, short generations) on Kimi K2.5. Claimed: Together Inference Engine delivers 31% more TPS than TensorRT-LLM on the same hardware class and ~2× better TTFT at saturation; SGLang needed more GPUs in their setup.

```bibtex
@misc{benchgecko-agents-pricing,
  title        = {Cheapest Agent LLMs Ranked by Price and Tool Use Score},
  author       = {{BenchGecko}},
  howpublished = {\url{https://benchgecko.ai/pricing/agents}},
  note         = {Living leaderboard}
}

@misc{tokenade2026agentic-cost,
  title        = {Agentic Coding Cost Benchmarks (2026)},
  author       = {{Tokenade}},
  year         = {2026},
  howpublished = {\url{https://tokenade.net/en/stats/agentic-coding-cost-benchmarks}},
  note         = {Secondary compilation}
}

@misc{llmpodium-agentic,
  title        = {Best Agentic LLMs: OSWorld, $\tau^2$-Bench \& Toolathlon},
  author       = {{LLMPodium}},
  howpublished = {\url{https://llmpodium.com/leaderboard/agentic}},
  note         = {Living leaderboard}
}

@misc{together2026coding-agents,
  title        = {Benchmarking Inference at Scale: Coding Agents},
  author       = {{Together AI}},
  year         = {2026},
  howpublished = {\url{https://www.together.ai/blog/coding-agent-benchmarks}},
  note         = {Vendor blog}
}
```

---

## Notes on compilation

- RoleKV authors were not public on OpenReview at compilation time (ACL ARR double-blind).
- Living leaderboards (BenchGecko, LLMPodium, HAL site, Exgentic) change; pin an access date if you cite scores.
- PBKV explicitly treats KVFlow as the static-workflow SOTA baseline.
- DeepSeek “Agent Teams” exists both as experimental first-party packages and as several third-party plugins with incompatible version pins — cite the specific repo and version you used.
