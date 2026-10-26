# SWEEP: kv-context-engineering via reddit - 2026-10-06

source-fetched: 2026-10-06. Runner: sweep-kv-context-engineering-reddit (subagent, dwfrun actor 3).
Research questions (from the ask): (1) Theo falsifier B, is cache-writes-dominate-spend true on
our fleet's dispatch shape; (2) strict-prefix cache-resume, law stamps appending over a
byte-identical boot prefix, and the banked cache-hit delta; (3) context-compression gateway
(2609.22114) two-axes finding transferring to mag.cmd context-pack; (4) Compaction Cliff
placement on zknot/warm_state archives vs 2608.22752, and the Open WebUI compaction-filter fit;
(5) KV q4_0 at 128k-class contexts after B4's q8_0 win, does the KV cliff move with quant level.

## Doors (measured this sitting, not assumed)

- old.reddit.com top.json on all four subs via WebFetch: welcome-page shell, zero post data
  (4/4 dead). old.reddit.com thread HTML: same shell. www.reddit.com listing and thread: bare
  "Reddit" stub. Matches the door law the burns lens already holds (burns.md:100-102: reddit
  JSON doors dead from this host).
- redlib mirrors: redlib.catsarch.com HTTP 429 (two tries), rl.bloat.cat ECONNRESET,
  redlib.privacyredirect.com and l.opnxng.com socket close. PullPush not retried (day-5
  measured hard 429-by-policy; burns.md:101).
- mcp web_reader on a reddit URL: backend rate-limited (1302), no fetch.
- WebSearch (z.ai backend): worked for DISCOVERY and supplied 7 full permalinks in one query
  ("reddit.com/r/LocalLLaMA/comments" quoted); it ignores site:/domain restriction and
  truncates most links, so permalink yield is luck-of-the-query.
