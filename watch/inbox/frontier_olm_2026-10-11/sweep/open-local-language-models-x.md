# SWEEP: open-local-language-models via x (frontier_olm_2026-10-11)

source-fetched: 2026-10-11. Seat: sweep gopher, x door. House laws held: ascii only, no em
or en dashes, every claim cites what was read or run this sitting. Banked items carry
verbatim quotes from pages fetched this sitting; anything not observed is marked OWED.

## Door status (X surface, this sitting)

- WebSearch with site:x.com queries returned ZERO x.com results across 8+ query shapes
  ("open weights" release, Qwen, local LLM llama.cpp, status/2108 snowflake shapes,
  site:techwitter.com, site:threadreaderapp.com). X blocks crawler indexing; the search
  path to post IDs is dead, not throttled.
- nitter.poast.org/MistralAI: getaddrinfo ENOTFOUND (host dead).
- fxtwitter: healthy but per-post only. api.fxtwitter.com/MistralAI returns profile fields
  only (screen_name, followers 222359, tweets 190, NO timeline, NO statuses). Post
  resolution needs an ID already in hand.
- The estate's own radar DID catch one load-bearing X post this window:
  memory/runs/x_reply_radar/out_2026-10-07.json holds the MistralAI announcement snippet
  "Meet Mistral Large 4, aka Le Chonk. - 1T parameters, natively multimodal. 49B active."
  at 38,367 likes, plus top reply "me with 12 GB of VRAM reading 'open weights, 1.05T
  parameters'" (1,767 likes, @anxuanng). Note the radar snippet says 49B active while the
  primary blog says 52B active: a third number for section 5 below.
- Snowflake check run this sitting: the estate's own banked post
  x.com/NachoQuixotic/status/2083554359439147211 (watch/inbox/
  nacho_aug1_plain_english_seed_20261011/POST.md:3) decodes to 2026-08-01T14:04Z, matching
  the card's stated stamp, so Oct 2026 IDs live in the ~2108+ range; the one "MistralAI"
  status link search surfaced (19575160080437292, 17 digits) decodes to mid-2025 and is
  truncated, so it was NOT resolved and NOT banked.
- Verdict per recipe: the resolution door works, the discovery door is degraded. Items are
  banked through their primary pages (fetched this sitting) with the degradation named.
  The x-history miner (named cure, commit e8eedd8eb) stays OWED.

## Pass 1: candidates (36 considered, 2026-09-11..2026-10-11)

