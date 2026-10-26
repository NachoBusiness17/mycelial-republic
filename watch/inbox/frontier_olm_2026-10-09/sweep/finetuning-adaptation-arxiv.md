# SWEEP: finetuning-adaptation via arXiv (frontier_olm 2026-10-09)

source-fetched: 2026-10-09. Seat: sweep-finetuning-adaptation-arxiv (workflow gopher). All items below were fetched and read by this seat during this ask. Every quote is verbatim from the fetched page.

## Door health

- arXiv export API (https://export.arxiv.org/api/query?...) returned full Atom feeds on all 6 pass-1 queries: green.
- Three pass-2 fetches of arxiv.org/abs (2610.06542, 2609.40236, 2610.11620) timed out at 60s on first try; the export.arxiv.org mirror served all three. Degradation noted, no fabrication. Verbatim abstract text for 2610.09772 and 2610.11620 was pulled by curl from the export API because the fetch relay caps verbatim quotes at 125 chars.

## Pass 1 (broad): 60+ entries surfaced, ~32 on-topic candidates, window 2026-09-09 to 2026-10-09

Queries: all:"LoRA" (40 hits, 318 total reported), all:"parameter-efficient" (40 hits), abs:"fine-tuning" AND abs:"single GPU"/"consumer GPU"/"consumer-grade" (9 hits), abs:"QLoRA"/"quantized low-rank"/"4-bit" (30 hits), abs:"low-rank adaptation" (30 hits). On-topic candidates include: 2610.09934, 2610.11655, 2610.04507, 2610.09122, 2610.06542, 2610.09772, 2610.08669, 2610.11620, 2610.11715, 2610.10349, 2610.10345, 2610.09835, 2610.07553, 2610.07533, 2610.07518, 2610.07212, 2610.06621, 2610.06387, 2610.06243, 2610.05800, 2610.05748, 2610.05481, 2610.08882, 2610.08049, 2610.07848, 2610.06765, 2610.01493, 2610.10657, 2609.40236, 2609.23959, 2610.00665, 2610.09007.

## Overlap check (grep, run this session)

- Instrument: ripgrep 14.1.1 (absolute path, coreutils absent in sandbox), patterns = distinctive title phrases of all candidates above, over catalog/catalog.jsonl and memory/ (trajectory noise excluded with -g).
- catalog/catalog.jsonl: 1,343,390 rows measured (`rg -c "^"`); 806 rows match LoRA|PEFT|fine-tun.
- Only catalog hits: two DIFFERENT subliminal-learning papers already held (2609.16927 "Verbalizing Subliminal Learning Effects Using Text Optimization", 2609.20027 "Can Data Attribution Filter Out Subliminal Learning? Not Reliably"). Adjacency, not overlap with 2610.10657 "Beyond Owls", which stays bankable.
- memory/ hits: only 2609.23959 "Open-Jev Judgments on CallScreenBench" (memory/runs/corpus_gap_research/MAP_BACKFILL.md:836, ARXIV_REGISTER.json:5069), already swept 2026-09-28. EXCLUDED from banking as known.
- "second descent" appears in memory/runs/quote_audit_wide_20260925/canon_concat.txt as generic canon text, NOT the 2610.04507 paper. All other candidate titles: zero hits, genuinely new.

## Pass 2 (deep reads, 10 items read end to end)

### 1. Harness Evolution Hits a Ceiling: When Weight Training Should Begin (2610.11655, 2026-10-08) : THE RQ3 ANSWER
https://arxiv.org/abs/2610.11655
"LoRA adapters trained on evolved-harness trajectories internalise the gain: under the original harness they add +0.13 on held-out tasks for both sizes." Qwen3.5-4B/9B on DeepPlanning: harness loop lifts 4B 0.16 to 0.30, 9B 0.32 to 0.44; LoRA on evolved trajectories stacks to more than double the 4B held-out score; on 9B the adapter alone matches the full evolution line, cutting content failures from one quarter to one in twenty; placebo adapter (answer-shuffled trajectories) falls below base; WebArena-Lite +0.09 where the gain lives in what the model sees and adapters add nothing. This is a diagnose-then-intervene rule for the skills_pack question: keep compounding the harness/skill ledger first, read failure composition (process vs content failures), and only bank the trainable gains into adapter weights, with a placebo-adapter run as the falsifier. Directly compatible with LENS 3: the skill ledger and weight adaptation are sequential stages of one loop, not rivals.

### 2. Itgan at NADI 2026 shared task (2610.09934, 2026-10-07) : RQ1 FIELD PROOF
https://arxiv.org/abs/2610.09934
"All three share one recipe, Whisper adapted with LoRA on consumer GPUs, and each was carried by a different addition to it." Competition-grade results (57.1 / 46.7 / 14.49 WER) from one consumer-GPU LoRA recipe. Transferable lessons: per-domain specialists continued from a pooled adapter beat one big adapter; base-model choice mattered more than adapter capacity (subtask 1.2); the last 0.60 WER came free from exact weight-space averaging of independently trained runs, no further training; a linear probe on frozen features recovers 44% of oracle routing; eight negative directions reported. Every comparison carries a paired-bootstrap test.

### 3. Comparison of techniques for fine-tuning open-weight models for entity extraction from radiology reports (2609.40236, 2026-09-30) : RQ1 ENVELOPE + DATA-SOURCE LAW
https://arxiv.org/abs/2609.40236
"Fine-tuning and inference fit within the memory envelope of a single 24 GB consumer GPU." Gemma-3-12B instruction-tuned on distilled REAL GPT-4o-labeled reports matched GPT-4o (macro-F1 0.845 vs 0.850, p = 1.000) on ICH acuity extraction; models trained on SYNTHETIC GPT-4o-generated reports never beat the untuned base (base gain +0.178 came from real-report distillation). Law for the estate: distill real specialist outputs (Hermes/prime lanes), do not synthesize training rows. Date note: 09-30, one day before the ask's "since 10-01" boundary but inside the 30-day sweep window.

### 4. LoRA's Second Descent Extends Beyond Parameter Parity (2610.04507, 2026-10-03) : RQ2 CAPACITY MATH
https://arxiv.org/abs/2610.04507
"LoRA thus exhibits a second descent, but matches dense risk only after losing its parameter advantage, first on DeiT-Tiny at four times dense's projection weights." Module-matched rank sweep (MMRS) on four vision backbones and a 7B LM under label noise. Rank-1 LoRA beat dense fine-tuning on 3 of 4 vision backbones (strong regularization at small rank); past the interpolation cliff, no parameter-saving rank matched dense risk. Answer to "adapter or full-parameter default": adapters stay the default, but rank is a capacity dial; matching full-FT quality can cost the very savings that motivate LoRA, so for janitors keep rank small and treat it as regularization.

### 5. Are Parameter-Efficient Fine-tuning Methods Really Different? (2610.09122, 2026-10-06) : RQ2 METHOD CHOICE
https://arxiv.org/abs/2610.09122
"LoRA most consistently limits forgetting at competitive performance, DoRA achieves higher mean task scores than LoRA in most comparisons". Six PEFT methods across language and diffusion models; PiSSA often costs more retention; restoring drifted singular-value spectra largely preserves task performance, questioning the necessity of explicit geometric preservation. Practical pick for the janitor fleet: plain LoRA when retention matters, DoRA when mean task score matters.

### 6. A Fine-Grained Analysis of the LoRA Fine-Tuning Landscape (2610.06542, 2026-10-05) : RQ2+RQ4 RANK-DATA COUPLING
https://arxiv.org/abs/2610.06542
"the appropriate adapter rank should depend on the quality of the data-induced optimization geometry, rather than on the model alone". LoRA-RIP: a data-dependent restricted-isometry metric; sufficient rank over-parameterization (rank set by the LoRA-RIP constant) eliminates spurious local minima; enables principled data selection under a fixed rank budget; "rank and data quality are two coupled resources". Feeds the curriculum question directly: corpus rows must be screened for conditioning before any adapter run; bad curriculum bytes poison the rank budget.

### 7. Decoupling Logic from Persona (2610.09772, 2026-10-07) : RQ1+RQ3 HOT-SWAP ADAPTERS, WITH A FLOOR
https://arxiv.org/abs/2610.09772
"the decoupled logic path is structurally invariant to pollution: its prompt stays at 180 (Llama) or 167 (Gemma) tokens while the mixed single-pass prompt grows from 242 to 1,203". Llama-3.1-8B-Instruct and Gemma-3-4B-it, both 4-bit, one Apple M2 laptop, 480 runs; persona adapters hot-swap in 1.7 ms; logic path byte-identical across pollution levels (40/40); robust on 8B (failure 0-20% vs 80-95%), but BOTH paths collapse on the 4B model under polluted logic input. Caution for the estate: gemma:2b janitor sits below the viability floor for the adapter-split pattern; the 8B rung clears it. This is also a precedent-magnet alternative axis: personas as swappable adapters instead of ledger entries.

### 8. Where to Adapt Matters: Layer-Selective Fine-Tuning (2610.11620, 2026-10-08) : RQ2 CHEAP LAYER SELECTION
https://arxiv.org/abs/2610.11620
"Experiments on mathematical reasoning and code generation show that LS-LoRA improves average target-task performance while retaining substantially more commonsense reasoning capability than standard all-layer LoRA". Layer-wise input-output cosine similarity is a forward-only proxy for Fisher scores, so adapter placement needs no backward pass; low-similarity layers get the adapters. Cheap enough to run inside a T0/T1 local boundary.

## Read but cut from the 8 (kept for the model garden)

- Internalizer (2610.11715, 2026-10-08): hypernetwork maps a document to a LoRA adapter on frozen 284B DeepSeek v4 Flash; adapters reach 84.9% top-1 vs 63.4% base with a three-word instruction; trunk is model-agnostic, trains cheap on small models, ports up. Conceptually the "corpus rows become parameters" endgame; cut only for slot count.
- MemFLoRA (2610.08669, 2026-10-06, ASP-DAC 2027): "MemFLoRA reduces saved-activation memory by 98.5-98.7% and peak training-state memory by 94.9-97.3% relative to full fine-tuning" but it is CNN/HAR-specific; the activation-memory-floor principle may port, the numbers do not.
- Also strong on-topic, unread beyond abstract: AutoAdapt 2610.10349 (per-domain LoRA + parameter-free routing), CoDe-LoRA 2610.08312, Riemannian LoRA 2610.08049, frozen-B study 2610.06621 (freezing B trails free LoRA by 8-18 points), FinVector-Market-4B 2610.08882 (rank-16 LoRA on Qwen 4B: FinQA 14.7 to 40.0), MOLT 2610.05748, TRACE 2610.07518, GRADE 2610.07553, SLDR 2610.10345, entropy-rate filtering 2610.01493.

## Answers to the four research questions

1. RQ1 (consumer-GPU results since 10-01 inside T0/T1): YES, three independent proofs. 2610.09934 (Whisper LoRA on consumer GPUs, competition WERs), 2610.09772 (4-bit 8B/4B adaptation + hot-swap on an M2 laptop), plus the envelope proof 2609.40236 (24 GB, Gemma-3-12B, 09-30). Nothing requires leaving the local boundary; the binding constraint is activation memory and data source, not the GPU.
2. RQ2 (adapter vs full-parameter default; does the corpus hold primer bytes): adapters are the frontier default for sub-8B (2610.04507, 2610.09122), but rank is chosen by data geometry (2610.06542). On the corpus: I measured catalog/catalog.jsonl at 1,343,390 rows with 806 rows matching LoRA|PEFT|fine-tun; the ask's LENS 1 figure of 52,313 curriculum rows is taken from the ask, I did not verify that subset definition this session, and nothing I read establishes whether those rows are training-grade primer bytes or inference-only material. That determination is OWED to a lens pass, not asserted here.
3. RQ3 (does weight adaptation break the skills_pack precedent magnet): no, it sequences after it. 2610.11655 gives the merge rule: harness/skill ledger first, then internalize its gains into LoRA adapters, verified against a placebo adapter; where the gain lives in what the model sees (harness), adapters add nothing. Keep compounding the ledger AND bank its trainable residue into weights.
4. RQ4 (day-8 mine's 32 unbanked sweeps verifiable via the green door in one funded session): the claim classes this sweep verified through the arXiv door in one session are (a) harness-vs-weights decision rule, (b) consumer-GPU LoRA feasibility incl. 24 GB envelope, (c) PEFT method differentiation, (d) rank-data coupling, (e) real-distillation beats synthetic. I could NOT locate a register literally named as the day-8 mine's 32 unbanked sweeps: my pattern search (unbanked|day-8 mine|day_8|day8 over memory/, trajectory excluded) returned only generic matches, so that inventory claim stays with the ask, unverified by me.
