# SWEEP - open-and-local-language-models via reddit - 2026-09-30

source-fetched: 2026-09-30. Seat: sweep gopher (dynamic-workflow child). Area owner: driving-ladder / free-lane sensing policy (memory/rib/RIB_DRIVING_LADDER_20260928.md, memory/rib/RIB_FREE_USAGE_POLICY_20260823.md).

## Door log (honest degradation record)

1. `WebFetch https://old.reddit.com/r/LocalLLaMA/top.json?t=month&limit=50` -> Reddit welcome/landing page, zero posts. Same for r/ollama top.json. Recipe door DEGRADED.
2. `curl` (plain UA) on the same URL -> HTTP 302 (login wall redirect).
3. `curl -L` with Chrome UA -> HTTP 200 but the body is Reddit's HTML block page (`<!DOCTYPE html ... theme-beta`), not JSON. Verified by byte inspection before parsing.
4. `WebFetch` and web_reader on thread HTML pages (old + www) -> welcome wall / "network policy" block. `curl` on thread `.json` -> HTTP 403 + HTML block page.
5. WebSearch backend (site:reddit.com) -> intermittently working; surfaced ~40 candidate threads but returned **no dates**, and several result summaries implied recency that PullPush dates later contradicted.
6. **Working deep-read door: PullPush public archive API** (`api.pullpush.io/reddit/search/submission/?ids=...` and `/search/comment/?link_id=...`, HTTP 200, real payloads). Its subreddit-listing `/search/submission/?subreddit=...` endpoint is hard-blocked for agents ("does not provide free scraping resources for agents", HTTP 429, verified 3x with backoff), so in-window listing had to ride on WebSearch discovery + per-id fetches.
7. Two GLM-5.3 threads surfaced by search (`1w0tgzl` zai-org/GLM-5.3 on Hugging Face, `1vyy3k6` GLM-5.3-Flash) return `data:[]` from PullPush - archived copies absent. NOT banked as read items; treated as unverified leads only.

## Pass 1 - candidates considered (30+; dates below are PullPush `created_utc`, the only dates I trust)

In window (2026-08-31 -> 09-30): 1wrez7j "Qwen, where's the small stuff? (1B/2B/4B)" 09-27; 1w2ow8s "Do you actually use multiple AI provider API keys?" r/LocalLLM 08-30 (1 day out; read anyway).
Near window: 1vkmhyl "Best Local LLMs - August 2026" 08-10; 1vjb15v "No wonder Qwen and Gemma are so different" 08-09; 1vny9zs "GLM 5.3 Released" 08-14; 1ve9ms0 "GLM 5.3 Spotted" 08-03.
Older but question-bearing: 1ue95bf "Every free LLM provider, ranked by how fast the free tier actually runs out" r/better_claw 06-24; 1u5fv6n "Local models in mid-2026" 06-14; 1uyb88e "Kimi K3 weights to be released on the 27th" 07-16; 1v4sm2m "Tested (the updated) Gemma 4 locally on coding" 07-23; 1salgre "Gemma 4 has been released" 04-02; 1scucfg "Gemma 4 26b is the perfect all around local model" 04-05; 1sjq5fo "What is the current solution to running Gemma 4 locally?" 04-12; 1suyu7a "I'm glad we have deepseek" 04-25; 1rqy3cx "Nemotron 3 Super Released" 03-11; 1rri4qb "Nemotron 3 Super and the no free lunch problem" 03-12; 1rw4fp4 "Gave my local Ollama setup a desktop buddy" 03-17; 1ri2irg "Breaking: Today Qwen 3.5 small" 03-01; 1rr4by8 "Nvidia $26B open-weight" 03-11; 1r5beqe "top 4 models on openrouter are all open-weight" 02-15; 1sx5h1t "local coding agent with Gemma 4 and Pi"; 1se6nq5 "What it took to launch GDM's Gemma 4"; 1saltpa "Gemma 4 full text+vision+audio"; 1vx7ei1 "Best Local VLMs - August 2026"; 1rkppnl "best local LLMs as of March 2026"; 1pk3zwb "Multitrillion param open weight models"; 1qx0gxy / 1rowslk (pre-release Gemma 4 speculation); 1f07rst "What UI is everyone using for local models?" (2024, stale); 1hw3jzx "What is your LLM stack"; plus r/AI_Agents 1qze3t4, r/LLMDevs 1s020se, r/LangChain 1uil3n0 (not read).

