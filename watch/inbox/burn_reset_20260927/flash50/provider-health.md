# Provider health table - f-18 (2026-09-28)

Census of `configs/providers.yaml` (28 provider blocks, lines 45-817) cross-folded against
`logs/provider_usage.jsonl` (76,568 rows, 0 unparseable, span 2026-07-20T15:20:47Z to
2026-09-28T18:05:59Z), `logs/usage.jsonl` (163,102 rows, last 2026-09-28T21:44:22Z), and
`logs/quota_state.json` (updated 2026-09-28T18:05:59Z). Key presence resolved through the
repo's own resolver (`models/providers.py:116-148` `_key_env_names` + `provider_keys`) after
`models.env_load.load_dotenv('.env')`. Key VALUES were never printed; only presence and
value-length were inspected. All times UTC.

"last used" = last row in the metered seam (`logs/provider_usage.jsonl`, written by
`models/quota.py:164` `record_usage`, called from the `chat_provider` path
`models/providers.py:324`). Where the L0 router path (logged only to `logs/usage.jsonl`)
used a provider more recently than the metered seam, both are shown.

| provider | default model | base_url | key_env(s) | key in .env | last used (UTC) | metered rows (ok) | state |
|---|---|---|---|---|---|---|---|
| saelis | saelis | http://127.0.0.1:8080/v1 (via SAELIS_BASE_URL) | none (api_key_default "saelis") | n/a | never (0 rows) | 0 (0) | DORMANT (yaml:64) |
| ollama | qwen2.5-coder:7b (6 listed) | http://127.0.0.1:11434/v1 (via OLLAMA_HOST) | none (api_key_default "ollama") | n/a | 2026-09-28T21:44:22Z L0 gemma:2b (usage.jsonl); metered seam last 2026-09-26T19:20:15Z | 3,031 (1,141) | LIVE (L0 today) |
| mlx-cluster | mlx-flagship | http://127.0.0.1:7777/v1 | none | n/a | never (0 rows) | 0 (0) | STUB, machines not landed (yaml:128-136) |
| nous | none set (first listed z-ai/glm-5.3-prime) | https://inference-api.nousresearch.com/v1 | HERMES_API_KEY_1, HERMES_API_KEY_2 | both nonempty | 2026-09-26T04:25:31Z | 3 (3) | IDLE-WARM, all 3 rows glm-5.3-prime |
| openrouter | openrouter/auto (14 listed) | https://openrouter.ai/api/v1 | OPENROUTER_API_KEY, OPENROUTER_API_KEY_2, OR_API_KEY, OR_API_KEY_2 | first 2 nonempty; OR_* absent | 2026-09-26T19:55:57Z | 185 (152) | IDLE-WARM |
| nous_api | stealth/space-bunny-alpha | https://inference-api.nousresearch.com/v1 | HERMES_API_KEY_1, HERMES_API_KEY_2 | both nonempty | never (0 rows) | 0 (0) | KEYED, NEVER METERED |
| openai | gpt-4o-mini | https://api.openai.com/v1 | OPENAI_API_KEY | nonempty | 2026-08-28T23:31:41Z | 21 (0) | BROKEN: 0 of 21 metered rows ok |
| anthropic | claude-sonnet-4-20250514 | https://api.anthropic.com/v1 | ANTHROPIC_API_KEY | nonempty | never (0 rows) | 0 (0) | KEYED, NEVER METERED; UNFUNDED per DRIVING LADDER (AGENTS.md) |
| groq | openai/gpt-oss-120b | https://api.groq.com/openai/v1 | GROQ_API_KEY, GROQ_API_KEY_2 | both nonempty | 2026-09-26T13:38:04Z | 536 (271) | IDLE-WARM |
| deepseek | deepseek-v4-flash | https://api.deepseek.com/v1 | DEEPSEEK_API_KEY, DEEPSEEK_SWARM_API_KEY | primary nonempty; SWARM alias absent | 2026-09-28T18:05:59Z | 70,827 (70,419) | LIVE, the workhorse: 92.5% of all metered rows, 99.4% ok |
| deepseek_overmind | deepseek-v4-flash | https://api.deepseek.com/v1 | DEEPSEEK_OVERMIND_API_KEY | ABSENT | 2026-08-09T17:12:42Z | 156 (156) | STALE + NO KEY: 0 resolvable keys today |
| vast | deepseek-v4-flash (override via VAST_OPENAI_MODEL) | https://api.vast.ai/v1 (via VAST_OPENAI_BASE_URL) | VAST_OPENAI_API_KEY | ABSENT | never (0 rows) | 0 (0) | NO KEY, NEVER USED |
| gemini | none set (roster purged B2-61) | https://generativelanguage.googleapis.com/v1beta/openai | GEMINI_API_KEY (+ alias GOOGLE_API_KEY) | both nonempty | 2026-07-28T09:50:47Z | 5 (0) | DORMANT (yaml:486), generation 401-dead; key present but lane dead |
| xai | grok-3-mini | https://api.x.ai/v1 | XAI_API_KEY, XAI_API_KEY_2, GROK_API_KEY, GROK_API_KEY_2 | XAI_API_KEY NOT in .env but set in Windows host env; XAI_API_KEY_2 absent; GROK_API_KEY nonempty; GROK_API_KEY_2 present but EMPTY value | 2026-09-26T01:07:33Z | 96 (48) | IDLE-WARM (resolves 2 keys: host-env XAI + .env GROK) |
| together | deepseek-ai/DeepSeek-V4-Flash-0731 | https://api.together.xyz/v1 | TOGETHER_API_KEY | nonempty | 2026-09-07T00:32:53Z | 12 (11) | IDLE |
| z_ai | none set (glm-4.7-flash listed) | https://api.z.ai/api/paas/v4 | ZAI_API_KEY | nonempty | 2026-09-22T04:46:30Z | 570 (338) | IDLE; opencode_only lane (yaml:542) |
| z_ai2 | none set (glm-4.7-flash, glm-5.3-flash) | https://api.z.ai/api/coding/paas/v4 | ZAI_API_KEY_Pro | nonempty | 2026-09-16T17:10:59Z | 202 (74) | IDLE |
| z_ai3 | none set (glm-4.7-flash, glm-5.3-flash) | https://api.z.ai/api/coding/paas/v4 | ZAI_API_KEY_Lite | nonempty | 2026-09-28T15:16:38Z | 624 (252) | LIVE (today) |
| z_ai4 | glm-4.7-flash | https://api.z.ai/api/paas/v4 | ZAI_API_KEY_2 | nonempty | 2026-08-27T11:15:04Z | 5 (2) | STALE; opencode_only lane |
| github_models | gpt-4o-mini | https://models.inference.ai.azure.com | GITHUB_MODELS_TOKEN | ABSENT | never (0 rows) | 0 (0) | NO KEY, NEVER USED |
| mistral | mistral-small-latest | https://api.mistral.ai/v1 | MISTRAL_API_KEY | nonempty (B2-296 canonical names) | never (0 rows) | 0 (0) | DORMANT (yaml:651), request-minute limit 0 live |
| moonshot | kimi-k2 | https://api.moonshot.ai/v1 | MOONSHOT_API_KEY | ABSENT | never (0 rows) | 0 (0) | NO KEY, NEVER USED |
| fireworks | accounts/fireworks/models/llama-v3p1-70b-instruct | https://api.fireworks.ai/inference/v1 | FIREWORKS_API_KEY | ABSENT | never (0 rows) | 0 (0) | NO KEY, NEVER USED |
| cerebras | gpt-oss-120b | https://api.cerebras.ai/v1 | CEREBRAS_API_KEY, CEREBAS_API_KEY | CEREBRAS_API_KEY absent; CEREBAS_API_KEY (the old one-R typo spelling) nonempty | 2026-09-26T13:37:14Z | 165 (155) | DORMANT (yaml:714), card-gated trial; resolves 1 key via typo name |
| nvidia | none set (roster purged B2-61) | https://integrate.api.nvidia.com/v1 | api_key_env NVIDIABuild; api_key_envs chain NVIDIA_API_KEY, NVIDIABuild-Autogen-46 | NVIDIABuild nonempty in .env, but the other two ABSENT | 2026-08-24T23:01:00Z | 100 (86) | DORMANT (yaml:758) + KEY TRAP: 0 resolvable keys, see finding K3 |
| cohere | command-r-plus | https://api.cohere.com | COHERE_API_KEY | ABSENT | never (0 rows) | 0 (0) | NO KEY, NEVER USED |
| hf_router | meta-llama/Llama-3.3-70B-Instruct | https://router.huggingface.co/v1 | HF_TOKEN | ABSENT | never (0 rows) | 0 (0) | NO KEY, NEVER USED |
| dashscope | qwen-max | https://dashscope.aliyuncs.com/compatible-mode/v1 | DASHSCOPE_API_KEY | ABSENT | never (0 rows) | 0 (0) | NO KEY, NEVER USED |

