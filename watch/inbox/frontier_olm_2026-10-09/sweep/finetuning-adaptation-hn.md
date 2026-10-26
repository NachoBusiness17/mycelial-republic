# SWEEP: finetuning-adaptation via HN (frontier_olm_2026-10-09)

source-fetched: 2026-10-09. Seat: sweep-finetuning-adaptation-hn (dynamic-workflow gopher, Mag Resource Harness). Window: created_at_i > 1788912000 = 2026-09-09 .. 2026-10-09. Door: HN Algolia API (search_by_date + search, tags=story), then news.ycombinator.com item pages and primary articles. Every item below was read by me this sitting; nothing banked unread.

## Door health

- Algolia queries fired: LoRA (by-date: 30 rows, mostly fuzzy noise: "local", "Clara"), fine-tuning (18 story hits), finetune (18 hits), QLoRA (16 hits), "trained on VRAM" (1 hit), MLX/OR-axolotl multi-term (0, nbHits=0), "LoRA fine-tuning" relevance (0, nbHits=0), fine-tune local LLM relevance (2 hits). Multi-term AND queries and two fetches TIMED OUT at 60s under WebFetch (finetune, QLoRA OR PEFT on first attempt); both recovered on refetch as single-term queries. Reported as observed, not degraded.
- news.ycombinator.com item pages: fetched clean (thread 50016644 read).
- dealroom.co returned HTTP 403 under WebFetch; recovered through the mcp web_reader fallback fetcher (same fallback the 09-28 capture calls canonical, watch/inbox/frontier_olm_20260928/sweep/_raw/nemotron35_fastino_article.md:15-17). Quotes from that fetch only. No fallback success claimed beyond the fetched bytes.

## Pass 1: candidate census

83 rows seen across the queries; 19+ on-topic candidates in-window. The dominant fact of this sweep: the estate's own prior sweeps already banked almost every strong in-window item. Dedup wall verified by grep before banking:

- 10-01 (watch/inbox/frontier_olm_2026-10-01/sweep/finetuning-adaptation-hn.md): duane.sh Qwen3.5-4B, cacheverifier, Ask HN worth-it, Mini-AGI, SecMask, CUA-S1, Shopify Sidekick, arXiv 2609.06986; considered-not-read: MOLT, QLoRA Explained, Local JEV Mac Air, 188M Hindi encoder.
- 10-05 (frontier_olm_2026-10-05/sweep/finetuning-adaptation-hn.md:31,133-138): Clef BANKED with the blog primary fetched via curl (_clef.html) plus 30+ comments.
- 10-06 (frontier_olm_2026-10-06/sweep/finetuning-adaptation-arxiv.md:194-196): arXiv 2610.01493 entropy-rate filtering BANKED, full text read (267,633 B raw).
- 10-07 (frontier_olm_2026-10-07/sweep/finetuning-adaptation-hn.md): Swift-Qwen3.8-27B, Goodfire, LatentMathBench, Astra-no-CoT.
- 10-08 (frontier_olm_2026-10-08/sweep/finetuning-adaptation-hn.md, items 1-8): DeltaTensors, Ask HN worth-it (2nd bank), Cactus Needle 3, duane.sh (2nd bank), easycommand/dirac.run, Laya Studio, EmbeddingGemma 2 primary, MOLT.
- 10-08 open-local sibling (open-local-models-hn.md:111-114): Jiwo decision models banked.
- 10-01 open-local siblings: PewDiePie Qwen 2.5 9B tune dropped twice (video, no measured content, open-local-language-models-arxiv.md:74).
- Out of window / out of scope: 188M Hindi encoder (HN 49587099, created 2026-09-06, before window AND from-scratch pretraining, not adaptation), pi0.5 manufacturing (robotics), NASA-IBM Lunar (domain FM).

