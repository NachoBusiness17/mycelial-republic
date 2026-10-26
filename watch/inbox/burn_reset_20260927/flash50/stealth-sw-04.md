# stealth-sw-04: Chaos engineering applied to AI agent systems

Date: 2026-09-28. Seat: stealth-sw-04. Method: WebSearch + WebFetch (z.ai web_search_prime backend) this session. Every claim below names how it was verified. Items marked [search-result] were read only as search-engine summaries; the underlying page was not fetched, so their numbers are findings, not verified facts. Two fetch failures are recorded rather than papered over. No fabrication: anything I could not verify is flagged as such.

## 1. The field splits into two directions

The literature in 2025-2026 splits cleanly:

1. **Chaos FOR agents**: injecting faults into agent pipelines (LLM API calls, tool calls, inter-agent messages) to measure resilience.
2. **Chaos BY agents**: LLM agents generating and running chaos experiments against ordinary distributed systems.

Both are mature enough to have papers and production tooling.

## 2. Chaos FOR agents: how teams inject failures

### MAS-FIRE (arXiv:2602.19843, Jia, Deng, Chen, Wang, Zheng; submitted 2026-02-23) [abstract fetched directly]

The most complete agent-native fault taxonomy found:

- **15 fault types** in two families: intra-agent cognitive errors (failures inside one agent's reasoning) and inter-agent coordination failures (message passing between agents).
- Core thesis: agents coordinate "through unstructured natural language rather than rigid protocols," so they suffer **semantic failures** (hallucinations, misread instructions, reasoning drift) that "spread silently without runtime exceptions." Classic infra chaos (kill a pod, drop a packet, add latency) cannot reach this fault class; end-to-end success metrics alone cannot show how failures emerge or how agents recover.
- **Three non-invasive injection mechanisms**: (1) prompt modification, (2) response rewriting, (3) message routing manipulation. All operate on the agent system's own communications, zero code changes.
- Findings across three representative MAS architectures: fault-tolerant behaviors organize into **four tiers: mechanism, rule, prompt, reasoning** (a fine-grained diagnosis ladder: at which tier did the system absorb or fail the fault); **stronger foundation models do not uniformly improve robustness**; topology matters equally, with "iterative, closed-loop designs neutralizing over 40% of faults that cause catastrophic collapse in linear workflows."

### AgentChaos [search-result: agentpatterns.ai, scholarbro.com, Hugging Face discuss]

- Injects faults at the **HTTP layer of LLM API calls**: since every agent system reaches models through APIs, that single chokepoint makes agent chaos "a systems problem, not a model problem."
- Benchmark-hygiene detail worth stealing: it **verifies an injected fault was actually triggered and filters untriggered cases** from scoring. In a nondeterministic LLM system a perturbation can silently not take effect, so verifying the injection itself is part of the method.
- Reported: robustness scores track **agent architecture more than model choice**. (Underlying pages not fetched.)

### ReliabilityBench [search-result only]

- Chaos-engineering-style fault injection framework with four fault categories: **timeouts, rate limits, partial responses, schema drift**, applied under repeated execution, semantic perturbation, and tool/API failure conditions. Headline claim from search summaries: **rate limiting is the most damaging failure mode for agents**. No arXiv ID surfaced this session; the paper itself was not read, so treat as unverified until it is.

### AgentCheck (arXiv, Jul 2026) [search-result only]

- A "Reproduce-Intervene-Mitigate" workbench. Search summary claims fault injection succeeded in all 120 scenarios with every agent engaging, plus a 36-scenario reproducibility re-run. Page not fetched.

### Chaos BY agents: ChaosEater (arXiv:2501.11107, Kikuta, Ikeuchi, Tajiri, CyberAgent, Jan 2025) [search-result]

- Automates the full chaos-engineering loop for distributed systems (Kubernetes): **fault hypothesis generation, fault injection, post-injection analysis**, tasks that traditionally need senior SREs.
- Converts chaos experiment plans **to Infrastructure-as-Code automatically**, and **automatically identifies and recovers from errors during fault injection** (the chaos tool itself must be resilient).
- OpenReview title: "LLM-Powered Fully Automated Chaos Engineering: Towards Enabling Anyone to Build Resilient Software Systems at Low Cost." Note the inverted role: the LLM is the chaos engineer, not the chaos subject.

### Agent-run chaos tooling [search-result]

- **AWS Chaos Engineering MCP Server** (GitHub): converts natural-language descriptions into validated AWS Fault Injection Service experiment templates, so an LLM agent can author chaos experiments through MCP tool calls.
- **DragonCrawl** (via Emergent Mind): LLM-driven mobile chaos testing, dynamically crawling app flows under fault injection.
- AWS Builder community post (Sep 2026): "Chaos Engineering for Serverless AI Pipelines," framed as "breaking your own agents."

## 3. Self-healing agent patterns

### A tier ladder by blast radius (synthesis of the fetched sources)

- **Per-call**: retry with exponential backoff and jitter for transient 429s/timeouts.
- **Per-tool**: circuit breakers, fallback routing to alternate providers or tools.
- **Per-run**: checkpointing for resumable runs, replanning, automatic prompt self-correction when output is malformed.
- **Per-system**: reflective runtimes that repair the agent's own prompts and propose code fixes.

### Agent circuit breaker (agentic-patterns.com/patterns/agent-circuit-breaker; page fetched in full)

- Three states: **closed** (calls pass, failures counted), **open** (calls blocked instantly, cached error or fallback returned), **half-open** (after cooldown, exactly one probe call; success resets to closed, failure re-opens). Transitions: closed to open when failure count hits threshold; open to half-open when cooldown elapses.
- Reference Python implementation on the page: `AgentCircuitBreaker(failure_threshold, cooldown_seconds)` raising `CircuitOpenError` while open, with `opened_at` tracking for the cooldown.
- Agent-specific adaptations: **token-aware thresholds** (trip after N tokens wasted, not just N failures), **fallback routing** (notify the agent's prompt when a circuit opens so it replans with alternate tools), **per-tool breaker instances**, **session-scoped state** (reset between sessions, unlike persistent microservice breakers).
- Tuning from the page: fast APIs threshold 3 / cooldown 30s; slow tools (scraping, compilation) threshold 2 / 120s. Claimed **40-60% token savings** in production agent systems, evidence grade "medium" per the page's own grading.
- Avoid when: all tools local/deterministic, or single-shot agents with no retry logic.

### VIGIL (arXiv:2512.07094, Christopher Cruz, Dec 2025) [abstract fetched directly]

A reflective runtime supervising a sibling agent (it performs autonomous maintenance, not task execution):

- Ingests the agent's behavioral logs, appraises each event into structured emotional representations, and keeps a persistent **EmoBank** governed by decay and contextual policies.
- Runs as a **state-gated pipeline: illegal transitions raise explicit errors instead of letting the LLM improvise**. Containment law: the runtime, not the model, decides which state transitions are legal.
- Emits an **RBT diagnosis** classifying recent behavior into strengths, opportunities, and failures, then generates **guarded prompt updates that preserve the agent's core identity semantics**, plus read-only code proposals from a strategy engine working from log evidence and identified code hotspots.
- Case study: detected elevated reminder latency, proposed both prompt and code repairs, and when its own diagnostic tool failed on a schema conflict it surfaced the internal error, produced a fallback diagnosis, and emitted a repair plan. The paper calls this "meta level self repair in a deployed agent runtime."
- Two sibling papers surfaced in search (not fetched): VIGIL runtime enforcement of behavioral specifications on agent skill traces (arXiv:2606.26524, reported 95.8% recall / 89.6% precision) and VIGIL tool stream injection defense (arXiv:2601.05755).

### AWS Well-Architected AGENTREL07-BP02 [search-result; direct fetch FAILED]

Search summaries say: extend retries into full recovery workflows, give common failure patterns targeted remediations, and use automatic prompt refinement for malformed LLM output. Honest note: my fetch of the BP02 page returned only the generic Machine Learning Lens intro (title, no BP02 body), so this item rests on the search summary alone. Same for a follow-up Cruz paper (arXiv:2603.00495) arguing post-hoc diagnostics are insufficient for long-horizon agent failures.

### Classic distributed-systems imports [search-result summaries]

- Circuit breakers and bulkheads to contain retry storms; sagas and outbox patterns for correctness when microservices integrate agents (uberconf talk summary).
- Checkpointing for crash-safe resumable workflows; fallback chains across models/providers (multiple practical write-ups: agentiveaiagents.com, dev.to self-healing test frameworks with AI fallback locator ranking).

## 4. Cross-cutting findings

1. **Semantic faults are the agent-native fault class.** MAS-FIRE: failures "spread silently without runtime exceptions," so exception-based monitoring is blind to them; injection must operate at prompt and message level, not just infra level.
2. **Injection verification is mandatory.** AgentChaos filters untriggered faults from scoring. A chaos experiment on a nondeterministic system needs its own check that the fault actually landed; otherwise you measure noise.
3. **Architecture beats model upgrades.** Two independent sources agree: MAS-FIRE (closed-loop topology neutralizes over 40% of catastrophic faults; stronger models do not uniformly help) and AgentChaos (robustness tracks architecture more than model choice).
4. **Rate limiting is the most damaging injected fault** per ReliabilityBench search summaries. This repo's own fan-out width law (dispatch shape, not width alone, caps throughput; 429/1302 storms) is the same physics observed in production.
5. **Self-healing converges on: runtime owns legality, model proposes repairs.** State-gated pipelines raise explicit errors, guarded prompt updates preserve identity, code fixes stay read-only proposals until verified. Self-healing output is a candidate, and something downstream gates it.
6. **The open loop**: no fetched source yet closes the circle of an agent running ChaosEater-style experiments on its own pipeline, verifying the injection landed, and feeding MAS-FIRE-style tiered findings into guarded self-repair. That composite (chaos BY agents aimed at chaos FOR agents, with verification) is the gap the field is approaching but has not landed.

## Sources

Fetched in full this session:

- https://arxiv.org/abs/2602.19843 (MAS-FIRE)
- https://arxiv.org/abs/2512.07094 (VIGIL)
- https://agentic-patterns.com/ and https://agentic-patterns.com/patterns/agent-circuit-breaker

Fetch attempted, failed (recorded, not faked):

- AWS ML Lens AGENTREL07-BP02 page (returned lens intro only)
- export.arxiv.org API queries (HTTP 429)

Search-result level only (pages not fetched):

- ChaosEater https://arxiv.org/abs/2501.11107 (also OpenReview)
- ReliabilityBench (no arXiv ID found this session)
- AgentCheck (arXiv, Jul 2026, no ID captured)
- AgentChaos (agentpatterns.ai / scholarbro.com / discuss.huggingface.co)
- AWS Chaos Engineering MCP Server (github.com), DragonCrawl (emergentmind.com)
- builder.aws.com serverless AI pipelines chaos post; uberconf agentic microservices talk
- VIGIL siblings arXiv:2606.26524, arXiv:2601.05755; Cruz follow-up arXiv:2603.00495
