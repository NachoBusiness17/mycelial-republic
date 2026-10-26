# STEAL CARD: quantization-compression via reddit (Round 2, v2 after critique)

- Date: 2026-10-09. Area: quantization-compression via reddit. Seat: steal-quantization-compression via reddit (dynamic workflow, branch mag/run-beta1-factory-build-audi-20260806T231709Z).
- Source: https://www.reddit.com/r/LocalLLaMA/comments/1x1bdvl/ (miner confidence 0.95). Thread: "LoRA over GGUF: Train Qwen3.8-Flash-Next in 40G VRAM" by /u/woct0rdho.
- v1 critique: approve=false, six fixes. All six landed in this v2; every load-bearing fact re-verified first-hand this sitting (commands named inline).

## Find, verified (all line numbers from the estate mirror watch/inbox/frontier_olm_2026-10-09/sweep/_txt_1x1bdvl.txt, read in full this sitting; live RSS fetch was verified in round 1 of this session)

- :3 recipe: Qwen3.8-Flash-Next (125B-A6B + 51B engram) trained in 40 GiB VRAM, no CPU offloading.
- :5 STACK GATE: "Since transformers 5.18, initial support for modern GGUF has been merged".
- :15 QLoRA over GGUF: "LoRA on Quantized base model", GGUF replacing the aged bnb 4-bit.
- :24 train/serve asymmetry: author trains on Q2_0 (MMQ ~1.5x as fast as IQ4_NL), serves on IQ4_NL; the only support offered there is anecdotal (one RP concept "definitely not in Qwen's training data").
- :25 HYPOTHESIS A, author-stated, hypothesis-grade: "My hypothesis is that as long as the LoRA rank is low, it will not learn the quantization error (which is mostly unbiased in modern quantization formats)".
- :28-29 LAW CANDIDATE B, ZenZombie117's counter-datum, n=1, DIFFERENT FAMILY: not the 125B recipe but "the Qwen3-4B, a tool-calling LoRA"; merged into Q4_K_M "the exact score fell from 1.00 back to the base of 0.69", "Q8_0/fp16 kept it"; "keep it as an adapter and dont merge" is ZenZombie117's line, not the author's.
- :32 the author's own words are weaker: "Merging a LoRA into a quantized model is a nontrivial task."
- Scoping carried from the sweep digest (watch/inbox/frontier_olm_2026-10-09/sweep/quantization-compression-reddit.md:82-89): the collapse datum is a cross-family n=1; the banked law candidate is "adapter-on-quantized transfers, merge-into-Q4_K_M does not", nothing stronger.

## Unbanked status, re-run first-hand this sitting, with both disclosures

- `grep -c "1x1bdvl" catalog/catalog.jsonl` returned 0 (run this session, round 1; critique re-ran with the same result).
- `grep -rln "1x1bdvl" memory/ corpus/` this sitting returned exactly one file, memory/trajectory/steps.jsonl (25 mentions, first at :73106, ts 2026-10-09T15:00Z, session_id sess_dwf-dwfrun-ce3840bf): SELF-CONTAMINATION from this workflow session's own step log, the same disclosure class the sibling card made at quantization-compression.md:15. The same grep exited 2 (at least one unreadable path mid-walk: memory/biography/knots/2026-08-10_1916_biography_mag-agen_3c265eaf.knot.json and memory/biography/knots/2026-08-11_1118_session_mag-agen_66a43508.knot.json, both "No such file or directory"), so the walk is NOT provably exhaustive.
- watch/inbox hits are exactly today's own sweep artifacts (verified this session, round 1). Nearest prior confirmed at watch/inbox/frontier_olm_2026-10-04/sweep/_fta_thread_1wslgkw.txt:113 (09-28 passing mention of the author's earlier repo).
- Percolator, checked this sitting: memory/percolator/candidates.jsonl reads 31 rows; no row contains "adapter" or the thread id; the only two "merge" rows are 09-28/09-30 frontier pointer rows (`grep -in "merge"` lines 1 and 13). No double-bank.

## The steal (mechanism, not links)

One recipe, one hypothesis, one scoped law candidate:

1. RECIPE: QLoRA over GGUF, the quantized GGUF itself as the frozen base (replacing bnb 4-bit), trains a 125B-A6B MoE fully local in 40 GiB (:3,:15). Fills UNMEASURED model-grid cells without leaving the T0/T1 local-first boundary. Stack floor: transformers >= 5.18 (:5).
2. HYPOTHESIS A (author-stated, one anecdote, not a law): a low-rank adapter does not learn the (mostly unbiased) quantization error, so a train-arm and serve-arm quant may legally differ (Q2_0 train, IQ4_NL serve, :24-25). The cross-quant transfer question was asked in-thread and left at anecdote level (:21).
3. LAW CANDIDATE B (n=1, cross-family, scoped): merging the adapter into Q4_K_M collapsed ZenZombie117's Qwen3-4B tool-calling exact score 1.00 -> 0.69 to base while Q8_0/fp16 merges kept it (:28-29); the author calls quantized merging "nontrivial" (:32). The correction must live in the adapter; folding it into the lossy base destroyed it.

