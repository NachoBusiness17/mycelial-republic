# Sweep: kv-cache-context-engineering via reddit (2026-10-07)

source-fetched: 2026-10-07. Seat: sweep-kv-cache-context-engineering-reddit (frontier_olm_2026-10-07). House
laws held: ascii-only in my own prose (verbatim source quotes keep their original characters), no em or en
dashes of my own, every claim cites the record fetched this sitting, anything unverifiable marked OWED.

## Door record (degraded primary, per recipe)

1. `old.reddit.com/r/LocalLLaMA/top.json?t=month&limit=50` and the r/MachineLearning twin: WebFetch
   returned the "Welcome to Reddit" landing shell, zero posts. A second fetcher (mcp web_reader) showed the
   wall explicitly: "Log in to use old Reddit. To keep Reddit safe, accounts are required to access old
   Reddit." Same for the HTML variant `/top/?t=month` on r/LocalLLaMA and r/LocalLLM.
2. `www.reddit.com/r/LocalLLaMA/top.json`: "You've been blocked by network security" (webReader). Thread
   HTML on www via WebFetch: empty "Reddit" shell. `r.jina.ai` proxy of a thread: the same reddit
   network-security 403.
3. redlib mirrors: catsarch 429, perennialte 403, rl.bloat.cat ECONNRESET.
4. `api.pullpush.io`: the ids= lookup worked once (DKV 1v5wviz, full selftext), then the search endpoint
   429'd on every retry, from both WebFetch and a local urllib client.
5. WORKING DOORS this sitting: `arctic-shift.photon-reddit.com/api/posts/search` (quoted-phrase queries,
   newest-first, intermittent null-data responses that need retry+pace), `/api/posts/ids`, and
   `/api/comments/search?link_id=`. This matches the door log of today's sibling
   quantization-compression-reddit sweep (same file dir, line 13) and the estate's standing record that
   every Reddit JSON door is dead (lens/burns.md:211-212).
6. Recipe fallback WebSearch `site:reddit.com`: used for discovery; several calls died in 429/1302
   rate-limit storms and were retried paced; results drifted off-reddit, so the arctic-shift matrix was
   the real census instrument.

No fallback success is fabricated: every failed door above is recorded as failed.

## Pass 1 (broad sweep; 519 unique in-window candidates)

Instrument: a local Python matrix (urllib, paced, written this sitting at
C:\Users\foste\AppData\Local\Temp\as_fetch.py) over arctic-shift posts/search: 4 subreddits
(LocalLLaMA, MachineLearning, LocalLLM, ollama) x 17 quoted queries (kv cache, kv-cache, kv cache
quantization, prompt cache, prefix cach, cache reuse, context compaction, compaction, context
engineering, context pack, summariz context, rag vs long context, long context vs rag, context window,
sliding window, attention sink, mla), 3 pages each, locally filtered to created_utc >= 1788739200
(2026-09-07). Output: 519 unique in-window submissions (raw digest kept at
C:\Users\foste\AppData\Local\Temp\as_sweep_out2.txt), sorted by score. Plus WebSearch site:reddit.com
discovery (the DKV/TurboQuant/UL-compression cluster, all already known, see overlap). Well past the
30-candidate minimum; the full digest enumerates them.

Honest window note: the r/LocalLLaMA in-window surface is dominated by the Qwen 3.8 / Flash-Next
hardware wave; the KV/context-engineering threads are mostly 1-25 pt niche posts, and the three
highest-signal ones I shortlisted were killed by moderators or emptied (below). Scores are the
archive snapshot, not live.

## Pass 2 (deep reads: 16 threads read end to end; 8 bankable)

Two batches via arctic-shift posts/ids + comments/search (raw JSON banked in this dir under tmp/:
post_<id>.json and comments_<id>.json for all 16). Content-dead on arrival, recorded not banked:
1wyqjsc "I Cast 'Forget' on 98% of the KV cache. The model still passed RULER" (2026-10-06: selftext is
one sentence, the benchmark lives in an image I cannot read); 1wixud0 "attention dilution mathematical
analysis" (2026-09-17: [removed] by AutoModerator karma gate); 1wpqlhj "entail declaration-vs-execution
checks" (r/ML, 2026-09-25: [removed] rule 5); 1wvwdn1 anzar09 needle-retrieval re-post (2026-10-02:
[removed]); 1wv0b24 KV-connector-persists-to-disk (2026-10-01: empty selftext, zero comments). The
removal pattern is itself a finding: the only in-window reddit attempts at a mathematical
compaction-degradation treatment and an inference-stack correctness checker are both gone from the
platform, preserved as titles only in the archive.

