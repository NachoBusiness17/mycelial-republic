# SWEEP: quantization-and-compression via reddit - source-fetched: 2026-10-04

Seat: sweep-quantization-and-compression-reddit (frontier gopher). Window: 2026-09-04T00:00Z
through 2026-10-04T00:00Z (epochs 1788480000 / 1791072000; conversions re-run this sitting with
.venv/Scripts/python.exe utcfromtimestamp after bare python was refused by the seat law).
House laws held: ascii only, no em or en dashes, every claim cites what was fetched or run this
sitting. Sibling sweeps read for dedup before banking: today's
quantization-and-compression-arxiv.md (6 banks) and open-and-local-language-models-reddit.md
(8 banks), frontier_olm_2026-10-03/register.jsonl (42 rows), frontier_olm_2026-10-03/lens/burns.md
via lens/burns.md, lens/questions.md.

## Door scoreboard (all probed this sitting)

| Door | Verdict | Evidence |
|---|---|---|
| old.reddit.com/r/<sub>/top.json?t=month (the recipe door, x4 subs) | DEAD | WebFetch returned the "Welcome to Reddit / Skip to main content" shell for all four subs, zero post fields |
| old.reddit.com JSON + thread pages via the web_reader backend | DEAD | "Log in to use old Reddit" login wall, both the top.json feed and thread 1gqgl0u |
| www.reddit.com/r/LocalLLaMA/top/.json | DEAD | HTTP 403 Blocked (Retry-After: 0) |
| www.reddit.com thread + top pages via web_reader | DEAD | "You've been blocked by network security" |
| r.jina.ai text proxy on an old.reddit thread | DEAD | 500 network error from the proxy itself |
| api.pullpush.io | PARTIAL | /submission/?ids= answered 3 times (1ba55rj, 1cnpul3, and a 7-id batch that dated the candidates); the search endpoint agent-blocked twice ("Rate limit exceeded... does not provide free scraping resources for agents") |
| arctic-shift.photon-reddit.com /api/posts/ids + /api/comments/search | WORKS | full bodies for 9 ids, 15-comment trees for 1whqwdq and 1woxb4n |
| arctic-shift /api/posts/search | WORKS with quirks | after= windows answered; sort_type=score returns 400, sort_type=created_utc works; score> filter 400s; query=quant worked twice, query=EXL3 / imatrix / Schmidhuber / compression 422 or timed out; title= param 422 |
| www.reddit.com/r/<sub>/top/.rss?t=month via WebFetch (sibling recipe) | WORKS paced | r/LocalLLaMA 24 entries, r/LocalLLM 25, r/ollama 21 (one 429 first try, clean on retry after a cool-down) |
| WebSearch site:reddit.com fallback | DEGRADED | returned non-reddit blog noise and repeated "Links: No links found"; used for discovery hints only, nothing banked from snippets |

## Pass 1 - candidates considered

Roughly 130 listing rows screened this sitting: r/LocalLLaMA top-month 24, r/LocalLLM top-month
25, r/ollama top-month 21, arctic newest r/LocalLLaMA 17, arctic newest r/MachineLearning 24,
arctic query=quant r/LocalLLaMA 11, arctic query=quant r/MachineLearning 1, plus 7 older threads
dated (and screened out) via the pullpush ids door. In-window, on-area candidates that survived
the held-set screen: 1wxfdt9, 1whqwdq, 1woxb4n, 1wwipz4, 1wvxih5, 1wvsbck, plus 1wdramg and
1ww6750 at title level. Already-held classes skipped on sight (per lens/burns.md section 6 and
today's sibling files): Jev (1wijo3e + duplicate + moderation thread), Strata class (1wxgwog,
1wxepgu, 1wwamjw, 1wwo3ps; STRATA_DROP_20261001 + 10-03 astroturf bank), iPhone-second-GPU
1wvz1ex (banked by the 10-03 kv-cache sibling per the sibling reddit sweep), ollama release
train, subsidised-compute 1wt5f4e, Bonsai 2 release 1wj6c4l (adjacent to banked 1wjnklv), and
1wt0tot (banked 2026-09-30 by swarm-orchestration-reddit.md item 8; its raw dumps are catalog
rows f2c1c483eb3d, f93b598039d9, aaec554ef5c9).

## Pass 2 - deep reads (7 fetched and read end to end; minimum was 5)

