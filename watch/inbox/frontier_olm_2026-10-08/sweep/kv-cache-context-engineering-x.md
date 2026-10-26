# Sweep: kv-cache-context-engineering via X (frontier_olm 2026-10-08)

source-fetched: 2026-10-08. Seat: sweep-kv-cache-context-engineering-x. Area feeds
the deliberate-ask frozen-prefix carriers, the P3 thinking-default reader, the
context_compression.py invariant set (memory/percolator/invariants.json), and the
per-family cache grammar rows in the model garden.

## Door health (this sitting)

- WebSearch (X door leg 1): 5 query batches issued. One hard timeout (llama.cpp
  KV offload phrasing), one content-filter block (error 1301 on the word pair in
  that query) then 1302 rate limits on its retries; the reworded Nous and Ollama
  batches answered clean. Unlike day-7 (search truncating every x.com URL to bare
  https://x.com), TODAY the door returned full status IDs on every hit
  (watch/inbox/frontier_olm_2026-10-07/sweep/kv-cache-context-engineering-x.md:13-16
  named that failure; it did not recur).
- fxtwitter door: ALIVE and used for real. 6 candidate posts resolved to full JSON
  (HTTP 200 each, 2s pacing, raw saved under sweep/_raw/fx_*.json). Threads read
  end to end from the returned text bodies.
- curl door: api-docs.deepseek.com serves a 48,088-byte JS shell to curl (three
  URLs, zero content hits); WebFetch renders it. platform.moonshot.ai and
  platform.moonshot.cn doors dead (162-byte responses); platform.kimi.ai serves a
  Mintlify shell whose article body is embedded in the HTML and was extracted
  programmatically (extraction script run this sitting, bytes saved).
- Degradations stated, never papered: the shmidtqq "bill by 10 / 256 rule" X
  ARTICLE body is unresolvable through every door (fxtwitter returns the wrapper
  post only); banked at resolved-post tier below, content claim stays snippet.

## Method and bars

- Pass 1 census: 49 candidates considered this sitting: 10 X-door results (search
  1) + 9 Nous-search results + 9 Ollama-search results + 7 resolved-or-rejected X
  posts incl. Step 5 Preview (off-axis, rejected) + 14 vendor/doc/primary pages
  fetched or probed (DeepSeek x4, Moonshot/Kimi x5, hermes-agent x4 fetched +
  issue/reddit leads, llama.cpp server README, LMCache mirror). Window honesty:
  today is 2026-10-08, strict 30-day window opens 2026-09-08. In-window by
  artifact date: the Pachaar NVIDIA thread (Sep 8), Kimi/DeepSeek/Hermes living
  pages (every quote re-fetched today). Out of window, disclosed: Chawla
  compaction post (Aug 22, banked on strength), shmidtqq article (Aug 24).
- Pass 2 deep reads, end to end this sitting: hermes-agent prompt-assembly;
  hermes-agent context-compression-and-caching; hermes-agent configuring-models;
  hermes-agent api-server; DeepSeek thinking_mode (WebFetch render); Kimi
  context-caching (embedded body + full pricing table); Kimi dynamic tool loading;
  nanobot.wiki Ollama prompt-cache guide; llama.cpp server README (flag table);
  plus two full fxtwitter thread reads (Chawla 2091078211904139377, Pachaar
  2097421509220561028). That is 10+ against the >=5 floor.

## Estate priors honored (anti-rebank, all read this sitting)

Day-7 banked and therefore NOT re-banked: xAI What-Breaks-Caching + multi-turn +
usage-and-pricing pages; xAI Context Compaction API; Anthropic prompt caching +
compaction + context editing; the contradicted OpenAI caching claim (DIGEST.md:90:
real page = automatic, free, 1,024-token minimum, in_memory/24h retention);
Together serving DeepSeek-V4; Chawla dailydoseofds four-layer article (its Sep 3
post form, status 2095445303679988200, resolved today via fxtwitter, is the same
content - not banked); DeepSeek context-caching semantics (estate-held,
memory/improve/deepseek_api/context_caching.txt, re-confirmed unchanged in
structure). Day-6 banked: BreadthKV 2610.05685, BARQ 2610.04490. Day-7 arxiv lane:
ReFold 2610.07863 + steal card, LORE-KV, Lachesis. NEW this sitting:
arXiv 2608.03893 (cross-model KV transfer, the Pachaar thread's paper) is
ESTATE-HELD as a bibverify VERIFIED row
(memory/research_packs/bibverify/part1_tiers.jsonl: status VERIFIED, "Receiver LLM
reuses another model's KV cache to skip prefill") - the thread was NOT banked as
an item on that ground.

## Banked items (8, strongest first)

### 1. Hermes Agent prompt-assembly docs: the three-tier frozen-prefix law
https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly
(living page, fetched and read 2026-10-08). The estate's own upstream harness
documents the exact deliberate-ask shape: system prompt assembled "stable ->
context -> volatile"; shared project files precede worktree-specific ones so
sessions "share a prompt prefix covering the whole context block" and "that
prefix is what a longest-prefix provider cache reuses"; memory/profile snapshots
stay inside the cached system prompt ("not injected as ad-hoc mid-turn
overlays"); mid-session memory writes "do not mutate the already-built cached
system prompt until a rebuild path runs"; plugin context "is appended to the
current turn's user message, not written into the cached system prompt" so "the
cached prefix survives"; platform hints resolve to "a byte-stable hint for a
fixed config". This is the vendor-documented answer to research question 1: the
fix for warm_state/briefs/world_state mutation is placement + rebuild gating,
not smaller prompts. Overlap: catalog 0 for "hermes-agent.nousresearch.com" and
"prompt-assembly"; memory hits are 3 bare-URL session-journal echoes
(memory/agent_sessions/orc-t*.json, inspected: URL only, no content).

### 2. Nous Portal grammar: caches keyed to the model; OpenRouter path rewrites the prior turn's cache
https://hermes-agent.nousresearch.com/docs/user-guide/configuring-models
(fetched and read 2026-10-08). Verbatim: "Prompt caches are keyed to the model
serving the request" so a mid-conversation model change "re-reads the entire
conversation at full input-token price instead of the cached (~75-90%
discounted) rate"; "A one-turn switch breaks the provider's prompt-cache prefix
twice (switching out and back)"; and the measured defect: on the Portal's
OpenRouter path the harness "re-writes the previous turn's prompt cache on 14-20%
of consecutive calls in concurrent tool loops", while "the chat route measured 0
on the same test". Also: "signed thinking blocks pass through unchanged" on the
native wire. Grammar rows for the funded Nous primes lane (glm-5.3-prime /
qwen3.8-max-prime), with a number: concurrent tool loops on the OpenRouter route
are a 14-20% prefix-instability surface. Overlap: catalog 0; memory
"cache_read_tokens" hits are estate run logs
(memory/runs/compaction_eval/steps_frozen_20260920.jsonl et al.), not docs.

### 3. Hermes Agent context-compression-and-caching: the dual-compressor with cache-aware boundaries
https://hermes-agent.nousresearch.com/docs/developer-guide/context-compression-and-caching
(fetched and read 2026-10-08). Two layers: gateway session hygiene at 85%
(pre-agent), Agent ContextCompressor at 50% default (matching 50% at the gateway
"caused premature compression on every turn"). Cache interaction: a
"system_and_3" strategy (system prompt plus last three non-system messages as
cache breakpoints, ephemeral markers with 1-hour TTL); "the cache is invalidated
for the compressed region but the system prompt cache survives" and
re-establishes "within 1-2 turns"; prompt caching "reduces input token costs by
~75% on multi-turn conversations"; cooldown escalation 60s -> 300s -> 900s on
failed summaries; measured compaction benchmark: "Result on 500K-token real
sessions: ~49K retained vs ~162K" (lean tail). This is the measured shape the
context_compression.py invariant set (item: Q5 below) should encode. Overlap:
catalog 0 for "system_and_3"; memory hit is my own steps.jsonl journal.

### 4. DeepSeek thinking-mode grammar, live re-verified: reasoning_content is conditional on tools
https://api-docs.deepseek.com/guides/thinking_mode (curl gets a JS shell;
WebFetch render read 2026-10-08). Verbatim: no-tools case - "reasoning_content
does not need to be passed back... even if passed to the API, it will be ignored
and will not be concatenated into the context"; tools case - "the
reasoning_content of all previous turns should be passed back to the API and
will be concatenated into the context... even for turns where the model did not
perform a tool call. If your code does not correctly pass back
reasoning_content, the API will return a 400 error." This is the per-family
grammar row OPPOSITE to xAI (where omission = top cache-miss cause): on
DeepSeek, dropping reasoning on replay is HARMLESS without tools and a hard 400
with tools. The estate archive holds the older wording
(memory/improve/deepseek_api/thinking_mode.txt, fetched Aug 2, "must be passed
back" for tool turns, "ignored" otherwise); the 400-error sentence and the
concatenation semantics are the live sharpening. Overlap: archive named above;
catalog holds the mirror rows only.

### 5. Kimi context caching: full grammar + priced rows (and the 256-rule resolution)
https://platform.kimi.ai/docs/guide/context-caching (platform.moonshot.ai 301s
here; shell body extracted from fetched bytes 2026-10-08). Verbatim: "for
kimi-k3, the cache-hit price is only one-tenth of the cache-miss price"; "Cache
Write is billed as a separate item, and two cache TTL (time to live) options are
offered: 5m and 1h"; "When any part of a prefix changes, the content after that
position cannot be reused"; "Do not put timestamps, random IDs, or other dynamic
fields in the prefix"; cache isolated by organization; no manual clear; expiry
after TTL inactivity. Pricing table extracted verbatim: Input (cache miss)
$3.00 per 1M, Cache Write (5m) $3.00, Cache Write (1h) $6.00, Cached Input (hit)
$0.30; each hit resets TTL validity. RESOLUTION of day-7's snippet-tier "256
rule" (prior item 8): the shmidtqq post is real and now resolved (author, date
Aug 24, article link https://x.com/i/article/2090244934955900928 via fxtwitter),
but its article body is unresolvable, and the Kimi primary page states NO
minimum token threshold anywhere in the guide body (programmatic search: 0
hits). The 256 figure remains sourceless; keep day-7's do-not-quote flag
standing. Overlap: catalog "kimi-k3" = 1 row, the model tesuji card
(memory/improve/evals/models/kimi-k3-2026-07-27.md), not the caching docs;
platform.kimi.ai known via tesuji card + ingest registry + salon1 items.

### 6. nanobot.wiki Ollama prompt-cache guide: the measured local-lane fix (44.22% -> 99.82% cached)
https://nanobot.wiki/docs/0.3.5/guides/configure-ollama-prompt-cache (fetched
and read 2026-10-08). Mechanism: stock Ollama tool templates (llama3.1:8b shown)
render the tool block conditionally on "user message is last"
("{{- if and $.Tools $last }}"), so once tool results append, tools re-render at
a NEW position and prefix reuse collapses. Diagnosis: OLLAMA_DEBUG=1 single-slot,
read the "initially cached" n_tokens lines. Fix: a PrefixStable.Modelfile whose
template "keeps concrete tool definitions in the system block"; ollama create
reuses existing layers (template + manifest only). Measured on Ollama 0.32.1,
llama3.1:8b, one slot: second main request went "from 3767/8519 initially cached
(44.22%) to 8505/8520 (99.82%)", re-evaluated tokens 4752 -> 15. This is the
local twin of the estate's A2 freeze (mag/agent_cli.py:1018-1026: system body +
TOOL_SCHEMAS frozen byte-identical, live values appended at the END) - the
estate already implements the fix server-side; the page supplies the Ollama-side
measurement instrument (cached n_tokens log lines) for our 0.34.3 daemon.
Overlap: catalog 0 for "nanobot"/"configure-ollama-prompt-cache"; memory holds
the framework as a LINKS row ("MIT lightweight agent framework - Rocinante-side
hermes alternative", memory/corpus/LINKS.jsonl), not this guide.

### 7. Kimi dynamically loaded tools: tool declarations appended, never spliced
https://platform.kimi.ai/docs/guide/use-dynamic-tool-loading (extracted from
fetched bytes 2026-10-08). Verbatim: "Because tool declarations are only ever
appended to the end of messages, the existing conversation prefix stays
unchanged, so dynamic loading does not break the prefix cache you have already
built up and can be combined with Context Caching to further reduce cost and
latency." Also names Tool Definition Bloat: every request carrying all schemas
"driving up token usage" and degrading tool selection. Grammar consequence: the
Anthropic hierarchy (tools -> system -> messages, banked day-7) makes tool edits
the most expensive invalidation class; Kimi's provider-side answer is to move
incremental tools onto the append-only tail. Direct design input for the estate's
tool-schema freeze + the workflow-gate tool surface. Overlap: catalog 0; not in
memory outside my journal.

### 8. X post (resolved full read): compaction that edits the front of the transcript raises costs
https://x.com/_avichawla/status/2091078211904139377 (fxtwitter JSON, author and
date verified: 2026-08-22, out of strict window, disclosed; full text read this
sitting). Verbatim: "Providers bill that span as a cache read, which on
Anthropic is 10% of base input, so a context that grows only at the tail stays
cheap no matter how large it gets" and "Compaction edits the front of the
transcript rather than the tail." The mechanism statement for why ReFold-class
reversible folding (banked day-7) beats summarizing compaction: any compaction
that rewrites earlier bytes converts cache reads back into full-price writes.
Pairs with item 3's region-scoped invalidation as the measured cure. Overlap:
catalog 0 for "Compacting your agent"; memory hit is the steps.jsonl journal
only; the sibling day-7 card banked this author's four-layer article, a
different claim.

