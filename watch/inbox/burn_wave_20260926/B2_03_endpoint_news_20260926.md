# B2-03 endpoint news pass 2 (2026-09-26)

## Verdict

STEAL with two ALERTs. Free-lane landscape: OpenRouter stable (the big capacity lane holds), z.ai free Flash models hold, Groq denominators corrected and confirmed, but the Groq fleet config is broken (2 of 3 configured model ids dead) and Cerebras is no longer a free lane at all (card-gated 30-day trial). NVIDIA post-purge re-probe landed: key alive, catalog exactly 82 models. Fresh cross-provider pattern: three providers (Google, Mistral, NVIDIA) now withhold published per-model denominators behind login-gated dashboards, so lane math gets harder to verify every pass. B2-04 marked done with no receipt on disk: process debt.

## Evidence with source quotes

- Groq docs (fetched 2026-09-26): rows verbatim "openai/gpt-oss-120b | 30 | 1K | 8K | 200K", identical for gpt-oss-20b and qwen/qwen3.8-27b; "Cached tokens do not count towards your rate limits"; "apply at the organization level". 14.4K RPD appears only on llama-prompt-guard classifiers. The stale 14.4K free-tier denominator from the 09-18 scout row is confirmed dead for all text models.
- Groq live probe: GET /openai/v1/models HTTP 200, 11 models; qwen/qwen3.6-27b and groq/compound-mini absent. providers.yaml groq lane references both dead ids.
- Cerebras docs verbatim: "If you skip adding a payment method at sign-up, Playground and API access remain inactive until you do."; "New accounts receive $5 in free credits after adding a verified payment method. These credits expire 30 days after they're granted". Table: gpt-oss-120b and qwen-3.8-27b, 5 RPM / 30K uncached TPM / 90K total TPM / 1M TPD, no RPD. Live probe: HTTP 200, exactly those 2 models.
- NVIDIA: no numeric denominator published (docs.api.nvidia.com landing has none; /nim/reference/rate-limits 404; /faq 404). Live probe: /v1/models HTTP 200, 82 models; deepseek-ai/deepseek-v4.1-flash present, config id deepseek-v4-flash-0731 gone; z-ai/glm-5.3-flash, openai/gpt-oss-20b, nemotron-3 family present. Note: purge removed 82 on 09-20; catalog now holds 82; different sets, not a restore.
- Gemini: docs rate-limits page no longer carries the static free-tier table; it points to the logged-in AI Studio view. Pricing page: 2.5 Pro / Flash / Flash-Lite and Gemma 4 "Free of charge"; no per-model RPD; grounding 500 RPD shared (Flash/Lite), 1500 RPD (Pro). Config ids gemini-2.0-flash / 1.5-flash absent from the pricing page.
- OpenRouter docs: 20 RPM on :free; "Fewer than 10 credits purchased: 50 requests/day; At least 10 credits purchased: 1000 requests/day", granted from 9 credits. Unchanged; 18-lane math holds.
- Mistral: docs pricing page 308-redirects to mistral.ai/pricing; consumer plans bundle "$10 /mo in API credits" (Free) and "$30 /mo" (Pro). Old 1 RPS / 500K TPM figures unverifiable from any official page; not asserted (no-synthesis law).
- z.ai docs pricing: GLM-4.7-Flash / 4.5-Flash / 4.6V-Flash all $0; GLM-5.3-Flash new at $0.15/$0.50 per MTok; rate-limit URLs 404.

## Work done

7 providers fetched from official pages; 3 read-only live probes (Groq, Cerebras, NVIDIA model lists, lane keys, no synthetic content sent beyond GET). 9 rows appended to watch/inbox/LINKS.jsonl (writer endpoint-news, 3 ALERT rows) via .venv python json.dumps. Ledger row appended. Queue self-fed.

## Falsifier

This receipt fails if: (a) any LINKS row cites a denominator not present on the cited URL at fetch time (spot-check the five quoted strings); (b) the Groq or Cerebras live probes cannot be reproduced with the lane keys (rerun GET /models, expect 11 and 2 models); (c) an em-dash exists in the appended rows or this receipt.

## Bibliography closed

console.groq.com/docs/rate-limits; inference-docs.cerebras.ai/support/rate-limits; docs.api.nvidia.com (+ two 404s); ai.google.dev/gemini-api/docs/rate-limits and /pricing; openrouter.ai/docs/api-reference/limits; mistral.ai/pricing (via docs.mistral.ai 308); docs.z.ai/guides/overview/pricing. All fetched 2026-09-26. Live probes: api.groq.com, api.cerebras.ai, integrate.api.nvidia.com, 2026-09-26T11:30Z window. Prior receipt: BURN_free-resource-landscape_20260925.md. B2-04 PROVIDER_HEALTH_20260926.md: searched, does not exist, filed owed.
