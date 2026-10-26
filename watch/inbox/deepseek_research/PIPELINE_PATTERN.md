# THE DEEPSEEK RESEARCH PIPELINE — tweet → grounded literature briefing · 2026-09-23

## What the operator built

A prompt pipeline on DeepSeek that takes a batch of tweet URLs and returns a
**speculative research briefing** for each: related arXiv papers, GitHub repos,
scientific importance ranking, journal/venue quality assessment, and Socratic
expansion questions. Cost per batch: ~$0.10–0.50 depending on model (flash vs pro).

## The prompt pattern (self-steal this into our own pipeline)

```
You are a speculative research analyst. For each tweet below:
1. Identify the core scientific/technical claim
2. Find related arXiv papers and GitHub repositories
3. Rank scientific importance (High/Medium-High/Foundational/Low)
4. Assess journal/venue quality
5. Socratic expansion: 3 open questions the field should answer

Format: markdown table per tweet with paper references, repos, and summaries.
```

## Standing capability

Every time tweets come in → run through this prompt on deepseek-flash (cheap)
or deepseek-v4-pro (deep analysis). The output files go to watch/inbox/deepseek_research/.

## The six tweets analyzed (2026-09-22 UTC)

1. @techNmak — LLM serving: six systems techniques (prefix caching, batching, PagedAttention, etc.)
2. @omarsar0 — WFM: Wiki Foundation Model for agent memory
3. @mathemetica — Sigma-delta modulators: noise shaping
4. @HuggingApps — Qwen-Image-2.1 Turbo: 4-step distillation
5. @LensScientific — QCD color confinement: flux tubes
6. @antoniolupetti — The Great Story of Numbers: open number theory text

## Cost

deepseek-v4-pro: 5 calls, $4.98 (the operator's manual analysis run)
deepseek-flash: 14 calls, $0.46 (background lane)

The pro calls were the operator intentionally paying for depth. The flash calls
were the standing fleet lane. Total: $5.44.