### Banked items (strongest first; quotes verbatim from the fetched archive records)

1. **MTP + prefix caching still broken on Arc Pro B70 (llm-scaler 0.26.0-b2), filed intel/llm-scaler#741**
   (r/LocalLLM 1wwp0q8, 2026-10-03, 4,832-char methodology + 2 comments).
   https://www.reddit.com/r/LocalLLM/comments/1wwp0q8/mtp_prefix_caching_still_broken_on_arc_pro_b70/
   The RQ2 correctness core: under MTP + prefix caching, 8/8 fixed-seed serial-vs-serial output hash
   mismatches (and the no-spec control 0/8), an EngineCore death under concurrent shared-prefix traffic,
   superlinear MTP prefill on the pinned build (TTFT 7.5s @2.4K to timeout @19K), the drafter silently
   autoselecting FLASH_ATTN against an FP8 KV target, and the methodology law the estate should steal:
   quality evals passed 100% in both arms while determinism was broken. Also in-thread: 92.7% draft
   acceptance over 27K drafts, +11-22% end-to-end decode; and the operator's priority ordering for
   agentic fleets: "prefix caching matters more than speculative decoding". Quote: "Both arms scored
   100% on quality evals - a quality pass does not certify determinism. The fixed-seed hash compare is
   what surfaced it." Overlap: rg "llm-scaler" over catalog + frontier_olm days + memory mining
   surfaces: only harvest pools (10-04 _amc, 10-03 tmp, 10-06 doors); never banked. NEW.

2. **Context Language Models: model-edited context instead of compaction** (r/LocalLLaMA 1wyf63m,
   2026-10-05, sc=103, 41 comments read).
   https://www.reddit.com/r/LocalLLaMA/comments/1wyf63m/yall_this_is_a_sexy_paper_context_language_models/
   Paper arXiv 2609.37725 + authors' pi plugin (github.com/lolipopshock/pi-clm). The harness exposes the
   context as a file the model edits on the go; pros per OP: better long-task outcomes, compute and
   wall-clock efficiency (dependent on an inference-engine cache optimization that exists only for
   SGLang), less context bloat, "No more slow and unreliable compacts"; cons: SGLang-only optimization,
   prompt injections persist (are much less likely to be forgotten), needs harness customization;
   tested qwen3.6-9b, qwen3.8-27b, claude sonnet 4.6, works better on larger models. The technical
   caveat a commenter adds is the KV-splice truth: recompute only the changed span, splice the partial
   KV into the old cache, re-rotate keys for length shifts, everything after the edit runs on stale
   values; the paper claims accuracy holds. This is the live third way between full re-prefill and
   lossy summaries, directly relevant to the CONTEXT-PACK propagation gap and the context pack as a
   droppable tour guide. Quote (u/wishstudio): "Its 'optimization' is basically only recomputing
   changed part and splicing the resulting partial kv cache to the original one. So anything after
   the changed part is kind of using stale values." Overlap: rg "2609.37725" -> only a 10-03 X-lane
   OWED-hn pool mention (story 49922437) and pools; never banked as an item. NEW.

