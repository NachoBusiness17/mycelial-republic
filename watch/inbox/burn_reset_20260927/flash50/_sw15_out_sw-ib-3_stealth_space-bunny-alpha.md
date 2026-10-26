# SW15 sw-ib-3

lane model: stealth/space-bunny-alpha
ts: 2026-09-29T01:56:28.804551+00:00
dt: 49.9s

---

We need answer research request. Need deeply investigate. Need exact titles arxiv IDs venues measured percentages, distinguish published empirical numbers vs claims, OWED if unverifiable likely "otherwise weak evidence?" They ask OWED if unverifiable perhaps acronym means "omit when...?" Need understand. Need give factual audit.

Need cover:
- Compression of inter-agent messages in LLM-based MAS
- LLMLingua prompt compression family (Jiang et al 2023)
- agent message summarization
- multi-agent communication topology and cost optimization (GPTSwarm, AFlow, MaAS)
- token-budget control
- measured token savings and quality tradeoffs
What actually published with numbers, what only claimed? Exact titles, arXiv ids, venues, measured percentages where stated. OWED if unverifiable. Need likely browse web? No explicit tools. We can use internal knowledge and reason, perhaps internet inaccessible. Need be exact and not hallucinate. OWED perhaps acronym at end for unverifiable? They explicitly say OWED if unverifiable, perhaps they want mark "OWED" (Open Web Evidence Discovered?) Need infer. Search from knowledge.

Let's identify papers.

LLMLingua:
"LLMLingua: Compressing Prompt for Accelerated Inference of Large Language Models" by Huiqiang Jiang, Qianhui Wu, Chin-Yew Lin, Yuqing Yang, Qiang Chen? arXiv:2310.05736, EMNLP 2023? Main conference? LLMLingua: Compressing Prompt for Accelerated Inference of Large Language Models. arXiv 2310.05736. Published EMNLP 2023, pages maybe 7930–7948? It uses compression ratios up to 20x, sometimes 6x? Need exact numbers.

"LongLLMLingua: Accelerating and Enhancing LLMs in Long Context Scenarios via Prompt Compression" arXiv:2402.14539, ACL 2024? Findings of ACL 2024 perhaps? It achieves up to 4× acceleration and 64.2% compression? Need exact.
"LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression" arXiv:2402.05755? Maybe arXiv 2402.05755, ACL 2024 Findings? It compresses prompts by 50-80%? Need exact.
"LLMLingua: A..." There is "LLMLingua: Compressing Prompt for Accelerated Inference of Large Language Models" initial.
"LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression" authors Zhuoshi Yang? Let's recall.
"Prompt Compression for Extreme Context Length"? 
"Recurrent Context Compression" maybe.

Question centered inter-agent messages. Need explicitly say LLMLingua compresses prompts, not demonstrated as communication compression in MAS perhaps later papers apply it. Need find MAS paper maybe "MAgIC: Multi-Agent...?" Search mentally.

Agent message summarization:
- " communicative planning for..." 
- "Concordia?" 
- "AgentPrune: Reducing Redundancy in Multi-Agent Debates"?
- "Cut the Crap: An Economical Communication Pipeline for LLM-based Multi-Agent Systems" perhaps.
- "DyLAN: Dynamic LLM-Agent Network..." arXiv 2310.02170, "Dynamic LLM-Agent Network: Agent-Robustness and Collaboration..."?
- "GPTSwarm: Language Agents as Optimizable Graphs" arXiv:2402.16823, ICML 2024? measured token costs and performance.
- "AFlow: Automating Agentic Workflow Generation" arXiv 2410.10762, maybe ICLR 2025? Published? Numbers.
- "MaAS: Multi-agent architecture search via agentic supernet" arXiv 2502.04133? CVPR 2025? "Multi-agent Architecture Search via Agentic Supernet" by X? MaAS, arXiv:2502.04133 likely. Claims up to 80% cost? Need verify exact tables.
- "TokenFlow?" Multi-agent token budgets.
- "Multi-Agent Collaboration via Evolving Orchestration" etc.
- "AgentDropout?"
- "CATS: ..." 
- "A Dynamic LLM-Powered Agent Network for Task-Oriented Agent Collaboration" no.
- "Adaptive Inference-Time Compute: LLM Multi-Agent Debate..."
- "Multi-Agent Debate with Adaptive..." communication rounds.