## Tally

- 28 providers declared; 5 with `dormant: true` (saelis, gemini, mistral, cerebras, nvidia).
- 18 providers resolve at least 1 key through the repo resolver; 10 resolve 0 (mlx-cluster is
  keyless by design as a local stub, so 9 remote lanes are zero-keyed: deepseek_overmind,
  vast, github_models, moonshot, fireworks, nvidia, cohere, hf_router, dashscope).
- 12 providers have 0 metered rows ever (saelis, mlx-cluster, nous_api, anthropic, vast,
  github_models, mistral, moonshot, fireworks, cohere, hf_router, dashscope).
- 3 providers fired on 2026-09-28 (UTC): deepseek 18:05:59Z, z_ai3 15:16:38Z, ollama 21:44:22Z
  (L0 path, usage.jsonl only).
- deepseek is 70,827 of 76,568 metered rows (92.5%); ok rate 70,419/70,827 = 99.4%.
- .env declares 54 variable names (mtime 2026-09-28 check: file mtime 2026-09-27T07:52:26 local);
  GROK_API_KEY_2 is declared with an EMPTY value.

## Findings

- K1 (empty key): `GROK_API_KEY_2` sits in .env with a zero-length value; `provider_keys`
  (models/providers.py:136-148) requires a non-empty value, so the xai chain really runs on
  2 keys (host-env XAI_API_KEY + .env GROK_API_KEY), not 4.
