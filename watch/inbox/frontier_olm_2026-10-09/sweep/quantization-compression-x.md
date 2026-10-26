# Sweep: quantization-compression via X - 2026-10-09

source-fetched: 2026-10-09

Lane: quantization-compression-x (frontier_olm daily, day-9). Window: 2026-09-09 .. 2026-10-09 (last 30 days).
Seat: sweep-quantization-compression-x (dynamic workflow run, branch mag/run-beta1-factory-build-audi-20260806T231709Z).
Doors: WebSearch `site:x.com` for pass 1; fxtwitter per-status (`https://api.fxtwitter.com/<user>/status/<id>`) for pass 2; arXiv export API for the RQ3 re-verification the ask names. Raw receipts: `sweep/_fx/*.json` (6 fxtwitter posts) and `sweep/_fx/arxiv_reverify_20261009.xml` + `sweep/_fx/arxiv_onlineqat_2610.09346.xml` (2 GETs), all fetched this sitting.

## Doors, honestly

- WebSearch `site:x.com`: rate-limited hard this sitting. Three separate queries returned repeated MCP 1302 "Rate limit reached" bursts before answering on a reworded retry (the huizi_mao MXFP4 query burned 3 dead attempts; the October-GGUF query burned 2; the low-bit-paper query burned 2). Same shape as the day-8 lane recorded. Nothing was invented from a failed call; every banked claim traces to a fetch that returned.
- fxtwitter: 6 of 6 resolves HTTP 200 first try this sitting (receipts in `sweep/_fx/`). Day-8's 60 s timeouts did not reproduce.
- arXiv export API: both GETs HTTP 200 (door recipe per lens/doors.md:11-14).
- Reddit door: not touched this sitting (closed per lens/doors.md:21-26; nothing in my candidate set needed it).

## Pass 1 - candidate census (55+ considered)

55+ distinct candidates surfaced from 9 `site:x.com` queries (Q4-vs-Q8 explainers, QAT/LoRA-on-quantized, GGUF benchmarks, pruning/weight-sharing, BitNet 1.58-bit, MXFP4 gpt-oss, Unsloth dynamic quants, Gemma 4 QAT, October low-bit papers). Every single-post candidate got snowflake-ID date triage via `.venv/Scripts/python.exe` (`(id >> 22) + 1288834974657`), this sitting. Result, stated honestly: the X door's quantization discourse is evergreen. Only TWO resolvable posts land inside the window: Fred834567 2026-09-10 (Nex-N2.5 Mini) and thesupermannx 2026-10-08 (LittleBit resurgence). Everything else measured clusters 2026-05..07 (cjzafir 05-10, Sumanth_077 07-30) or is June release noise (the four Gemma 4 QAT posts 06-05/06-06). Sharp IN-window material for these exact questions lives on arXiv, not X: 2610.04403 (10-03, held day-6), 2610.06026 (10-05, mirrored by day-8), 2610.09827 (10-07, held day-8), and 2610.09346 OnlineQAT (10-07, mirrored-but-unbanked, banked below).

## Pass 2 - deep reads (fetched and read this sitting)

Six posts resolved end to end via fxtwitter: thesupermannx 2108098865073410484, Sumanth_077 2082834159937241270, cjzafir 2053341219380674816, Fred834567 2098036015793660124, WesRoth 2063048224298996062, mfranz_on 2096225605142355983. Two arXiv GETs read at abstract level: id_list batch (2610.04403, 2609.26219, 2610.09827, 2610.06026) and 2610.09346. Estate reads for grounding: watch/inbox/frontier_olm_2026-10-08/steal/quantization-compression via hn.md (full), steal/kv-cache-context-engineering.md :1-75, sweep/quant_ab/SUMMARY.json (full, first-hand), lens/ directory of this run (burns, corpus, doors, questions).

## Answers to the four research questions

**RQ1 (did anything since 10-01 move the qwen2.5:7b Q4-vs-q8 ceiling?).** For post-training quantization at the estate's task ceiling: NO X-surfaced result moves it, and the second independent practitioner datum now corroborates the tie at a NEIGHBORING size. The estate's own A/B (run 10-08, read first-hand this sitting at sweep/quant_ab/SUMMARY.json): 50/50 vs 50/50 full-pipeline, strict 49/50 both, all 50 output pairs byte-identical, per-task spread 0.0, only speed separates (6.90 vs 3.00 tok/s). cjzafir (05-10, out-of-window, banked marked): a 4B fine-tune at 98 pct accuracy on full precision AND Q8, ~1 pct loss at Q4. Two sizes, same shape: Q8 == FP, Q4 within noise, at and above 4B. The frontier action has moved BELOW four bits, where PTQ provably breaks (2610.04403: sub-2B definitional collapse at Q2, re-verified live this sitting) and QAT-class methods recover it (OnlineQAT, 10-07, on Qwen3-1.7B). So the standing rule is: Q4-at-ceiling holds for PTQ janitor pins; the floor, not the ceiling, is where the frontier is now working.