Verification-not-rebank reads this sitting (already banked by siblings; my reads confirm their quotes byte-for-byte where re-fetched): Clef blog ("By freezing Qwen3.8-27B for Clef and Qwen3.5-9B for Clef-flash, we jointly optimized the routing head alongside rank-256 low-rank adapters."), duane.sh ("Training went through the 24,000 examples once, on one rented H100 GPU, in 1.6 hours, for about $7."), dirac.run ("The 4-bit versions surprisingly keep most of the gains of the 16-bit versions, and they are convenient to run on CPU systems."), MOLT README ("Thermally aware, memory-efficient QLoRA fine-tuning for consumer NVIDIA GPUs." + "This is complete single-seed development evidence, not a universal superiority claim." + PolyForm Shield 1.0.0 license, v0.12.0, 2 stars).

## Pass 2: banked items (5, strongest first; all read end to end this sitting)

### 1. One Model Family, Two Gold-Level Results: Fine-Tuning Nemotron for IOI and IMO (NVIDIA HF blog, HN 49995058, 2026-10-07)

- URL: https://huggingface.co/blog/nvidia/nemotron-ioi-and-imo-2026 (read in full).
- Quote (verbatim): "It scored 30 out of 42 points, including full credit on four of the six problems, and exceeded the official gold-medal threshold."
- Why: RQ2 frontier answer at the top of the scale. Nemotron-3-Ultra-CC (550B total / 55B active) hit IOI 2026 535.4/600 and IMO 30/42; Nemotron-3-Nano-CC (30B total / 3B active) reached 468 on IOI 2025 (gold 438.3) with SFT + RL + GenCorrect generate-evaluate-refine. Method is FULL SFT+RL on curated data (22k programming problems with synthetic traces; 414,890 SFT + 9,597 RL proof examples), "The medals were not produced by fine-tuning alone, and they were not produced by brute-force sampling alone." Weights, both training datasets, checkpoints and Nemotron-IMO-Bench released. The inference-side loop (generate, score, critique, refine) is the stealable part for janitor-scale verification; the training side prices what the estate does NOT do (frontier RL runs).
- Overlap: catalog holds the Nemotron-3-Nano-30B-A3B family as MLX INFERENCE model cards only (catalog.jsonl ids 6f5c258a82bd, 57c324bc6ab3, be9aefe099fa et al., mine/raw/agent_bleeding_edge/exo-explore/); sibling bank of 2026-09-28 covered a DIFFERENT Nemotron fine-tune article (Fastino Lightning, _raw/nemotron35_fastino_article.md). grep nemotron-ioi across today's sweep dir: 0. New.

### 2. Local JEV, fine-tuned in under 30 minutes on a 16 GB MacBook Air (shmcsensei, HN 49831831, 2026-09-24)

- URL: https://shmcsensei.github.io/easy-jev-fine-tune/ (read in full).
- Quote (verbatim): "I trained it on 10,003 banking messages in under 30 minutes--on a 16 GB MacBook Air." (em-dash in source rendered as --)
- Why: RQ1's cleanest in-boundary consumer result. SmolLM2-135M + LoRA on Banking77: exact intent accuracy 1.62 to 83.25 percent, operational decision accuracy 47.99 to 92.01, calibration error 27.39 to 6.78; a 0.70 confidence threshold automates 67 percent of traffic at 98.45 percent decision accuracy on accepted cases and routes the rest to human review. Serving: p50 35.16 ms on the same Air. The architectural sentence is estate law in the wild: "That separation matters. The model estimates what the customer needs. Ordinary, inspectable code decides what the product should do about it." That is exactly our janitor-proposes/switchboard-authorizes split, trained in half an hour on the smallest rung of the T0/T1 ladder.
- Overlap: considered-not-read on 10-01 (frontier_olm_2026-10-01/sweep/finetuning-adaptation-hn.md:9); no catalog or memory rows (grep easy-jev / shmcsensei = 0). My read is the first. New.

### 3. Fine-tuning STT models to help with my Lisp, part 2 (vivekkairi.com, HN 49917734, 2026-10-01)

