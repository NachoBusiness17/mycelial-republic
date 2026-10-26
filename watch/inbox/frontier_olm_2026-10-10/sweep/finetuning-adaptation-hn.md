# SWEEP: finetuning-adaptation via HN (frontier_olm_2026-10-10)

source-fetched: 2026-10-10. Seat: sweep-finetuning-adaptation-hn (dynamic-workflow gopher, Mag Resource Harness). Window: created_at_i > 1788998400 = 2026-09-10 .. 2026-10-10. Doors: hn.algolia.com search_by_date + search (tags=story), news.ycombinator.com item pages for threads, primary articles fetched direct. Every banked item below was read by me this sitting; nothing banked unread.

## Door health

- Algolia queries fired (8): "fine-tuning" (17 story hits), LoRA (30 rows, mostly local-LLM noise), distillation (19), "test-time training" exact phrase (nbHits=0, a real empty window, not a degradation), quantization (13), unsloth (5), finetune (19), relevance search "fine-tuning small models" (30). One query ("in-context", by-date) TIMED OUT at 60s on its only attempt and was not retried; the in-context-vs-weights angle was covered instead by the relevance lane, the Ask HN 49807413 thread, the Clef thread, and today's itsodeleo read. github.com/volotat/mini-AGI timed out once and recovered on refetch.
- news.ycombinator.com item pages fetched clean (threads 49923692, 49807413, 49783133).

## Pass 1: candidate census

~108 rows seen across the queries, 40+ on-topic in-window candidates, 30+ considered. Headline candidates: Clef decision models (641 pts), Mini-AGI (277), Cactus Needle 3 (236), Ask HN worth-it, duane.sh Qwen3.5-4B, Unsloth decision-model doc, Nemotron IOI/IMO, MOLT QLoRA, easycommand, Sentry, itsodeleo, UniEvo-VL, Shrewd, DeltaTensors, Swift-Qwen3.8, recursive self-improvement via on-policy distillation (2609.30652), Jensen Huang distillation-is-competition, distillation-defenses arXiv rows.

## The dedup wall (dominant fact, verified before banking)

Prior sibling banks + the estate ingest lane already hold almost every strong in-window item:
- 10-01 (watch/inbox/frontier_olm_2026-10-01/sweep/finetuning-adaptation-hn.md): duane.sh, cacheverifier, Ask HN worth-it, Mini-AGI, SecMask, CUA-S1, Sidekick.
- 10-02 (frontier_olm_2026-10-02/sweep/finetuning-adaptation-hn.md): Clef blog + HN thread, Mini-AGI thread, Cactus Needle 3 thread, Ask HN thread, duane.sh, all read there.
- 10-05: Clef re-verified. 10-07 (swarm sibling, swarm-orchestration-hn.md item 4): Sentry BANKED (same quote, same 81.7% / 939-failure numbers).
- 10-08: DeltaTensors, Ask HN worth-it (2nd), Cactus Needle 3, duane.sh (2nd), easycommand, Laya Studio, MOLT.
- 10-09 (frontier_olm_2026-10-09/sweep/finetuning-adaptation-hn.md): Nemotron IOI/IMO, Local JEV Mac Air, STT Lisp; Shrewd banked 09-30; Swift-Qwen3.8 banked 10-07.
- state/arxiv ingest lane holds 2609.30652 since 2026-09-28 (state/arxiv/2026-09-28/2609.30652v1.txt) and it also appears in the 09-30 and 10-03 finetuning-hn banks, so my read of it this sitting is verification only, NOT banked.

## Pass 2: verification reads this sitting (11 pages fetched and read end to end)

Clef blog (re-confirmed: frozen Qwen3.8-27B/9B + rank-256 LoRA + routing head, Apache 2.0, BFCL 98.47, BANKING77 94.20 vs Jev 79.74), Clef thread (texture: mikeocool "If I have to gather and tag data to fine-tune Jev, I can probably just train an 'old school' classifier"; Foobar8568 beat Jev locally on consumer GPU; Clef 2-3x slower than Jev in practice; pareto chart omitted cost), Mini-AGI README + thread (jmatthews replication: "Most of your claims prove out but the lever is essentially Biderman et als 'learn less forget less'", already quoted in the 10-02 bank), Ask HN 49807413 (speedgoose "almost never worth it now"; minimaxir data+hosting criteria; spottedmarley dataset-creation-is-the-cost), Needle 3 page (29-121M params, LoRA lifts subnetworks 18-36 pts, passes DeepSeek V4 Flash from 29M params on DroidCall), duane.sh ($7 / 1.6h H100 SFT + GRPO with Opus grader, 71% cheaper than Flash-Lite), Unsloth decision doc, MOLT README (23% faster than Unsloth single-seed, PolyForm Shield), Sentry README, itsodeleo post, UniEvo-VL and 2609.30652 abs pages.