**RQ2 (which QAT methods fill UNMEASURED grid cells without breaking T0/T1 local-first?).** Two, both verified this sitting. (1) RELEASED QAT CHECKPOINTS: Google shipped Gemma 4 QAT checkpoints 2026-06-05/06 (WesRoth/googledevs/googlegemma/TeksEdge posts, all resolved 06-05/06-06): Q4_0-format checkpoints for all sizes plus drafters, llama.cpp/Ollama/LM Studio support, E2B under 1 GB, explicitly "preserving more model quality than standard post-training quantization". Zero estate holdings (overlap greps below). This is the local-first grid-cell fill: download once, run on the T0/T1 box, no datacenter. The port is to pull a gemma-4 QAT-q4_0 GGUF and rerun the quant_ab instrument against the PTQ arm at matched bits, which converts the UNMEASURED QAT-vs-PTQ cell into a measured one on-box. Note the estate's short worker IS gemma4. (2) OnlineQAT (arXiv 2610.09346, 10-07): block-wise QAT init + on-policy distillation from a frozen full-precision teacher on student-generated prefixes; W3A16 57.28 / W2A16 32.52 on Qwen3-1.7B, beating ReasoningQAT by 2.90 / 0.44. Training-side, so it is a Lab/funded-tier option, not a janitor-lane act; the inference-side act is consuming its eventual released checkpoints the same way as Gemma's.

**RQ3 (of the day-8 mine's 6 unbanked cards, which carry quantization claims re-verifiable in one GET through the green arXiv door?).** The six cards (frontier_olm_2026-10-08/steal/): finetuning-adaptation, inference-efficiency-hn, kv-cache-context-engineering, open-local-models, open-local-models via reddit, quantization-compression via hn. Verdict, from one id_list GET (HTTP 200, 4 entries, receipt `_fx/arxiv_reverify_20261009.xml`): THREE cards carry arXiv-cited quantization claims and ALL THREE re-verify clean. quant-hn card: 2610.04403 confirmed live ("Saying, Not Knowing...", published 2026-10-03, 27 artifacts / 13 families / 0.35B-14B down to Q2_K). kv-cache card: 2610.09827 confirmed live ("Dual-QK: Sharp Queries and Flat Keys for Prunable 2-bit KV Caches", 2026-10-07) and 2609.26219 confirmed live as PatchKV (2026-08-18; its abstract carries the card's verbatim quote about altered causal histories and rotary positions). finetuning card: 2610.06851 is its paper but it is a token-cues paper, not quantization; its pruning numbers (0.449 vs 0.146) are X-post-sourced, NOT door-verifiable. The remaining cards carry no one-GET-verifiable arXiv quant claims (inference-efficiency-hn is estate-internal A/B content; the open-local pair is HF-model-card-shaped). The Q3 MISS the cards did not catch: arXiv 2610.09346 OnlineQAT sat mirrored at state/arxiv/2026-10-08/2610.09346v1.txt with a title row in the day-8 mirror TSV (sweep/_raw/mirror_titles_1006_1008.tsv:503), seen but never banked, and it is the single most on-question quantization paper of the window. Banked as item 1 below. Also: 2610.06026 "Differentiable Bit-Widths" (SVD co-optimized pruning+quantization, 10-05) re-verified live AND already mirrored by day-8 (sweep/open-local-models-arxiv.md:50), so it is NOT re-banked.

