# SWEEP: quantization-compression via x (2026-10-07)

Area: quantization-compression. Door: X per the ask's recipe - WebSearch `site:x.com`
queries, single posts resolved through the fxtwitter door
`https://api.fxtwitter.com/<user>/status/<id>` (JSON, no login), plus the
syndication-timeline harvester inherited from the day-6 x sweep
(`watch/inbox/frontier_olm_2026-10-06/sweep/_raw/bing/parse_synd.py`, parser shape
reused in `tmp_synd_quant.py` in this dir). Stamp: source-fetched: 2026-10-07. Seat:
sweep-quantization-compression-x.

## Doors: what worked, what degraded (honest)

- WebSearch `site:x.com`: usable but rate-limited and noisy. Queries built from exact
  quant jargon worked (Q4_K_M, IQ1_M, KLD, "R4 quant", "126 TOPS"); generic phrasings
  returned either backend 429/1302 rate-limit errors or non-X results. Many hits
  resolve only to the profile root with no status ID, which the recipe covers by
  snippet-banking (two such items are banked below, marked snippet-tier).
- fxtwitter door: 7/7 successful resolves, including X long-form ARTICLES - an article
  whose public URL is `x.com/<user>/article/<id>` resolves at
`api.fxtwitter.com/<user>/status/<id>` and returns the article metadata plus a detailed
  content summary. The direct `x.com/i/article/<id>` URL 404s for anonymous fetch; the
  article body is only reachable through the parent post's fxtwitter JSON. This is how
  the KLD article, the local-models guide, and the EVO-X3 piece were read.
- Syndication door (`syndication.twitter.com/srv/timeline-profile/screen-name/<handle>`):
  first burst of 12 handles worked, then hard-429'd. Fresh timelines: UnslothAI, ollama,
  typesafeai, Togethercompute, rasbt. Stale embeds (no in-window rows): ggml_org,
  ggerganov, vllm_project, DeepSeek_AI, lmsysorg. Empty: ikawrakow, Qwen_Qwen,
  eleutherai, SOTAAZ, BrandonMusicKy (0 tweets - article-only account), above_spec
  (NEXT_DATA present, 0 tweet objects). Second batch (danielhanchen, reach_vb,
  rohanpaul_ai, HuggingFace) 429'd twice with 20-45s pacing. Fermonroyh embed carries
  only 2022-2023 posts. Raw dumps kept at `_raw/synd_*.html`.
- sotwe.com mirror: 403. web_reader MCP: 429. nitter mirrors: known dead (day-6 x sweep
  recorded the JS-challenge walls; not retried).

## Pass 1: candidate pool (30+ considered)

In-window means 2026-09-07..2026-10-07. Pool by source:

