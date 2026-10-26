# sweep: kv-cache-context-engineering via x — 2026-09-28

source-fetched: 2026-09-28 (fxtwitter door + direct WebFetch; two passes). Area: kv-cache-context-engineering.
Sweeper: sweep gopher, dynamic workflow ask. Questions: watch/inbox/frontier_olm_20260928/lens/questions.md ##6 (lines 83-95).

## Door status

- `api.fxtwitter.com` answered for every status resolved this session (7/7): shmidtqq 2091944893862072364, truefoundry 2091811874648240299, MLStreetTalk 2040302198605943255, 0xblacklight 2094479795748999486, GergelyOrosz 2077004868317831557, Trorram 2104386160688509292, kirillk_web3 2087619214915826155, akshay_pachaar 2064700531600458093.
- The search backend collapses most `site:x.com` hits to the bare `https://x.com` root, so exact status URLs had to be recovered by title-re queries. One strong lead never resolved to a status URL: "I failed to make GLM-5.3 Flash usable on 4x RTX 3090" (Sep 7, 2026, snippet: "320B parameters. 96 GB of VRAM. Vision, 256K context"). Banked as a lead only, not an item; recipe fallback observed.
- Two search-narrative fabrications caught by reading the primary source (trust bytes, not reports): (1) it claimed llama.cpp issue #71 says quality degrades after the KV window shifts by one token; the actual issue (read) is about `-n 0` infinite generation mode and says nothing of the sort. (2) It claimed `--context-shift` is "enabled by default"; the server README (read) says "whether to use context shift on infinite text generation (default: disabled)".

## Pass 1 census

45 candidate items surfaced (list in item notes; dates from fxtwitter fetches, not guesses). Strictly in-window (>= 2026-08-30): marfinxx (09-26), Trorram (09-28), 0xblacklight (08-31), the unresolved GLM-5.3 Flash post (09-07). The rest of the corpus cluster runs Aug 24 (a real cluster: shmidtqq + avichawla/truefoundry same day), Jun-Jul (GergelyOrosz 07-14, akshay 06-10, FireworksAI), and an April serving cluster (MLStreetTalk 04-04, Prince_Canuma 04-02). Items banked below carry their true dates; nothing is dated by inference.

## Findings by question

### Q1 prompt-cache design patterns for agent loops (beyond the playbook)

The playbook (corpus/steal/ZCODE_OPERATING_PLAYBOOK_20260925.md) verified: byte-identical ask keying (FNV-1a, hash.ts:48), amend-cache closes on first workspace write (scheduler.ts:233-237), compact cliff 166K/200K (policy.ts:6-14), 30KB bash cap. What the X literature adds, read this session:

- **Measured hit-rate numbers exist and are quotable.** Kimi K3: $3.00/M cache-miss vs $0.30/M hit input (10x gap; K2 was ~6x); Mooncake reports 90%+ cache hit on coding workloads; worked example: 1,000 runs/day differ by $4,860/day between all-miss ($6.08/run) and all-hit ($1.22/run); "<70% hit rate in agent loops = leaking prefix" (shmidtqq article, read via door). Kimi's TTL is unpublished; 256-token caching floor; no manual cache control on K3.
- **The stable-to-volatile law, operationalized.** shmidtqq's three laws (prefix-only matching; stable content on top, volatile at bottom; measure via `cached_tokens`) plus eight rules: build requests stable-to-volatile, freeze system prompts, append history rather than sliding it, declare tools once, send `prompt_cache_key`, return full assistant messages including `reasoning_content`, fix RAG chunk ordering/placement, log hit rates. The catalog already holds OpenAI's `prompt_cache_key` implementation (catalog cae4daeac830/9e48124f45ba/067e79ced651, openai-agents-python) — the estate holds the mechanism but not the measured claim.
- **CI prefix-fingerprint test.** shmidtqq ships an audit: a CI check that fingerprints the request prefix so a wording drift fails the build. This is the estate's byte-identical-ask law turned into a machine gate — directly liftable into `tools/workflow_gate.py` territory.
- **Harness-side token economics (measured).** Avi Chawla/TrueFoundry: a 50K tool payload at step 4 re-read on every call burns ~800K tokens by step 19; caching makes that ~3x a single read instead of 16x; deepagents-cli went 52.8% -> 66.5% on Terminal Bench 2.0 (gpt-5.2-codex pinned) by harness changes alone, rank 5 from outside the top 30; TrueForge ran the same tasks at ~40% of Claude Managed Agents' tokens and 2.7x fewer tokens than deepagents. The four levers: offload tool responses to disk (preview + path stay), deferred tool discovery (98 of 100 unused tools never enter the prompt), subagents, code-mode joins. None of this is in the playbook; it is the "first workspace write closes the cache" law generalized to a whole harness economy.

### Q2 structure-not-prose (memweave) evidence

