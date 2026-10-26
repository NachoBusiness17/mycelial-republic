# Sweep: inference-efficiency via hn - source-fetched: 2026-09-30

Seat: sweep gopher (inference-efficiency, Hacker News door). Two passes per ask: pass 1 scanned
the HN Algolia API (search_by_date, numericFilters=created_at_i>1788220800, tags=story) over
9 queries: speculative decoding, llama.cpp, vLLM, local LLM, ollama, "tokens per second",
"paged attention", "continuous batching", rate limit - roughly 45 distinct candidate stories
considered from the last 30 days (2026-08-31 to 2026-09-30). Pass 2 deep-read 8 items end to end
(article and/or HN thread). Only items I fetched myself are banked. No door 403s; one query
("paged attention") returned only the Magnitude story, reported as-is.

## Estate-side grounding (what I ran here)

- Ledger aggregation (command: python over training/cost_ledger.jsonl, run this session):
  2,439 rows, ts 2026-08-05T21:55Z to 2026-09-30T12:49Z.
  - deepseek/deepseek: n=498, usd_total $128.06, 129 successful leaves, usd_succ $25.95, so
    $0.201 per leaf verdict (leaf_kinds: test 28, terminal 101, none 369).
  - ollama/ollama: n=1787, 470 leaf verdicts, usd_total $0.00 (local = no marginal $).
  - glm/glm n=44, grok/grok n=32, xai/grok n=4 (grok-4.5): all $0.00 rows - the funded
    tier's spend is NOT in this ledger (driving ladder banks usage in dispatch receipts, not here).
- Tier crossover (funded beats local per correct verdict): OWED. Grep for
  crossover/break-even/per-verdict in memory/ + training/ finds the cache-STACK crossover
  computed (stack >=2 asks on DeepSeek flash/pro, ~4-6 asks on grok 4x; N > 1/r, at
  memory/research_packs/20260809T021009Z_cache-aware-context-batching.answer.remote.md:21,96)
  but the quality-per-$ tier crossover is explicitly listed unknown/RQ1-FUTURE in
  memory/research_packs/20260807T205500Z_context-tax-deliberate-ask-research-project.md:14,20,36.
  The ledger cannot close it: funded-tier rows carry $0.00 (see above), so a receipt-side join
  is the missing instrument.
- Deliberate-ask economics (lens laws.md:28): the 6.5%->98% / $161->$3.60 proof lives in
  memory/rib/RIB_SELF_MY_EFFICIENCY.md:6-9, minted under the OLD funded set (DeepSeek 50x/120x,
  grok 4x cache multipliers). Current funded set is Nous glm-5.3-prime / qwen3.8-max-prime +
  grok-4.7 xAI SD (memory/rib/RIB_DRIVING_LADDER_20260928.md:7-12). No file in memory/ records
  a measured cache multiplier for those two, so per the ONE-BUG law (lens laws.md:18: instrument,
  moment, context) the paid-tier shape needs a re-measure before reuse. The Mercury thread
  below is the external warning that makes this non-optional: Cerebras charges FULL input rate
  (no cache discount), which would erase frozen-prefix economics entirely on such a provider.
- Overnight ceiling inputs: AGENTS.md clippy census (9.34s suite, 3,220 collected);
  ledger shows the ollama fleet is 73% of all ledger rows (1,787 of 2,439) - the janitor cycle IS
  the estate's dominant inference workload, so external findings about configuration-over-engine
  and SSD-wear ceilings apply at exactly our scale.

## Banked items (8, strongest first)

1. Show HN: Running 104GB Qwen3.8-Flash-Next on 48GB Mac at ~12 tok/s (slotstream, HN item
   49524447, 2026-09-01, 240 pts/118 comments). Expert-offload + SSD streaming of a 4-bit 125B
   model on 16-48GB Macs. Thread is a receipt pile: OP "86% acceptance and about 1.24x faster
   decoding" after adding a 1.5GB MTP draft head (speculative decoding, consumer hardware,
   measured); ig0r0 ~200k ctx at ~20 tok/s (27B 4-bit, rapid-mlx); jedbrooke 0.5 tok/s on M2 mini
   with USB disk (disk-bound 400 MB/s); Balooga 10-11 tok/s on a 2013 Mac Pro trashcan via
   llama.cpp. Ceiling material for Q4: ElectricalUnion "around 900GB of writes a day" of swap on
   a memory-starved machine - SSD wear + thermals are the real overnight-inference ceiling, not
   just wall-clock. Estate angle: our janitors run from RAM/NVMe on Windows; anything streaming
   from disk overnight must budget write endurance.
   Overlap: catalog 0 hits; memory 2 incidental files (thinking/trajectory logs). Genuinely new.

