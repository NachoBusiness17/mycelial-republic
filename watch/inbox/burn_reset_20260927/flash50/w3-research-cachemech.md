# w3-research-cachemech: prompt caching in production LLM APIs vs our frozen-prefix

Date: 2026-09-28. Lane: mickey gopher (w3), flash50 research dig.
Method: live provider docs fetched 2026-09-28 via WebFetch (URLs cited per section), repo
recon via rg + Read on this tree, plus the estate's own cache KPI run (exact command in
section 5). Anything not verifiable this session is marked OWED in section 7. No em-dashes.

## 1. Sources read and commands run

Fetched (read this session):
- Anthropic prompt caching: https://platform.claude.com/docs/en/build-with-claude/prompt-caching (reached via 302 from docs.claude.com/en/docs/build-with-claude/prompt-caching)
- Google Gemini context caching (implicit + Interactions API note): https://ai.google.dev/gemini-api/docs/caching
- Google Gemini CachedContent API reference: https://ai.google.dev/api/caching (page rendered in German; field names quoted as-is)
- Google Gemini pricing: https://ai.google.dev/gemini-api/docs/pricing
- OpenRouter prompt caching: https://openrouter.ai/docs/features/prompt-caching
- WebSearch (z.ai-backed) used only to hunt the Gemini explicit-TTL default; results labeled as search paraphrase, not page reads (see OWED).

Ran (exact commands, this session):
- `rg -i -n "frozen[-_ ]?prefix" mag/ tools/ scripts/ main.py` (recon, plus an earlier repo-wide rg banked to the harness exec log)
- `.venv/Scripts/python.exe tools/cache_kpi.py --since 2026-09` (output in section 5)
- `.venv/Scripts/python.exe mag/glm_flash.py` (status JSON in section 5)

## 2. Anthropic (explicit, breakpoint-based, tiered TTL)

Mechanics: cache references the full prompt in order tools, system, messages, up to and
including the block marked `cache_control`. Hits require 100% identical bytes up to that
block. Writes happen only at breakpoints (hash of the prefix ending there); 20-block
lookback window per breakpoint; up to 4 breakpoints. A top-level
`cache_control: {"type":"ephemeral"}` applies an automatic breakpoint to the last
cacheable block and advances it as the conversation grows (400 error if 4 explicit
breakpoints already exist).

Minimum cacheable tokens (below it, content is processed uncached, no error):
- 512: Fable 5.1, Mythos 5.1, Opus 5.5, Opus 5, Sonnet 5.5, Fable 5, Mythos 5
- 1,024: Opus 4.8, Sonnet 5, Sonnet 4.6, Sonnet 4.5, Opus 4.1, Opus 4, Sonnet 4
- 2,048: Mythos Preview, Opus 4.7, Haiku 3.5
- 4,096: Opus 4.6, Opus 4.5, Haiku 4.5

TTL: 5-minute default, refreshed at no cost on each use. Lifetime is measured from the
START of the request that writes or reads the entry (generation time counts against it).
Extended: `"cache_control": {"type":"ephemeral","ttl":"1h"}`. Mixing rule: longer TTLs
must precede shorter ones; billing reads up to the highest hit, then 1h writes for the
(B-A) span, then 5m writes for the (C-B) span. No `extended-cache-ttl` header exists on
the current page (the old beta header is gone from the doc).

Pricing multipliers (of base input): 5m write 1.25x, 1h write 2x, read 0.1x generally
(0.025x on Fable 5.1 / Mythos 5.1, 0.05x on Opus 5.5). Breakpoints themselves are free.

Invalidation cascades through tools -> system -> messages: a tool definition change
invalidates everything; tool_choice changes or images added/removed invalidate messages;
thinking parameters and `output_config.effort` always invalidate messages; a dropped
thinking block invalidates from that block onward.

Usage fields: `cache_creation_input_tokens`, `cache_read_input_tokens`, `input_tokens`;
1h split via `cache_creation.ephemeral_1h_input_tokens` / `ephemeral_5m_input_tokens`.