Honest answer: no public controlled A/B of structure-vs-prose INPUT injection with attention-fidelity measurement was found in the 9 reads. What exists: (a) practitioner write-back loops — kirillk_web3's graph-engineering article (767K views) claims facts stored as triples and re-fed beat bigger models, but it is a how-to, not an ablation; (b) memory-benchmark numbers — Mem0 "BEAM 64.1 at 1M tokens", Cognee "BEAM 100K SOTA 0.79" (Trorram thread), which measure structured memory layers but against prose context baselines we did not see specified; (c) TrueForge's compaction "into a structured summary" and the anti-aging pillar "JSON queue handoffs" (marfinxx) — structure advocated for reliability, not measured for fidelity; (d) an arXiv structured-output benchmark (2604.25359, surfaced by search only, NOT read) said to show schema compliance high while leaf-value accuracy lags — output-side anyway. The cache-behavior half of memweave IS supported: byte-stable structures are prefix-stable by construction, so the `<70% = leaking prefix` audit applies to memlang packs directly. Estate-side replication experiment (proposed, not run): arms A (current prose context-pack from mag/context_pack.py) vs B (memlang-structured pack, byte-stable serialization), same 20-prompt scut battery x3 on gemma:2b, measure llama.cpp cached-prefix reuse from server timings, graded task accuracy, and a mid-pack needle-recall probe. Falsifiable frame: structure should move accuracy and needle recall, NOT cache hit rate — cache is governed by prefix stability, which both arms can satisfy. If B beats A on accuracy at equal hit rate, memweave has its first causal datapoint.

### Q3 KV quantization/offload for llama.cpp / Ollama-class 2B-8B

