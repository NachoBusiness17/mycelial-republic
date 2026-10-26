# Compute map: what's free today and the two-minute path (2026-10-24)

**Order:** find new compute, make claiming it easy. "If it's not easy it's not water."

## The map, probed live

| state | provider | detail |
|---|---|---|
| **READY** | deepseek | deepseek-flash · 1.1 s |
| **READY** | z.ai coding plan | glm-4.6 · 3.1 s (coding endpoint works where paas/v4 says no balance) |
| **READY** | OpenRouter `:free` | liquid/lfm-2.5-2.6b · 2.1 s |
| **READY** | Nous free | longcat-2.5 · 2.2 s |
| **READY** | Grok CLI | 123 s, subscription window |
| UNVERIFIED | GitHub Models | 200 in 250 ms, but it **echoes "OK" for any prompt** - not a completion. Left in the catalog, marked honest. |
| **CLAIM** (2 min) | LLM7.io | no card, no phone - 60 RPM free token |
| **CLAIM** (2 min) | Ollama Cloud | 6 free models |
| **CLAIM** (2 min) | SambaNova | free tier, ~294 tok/s, DeepSeek R1 |
| **CLAIM** (2 min) | Cloudflare Workers AI | 10k neurons/day |
| **NEEDS ONE KEY** | Google AI Studio | the current `GEMINI_API_KEY` is an OAuth-only Cloud key (401 "API keys not supported"); a Studio key is a different token |
| **NEW KEY** | Groq | both existing keys are 401 - free plan is 1k req/day once replaced |
| **NEW KEY** | Mistral | both keys 429 on the free plan |
| DEAD | Cerebras | account has no entitlement (402 on gpt-oss-120b) |
| DEAD | NVIDIA NIM | key lists models, chat returns 403 |

## The easy path (this is the whole point)

```
python tools/compute_finder.py claim        # the 7 above, with URLs
python tools/compute_finder.py add llm7     # paste key at the prompt
```

`add` **verifies before it writes**: if the key does not answer, nothing touches
`.env`; if it does, the key is appended and reported with its latency. One command,
one paste, no file editing, no restart.

Then it is immediately burnable:

```
python tools/burn_lanes.py run --lanes llm7 --tasks jung-no-freud
```

## What changed in the harness

- `tools/compute_finder.py` - catalog probe with READY / CLAIM / DEAD and the `add` flow.
- `configs/compute_catalog.json` - 14 providers, each with base URL, model, env var,
  free-tier note and signup link.
- `tools/burn_lanes.py` - learned to pass provider-specific headers and to accept
  non-JSON responses (GitHub Models), plus the reasoning-budget fix from the last wave.

## Honest scoreboard

Before this: 11 usable lanes, several requiring re-auth. Now: **5 ready without
touching anything, 7 one-paste away**, 2 provably dead. The bottleneck is no longer
discovery - it is that four keys need a human to log in, and that is a two-minute
job per provider with the exact URL printed above.