Structure guidance (their stated best practices): static content (tools, system, context,
examples) first, breakpoint on the LAST block whose prefix is identical across requests;
the classic killer is a breakpoint on a varying block like a timestamp (writes only occur
at breakpoints, so the hash never matches). Pre-warm by sending `max_tokens: 0` with an
explicit breakpoint on shared content (rejected with stream:true, extended thinking,
structured outputs, forced tool_choice). A cache entry is usable only after the first
response begins. Caches are workspace-isolated. Combine explicit breakpoints (stable
system) with automatic caching (growing conversation).

## 3. Google Gemini (implicit automatic + explicit rented caches)

Implicit caching: on by default for Gemini 2.5 and newer; nothing to enable; hits surface
in `usage.total_cached_tokens`. Minimum prefix sizes: 4,096 tokens for Gemini 3.8 / 3.7 /
3.6 / 3.5 Flash and 3.1 Pro Preview; 2,048 for Gemini 2.5 Flash and 2.5 Pro. Official
advice: "put large and common contents at the beginning of your prompt" and "send
requests with similar prefix in a short amount of time." The Interactions API supports
implicit only; explicit caching (cachedContents objects) is generateContent-API only.

Explicit caching: `cachedContents` resource under /v1beta with immutable, model-locked
`contents`, `tools`, `systemInstruction`, `toolConfig`; `displayName` max 128 chars;
`usageMetadata.totalTokenCount`. Expiration is a mutually exclusive union:
`expireTime` (RFC 3339 timestamp, always set on output) or `ttl` (input-only duration,
e.g. "300s"). `cachedContents.patch` can update ONLY the expiration. Create example in
the reference uses `"ttl": "300s"`, then generateContent with `"cachedContent":
"cachedContents/{id}"`.

TTL default and minimum: default 1 hour when unspecified, minimum 2 minutes. This came
from WebSearch result summaries and a discuss.ai.google.dev thread snippet, not from a
live ai.google.dev page (the caching page was restructured to Interactions-only and
/api/caching documents the ttl field without a default). Labeled OWED in section 7.

Pricing (standard tier, per 1M tokens): cached reads are 10% of input price across the
board, with an hourly storage rent. Gemini 2.5 Pro: input $1.25 (<=200K) / $2.50 (>200K),
cached $0.125 / $0.25, storage $4.50/hr. Gemini 2.5 Flash: input $0.30, cached $0.03,
storage $1.00/hr. 2.5 Flash-Lite: $0.10 / $0.01 / $1.00/hr. Gemini 3.8 Flash: input
$0.75 until 2026-12-31 then $1.50, cached $0.075 then $0.15, storage $0.50/hr then
$1.00/hr. 3.1 Pro Preview: $2.00 / $4.00 input, $0.20 / $0.40 cached, $4.50/hr storage.
Batch and Flex tiers charge roughly half the caching price; Priority is higher.

Shape difference vs Anthropic: Gemini explicit caching is a RENTED, STATEFUL object (pay
per cached-token-hour, then never resend the prefix), not a per-request write.

## 4. OpenRouter (provider-side caching + sticky routing)

Caching is provider-side; OpenRouter routes for it. Most providers cache automatically;
Anthropic and Alibaba require per-message opt-in via `cache_control`. After a cached
request OpenRouter applies sticky routing to keep hitting the same endpoint; sticky
sessions expire after 10 minutes of inactivity and every successful request resets the
timer. Routing activates only when cache-read pricing beats regular prompt pricing.
Sticky keys hash the first system/developer message plus the first non-system message,
per account/model/conversation. Override with `session_id` (body, takes precedence) or
`x-session-id` header (max 256 chars), or OpenAI-style `prompt_cache_key`; with an
explicit session_id, stickiness activates on any successful request, even before a hit.
Manual `provider.order` disables sticky routing (reroute still happens on error).

