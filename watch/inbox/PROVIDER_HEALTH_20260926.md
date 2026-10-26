# PROVIDER HEALTH 2026-09-26 (B2-04 live probe)

Live probe of every free lane in configs/providers.yaml with a key on file in .env.
Method: urllib GET /models, then 3 tiny alive calls, then 3 synthetic estate prompts
(public-domain Gettysburg summarize, Go position classify, word count). All prompts
synthetic/public; no repo contents or private material left the machine. Harness:
watch/inbox/burn_wave_20260926/B2_04_probe.py (round 1) + B2_04_probe2.py (round 2
diagnostics). Raw JSON: B2_04_probe_results.json, B2_04_probe_results2.json.

## Scoreboard

| Lane | Endpoint | Model tested | Alive | Measured denominator (live response) | Tokens burned today |
|---|---|---|---|---|---|
| groq | api.groq.com/openai/v1 | openai/gpt-oss-120b (reasoning_effort low) | YES 3/3 | x-ratelimit-limit-requests: 1000, x-ratelimit-limit-tokens: 8000 (min window; reset observed 7m12s / 3.78s) | 489 |
| openrouter key1 | openrouter.ai/api/v1 | stealth/space-bunny-alpha | YES 3/3 | /key: limit null (no cap), usage $4.608; catalog 458 models, 17 :free ids | 801 |
| openrouter key2 | openrouter.ai/api/v1 | stealth/space-bunny-alpha | YES 3/3 | /key: limit null, usage $0.7377 | 808 |
| nous (Hermes k1) | inference-api.nousresearch.com/v1 | stealth/space-bunny-alpha | YES 3/3 | full x-ratelimit set exposed (50 req/min, 2100 req/h, 500k tok/min, 6M tok/h; B2_04_probe_results.json rl block); 0 x 429 across 7 calls | 822 |
| together | api.together.xyz/v1 | deepseek-ai/DeepSeek-V4-Flash-0731 | YES 3/3 | no rate headers exposed; trial credits, unmeasured remainder | 540 |
| cohere | api.cohere.com/compatibility/v1 | command-r-plus-08-2024 | YES 3/3 | no rate headers exposed; trial key COHERE_API_KEY_FREE | 180 |
| z_ai Pro | api.z.ai/api/coding/paas/v4 | glm-4.7-flash | YES (degraded) | 429 code 1305 "temporarily overloaded" on ~1 in 3 calls at 6s spacing; recovers after 15s wait | 1801 (incl 1 alive call) |
| z_ai Lite | api.z.ai/api/coding/paas/v4 | glm-4.7-flash | YES (degraded) | heavier 429s: 2 of 5 attempts rejected incl 1 retry; count_words never landed | 1449 (incl 1 alive call) |
| cerebras | api.cerebras.ai/v1 | gpt-oss-120b | NO | /models 200 (2 models: qwen-3.8-27b, gpt-oss-120b) but chat 402 Payment Required x3, empty body = zero usable credit | 0 |
| nvidia | integrate.api.nvidia.com/v1 | meta/llama-3.1-8b chain, then 01-ai/yi-large | NO | /models 200 (82 models, stale roster) but chat 410 Gone x3; listed model 404: "Function '23bd454d...': Not found for account" = zero callable functions post-purge | 0 |
| gemini | generativelanguage.googleapis.com/v1beta | gemini-2.5-flash | NO (inference) | /models 200 (61 models) with Bearer AQ.* key, but generateContent 401 as API key ("API keys are not supported by this API") and 401 as Bearer ("invalid authentication credentials") | 0 |
| mistral | api.mistral.ai/v1 | mistral-small-latest | NO (quota zero) | /models 200 (46 models) but chat 429 x3 with x-ratelimit-limit-req-minute: 0, remaining: 0 | 0 |
| ollama (local) | 127.0.0.1:11434/v1 | n/a (context row) | YES | /models 200, 16 models | local, n/a |
| saelis | 127.0.0.1:8080/v1 | n/a | NO (declared dormant) | one probe per law: connection refused (status 0); providers.yaml says never probe | 0 |
| hf_router | router.huggingface.co/v1 | - | NO PROBE | no HF_TOKEN on file | 0 |
| github_models | models.inference.ai.azure.com | - | NO PROBE | no GITHUB_MODELS_TOKEN; gh CLI token absent | 0 |
| dashscope | dashscope.aliyuncs.com | - | NO PROBE | no DASHSCOPE_API_KEY on file | 0 |
| moonshot | api.moonshot.ai/v1 | - | NO PROBE | no MOONSHOT_API_KEY on file | 0 |
| fireworks | api.fireworks.ai/inference/v1 | - | NO PROBE | no FIREWORKS_API_KEY on file | 0 |
| z_ai main + sd-max | api.z.ai/api/paas/v4 | - | SKIPPED | opencode_only per providers.yaml law; raw use is fence risk (fake-1113 lore) | 0 |

Total external burn today: 6,586 tokens on the estate prompts, plus 304 on alive
pings (z_ai lanes) = 6,890 usage-reported tokens across 8 answering lane-keys.

## Burn answers (real, trimmed)

Word-count ground truth: 14 words. Cohere answered 13; all other lanes 14.

- groq summarize: "In 1776, the founders established a nation founded on liberty and the belief that all people are eq..." (dates it 1776; prompt said Gettysburg 1863, "four score and seven")
- nous summarize: "Eighty-seven years earlier, the Founding Fathers created the United States as a nation dedicated to..."
- together summarize: "Eighty-seven years ago, the founders established a new nation on the principles of liberty and the..."
- cohere summarize: "In 1863, Abraham Lincoln's Gettysburg Address referenced the founding of the United States, a natio..."
- openrouter stealth (both keys): "Eighty-seven years earlier, America's founders created a nation dedicated to liberty and e..." / "In 1863, Lincoln declared that the United States was founded as a nation dedicated to libe..."
- zai-pro summarize: "Our nation was founded 87 years ago on this continent with the ideals of liberty and equal..." ; go classify died into reasoning at 600 budget (600 completion tokens, no content); count: "14" after one 429 + retry
- zai-lite: summarize died into reasoning at 600 budget; go classify: "opening"; count_words: 429 (code 1305) even after retry

## Verdict lines for dormant / dead lanes

- cerebras: endpoint serves a catalog, sells no inference to this key. 402 x3. Fix = credits/billing, not config.
- nvidia: catalog is a fossil (82 ids incl fuyu-8b, dbrx); every chat id is gone for this account (410/404 function not found). Config roster of 18 ids needs a full purge or the lane needs a new key class.
- gemini: the AQ.* credential reads the catalog but cannot generate. Both auth modes 401. Swap to an AI Studio AIza key or wire OAuth.
- mistral: free tier measured at literally 0 req/min on this key. Lane is a nameplate until the account is validated.
- old openrouter :free ids in providers.yaml (meta-llama/llama-3.3-70b-instruct:free, google/gemma-2-9b-it:free): 404, absent from today's 458-model catalog. The 17 real :free ids today include qwen/qwen3.8-27b:free and inclusionai/ling-3.0-flash-{sante,fin}:free.

Receipt: watch/inbox/burn_wave_20260926/B2_04_provider_health_20260926.md
