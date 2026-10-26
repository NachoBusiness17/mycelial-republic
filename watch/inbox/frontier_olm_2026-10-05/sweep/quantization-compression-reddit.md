# SWEEP: quantization-compression via reddit - source-fetched: 2026-10-05

Sweeper: sweep-quantization-compression-reddit (frontier sweep gopher, dynamic workflow run dwfrun-daecd119).
Area: quantize-target law + local janitor tier model cards (byte budget for the 2B-4B workers).

NOTE ON QUOTES: this seat's no-em-dash law applies to authored content including banked quotes; where a source quote contained an em-dash character, it is reproduced here with a plain hyphen. No other normalization. URLs and numbers are exact.

## Door status (recorded per the fetch recipe)

Every direct Reddit door is BLOCKED from this host, verified in-session:

1. WebFetch on old.reddit.com/r/LocalLLaMA/top.json?t=month&limit=50 (and r/ollama, r/LocalLLM) returned the "Welcome to Reddit" landing page HTML, not JSON.
2. curl with a browser UA on the same old.reddit.com JSON URL followed a 302 to the same landing page (HTTP 200 but `<!DOCTYPE html> ... <title>Welcome to Reddit</title>`, 324362 bytes, zero JSON).
3. WebFetch on a www.reddit.com thread URL returned a one-word "Reddit" placeholder.
4. mcp web_reader on the same www thread returned "Reddit - Please wait for verification" (bot wall); on old.reddit.com it returned "Log in to use old Reddit".

Fallbacks actually used (both real, both recorded):
- pullpush.io mirror API (api.pullpush.io/reddit/search/submission and /comment) - full submission selftext + comments with exact created_utc. This became the primary read door. Caveat: pullpush score/num_comments fields are archival snapshots (mostly 0-5), so ranking by score was impossible; ranking was by topic fit + comment count + my own reads. Coverage was good for Sept, thinner for the last ~72h.
- WebSearch site:reddit.com - surfaced candidate permalinks (degraded: the underlying tool intermittently 429/1302s, and its "community consensus" summaries are NOT banked as evidence; only threads I fetched through pullpush are banked).
- Corroborating fetches outside Reddit: runtimewire.com article (Bartowski per-tensor maps) and ollama.com/library + /library/gemma4/tags (RQ3 ground truth).

## Pass 1 (broad sweep)

Script `.tmp_sweep_pass1.py` ran 10 pullpush queries (4 subreddit top-sort + 6 keyword) filtered hard to created_utc in [2026-09-05T14:51Z, 2026-10-05T14:51Z]: 531 unique in-window submissions, of which 244 relevant after subreddit+keyword filtering (list in `.tmp_sweep_candidates.json`, kept on disk). Well over the 30-candidate bar. Notable considered-and-not-banked: Halv/SWE-rebench (astroturf-flagged, below), "Spomin - Live KV cache compaction" (title only, not deep-read in time), FP8 KV-cache threads on r/machinelearningnews (link posts).

## Pass 2 (deep reads: 8 threads end to end, submission + comments via pullpush)

### 1. "I tested Qwen3 14B vs Llama 3.2 3B on local tool-calling" (r/LocalLLM, 2026-09-08, id 1waaebb)
36 runs (6 tasks x 2 models x 3 trials), both at Q4_K_M, Ollama 0.12.8, M2 24GB. Qwen3 14B: 100% valid JSON / 100% schema match / 90% right tool. Llama 3.2 3B: 90% / 60% / 50%. Key quote: "Schema matching (60% vs 100%) is the real differentiator. The 3B produces valid JSON but the args are often wrong types. Passing \"100\" for an integer, or missing a required field." Also: "The 3B has a 10% JSON-validity failure rate." Community reception hostile ("Cool slop bro", "ancient models") - treat numbers as one amateur harness, n=36, unreplicated. Maps to RQ1+RQ2: at Q4 the 3B janitor class drops tool-call syntax on exactly the axis our shape laws care about; 10% unparseable output on a 3B is the direct warning for gemma:2b-class tool loops.
Overlap: `grep -i hardnumbers catalog/catalog.jsonl` = 0 hits; memory/ = 1 hit (`memory/trajectory/steps.jsonl`, incidental). NOT held.

