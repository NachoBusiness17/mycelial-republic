# Frontier sweep: open-local-language-models via X (adhoc, 2026-10-11)

source-fetched: adhoc. Seat: sweep-open-local-language-models-x (dynamic workflow subagent of the
frontier_olm program). Laws held: no fabrication (OWED where unreachable), byte/URL cites, ascii
only, no em-dashes in my prose (verbatim source quotes preserved as fetched).

## Door health (what actually ran this sitting)

- site:x.com WebSearch: DEAD for content (two timeouts, then a run whose own summary said
  "restricting the search to x.com found no matching posts... X/Twitter content is often poorly
  indexed"). Fallback per recipe: broader queries that surface x.com post/profile URLs.
- The working X door this sitting was mcp__web_reader__webReader on x.com PROFILE pages
  (logged-out render, verbatim post text + dates, no status IDs exposed): x.com/UnslothAI,
  x.com/ollama, x.com/OpenBMB all rendered. The fxtwitter door
  (api.fxtwitter.com/<user>/status/<id>) could NOT be exercised: no status ID ever surfaced
  (search indexes give profile URLs, profile renders give no IDs). Not one item below is resolved
  through fxtwitter; every X-derived quote comes from a profile render I read or a
  search-result snippet banked as such.
- Failures, honestly: sourcefeed.dev DNS-failed on WebFetch (ENOTFOUND) and 500-errored on
  webReader (error id 202610111129586dd52bf0d8014349349-class network error) - snippet-only
  bank. umesh-malik.com AirLLM blog URL (from search) 404s on WebFetch - snippet-only.
  huggingface.co/discussions (global) returns 404: HF discussions are per-repo only. WebSearch
  hit MCP 429/1302 rate limits three times mid-sweep (retried later, succeeded).

## Method

- Pass 1 (broad, ~40 candidates considered, all within ~30-90 days unless flagged): 11
  WebSearch queries (x.com LocalLLaMA, UnslothAI/Gemma 4, AirLLM benchmarks, lobste.rs local
  LLM, small open models Oct 2026, Ollama release notes, sourcefeed AirLLM, Docker tool-calling
  leaderboard, x.com/UnslothAI/status) + 3 x.com profile renders + news.smol.ai front + the
  lobste.rs search page. Candidate clusters: Ollama v0.34.1-v0.40.3 releases; UnslothAI
  (Desktop, Laya, Qwen3.8-27B GGUF #1, Qwen-Image-2.1 7B); OpenBMB (MiniCPM-o 4.5 TyloQuant
  MFQ, Ultra-FineWeb-L1); Qwen3.8 family docs; AirLLM trio (README/dev.to/HN); lobste.rs local
  LLM stories (Bonsai 2, Qwen overthinking, speed-over-intelligence, multi-GPU drifting);
  AINews editions (DeepSeek V4.1-Flash, GLM-5.3-Flash consumer quants, Ornith-1.5, Nemotron
  3.5 Lightning, Muse Glimmer); PromptQuorum Gemma-4-27B-on-24GB claim (snippet, 429 on
  follow-up); Docker Jun-2025 leaderboard (dated out); Toolery 0.1.0 (unfetched, date
  unverified); Toolathlon (search snippet only); May-2026 Ollama CVEs (out of window).
- Pass 2 (deep reads, read end to end by this seat): github.com/ollama/ollama/releases;
  github.com/lyogavin/airllm README; dev.to AirLLM analysis; news.ycombinator.com/item?id=
  49154228; unsloth.ai/docs/models/qwen3.8; lobste.rs/s/r9wkkk (Bonsai 2); lobste.rs/s/k7myyp
  (Qwen overthinking); news.smol.ai front. Plus 3 full x.com profile renders. That is 8 deep
  page reads + 3 profile renders.

## Overlap instruments (commands actually run)

- grep -i -c over catalog/catalog.jsonl: Qwen3.8 71, Bonsai 125, MLX 229, Flash-Next 2,
  Clef 2, reasoning-effort 6, AirLLM 0, Toolathlon 0, TyloQuant 0, systemone 0, v0.40 0,
  overthinking 0.
- Follow-ups: Bonsai's 125 rows are mostly Facebook Sapling's Mercurial "bonsai" data model
  (mine/raw/agent_platform/.../bonsai*.rs) BUT memory/runs/gapwave/splash_bonsai_livetranslate_
  verified_20260920.md is a VERIFIED DIGEST of "Ternary Bonsai 2" (prism-ml HF card +
  prismml.com) + Qwen3.8-27B: Bonsai 2 the model IS already banked. Flash-Next rows are intake
  txts from the 10-09 sibling sweep. memory/runs/gapwave/laya_digest.md: Laya banked. Sibling
  banks read in full this sitting: watch/inbox/frontier_olm_2026-10-09/sweep/open-local-
  language-models-hn.md (Gutsy/VeriLoop/llama.cpp decision table/Strands/Mistral Large 4/Clef/
  Mozilla/Jev index) and grep-level check of frontier_olm_2026-10-08/sweep/open-local-models-x.md
  (it already READ ollama releases v0.35.0-v0.40.2-rc0, llama.cpp releases, and lists gemma4/
  gemma4-desk/gemma4-hermes as distinct estate models).

## Banked items (8, strongest first; deltas over siblings only)

### 1. AirLLM measured verdict: disk streaming loses 2-3 orders of magnitude to quantized local inference

- Source: https://dev.to/arshtechpro/airllm-runs-a-70b-model-on-a-4gb-gpu-its-true-and-thats-not-the-interesting-part-hha
  (read end to end; Aug 3 2026 per site copyright).
- What I read: official benchmark (RTX 6000 Ada, v3.1.0 release notes) generation at "292
  s/token, disk-bound", init 900 s; community 70B-on-NVMe "roughly 5-35 seconds per token",
  MacBook "as low as ~0.07 tokens/sec"; the baseline row: "llama.cpp with a quantized 70B on
  an RTX 4090: 8-15 tokens per second"; batch amortization "35 s/token for a single prompt vs
  5.3 s/token when batching 50" (6.6x); disk math Gen4 NVMe ~20 s/token, Gen3 ~40 s, SATA
  ~280 s; quality stance: AirLLM keeps full-precision weights, 4-bit optional purely to
  shrink bytes read. Verdict quote: "AirLLM didn't remove the cost of running a huge model.
  It moved it - out of VRAM, into time and disk I/O."
- Why: this is RQ4's answer for the 24GB card. Sub-4-bit quant resident in VRAM (8-15 tok/s
  class) beats layer-streaming (0.003-0.2 tok/s class) by 2-3 orders of magnitude on speed;
  disk streaming's only wins are batch-offline amortization and full-precision fidelity. The
  estate's big-model disk lane (VHDX economics in the smith v1.1 disk-ETA work) now has the
  public numbers to cite.
