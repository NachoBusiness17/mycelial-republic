# w3-research-selfplay: self-evolving LLM agents 2025-2026 (research receipt)

- Item: w3-research-selfplay (flash50 workflow dig)
- Date: 2026-09-28
- Ask: who has built agents that improve themselves through their own experience; key papers, repos; whether any use a receipt/ledger system like ours for tracking self-modifications. OWED if unverifiable.
- Method (everything below was fetched or read this session): 11 WebSearch queries, 20 WebFetch page fetches, 3 local file reads. All arXiv facts come from the arXiv abs pages fetched 2026-09-28; all repo facts come from the GitHub pages fetched 2026-09-28. Star counts are point-in-time from those fetches and will drift. The search backend threw intermittent rate-limit errors (MCP -429 / "1302") on several queries; where a fact rests on a search-result summary instead of a fetched page it is labeled search-level below.

## 1. Landscape: four families

The field has consolidated enough that two 2025 surveys exist and both were fetched and verified:

- arXiv:2507.21046, "A Survey of Self-Evolving Agents: What, When, How, and Where to Evolve on the Path to Artificial Super Intelligence", Gao et al. (27 authors), v1 2025-07-28, v4 2026-01-16, published in TMLR 01/2026. Taxonomy: WHAT to evolve (models, memory, tools, architecture), WHEN (intra-test-time vs inter-test-time), HOW (scalar rewards vs textual feedback, single vs multi-agent). Calls itself "the first systematic and comprehensive review of self-evolving agents".
- arXiv:2508.07407, "A Comprehensive Survey of Self-Evolving AI Agents: A New Paradigm Bridging Foundation Models and Lifelong Agentic Systems", Fang et al., v1 2025-08-10. Proposes a unified System Inputs / Agent System / Environment / Optimisers frame and reviews evolution per domain (biomedicine, programming, finance) plus safety and ethics.

Families found in the verified corpus:

1. Experience-to-memory (no weight updates): AWM, Memento, ReasoningBank, EvolveR.
2. Experience-to-weights (self-generated training data or rewards): SEAL, Early Experience, Absolute Zero, AgentEvolver.
3. Prompt/context/workflow evolution (the agent improves its own instructions or code): GEPA, ACE, DGM, AlphaEvolve, ShinkaEvolve, OpenEvolve, EvoAgentX, Godel Agent.
4. Self-play task generation (model writes its own curriculum): Absolute Zero, AgentEvolver's self-questioning.

## 2. Key papers (all verified on arXiv abs pages 2026-09-28)

### Self-modifying-code agents (closest to the ask's "improve themselves")

- **Darwin Godel Machine (DGM)** - arXiv:2505.22954, Zhang, Hu, Cong Lu, Lange, Jeff Clune; v1 2025-05-29, v3 2026-03-12. A coding agent that rewrites its own code and keeps "an archive of generated coding agents"; empirical keep/kill on benchmarks, "increasing performance on SWE-bench from 20.0% to 50.0%". Abstract notes precautions "such as sandboxing and human oversight". Code: github.com/jennyzzt/dgm. Note: a search-result summary attributed "objective hacking observed during self-modification" to the paper; my abs-page fetch did not contain that language and I did not read the paper body, so that specific claim is search-level, not verified here.
- **Godel Agent** - arXiv:2410.04444, Yin, Wang, Pan, Lin, Wan, Wang; v1 2024-10-06, v4 2025-05-31 (also in ACL Anthology per search). Runtime recursive self-improvement: "enabling agents to recursively improve themselves without relying on predefined routines or fixed optimization algorithms". Pre-dates the 2025 wave but is the direct ancestor of the DGM line's framing.
- **AlphaEvolve (Google DeepMind)** - arXiv:2506.13131, Novikov et al. (18 authors), submitted 2025-06-16. "In this white paper, we present AlphaEvolve, an evolutionary coding agent": LLMs propose direct code changes, automated evaluators score them, an evolutionary loop iterates. Widely covered results (matrix-multiplication improvement, datacenter scheduling, Gemini training kernels) are search-level context, not re-verified here. No code release; the open implementations below are the community versions.
- **ShinkaEvolve (Sakana AI)** - arXiv:2509.19349, Lange, Imajuku, Cetin; v1 2025-09-17. Open-source evolutionary program search; innovations are novelty-driven parent sampling, code-similarity rejection sampling, bandit LLM ensemble selection; "discovers a new state-of-the-art circle packing solution using only 150 samples". Repo verified: github.com/SakanaAI/ShinkaEvolve, Apache-2.0, ~1.4k stars, ICLR 2026, "pip install shinka-evolve".
- **OpenEvolve (community)** - github.com/algorithmicsuperintelligence/openevolve (fetched; the codelion/openevolve URL lands there), Apache-2.0, ~7.5k stars / 1.2k forks. Open AlphaEvolve reimplementation with a MAP-Elites-style database (population_size 500, num_islands 5, feature_dimensions complexity/diversity/performance), a PopulationSnapshot with admit/archive/evict/migrate hooks, periodic checkpoints, and a visualizer showing an "Evolution tree with parent-child relationships".
- **EvoAgentX** - github.com/ANative-Lab/EvoAgentX (fetched via EvoAgentX/EvoAgentX URL), MIT, ~3.4k stars. "Building a Self-Evolving Ecosystem of AI Agents": workflow generation plus a self-evolution engine wrapping TextGrad, AFlow, MIPRO, EvoPrompt.