## Banked items (3 genuinely new, strongest first; all read end to end this sitting)

### 1. Train your own Decision Model with Unsloth (unsloth.ai docs; HN 50024959 2026-10-09 + 50030016 2026-10-10)
- URL: https://unsloth.ai/docs/basics/train-your-own-decision-model-with-unsloth
- Quote (verbatim): "Qwen3.5-4B reached 76% in 10 minutes on an L4."
- Why: RQ1+RQ2 anchor. The decision-model pattern (frozen LLM + Clef-style classification head, prefill-only option scoring) is now a turnkey single-host recipe: Qwen3.5-0.8B trains in 4GB VRAM, 2B in 8GB, Llama-3.2-3B 4.1GB, Gemma-4-E4B 14.4GB; free Colab/Kaggle L4; one epoch 10-49 min; 4-bit LoRA rank 16, LR 2e-4, 2 epochs. Measured lifts: typed-decisions 36 -> 73 (0.8B), BANKING77 7 -> 74, CLINC150 19 -> 76; test accuracy 77-81%; decontamination claimed, unverified. This is the cheapest measured weight-path for exactly the lesson classes that are CHOICE-shaped (route/approve/classify/score), runnable inside the estate's T0/T1 boundary (no rented H100 needed, unlike duane.sh).
- Overlap: grep "train-your-own-decision-model" + "FastDecisionModel" across all frontier_olm sweep files (2026-09-28..10-10), memory/, catalog.jsonl: sole hit is the URL string inside frontier_olm_2026-10-08/sweep/_raw/ft_pool_1008.json (raw reddit harvest pool, listed-not-read, never banked). HN submission 2026-10-09T18:42Z postdates the 10-09 sweep window. First end-to-end read.

### 2. If LLMs Can Decide Without Fine-Tuning, Do We Still Need Models Like Jev? (itsodeleo.github.io; HN 50032037, 2026-10-10)
- URL: https://itsodeleo.github.io/posts/local-decision-workflow/
- Quote (verbatim): "small specialist models can be very fast, but useful judgment does not necessarily require additional training"
- Why: RQ3's cleanest measured counter-result. On 300 fixed self-authored questions (M2 Max 64GB): direct scoring (read answer-label logits at final position, no generation, no fine-tune) with Gemma-4-26B hit 75% at 259ms median, vs 77% for the best finetuned OpenDecider-small config, vs 35-51% for Laya variants and 37% for full generation with the same Gemma weights at ~2.2s. Author's caveats: uncontrolled comparison, logit scores are not calibrated probabilities, fixed-options only, and Laya's public-benchmark gap (77% public vs 51% here) suggests task overfitting. Estate feed: before any janitor gets a LoRA, measure whether the resident model's logits already decide the lane; the rib path may win outright at zero training cost.
- Overlap: grep itsodeleo / "direct scoring" / OpenDecider / 50032037 across all sweep banks, memory/, catalog.jsonl: only 50032037 appears, in today's lens/doors.md door-probe listing (title seen, not banked). Zero bank rows. First read.

### 3. UniEvo-VL: Self-Distillation Training for Multimodal Model Self-Improvement (arXiv 2609.38721; HN 49985292, 2026-10-06, 16 pts)
- URL: https://arxiv.org/abs/2609.38721
- Quote (verbatim): "we leverage their self-critiques as privileged information and ask a single multimodal model to act as both teacher and student"
- Why: RQ1 pattern-witness: teacher-free self-improvement where the SAME model, conditioned on its own test-time self-critique, becomes the privileged teacher for on-policy self-distillation along the student's own trajectories (per-state divergence of diffusion distributions). Measured on Qwen-image-2512: GenEval 0.747 -> 0.808, Soft-TIFA 32.97 -> 35.53; gains non-uniform (text rendering mixed); external critics (GPT5.6-Luna) suggest a higher ceiling for strong judges. Multimodal domain, so transfer to text janitors is unproven (OWED), but it independently corroborates the privileged-self-teacher pattern the estate cares about (ASCENT's hindsight teacher, banked today by the arXiv sibling; 2609.30652's co-evolving teacher, held since 09-28): the distillation door does not need funded-tier teacher spend.
- Overlap: grep "unievo" / "2609.38721" across state/arxiv ingest lane (all dates), every frontier_olm sweep file, watch/inbox, catalog.jsonl: 0 hits. New.

