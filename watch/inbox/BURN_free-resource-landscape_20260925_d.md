# BURN receipt: free-resource-landscape (2026-09-26, pass d)

## Verdict
steal

## Evidence
1. build.nvidia.com/explore (fetched 2026-09-26): featured block reads "The leading open models built by the community, optimized and accelerated by NVIDIA's enterprise-ready inference runtime" over exactly four cards: kimi-k3, deepseek-v4-pro-0813, nemotron-3.5-lightning-30b-a3b, nemotron-3-ultra-550b-a55b. No Llama in featured. No counts, credits, or limits text anywhere. Primary confirmation of pass-b's snippet-level signal.
2. https://integrate.api.nvidia.com/v1/models fetched with NO API key: returns a JSON list of 82 model IDs. Contains moonshotai/kimi-k2.6 and moonshotai/kimi-k3, deepseek-ai/deepseek-v4.1-flash, nvidia/nemotron-3-super-120b-a12b, nvidia/nemotron-3-ultra-550b-a55b, nvidia/nemotron-3.5-lightning-30b-a3b, z-ai/glm-5.3, z-ai/glm-5.3-flash, openai/gpt-oss-20b, google/gemma-4-31b-it. Llama survives only as legacy meta rows (llama2-70b, codellama-70b, the llama-3.2 vision pair, llama-guard-4) and nvidia/llama-3.1-nemotron branded lines. Caveats: the list also carries 2024-era IDs (01-ai/yi-large, databricks/dbrx-instruct, nvidia/neva-22b, microsoft/kosmos-2), so it is a catalog listing, not proof of served inference; featured deepseek-v4-pro-0813 is absent from the list while deepseek-v4.1-flash is present, so featured and callable sets are not identical.
3. Cerebras re-probe, three official surfaces: www.cerebras.ai/pricing renders only the headings "Cerebras Inference tier pricing" and "Developer Tier Pricing", no table, no card language; inference-docs.cerebras.ai/support/pricing still 307s to that same page; cloud.cerebras.ai returns a title-only shell. All dead for card-gate evidence.
4. Fresh search: signal that NVIDIA moved from the 1,000-credit free tier to unpublished per-model rate limits; a Jun 17 2026 NVIDIA developer-forum post titled "Request for NVIDIA Build API Rate Limit Increase (40 RPM)" implies a roughly 40 RPM default. The one fetch (decodethefuture.org) returned an unrelated Polish finance blog: phantom search citation, filed owed, not synthesized. Forum thread itself not fetched (bare-domain link), so snippet-level only.

## Steal or Vacuous
Steal, three adoptions:
1. The pass-b roster gap closes at primary: featured 4 confirmed, the no-Llama claim is now scoped to featured only (legacy meta rows persist in the callable list), and the full callable roster is enumerated at 82 via the unauthenticated /v1/models endpoint. Adopt that endpoint as a no-key roster probe tool for lane audits. When the NVIDIA key gap (baseline still 0) closes, first candidates: z-ai/glm-5.3-flash, openai/gpt-oss-20b, nemotron-3-super-120b-a12b.
2. Pre-register the expectation that NVIDIA's free lane is rate-limit governed (about 40 RPM class, unpublished per model), not credit governed; the old 1,000-credit denominator in fleet notes is likely stale. Held as expectation until the forum thread is fetched, not doctrine.
3. Cerebras card gate: unchanged and now triple-confirmed empty at official surfaces. Only the live sign-up flow settles card-required vs no-card; the aggregator contradiction stays a watch-item and the operator decision stays unmade.

## Falsifier
none proposed

## Bibliography
- watch/inbox/LINKS.jsonl (SCOUT rows, 2026-09-20 through 2026-09-22)
- memory/facts/behavioral.jsonl (skimmed, 404 rows, no vendor facts)
- watch/inbox/BURN_free-resource-landscape_20260925.md, _b.md, _c.md (prior passes, read in full)
- https://build.nvidia.com/explore (fetched 2026-09-26)
- https://integrate.api.nvidia.com/v1/models (fetched 2026-09-26, unauthenticated)
- https://www.cerebras.ai/pricing (fetched 2026-09-26, headings only)
- https://inference-docs.cerebras.ai/support/pricing (307 redirect, owed)
- https://cloud.cerebras.ai (title-only shell, owed)
- Web search summary citing forums.developer.nvidia.com "Request for NVIDIA Build API Rate Limit Increase (40 RPM)" (Jun 17 2026, snippet only, thread fetch owed)
- https://decodethefuture.org (fetched 2026-09-26, unrelated Polish finance blog, phantom citation, owed)
