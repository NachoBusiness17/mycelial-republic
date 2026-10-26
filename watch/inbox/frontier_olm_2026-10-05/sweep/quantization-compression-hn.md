# SWEEP: quantization-compression via hn (frontier_olm 2026-10-05)

source-fetched: 2026-10-05
Door: Hacker News (hn.algolia.com API + news.ycombinator.com threads). Seat: sweep gopher, quantization-compression.
Estate map served: the deliberate-ask quantize-target law and the local janitor tier's model cards (gemma:2b scut / gemma4 short worker byte budgets).

## Method (what I actually ran)

Pass 1, broad sweep. Eight Algolia API calls via WebFetch, window created_at_i > 1788566400 (2026-09-05), tags=story:

1. search_by_date query=quantization → 9 hits, all in-window
2. search_by_date query=GGUF → 19 hits, all in-window
3. search_by_date query=AWQ → DEGRADED (see door notes below)
4. search_by_date query=Ollama → 30 hits, all in-window
5. search_by_date query="structured output" (phrase) → 4 hits
6. search_by_date query="context compression" (phrase) → 0 hits; unquoted AND fallback → 5 hits
7. search_by_date query="KV cache" (phrase) → 19 hits
8. search_by_date query="tool calling" (phrase) → 12 hits
9. search_by_date query=gemma → 30 fetched, mostly German-language noise; 1 usable
10. search_by_date query=GPTQ → DEGRADED (fuzzy match on "GPT")
11. search endpoint query=AWQ (relevance fallback) → mixed, mostly out-of-window
12. search endpoint query=quantization (relevance) → confirms only one in-window front-pager

Roughly 180 hit rows fetched across the calls; after dedup by objectID, about 70 distinct in-window candidates were considered, comfortably past the 30-candidate bar. Titles and metadata are from the API responses this session; nothing below is hand-copied from memory.

Pass 2, deep reads (12 pages read end to end this session):

1. quesma.com/blog/qwen38-27b-quantizations-benchmarked/ (article)
2. news.ycombinator.com/item?id=49611128 (its 139-comment thread)
3. github.com/Vibra-Ingenn/Janus (README)
4. news.ycombinator.com/item?id=49926773 (Janus thread, 19 comments)
5. huggingface.co/apple/LensVLM-9B (model card)
6. news.ycombinator.com/item?id=49911910 (token compression CLI, story text + 5 comments)
7. blog.mlc.ai/2026/05/04/xgrammar-2-fast-customizable-structured-generation
8. seangoedecke.com/jev-means-structured-output-is-interesting-again/
9. ollama.com/blog/ollama-now-supports-jev-style-decision-models
10. github.com/gauravapiscean/agentic-kv-cache (README)
11. xyntetik.com/runner/truncation-safe-tool-calling/
12. weaviate.io/blog/4-bit-rotational-quantization + discuss.huggingface.co VeriLoop E2 release thread (180723)

## Answers to the four research questions

### Q1: quality-versus-bits on 2B-8B at 4-bit vs 8-bit, tool-calling and repo-editing tasks

The window's flagship measurement is at 27B, not 2B-8B, and the estate already holds it: Quesma's Qwen3.8 27B benchmark (286 pts, HN 49611128) found "Yet the 17 GB Q4_K_M matches the full model on a popular agentic coding benchmark, Terminal-Bench 2.1", IFBench flat down to 2-bit, and "At 1 bit, the model performs around random chance on GPQA Diamond". That is banked ground: memory/percolator/candidates.jsonl row from 2026-10-02 (file watch/inbox/frontier_olm_20260928/percolator_candidates.jsonl, row 4, canonical 4c063d5e2820785a) holds the quant-floor law (Q4_K_M safe default, 2-bit the instruction-following floor, 1-bit collapse) plus the sibling arXiv 2609.32042 row (row 3, canonical 14053729808aeaa3) with the 3-bit-to-2-bit cliff replicated across model sizes.

