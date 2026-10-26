# Sweep: quantization-compression via Reddit - 2026-10-01

source-fetched: 2026-10-01. Seat: sweep-quantization-compression-reddit (workflow gopher).

## Doors, honestly

- `old.reddit.com/r/*/top.json` (all four subreddits: LocalLLaMA, MachineLearning, LocalLLM, ollama): returned an empty "Welcome to Reddit" shell, no JSON data.
- `www.reddit.com/*/top.json`: HTTP 403 Blocked.
- `old.reddit.com/r/LocalLLaMA/top/?t=month` HTML: empty welcome shell. Thread pages on old/www: welcome shell / JS shell. `curl -L` with a browser UA lands on `old.reddit.com/login/?reason=lor2`.
- `r.jina.ai` reader proxy: Reddit 403 "network policy" through the proxy. `redlib.catsarch.com` 429; `redlib.perennialte.ch` 403; `rl.bloat.cat` ECONNRESET.
- **Working door: PullPush API** (`api.pullpush.io/reddit/search/submission/?ids=...` and `/comment/?link_id=...`): full selftext + comments as JSON, actively ingesting (scrape stamps to 2026-09). Its `after=`/`sort_type=` search endpoint is agent-blocked ("Rate limit exceeded... free scraping resources for agents"), so candidates came from WebSearch `site:reddit.com` and were date-verified one-by-one through PullPush `ids=`.
- Wayback Machine (`archive.org/wayback/available`) worked intermittently (one "Temporarily Offline" burst, later 429s); it supplied no extra reddit threads beyond what PullPush already gave.
- WebSearch itself rate-limited (1302/429) repeatedly; about 1 in 2 query batches landed.

## Pass 1 - candidates (broad)

50+ candidate threads were surfaced by 8 WebSearch queries (Q4-vs-Q8 benchmarks, EXL2/EXL3, KV-cache quantization, IQ-vs-K quants, Unsloth dynamic quants, distillation, small-model quants, r/MachineLearning papers). 26 were date-verified via PullPush `ids=`. **Only 2 of the readable ones are inside the 30-day window (since 2026-09-01):** 1wdqit1 (09-11) and 1wa36d1 (09-07). The search door does not date-filter, so most hits were stale (2025-08 through 2026-06). Verified-date table (id | date | title):

- 1wdqit1 | 2026-09-11 | Running Qwen3.8-27B-Q4 at max context on a 32 GB GPU while avoiding kvcache quantization
- 1wa36d1 | 2026-09-07 | ExLlamaV3 is underrated
- 1vwh3u7 | 2026-08-23 | We quantized Qwen 3.8 27B and compared the quants on an RTX 6000 (Atomic Dynamic GGUF)
- 1vqyq8r | 2026-08-17 | Artificial Analysis' Qwen3.8-27B benchmarks (score 898, link post, no selftext)
- 1vcwl43 | 2026-08-01 | Is there a point where models just cannot get any smaller without losing intelligence? (score 101, 107 comments)
- 1ugo5nw | 2026-06-27 | How to distill my own models?
- 1tyfnqi | 2026-06-06 | Has there been any recent new development on which quant is considered optimal?
- 1twnj5r | 2026-06-04 | KVarN: Variance-Normalized KV-Cache Quantization [R] (r/MachineLearning)
- 1u3wegv | 2026-06-12 | Two-shot with Hermes, Qwen3.6_35b on RTX3060/12gb
- 1tyxu55 | 2026-06-07 | Gemma 4 31B QAT Q4 vs standard Q4 - Top1 KLD
- 1sdqn13 | 2026-04-06 | Qwen3.5-4B GGUF quants comparison (KLD vs speed) - Lunar Lake (score 133)
- 1sxzqry | 2026-04-28 | Qwen 3.6 27B BF16 vs Q4_K_M vs Q8_0 GGUF evaluation (score 695)
- 1t53dhp | 2026-05-06 | Quality comparison between Qwen 3.6 27B quantizations (score 515)
- 1suur3s | 2026-04-24 | Qwen3.6 27B's surprising KV cache quantization test results
- 1tfqfvt | 2026-05-17 | Developers who use local AI - Q4_0 vs Q8_0 KV quant?
- 1tgk9y6 | 2026-05-18 | Quantizing MTP KV Cache = free lunch?
- 1s720r8 | 2026-03-29 | kv rotation PR: existing q8 kv quants tank performance on AIME25
- 1s6a488 | 2026-03-28 | Do not use mixed KV cache quantization
- 1s3dqeg | 2026-03-25 | What aspects of local LLMs are not scaling/compressing well
- 1reqdpb | 2026-02-25 | Overwhelmed by so many quantization variants (score 112)
- 1s8yni2 | 2026-03-31 | [D] TurboQuant author replies on OpenReview (r/MachineLearning, score 133)
- 1serby2 | 2026-04-07 | TriAttention: Efficient KV Cache Compression [R]
- 1pyrjke | 2025-12-29 | Benchmarks for Quantized Models?
- 1o5mr9j | 2025-10-13 | Do you guys personally notice a difference between Q4 - Q8?
- 1mhlj69 | 2025-08-04 | What's the verdict on using quantized KV cache?
- 1mgl1qz | 2025-08-03 | Is EXL3 doomed?

