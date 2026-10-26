# SWEEP: quantization-compression via reddit - 2026-09-30

Stamp: source-fetched: 2026-09-30. Seat: sweep gopher (quantization-compression, reddit door). Estate map: feeds percolator auto_quantize + the deliberate-ask law.

## Doors (honest ledger)

- `old.reddit.com/r/*/top.json` (the recipe's primary door): DEGRADED. WebFetch and curl both land on the logged-out "Welcome to Reddit" login-redirect stub (`?reason=lor2`), verified 3x.
- `old.reddit.com` thread HTML: DEGRADED, same stub (tested on 1o3r6et).
- `www.reddit.com/*.json` via curl + browser UA: 403 network-policy block, verified.
- `r.jina.ai` text proxy: upstream Reddit 403, verified.
- `api.pullpush.io`: worked twice (comment reads for 1uwnhlv, 1rgel19; submission dates for 9 ids), then went hard 429 with "This website does not provide free scraping resources for agents." Not hammered further (ox-alpha law).
- **WORKING DOOR: Reddit RSS.** `https://www.reddit.com/r/<sub>/search.rss?q=quant&restrict_sr=on&sort=top&t=month` and `https://www.reddit.com/r/<sub>/comments/<id>.rss?sort=top` return 200 with full Atom XML (selftext + comment bodies) to curl with a browser UA. This door recovered the native last-30-days slice. r/LocalLLaMA + r/LocalLLM + TAK comments pulled; r/ollama and r/MachineLearning RSS 429'd on the same burst (reddit throttles per-IP with short windows) - noted, not retried that minute.
- WebSearch (z.ai web_search_prime): rate-capped in bursts; worked serially with 60-90s gaps. It surfaced mostly older threads; the RSS door is what actually satisfied the last-30-days constraint.

## Pass 1 census (candidates considered, last 30 days unless noted)

From RSS month feeds (in window): 1wj3s31, 1wg7dd5, 1wmb875, 1wp0z3i, 1wqcrly, 1wgszma, 1wn2ybk, 1wp7zyb, 1w7ee1c, 1wp6gal, 1wl56g2, 1wnxm0r, 1wmgokc, 1w75rp4, 1wb7p70, 1wt7e94, 1wj4qj4, 1wa5dp9, 1wgiefk, 1wtvx1g, 1w6ccgs, 1w44jnv, 1w4mevo, 1wf4yqe, 1wjwxeq, 1w2uccy, 1w3vts8, 1wabrlq, 1wpza1i, 1w53inj, 1w61u7t, 1w8bj0o, 1wje0ke, 1wmllbx, 1wixlzd, 1wcywae, 1wnmep7, 1wojbs4, 1wrjzye, 1wplw7v, 1wkxlg6, 1w6najp, 1wdkbpu, 1worbst, 1wg0jax. Plus search-surfaced (mostly outside window, considered and dated out): 1uwnhlv (07-14), 1udhvcv (06-23), 1td6nxk (05-13), 1scucfg (04-02), 1rgel19 (02-27), 1pxm29c (2025-12-28), 1o3r6et (2025-10-11), 1rkyrja (03-2026), Red Hat 500k-evals, arXiv:2410.14766, Spheron 2026, Ginger Labs, ionio, jarvislabs, kaitchup Qwen3.5 analysis, unsloth docs x2. Total considered: 55+. The window-only subset is itself 45; the 30-candidate floor is met with room to spare.

## Pass 2 deep reads (read end to end this session)

1. TAK self-post 1wa5dp9 (raw RSS content field, parsed myself) + 26 top comments (comments RSS, parsed myself).
2. Opti 27B 1wje0ke full selftext incl. the pre-registered agent test, license, and reproduce-command blocks.
3. Voodoo Dynamic Quant 1wgszma full selftext (methodology disclosure).
4. 21-variants benchmark 1w7ee1c selftext + 9 edit rounds.
5. FP4-stop 1wl56g2 full selftext incl. the Q4-anatomy edit.
6. unofficial quant tests 1w6najp selftext (part 1 of ranked list).
7. Kaitchup Q4-to-Q1 1w4mevo selftext.
8. IQ3_S-coding testimonial 1w2wdlc (2026-08-30, one day outside window; read for context, not banked as window item).
9. pullpush: 1uwnhlv comments (1-bit consensus; 2026-07-14, outside window) and 1rgel19 comments (Qwen3.5 Unsloth thread; 2026-02-27, outside window; Phaelon74 NVFP4 KLD numbers + Doomslayer606 loop report came from here).
10. unsloth.ai/docs/models/qwen3.5/gguf-benchmarks and unsloth.ai/docs/basics/dynamic-3.0-ggufs (fetched via WebFetch, extractor-mediated quotes marked below).
11. developers.redhat.com 500k-evals article; arxiv.org/abs/2410.14766 abstract page; spheron.network 2026 GPTQ-vs-AWQ-vs-GGUF post.

## RQ1 - measured quality retention at janitor-class scale on held-out evals

The window's strongest measured claims, all task-eval-based rather than PPL-only:

- **Opti 27B** (Qwen3.8-27B, 3.47 bpw, 11.8 GB): wikitext-2 PPL 6.487 vs 6.456 FP16 (1.005x) AND a task ladder: MMLU-Pro 53.9 +/- 0.5 (12,032 q), plus a pre-registered agent test (one coding task, 37 hidden tests, 100 runs on 10 GPUs, paired per GPU): 40% vs 12% perfect solutions vs IQ2_M (p=0.0026), 72% vs 48% passed. Paired per-window vs Q4_K_M: "+0.4% +/- 0.5%, not distinguishable, at 29.5% fewer bytes." Decontamination named: training text scrubbed against the wikitext-2 test split by 10-word n-gram overlap. Honesty field: "KL to FP16 logits: not run yet."
- **TAK** (core already held, see overlap): 27B 2-bit-class task-aware quant 82.81% reasoning vs 77.34% byte-matched Unsloth UD-IQ2_S and 83.59% BF16, i.e. 99% of BF16 at 15% size, on a held-out set; new this session: independent in-thread replication by peculiar-ragdoll (task-aware imatrix for agentic coding on Ornith 35b-a3b, "benchmarked on out-of-corpus agentic coding tasks from after training cutoff it holds up!").
- **21-variant practitioner benchmark** (1w7ee1c): held-out set is the author's actual C codebase on RTX 5080/16GB; 21 GGUFs ranked across 9 edit rounds incl. ternary Bonsai Q2_g64, AWQ-int4-converted GGUF, MQ-IQ2_M_1; winner IQ4_XS.
- **Unsloth Dynamic 3.0 docs**: "Divergence-300 @32" = 300 held-out examples NOT in calibration (sourced from Terminal-Bench 2.1 + DeepSWE + Harbor + MathArena 2025-26 + non-Latin/long-doc prompts), greedy 32-token trajectory divergence vs BF16; UD-IQ1_S 6.2GB retains "around 72% top-1 accuracy yet being 89% smaller"; below UD-Q2_K_XL 32-token accuracy drops to "under 8-10%" and tool calling/agentic breaks.
- Held over from the 09-28 bank (do not re-derive): Quesma's Qwen3.8-27B ladder (Q4_K_M matches BF16 on GPQA/Terminal-Bench; 1-bit collapses) and Red Hat's 500k-eval result (Llama-3.1-8B: 8-bit recovers 99.9% / 4-bit 98.9% on HumanEval+; published Oct 2024, still the best large-N janitor-class citation).

Net: at 27B (the janitor workhorse class) the 2026 picture is 4-bit = no measurable loss on held-out task evals; 3-bit near-lossless with the right dynamic layout (Kaitchup: UD Q3_K_XL 100% accuracy at 12.8GB; community IQ3_S testimonials); 2-bit survivable ONLY with task-aware/held-out-verified allocation (TAK, UD-Q2_K_XL with presence_penalty=1.5 mitigation); 1-bit aggregate claims (~72-77% top-1) coexist with task-level collapse (Quesma, held). Aggregate accuracy is not task survival.

## RQ2 - do auto_quantize's 4 invariants survive the five-axis test?

The 4 invariants (from `memory/knowledge_graph.json` module:auto_quantize.py node, matching `mag/auto_quantize.py:21-24`): (1) SCHEMA auto_quantize.v1; (2) "Anomalies are NEVER quantized. Keep raw forever."; (3) "Variance determines resolution. Low variance = high compression."; (4) "The chain root is always recoverable from any quantization level."

- **Invariant alignment gate (axis 1, laws.md:34 passes first):** INV2 is not just surviving, it IS the field's 2026 frontier mechanism: TAK's knapsack, Voodoo's gradient-trained per-tensor scalar gates ("I found a way to use gradient descent to optimize the per-tensor quant layout"), Unsloth's per-layer dynamic selection, Opti's per-block correction network - all are variance/importance-driven resolution ladders. INV1 is standard practice transposed: the FP4-stop thread's edit states the anatomy - "a standard Q4 quantisation usually leaves more sensitive tensors in BF16, Q8 or Q6/5. Also, usually the K/V cache is quantized max to FP8/Q8" - i.e. the field's "anomalies" (salient tensors, KV) are exactly what never gets quantized hard. ALIGN: pass.
- **Quality axis:** the field's discipline is byte-matched controls + held-out sets (TAK vs byte-matched UD-IQ2_S; Opti paired per-window vs Q4_K_M; Unsloth Divergence-300 "NOT in calibration dataset"). auto_quantize's variance ladder has no held-out-task control in-repo; if promoted, the TAK lesson says the control is mandatory: byte-matched arm + held-out battery.
- **Generalization axis (the sharpest warning):** TAK is domain-locked (repetition loops outside the reasoning corpus; author: "Coding was not part of the protected set of tensors and outside its domain"); the benchmax critique ("task-aware" = "benchmax-aware", author concedes "benchmark aware" is fair) applies to any allocator trained on a narrow corpus. Transposed to auto_quantize: variance-gated L1-L5 aggregation of estate event logs will silently destroy exactly the event classes that are rare in the calibration window, i.e. the invariant-2 escape hatch is load-bearing, and an out-of-domain probe (replay a held-out event slice, compare aggregate-derived conclusions vs L0 truth) is OWED before any promotion beyond banked sensing.
- **INV3 (chain root recoverable from any level): NO external analog found.** Every weight-quant method read this window is lossy by construction; none claims reversibility. Opti even changes the file format (a small extra network per block; "stock refuses this file"). This invariant is estate-internal and unverifiable against literature - it survives as a design goal only if the estate's own bytes-check (re-derive L0 aggregate from any level) actually runs. Not stale, but UNPROVEN: funded-tier or local-bytes verification OWED; sensing cannot certify it.
- **Estate-map correction:** the ask cites "its promote gate (mag/percolator.py:264-272)". Grep "promote|PROMOTE" in mag/percolator.py returns ZERO hits; those lines are the invariant-registry auto-heal merge (the Z15 max-merge fix). The gate the map names does not exist at the cited location. Citation is stale; fix the map before the gate story is retold.

Verdict: invariants 1-2 are ALIVE and field-confirmed in mechanism; invariant 3 is estate-internal and unproven; invariant 4 is fine as schema hygiene. Nothing here is promotable on sensing alone - per the driving ladder, the five-axis quality/generalization axes need a funded-tier or local-bytes run before auto_quantize receipts pass any promote gate as verified work.

## RQ3 - quantization-induced divergence in multi-sample / consensus decoding

- **Direct measurement: NONE FOUND on reddit in the window.** No thread in the 45 in-window candidates measures n-sample agreement/self-consistency as a function of quant level. The estate's consensus-illusion question (laws.md:33) has no public reddit echo; the delta is real and open.
- **What the window does show is an adjacent, stronger form of the same disease: quant level changes WHICH failure modes appear while PPL/KLD stay flat.** Three independent in-window reports: TAK's reasoning-specialized quant falls into repetition loops on coding (post edit + Doaxan screenshot + author confirmation); 1w6najp's worst-ranked fine-tune "just loops when its starts working on the project... it repeats it self forever"; and (via pullpush, 1rgel19, outside window but read this session) Doomslayer606: "the UD-Q4_K_XL version sometimes falls into infinite reasoning loops" while the same model's MXFP4_MOE build does not, with the suspect being which layers stay at Q8_0. Phaelon74's numbers in that thread (NVFP4 mean KLD 0.109275 vs W4A16_GS32 0.048686 on Llama-3.1-8B, i.e. "TWO TIMES worse accuracy wise" without QAD) show distribution-level divergence is measurable and large - and noctrex's report there ("despite the lower KLD and PPL scores, it actually behaves better when using it in harnesses") shows even the divergence metrics disagree with harness behavior.
- Extension for the estate: consensus-illusion (laws.md:33) says agreement is not correctness; the 2026 window adds that the agreement surface itself is quant-dependent, so an n-sample consensus run on a Q4 build does not transfer to an IQ3 or FP4 build of the same model. OWED probe (sensing-tier, local): same frozen prompt battery, n-sample greedy agreement rate across Q4_K_M / IQ3_XXS / UD-IQ2_S of the same janitor model; hypothesis from this window: agreement rate degrades nonlinearly and failure-mode classes shift (loops, tool-call format breaks) before mean scores move.

## RQ4 - the quantize target in a deliberate ask (frozen prefix + tight ask + output contract)

Convergent template from the sources that did this best, mapped to the map law (laws.md:35: grounded, honest, versioned):

1. **Pin the object:** exact GGUF file + sha256 + llama.cpp build hash (Opti pins its runtime patch to llama.cpp 6a1a922d, 13 files, 471 insertions - content-addressed, revertable).
2. **Freeze the decode contract:** greedy (temp 0) for anything byte-compared; otherwise publish exact flags (1w6najp's working contract: `-ctk q8_0 -ctv q8_0 --temp 1.0 --top-p 0.95 --top-k 20 --min-p 0.0` + MTP state). Phaelon74's correction: context length is part of the contract - PPL at 512 "is not apples to apples"; freeze 2048.
3. **The instrument:** Unsloth's Divergence-300@32 shape is the deliberate-ask quantize target almost verbatim - 300 held-out prompts NOT in the calibration set, greedy 32-token completion, divergence measured against the BF16 reference, threshold named. It is cheap, deterministic, and re-derivable from raw provenance.
4. **The receipt:** expected value with CI and the exact one-command reproduction line (Opti: `llama-perplexity -m Opti-27B.gguf -f wiki.test.raw -c 1024 --chunks 96 -ngl 999` gives `6.4865 +/- 0.0703`), plus explicit not-run fields ("KL to FP16 logits: not run yet") - the honesty the estate's OWED law already requires.
5. **Task survival over aggregates:** pre-registered hidden-test battery (Opti: one coding task, 37 hidden tests, declared before the run, paired per GPU) - the TAK/consensus lesson in ask form: aggregate scores ride on the calibration distribution; hidden held-out tests catch domain lock before production does.

## Overlap method + results

`grep -c/-rl` over `catalog/catalog.jsonl` (691,788 lines) and scoped memory dirs (`memory/rib`, `memory/press`, `memory/percolator`, `watch/inbox`, `corpus/steal`), plus id-level checks against the 09-28 sibling sweep (`watch/inbox/frontier_olm_20260928/`). Results: 1wje0ke/1wgszma/1wl56g2/1w7ee1c/1w6najp/1w4mevo and the strings "Task Aware Knapsack delta/peculiar-ragdoll/Opti 27B/Voodoo/kaitchup" - all 0 in catalog; 0 in 09-28 .md holdings. 1wa5dp9 = HELD (frontier_olm_20260928/steal/quantization-compression.md:9-54 banked the TAK core incl. the failure mode; only the peculiar-ragdoll independent-replication comment is banked as new here). "Divergence-300" string already appears in frontier_olm_20260928/sweep/quantization-compression-x.md:28 (the Unsloth x.com claims were held; the docs-page methodology detail is the new delta). NVFP4/imatrix catalog hits are llama.cpp source files in burn_reset work dirs, not research holdings.

## Not run / OWED

- No local model runs, no eval batteries, no Ollama queries this session (sensing sweep only; every probe above is a proposal, not a result).
- r/ollama and r/MachineLearning month slices not pulled (RSS 429 burst); the r/LocalLLaMA + r/LocalLLM slices carried the quant density; noted as a gap, not fabricated.
- Kaitchup's full Q4-to-Q1 table is paywalled; only the post-level claim is banked.
- Unsloth docs quotes are extractor-mediated (WebFetch small-model extraction); RSS-sourced quotes are raw bytes parsed by this session's own script.
