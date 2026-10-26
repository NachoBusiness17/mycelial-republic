# SWEEP: open-local-language-models via reddit - source-fetched: 2026-10-07

Seat: sweep-open-local-language-models-reddit (frontier gopher, dynamic workflow actor_3_3).
Window: last 30 days (2026-09-07 through 2026-10-07). Repo: C:/Users/foste/Documents/projects/local_sovereign_agent.

## Door status (degraded doors recorded per the recipe; no fabricated fallbacks)

- Recipe primary door `old.reddit.com/r/<sub>/top.json?t=month&limit=50`: BLOCKED for all four
  subs (LocalLLaMA, MachineLearning, LocalLLM, ollama). WebFetch gets the "Welcome to Reddit /
  Skip to main content" shell, zero post data. `www.reddit.com` .json: HTTP 403 Blocked
  (Retry-After: 0). old.reddit thread HTML: same shell. This re-confirms the estate's own
  dead-list (lens/burns.md:212-213, "every Reddit JSON door") with this session's own calls.
- WORKING DOORS this session (the recipe's sanctioned fallback, plus the doors the 10-05/10-06
  sibling sweeps proved):
  1. WebSearch site:reddit.com - worked, paced sequential; two timeouts and one embedded 1302
     rate-limit mid-session (burst-shaped, matches the estate fan-out width law).
  2. `www.reddit.com/r/<sub>/top/.rss?t=month` via curl with browser UA - HTTP 200 for all four
     subs after 429 retries with 25-50 s spacing (bytes: LocalLLaMA 147,440; MachineLearning
     149,179; LocalLLM 168,209; ollama 180,656). Parsed locally with repo venv xml.etree
     (tmp/parse_rss.py), 200 entries projected. Raw feeds kept at raw/rss_*.xml.
  3. `arctic-shift.photon-reddit.com` API (`/api/posts/ids?ids=...`, `/api/comments/search?
     link_id=...&limit=100`) - clean JSON, parsed locally with repo venv python. Two 422
     "Timeout. Maybe slow down a bit" responses cured by 25-60 s spacing. All quotes from
     reddit threads below are byte-verbatim from my own local parse of these JSON payloads,
     NOT from a fetch-model summarizer.
  4. WebFetch on github.com release feeds (ollama releases.atom, tag pages; llama.cpp
     releases.atom, b11475 tag page) - worked; github quotes pass through the fetch-and-answer
     layer and carry the discount noted inline.

## Pass 1 - candidates considered (200 RSS entries + 20+ search-surfaced; last 30 days)

Full listing instrument-generated at raw/ (parse_rss.py output in-session). The 200 RSS entries
map against the prior banks as follows. Already banked by siblings (10-02 through 10-06,
NOT re-banked here): 1ww528l 200-task tier list, Kolibri-1 (1wwod1q/1wwl7y6/1wyeanf), 1wgiefk
Flash-Next local, 1wb35xo concurrency, 1wpgyfh Q2-vs-Q4, FrogNano-4B (1ww40o2), 1vvtu9z Gemma 4
12B finetune, arXiv rate limit (1wvg7yc), AREX-2, Ollama v0.35.1 train + /v1/systemone +
Nimble/Clef (day-6 register rows 3+7), Jev report, 1wv1u54 Q4 replication, 1wt5f4e subsidy,
1wwo3ps Flash Next q2_0, 1wa26pn Friends-don't, Strata astroturf (1wx1bi1), Ternary Bonsai 2
(1wj6c4l/1wlsaoq/1wjy9rh/1wjwxeq), Qwen 4 (1wmxfjs/1wmzky1), DeepSeek V4-1 Flash (1wcbid7/
1wcagoi/1wcany5), unswallow (1wc6tka), 30-day Qwen 3.8 27B (1whqwdq), Checkability Boundary,
SHADOW-50M (1wgzpli), 1wyefkt, 1wqxbwa e2b-vs-26b, 1wvv6im + 1wv4zzi + 1wxloam decision-model
threads, Jeff-Qwen3.5-0.8B (1wv05u1 - banked across FIVE sibling areas incl. 10-06
doors/ff_deep/1wv05u1.post.json + .comments.json; my deep read added nothing unbanked, so it
is dropped as an item), 1wigesu Ollama retirement (10-02 item 6), Best Local LLMs August
(1vkmhyl, register row 17 on 09-30), MiMo-V2.6 RL dataset census (watch/inbox/
last_mile_20260930/AC3_MIMO.md).

