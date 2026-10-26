# inference-efficiency via X - sweep 2026-10-01

Lane: sweep-inference-efficiency-x (frontier_olm_2026-10-01). Doors: WebSearch (site:x.com queries) then the fxtwitter door `https://api.fxtwitter.com/<user>/status/<id>` for resolution. Stamp: source-fetched: 2026-10-01.

## Door status (never fabricated)

- fxtwitter resolved 10/10 single-status fetches this session with verbatim-grade text and created_at dates (ArtificialAnlys x2, TeksEdge, kunchenguid, Oluwaphilemon1, omarsar0, pseudokid, exolabs, ethankurz, liquidai, skalskip92, ZhihuFrontier, cerebras).
- X long-form articles are link-only through fxtwitter (tweet body is just a t.co/x.com/i/article URL): hit on cerebras 2067357992929153268 (Jun 17, out of window anyway), theneurondaily 2102748781674639866, exolabs 2103617535765573959. For those, the banked quote is the search-result snippet or the article snippet the door returned, labeled as such per the fetch recipe.
- WebSearch itself threw its own upstream 1302 rate-limit errors on 4 attempts (GLM pricing, grok-4.7 pricing, rate-limits query, first AA GLM query); retries succeeded. One search (vLLM vs llama.cpp on x.com) returned only spam; the serving-stack RQ fell back to non-X sources, which this lane does not bank as items.
- Lens open questions live at `watch/inbox/frontier_olm_2026-10-01/lens/laws.md` (the ask's "lens/laws.md"): #8 cool/heat map at line 77, #12 the reasoning tax at line 81.

## Pass 1: candidates considered (broad sweep, 30+)

In-window leads: TeksEdge DSpark 3.13x spec-decode; kunchenguid reasoning-effort crash course; Oluwaphilemon1 useful-work-per-dollar; omarsar0 Ember-1 40% fewer reasoning tokens; theneurondaily GLM-5.3 Flash 380 / Max 790 tok/s price-war rundown; pseudokid MiMo vs GLM 5.3 vs Kimi K3 pricing; exolabs DGX Spark Handbook sparse-LLM piece; ethankurz Wafer 30-50% more tokens per dollar; ArtificialAnlys Cyber Index Pareto post; ArtificialAnlys Nemotron 3 Nano ~380 tok/s; hanrui_w GLM-5.3-Flash on Nebius 294 tok/s (id dates it ~Aug 31, dropped); fastinoAI Kimi K3 / GLM-5.3 tie at AA 60; johnseach GLM-5.3 for coding; ItsmeAjayKV GLM-5.3-Flash ~$0.25 pricing; thtbee_ GLM-5.3-Flash 57 AA-II at $0.045/task; benitoz GB300 9.7x tokens-per-dollar; Signal_65 B200 vs MI355X tokens-per-dollar; meggmcnulty Jalapeno vs Rubin; polynoamial test-time-compute scale implications.
Out-of-window reads that sharpened the synthesis but are NOT banked: ArtificialAnlys Qwen3.8 Max 56 @ $1.14/task, 2x Qwen3.7's $0.53 (Aug 6, funded qwen3.8 lane context); cerebras economics of reasoning, ~20% benchmark gain for 5-10x reasoning tokens, "85% cheaper" with reasoning off (Jun 17); aakashgupta thinking ~10x tokens ~5x latency; ZhihuFrontier Qwen3.8-Max $2/$6/$0.25-cached card (Aug 3); skalskip92 Qwen3.8 Flash "20x cheaper and ~2x faster than Qwen3.8 Max" (Aug 28); liquidai DSpark thread (Aug 20, H100 + on-device numbers, MoE weakest case 1.18x on M4 Max); _avichawla KV/prefix/prompt-caching article (cache reads ~0.1x, writes ~1.25x); akshay_pachaar and alexalbert__ 10%-of-input cache pricing (older); ramin_m_h draft-model speedup (Aug 19); AGTPinsights DFlash 2 (already banked by the 09-30 lane via reddit); stanine open-weight-vs-frontier 600K tokens/turn, Grok $791 vs Opus $2,509 (article, unresolvable).
Non-X fallbacks seen, not banked (this lane banks X-door items): computingforgeeks vLLM 2.8-4.4x aggregate throughput of llama.cpp; towardsai "Ollama collapses to 41 tok/s under load vs ~793 vLLM"; Red Hat 2026 llama.cpp-vs-vLLM piece; RouteLLM ~95% quality at ~85% cheap-routed queries (tianpan.co); reddit Jev-routing 33.2% pilot.

## Pass 2: deep reads (fetched through fxtwitter this session)

13 posts fetched and read end to end: the 8 banked below plus cerebras (Jun 17), liquidai (Aug 20), skalskip92 (Aug 28), ZhihuFrontier (Aug 3), ArtificialAnlys Qwen3.8 (Aug 6). All read, all dated out of window, none banked.

## Banked items (8, strongest first)

### 1. Artificial Analysis, Cyber Index vs Cost per Task Pareto (2026-09-28)
URL: https://x.com/ArtificialAnlys/status/2104548889919668581
Quote (verbatim, fxtwitter): "Grok 4.7 (xhigh) matches MiMo-V2.6-Pro at 56 but costs $11.67 per task."
Why: first measured reasoning-tax number for two funded lanes on one eval axis. Grok 4.7 at xhigh effort costs 36x GLM-5.3-Flash ($0.32/task, score 50, "the only other model in the most attractive quadrant") and 65x MiMo-V2.6-Pro ($0.18/task, tied score 56) for the same score. That is the cool/heat lane map open question (`lens/laws.md:77`) with numbers: xhigh effort is the heat extreme, flash is the cool rung at near-parity on this index. Overlap: "Cyber Index" 0 hits in `catalog/catalog.jsonl`; yesterday's marked rerun in `watch/inbox/frontier_olm_2026-09-30/sweep/inference-efficiency-x.md:22` recorded grok-4.7=0 in catalog; the estate holds price CARDS (grok $2/$6, cached $0.50, read 09-30; glm-5.3-flash $0.04/$0.50 per FLASHX_PROBE_20260927) but no third-party cost-per-task measurement. NEW.

### 2. TeksEdge, DSpark speculative decoding on consumer rigs (2026-09-25)
URL: https://x.com/TeksEdge/status/2103545065444692306
Quote (verbatim, fxtwitter): "Wow, speculative decoding just gave a local vision model up to a 3.13× decode speedup."
Why: the janitor-speed RQ answered with measured consumer numbers. Liquid AI LFM2.5-VL-3B + ~280M draft (+8.9% params) = 2.30-3.13x decode (up to 2.62x end-to-end) on M5 Max via MLX-VLM, and 1.57-2.14x decode (up to 1.77x end-to-end) on M3 Ultra via llama.cpp; llama.cpp/GGUF/MLX/SGLang supported; gains measured FP16/BF16. Overlap: "DSpark" 0 in catalog; catalog's 17 speculative-decoding hits are arxiv pulls (Osprey 2609.09338, PELM 2609.09662, LoopSpec 2609.17184), a complementary paper line with no consumer numbers held; yesterday's lane listed "TeksEdge 3.13x CUDA spec-decode (no status id)" as an UNBANKED pass-1 lead (`frontier_olm_2026-09-30/sweep/inference-efficiency-x.md:55`) and this read completes that lead with the status id. NEW.

### 3. omarsar0, Ember-1 shorter reasoning traces (2026-09-27)
URL: https://x.com/omarsar0/status/2104341259540123718
Quote (verbatim, fxtwitter, quoting Fireworks' Ember-1): "Ember-1 produces shorter reasoning traces (40% fewer tokens) without sacrificing performance."
Why: the reasoning tax open question (`lens/laws.md:81`) has a live counterexample: a Kimi-K3-based model shipping 40% fewer thinking tokens at held performance, which elvis calls "a bigger deal than it seems", praising "this push on the Pareto frontier to squeeze as much as you can out of your tokens. Feels underexplored." Direct precedent for the estate's visible-channel/extractor guards: the canon is moving thinking out of the bill, not just capping it. Overlap: "Ember-1" 0 in catalog; memory hits are estate-internal ember-named artifacts (memory/behavioral/animals/fireworks_ember_1.jsonl, memory/burns/LEDGER.jsonl), the estate's own naming and not this model's economics. NEW.

### 4. kunchenguid, reasoning effort is a ceiling not a floor (2026-09-25)
URL: https://x.com/kunchenguid/status/2103325882752598078
Quote (verbatim, fxtwitter): "thinking tokens is always a penalty, not a reward"
Why: mechanism for the reasoning-tax guards. Effort settings are a token-penalty strength knob ("a 'ceiling', not a 'floor'"), high effort does not force long thinking on every prompt, and the author avoids max mode because it forces thinking on every request, while the estate's descent protocol pays premium turns one deliverable at a time. This answers the "which animals need which guard" question (`lens/laws.md:81`) at the API-semantics level: cap effort on structure-critical asks instead of post-hoc extraction. Overlap: kunchenguid in memory/catalog is github.com/kunchenguid/backpass, a different artifact (banked by today's agent-memory-continuity-hn lane as its item 2); this post is distinct. NEW.

### 5. Oluwaphilemon1, useful work per dollar not tokens per dollar (2026-09-17)
URL: https://x.com/Oluwaphilemon1/status/2100406861371478251
Quote (verbatim, fxtwitter): "The real metric isn't tokens per dollar. It's useful work per dollar."
Why: the RQ5 metric the estate's ledger already gropes toward (cost per SUCCESSFUL leaf is computed; cost per CORRECT is OWED per the 09-30 lane). The post derives a $0.37/M-output electricity-only estimate from a Qwen3.8-27B local walkthrough, states the caveats (mixed precision, power is not total ownership), and prescribes: test a quantized model on current hardware against 10 real tasks, count usable answers and fix-time. That is a runnable janitor-bake-off protocol. Overlap: same author banked yesterday (status 2096794721288847676, 2026-09-07 RTX 5070 Ti build), a DIFFERENT post verified by id; "useful work per dollar" 0 in catalog. NEW.

### 6. The Neuron, GLM-5.3 Flash 380 tok/s and GLM-5.3 Max 790 tok/s hosted (2026-09-23)
URL: https://x.com/theneurondaily/status/2102748781674639866
Quote (search-result snippet, NOT the fetched page: the tweet body is link-only through fxtwitter, which returned the article title "90 Minutes, 3 New AI Models & a Price War: Here's the Full Rundown"): "Hosted GLM-5.3 Flash reaches 380 tokens/second, GLM-5.3 Max 790 tokens/second"
Why: latency leg of the funded GLM lane: hosted 5.3-Flash at 380 tok/s and 5.3 Max at 790 tok/s, riding the late-Sept price war. Banked degraded per recipe: the thread resolved but the article content truncated, so the numbers ride the search snippet. Overlap: GLM-5.3-Flash estate doctrine exists (docs/ref/GLM53_ARCHITECTURE_PRO.md, docs/ref/GLM53_FLASH_EXPLOITATION.md, 28 catalog hits) but no hosted tok/s benchmark rows are held; yesterday's lane held choblin29's FlashX 200 tok/s on a different tier. NEW with caveat. Confidence 0.55.

### 7. pseudokid, MiMo vs GLM 5.3 vs Kimi K3 price and speed (2026-09-22)
URL: https://x.com/pseudokid/status/2102337495283253586
Quote (verbatim, fxtwitter): "does not fight with my setup"
Why: a practitioner's cool/heat comparison across the exact model family the estate funds. Per the post's own summary of AA charts, MiMo is priced ~1.5-2.4x cheaper than GLM 5.3 and 3.4-8.6x cheaper than Kimi K3 at ~2x the speed, with the qualitative law that faster inference "keeps them in a flow state longer, making slower models harder to tolerate": latency is a steering variable, not just a cost line. Numbers are the fetch's faithful summary of a chart post, not tabulated benchmarks. Overlap: "MiMo-V2.6" 0 in catalog; yesterday's ledger verdict named mimo a funded tier with zero rows in memory/runs/hermes_burn/usage.jsonl, so third-party price/speed for it is unheld. NEW. Confidence 0.65.

### 8. EXO Labs, DGX Spark Handbook: sparse LLMs on low-bandwidth bricks (2026-09-25)
URL: https://x.com/exolabs/status/2103617535765573959
Quote (article snippet returned by fxtwitter): "If you are considering running inference locally, you will no doubt learn about this interesting golden brick."
Why: RQ5-adjacent hardware-class datum: the handbook line the search surface surfaced says sparse LLMs "pair well with its lower memory bandwidth", the same bandwidth-first law the estate's local lane keeps re-deriving (CPU offload, not quant, kills local speed, per the 09-30 lane's banked 5070 Ti post). Banked weakest of the eight: link-only tweet, snippet-grade content, handbook unread end to end. Overlap: exolabs 0 in catalog; DGX Spark unheld estate-side. Confidence 0.6.