## Estate map (organ: the quantizer)

The model-quant organ is the janitor pin surface plus its measuring instrument. Pins: configs/lanes.yaml:28-41 (envelope comment :28: RX 5600 XT ~6 GB VRAM, 64 GB RAM, AMD no CUDA; gemma:2b clerk/router/orchestrator/voice :31-35, qwen2.5-coder:7b worker :37, never stack two 7B/8B). Instrument: watch/inbox/frontier_olm_2026-10-08/sweep/quant_ab/run_ab.py, all four hardcodes re-read this sitting: ARMS two-tag dict :36, arm-keyed results path :302, summarize for-arm("A","B") :355-359, armA|armB-only dispatcher :431-432; scoring surface :10 (full-pipeline success), TASKS :48, first_json_object :236, grade(text, expect) :257, per-task spread :388; caps TEMP 0.0 / NUM_PREDICT 512 / NUM_CTX 8192 (:37-39). Its 10-08 run: TIE AT CEILING, 50/50 both arms, nothing promotes (RECEIPT.md:38-43), difficulty-hardened floor-near set OWED (:100-104), long-horizon blocked by the 6 GB arithmetic (:118-124).

Port moves:

1. GUARD LAW FIRST (zero compute), correctly attributed: guard motivated by the author's "nontrivial" (:32) plus one n=1 cross-family collapse (:28-29), not by the 125B result. Bank "no adapter merges into a sub-8-bit pinned GGUF" as a promotion-gate rule until the probe decides.
2. CLONE, DO NOT BEND: the probe reuses the quant_ab instrument via the clone-the-dir move (single edit to ARMS :36 plus the arm-keyed paths the hardcodes force; see sibling card watch/inbox/frontier_olm_2026-10-09/steal/quantization-compression.md, whose territory is QAT-checkpoint consumption and matched PTQ pairs, disjoint from the adapter lifecycle).
3. PERCOLATOR CANDIDATES RECORD THE DELTA AGAINST IN-FILE PRIOR ART: mag/auto_quantize.py:22 already holds "LAW: Anomalies are NEVER quantized. Keep raw forever." and :24 "LAW: The chain root is always recoverable from any quantization level." Those govern anomaly retention and root recovery; the new guard governs a different thing, the STORAGE LOCATION OF CORRECTIONS (deltas live against the compressed artifact, fold back only into the high-fidelity arm). Citing both so the candidate is a delta, not a re-derivation.
4. SOVEREIGN MIRROR honesty: the find moves frontier-scale TRAINING into the local column, but for THIS estate it is banked capability, not on-box capability (40 GiB recipe vs 6 GB pinned box, configs/lanes.yaml:28; RECEIPT.md:118-124). What ports today is the recipe shape at toy scale plus the hypothesis and scoped law.

## Probe (one, falsifiable, cheap, this week; fixed per critique fixes 1, 2, 4)

STEP 0, GATE: upgrade the estate venv transformers 5.15.0 to >= 5.18 on Windows/CPU torch (estate stack verified this sitting: transformers 5.15.0, peft 0.21.2, torch 2.13.0+cpu, import check exit 0; thread floor :5). If the upgrade fails, the probe reports NOT-RUN; no substitute stack, no bent instrument.

TRAINING CORPUS (named so the instrument can score it): a held-in set of tool-failure-recovery pairs in the exact input/output shape of run_ab.py TASKS (:48), then score on the instrument's fixed 10-task x 5-phrasing set with grade() (:257) exact-expect JSON matching at TEMP 0.0 / NUM_PREDICT 512 (:37-39).

FIVE ARMS at gemma:2b toy scale, $0 on-box, one rank-8 ~200-step adapter trained over the Q4_K_M base: (D) base, no adapter, unmerged baseline; (A) unmerged adapter over the training-base quant; (B) adapter merged into Q4_K_M; (C) adapter merged into q8_0; (E) unmerged adapter served over a DIFFERENT quant than trained on (tests HYPOTHESIS A, the question the thread asked at :21). Merge path is the transformers >= 5.18 GGUF support; if GGUF-native merge proves unavailable on Windows/CPU, report NOT-RUN.

GATED PREDICTIONS:
- Training-sanity gate: A must beat D by more than the 10-08 instrument's noise bar (0.0 pp per-task spread, RECEIPT.md:38-40). If A <= D, the toy run learned nothing: report INCONCLUSIVE-TRAINING, test no law, bank nothing, no downgrade.
- Merge law, only if the gate passes: B collapses toward D while C holds near A, the collapse transfers at toy scale; B within noise of A, LAW CANDIDATE B does not transfer: downgrade to WATCH and bank the SCOPED null (gemma:2b toy, not Qwen3-4B, not 125B).
- HYPOTHESIS A, only if the gate passes: E holds near A, low-rank adapters do not encode base-quant error and cross-quant serve is legal; E drops well below A, the adapter absorbed base-specific quant error and HYPOTHESIS A is falsified at toy scale.
