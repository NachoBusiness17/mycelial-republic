# BURN receipt: free-resource-landscape (2026-09-26, pass e)

## Verdict
steal

## Evidence
1. https://inference-docs.cerebras.ai/support/rate-limits (fetched 2026-09-26; this route renders, unlike /pricing): "New accounts receive $5 in free credits after adding a verified payment method. These credits expire 30 days after they're granted." Also: "If you skip adding a payment method at sign-up, Playground and API access remain inactive until you do." Also: "API and Playground access stop on the Free Trial tier until you purchase credits." Free Trial limits per model (table lists gpt-oss-120b and qwen-3.8-27b): 5 RPM, 30K uncached TPM, 90K total TPM, 1M TPH, 1M TPD. Developer tier: gpt-oss-120b at 1K RPM, no daily caps.
2. https://www.cerebras.ai/inference (fetched 2026-09-26; route never tried in passes a-d): "Get started with $5 in free credit after creating an account." Developer plan: "get 10x higher rate limits than Free". No card mention anywhere on the page.
3. Wayback capture of www.cerebras.ai/pricing dated 2026-09-24: headings only, no table. The /pricing SPA is empty even in archive; the docs route was the way in.
4. Forum hunt: search "cerebras forum credits rate limits inference" surfaced no Cerebras forum thread (only HN Kimi K3 chatter, GitHub free-LLM lists, Product Hunt AMD/Cerebras). Nothing to fetch; owed.
5. Fresh search "Cerebras free tier September 2026 status": search backend 429 (code 1302) on every attempt, zero results. Owed, not synthesized.

## Steal or Vacuous
Steal. The Cerebras slot CLOSES as corrected at primary:
1. Card gate CONFIRMED by docs: a verified payment method is required and access stays inactive without it. ALERT-CEREBRAS-CARD stands. The aggregator "no card" echo is explained: it traces to the vendor's own marketing page ("after creating an account", gate omitted). Never flip on marketing copy.
2. The credits-to-rate-limits expectation (~40 RPM) is dead: the free lane is a $5, 30-day trial-credit tier capped at 5 RPM and 1M TPD per listed model, then paid only. Retire the 40 RPM figure; it never had more than a snippet.
3. Operator decision input: a Cerebras key costs a card and buys a 30-day, 5 RPM trial, not a durable free lane. Trial-class, far below the Groq lane (1K req/day). Keep the key gap filed but downgraded: not worth a card unless Developer-tier terms or a promo change.
4. Roster note: the limits table names only gpt-oss-120b and qwen-3.8-27b, consistent with SCOUT-CEREBRAS-SWAP (gemma leaving the lineup).

## Falsifier
none proposed

## Bibliography
- watch/inbox/LINKS.jsonl (SCOUT rows 2026-09-20 through 2026-09-22, grep SCOUT-)
- memory/facts/behavioral.jsonl (skimmed tail; harness invariants, no vendor facts)
- watch/inbox/BURN_free-resource-landscape_20260925.md, _b.md, _c.md, _d.md (prior passes, read)
- https://inference-docs.cerebras.ai/support/rate-limits (fetched 2026-09-26)
- https://www.cerebras.ai/inference (fetched 2026-09-26)
- https://web.archive.org/web/2026/https://www.cerebras.ai/pricing (snapshot 2026-09-24, fetched 2026-09-26)
- Two web searches 2026-09-26: forum-thread query (no thread found, owed); status query (backend 429, owed)