2. JevBench: reproducible benchmark for typed decision models (benchmarkheaven.com/jev-models,
   HN item 49800574, 2026-09-22, 153 pts/39 comments). A public instrument that scores DECISION
   models (bounded choices/probabilities, not prose) on "scoring accuracy, latency, and price in
   a configurable weighted way. A full run is 534 English decisions": top = Jev 74.4, SemIf 73.1,
   djev 73.0, Winnow-12B Q8 71.2, reflex 4B 70.3; discloses a "+150 ms on my servers" latency
   adjustment; rotates the test set; seals held-out sets. hbrn: Jev is "twice as expensive" as
   SemIf at parity accuracy. Why it matters: cost-per-correct-verdict accounting as a public
   discipline - the exact shape the estate's tier crossover owes (Q2). Their design choices
   (weighted scoring, sealed held-out, disclosed adjustments) are the template; the thread also
   shows the failure mode (overfit-to-534, benchmark-blaming when a funded model loses).
   Overlap: catalog 0; mickey17 hn-week lane SAW it but did not row it ("Not rowed due to 5-row
   cap... candidate for next lane pass", memory/runs/mickey17_v2/runs/agent-engineering-frontier-
   sweep-40/lanes/hn-week.json:71); estate holds openjev/SemIf prior art on the Jev sphere
   (memory/runs/mickey17_v2/lanes/small-model-agents.json:24,28). This banking is the row that
   lane deferred.

3. Speculative Decoding in vLLM on AMD GPUs (vllm.ai blog, HN item 49596054, 2026-09-07, 145
   pts/53 comments). The community did the vendor-claim autopsy for us: lrvick "4x r9700s as my
   coding daily drivers running qwen 3.8 27b at 80tps each. Zero complaints. Especially at $1200
   each", and pyrolistical checks the math - a single R9700 at 637 GB/s caps Qwen 27B q4 at ~33
   tok/s without MTP, so 80 t/s needs 4-way TP + MTP. Roark66 debunks Intel's "~1400 tok/s" Arc
   B70 claim (200 users with identical 1024-token prompts; real single-user below an RTX 3090).
   Thread also carries a clean draft-and-verify explainer (one parallel forward pass verifies all
   candidates; logit match or rejection sampling keeps the distribution). Why it matters: a
   worked example of receipts-not-vendor-claims (Q1) - bandwidth math bounds tok/s before you
   benchmark, the sanity check our own janitor tok/s claims should always pass.
   Overlap: catalog 0; memory only this session's trajectory log. Genuinely new.

4. Mercury 2.5 hits 770 tokens per second (artificialanalysis.ai, HN item 49823348, 2026-09-23,
   151 pts/92 comments). Speed-economics thread: Mercury 2.5 $0.25/$0.75 per M but "below average
   in intelligence"; freakynit found it ~14B-parity. Cerebras gpt-oss-120b = 1400 tk/s but
   LoganDark reports "$5-10/minute" for a single agent with NO discounted input-cache pricing -
   the direct external warning that frozen-prefix/deliberate-ask economics are provider-
   cache-policy-dependent (Q5). Workload-shape debate lands on our side: physicallyIllfr "Nobody
   needs to code at 600 words per second" vs calgoo "high tps enables querying several agents in
   parallel" - batch/parallel verdict workloads are where speed converts to value, which is the
   estate's actual shape (flock sweeps, burn waves).
   Overlap: catalog 0; memory 2 incidental files (quote_audit inbox_concat, trajectory log).

5. Ollaya - Ollama for open-source, Jev-style decision models (ollaya.dev, HN item 49848269,
   2026-09-25, 613 pts/145 comments). Local janitor-class decision models as a drop-in: ran on
   "a GTX 970 with 4GB of vram" (nickstinemates), 2k context. Author candid on the quality floor:
   small models are "well below Jev on harder queries, but fine for simple, well-defined
   questions"; lgas watched it "just fell apart" on varied queries. Economics from users: mtkd
   ~1.5bn tokens ~ $40, "~$0.00003/req"; devttyeu pushed 250MB/1M log lines for ~$10 vs
   DeepSeek-class "10x costlier and far slower". Why it matters: external confirmation of the
   estate's routing law (scut local, judgment funded) with numbers - simple typed decisions are
   effectively free locally, hard queries need the funded tier; the per-task quality cliff is
   exactly where our crossover sits (Q2).
   Overlap: catalog 0; memory 2 incidental; Jev-sphere prior art known (openjev/SemIf), the
   Ollaya runtime + user economics numbers are the new delta.

