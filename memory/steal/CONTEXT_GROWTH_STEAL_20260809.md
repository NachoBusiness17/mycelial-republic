# STEAL Research — Context Growth Management in Agent Frameworks (2026-08-09)

Steal-before-build pass. Informed the `context_growth` analyzer + repack work. Sources:
`mine/raw/steal_protocol/` (11 repos). Schema: steal_report.v1

## Why
Our calibration showed per-call input is dominated by multi-turn context GROWTH
(~500 calls/goal, ~62K tok avg/call), not the initial frozen prefix. Before building our
own context-growth controls, steal the best existing mechanisms.

## Patterns found (repo / file / mechanism / trigger)

### Compaction (the crown jewel)
- **Bradliebs/ollama-agent-harness** `src/context/compaction.ts` — layered strategy chain:
  1. `applyBudgetReduction` (always): truncate tool results to 4000 chars
  2. `applyAutoCompact` at **>85%** of window: keep last 2 msgs, LLM-summarize rest
  3. `applySnip` at **>70%**: keep `max(6,half)` + `[N earlier snipped]` boundary
  - `validateCompactionSummary` scores summary (extract required terms), fallback to snip if <0.25
  - `HISTORICAL_CONTEXT_BEGIN/END_MARKER` stops model re-executing finished work

### Well-formedness after trim
- **robzilla1738/agentswarm** `src/agent.ts` `pruneOrphanedToolMessages()` — prune orphaned
  tool results/tool_calls after any compact so the API never rejects a trimmed conversation.

### Context-size estimation
- **agentswarm** `estimateMessages()` = chars/3.5 + 6/msg + tool-schema JSON length (tool schemas
  under-count by ~300-850 tok). `contextLimitFor()` = `min(limit, 0.85×window)`.
- **ollama-agent-harness** `estimateTokenCount()` = chars/4.

### Compaction summary = durable checkpoint (pointer)
- **agentswarm** `onCheckpoint` hook + `memory.ts` cross-run memory (JSON per workspace, inject
  last 8 as "PRIOR RUNS" block) — cheap persistent summary replaces full history.
- **ollama-agent-harness** `ccmem/` Concept Cells Memory (neuron-like cells, semantic recall).
- **EIT-EAST-Lab/C3** `context_key.py` `hash63`/`fingerprint` — compact stable identity for memoization.

### Token-budgeted assembly
- **hemantsingh443/blackboard-core** `state.py` `to_context_string(max_tokens, ...)` — hard budget
  per section, priority order (goal > feedback > artifacts), head/tail preview `[...N omitted...]`.
- **ollama-agent-harness** `trimContextText()`.

### Cache-aware cost (the big lever)
- **marikarx/subagent-router** `estimate_cost_usd()` — splits `cached_tokens` vs `miss_tokens`,
  prices separately (DeepSeek V4 Flash $0.14 miss / $0.0028 hit ≈ 50x). `supports_cache_tokens`.
- **microsoft/conductor** pricing `cache_read/write_per_mtok`.
- Keep a STABLE system/prefix block to maximize prompt-cache hits.

### Rolling-window / budget (bound growth)
- **agentswarm** `breaker.ts` CircuitBreaker (rate-trip >70% over window 10, fast-trip 5 consecutive)
  + `maxTokensPerRun` (12M default). `prompts.ts` phases via `set_phase` so plan survives trimming.
- **ollama-agent-harness** `iterationBudget` with refunds, rolling timeout.
- **arvarik/bmas** budget ceiling + stall detection.

### Agent-as-cleaner
- **arvarik/bmas** `traditional.py` Board Pressure Guard — deterministic trigger at **8000 tokens**
  (chars/4), cleaner agent scores entries by retention weight (salience 2.0 / confidence 1.0 /
  recency 0.1 / size-penalty 0.01), condenses low-value into a `condensed_finding`.

## Patterns to ADOPT (for our self-driving agent)
1. **Layered compaction** (harness): reduce tool results → summarize at 85% → snip at 70%, with
   summary-quality validation + fallback. (Our `agent_cli.repack_messages` is close; add the
   quality gate + boundary markers.)
2. **Orphan-tool pruning** (agentswarm) after every compact — prevent API-rejected conversations.
3. **Tool-schema-aware + headroom** token estimate (`0.85×window`).
4. **Compaction = checkpoint** — persist each repack summary + inject as compact prior block on
   resume (our session_maze/HANDOFF.md is the natural seam).
5. **Token-budgeted assembly** with priority + head/tail preview (our context_pack).
6. **Cache-aware cost + stable prefix** (already our core doctrine — keep metering cached vs miss).
7. **Rolling-window breaker + run budget** (agentswarm) — bound token burn on doomed long loops.
8. **Agent-as-cleaner** (bmas) — deterministic trigger + retention-weighted eviction.

## Guardrails (steal law)
- Contracts only, never default seat, T2 research max. Cite file paths; no wholesale copy of code —
  adapt the mechanism to our deterministic/architecture-native shape.