3. **KV cache transplants across quantizations (start big, swap down) + CacheBack retained-positions
   lead** (r/LocalLLaMA 1wq76f6, wadeAlexC, 2026-09-25, 11,498-char methodology, 28 archived comments).
   https://www.reddit.com/r/LocalLLaMA/comments/1wq76f6/qwen3827b_using_kv_cache_transplants_to_boost/
   Builds on Cache-to-Cache (arXiv 2510.03215; agent-to-agent KV fusion). The reddit delta: reuse a KV
   cache BETWEEN quants of the same model, no converter net: run Q6_K f16 early, hot-swap to Q4_K_XL
   then IQ3_S as context grows (with mid-run f16<->q8_0 KV conversion), and the dynamic ladder beats
   the matching static small-quant strategy on his NIAH suite (dozens of tasks, 5 strategies, 14-15 GPU
   hours; correctness table included; author flags small n). Comment thread adds: Dany0's 26-pt
   hypothesis that this is how frontier providers degrade under load; and u/maxr0ssi naming CacheBack
   (agentcacheback.github.io), training-free retained-position selection for agent handoffs, explicitly
   untested in combination with the transplant ladder. That is the retained-token-count frontier
   (BreadthKV's question, lens/burns.md:111-114) showing up as an un-combined axis on reddit. Quote
   (u/maxr0ssi): "Have you also considered reducing the number of retained positions? We've been
   exploring that for agent handoffs, using the receiving agent's request to select what to send. Our
   method, CacheBack, is training-free." Overlap: Cache-to-Cache paper itself is HELD
   (memory/corpus/LINKS.jsonl LINKS-278, DISPUTED tag, per the 10-05 kv-hn sweep line 31); CacheBack
   appears only inside a 10-03 X-lane raw harvest (q7_agent.xml), never banked; the transplant
   experiment itself has zero prior hits. NEW with stated overlap.

4. **"Is there a coding harness that will not invalidate the entire context cache at each prompt?"**
   (r/LocalLLaMA 1wi17z6, Academic-Tea6729, 2026-09-16, 35 comments read).
   https://www.reddit.com/r/LocalLLaMA/comments/1wi17z6/is_there_a_coding_harness_that_will_not/
   The byte-identical-prefix law's practitioner echo, in-window. OP: Cline and the Qwen VS Code addon
   invalidate a 100k-token context cache on trivial requests ("please update the md file" -> 40 s
   re-prefill), older versions did not. Field answers: Pi Coding Agent recommended top (27 pts);
   "any decent agent shouldn't do this shit in 2026" (13 pts); a harness bug is one cause but so is
   inference config: llama.cpp invalidated long-context checkpoints when KV was RAM-heavy until the
   commenter raised checkpoint cache count and KV RAM to 64 GB; OpenCode truncates tool-call responses
   mid-context to save API tokens, forcing local re-prefill every tool call (a cloud-cost vs
   local-prefill trade the estate's law already prices); a separate user reports OpenCode cache hit
   rates 92-98%; and the preserve_thinking chat-template kwarg matters for cache survival. Quote (OP):
   "I don't think it's normal to invalidate 100k of context cache for no reason." Overlap: phrase grep
   found only harvest pools; not banked on any prior day. NEW.

5. **phantom-kv: trained KV-cache bank injection, with a measured decay half-life** (r/LocalLLaMA
   1wms904, Anony6666, 2026-09-21, sc=416, 2,090-char selftext + 59 comments read). This fires the
   deep-read the 10-02 quant sweep explicitly OWED (its line 67: "1wms904 phantom-kv selftext not read
   this sitting; worth a next-window deep read").
   https://www.reddit.com/r/LocalLLaMA/comments/1wms904/uncensor_an_llm_without_touching_weights_inject_a/
   An 18 MB learned KV bank loaded into the KV cache as context: no weight edits, no runtime hooks,
   per-request hot-swappable, base model byte-identical on unload. The estate-relevant part is the
   self-audit: an 8B-judge audit found lexical refusal metrics over-claim compliance (semantic refusal
   persists as rephrasing), and the graft DECAYS in long sessions with a measured half-life and a
   re-injection cadence that mitigates it. Comment tree: the 119-pt explanation of why this is not a
   system prompt (prefilled KV bytes bypass the weights' censored trajectory entirely), the LoRA-like
   reading (cache content as fine-tunable-but-frozen-model parameters, Square_Alps1349), and the
   steering niche (author-mimicry banks, BannedGoNext). For the estate: this is the measured-lifetime
   datapoint for any skill/KV-injection scheme (cf. the "injecting skills into the KV cache" idea the
   search surfaced) and a caution that injected context fades over long agentic sessions. Quote (OP
   self-audit): "the graft fades with a ~2-4k token half-life in long sessions (and a measured
   re-injection cadence mitigates it)". Overlap: phantom-kv named in the 10-02 sweep only as
   title-only-not-read; the 10-06 doors file holds a thread_d8 HTML fetch (pool). Deep read is NEW.

6. **Adaptive KV-Cache Streaming V2 with full-context MTP** (r/LocalLLM 1wt03zh, raymondh210129,
   2026-09-29, sc=23, 4,525-char methodology + 33 comment records).
   https://www.reddit.com/r/LocalLLM/comments/1wt03zh/adaptive_kvcache_streaming_v2_full_context_mtp/
   llama.cpp fork: streaming KV eviction with an explicit memory-ownership/leasing layer (backend
   neutral), MTP draft KV as a 17th logical attention layer sharing the main resident pool and ring
   buffer (host-resident history, pinned-memory rollback snapshots), keeping the effective decode KV
   pool ~2.2 GiB at 256K context with draft length 3; decode 82 tok/s avg 8K-72K, 19 tok/s at 256K on
   a 5070 Ti; the span-aware kernel follows stock calculation order to minimize numerical drift, and
   the author reports decoded-256-token output equality with the stock kernel per MTP setting.
   Caveats: MTP must share the main model's K/V quant; author declines to upstream; Wikipedia-file
   acceptance test is favorable-case. Independent in-tree replication: tsangberg gets ~50 t/s low
   context, ~40 above 160k, Qwen 3.8 27B IQ4_XS on a 5060 Ti 16GB. This is the streaming-eviction +
   spec-decode composition the estate's KV ladder wants numbers for. Quote (OP): "The decoded 256
   tokens at each MTP setting is exactly same as what stock kernel outputs." Overlap: rg
   adaptive-kv-streaming -> only pools. NEW.

7. **DeepSeek V4.1-Flash SWA bounded replay: recall degradation verdict** (r/LocalLLaMA 1wcywl4,
   Top-Handle-5728, 2026-09-10, sc=11, 803-char question + the one answer that matters).
   https://www.reddit.com/r/LocalLLaMA/comments/1wcywl4/is_deepseek_v41flashs_swa_replay_a_free_lunch_or/
   The sink/sliding-hybrid lineage question asked precisely: V4.1-Flash discards the SWA KV and
   approximately reconstructs it on replay from only the last N_window tokens, losing the depth-shaped
   receptive field; does the parallel global KV compensate? The single practitioner answer (u/
   mostly_idempotent): rebuild degradation was significant enough to impact overall system
   reliability. RQ1's correctness edge for hybrid-attention models under session restart / cache miss,
   in one measured verdict. Quote: "Our testing showed significant enough degradation on KV rebuild
   that it impacted overall system reliability. Not a free lunch (yet)." Overlap: rg "SWA replay" ->
   pools only. NEW.

8. **The compaction re-prefill tax, measured across 10 rigs** (r/LocalLLaMA 1wrul9r,
   Express_Quail_1493, 2026-09-27, 15 comments).
   https://www.reddit.com/r/LocalLLaMA/comments/1wrul9r/qwen38flashnext_please_share_cold_prefill_at/
   The OP names the exact blind spot the estate's count-compactions KPI prices: everyone shares decode
   and clean prefill numbers, nobody shares prefill at compaction boundaries. The comment census
   (self-reported, mixed engines): FreeToken 5,133 tok/s on a 139K prompt (5090 + 160 GB); ExLlamaV3
   6.05bpw 819/585 t/s interval-cumulative on a 192K prompt; 3,026 t/s @32K on 4x3090 patched vLLM;
   ~450 semi-cold (expert cache warm) on 3090+2x3060; ~900 tok/s M3 Ultra with ANE prefill; ~2,700
   tok/s dual RTX 4000 Pro; and the llama.cpp tail: 200-220 t/s at 16K degrading to 20-40 t/s at 200K
   context ("abysmal", u/milpeter). That tail is the compaction tax on the estate's own engine class:
   every compaction on a llama.cpp-served long session re-buys a prefill at 20-40 t/s. Quote (OP):
   "no one is sharing their prefill speed when the harness is COMPACTING". Overlap: rg the phrase ->
   pools only; the 10-05 sweep banked the count-compactions KPI concept from a different thread
   (1wlss89), this is the numbers census. NEW.

### Ops note (recorded in full, not one of the 8 items)

**LMCache phones home by default** (r/LocalLLM 1wzhtld, 2026-10-06, 1,391 chars + 4 comments):
stats.lmcache.ai, ~18 connections/hour, on-by-default usage telemetry gated by
is_usage_tracking_enabled() in usage_telemetry/identity.py; disable with LMCACHE_TRACK_USAGE=false or
DO_NOT_TRACK=1. Directly relevant to the estate's 2,333-row corpus/library/lmcache-src shelf and any
LMCache adoption. rg "stats.lmcache.ai" -> zero estate hits. NEW, filed here because it is ops rather
than an area item.

## What this answers of the five questions

- Q1 (KV compression under long agentic sessions; retained-token frontier): reddit in-window adds four
  families beyond the estate's banked BreadthKV/LORE-KV/Lachesis axis: cross-quant KV transplant
  ladders (1wq76f6), KV-as-injected-context with measured 2-4k-token half-life (1wms904), streaming KV
  eviction composed with MTP on one pool (1wt03zh), and the SWA-replay rebuild cost on hybrid
  attention (1wcywl4). On retained token count specifically: nobody on this door posts a
  retained-tokens-vs-accuracy table; CacheBack is named (in the transplant thread) as training-free
  retained-position selection for handoffs, explicitly untested against quant ladders. That
  combination (selection + quantization) is an open seam the estate could fire cheaply.
- Q2 (prompt-cache correctness and invalidation): the strongest window evidence is methodological:
  fixed-seed hash comparison is what exposes MTP+prefix-cache nondeterminism that 100%-passing quality
  evals hide (1wwp0q8) - the estate's own byte-identical-ask law and the sibling HN lane's provider
  docs both get a practitioner enforcement instrument. 1wi17z6 adds the harness-side invalidation
  census (Pi/Hermes clean; Cline/Qwen-addon dirty; llama.cpp checkpoint RAM sizing as a silent
  invalidator; OpenCode's tool-response truncation as a deliberate API-cost-vs-local-prefill trade).
  Adjacent, in the write-up's pools: vLLM's "cached block exists only after its prefill completes"
  warm-then-fan-out rule (1wtyc4y, bot-flagged OP, doc-cited answer).
- Q3 (compaction preserving continuity): the reddit window's contribution is cost-shaped, not
  fidelity-shaped: the compaction re-prefill census (1wrul9r) prices every compaction event on the
  estate's engine class; the CLM thread (1wyf63m) is the in-window "replace compaction with
  model-edited context" datapoint with its stale-values and SGLang-only caveats; the Warm Compaction
  post (1wzlqac) is a title-only lead (empty body in the archive) for cache-preserving compaction on
  Hermes Agent, of direct estate interest, OWED a real read if a body surfaces. Fidelity measurements
  remain held by the 10-05 bank (Crucible instruction-loss) and today's HN lane (FutureOS/Codex/
  OpenCode); nothing new on reddit this window.
- Q4 (long-context vs retrieval at local scale): no in-window measured long-context-vs-retrieval
  comparison surfaced through this door. The nearest evidence stays cost-side (1wrul9r prefill
  curves; the Qwen-Flash-Next hardware wave's implicit answer that RAM-tiered KV is beating
  retrieval-shy contexts at 128K-1M). OWED: this question is better served by the arxiv lane (EDAR,
  UNREAL banked today by the sibling).
- Q5 (guide/summary abstraction information loss): phantom-kv's self-audit is the discipline datapoint
  (lexical metrics over-claim; semantic content persists as rephrasing) for any
  abstraction-then-measure loop; the CLM thread supplies the abstraction-without-summary alternative
  with its own measured claim (accuracy holds under KV splicing, per the paper, disputed in-thread).
  The one direct mathematical treatment (attention dilution) was removed by moderators before content
  survived; if an off-reddit copy exists it is OWED.

## Overlap ledger (commands run this sitting)

rg -i over catalog/catalog.jsonl + all frontier_olm_2026-09-30..10-07 day dirs + memory/burns,
memory/frontier, memory/percolator, memory/lenses, memory/press, memory/research_packs, memory/steal:
BreadthKV (held: 10-06/10-07 lanes, day-6 register), TurboQuant (held: 9 catalog rows, vendored
lmcache-src serde), DifferentialKV/DKV (held: listed in the 10-02 pass-1), KVarN (held), Spomin (held:
10-05 item 2), Crucible/1wbgqnp (held: 10-05 item 1), KV-approximation wave (held: 10-05 item 3),
tcclaviger (held: 10-05 item 8), FP8-KV-preempting study (held: today's inference-efficiency-hn
line 47, HN twin of the 2muchgut reddit post - excluded here), phantom-kv (title-only prior, deep read
now fired), Cache-to-Cache paper (held, LINKS-278), 2609.37725 (pools only), llm-scaler (pools only),
CacheBack (one raw X harvest only), adaptive-kv-streaming (pools only), SWA replay (pools only),
Warm Compaction (zero hits). Also excluded as known: today's sibling kv-hn and kv-arxiv banked items
(FutureOS compaction measured, vLLM prefix keepalive, context rot, LensVLM, Yandex KV runtime,
LORE-KV, Lachesis, ReFold, EDAR, UNREAL, MII).

## Not run / OWED

- The r/LocalLLaMA karma gate and r/ML rule 5 killed the three most on-question submissions
  (attention-dilution analysis, entail correctness checks, needle-retrieval-vs-perplexity post); their
  content does not exist on reddit anymore. If the entail tool or the dilution analysis exists on
  GitHub/arXiv, an arxiv/github-lane sweep owes them a look.
- 1wzlqac Warm Compaction: title claim only (3-4x faster compaction via prompt-cache reuse on Hermes
  Agent); body empty in the archive. Re-pull when a body or repo link surfaces.
- 1wyqjsc RULER-at-98%-eviction claim: benchmark is an image; unreadable here.
- No live-reddit cross-verification was possible (all live doors blocked); dates/scores/quotes are
  arctic-shift archive snapshots, same instrument class the 10-04/10-05 sweeps graded at 0.8-0.85.
