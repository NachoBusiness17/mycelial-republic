# Corpus arXiv Reading List - Top 25 for Agent-Swarm Research

Item f-04, banked 2026-09-28. Source: full scan of `corpus/` in the Mag Resource Harness repo.

## Method (what actually ran)

1. Regex scan of every readable file under `corpus/`: pattern `arXiv[: ]?\d{4}.\d{4,5}` (the ask's regex with `\d` restored; `.` kept literal-dot in the strict counter, any-char in the primary counter). Scanner: `python f04_scan.py` on `.venv\Scripts\python.exe` 3.11.15, utf-8 errors-ignore, binary extensions skipped.
2. Scan result: 71,590 files scanned (5,601,766,888 bytes), 88 files with hits, 1,959 matches (all of them strict dotted form), 335 unique IDs after zero-padding normalization, 0 read errors.
3. Abstract fetch for every unique ID from arXiv's own export API (`https://export.arxiv.org/api/query?id_list=...`, Atom, batches of 40, default User-Agent, 3s spacing). Result: 335/335 resolved, 0 unresolved, 0 network errors. Spot check: `curl -o /dev/null -w %{http_code} https://arxiv.org/abs/2305.14325` returned 200.
4. Ranking lens for agent-swarm relevance: (a) multi-agent coordination and debate frameworks, (b) emergent collective dynamics and swarm pathology, (c) collective learning across agent experience, (d) swarm-serving infrastructure (shared KV cache, workflow-aware serving), (e) long-horizon evaluation of agent collectives. Ranking is my judgment over the fetched titles and abstracts; corpus hit counts are recorded per entry as a local-relevance signal, not the ranking key.

Two fetch lessons are banked in the receipt (`f-04.md`): a custom User-Agent string got HTTP 400 from the egress middlebox while the default UA passed, and one malformed ID in an `id_list` batch 400s the entire batch, so IDs were queried in canonical zero-padded form.

## The 25

### 1. arXiv:2305.14325 - Improving Factuality and Reasoning in Language Models through Multiagent Debate

- Yilun Du et al., 2023. cs.CL. Corpus hits: 33. Corpus source: `corpus/oral_history/seat_pools/codex_sessions/2026/08/30/rollout-2026-08-30T09-09-46-01a052ca-543c-76f2-bf93-53a538bf5b3e.jsonl` line 96.
- Link: https://arxiv.org/abs/2305.14325
- Why it is on the list: The founding swarm-reasoning result: multiple LLM instances propose and debate individual answers, and factuality and reasoning improve over single-model chains. The protocol nearly every later multi-agent paper builds on, benchmarks against, or tears down.

### 2. arXiv:2304.03442 - Generative Agents: Interactive Simulacra of Human Behavior

- Joon Sung Park et al., 2023. cs.HC. Corpus hits: 24. Corpus source: `corpus/oral_history/marathon_body/marathon_25fbcaab_20260815_20260820.jsonl` line 1.
- Link: https://arxiv.org/abs/2304.03442
- Why it is on the list: The canonical agent-society simulation: 25 generative agents with memory streams, reflection, and planning in a Smallville-style town, exhibiting emergent information diffusion, relationship formation, and coordinated behavior (the party) purely from agent-agent interaction.

### 3. arXiv:2402.01680 - Large Language Model based Multi-Agents: A Survey of Progress and Challenges

- Taicheng Guo et al., 2024. cs.CL. Corpus hits: 3. Corpus source: `corpus/oral_history/marathon_body/marathon_25fbcaab_20260815_20260820.jsonl` line 1.
- Link: https://arxiv.org/abs/2402.01680
- Why it is on the list: The field map for LLM-based multi-agent systems: taxonomies of cooperation, competition, and world simulation, plus the centralized-vs-decentralized communication question every swarm design inherits.

### 4. arXiv:2308.00352 - MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework

- Sirui Hong et al., 2023. cs.AI. Corpus hits: 2. Corpus source: `corpus/library/jev_steal_library/sovereign_ai_fleet_consolidated_bibliography (2).md` line 33.
- Link: https://arxiv.org/abs/2308.00352
- Why it is on the list: MetaGPT encodes human Standard Operating Procedures into a role-specialized agent society (product manager, architect, engineer, QA), using an assembly-line structure to cut cascading hallucination in agent collectives.

### 5. arXiv:2308.08155 - AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation

- Qingyun Wu et al., 2023. cs.AI. Corpus hits: 2. Corpus source: `corpus/library/jev_steal_library/sovereign_ai_fleet_consolidated_bibliography (2).md` line 34.
- Link: https://arxiv.org/abs/2308.08155
- Why it is on the list: AutoGen: the most-deployed open-source multi-agent conversation runtime. Conversation programming as the swarm control plane: agents that are customizable, conversable, and mix LLMs, tools, and human inputs.

### 6. arXiv:2308.10848 - AgentVerse: Facilitating Multi-Agent Collaboration and Exploring Emergent Behaviors

- Weize Chen et al., 2023. cs.CL. Corpus hits: 2. Corpus source: `corpus/library/jev_steal_library/sovereign_ai_fleet_consolidated_bibliography (2).md` line 36.
- Link: https://arxiv.org/abs/2308.10848
- Why it is on the list: AgentVerse dynamically re-composes its agent group mid-task and documents emergent behaviors in multi-agent collaboration, both the positive ones and the pathological ones (hallucination spirals, failed consensus).

### 7. arXiv:2307.07924 - ChatDev: Communicative Agents for Software Development

- Chen Qian et al., 2023. cs.SE. Corpus hits: 2. Corpus source: `corpus/library/jev_steal_library/sovereign_ai_fleet_consolidated_bibliography (2).md` line 35.
- Link: https://arxiv.org/abs/2307.07924
- Why it is on the list: ChatDev: communicative agents in a chat-chain for software development, with dual-agent phase reviews (coder + reviewer) as the unit of swarm coordination.

### 8. arXiv:2406.04692 - Mixture-of-Agents Enhances Large Language Model Capabilities

- Junlin Wang et al., 2024. cs.CL. Corpus hits: 13. Corpus source: `corpus/oral_history/marathon_body/marathon_25fbcaab_20260815_20260820.jsonl` line 1.
- Link: https://arxiv.org/abs/2406.04692
- Why it is on the list: Mixture-of-Agents: a layered swarm where each aggregator layer conditions on all prior-layer proposals, showing that the collective expertise of multiple off-the-shelf LLMs can beat the strongest single model.

### 9. arXiv:2406.11776 - Improving Multi-Agent Debate with Sparse Communication Topology

- Yunxuan Li et al., 2024. cs.CL. Corpus hits: 3. Corpus source: `corpus/oral_history/nacho_archaeology/extracted/nacho-archaeology-part1-chats-produced/chat-transcripts/4a30dd44-e0bc-4e3c-af2a-13da6e62cef5/4a30dd44-e0bc-4e3c-af2a-13da6e62cef5.jsonl` line 310.
- Link: https://arxiv.org/abs/2406.11776
- Why it is on the list: Replaces all-to-all agent communication with pruned, sparse topologies in multi-agent debate: direct evidence that swarm connectivity is a tunable design axis, not a fixed cost.

### 10. arXiv:2305.19118 - Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate

- Tian Liang et al., 2023. cs.CL. Corpus hits: 2. Corpus source: `corpus/oral_history/seat_pools/codex_sessions/2026/08/12/rollout-2026-08-12T19-34-11-019ff853-8656-7630-89e3-51293569847d.jsonl` line 1086.
- Link: https://arxiv.org/abs/2305.19118
- Why it is on the list: Diagnoses when swarm diversity actually helps: multi-agent debate gains come from divergent first-shot answers, not from iterative refinement of a converging one.

### 11. arXiv:2502.08788 - Stop Overvaluing Multi-Agent Debate -- We Must Rethink Evaluation and Embrace Model Heterogeneity

- Hangfan Zhang et al., 2025. cs.CL. Corpus hits: 3. Corpus source: `corpus/oral_history/nacho_archaeology/extracted/nacho-archaeology-part1-chats-produced/chat-transcripts/4a30dd44-e0bc-4e3c-af2a-13da6e62cef5/4a30dd44-e0bc-4e3c-af2a-13da6e62cef5.jsonl` line 310.
- Link: https://arxiv.org/abs/2502.08788
- Why it is on the list: The systematic anti-hype re-evaluation: five representative MAD methods against stronger single-agent baselines shrink to marginal or no gains; argues evaluation rigor and model heterogeneity are the real variables.

### 12. arXiv:2604.02460 - Single-Agent LLMs Outperform Multi-Agent Systems on Multi-Hop Reasoning Under Equal Thinking Token Budgets

- Dat Tran et al., 2026. cs.CL. Corpus hits: 2. Corpus source: `corpus/oral_history/nacho_archaeology/extracted/nacho-archaeology-part10-mag-disk/mag-disk/dashboard/static/night/chord_v4.html` line 19.
- Link: https://arxiv.org/abs/2604.02460
- Why it is on the list: The anti-swarm control: an information-theoretic (Data Processing Inequality) argument plus experiments that under an equal thinking-token budget single-agent systems match or beat multi-agent ones. Every swarm claim now has to beat this baseline.

### 13. arXiv:2608.22152 - The Collaboration Tax: How Much LLM Multi-Agent Systems Pay to Coordinate

- Weixiang Sun et al., 2026. cs.CL. Corpus hits: 1. Corpus source: `corpus/oral_history/nacho_archaeology/extracted/nacho-archaeology-part10-mag-disk/mag-disk/dashboard/static/night/chord_v4.html` line 57.
- Link: https://arxiv.org/abs/2608.22152
- Why it is on the list: Names and formalizes the coordination cost: collaboration tax as the team-decentralisation loss of a two-player cooperative game with private information, operationalized on solo-tractable tasks. Quantifies what swarms surrender to coordinate.

### 14. arXiv:2608.23541 - The Interaction Tax: When Communication Erases Diversity in Multi-Agent Teams

- Summer Eunhyung Ann et al., 2026. cs.MA. Corpus hits: 2. Corpus source: `corpus/oral_history/nacho_archaeology/extracted/nacho-archaeology-part10-mag-disk/mag-disk/dashboard/static/night/chord_v4.html` line 17.
- Link: https://arxiv.org/abs/2608.23541
- Why it is on the list: Reconciles the pro- and anti-multi-agent literature by arguing interaction itself erases response diversity: the swarm's gains depend on protecting heterogeneity that communication tends to homogenize.

### 15. arXiv:2608.10218 - Mind Viruses: Self-Propagating Ideas in Multi-Agent LLM Systems

- Vassilis Papadopoulos et al., 2026. cs.AI. Corpus hits: 24. Corpus source: `corpus/oral_history/marathon_body/marathon_25fbcaab_20260815_20260820.jsonl` line 1.
- Link: https://arxiv.org/abs/2608.10218
- Why it is on the list: Mind viruses: ideas or goals that propagate agent-to-agent in multi-agent LLM systems, inducing hosts to transmit them onward and altering host behavior. Memetic epidemiology as a swarm-safety discipline.

### 16. arXiv:2607.00918 - From Personas to Plot: Character-Grounded Multi-Agent Story Generation for Long-Form Narratives

- Aayush Aluru et al., 2026. cs.CL. Corpus hits: 47. Corpus source: `corpus/oral_history/marathon_body/marathon_25fbcaab_20260815_20260820.jsonl` line 1.
- Link: https://arxiv.org/abs/2607.00918
- Why it is on the list: MAGNET: persona-grounded character agents proposing actions against a shared world state with verifier loops. The second-most-referenced arXiv ID in this corpus (47 hits); a worked example of narrative-scale agent coordination.

### 17. arXiv:2603.25158 - Trace2Skill: Distill Trajectory-Local Lessons into Transferable Agent Skills

- Jingwei Ni et al., 2026. cs.AI. Corpus hits: 33. Corpus source: `corpus/oral_history/seat_pools/grok_sessions/C%3A%5CUsers%5Cfoste%5CDocuments%5Cprojects%5Clocal_sovereign_agent/01a045ac-6ab5-7523-be8d-56125027b7c0/updates.jsonl` line 149.
- Link: https://arxiv.org/abs/2603.25158
- Why it is on the list: Trace2Skill consolidates parallel execution trajectories into a unified skill directory via inductive reasoning over agent experience: collective learning, where one agent's scars become every agent's skill.

### 18. arXiv:2605.18032 - PROTEA: Offline Evaluation and Iterative Refinement for Multi-Agent LLM Workflows

- Kazuki Kawamura et al., 2026. cs.CL. Corpus hits: 9. Corpus source: `corpus/oral_history/seat_pools/grok_sessions/C%3A%5CUsers%5Cfoste%5CDocuments%5Cprojects%5Clocal_sovereign_agent/01a045ac-6ccd-7a90-9522-a68f41cd359f/updates.jsonl` line 167.
- Link: https://arxiv.org/abs/2605.18032
- Why it is on the list: PROTEA: offline, test-driven improvement of multi-agent workflows, with failure localization across intermediate outputs that propagate downstream between agents.

### 19. arXiv:2507.07400 - KVFlow: Efficient Prefix Caching for Accelerating LLM-Based Multi-Agent Workflows

- Zaifeng Pan et al., 2025. cs.DC. Corpus hits: 6. Corpus source: `corpus/library/jev_steal_library/sovereign_ai_fleet_consolidated_bibliography (2).md` line 198.
- Link: https://arxiv.org/abs/2507.07400
- Why it is on the list: KVFlow: workflow-aware prefix caching for multi-agent serving. Shows LRU eviction misprices agent workflows and replaces it with DAG-aware eviction; the swarm's serving substrate as a first-class research object.

### 20. arXiv:2604.03143 - TokenDance: Scaling Multi-Agent LLM Serving via Collective KV Cache Sharing

- Zhuohang Bian et al., 2026. cs.DC. Corpus hits: 1. Corpus source: `corpus/library/jev_steal_library/sovereign_ai_fleet_consolidated_bibliography (2).md` line 1278.
- Link: https://arxiv.org/abs/2604.03143
- Why it is on the list: TokenDance exploits the shared KV blocks inside all-gather synchronization rounds to scale the number of concurrent agents: collective cache sharing as the mechanism that makes wide swarms affordable.

### 21. arXiv:2603.16104 - Efficient LLM Serving for Agentic Workflows: A Data Systems Perspective

- Noppanat Wadlom et al., 2026. cs.MA. Corpus hits: 1. Corpus source: `corpus/library/jev_steal_library/sovereign_ai_fleet_consolidated_bibliography (2).md` line 1274.
- Link: https://arxiv.org/abs/2603.16104
- Why it is on the list: A data-systems view of agentic workflows as the dominant LLM workload: cross-call redundancy from overlapping prompts and speculative parallel exploration, and why per-call optimizers like vLLM miss it.

### 22. arXiv:2502.15840 - Vending-Bench: A Benchmark for Long-Term Coherence of Autonomous Agents

- Axel Backlund et al., 2025. cs.AI. Corpus hits: 5. Corpus source: `corpus/oral_history/seat_pools/codex_sessions/2026/08/30/rollout-2026-08-30T09-09-46-01a052ca-543c-76f2-bf93-53a538bf5b3e.jsonl` line 20625.
- Link: https://arxiv.org/abs/2502.15840
- Why it is on the list: Vending-Bench: a long-running business simulation where accumulated small errors compound into incoherence. The swarm failure mode at long horizons is drift accumulation, not single bad decisions.

### 23. arXiv:2609.04611 - $τ^τ$-Bench: An Environment for End-To-End, Realistic Agent Construction

- Quan Shi et al., 2026. cs.AI. Corpus hits: 4. Corpus source: `corpus/library/jev_steal_library/sovereign_ai_fleet_consolidated_bibliography (2).md` line 344.
- Link: https://arxiv.org/abs/2609.04611
- Why it is on the list: Makes agent construction itself the benchmark task: a developer-agent must deliver a working agent under real client-engagement conditions (budget, eval criteria, handoff).

### 24. arXiv:2605.08580 - Slipstream: Trajectory-Grounded Compaction Validation for Long-Horizon Agents

- Zhuofu Chen et al., 2026. cs.MA. Corpus hits: 16. Corpus source: `corpus/oral_history/seat_pools/codex_sessions/2026/08/30/rollout-2026-08-30T09-09-46-01a052ca-543c-76f2-bf93-53a538bf5b3e.jsonl` line 14591.
- Link: https://arxiv.org/abs/2605.08580
- Why it is on the list: Slipstream: trajectory-grounded validation for context compaction in long-horizon agents, moving compaction off the critical path while checking what the summary destroyed before the agent resumes from it.

### 25. arXiv:2608.23651 - Feedback That Backfires: Why Small Language Model Agents Repeat the Call They Just Watched Fail

- Esmail Gumaan et al., 2026. cs.SE. Corpus hits: 24. Corpus source: `corpus/oral_history/seat_pools/grok_sessions/C%3A%5CUsers%5Cfoste%5CDocuments%5Cprojects%5Clocal_sovereign_agent/01a048ad-1c90-7e31-83cb-89b3ed063bcc/updates.jsonl` line 176.
- Link: https://arxiv.org/abs/2608.23651
- Why it is on the list: Measures corrective gain of a logged failure record and finds it negative for every small instruction-tuned model tested (135M-1.7B, 4 families): small-model janitor swarms re-emit the call they just watched fail.

## Shortlist: next 10 (relevant, cut by the 25 cap)

- arXiv:2308.09687 - Graph of Thoughts: Solving Elaborate Problems with Large Language Models (Maciej Besta et al., 2023). Graph of Thoughts: arbitrary graphs of LLM thoughts with arbitrary dependencies; 22 corpus hits; parallel-reasoning topology adjacent to swarm structure.
- arXiv:2607.28956 - MerchantBench: Benchmarking LLM Agents for Long-Term Coherence in E-Commerce Operations (Qiming Shi et al., 2026). MerchantBench: long-term coherence for LLM agents in e-commerce operations; the single most-referenced arXiv ID in this corpus (67 hits) though its lens is long-horizon evaluation more than swarm coordination.
- arXiv:2506.19143 - Thought Anchors: Which LLM Reasoning Steps Matter? (Paul C. Bogdan et al., 2025). Thought Anchors: sentence-level attribution of which reasoning steps matter; 33 corpus hits; a measurement tool applicable to inter-agent transcripts.
- arXiv:2602.06052 - A Survey of Agent Memory in the Second Half: Towards Self-Evolving and Long-Horizon Agents (Wei-Chieh Huang et al., 2026). Survey of agent memory in the second half: context explosion and continuous accumulation as the defining problem of long-horizon agents.
- arXiv:2504.13171 - Sleep-time Compute: Beyond Inference Scaling at Test-time (Kevin Lin et al., 2025). Sleep-time compute: pre-computing offline about contexts before queries arrive; the mechanism behind off-peak swarm work.
- arXiv:2601.02163 - EverMemOS: A Self-Organizing Memory Operating System for Structured Long-Horizon Reasoning (Chuanrui Hu et al., 2026). EverMemOS: a self-organizing memory operating system for structured long-horizon reasoning; 12 corpus hits, already cited in mag/memory_consolidate.py's neighborhood.
- arXiv:2605.09104 - Token Economics for LLM Agents: A Dual-View Study from Computing and Economics (Yuxi Chen et al., 2026). Token economics for LLM agents from computing and economics viewpoints; the swarm's budget line.
- arXiv:2606.23525 - Self-Compacting Language Model Agents (Tianjian Li et al., 2026). Self-compacting language model agents: agents that compress their own context mid-episode.
- arXiv:2605.29256 - DynSess: Dynamic Session-Level Evaluation and Optimization Framework for Role-Playing Agents (Rongsheng Zhang et al., 2026). DynSess: dynamic session-level evaluation and optimization for role-playing agents.
- arXiv:2507.13334 - A Survey of Context Engineering for Large Language Models (Lingrui Mei et al., 2025). A survey of context engineering for LLMs: the shared vocabulary for what swarms pass between nodes.

## Coverage notes

- All 335 unique corpus IDs resolved on arXiv; there are no unresolvable IDs to report and nothing on this list is unfetched. Three corpus IDs carry 4-digit suffixes (`1201.0749`, `1402.2295`, `1406.2294`); their 5-digit paddings do not exist and the raw forms resolved (a 2012 sudoku-combinatorics paper, a stoquastic-Hamiltonian Monte Carlo paper, and the jump consistent-hash paper). None are swarm-relevant; they are recorded here because they are the only IDs where corpus form and arXiv canonical form disagree.
- The corpus's biggest arXiv clusters are reasoning-trace work (DeepSeek-R1 44 hits, chain-of-thought family 15-21 hits each) rather than swarm work; those went to the shortlist or off-list because the ask ranks for agent-swarm research, not overall corpus weight.
- Full census receipt with commands, counts, and the complete 335-ID list: `watch/inbox/burn_reset_20260927/flash50/f-04.md`.