- Overlap: grep "AirLLM"/"airllm" = 0 rows in catalog.jsonl; no sibling sweep bank (10-09 hn
  bank has nothing on it). NEW lane.
- Confidence: 0.9 (numbers quoted from the article's own citations; I did not run AirLLM).

### 2. AirLLM HN thread: the 416-day/80x-cost arithmetic and the community consensus for quantization

- Source: https://news.ycombinator.com/item?id=49154228 (read end to end; ~2026-08-04 by
  68-days-before-snapshot arithmetic; comments to ~Aug 9).
- What I read: imenani cites the project's own "Kimi K3 on RTX 6000 Ada (48GB) takes 292
  s/token"; logicallee's math: "that's 0.003 tokens/second", an hour of normal output (108k
  tokens) "will take 416 days", ~$124.61 electricity, "80x more expensive" than the API;
  junsu22 "quantization might still win on speed?"; sixothree links prior threads showing
  unsloth quants + llama.cpp -cmoe/-mmap "compare negatively" for AirLLM; dsl's salvage:
  overnight batch on sensitive data.
- Why: independent corroboration of item 1 plus the MoE angle (pizza234: MoE on PC needs
  memory-bandwidth-class boxes). Confirms no 2026 head-to-head QUALITY measurement exists in
  any thread I read - speed consensus only. The estate's OWED stays: a controlled AirLLM-vs-
  IQ2/IQ3 quality A/B on the same model.
- Overlap: AirLLM = 0 catalog rows. NEW.
- Confidence: 0.85.

### 3. Bonsai 2 27B agentic head-to-head: benchmark-grade bpw claims die on long-horizon tasks

- Source: https://lobste.rs/s/r9wkkk (story + comments read end to end; submitted 2026-09-18
  by mpweiher, tagged vibecoding, 10 comments, 11 upvotes).
