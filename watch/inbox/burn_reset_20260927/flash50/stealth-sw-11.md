# stealth-sw-11: Open-source AI agent landscape, September 2026

Lane: sw-11 (stealth flash50). Date: 2026-09-28 (local EDT; GitHub API timestamps read 2026-09-28/29 UTC).

## Method (what I actually ran this ask)

- 6 web searches via WebSearch: 4 returned results, 2 died mid-fanout with upstream 1302 rate-limit errors (recorded in the tool output, not papered over).
- 1 page fetch via WebFetch: langfuse.com blog "Comparing Open-Source AI Agent Frameworks" (updated July 2026 per that page).
- 1 GitHub REST API census, run here: `curl -s https://api.github.com/repos/<owner>/<repo>` piped to the repo venv python (`C:\Users\foste\Documents\projects\local_sovereign_agent\.venv\Scripts\python.exe`) parsing `stargazers_count`, `pushed_at`, `forks_count`, license SPDX, archived flag; plus 2 `api.github.com/search/repositories` queries (OpenHands in:name, SWE-agent in:name). 20 repo lookups total; every number in the table below is from that live API output, not from a blog.

## Verified activity census (GitHub API, this ask)

| Repo | Stars | Last push (UTC) | License |
|---|---|---|---|
| n8n-io/n8n | 206,230 | 2026-09-29 | NOASSERTION (fair-code, not OSI) |
| langgenius/dify | 157,434 | 2026-09-29 | NOASSERTION (custom) |
| langchain-ai/langchain | 147,215 | 2026-09-28 | MIT |
| browser-use/browser-use | 116,635 | 2026-09-26 | MIT |
| OpenHands/OpenHands | 89,416 | 2026-09-29 | (found via search API; org renamed from All-Hands-AI) |
| FoundationAgents/MetaGPT | 70,673 | 2026-01-21 | MIT, STALE ~8 months |
| microsoft/autogen | 61,210 | 2026-04-15 | CC-BY-4.0, FROZEN ~5.5 months |
| crewAIInc/crewAI | 59,150 | 2026-09-28 | MIT |
| agno-agi/agno | 42,372 | 2026-09-28 | Apache-2.0 |
| langchain-ai/langgraph | 42,428 | 2026-09-29 | MIT |
| huggingface/smolagents | 29,565 | 2026-09-23 | Apache-2.0 |
| openai/openai-agents-python | 29,750 | 2026-09-28 | MIT |
| letta-ai/letta | 24,961 | 2026-09-10 | Apache-2.0 |
| google/adk-python | 21,671 | 2026-09-29 | Apache-2.0 |
| pydantic/pydantic-ai | 20,245 | 2026-09-29 | MIT |
| SWE-agent/SWE-agent | 20,436 | 2026-09-28 | (moved out of princeton-nlp; old path 404s) |
| microsoft/agent-framework | 13,848 | 2026-09-28 | MIT |
| SWE-agent/mini-swe-agent | 8,055 | 2026-09-28 | (new org same day) |

First batch had two failures that taught real facts: `All-Hands-AI/OpenHands` returned MISSING and `princeton-nlp/SWE-agent` returned MISSING, both resolved by the search API to renamed orgs (OpenHands/OpenHands at 89,416 stars corroborates and exceeds the ~87,800 figure a vortx.ch article from 2026-09-14 cites; SWE-agent/SWE-agent).

### Read 1: stars are vanity, pushed_at is sanity

The two most misleading repos by star count are MetaGPT (70,673 stars, last push 2026-01-21, roughly 8 months frozen) and AutoGen (61,210 stars, last push 2026-04-15, and the repo license now reads CC-BY-4.0, not the MIT a new adopter would expect). Both would sit near the top of any "most starred frameworks" list while being dead or maintenance-only as code. The actually-live front line by commit pulse on the day I checked: langgraph, pydantic-ai, adk-python, dify, n8n, OpenHands, SWE-agent, crewAI, agno, microsoft/agent-framework, all with pushes inside roughly the last 72 hours. A solo operator who adopts by star count lands on a fossil; adoption must be gated on `pushed_at` and release cadence, which is one curl to verify.

## Landscape structure (Langfuse comparison, fetched this ask)

The Langfuse July 2026 roundup covers 13 frameworks: LangGraph, LangChain DeepAgents, OpenAI Agents SDK, Claude Agent SDK, Google ADK, Pydantic AI, CrewAI, AWS Strands Agents, Mastra, Vercel AI SDK, Microsoft Agent Framework, Agno, Smolagents. Its structural verdicts, which match my own API evidence:

- **Graph-shaped (LangGraph, Microsoft Agent Framework):** explicit node structure, durable execution, auditable state; the enterprise default for complex stateful workflows. Cost note echoed by a Towards AI 2026 piece: explicit graphs make token spend predictable, conversational orchestration (AutoGen style) carries the biggest cost risk.
- **Role-based (CrewAI):** most approachable multi-agent teams; pragmatic agent isolation.
- **Code-as-action (smolagents):** about a 1,000-line core where the agent writes Python as its action space; minimal but slow release cadence, per Langfuse, consistent with its 2026-09-23 push.
- **Self-hosted runtime (Agno):** SDK plus AgentOS, the sovereignty option.
- **Consolidation:** AutoGen is explicitly legacy (Langfuse: maintenance mode, no new features; my API read shows the frozen repo and a relicensed main branch). Microsoft folded AutoGen plus Semantic Kernel into Microsoft Agent Framework, the only first-class C# option, already 13,848 stars within months. The giant generation-one projects are being cannibalized by their vendors' successors.
- **Vendor SDKs went open source:** openai-agents-python (MIT, 29,750 stars, pushed 2026-09-28) and the Claude Agent SDK (the Claude Code harness shipped as a library: hooks, permissions, in-process MCP) are free code. The moat moved from code to the harness-model pair.

## Proprietary vs open

The interesting 2026 fact: the open/proprietary line has mostly dissolved at the SDK layer and re-hardened at the model layer. OpenAI's and Anthropic's agent SDKs are MIT-licensed and provider-reachable (OpenAI Agents SDK claims 100+ models via LiteLLM per the Langfuse fetch), yet adoption concentrates on the vendor pair: a VB Pulse figure cited by bizflowai (2026-09, secondary source, not independently verified) says 69% of enterprises using OpenAI's Agents SDK make it their primary orchestrator versus 38% for Claude's platform. Open source wins where it always wins: model-agnosticism (LangGraph runs anything), self-host (Agno, Letta for memory-centric agents, Dify/n8n for no-code), privacy, and exit rights. Proprietary wins where the harness is co-designed with the model: the Claude Agent SDK loop is production-tested against exactly one model family, and that tightness is the product.

Anthropic's own engineering guidance ("Building Effective Agents", Schluntz and Zhang, December 2024; search-verified) cuts against framework maximalism from the proprietary side: start with the single simplest LLM call, distinguish workflows (predefined code paths) from agents (model-directed), build from five composable patterns (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer), and if you do use a framework, make sure you understand the underlying code so prompts do not hide behind abstraction layers.

## What a solo operator can learn (cross-checked against this estate)

1. **Gate adoption on `pushed_at`, not stars.** One curl per candidate (the exact command above) separates the live front line from the fossil generation. MetaGPT and AutoGen are the cautionary pair, both with star counts high enough to fool a resume-driven choice.
2. **The production frameworks independently converged on this estate's shape.** LangGraph's durable graph execution with checkpoints is the same design as this repo's percolator/index_events receipt chain; smolagents' code-as-action is the gopher-script pattern; the Claude Agent SDK's harness-as-library (hooks, permissions, memory files) is what AGENTS.md encodes as the Clippy block, gates, and ribs. A solo operator's durable edge is the harness and the memory, not the model: every framework that survived added receipts, gates, and state files first.
3. **Thin abstractions win at the bottom of the tier ladder.** Anthropic's five patterns are exactly the composition of a solo stack: local janitors (Ollama) for chaining and routing, one funded specialist rung for evaluator-optimizer judgment. The n8n-plus-Ollama no-code local stack (search-verified guides, June 2026 Hermes-plus-Ollama dual local/cloud writeups) is the same ladder for non-coders. Sensing is cheap; judgment climbs; frameworks are optional plumbing on top.
4. **Instrument before you commit.** Langfuse's closing advice: OTel-trace cost, latency, and failure modes across two candidate frameworks before choosing. This estate's cost_ledger (2,316 rows still writing through 2026-09-28 per the corpus-02 compass census) is the same discipline applied to itself.
5. **Check the license field, not the word "open".** n8n and Dify are the two biggest agent platforms by stars and both read NOASSERTION in the API (fair-code and custom licenses, not OSI). AutoGen's main branch now reads CC-BY-4.0. Solo sovereignty means reading the SPDX line that ships in the same API response you already fetched for stars.

## Not verified, stated as such

- 2 of 6 searches failed with 1302 rate-limit errors; their sub-questions (smolagents release cadence detail, Claude Agent SDK star count) were not answered.
- The 69% vs 38% enterprise split rests on one secondary citation (bizflowai citing VB Pulse); treat as unconfirmed.
- I fetched repo metadata and two articles; I ran no framework code, so all capability claims are sourced to the Langfuse fetch and search summaries, not to execution.
- princeton-nlp/SWE-agent and All-Hands-AI/OpenHands 404 at their old paths; both moves verified only via GitHub search API results.

Sources: langfuse.com/blog/2025-03-19-ai-agent-comparison (fetched), anthropic.com/engineering/building-effective-agents (search-verified), vortx.ch OpenHands 1.0 piece (2026-09-14), bizflowai VB Pulse citation, pub.towardsai.net LangGraph/CrewAI/AutoGen 2026 guide, api.github.com live census (commands quoted above).
