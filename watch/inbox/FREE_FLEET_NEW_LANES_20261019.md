# FREE FLEET NEW LANES - 2026 survey + live pings (2026-10-19)

Classification: RECEIPT (survey + live probe evidence; lane-opening intel for the free fleet)
Producer: zcode-seat L2-new-lanes, 2026-10-19
Method: WebSearch sweep (2026 sources) + live curl against every lane the estate holds a key for, plus three keyless providers. Key values never echoed; results quoted are byte-backed in this seat's transcript. Baseline compared against `watch/inbox/free_keys_20261014/VERDICT.md` (5 days of drift).

## HEADLINE (3 lines)

1. The Gemini 404 drift is SOLVED: new-account keys (G_API_NACHO/G_API_SD class) serve **gemini-3.5-flash** and **gemini-3.1-flash-lite** free, verified 200 end to end today. gemini-3.8-flash still hangs; gemini-2.5-flash is 404-locked for new users.
2. Two brand-new KEYLESS lanes verified live with zero signup: **LLM7.io** (anonymous chat 200, GLM-5.3-Flash) and **OVHcloud AI Endpoints** (anonymous chat 200, Qwen3.8-27B, EU-hosted, 2 RPM/IP/model).
3. GitHub Models is RETIRED (chat endpoint answers a bare "OK" stub, docs say fully retired 2026-07-30): the unpinged GITHUB_TOKEN lane is dead on arrival for inference.

## Section 1: NEW LIVE LANES, verified keyless today

### LLM7.io - LIVE, keyless, anonymous

- Endpoint: `https://api.llm7.io/v1/chat/completions` (OpenAI-compatible). Anonymous works with no key (send `Authorization: Bearer unused` or none for anonymous tier).
- Verified today: chat 200 twice - GLM-5.3-Flash replied "OK" in 4.85s; gpt-oss:20b replied in 1.44s (reasoning-class: burns budget on `reasoning`, set max_tokens >= 300, same one-bug as RIB_INFERENCE_BUDGET).
- Limits (per awesome-free-llm-apis, 2026): free token gives 60 RPM, 250 req/h, 100K tokens/24h; anonymous tier is smaller. Get token at https://token.llm7.io / https://dash.llm7.io.
- Model list (live `/v1/models`): GLM-5.3-Flash, gpt-oss:20b, DeepSeek-V4-Flash-0731, DeepSeek-V4.1-Flash (401 without a real key - keyless tier is per-model), plus a menu of claude-* names likely gated for anonymous.
- Fit: instant $0 sensing lane, no account, no key rotation - drop-in for the hermes_burn free queue as a second host to diversify 429 windows.

### OVHcloud AI Endpoints - LIVE, keyless, anonymous

- Endpoint: `https://oai.endpoints.kepler.ai.cloud.ovh.net/v1/chat/completions` (OpenAI-compatible).
- Verified today: `/v1/models` 200 keyless; chat 200 on **Qwen3.8-27B** (12.1s, reasoning model - it spent the whole 20-token budget thinking; budget >= 300 and consider Qwen3.5-9B for non-reasoning scut).
- Limits (2026): anonymous, 2 RPM per IP per model, no signup.
- Catalog highlights (live list): Qwen3.8-27B, Qwen3.5-9B, Qwen2.5-VL-72B-Instruct (vision), whisper-large-v3 + turbo (audio), bge-m3 / Qwen3-Embedding-8B (embeddings), Qwen3Guard-Gen-8B (safety).
- Fit: free EU-hosted vision + audio + embeddings that the local ollama shelf does not cover, keyless so any seat or cron can call it.

### Kilo Code gateway - models keyless, chat gated

- `https://api.kilo.ai/api/gateway/v1/models` returns 200 keyless (kilo-auto/efficient router, nemotron-3-ultra 550B, step-3.7-flash class models). Chat without sign-in: 401 `PAID_MODEL_AUTH_REQUIRED`.
- Limits per awesome-free-llm-apis: with a (free) account, 200 req/h per IP, no API key needed in the client.
- Fit: large-model sensing pool worth a free signup, but NOT keyless today. Park until an account is minted.

## Section 2: KEYED LANES, status refresh vs the 2026-10-14 verdict

### Gemini - DRIFT SOLVED, free tier confirmed alive on new keys