- URL: https://vivekkairi.com/fine-tuning-stt-models-to-my-speech-part-2/ (read in full; the HN title's "Lisp" framing is not restated in the fetched page text - motivation given as base-model WER on the author's speech).
- Quote (verbatim): "I trained Whisper using LoRA, for Parakeet I decided to finetune the whole encoder."
- Why: the adapter-vs-full counterexample at 0.6B. NVIDIA Parakeet TDT 0.6B v2, FULL encoder fine-tune (decoder + joint frozen) on 720 self-recorded Harvard sentences, later doubled to 1,296 clips by padding with 0.2-1.5 s room silence (silence distribution was the transfer killer: run 1 aced the test split at 11.26 but hit 40-50 percent WER on new sentences with leading/trailing silence; run 2 with augmented clips: 6.14 test, 5.29 with-silence). Trained on Kaggle free tier, served int8 ONNX on an M4 Pro CPU, encoder 2.4 GB to 622 MB. Estate feeds: (a) consent-clean adaptation template - one person's own voice, zero third-party speakers; (b) the augmentation lesson is the corpus-law lesson: fix the DATA distribution, not the loss; (c) sub-1B full-parameter tuning is routine and cheap, no LoRA needed.
- Overlap: grep "lisp|stt model" across sibling sweeps 2026-09-28..10-09: 0 hits. New.

### 4. Ask HN: Are you a subscribed LLM or a locally deployed open-source model? (HN 50016644, 2026-10-09, 13 comments)

- URL: https://news.ycombinator.com/item?id=50016644 (thread read end to end).
- Quote (bravetraveler, verbatim): "despite my employer both demanding 'the frontier' and providing unlimited spend/quota" (preceded in-thread by "Open models exclusively on hardware I own").
- Why: LENS 2 consent-boundary signal, same-day. The 13-comment split: subscription default for ease (gkoenig: "I do not have the personal budget for a machine powerful enough, or I am not knowledgeable enough to know how to get one for 20$/month"; zephyreon "one shot it"); local chosen for cost-at-scale testing (rahuljha0403: "I exhausted free limit in just 5-7 hrs of testing when I used hugging face api") and for sovereignty-by-default (bravetraveler runs own hardware against unlimited employer spend, explicitly to prove deliverables without tracked token usage). olvy0's cleanup-cost rant (AI features took as long to fix as hand-writing: "comment slop," hidden bugs) is the hidden-cost counterweight. The estate's local-first stance is the minority position even on HN, which is exactly why it is a moat.
- Overlap: grep 50016644 and "subscribed|locally deployed" across today's sibling sweeps: 0 hits. New.

### 5. Latham & Watkins buys Nvidia servers to fine-tune open weights in-house (Dealroom, HN 49702607 + 49698231, 2026-09-14)

- URL: https://dealroom.co/news/150680-latham-watkins-buys-nvidia-servers-to-fine-tune-open-weights-in-house/ (WebFetch 403; read via mcp web_reader fallback).
- Quote (from the fetched page, verbatim): "Latham & Watkins is buying Nvidia servers to fine-tune open-weight models in-house"
- Why: sovereignty-adjacency going mainstream: a top US law firm procuring local compute to fine-tune open weights on privileged client data instead of sending it to frontier APIs. Same wave as the Nvidia+Palantir 30B sovereign story (HN 49743986, 2026-09-17, unbanked, listed not read). Validates the estate's consent-boundary thesis from the enterprise end: the T0/T1 line is not just an austerity law, it is what regulated industries are buying. Caveat: the page cites the Financial Times, which I did NOT read (paywalled); this is a secondary source.
- Overlap: grep latham|dealroom across sibling sweeps: 0 hits. New.

## RQ answers (grounded)

