# DEEPSEEK API DOSSIER - full surface vs what the estate actually uses

**Schema:** wiring.dossier.deepseek_api.v1 - **ts:** 2026-10-02T00:30Z - **lane:** API-1 DEEPSEEK DEEP DIVE (ZCode subagent)
**Method:** official docs read at api-docs.deepseek.com (2026-10-02, cited per row) + live probes against
api.deepseek.com (receipts: `watch/inbox/model_garden/deepseek_api_probe/probe_receipts.jsonl`,
instrument `probe.py` same dir). Probe spend **$0.000937 of the $0.50 budget** (5 calls, all 200).
**Local usage diffed:** `tools/ds_workhorse.py`, `tools/model_garden.py`, `memory/runs/hermes_burn/usage.jsonl`
(zero deepseek rows: that ledger is the Nous/Anthropic lane), `memory/runs/model_garden/usage.jsonl`
(67 deepseek rows, the real lane ledger), `configs/cost_rates.yaml`.

---

## 1. The full surface (cited)

### 1.1 Endpoints [api-docs.deepseek.com/ sidebar + /api/create-chat-completion]

| Endpoint | Path | Status | Estate uses it |
|---|---|---|---|
| Chat Completions | POST `/chat/completions` (base `https://api.deepseek.com`, OpenAI-compatible) | GA | YES (the only production path) |
| Responses API | POST `/responses` (OpenAI Responses format, stateless) | GA | no |
| FIM Completion | POST `/beta/completions` (base_url must be `https://api.deepseek.com/beta`) | Beta | no (probe only, P4) |
| List Models | GET `/models` | GA | no (probe only, P0) |
| Get User Balance | GET `/user/balance` | GA | no (probe only, P1) |
| Files API | POST `/api-file` family: upload / list / retrieve / delete | GA | no |
| Anthropic format | base `https://api.deepseek.com/anthropic`, `/messages` | GA | no |

No batch/discounted-batch endpoint exists anywhere in the current docs (sidebar checked 2026-10-02).
The width multiplier is the concurrency limit (section 1.5), not a batch API.

### 1.2 Models + exact ids [pricing page + /api/list-models + /updates changelog]

| id | version | context | max out | modalities | effort levels (default) | concurrency |
|---|---|---|---|---|---|---|
| `deepseek-flash` | DeepSeek-V4.1-Flash (2026-09-10) | 1,048,576 | 393,216 (384K) | text+image in, text out | low/high/max (high) | 2500 |
| `deepseek-v4-pro` | DeepSeek-V4-Pro-0813 | 1,048,576 | 393,216 | text only | low/high/max (high) | 500 |

- Legacy `deepseek-v4-flash` and `deepseek-v4-flash-vision-exp` still resolve but are retired; served by Flash at Flash price [pricing page].
- **`deepseek-chat` / `deepseek-reasoner` were discontinued by 2026-07-24** with a "temporary" mapping to V4-Flash non-thinking/thinking [changelog 2026-04-24]. They still work today (our ledger rows 2026-10-01T23:00Z) and are **absent from GET /models** (probe P0 lists exactly two ids). This is an unmapped removal risk on the estate's primary cheap lane.

### 1.3 Pricing (USD per 1M tokens) [pricing page, verified 2026-10-02]

| model | input cache hit off/peak | input cache miss off/peak | output off/peak |
|---|---|---|---|
| `deepseek-flash` | $0.003 / $0.006 | $0.15 / $0.30 | $0.60 / $1.20 |
| `deepseek-v4-pro` | $0.022 / $0.044 | $0.66 / $1.32 | $1.98 / $3.96 |

