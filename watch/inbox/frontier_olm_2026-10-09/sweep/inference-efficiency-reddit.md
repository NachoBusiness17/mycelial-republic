# Frontier sweep: inference-efficiency via reddit - 2026-10-09

source-fetched: 2026-10-09. Seat: sweep-inference-efficiency-reddit (dynamic workflow gopher).
Ask: four research questions (spec-decode/batching vs the driving ladder and the inference-budget
terminal rule; serving-stack benchmarks vs the estate's free-lane row counts; which of the day-8
mine's 32 unbanked sweeps carry inference-efficiency claims to re-measure first at funded tier;
whether inference-efficiency is zero-coverage or shelf-held).

## Door record (degraded, as the recipe requires recorded)

- Recipe door `old.reddit.com/r/*/top.json`: WALLED. WebFetch returned the "Welcome to Reddit"
  shell for r/LocalLLaMA and r/ollama; r/LocalLLM timed out at 60s. curl measured the wall
  directly: `old.reddit.com` returns HTTP 302 (login redirect), `www.reddit.com/r/LocalLLaMA/top.json`
  returns HTTP 200 but 189,908 bytes of HTML block page, not JSON (commands run this session,
  outputs observed).
- Arctic Shift archive API (the door the day-9 agent-memory sibling proved this morning):
  HARD-DOWN this session. Every call to `arctic-shift.photon-reddit.com` returned HTTP 522
  (Cloudflare origin timeout) across 3 retries x 3 backoffs on two queries before the job was
  stopped; log at `_ais` run trail. It worked for the sibling earlier today, so this is an
  outage window, not a dead host.
- PullPush: alive but empty for recent IDs (`api.pullpush.io/reddit/search/submission/?ids=1x023z4`
  returned `{"data":[],...}`), matching the day-8 seat's finding.
- WebSearch `site:reddit.com`: WORKED but rate-limited (one query burned 2 dead 1302 attempts
  before answering on retry; others answered first try). Used as the discovery aid per the
  recipe fallback. Its date filtering is unreliable: it surfaced several high-value threads
  that redlib dates place OUTSIDE the 30-day window (stated per item below; never backdated).
- WORKING DOOR (all deep reads): safereddit.com redlib + Anubis proof-of-work solve, the door
  day-8's `_redlib_read.py` proved. Reused this session via `_redlib_ie.py` (wave 1: 10 threads,
  exit 0) and `_redlib_listings.py` (top-month + search listings, exit 0, census saved to
  `ie_listings_census.json`, 56 unique rows). Text extracted with day-8's proven
  `_redlib_extract.py` into `_txt_ie_*.txt` / `_txt_ie2_*.txt`; raw HTML kept as `ie_*.html` /
  `ie2_*.html`. Quote-fidelity caveat: redlib is a rendering mirror; verbatim quotes below come
  from those renders, one fetch-layer discount applies.