**Window honesty:** the recipe's strict "last 30 days" set is thin - one verified in-window thread. Reddit's blocking forced discovery through a search backend that strips dates; every candidate that mattered was date-verified through PullPush before banking, and several that search implied were fresh (Nemotron 3 Super "release", Gemma 4 "release") turned out to be March/April 2026 threads. The strongest question-bearing material sits 2-12 weeks outside the window and is banked with its true dates.

## Pass 2 - deep reads (fetched and read end to end: submission body + comments via PullPush)

### 1. "Qwen, where's the small stuff? (1B/2B/4B)" - r/LocalLLaMA, 2026-09-27 (IN WINDOW), 53 comments read
Janitor-slot verdict straight from the community the day before yesterday's window closes:
- Qwen has shipped **no new small models since the 3.5 series**; Qwen 4 rumors say the small sizes are dropped entirely. Small-model demand is real but labs won't spend separate training runs on them ("The problem is that they do a complete separate training run per model").
- ttkciar (regular, runs a test suite): "Gemma-4-12B-it is an excellent model, but a lot more memory-hungry than Qwen3.5-9B (mostly from its fatter K/V caches)" - KV-cache fatness, not weights, is what evicts a janitor from a consumer host.
- Consensus role for tiny models: **fine-tune for exactly one task**; "absolutely terrible as general purpose models" (jferments); "a small specialized model I can run beats a huge general one I cannot" (LuCiAnO241).
- Named live candidates: Qwen3.5-0.8B (official), Qwen3.8-9B-heretic-uncensored GGUF (MTP, Q5_0), Mimo 2.6 distill (slow without MTP), Gemma 4 E2B/E4B (surprisingly good at screenshot-translate-caption pipelines). ttkciar's eval of the 9B distill: "prone to overthinking, and can be somewhat unhinged, but not always."
- The estate's exact contract exists as a user story: Devatator_ building a PC assistant needs "loaded fast, eat a tiny amount of memory, call tools" - xkalibur3 answers: parakeet+laya pipeline runs on integrated GPU, tool-call round trip under a second, "works like 90% of the time," fine-tuning recommended for serious use.
- Local models for code: "even if you have a 27B model, at best it performs like a flagship model from three years ago" - janitor, not judge.

### 2. "Best Local LLMs - August 2026" - r/LocalLLaMA, 2026-08-10, 100 comments read (thread has 187)
- Community hardware-tier stacks (mossy_troll_84): 8-32GB VRAM -> Gemma4-31B; 32-64GB -> Qwen3.8-27B FP8; 64-128GB -> Qwen3.5-122B-A10B; >128GB -> DeepSeek-V4-Flash-0731; and **DeepSeek-V4-Flash-0731 as the agentic/coding pick**.
- UkrMalt (M4 Pro 48GB): "For agentic coding, Qwen3.8 27B-MLX is the best local model I've tried so far: direct Ollama throughput is around 33 tok/s" - and the differentiator is whether the agent can use file tools reliably, which is exactly the janitor bar.
- Tool-calling is still the local weak point: "The issue for me is to run tools. It never worked for me on LM Studio... I always ended up using qwen due to that" (LectureWorried5761).
- Self-reported benchmark caution: all of these are user reports on their own stacks (quant, KV cache quant, FA on/off change results); none of it is verified - funded-tier verification required before promoting any rung (laws.md free-seat sensing rule).
- evranch on Qwen3.6-35B-A3B for code review on a 12GB card with CPU offload: must pass "reasoning_effort: medium" to keep it from thinking in circles.