(1) 1wxfdt9 full body (0 comments exist), (2) 1whqwdq full body + 15-comment tree,
(3) 1woxb4n full body + 15-comment tree, (4) 1wwipz4 full body (0 comments), (5) 1wvxih5 full
body, (6) 1wt0tot full body as held-context (not re-banked), (7) 1wvsbck full body.
Extraction caveat, stated once: every body and comment passed the WebFetch/arctic rendering
layer; the one attempt to read raw arctic JSON through the web_reader backend returned a
truncated payload in this seat's view, so no byte-level HTML diff ran. Titles and ids are
byte-verbatim from the arctic/listing layer; long numbers in bodies are fetch-rendered.

## Answers to the five research questions

Q1 (quant-vs-reasoning rungs): the window's strongest new rung is community-measured, not
paper-measured. 1wxfdt9 (r/LocalLLaMA, 2026-10-04T13:12Z) reports a W3 build of Qwen3.8 27B
where only the large projection matrices (about 24.3B params, about 3.1 effective bits per
weight) are 3-bit, rotated then GPTQ-calibrated on roughly 293K tokens, on the same R9700 card
against their MXFP4 build: fetch-rendered pairs are decode 156.1 to 179.7 tok/s, KV capacity
174,634 to 393,216 tokens, GSM8K 95.68 to 95.22, HumanEval 95.12 to 94.51, MMLU-Pro 62.57 to
60.57 with a paired-question CI of -4.8 to -0.9 naming MMLU-Pro the only beyond-noise loss; the
author's own summary is that 2-3 MMLU-Pro points buy 15 percent speed and 2.25x cache. This
does NOT contradict the banked W3 rungs (RATIO 2609.39801's 2.94-3.77x CoT inflation was
1.5B-class; 2609.26708's sub-3-bit retention was about 2-bit-class with exposure-bias failure):
it sits between them, a 27B partial-stack W3 that holds math/code and pays knowledge recall,
which is the asymmetric-cost shape banked as 2609.06473. The exposure-bias signature (loop
degeneration) was not observable in-thread; that diagnostic stays armed for probe 5.
1whqwdq (r/LocalLLM, 2026-09-16) is the 30-day agentic arm: Unsloth UD-Q4_K_XL daily coding,
reasoning tokens up to half the context, "poisoned tool calls" loops suspected at 100K+
context, Dflash2+ngram measured 20 percent faster than MTP+ngram on their rig. 1wwipz4
(2026-10-03) decomposes the NVFP4 speed story: stock Q4_K_M 68 t/s jumps to 141 with MTP, so
"a big part of the 'ninfer is fast' story is really 'MTP is fast'", and the quality check found
only the NVFP4 build's game legally winnable (single runs, author-flagged). 1woxb4n (2026-09-24)
is the live dispute: OP claims NVFP4 Q4 matched Q8 quality; the top commenters disagree ("the
eye test feels like base q8 is smarter by a good margin"), one measured groupwise-int 10
percent slower than nvfp4.

Q2 (KV quant bounds): 1wvsbck (2026-10-02, 55 pts/44 cmts) states the community bound
verbatim: "K cache should *never* be below q8 unless youre running on less than 80k context",
with V cache tolerating q4 to roughly 150k and q8-for-both as the default. 1wxfdt9 stacks
weight-W3 with a 4-bit KV mode and reports math/code within paired noise, MMLU-Pro paying the
bill: the stack bound is not violated by 4-bit K on this model at 262K context, but the loss
channel moved to knowledge recall. Held context that corroborates the K-side floor: 1wt0tot's
400-agent production stack runs q8_0 KV over Q4_K_M weights (banked 09-30), and the register
holds 2609.04098 (FP8 KV with calibrated scales, 83 percent penalty recovery) and 2609.36760
(INT2-content/INT4-RoPE, RoPE the fragile half). Net: the ladder may stack to weight-W3 plus
KV-q4 for math/code work, but K below q8 under 80k is the only explicitly community-bounded
regime, and nobody in-window measured weight-4bit plus KV-2bit on a reasoning model.

Q3 (compression-as-progress lineage): the reddit door is empty in-window. Two arctic query=
attempts (Schmidhuber, compression) 422'd or timed out, the one WebSearch pass returned nothing
reddit-side, and the only compression-represents-intelligence reddit threads found are 2024
(1c76tpe and siblings), out of window. The estate's Q3 evidence base was already extended
TODAY by the sibling arxiv sweep (2606.11417 Goodhart-on-own-stream and 2607.18433 closed-form
learnable novelty). One cross-door lead sighted, NOT banked by this seat:
"Efficient Exploration Is Enough" (arxiv, dated Sep 7, 2026 in search results) cites
Schmidhuber 2008 compression progress as the intrinsic objective; the arxiv sibling should
claim it if it survives their screen. Verdict for the percolator's curiosity-scored
lane-selection candidate: reddit adds nothing this window; the sibling's two papers already
supply both the estimator and the Goodhart constraint.

Q4 (janitor-fleet format choice): community measurement ranks IQ4_XS above Q4_K_M on
quality-per-size (1wvsbck principle claim; the llama-roofline result cited in search puts the
whole 4-bit class within 4 percent on a Pi 5 with IQ4_XS winning energy-quality), and ranks
UD/dynamic quants above stock at 27B (1whqwdq's month on UD-Q4_K_XL). The ranking is NOT
stable across hardware: 1wvxih5 (M4 Max) measures NVFP4/MLX at 40-41 t/s versus 10.7 t/s for
GGUF Q4_K_M (3.8x) with the same q8_0 KV, and the banked 2609.14864 already showed Q4 beating
Q8 1.29-1.49x everywhere but IQ2/Q2 order flipping between Apple and RTX. Nothing in-window
measures gemma-family quants specifically, so the janitor fleet's own family stays unranked by
this sweep (OWED). The harness-not-intelligence finding recurs: 1whqwdq's comment tree carries
"local models seem less limited by raw intelligence and more by whether the harness can keep
them from wasting their context or getting stuck in tool loops", which lands directly on
probe design: grade the loop-detector, not just the quant.

Q5 (shelf seeds): the corpus today holds lmcache KV docs and zero quant-literature rows
(catalog greps this sitting: quant/gguf/awq/gptq/exl2/exl3/kv-cache/compression hit only
incidental infrastructure files). First-row seed set this sweep nominates: the six banked
community threads below (each carries a reproducible A/B or a stated bound), the ExLlamaV3
eval/compare_q.py PPL/KLD harness (surfaced in search results via an HF model-card mention,
not fetched this sitting), the ik_llama.cpp IQ_K discussion (IQ4_K claimed 2.7x lower error
than Q4_0, snippet-level only, UNVERIFIED), and the sibling arxiv six already banked today.

## Banked finds (6, strongest first)

1. 1wxfdt9 (r/LocalLLaMA 2026-10-04): the measured W3-plus-KV4 rung. Title verbatim from the
   arctic layer: "Qwen3.8 27B | 1 x R9700: 262K context, half a million tokens of reusable
   cache, ~180 tok/s. And yes, let's talk about the '3-bit' :)". Body numbers fetch-rendered:
   +15 percent decode, 2.25x cache, GSM8K/HumanEval within paired noise, MMLU-Pro -2 to -3
   (paired CI -4.8 to -0.9). Fills the ladder's W3 rung at 27B partial-stack and arms probe 5's
   diagnostic channels. Overlap: greps "1wxfdt9" and "long-kv4" = 0 in catalog.jsonl and
   memory/ (own-session trajectory echo only); absent from register rows 1-42 and both sibling
   banks today.
2. 1whqwdq (r/LocalLLM 2026-09-16): the 30-day UD-Q4_K_XL agentic arm; reasoning up to half
   the context, "poisoned tool calls" at 100K+, Dflash2+ngram +20 percent over MTP+ngram;
   comments add 16GB IQ3/IQ4 full-GPU at 200K+ context via KV-history offload (wangleye) and
   "The *MTP* draft does contribute to incorrect token outputs" (HenkPoley). Overlap: greps
   "UD-Q4_K_XL", "poisoned tool calls", id = 0/0.
3. 1wvsbck (r/LocalLLaMA 2026-10-02): the KV bound ("K cache should *never* be below q8 unless
   youre running on less than 80k context", V to ~150k at q4) plus IQ4_XS-over-Q4_K_M ranking
   and the warning that search engines misanswer custom-quant questions. Overlap: title and id
   0/0 in catalog/memory; sighted only in the 10-03 raw listing dumps (sw2_full.jsonl,
   arctic_*.json), never banked.
4. 1wwipz4 (r/LocalLLaMA 2026-10-03): MTP carries the speed story (68 to 141 t/s), NVFP4 only
   build with a legally winnable game, "For reasoning models I'd look at time-to-result, not
   just t/s" - the wall-clock law for any ladder A/B. Overlap: id 0/0; "ninfer" catalog hits
   are openInference false friends (arize phoenix docs).
5. 1wvxih5 (r/ollama 2026-10-02): M4 Max, NVFP4/MLX 3.8x over GGUF Q4_K_M at q8_0 KV; TTFT
   cliff (3m15s at 30K, 21 min wait at 115K with decode down to ~14 t/s) while 4/4 integrity
   checks still pass: capacity is not occupancy, and format ranking is hardware-bound.
   Overlap: id 0/0; related register row 21 (2609.14864) is a different artifact.
6. 1woxb4n (r/LocalLLM 2026-09-24): the NVFP4 quality dispute (OP Q4=Q8 vs commenters' q8-smarter
   eye test and groupwise-int 10-percent-slower measurement). Overlap: id 0/0; NVFP4 held at
   register rows 23/38 (arxiv 2609.04098), engine thread not previously held.

## Sighted, NOT banked

1wt0tot (held, 09-30 bank, quant stack cited above as held context); Strata class (banked
class); 1wj6c4l Bonsai release (banked claim's sibling thread); DwarfStar 1wx0jtb and 1ww6750
DFlash2 (title-level only, bodies not fetched); out-of-window threads dated via pullpush and
screened: 1v9cnd9 "Thank you, whoever said don't quant the KV" (2026-07-28, 380 pts, the
strongest public KV-degradation anecdote, predates the window), 1vsmrwn (2026-08-18),
1vu8atq (2026-08-20), 1vsjcf7 (2026-08-18), 1s812cs (2026-03-29), 1p8p844 (2025-11-27);
"Efficient Exploration Is Enough" arxiv lead (cross-door, left to the arxiv sibling).

## OWED / not run

- EXL2/EXL3 community ranking in-window: arctic query=EXL3 422'd/timed out both tries; today's
  arxiv sibling's EXL2/EXL3 OWED (their file, "OWED / not run") stands unmet.
- The 1wxfdt9 body numbers are fetch-rendered; a byte-level selftext diff against raw arctic
  JSON did not run (raw fetch truncated in this seat's view).
- r/MachineLearning quant coverage in-window is effectively empty: query=quant returned one
  post (AIStats 2027 Questions), the newest-first listing returned zero on-area titles.
- No probe fired this sitting: the reasoning-quant ladder (percolator row 7) and probe 5
  (qwen2.5:7b Q4_K_M vs q8_0) stay armed, not run. The 1wxfdt9 paired-question design and the
  1wwipz4 time-to-result law are the two design inputs this sweep contributes to them.
- gemma-family quant rankings (the janitor fleet's own family): nothing found in-window.

## ERRATUM (same sitting, post-submit instrument delta)

The overlap greps for the six banks ran twice and the two instruments disagree: the foreground
`rg -l -i -F <anchor> memory/` (gitignore-aware) reported NONE for every anchor, while the
slower background plain `grep -r -c -i -F` (sees ignored dirs) found pre-existing memory hits
for exactly one banked anchor, "UD-Q4_K_XL" (5 files: memory/runs/corpus_selfsteal/INDEX.json
x4, memory/runs/compaction_eval/steps_frozen_20260920.jsonl:8344, a binary-flagged
quote_audit concat, and own-session echoes in memory/thinking/app_reasoning.jsonl). Inspected
this sitting: the INDEX entries are model-name metadata ("deepseek-v4-flash-ud-q4_k_xl",
"ud-q4_k_xl"), the compaction_eval hit is a GGUF filename inside a disk-walk bash command, so
none is a holding of thread 1whqwdq; the submitted overlap claim "0 in memory/" was true of
the rg instrument only and is hereby downgraded to "no holding hits; metadata-string hits
under grep -r, none substantive". The NInfer memory hits (biography/ingest) were also
inspected and are all openinference substring false friends (arize-ai spec pages), matching
the catalog class already recorded. The submitted SweepResult JSON is append-only and was
already accepted when the background grep landed; this section is the durable correction.