Search-discovered (x.com): @Dev_trader0 2085101341794316539 (2026-08-05, llama.cpp
learning checklist incl "compare Q4_K_M, Q5_K_M, and Q8_0"); @zettelkastten article
2085438554885193947 (2026-08-06, quant compendium); @BrandonMusicKy KLD article
2102950326487703652 (2026-09-24); @ankit_appy (KV-cache formats benchmarked on
Gemma-4-31B, no ID found); @Fermonroyh (Qwen 3.6 27B dense, "single file agentic
benchmark series", Q4_K_M 16GB then Q8_0, no ID); @Shiken_Tei (UD-IQ tier size list,
no ID); X "LLM Community" imatrix explainer (no ID); a local-AI setup guide citing
GLM-5.2-GGUF UD-Q4_K_M ~373GB sizes (2026-06-21, out-of-window); an experimenter post
on "tool calls and the degradation caused by quantization" (no ID); @gmktecdotcom
EVO-X3 article 2076949207433535653 (2026-07-14); @above_spec (ik_llama.cpp R4 quant,
"faster than the 5070 Ti... consistent from 0 to 139k context", no ID); "Kimi K3
Shoves Routing Into The Hot Path" article (2026-07-24, out-of-window, dropped);
@rohanpaul_ai ChunkKV post (paper is 2025-02, out-of-window, dropped);
@JakeKAllDay 2102483667536781387 (2026-09-22, KV cache VRAM article pointer - found by
reading the day-6 sibling's raw reddit dump, which cites this X URL).

Syndication-discovered (in-window rows): UnslothAI 15 in-window rows (6 quant-matched:
EmbeddingGemma 2 GGUF 2026-10-06, DGX "faster quantization" 2026-09-23, 500M downloads
2026-09-23, Qwen-Image-2.1 FP8+GGUF Desktop 2026-09-23, Qwen-Image-2.1 12GB GGUF +
Dynamic FP8 6GB 2026-09-22, Qwen3.8-27B GGUF #1-most-liked 2026-09-08); ollama 29
in-window rows (none quant-specific; EmbeddingGemma 2 pulls); typesafeai 37 (Jev
surface, no quant); Togethercompute 25 (Beam/GLM flash, no quant); rasbt 1. Stale pools
triaged and discarded: ggml_org 30, ggerganov 116, vllm_project 150, DeepSeek_AI 99,
lmsysorg 122 (all pre-window embeds).

Off-door leads surfaced by the searches, recorded NOT banked (not X reads):
particula.tech claim "FP8 KV cache fell from 91% to 13% on a 128k needle test";
sotaaz.com llama.cpp q8_0-KV A100 measurement (2.1 GiB saved at 32K, decode at ~55% of
f16 speed at 64K depth); avenchat.com "Gemma 4 Q4 vs Q8: Which Quantization to Actually
Download"; the Kyojin Strix-Halo EXL3 pack (r/LocalLLaMA 1wwocik - already held raw by
the day-6 sibling at `watch/inbox/frontier_olm_2026-10-06/sweep/doors/ff_arctic_posts.jsonl`,
unbanked).

## Pass 2: deep reads (7 items fetched and read end to end via fxtwitter this session)

1. @JakeKAllDay 2102483667536781387 (2026-09-22, 1,781 views) + its linked X article
   "You're Probably Spending Way Too Much VRAM on KV Cache"
   (x.com/i/article/2101730612021530624, read via the post's fxtwitter JSON summary).
2. @BrandonMusicKy (with @Phaelon74) article 2102950326487703652 (2026-09-24),
   "Reading KLD: What Those Nats Mean for Your Quant's Usability".
3. @zettelkastten article 2085438554885193947 (2026-08-06), "How to Run Large Models
   Locally (and for Free). Quantization".
4. @gmktecdotcom article 2076949207433535653 (2026-07-14), "126 TOPS Isn't the Whole
   Story: What EVO-X3 Reveals About Real-World Local LLM Performance".
5. @UnslothAI 2102431304591761728 (2026-09-22, 358,329 views), Qwen-Image-2.1 GGUF
   12GB + Dynamic FP8 6GB.
6. @UnslothAI 2102786338500333960 (2026-09-23, 51,484 views), 500M downloads,
   Qwen3.8-27B GGUF #1 most-downloaded ever.
7. @Dev_trader0 2085101341794316539 (2026-08-05, 6,646 views), llama.cpp learning
   checklist (quant trade-offs among seven named areas; read, judged too thin to bank).

## Answers to the five research questions (X-door slice)

- RQ1 (owed qwen2.5:7b Q4_K_M vs q8_0 task-graded A/B - what do published task-graded
  comparisons at 7B report?): The estate ALREADY holds the strongest external
  task-graded X material (10-01 x sweep, not re-derived here): superalesha's 08-20
  bake-off (5 stacks, 40 arms: AWQ INT4 90.0 / NVFP4 89.3 / GGUF Q4_K_M 89.3 / FP8
  88.7 pass@1, McNemar tie at 27B-class) and outsource_'s 08-15 runbook (Q4 14/22 vs
  Q5 15/22 vs BF16 on 27B). NEW increments this session: (a) the KLD article FULL READ
  (the 10-01 sweep banked only the pointer and marked the essay OWED - see item 2): at
  the adjacent 8B scale Q8_0 = 0.0014 nats vs Q4_K_M = 0.031 nats, Q4_K_M "picks a
  different top token than FP16 at about 8% of positions", Q2_K matches only ~71% -
  and its explicit thesis that KLD must be PAIRED with task results, never trusted
  alone; (b) the zettelkastten guide citing an IJCAI 2025 study: 70B holds 4 bits
  well, small models drop catastrophically - so the Q4 arm should bite harder at 7B
  than at 70B, matching the estate's 0.6B cliff shape; operating rule "70B@Q4 usually
  beats 8B@FP16 at equal VRAM" prices the cross-over; (c) snippet-tier: @Fermonroyh
  runs a "single file agentic benchmark series" on Qwen 3.6 27B dense explicitly
  trying Q4_K_M ("only 16GB, totally fits") then Q8_0 - exactly the estate's A/B shape
  at 27B, but the delta numbers did not surface through this door. NET: at 7B the
  published world still has NO task-graded Q4_K_M-vs-Q8_0 number; the A/B remains the
  estate's to run, the mechanism (8% top-token disagreement compounding over
  multi-step agentic loops) is the thing to measure, and per the 10-01 steal the KV
  axis can be pre-spent to q8_0/TQ class before the weight arm matters.