- Live test on G_API_SD (new-account key): models list 200 (63 models). Chat: **gemini-3.5-flash 200 "OK" in 1.35s**, **gemini-3.1-flash-lite 200 "OK" in 0.78s**. gemini-2.5-flash: 404 "no longer available to new users" (unchanged). gemini-3.8-flash: hangs past 40s (the 10-14 503 became a hang; still not serving).
- Grandfathered GEMINI_API_KEY still lists 63 models and served gemini-2.0-flash on 10-14.
- 2026 landscape: Pro models left the free tier April 2026 (https://www.cloudzero.com/blog/gemini-pricing); per-model free rate limits no longer published (https://ai.google.dev/gemini-api/docs/rate-limits); an AI-forum thread reports free-tier changes around Oct 20, 2026 - TOMORROW (https://discuss.ai.google.dev/t/has-gemini-api-completely-stopped-its-free-tier/109230). Re-probe daily; treat free tier as at-risk.
- Fit: the desktop heavy tier named in the 10-16 DRY amendment now has a working API face again - wire gemini-3.5-flash into the judgment ladder as the free long-context rung.

### NVIDIA NIM - chat still 403-gated; catalog refreshed and worth the fix

- Live: `/v1/models` 200 with all three keys (81 models). Chat on ANY model = 403 "Authorization failed" (retested on current IDs: nemotron-3-ultra-550b-a55b, nemotron-3.5-lightning-30b-a3b, deepseek-v4.1-flash). Matches the 10-14 verdict: keys are list-scoped, chat tier-gated.
- Root cause and fix: the free 1,000-credit trial expired/never activated; chat requires joining the free NVIDIA Developer Program, which upgrades to 40 RPM / 10,000 RPD per model (https://build.nvidia.com/explore/discover, tier facts via https://github.com/mnfst/awesome-free-llm-apis).
- Catalog worth the fix: nvidia/nemotron-3-ultra-550b-a55b (1M-context class), nemotron-3-super-120b-a12b, nemotron-3.5-lightning-30b-a3b, deepseek-ai/deepseek-v4.1-flash. The old meta/* llama models are all EOL since 2026-08-26 (410 Gone).
- Fit: would be the estate's free long-context judgment lane (nemotron-3-ultra 1M ctx) - one free Developer Program signup lifts three dead keys.

### Mistral - still hard 429, sensor-lane only

- Live: both MISTRAL_API_KEY and MISTRAL_API_KEY_2 return 429 code 1300 immediately on chat, even paced 62s apart. Unchanged from 10-14. Free "Experiment" tier is phone-verified and training-data-shared (https://docs.mistral.ai/deployment/laplateforme/tier/).
- Fit: keep as a 1-req/min sensor at best; do not plan work on it.

### GitHub Models - RETIRED, lane dead

- Live: `POST https://models.github.ai/inference/chat/completions` with GITHUB_TOKEN answers HTTP 200 with body literally `OK` - a stub, not a chat completion object. `models.github.ai` still serves a marketing page. Docs confirm full retirement 2026-07-30 (https://docs.github.com/en/github-models; community note https://github.com/orgs/community/discussions/149698).
- Fit: NONE for inference. GITHUB_TOKEN stays useful for repos/API only. Migration targets named by GitHub: Azure AI Foundry, OpenRouter.

### Confirmed dead / parked (no change from 10-14, spot-checked)

- Groq: both keys 401 (10-14, curl cross-checked). xAI/Grok: credits-dry (10-14). Cerebras: 402 payment-required card-gate (10-14); 2026 web sources conflict on whether a permanent free tier still exists (https://klymentiev.com/blog/free-llm-api says it became a $5/30-day credit) - matches the estate's card-gate experience, stays parked.
- Together: auth valid, serverless-tier chat worked on 10-14 - still the estate's only "free-ish" turbo lane; unchanged.

## Section 3: FREE TIERS WORTH AN ACCOUNT (no estate key yet)

| Provider | What is free | How the estate keys up | One-line fit |
|---|---|---|---|
| Cloudflare Workers AI | 10,000 Neurons/day, resets 00:00 UTC, fails-not-bills (https://developers.cloudflare.com/workers-ai/platform/pricing) | Free signup + API token; no CF key in .env today | ~2-3M LLM tokens/day free incl gpt-oss-120b, llama-3.3-70b, glm-4.7-flash, deepseek-r1-distill - the biggest untapped daily free budget on this list |
| Ollama Cloud | Session windows every 5h + weekly caps, 16 cloud model families (deepseek-v4-pro, kimi-k3, qwen3.5:397b-class) (https://ollama.com/pricing) | Free ollama.com account; existing local CLI speaks it natively | Remote big-model GPU bursts with zero new client code - the estate's ollama muscle lifted to 100B+ class |
| NVIDIA Developer Program | Lifts all 3 dead keys to 40 RPM / 10,000 RPD per model, 100+ models | Free join at https://www.nvidia.com/en-us/developer-program/ | The 1M-context nemotron judgment lane, see Section 2 |
| HF Inference Providers | $0.10/month credits for free accounts (https://huggingface.co/docs/inference-providers/en/pricing) | Free HF account + token (none in .env) | Near-zero value - skip unless a HF account exists for Spaces anyway |
| Aion Labs | 15 RPM, 20K tokens/day, no card (aion-2.0/3.0, 128K ctx) (https://www.aionlabs.ai) | Free signup + key | Minor extra sensing lane, 128K context |
| ModelScope (CN) | 2,000 RPD total, 500/model, Qwen3.5 family (https://modelscope.cn) | Alibaba Cloud binding + real-name verification | Blocked by real-name gate for intl users - skip |
| SiliconFlow (CN) | Permanently free Qwen3-8B, 1,000 RPM (https://cloud.siliconflow.cn) | Real-name ID verification; intl needs support contact | Skip - verification wall |

## Section 4: FREE GPU COMPUTE, 2026 state

| Platform | Free allowance (2026) | Card needed | One-line fit |
|---|---|---|---|
| Kaggle | ~30 GPU h/week, P100 or 2xT4 (16GB), 12h sessions, most predictable quota (https://www.kaggle.com/product-announcements/575468) | No | Weekly batch jobs: evals, GGUF quantizing, dataset processing off the RX 5600 XT |
| Google Colab free | ~15-30 GPU h/week, T4/P100, no guarantee, idle disconnects | No | Ad-hoc GPU scut when Kaggle quota is spent; combined ~60 h/week |
| Lightning AI | 15 monthly credits (~22 T4 h) + one-time 80 free GPU hours; 4h active CPU studio (https://lightning.ai/pricing) | No | Second monthly GPU tranche with persistent Studio storage |
| vast.ai | (already in estate, paid rental) | - | Keep as the paid overflow rung per the GPU ladder rib |

- Paperspace Gradient: no 2026 source surfaced a live free GPU tier after the DigitalOcean acquisition - treat as dead until proven otherwise.
- Estate box context (RIB_GPU_LADDER_20261001): AMD RX 5600 XT - these cloud tiers are the only CUDA path short of a card purchase, useful for quant/correction work the rib already banked.

## Section 5: FREE AGENT HOSTING, 2026 state

- Hugging Face Spaces: free CPU Spaces + 2 ZeroGPU Gradio Spaces per free account; Static Spaces free; free Docker SDK restricted and Spaces sleep after ~48h inactivity (https://huggingface.co/pricing). Fit: demo/public face for harness organs, not for always-on agents.
- Render: free web services historically 750 instance-hours with 15-min spin-down (2026 status unverified, rate-limited search; https://render.com/docs/free). Fit: low-traffic webhook endpoints if spin-down is tolerated.
- Fly.io: free plans discontinued Oct 2024, new orgs pay-as-you-go (https://docs.fly.io/about/discontinued-plans). Fit: none for free.
- Cloudflare Workers free plan (100K req/day) + Workers AI Neurons: the strongest free agent-hosting combo in 2026 given the estate already runs Vercel-shaped services. Fit: cron-grade always-on agents at $0.

## Scoreboard

- New lanes verified LIVE today, zero signup: 2 (LLM7.io, OVHcloud AI Endpoints).
- Keyed lanes flipped to working: 1 class (Gemini new-account keys: gemini-3.5-flash + gemini-3.1-flash-lite; effectively 2-3 keys revived).
- Lanes confirmed dead today: 1 (GitHub Models, retired).
- Lanes one-free-signup away: 4 (Cloudflare Workers AI, NVIDIA Developer Program lift, Ollama Cloud, Kilo Code).
- Free GPU weekly envelope available with zero card: ~60-75 GPU-hours (Kaggle + Colab + Lightning).

## Falsifier

If wiring gemini-3.5-flash and the two keyless lanes into the free queue does not raise landed-per-day above the 10-16 single-host baseline (5 deliverables/day), the lanes are redundant windows on the same upstream, not added capacity - re-measure before adding more.

## NEXT TASK (self-designed)

Wire the three zero-cost wins into the free queue in one sitting: (1) register a Cloudflare free account + API token and bank it as `CLOUDFLARE_AI_TOKEN` in .env (10,000 Neurons/day is the biggest untapped daily budget); (2) add LLM7.io + OVHcloud anonymous endpoints as keyless hosts in `tools/hermes_burn.py`'s free-lane config (both OpenAI-compatible, no keys to rotate); (3) point the Gemini lane's new-account keys at gemini-3.5-flash and run a daily re-probe tripwire, because the free tier reportedly shifts around 2026-10-20.