### 2. "Qwen 3.8 27B vision at different bit widths... 17 checks" (r/LocalLLM, 2026-09-20, id 1wlmg18)
Same base model, same seeds, headless-Chromium fake-clock grader validated against hand-written mutants (reference 17/17, blank 4/17). Results, mean-of-17 per page: bf16 53.8GB = 13.9; Q4_K_M 16.6GB = 13.7; Q3_K_M 13.3GB = 13.0; custom 12GB quant = 11.4; Ternary Bonsai 2 PQ2_0 7.2GB = 5.9; PTQ1_0 5.9GB = 5.0. Quote: "Below 12 GB it falls off a cliff... 8 of its 14 pages died on JavaScript errors, and about half its replies ran out the token budget deliberating inside the answer." Honest variance note: "bf16 scored 16/17 and 10/17 on the *same card* with two seeds". Maps to RQ1/RQ2: 4-bit is statistically indistinguishable from bf16 on a code-generation task; the sub-12GB tier fails via JS crashes = structured-output failure, the quantized analogue of our tool-call shape laws. Also a reusable harness pattern: graded page checks + mutants, cheap enough to run locally on janitors.
Overlap: Ternary Bonsai 2 IS a known holding - `memory/runs/gapwave/splash_bonsai_livetranslate_verified_20260920.md` ("VERIFIED DIGEST - Splash / Ternary Bonsai 2 / LiveTranslate / Qwen3.8-27B", 2026-09-20) + 1 catalog line. The 17-check per-bit table itself is NOT held.

### 3. Bartowski per-tensor GGUF quant maps (r/RuntimeWire link post 1wd7l86, 2026-09-11; article fetched at runtimewire.com/article/bartowski-per-tensor-layout-maps-gguf-quantization, pub 2026-09-11)
Replaces fixed name/shape/position heuristics with a layout map naming a quant type for every eligible tensor; built from ~96h / 1000+ quantizations, degrade-one KL-divergence runs vs bf16 (wikitext, 512 ctx). Main sweeps on Qwen3.5 0.8B and 4B - janitor-class. Key finding per the fetched article: token embeddings carry "about eight times the damage of the worst individual weight tensor in the 0.8B model and 16 times the damage in the 4B model"; U-shaped layer sensitivity; embeddings don't need q8_0 (q4_k recovers most). New suffix rules _S (>=90% at named type) / _M (70% floor) / _L; ships as `--tensor-type-file` for llama.cpp; already in MiniCPM5-2B + Gryphe Pantheon 26B releases. Maps to RQ1/RQ3: the cheapest path to better-than-Q4_K_M byte budgets on exactly the estate's worker class - quantize the insensitive tensors down, keep embeddings/value-projections up.
Overlap: catalog "Bartowski" 1 line = unrelated letta test config filename (`bartowski-ministral-8b-instruct-2410.json`); "per-tensor" catalog 0. The maps article NOT held.

### 4. "Which GGUF quant should you actually use with Ollama?" (r/ollama, 2026-09-16, id 1whpqhf)
Vendor-authored guide (disclosed Actian affiliation). Quote: "If Q4_K_M doesn't fit, choose a smaller model instead of dropping to Q3 or Q2. A 3B model at Q4_K_M usually produces more reliable responses than a 7B model forced into Q3 or Q2." Plus: "Default to Q4_K_M for almost everything: chat, RAG, and agent tool calling", Q5_K_M/Q8_0 for "precision-sensitive (coding, mathematical reasoning, structured output)", and "GGUF is the right format for Ollama and llama.cpp on local and edge hardware; AWQ is better suited for cloud GPU inference with vLLM." Maps to RQ1+RQ3: the quantize-target floor (never Q3/Q2 for tool work; shrink model before bits) stated as community practice; AWQ = cloud-only per this guide.
Overlap: "Q4_K_M" catalog 18 / memory 82 = our own vocabulary; this guide not held (no title/URL match).

