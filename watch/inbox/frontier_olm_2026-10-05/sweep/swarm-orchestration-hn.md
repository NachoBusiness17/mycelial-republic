# sweep: swarm-orchestration via hn (2026-10-05)

source-fetched: 2026-10-05. Door: Hacker News via hn.algolia.com API (search_by_date and /search, numericFilters created_at_i>1788566400 = 2026-09-05 window) plus news.ycombinator.com item pages for threads and the linked articles/repos for strong hits. No door 403'd. One degradation: a search_by_date query for "Evennia" returned typo-tolerant junk (unrelated "evening"/"EventMaxxer" rows); retried with /search relevance and got clean results - reported as the retry, not a fabricated fallback.

## Method

- Pass 1 (broad): 12 Algolia queries (multi-agent; LLM agents; "rate limit"; model routing; swarm agents; consensus LLM; Minecraft agents; Evennia x2; AzerothCore; "exponential backoff" agents; playerbots). About 130 rows returned, 45+ distinct in-window candidate stories considered.
- Pass 2 (deep): 8 items read end to end (HN thread pages plus linked pages). 2 dropped as already-held by the estate (see Drops). 7 banked.
- Overlap check per candidate: grep -c -F against catalog/catalog.jsonl (1,096,848 rows) and grep -rlF against memory/. The memory/trajectory/steps.jsonl and memory/thinking/app_reasoning.jsonl hits were verified to be this run's own telemetry (the grep loop's own phrases echoed into the step log), not holdings.

## Findings by research question

### Q1 retry / backoff / admission control vs rolling-throughput caps (429/1302-class)

The public shape is converging on queue-and-pace (admission control before the request fires) rather than retry-after-failure. Relay (banked below) is the cleanest statement: queue-first routing absorbs bursts, per-model cooldowns, and a "wait budget" that prefers waiting for the preferred model over degrading to a weaker one. That is a different dispatch shape from our Task-agent retry path (maxAttempts 11 + driver backoff, AGENTS.md fan-out width law): it spends latency instead of spend-and-retry. Nothing in the window reported width-vs-429 boundary measurements comparable to our R062 429s-only-at-width-13 finding; our envelope data is still ahead of what HN carries.

The strongest throughput lever found is not retry tuning at all but prompt-prefix determinism: doug.sh's vLLM prefix-cache post (banked) shows 55% to 95% cached-token share and 26-28s to 7.3s time-to-first-token purely from making every turn's prompt serialize identically (sort JSON keys in tool schemas, push volatile content to the end). This independently validates the estate's byte-identical-asks-for-cache-hits law (corpus/steal/ZCODE_OPERATING_PLAYBOOK_20260925.md) from the serving side. The Magnitude thread (banked) adds the operator-side confirmation: single-stream tok/s is not the pain; the cold-context wake after each tool call is.

### Q2 heterogeneous-tier dispatch (cheap workers + scarce premium judgment)

"Most Agent Turns Don't Need a Frontier Model" (banked) is the direct hit: public routing math from LangChain's Switchyard benchmark showing only ~7% of agent turns needed the frontier model (93% handled by a 30B), 74% cost reduction against roughly six points of accuracy loss, and teams routing nothing paying about 4x more than necessary. This is public corroboration of the driving ladder's cheap-first shape (local janitors + scarce premium, AGENTS.md) and of THE DESCENT PROTOCOL's cheap-first SHERPA leg. The new quantitative bit the estate did not have: the ~7% frontier-turn share and the 4x no-routing penalty as public numbers we can cite when justifying tier assignments.

### Q3 game-world repos as long-horizon multi-agent coordination benchmarks

Negative result, cleanly established: in the 30-day window there are ZERO HN stories for AzerothCore, ZERO for playerbots (mod-playerbots), and ZERO for Evennia. Evennia's newest HN story ever is 2024-12-18 (id 42447779, 3 pts, 0 comments); its flagship thread is 2023-08-31 (id 37339098, 111 pts, 78 comments), pre-agent-LLM era. Nobody is publishing HN-visible results on these repos as agent benchmarks. The nearest in-window proxies (MineTrials, banked; AsyncLLM's DOOM demo, already held) are explicitly single-agent: MineTrials has no multi-agent coordination at all, and AsyncLLM's coordination is among coroutines inside one agent. The estate's catalog rows (azerothcore-wow 10,356 / mod-playerbots 5,019 / evennia 1,579) as long-horizon coordination benchmarks remain unclaimed territory on this door; a first-publication claim would need a separate literature check beyond HN before asserting it globally.

### Q4 no-throne consensus (N lanes merging without a coordinator)

Two banked items bracket the problem. "Extraordinary Multi-Agent Delusions" (banked) is the consensus-illusion law made empirical: in a grader experiment, when agents' private signals conflicted with a shared board, they treated the board as aggregating independent signals when it was actually conformity; agents cited the board majority over 90% of the time when rationalizing; communication made the swarm more consistently wrong; the proposed fix is institutional (require agents to post raw private results), which maps directly onto the estate's receipts-and-verdicts discipline. The Ask HN leaderless thread (banked) shows the question is live but unanswered: 3 comments, no substance, no shared experience. Foremerge (dropped, already held) remains the estate's best-known no-throne mechanism: advisory intent claims in shared state, deterministic flagging, hard stop only at acceptance for HIGH signals, tested to 98 parallel agents. Combined picture: nobody on this door has a working no-throne consensus story; governance-of-communication (raw-result posting, advisory leases, deterministic checks) is the direction of travel, which is what the estate already does.

## Drops (already held; re-banking is waste)

- Foremerge (HN 49789356): already claimed by memory/runs/mickey17_v2/runs/agent-engineering-frontier-sweep-40/lanes/hn-week.json with an audit row in hn-week.checks.json. Catalog grep 0; memory hit is the prior sweep's lane file.
- AsyncLLM "LLMs are General Asynchronous Agents" (arXiv 2609.35427): already in catalog as row bba80b62c361 (state/arxiv/2026-09-29/2609.35427v1.txt, mtime 2026-09-29). My page read added only marginal detail beyond the held abstract.

## Banked items (7, strongest first)

Full structured records are in the SweepResult JSON. Quote provenance: each quote is verbatim from the fetched page as extracted by the fetch tool (model-mediated extraction; confidence held at 0.8-0.85 accordingly, not 1.0).

## Door health

All 12 query fetches and 9 page fetches returned live. The only anomaly was the Evennia search_by_date junk-result row (degraded, retried via /search as the recipe's fallback path allows). AzerothCore, playerbots, and "exponential backoff" agents legitimately returned ZERO HITS (empty result, not an error).