- **Peak windows: Mon-Fri 01:00-04:00 and 06:00-10:00 UTC, excluding Chinese public holidays. Everything else is offpeak at exactly half price** (weekends always offpeak). Price cut with the V4.1-Flash release 2026-09-10.
- Cache-hit input is **0.6% of miss input** (50x discount, both windows).
- The estate's three local price tables are ALL stale relative to this page:
  - `tools/ds_workhorse.py:67-68` $0.27/$1.10 (flat, no cache split, no windows)
  - `tools/model_garden.py:90` $0.44/$1.32 "flash PEAK" (actually cost_rates.yaml's inverted-window "peak")
  - `configs/cost_rates.yaml:9-15` flash offpeak miss $0.22 / peak miss $0.44 with the window comment INVERTED (it calls 01:00-04:00 + 06:00-10:00 UTC "the official schedule" for offpeak; the official page calls those PEAK)
  - `tools/tier_probe.py:21-22` hit $0.0028 / miss $0.14 / out $0.28 (a fourth, older sheet)

### 1.4 Context caching (on by default) [guides/kv_cache + api/create-chat-completion]

- Disk-based, **enabled by default, zero code changes to benefit** on the bill; the API metering is where we lose the visibility.
- Hit rules: prefixes persist as complete units at (1) request boundaries (end of user input + end of model output), (2) common-prefix detection across requests, (3) fixed token intervals for long inputs.
- **Usage signals (exact fields):** `usage.prompt_cache_hit_tokens`, `usage.prompt_cache_miss_tokens`, and `usage.prompt_tokens_details.cached_tokens` (same value). Confirmed live in probes P2/P3/P4.
- Best-effort; unused caches clear in "hours to days". No storage fee, no minimum documented (our probe measured the effective unit: see section 3).
- `user_id` param isolates KVCache, safety, and scheduling per end user [rate_limit page].

### 1.5 Rate limits [quick_start/rate_limit]

- **Concurrency-based, not RPM/TPM**: flash 2500, pro 500 concurrent per account (any key). 429 on breach. Expansion free via Feishu form.
- Keep-alive: non-streaming emits empty lines, streaming SSE comments; server drops requests not started within 10 minutes.
- Error ladder [error_codes]: 400 invalid format, 401 auth, 402 insufficient balance, 422 invalid params, 429 rate limit, 500 server, 503 overloaded (retry short-wait on 429/500/503).

### 1.6 Thinking control per surface [guides/thinking_mode]

| surface | toggle | effort |
|---|---|---|
| OpenAI format (`/chat/completions`) | `thinking: {type: enabled|disabled}` (default **enabled**) | `reasoning_effort: none/low/high/max` (default high) |
| Anthropic format | `reasoning: {effort: none|low|high|max}` (none disables) | same object |
| Responses API | `reasoning.effort` | `output_config.effort` |

- Thinking ON: `temperature`/`frequency_penalty`/`presence_penalty` silently ignored; `top_p` clamped 0.95-1.0; chain-of-thought in `message.reasoning_content` (billed as output); with `tools` present, prior turns' `reasoning_content` MUST be sent back (400 otherwise). `tool_choice` required/named unsupported in thinking mode.
- `max_tokens` defaults: 8K non-thinking, 64K thinking (128K at max effort). Range 1-384K.

### 1.7 Structured output + tools [guides/json_mode + guides/tool_calls + api/create-chat-completion]

- JSON mode: `response_format: {type: json_object}`; prompt must contain the word "json" + a format sample; set `max_tokens` to avoid mid-JSON truncation; occasional empty content documented (retry).
- Tool calls: OpenAI `tools`/`tool_choice` shape; results returned as `message.tool_calls[]` then fed back as `role: tool` messages; strict JSON-schema mode (Beta): `strict: true` per function + base_url `.../beta` + `additionalProperties: false` + all properties in `required`; supports $ref/$defs, enum, anyOf; validates server-side.
- Responses API additionally offers `text.format: json_schema` (schema-enforced output, no tools needed).

### 1.8 FIM + prefix completion + vision + files [api/create-completion + guides]

- FIM (Beta): POST `/beta/completions`, params `prompt` + `suffix` (+ max_tokens, stop<=16, stream, echo, logprobs<=20). Non-thinking only per pricing-page feature note. `frequency_penalty`/`presence_penalty` deprecated (no effect).
- Chat Prefix Completion (Beta): `prefix: true` on an assistant message (base_url `.../beta`) forces the model to continue from given partial content; `reasoning_content` can be passed in as input.
- Vision (Flash only): JPEG/PNG/GIF/WebP via base64 data-URL (<=48 MiB body), public URL (<=32 MiB, 60s), or Files API `file_id` (<=64 MiB); ~1024 tokens per image after resize; user-role messages only.
- Files API: upload/list/retrieve/delete, `file-api-...` ids, reusable across requests.

### 1.9 Streaming

- SSE, terminated by `data: [DONE]`; `stream_options.include_usage` puts the full usage (cache split included, confirmed by the FIM reference) on the final chunk. The estate fires non-streaming only, which is correct for file-backed batches.

---

## 2. We-use vs we-waste (the diff)

**What we send today** (`tools/ds_workhorse.py:48-57`, `tools/model_garden.py:164-169`): one POST to
`/chat/completions` (or `/v1/chat/completions` via the garden rail), body `{model, messages, max_tokens,
temperature, stream:false}` (+ optional extra_body from the budget recipe). Model id `deepseek-chat`
(legacy mapping) everywhere except `tools/research_mine.py` which already says `deepseek-flash`.

**What we read back** (`ds_workhorse.py:63-68`, `model_garden.py:356-393`): `choices[0].message.content`,
fallback `message.reasoning_content`, `usage.prompt_tokens`, `usage.completion_tokens`,
`usage.completion_tokens_details.reasoning_tokens`. **ds_workhorse persists NO usage tokens at all** -
only its own estimated cost (chan-x4 ledger rows carry `"tokens not reported by lane"`).

| # | Capability | Status in estate | Cost of ignoring it |
|---|---|---|---|
| 1 | `prompt_cache_hit_tokens` / `prompt_cache_miss_tokens` | read only by probes (`tools/tier_probe.py:179-184`, `tools/cache_kpi.py`); production lanes blind | ledger overstates real spend ~2.7x (see math below); retries/revision turns already ride hit price invisibly |
| 2 | Offpeak windows (half price outside Mon-Fri 01-04/06-10 UTC) | unknown to metering; not used for scheduling | every peak-hour fire pays 2x for nothing |
| 3 | Canonical model id `deepseek-flash` + explicit `thinking disabled` | `deepseek-chat` legacy alias | standing outage risk: alias discontinued-by date already passed, id absent from /models |
| 4 | GET `/user/balance` (free) | never called | no live spend meter; $47.54 sat on the account unread until probe P1 |
| 5 | JSON output mode | never in production (DOLLAR_BURN aggregate parses 3-line text verdicts by regex; 6 self-contradictory verdicts had to be hand-discounted) | verdict-parse fragility + the empty-output retry class |
| 6 | Concurrency 2500 (flash) | ds_workhorse fires strictly serial, ~4 files/s observed 19:18-19:21 UTC | wall-time only; width is free for the taking |
| 7 | Tool calling + strict schema mode | unused | structured adjudication without regex parsing |
| 8 | FIM `/beta/completions` | unused (works, probe P4) | mid-file code edits pay full-context chat prices |
| 9 | Responses API (`/responses`, json_schema, reasoning.effort none) | unused | n/a today; alternative structured lane |
| 10 | Vision on flash | unused | screenshot adjudication lanes could ride the cheap tier |
| 11 | Files API | unused | re-sending the same big evidence bytes per ask; file_id reuse + cache would collapse it |
| 12 | `reasoning_effort` ladder (none/low/high/max) | binary on/off only (AH10 law keeps it off; fine) | none: off is correct for mechanical work |
| 13 | Anthropic-format base | unused | Claude-shaped tools could burn DeepSeek credits instead of unfunded Anthropic keys |
| 14 | `user_id` isolation | unused | KVCache privacy + scheduling isolation |
| 15 | `logprobs`/`top_logprobs`, chat prefix completion, `echo` | unused | grader-lane features, low priority |

**Ledger truth-up (the 61 token-bearing deepseek rows, 2026-10-01):** 317,778 prompt + 31,084 completion
tokens, metered $0.1808 at model_garden's 0.44/1.32. All fires landed 19:18-23:37 UTC Thursday = OFFPEAK
on the official clock. True price: 317,778 x $0.15/M + 31,084 x $0.60/M = **$0.0663, a 2.7x overstatement**,
before counting cache hits (which the rows cannot see).

---

## 3. Live probes (exact bytes in probe_receipts.jsonl; spend $0.000937)

- **P0 GET /models -> 200**: exactly `["deepseek-flash", "deepseek-v4-pro"]`. flash: context 1,048,576, max out 393,216, modalities text+image, efforts low/high/max default high, `anthropic_messages.system_prompt_update: in-history`.
- **P1 GET /user/balance -> 200**: `{"is_available": true, "balance_infos": [{"currency": "USD", "total_balance": "47.54", "granted_balance": "0.00", "topped_up_balance": "47.54"}]}`. Live spend meter proven, zero cost.
- **P2 prefix-cache A/B/C** (5,299-token prompt, identical 23,159-char scaffold prefix, distinct final question, `deepseek-flash` thinking disabled, fired 00:27 UTC = offpeak):

| fire | prompt_tokens | hit | miss | out | cost (offpeak rates) | latency |
|---|---|---|---|---|---|---|
| A (cold) | 5,299 | 0 | 5,299 | 1 | $0.000795 | 1.15s |
| B (same prefix) | 5,300 | **5,120** | 180 | 1 | $0.000043 | 1.16s |
| C (same prefix) | 5,299 | **5,120** | 179 | 4 | $0.000045 | 1.40s |

  Result: **96.6% of the repeat prompt rides hit price; fire B cost 5.4% of fire A (18.5x cheaper)**.
  Both B and C hit exactly 5,120 tokens -> the fixed-interval persistence unit is 5,120 tokens; the
  trailing ~180 tokens (question + boundary) stay miss. **Practical law: a shared scaffold below
  ~5,120 tokens will NOT cache; hoist scaffolds to >= 5,120 tokens to ride the hit price.**
- **P3 JSON mode -> 200**: `response_format {type: json_object}`, request included the word "json" + format sample. Returned exactly `{"verdict": "PASS", "confidence": 1}`, `json.loads` clean. usage: 80 in / 14 out.
- **P4 FIM -> 200**: POST `https://api.deepseek.com/beta/completions`, body `{model: deepseek-flash, prompt: "def connect_tile(a, b):\n    ...", suffix: "\n\nclass Board:\n    pass", max_tokens: 100}`. Returned `object: "text_completion"`, `finish_reason: "stop"`, and a syntactically coherent function BODY that ends where the suffix begins. usage fields include the cache split.

---

## 4. Swarm-repricing math (what caching alone does to a 391-file sweep)

Baseline: DOLLAR_BURN_SWEEP (receipt `watch/inbox/model_garden/DOLLAR_BURN_SWEEP.md`), 391 files,
8 ds_workhorse batches, fired 19:18-19:21 UTC Thursday = **offpeak**, metered **$0.5193** at
ds_workhorse's flat $0.27/$1.10 (tokens derived from that meter: ~1.80M in, ~31k out).

1. **Metering truth alone (no behavior change):** 1.80M x $0.15/M + 31k x $0.60/M = **$0.289**.
   The receipt overstated the sweep 1.8x because the flat table ignores the offpeak clock.
2. **Caching as-shaped: ~nothing.** The shared scaffold is 1,542 chars (~360 tokens) and sits first
   (good), but 360 < the 5,120-token persistence unit (probe P2), and the unique file text is ~98% of
   input, which cannot cross-item cache. The retry-once path DOES silently ride hit price on the real
   invoice (identical prompt re-fire) - our meter just cannot see it.
3. **Caching reshaped (the play):** hoist the scaffold to >= 5,120 tokens (full organ rubric, definitions,
   worked examples, output contract - quality we anyway want for verdict consistency). Then 390 of 391
   fires hit 5,120 tokens:
   - scaffold share without cache: 390 x 5,120 x $0.15/M = **$0.2995**
   - with cache: 390 x 5,120 x $0.003/M = **$0.0060** -> **the 5k rubric rides at 2% of miss price; every shared token above the 5,120 boundary costs 0.6% of a fresh token** (50x, both windows: peak 0.006 vs 0.30).
   - Net effect on the whole sweep: you can afford a 14x bigger shared contract for ~$0.03 total instead
     of ~$0.30; the unique-text bill (~$0.27) is unchanged and is the floor.
4. **Where caching bites hardest in our shapes (the repeat class, 50x each):**
   - retry-once on empty (ds_workhorse law): the retry is an identical-prefix re-fire = ~96% hit.
   - model_garden turn-2 revision (`model_garden.py:334-336` re-sends the original user msg): the whole
     turn-1 prefix hits; revision turns stop doubling input cost.
   - patrol RE-RUNS of an unchanged tree (the receipt's own "rerun ~$0.52 at wave close"): unchanged file
     prefixes + scaffold all hit; a no-drift rerun collapses toward output cost only (~$0.02-0.03).
   - SWARM cross-check rows where the DeepSeek lane re-reads the same evidence files per ask
     (SWARM_1 deepseek $0.1599 metered): same evidence re-sent across asks/turns rides hit.
5. **Width:** no batch API exists, but concurrency 2500 means the 391-file sweep can fire 50-100 wide
   (file-backed batches make this trivial); wall time drops from ~3.5 min serial to seconds. Width is a
   latency multiplier, not a price one.

---

## 5. The 3 highest-value adoptions (tickets)

**T1 - PRICE TRUTH: canonicalize the lane** (touches `tools/ds_workhorse.py`, `tools/model_garden.py`,
`configs/cost_rates.yaml`): switch model id `deepseek-chat` -> `deepseek-flash` + explicit
`thinking: {type: disabled}` (byte-identical behavior, AH10 law preserved; probe P2/P3 prove disabled
works on flash); replace the three divergent price tables with the canonical peak/offpeak schedule
(fixing cost_rates.yaml's inverted window comment); read `prompt_cache_hit_tokens` /
`prompt_cache_miss_tokens` from every response and bank them in the ledgers; ds_workhorse starts
persisting usage (it currently discards it). Payoff: kills the deprecated-alias outage risk, ends the
2.7x cost overstatement, makes cache wins visible. Falsifier: ledger cost vs invoice diverges > 10%.

**T2 - OFFPEAK LAW + SCAFFOLD LAW for mechanical sweeps**: schedule ds_workhorse batches outside
Mon-Fri 01:00-04:00 / 06:00-10:00 UTC (everything halves; our sweeps already fire offpeak by luck -
make it law), and hoist shared scaffolds to >= 5,120 tokens scaffold-first with per-item text LAST
(ds_workhorse already puts {text} last - grow the template past the unit boundary). Payoff: 2x on
timing plus 50x on every shared scaffold token; a no-drift patrol rerun drops from ~$0.29 to ~$0.03.

**T3 - LIVE SPEND METER + JSON VERDICTS**: GET `/user/balance` (free, P1-proven) wired into
`mag/hermes_warm_boot.py` warm state + after every batch, surfaced on the dashboard; switch sweep
verdicts to `response_format json_object` with the format sample in the prompt (P3-proven parse-clean),
retiring aggregate.py's regex fragility and the self-contradictory-verdict discount class.
Payoff: operator sees the real $47.54 burn-down in real time; verdict parsing becomes structural.

---

## 6. Summary line

**Features found: 10 endpoint families / 20 capabilities. Used today: 1 endpoint (chat/completions),
1 legacy model id, 5 request fields, 5 response fields. Wasted: 15 capabilities including the entire
cache economics, offpeak clock, balance meter, JSON mode, 2500-wide concurrency, FIM, vision, files, tools.**
**Cache A/B: cold fire $0.000795 (0/5,299 hit) vs warm fire $0.000043 (5,120/5,300 hit, 96.6%) = 18.5x
cheaper on the repeat; hit unit measured at 5,120 tokens.**
**Single biggest adoption: T1 PRICE TRUTH - canonical `deepseek-flash` + thinking-off + peak/offpeak
canonical rates + banked hit/miss tokens in the production lanes, because the ledger currently
overstates the lane 2.7x, rides a discontinued model alias, and cannot see the 50x cache discount
it is already being granted.**