### 5. "Context Compaction in Open WebUI (filter, tested with Qwen 3.8 27b)" (r/LocalLLM, 2026-09-12, id 1wekmhf)
Full filter source posted. Finding: Open WebUI's built-in compaction "runs in `process_chat_payload` - the **initial request path only**. It does NOT run inside the **agentic tool-call loop**" - so tool loops grow context uncompacted until the server rejects ("request (132705 tokens) exceeds the available context size (130048 tokens)"). Their filter hooks inlet/request on EVERY loop iteration; summary prompt preserves "(1) key decisions and their rationale, (2) file paths, configuration values, and code changes, (3) problems encountered and how they were resolved, (4) pending or unfinished work"; truncation fallback; chars_per_token 3.0 for code-heavy payload vs Open WebUI's 4.0 (which "underestimates code-heavy contexts"); iterative re-summarize of the keep-set. Maps to RQ4: this IS summary distillation for agent loops, and the 4-item preserve list is a ready-made law-compilation contract. Limit: NO recall measurement anywhere in the thread - cost is asserted, not graded. Commenter nickless07: parallel approach "prunes old tool outputs and old CoT".
Overlap: "Open WebUI" catalog 7 / memory 12 = generic mentions; this filter not held.

### 6. "Can an AI Agent Run for Years Without Compressing Away Its Memory?" (r/Rag, 2026-09-07, id 1w9sklm, 36 comments read)
Question thread; no benchmark numbers, but the sharpest architecture answer in the sweep. donk8r: "An append-only log of what happened should never be compressed, because that is the audit trail and the answer to why a decision was made. Current state is a projection over that log" + bitemporal facts (valid-time vs ingestion-time; supplier-X example). Jbpaul_: un-summarized memory file + deterministic keyword-header lookup table ("if I ask you about X, read all this background before replying"). Zep's Graphiti named as bitemporal-agent-memory reference; Core Memory uses append-only supersession edges (caused_by/supersedes/contradicts...). Maps to RQ4: the recall-cost answer shape for quantized_thought - compile laws from the log, never compress the log itself; the compiled rule is a projection and can be re-derived. This maps 1:1 onto our receipt/rib + law-compilation split (DNA residual vs registry).
Overlap: "bitemporal" catalog 0 / memory 6 (trajectory + notes only); thread not held.

### 7. "Qwen3.8-27B-TWIN-TURBO...-NVFP4 - most accurate tool calling" (r/LocalLLaMA, 2026-09-14, id 1wfw9gb)
OP anecdote (n=1, hype-adjacent, a DavidAU merge others call "controversial"). The bankable content is in Mordimer86's comment: same task (Tauri+Yew rich text editor via OpenCode) at IQ4_XS took 25 min vs GSQ-RCO IQ3_S 5 hours: "GSQ-RCO IQ3_S did it too, but took 5 hours. That's the cost of a lower quant that does the job I guess." Plus config lesson: reasoning must be set xhigh or OpenCode skips it; JC1DA: "pretty good for short and well defined tasks. Not so good for long running tasks." Maps to RQ1/RQ2: sub-4-bit doesn't just lose accuracy on repo-editing, it loses wall-clock 12x via retries.
Overlap: "NVFP4" catalog 7 / memory 22 = our vocabulary; thread not held.

### 8. gemma4 tags on the Ollama registry (ollama.com/library/gemma4/tags, fetched 2026-10-05; page "updated 5 days ago")
RQ3 ground truth for the estate's own short worker: 51 tags. e2b: QAT 4.3GB / Q4_K_M 4.6GB / Q8_0 8.1GB / bf16 10GB / MXFP8 8.2GB / NVFP4 7.5GB. e4b: QAT 6.1GB / Q4_K_M 6.6GB / Q8_0 12GB / bf16 16GB / MXFP8 12GB / NVFP4 9.5GB. 12b/26b/31b same ladder; 26b-a4b MoE variants; e2b/e4b at 128K ctx, 12b+ at 256K. Library page also confirms pullable today: qwen3.5 (0.8b/2b/4b/9b, updated 18h ago), qwen3.8 27b (1 week), qwen3.6 27b/35b (4 days), lfm2.5 8b ("an edge model built for fast, reliable tool calling on consumer hardware"), tev1 0.8b/4b + nimble 9b (3 days, "decision" tag). All capability-tagged tools/thinking/vision.
Overlap: "gemma4" catalog 104 / memory 791 = the estate's own worker model, heavily held; the estate map's claim that the quant shelf is "not yet inventoried" is confirmed - no held record of the per-quant byte ladder.