- RQ1 (consumer-GPU LoRA/PEFT since 10-01, inside T0/T1): the in-window consumer results were already banked by siblings (easycommand 10-05 CPU-runnable 4-bit; MOLT Windows-laptop QLoRA 10-08; EmbeddingGemma 10-08). This sweep's NEW additions bracket the boundary: Mac Air (16 GB, 30 min, item 2) and Kaggle-free Parakeet (item 3) train fully off-estate; duane.sh's $7 rented-H100 tier (re-verified byte-for-byte this sitting) is the single exception that needs an operator ruling on the T0/T1 line - the GPU_LADDER gate guards serving, not training (10-08 sweep, item 4, citing memory/rib/RIB_GPU_LADDER_20261001.md).
- RQ2 (adapters vs full-parameter for sub-8B): the scale gradient across my reads: 27B/9B frozen backbone + rank-256 LoRA (Clef, production), 4B LoRA r32 + DPO + GRPO (duane.sh), 1.5B LoRA SFT (easycommand), 0.6B FULL encoder fine-tune (Parakeet, item 3), 550B/30B full SFT+RL (Nemotron, item 1). Adapter tuning is the default exactly where the frozen base is a shared asset (>=4B); at <=1B full-parameter is standard and cheap. On the corpus library: the ask's 52,313-row curriculum figure I could NOT confirm on disk - catalog/catalog.jsonl reads 1,343,390 lines (wc -l this sitting), memory/lenses/corpus_index.json is research_lens.v1 with count=107; whether any curriculum surface holds training-ready primer bytes vs inference captures stays OWED. The captures I saw (state/arxiv/*.txt, HTML chapters) are prose, not SFT pairs; no dataset-format rows surfaced in my greps. Inference-only is the working assumption, unproven.
- RQ3 (does weight adaptation break the skills_pack magnet): the magnet is code-addressable: mag/knowledge_graph.py:164 sets maps_to = "mag/skills_pack.py" for precedent rows (see also mag/knowledge_graph.py:142-145 pointing at mag/skills_pack.py:99-106 and mag/skill_ledger.py:137 decision.v1 rows). The ask's 287-edge figure I could NOT verify locally: grep -c case_law on memory/mycelium/edges.jsonl = 0 (no case_law, case-law, or caseLaw variant). Structural answer from the reads: adapters and the skill ledger live on different axes - Parakeet/MOLT/Clef all ship PEFT-compatible safetensors adapter FILES bound to one base model, while the ledger is replayable text proven by re-execution; adapting a janitor does not move any precedent row. Keep compounding the ledger; treat an adapter shelf as a second, model-scoped artifact with its own provenance (base-model hash + dataset receipt), or the DeltaTensors sha-parent chain already banked 10-08.
- RQ4 (day-8 mine verifiable through the green arXiv door in one funded session): the day-8 mine is watch/inbox/frontier_olm_2026-10-01/sweep/ (36 sweep files on disk, 9 areas x 4 doors; the ask's "32 unbanked" I could not reproduce - the 10-06 lens counted 28 finetuning items across the four door files). Already arXiv-verified since then: 2610.01493 (full text, 10-06) and 2609.06986 (abstract-level, 10-01). The day-8 OWED FT-vs-RAG ablation is NOT arXiv-verifiable - no paper in my census measures it; it needs an estate run. What one funded session CAN verify from today's arxiv sibling list (frontier_olm_2026-10-09/sweep/finetuning-adaptation-arxiv.md:12,60: 40 fresh on-topic hits incl. 2610.09934, 2610.11655, 2610.04507, frozen-B study 2610.06621 "freezing B trails free LoRA by 8-18 points", MOLT 2610.05748): abstract-level claim checks on roughly 10-20 papers, enough to bank or strike the sibling's unread candidates.

## Overlap instruments run this sitting

wc -l catalog/catalog.jsonl = 1,343,390. grep -i qlora|lora catalog: 209 rows (model cards and captures, none matching today's banked URLs). grep mini-agi|cactus needle|deltatensors|clef|nemotron catalog: only Nemotron inference-card rows. memory/ recursive grep (mini-agi...easy-jev): only incidental substrings in DLB book chapters and a biography PDF. Sibling-sweep greps as cited per item. No re-banking; every banked item above is absent from all sibling sweep files and prior-day finetuning sweeps.

## OWED

1. Corpus curriculum primer-bytes audit: does ANY 52,313-row curriculum surface exist, and is it inference captures or training pairs? (RQ2, unproven this sitting.)
2. case_law edge count under the ask's lens numbering: find the real tag/location backing "287 case_law edges mapped to one module" (edges.jsonl has zero under every spelling tried).
3. FT-vs-RAG ablation at 2B on estate-law jargon (carried from 10-01, still owed, not arXiv-answerable).
4. Operator ruling: does a $7 rented-H100 training pass violate the T0/T1 boundary when the artifact (adapter) lives local? (duane.sh economics make this a real decision, not a hypothetical.)
5. Nvidia+Palantir 30B sovereign fine-tune (HN 49743986): listed, not read; thenewstack URL not captured by Algolia output this sitting.