Unverified leads (titles only from search snippets; PullPush had not ingested them and Wayback has no snapshot, so I could NOT read them and did NOT bank): 1w4mevo "Kaitchup posted Qwen3.8 27B Benchmarks for quants from Q4 to Q1", 1wa5dp9 "My Qwen3.8-27B task-aware quant reaches 99% of BF16 (TAK quant: 82.81% vs 83.59% BF16)", 1wju8ky "Prism-ML Bonsai 2 Joins Our Qwen3.8 Quantization Comparison (~91.5% composite)", 1w1e1uq, 1vz3ieu "Benchmarking Qwen3.8 27B quantizations: 4-bit holds up, 1-bit collapses", 1vxc1gh "$100 benchmarking different Qwen3.8-27B quants and KV cache". These are OWED follow-ups for the next sweep window once PullPush ingests them.

## Pass 2 - deep reads (6 threads end to end: full selftext + top comments)

### 1. 1wdqit1 - dynamic KV/config ladder instead of static KV quant (IN WINDOW, 2026-09-11)
wadeAlexC built `llama-manager` (github.com/wadealexc/llama-manager) around a llama.cpp fork with runtime context reconfiguration, KV cache preserved across reconfigs. Quality-first degradation ladder on 32 GB GPU with Qwen3.8-27B-UD-Q4_K_XL: baseline f16-KV 167,680 tokens -> `disable-spec` (+33,280) -> `mmproj-to-cpu` (+17,920) -> `quantize-kv-q8` (+43,264 -> 262,144). His own verdict: KV quantization is the LAST resort. Top comments: nasone32 + feng_sg + Tormeister point to beellama's KVarN8 quant and the "precision tail" (anbeeld.com article: keep the newest 128-2048 tokens full precision) as higher-quality KV compression than plain q8_0; Fancy-Snow7 reports (own Qwen3.8 benchmarks) "virtually any difference until I drop below q3_0" KV, and that raising model quant while dropping KV quant beats the reverse at low model quants; Itsluc: no FP16-vs-Q8_0 KV difference in heavy coding tasks, but UD-Q4_K_XL vs UD-Q5_K_XL model quants clearly differ - prefers Q5 model + Q8_0 KV over Q4 model + FP16 KV. **Estate fit: direct design pattern for janitor seats - a ladder (spec off -> mmproj to CPU -> KV q8 -> KV q4) instead of a fixed KV quant, exactly the "size the local baseline precisely" deliberate-ask target.**

### 2. 1sdqn13 - Qwen3.5-4B GGUF quant KLD-vs-speed table (2026-04-06, janitor-class)
Tryshea tested ~36 quants of a 4B model on Intel Lunar Lake iGPU (258V/140V, 18 GB, Vulkan; Intel SYCL slower). Best KLD/GB: Bartowski Q5_K_S (KLD 0.00778, 2.91 GB, 22.7 tok/s); Q4_K_M class sits at KLD 0.0216-0.0250 (Bartowski/Unsloth) at ~25 tok/s; plain Q4_0 nearly 2x worse KLD (0.0498-0.059). Comments add the honesty law in the wild: the author's reruns showed KLD "jumping up-and-down full grid lines" run to run; imatrix-vs-static unresolved; a commenter asks for agent/reasoning benchmarks because "I wonder if KLD would correlate". **Estate fit: the closest thing to a measured answer for 2B-8B janitors: at 4B, Q4_K_M still costs measurable KLD; Q5_K_S is the quality-per-byte sweet spot when you can afford ~0.3 GB more. KLD is noisy - treat any single-run verdict as suspect (lens/laws.md conditions rule).**