- What I read: the claim, per commenter: "The fact that you get 98.2% of the benchmark
  performance after going from 16 bits per weight to 1.76 bits per weight"; the counter-test
  (ar-nelson, Lua platformer-physics task): Qwen3.8-Flash-Next 27B finished "in about 4 hours
  with no steering needed" while Bonsai 2 "seemed to take 2-3 times as long to accomplish
  each step" despite "twice the tokens/second", looping on repeated paragraphs, and "the
  worst part is it doesn't even save VRAM" (~100K context at 4-bit KV); frontsideair relays
  the r/LocalLLaMA consensus: "Bonsai models are not as good as authors claim them to be,
  getting lost in long horizon tasks" and "their numbers seem cherry-picked".
- Why: two steal rows. (a) Qwen3.8-Flash-Next 27B is the window's best public evidence of a
  local model sustaining a multi-step build task unsteered (RQ1, but at 27B, not 1-8B).
  (b) The Bonsai 2 pattern extends the estate's quant-stratification law (fold row 2:
  perplexity holds while a capability class dies) onto the 1.76bpw frontier: benchmark
  retention 98.2% coexisting with long-horizon agentic collapse. The gapwave verified digest
  (memory/runs/gapwave/splash_bonsai_livetranslate_verified_20260920.md) verified Bonsai 2's
  OWN numbers; this thread is the first banked adversarial field test.
- Overlap: Bonsai 2 model banked (gapwave digest 2026-09-20); Flash-Next touched by 10-09
  sweep intake txts. The head-to-head result and cherry-pick consensus are in no prior bank.
  Delta bank.
- Confidence: 0.8 (commenter evidence, n=1 task, but specific and internally consistent).

### 4. lobste.rs is the live fourth-lane door for r/LocalLLaMA-grade signal (RQ3 answered)

- Source: https://lobste.rs/search?q=llama (page read this sitting; stories span
  2026-06-19 to 2026-10-02).
- What I read (exact titles): "Bonsai 2 27B: Near-Lossless Compression in a 9x Smaller
  Footprint" (2026-09-18); "Qwen 3.8 27B is excellent, but it defaults to wildly
  overthinking things" (2026-08-18); "I'm (mostly) picking models on speed now, not
  intelligence" (2026-08-03); "AI At Home Part 2: Multi GPU Drifting" (2026-08-25);
  "Running local models is good now" (2026-06-19); "MAX models can now run on Apple silicon
  GPUs" (2026-06-28). 233 results over 12 pages for "llama".
- Why: with old.reddit.com JSON walled (the ask's premise), lobste.rs carries exactly the
  missing class: practitioner threads with hardware specifics, benchmark skepticism, and
  relayed r/LocalLLaMA consensus (the Bonsai thread literally quotes the subreddit's
  verdict). Auth-free, fetchable by plain WebFetch, story pages render comments fully.
  Negative rows from the same probe: huggingface.co/discussions (global) 404s (per-repo
  only); HF model-card discussions remain reachable per-repo and are where the VeriLoop-
  class ladders live (10-09 bank item 2).
- Overlap: no sibling sweep used lobste.rs (greps over 10-08/10-09 sweep files: no "lobste"
  rows). NEW door for the daily lanes.
- Confidence: 0.95 (I fetched it; the titles are verbatim).

### 5. Ollama v0.40.2 (stable, Oct 8) + v0.40.3-rc0: background model upgrades land on the janitor lane

- Source: https://github.com/ollama/ollama/releases (read end to end this sitting; supersedes
  the 10-08 sibling read which stopped at v0.40.2-rc0).
- Delta over the 10-08 bank: v0.40.2 is now Latest (08 Oct) with models downloaded earlier
  "upgraded in the background the first time you run them" (llama.cpp compatibility; originals
  kept as backups; "ollama list no longer shows duplicate entries for upgraded models");
  v0.40.3-rc0 (11 Oct) pauses "background model upgrades, which added overhead to every
  request in high-volume use such as embeddings" and gives Claude launch "the model's full
  context length". Older-but-unbanked v0.34.x rows: /api/tags "3.1 s -> 294 ms cold";
  runaway-repeat detection now needs 100 repeat tokens (fewer OCR false positives);
  "Structured outputs on thinking models now apply in a single pass"; "Gemma 4 on Apple
  Silicon now picks the best image resolution per image". No new quant formats shipped in
  the whole v0.34-v0.40 range.
