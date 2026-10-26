# inference-efficiency via X - sweep 2026-10-09

Lane: sweep-inference-efficiency-x (frontier_olm_2026-10-09). Doors: WebSearch (site:x.com queries) then the fxtwitter door `https://api.fxtwitter.com/<user>/status/<id>` for resolution. Stamp: source-fetched: 2026-10-09.

## Door status (never fabricated)

- fxtwitter resolved 11/11 single-status fetches this session with created_at dates: ziv_ravid (article-summary), ZhihuFrontier, mikenevermiss (article-summary), nathanhabib1011 (article-summary), cv_usk, RMladek, sgl_project, rohanpaul_ai, _avichawla, cybernetic_lab (article-summary), llm_frontier_jp. Zero 403/404s on the single-post door.
- Three of those resolve to link-only tweets whose bodies are just an x.com/i/article URL (mikenevermiss, nathanhabib1011, cybernetic_lab, llm_frontier_jp); for those the article content rides the fetch's summary or the search snippet, labeled as such per the fetch recipe. The Strata README was fetched directly from the cited GitHub repo (github.com/Niko1221/Strata) to get byte-verbatim lines.
- WebSearch: 1 query timed out at the 60s limit (EAGLE-3 speedup); 1 query hit an upstream 1302 rate-limit once and the tool retried successfully on its own (disclosed by the tool); all other queries clean. No fabricated fallback success.
- Post dates were verified two ways: fxtwitter created_at for fetched posts, and repo-python snowflake math (`ts_ms = (id >> 22) + 1288834974657`) for the rest. One search-returned id (karan_prefill 2100258037223223) decodes to 2010-11-09 - a mangled id, discarded rather than guessed.

## Pass 1: candidates considered (broad sweep, 30+)

~71 candidates scanned across 9 site:x.com searches (speculative decoding; vLLM continuous batching; SGLang throughput; llama.cpp local speedup; KV cache/LMCache; Groq/OpenRouter free tiers; DeepSeek serving economics; vLLM release benchmarks; llama.cpp/Ollama October improvements).

Date discipline (30-day window = 2026-09-09..10-09): in-window verified includes ZhihuFrontier 10-02, llm_frontier_jp 10-03, RMladek 09-26, rohanpaul_ai 09-16, sgl_project 09-15, cv_usk 09-13, _avichawla 09-09, inferact/vLLM B300 repost ~09-17. STRONG but OUT of window, read as context and NOT banked: ziv_ravid DSpark explainer 07-11 (DSpark: bigram-head drafter beats Eagle3 27-31% accepted length + throughput-aware confidence scheduler); DFlash 2 08-18 (4.6x block-diffusion drafting; llama.cpp/SGLang/vLLM support per Zhijian Liu/testingcatalog snippets); Hyperbolic serving bake-off (2025-04); Banghua 12K tok/s/GPU 06-12; akshay_pachaar KV/LMCache articles 06-07 to 07-07; mikenevermiss free-resource census 08-20 (Groq ~30 req/min, ~6,000 tok/min); nathanhabib1011 "Stop benchmarking Inference Providers!" 04-13 (transformers continuous batching ~80% of vLLM; benchmark-the-provider-not-the-model warning); cybernetic_lab "Robot inference is not LLM inference" 09-08 (one day out of window; continuous batching does not fit hard-deadline workloads - a useful counter-law for our fixed-shape janitor lanes).

## Pass 2: deep reads (fetched through fxtwitter this session)

11 posts fetched and read end to end: the 8 banked below plus ziv_ravid (07-11), mikenevermiss (08-20), nathanhabib1011 (04-13), cybernetic_lab (09-08) - the latter four dated out of window, kept as context only.

## Overlap / dedupe record (grep catalog/catalog.jsonl + memory/)