1. Mistral Large 4 preview, 1T MoE, weights due end of Oct (2026-10-06, mistral.ai)
2. Reflection AI Beam unveil, 501B/23B MoE, Apache 2.0 weights later Oct (10-05)
3. vLLM Vera Rubin NVL72 day-0 support, 7.84x over GB200 (10-09, blog.vllm.ai)
4. vLLM DeepSeek-V4.1-Flash 5x agentic post (10-07, blog.vllm.ai)
5. vLLM disaggregated serving guide (09-29)
6. vLLM watermarking post (09-24)
7. vllm-metal concurrent serving on Apple Silicon (09-22)
8. vLLM Kimi K3 2.8x throughput post (09-13)
9. llama.cpp b11325 (10-01, newreleases.io)
10. Ollama structured outputs single-pass on thinking models (09-23, roundup; ollama.com/notes 404'd)
11. Ollama v0.34.2 desktop + first-run local-only option (late Sep)
12. GLM-5.3-FlashX weights (09-18)
13. Anthropic analysis: GLM-5.3 weights autonomously build exploit code (late Sep)
14. Nvidia in talks to acquire or invest in Reflection AI (10-10, FT)
15. Nous Research $90M Series B at $1.5B + Hermes for Businesses (10-07)
16. BenchLM: 50% of 889 tracked models open-weight as of 10-10
17. Xiaomi MiMo-V2.6-Pro 1.02T/42B MIT (09-21, felloai roundup)
18. Qwen Image 2.1 Pro lands on LLM Gateway (10-05)
19. HF daily papers: TokenRouter efficient routing (this week)
20. HN Ask: Best Local LLM Box? (10-11, fetched via Algolia items API: zero comments)
21. HN: SRA-RiskGate-4B stablecoin risk gate (10-05, repost 10-10)
22. HN: Local LLM Inference at Scale with vLLM, data4sci (10-09/10-10)
23. HN: All local LLMs on all Apple devices, simulkit (10-05)
24. HN: Shlexball, local 1.5B file finder on Mac (10-04)
25. HN: NobodyWho "When Chat Templates Go Wrong" (10-02)
26. xda: free local LLM replaces $20 subscriptions (10-07, 52 pts)
27. Aleph Alpha Kolibri 78.1B/3.46B active (10-03) - ALREADY BANKED, adhoc register row 23
28. Kisoku 1.6B scratch-trained (10-08) - ALREADY BANKED, adhoc register row 18
29. Windows ML experimental llama.cpp (10-07) - ALREADY BANKED, adhoc register row 14
30. Mozilla local-LLM server benchmark (09-17) - ALREADY BANKED, adhoc register row 13
31. Sunk Cost 3090 rig thread (09-15) - ALREADY BANKED, adhoc register row 11
32. Qwen3.8-Flash-Next GSQ quant (09-14) - ALREADY BANKED, adhoc register row 10
33. ML4 parameter-count conflict analyses (10-06, shattered.io + llm-stats)
34. Gemma 4 12B + MAI models roundup (chooseto.co, date unverified, not banked)
35. Open-source AI tooling briefing October 2026 (essamamdani.com, not banked)
36. arXiv 2610.11959 MiMo-V2.6 RL paper stub (10-09, already in catalog, row 3dae8d20f9dd)

## Pass 2: end-to-end reads this sitting (8)

1. https://mistral.ai/news/mistral-large-4 (10-06): "ML4 is a 1 trillion-parameter natively
   multimodal model with 52 billion active parameters."; "We will release the weights by
   the end of the month"; API $1.36/M in, $4.18/M out; Coding Agent Index 49.8% "ahead of
   DeepSeek V4 Pro 0813 and Qwen3.8 Max"; Surge AI blind human eval 3.74, 2nd of 5, behind
   Claude Opus 5 (4.22), ahead of Kimi K3 (3.59) and GLM-5.3 (3.60); "trained from scratch
   on 3,800 NVIDIA Grace Blackwell GPUs". No X post links on the page.
2. https://reflection.ai/blog/introducing-beam (10-05): "a sparse Mixture-of-Experts model
   with 501 billion total parameters, 23 billion active"; "This month, we will release the
   weights under an Apache 2.0 license"; "it achieves scores comparable to GLM-5.2 while
   using 3-4x less inference compute"; SWE Bench Pro v1 65.5 vs GLM 5.2 at 62.1; RL on
   10.5K GB300s, 100M+ rollouts. Update dated 10/8/26.
3. https://www.nobodywho.ai/posts/when-chat-templates-go-wrong/ (10-01): template-deviation
   degradation; llama_chat_apply_template "ignores the model's embedded template"; GGUF
   out-of-range special-token ids fall back silently; tool shipped:
   github.com/nobodywho-ooo/gguf-surgeon (tensor data stays byte-identical).
4. https://huggingface.co/sriram1983007/SRA-RiskGate-4B (uploaded 10-03, modified 10-11):
   Qwen3-4B-Instruct-2507 fine-tune, Apache 2.0, approve/hold/reject on x402, EIP-3009,
   ERC-20 payments; self-reported on its own 2,000-case bench (composite 0.913 vs 0.421
   base); "Prompt injection is the main remaining risk"; requires temperature=0.0 and the
   exact training prompt format.
5. https://shattered.io/mistral-large-4-parameter-count-gap-2026/ (10-06): "The model
   listing that Mistral published alongside the preview states 675 billion total
   parameters and 41 billion active parameters." Author Ryan Cole advises planning on
   official figures until weights ship; llm-stats.com/models/mistral-large-4 separately
   lists 1.05T/52B, proprietary license, $0.68/M in, $2.09/M out (conflicts with the
   primary page's $1.36/$4.18 on the same model).
6. https://vllm.ai/blog/2026-10-09-vera-rubin-preview (10-09): "It is a new GPU compile
   target (sm107), but kernels built for the Blackwell family target (sm100f) can also run
   on it."; day-0 DeepSeek, Kimi, GLM, MiniMax; 7.84x per-GB200 on AgentX at matched
   interactivity; nightly container vllm/vllm-openai:cu134-nightly.
7. https://data4sci.com/blog/local-llm-inference-at-scale-with (10-09, Bruno Goncalves):
   continuous batching, PagedAttention, prefix caching (69% measured hit on a 1,235-token
   prefix), FP8; hardware: DGX Spark GB10, 128 GB unified LPDDR5x at 273 GB/s; 34 tok/s
   single request to 284 tok/s at batch 256 on Qwen3.5-35B-A3B-FP8.
8. https://vllm.ai/blog/2026-10-07-deepseek-v41-flash (10-07): "achieving a 1.9x speedup at
   low concurrency and a 5.3x throughput improvement under a 150 TPS constraint"; SWA
   bounded replay on by default (30-40% prefill cut, accuracy gaps within ~1.5 standard
   errors on GSM8K/GPQA); MegaAttention NVFP4 KV "45% smaller" than FP8; measured on
   GB200/GB300; no speculative decoding.

## Research question answers

### Q1. Releases after 2026-10-09 vs the funded-tier roster

No big open-weight WEIGHTS drop landed after 2026-10-09 as of this sitting: ML4 weights
are committed "by the end of the month" (primary page) and Beam weights "later this month"
under Apache 2.0 (primary page). Both announcements (10-06, 10-05) predate the 10-09
state/arxiv sweep edge (lens/corpus.md:16), so the edge itself did not miss them; what it
misses going forward is the weights-drop events. Roster read: ML4's Coding Agent Index
49.8% places it ahead of the estate workhorse family's flagship (DeepSeek V4 Pro 0813) and
Qwen3.8 Max on that vendor index; Beam claims GLM-5.2-class scores at 3-4x less inference
compute. Both are roster candidates pending a funded-carrier listing; neither can be
measured until reachable, and the battery law gates that (Q2). The adhoc run's 7 confirmed
finds (watch/inbox/frontier_olm_adhoc/register.jsonl, rows for area
open-local-language-models: 10, 11, 12, 13, 14, 18, 23) name TWO roster-class releases:
Kolibri (10-03, Apache 2.0) and Kisoku 1.6B (10-08, Apache 2.0). And YES, the frozen
ledger cannot record them: memory/burns/LEDGER.jsonl reads 705 rows with zero "2026-10"
ts rows this sitting (wc -l = 705; grep -c '"ts": "2026-10-' = 0), max ts 2026-09-28, no
writer instrument (five-lens incident, lens/burns.md:73-76). Every roster candidate in
this sweep (ML4, Beam, Kolibri, Kisoku) is unrecordable there until a writer exists; the
register.jsonl + DIGEST + git commit remains the only mining record (anti-rebank rule in
lens/burns.md:73-76).

### Q2. Gates before any roster addition fires a paid call

From memory/rib/RIB_MODEL_GATES_20261001.md (read this sitting): the animal gets its OWN
harness, transport + rails + failure modes (lines 7-11); a model whose fingerprint changed
is a NEW animal, cold start, no inherited trust (lines 64-67); the executable leg is
mag/inference_budget.py: FAMILY_TABLE with per-animal thinking control, forbidden params,
max_tokens floors; plan_call before every fire and guard_terminal on every response; both
paid carriers already call them (lines 69-84). From the routing battery
(memory/rib/RIB_MODEL_GARDEN_ROUTING.md, read this sitting): the 8 columns are
code-writing, analysis, extraction, judgment, creative, adversarial-review,
schema-design, planning (column list atop the seeded grid); law 1 INSTRUMENTS ONLY, no
vendor benchmark fills a cell (lines 47-53); law 2 rows carry a moment and expire at 30
days or a family event (lines 54-62); law 4 funding gates WHICH families may fire, never
fills verdict cells (lines 66-68). Minimal cheapest legal first call for a new animal:
(1) reachability via a funded carrier confirmed first (funding column); (2) wire the
animal into FAMILY_TABLE with explicit thinking control and max_tokens floor, plan_call +
guard_terminal on; (3) fire the extraction cell in the F4 mini-task shape with
strict-JSON auto-validation (the $0.0001/answer class, the cheapest measured shape in the
grid) and the judgment cell with a second-family judge (never ember-1 sole,
RIB_MODEL_GATES lines 51-53; glm-never-judges-glm contamination rule); (4) record
condition + moment; row expires in 30 days. Vendor numbers (ML4's 49.8% index, Beam's
SWE-bench table, SRA-RiskGate's 0.913 composite) are ECON-class planning inputs only.

### Q3. Does the HN 'local llm' pool surface serving or gating tooling the estate lacks?

Live probe this sitting:
https://hn.algolia.com/api/v1/search_by_date?query=%22local%20llm%22&tags=story
&hitsPerPage=20&numericFilters=created_at_i>1790812800 returned 10 stories since 10-01.
What it surfaces that the estate lacks: (a) gguf-surgeon (nobodywho.ai post) - GGUF
metadata surgery with byte-identical tensors; the estate has no GGUF template/tokenizer
metadata repair instrument, and the chat-template failure class is exactly the local
janitor lane's harness gap; (b) SRA-RiskGate-4B - a local model AS a gate organ
(approve/hold/reject on payment rails), the model-gates concept in miniature, with
self-reported numbers the estate cannot cross-check because the corpus holds no
ML-benchmark or peer-reviewed safety-venue material (bounded claim,
lens/corpus.md:29); (c) data4sci's vLLM-at-scale tutorial - the estate catalog holds
lmcache-src (KV-cache serving) but no vLLM source and no continuous-batching education;
(d) simulkit's Apple-device local catalog and Shlexball (1.5B Mac file finder) - local
retrieval surfaces, weaker fits. The chat-template post and SRA card are the two strongest
steals; both carry caveats (self-reported evals; template claims measured on one engine
trio).

### Q4. GPU-ladder five gates after the 10-10/10-11 carrier waves

memory/rib/RIB_GPU_LADDER_20261001.md (read this sitting): gates are ARCH (SM90/SM100,
lines 12-14), VRAM 24GB min (15-16), PRICE triggers (17-19), SOFTWARE CUDA 12.8+ stack
(19-21), WORKLOAD real FP8/MoE QPS demand (21-23). This sitting's walk: the estate box is
unchanged (AMD RX 5600 XT, rib lines 5-7); the 10-10/10-11 drop cards bought nothing:
gstd_perimeter_design_20261010/CARD.md is vast.ai long-term RENTAL of entry-class
instances plus a used Dell CPU blade (lines 33-67, "entry GPU like 3090 or CPU-heavy
listings", "$0 capex"); the only Blackwell mention in the window is Doug Thomson's own rig
in watch/inbox/hut_bible_doug_20261011/HUT_BIBLE_v3.md:200 (third-party spec, not estate
hardware); no other 10-10+ drop card names a GPU purchase (my grep of the five
hardware-adjacent cards for 5090/H100/Blackwell/RX 9070/Arc B580 hit only the hut bible).
The Vera Rubin post shows the arch landscape moving (sm107, Blackwell-family compile
target) but is datacenter-class with no price input for the estate. WORKLOAD unchanged:
the GSTD perimeter runs 1-2GB small models per node container (CARD.md:50-51), not FP8/MoE
QPS demand. Verdict: all five gates still false; the perimeter design adds a rental path
that bypasses the ladder for serving-class work rather than moving any gate input.

## Overlap ledger (grep instruments this sitting)

- catalog/catalog.jsonl (1,136,889 rows): "Mistral Large 4" 0, "Le Chonk" 0,
  "introducing-beam" 0, "Reflection AI" 0, "swa-bounded-replay" 0, "MegaAttention" 0,
  "gguf-surgeon" 0, "NobodyWho" 0, "SRA-RiskGate" 0, "Hermes for Businesses" 0,
  "Vera Rubin" 0, "MiMo-V2" 3 rows (arxiv stub 2610.11959v1.txt 10-09 + AC3_MIMO.md x2).
- memory/rib + memory/frontier + memory/press + memory/lenses + memory/research_packs +
  memory/steal + memory/improve + attention.md + knowledge_graph.json + warm_state.json +
  runs/x_reply_radar: all candidate phrases zero EXCEPT "Mistral Large 4"/"Le Chonk" in
  memory/runs/x_reply_radar/out_2026-10-07.json (raw radar capture, no banked card) and
  "disaggregated serving" substring noise in memory/research_packs/bibverify/*.jsonl
  (bibliography corpus, unrelated).
- Sibling doors of this run (read this sitting): the reddit-door sibling already banks ML4
  open weights and Qwen 4 as PENDING releases (sweep/open-local-language-models-reddit.md
  lines 35, 59); the arxiv-door sibling cites SRA-RiskGate-4B and the data4sci HN story
  (sweep/open-local-language-models-arxiv.md lines 29, 119, 143, 190); the 10-10 run's
  swarm door banked the vLLM DeepSeek-V4.1-Flash post with the same quote
  (frontier_olm_2026-10-10/sweep/swarm-orchestration-x.md:28). My adds over siblings: the
  ML4 primary-page read (pricing, benchmarks, weights date, 52B-vs-49B-vs-41B conflict),
  the Beam primary read, the chat-template post body + gguf-surgeon, the HF card read, and
  the Vera Rubin + data4sci bodies.
- MiMo-V2.6-Pro NOT banked as a find: the estate holds the AC3 RL-dataset census
  (watch/inbox/last_mile_20260930/AC3_MIMO.md, 09-29, pyarrow over 5 parquet shards,
  7,780 rows) plus the arxiv stub; the felloai "best open-weight" roundup adds nothing
  measured.
- Not run this sitting: no pytest, no corpus FTS write, no fxtwitter post resolution of a
  NEW id (no legitimate Oct 2026 status id was obtainable; the @jack/status/20 probe and
  the nacho card reads stand as the recipe's verified working examples).

## OWED

- The x-history miner: the discovery half of the X door is the standing gap; the radar
  output (memory/runs/x_reply_radar/) is the seed corpus.
- Ledger writer for memory/burns/LEDGER.jsonl (sixth lens would read it frozen).
- Watch ML4 + Beam weights drops end of October; each is a routing-battery candidate ONLY
  after a funded carrier lists it (funding column of truth).
- Nous Series B / Hermes for Businesses (10-07, multi-outlet corroboration citing WSJ and
  TechCrunch) is snippet-grade only: no primary page was fetched, no clean article URL was
  captured from search, so it is context here, NOT a banked item.