- Why (RQ2): the estate's ollama janitors auto-upgrade models on first run after moving to
  v0.40.2+ - the gemma:2b + gemma4 lane should expect a one-time background re-download,
  backup copies left on disk (disk-floor pressure the smith disk-ETA alert watches), and the
  pre-v0.40.2 duplicate-list bug. v0.40.3-rc0's embeddings-overhead pause matters if the
  percolator/embedding lanes run high-volume.
- Overlap: v0.35.0/v0.35.1/v0.40.0/v0.40.1 already banked by 10-08 x sweep item 5 (verified
  by grep of its file). Delta: v0.40.2-stable behavior, v0.40.3-rc0, v0.34.x perf/fix rows.
- Confidence: 0.95 (primary page, fetched this sitting).

### 6. Unsloth Qwen3.8 docs: the 27B quant ladder + tool-calling contract details

- Source: https://unsloth.ai/docs/models/qwen3.8 (read end to end; page carries an "Aug 19
  Update" note, fetched 2026-10-11).
- What I read: "Qwen3.8-27B has vision and reasoning capabilities, a 256K context window, and
  runs locally on 17GB RAM/VRAM setups"; tool calling: "Developer Role Support for agentic
  tools like Codex" and "Improved parsing nested objects to make tools succeed more"; quant
  table for 27B: 4-bit 16-19 GB (fits the 24GB card), 3-bit 12-14 GB, 2-bit 9-11 GB, 1-bit
  7-8 GB; "NVFP4 is consistency 92% to 97% accuracy recovery vs BF16" and runs "~1.5x faster
  than BF16" on Blackwell; 1.585-class TQ1_0/Q1_0 at "1.1875 bpw... fine for post training
  quantization (PTQ) without the need for QAT or QAD"; benchmarks Terminal Bench 2.1: 73.0,
  SWE-bench Pro: 61.7.
- Why (RQ1): the honest answer is the 1-8B chat class produced NO new in-window replacement
  (matching the 10-08/10-09 verdicts); the local agentic action the evidence supports is
  27B-at-4bit on 24GB (16-19GB weights + KV), with the tool-calling contract now explicitly
  hardened (developer role + nested-object parsing - the exact contract the Qwen X AMA was
  asked to stabilize).
- Overlap: Qwen3.8 is estate-known (71 catalog rows: kev PLAN_27b, probes, behavioral
  animals; splash digest). The Unsloth-docs specifics (NVFP4 recovery band, 1.1875bpw PTQ
  claim, nested-object tool parsing, 27B quant table) are in none of the sibling banks I
  read. Delta bank.
- Confidence: 0.85.

### 7. Qwen 3.8 overthinking thread: llama-server --reasoning-effort + "speed, not capability, is the bottleneck"

- Source: https://lobste.rs/s/k7myyp (story + comments read end to end; submitted 2026-08-17
  by Yogthos linking Simon Willison; 5 comments, 24 points).
- What I read: lifepillar: "recently llama-server has gained --reasoning-effort" and Pi
  supports "supportsReasoningEffort and thinkingLevelMap" (toggle no-thinking/low/medium/
  xhigh with Shift-Tab); "Speed, rather than capability, is currently the main bottleneck
  for effective use of local language models on consumer hardware"; Yogthos: "For easy
  problems, it's better to limit the budget so it doesn't overdesign".
- Why: janitor-lane config signal - the estate's thinking-mode-axis law (AGENTS.md) now has
  the server-side flag and the client config shape for it; the speed-over-capability
  judgment from a practitioner thread matches the estate's own tier ladder (janitors cheap,
  judgment climbs).
- Overlap: reasoning-effort has 6 catalog rows (estate's own probes); the llama-server flag
  arrival + Pi config + the bottleneck quote are new to the banks I read. Delta bank.
- Confidence: 0.8.

### 8. UnslothAI X profile: Unsloth Desktop (self-healing tool calls) + the Gemma 4 re-download signal

- Source: https://x.com/UnslothAI (full profile render via webReader this sitting; visible
  posts Aug 11 - Sep 28).
- What I read (verbatim from render): "Unsloth Desktop is here! The first desktop app to run
  and train models locally. It's open source. It's private. All running locally. Connect
  Claude Code and Codex to local LLMs. 50% more accurate, self-healing tool calls, works
  with your existing setup."; "Qwen3.8-27B GGUF is already Unsloth's #1 most-downloaded
  model ever" (Sep 23); Laya decision models "run locally on 4GB RAM" with "Jev-compatible
  API" (Sep 28); Qwen-Image-2.1 7B local on 12GB VRAM (Sep 22). Search-snippet (NOT in my
  render window; banked as snippet per recipe): "Gemma 4 is now faster and much more
  accurate! Google made huge improvements to tool-calling and chat accuracy, reliability +
  speed. To get fixes, re-download..."
