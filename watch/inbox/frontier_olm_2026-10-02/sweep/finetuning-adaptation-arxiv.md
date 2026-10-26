# SWEEP: finetuning-adaptation via arxiv (2026-10-02)

source-fetched: 2026-10-02. Seat: sweep gopher, actor_3_25 of run sess_dwf-dwfrun-bc564831-f325-4fc6-be3d-b3384a8ddc79.

## Doors and degradation

- arXiv API door (export.arxiv.org/api/query) worked for 7 of 8 queries; one query (all:"agent trajectories"+fine-tuning) and one retry (all:"self-evolving"+LLM agent) timed out at 60s twice. Reported as degraded, not faked.
- WebSearch door degraded: the backend returned MCP error -429 code 1302 on five consecutive attempts (rate limit). No websearch results were used. Recipe fallback (the API door + list pages) covered the gap; /list/cs.CL/recent was not fetched because the API door returned fresh sorted listings for the same window.
- All 8 banked items were fetched by this seat this session: five papers end to end via arxiv.org/html full text (2610.01493, 2609.10750, 2609.24186, 2609.23916, 2609.06986), two via abs pages after HTML 404 or for listing-level items (2609.15309 after its HTML 404'd, 2609.12353, 2609.27262). Quotes are verbatim as relayed by the fetch reader (it caps excerpts at 125 chars); confidence reflects that relay.

## Pass 1 (broad, >=30 candidates from last 30 days, 2026-09-02..2026-10-02)

Queries run against the API, sorted by submittedDate desc: QLoRA (30 returned, 22 in-window), Gemma+LoRA (30 returned, ~8 in-window), continual learning+LLM agent (30 returned, ~6 in-window), catastrophic forgetting+fine-tuning (28 returned, ~23 in-window), function calling+fine-tuning (20 returned, ~5 in-window), instruction tuning+data curation (18 returned, 2 in-window), data mixture+fine-tuning (20 returned, ~5 in-window), deduplication+language model (20 returned, ~13 in-window). In-window candidates considered: well over 30 (sum approx 80+ with overlap across queries). Strongest excluded for recency: Data Turnstile 2607.29250 (Jul 31), Small Reasoning Models IFFC 2608.22472 (Aug 23), Knowing but Not Saying 2608.20757 (Aug 21), Learning New Facts with QLoRA 2608.25677 (Aug 26).

Overlap greps run this session (commands: grep over catalog/catalog.jsonl and memory/):
- 2609.25373 FunctionGemma: catalog hit at watch/inbox/frontier_olm_20260928/sweep/_raw/full_2609.25373.txt (76KB full text) + memory/runs/corpus_gap_research/ARXIV_REGISTER.json line 5141. FULLY BANKED by the 20260928 sweep. Excluded from items.
- 2609.09476 Readable Schemas: catalog state/arxiv/2026-09-10/2609.09476v1.txt (abstract snapshot). Excluded.
- 2609.17346 Where Should a Document Live: catalog state/arxiv/2026-09-16/2609.17346v1.txt. Excluded.
- 2610.01493, 2609.23916, 2609.27262: abstract-only snapshots in the daily arxiv ingest (1.5-1.9KB each); no deep read anywhere in the estate. Deep reads banked here.
- 2609.10750, 2609.24186, 2609.15309, 2609.12353, 2609.06986: zero catalog hits, zero memory hits (memory/trajectory/steps.jsonl matches were this session's own journal rows, verified by session_id ...actor_3_25). Genuinely new.

## Answers to the four research questions

### RQ1: PEFT/QLoRA recipes for gemma-class narrow tool-use on consumer VRAM, task metrics

The estate already holds the two best direct hits (FunctionGemma 270M, 29.3 to 76.5 percent accuracy; Readable Schemas, representation beats scale at 270M-1.7B) from earlier sweeps. New this window: 2609.27262 (Amazon, 13 models incl Gemma-3, 8 support datasets, 200+ checkpoints) says multi-task full fine-tuning beats specialists at every size, specialists degrade sharply off-task, and sequential LoRA preserves earlier skills better than sequential full FT. For a janitor fleet that means: one multi-task adapter over all janitor verbs beats one adapter per verb unless you also built the router. Also in-window negative results worth holding: real 4-bit NF4 QLoRA underperformed plain LoRA in the dysarthric-ASR case study (2609.02735), and AQLoRA (2608.23816, just out of window) trades 1 accuracy point for 11 percent faster training by keeping error-ranked layers fp16.

### RQ2: curation laws for session tapes to SFT pairs (the mem0 flattens-progressive-phrasing warning class)

Three independent papers converge on a curation doctrine:
1. 2610.01493: when iterating on your own outputs, filter each generation by Kontoyiannis entropy rate (a match-length statistic, no model needed, <10ms per 1500-word doc). Unfiltered self-distillation collapses distinct-3 by 42 percent relative; entropy-filtered keeps it. Logprob-based filtering does nothing (its variance collapses after one FT step, SD 2.17 to 0.13). Collapse mechanism: progressive loss of distributional tails, surface signature repeated n-grams. Law: select top-k by entropy WITHIN domain (stratify; domains differ in baseline entropy), discard short texts.
2. 2609.24186 LIMIT: 796 curated samples beat 24,457 full-data on BIRD (66.9 vs 67.8 close to parity, 91 percent GPU-time cut). Pipeline: easy-removal (one greedy rollout correct = drop), hard-removal (fewer than 2 of 8 rollouts correct = drop), shortest-correct CoT, multi-dim LLM-judge, then genetic selection with fitness = 0.2 table coverage + 0.3 column coverage + 0.5 quality - 0.5 size penalty. The coverage term matters most: dropping it costs 7.0 EX. Law: diversity-of-coverage is a weighted fitness term, not a filter.
3. 2609.12353 SynthSentry: corpus-level contamination screen (lexical diversity collapse, n-gram tail truncation, perplexity variance) that needs no generator access; naive quantile thresholds run 4x over the false-positive budget, calibrate with covariance shrinkage + bootstrap.
For the seat-tape organ this composes into: entropy-rate pre-filter (free, catches the flattening), coverage-weighted selection (catches phrasing monoculture), contamination screen before any mix with public corpora.

### RQ3: continual adaptation to own session data without catastrophic forgetting, and the evals that catch it

- 2609.10750 is the estate's exact case: a production 34,396-skill router LoRA-fine-tuned on ~28K synthetic pairs built from ~1K real agent trials. Aggressive LoRA (r=16/32) lifted in-distribution recall but dropped Terminal-Bench 2 recall@10 from 0.850 to 0.650. Mitigations (embedding-anchor, L2-init, EWC, LwF) all landed within noise of each other; the dominant lever was LoRA rank r=8 + lr 5e-6 + attention-only. Law candidate: rank is the retention knob, regularizer choice is not.
- 2609.06986: at 100-task horizon, naive sequential SFT retains 1.2 percent, best single mechanism 8.1 percent, composed generative-replay + merged-LoRA 34.9 percent (super-additive). Evals that catch it: final-retention over all tasks, per-task diag accuracy (to separate acquisition failure from forgetting), memory half-life, AND general-capability probes, because all methods lost GSM8K/MMLU while retention looked fine. Verbatim eval lesson: retention on training queries is not capability.
- 2609.15309: Elo-per-token shows agent marginal gains fall below the independent-sampling reference while human contestants improve superlinearly; also splits 100M tokens across parallel sessions beat one long session (+264 Elo). Implication for the estate's eval organs: measure scaling shape, not single-shot, and prefer parallel short sessions over one long grind.
- 2609.28395 (WMT, abstract-only catalog snapshot): general-forgetting mitigation (EWC) does not preserve task-specific instruction following; only control-task data mixing did. Evals must be instruction-level, not capability-level.

### RQ4: does fold-conduct-tracks-model-date-not-vendor generalize to training data (recency vs vendor diversity)?

Partial support with a mechanism correction from 2609.23916 (six models incl Gemma-3-1B, post-cutoff FineWeb-Edu). Their finding: plasticity tracks pretraining saturation (tokens-per-parameter, rho = -0.63), NOT recency per se; and catastrophic forgetting is "a property of disjoint regimes, not of CPT per se", because web revisits (60-70 percent of URLs) give implicit replay. Quality dominates quantity (6B high-quality tokens match 40B broader). Generalizing honestly: recency outranks vendor diversity only insofar as recent estate tapes are the disjoint regime a fresh checkpoint has not seen; the driver is disjointness plus quality, not the calendar date itself. The fold finding and this paper agree on the deeper law: measure the checkpoint's exposure, not the vendor label. Single-paper evidence, pretraining context not SFT, so this is a refinement to carry into the corpus doctrine, not a settled law.

## Banked items (8, strongest first)

1. 2610.01493 No Model Required: Text Entropy Rate Filtering Mitigates Iterative Fine-Tuning Collapse (2026-10-01). Free model-less entropy-rate filter stops self-distillation collapse; the direct counter-weapon to the mem0 flattens-progressive-phrasing class for the seat-tape organ. Quote: "converges almost surely to the entropy rate H of any stationary ergodic process" (method claim via fetch relay). Overlap: 1 catalog hit, today's abstract snapshot only.
2. 2609.10750 When Synthetic Data Hurts: On Catastrophic Forgetting in Skill Retrieval for LLM Agents (2026-09-09). Production agent fine-tuned on synthetic self-data forgets OOD; rank beats regularizers. Quote: "LoRA rank r is the primary factor controlling the performance-retention trade-off". Overlap: zero hits, new.
3. 2609.23916 Time-Incremental Continued Pretraining (2026-09-20). Recency question answered mechanistically: saturation, not date; forgetting is disjoint-regime property. Quote: "Plasticity therefore tracks how far past compute-optimal a checkpoint was trained, not how much compute it consumed." Overlap: abstract snapshot in catalog ingest only.
4. 2609.24186 LIMIT: Less Is More for Instruction Tuning in Text-to-SQL (2026-09-21). 796 curated samples at near parity with 24,457; coverage-weighted genetic selection; task metrics (EX) not loss. Quote: "careful data curation, rather than scale, is the key to efficient Text-to-SQL learning." Overlap: zero hits, new.
5. 2609.06986 Continual Learning Mechanisms Compose for Long-Horizon Memorization (2026-09-07). Replay + merged-LoRA super-additive, 1.2 to 34.9 percent retention at 100 tasks; general capability still degrades. Quote: "The data anchor and merged LoRA provide the largest average gains and interact super-additively on all three datasets." Overlap: zero hits, new.
6. 2609.12353 SynthSentry (2026-09-11). Corpus-level contamination screen before training, calibrated thresholds. Quote: "We frame screening as a data-curation defense rather than a post-hoc diagnosis and release the scoring toolkit." Overlap: zero hits, new.
7. 2609.15309 When Agents Slow Down (2026-09-14). Elo-per-token eval instrument; agents fall below sampling reference, humans superlinear. Quote: "the strongest historical human contestants improve superlinearly over contest time". Overlap: zero hits, new. HTML 404'd; read via abs page.
8. 2609.27262 Can One Adapted Model Do It All? (2026-09-23). Multi-task FT beats specialist adapters at all sizes on Gemma-3 class models; sequential LoRA preserves skills. Quote: "multi-task full fine-tuning is the strongest operational default at every model size we test". Overlap: abstract snapshot in catalog ingest only.

## Honest limits

- Quotes passed through the WebFetch reading model (it refuses >125-char excerpts); they are short verbatim sentences as returned per-page, not my direct byte reads. No quote is hand-invented.
- WebSearch door dead this window (1302 x5), arXiv /list pages not fetched (API door sufficient). Both stated rather than papered over.
- 2609.15309 was read at abstract level only (full-text HTML 404). 2609.12353 and 2609.27262 same. The other five were read end to end.
- RQ4 generalization rests on one paper plus the banked fold finding; marked refinement, not law.