- The day-8 mine's own X lane (`watch/inbox/frontier_olm_2026-10-01/sweep/inference-efficiency-x.md`) already banked TeksEdge DSpark 3.13x (09-25), AA Cyber Index Pareto (09-28), Ember-1, kunchenguid, Oluwaphilemon1, theneurondaily GLM tok/s, pseudokid, exolabs. NONE of my banked items duplicate those.
- cv_usk's paper is ALREADY VENDORED: catalog/catalog.jsonl:443903 -> `state/arxiv/2026-09-11/2609.11744v1.txt` ("Building py-kvcache: A Performance Characterization of External KV Caching for vLLM with NVMe SSDs"). Banked only for the X post's break-even-gate reading; overlap recorded on the item.
- LMCache is heavily held (3,427 catalog lines; `corpus/library/lmcache-src` vendored source; `memory/research_polished/kv_cache_compaction.md` covers CacheBlend). The _avichawla 09-09 LMCache-as-a-standalone-service post is therefore NOT banked - re-banking known work.
- "HiCache" and "Cognos": 0 catalog/memory hits (Cognos matches only Gutenberg fiction noise). "Draft Fast": 0. "gross margin": 0. "B300": 0 (the LEDGER.jsonl hit was the hex hash "db3005", a false positive). "Strata": 0 catalog hits (memory hits are unrelated estate artifacts). "TurboQuant": name collision with lmcache-src's serde docs (`corpus/library/lmcache-src/docs/design/v1/distributed/serde/turboquant.md` et al.) - different artifact from the X posts' KV-compression claim; flagged on the item.
- Mozilla: 11 catalog hits, all `memory/corpus/ai_canon/chapters/dlb_*.html` footnote noise; the 91-page Mozilla AI report itself is not held.

## Banked items (8, strongest first)

### 1. ZhihuFrontier, "Draft Fast, Verify": the serving cost of speculative decoding (2026-10-02)
URL: https://x.com/ZhihuFrontier/status/2106038772123197700
Quote (verbatim, fxtwitter): "Auxiliary modules: Methods such as EAGLE and MTP use additional components tied to the target model."
Why: the drafting/verification ledger the ladder needs before arming local specdec: drafting and verification both cost compute, serving engines need extra KV-cache space and must roll back rejected positions; the real trade is draft cost vs tokens surviving verification. Three draft classes named (separate draft model, auxiliary modules, pattern matching). This prices the overhead that DFlash-in-llama.cpp headlines omit - the difference between a 3x decode claim and a net win on a gemma:2b janitor. Overlap: "Draft Fast" 0 in catalog/memory; the day-8 X lane read a DIFFERENT ZhihuFrontier post (Qwen3.8-Max pricing card, 08-03, out of window, unbanked). NEW. Confidence 0.85.

### 2. RMladek, 23-part token-selling economics thread (2026-09-26)
URL: https://x.com/RMladek/status/2103977307186868402
Quote (verbatim, fxtwitter): "selling tokens is a ~10 to 25% gross margin business"
Why: the macro frame for the driving ladder. Labs own the models and still clear 10-25% gross; "both labs spend 2.5x to 4x their api revenue on training"; margin sits at the compute layer (one lab rents GPUs, another runs ~100,000 Chinese chips); volume is unstable (one lab dropped 75% of its OpenRouter tokens in ten weeks, another captured 31% of the platform in six days with a free model); "capability is the only pricing power". Estate read: funded remote inference is a reseller-shaped cost with someone else's margin baked in; the local-janitor layer is where margin can actually be captured. Overlap: "gross margin" 0 in catalog/memory; the day-8 lanes held per-task costs (AA Cyber Index) but no lab-margin macro. NEW. Confidence 0.85.

### 3. SGLang + Samsung, HiCache x Cognos whitepaper (2026-09-15)
URL: https://x.com/sgl_project/status/2099667204644237657
Quote (verbatim, fxtwitter full text): "delivering up to 3.1x lower latency and 2.2x higher throughput on the same GPU hardware"
Why: KV-tiering leaves the research-paper stage: SGLang HiCache + Samsung Cognos "extend GPU memory with a composable AI Memory Node" on the same hardware - the same tiering the estate vendors as LMCache source, now shipping inside a mainstream engine with a joint whitepaper. Direct input for the ds_workhorse batch lane: if prefix-heavy agent workloads get 3.1x on unchanged GPUs via KV tiers, the estate's context-pack reuse discipline has an engine-grade precedent. Overlap: "HiCache" 0 and "Cognos" 0 relevant hits in catalog/memory. NEW. Confidence 0.9.