**RQ4 (weight-sharing and pruning for sub-8B the corpus does not hold?).** The X door adds NOTHING new in-window: the two candidates (LittleBit resurgence post 10-08; PavloMolchanov's pruning+weight-sharing OpenReview mentions) are both already-covered subjects. LittleBit (arXiv 2506.13771, sign latent factorization, 0.1 BPW, Llama2-13B under 1 GB, XOR-instead-of-matmul compute, 11.6x FP16 speedup claim) is held by the day-8 reddit lane (frontier_olm_2026-10-08/sweep/quantization-compression-reddit.md:42, :121-123, incl. the LittleBit-2 follow-up 2603.00042) plus watch/inbox/LINK_DROP_LITTLEBIT_20261008.md; 2610.06026 is mirrored day-8. Per LENS 1 (lens/corpus.md:19-27) the corpus has NO compression shelf: the library is curriculum + serving (ms-genai 12,142; lmcache-src 2,331 KV-storage), so the sub-8B pruning/writing gap is real but the X door did not close it this window. Molchanov is profile-level only, unresolvable through the door.

## Overlap ledger (greps run this sitting)

- catalog/catalog.jsonl full streaming pass (repo venv python, all 1,343,390 rows): "gemma 4 qat" 0, "qat-q4_0" 0, "qat" 1 (state/arxiv/2026-10-08/2610.09346v1.txt), "54.56" 0, "kimi k3" 3 (model-level intake watch/INTAKE_KIMI_K3_MATH_20260904.md + prompt-leak files; no quant numbers), "nex-n2.5" 0, "21.17" 0, "camry" 0, "littlebit" 2 (watch/inbox/LINK_DROP_LITTLEBIT_20261008.md + LINK_DROP_SLICE_DESK_20261008.md), "2506.13771" 0 (ID never cited; coverage is by name).
- memory/ + watch/inbox/ + corpus/steal/ + queue/ + state/ recursive grep for "build camry", "codex 5.5", "preserving more model quality than standard", "57.28 at W3A16", "perplexity of 54.56": hits only in memory/trajectory/steps.jsonl (THIS session's own log, contamination per the day-8 precedent), watch/inbox/frontier_olm_2026-10-03/sweep/tmp/sw2_full.jsonl ("Codex 5.5" x3 = an unrelated r/codex product post, read this sitting, NOT cjzafir), and the OnlineQAT mirror + its state/arxiv/2026-10-08/digest.jsonl title row.
- The three most recent mines grepped for "2610.09346|OnlineQAT" excluding _raw mirrors: zero hits outside the TSV row. The 2610.09346 mirror is unbanked.
- Day-8's own X lane (frontier_olm_2026-10-08/sweep/quantization-compression-x.md, read in full this sitting) holds bnjmn_marie's ladder, FIT-GGUF, GPU price triggers, 2610.00983 + 2610.06174: none of my five banks collide.

## Anti-rebank dispositions

1. thesupermannx LittleBit post (10-08, in-window, resolved, read): NOT banked. Paper + follow-up + code already held (day-8 reddit lane + LINK_DROP). The post adds only a virality signal and the XOR-compute framing.
2. 2610.06026 Differentiable Bit-Widths: re-verified live but already mirrored day-8. NOT banked.
3. 2610.04403: held day-6, re-verified live this sitting as the RQ3 re-verification, not re-banked.
4. mfranz_on 09-05 llama.cpp explainer (resolved, read): evergreen, 4 days out of window, zero new measurement. Considered, not banked.
5. qwen2.5:7b A/B: RUN and tie (anti-rebank rule 2 of lens/burns.md); cited as estate ground truth only.

## Banked items (strongest first)

1. arXiv 2610.09346 OnlineQAT (2026-10-07, IN window): on-policy distillation QAT recovering W2/W3 accuracy on Qwen3-1.7B; mirrored-but-unbanked; live-re-verified via my own GET.
2. WesRoth 2063048224298996062 (2026-06-06, OUT of window by 122 days, marked): Gemma 4 QAT Q4_0 checkpoints for the janitor family; zero estate holdings; the direct RQ2 port.
3. Sumanth_077 2082834159937241270 (2026-07-30, OUT by 71 days, marked): naive community 1-bit PPL 54.56 vs Unsloth dynamic 2.58 (21x); the measured cliff half of RQ1.
4. cjzafir 2053341219380674816 (2026-05-10, OUT by 152 days, marked): 4B fine-tune 98 pct at FP and Q8, ~1 pct Q4 loss; second independent Q4-vs-Q8 tie datum at 4B.
5. Fred834567 2098036015793660124 (2026-09-10, IN window): Nex-N2.5 Mini 35B MoE, GGUF Q4_K_M ~21.17 GB with honest 24 GB caveats; the only in-window X post with quantization substance besides the anti-rebanked LittleBit post.

## Falsifier / caveats

- Items 2-4 are OUT of the 30-day window and are banked marked-as-such because they carry the estate's unheld answers to RQ1/RQ2 (day-8 precedent: out-of-window strongest banked with true dates).
- cjzafir is anecdotal: single fine-tune, eval undefined, self-reported percentages. Confidence capped at 0.7 accordingly.
- arXiv banks are abstract-level; the OnlineQAT full text was never read (only mirror txt + live abstract).
- No pytest run this sitting (not applicable to a sweep lane); no lane config changed; every external claim traces to a URL or file fetched this sitting, every estate claim to a path:line read this sitting.
