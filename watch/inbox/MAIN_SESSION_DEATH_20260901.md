# MAIN_SESSION_DEATH_20260901 — why `agent:main:main` looked 187% and died at 05:59Z
> **[AUDIT-TYPED 2026-09-08]** status: PROSE · claims: the "187%" was a cumulative-spend accounting artifact; the session actually died to a z.ai request timeout at 14% live context — SUPPORTED (byte-backed from session JSONL + store per card, probes consistent with provider congestion) · falsifier: last-turn usage showing live context near the 1M window, or a compaction guard having tripped before death

**Class:** DIAGNOSIS (agent-generated, byte-backed from session JSONL + store)
**Session:** `agent:main:main` → `64543440-8a1e-4432-86e4-3e57a26d74d0` (night shift, 04:06→06:04Z, 100 metered turns, glm-5.3-flash)
**Operator complaint:** "why didn't you stop yourself from getting to 100%?"

## Findings (bytes, not vibes)

1. **Context never overflowed.** Peak single-turn context = `input+cacheRead+cacheWrite` ≈ **145.8K of 1,049K (14%)**. Last metered turn before death: 566 in / 145,280 cacheRead / 867 out.
2. **The scary number is an accounting artifact.** Store `totalTokens: 1,956,219` ≈ cumulative sum of *per-turn input tokens* across 100 turns (cache-heavy loop work repeats input billing every turn). `openclaw sessions list` divides that cumulative counter by the per-request window → "1956k/1049k (187%)". That figure counts the whole night's spend-shaped work, not live context. Warnings/compaction watch live context; the artifact was never the thing they watch.
3. **Zero compactions fired because none were needed:** `compactionCount: 0`; auto-compaction guards (reserveTokens 24576, midTurnPrecheck, 4MB transcript byte-guard vs actual 1.6MB transcript) never tripped at 14%.
4. **Actual cause of death (05:59:21.142Z, custom `openclaw:prompt-error`):** `"request timed out"` on zai/glm-5.3-flash. OpenClaw aborted the run (in-flight exec SIGTERM'd at the same ms — the 06:00Z DeepSeek-wait loop), marked `abortedLastRun: true`. Operator's 06:04Z message landed in an aborted session → silence.
5. **Z.ai was congested that window — session's own probes prove it:** 05:52Z "Lite spawn died to provider congestion (strike 1)", 05:56Z probe waves `401/401` fail, prior turn measured the 1305 fence re-arming even at par=1. The timeout is consistent with the same congestion the session itself was measuring.

## Why no warning fired (direct answer)

Warnings were never bypassed. VS-Code-style % is a per-request gauge; OpenClaw's guards watch live context (14%) and never saw danger. The 100%+ number the operator saw is the sessions-list cumulative-counter artifact (finding 2). Two real gaps:
- **GAP-A (display):** sessions list shows cumulative tokens as % of window → misleading "187%". No live-context gauge surfaced in the UI before a failure.
- **GAP-B (resilience):** single `request timed out` on a congested free lane aborts the run with no visible recovery/retry surface in the chat; session reads "dead" to the operator.

## Action taken

- 06:37Z: manual compaction of `agent:main:main` via `openclaw sessions compact` (operator-requested). Receipt: compaction result appended by runner if it completes.
- Full history preserved on disk (compaction is a view change, not deletion): `/root/.openclaw/agents/main/sessions/64543440-*.jsonl`.

## Law candidates (for operator, not auto-applied)

1. **Night-shift sessions should not die silently on a single provider timeout** — model_failover exists; free-lane congestion windows (z.ai evening) are known; consider pinning long unattended runs to DeepSeek or enabling compaction.model fallback.
2. **Never read the sessions-list % as context pressure** — it is cumulative spend-shaped counter ÷ window. Live gauge = `/status` contextTokens or last-turn `usage.input+cacheRead`.