- WORKING DOOR: safereddit.com (the Anubis-gated redlib instance the day-5 sibling scripted
  against) via WebFetch on /r/<sub>/comments/<id>/ pages. All 12 thread reads this sitting came
  through it, including r/LocalLLM and r/ollama threads. One transient 404 pair (1wpjhkf,
  1wz58o6) cleared on retry with the full slug. RSS door evidence reused from the sibling's
  same-run files (_localllama_rss.xml, doors/*.rss) for the candidate census only.

## Pass 1 (broad census, well over the 30 bar)

Candidates considered this sitting: 148 rows in doors/memsearch_candidates.json (dated
2026-09-05..2026-10-06, read in full via the venv python), 25 entries in _localllama_rss.xml
(newest, all 2026-10-06), top-month titles from r/LocalLLM + r/MachineLearning + r/ollama RSS
(~60 titles), 22 rows from a saferedddit month search, 7 WebSearch permalink hits. Total
considered: 260+; on-area (kv/cache/context/compaction/long-context) after dedup: 32.

Exclusions applied before banking (the day-5 same-area run is dense):
- Day-5 kv-cache-context-engineering banked ids (watch/inbox/frontier_olm_2026-10-05/sweep/
  kv-cache-context-engineering-reddit.md:35-42): 1wbgqnp, 1wdaq1v, 1wd4xxv, 1whx5xi, 1weolwq,
  1wlss89, 1wn6vwm, 1wtg12r; plus 1wiu7xj (doug.sh re-bank), and its exclusion lists from the
  09-28 sweep (10 ids), the 10-02 fold (1wr5ylm, 1wq76f6), the 10-03 sweep (16 ids incl.
  1wvxih5, 1wj0arv, 1wqxbwa), and 1wl3828 (stays sweep-level per burns.md:202).
- Today's sibling areas: 1wvz1ex, 1wekmhf excluded per the day-5 file's cross-area row;
  today's quantization-compression lane holds an active claim on generic KV-quant threads
  (their search script tmp_reddit_search.py was live at 12:16); my RQ5 bankings stay on the
  long-context KV shape those searches did not list as read.
- 1wlbqnl and 1wz3xnf appear in day-5's raw/ evidence store (thread_*.txt) but NOT in its
  banked set (day-5 Pass 2 list is the nine ids above); both re-read end to end by me this
  sitting before any banking decision. 1wlbqnl stays unbanked here (agent-memory sibling
  territory); 1wz3xnf banked below.

## Pass 2 (deep reads, 12 fetched end to end through safereddit)

In-window read and banked: 1wmucw0, 1wfdtm7, 1wwkqyb, 1wpjhkf, 1wmoqgz, 1wz3xnf.
Out-of-window read, banked flagged (both load-bearing for RQ2, dated honestly): 1qzitx1
(2026-02-08), 1rp4loz (2026-03-09).
Read and REJECTED: 1wz58o6 "New kvcache-reduction method" (2026-10-06: 3 upvotes, 62%, 14c,
screenshots only, no code, "ai slop" reception; unverifiable, trust-bytes fails) and 1wougsk
"Context compaction, measured: FutureOS vs Codex vs OpenCode" (12d ago: link-post self-promo,
2 comments, "Are you affiliated with futureOS?", zero numbers despite the measured-sounding
title). Read, out-of-window, not banked: 1qu48tt (2026-02-02, 1 upvote, 5c; conceptual
only: KV cache is not prompt cache, a 50%-cached prefix is not a 50%-shorter prompt since Q,
attention matmuls and MLP still run) and 1uzfoep (2026-07-17, KV engineering cross-model idea,
community verdict: prefix tuning/prefix caching, not KV transfer; jacksonxly + Negaaaa7).

## Banked items (strongest first)

1. **NInfer v1.3: Q4-G64 KV at true 131k on 16GB, plus a shipping "rolling-tool" prefix
   checkpoint policy for agent loops** (r/LocalLLM 1wmucw0, 2026-09-22 per "14d ago" on the
   fetched page, 96 pts/96c). toddballinger/ninfer-5080: mixed 3.95 BPW weights, Q4 G64 KV,
   118,001-token prompt measured 1380.6 tok/s prefill / 71.57 tok/s decode / MTP acceptance
   44.74%; DependentVacation358 reports 95k needle-in-haystack passes but quality degradation
   on very long generations (30-56k reasoning tokens, logically broken output); transanethole
   runs 8 concurrent 100k sessions on a 5090 and says Q4 KV quality "not as bad as I was
   expecting". The RQ2 payload is in the v1.3 changelog: a rolling-tool prefix checkpoint
   policy for agent loops, OpenClaw-tested 3 advances / 0 regressions with uncached suffix
   <4096 tokens; author describes the KV codec as signed symmetric INT4-G64 with INT8
   tensor-core QK and BF16 dequant PV. Why: this is the strongest public existence proof that
   q4-class KV holds retrieval-grade accuracy at 128k-class context, AND a shipped
   strict-prefix resume design for agent loops, the exact shape the estate's cache-resume
   play wants. Overlap: rg "NInfer v1.3" / "rolling-tool" = 0 in catalog + memory; the 45
   "ninfer" catalog rows are all nInference* tracing-instrumentation files, a different thing.
   Confidence 0.9.
2. **FP8-e4m3 KV at 147k on a 24GB 3090: 94.7% BenchLocal WITH fp8 KV, and the counter-voice
   that fp8 costs long-CoT coherence** (r/LocalLLaMA 1wfdtm7, 2026-09-14 per "22d ago", 90
   pts/38c). Altruistic_Heat_9531's vLLM AOT recipe: INT4 AutoRound weights, kv-cache-dtype
   fp8_e4m3, 147,456 ctx, prefix caching on, BenchLocal 71/75 = 94.7% (ToolCall 14/15,
   InstructFollow 15/15, ReasonMath 14/15) at reasoning_effort=low; decode 38.4 tok/s avg.
   Counter-evidence in-thread: EuphoricPenguin22 argues FP8 KV degrades Qwen 3.8's long
   chain-of-thought coherence and prefers unquantized KV at 104k (~40 t/s); Gauntlet4933 gives
   the mechanism: FP8 KV gets hardware compute acceleration while llama.cpp q8_0 KV only saves
   bandwidth. Bonus trust finding: kevin_1994 + Dsphar flag the syv-ai repo (which day-5 banked
   as a KV-approximation porter) as suspected astroturf. Why: first thread this week carrying
   BOTH sides of the KV-quant-at-long-context question with a benchmark number on each side;
   the estate's q4_0-at-128k probe should copy the bench-plus-long-CoT two-instrument design,
   not BenchLocal alone. Overlap: rg "144K FP8" / "kv-cache-dtype fp8" = 0; syv-ai is held at
   frontier_olm_2026-10-05/sweep/kv-cache-context-engineering-reddit.md:37 as a replication
   porter, the astroturf suspicion is new. Confidence 0.85.
3. **SWA / hybrid-recurrent layers are a runtime gate on prompt caching that byte-identity
   cannot fix** (r/LocalLLaMA 1qzitx1, 2026-02-08, OUTSIDE the 30-day window, flagged, 10
   pts/13c; read because it is the sharpest RQ2 evidence found). Qwen3-Next on llama-server
   reports "forcing full prompt re-processing due to lack of cache data lilely due to SWA or
   hybrid recurrent memory" [sic] even with --slot-save-path and --cache-prompt; fixes named in
   thread: llama.cpp PR 19408, drop --lookup-cache-dynamic (speculative, not prompt reuse),
   --ctx-checkpoints 69 as a partial workaround, and W61k3r reports it STILL persists with
   qwen3.6 as of Jun 16 '26. Why: the estate's strict-prefix cache-resume law stamp plan
   (burns day-4 steal) assumes byte-identical prefix is sufficient; this is documented proof
   that the runtime architecture is a second gate, so the boot-pack probe must check the
   target model's attention class, not just its prefix bytes. Overlap: rg "1qzitx1" /
   "ctx-checkpoints" = 0. Confidence 0.8.
4. **Per-request metadata silently zeroes prefix cache: Claude Code's attribution header**
   (r/LocalLLaMA 1rp4loz, 2026-03-09, OUTSIDE the 30-day window, flagged, 15 pts/17c).
   PhilippeEiffel: "Prefix cache hit rate stuck at 0.0% despite Claude Code requests sharing
   identical prefixes"; xeed's fix: set CLAUDE_CODE_ATTRIBUTION_HEADER: "0", otherwise the
   billing header breaks prefix caching; laterbreh's own fix for re-processing was vLLM
   0.17.0 + mamba-cache-mode align + performance-mode interactivity. Why: the falsifier shape
   for "identical prefix = cache hit": anything per-request in the rendered request (headers,
   tool lists, stamps) can gate the hit; if the estate ever dispatches through an API shim,
   this is the first tripwire. Overlap: rg "CLAUDE_CODE_ATTRIBUTION_HEADER" / "attribution
   header" = 0. Confidence 0.8.
5. **Deterministic state re-anchor beats trusting the post-compaction summary** (r/LocalLLaMA
   1wwkqyb, 2026-10-03 per "3d ago", 4 pts/7c). paulqq's dsh-local-long-horizon plugin:
   "Once context window compaction hits after a few thousand tokens, the model loses sight of
   the original scope"; the plugin keeps Active / Now / Next 3 / Done (with checkpoints, exit
   codes, test status) outside the chat buffer and re-anchors to that state file on compaction
   instead of trusting the lossy summary; zrail points at lllyasviel/VCC used via pi-vcc
   ("works exceptionally well and is incredibly fast"). Why: field replication of the
   compact-anchor design doc's core bet (law/state re-anchor after compaction) on the local
   stack, four days old, with a second named implementation (VCC) the estate does not hold.
   Overlap: rg "dsh-local-long-horizon" / "lllyasviel/VCC" = 0; pi-vcc itself is held at
   frontier_olm_2026-10-05/sweep/kv-cache-context-engineering-reddit.md:39, the VCC upstream
   and this plugin are not. Confidence 0.75.
6. **Practitioner census: context as scratchpad, external state in docs, prefix ordering**
   (r/LocalLLaMA 1wpjhkf, 2026-09-25 per "11d ago", 12 pts/23c). OP: context is a "temp
   scratchpad to start each step", working state lives in continuously edited docs with git as
   recall; Natrimo's top answer: "Give it only what it needs, only when it needs it";
   teachersecret: full reprocessing works but is slow, prefix caching (system prompt -> file ->
   user request) speeds iteration though stale cached data can confuse long tasks; airylizard's
   KV math: at Q8 KV a 64-layer 8-KV-head model burns ~128KB per token, so a 64k window eats
   ~8GB of 32GB VRAM before weights; o0genesis0o: never insert a message between tool return
   and assistant response, models are string completion and the multi-turn structure is
   load-bearing; thebadslime: never exceed 89k ctx with autocompaction plus salience+recency
   indexed logs. Why: this is the two-axes finding (what to keep vs what to recompute)
   re-derived in the field, with the ordering rule our context-pack composition already
   follows and one warning it lacks (stale cache on long tasks = our law-stamp refresh is a
   feature, not a bug). Overlap: rg "thinking about context now" = 0. Confidence 0.8.
7. **llama.cpp at 60k-262k real context: prefill decay, ubatch law, and single-GPU-for-agentic**
   (r/LocalLLaMA 1wmoqgz, 2026-09-22 per "14d ago", 8 pts/21c). Blindax: 27B Q8 split vs Q6
   single 5090 (2766 vs 2687 t/s prefill, ~100 vs 69.5 t/s decode), ubatch 2048->4096 = +31%
   prefill, batch=ubatch kills 2-GPU pipelining, at 262k ctx keep ubatch 1024 or the 7.1 GiB
   compute buffer spills; MTP acceptance is task-shaped (75% numeric at 5k, 73% summary at
   61k, 75% GDPR at 97k, decode decaying 128.8 -> 86.0 t/s); killerkettle: "Pcie 5x8 kill all
   prefill speed for MOE models"; Sisuuu: vLLM W4A16-FP8 does 884 t/s prefill on a 257,347-token
   prompt at 262k ctx; Dany0: single-GPU wins for agentic use since dual-GPU prefill tanks.
   Why: the B4-style q8_0 KV long-context numbers now have a public tuning envelope to sit in
   (our 100.8 t/s decode win is in-family with this thread's 69.5-100 t/s band), and the
   prefill-decay curves are the missing context for judging cache-resume savings at our
   window shapes. Overlap: rg "1wmoqgz" = 0; the 10-03 sweep banked 1wvxih5 (M4 Max) and day-5
   banked 1wn6vwm (allocated-vs-occupied); this thread is distinct. Confidence 0.85.
8. **Field failure report: repetition onset at ~16k used on a 128k window with q8_0 KV**
   (r/LocalLLaMA 1wz3xnf, 2026-10-06, 1 pt/22c). OP (Erebus-RP-12B Q6_K, --ctx-size 128000,
   --cache-type-k/v q8_0, --no-kv-offload): the model "starts to forget almost everything"
   and loops the same questions around 16k tokens used; starkruzr: "you're quantizing kv and
   you're surprised it's printing nonsense?"; Edenar: keep KV 16-bit for long context;
   Emotional-Package-91's alternative diagnosis: RP finetunes trained on 4k-16k-token samples
   enter repetition loops past their training density. Why: a same-week field datapoint that
   the degradation cliff can sit at ~12% of the advertised window on a small finetune, with
   the KV-quant and finetune causes NOT isolated; it constrains our Compaction Cliff placement
   work (the cliff is not at the window edge) and warns that B4's q8_0 win must be re-proved
   per model family, not assumed. Confound stated: single 1-point thread, RP finetune, no
   controlled A/B. Overlap: rg "Only 13 % of context" / "1wz3xnf" = 0; day-5 fetched the
   thread into raw/thread_1wz3xnf.txt but never banked or analyzed it. Confidence 0.7.

## Findings against the five research questions

- RQ1 (Theo falsifier B on our receipts): reddit contributes NO direct spend measurement this
  window. Closest color: 1wmoqgz shows local long-context workloads are prefill-dominated
  (prefill t/s 20-40x decode t/s at 97k-262k), which is the local mirror of the cache-write
  cost question, and 1qu48tt's OP cautions a 50%-cached prefix is not 50% cheaper. The
  falsifier stays OWED on our own usage.jsonl; nothing here lets us bank or kill it.
- RQ2 (strict-prefix cache-resume): the byte-identity assumption survives, but two NEW gates
  surfaced that sit between identical prefix bytes and an actual hit: runtime attention class
  (SWA/hybrid forces reprocess, 1qzitx1, still broken on qwen3.6 in June) and per-request
  metadata (attribution header zeroes hit rate, 1rp4loz). The positive proof the shape ships
  is NInfer's rolling-tool prefix checkpoints with uncached suffix <4096 (1wmucw0). Estate
  probe update: the boot-pack byte-identity test must be joined by an attention-class check
  and a rendered-request diff (headers + tool list + stamp placement), and the cache-hit delta
  it banks should be modeled on 1wmoqgz's prefill-decay curves, not flat prefill t/s.
- RQ3 (two-axes transfer to context-pack): transfers cleanly. 1wpjhkf is the field version of
  2609.22114: keep = persistent docs + pinned prefix (system -> file -> request), recompute =
  per-step scratchpad reload; the new sharpening for context-pack is o0genesis0o's
  never-insert-between-tool-return-and-assistant rule (our pack builder must not interleave
  pack blocks into the turn sequence) and teachersecret's stale-cache warning (a refreshed law
  stamp intentionally breaks cache; price it, do not avoid it). sburel in 1wqa5da prices the
  per-request relevance check: a second model call per turn vs a cheap keyword match that
  misses, the same keep-vs-recompute axis at the pack-selection layer.
- RQ4 (Compaction Cliff placement, Open WebUI pattern): field placement is far below the
  window: repetition onset ~16k used on a 128k window (1wz3xnf, confounded), scope drift
  "after a few thousand tokens" of compaction cycles (1wwkqyb), and /compact called
  session-killing with DCP (dynamic context pruning, opencode-dynamic-context-pruning)
  recommended instead (Atretador in 1wqa5da; rg "dynamic context pruning" = 0, unheld). The
  Open WebUI summarize-on-threshold pattern has no defender in any thread read this sitting;
  the recurring winner is deterministic external state re-anchored after compaction
  (1wwkqyb, pi-vcc via zrail), which is exactly our compact-anchor design and the zknot
  law-stamp append shape.
- RQ5 (KV q4_0 at 128k, does the cliff move with quant level): convergent answer at 27B:
  q4-class and fp8 KV hold retrieval/bench accuracy at 128k-147k (94.7% BenchLocal with fp8 KV
  at 147k; 95k NIAH passes with Q4-G64 KV) while TWO independent threads report the loss
  appears in long-form generation, not retrieval (30-56k reasoning tokens degrade, 1wmucw0;
  long-CoT coherence, 1wfdtm7). So the cliff moves with quant level and shows first in
  generation length. No 7b-specific KV-q4_0-at-128k measurement surfaced on any door this
  sitting; the estate's owed scoped qwen2.5:7b A/B (burns.md:209) stands, and NInfer's INT4-G64
  codec (INT8 QK / BF16 PV) is the concrete mechanism to port for it.

## Not run / not found (no fabrication)

- r/MachineLearning top-month RSS reused from the sibling's file was all off-area (NeurIPS/
  training threads); no ML-only KV thread surfaced on any door this sitting.
- The "Small compaction model next to Qwen3.8-27B in dsh" thread (seen once as a WebSearch
  snippet, day unknown) was never located on a fetchable door despite two searches; not banked.
- The tiny-compaction-model thread's content is known only from that search snippet; its
  question (is a 4B summary model good enough) is folded here as UNVERIFIED color only.
- DeepSeek cache-hit/miss pricing threads (1n12aqj class) surfaced as search snippets only;
  not read, not banked.
- 1qzitx1 and 1rp4loz are outside the 30-day window; banked anyway as flagged, dated honestly,
  because they are the only RQ2 gate evidence found on any door this sitting.
- No direct cache-spend-vs-cache-write measurement found anywhere in the window (RQ1 stays
  open on our own receipts).