## Synthesis against the research questions

- RQ1 reasoning tax, with numbers: AA's Cyber Index prices it per task on funded lanes (grok-4.7 xhigh $11.67 vs GLM-5.3-Flash $0.32 at near-parity scores; item 1); the out-of-window cerebras read frames the same tax as ~20% quality for 5-10x tokens; Ember-1 shows the tax is compressible 40% at held quality (item 3); effort knobs are penalty-strength dials, not floors (item 4). Open question #12 (`lens/laws.md:81`) gets a first quantitative answer: the tax is real, lane-dependent (36x between funded rungs), and partially refundable.
- RQ2 janitor speed: DSpark gives the strongest consumer-hardware spec-decode receipt this window (1.57-3.13x decode for +8.9% params, llama.cpp supported; item 2), and the estate already holds the MoE-weakest-case caveat from the liquidai thread (1.18x on M4 Max) plus the acceptance-rate-vs-KV-quant counter-law.
- RQ3 routing cheap-vs-premium: item 1 is a published Pareto frontier with measured per-task accuracy and cost, a candidate shape for the cool/heat lane map; item 7 adds the practitioner weighting of latency.
- RQ4 concurrency/prefix reuse: NOT banked this window. Every in-window X hit either 429ed at the search layer or dated out of window; the estate's rolling-throughput finding (width 10 clean, 15-16 untested, AGENTS.md fan-out law) remains unchallenged by anything found here, and prefix-reuse economics were already banked 09-30 (grok cached-input 4x, cache-hit pricing tables). Gap stands; no provider-side envelope numbers found on X in-window.
- RQ5 throughput-per-dollar: item 5 names the right metric (useful work per dollar) with a runnable 10-task protocol; item 8 is the hardware-class adjacent lead. The serving-stack bake-off (llama.cpp vs vLLM vs Ollama) surfaced only non-X sources this window (vLLM 2.8-4.4x aggregate, Ollama 41 tok/s under load), listed in pass 1 and not banked per lane scope.

## Falsifiers and OWED

- GLM-5.3 Flash/Max tok/s numbers (item 6) rest on a search snippet; the article was never fetched. If the estate acts on them, fetch the article first.
- pseudokid's pricing multiples are a chart-post summary, not a provider card; verify against z.ai/x.ai cards before quoting in a rib.
- No in-window provider concurrency-envelope item was found on X; RQ4 stays open.
- AA cost-per-task numbers inherit AA's task mix (agentic evals, more turns = more cost); they are eval-shaped money, not API price cards.