Agent summarization specific:
- "S^2M: ...?" Search memories from papers.
Could use web through shell? No tools shown. We only have language model, but can reconstruct and mark unverifiable. Need likely answer with high confidence and OWED tags. User expects bibliography/audit. Need perhaps mention exact percentages from primary papers.

Let's parse wording: "Compression of inter-agent messages in LLM-based multi-agent systems: LLMLingua prompt compression family (Jiang et al 2023), agent message summarization, multi-agent communication topology and cost optimization (GPTSwarm, AFlow, MaAS), token-budget control, measured token savings and quality tradeoffs. What is actually published with numbers, and what is only claimed? Exact titles, arXiv ids, venues, measured percentages where stated. OWED if unverifiable."

Maybe "OWED" = "Open Web Evidence Date?" They instruct if unverifiable, say OWED. We can define [OWED] as "original-work/paper not directly verified"? Could use "OWED (original-work evidence not directly verifiable)" marker. Need not guess.

Could perhaps access external through latent knowledge. Let's systematically identify each.

1. LLMLingua primary:
Title exact. Authors maybe not requested but could include.
arXiv 2310.05736.
Venue EMNLP 2023. DOI possibly.
Reported:
- compression ratio 20x in worst case without hurting performance
- 6x? Speedup: "achieves up to 20× compression ratio and 6× acceleration in latency, with minimal performance degradation." Let's recall abstract:
"we propose LLMLingua, a prompt compression method that ... compresses the original prompt into a much shorter one without significantly degrading the performance of LLMs. ... extensive experiments show that LLMLingua can achieve up to 20x compression ratio and 6x acceleration in latency, while retaining desirable performance. ... open-source..." Exact.
Might report 1.6x model response latency? Latency is prompt compression plus model input? Abstract exact likely 20x and 6x. Need caution: compression measured by token count, acceleration end-to-end. Not inter-agent message. Quality often maintained, not universal.

2. LongLLMLingua:
Exact title maybe "LongLLMLingua: Accelerating and Enhancing LLMs in Long Context Scenarios via Prompt Compression"
arXiv:2402.14539.
Venue ACL 2024? Let's recall paper listings. It may be ACL 2024 Main, pages. Authors Huiqiang Jiang, Qianhui Wu, Chin-Yew Lin, Yuqing Yang, Qiang Chen? Search latent. Abstract:
"we propose LongLLMLingua, a prompt compression method ... accelerates and enhances LLMs in long context scenarios. It comprehensively considers query-aware compression, extraction, and optimal allocation of compression budget. Extensive experiments show that LongLLMLingua can reduce the prompt length by 64.2% on average without compromising model performance, and achieve up to 1.94x acceleration in latency, while also enhancing..." Maybe exact values.
I recall reading papers:
LongLLMLingua abstract: "LongLLMLingua can reduce the prompt length by 64.2% on average without compromising model performance, and achieve up to 1.94× acceleration in latency." Maybe yes.
On LongBench, "compresses 64.2% of prompt tokens and improves response latency by 1.94x." Need distinguish token reduction 64.2%, so 35.8% remains. "up to 4× speedup" may be memory/time under batch? Let's investigate latent.

I have seen HuggingFace model card:
"LongLLMLingua reduces prompt length by up to 94.3% and accelerates inference speed by up to 2x, without compromising model performance." Hmm.
Abstract maybe:
"Extensive experiments show that LongLLMLingua can reduce the prompt length by 64.2% on average without compromising model performance, and achieve up to 1.94x acceleration in latency." likely.

Venue maybe ACL 2024 Findings. Search memory of ACL Anthology titles. LongLLMLingua likely Findings of the Association for Computational Linguistics: ACL 2024, pages 119?? It came Feb 2024 and accepted ACL. Could be "Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)"? LLMLingua-2 maybe ACL 2024 main. LongLLMLingua likely ACL 2024 main due prominence. Need not specify pages unless confident; venue exact enough.

3. LLMLingua-2:
Title exact. arXiv maybe 2402.05755. Venue: ACL 2024? It may be "Findings of ACL 2024" pages 114??.
Abstract: "Prompt compression is critical for reducing costs and improving efficiency of LLMs. Existing methods primarily rely on small language models and heuristics, limiting compression ratio and task generalization. We propose LLMLingua-2, a task-agnostic prompt compression method that leverages the strong capability of LLMs to distill prompts into a shorter form. Specifically, we formulate prompt compression as a data distillation problem and propose a token-level approach with budget controller. Extensive experiments on 12 datasets show that LLMLingua-2 significantly outperforms ... up to 2x compression ratio while preserving performance; 3x speedup?" Need exact.

