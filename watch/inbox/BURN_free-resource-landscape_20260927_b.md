# BURN free-resource-landscape 20260927 b

## Verdict

steal

## Evidence

Ledger rows read this session (watch/inbox/LINKS.jsonl, last 50 rows; quotes are ledger text, which itself quotes the named pages):

- EPNEWS-GROQ-RPD-CONFIRMED 2026-09-26 (quoting console.groq.com/docs/rate-limits): "openai/gpt-oss-120b | 30 | 1K | 8K | 200K"; "Cached tokens do not count towards your rate limits". Free plan denominator: 1K requests/day, 200K tokens/day per text model.
- EPNEWS-OPENROUTER-STABLE: "50 requests/day below 10 all-time credits, 1000 requests/day from 9+ credits"; "the 18-lane x 1000/day lane math on funded accounts still holds".
- B2-142-TRIAL-SHAPES-LIVE (quoting inference-docs.cerebras.ai): "Free Trial per model 5 RPM / 30K uncached TPM / 90K total TPM / 1M TPH / 1M TPD"; credits "expire 30 days after they are granted"; "no permanent free tier".
- LINKS seq 1790452819074583 (B2-144, DeepSeek pricing page): "off-peak halves everything (peak 01:00-04:00 + 06:00-10:00 UTC Mon-Fri)".

Fresh search this session (one WebSearch pass, 2026-09-27): first query returned "MCP error -429 ... 1302 Rate limit reached"; retry returned thin aggregator snippets only, primary pages not opened. Snippet-grade, unverified: moclaw.ai claims MiniMax "ended its free M3 API access; it was a 14-day sponsored free tier that expired"; bodegaone.ai claims Tabnine "replaced its free tier with a time-limited developer preview program". Filed as owed, not asserted.

## Steal or Vacuous

Steal, all from verified ledger bytes. (1) Windows to hammer: DeepSeek off-peak (half price on everything); OpenRouter funded lanes at 1000 requests/day each, 18-lane math holds; Groq 1K RPD per model, cached tokens ride free of the denominator. (2) Churn runs one direction this month: Cerebras free tier became a card-gated 30-day trial (one-shot 30-day batch sprint, never a routing-list add), MiniMax's 14-day sponsored window reportedly closed, Tabnine reportedly converted to a preview. Sponsored freelanes are expire-dated windows, not tiers; stamp every new one with a death date on arrival. (3) Key gaps owed: six unprobed lane names from the free-claude-code drop (Featherless, Chutes, SiliconFlow, LLM7, Scaleway, Lightning AI); NVIDIA and Gemini denominators now login-gated; B2-04 per-lane 3-call measurement unfiled; providers.yaml Groq surgery owed (qwen3.6 to qwen3.8, drop compound-mini). Filing law for any promotion of the snippet-grade items into LINKS rows: python -m mag.link_library add only; hand-appends caused 5 silent dupes (B2-06 receipt).

## Bibliography

Read this session: watch/inbox/LINKS.jsonl (tail, last 50 rows); watch/inbox/burn_wave_20260926/B2_06_link_dupes_20260926.md; memory/facts/behavioral.jsonl (tail, percolator invariant noise, no topic signal). WebSearch result text for "free LLM API tier changes September 2026 free inference credits new model preview" (2026-09-27); linked pages (moclaw.ai, bodegaone.ai, coworker.ai) not opened. Pages quoted secondhand through ledger rows (console.groq.com, inference-docs.cerebras.ai, ai.google.dev, DeepSeek pricing) not re-read this session.