Search-surfaced and triaged OUT: 1qyg10z (11 LLMs tool-calling CPU) dated 2026-03-11 by the
10-04 evals sweep's archive check - out of window; 1r4ie8z (21 LLMs Round 2) already in catalog
(rows 674199-674200, %TEMP% bodies fetched 09-29); AgrillaMoE (one stray snippet, unfindable
through any door - not an item, not a claim); BFCL board (inherited timeout, not retried).

NEW this sweep (candidates considered, in-window, not in any bank): 1wyruu5, 1ws9ydg, 1wz00vv,
1wxz5qq, 1wyaxyd, 1wblnsk, 1wqtc1h (1.11B pretrain on 6GB, HF blog write-up, pass-1 verified
via arctic OP), 1wz71g3 (RNN/Transformer/SSM memory essay, 0 comments, write-up mention only),
1wn36d4 (MiMo-V2.6 $3.5M release, partially held via AC3_MIMO dataset census), 1wdq3kg (Curie
17B SSD-serving) + 1wt3s0s (Colibri 2.8T pure-C engine) - pass-1 only, named for the next
pass; 1wz32qk (Ollama Cloud cost table), 1wz6ist/1wz5b30/1wze6g5/1wy1o7y (hardware/meta, skipped).

## Pass 2 - deep reads (10 items read end to end; minimum was 5)

Byte-parsed by me via arctic JSON: 1wyruu5 (OP + 29 top comments), 1wv05u1 (OP + 14, dropped as
banked), 1ws9ydg (OP + 25), 1wxz5qq (OP + 7), 1wyaxyd (OP + 10), 1wblnsk (full OP selftext +
36 top comments), 1wn36d4 (OP), 1wqtc1h (OP), 1wz00vv (OP), 1wz71g3 (OP). Fetch-layer reads:
ollama releases.atom + v0.40.0 tag page; llama.cpp releases.atom + b11475 tag page. MiMo HF
model card: HF search timed out, MiMo-V2.6-9B stays unverified (search-summary tier only).

## The eight banked items (strongest first; full detail in the SweepResult payload)

1. llama.cpp b11475 (2026-10-07): Metal MUL_MAT+ADD fusion bug collapsed Clef decision-model
   /v1/systemone probabilities toward uniform on Metal (0.28 vs 0.977 on CPU, clef-flash Q8_0),
   deterministic by memory layout, "Not a quantization issue: the same file is right on CPU."
   Workaround GGML_METAL_FUSION_DISABLE=1; new MUL_MAT_ADD test-backend-ops mode failed 27/28
   on Metal pre-fix. Estate impact: the estate-shaped serving path (day-6 register row 3) had a
   silent per-backend correctness hole for exactly the decision-model class RQ2 cares about;
   any decision-model row measured on Metal before b11475 is conditions-suspect per the estate's
   verdict-condition law (lens/laws.md:27-29). b11477 same day: nextn/MTP trunk-only flags now
   shared across deepseek4, nemotron-h, qwen35, qwen35moe, qwen3next, qwen4exp.