## Question-by-question verdicts

- Q1 (which ask paths mutate the frozen prefix; what a prefix-stable boot block
  saves): estate side, bytes read this sitting: the A2 freeze holds per session
  (mag/agent_cli.py:1018-1026, re-read via grep this sitting: system body +
  TOOL_SCHEMAS frozen byte-identical, new instructions appended at the END,
  "never spliced into the frozen prefix"); but the context pack's volatile
  excerpt builders sort by file mtime (mag/context_pack.py:619-633 clue chain:
  sorted by st_mtime, newest first; zeitgeist at :636-649), so any refreshed
  warm_state/brief/world_state file re-sorts its block; whether that block sits
  inside the cache-shared prefix per mode is NOT byte-verified by me this
  sitting (the day-7 card's freeze-primitive line cites have drifted; the zknot
  placement law already measured one volatile line at byte 57 causing the 0.59%
  prefix share, lens/burns.md:112-113 of the day-7 lens). External answer,
  measured: item 1's three-tier law (stable -> context -> volatile, rebuild-only
  mutation, per-turn channel for ephemerals) plus item 6's local measurement
  (tool-block position alone moved cached share 44.22% -> 99.82%). Savings in
  vendor-priced terms: cache reads bill at 10% of base (Anthropic, item 8),
  ~75-90% discounted (Nous, item 2), 1/10 price (Kimi, item 5). NOT RUN: the
  estate's own Probe A (grok-4.7 cached_tokens) remains proposed-not-run; no
  estate token measurement was faked here.
