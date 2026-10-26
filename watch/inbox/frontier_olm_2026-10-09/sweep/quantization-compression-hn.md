# Sweep: quantization-compression via Hacker News - 2026-10-09

source-fetched: 2026-10-09. Door: HN Algolia API (search_by_date + search, tags=story,
numericFilters=created_at_i>1788912000 = 2026-09-09, 30-day window), then per-item page
fetches; news.ycombinator.com item pages for thread reads; arXiv abstract pages plus ONE
export.arxiv.org GET for the day-8-card re-verification. All quotes below are from pages
fetched this sitting.

## Doors and degradation

- hn.algolia.com: worked, every query sub-second. 11 queries run, all search_by_date
  except two: quantization, GGUF, BitNet, "quantization-aware training" (quoted phrase,
  0 hits), pruning LLM, "small language model", llama.cpp, "KV cache quantization"
  (0 hits), on-device LLM, plus the relevance variant of quantization. One malformed
  query ("1-bit OR ternary OR 1.58-bit") returned 0 hits; the OR syntax is not Algolia
  shape. Plain-term queries carried the sweep, same lesson as day-8's note.
- news.ycombinator.com item pages: worked for 49884625 (31-comment thread) and 49835080
  (text post). No timeouts.
- arxiv.org/abs pages: worked (2609.21341 fetched in full).
- export.arxiv.org: GREEN, one GET, id_list shape with three ids at once
  (2610.04403,2610.09827,2609.26219) returned all three Atom entries. This is the Q3
  re-verification instrument, see the day-8-cards section.
- One redirect: theneuralmaze.substack.com (QLoRA explainer, HN 49778955) 301s to
  www.theneuralmaze.com; NOT followed (see OWED). The item stays unbanked.

## Pass 1 - candidates considered (30-day window; 65 raw distinct hits, 11 queries)

On-topic strong ground: 49884625 ESP32S3 1.58-bit BitNet cluster (150 pts, held day-02),
49803325 Pruning LLMs Like a Physicist (NEW, banked below), 49966238 EasyCommand
finetuned 1.5B/0.6B Qwen bash (delta banked below), 49835080 IttyBittyAI Qwen2.5:0.5B on
a 2017 phone (NEW read, banked below), 2609.21341 What Stops a Small Language Model From
Driving a Database Agent (held day-0, re-read this sitting), 49743523 Weaviate 4-bit
rotational quantization (held day-05), 49778955 QLoRA explainer (redirect, unbanked),
49812339 Transformers now runs llama.cpp quants (held day-09-30/10-01), 49963837
OntoPrune 85% context-token pruning on CPU (candidate only, context-side not
weight-side), 49913715 FGRF v3 weight-topology probing (candidate only), 49710030 Apple
on-device LLM measured across an OS beta (candidate only), 49941824 Gufo Qwen3.6-35B
Q6dense Strix Halo (day-08 candidate, untouched), 50002054 Bonsai-2 ByteShape comparison
(day-08 candidate, untouched), 49823211 quant-delta-predictor (day-08 candidate,
untouched), 49644045 GLQ trellis-quant vLLM plugin (day-08 candidate, untouched).

Off-topic noise excluded: 5 Bitget crypto stories matching "BitNet", GPU-price and app
ShowHNs from the pruning/on-device queries, the 868-point "limit the AI news flood" Ask.

## Pass 2 - end-to-end reads this sitting (6)

49884625 HN thread, the MultiverseComputing pruning blog, dirac.run/posts/easycommand,
49835080 HN item, arxiv.org/abs/2609.21341, weaviate.io 4-bit rotational blog. Plus one
export.arxiv.org id_list GET (three papers). Bank only what was read: done.

## RQ1. Did anything since 10-01 move small-model quality off the Q4-at-ceiling rule?

Verdict: NO result read this window moves the qwen2.5:7b Q4-vs-q8 TIE AT CEILING
(sweep/quant_ab/RECEIPT.md, RUN COMPLETE 2026-10-08); the window's evidence piles ONTO
the rule, and locates the movable part elsewhere:

- Weight-quant channel: 2610.04403 (re-verified live this sitting via the export-API GET)
  still reads "Aggressively quantized small models can keep generating fluent text while
  no longer knowing what it means" - the cliff is at Q2/sub-2B, Q4_K_M stays clean at
  >=1B. Janitor-class at Q4 is untouched.
