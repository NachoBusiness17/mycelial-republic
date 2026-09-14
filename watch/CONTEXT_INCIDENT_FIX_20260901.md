# CONTEXT INCIDENT 20260901 — 100% silent compaction (fix state)

> **[AUDIT-TYPED 2026-09-08]** status: PROSE · claims: silent 100% compaction was caused by unpruned tool-result echoes (450KB = 57% of bytes), fixed via compaction notifier hook + ctx_watch watchdog + NO SILENT 100% LAW — SUPPORTED (audit receipt /board/CONTEXT_HOG_AUDIT_20260901.md cited in card) · falsifier: none stated in card (ctx_watch WARN/CRIT tripwires are the standing guard)

## Verdict (audit: /board/CONTEXT_HOG_AUDIT_20260901.md)
- Dead session (64543440, compaction boundary): **tool-result class = 450KB = 57%** of all bytes. Assistant-text 286KB. Completion events only 11KB (children were NOT the problem).
- Single worst message: #114 gateway config echo, 19KB. Pattern: config.schema.lookup / workboard / cron full-JSON echoes + exec stderr dumps (incl. the .env sourcing fiasco).
- Systemic gaps: (1) compaction is **silent by default** (`notifyUser` off) — the warning we "bypassed" was never on; (2) **tool-result pruning ships off for non-Anthropic providers** — ours was off all night; (3) byte-guard (`maxActiveTranscriptBytes`) unset.

## Fixed by seat (in-scope)
- `truncateAfterCompaction: true` patched (gateway returned noop → already on; rotation did happen at the 05:4xZ compaction — we are in the successor session now).
- **compaction-notifier bundled hook ENABLED** (openclaw hooks enable — file-level, no protected config): visible 🧹 notices on compaction start/finish. Live after 06:55Z restart. THE missing warning, found in the docs and turned on.
- **ctx_watch.mjs watchdog** (WARN@10MB / CRIT@16MB active transcript) wired into every night_shift_ticker tick; CRIT wakes main session with inline-payloads-banned order. Ticker also carries ctx byte in its tick line. First reading: 0.22MB OK.
- **Ticker death-switch bug fixed**: deleteAfterRun was true — night watch would have self-deleted on its first successful tick.
- Seat law (MEMORY.md NO SILENT 100% LAW): bulk reads → spawn lanes; never re-print tool JSON; children answer one line; heavy payloads → /board pointers.
- Audit + this receipt on /board. DS cache probe COMPLETE: 12/12 calls 4864/4864 cached, ~490ms median — sub-second warm fleet memory.

## Needs operator paste (agent-protected config paths)
Merge into `~/.openclaw/openclaw.json` → `agents.defaults` (preserve/merge, do NOT replace the file):
```json
{
  "compaction": { "notifyUser": true, "maxActiveTranscriptBytes": "20mb" },
  "contextPruning": { "mode": "cache-ttl", "ttl": "5m" }
}
```
Effect: compaction notices in chat ("🧹 Compacting..."), old tool results pruned per-request after 5m cache TTL, transcript hard-capped at 20mb.

## Gen C battery status (unchanged by incident)
- deepseek 20/20 · nvidia 20/20 · together 20/20 (paid $0.0045 gated) · cerebras fetch-dead (2-strike bailed) · openrouter free-slug 404 · groq + zai-lite provider-congested → ticker retries.