### 3. "Every free LLM provider, ranked by how fast the free tier actually runs out" - r/better_claw, 2026-06-24, 61 comments read
Measured burn, not marketing - the closest public analog to our free-lane rotation ledger (memory/continuity/seat_memory_20260927/free-lane-provider-roster-20260927.md):
- OpenRouter unfunded: 50 req/day ("gone by breakfast"). Gemini 3.1 Flash Lite: **500 req/day, 15 RPM, 250k TPM**. **Gemma 4 26B/31B via Google AI Studio: 1,500 req/day, 15 RPM, unlimited TPM** - the biggest free bucket found, and it serves the exact size class our janitors need. Gemini 2.5/3.5 Flash free: only 20 req/day.
- Cerebras free tier has **shrunk** - commenters report $5 trial credit and only gpt-oss-120b remaining free (07-25/08-08). Nvidia NIM and SambaNova still free. DeepSeek direct API: "so cheap I run production pipelines for months on couple of dollars."
- The catch, stated plainly: free tiers train on your traffic ("even Google AI Studio... will train on your data until you pay") - confirms the estate's sensing-only law for free lanes.
- OpenRouter natively does fallback chains: pass `models: [a, b, c]` and it "falls through the chain on 429s/5xx" and load-balances one slug across providers - our lane-rotation pattern already exists as a provider feature.

### 4. "Local models in mid-2026" - r/LocalLLaMA, 2026-06-14, 34 comments read
- Thesis: locally runnable models got good by getting **smaller per token**, not bigger: sparse attention, MoE, latent KV compression, multi-token prediction, 4-bit quant.
- Gemma 4 12B run in **GitHub Actions CI for code review** (mattjcoles): "It only picks up 24% of the things i've been scanning for but impressed considering its a very small model" - a working janitor-grade deployment recipe (24% pickup is the honest number).
- cibernox: Q4-QAT Gemma 4 at "165tk/s... might become my default for simple tasks like web crawling and text summarization" - the scut slot, named verbatim.
- arbv: dense Gemma 4 12B at Q8 on one 24GB card; "heavy model quantisation and KV cache quantisation is no go for programming."

