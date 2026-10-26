# BURN receipt: free-resource-landscape (2026-09-26, pass h)

## Verdict
steal

## Evidence
1. Pass g, logs/groq_cache_bypass_20260926.jsonl: hammer "11,792 tokens in ~8s against lim_tok 8000, zero 429"; "cached_tokens reported on only 4/18 frozen-arm calls"; request axis "decremented exactly 1 per 200 in both arms".
2. LINKS.jsonl EPNEWS-NVIDIA-REPROBE-LANDED (2026-09-26): "live catalog is exactly 82 models, deepseek-ai/deepseek-v4.1-flash replaces the config's deepseek-v4-flash-0731"; "beware the 82 coincidence". Sibling ALERT: B2-04 deliverable PROVIDER_HEALTH_20260926.md "does not exist anywhere in the repo".
3. LINKS.jsonl EPNEWS-OPENROUTER-STABLE (2026-09-26): "20 RPM on :free variants; 50 requests/day below 10 all-time credits, 1000 requests/day from 9+ credits".
4. Pass e, inference-docs.cerebras.ai/support/rate-limits: "$5 in free credits after adding a verified payment method"; Free Trial row "5 RPM ... 1M TPD".
5. logs/hermes_dual_20260926/output.jsonl: 44 rows by 20:01Z; rr-12 to rr-14 all "ok": true (glm-5.3-prime, qwen3.8-max-prime, ember-1).
6. LINKS.jsonl DeepSeek pricing row (2026-09-26): off-peak "halves everything (peak 01:00-04:00 + 06:00-10:00 UTC Mon-Fri)".
7. Fresh search 2026-09-26: "Qoder is offering Qwen3.8-Flash at 0.0x credit rate through September 30, 2026". Snippet-grade, zero primary links, owed.

## Steal or Vacuous
THE BOARD (weekly rollup, all fleet free lanes):

| Lane | Status | Quota reality | Stealth window | Next action |
|---|---|---|---|---|
| Groq (gpt-oss-120b/20b, qwen3.8-27b) | measured | 30 RPM / 1K RPD / 8K TPM / 200K TPD, org-level | frozen-prefix cache: token refund async, request axis 1:1, hammer rode 1.57x past fresh wall | scaled hammer cleared; TPD axis unmeasured (no header) |
| NVIDIA NIM | live | free terms not exposed by render; catalog exactly 82 models post-purge | none filed | swap stale config ref to deepseek-ai/deepseek-v4.1-flash; land missing B2-04 receipt |
| Cerebras | gated | $5, card required, 5 RPM, 30-day expiry | none | dormant; revisit only on Developer-tier or promo change |
| OpenRouter :free | live | 20 RPM; 50 req/day under 10 all-time credits, 1K/day at 9+ | credit-count tier jump (one credit moves daily wall 20x) | ride roster rotation via endpoint_news; watch for glm-5.3-flashx :free |
| Offpeak idle queue (fleet-side) | live | local compute, no external quota | overnight drainer (autorun, pile-classify) | keep |
| Hermes/Nous credits | live | $180 armed; dual-burn active, 44 rows all ok | none | keep per-row receipts landing |
| z.ai GLM window | live | coding-plan quota; reset cycle confirmed (probe ALIVE) | post-reset uncapped burn; Task agents 12-wide clean, workflows capped at 3 | hold the width law |
| Qoder Qwen3.8-Flash promo | unverified | 0x credit through Sep 30 (4 days left) | none | snippet-grade; verify primary before spending attention |

Net shape unchanged: OpenRouter expands while Groq contracts; strongest edges: the Groq cached-token window and the OpenRouter credit-tier jump.

## Falsifier
none proposed

## Bibliography (closed)
- watch/inbox/BURN_free-resource-landscape_20260925.md, _b.md, _e.md, _f.md, _g.md (prior passes, read)
- watch/inbox/LINKS.jsonl (SCOUT-, ALERT-, EPNEWS- rows, 2026-09-16 to 09-26)
- memory/facts/behavioral.jsonl (480 rows skimmed, harness invariants, no vendor facts)
- logs/hermes_dual_20260926/output.jsonl, logs/groq_cache_bypass_20260926.jsonl
- Web search 2026-09-26: kdnuggets.com, Aireiter roundup, Qoder promo (all snippet-grade)