### 3. anbeeld.com - KV cache precision tail, measured (reached from 1wdqit1 comments)
BeeLlama v0.4.0 (llama.cpp fork) implements an exact recent tail on a quantized KV cache. Conditions: RTX 3090, CUDA 13.1, Qwen 3.6 27B @64k ctx and Gemma 4 31B @16k ctx, Q5_K_S weights, teacher-forced Wikitext-2, KLD vs BF16-cache baseline. q2_0 median KLD 0.0194 -> 0.0037 with a 2048-token tail; q4_0 0.00185 -> 0.00102; q8_0 essentially unchanged (0.00091 -> 0.00090). q4_0 + 1024 tail (0.00106 KLD, 1248 MiB) beats q5_0 no-tail (0.00115, 1408 MiB) on BOTH quality and memory. Caveat stated: tail-128 gains partly reflect Wikitext recency bias. **Estate fit: the "window/sink trick" of research question 3, with numbers - a cheap, local-first KV quality recoverer; the Gemma sliding-window note (tail 1024 makes the whole visible window exact) is directly relevant since estate janitors are Gemma-family.**

### 4. 1wa36d1 - ExLlamaV3 underrated (IN WINDOW, 2026-09-07)
Post is anecdote ("these are not benchmarks"): claims EXL3 beats llama.cpp on quality-per-size, KLD, and speed; CPU MoE offload recently landed. Comments carry the measurable bits: SBoots (5090+4090, Qwen3.8-27B 8-bit, 256k ctx): ~65 -> ~80 tok/s switching llama-server -> TabbyAPI/exl3; kansasmanjar0: Qwen3.8-27B-exl3-SC-6bpw several GB smaller than Unsloth q6_KL, "~10% faster tg, 10% less vram, 20% more context", while admitting he "can't tell" a quality difference; vacon04: hybrid inference needs exl3 quants with the mul1 codebook (old mcg-codebook quants misbehave). **Estate fit: EXL3 is a real llama.cpp alternative for the specialist leg on NVIDIA-only seats, but the quality claims are folklore - no bench in thread; treat as lead, not verdict.**

### 5. 1twnj5r - KVarN: variance-normalized KV quantization (r/MachineLearning, 2026-06-04)
Author post: Hadamard rotation + variance normalization on both K and V axes, round-to-nearest; 3-4x KV compression at mostly 0-1% accuracy drop on AIME24, faster than fp16 baseline in vLLM. Paper arXiv:2606.03458; code github.com/huawei-csl/KVarN. Error analysis: spend the MSE budget on few big errors (bad token-scales). Not llama.cpp-native today (vLLM impl), but the same rotation idea shows up in llama.cpp's kv-rotation PR line (1s720r8, 2026-03-29: existing q8 KV quants "tank performance on AIME25" until rotation). **Estate fit: the technique behind the next-gen KV quant; watch for it landing in llama.cpp/Ollama before adopting KV q8 for reasoning workloads.**

### 6. 1vwh3u7 - Atomic Dynamic quants, Qwen 3.8 27B (2026-08-23)
Team-posted table, conditions stated (voxel-island creation task, RTX PRO 6000, top-1 vs BF16 + mean KLD + decode): AD-Q4_K_M 17.1 GB / 95.6% / 0.0113 / 67 tok/s; AD-Q5_K_M 20.2 GB / 97.3% / 0.0042; AD-Q6_K 25.0 GB / 98.7% / 0.0011; Q8_0 28.9 GB / 98.9% / 0.0006 / 50 tok/s. Sometimes preferred Q4 output; safest pick AD-Q6_K. **Estate fit: Q4->Q8 delta measured WITH task+hardware conditions: ~3.3 points top-1 and ~11x KLD between Q4_K_M and Q8_0, Q4 faster on the same card - matches the Itsluc coding-task observation from item 1 (quality gap concentrated in hard tasks).**