- RQ2 (protected-spine / mixed-precision late-2026 best practice + open
  implementations): VeriLoop (banked day-6, register row 15) stays the estate's ladder
  anchor. NEW X evidence sharpens WHERE the spine goes: the KLD article's MoE section
  measures that under quant, ROUTING is what breaks - Qwen3.6-35B-A3B FP8 shows ~36% of
  expert-routing choices differing from reference, and FORCING reference expert IDs
  drops KLD from 0.0173 to 0.0076 (more than half the damage is router, not expert
  weights). Combined with zettelkastten's AWQ note (protecting ~1% salient channels
  sharply cuts error, AutoAWK ships open) and llama.cpp's built-in imatrix ("Below
  Q5_K_M an imatrix is highly recommended; a Q2 quant without one is broken"), the
  late-2026 open-implementation answer is: imatrix + AWQ salient-channel + per-layer
  dynamic mixes (Unsloth UD tiers) for dense, and protect-the-router for MoE. No new
  open mixed-precision implementation shipped on X this window.
- RQ3 (does the day-6 cliff bf16 0.757 / Q8_0 0.750 / Q4_K_M 0.703 replicate in
  published sub-1B ladders; where do IQ quants sit): directionally yes, via the
  zettelkastten guide's IJCAI-cited small-model catastrophic drop at 4 bits vs 70B
  robustness, and via the KLD tier table where Q8_0 sits in the "Golden Zone" (<=0.05
  nats, "indistinguishable in everyday use") - consistent with the estate's measured
  Q8_0-almost-free at 0.6B. No new sub-1B quant ladder published on X this window;
  IQ-quant placement on the curve remains carried by the banked VeriLoop ladder
  (protected-spine IQ1_M > uniform IQ2_S on same-top-p) plus the KLD article's
  i-quant ~2.0 bits-average note.
- RQ4 (KV compression frontier under local long-context serving; who optimizes
  retained token count like BreadthKV): STRONGEST X FIND OF THE SWEEP - @JakeKAllDay
  (llamAmpere author), 2026-09-22: on a Qwen-class hybrid linear-attention model
  (~75% of layers skip full KV attention), task-graded KV quant (GPQA Diamond +
  LiveCodeBench, 120 questions, repeated seeds) shows NO statistically significant
  quality difference for TQ5/TQ4 vs 8/8 KV; 8/8 at 256K context costs 17.8 GB VRAM vs
  ~9.8 GB at TQ5/TQ4; KV KLD (~0.0039 nats at 8/TQ3) is dwarfed by 4-5-bit weight
  quant error (~0.0065); KV divergence does NOT grow with context length on hybrid
  architectures; below 11 total bits split K/V uniformly (4/4 beats 5/3); avoid 2-bit
  weight quants. This complements banked BreadthKV (buy-count-before-fidelity at
  decode time) from the opposite side: JakeKAllDay buys VRAM at ~zero fidelity cost at
  serve time; the two COMPOSE (more retained tokens AND cheaper per-token KV). The
  reddit companion post (1wsmtd4, already held raw by the day-6 sibling) adds KVaRN as
  the next-release lane. Snippet-tier corroboration: @ankit_appy benchmarks two KV
  cache formats on Gemma-4-31B "and what the numbers actually mean for people who use
  long context" (unresolved).