Deltas I add on that held ground, from reading the thread end to end this session:
- Counter-signal against "4-bit is free" at the fine grain: anyfoo reports "Q6_K_XL (from unsloth) comes up with a solution, anything Q5 doesn't", i.e. per-task cliffs sit well above the benchmark-aggregate floor.
- kmike84's point: KL-divergence measured on wikitext badly understates divergence on agentic/coding traces; task benchmarks, not perplexity, must pick the quant. This reinforces the held floor law's justification.
- The missing-Q3 debate: commenters note no Q3 data point although 16GB-class GPUs need it for usable context. The estate's 4B-8B janitor cards live exactly in that band; the held law has no Q3 rung measured for small models.
- Honest scope: on HN this window I found NO 4-bit-vs-8-bit tool-calling quality table for a 2B-8B model. The nearest real measurement at janitor scale is the Xyntetik Runner page (new, banked below): schema conformance and tool selection held at 100 percent down to Q4_0 on granite-4.1-3b and Qwen3-1.7B, but argument agreement with a Q8_0 reference fell to 50 percent. Its one-line law: "Shape is guaranteed at any quantization. Contents are not."

### Q2: does sub-8-bit quantization degrade structured tool-call syntax and JSON adherence?

Three independent in-window sources say the shape half of the estate's worry is solvable by construction, not by bit-depth:
- XGrammar-2 (MLC, banked below): constrained decoding with structural tags gives 100 percent schema accuracy on BFCL-V3 subsets and claims gains concentrated on small models: "On-device scenarios typically use small models, which benefit from constrained decoding even more than large ones". Integrated into SGLang, vLLM, TensorRT-LLM, MLC-LLM.
- Xyntetik Runner (banked below): schema-legal endings emitted at the token limit, tested against vLLM 0.27.1, llama.cpp b10488, Ollama 0.32.14, TensorRT-LLM 1.2.1, SGLang 0.5.17; below a 16-token budget "only Runner returns a parseable call", with others leaking framing into prose, emitting unparseable arguments (llama.cpp), or HTTP 500 (Ollama).
- Sean Goedecke (banked below): the reliability edge of new "System One" structured-output models is thin because "fast structured output is already available" via grammar-constrained decoding on ordinary LLMs.
The content half (which arguments, how sane) is where quantization bites: Xyntetik's 50 percent argument agreement at Q4_0 vs Q8_0 reference, and the Quesma thread's cascade warning (rare token differences compound into task failure). Estate translation: the tool-call shape laws are safe at 4-bit; the law CONTENT compiled by the thought quantizer needs a content-scored eval slice, which the held percolator probe already sketches (protocol-shape and content scored separately).

### Q3: which GGUF/AWQ variants of the newest open models are downloadable and runnable on a local Ollama host today