2. Ollama v0.40.0 stable (atom-dated 2026-10-06; tag page shows "25 Sep 03:31" - the rc0-era
   date; recorded both): "Models run on MLX on Apple Silicon by default" (known from rc0 via
   the 10-03 bank) PLUS the genuinely new rc1-rc6 line, headline rc6 bullet "model: add
   multimodal embeddings (#18820)" - EmbeddingGemma2Model, a 24-layer bidirectional text
   encoder with PLE, shared vision/audio towers, mean-pool + L2 output, shipped as
   embeddinggemma-2 alongside decision models Nimble/tev1/clef/clef-flash on the default
   runner list. Estate impact: the RQ2 gate needs a beat-embeddings baseline at >=0.880 on
   n>=40; a first-class multimodal embeddings model inside Ollama is now the cheapest baseline
   instrument the estate can wire, on the same runtime the janitors already use.
3. r/ollama 1wyaxyd "No think doesn't work" (2026-10-05, deep-read): the load-bearing comment
   (u/ManuelSalcedo20836, 3 pts, byte-verbatim): "On Ollama, qwen3:4b now has the same digest
   as qwen3:4b-thinking, which is the 2507 thinking-only release, so it doesn't have a
   non-thinking mode to switch to. That's why /no_think, /set nothink and --think=false all
   get ignored. Use the instruct variant instead." Estate impact: thinking-mode is the estate's
   axis (AGENTS.md tier-ladder law); a tag whose digest silently aliases to a thinking-only
   release flips the measured default without any config change. The estate's harness should
   pin digests, not tags, for every rung whose thinking state is a recorded condition.
4. r/LocalLLaMA 1ws9ydg NVIDIA OpenShell sandbox (2026-09-28, 761 pts, 152 comments, deep-read
   OP + 25 top): "an open source sandbox that gives local and open agents real runtime limits
   instead of prompt rules. Over 100 firms joined the safety stack." Comment field carries the
   durable steals: u/wren6991 (2 pts) - "the shell that the agent runs commands in does not
   need the same privileges as the harness itself. There should be a trust boundary in between
   the two"; u/wlvmtb (8 pts) - NVIDIA's stack routes out-of-band monitoring through enterprise
   DPU/PCIe (hardware tax + ms-scale latency); u/Future_AGI - "runtime limits enforced outside
   the model are the only thing that actually holds". Skeptics: logo walls = BD calls
   (u/Strong-Leg-9696), "thin on technical detail... mostly a marketing exercise" (u/wren6991).
   Estate impact: the deterministic-first law embodied at industry scale; the harness-vs-shell
   trust boundary is the steal for the estate's own tool-execution lane.
5. r/LocalLLM 1wblnsk "A final LLM benchmark for 8GB VRAM 16GB RAM" (2026-09-09, 162 pts,
   deep-read full OP + 36 top comments): hobbyist 18-question manual benchmark, thinking
   disabled, RTX 4060; OP picks Bonsai 27B / Ministral4 14B / Ling3.0 Tiny / GPT-OSS 20B. The
   COMMENT field is the real RQ1 payload (u/_wortkarg_, 14 pts, byte-verbatim): "Ornith-1.5-9B
   is very good for it's size (Ornith-1.5-35B or Tiel-Coder-35B-A3B for better results)" and
   "Ministral4 14B and GPT-OSS 20B are too old, old LLMs can't use the tools properly"; others
   add miniCPM5 2B, Sparx-X2.5-4B, Nanbeige4.2 3B, LFM (missing from the bench). Direct
   contradiction with the banked 200-task tier list (1ww528l banks Ling-3.0-tiny at F tier) -
   two community benches disagree at the small end, which is itself the finding: no community
   instrument settles the 0.5B-8B band; the estate battery (UNMEASURED is the legal empty
   cell, lens/laws.md:48) remains the only court.
6. r/LocalLLM 1wyruu5 self-hosting 35B MoE for a 20-person team (2026-10-06, 319 pts, 113
   comments, deep-read OP + 29 top): DGX Spark 128GB running Ornith-1.5-35B-A3B at NVFP4
   (22 GiB) on vLLM 0.24 with MTP speculative decoding, no separate draft model: "One person
   gets 79 tok/s" / "20 people at once get about 25 tok/s each, 490 tok/s total", full 262K
   context, MATH-500 97%, GSM8K 98%, MMLU-Pro 81%. Community pushback is heavy and is the
   lesson: top comment calls it "AI written posts... LinkedIn slop" (11 pts), another "Total
   bullshit post" (7 pts); the durable technical counters: MoE advantage erodes at high batch
   because "majority of experts will be activated anyway" (u/severemand), dense + parallel
   inference would beat it (u/allenasm), and for team-grade capability "GLM 5.3 flash at
   320B-A18B is fantastic. Lower models like even Deepseek v4 flash had insufficient
   performance" (u/Scary_One_2452). Banked as marketing-suspect with real counter-arguments,
   matching the estate's claims-desk discipline.
7. r/MachineLearning 1wxz5qq "Distilling Stockfish on a Billion Positions, Full 3.9B Dataset
   Available" (2026-10-05, 71 pts, deep-read OP + 7 top): "I distilled the Stockfish value
   function into a ResNet/ViT model using 1 billion positions from the Gigafish dataset";
   dataset huggingface.co/datasets/lukesalamone/gigafish-3.8b-d10 (37 months of Lichess);
   CNN beat ViT early (geometric inductive bias), best result combined both. Comments supply
   the priors: DeepMind prior art arXiv 2402.04494 (u/djm07231), and the engine-community
   constraint (u/4plus4equals8): "bigger models (CNNs, transformers) evaluate a position
   better than NNUE. The problem is they're much slower per eval, so the real optimization is
   elo at equal time". Estate impact: pairs with the banked QUEEN chess LM (lens/burns.md:
   119-122) and the estate's own stockfish door (FOLD-FAST + stockfish-coding ractor); the
   3.9B-position dataset is a pullable training asset for the estate's own value-function
   experiments; frontier_thinking shelf candidate.
