# Sweep: quantization-compression via reddit (frontier OLM adhoc, run 2)

source-fetched: adhoc - swept 2026-10-11 by the quantization-compression-reddit gopher (arctic-shift archive door).
Supersedes-but-preserves: the prior sibling sweep at `quantization-compression-reddit.v1-20261010-preserved.md` (different ask generation: PullPush door, April-July 2026 out-of-window deep reads, QuantOne/EvalShift steal list). Its findings remain valid banked work; nothing here contradicts them, and the two runs are complementary (v1: 2026-04..07 threads; this run: strictly last-30-days).

## Door status (all attempted this run, no fabrication)

The recipe's primary door is walled exactly as doors.md:52-60 warned:

- WebFetch `old.reddit.com/r/*/top.json?t=month&limit=50` on all four subs (LocalLLaMA, MachineLearning, LocalLLM, ollama) returned only Reddit's welcome banner, zero listing data.
- WebFetch `old.reddit.com/r/LocalLLaMA/top/?t=month` (HTML): welcome page only.
- curl `old.reddit.com/.../top.json`: HTTP 302, follows to `old.reddit.com/login/?reason=lor2` (login wall, 200 on the login page).
- curl `www.reddit.com/.../top.json` with browser UA: HTTP 403 (block page, 189908 bytes).
- mcp web_reader on the JSON feed rendered "Log in to use old Reddit" ("To keep Reddit safe, accounts are required to access old Reddit").
- pullpush.io: HTTP 429 "This website does not provide free scraping resources for agents" (hard no; note the v1 sweep reached its ids= endpoints - now blocked).
- redlib mirrors: safereddit.com = "Verifying your browser" JS challenge; redlib.perennialte.ch 403; l.opnxng.com 302 with 0 bytes; reddit.nerdvpn.de serves the "Gandalf" anti-bot page; catsarch/bloat.cat/artemislena/privacyredirect = connection failed (HTTP 000).

WORKING DOOR (the degraded-door substitute this run): the arctic-shift.photon-reddit.com public archive API (`/api/posts/search?subreddit=...&after=<epoch>&limit=100&sort=desc` and `/api/comments/search?link_id=...`). It returned full submission records (title, score, num_comments, created_utc, author, full selftext) and full comment trees, so this run achieved a true month-scoped enumeration plus end-to-end thread reads that v1 could not. WebSearch with allowed_domains=reddit.com was used only as a secondary cross-check (its `site:` operator is ignored by the underlying engine; noted, not relied on).

## Pass 1 - census (30-item floor: cleared 14x)

`_pager.py` collected 1638 submissions from the last 30 days (after=1789152920): r/LocalLLaMA full window (800) plus title-keyword slices (quant/GGUF/Q4), r/LocalLLM full window (800), r/ollama quant (3), r/MachineLearning quantization (0). `_filter.py` scored quant/compression relevance and produced 435 quant-relevant candidates (strong keyword hit in title+selftext). Census JSON kept at `_census.json` in this directory.

## Pass 2 - deep reads (banked only what was read)

Ten posts read end-to-end (full selftext) plus three comment trees via the comments API (42 + 13 + 8 comments): 1wyui4o, 1x357dq, 1wgszma, 1wyeanf, 1wi87us, 1whpqhf, 1x2wijv, 1wxqoa3, 1x1dt7q, 1wyc2b0. All inside the last 30 days (2026-09-15 to 2026-10-11), unlike v1. Eight banked below; near-misses at the end.

## Overlap checks (commands run this session)