- Q2 (does the P3 reader + omission-is-measured-ON close the reasoning_content
  miss mode; do the six carriers drop reasoning on replay): grep run this
  sitting across all six named carriers: ZERO construct an assistant-history
  replay. mag/tesuji_fire.py:151-154 (single fire; the ONLY carrier that returns
  reasoning bytes to its caller, and it already reads prompt_cache_hit_tokens at
  :146-150); mag/lite_scale.py:86-98 (single fire; reasoning kept only as a
  200-char error detail, discarded otherwise); mag/lane_runner.py:706-709
  (system+user only); mag/wave_fire.py:64 (single user message);
  tools/duel_harness.py:177-180 (single user message + REASONING_CAP=6000);
  tools/stealth_driver.py:201-229 (LESSIG rails bank the reasoning tail labeled
  unverified; single-shot dispatch). Verdict: the xAI omission miss mode is
  STRUCTURALLY ABSENT today (no replay exists to omit from), not closed by P3;
  the exposure arms the moment any carrier grows turn 2, and then the grammar is
  conditional per family (xAI: carry required; DeepSeek: ignore without tools,
  400 with tools, item 4; Nous native wire: signed thinking blocks pass through,
  item 2). A carrier-level red test is now writable: replay a tool-turn history
  minus reasoning_content on DeepSeek and assert the 400.
