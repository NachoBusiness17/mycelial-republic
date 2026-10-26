# sweep: swarm-orchestration via HN

source-fetched: 2026-10-01
Gopher: sweep-swarm-orchestration-hn (frontier sweep, Mag Resource Harness)
Door: Hacker News via Algolia API (hn.algolia.com/api/v1/search_by_date, numericFilters created_at_i>1788220800 = since 2026-09-01). Door never 403'd; no fallback needed.

## Method

Pass 1 (broad sweep): 12 Algolia queries (multi-agent, agent orchestration, rate limit LLM, speculative decoding, mixture of agents, swarm agents, 429 LLM, backoff retry, self-consistency, ensemble decoding, token cost agents, agent supervisor orchestrator). Raw candidate pool: 100+ story rows from the last 30 days; 40+ distinct relevant candidates after dropping off-topic hits (SETI satire, password-manager asks, RGB lighting). "mixture of agents", "self-consistency", and "ensemble decoding" as exact phrases returned zero story hits in the window: the flock-decode vocabulary is NOT the public HN vocabulary right now, which is itself a finding for the lens/laws.md flock question.

Pass 2 (deep read): fetched and read end to end, via news.ycombinator.com/item?id=NNN unless noted:
1. 49911995 Launch HN: Magnitude (YC S25) self-optimizing inference engine for agents (178 pts, 87 comments)
2. 49772806 Orchestrating Claude Code Agents: The Chief of Staff Pattern (25 pts, 23 comments)
3. 49596054 Speculative Decoding in vLLM on AMD GPUs (145 pts, 53 comments)
4. 49689454 Ask HN: Multi-agent workflows in production; 1000s of agents? (6 comments)
5. 49574349 TokenOps: Cost-to-Outcome Frontier in Multi-Agent Systems (HN thread + github.com/theagentplane/tokenops README)
6. 49783040 Ask HN: Is provider KV caching sufficient for agent swarms? (0 comments, ask text only)
7. 49847249 Ask HN: Has anyone built a leaderless multi-agent system? (2 comments)
8. 49800187 Show HN: Relay, self-hosted LLM gateway with request pacing (3 comments)
9. 49758259 Keeping vLLM's Prefix Cache Warm Between Agent Turns (article: doug.sh/posts/vllm-kv-cache-agents/)
10. 49711603 Who bankrolls the AI agent swarm? (article: noperator.dev)
Only items actually read are banked.

Overlap greps run against catalog/catalog.jsonl and memory/ (grep -i, per title and distinctive phrase, output bounded):
- "chief of staff": only memory/runs/x_bookmark_harvest_20260905/shift9_targets.json:313, an unrelated GrokBot recap note. Item is new to the estate.
- "magnitude": catalog hits are watch/inbox/physical_computing/receipts/GA_SIGNAL_MAGNITUDE.md (signal processing receipt) and an unrelated arxiv title. The inference engine is new.
- "prefix cache": real overlap. memory/design/compact-anchor-context-mechanism.md:15,164,207 and memory/improve/deepseek_api/multi_agent_integration_plan.md:4 already design around provider prefix caches. The doug.sh measured numbers and tool-schema-sorting bug are the new part.
- "tokenops" / "cost-to-outcome": only reference/gstdcoin/ai/frontend/src/hooks/useTokenOps.ts (unrelated frontend hook). New.
- "speculative decoding": catalog holds 5 arxiv abstracts (Osprey 2609.09338, ECHO 2609.17241, LoopSpec 2609.17184, Jina-OCR-v1, PELM, under state/arxiv/2026-09-*). The vLLM-on-AMD operator thread adds throughput numbers the abstracts lack.
- "request pacing" / "queue-first": only a match inside memory/thinking/app_reasoning.jsonl (our own subagent trace). New.
- "per-agent tracing" / "1000s of agents": zero hits. New.
- "leaderless": memory/facts/fuel_feed.jsonl:276,443 and memory/facts/ox_artifact.jsonl:302,305 already hold leaderless swarm/flock consensus material. Conceptual overlap; the HN ask adds nothing beyond that.

## Answers to the four research questions

### Q1. Fan-out and retry shapes vs the estate's measured split

The estate holds: workflow children maxAttempts 0 (die on first 429/1302), Task agents maxAttempts 11 + driver backoff on the main-session retry path, limit is rolling throughput not width, width 10 measured clean at 109.4M tok/h (corpus/steal/TETHERED_LINK_STEAL_20260925.md, watch/inbox/burn_wave_20260926/B2_443). What the HN window adds:

- The strongest public alternative shape is admission control, not retry: Relay (49800187) queues and paces requests against configured provider limits instead of firing then retrying, and treats provider/cache affinity as part of the routing decision (sticky per conversation so the prefix cache survives). Nobody in the window publishes a measured maxAttempts split; the estate's ledger is more instrumented than anything I read.
- Magnitude (49911995) moves the fan-out problem into the engine: shared prefix-tree caches, KV quantization, automatic speculative drafting, with commenters naming agent workloads as "bursty and interleaved" and the real bottleneck "KV cache for 5+ concurrent 128k contexts on 24GB VRAM". Same physics as our rolling-throughput finding: the cap is memory bandwidth and cache reuse, not a width number.
- The production Ask (49689454) found no one publishing width numbers either; operators report observability (per-agent tracing) as the scaling bottleneck, with one K8s operator running pods-per-N-agents on OpenTelemetry + Prometheus.
- Actionable for the estate: a gateway-side pacing lane (Relay shape) would sit above both our shapes: schedule the fan-out against the rolling window instead of paying the 429 tax. Worth one experiment in the next burn wave.

### Q2. Flock / multi-model decode state

- Speculative decoding is now boring operator infrastructure: the vLLM AMD thread (49596054) treats draft-verify as memory-bound arbitrage, three tokens at "the (memory read) price of one", with acceptance rates workload-dependent (~80 t/s on predictable code/JSON vs ~45 on prose, Qwen 3.8 27B class on 4x R9700).
- The estate's 5 cataloged arxiv spec-dec abstracts (Osprey target-agnostic drafters, ECHO hierarchical orchestration with bonus logits, LoopSpec) cover the drafting side; what is missing for the flock decode redesign is the VOTING/consensus side: zero HN story hits in 30 days for "self-consistency", "ensemble decoding", or "mixture of agents". The public thread has moved to single-model+drafter, away from multi-model voting.
- The closest flock-shaped public signal is the 0-comment Ask (49783040) asking whether provider KV caching supports forking agents from the same cached prefix and manually persisting caches: exactly the shared-prefix flock shape in lens/laws.md, and it got no public answers. The field is open; the redesign should cite the spec-dec verification economics (cheap drafter, expensive verifier) as the load-bearing prior, and note the prefix-fork Ask as evidence nobody ships this yet.

### Q3. Controller-of-controllers and the one-controller law

The Chief of Staff thread (49772806) is the densest failure-mode catalog in the window, and it is all about the CONTROLLER being the unreliable component:
- Coordinators fail like any agent: empty assertions, stale memory (zhoujinliang runs several in parallel and picks one output).
- An orchestrator "ordered more and more tests" for two weeks and delivered an unusable product (traktorn); teams wrote "tests that test tests" and 10K-line PRs (nvch); a shared grammar tweak caused a 10K-line commit explosion (gritzko, who keeps the pattern but says it "devolves into a mess real fast" without oversight).
- Mitigations named: phase-scoped orchestrators (~4-5h, fresh context per phase, human review between phases) to control the controller's own context decay; keeping the chief only for "mundane things".
- The leaderless counterfactual (49847249) drew 2 comments and zero design substance; nobody public is running leaderless. The estate's one-controller law is consistent with public practice, and the public failure catalog (coordinator drift, scope explosion) validates the law's premise: the controller is the highest-variance agent, so it needs the tightest contract. The estate's facts already hold leaderless consensus math (memory/facts/fuel_feed.jsonl:276,443); public discourse has not caught up.

### Q4. Per-agent-turn cost accounting

- TokenOps (49574349 + README) is the direct comparable: run-aware token governance, one budget per multi-agent workflow, enforced before every model call with a halt, shared ledger across processes, and per-agent attribution afterwards ("the Dashboard attributes cost per agent"; claims up to 65% waste cut). It is a BUDGET GOVERNOR, not a per-turn ledger: no per-turn row format, no cost-to-outcome measurement despite the title. The estate's memory/runs/hermes_burn/usage.jsonl (16 rows, $5.9155 window 1) is finer-grained than anything public I found; nobody in the window publishes a per-agent-turn ledger schema.
- The doug.sh post (49758259) contributes the metric that should sit next to our ledger: cost per turn is dominated by cache-hit share, measured 55% to 95% cached (27s to 7.3s first-token) by fixing prompt instability, with the closing law "Measure the share of prompt tokens served from cache, not the number of cache hits."
- noperator.dev (49711603) frames swarm economics qualitatively: "This is not the kind of workload you launch casually"; spend visibility is the traceability anchor. No numbers.
- Suggested fold: add a cache-hit-share column to usage.jsonl rows (the data may already be in provider responses) so the descent protocol's per-turn banking captures the true marginal cost per turn.

## Banked items (8, strongest first)

See the JSON result for the structured entries. Every quote below was carried back verbatim from the fetched page by this session's fetches.

## Door status

All fetches succeeded. No 403s, no degraded reads. The only thin reads were small threads (TokenOps 1 comment, KV-caching Ask 0 comments, leaderless Ask 2 comments); for those the ask/README text itself was read as the signal, which the recipe's "the thread is often the real signal" clause covers in reverse.