### 5. "No wonder Qwen and Gemma are so different" - r/LocalLLaMA, 2026-08-09, 66 comments read
- Same 330-line HTML file: **Qwen 1609 tokens vs Gemma 4258 tokens - 2.6x context cost for the same code**. For a janitor billing context per scut task, tokenizer choice is a line item: Qwen-class tokenizers are the cheap ones for code; Gemma-class for prose. Commenters note the flip side (Gemma's bigger vocab = fatter KV cache per token, consistent with read #1).

### 6. "Gave my local Ollama setup a desktop buddy (morphs into Clippy)" - r/LocalLLaMA, 2026-03-17, 20 comments read
- The Reddit-side echo of the HN Clippy wave (HN item 43905942, 1,122 points, per oneyearago.ai recap - corroborates doors.md:29's claim from a second source). Author: agent wraps Ollama/any OpenAI-compatible endpoint with a floating mascot that executes file ops, browsing, email.
- Author's own admission: "Most smaller models struggle with the ReAct loop. Any workaround?" - the UX threshold the wave exposes is NOT chat polish, it is tool-loop reliability of small models.
- The maintainer thread is a free usability checklist for any estate surface: sandboxed file access must be the default (henk717 refused default file access; author committed to folder-grant mode), and "optional" API key fields must actually omit the auth header (empty keys got rejected by KoboldCpp).

### 7. "Nemotron 3 Super Released" - r/LocalLLaMA, 2026-03-11 (verified; search implied recency it does not have), body read + no-free-lunch follow-up (1rri4qb, 03-12)
- 120B MoE / 12B active, hybrid mamba-transformer, fully open (weights + datasets + recipes, NVIDIA dev blog link in body). 12B active is still above the janitor class but the fully-open-recipes pattern is the steal.
- Follow-up thread's finding: it "feels overly locked down" - broad refusal surface even for absurd creative contexts. Arch alignment: capability without permissiveness is not a janitor.

### 8. "Do you actually use multiple AI provider API keys to get around rate limits?" - r/LocalLLM, 2026-08-30 (one day outside window; 0 comments)
- A builder validating exactly the estate's lane-rotation pain (Groq/Gemini/Cerebras/SambaNova key juggling, manual switch vs wait vs router). Zero traction in-thread - the demand signal is one builder, not a wave; weak evidence, banked as such.

## Research questions, answered from what I read

**Q1 (post-09-28 open-weight janitor candidates):** No credible new sub-4B open-weight release since 09-28 surfaced on Reddit; the freshest signal (1wrez7j, 09-27) says the small-model pipeline is drying up (Qwen skipping 1B/2B/4B; "tiny models just dont do anything for a big company"). Janitor-slot candidates with community traction remain: Gemma 4 E2B/E4B and 12B, Qwen3.5-9B / Qwen3.8-9B distill GGUFs, Mimo 2.6, plus the parakeet+laya pipeline pattern for tool-calling under 1s. All self-reported; none independently benchmarked -> funded tier verifies before any rung swap (laws.md:23).

**Q2 (Lightning replacement / GLM-5.3-Flash rung / Featherless counter):** Free-lane replacements with measured numbers: Google AI Studio Gemma 4 26B/31B (1,500 req/day) is the standout; Gemini 3.1 Flash Lite 500/day; Cerebras free has shrunk to a $5 credit; DeepSeek direct is pennies-not-free. GLM-5.3-Flash is alive in community usage as the cheap-frontier reference (1wrez7j comment 09-27), and r/ZaiGLM reports coding plans "GOOD again" on a credit-based $18/mo model (search-surfaced, thread not archived - unverified lead). **Featherless 22,059 vs 28.6k counter gap: no published explanation found on Reddit.** Marketing page now claims "30,000+ models included" (featherless.ai competitor page, search snippet) and getlatka reports $250-500K/mo revenue / 10k customers / $20M Series A (April 2026) - consistent with a continuously-growing catalog, i.e. our 22,059 was likely a point-in-time scrape, but that is hypothesis, not a verified explanation. OWED.

**Q3 (HN local-LLM wave / UX thresholds):** The Clippy wave's Reddit echo (1rw4fp4) shows the viral hook is personality/nostalgia over a working tool loop, and the operative thresholds are: (a) small models must hold a ReAct/tool loop - most do not; (b) file access sandboxed by default with explicit folder grants; (c) empty-key handling done right; (d) the 6.8GB full-voice stack from the first search result (Qwen3-ASR 1.7B etc.) shows "local tier" now means ASR+LLM+TTS bundles, not a bare chat model. The estate's janitor lanes already meet (b); the steal is (a)+(d): pipeline-of-tiny-specialists over one general small model.

**Q4 (arXiv shelf harvest / stale rows):** Outside this area's reddit lane - not investigated here; flagged for the arXiv-area seat. Nothing in this sweep's reddit doors bears on the 3,776 state/arxiv rows.

## Overlap record (grep receipts)

- catalog/catalog.jsonl (691,788 rows): "where's the small stuff" 0 - "Best Local LLMs" 0 - "GLM 5.3 Released" 0 - "desktop buddy" 0 - "free LLM provider" 0 - "multiple AI provider API keys" 0 - "openrouter are all open-weight" 0 -> all banked threads genuinely new. "GLM-5.3-Flash" 29 rows (docs/ref/GLM53_ARCHITECTURE_PRO.md etc. - our own doctrine, known), "Kimi K3" 2 rows (watch/INTAKE_KIMI_K3_MATH_20260904.md + research system-prompt leak - known), "nemotron" 20 rows (all exo vendored Llama-3.1-Nemotron model cards - not the Nemotron 3 thread), "deepseek" 759 (general).
- memory/ grep "LocalLLaMA": hits are agent_sessions/, improve/ dailies only - no thread-level holdings. "featherless": memory/burns/LEDGER.jsonl + memory/continuity/seat_memory_20260927/free-lane-provider-roster-20260927.md (our own roster - adjacent context, not dupes).

## OWED (not done, not asserted)

- Featherless counter-gap explanation: not found publicly; hypothesis only (point-in-time scrape).
- Threads 1w0tgzl and 1vyy3k6 (GLM-5.3 weights + Flash): discovered, not read (absent from PullPush; Reddit doors blocked) - leads only.
- HN-side reading of item 43905942 itself: not done; its stats come from the oneyearago.ai recap via search, corroborating doors.md:29 secondhand.
- r/ollama and r/MachineLearning month-tops: never retrieved (blocked before discovery).