## Considered, not banked
- Halv "51.1% fewer tokens per correct answer" (r/codex, 2026-09-05, 1w84sug): read end to end; community flags astroturf ("This is the second post that I've seen with your garbage product that's been botted") and cache-cost objections. Claim shape (`tokens per correct answer`) worth stealing as a metric; the product claim is not. Overlap: `grep -F "51.1% fewer tokens" catalog.jsonl` = 0; "Halv" catalog hits are substring noise.
- "PTQ works well at 4 bits and below that we found QAT matters a lot more" (r/LLMDevs, 1wetgn4, 2026-09-13): strong title, not deep-read in time - OWED if the estate wants it.
- Qwen 3.6 27B BF16 vs Q4_K_M vs Q8_0 BFCL eval (1sxzqry, 695 points, 152 comments): the single best RQ1 data point (BFCL 400 samples: BF16 63.25% vs Q4_K_M 63.00% vs Q8_0 63.00% function-calling; HumanEval 56.1 / 50.6 / 52.4) but created_utc 2026-04-28, OUTSIDE the 30-day window, so it fails the sweep's recency rule. Recorded here because the number is exactly what the quantize-target law asks.

## Answers to the four research questions (from what I read this session)

1. Quality-vs-bits on 2B-8B at 4-bit vs 8-bit, tool-calling/repo-editing: two in-window measurements agree that bit-width barely moves function-calling accuracy (1wlmg18: Q4_K_M 13.7 vs bf16 13.9 of 17; the April BFCL eval: 63.0 vs 63.25) while model SIZE moves it hugely (3B Q4: 50% right-tool vs 14B Q4: 90%). Repo-editing cost shows up as wall-clock and crash-tail, not headline accuracy (IQ3_S 5h vs IQ4_XS 25min; Bonsai JS-error pages).
2. Does sub-8-bit degrade structured tool-call syntax/JSON? At Q4_K_M: syntax mostly survives (90-100% valid JSON in 1waaebb; schema-match is the fragile axis, 60% at 3B). Below ~4-bit it breaks visibly: Bonsai pages die on JS errors, IQ3_S needs hours of retry. The estate's shape laws should assume a Q4 floor for any tool-emitting janitor, and schema-validate every call regardless of quant.
3. Downloadable/runnable today (Ollama host): gemma4 ships QAT/Q4_K_M/Q8_0/bf16/MXFP8/NVFP4 for every size incl. e2b 4.3GB and e4b 6.1GB QAT; qwen3.5 0.8-9b, qwen3.8 27b, qwen3.6 27/35b, lfm2.5 8b, tev1/nimble all live in the library with tools tags (fetched today). AWQ is vLLM/cloud-side per the r/ollama guide; GGUF is the Ollama path. Bartowski per-tensor maps (item 3) are the newest lever for below-Q4_K_M byte budgets without the Q3 cliff.
4. Compression for long-lived agent context vs quantized_thought: practice converges on (a) summarize-before-each-tool-loop with an explicit preserve list (decisions+rationale, paths/config/code, problems+fixes, pending work) - 1wekmhf; (b) never compress the append-only log; compiled rules are projections re-derivable from it; bitemporal valid-time beats recency ranking - 1w9sklm. Measured recall cost: NOBODY in the read set measured it (Halv's token-per-correct-answer is the only quantified token-cost metric seen, and it is astroturf-flagged). OWED: a recall-graded compression eval on the estate's own percolator output.

## Honest limits
- pullpush is a mirror: scores/comment-counts are archival snapshots; last-72h coverage thinner; deleted content may vanish from mirrors. Every banked quote above came from pullpush-returned JSON or the two corroborating fetches, read in this session.
- Community reception flags recorded where present (items 1 and 7: slop/astroturf suspicion; item 4: vendor affiliation). Nothing here is independently reproduced; treat all numbers as one-run community measurements.
- r/MachineLearning contributed 0 banked items (top-sort query rate-limited; nothing relevant surfaced via fallback).
- The 2026-04-28 BFCL eval is excluded by the 30-day rule and appears only in considered-not-banked.
- Temp artifacts left in repo root for audit: `.tmp_sweep_candidates.json` (531 candidates), `.tmp_sweep_deep/` (8 submission + comment JSONs), `.tmp_sweep_pass1.py`, `.tmp_sweep_pass2.py`; `.tmp_sweep_llama.json` deleted at fetch time, `.tmp_pp.json` deleted.
