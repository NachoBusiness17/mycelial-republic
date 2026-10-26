# FREE KEYS PROBE - full verdict (2026-10-14, three rounds, curl + urllib cross-checked)

Method: /models list + 1-token chat per key per lane; values never echoed;
raw results in probe_results.json; rounds 2-4 re-probed the 403/404/429
classes with curl (urllib's TLS fingerprint was being blocked by two
providers, masking real errors).

## LIVE (chat verified end to end)

| lane | keys | evidence |
|---|---|---|
| OpenRouter | OPENROUTER_API_KEY, OPENROUTER_API_KEY_2 | 400 models, chat OK 0.5-1.8s via openrouter/auto |
| Z.ai | ZAI_API_KEY, ZAI_API_KEY_2, ZAI_API_KEY_3 | 11 models, chat OK ~1s via glm-4.5-flash; NOTE content returned empty at max_tokens 8 - the RIB_INFERENCE_BUDGET one-bug (flash reasons); lane config wants thinking-disabled + >=256 budget |
| Cohere | COHERE_API_KEY_FREE, COHERE_API_KEY_PAID | 20 models, chat OK via command-r-08-2024: 'Ok.' |
| Together | TOGETHER_API_KEY, TOGETHER_API_KEY2 | auth valid; chat 200 via meta-llama/Llama-3.3-70B-Instruct-Turbo (serverless tier only - non-serverless models 400 with dedicated-endpoint upsell) |
| Gemini (old account) | GEMINI_API_KEY | 63 models, chat OK via gemini-2.0-flash (grandfathered account) |

## VALID KEY, QUOTA/GATE CLASS (auth passes, service refuses)

| lane | verdict |
|---|---|
| Mistral | MISTRAL_API_KEY, MISTRAL_API_KEY_2: AUTH VALID (45/46 models listed), chat 429 rate-limited immediately - free tier rpm is tiny; lane wants 1 req/min pacing or it is a sensor lane only |
| Gemini (new accounts) | G_API_NACHO, G_API_SD: auth + models list OK; chat 404 - Google's own migration notice: "gemini-2.5-flash is no longer available to NEW USERS. Please use models/gemini-3.8-flash." gemini-3.8-flash then 503s for ALL keys (capacity) - the new generation exists but is not serving yet. INTEL: gemini-3.8-flash is the new model name; retest daily until 503 clears |
| Cerebras | CEREBAS_API_KEY: auth valid (404 model first, then 402 payment_required on gpt-oss-120b) - the card-gated trial from 09-26, quota empty. Lane stays dormant per the operator's PARKED ruling |
| xAI/Grok | GROK_API_KEY: auth valid, "team has used all available credits" - matches the known credits-dry state. GROK_API_KEY_2 not re-probed (same team expected) |
| NVIDIA | NVIDIA_API_KEY: /models 200 (80 models), chat 403 Authorization failed - key is models-list-scoped or chat-tier-gated; unusable for settles |

## DEAD / UNKNOWN

| lane | verdict |
|---|---|
| Groq | GROQ_API_KEY, GROQ_API_KEY_2: 401 Invalid API Key via curl (round-1 403 was urllib fingerprinting) - BOTH KEYS INVALID. If these were meant to be new, they were mistyped or revoked; owner action: re-copy from the console |
| OpenCode | OPENCODE, OPENCODE2: gateway reachable, auth reaches upstream, but every model tried (claude-sonnet-4, code-supernova, grok-code) returns "Upstream request failed: Model is unavailable" - account not provisioned for model access or wrong model ids; owner action: check the opencode console for the provisioned model list |

## Actions available (not taken - configs are sealed)

Wire the LIVE keys into providers.yaml api_key_envs lists (cohere FREE/PAID,
mistral_2, together_2, zai_3, gemini G_API_* when 3.8 clears, cerebras_2)
+ re-seal by name. Mistral/Z.ai lane configs want the inference-budget
params (thinking-disabled, paced rpm). Gemini new-account lanes should
carry gemini-3.8-flash with the 503 expected until Google's capacity lands.