### 7. 1vcwl43 - how small can models get (2026-08-01, score 101)
Discussion of shrinking ceilings with DeepSeek V4 Flash as the hook. The load-bearing comment (score 102) anchors Allen-Zhu & Li, "Physics of Language Models 3.3: Knowledge Capacity Scaling Laws" - ~2 bits of knowledge per parameter (commenter NandaVegg argues 3-4 bits/param on real pretraining mixes, up to ~5 on code-heavy). segmond: Q1-quantized 1T/3T models stay usable; a 30B at Q1 is garbage - the compression floor scales with model size. **Estate fit: hard physics for the janitor question: a 2-4B janitor carries roughly 1-2 GB-equivalent of knowledge at FP - it can hold procedure, not world knowledge; do not ask scut seats to know things, only to do things.**

### 8. 1ugo5nw - DIY distillation for a niche agentic skill (2026-06-27)
Theorem-proving distill thread. Commenters: logit distillation is "easy, you can base your work on others' scripts"; DeepSeek precedent of a 7B Lean fine-tune; dataset scale "at least a few GBs of training data"; StudentZuo's framing: log failure types first (wrong tactic / bad formalization / missing lemma search / proof-state misunderstanding) and make them the eval buckets, else the small model learns to sound confident while failing the same step. **Estate fit: this is the reproducible-without-datacenter recipe shape: trace-derived dataset from the frontier leg, failure-type eval buckets, LoRA/fine-tune a 4-8B. Maps 1:1 onto the estate's seat tapes as training corpus (code-agent-data skill). Frontier-lab-official distillation recipes did NOT surface as readable reddit threads this window - coverage gap noted, not faked.**

## Answers sketch (per research question)

1. **Formats, quality-per-byte (2B-8B, llama.cpp/Ollama):** no leaderboard exists; the closest measured evidence is 1sdqn13 (Q5_K_S best KLD/GB at 4B; Q4_K_M 2-3x the KLD of Q5_K_S but ~+2 tok/s on iGPU) plus the Kaitchup/Unsloth benchmark threads as unverified leads. AWQ/GPTQ barely appear in current small-model local talk - GGUF K/I-quants dominate; EXL3 is the enthusiast alternative (item 4).
2. **Q4 vs Q8 measured delta:** three independent conditions-rich data points (1vwh3u7: 95.6% vs 98.9% top-1, 0.0113 vs 0.0006 KLD on 27B voxel task; Itsluc in 1wdqit1 comments: coding tasks, Q4-vs-Q5 model quant visible, KV FP16-vs-Q8_0 invisible; 1sdqn13: KLD table at 4B). No thread met the bar of a task-benchmarked Q4-vs-Q8 on a 2-8B model with hardware stated - that exact experiment is still OWED, and the KLD-noise commentary (item 2) warns against single-run verdicts.
3. **KV/context compression:** strongest area. Precision tail (item 3, measured), KVarN (item 5, 3-4x at 0-1%), dynamic degradation ladder (item 1, in-window), plus warnings: mixed K/V quant caution (1s6a488), pre-rotation q8 KV tanking AIME25 (1s720r8), KV quant forcing excess processing onto CPU (1ng0fmv, 2025-09-13).
4. **Frontier distill recipes:** reddit door gave practitioner recipes (item 8) and the capacity-law physics (item 7), but no frontier-lab recipe thread readable this window - OWED to a later sweep (the unverified TurboQuant/TAK/Kaitchup leads are quant-side, not distill-side).

## Overlap check (run 2026-10-01)

`catalog/catalog.jsonl` (193 MB): grep for all 8 titles/IDs/slugs = 0 hits; `kvarn|anbeeld|beellama` = 0; `exl3|exllamav3` = 0; `KLD` = 0. Generic terms exist (quantiz 206, distill 155, kv-cache 175 lines) but no item-level overlap. `memory/`: nearest neighbors are our own llama3.2-3B-Q4_K_M Ollama bench (`memory/improve/sources/ponytail-2026-08-03/benchmarks/results/2026-06-15-llama3.2-local.md` - complements item 2, does not duplicate) and `memory/runs/corpus_gap_research/ARXIV_REGISTER.json` (KV papers ActKV/AgentKV/CacheGen/D-Quant/KV-COBRA/DeepSeek-V4.1-Flash registered; KVarN arXiv 2606.03458 is NOT in it - candidate to add).

## Raw materials

PullPush JSON for every read item sits in `$TEMP/sweep_qc/` (sub_*.json, cmt_*.json) on this machine - ephemeral cache; the quotes above were taken from those files at read time.