- VeriLoop E2 (banked below): a complete, downloadable GGUF ladder BF16 → Q8_0 → Q6_K → Q5_K_M → Q4_K_M → Q3_K_M → IQ2_S → IQ1_M, each tier built from canonical BF16 (not requantized from lower tiers), with per-tier retention metrics (IQ1_M: +0.3191 percent PPL drift, KLD 0.014357, 95.870 percent same top-p) and the explicit warning "these are quantization-retention measurements, not downstream benchmark-loss percentages." License not stated anywhere in the thread (OWED). A user reports working Colab L4 pulls.
- Janus (banked below): a single MIT-licensed Go binary running .gguf via Vulkan on Windows 10/11 first, OpenAI-compatible API on 127.0.0.1:8990, hot-swap without restart, early maturity (2 commits, 126 stars). Thread verdict: "This seems to be a thin wrapper around libllama, what's the point? Llama.cpp already ships a web server", and no benchmarks were posted. Fallback host option, not an Ollama replacement.
- Ollama 0.35 decision models (nimble 9B, tev1 4B, tev1:0.8b) are HELD ground: memory/percolator/candidates.jsonl 2026-10-01 row 3 (canonical b26a58cafeffd968) already banks them plus the 91ms vendor-demo guard; not re-banked.
- Also surfaced, unread beyond metadata (not banked): pfeifferj Qwen3.8-Flash-Next GSQ-RCO GGUF (HN 49703818), Ternary-Bonsai-8B-gguf (HN 49774861), Gufo-Qwen3.6-35B-A3B-Q6dense on Strix Halo (HN 49941824), VeriLoop's sibling prism-ml Bonsai 2 27B (HN 49813964).
- AWQ specifically: no in-window AWQ release story survived the degraded query (see door notes). The strongest AWQ artifact the relevance fallback surfaced is out-of-window (oobabooga's GPTQ/AWQ/EXL2/q4_K_M comparison, 2023). OWED: a fresh AWQ availability check was not achievable through this door today.

### Q4: long-lived agent context compression mapping onto quantized_thought law-compilation

- agentic-kv-cache (HELD ground, same percolator row 4): radix-leaf LRU is brutally hard to beat; over 68,266 replayed Claude Code session requests, "under capacity pressure, most recomputation comes from tool-calling loops seconds apart, not from sessions idling past a TTL". Delta I add: its own law of method, "If you build one of these, make your first test 'does Belady beat LRU?'", is the falsifier the estate should bolt onto any quantized_thought recall probe.
- Token compression CLI (banked below): compress the tool-output side of agent transcripts through a proxy (fine-tuned Qwen trims Codex tool call outputs), 29.6 percent token reduction with the KV cache untouched. This is transcript-side law compilation in the wild, and its open wound is exactly the estate's question: "It would also be useful to check whether task success rate drops after compression." No commenter reported measured quality loss; the concern is untested.
- LensVLM-9B (banked below): a different compression axis, pages as compressed images with selective expansion to text, 5x/10x/15x ratios on a 9B VLM with nine community quants (llama.cpp/Ollama compatible). Recall cost OWED: the model card carries no benchmark tables.
- Weaviate 4-bit rotational quantization (banked below): the recall-cost template from the vector side, 4-bit embeddings with recall flat from 1M to 250M vectors at 45 percent heap reduction vs 8-bit. That is the measurement shape (recall vs bits, at scale, with a flat line as the win) the corpus FTS/vector lens should copy when it inventories the shelf.

## Dedup / overlap ledger (greps actually run this session)

- rg -i over catalog/catalog.jsonl + memory/: quantiz 387 lines, gguf 43, awq 7 (mostly unrelated)
- Quesma benchmark: HELD, memory/percolator/candidates.jsonl (2026-10-02, frontier_olm_20260928 row 4) banked it with the agentic-kv-cache LRU steal; not re-banked as items
- Ollama Jev decision models: HELD, memory/percolator/candidates.jsonl (2026-10-01, frontier_olm_2026-10-01 row 3) + prior 09-30 sweep
- DeepSeek-V4.1 Flash KV compression: HELD, catalog rows state/arxiv/2026-09-18/2609.19969v1.txt + watch/inbox/DESK_DSV41FLASH_20260911.md; not re-banked
- Zero-hit (genuinely new) terms: xyntetik, truncation-safe, XGrammar, Structural Tag, VeriLoop, Vibra-Ingenn, LensVLM, spenmcke, seangoedecke, "structured output is interesting", per-tensor layout, rotational quantization, Ternary-Bonsai, Gufo-Qwen
- Catalog weaviate rows are corpus/library/openai-cookbook notebooks, unrelated to the Weaviate RQ blog
- Today's sibling doors: watch/inbox/frontier_olm_2026-10-05/sweep/ holds only raw/ at write time; no collision

## Door notes (degradations, honestly)

- No 403s anywhere; hn.algolia.com and news.ycombinator.com and all fetched pages returned normally.
- AWQ by-date query: the API returned an unfiltered recent feed (hits unrelated to AWQ), i.e. the query term was effectively ignored. Relevance-endpoint fallback ran and returned mixed/out-of-window results; no AWQ item was banked from it.
- GPTQ by-date: fuzzy typo-matching on "GPT" flooded the results with GPT-6 Astra stories; nothing usable.
- Exact-phrase "context compression" returned nbHits 0; unquoted AND fallback returned 5 usable hits. Reported as the fallback it was, not as success of the original query.
- One local tool miss: curl to the Algolia API failed (exit 23) in this shell; all fetching went through WebFetch. Raw-JSON verbatim backup was therefore not available; quotes below are the fetcher's extractions from single-page reads, reflected in slightly reduced confidence values, and two-source corroboration was used where the same fact appeared in both a thread and its linked page.

## Banked items (strongest first)

1. Runner truncation-safe tool calling (Xyntetik, HN 49719027, measured 2026-08-19, submitted 2026-09-15). "Shape is guaranteed at any quantization. Contents are not." Schema/tool-selection 100 percent to Q4_0 on granite-4.1-3b and Qwen3-1.7B; argument agreement vs Q8_0 falls to 50 percent; benchmarks vs vLLM/llama.cpp/Ollama/TensorRT-LLM/SGLang at token budgets 1-64.
2. XGrammar-2 (MLC blog, HN 49796733). "On-device scenarios typically use small models, which benefit from constrained decoding even more than large ones." 80x compile speedup, structural-tag DSL, adopted by xAI/Databricks/DeepSeek, shipped in SGLang/vLLM/TensorRT-LLM/MLC-LLM.
3. VeriLoop E2 GGUF ladder (HF discuss thread, HN 49847732, 2026-09-25). "these are quantization-retention measurements, not downstream benchmark-loss percentages." Full downloadable BF16-to-IQ1_M ladder, per-tier PPL/KLD/top-p retention recorded; license OWED.
4. Janus (GitHub + HN 49926773, 2026-10-01). "Janus is a single Go binary that runs .gguf models on your machine (GPU or CPU) and exposes an OpenAI-compatible API." MIT, Windows-first Vulkan, 2 commits/126 stars; thread calls it a thin llama.cpp wrapper with no benchmarks.
5. Token compression CLI (HN 49911910, 2026-09-30). "It would also be useful to check whether task success rate drops after compression." Proxy-side trimming of tool-call outputs, 29.6 percent token reduction, KV cache untouched; task-success effect unmeasured.
6. Jev structured output (seangoedecke.com, HN 49748997, 2026-09-18). "I suspect Jev does not have a substantial technical moat, and their claimed 'Reinforcement Learning for Calibrated Decisions' is not a brand-new scaling axis." Constrained decoding on ordinary LLMs already delivers fast structured output; System One models add latency consistency, not a new reliability class.
7. LensVLM-9B (Apple, HN 49820496, 2026-09-23). "LensVLM is a 9B Vision Language Model (VLM) that scans compressed images of text, then selectively expands only the relevant pages." 5x/10x/15x compression ratios; per-ratio recall numbers not on the model card (OWED).
8. Weaviate 4-bit rotational quantization (HN 49743523, 2026-09-17). "8-bit RQ is now significantly faster in 1.39 and 4-bit RQ provides similar recall with a 45% heap reduction." Vector-side recall-vs-bits measurement template: recall flat 1M to 250M vectors.

## OWED (not found, not fabricated)

- 4-bit-vs-8-bit tool-calling/JSON quality table for an actual 2B-8B model from this window: not found on HN. Closest is Xyntetik's Q4_0-vs-Q8_0 argument-agreement number at 1.7B-4B scale.
- AWQ in-window availability story: degraded query, nothing banked.
- LensVLM recall-vs-compression-ratio numbers: not on the model card; lives in the paper/repo (unread).
- VeriLoop E2 license: absent from the release thread.
- Janus: no third-party benchmarks; maturity unverifiable beyond repo metadata.
