# MODEL GARDEN CENSUS - lane 1 (CENSUS) of the 20-wide model-garden dig

- Moment: probes 2026-10-01T21:58:56Z through 22:01:37Z; UA-fixed pass window 22:02-22:10Z; receipt written same session
- Instrument: urllib probe v1 (ephemeral, OS temp dir; every row below is the transcribed byte outcome), 1 attempt per call, 20s timeouts, temperature 0, max_tokens 1. Key VALUES never read into any output; only env NAMES appear here.
- Operator steer (mid-run, honored): "all the models are in hermes" - the Nous inference API is the PRIMARY garden; the multi-base probes became the SECONDARY section.
- Spend: ~60 one-token calls, nearly all on Nous credits / free lanes / $0-billed failures. Worst case ~60 output + ~600 input tokens. Estimated under $0.01, cap $0.05 respected.

## PRIMARY: the Nous garden (base https://inference-api.nousresearch.com/v1, key env HERMES_API_KEY_2, failover HERMES_API_KEY_1)

Catalog instrument: GET /v1/models = HTTP 200 in 455ms. Run 1 read 427 ids at 21:58:57Z; the archived grouping fetch read 424 ids moments later (same-hour catalog drift of 3 ids; the archived 424-id JSON is the grouping basis). 52 distinct vendor families.

Probe law: ONE 1-token chat call per DISTINCT family (not per SKU). "reasoning burned" = HTTP 200 with finish=length, content_len=0 (the 1-token cap was consumed by reasoning; the model is reachable and answering - size max_tokens up for real content, per the providers.yaml nous note).

| family | SKUs | probed model | status | ms | verdict |
|---|---|---|---|---|---|
| openai | 107 | openai/o3-mini | 200 | 1590 | LIVE (reasoning burned) |
| qwen | 53 | qwen/qwen3.8-max-prime | 200 | 2491 | LIVE (reasoning burned, run 1) |
| google | 34 | google/gemini-2.5-pro | 200 | 1201 | LIVE (reasoning burned) |
| anthropic | 29 | anthropic/claude-haiku-4.5 | 200 | 950 | LIVE (content "#" back, run 1) |
| mistralai | 26 | mistralai/ministral-3b-2512 | 200 | 972 | LIVE (content back) |
| z-ai | 20 | z-ai/glm-5.3-prime | 200 | 922 | LIVE (reasoning burned, run 1) |
| deepseek | 17 | deepseek/deepseek-v4-flash | 200 | 1842 | LIVE (reasoning burned) |
| moonshotai | 9 | moonshotai/kimi-k2 | 200 | 791 | LIVE (content 5 chars back) |
| x-ai | 7 | x-ai/grok-4.3 | 200 | 4364 | LIVE (reasoning burned) |
| bytedance-seed | 6 | bytedance-seed/seed-2.0-lite | 200 | 2905 | LIVE (reasoning burned) |
| minimax | 6 | minimax/minimax-m1 | 200 | 1275 | LIVE (reasoning burned) |
| aion-labs | 5 | aion-labs/aion-3.0-mini | 200 | 819 | LIVE (200, no content at cap 1) |
| amazon | 5 | amazon/nova-lite-v1 | 200 | 741 | LIVE (content 2 chars) |
| inclusionai | 5 | inclusionai/ling-3.0-flash | 200 | 1991 | LIVE (reasoning burned) |
| meta-llama | 5 | meta-llama/llama-3.1-8b-instruct | 200 | 573 | LIVE (content back) |
| sentence-transformers | 5 | all-minilm-l6-v2 (embeddings) | 200 | 1428 | LIVE embed dim=384 |
| voyageai | 5 | voyage-4-lite (embeddings) | 200 | 388 | LIVE embed dim=1024 |
| xiaomi | 5 | xiaomi/mimo-v2.6-flash | 200 | 882 | LIVE (200, no content at cap 1) |
| ~openai | 5 | ~openai/gpt-mini-latest | 200 | 1166 | LIVE (content 50 chars) |
| meta | 4 | meta/muse-spark-1.1 | 200 | 1862 | LIVE (200, no content at cap 1) |
| nvidia | 4 | nvidia/nemotron-3-nano-30b-a3b | 200 | 1828 | LIVE (reasoning burned) |
| poolside | 4 | poolside/laguna-xs-2.1 | 200 | 487 | LIVE (reasoning burned) |
| ~anthropic | 4 | ~anthropic/claude-opus-latest | 200 | 1769 | LIVE (200, no content at cap 1) |
| baai | 3 | bge-m3 (embeddings) | 200 | 749 | LIVE embed dim=1024 |
| cohere | 3 | cohere/command-a-plus | 200 | 496 | LIVE (reasoning burned) |
| intfloat | 3 | e5-base-v2 (embeddings) | 200 | 1359 | LIVE embed dim=768 |
| meituan | 3 | meituan/longcat-2.0 | 200 | 2932 | LIVE (reasoning burned) |
| sakana | 3 | sakana/fugu-max | 400 | 637 | PROBE-400 "request is not valid, check model name and parameters" (one-attempt law, not retried; may be param shape, not family death) |
| stepfun | 3 | stepfun/step-3.5-flash | 200 | 1030 | LIVE (reasoning burned) |
| tencent | 3 | tencent/hy3 | 200 | 1466 | LIVE (reasoning burned) |
| upstage | 3 | upstage/solar-mini4 | 200 | 712 | LIVE (content 1 char) |
| ~deepseek | 3 | ~deepseek/deepseek-flash-latest | 200 | 688 | LIVE (reasoning burned) |
| inception | 2 | inception/mercury-2 | 200 | 1804 | LIVE (200, no content at cap 1) |
| perplexity | 2 | pplx-embed-v1-4b (embeddings) | 200 | 425 | LIVE embed dim=2560 |
| thenlper | 2 | gte-base (embeddings) | 200 | 960 | LIVE embed dim=768 |
| thinkingmachines | 2 | thinkingmachines/inkling-small | 200 | 618 | LIVE (200, no content at cap 1) |
| unbiased | 2 | unbiased/pareto | 200 | 2179 | LIVE (content 35 chars, finish=stop) |
| ~google | 2 | ~google/gemini-pro-latest | 200 | 2686 | LIVE (200, no content at cap 1) |
| ~z-ai | 2 | ~z-ai/glm-flash-latest | 200 | 3797 | LIVE (reasoning burned) |
| arcee-ai | 1 | arcee-ai/trinity-large-thinking | 200 | 746 | LIVE (reasoning burned) |
| fireworks | 1 | fireworks/ember-1 | 200 | 1039 | LIVE (reasoning burned) |
| ibm-granite | 1 | ibm-granite/granite-4.2-8b | 200 | 1888 | LIVE (reasoning burned) |
| kwaipilot | 1 | kwaipilot/kat-coder-pro-v2.5 | 400 | 845 | PROBE-400 "request is not valid, check model name and parameters" (one-attempt law, not retried; may be param shape) |
| nex-agi | 1 | nex-agi/nex-n2.5-pro | 200 | 2513 | LIVE (reasoning burned) |
| perceptron | 1 | perceptron/perceptron-mk1.5 | 200 | 1816 | LIVE (200, no content at cap 1) |
| prism-ml | 1 | prism-ml/ternary-bonsai-2-27b | 200 | 1018 | LIVE (reasoning burned) |
| rekaai | 1 | rekaai/reka-edge | 200 | 925 | LIVE (content 5 chars) |
| relace | 1 | relace/relace-search | 200 | 1573 | LIVE (content 5 chars; search-surface model) |
| sao10k | 1 | sao10k/l3.1-euryale-70b | 200 | 1349 | LIVE (content 1 char) |
| stealth | 1 | stealth/space-bunny-alpha | 200 | 2798 | LIVE (200, no content at cap 1) |
| ~moonshotai | 1 | ~moonshotai/kimi-latest | 200 | 1938 | LIVE (reasoning burned) |
| ~x-ai | 1 | ~x-ai/grok-latest | 200 | 9823 | LIVE (reasoning burned; slowest row) |