- K2 (host-env-only key): `XAI_API_KEY` is absent from .env but set in the Windows host
  environment; it resolves only where the host env reaches (measured: `os.environ` had it
  before load_dotenv ran). A WSL/docker seat without that host var loses the xai primary.
- K3 (chain-list shadowing): for nvidia, `api_key_envs` is a list, and `_key_env_names`
  (models/providers.py:121-124) uses ONLY that list, dropping the primary `api_key_env`
  NVIDIABuild, which IS nonempty in .env. Net: nvidia resolves 0 keys despite the live key
  sitting in .env under the primary name. The yaml comment at configs/providers.yaml:741-742
  ("the live key sits in .env under ... NVIDIABuild-Autogen-46") is stale against current
  .env bytes. Inert today only because the lane is dormant.
- K4 (meter coverage): `logs/provider_usage.jsonl` meters only the routed provider-client
  path; the L0 router path writes `logs/usage.jsonl` only. ollama's true last-used is
  2026-09-28T21:44:22Z (L0 gemma:2b), not the metered seam's 2026-09-26T19:20:15Z. Also:
  `mag/cost_truth.py:172` records that coding-plan usage is not exposed in
  provider_usage.jsonl, so the z_ai lane counts understate harness-side use of the same keys.
- K5 (openai broken): last 21 metered openai rows (through 2026-08-28T23:31:41Z) all carry
  ok=false; the lane has not been retried since.
- K6 (log stray): `test_provider` appears in the log (30 rows, model test-model, last
  2026-08-05T01:28:16Z) but is not in providers.yaml; probe residue.

## Method (commands run)

1. Read `configs/providers.yaml` in full (40,258 bytes; 28 blocks counted by yaml parse:
   `PROVIDER_COUNT 28`).
2. `.venv/Scripts/python.exe C:/Users/foste/AppData/Local/Temp/f18_census.py` - parsed the
   yaml, folded 76,568 `provider_usage.jsonl` rows (0 bad), matched every `api_key_env` /
   `api_key_envs` name against .env names.
3. Folded `logs/usage.jsonl` (163,102 rows) by `meta.model` for L0-path last-used.
4. Dumped `logs/quota_state.json` per-provider last_ts/last_ok as cross-check (agrees with
   the jsonl fold on every provider it tracks).
5. Resolved keys live through `models.providers._key_env_names` + `provider_keys` after
   `models.env_load.load_dotenv(Path('.env'))` (counts only, values never printed).
6. Classified each key name as .env nonempty / EMPTY / absent plus Windows host-env presence.