- Why: RQ1/RQ2 bridge - a Google-side Gemma 4 weights refresh (the re-download advice)
  touches the estate's gemma4 janitor directly; the estate already runs a gemma4-desk model
  (10-08 x bank line 28-29), and Unsloth Desktop is the plausibly-matching product (identity
  unverified, OWED). "Self-healing tool calls" is the exact failure class the estate's
  retry/verification organs own.
- Overlap: Laya banked (memory/runs/gapwave/laya_digest.md - re-bank avoided, cited only);
  Qwen3.8-27B GGUF popularity known at family level; Desktop + Gemma-4-refresh snippet in no
  prior bank I read. Delta bank.
- Confidence: 0.7 (profile renders truncate; the Gemma 4 line is snippet-only).

## Per-research-question verdicts

- RQ1 (1-8B class sustaining multi-step tool-calling on 24GB at measured tok/s since
  2026-10-01): NO new 1-8B chat model surfaced that clears the bar - replicating the 10-08/
  10-09 verdicts from the X/lobste doors. The window's local multi-step evidence sits at
  27B: Qwen3.8-Flash-Next's unsteered 4-hour build (item 3), Qwen3.8-27B at 4-bit 16-19GB
  with the hardened tool-calling contract (item 6). The 1-8B measured action remains
  decision models (Gutsy 0.8B, tev1, per the 10-09 bank). PromptQuorum's "Gemma 4 27B best
  for tool calling on a 24GB GPU" claim is snippet-only (follow-up 429-limited): OWED.
- RQ2 (Ollama runtime since 2026-07-20, touching gemma:2b + gemma4): engine split MLX-default
  on Apple Silicon (v0.40.0) with gemma4 + qwen3.8 named; v0.40.2's background model
  upgrades hit the janitor lane (one-time re-download + backups + pre-fix duplicate-list
  bug); Windows-specific: 2GiB clef-head read fix and symlink avoidance (v0.40.1); API
  surface grew /v1/systemone decision endpoints + CAPABILITY Modelfiles; /api/tags 294ms;
  NO new quant formats in v0.34-v0.40. The estate's 2026-07-20 basics pack predates all of
  this.
- RQ3 (auth-free reddit replacement): lobste.rs verified live and signal-dense (item 4);
  AINews (news.smol.ai) aggregates X/Reddit local-model discourse but its front page I read
  only reached Sep 09 editions - October editions unfetched, OWED; HF global discussions
  404 (per-repo only); the fxtwitter door untested for lack of status IDs (profile renders
  substituted).
- RQ4 (AirLLM-style vs sub-4-bit on 24GB): answered by items 1-2 with measured numbers:
  disk streaming is 2-3 orders slower (0.003-0.2 tok/s vs 8-15 tok/s quantized 70B on a
  4090); its quality argument (unquantized weights) is real but NO rigorous 2026 quality
  head-to-head exists in anything I read - that A/B stays OWED. AirLLM itself is alive and
  2026-current (README updated 2026/09; Qwen3.8-Flash-Next 5.95GB and Kimi K3 3.72GB rows).

## Not run / OWED (do not assert)

- No estate instrument fired (no ollama pull, no battery, no pytest). All numbers are
  fetched external claims.
- sourcefeed.dev and umesh-malik.com pieces: snippet-only, both doors failed.
- PromptQuorum Gemma-4-27B-on-24GB piece: unfetched (WebSearch 429 twice).
- Toolery 0.1.0 deterministic tool-calling benchmark: surfaced in search, date and content
  unverified.
- Unsloth Desktop vs estate gemma4-desk identity: one fetch owed.
- fxtwitter JSON door: never exercised (no status IDs surfaced); profile renders were the X
  evidence actually read.
- AINews October editions: unfetched.

## Receipt

11 WebSearch calls (3 rate-limit retries), 3 webReader x.com profile renders, 8 deep page
reads (ollama releases, airllm README, dev.to, HN 49154228, unsloth qwen3.8 docs, 2 lobste.rs
stories, lobste.rs search) + news.smol.ai front. Overlap: 12 catalog greps, bounded memory/
sibling greps, full read of the 10-09 hn bank, grep of the 10-08 x bank, head of the gapwave
splash digest. This file is the bank; the JSON result carries the same 8 items.
