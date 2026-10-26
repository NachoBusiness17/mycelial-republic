# B2-340 receipt (2026-09-26)

## Verdict

LANDED. Four verified LINKS rows registered (watch/inbox/LINKS.jsonl, writer zcode-sw-10-b2-340), one per provider, every number quoted from pages fetched 2026-09-26. Unreachable items are named per provider, not guessed. The matrix below replaces the self-doubting model text UF-127 carried.

## Evidence file:line quotes

All quotes are from fetches executed in this lane on 2026-09-26 (the two 301 redirects are named, the fetched targets are what the quotes come from).

- ANTHROPIC (docs.anthropic.com 301 to platform.claude.com/docs/en/docs/build-with-claude/prompt-caching): "5-minute cache write tokens are 1.25 times the base input tokens price"; "1-hour cache write tokens are 2 times the base input tokens price"; "Cache read tokens are 0.1 times the base input tokens price"; "By default, the cache has a 5-minute lifetime"; "The cache is refreshed for no additional cost each time the cached content is used"; invalidation hierarchy tools, system, messages, "Changes at each level invalidate that level and all subsequent levels"; hits require "100% identical prompt segments"; minimum cacheable prefix 512/1024/2048/4096 by model tier; Sonnet 5 example: base $2, 5m write $2.50, 1h write $4, hits $0.20 per MTok.
- OPENAI (platform.openai.com 301 to developers.openai.com/api/docs/guides/prompt-caching): cached input "discounted up to 90%"; "for GPT-5.6+, cache reads cost 0.1x and writes 1.25x the standard uncached input rate"; "Prompt caching is enabled by default"; GPT-5.6+ ttl "30m", "eligible for reuse for 30 minutes after its most recent write or reuse"; earlier models in_memory tier "typically 5-10 minutes" of inactivity (up to one hour), 24h tier "typically 30 minutes" (up to 24 hours), default 24h outside ZDR; any prefix change means "the prefix after that change cannot match the existing cache entry"; "The minimum cacheable prompt length is 1,024 tokens for GPT-5.6 and later". UNREACHABLE: per-model cached rates for gpt-4o/4.1/5, the page says "Model-dependent" and points to API pricing.
- GOOGLE (ai.google.dev/gemini-api/docs/caching + /pricing): "Implicit caching is enabled by default for all Gemini 2.5 and newer models"; "We automatically pass on cost savings if your request hits caches"; min cache 2,048 tokens for 2.5 Pro/Flash, 4,096 for the 3.x tier; pricing (page fetched with a hi-IN renderer locale, numerals exact): 2.5 Pro input $1.25 (<=200K prompt), cached $0.125, storage $4.50 per 1M tokens per hour; 2.5 Flash input $0.30, cached $0.03, storage $1.00 per 1M/hr; Gemini 3 Flash input $0.75 until 31 Dec 2026 then $1.50, cached $0.075 then $0.15, storage $0.50 then $1.00 per 1M/hr; 3.1 Pro Preview cached $0.20 / $0.40, storage $4.50 per 1M/hr. UNREACHABLE: TTL / default lifetime / refresh_on_use and invalidation rules are not stated on either fetched page; the historical 1-hour default is NOT quoted because these bytes do not carry it.
- ZAI (docs.z.ai/guides/overview/pricing): per 1M tokens USD, GLM-4.6 input 0.6 / cached 0.11; GLM-4.5 0.6 / 0.11; GLM-4.5-Air 0.2 / 0.03; GLM-4.5-X 2.2 / 0.45; GLM-4.5-AirX 1.1 / 0.22; GLM-4.6V 0.3 / 0.05; GLM-4.5V 0.6 / 0.11; cache storage column reads "Limited-time Free" on every row; Flash tier listed Free. Cached input sits at roughly 18 pct of input in the 0.6 class. UNREACHABLE: no TTL or storage-free window stated on the page.

## Work done

1. Fetched all four provider caching surfaces live (two via named 301 redirects), same day.
2. Appended one verified LINKS.jsonl row per provider with the quotes above in the note field (file grew 337 to 341 lines during the lane; concurrent writers active, appends only).
3. Filed this matrix as the payoff the gap row owed, replacing UF-127's self-doubting text with byte-quoted numbers.

## Falsifier

The brief's falsifier: a provider row whose numbers cannot be quoted from fetched bytes. Guard: every number above carries its fetch date and page; re-fetch any of the four URLs and a mismatched number kills this row set. Named soft spots: Google TTL and zai TTL are marked unreachable rather than filled, so any matrix that later states them has to land new bytes; OpenAI per-model prices are "Model-dependent" on the fetched guide, so the matrix deliberately does not give them.

## Bibliography closed

- https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching (fetched 2026-09-26)
- https://developers.openai.com/api/docs/guides/prompt-caching (fetched 2026-09-26)
- https://ai.google.dev/gemini-api/docs/caching and https://ai.google.dev/gemini-api/docs/pricing (fetched 2026-09-26)
- https://docs.z.ai/guides/overview/pricing (fetched 2026-09-26)
- watch/inbox/LINKS.jsonl (4 rows appended, writer zcode-sw-10-b2-340)
- watch/inbox/burn_wave_20260926/B2_78_denominator_refresh_20260926.md (refreshed gap row 4)