### Experience-to-memory agents (learn from their own trajectories)

- **Agent Workflow Memory (AWM)** - arXiv:2409.07429, Wang, Mao, Fried, Neubig; 2024-09-11. "A method for inducing commonly reused routines, i.e., workflows, and selectively providing workflows to the agent to guide subsequent generations." Mind2Web +24.6% and WebArena +51.1% relative success. The 2025 wave's memory line builds on this.
- **Memento** - arXiv:2508.16153, Zhou et al.; v1 2025-08-22. Fine-tuning LLM agents without fine-tuning LLMs: episodic memory + case-selection policy, "our method enables low-cost continual adaptation via memory-based online reinforcement learning". GAIA validation 87.88% Pass@3. Code cited on abs page: github.com/Agent-on-the-Fly/Memento (repo itself not fetched).
- **ReasoningBank (Google)** - arXiv:2509.25140, Ouyang et al.; v1 2025-09-29, v2 2026-03-16, ICLR 2026. Agent "distills generalizable reasoning strategies from an agent's self-judged successful and failed experiences", retrieves them at test time, writes new learnings back; adds MaTTS (memory-aware test-time scaling).
- **EvolveR** - arXiv:2510.16079, Wu et al.; v1 2025-10-17, v3 2026-05-16, ICML 2026. Closed loop: offline self-distillation where "interaction trajectories are synthesized into a structured repository of abstract, reusable strategic principles", then online task solving with retrieval plus policy reinforcement on the trajectories.

### Experience-to-weights agents

- **SEAL (MIT)** - arXiv:2506.10943, Zweiger, Pari, Guo, Akyurek, Kim, Agrawal; v1 2025-06-12, v2 2025-09-18. "A framework that enables LLMs to self-adapt by generating their own finetuning data and update directives" (self-edits), applied via SFT, with RL training the edit policy on downstream performance. Project page cited: jyopari.github.io/posts/seal.
- **Agent Learning via Early Experience (Meta-led, 30 authors incl. Jason Weston)** - arXiv:2510.08558; v1 2025-10-09, ICML 2026. "Interaction data generated by the agent's own actions, where the resulting future states serve as supervision without reward signals"; implicit world modeling + self-reflection as the two strategies. (Meta affiliation per search summary; the abs page does not state affiliations.)
- **Absolute Zero** - arXiv:2505.03335, Zhao et al.; v1 2025-05-06, v3 2025-10-16. "A single model learns to propose tasks that maximize its own learning progress and improves reasoning by solving them, without relying on any external data"; code executor validates both tasks and answers (Absolute Zero Reasoner).
- **AgentEvolver (Alibaba-affiliated team per search, 13 authors led by Yunpeng Zhai)** - arXiv:2511.10395, v1 2025-11-13. Three mechanisms: self-questioning ("curiosity-driven task generation in novel environments, reducing dependence on handcrafted datasets"), self-navigating ("improves exploration efficiency through experience reuse and hybrid policy guidance"), self-attributing ("assigning differentiated rewards to trajectory states and actions based on their contribution"). No code link on the abs page.

### Prompt/context evolution

- **GEPA** - arXiv:2507.19457, Agrawal et al.; v1 2025-07-25, v2 2026-02-14, ICLR 2026 Oral. Reflective prompt evolution: "Across six tasks, GEPA outperforms GRPO by 6% on average and by up to 20%, while using up to 35x fewer rollouts." Code: github.com/gepa-ai/gepa (cited on abs page; not fetched).
- **ACE, Agentic Context Engineering** - arXiv:2510.04618, Zhang et al.; v1 2025-10-06, v3 2026-03-29, ICLR 2026. "A framework that treats contexts as evolving playbooks that accumulate, refine, and organize strategies"; targets "brevity bias" and "context collapse"; "ACE prevents collapse with structured, incremental updates that preserve detailed knowledge" applied "through a modular process of generation, reflection, and curation". No code link on the abs page (search results referenced one; unverified).

## 3. The receipt/ledger question

Direct answer: **no verified system in the 2025-2026 self-evolving-agent corpus uses a receipt/ledger like ours.** Nothing fetched describes a human-gated, append-only, hash-pointer receipt log over an agent's own self-modifications with registered-debt semantics. Two searches on the topic came back as follows:

- Query "LLM agent self-modification audit ledger receipt tracking system": results were irrelevant (image-captioning surveys, municipal web pages). Negative result; no such named system is well-indexed under that vocabulary.
- Query "tamper-evident audit log AI agents safety monitorability arxiv 2025": surfaced only governance/oversight work at search-summary level - a control-theoretic governance architecture (Dec 2025) proposing tamper-evident logs as design-time controls, a "Frontier AI Auditing" proposal (Jan 2026) for third-party audits with cryptographic provenance tooling, CoT monitorability (arXiv:2507.11473), and an IETF draft benchmark requiring tamper-evident operation logs for AI agents. These are external-oversight proposals, not an agent's own self-mod ledger, and I did not fetch their full texts, so they stay search-level. Exact arXiv ids for the governance/auditing items: OWED.