### 4. Rohan Paul on Mozilla's 91-page open-weight AI report (2026-09-16)
URL: https://x.com/rohanpaul_ai/status/2100344356737806825
Quote (fetch-summary grade: the post text exceeded the fetcher's quoting limit; numbers as returned by the fetch): "8 of OpenRouter's top 10 models by token volume were open-weight"
Why: quantifies the free/open lane the digest's rows ride: open models ~20% of usage but ~4% of model-layer revenue; closed models cost ~6x more per call at ~90% capability parity; open-weight lags frontier by ~4 months; 79% of developers use open models but only 51% of open deployments reach production. The 6x-price/90%-parity pair is the cleanest third-party anchor yet for "janitors first, funded remote only for judgment". Overlap: "mozilla" 11 catalog hits, all ai_canon chapter noise; report not held. NEW with caveat (quote summary-grade, report unread end to end). Confidence 0.65.

### 5. cv_usk on py-kvcache: external KV caching has a break-even gate (2026-09-13)
URL: https://x.com/cv_usk/status/2099121418042855434
Quote (fxtwitter, quoted phrase from the post): "near-full SSD read bandwidth of 13.5GB/s"
Why: the counter-law to naive KV offload, and it rhymes with estate law: io_uring on NVMe reaches near-full SSD bandwidth, "scheduler-aware preloading" plus a "break-even gate" skip loads that would not improve TTFT; 6.02-7.43x over GPU recompute and 2.77-3.64x over LMCache on LongBench, but external caching wins on low-end GPUs (RTX 4000 Ada) and "often isn't worthwhile on an H100". Gate-don't-refire is exactly the inference-budget terminal rule's shape (mag/inference_budget.py:19). Overlap: PAPER HELD - catalog/catalog.jsonl:443903 -> state/arxiv/2026-09-11/2609.11744v1.txt; banked only for the post's break-even-gate reading and hardware-specific verdict. PARTIAL. Confidence 0.8.

### 6. llm_frontier_jp, "Is the 'Fit Everything in VRAM' Era of Local LLMs Ending?" - Strata x TensorFold (2026-10-03)
URL: https://x.com/llm_frontier_jp/status/2106438851267019246
Quote (verbatim, from the article's cited repo README, fetched at github.com/Niko1221/Strata): "Run a 125-billion-parameter AI model on your own gaming PC"
Why: the local-janitor thesis gets a consumer-engine existence proof beyond quantized dense models: Strata (MIT) runs Qwen3.8-Flash-Next, a 125B MoE (24,576 experts, 10 active per token), on a 12GB GPU by splitting experts across GPU/RAM/CPU, with a speculative-decoding helper for "1.6-1.8x sooner" answers and OpenAI/Anthropic-compatible localhost APIs. The tweet body is link-only through fxtwitter (article unread end to end - degraded per recipe); the README fetch is byte-verbatim. Shape note for the estate: expert-offload + specdec is the plausible next rung above gemma-class scut. Overlap: "Strata" 0 catalog hits; memory hits are unrelated estate artifacts. NEW (degraded on the article body). Confidence 0.7.

### 7. Inferact, Kimi K3 serving in vLLM at 2.2-2.8x vs v0.27.1 on B300 (~2026-09-17)
URL: https://x.com/inferact (profile - the single status id could not be recovered; vLLM repost dated Sep 17 by search)
Quote (search-result snippet, NOT fetched end to end; degraded per recipe): "Kimi K3 serving in vLLM now delivers 2.2-2.8x throughput on our B300 benchmark vs v0.27.1"
Why: the frontier serving-stack benchmark of the window, and it reconciles with our stack rather than our rows: the gain is attributed to engine work (vllm-openai:kimi-k3 image + DSpark specdec), repro commands claimed - engine-version drift, not provider magic, moves throughput. Banked degraded: no status id resolvable, post text never fetched. Overlap: "B300" 0 real hits in catalog/memory. NEW with caveat. Confidence 0.55.

### 8. TurboQuant KV compression for llama.cpp (date unverified, likely in window)
URL: https://x.com/datageek_ai (profile - no status id in search results)
Quote (search-result snippet, NOT fetched end to end; degraded per recipe): "TurboQuant CUDA for llama.cpp: 3.5x KV cache compression that BEATS q8_0 quality (-1.17% PPL)"
Why: the janitor-critical number if it holds: 3.5x KV compression at better-than-q8_0 quality with 99.6% prefill / 97.5% decode speed and 128K context on an RTX 3090 24GB; a second account (vibhavagarwal5) reports 4x smaller KV with vLLM, 4-bit model in 24GB. KV size, not weights, is the binding constraint on long-context janitors. Banked degraded: no status id, date unverified, claims unfetched. Overlap: name collision with lmcache-src's serde TurboQuant docs (corpus/library/lmcache-src/docs/design/v1/distributed/serde/turboquant.md) - different artifact, relationship unverified. NEW with caveat. Confidence 0.5.

## Synthesis against the research questions

- RQ1 (specdec + continuous batching shifting work down the ladder vs the LENS 2 terminal rule): the shift is real and law-compliant. Engine-side: llama.cpp carries DFlash block-diffusion drafting (out-of-window snippets, testingcatalog/Zhijian Liu) and Strata ships a specdec helper on consumer rigs (item 6); the DSpark explainer (07-11, context) adds a throughput-aware scheduler that keeps specdec lossless under load. The terminal rule constrains HOW, not whether: `mag/inference_budget.py:19` mints EMPTY_REASONING as TERMINAL for (ask, family), "same params NEVER refired, two sanctioned recoveries only" (mint at :319-325, skip-on-sight at :339-344), with per-animal floors (small_floor=8000 / review_floor=24000, rails at memory/behavioral/animals/*.jsonl:1). Speedups move work down tiers; the rule still bans silent refires on empty content. Watch-item: RATIO (held by day-8 arxiv lane) showed quantized local models inflate CoT - local lanes need the same thinking caps the funded lanes got.
- RQ2 (frontier serving benchmarks vs the estate's free-lane row counts): they do not reconcile because they measure different units. Digest commit f80961cd9 ("openrouter 469 +7 below-threshold adds, groq 11, mistral 46"; files watch/inbox/endpoint_news/snapshot_groq.json + snapshot_openrouter.json + endpoint_news.jsonl) counts catalog-add events per day; external numbers are throughput or caps (Groq ~6,000 tok/min free cap per the out-of-window mikenevermiss census; Inferact's 2.2-2.8x engine-vs-engine on B300, item 7). Our concurrency economics are rolling-throughput-bound on our own account (AGENTS.md fan-out law: width 10 clean at 109.4M tok/h, 15-16 untested). Nothing in-window contradicts the row counts; nothing measured OpenRouter free-tier throughput directly. Held evidence says provider dispersion dwarfs engine gains anyway (FACET, state/arxiv/2026-09-30/2609.37902v1.txt: up to 8.8x price and 68x latency spread for one model across providers, per the day-8 arxiv lane).
- RQ3 (which day-8 sweeps leg 3 should re-measure first at funded tier): the day-8 mine is `watch/inbox/frontier_olm_2026-10-01/sweep/` (36 files, 9 areas x 4 doors; its inference-efficiency + kv-cache areas are the carriers). Note: sibling sweeps could not reproduce "32 unbanked" as a literal register (finetuning-adaptation-arxiv.md / -hn.md / -reddit.md each state the count did not verify; -hn counted 28 finetuning items in the 10-06 lens) - I inherit that caveat. Named re-measures, in order: (1) theneurondaily GLM-5.3 Flash 380 / Max 790 tok/s (day-8 x item 6, OWED on a search snippet) - fetch the article and one live probe, land a receipt; (2) AA Cyber Index Pareto (day-8 x item 1) - replicate cost-per-task on the estate's eval mix through one funded turn per lane, auto-banked by hermes_burn usage.jsonl; (3) FACET's 8.8x/68x provider dispersion (held) - build the per-provider envelope table from the estate's own dispatches; (4) consumer specdec (TeksEdge/SEED, day-8) - a llama.cpp DFlash/DSpark probe on gemma:2b-class hardware BEFORE any funded specdec spend, since SEED fine-tunes the target and is not drop-in.
- RQ4 (zero-coverage like biology/web3?): decisively NO. Census over catalog/catalog.jsonl (rg -o | sort | uniq -c): lmcache 3,427 (+44 case variants), ollama 1,583, vllm ~289, sglang 40, speculative 64, tensorrt 18, llama.cpp 15, continuous batching 2. The shelf holds vendored lmcache-src source, daily state/arxiv specdec pulls (Osprey 2609.09338, PELM 2609.09662, LoopSpec 2609.17184, py-kvcache 2609.11744), research_polished/kv_cache_compaction.md, and the day-8 mine ran four-door inference-efficiency and kv-cache sweeps. The genuinely thin stratum is serving ECONOMICS (lab margins, VRAM-era shift, provider dispersion), not mechanics - which is where 5 of today's 8 banked items sit.

## Falsifiers and OWED

- Items 7 and 8 are snippet-grade with no status ids; if the estate acts on them, recover the ids (profile timelines) and fetch before quoting in a rib.
- Item 4's numbers are fetch-summary grade; the Mozilla report itself was not read. Item 6's article body was not read; only its cited README was.
- The inferact B300 date rides the vLLM repost (Sep 17 per search); the original post date is unverified.
- The TurboQuant relationship to lmcache-src's serde TurboQuant is unverified - name collision only.
- No in-window X item measured provider-side concurrency envelopes (429 decay, rolling throughput); the day-8 lane's RQ4 gap persists.
- DFlash-in-llama.cpp support rests on out-of-window posts; verify against the llama.cpp changelog before arming a janitor specdec probe.