Tally: 50 of 52 families LIVE (41 chat 200 sweep + 3 chat 200 run 1 + 6 embeddings 200). 2 probe-400 (sakana, kwaipilot).

## KIMI VERDICT: LIVE via Nous (acquisition door NOT needed)

- Byte evidence: moonshotai/kimi-k2 chat HTTP 200 in 791ms with 5 chars of real content; ~moonshotai/kimi-latest HTTP 200 in 1938ms (reasoning burned the 1-token cap). Moment 2026-10-01T22:00:17-22:01:37Z sweep.
- Kimi SKUs the garden already serves (Nous catalog, 9 + 1 alias): kimi-k2, kimi-k2-0905, kimi-k2-thinking, kimi-k2.5, kimi-k2.6, kimi-k2.7-code, kimi-k3, kimi-k3:US, kimi-k3:batch, plus ~moonshotai/kimi-latest.
- Acquisition door card (only if Nous drops Kimi):
  - Direct door: https://platform.kimi.ai (https://platform.moonshot.ai 301-redirects there; observed 2026-10-01). API base api.moonshot.ai/v1 is ALREADY wired in configs/providers.yaml as the (dormant) moonshot provider block, key env MOONSHOT_API_KEY, which is ABSENT from .env (checked by name-grep, case-tolerant). The pricing page (platform.kimi.ai/docs/pricing/chat) documents NO free tier - only "temporarily free" file APIs (content extraction and storage) for inference customers; card requirement not stated on that page. No signup was performed (mission law).
  - Aggregator door: OpenRouter (key on file) carries 9 moonshotai ids (kimi-k3, kimi-k2.7-code, kimi-k2.6, kimi-k2.5, kimi-k2-thinking, kimi-k2-0905, kimi-k2, plus :batch and ~moonshotai/kimi-latest), ZERO :free variants among them (GET /api/v1/models 200, 464 ids, 2026-10-01T21:59Z).

