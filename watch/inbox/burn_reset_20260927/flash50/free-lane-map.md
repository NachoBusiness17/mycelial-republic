# FREE-LANE MAP - every provider, model, rate limit, auth mechanism, cost

Item s2-21, census of 2026-09-28 (snapshot moment ~23:20-23:40 UTC). Read-only census; no
lane was fired from this session. Every number below comes from a file read or a command run
during this ask, cited inline. No fabrication: anything I did not measure is labeled as a
recorded claim, not a live verdict.

Instruments run this session:
- `git grep` for LANES / stealth surfaces; Read of every file cited below
- `.venv/Scripts/python.exe -c ...` census scripts over `configs/providers.yaml`,
  `configs/keys.json`, `.env` (names only, never values), `state/fuel/*`
- `.venv/Scripts/python.exe -m mag.free_tier status` (live surface status, ok rates from
  fuel_feed's lane profile ledger)
- hermes `.env` read for variable NAMES only (`C:/Users/foste/AppData/Local/hermes/.env`)

---

## 1. The two named anchors

### 1.1 configs/providers.yaml (835 lines, 28 provider blocks, 62 model rows, 51 distinct model ids)

Census command: yaml.safe_load + per-block property scan (run this session). Headlines:

- 28 provider blocks. dormant: 5 (saelis, gemini, mistral, nvidia, cerebras). paid: 6
  (anthropic, deepseek, deepseek_overmind, gemini, openai, xai). free_local: 2 (ollama,
  mlx-cluster). `free: true` flag: 3 (z_ai2, z_ai3, z_ai4).
- 62 model rows, 51 distinct ids, 13 distinct `:free` ids (all under the openrouter and
  nous_api blocks).
- prefer_order (defaults block, providers.yaml:12-44): ollama, z_ai, openrouter, groq,
  together, github_models, moonshot, fireworks, cohere, hf_router, dashscope, deepseek,
  deepseek_overmind, anthropic, openai, xai. The 09-26 purge (B2-61/B2-36) removed nvidia,
  mistral, gemini, cerebras from every routing list; pick_provider does not read dormant,
  the lists are the enforcement point (providers.yaml:822-827).
- routing: 6 job classes (scut, recall, public_summarize, hard_code, hard_reason, default);
  only ollama+openrouter+groq appear in all the free positions (providers.yaml:828-835).
- Header law (providers.yaml:4-6): free tiers do NOT expose remaining-until-reset via API;
  Mag tracks usage against locally-set period+limits and refuses when empty. These guards
  are soft caps, not vendor denominators.

Per-block one-liners (id | base | auth env chain | models | Mag quota guard | state):

| id | base_url | api_key_env(s) | models | guard | state |
|---|---|---|---|---|---|
| saelis | SAELIS_BASE_URL env / 127.0.0.1:8080/v1 | null (default "saelis") | saelis | none | dormant (0 uses) |
| ollama | OLLAMA_HOST env / 127.0.0.1:11434/v1 | none (key ignored, sends "ollama") | gemma:2b, qwen-desk, qwen2.5:3b-instruct, qwen2.5-coder:7b, gemma4, gemma4-desk | none (unlimited local) | FREE, local, tier_max T1 |
| mlx-cluster | 127.0.0.1:7777/v1 | none | mlx-flagship (stub, machines not landed) | none | FREE local stub |
| nous | inference-api.nousresearch.com/v1 | HERMES_API_KEY_1, HERMES_API_KEY_2 | z-ai/glm-5.3-prime, qwen/qwen3.8-max-prime, fireworks/ember-1 | none tracked | FUNDED ($180 SDD credits); 200-verified on 5.3-prime 09-25 (providers.yaml:156) |
| nous_api | same host | same | stealth/space-bunny-alpha, ling-3.0-flash-sante:free, ling-3.0-flash-fin:free, meituan/longcat-2.0:free, poolside/laguna-s-2.1:free | none | stealth-window $0/$0 mirror (providers.yaml:240-258) |
| openrouter | openrouter.ai/api/v1 | OPENROUTER_API_KEY, OPENROUTER_API_KEY_2, OR_API_KEY, OR_API_KEY_2 | 14 rows: openrouter/auto + 13 :free ids (full list below) | monthly 200 calls / 500K tok | LIVE; 2 accounts (a1 funded nacho, a2 free fostertron/ox) |
| openai | api.openai.com/v1 | OPENAI_API_KEY | gpt-4o-mini, gpt-4o | monthly 100 / 200K | paid |
| anthropic | api.anthropic.com/v1 (anthropic_messages kind) | ANTHROPIC_API_KEY | claude-sonnet-4, claude-3-5-haiku | monthly 80 / 300K | paid, UNFUNDED per RIB_DRIVING_LADDER_20260928 |
| groq | api.groq.com/openai/v1 | GROQ_API_KEY, GROQ_API_KEY_2 | openai/gpt-oss-120b, qwen/qwen3.8-27b (+9 out_of_routing_scope ids) | daily 100 calls / 100K tok | FREE, LIVE |
| deepseek | api.deepseek.com/v1 | DEEPSEEK_API_KEY, DEEPSEEK_SWARM_API_KEY | deepseek-v4-flash, deepseek-v4-pro | daily 10K calls / 30M tok | paid workhorse (superseded as "funded" by the ladder RIB) |
| deepseek_overmind | api.deepseek.com/v1 | DEEPSEEK_OVERMIND_API_KEY | deepseek-v4-flash/pro | monthly unbounded | paid |
| vast | VAST_OPENAI_BASE_URL env | VAST_OPENAI_API_KEY | (model_env VAST_OPENAI_MODEL, default deepseek-v4-flash) | none (vendor balance) | paid rented GPU |
| gemini | generativelanguage.googleapis.com/v1beta/openai | GEMINI_API_KEY | (roster emptied B2-61) | daily 50 / 200K | dormant: generation 401-dead, key is a Vertex express key (B2-63, providers.yaml:458-472) |
| xai | api.x.ai/v1 | XAI_API_KEY, XAI_API_KEY_2, GROK_API_KEY, GROK_API_KEY_2 | grok-3-mini, grok-3, grok-4.5 | monthly 100 / 300K | paid |
| together | api.together.xyz/v1 | TOGETHER_API_KEY | deepseek-ai/DeepSeek-V4-Flash-0731 | monthly 100 / 200K | trial; B2-04 verified-live 3/3 (keys.json) |
| z_ai | api.z.ai/api/paas/v4 | ZAI_API_KEY | glm-4.7-flash | none block | opencode_only (raw-API 1305/1302 + fence risk) |
| z_ai2 | api.z.ai/api/coding/paas/v4 | ZAI_API_KEY_Pro | glm-4.7-flash, glm-5.3-flash | none block | free:true, funded Pro, retry_overload (B2-62) |
| z_ai3 | api.z.ai/api/coding/paas/v4 | ZAI_API_KEY_Lite | glm-4.7-flash, glm-5.3-flash | none block | free:true, Lite, METERED (see 4.3) |
| z_ai4 | api.z.ai/api/paas/v4 | ZAI_API_KEY_2 | glm-4.7-flash, glm-4.5-flash | monthly 5000 / 5M | coding-plan key #2, opencode_only |
| github_models | models.inference.ai.azure.com | GITHUB_MODELS_TOKEN | gpt-4o-mini, claude-3-5-sonnet, Meta-Llama-3.3-70B | daily 50 / 100K | free tier |
| mistral | api.mistral.ai/v1 | MISTRAL_API_KEY (env_2 exists) | mistral-small-latest | monthly 100 / 200K | dormant: x-ratelimit-limit-req-minute: 0 measured (B2-61) |
| moonshot | api.moonshot.ai/v1 | MOONSHOT_API_KEY | kimi-k2 | monthly 100 / 200K | trial |
| fireworks | api.fireworks.ai/inference/v1 | FIREWORKS_API_KEY | llama-v3p1-70b-instruct | monthly 100 / 200K | free tier (id flagged verify) |
| cerebras | api.cerebras.ai/v1 | CEREBRAS_API_KEY, CEREBAS_API_KEY | gpt-oss-120b, qwen-3.8-27b | monthly 100 / 200K | dormant: card-gated 30-day trial, chat 402 live (B2-36) |
| nvidia | integrate.api.nvidia.com/v1 | NVIDIA_API_KEY, NVIDIABuild-Autogen-46 | (roster purged B2-61) | monthly 100 / 200K | dormant: 410 EOL + 404 for-account |
| cohere | api.cohere.com | COHERE_API_KEY | command-r-plus | monthly 100 / 200K | trial |
| hf_router | router.huggingface.co/v1 | HF_TOKEN | Meta-Llama-3.3-70B-Instruct | monthly 100 / 200K | free, rate-limited |
| dashscope | dashscope.aliyuncs.com/compatible-mode/v1 | DASHSCOPE_API_KEY | qwen-max | monthly 100 / 200K | trial (phone-verified acct) |

The 13 distinct `:free` ids in the yaml: cohere/north-mini-code:free,
dots-studio/dots-3-note-preview:free, inclusionai/ling-3.0-flash-fin:free,
inclusionai/ling-3.0-flash-sante:free, liquid/lfm-2.5-2.6b:free,
meituan/longcat-2.0:free, nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free,
nvidia/nemotron-3-super-120b-a12b:free, nvidia/nemotron-3-ultra-550b-a55b:free,
nvidia/nemotron-3.5-content-safety:free, nvidia/nemotron-3.5-lightning:free,
poolside/laguna-s-2.1:free, poolside/laguna-xs-2.1:free. Each earned its line through a
live chat gate (B2-295 + B2-202, byte evidence
watch/inbox/burn_wave_20260926/B2_295_gate_results2.json and B2_202_gate_results.json).
Gate-FAILED and therefore NOT listed: qwen/qwen3.8-27b:free and google/gemma-4-31b-it:free
and google/gemma-4-26b-a4b-it:free (429 upstream shared pool), thinkingmachines/inkling-small:free
and thinkingmachines/inkling:free (403 agents-only) (providers.yaml:202-206).
stealth/space-bunny-alpha is FREE but not `:free`-suffixed: 1M ctx, text+image+video->text,
mandatory reasoning, expires when the stealth drop ends (providers.yaml:181).

### 1.2 The stealth driver LANES table (tools/stealth_driver.py:205-251, `_work_lanes`)

"THE LADDER" (operator-corrected 2026-09-28): free tiers are the default; judgment and
scarce5 are the climb. 9 lanes when every key is present, round-robin with 30-minute
per-lane spacing (stealth_driver.py:340), budget 4000 tokens with one 4x retry when
finish=length + reasoning present (stealth_driver.py:147-148, 415-421), every lane stamped
with a reasoning-effort policy: free=low, judgment/scarce5=max (stealth_driver.py:161-165);
wire knobs: openrouter takes `reasoning.effort`, nous takes top-level `reasoning_effort`
(stealth_driver.py:163-165); hermes (headless CLI) and llm7 (non-reasoning model) carry the
config value but get no wire knob.

| # | family | key source | tier | model | base |
|---|---|---|---|---|---|
| 0 | hermes | headless (hermes_cli.main -z, 600s timeout, stealth_driver.py:254-282) | free | ling-3.0-flash-sante:free (via nous) | subprocess, no wire API |
| 1 | openrouter | OPENROUTER_API_KEY (a1, funded) | free | stealth/space-bunny-alpha | openrouter.ai/api/v1/chat/completions |
| 2 | openrouter | OPENROUTER_API_KEY_2 (a2, free acct) | free | inclusionai/ling-3.0-flash-sante:free | same |
| 3 | openrouter | OPENROUTER_API_KEY_2 | free | meta/muse-glimmer-30b | same |
| 4 | openrouter | OPENROUTER_API_KEY_2 | free | thinkingmachines/inkling-small:free | same |
| 5 | llm7 | NONE - anonymous (Bearer header omitted) | free | gpt-4o-mini | api.llm7.io/v1/chat/completions |
| 6 | openrouter | OPENROUTER_API_KEY | judgment | anthropic/claude-opus-5.5 | same |
| 7 | openrouter | OPENROUTER_API_KEY_2 | judgment | openai/gpt-6-astra | same |
| 8 | nous | NOUS_SDD_API_KEY from hermes .env (stealth_driver.py:192-202) | scarce5 | z-ai/glm-5.3-prime | inference-api.nousresearch.com/v1/chat/completions |

POST boundary (stealth_driver.py:495-503): work dispatches may only hit exactly three
bases (openrouter, nous, llm7). GET boundary (stealth_driver.py:74-79): exactly four URLs
(the three /models rosters + the fixed loopback llama-server health probe), redirects
disabled, hosts must resolve public IPs.

Work flow observed live: `state/fuel/stealth_work_state.json` lane bookkeeping +
`state/fuel/stealth_work_queue.jsonl` 13 rows (12 pending, 1 sensed, all tier=free) +
`watch/inbox/STEALTH_MINED_FINDINGS.jsonl` 151 mined rows (openrouter 80, hermes 36,
nous 22, stealth-fanout-wave2 10, operator-image-drop 3). Every dispatch is banked with
lane+model provenance and rides the no-fabrication/no-em-dash laws inside the ask
(stealth_driver.py:128-129); a free-lane answer is SENSED, never DONE, until the funded
tier verifies (stealth_driver.py:486-492).

---

## 2. Every other lane table in the estate (all gated by the dormant flag)

`mag/dormant.py` is the ONE reader of `dormant: true` in providers.yaml; a dormant
provider id (or base_url host) drops out of every hardcoded list with no code edit
(mag/dormant.py:43-84). Currently gated out everywhere: cerebras, nvidia, mistral (host),
gemini, saelis.

| table | file:line | declared | live post-gate | members |
|---|---|---|---|---|
| fuel_feed FREE_LANES | mag/fuel_feed.py:52-111 | 7 | 5 | ox, openrouter-a1, openrouter-a2, groq, z_ai3 (nvidia + cerebras gated out) |
| STRONG/FAST/CACHE split | mag/fuel_feed.py:119-123 | - | - | STRONG: ox, a1, a2; FAST: groq; CACHE: z_ai3; entropy >= 0.5 routes hard signals to STRONG |
| fuel_feed LANE_MAX_TOKENS | mag/fuel_feed.py:134-135 | 6 | - | ox 5000, nvidia 2200, a1 5000, a2 5000, z_ai2 2000, z_ai3 2000 (reasoning models eat small budgets empty) |
| free_tier FREE_SURFACES | mag/free_tier.py:51-104 | 12 | 10 | z_ai3, groq, openrouter-a1, openrouter-a2, ox, together, ollama, coding_plan, grok_free, nous (cerebras + nvidia gated out) |
| stealth_fanout LANES | tools/stealth_fanout.py:37-56 | 10 | 10 (env-gated) | OR1 stealth/space-bunny-alpha; OR2 ling-sante:free, meta/muse-spark-1.3, meta/muse-spark-1.2, meta/muse-glimmer-30b, inclusionai/ling-3.0-flash-vl, thinkingmachines/inkling-small:free; N1 z-ai/glm-5.3-prime; N2 qwen/qwen3.8-max-prime; llm7 gpt-4o-mini anon |
| quorum_window FREE_LANES | mag/quorum_window.py:60-73 | 4 | 2 | groq, openrouter/auto (nvidia + cerebras gated out) |
| lane_salon WITNESSES | mag/lane_salon.py:47-63 | 7 | 5 | grok-tandem (CLI, $0), openrouter/auto, groq, together (paid), deepseek-pro (paid) |
| research_fanout LANES | mag/research_fanout.py:122-170 | 12 | 8 | groq-qwen, groq-oss, groq-oss20, zai-lite (ZAI_API_KEY_Lite glm-5.3-flash on /api/coding/paas/v4), or-union-alpha, or-glm52, or-nemotron, or-ling3 (cerebras + mistral hosts gated out) |
| rotation_harness LANES | mag/rotation_harness.py:28-35 | 2 | 1 | groq (cerebras gated out) |
| lane_probe LANES | mag/lane_probe.py:22-44 | 3 | 3 | deepseek, zai (glm-4.5-flash), groq (gpt-oss-20b); keys read from .env for headers only, never logged |

---

## 3. Rate limits (external vendor denominators vs the estate's own guards)

### 3.1 OpenRouter
- Recorded free capacity: "18 lanes x 1000/day (the big free capacity)" (providers.yaml:17);
  RIB_FREE_USAGE_POLICY_20260823: "~18 lanes x 2 accounts, ~144 reliable parallel agents
  max". These are recorded planning numbers, not re-measured this session.
- Estate guard: monthly 200 calls / 500K tokens per the quota block (providers.yaml:227-232);
  dashboard is declared source of truth.
- Live catalog measured by the driver roster probe 2026-09-28T23:19:58Z (configs/mirrors.json,
  cross-checked in heartbeat cycle 62): GET /api/v1/models = 460 models.
- Known per-model failure modes, byte-recorded: `:free` ids 429 with
  `limit_source upstream_provider_shared_pool` (qwen3.8-27b, gemma-4s); inkling ids 403
  agents-only; stealth/ox-alpha 429 upstream (free_tier.py:75, ok_rate 0.613).
- Measured openrouter/auto behavior: routes to reasoning models, ignores
  thinking:disabled, eats small budgets (600 -> empty, 2000 -> content) - hence 5000-token
  lanes (providers.yaml:219-223, fuel_feed.py:127-135).

### 3.2 Groq
- External denominator: 1K RPD / 200K TPD PER text model (LINKS EPNEWS-GROQ-RPD-CONFIRMED,
  cited at providers.yaml:309-310 and 336-347).
- Estate guard binds first: provider-level daily 100 calls / 100K tokens, so total pull is
  capped at 100K tok/day regardless of per-model buckets (providers.yaml:342-344). This is
  why a third chat lane was DECISION-skipped (B2-114).
- Live roster 09-26: 11 ids (B2-35); 2 in routing (gpt-oss-120b, qwen3.8-27b), 9 registered
  out_of_routing_scope (ASR/TTS/guard models/allam/gpt-oss-20b/safeguard-20b)
  (providers.yaml:323-352).
- Driver roster probe reads groq /models with `Authorization: Bearer GROQ_API_KEY` because
  /models 403s anonymous (stealth_driver.py:583-589); the driver's env did not resolve the
  key at cycle 62, so mirrors.json records groq "unreachable" (HTTP 403) - a probe-env
  artifact, NOT a lane outage: the lane itself measured ok_rate 0.891 in free_tier status.

### 3.3 z.ai (the z_ai* family)
- Endpoint law: coding-plan keys fake-1113 "insufficient balance" on raw /api/paas/v4; the
  real path is /api/coding/paas/v4 (providers.yaml:549-552, research_fanout.py:128-134).
- 429 overload family: code 1305/1302; measured ~1-in-3 at 6s spacing on Pro
  (providers.yaml:556-558, docs/ref/ZAI_API_EXPERT_REFERENCE.md:98-107); retry_overload
  backs off 15s then 30s.
- Published plan denominators (operator paste receipted 09-04, ZAI ref doc:224-225, 31-36):
  Lite 2,000 credits/5h rolling + 10,000/week ($18/mo); Pro 12,000/60,000 (~$60/mo); Max
  28,000/140,000 (~$120/mo). Credit formula (input x in_mult + cached x cache_mult + output
  x out_mult)/10,000; GLM-5.3 multipliers 6.9/1.7/24, Flash 2.3/0.56/8; MCP calls x1.2;
  off-peak 50% credit rate (peak = Mon-Fri 14:00-18:00 SGT).
- Measured Lite truth: METERED, ~53K tokens per credit (TOK_PER_CREDIT, mag/lite_guard.py),
  empirically >= 50 in-flight on glm-5.3-flash (ZAI ref doc:393-395); fleet pacing ceiling
  1,400 credits/day (DEFAULT_CEILING, mag/lite_guard.py law 15), env LITE_DAILY_CREDITS=0
  disables. Ledger state/fuel/lite_pacing.jsonl: 137 rows, last row today 23:36Z (door
  research_fanout, 159 tokens) - the guard is live and writing.
- API-balance concurrency table (NOT applicable to the package keys, ZAI ref doc:207-221,
  393-404): glm-5.3-flash 50, glm-4.7-flash 1, glm-4.5-flash 2, glm-5.3 5, glm-4.7-flashx 3.
- glm-4.7-flash and glm-4.5-flash are FREE at all tiers (providers.yaml:597-603,
  configs/cost_rates.yaml free: true rows); glm-4.7-flashx + glm-4.7 are PAID and not
  wired into free lanes.

### 3.4 Nous / Hermes
- Funded rung: $180 Nous credits is the ONLY funded tier (RIB_DRIVING_LADDER_20260928,
  invariant 1); glm-5.3-prime + qwen3.8-max-prime are the workhorse+judgment models; the
  Anthropic keys in .env are UNFUNDED (no Opus rung).
- Auth: HERMES_API_KEY_1/2 static keys (Portal OAuth path blocked on operator login,
  free_tier.py:91-93); the driver's scarce5 lane reads NOUS_SDD_API_KEY from
  C:/Users/foste/AppData/Local/hermes/.env (stealth_driver.py:192-202) - both
  NOUS_SDD_API_KEY and NOUS_NACHO_API_KEY confirmed present by name in that file this
  session (values never read).
- Catalog: "417-model OpenRouter-compatible catalog" measured 09-24 via mag.probe_route
  (providers.yaml:240-244); keys.json hermes_1 role string says "mirror_catalog_415_models".
  Two recorded counts, not re-measured this session; treated here as one same-day-class
  measurement with a 2-model drift between recordings.
- Failure mode observed live: nous:3 lane error "HTTPError: HTTP Error 402: Payment
  Required" in state/fuel/stealth_work_state.json - a Nous key ran dry of credits.
- Mag quota block: none tracked (providers.yaml:165-168).

### 3.5 LLM7 (the anonymous lane)
- No key, no auth; Bearer header omitted entirely (tools/stealth_fanout.py:114-116).
- Live roster measured today: 64 models (mirrors.json + heartbeat cycle 62).
- Failure observed live: llm7:5 "HTTPError: HTTP Error 400: Bad Request" on a gpt-4o-mini
  dispatch (stealth_work_state.json). LLM7 appears in NO providers.yaml block - it exists
  only in the stealth tooling (stealth_driver.py:232-234, stealth_fanout.py:54-56).

### 3.6 The dormant four (causes, all live-measured per B2-61/B2-36/B2-63)
- nvidia: default id 410 EOL 2026-09-21; listed ids 404 for-account; roster purged, no ids
  until re-verified live.
- mistral: chat 429 with x-ratelimit-limit-req-minute: 0 (code 1300); large-latest 403
  tier_not_allowed and catalog-absent (46-id catalog, B2-61).
- gemini: the on-file key is a Vertex express key; generativelanguage 401s generation in
  every carriage; live catalog (61 ids) contains none of the yaml ids; auth shape PROVEN on
  aiplatform (x-goog-api-key + ?key= both authenticate, 403 PERMISSION_DENIED = API not
  enabled). Operator GO paths (a) enable aiplatform on project 1055073037365 + native lane
  kind, or (b) mint an AI Studio AIza key (providers.yaml:458-486).
- cerebras: card-gated 30-day trial, NOT a free lane; $5 credits expire 30 days after card
  attach; chat 402 no-credit live; trial denominators 5 RPM / 90K total TPM / 1M TPD, no
  RPD; live catalog collapsed to 2 ids (gpt-oss-120b, qwen-3.8-27b) (providers.yaml:701-734).
  Operator GO surfaced in queue/todo.md, deadline 2026-10-03.

### 3.7 Local (the true $0 tiers)
- ollama: quota period none (unlimited), 6 models, tier_max T1, 90s timeout (providers.yaml:90-126).
- mlx-cluster: 4x Mac Studio stub, endpoint does not exist until the machines land (providers.yaml:128-148).

---

## 4. Auth mechanisms (what was actually read in code)

1. **Bearer + env var chains** (the default, models/env + per-provider api_key_envs).
   35 api_key env names are declared across providers.yaml; 16 of them are ABSENT from
   .env (checked by name this session): CEREBRAS_API_KEY, COHERE_API_KEY,
   DASHSCOPE_API_KEY, DEEPSEEK_OVERMIND_API_KEY, DEEPSEEK_SWARM_API_KEY,
   FIREWORKS_API_KEY, GITHUB_MODELS_TOKEN, HF_TOKEN, MOONSHOT_API_KEY,
   NVIDIABuild-Autogen-46, NVIDIA_API_KEY, OR_API_KEY, OR_API_KEY_2, VAST_OPENAI_API_KEY,
   XAI_API_KEY, XAI_API_KEY_2. Name-drift cases with substitutes in .env under other
   names: cohere (env has COHERE_API_KEY_FREE/_PAID), xai (env has GROK_API_KEY/_2 +
   XAI_SD_API_KEY), vast (env has VASTAI_API_KEY), nvidia (env has NVIDIABuild +
   NVIDIABuild2, registered in keys.json but in NEITHER yaml env chain), cerebras (env has
   the typo spelling CEREBAS_API_KEY/_2 which the yaml does read via api_key_envs).
   .env holds 54 variable names total (names-only scan).
2. **Anonymous** (no credential): llm7 (Bearer omitted), ollama (ignores keys, sends
   "ollama"), mlx-cluster (none).
3. **Headless CLI seats** (no wire auth): Hermes via
   `[python, -m, hermes_cli.main, -z, ask]` with CREATE_NO_WINDOW on win32
   (stealth_driver.py:272-278); Grok subscription CLI seats at ~/.grok and ~/.grok-sd
   (keys.json grok_cli, env field "NONE_USES_CLI_SEATS"); opencode seats (OPENCODE /
   OPENCODE2 env presence, keys.json).
4. **Key law** (configs/keys.json:2, KEY LAW 2026-09-23): one key, one canonical name,
   declared once, readers use mag.key_law.get(name); 32 entries registered with roles and
   live status strings (nvidia/mistral/cerebras entries carry their dormancy receipts
   inline).
5. **Extra headers**: OpenRouter calls carry HTTP-Referer http://127.0.0.1:8765 and
   X-Title "Mag Resource Harness" (providers.yaml:224-226).
6. **Google express key**: authenticates via x-goog-api-key header AND ?key= param on
   aiplatform.googleapis.com, 403s on the un-enabled API (B2-63 bytes,
   providers.yaml:458-472) - auth shape proven, API enablement owed.
7. **SSRF boundaries** (Mimosa-guarded): stealth_driver GET allowlist = exactly 4 URLs,
   POST allowlist = exactly 3 chat-completions bases, scheme + public-IP resolution +
   no-redirect checks (stealth_driver.py:86-111, 495-513); stealth_fanout same pattern
   (stealth_fanout.py:73-99); lite_guard's monitor reads https-only + public-IP
   (mag/lite_guard.py:62-79).
8. **z.ai monitor side-door**: undocumented GET endpoints
   api.z.ai/api/monitor/usage/quota/limit (+ model-usage, tool-usage, subscription/list)
   read with just the Lite key, no browser, verified live 09-05 (mag/lite_guard.py:36-45).

---

## 5. Costs

| surface | cost | evidence |
|---|---|---|
| ollama (local) | $0 marginal (electricity unmeasured) | configs/cost_rates.yaml seats.ollama, cost_truth notes |
| OpenRouter `:free` ids | $0 (free_or_quota pricing state) | mag/cost_truth.py:157-158 |
| OpenRouter stealth/space-bunny-alpha | $0/$0 during stealth window, expires when stealth ends | providers.yaml:181, 241-244 |
| llm7 anonymous | free (unpriced in the rate table; no meter anywhere) | absence in cost_rates.yaml + configs |
| groq free tier | $0 within denominators; cost_truth keeps groq in _PROVIDER_FREE_OR_CREDIT (post-gate set = {groq, together}) | mag/cost_truth.py:40-51 |
| glm-4.7-flash, glm-4.5-flash (API balance) | free: true in the canonical rate table | configs/cost_rates.yaml |
| z.ai coding-plan usage | NOT API-priced: cost_truth returns state "unpriced / zai_coding_plan_not_metered"; plan seats are subscriptions, tracked separately (Lite $18/mo, Pro ~$60/mo, Max ~$120/mo) | cost_truth.py:165-173, ZAI ref doc:31-36 |
| z_ai3 Lite fleet ceiling | 1,400 credits/day of a 10,000/wk pool, ~53K tok/credit | mag/lite_guard.py |
| Nous | $180 funded credits remaining (the ONLY funded tier); :free-tagged mirror ids $0 during stealth | RIB_DRIVING_LADDER_20260928; providers.yaml:258 |
| Grok CLI seats | $0 marginal (subscription seats, not API-billed) | keys.json grok_cli |
| deepseek (reference, paid) | v4-flash offpeak 0.007 hit / 0.22 miss / 0.66 out per M, peak 2x; v4-pro 0.022/0.66/1.98 offpeak | configs/cost_rates.yaml |
| glm-5.3-flash (API balance, reference) | 0.015 hit / 0.075 miss / 0.25 out per M (50% promo ended Sep 9 2026; list 0.15/0.03/0.50) | configs/cost_rates.yaml, ZAI ref doc:22 |
| grok-4.5 (reference, paid) | 0.3 / 2.0 / 6.0 per M | configs/cost_rates.yaml |
| cerebras | $5 trial credits, expire 30 days after card attach; lane dormant | providers.yaml:706-712 |

Cost doctrine (mag/cost_truth.py): billable volume = cache-miss input + output; dollar
figures are labeled calculated_api_cost_usd, never "actual"; unpriced rows stay visible so
missing instrumentation cannot masquerade as free.

---

## 6. Live state measured this session

- `.venv/Scripts/python.exe -m mag.free_tier status` returned ok=true, 10 surfaces
  (post-dormant-gate), every listed key present. Telemetry from the fuel_feed lane profile:
  groq ok_rate 0.891, openrouter-a1 0.618, openrouter-a2 0.333, ox 0.613, z_ai3 0.0
  (read timeouts), together 0.0 (its fail hints are "missing API key (TOGETHER_API_KEY)"
  history rows even though the key is present in .env today - the profile ledger is
  historical). ollama/coding_plan/grok_free/nous: no telemetry (ok_rate null).
- Driver heartbeat state/fuel/stealth_driver.jsonl: 7 rows, latest cycle 62 at
  2026-09-28T23:25:06Z. Roster: openrouter=460, llm7=64, groq=ERR(403). Work topic in that
  cycle: "ERR openrouter/thinkingmachines/inkling-small:free: HTTP Error 403: Forbidden".
  cache_stats tail shows live dispatches: stealth/space-bunny-alpha prompt 293 tok with
  ~149-152 cached (roughly half the preamble cache-hits), ling-sante 165/0 cached,
  muse-glimmer-194/64, hermes rows carry null usage (headless CLI reports none).
- configs/mirrors.json (driver-maintained): ts 2026-09-28T23:19:58Z, groq unreachable
  stable, llm7 64 stable, openrouter 460 stable.
- stealth_work_state.json lane_errors: nous:3 402 Payment Required, nous:4 read timeout,
  llm7:5 400 Bad Request, openrouter:4 403 Forbidden, openrouter:1 empty-content
  (provider returned an empty response). These five errors are the live map of where the
  free lanes are actually breaking today.
- The queue's tier distribution is 100% free (13/13 rows) - the judgment/scarce5 rungs
  exist in code but nothing has been dispatched at those tiers yet (no row carries a
  non-free tier).

---

## 7. Cross-reference findings (yaml vs the stealth LANES table vs live bytes)

1. **inkling-small:free is a known-dead lane still in the driver's ladder.**
   providers.yaml:204-206 records the 403 agents-only gate FAIL (B2-202); the driver still
   builds the lane (stealth_driver.py:229-231) and heartbeat cycle 62 shows it failing 403
   again today. The driver rotates into a lane the yaml roster explicitly refuses.
2. **Five driver/fanout models are unregistered in providers.yaml**: meta/muse-glimmer-30b,
   meta/muse-spark-1.2, meta/muse-spark-1.3, inclusionai/ling-3.0-flash-vl, llm7's
   gpt-4o-mini. The yaml's own law (providers.yaml:203: "catalog-present but gate-FAILED,
   no line until they pass") implies registration-earned-lines; these five have no yaml
   line and no gate receipt cited anywhere in the yaml. muse-glimmer-30b IS dispatching
   successfully today (cache_stats rows with finish=stop), so the gap is real in both
   directions.
3. **The judgment rung is yaml-invisible**: anthropic/claude-opus-5.5 and openai/gpt-6-astra
   ride the funded OpenRouter account in the driver ladder but appear in no providers.yaml
   block (yaml's anthropic/openai blocks list older API ids and are PAID-deferred lanes).
4. **z_ai3's free:true flag is half-true**: the Lite package is METERED (2,000/5h +
   10,000/wk real credits, proven 09-05); fuel_feed.py:78-81 and mag/lite_guard.py carry the
   correction, but providers.yaml:569 still declares `free: true` with no meter pointer.
5. **nvidia's yaml env chain matches zero .env names**: yaml reads NVIDIA_API_KEY +
   NVIDIABuild-Autogen-46 (providers.yaml:743); .env holds NVIDIABuild + NVIDIABuild2
   (registered in keys.json only). The lane is dormant so nothing dials it, but an operator
   GO would first 404 on the key chain itself.
6. **Lane-state index drift**: state/fuel/stealth_work_state.json last_lane_ts keys
   (nous:1..4, openrouter:0..4) reference a superseded lane ordering; the current ladder
   has exactly one nous lane at index 8. The 30-minute spacing gate reads stale indexes,
   so per-lane spacing against moved lanes resets silently.
7. **groq "unreachable" in mirrors.json is a probe-env artifact, not a lane outage** (the
   driver's env did not resolve GROQ_API_KEY for the /models GET; the lane itself is the
   most reliable surface at ok_rate 0.891).
8. **Nous catalog count drifted between recordings**: 417 (providers.yaml:241, 09-24) vs
   415 (keys.json hermes_1 role string). Not re-measured here; flagging the drift, not
   adjudicating it.
9. **free_tier.py's nvidia model list is stale** (z-ai/glm-5.3-flash,
   deepseek-ai/deepseek-v4.1-flash, free_tier.py:64) against the yaml's purged roster
   (providers.yaml models: [] per B2-61); dormant-gating keeps it inert either way.

---

## 8. Limits of this census

- No live API call was fired from this session to any provider: all vendor-side numbers are
  (a) recorded receipts in the repo (dated, cited) or (b) today's driver-heartbeat
  measurements read from disk. The "460 / 64 models" roster counts are the driver's
  measurement from 23:19-23:25Z today, not mine.
- External vendor denominators (OpenRouter per-lane daily caps, groq 1K RPD/200K TPD,
  cerebras trial caps, z.ai plan credits) are quoted from repo receipts and the operator's
  verbatim paste (ZAI ref doc), never re-verified against the vendors from here.
- .env and hermes .env were read as NAMES only; no key value was printed, logged, or
  banked anywhere in this file.
- The 2,303-test suite was not run; this is a file-and-ledger census, not a test run.