- Task-quality channel: the movable part is TASK data, not bits. EasyCommand (read) got
  0.6B/1.5B models to near-GPT-4o on ONE narrow task via 402k domain pairs, and the
  4-bit exports "keep most of the gains of the 16-bit versions". Q4-vs-q8 is a tie
  because both rungs sit at the data-limited ceiling; the ceiling itself moves with
  domain SFT, not with bit width.
- Failure-attribution channel: 2609.21341 (held day-0, re-read) attributes 75.7% of
  2,100 model-attributed agent losses to tool-invoking runs (transport/mechanical), and
  5 server changes moved 6 models by 6-21 cells with no model change. Part of the
  "ceiling" was never in the weights at all - consistent with the day-8 Strata finding
  (engine dominates at fixed weights).
- Extreme low-bit: the ESP32S3 thread (held day-02) still stands: 1.58-bit ternary at
  0.5B is mechanically runnable and qualitatively "a fancy llm noise-maker" (cameron_b).
  Below Q4, below ~1B, quality falls off the table.
- NEW floor datum (IttyBittyAI, banked below): Qwen2.5-0.5B Q4 runs at ~4.5 tok/s
  generate / ~13 tok/s prompt-read in ~570 MB RAM on a 2017 Snapdragon 430 phone, while
  SmolLM2-360M "looped and refused to answer things". Sub-0.5B is below the usable
  janitor floor; 0.5B Q4 is on it. Fetcher-mediated numbers, post not byte-fetched.

Standing rule maintained: Q4-at-ceiling for janitor-class (>=1B robustly, 0.5B usable),
with the amendment that the ceiling is task-data-limited and partly transport-limited,
not quantization-limited.

## RQ2. QAT / LoRA-on-quantized filling UNMEASURED grid cells without breaking T0/T1

- The method with in-window local-first evidence is POST-train LoRA SFT then quantize,
  not QAT: EasyCommand released merged BF16 checkpoints + original LoRA adapters + 4-bit
  GGUFs (1.5B at 940.4 MiB, 0.6B at 461.8-767.5 MiB), CPU-runnable, Apache-2.0. That
  recipe fills a grid cell (domain-specific 0.6B/1.5B Q4 janitor) entirely inside the
  T0/T1 boundary.
- Day-05's finetuning bank already carries the EasyCommand scores and the
  "evaluating the actual quantized file became part of selection" line; my delta below
  is the 4-bit-retention + CPU-runnability sentence, new to the estate (grep: 0 hits).
- NO new QAT result was read this window. The one QAT claim in reach stays
  thread-comment tier: day-08 carried seamossfet's "you need somewhere near 50x
  chinchilla to do QAT" for 1-2 bit targets as OWED paper hunt; nothing read today
  discharges or contradicts it. QLoRA (LoRA ON a 4-bit NF4 base) is the canonical
  training-on-quantized method but the explainer HN hit is redundant corpus ground:
  catalog/catalog.jsonl already holds 12 QLoRA rows; not banked.

## RQ3. The day-8 mine's 6 unbanked cards: which carry arXiv-verifiable quantization claims?

The 6 cards are watch/inbox/frontier_olm_2026-10-08/steal/{finetuning-adaptation,
inference-efficiency-hn,kv-cache-context-engineering,open-local-models,"open-local-models
via reddit","quantization-compression via hn"}.md (lens/burns.md:87, section 2b). Grep
census of "quant" per card: 5 / 9 / 12 / 11 / 3 / 20 hits.

- TWO cards carry frontier quantization claims re-verifiable in ONE GET:
  1. quantization-compression via hn.md -> arXiv 2610.04403 (weight-quantization regime
     paper).
  2. kv-cache-context-engineering.md -> arXiv 2610.09827 Dual-QK (2-bit KV-survival
     recipe: KV-cache compression claims) and 2609.26219 PatchKV (KV-reuse compression,
     quantization-adjacent).
- The other four cards' "quant" hits are estate-organ references (quantized_thought
  instructions, the quant A/B receipt), not frontier claims: inference-efficiency-hn.md
  :23-32 points at memory/corpus/quantized_thought and sweep/quant_ab/RECEIPT.md;
  finetuning-adaptation.md's arXiv id is 2610.06851 (token cues, not quantization).