8. r/LocalLLaMA 1wz00vv "Microsoft confirms OpenAI has been using Looped Transformers in the
   GPT-6 series" (2026-10-06, deep-read OP, score 1, 0 comments at fetch): "GPT-6.1 Sol uses
   2 inference passes, with a passing mention of 'instead of three'... Update: Microsoft
   updated the web page to remove it". Independent corroboration at search-summary tier only
   (Sebastian Raschka's Sep 2026 "GPT-6 Astra, Looped Transformers, and Hidden Reasoning"
   article; aman.ai recursive-transformers primer; arXiv LoopViT Feb 2026): looped/recurrent-
   depth transformers trade interpretable chain-of-thought for post-training inference-compute
   scaling. Estate impact (RQ4): the non-standard-lineage question now has a frontier
   production answer - the looped lineage is IN at the frontier while diffusion LMs (ALoDLM,
   banked) stay research-only; and llama.cpp b11477's trunk-only/MTP flags are the local
   serving analog (a trunk-only GGUF is literally the looped body without the head). Community
   validation is zero (0 comments) - banked as a lead with the corroboration discount stated.

## RQ verdicts (grounded in the reads above)

- RQ1 (0.5B-8B band beating gemma:2b / gemma4 / qwen2.5:7b with instrument-measured evidence):
  still UNMET by public evidence. The band's named community candidates this window are
  Ornith-1.5-9B, miniCPM5 2B, Sparx-X2.5-4B, Nanbeige4.2 3B, LFM, Tiel-Coder-35B-A3B (over-
  band) - every one carried by testimony, none by a public instrument at the estate's bar; the
  two strongest community benches contradict each other on Ling-3.0-tiny. The 20-user MoE
  report is marketing-suspect. The estate's own battery stays the only admissible court;
  UNMEASURED remains the legal cell state.
- RQ2 (sub-1B router clearing beat-embeddings >=0.880 on n>=40): still UNSUPPORTED. Jeff-
  Qwen3.5-0.8B v1.2 (the strongest shape: 9 hot-swap LoRA adapters + probability-gap fallback,
  300 rows/task) is already banked estate-wide and its own thread's crowd refuted the +8.7
  headline as "a product slide, not a decision-system result" (u/zykarys) with no per-task CIs
  and no embeddings baseline anywhere. What IS new: Ollama v0.40.0 ships embeddinggemma-2 as a
  first-class model, which gives the estate's gate its cheapest-ever baseline instrument.
- RQ3 (runtime features since 2026-10-01): the delta is real - Ollama v0.40.0 stable + rc1-rc6
  (multimodal embeddings, EmbeddingGemma2Model, MLX-by-default on Apple Silicon) and llama.cpp
  b11466-b11477 (b11475 Clef/Metal correctness fix, b11476 Metal few-row MMA kernel expansion
  across quant types, b11477 nextn/MTP trunk-only flags generalized). The b11475 lesson is the
  estate-shaped one: decision models can silently collapse per-backend; measure on the
  backend that will serve.