- RQ5 (CPU/Vulkan-specific quant for 2B-9B): the X door produced no in-window
  Vulkan-specific quant benchmark. Nearest measured non-CUDA data: the GMKtec EVO-X3
  article (2026-07-14, vendor self-test, out-of-window) - AMD Ryzen AI Max+ 395 (Strix
  Halo, 128GB LPDDR5X-8000 unified memory, Radeon 8060S): gpt-oss-20b Q4_K_M at 65
  tok/s / 0.99s TTFT; Qwen3-30B-A3B GGUF 65 tok/s; DeepSeek-R1:32B only 10 tok/s -
  conclusion "TOPS is only theoretical potential", memory bandwidth + architecture +
  active params dominate. Snippet-tier: @above_spec on ik_llama.cpp's R4 quant
  ("Faster than the 5070 Ti on mainline llama.cpp. Performance stays consistent from
  0 to 139k context") - ik_llama.cpp is the CPU/AVX-optimized fork, so its quant
  formats are the closest public CPU-class evidence; unresolved this session. The
  estate's 12x Vulkan-vs-CPU claim stays tier-2 unconfirmed externally.

## Dedup / overlap ledger (greps run this session)

Instrument: targeted `grep -c/-rc` over `catalog/catalog.jsonl` and
`watch/inbox/frontier_olm_2026-10-0{5,6,7}/`, plus ripgrep
(`rg -i --max-filesize 20M`) over catalog.jsonl + the full 9.3GB `memory/` tree, plus
a read of the 10-01 sibling's quantization-compression-x.md after its catalog rows
surfaced. Results:

- JakeKAllDay / llamAmpere / JakeATX: catalog 0, memory 0 (ripgrep over the full 9.3GB
  memory tree, 20MB file cap). The X URL appears ONLY inside unconfirmed raw dumps
  held by the day-6 sibling (ff_arctic_posts.jsonl:32 carries the citing reddit body;
  as_rows.jsonl, search HTML caches) - never resolved, never banked. NEW as an X-door
  item; the sibling holds the citing reddit post raw (r/LocalLLaMA 1wsmtd4,
  llamAmpere v0.4).
- "8-13 bits" KV rule, TQ5/TQ4, TurboQuant 5/5: 0 hits catalog + frontier dirs +
  memory. NEW.
- Reading KLD / BrandonMusicKy: catalog holds TWO rows pointing at raw fetches made by
  the 10-01 sweep (`catalog ids a8e3d1a5f638 + e1010f686330`,
  `watch/inbox/frontier_olm_2026-10-01/sweep/_fx/BrandonMusicKy_status_2102950326487703652.json`,
  19,895 bytes, mtime 2026-10-01T14:37:54Z). The 10-01 x sweep banked item 8 as the
  essay POINTER with "essay 404s through the door: degraded, OWED read via another
  door" (its sweep file line 40) and its DIGEST recorded "X long-form article door is
  down... Six article bodies were never read". THIS session read the article body via
  the /status/ resolution path (their probes used only i/article paths). Item 2 below
  therefore DISCHARGES that owed read; the banked increment is the article content
  (tier thresholds, 8% divergence, MoE routing damage), not the pointer. Thematic
  overlap STATED with the banked VeriLoop Mean-KLD ladder (day-6 register row 15):
  same metric family, different source.
- The 10-01 sibling's "article door is down" law is hereby CORRECTED for the estate:
  fxtwitter resolves X long-form articles at `api.fxtwitter.com/<user>/status/<id>`
  when the numeric article ID is known; only the `i/article` paths 404. Three of the
  six never-read 10-01 articles may be recoverable this way (their raw `_fx` receipts
  hold the pins).
- zettelkastten / "How to Run Large Models Locally": catalog 0; memory 1 incidental
  visit in memory/trajectory/steps.jsonl (URL trace, not a holding). NEW.
- EVO-X3 / gmktec: catalog 0, memory 0. Strix Halo PLATFORM appears in unbanked
  sibling raw candidates (Kyojin 1wwocik, agentionai 1wo7sfo - ff_arctic_posts.jsonl),
  not in register/percolator/DIGEST (grep: 0). NEW.
- Qwen-Image-2.1: considered by the day-6 x sweep pool
  (inference-efficiency-x.md:15 "Qwen-Image-2.1 VRAM cuts"), NOT banked there; catalog
  0. The 2026-09-22 post + numbers are the new increment.
- Unsloth 500M / "most-downloaded": the 2026-09-08 "most-liked GGUF" row was in the
  day-6 considered pool; the 2026-09-23 500M + #1-most-downloaded-ever row is NEW.
- GLM-5.3-Flash 3.3x (2095852388888522890): SIBLING-BANKED day-6
  (inference-efficiency-x.md banked item 1) - not re-banked here.
- Fermonroyh / ankit_appy / above_spec / Shiken_Tei: catalog 0; frontier-lens hits are
  inside raw search caches only. Snippet-tier NEW.
- Estate-internal anchors NOT re-derived: the 0.6B decision ladder (reddit 1wn0gga,
  day-6 register row 14), VeriLoop E2 GGUF ladder (1wpwdxl, row 15), BreadthKV
  (2610.05685), BARQ (2610.04490) - all per the 10-07 lens burns.md:95-98, :112-113;
  and the 10-01 x-sweep banks (superalesha bake-off, outsource_ runbook, TeksEdge
  Xing4.0 + MiniCPM5-2B, Qwen3.5-4B KLD-vs-speed Lunar Lake row, AD-Q4_K_M
  task-conditioned template) per `frontier_olm_2026-10-01/sweep/quantization-compression-x.md`
  items 1-8 and its register.

## Banked items (strongest first; quotes verbatim from fxtwitter JSON fetched this session)

1. KV cache bits rule, task-graded (JakeKAllDay, 2026-09-22). "If you're running 8/8
   on your KV cache, good news: you should probably run 8-13 bits instead." + article:
   GPQA/LiveCodeBench no-significant-difference at TQ5/TQ4, 17.8 vs ~9.8 GB at 256K,
   hybrid KV divergence flat in context, 4/4 beats 5/3 below 11 bits, KV error dwarfed
   by 4-5-bit weight error, avoid 2-bit weights. Feeds the owed 7B A/B design directly
   (weight quant is the axis that matters; KV can be spent down to ~9-13 bits first).
2. Reading KLD (BrandonMusicKy + Phaelon74, 2026-09-24). DISCHARGES the 10-01 sweep's
   owed read (they banked the pointer, essay body unreadable through their door
   paths). KLD usability tiers (<=0.05 golden / 0.05-0.10 highly stable / 0.10-0.15
   viable / 0.15-0.30 noticeable / >0.30 trash), Q8_0 0.0014 vs Q4_K_M 0.031 nats at
   8B, Q2_K matches FP16 top token only ~71%, MoE routing damage (36% routing choices
   differ at FP8 on Qwen3.6-35B-A3B; forcing reference experts halves KLD 0.0173 ->
   0.0076). The estate's VeriLoop meters gain a published interpretation scale.
3. Quantization compendium (zettelkastten, 2026-08-06, out-of-window disclosed).
   Q4_K_M = 4.89 bits/weight actual, Q8_0 = 8.50; imatrix required below Q5_K_M;
   AWQ ~1% salient-channel protection; GPTQ 3.25x A100 speedup; 70B@Q4 > 8B@FP16 at
   equal VRAM; small models can drop catastrophically at 4 bits; KV: FP8 halves, NVFP4
   cuts ~75%, E4M3 preferred over E5M2, at long context KV spend "often buys more
   than everything else combined".
4. EVO-X3 non-CUDA serving table (gmktecdotcom, 2026-07-14, out-of-window, vendor
   self-test). gpt-oss-20b Q4_K_M 65 tok/s / 0.99s TTFT on Strix Halo 128GB; 10-65
   tok/s spread across architectures on identical hardware; TOPS is not throughput.
5. Qwen-Image-2.1 GGUF 12GB + Dynamic FP8 6GB (UnslothAI, 2026-09-22). Dynamic
   precision with offload as the low-VRAM serving pattern for a 7B-class model.
6. Qwen3.8-27B GGUF = #1 most-downloaded model ever, 500M total (UnslothAI,
   2026-09-23). Ecosystem datum: the quantized 27B class is the local world's actual
   workhorse - the estate's qwen2.5:7b A/B rides the same rail family.
7. SNIPPET-TIER: Qwen 3.6 27B single-file agentic benchmark, Q4_K_M then Q8_0
   (Fermonroyh, date unknown). The exact estate A/B shape externally; numbers did not
   clear the door.
8. SNIPPET-TIER: ik_llama.cpp R4 quant, "faster than the 5070 Ti... 0 to 139k context"
   (above_spec, date unknown). The CPU-class quant lane's performance claim; unresolved.

## Falsifier / caveats

- Items 2-4 are X long-form articles read through fxtwitter's JSON summary of the
  article (the door's only readable form); the summary is machine-extracted, so
  verbatim-quote fidelity is per that JSON, not per the rendered article page.
- Item 4 is a vendor testing its own product; treat as directional only.
- Items 7-8 are search-snippet banks per the recipe's unresolved-thread clause; quotes
  are the search snippets, confidence 0.35, and both carry profile-root URLs because
  no status ID cleared any door.
- Out-of-window items (3: 2026-08-06, 4: 2026-07-14) are kept with dates disclosed,
  same as the day-6 x sweep's item-1 precedent; both are unbanked anywhere in catalog
  or memory.
- No pytest, no live ollama runs this session; every claim above traces to a fetched
  URL, a raw file, or a grep named in the ledger.