`grep -ril` over `catalog/catalog.jsonl` and `memory/` for each distinctive phrase ("voodoo", "uniform GGUF", "Kolibri", "Sakura-MicroQuality", "GSQ-RCO", "ISTA-DASLab", "IQ3_XXS", "UD-IQ4_XS", "MXFP4", "pelican riding", all ten post IDs, "RCOL", "GGUF quant should you actually") returned zero hits (the lone "RCOL" hit is a binary .mp4 filename in memory/corpus/kungfu/, a false positive, not a holding). The same phrases over `memory/corpus/quantized_thought/`, `corpus/steal/CORPUS_FOLD_FRONTIER_OLM_20261001.md` and `CORPUS_CATALOG.md` returned zero hits. The catalog holds 91 r/LocalLLaMA-mentioning lines but none of these works. ONE subject-twin exists: catalog.jsonl already carries "Why Gated DeltaNet Survives 4-Bit Quantization: NVFP4 W4A4 for the Recurrent Half of a Hybrid 27B LLM" (2 lines). That is the arXiv-side *survives* claim; banked item 1 is the independent consumer-side *fails* report. Complementary, not duplicate; flagged in that item's overlap line. No overlap with v1's six threads either (different IDs, different window; v1's items predate this census window).

## Banked items (strongest first)

### 1. Uniform GGUF quants silently break Qwen3.8-27B's deep thinking - reproduced on llama.cpp AND vLLM (short tasks unaffected)
https://www.reddit.com/r/LocalLLM/comments/1wyui4o/uniform_gguf_quants_silently_break_qwen3827bs/ - 2026-10-06, 13 comments (tree read).
The banked stratification law, found independently from the consumer side: uniform-integer GGUF quants (even careful 6-bit dynamic ones) keep short-task and chat behavior intact while long-horizon thinking diverges (tail-loops, non-termination) on the Gated DeltaNet hybrid; mixed-precision NVFP4 (FP8 attention/GDN + FP4 MLP) converges in about 17K tokens on the same prompt. "The quant structure matters more than the average bits." The comment tree adds an independent repro at 40K tokens on Q6_K_XL summarization and sharp pushback ("UD quants are anything but uniform", a Q8-KV counterexample run), and the OP re-verified with programmatic SVG-palette diffs. A falsification recipe is included: keep GDN projections at f16/q8 via `--override-tensor` while MLP stays 6-bit. This is the exact shape of the estate's induction-vs-retrieval split: one capability mode retained, the other silently collapsed, standard evals blind to both. Feeds RQ1 (fire the janitor battery as a long-horizon convergence canary with zero scoring infra) and RQ2 (the lore arXiv missed: the failure mode, not the perplexity table).

### 2. Standard evals can't tell my local quants apart. My own agentic bench can (Qwen3.8 27B / Flash-Next, Q3 to Q8)
https://www.reddit.com/r/LocalLLaMA/comments/1x357dq/standard_evals_cant_tell_my_local_quants_apart_my/ - 2026-10-11.
Five quants of the same model score within 2 pts on GSM8K/MMLU-Pro/IFEval while differing 1-in-28 on top-1 token choice; only KLD/top-1 agreement orders them, and only a certified agentic bench (AST-mutation-injected bugs, hidden tests, 112 runs per model, paired McNemar) separates models (77% vs 98%; SWE-rebench 69% vs 82%, p about 0.007). A ~3-bit GSQ-RCO IQ3_S run locally matches the 4.5-bit NVFP4 on 11 of 12 discriminating tasks and misses one specific bug every single time: a deterministic sub-4-bit failure mode, not a score dip. This is the ready-made design for the fold's named-but-unfired janitor induction/retrieval battery (RQ1) and the headroom map above the closed ceiling tie (RQ5): saturation on standard evals is why the estate's re-run must be agentic with paired stats, not perplexity.

### 3. Voodoo Dynamic Quant - Now MIT Licensed
https://www.reddit.com/r/LocalLLaMA/comments/1wgszma/voodoo_dynamic_quant_now_mit_licensed/ - 2026-09-15, score 328, 42 comments (tree read).
First open method to pick per-tensor quant levels by gradient descent (all quant levels live at once, one scalar gate per tensor per level, tau-annealed freezing, KLD-vs-BF16 loss plus a filesize target). The author reports it beating Unsloth Dynamic at aggressive levels; the comment tree carries the ecosystem reaction: bartowski (noneabove1182) says GD selection is not incorporable at 3090 scale, and stoppableDissolution reports a parallel KL-loss attempt on gemma 31 costing about 40 min per step at batch-128 on a 6000 Pro: direct difficulty data for pointing this at the estate's janitor fleet. Repo: github.com/curvedinf/voodoo-dyn-quant. Feeds RQ5 (sub-4-bit scheme with measured KLD gains) and RQ1 (a way to build gemma:2b/gemma4 quant ladders with per-tensor budgets).

### 4. I squeezed Kolibri-1 78B-A3.5B to 20.9 GiB / 2.30 bpw - 59% lower KL than standard IQ2_XS
https://www.reddit.com/r/LocalLLaMA/comments/1wyeanf/i_squeezed_kolibri1_78ba35b_to_209_gib_230_bpw_59/ - 2026-10-05.
A sub-2.5-bit MoE GGUF at 90.5% top-token agreement (vs 84.6% for standard IQ2_XS) via tensor/layer sensitivity bit allocation, measured against a near-lossless Q8_0 reference; plus a second compression lever: routing-statistics expert pruning (19 least-used experts per layer, 0.07% of selections, 375 of 950 pruned experts never selected at all, no retraining, top-6 routing unchanged). Feeds RQ5: compression headroom beyond bits, exactly the headroom above the closed ceiling tie the ask wants, with a falsifiable usage-stats protocol.

### 5. I retrained only the fp16 block scales of ISTA's 3-bit Qwen3.8-27B GGUF against the BF16 parent
https://www.reddit.com/r/LocalLLaMA/comments/1wi87us/i_retrained_only_the_fp16_block_scales_of_istas/ - 2026-09-16.
Post-hoc scale-only recovery (EfficientQAT phase 2 applied to an existing file: same codes, same bytes, same offsets, 300 steps of top-64 forward KL on 0.6M tokens) moved KLD 0.0480 to 0.0450 with paired CI [-0.0098, +0.0038], claimed as "inside the bar" and "a consistent direction with an unresolved magnitude", NOT "better", and did not move HellaSwag (+0.10 [-0.30, +0.50]). The discipline line is the steal: "Fidelity and benchmark equivalence are different quantities." That is the reddit-side answer to RQ3's shape (what a measurement row can and cannot carry): a KLD delta with an honest interval carries no task-quality decision force, and the author refuses to let the table imply it.

### 6. Qwen3.8-Flash-Next on an RTX 5090 + 128GB RAM: IQ3_XXS vs IQ3_S vs UD-IQ4_XS - Speed and Accuracy with Strata
https://www.reddit.com/r/LocalLLM/comments/1x2wijv/qwen38flashnext_on_an_rtx_5090_128gb_ram_iq3_xxs/ - 2026-10-11.
The cleanest 2026 sub-4-bit ladder measurement in this census: ~3-bit IQ3_XXS is the FASTEST at every context length (193.8 tok/s at 4K up to 192.4 at 128K vs UD-IQ4_XS 116-120), all three quants pass 12/12 basic functional checks including JSON and instruction following, all three pass exact needle recall at 125K-248K, and all three FAIL the count-130 repeated-sentences check identically (answered 100): a quant-independent long-horizon failure identical in shape to item 1's canary. RQ5: structured-output reliability holds at ~3-bit on this family; the repetition/recall split is the battery.

### 7. GLM-4.7 benchmark compared MXFP4 vs Q4_K_M vs Q4_K_XL using Radeon 6800H iGPU 680M
https://www.reddit.com/r/LocalLLaMA/comments/1wxqoa3/glm47_benchmark_compared_mxfp4_vs_q4_k_m_vs_q4_k/ - 2026-10-04.
Quant-on-current-box lore for the GPU-ladder rib (laws.md:50): on an iGPU with no native FP4 (`fp4: 0`), MXFP4 still wins prompt processing (258 vs 218 vs 160 t/s) while Q4_K_XL wins generation (13.13 vs 12.09 vs 11.66 t/s): the format choice flips by workload phase on bandwidth-starved hardware. Also a metadata honesty note: llama-bench reads the GGUF header (deepseek2 30B.A3B) over the filename's "GLM-4.7" claim.

### 8. Which GGUF quant should you actually use with Ollama?
https://www.reddit.com/r/ollama/comments/1whpqhf/which_gguf_quant_should_you_actually_use_with/ - 2026-09-16.
Janitor-fleet serving-path guidance (the estate's janitors are ollama-served): default Q4_K_M for chat, RAG and tool calling; Q5/Q8 only for precision-sensitive work; and the stratification-relevant rule that a 3B model at Q4_K_M usually produces more reliable responses than a 7B model forced into Q3 or Q2, i.e. prefer model-size down over quant down, the practical form of the banked induction/retrieval split for the gemma:2b tier. Vendor-affiliated (Actian) and general-audience, hence ranked last.

## Near-misses (read, not banked; free for a later fold)

- 1x1dt7q "Release: Qwen-2B-RCOL Dynamic Low-Bit Quantization (IQ1_M, IQ2_M, IQ3_M)": an RCO-variant with KLD wins at 1-2 bit on a 2B (janitor-tier) model; HF trubisky/Qwen3.5-2B-RCOL. Dropped only because items 3, 4 and 6 already cover scheme-level lore with stronger measurement discipline.
- 1wyc2b0 "4-bit Qwen2.5 that stays closer to fp16 than the official AWQ": grid-fitted GPTQ packing into the AWQ format; honest that at 3 bits it "loses more than half of code and math ability" (another stratification datapoint). Comment pushback: Qwen2.5 is dated.
- 1wtv43r (score 152) ISTA GGUF 12GB-VRAM thread and 1x1emib NVFP4 daily-driving telemetry: engine-strategy items, quant-adjacent only.

## Answers to the research questions (what this sweep adds)

- RQ1: The stratification law holds independently in community data, with a cheaper instrument than the fold's battery: a long-horizon convergence canary (item 1) plus a certified mutation bench (item 2). The battery to fire on gemma:2b/gemma4 = termination/convergence checks plus hidden-test agentic tasks at each quant step with paired stats; perplexity-class evals provably cannot see Q3-to-Q8 differences (item 2) and miss the collapse mode entirely (item 1).
- RQ2: The census floor is cleared with 435 candidates from the last 30 days (1638 submissions paged); the lore arXiv missed is: (a) capability-mode-specific silent failure under uniform quant (item 1), (b) KLD-vs-task-equivalence discipline (items 2 and 5), (c) open GD quant-layout search and its cost curve (item 3), (d) expert-routing pruning as a second lever (item 4).
- RQ3: The reddit analog says a provenance/fidelity row does not carry task decision force and must not be worded as if it did (item 5's paired-CI refusal). By the estate's own law (path:line receipts as the only carrier, laws.md:114) the 24 provenance-only rows stay non-decisional; this sweep's receipts are the fetch commands and archive JSON in this directory.
- RQ4 (sovereign isolation): no banked item demonstrates a quantized serving path refusing cloud fallback; the closest signal is negative-space (Strata/llama.cpp/vLLM local stacks throughout, no cloud-fallback claims tested). Not answered by this area; OWED to the sovereign-isolation area.
- RQ5: sub-4-bit schemes with 2026 structured-output evidence: GSQ-RCO ~3-bit (item 2: 11/12 agentic parity; item 6: 12/12 JSON checks), IQ3_XXS (item 6), sensitivity-allocated IQ2_XS at 2.30 bpw (item 4), GD dynamic layouts (item 3); counter-evidence: 3-bit GPTQ losing more than half of code and math ability (near-miss 1wyc2b0), and long-horizon repetition failing at ALL quant levels including Q8 (items 1 and 6): the ceiling is capability-mode, not bits. This converges with v1's Q3_K_M refusal-collapse finding (1upc6md): below Q4 the failure is capability-mode-shaped, not score-shaped.

## Receipts

- Census: `_pager.py` produced `_census.json` (1638 submissions, arctic-shift API, after=1789152920).
- Filter: `_filter.py` produced 435 candidates ranked by strong-keyword hits then score.
- Comment trees: `_comments.py` produced `_comments_1wgszma.json` (42), `_comments_1wyui4o.json` (13), `_comments_1wyc2b0.json` (8).
- Door-recon artifacts: `_probe_*.html`, `_probe2_*.html`, `_raw_*.json` in this directory.
- Overlap greps as named in the Overlap checks section, run against `catalog/catalog.jsonl` (326 MB, 540 lines matching 'quant') and `memory/`.
- Prior-sweep preservation: `mv quantization-compression-reddit.md quantization-compression-reddit.v1-20261010-preserved.md` before writing this file.
