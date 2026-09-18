# COMPUTE WEALTH INVENTORY — every alive API key, every model (2026-09-18)

*Operator: "this is a wealth of knowledge sitting here unmined and unexploited."*

## CONFIRMED ALIVE (12 endpoints, 100+ models)

| Provider | Key | Status | Notable models |
|---|---|---|---|
| **groq** | GROQ_API_KEY | ALIVE (browser UA) | llama-3.3-70b, qwen3.8-27b, gpt-oss-120b/20b, +more |
| **groq2** | GROQ_API_KEY_2 | ALIVE (second account — doubles rate ceiling) | same catalog |
| **deepseek** | DEEPSEEK_API_KEY | ALIVE (526ms) | deepseek-chat, deepseek-reasoner |
| **gemini** | GEMINI_API_KEY | ALIVE (277ms) | gemini-2.0-flash, +more |
| **cohere** | COHERE_API_KEY_FREE | ALIVE (259ms) | command-r7b, +more |
| **xai** | XAI_API_KEY | ALIVE (293ms) | grok-3-mini, +more |
| **mistral** | Mistral_API_KEY | ALIVE (395ms) | ministral-8b, mistral-small, +more |
| **mistral2** | Mistral_API_KEY_2 | ALIVE (second account) | same catalog |
| **openai** | OPENAI_API_KEY | ALIVE (1128ms) | gpt-4o-mini, +more |
| **openrouter k1** | OPENROUTER_API_KEY | ALIVE (341ms) | stealth, free models, +200 more |
| **openrouter k2** | OPENROUTER_API_KEY_2 | ALIVE (second key — doubles stealth rate) | same |
| **nvidia** | NVIDIABuild | ALIVE (102 models confirmed in providers.yaml) | deepseek-v4-flash, llama-3.3, nemotron, kimi-k2.6, +97 more |
| **together** | TOGETHER_API_KEY | ALIVE (browser UA) | llama-3.3-70b-turbo, +more |
| **cerebras** | CEREBRAS_API_KEY | key name mismatch in .env (CEREBRAS vs actual) — need to find correct env var name | llama3.1-8b, +more |

## THE MATH

12 alive endpoints × 3-10 models each = **~50-100 unique model-lanes available at $0 or near-$0.**

The drivers currently use ~35 of these. The untapped: nvidia's 102-model catalog (only 3 wired), the second groq account (0 calls since the 7th), together, cohere, and the xai seat.

## WHAT TO DO

Every one of these needs to be in the research rotation and the build lane's fallback chain.
The free-tier rate ceilings are the constraint, not the model quality — gpt-oss-120b on groq
answers in 1-3 seconds, which is faster than most paid APIs. The wealth isn't one big model,
it's the DIVERSITY of the pool.