Per-provider read/write multipliers (of base input) as tabulated by OpenRouter:
- OpenAI: automatic, 1,024-token minimum; writes free pre-GPT-5.6, 1.25x on 5.6+; reads
  0.25x-0.50x. Explicit mode (GPT-5.6+ only): `prompt_cache_breakpoint` on text blocks +
  request-root `prompt_cache_options` {mode:"explicit", ttl:"30m"}, minimum 30-minute TTL.
- Anthropic: 1.25x write (5m) / 2x (1h) / 0.1x read; `cache_control` with optional
  "ttl":"1h"; four-breakpoint limit; minimums 4,096 (Opus 4.5-4.8, Haiku 4.5), 2,048
  (Haiku 3.5), 1,024 (Sonnet 4/4.5/4.6, Opus 4/4.1). (Note: OpenRouter's table lags the
  Anthropic native page's model table above.)
- DeepSeek: automatic; writes at normal input price; reads 0.1x.
- Google Gemini: implicit reads 0.25x, no write cost, ~3-5 min TTL; minimums 1,024
  (Flash) / 4,096 (Pro); explicit `cache_control` costs input plus prorated 5-minute
  storage with a FIXED 5-minute TTL that does not update.
- Grok: automatic, free writes, reads 0.25x. Moonshot: automatic, free writes, 0.25x.
- Groq: automatic, free writes, reads 0.5x (Kimi K2).
- Alibaba Qwen: explicit only (`cache_control: {"type":"ephemeral"}`), 1.25x / 0.1x,
  5-minute TTL.
- Z.AI: automatic, free writes, reads ~0.2x; OpenRouter derives a session affinity key
  from account + session_id.

Cross-provider translation: an Anthropic-style `cache_control` block becomes an OpenAI
`prompt_cache_breakpoint` when routed there, and vice versa (Anthropic/Google get a
default 5-minute cache_control). "TTLs are not translated": a cache_control ttl is
dropped toward OpenAI and `prompt_cache_options` stays OpenAI-only.

Usage accounting: `cached_tokens` (reads) and `cache_write_tokens` (first request that
establishes the cache) in `prompt_tokens_details` (Chat Completions) or
`input_tokens_details` (Responses); a `cache_discount` field shows savings (Anthropic
writes appear as negative discount); also on the Activity page and /api/v1/generation.

Their best practices: keep the start of the message array consistent, push variable
content to the end; for Gemini put dynamic content in a LATER user message (its
`systemInstruction` is treated as immutable when cached); reserve explicit breakpoints
for large static text (RAG, documents, character cards); use session_id for multi-turn
agentic workflows; use 1-hour Anthropic TTLs for long sessions to avoid repeated write
charges; in the Batch API, lines may run concurrently, so use 1h TTL on shared prefixes
or warm the cache synchronously first.

## 5. Our frozen-prefix approach (repo receipts, this tree)

The mechanism: a byte-identical standing prefix as the system role, tiny dynamic tail as
the user role, riding the provider's AUTOMATIC prefix cache. No cache_control, no TTL
purchase, no cache objects anywhere in our stack.

- mag/glm_flash.py:29-39: FROZEN_SELF = work_contract BRIEF + 5-rule STANDING doctrine,
  sent as `system` every call (line 66); tail = task + context[:12000] (line 57).
  Status run this session: `.venv/Scripts/python.exe mag/glm_flash.py` -> ok, model
  glm-4.7-flash, frozen_self_chars 763, frozen_self_tokens_est 190.
- mag/context_pack.py:430-449 (A2 law): system prompt + tool schemas must be
  BYTE-IDENTICAL for the whole session because "provider prompt caches key on exact
  prefix bytes"; schemas serialized canonically (json.dumps sort_keys=True).
  freeze_system_prompt (452-489) hashes sha256(prefix bytes + NUL seam + canonical
  schemas) so either half changing flips the hash; evolving_tail (492-509) carries all
  live values AFTER the prefix, capped at 5,200 chars.
- mag/agent_cli.py:952-963, 986-999, 1006-1019: the stable body is cut BEFORE the live
  context pack section; new instructions ride as TRAILING developer messages, "never
  spliced into the frozen prefix, where a mid-insert would re-price everything after it."
- scripts/steering_suite.py:846: "# Arm-outer so a frozen prefix stays hot on
  prefix-caching servers." That is our entire TTL strategy: keep-warm by call cadence.
- Measurement: scripts/probe_cache_ab.py (A/B with controlled prefix; verdict >=0.90 OK,
  >=0.50 WEAK, <0.50 BROKEN; its docstring records the 2026-08-25 dispute where the
  ledger said 0.3% and the controlled A/B said 99%+, root cause = prefix variation in
  OTHER callers, not provider behavior). mag/honest_cache_meter.py: HIT_tok
  (token-weighted), SAVINGS_dollars net of the cache-WRITE premium ("an honest meter can
  and will report NEGATIVE savings on write-heavy days"), coverage, nightly
  reconciliation against the provider invoice, provider-reported tokens only. mag/
  cache_watch.py: standing $0 monitor, alarms when probe or ledger ratio < 0.90; targets
  "~97% lifetime hit on deepseek, 99%+ on glm flash". mag/offerings.py:77,95 records
  "glm_flash.cached_chat ~99.6%" as the standing number.
- Fleet KPI run this session: `.venv/Scripts/python.exe tools/cache_kpi.py --since
  2026-09` on logs/provider_usage.jsonl (76,568 rows total, 38,324 since September):

```
provider    rows   err cache_rows hit_call%  prompt_tok    cached_tok    tok_hit%
deepseek   36937    61      36876    99.2%   601,535,750   578,095,488    96.1%
z_ai3        357   238        119    88.2%       253,155        20,194     7.2%
z_ai         188    28        160    86.9%     1,499,673     1,237,824    82.5%
openrouter    35     2         33    12.1%       181,606        25,792    14.2%
TOTAL      38324   803     37521    98.2%   603,952,323   579,399,778    95.9%
```

So the fleet's cache economics are real but concentrated: 601.5M September prompt tokens
on deepseek at 96.1% token hit (reads at 0.1x per OpenRouter's DeepSeek row = roughly
8.6x cheaper input on the cached share), while the small mixed-caller lanes (z_ai3 at
7.2%, openrouter at 14.2%) bleed exactly the way the probe docstring predicts: prefix
variation and routing unpinned, not provider refusal.

## 6. Comparison and steal list

Convergences (we already do what the providers prescribe):
1. Static-first, dynamic-last: FROZEN_SELF then task tail = Anthropic's "static content
   at the start, breakpoint on the last identical block" without needing breakpoints,
   because we ride automatic caches where the whole sent prefix IS the cacheable span.
2. Byte-identity including tool schemas: A2's prefix hash covering schemas matches
   Anthropic's invalidation cascade (a tool change invalidates everything) and OpenRouter
   sticky hashing (first system/developer message + first non-system message). Our
   sorted-key canonical serialization is the same discipline their SDKs apply.
3. Never mid-insert: trailing developer messages mirror their "push variable content to
   the end"; a mid-insert re-prices everything after it on every vendor.
4. Honest accounting: cache_kpi's per-provider telemetry normalization (openai
   cached_tokens / deepseek prompt_cache_hit_tokens / anthropic
   cache_read_input_tokens) and honest_cache_meter's write-premium-net savings track the
   exact field model the providers publish (cache_read_input_tokens,
   cache_creation.ephemeral_1h/5m split, cache_discount negatives on writes).

Divergences and gaps:
1. SIZE FLOOR. Our FROZEN_SELF is ~190 estimated tokens. Anthropic's floors are 512 to
   4,096 tokens by model (shorter prompts are silently processed UNCACHED, no error), and
   Gemini implicit needs 2,048 to 4,096. Ported verbatim to those providers, our prefix
   would never cache. It works on deepseek/z.ai because those vendors enforce no floor
   we have observed. Actionable: any Anthropic/Gemini lane must fatten the static prefix
   past the floor (system + tools + docs) rather than assume the flash-era trick ports.
2. NO TTL TIER. We buy no 1h entries and create no cache objects; our only levers are
   cadence (arm-outer) and tight loops. Breakeven arithmetic from the fetched
   multipliers (derived, not measured): 5m entry costs 1.25x on write and refreshes free
   per read; a 1h entry costs 2x once. Tight loop (<5m gaps): 5m wins (1.25 + n*0.1 vs
   2 + n*0.1). Sparse access (gaps of 5m to 1h): each 5m expiry forces a 1.25x rewrite,
   so 1h wins from the second generation onward (example: 6 calls 10 minutes apart = 7.5x
   on 5m vs 2.5x on 1h). Our janitor cycles are tight-loop, so status quo is right for
   deepseek, but a sparse Anthropic session is the documented case for ttl:"1h"
   (OpenRouter names exactly this for long agentic sessions and Batch API races).
3. NO AFFINITY PINNING. Our single-provider lanes cannot drift; the 35 September
   openrouter rows at 14.2% hit show what unpinned multi-provider traffic costs. When we
   route through OpenRouter again, send session_id (it activates stickiness before any
   hit and survives the 10-minute inactivity expiry as long as requests keep flowing).
4. THE 0.3% LEDGER GHOST IS THEIR DISEASE TOO. Our probe docstring's prefix-variation
   diagnosis is the same failure OpenRouter's sticky routing + session_id machinery
   exists to fix at the fleet level. Our fix (control the prefix, probe A/B) and theirs
   (pin the route, hash the head) are complementary halves.
5. GEMINI EXPLICIT IS A DIFFERENT SHAPE. A rented cachedContent is stateful (pay per
   token-hour, never resend). For our small frozen self, rent would exceed resend cost
   on free lanes; for a future fat-prefix lane (a 50K-token corpus in system), the rent
   math flips: 2.5 Flash at $1.00/Mtok/hr rent vs $0.27/Mtok saved per resend means
   break-even at roughly 3.7 resends per cached-hour. Our resend model is the right
   default; rented caches are a fat-prefix-only tool.

Steal list (ranked):
1. Explicit `cache_control` + fattened static prefix on any future Anthropic lane
   (floors 512-4,096); top-level automatic cache_control for growing conversations,
   explicit breakpoint on the stable system block.
2. ttl:"1h" only for sparse (>5m gap) Anthropic sessions; keep 5m default for tight
   loops; bill the choice through honest_cache_meter's write-premium columns.
3. max_tokens:0 pre-warm probe before first real call on a cold shared prefix
   (Anthropic-supported; their documented rejection cases: streaming, extended thinking,
   structured outputs, forced tool_choice).
4. session_id on all OpenRouter traffic; expect openrouter tok_hit to jump from 14.2%.
5. cache_kpi already parses anthropic cache fields; extend the floor-warning (prompt_tok
   < 512/1024/2048/4096 by model means "uncached by law, not by drift") when such a lane
   appears.

## 7. OWED / not verified

- Gemini explicit-cache TTL default (1h) and minimum (2m): corroborated via WebSearch
  result summaries and a discuss.ai.google.dev thread snippet, NOT read from a live
  ai.google.dev page this session (the caching page now covers Interactions/implicit
  only; /api/caching documents the ttl field without a default). OWED: read it from the
  live generateContent caching guide before quoting it in any law.
- OpenAI platform.openai.com prompt-caching guide not fetched (OpenAI numbers above come
  from OpenRouter's provider table, which may lag; the GPT-5.6 explicit-cache fields are
  OpenRouter's description only).
- No live cache calls were made to Anthropic, Google, or OpenRouter this session (no
  authorized spend for this item): every provider number is doc text fetched 2026-09-28,
  not metered. Doc pages render through the fetch summarizer; quoted numbers are its
  extraction of the cited URLs.
- FROZEN_SELF token count is the repo's chars//4 estimate (mag/glm_flash.py:101), not a
  tokenizer truth; a real count could cross Anthropic's 512 floor or not.
- The breakeven arithmetic in 6.2 is derived from fetched multipliers, not from a
  billing experiment.