- Date authority: per-thread `<span class="created" title="...">` stamps from the fetched HTML
  (the census JSON's created column mis-pairs across rows; the per-thread stamps govern).

## Pass 1 (broad sweep, 30+ candidates)

Candidate pool this session: 56 unique listing rows from the redlib top-month/search census
(9 listing pages: r/LocalLLaMA top x2 pages, r/ollama top, r/LocalLLM top, plus searches for
speculative / vllm / throughput / performance / inference), ~20 candidates from 3 WebSearch
waves, 16 threads actually fetched and read (wave 1: 10, wave 2: 6). In-window (2026-09-09 to
2026-10-09) and on-area candidates considered include: 1x023z4 (flashnext 6xGPU, Oct 7),
1wwu6zj (overfit engines, Oct 3, 392 pts), 1wx0jtb (DwarfStar, Oct 3, 132), 1wvxih5 (M4 Max
bench, Oct 2, 200), 1wjnkgm (cost-per-task, Sep 18, 156), 1wj0arv (six days 16GB, Sep 17),
1wd8xc7 (Ollama Cloud v4.1, Sep 11), 1wc6tka (unswallow, Sep 10), DwarfStar-census Sep 21 row
(proved to be the Oct 3 thread on per-thread dating), "Finally got Qwen 3.8 Next running on my
v100 6gpu setup (TP2 PP3)" (r/LocalAIServers, 215), "Union Alpha is NOT a model... 2 tier
gateway" (Sep 10, 323), "400+ LLM agents living in a 2004-era MMO server, all local on
Qwen3-4B" (Oct 2, 290), "Germany... sovereign model Kolibri" (Oct 1, 460), "My agent kept
randomly stopping" census row, "Detecting hallucinations in local models without eating VRAM"
(83), "Thank you, Ollama" (72), "I stopped using the smartest AI models" (158), "The new
subscription model is bad.. really bad" (Sep 25, 73), "Qwen 3.8 flash with Ollama" (Oct 4, 27),
"What local Ollama models would you recommend RTX 5060 Ti 16GB" (Oct 8, 35), "Six days
building a local assistant" (29), "Built a fully local Mac app on Ollama" (33). Out-of-window
candidates the search engine surfaced, date-checked and handled per item: 1x12dkh (Vulkan
price-perf, REMOVED BY MODERATORS as LLM-slop; only its comment thread survives, treated as
lead), 1vx2i7k (ubatch PP/TG, Aug 24), 1vtc0z7 (flags/MTP bug, Aug 20), 1vi6hmw (Battlemage
SYCL gate, Aug 7), 1nwzs0k (Qwen3-Next pillars, Oct 2025), 1w34m6p (free tiers, Aug 31),
1ue95bf (free tier depletion, Jun 24), 1tw8jv6 (freellmpool, Jun 4). Count over the 30 floor.

## Pass 2 (deep reads, end to end, all via the redlib door)

Sixteen threads fetched (HTTP 200 each) and read via the extractor output in full: wave 1
(1x023z4, 1wwu6zj, 1x12dkh, 1vx2i7k, 1w34m6p, 1tw8jv6, 1ue95bf, 1vtc0z7, 1vi6hmw, 1nwzs0k),
wave 2 (1wd8xc7, 1wc6tka, 1wx0jtb, 1wjnkgm, 1wvxih5, 1wj0arv). OP + comment trees read for
every banked item; quotes below are verbatim from those reads.

## Anti-rebank base (read in full or targeted this session)

watch/inbox/frontier_olm_2026-10-08/sweep/inference-efficiency-reddit.md (8 banked threads),
inference-efficiency-hn.md (8 banked), inference-efficiency-arxiv.md (8 banked),
steal/inference-efficiency-hn.md (the two-find card), frontier_olm_2026-10-02/sweep/
inference-efficiency-reddit.md (D1-D7), frontier_olm_2026-10-03/sweep/
inference-efficiency-reddit.md (7 banked), frontier_olm_2026-10-03/sweep/
kv-cache-and-context-engineering-reddit.md (items 1-8: banks 1wjnkgm, 1wj0arv, 1wvxih5,
unswallow/1wc6tka), frontier_olm_2026-10-04/sweep/kv-cache-and-context-engineering-reddit.md
(D1-D6), day-9 sibling banks (kv-cache-hn/x, quantization-hn/x, open-local-language-models-*,
agent-memory-continuity-*), and day-9 lens files. The estate's own spec-decode holding:
memory/vault/astra_v2_companions/local-evidence.md:7 (L2 MTP: 85-90 pct acceptance, 1.8x TPS,
llama.cpp `--spec-type draft-mtp` merged, Ollama 0.31 auto-draft).

## Banked items (strongest first)

### 1. Qwen3.8-Flash-Next on 6x3090/6x4090 without NVLink: multi-session long-context serving patched 8-10x (r/LocalLLaMA 1x023z4, 2026-10-07)
Quote: "The point is the shape: patched prefill is flat from 5k to 250k and decode barely
drops, while upstream halves every 50k or so."
Measured (OP tables): prefill 1 session 250k ctx: 263 to 2,111 t/s on 6x3090 (8x), 744 to
7,403 on 6x4090 (10x); decode 1 session 250k: 10.2 to 33.7 (3.3x); decode 5 sessions each
250k: 2.3 to 27.3 per session (10.8x, self-flagged as against a collapsed baseline: "The 10.8x
is against a 2.3 t/s baseline, so do not quote that one"). Spec-decode in the same thread:
MTP "tried it, it was slower in most cases on this box"; n-gram lookup speculation 2-2.5x on
code rewrites/refactoring, 1.5x on code explanation, nothing on prose, and it "switches itself
off beyond two active users." vLLM ruled out on this topology: no layer/pipeline parallel, no
RAM prefix caching, no save/restore, model will not split 5-6 ways (OP edits). Binaries:
github.com/lukolszewski/llama.cpp-multigpu on upstream df03399b8; upstream discussion
ggml-org/llama.cpp#30071. Q1/Q2: continuous batching at long context is the biggest measured
local-rung gain of the window, and it is a serving-layer patch, not a model upgrade; the
estate's AMD/Vulkan box cannot use these CUDA tarballs directly, but the upstream discussion
is the fold to watch. Overlap: `git grep -ilI` 0 hits for "1x023z4", "llama.cpp-multigpu",
"lukolszewski" across catalog/memory/watch/docs/corpus (tracked tree, binaries skipped);
"30071" substring hits are numeric noise, none reference the discussion. NEW.

### 2. The Rise of Overfit Inference Engines (r/LocalLLaMA 1wwu6zj, 2026-10-03, 392 pts)
Quote: "Model hash, quant, context range, batch size, and GPU should be part of the artifact,
with an output-parity check before it becomes the default."
Category thread: Strata, ninfer, DwarfStar, Splash, llamAmpere, gufo, Halogen named as narrow
runtimes that "deliberately give up... generality" for one model + one hardware family.
Comment-forest measurements: "I used claude to take strata and port it over to v100, I get
about 1200 prefill and 60 tks" (AI-generated disposable engine ports are now normal); Halogen
(closed-source, telemetry-suspect, some users airgap it) vs gufo (open, "slightly better
speeds on my strix halo") running "4 agents in parallel all using qwen 3.8fn"; kernel-library
counter-trend (HF webgpu-kernels, FlashInfer). The steal is the top-rated governance comment:
specialized engine artifacts must carry their pin set and pass an output-parity check before
becoming default, "otherwise the speedup turns into a very annoying intermittent bug after the
next model swap" - the estate's digest-pinning law (burns.md:102-103 byte-identical sha256)
and replay-verified settlement spec, derived independently by the frontier. Overlap: listed as
a pass-1 candidate twice before (frontier_olm_2026-10-03/sweep/open-and-local-language-models-
reddit.md:85 and frontier_olm_2026-10-04/sweep/kv-cache-and-context-engineering-reddit.md:28)
but NEVER deep-read or banked; sibling threads Strata (1wx1bi1) and Jev (1wx1htr) were banked
10-03. This is the first bank of the thread itself and of the pinned-artifact rule. NEW
(narrowed: the Strata/Jev substance is held).

### 3. Benchmarked the free API tiers you can point a coding agent at (r/ChatGPTCoding 1w34m6p, 2026-08-31 - OUT OF WINDOW, marked)
Quote: "OpenRouter served NVIDIA's own model faster than NVIDIA did, and with a third of the
latency."
The strongest free-lane economics evidence the door surfaced; banked out-of-window per the
day-8 precedent (degraded-door sweeps bank marked older items when they carry the question's
strongest measurement; date is source-shown Aug 31 and the Groq re-sweep comment is later).
Census: DeepSeek 402 Insufficient Balance, SambaNova 402, Together read-only-until-deposit,
Cerebras and xAI card-walls, GitHub Models HTTP 410 (hard EOL July 30, 2026, comment-confirmed
against Google's changelog). Still free, same prompt/500-token cap/temp 0.3/US runner:
Groq gpt-oss-120b ~520 tok/s, Mistral mistral-small ~170, OpenRouter nemotron-3-super-120b
~46, NVIDIA same model 27-100, GLM glm-4-flash ~21. The apples-to-apples pair (same weights on
OpenRouter vs NVIDIA: 2.7 s TTFT at 45.7 tok/s vs 7.6 s at 36.7) plus the loop arithmetic
("Twenty tool calls in a loop and that gap alone is a minute and a half") and the Groq quirk
("Groq's 8000 TPM counts the max_tokens you declare, not what it actually generates" - 413
before one token). Instrument: github.com/build996/free-ai-api-benchmark. Q2: our 469-row
openrouter count is inventory; this measures the drain (and the churn that makes the scout's
daily digest necessary: "these tiers are changing every few weeks"). Overlap: 0 hits for
"free-ai-api-benchmark" and "build996". NEW.

### 4. Thank you, Ollama. DeepSeek v4.1 Flash is the best (r/ollama 1wd8xc7, 2026-09-11, 71 pts)
Quote: "It feels like I can get about 6 times more usage compared to GLM Flash."
Ollama Cloud as a NEW middle rung between free tiers and funded API: hosted open-weights,
off-peak-priced, no-training guarantee. Usage-efficiency arithmetic in the OP (707 requests /
37.5 pct vs 44 / 0.3 pct), contested in-thread ("173 per 1% on DeepSeek, 192 per 1% on glm
5.3 flash" runs the other way on a different mix - the per-plan denominators differ). Speed
100-230 t/s averaging 150-180, later degraded to 40-120 under load spikes from the post's own
traffic, recovering to 124-189. The quota-decay driver: "Slowly every month the usage gets
tinier and tinier. So I ordered more enterprise GPUs" (a hoster), and the new token-burned
plan "chewed through my monthly usage in one week." Q2: the estate's funded-remote rung
(DeepSeek direct / Nous primes) has a hosted-wrapper competitor whose price is plan-denominator
arithmetic exactly like our allowance.jsonl accounting; the in-thread model-name tip
(`deepseek-v4.1-flash:cloud` routes slow, plain name fast) is a free diagnostic. Overlap: raw
rows only (frontier_olm_2026-10-03/sweep/arctic_ollama.json, tmp/candidates_full.jsonl,
tmp/sw2_full.jsonl, frontier_olm_2026-10-04/sweep/_amc_harvest_ollama.jsonl); never banked.
NEW.

### 5. 3 days benchmarking most llama.cpp flags; the MTP multi-GPU bug and the bench-vs-production law (r/LocalLLaMA 1vtc0z7, 2026-08-20 - OUT OF WINDOW, marked)
Quote: "the per-ubatch draft catch-up decode breaks multi-GPU ubatch pipelining"
Measured: 16 to 27 t/s generation, prefill 376 to 573, context 220k to 262k on a 4090-laptop +
7900 XTX TB4 eGPU rig. Spec stack `--spec-type draft-mtp,ngram-map-k4v --spec-draft-n-max 3`
gives +50-70 pct generation but HALVES prefill on any layer split; root cause chased through
four killed theories to a filed bug (ggml-org/llama.cpp#27428); acceptance corroboration of
#26750 ("MTP acceptance collapses on CUDA: 41% vs 64% on Vulkan, same file"). The laws the
estate should copy: "-b 4096: +9% in llama-bench, exactly 0% in the real server. Bench your
production path before adopting anything"; "llama-bench can't measure spec at all"; levers are
workload-share-conditional ("Worth it because my workload is 77% generation time"); a trained
DSpark draft head hit 1-5 pct acceptance from a mislabeled GGUF ("Trained drafters aren't
plug-and-play yet"); free +13 pct generation from a rebuild ("upstream refactors absorbed what
the knobs were buying"). Tool: github.com/kylebakerio/LLM-Tuner. Q1: spec decode on the
janitor tier is real but workload- and topology-conditional; the estate's L2 MTP row
(local-evidence.md:7) should grow a conditions column (single vs split GPU, echo vs reasoning)
before any lane flips it on. The terminal rule is untouched (this is throughput, not refire
policy). Overlap: 0 hits for "LLM-Tuner", "kylebakerio"; 1vtc0z7 absent from all candidate
lists I read; the MTP acceptance numbers extend, and do not duplicate, the 10-04 D5 bank
(DSpark acceptance collapse during reasoning) and the 10-03 kv D2 acceptance ladder. NEW
(marked out-of-window).

### 6. DwarfStar thread: the consumer-economics counterweight (r/ollama 1wx0jtb, 2026-10-03, 132 pts)
Quote: "Yep, correct headline should be: 'DwarfStar compresses frontier models to run them on
expensive local machines'"
The estate intaked DwarfStar on 2026-09-12 via the X door (watch/inbox/INTAKE_XBATCH_20260912.md
row 17: "watch DwarfStar release; hot-expert retention = our organ on someone else's
hardware"). This thread is the Reddit reception delta: the product framing (aggressive
quantization + SSD streaming + deliberately narrow engine, MIT) meets a breakeven fight: M5
Max 128GB at EUR 5,889 vs a EUR 20/mo sub (payback measured in decades at 39.7 tok/s), the
heavy-user counter ("I use between 8-12b tokens a month... At $500mo the Mac Studio then beats
it in monthly cost"), and the sovereignty motives (privacy, "banned Chinese models" hedge,
subscription price risk: "I use $7,000-$11,000mo in API costs on my $200mo Claude plan"). Q2
reconciliation: the thread independently re-derives the day-8 H200 self-host kill (the machine
cannot physically serve the token volume that makes rental beat list price) at consumer scale,
while confirming the rung exists for privacy/price-risk buyers. Overlap: raw-held
(frontier_olm_2026-10-08/sweep/_raw/arctic_comments_1wx0jtb.json, endpoint_news row), intake
row 09-12; the r/ollama thread itself unbanked. NEW (narrowed: product facts held, economics
reception new).

### 7. Sticky-router delta on the banked six-days thread (r/ollama 1wj0arv, 2026-09-17, 27 pts)
Quote: "it costs about 344 ms on every message to catch a case those two buttons already
handle"
The 10-03 kv sweep banked this thread's KV-prefix and memory-injection halves (its item 2).
The unbanked slice is the escalation design, and it is the sharpest routing-ladder measurement
the door surfaced: the sticky router escalates only on a code fence, a pasted stack trace, over
80 words, or a long attachment; conversations stay on deep once escalated; worst case one 4-7 s
swap per conversation; and the optional classifier is OFF by default because of the 344 ms
per-message tax against two manual escape buttons ("Regenerate on deep" / "Wrong, retry on
deep"). Strongest finding: "I've had the deep slot pointed at the same model as fast, because
on 16 GB the swap costs more than the quality gain for most of what I actually ask. Every
routing decision is logged with its reason and the model load time, which is how I noticed."
Q1: the ladder's cheapest rung is not switching at all, and decision logging is what reveals
it; the estate's lane-budget gates already log - the 344 ms number prices what a classifier
gate must beat. Overlap: thread banked (10-03 kv item 2); this comment-level slice is not in
any bank I read. DELTA, explicitly scoped.

### 8. unswallow deltas: the 10 pct recoverability ceiling and the no-draft-head rebuttal (r/ollama 1wc6tka, 2026-09-10, 71 pts)
Quote: "I found it was not the most common cause, and new models did not exhibit this behavior"
The thread is banked (10-03 kv item 2: the swallowed-tool-call class, valid-200 halts,
github.com/0DukePan/unswallow). This session's read adds three banked-adjacent numbers the
prior bank does not carry: (a) an auditor's census that a truly complete, recoverable tool-call
envelope sits in the reasoning field of only "about 10% of thinking-only responses" (the rest
discuss or rehearse a call), which prices any salvage-before-terminal guard at a 10 pct
ceiling and makes false-positive gating the hard part; (b) "75% of my failures were on models
with no draft head", rebutting speculative-decoding as the cause; (c) an AI-posted review
comment demanding recovered calls stay "behind the same argument validation and approval checks
as normal tool calls" with detection-only mode first ("Envelope validity alone doesn't
establish intent"). LENS 2: none of this touches the terminal rule's correctness
(mag/inference_budget.py:349 classifies then never refires same params); it bounds the value
of a recovery probe in front of it at ~1 in 10 hollow turns. Overlap: thread banked 10-03;
these comment-level numbers appear in no bank I read. DELTA, explicitly scoped.

## Research-question synthesis

- Q1 (spec decode + continuous batching vs the ladder, terminal rule intact): the window's
  measured shape is conditional, not unconditional. Spec decode wins on echo-class work
  (n-gram 2-2.5x code rewrites, auto-off beyond two users; MTP +50-70 pct when the workload is
  generation-dominated) and loses on multi-GPU splits (prefill halves, bug filed), on reasoning
  (DSpark acceptance collapse, held 10-04), and sometimes outright (1x023z4: "MTP... slower in
  most cases on this box"). Continuous batching/multi-session serving is the bigger, less
  conditional win (2.3 to 27.3 t/s per session at 250k). Verdict: raise the local rung for
  multi-session long-context scut and echo-class speculation only, with the conditions column
  pinned per the L2 MTP row; nothing here touches the EMPTY_REASONING terminal rule
  (mag/inference_budget.py:349), which operates on refire policy, not throughput. The unswallow
  deltas bound a recovery probe at 10 pct.
- Q2 (frontier benchmarks vs our free-lane row counts): they do not conflict because they
  measure different axes. Commit f80961cd9's openrouter 469 (+7 below-threshold adds), groq 11,
  mistral 46 (verified this session via `git show f80961cd9`) counts INVENTORY; the Reddit
  threads count DRAIN: unfunded openrouter is 50 requests/day (1ue95bf), half the recommended
  tiers are gone or card-walled (1w34m6p), Groq's quota burns on declared max_tokens, TTFT
  dominates agent-loop cost, and provider quotas decay monthly (1wd8xc7). Our concurrency
  envelope (5 gated workflows x max_concurrency 10) is a dispatch-shape law these single-user
  benchmarks never test; the reconcile point is that the estate's drip-not-burst free-lane
  posture and its own counters (allowance.jsonl, usage.jsonl) are the correct instruments, and
  the frontier adds one instrument we lack: cooldown-benching failover that sums every tier's
  limits behind one endpoint (freellmpool, Jun 4, held as lead).
- Q3 (day-8 mine's 32 unbanked sweeps: re-measure order at funded tier): the 32 sweeps are the
  8-area x 4-door set in frontier_olm_2026-10-08/sweep/. Descent leg 3 order for
  inference-efficiency claims: (1) LEG A of the inference-efficiency-hn card, the $0 formal
  prompt-share census over memory/runs/hermes_burn/usage.jsonl and memory/runs/model_garden/
  usage.jsonl (coarse pass already read 80.5/77.4 pct) - it sets the budget priority for the
  six unwired fire surfaces and costs zero premium tokens; (2) the 2610.02267 guard-audit
  discipline from inference-efficiency-arxiv item 3 applied to that census (charge the guard's
  own tokens; 23.9 pct claimed vs 4.3 pct actual is the failure shape to avoid); (3) the Q3
  conditions-suspect DeepSeek off-state re-measure with the day-8 external dollar anchor
  (USD 13,200/mo self-host vs 3,500-7,000 API) as the expected band; (4) a local three-metric
  prefill/TTFT/decode re-measure on the estate's AMD/Vulkan box, per the M4-Max method (banked
  10-03 kv item 7) and this window's 94-97 pct prefill-dominance row; (5) KV-cache card claims
  (Dual-QK/PatchKV) re-verified live by the quant-x sibling but likely non-steal on this box
  (b11465-b11475 deltas proved Metal-specific, burns.md:93-94). The quantization slice of Q3
  was already adjudicated by the 10-09 quantization-compression-x sibling (three cards
  re-verify clean, OnlineQAT banked).
- Q4 (zero-coverage or shelf-held): NOT zero-coverage, and the negative case is countable.
  Catalog greps this session: "speculative decoding" 29 rows + "speculative-decoding" 23,
  "vllm" 157, "sglang" 25, "llama.cpp" 15, "continuous batching" 1, versus ZERO paths for
  biology/web3 (day-9 lens/corpus.md). The shelf holds the canon outright:
  corpus/library/ai-engineering-from-scratch/phases/10-llms-from-scratch/15-speculative-
  decoding-eagle3/docs/en.md and phases/17-infrastructure-and-production/05-eagle3-
  speculative-decoding/docs/en.md (EAGLE-3), 04-vllm-serving-internals/docs/en.md (the
  continuous-batching chapter, 13 matching lines), the lmcache-src mirror (2,331 rows,
  lens/corpus.md:38), docs/ref/VAST_DEEP_GROK_THROUGHPUT.md, plus state/arxiv mirrors of the
  September spec-decode papers (2609.03181, 2609.09338, 2609.09662, 2609.17184, 2609.17241,
  2609.17943). Thin corners: tabbyapi 0 rows, exllamav2 2. The estate's gap is not coverage
  but wiring: the serving-stack canon is on the shelf while the inference-budget guard remains
  unwired in six fire surfaces (lens/laws.md:154-158) - the library answers what exists, the
  ledger answers what we run, and only the ledger moves the driving ladder.

## Overlap instruments (exact commands this session)

- `git grep -ilI "<term>" -- catalog memory watch/inbox docs corpus` (tracked tree, binaries
  skipped, this run's own folder excluded) for: 1x023z4, llama.cpp-multigpu, lukolszewski, 30071,
  GGML_SYCL_FA_DECODE_KERNEL, freellmpool, free-ai-api-benchmark, build996, LLM-Tuner,
  kylebakerio, draft-mtp, 1wwu6zj, Strix Halo, 1wx0jtb, DwarfStar, 1wd8xc7, 1wc6tka, unswallow,
  0DukePan, 1wjnkgm, 1wvxih5, 1wj0arv, RuntimeWire, devbits, ollama-bench, Ollama Cloud.
  First pass without -I inflated counts via catalog/receipt_fts.sqlite and hash-substring
  collisions (e.g. "1wc6tka : 42"); the -I pass plus per-file inspection is the recorded
  instrument. Raw-prior-holdings distinguished from banks by reading the banked-item lists of
  every prior same-area sweep (10-02, 10-03 x2 areas, 10-04, 10-08) - all four cited inline above.
- A first catalog grep used findstr and was abandoned (win32 path mangling under the bash
  shell); the recorded counts above are git grep.
- `git show f80961cd9 --stat` + body grep: verified the free-lane row counts quoted in the ask.
- `sed -n` reads: mag/inference_budget.py:340-360 (guard_terminal), day-9 lens/burns.md:55-80,
  235-250, lens/questions.md:1-30, day-8 steal card in full.

## OWED / not done this session

- Arctic Shift re-probe when the 522 outage clears: it is the only door that enforces the
  30-day window by query parameter; this sweep approximated it with redlib top-month listings
  plus per-thread date stamps.
- r/MachineLearning got only search-level coverage this session (one listing page in the
  census; no deep reads from it). r/LocalLLM similarly thin (its top-month page contributed
  candidates but no bank).
- The v100 6gpu TP2/PP3 thread (r/LocalAIServers, 215 pts, in-window) and the Union Alpha
  2-tier gateway thread (Sep 10, 323) were census-surfaced but not deep-read; both look
  Q1/Q2-relevant. Left for the next window rather than shallow-banked.
- No estate probe was fired (no ledger cut, no pytest); this is a read-and-bank sweep.
- Quote fidelity: all quotes from safereddit redlib renders (raw HTML kept in ie_*.html /
  ie2_*.html); one fetch-layer discount applies as stated in the door record.