What exists instead, ranked by proximity:

1. **Evolutionary archives with lineage (machine provenance, not receipts).** DGM's "archive of generated coding agents" (arXiv:2505.22954), ShinkaEvolve's "archive of successful solutions, enabling knowledge transfer between different evolutionary islands" (repo README), OpenEvolve's MAP-Elites database with admit/archive/evict/migrate hooks and checkpointed "evolution tree with parent-child relationships". These record parentage and metrics so automated selection can keep/kill variants. What they lack vs ours: no human gate before a modification is promoted (DGM promotes on benchmark score alone), no no-fabrication law, no notion of registered vs fixable debt. Note: the DGM repo README (as fetched) documents output_dgm/ and Google-Drive FM logs but does not document the on-disk archive format; I did not clone the repo, so its exact archive schema (e.g. jsonl with parent ids) is OWED.
2. **ACE's incremental delta playbook** is conceptually the closest to a ledger of self-modifications for context: structured, incremental, bullet-level updates that preserve detail instead of rewriting. But the paper describes no tamper evidence, no append-only event log, and no operator gate.
3. **External audit/governance tamper-evident logging** (search-level, above) wants the property our inbox log has, but as an oversight layer bolted on for regulators, not as the substrate the agent itself improves through.

Grounding of "ours" (read this session):

- watch/inbox/INDEX.json:5: "INDEX.json is now DERIVED from the append-only event log index_events.jsonl (Ethereum fold pattern, EXP-002A). Writers APPEND events; they never rewrite this file or the log. The log is the source of truth." (event_count 4696, active_items 1415 at INDEX.json:10-14, derived 2026-09-28).
- memory/workflows/REGISTRY.jsonl:1-3: append-only per-run rows {ts, name, script digest, verdict, G1-G7 check results} - every workflow gate check registers a fact, including its own FAILs.
- tools/violation_ratchet.py:2-28: "fingerprint-ratcheted violation gate": sha256 fingerprints (first 16 hex) over (rule, file), "debt that exists today is a REGISTERED CLAIM in the baseline; only NEW violations fail", registration only by named baseline-update, exits 0/1/2, receipts cited in the docstring (B2-95, B2-11).

Assessment (mine, not sourced): the estate's loop is effectively a DGM with receipts. The keep/kill predicate is the same shape (empirical validation: their SWE-bench, our pytest + ratchet + workflow gate); the archive is the same shape (their agent archive, our git history + watch/inbox receipts). The difference is direction of authority: DGM's archive accepts automatically on score, ours requires receipt-before-promotion, named debt registration, and gates whose own failures append to a registry. The literature surveyed here has the machinery (lineage, metrics, archives) but not the audit law; the governance literature wants the audit law but is not building self-improving agents with it. The conjunction - a self-improving agent whose self-modifications are receipt-gated in an append-only ledger - appears to be unclaimed territory as of what I could verify today.

## 4. OWED (unverified, not fabricated)

1. DGM on-disk archive schema (parent-id fields, file format): requires cloning github.com/jennyzzt/dgm and reading DGM_outer.py. Not run this session.
2. Exact arXiv ids for: the Dec 2025 control-theoretic governance architecture, the Frontier AI Auditing proposal, the IETF AI-agent security benchmark draft. Search-summary level only.
3. ReasoningBank's "objective hacking"/safety-annex analogue for DGM: the "objective hacking observed during self-modification" attribution is search-level; the paper body was not read.
4. Code-repo existence for ACE and AgentEvolver (abs pages carry no links; search results hinted at repos). Unverified.
5. Repo URLs cited only from abs pages and not fetched: gepa-ai/gepa, Agent-on-the-Fly/Memento, SEAL project page jyopari.github.io/posts/seal.
6. AlphaEvolve results coverage (matrix multiplication, datacenter scheduling): search-level context only; the white paper abstract itself was fetched but does not carry those numbers.
7. Search backend rate limits (MCP -429 / "1302" errors) degraded several queries; some landscape corners (e.g. Sakana's AI Scientist line, TextGrad/DSPy specifics, post-2026-03 revisions) are under-covered by this receipt.

## Receipt

- Instruments run this session: WebSearch x11, WebFetch x20 (16 arXiv abs pages + 4 GitHub pages), Read x3 (INDEX.json, REGISTRY.jsonl, violation_ratchet.py), bash ls/git status x2. No tests were run: this is a research item, the ask names no suite, and the local reads are receipt-grounding only.
- Banked: watch/inbox/burn_reset_20260927/flash50/w3-research-selfplay.md (this file).
- Sources: all arXiv ids and GitHub repos listed in section 2, fetched 2026-09-28; local files cited by path:line in section 3.