## RQ answers (grounded in this sweep's reads + siblings' held items)

- RQ1 (lesson classes needing weights; cheap single-host distillation path): choice-shaped lesson classes now have a turnkey measured path (item 1: 4-bit LoRA r16 decision head, 4-14GB, free-tier GPU, BANKING77 7 -> 74). Teacher-free distillation is now a pattern with three independent witnesses (UniEvo-VL here; ASCENT and 2609.30652 held), so the ASTRA-successor door is a pattern, not a product. Procedural/judgment-shaped lessons still have no cheap weight carrier: the one cheap continual-learning exemplar (mini-AGI) is deflated in its own thread to Biderman's "learn less forget less" (held 10-02), and ASCENT needs verified trajectories the estate would have to generate anyway.
- RQ2 (QAT/low-rank vs babelfish record path, measured): single-host adaptation is cheap and measured at every rung (item 1; MOLT Windows QLoRA held 10-08; duane.sh $7 / 1.6h held). But NOTHING anywhere measures adaptation cost in babelfish units (2,778 claim lines -> 151/109/2,058 rows, fa0927b93); the arXiv sibling reached the same OWED today. And item 2 is the counter-warning: for choice-shaped decisions the no-training path (logits of a resident 26B) matched the finetuned specialist within 2 pts, so the rib path can win outright.
- RQ3 (steering-free covering rails): partially, on two lanes only. Decision lane: direct scoring, no training (item 2). Failure-recovery lane: Sentry's test-time playbook of verified lessons (held 10-07; my re-read confirms; code still unreleased, "2-3 weeks" per repo). "test-time training" as an exact phrase returned nbHits=0 on HN in the whole 30-day window; no evidence TTT covers rail/procedure engineering. Convergence is rails-as-weights from both sides (arXiv sibling: MetaSteer compiles steering into adapters; ASCENT writes LoRA).
- RQ4 (academic gap blocking?): No. HN delivered same-day engineering-grade measured items (the Unsloth doc hit HN 10-09/10-10 and is banked here 10-10); the arXiv sibling banked 8 fresh papers on the same RQs today; the state/arxiv ingest lane holds abstracts at 1-2 day latency (it held 2609.30652 since 09-28, which is why this sweep dropped it). The uncovered delta is digestion-tier (method detail) and the estate's own measured runs, not door access.

## Overlap instruments run this sitting (win32, repo venv)

1. Full-tree scan: .venv python walk of catalog/catalog.jsonl + memory/ (751,887 files) over 19 patterns with positive controls (qwen 4149 files, lora 1368, onlineqat 2, babelfish 170, astra 3316; instrument verified live).
2. Catalog line inspection: clef=2 rows (CLEF-2026 arXiv track), sentry=237 (Sentry monitoring tool in parked libs), molt=58 (MoltenCore WoW scripts), cactus=9 (game assets), unsloth=33 (corpus paths), flash-lite/duane.sh=1 (10-06 sweep confirm scratch): token collisions, not holdings.
3. Sweep-bank grep across frontier_olm_2026-09-28..10-10 for the four new-candidate markers (results inline per item).
4. state/arxiv + watch/inbox + catalog grep for 2609.30652 / 2609.38721 / "on-policy distillation" / "unievo": caught 2609.30652 as held (dropped), UniEvo clean.
Note: the first findstr-based greps under this seat's shell returned false zeros (literal %ERRORLEVEL%, silent dir; shell is not cmd.exe as labeled); all overlap claims above rest on the venv-python scans only.

## OWED

1. The babelfish-unit falsifier run (gemma:2b QAD/decision-LoRA hours-logged vs rib-authoring hours for one lesson class); shared with today's arXiv sibling OWED; no public source measures it.
2. Replicate itsodeleo's direct-scoring result on an estate decision lane (its 300 questions are self-authored and uncontrolled by the author's own admission).
3. UniEvo-VL full text: does the privileged-self-critique teacher transfer to text-only janitors?
4. Unsloth doc's decontamination claim: unverified; treat BANKING77/CLINC150 lifts as vendor-reported until an estate run.