Recall from GitHub:
LLMLingua-2 "compresses prompts by up to 50% while maintaining model performance, and achieves up to 2x speedup in end-to-end latency." Uses Mistral-7B? It is "Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression". On LongBench, compression ratio 2x, better than LLMLingua. Maybe reports "up to 50% compression ratio" (meaning 2x). Need inspect latent snippets:
Paper abstract likely:
"LLMLingua-2 compresses prompts by up to 50% and achieves up to 2x speedup in end-to-end latency, while maintaining model performance. It also outperforms existing methods by up to 3.3x in compression performance." Hmm.

But this is not inter-agent.

4. "LLMLingua: A ... multilingual?" Prompt compression methods maybe "Selective Context", "AutoCompressor", "Recurrent Context Compression (RCC)", "LongLLMLingua", "LLMLingua-2". User says family likely expect these.

Agent message summarization papers. Need identify credible specific published work. Maybe "Compressing Agent Dialogue:..." Search internal knowledge from arXiv trends.

Potential title:
- "Aging with LEGO: A Transparent and Modular Framework for Multi-Agent ..." no.
- "Cheap and Creative: LLMs as..." 
- "MetaGPT"? communications structured.
- "Adaptive Multi-Agent Communication for Large Language Models" uses "communication compression".
- "Multi-Agent Collaboration: Harnessing the Power of Intelligent LLM Agents" survey.
- "Multi-Agent Communication Learning for ..."
- "Efficient Multi-Agent Communication for Large Language Models via ..." 
Could be "DacAgent: A Dynamic Communication Topology for LLM-based Multi-Agent Systems" perhaps.
- "DART: Dynamic Agentic Retrieval..." 
- "GPTSwarm: Language Agents as Optimizable Graphs" includes edge optimization with "graph-based cost" and token cost.
- "DyLAN: Dynamic LLM-Agent Network for Task-Oriented LLM Collaboration" arXiv:2310.02170, AAAI 2024? It dynamically selects team and communication topology, measured communication efficiency? It claims 25% cost?
- "AgentPrune: Reducing Redundancy in Multi-Agent Debate via..." arXiv 2504? not yet perhaps.
- "Multi-Agent Debate with Sparse Communication" (Sparse MAD).
- "Selective Communication: A Communication-Efficient Multi-Agent Framework for..." 
- "MALT: Improving Reasoning with Multi-Agent LLM Training".
- "AgentVerse: Facilitating Multi-Agent Collaboration and Evolving..." has phase.
- "Optima: Optimizing Effectiveness and Efficiency for LLM-based Multi-Agent System" arXiv 2410.08115? It has "cost reward" and "conversation manager". Venue ICLR 2025 maybe. Measures token costs.
- "ADAS: Automated Design of Agentic Systems" arXiv 2408.08435, ICLR 2025; search workflows, measures success/cost.
- "AFlow" automation.
- "MaAS" architecture search.
- "GPTSwarm" graph.
Question explicitly names GPTSwarm, AFlow, MaAS likely wants those under topology/cost. We need report exact numerical tables relevant to savings.

Maybe this is a literature verification task, not need exhaustive obscure summarization. We should state no verified publication directly establishing LLMLingua as inter-agent message compressor; agent summarization examples are claims. Need potentially include OWED entries for unnamed paper.

Let's search memory from scholarly data.

GPTSwarm:
Exact title "GPTSwarm: Language Agents as Optimizable Graphs"
Authors Mingchen Zhuge, Haoran Chen, Yilun Zhao, Darshana Shah? Wait.
arXiv:2402.16823 (Feb 26 2024)
Venue ICML 2024? Paper likely Proceedings of the 41st International Conference on Machine Learning (ICML 2024), PMLR 235, pp 459??. It treats LLM agents as nodes and edges as functions, uses REINFORCE, "Graph Swarm" perhaps.
Numbers from abstract: "GPTSwarm can optimize the capability and cost of language agents, and achieves 10.7% improvement in accuracy and 17.7% reduction in token cost over GPT-4o? ... enables dynamic model assignment." Let's find exact.

I recall reading GPTSwarm GitHub/paper. Abstract:
"we model the LLM-based agents as a dynamical system and optimize the agent system as a graph. We propose GPTSwarm,