- TurboQuant (Google Research, arXiv 2504.19874, ICLR 2026) has a llama.cpp integration spec (discussion #20969, read): TQ3 ~3.25-3.5 bits/value (~4.4-4.9x compression vs FP16), TQ4 ~4.25 bits (~3.8x). Buffer math on DGX Spark: f16 KV 768 MiB, q8_0 408 MiB (-47%), q4_0 216 MiB (-72%). RTX 5090: ~14 KB/token vs ~64 KB FP16. NOT MERGED — community forks only.
- The caution that matters for janitors: "quality degrades on very small models (0.6B)"; independent REFRACT testing found TQ3 on the V cache collapses generation (Qwen3-32B 24.95 vs 59.32 trajectory score) — "the V cache is the critical component"; CUDA decode pays ~17-39% throughput during generation. Our 2B janitors sit between the 0.6B cliff and the 32B safe zone: q8_0 KV is the conservative setting, anything below that on V needs a battery re-run before adoption.
- MLX side (Prince_Canuma, read): gemma-4-31b at 128K ctx with `--kv-bits 3.5 --kv-quant-scheme turboquant`: KV 13.3 GB -> 4.9 GB (63% cut), peak 75.2 -> 65.8 GB, decode ~1.5x slower (kernel launch overhead, fix planned).
- Ollama behavior (MLStreetTalk, read): "Ollama takes 34 GB due to a pre-allocated 262K context" while MLX dynamic allocation used 16 GB on the same model — and "KV cache quantization is a non-factor at normal context lengths". Janitor implication: the win is not quantizing KV on gemma:2b; it is refusing giant default `num_ctx` preallocation. Context budget: set num_ctx per seat deliberately; keep KV f16 or q8_0; the 2B janitor model choice is unchanged by this literature, the serving config is what changes.

### Q4 ram-cache drift (rib open question, laws.md)

The published material supports closing the question by SPLITTING it — "drift" is three different mechanisms that get conflated:

1. **Provider prompt-cache decay** (API path): cache entries expire/evict between turns — Kimi TTL unpublished, Anthropic TTL 5m default (1h via option; from search snippet, docs not read this session) — so hit rate decays with idle time and prefix churn. Detection: log `cached_tokens`; shmidtqq's "<70% in agent loops = leaking prefix". This is drift of the CACHE, not of the model.
2. **Local serving nondeterminism** (llama.cpp path, README read): `--cache-prompt` reuse "can cause nondeterministic results" (differing batch sizes), `--cache-reuse N` reuses cache "via KV shifting" (chunk-level), and `--context-shift` exists but is default DISABLED. So a long session that rides cache reuse is literally re-batching old context — numerics move without any model change. Citation: tools/server/README.md (fetched this session).
3. **Attention-level degradation** (model path): GergelyOrosz (read, verbatim): "the more context you use in a context window (I called it context depth), over longer runs, the more errors can compound / the agent can drift" — reliability rule: less context + shorter runs. 0xblacklight (read): fundamental limits include O(N**2) attention and "performance degradation at long context". marfinxx (read, ad-shaped) names "interference" one of four decay modes.

Suggested rib closure wording: "ram-cache drift is not one cause; name the layer — cache decay (measure cached_tokens), cache-reuse nondeterminism (llama.cpp README), or context-depth error compounding (GergelyOrosz 2026-07-14). The estate's fix for layer 3 is already law: compact at boundaries, amend into new runs."

### Q5 context-window engineering at 100k+ turn scale

- Compaction triggers are threshold-based in the wild: TrueForge compacts history past a default 50,000-token threshold into a structured summary — interestingly BELOW the estate's 166K cliff law, i.e. practitioners compact earlier than the harness cliff.
- Distill-and-restart: 0xblacklight's pattern — when a long run turns to mess, distill into a `new-task.md` artifact and restart. This is the estate's amend-into-NEW-run law (playbook #3) already, independently arrived at.
- Anti-aging pillars (marfinxx, read, promotional source): compaction, relevance gating, JSON queue handoffs, health tripwires. The relevance-gating pillar is the one the estate does NOT have as a law: drop context that stopped earning its seat.
- Run-length discipline: GergelyOrosz's "use less context + have shorter runs" is the 100k-turn answer — nobody credible claims a clean 100k-turn single context; they all cut runs short and hand off. The estate's gala 50-wide fan-out shape is already the same physics.
- Memory-layer benchmarks to mine next (Trorram, read): Mem0 arXiv 2504.19413, Cognee arXiv 2505.24478, Graphiti bi-temporal facts; caveat verbatim: most rely on LLM-based extraction at write time — "é fato CRUD com LLM no meio" (it's just CRUD with an LLM in the middle).

## Items banked (8, strongest first)

1. shmidtqq — "Cache engineering: the new skill that divides your bill by 10. Worked out on Kimi K3" — 2026-08-24 — measured cache laws + hit-rate numbers + CI prefix-fingerprint gate.
2. TrueFoundry quoting Avi Chawla — "How to Cut Agent Tokens by 2.7x" — 2026-08-24 — harness token economics with Terminal Bench deltas; TrueForge levers.
3. MLStreetTalk (+quoted Prince_Canuma) — Gemma/Ollama serving bench — 2026-04-04 — Ollama 262K preallocation + MLX TurboQuant KV numbers (OUTSIDE 30d window; banked for Q3 because it is the only read source with both sides of the Ollama memory story).
4. llama.cpp discussion #20969 — TurboQuant integration spec — date not shown in fetch — TQ3/TQ4 compression numbers, V-cache collapse finding, not merged.
5. marfinxx — "The Anti-Aging Architecture: Jev Engineering and Long-Horizon Agent Lifespans" — 2026-09-26 — decay-mode taxonomy; AD-SHAPED (promotes TypeSafe AI jev-1.13.0), numbers uncorroborated.
6. GergelyOrosz — "context depth" drift — 2026-07-14 — the reliability rule; full text read.
7. kirillk_web3 — "Graph Engineering with Kimi K3" — 2026-08-12 — structured write-back loop as the closest public memweave analog.
8. Trorram — 11 open-source agent-memory projects + BEAM numbers — 2026-09-28 — benchmark pointers (Mem0/Cognee arXiv) and the extraction-cost caveat.

Read but not banked (cap 8): 0xblacklight 2094479795748999486 (2026-08-31, RPI + fundamental-limits list, feeds Q4/Q5 text above), akshay_pachaar 2064700531600458093 (2026-06-10, GRPO structured-output training, Qwen3-8B 62%->82% schema-valid — output-side, off-question), llama.cpp server README (Q4 citations), llama.cpp issue #71 (verification-negative).

## Overlap ledger (grep receipts)

Ran `grep -c -i -F <phrase> catalog/catalog.jsonl` + `grep -r -l -i -F <phrase> memory/` for 21 phrases (full output in session trajectory): "Cache engineering" 0, "256 rule" 0, "Cut Agent Tokens by 2.7x" 0, "TrueForge" 0, "Jev Engineering" 1 (= corpus/library/second-brain-os/docs/track-jev/README.md — concept kin, not the article), "Agent Lifespan" 0, "Anti-Aging" 0 catalog (mycelium graph nodes only), "TurboQuant" 9 (all corpus/library/lmcache-src serde/bench source rows), "262K context" 0 catalog (memory/runs/salons/ollama_maze_astra_20260907 discussed), "gemma-4-31b" 6 (exo model-card .toml rows), "context depth" 0, "BEAM 64.1" 0, "Graph Engineering with Kimi" 0, "kv-quant-scheme" 0, "kv_bits" 0, "Mooncake" 18 (lmcache connector source rows, not the hit-rate claim), "prompt_cache_key" 3 (OpenAI agents-python source rows), "cached_tokens" 2 (litellm test rows). One prior-fanout byte echo: "Cache engineering" matches memory/runs/quote_audit_wide_20260925/inbox_concat.txt (binary grep) — no steal/doctrine file cites it. No item below re-banks held work; all eight add claims the corpus does not carry.

## OWED / not done

- The GLM-5.3 Flash on 4x3090 post (2026-09-07) never resolved to a status URL through search; the NVIDIA-forum/GitHub/helix.ml fragments the search narrative attached to it were NOT read and are NOT asserted here.
- Claude/Anthropic docs page (tools -> system -> messages cache ordering) appeared only as a search snippet; docs fetch not performed this session. Not asserted as read.
- arXiv 2604.25359, KIVI, and the Weaviate TurboQuant blog: snippets only, not read; listed so the next window can fetch them deliberately.
- The estate-side memweave A/B experiment is PROPOSED, not run.