- THE ONE GET, run this sitting:
  https://export.arxiv.org/api/query?id_list=2610.04403,2610.09827,2609.26219&max_results=3
  returned all three Atom entries with the claims intact: 2610.04403 published 2026-10-03
  (abstract sentence quoted above), 2610.09827 published 2026-10-07 ("6.8x KV-cache
  compression and an estimated 8.3x reduction in KV read volume"), 2609.26219 published
  2026-08-18 ("2.51-3.85x speedup in mean resume time-to-first-token over full suffix
  recomputation"). The green arXiv door takes a comma-joined id_list: one GET verifies
  all card claims at once.

## RQ4. Weight-sharing and pruning for sub-8B: what the frontier says that we do not hold

- The strongest in-window pruning result (banked below, genuinely new to the estate)
  prunes DEPTH, not width: block removal as a constrained binary (Ising/QUBO) problem,
  solved exactly or with quantum-inspired solvers, excited states kept as candidates.
  Its smallest artifact is Llama-3.1-8B-Instruct (16/32 blocks); Qwen3-14B, Llama-3.3-70B,
  Nemotron-3-Nano-30B-A3B follow. NO sub-8B pruning result exists in this window's
  frontier read, and the estate holds none either: git grep over memory/ + watch/inbox/
  for Multiverse Computing / "Pruning LLMs Like a Physicist" = 0 hits; catalog = 0 rows.
  Sub-8B pruning stays an empty cell in BOTH the frontier window and the corpus library.
- Weight-sharing/ternary: the estate already holds the BitNet-on-microcontroller story
  (day-02 bank). This sitting's repo read adds the mechanism split the bank lacked:
  ternary 1.58-bit transformer layers + INT4 token embeddings (~14 MB in flash) +
  SPI daisy-chain across 7 boards. Sub-8B ternary quality remains the binding
  constraint, not runnability.

## Banked items (fetched and read this sitting; overlap greps against
catalog/catalog.jsonl via grep and memory/ + watch/inbox/ via git grep)

1. Pruning LLMs Like a Physicist: Block Removal as an Ising Optimization Problem
   https://huggingface.co/blog/MultiverseComputingCAI/pruning-llms-like-a-physicist-block-removal-as-an
   (HN 49803325, 2026-09-22, 2 pts)
   Quote: "at 50% compression of Llama-3.3-70B-Instruct, we gain almost 23 percentage
   points on MMLU over the best competing block-removal method"
   Overlap: git grep "Multiverse Computing|Pruning LLMs Like a Physicist" over memory/
   watch/inbox/ = 0 files; grep catalog/catalog.jsonl = 0 rows. Genuinely new.
   Estate read: depth-pruning frontier tops out at 8B smallest; the sub-8B cell our
   janitor tier would need is unaddressed; method (Hessian couplings + QUBO solvers +
   excited states) is the steal-worthy part if we ever prune our own fine-tunes.
2. EasyCommand quantization delta (dirac.run, HN 49966238, 2026-10-05)
   https://dirac.run/posts/easycommand
   Quote: "The 4-bit versions surprisingly keep most of the gains of the 16-bit
   versions, and they are convenient to run on CPU systems."
   Overlap: day-05 finetuning sweep banked the benchmark scores (212/300 ALFA-updated at
   Q4_K_M, GPT-4o 73.0 on original ALFA, baseline 54.0) at
   watch/inbox/frontier_olm_2026-10-05/sweep/finetuning-adaptation-hn.md:103-112; git
   grep "keep most of the gains" over memory/ + watch/inbox/ = 0 hits, so the retention
   + CPU-runnability datum and the released artifact shape (BF16 + LoRA adapters + 4-bit
   GGUFs at named sizes) are new. Catalog 0 for easycommand/dirac.run. This is a DELTA
   bank on a held source, stated as such.
3. IttyBittyAI - Qwen2.5:0.5B on a 2017 Asus smartphone (HN 49835080, 2026-09-24, 2 pts)
   https://news.ycombinator.com/item?id=49835080
   Quote (story title as shown): "Show HN: IttyBittyAI - Qwen2.5:0.5B running on a 2017
   Asus smartphone"
   Overlap: candidate-level in three prior sweeps (day-01 open-local :14, day-03
   open-and-local :61, day-03 finetuning :104), 2/0 each time, never read, absent from
   both DIGESTs; catalog 0 for IttyBitty/postmarketOS. First read.
   Estate read (numbers fetcher-reported from the item page): Qwen2.5-0.5B-Instruct Q4
   GGUF 403 MB, ~570 MB RAM, ~4.5 tok/s generate / ~13 tok/s prompt-read on a Snapdragon
   430 with 3 GB RAM, llama.cpp compiled on-device, SmolLM2-360M faster but "looped and
   refused to answer things". The janitor-floor datum for RQ1: 0.5B Q4 is the usable
   floor, sub-0.5B is not.
4. ESP32S3 cluster repo - mechanism delta under the day-02-banked thread
   https://github.com/Low-Zi-Hong/ESP32s3-LLM-Cluster (HN 49884625, 2026-09-28, 150 pts)
   Quote: "This project runs a sliced 0.5B LLM across a cluster of 7 ESP32s3. One act as
   master and others are node."
   Overlap: the thread verdict is banked at
   watch/inbox/frontier_olm_2026-10-02/sweep/quantization-compression-hn.md:25; git grep
   "sliced 0.5B" = 0 hits, so the repo mechanism (ternary 1.58-bit transformer layers +
   "Token Embedding (INT4, ~14MB in Flash)", SPI daisy-chain, no tok/s published) is
   new. Catalog "ESP32" hits are an unrelated openai-cookbook voice example; "BitNet"
   hits a day-06 door artifact. DELTA bank, stated as such.

## Held ground resurfaced (NOT re-banked)

2609.21341 (day-0 full-text read, frontier_olm_20260928/sweep/
finetuning-and-adaptation-arxiv.md:23,:31; raw HTML+TXT harvested, catalog rows
674050/674063/674064) - re-read this sitting for RQ1; no delta over day-0's summary.
Weaviate 4-bit rotational quantization (day-05 item 8, same quote). ESP32S3 thread
verdict (day-02 item 5). Transformers-runs-llama.cpp-quants (day-09-30 RSS + day-10-01
DIGEST/percolator). QLoRA explainer (catalog holds 12 QLoRA rows; redirect unfollowed).

## OWED / not done (never asserted as done)

- QLoRA substack redirect (www.theneuralmaze.com) not followed; item unbanked, cited as
  known corpus ground instead.
- IttyBittyAI numbers are fetcher-mediated (summary of the post text); the post's own
  screenshots/site (spottedmarley.com) not fetched.
- seamossfet's "~50x chinchilla for QAT" paper hunt (carried from day-08) still open;
  nothing this window discharges it.
- OntoPrune (49963837), FGRF (49913715), Apple on-device measurement (49710030),
  Gufo Q6dense (49941824), Bonsai-2 comparison (50002054), quant-delta-predictor
  (49823211), GLQ trellis plugin (49644045): candidate level only, not read.
- The pruning blog's full paper (linked from the post) not fetched; blog-level numbers
  only. Blog publish date not shown on the page; dated here by its HN story (09-22).

## Commands run this sitting

- 11 HN Algolia queries (listed under Doors).
- Page fetches: news.ycombinator.com x2, huggingface.co blog, dirac.run, arxiv.org abs,
  weaviate.io blog, github.com repo, export.arxiv.org id_list GET, theneuralmaze
  substack (301, not followed).
- grep -ic over catalog/catalog.jsonl for 8 candidate terms (ESP32 1, BitNet 1,
  MultiverseComputing/Physicist 0, easycommand/dirac.run 0, 2609.21341 6,
  RaBitQ/rotational 0, IttyBitty 0, QLoRA 12).
- git grep over memory/ + watch/inbox/: ESP32s3/Low-Zi-Hong (4 files), EasyCommand/dirac
  (5 files), RaBitQ/rotational (5 files), IttyBitty (5 files), Multiverse/Physicist (0),
  transformers-llama-cpp-quants (4 files), "keep most of the gains" (0), "sliced 0.5B"
  (0).
- Day-8 cards: grep -inc "quant" over the 6 cards (5/9/12/11/3/20) + context reads of
  the kv-cache and inference-efficiency hits.
- Day-0 holding check: grep 2609.21341 over frontier_olm_20260928 (DIGEST, RECEIPT, 2
  steal files, 1 sweep file) + catalog row inspection.