6. Faster prompt lookup drafting in llama.cpp (jadidbourbaki blog, HN item 49859982,
   2026-09-26, 89 pts/12 comments). Speculative decoding's n-gram draft path, measured via
   llama-lookup-stats on Apple M4 Pro (median of 3 runs): map-copy fix 4.5x-25.6x faster
   drafting; constmap cache load 6.32x-16.12x (3.76s to 0.23s at 541MB corpus); overall "up to
   42x faster while using up to 2.6x less memory" (up to 140x with Lemire's threshold pre-check
   PR). Honest gaps: NO end-to-end tok/s and no acceptance-rate numbers ("almost identical
   acceptance rates to the original"), WikiText replay only; HN commenter S0y asked exactly for
   end-user tok/s and got none. Why it matters: prompt-lookup is the cheapest spec-decode arm for
   estate work (our asks are input-grounded: patch context, receipts, trail text), and this shows
   the drafting overhead was pure data-structure debt, now cheap.
   Overlap: catalog 0; memory only trajectory log. Genuinely new.

7. Benchmarking Local LLM Servers: Llama.cpp, Llamafile, LM Studio, and Ollama (Mozilla.ai
   blog, HN item 49742415, 2026-09-17, 3 pts/2 comments). Real receipts: Mac Studio M4 Max,
   L40S, and a Steam Deck OLED (Vulkan) on identical GGUFs; 15 llama-benchy runs, trimmed mean;
   separates prompt-processing from token-generation. Finds: "The biggest speedups came from
   configuration, not the choice of engine"; fixed host overhead per token ~0.4 ms Mac / ~1.8 ms
   L40S / ~5.4 ms Deck; spec-decode draft length flips by platform (Metal draft 4 WORSE than
   none: ~15 vs 23.4 tok/s; draft 2 = 24-25 tok/s; CUDA draft 4 beats draft 2 by up to 16%);
   Vulkan toolchain alone +25.9-63.3% PP on the Deck. HN thread: Lockal's methodology criticism
   (numbers "can't compare together") - the blog's own methodology section is the rebuttal
   surface. Overlap: PARTIAL - a prior gapwave lane already banked this exact post
   (memory/runs/gapwave/hn_x_fanout/local_serving.md:22-23), and that lane's own "Need" line
   asked for exactly what my deep read adds: the platform-flip draft-length finding and the
   second Vulkan data point (local_serving.md:54). Kept for that delta only; the headline was
   already estate-held.

8. DeepSeek v4.1 Flash internal beta (HN item 49607094, 2026-09-08, 22 pts/8 comments).
   Provider rate-limit model data point (Q3): beta runs at "an account-level rate limit of 20
   concurrent requests", expire-by date encoded in the model name, v4-flash pricing. dyl000:
   "effective price is like 4 cents / m in on openrouter with cache hits." Why it matters:
   (a) published caps in the wild are CONCURRENCY-shaped, not rolling-throughput-shaped - nothing
   I read this window publishes a rolling-throughput/first-contact-HOLD model matching our
   measured envelope (AGENTS.md fan-out law; B2_443 census), so that finding stays
   estate-original; (b) cache-hit pricing culture is real and quantified publicly, which supports
   the deliberate-ask shape while underlining that its multiplier must be re-measured per
   provider (Q5). Overlap: catalog 0; the v4.1 LAUNCH was already covered by a gapwave lane as
   moat counter-evidence (memory/runs/gapwave/hn_x_fanout/skill_quantization.md:73-74); the
   beta-thread rate-limit shape + cache-price quote are the new delta.

## Door health

Algolia API + news.ycombinator.com item pages all fetched clean. "paged attention" and
"continuous batching" queries returned 1 story each (reported above); no fallback was needed and
none was fabricated.

## OWED / not done here

- Tier crossover per correct verdict: OWED (needs receipt-side spend join for glm/grok rows).
- glm-5.3-prime / grok-4.7 cache multipliers: not found in memory/ - re-measure before reusing
  the $161->$3.60 shape on the current funded set.
- Mercury/AI-review-time energy math for overnight local inference: no published ceiling found
  this window beyond the slotstream SSD-wear/thermal data point; estate-side wall-clock budget
  not measured here (my session did not run any local model).