- Q3 (per-family cache grammars from primary pages, superseding the day-7
  OpenAI claim): rows re-derived or freshly derived this sitting: xAI (day-7
  banked, stands); DeepSeek (item 4: conditional reasoning grammar; prefix-unit
  matching held in archive); Nous primes (items 1, 2, 3: model-keyed caches,
  75-90% discount band, 14-20% OpenRouter-path rewrite defect, system_and_3
  breakpoints, cache observability via usage.cache_read_tokens /
  usage.cache_write_tokens on GET /v1/runs/{run_id} and the run.completed SSE,
  api-server page read this sitting); Kimi (items 5, 7: priced 5m/1h TTLs, hit =
  1/10, org isolation, tools-append law); Anthropic (day-7 banked: hierarchy +
  512-4096 minimums + thinking-blocks-only-in-prior-turns); OpenAI (fold-fixed
  day-7: automatic, free, 1,024 minimum; today's search additionally surfaced
  "starting at 1,024 tokens, in 128-token increments" from
  openai.com/index/api-prompt-caching - snippet tier, not re-fetched, do not
  quote as verified). The day-7 fabricated OpenAI row stays struck; nothing in
  today's fetches revives it.
- Q4 (BreadthKV/BARQ/LMCache on llama.cpp/Ollama Windows/Vulkan): verdict from
  primary reads: NON-STEAL on this box at engine level. LMCache's own mirror in
  our corpus names vllm (5 rows) and triton in pyproject.toml, zero
  llama.cpp/ollama mentions in README/docs greps (run this sitting over
  corpus/library/lmcache-src); BreadthKV/BARQ are vLLM-class research (day-6
  cards). llama.cpp's own lever is placement, not policy: the server README
  (raw.githubusercontent.com/ggml-org/llama.cpp/master/tools/server/README.md,
  fetched 2026-10-08) documents "-kvo, --kv-offload, -nkvo, --no-kv-offload |
  whether to enable KV cache offloading (default: enabled)" and NOTHING
  Vulkan-specific about KV; the day-7 adjudication stands (b11465-b11476 deltas
  Metal-only, DIGEST.md:18). The local-lane steal that DOES exist here is
  item 6 (template-level prefix stability inside Ollama) plus keep_alive
  discipline (default 5m unload dumps the cache; Leanpub book page + ollama
  issue #17599 cache-contamination report surfaced in search, snippet tier).
- Q5 (falsifiable invariant set for context_compression.py): premise verified by
  instrument this sitting: memory/percolator/invariants.json holds 673 invariant
  rows, ZERO mentioning compression (python count run this sitting) - the module
  has no invariants registered at all, which is stronger than "never
  cross-linked". Proposed set, each falsifiable, honoring the RAM-cache mtime
  law (RIB_RAM_CACHE_STALE_SNAPSHOT_20260825, laws.md:91 of the day-7 lens):
  I1 PREFIX-IMMORTALITY: sha256 of the rendered frozen system block is equal
  before and after any compress event; red test = any sha change without an
  overflow marker fails the run. I2 TAIL-ONLY MUTATION: byte-diff of rendered
  context pre/post compression shows zero changed bytes before the frozen-prefix
  boundary. I3 REGION-SCOPED INVALIDATION (item 3's law): compression
  invalidates only the compressed region; cached-token ratio on the next two
  dispatches must re-establish within the 2-turn bound. I4 REVERSIBILITY (ReFold,
  banked): every shed section leaves a stub (source path + content sha); red
  test = restore re-render sha equals the stub's. I5 MTIME+SHA FINGERPRINT: any
  RAM cache of renders keys on (mtime, sha) of source organs; red test = touch
  without content change invalidates (mtime law) and content change with pinned
  mtime is caught by sha. I6 SCORER-IS-NOT-GATE: verify_compression's similarity
  score may measure loss but never certifies a restore; red test = a corrupted
  restore with a high similarity score must still fail I4. I7 CITE-SPAN
  SURVIVAL: any path:line citation inside compressed prose survives verbatim or
  the section is not compressible (the attribution-compression law, day-7 arxiv
  sweep item 8). Each row lands with a has_invariant edge so the graph orphans
  finding (lens/graph.md:29-35, day-7) does not regrow.

## Not run / OWED

- No pytest, no estate dispatch probes (Probe A/B remain proposed per the day-7
  card; nothing here fakes them). No warm_state/brief/world_state byte-order
  verification per mode (named above as not byte-verified).
- shmidtqq article body: unresolvable through every door today; the 256 figure
  stays flagged. NVIDIA 2608.03893: estate-held, thread not banked.
- Leanpub Ollama-in-Action cache chapter, ollama issue #17599 (mlx
  cache-contamination), GH nanobot issue #4867 (570-token reuse proof), the
  reddit warm-compaction plugin, openai 128-token increment line: snippet tier,
  surfaced in search, not deep-read; candidates for the next sweep.

## Receipt (commands and fetches this sitting)

WebSearch x5 batches (1 timeout, 1 content-filter + 1302 retries, rest clean);
fxtwitter x6 (all HTTP 200, raw under sweep/_raw/); WebFetch x11 (ds multi_round
render + thinking_mode render; docs.nousresearch.com ENOTFOUND; hermes x4; nanobot
x1; kimi moonshot redirect + platform timeout; llama.cpp server.md 404 then
tools/server/README.md OK); curl x11 (deepseek x4 shell, moonshot x4 dead,
kimi x3 with embedded-body extraction via venv python x4); estate reads: day-7 lens laws/burns/corpus/graph +
DIGEST + both kv sweep/steal cards, mag/agent_cli.py:1018-1026,
mag/context_pack.py:612-691, mag/tesuji_fire.py:135-164, mag/lite_scale.py:85-104,
mag/lane_runner.py:698-715, mag/wave_fire.py:64, tools/duel_harness.py grep,
tools/stealth_driver.py grep, memory/percolator/invariants.json (673 rows, 0
compression), memory/improve/deepseek_api/thinking_mode.txt + context_caching.txt,
memory/research_packs/bibverify/part1_tiers.jsonl; overlap greps: catalog 11
terms + memory 7 terms (commands and outputs in the session log; catalog is
1.19M rows so each memory term ran as a bounded head-3 listing).
