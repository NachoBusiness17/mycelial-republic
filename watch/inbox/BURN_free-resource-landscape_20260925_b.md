# BURN receipt: free-resource-landscape (2026-09-25, pass b)

## Verdict
steal

## Evidence
1. Groq rate-limits docs refetched 2026-09-25: "Cached tokens do not count towards your rate limits." The clause is officially documented; pass-a's open probe closes. New wrinkle: the live page now renders a "Free Plan Limits" / "Developer Plan Limits" toggle and the visible table is labeled Developer plan base limits, yet the gpt-oss-120b row reads 30 / 1K / 8K / 200K, the exact numbers pass-a attributed to the free plan.
2. NVIDIA build.nvidia.com/explore fetched 2026-09-25: catalog renders post-purge with 4 featured models: kimi-k3, deepseek-v4-pro-0813, nemotron-3.5-lightning-30b-a3b, nemotron-3-ultra-550b-a55b. No Llama in featured. Page text mentions no credits, tiers, or limits; total roster count not exposed by the render.
3. Cerebras inference-docs.cerebras.ai/support/pricing returns 307 redirect to www.cerebras.ai/pricing, which renders only headings ("Developer Tier Pricing", "Cerebras Inference tier pricing") with no table, no card language. Owed, not synthesized.
4. Fresh web search returned aggregator echo (freeairouter.com, openthorn.app, aitools.flocci.in, rfp.wiki, a "Nebi Chat" page dated Sep 14) asserting Cerebras and NVIDIA NIM are both "free tier friendly, no credit card required" and NIM holds "80+ models". This contradicts the ledger's ALERT-CEREBRAS-CARD (klymentiev.com Sep 11: card required) and has no primary backing.

## Steal or Vacuous
Steal, three adoptions:
1. Close the Groq caching probe: prompt-cache rate-limit bypass is official and quotable. The frozen-prefix deliberate-ask signature is a sanctioned way to stretch the 8K TPM floor. Register as lane doctrine in chat_provider notes, not folk wisdom.
2. NVIDIA post-purge re-probe advances to first data: catalog is live, Kimi plus DeepSeek plus Nemotron families present, Llama absent from featured, and nemotron-3.5-lightning matches the OpenRouter free-roster name (SCOUT-FREE-ROSTER). Full roster count and free-credit terms stay owed; the SPA hides them from a plain fetch.
3. Cerebras card gate: do NOT flip the ledger on aggregator echo. Aggregators now say "no card", the Sep 11 roundup said "card required", and official pages render nothing. The only trustworthy probe is the sign-up flow itself; the operator decision stands unresolved. File the contradiction as a watch-item.

## Falsifier
none proposed

## Bibliography
- watch/inbox/LINKS.jsonl scout rows 257 to 305 (2026-09-17 through 2026-09-22)
- watch/inbox/BURN_free-resource-landscape_20260925.md (prior pass, read in full)
- memory/facts/behavioral.jsonl (skimmed, 404 rows, no endpoint or key facts)
- https://console.groq.com/docs/rate-limits (fetched 2026-09-25)
- https://build.nvidia.com/explore (fetched 2026-09-25)
- https://inference-docs.cerebras.ai/support/pricing (307 redirect, owed)
- https://www.cerebras.ai/pricing (rendered empty of pricing, owed)
- Web search summary citing freeairouter.com, openthorn.app, aitools.flocci.in, rfp.wiki (aggregator echo, not fetched, untrusted)