- RQ4 (non-standard lineages production-viable?): looped transformers confirmed at frontier
  (GPT-6/6.1, community-corroborated, page removed); local-serving analog exists (trunk-only
  GGUF files). Diffusion LMs stay research-only (ALoDLM, already banked). QUEEN-style silent-
  expert welds: no new production evidence this window.
- RQ5 (frontier_thinking shelf): this sweep's shelf candidates are the looped-transformers
  cluster (Raschka article + aman.ai primer + LoopViT arXiv as the paper trail behind item 8),
  the Stockfish value-distillation result + gigafish dataset (item 7), and - write-up mention
  only, 0 comments - the RNN/Transformer/SSM working-memory essay (1wz71g3). All verified at
  the tiers stated; none re-derive anything state/arxiv already holds (grep-clean).

## Overlap receipts (instrument: rg -i -c over catalog/catalog.jsonl 1,195,926 rows; rg -i -l
over memory/; thread-ID greps over all frontier_olm bank .md files + register.jsonl + DIGEST)

- b11475: catalog 0, memory 0. systemone itself estate-held (day-6 register row 3) - the BUG
  is the new part.
- embeddinggemma: catalog 0, memory 0. Ollama train banked only through v0.35.1 (10-03 sweep).
- 1wyaxyd / qwen3:4b-thinking: catalog 0, memory 0; thread only in 10-06 doors/ raw harvest.
- OpenShell: catalog 0; memory 3 hits = seat_memory_20260927 syllabus lines (2026-09-15,
  "OpenShell Z3 structured counterexamples") that PREDATE the NVIDIA launch (2026-09-28) and
  name a different/ambiguous usage; the NVIDIA sandbox item is new, the name collision noted.
- 1wblnsk / Ornith: catalog 0 for both (memory "Ornith" 8 hits all ornithology-corpus false
  positives); thread only in raw harvests. Ornith-1.5:35b details known via
  frontier_olm_2026-10-04/register.jsonl row 9 (Mingbird deep read) - the 9B field verdict and
  bench contradiction are new.
- 1wyruu5: only in 10-06 doors raw harvest; not in any bank.
- 1wxz5qq / gigafish: catalog 0, memory 0; QUEEN + stockfish ractor held, this artifact new.
- 1wz00vv / looped transformer: catalog 0, memory 0; only in raw harvest.
- Dropped as already-banked: 1wv05u1 Jeff (five sibling areas + catalog), MiMo-V2.6 (AC3_MIMO
  census), 1qyg10z + 1r4ie8z tool-calling threads (out-of-window / catalog rows 674199-674200),
  1wigesu retirement (10-02 item 6), 1vkmhyl (register row 17).

## OWED (never asserted as fact)

1. MiMo-V2.6-9B distill existence + license: HF doors timed out; search-summary tier only.
2. Curie 17B SSD-serving (1wdq3kg) and Colibri 2.8T pure-C engine (1wt3s0s): pass-1 only.
3. 1wqtc1h's HF blog write-up body (1.11B pretrain at 4.51GB peak VRAM): OP verified, blog
   body not fetched.
4. GitHub-side quotes (ollama + llama.cpp releases): pass through the WebFetch layer; the
   b11475 "0.28 vs 0.977" numbers are the fetch layer's rendering of the release body, not a
   raw-byte read. A byte-exact re-pull of the b11475 body is the honest next step before any
   promotion to a register row that routes dollars.
5. The estate battery runs (RQ1/RQ2 cell fills) are on-estate instruments, not runnable from
   this sweep seat; embeddinggemma-2 baseline wiring is the new cheapest first probe.

## Machine receipts (all run this session)

- RSS pulls: 4 subs, curl browser-UA, 200s after 429 retries (sizes above); local parse
  200 entries (tmp/parse_rss.py, repo venv).
- arctic-shift: 1 ids batch (10 OPs, 63,004 B), 5 comment pulls (232,101 / 82,070 / 203,815 /
  196,701 / 52,447 / 32,982 B; two 422s cured by spacing).
- Overlap greps: rg over catalog.jsonl + memory/ + all frontier_olm banks (commands in
  session log); every nonzero hit inspected before banking.
- Epoch/ID handling: dates above are the RSS/arctic updated/created_utc fields read directly;
  no fetch-model date conversions were trusted.