## SECONDARY: outside-the-garden bases (one attempt per family; the Cloudflare 1010 story is an instrument finding, not a family verdict)

| family | base | key env | result | ms | verdict |
|---|---|---|---|---|---|
| xAI grok (SD acct) | https://api.x.ai/v1 | XAI_SD_API_KEY | /models 200 (14 ids: 9 grok chat incl grok-4.7 + grok-4.20 variants, 5 imagine media); chat grok-4.20-0309-non-reasoning 200, content 2 chars | 282 / 621 | LIVE (funded per driving ladder) |
| DeepSeek | https://api.deepseek.com/v1 | DEEPSEEK_API_KEY | chat deepseek-v4-flash 200 (thinking disabled carriage), content 2 chars | 702 | LIVE (the paid workhorse) |
| z.ai Pro | https://api.z.ai/api/coding/paas/v4 | ZAI_API_KEY_Pro | chat glm-4.7-flash 200, reasoning burned | 1084 | LIVE (free flash cache-mining) |
| z.ai Lite | same base | ZAI_API_KEY_Lite | chat glm-4.7-flash 200, reasoning burned | 1099 | LIVE (free flash cache-mining) |
| Groq | https://api.groq.com/openai/v1 | GROQ_API_KEY | first attempt 403 Cloudflare "error code: 1010" (urllib UA ban); UA-fixed single probe: chat openai/gpt-oss-120b 200 | 417 | LIVE (the 403 was the UA, not the lane) |
| Together | https://api.together.xyz/v1 | TOGETHER_API_KEY | first 403 CF-1010 same cause; UA-fixed: chat deepseek-ai/DeepSeek-V4-Flash-0731 200 | 1778 | LIVE |
| Cohere | https://api.cohere.com/compatibility/v1 | COHERE_API_KEY_FREE | /models 200 (35 ids); chat c4ai-aya-expanse-32b 200, content 2 chars | 240 / 288 | LIVE (NOTE: providers.yaml expects COHERE_API_KEY but .env carries COHERE_API_KEY_FREE / _PAID - a name gap) |
| OpenRouter | https://openrouter.ai/api/v1 | OPENROUTER_API_KEY | /models 200 (464 ids); chat liquid/lfm-2.5-2.6b:free 200 | 710 / 310 | LIVE (the aggregator; carries the 9 kimi ids above) |
| Ollama local | http://127.0.0.1:11434 | none | GET /api/tags 200, 17 local models (gemma:2b, athena-class, frob/ling-3.0-flash, qwen2.5:7b, maze-keeper, deepseek-r1:1.5b, ...) | 113 | LIVE (free local) |
| Gemini | https://generativelanguage.googleapis.com/v1beta/openai | GEMINI_API_KEY | /models 200 (61 ids); chat gemini-2.5-flash 404 "no longer available to new users" | 260 / 235 | DEAD for generation with the on-file key (B2-61/B2-63 verdict stands: Vertex express key, not AI Studio) |
| Mistral | https://api.mistral.ai/v1 | MISTRAL_API_KEY | chat mistral-small-latest 429 code 1300 rate limit (limit-0 class) | 322 | DEAD (dormant, B2-61 stands) |
| Anthropic direct | https://api.anthropic.com/v1 | ANTHROPIC_API_KEY | messages claude-3-5-haiku 401 "API key is invalid" | 249 | DEAD (unfunded; driving ladder's "no Opus rung" stands - but Claude IS reachable through the Nous garden and OpenRouter) |
| OpenAI direct | https://api.openai.com/v1 | OPENAI_API_KEY | chat gpt-4o-mini 429 "You have no credits remaining" | 1531 | DEAD (no credits; gpt family reachable via Nous garden) |
| Cerebras | https://api.cerebras.ai/v1 | CEREBAS_API_KEY | first 403 CF-1010 (UA); UA-fixed: 402 payment_required "Visit your billing tab" | 227 | DEAD (card-gated trial, B2-36 stands) |

## Prices (only where configs/cost_rates.yaml already carries them)

- deepseek-v4-flash: offpeak 0.007 hit / 0.22 miss / 0.66 out per M (peak 2x), source api-docs.deepseek.com
- glm-4.7-flash and glm-4.5-flash (z.ai): FREE (all tiers), source docs.z.ai
- glm-5.3-flash: 0.015 / 0.075 / 0.25 per M; grok-4.5: planning prior in cost_rates.yaml (API pricing separate)
- Everything else probed: price not in configs; Nous credits ($180 armed per driving ladder) or the vendor dashboard is the source of truth.

## Bottom line

The estate's reachable model garden is the Nous inference API: 52 families / 424-427 SKUs / 50 families live on one key chain (HERMES_API_KEY_1/2), Kimi included. Outside the garden, 8 secondary surfaces are live (xAI SD, DeepSeek, z.ai Pro + Lite, Groq, Together, Cohere free key, OpenRouter, Ollama local) and 5 are dead-with-evidence (Gemini generation, Mistral limit-0, Anthropic direct 401, OpenAI no-credits, Cerebras 402). Registered nothing else; no INDEX.json promotion from this lane.
