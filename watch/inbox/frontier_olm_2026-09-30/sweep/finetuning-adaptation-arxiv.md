# SWEEP: finetuning-adaptation via arXiv - frontier_olm 2026-09-30

source-fetched: 2026-09-30. Seat: sweep gopher (finetuning-adaptation area). Every quote below was pulled by my own fetch calls this session; every estate number was read from repo bytes this session.

## Doors: what worked, what degraded (per the fetch recipe, no invented fallbacks)

- export.arxiv.org API (primary door): DEGRADED all session. First call HTTP 503 (Retry-After: 0), retry HTTP 429, retry timed out at 60s WebFetch limit, final id_list retry HTTP 503. Zero successful API responses.
- arxiv.org/list/cs.CL/2609 (monthly): HTTP 404. arxiv.org/list/cs.CL/recent/skip=50 (pagination): HTTP 404.
- WORKING doors used instead (recipe's named fallbacks): arxiv.org/list/cs.CL/recent (full 50-entry title list fetched), arxiv.org/list/cs.LG/recent (50-entry list fetched), arxiv.org/abs/<id> and arxiv.org/html/<id>v1 for deep reads, WebSearch (site:arxiv.org filter 1302-rate-limited twice; broadened queries worked).
- WebSearch site:arxiv.org QLoRA query surfaced non-arXiv leads (OpenReview "Zero-Search Recipe for Fast Quantized LoRA", ResearchGate "Learning New Facts with QLoRA: Acquisition-Retention Frontier", ResearchSquare LoRA-vs-FFT medical QA, LowRA 2-bit): NOT verified on arXiv this session, NOT banked, listed as OWED leads.

## Pass 1 - candidates considered (last 30 days; arXiv IDs)

From cs.CL/recent + cs.LG/recent full lists and searches, 34 considered:
2609.10750, 2609.37807, 2609.38027, 2609.37891, 2609.37914, 2609.37624, 2609.37510, 2609.37915, 2609.38025, 2609.38104, 2609.37371, 2609.38137, 2609.37930, 2609.38021, 2609.37501, 2609.37498, 2609.37887, 2609.37868, 2609.37858, 2609.37852, 2609.37842, 2609.37836, 2609.38011, 2609.37469, 2609.37443, 2609.37635, 2609.37755, 2609.37713, 2609.37361, 2609.38169, 2609.38166, 2609.38121, 2609.37976, 2609.37924. Out-of-window leads seen and excluded from banking: 2603.08647 (Grow Don't Overwrite, Mar), 2601.18699 (Jan), 2506.01732 (Common Corpus, Jun), 2501.05465 (SLM survey).

## Pass 2 - deep reads (5 full-text end to end + 3 thorough abstract-level reads)

Full-text (arxiv.org/html): 2609.10750, 2609.38027, 2609.37868, 2609.37510, 2609.37807. Abstract-level with full numbers: 2609.37836, 2609.37914, 2609.37624. All 8 banked items below were read by me; the 4 non-full-text ones are marked in confidence.

## Q1 - QLoRA/LoRA recipes since 09-28 for absorbing session-tape corpora with measured retention

**2609.10750 "When Synthetic Data Hurts: On Catastrophic Forgetting in Skill Retrieval for LLM Agents" (2026-09-09) is the sweep's anchor find, zero overlap with our holdings.** It is structurally our exact problem: a production skill router over 34,396 skills, a 0.6B Qwen retriever+reranker, scarce real supervision (~273 positive pairs from real trials), padded with synthetic pairs (Tracks A/B, ~15K/~14K rows). Findings, read from the full text:
- Aggressive recipe (all-projection LoRA rank 16/32, lr 2e-5) improves in-distribution retrieval but drops OOD recall 0.8500 to 0.650 (23.5 percent drop, Wilcoxon p=0.0312) and hurts all six BEIR datasets.
- Conservative recipe (rank 8, attention-only, lr 5e-6) plus ANY ONE of: embedding-anchor regularization, LwF (T=2.0), EWC, or L2-init keeps OOD exactly at frozen-model level (Ring 3 = 0.8500 identical to frozen) while lifting synthetic in-distribution recall ~13.98 percent relative.
- Their stated knob law: "LoRA rank r is the primary factor controlling the performance-retention trade-off, whereas anchor weight (lambda) has only a minor effect."
- Deployed stack: anchor-regularized retriever + listwise-LwF reranker, ~169 ms p50, ~4.3 GB, and a frozen-retriever fallback for long-tail skills (positive coverage was only 0.52 percent of the catalogue).
Map to the estate: the 11,870 seat_pool rows (lens corpus.md:12, verified this session) are the same shape as their Track A/B synthetic-plus-real mixture. The transferable recipe: conservative rank 8, keep a frozen fallback, and treat real verified pairs as the retention anchor set.

**2609.38027 LIFT (2026-09-28)** adds the placement recipe: LoRA only on functionally critical layers found by AWQ sensitivity probing; 10.5M trainable vs 167.8M full-layer LoRA on Llama-3 GSM8K, beating full fine-tuning on most tasks (73.96 vs 67.76) at ~11.4 percent less training time. No retention experiments in the paper (honest gap), so bank it as a cost recipe, not a retention recipe.

## Q2 - which estate corpora are corpus-grade vs echo-inflated (content-read audit)

In-window literature gives the audit protocol, not a verdict on our corpora (I did not content-read seat_pool rows; OWED):
- 2609.37807 CompOrca (full text): row-level labelling of all 4,233,923 OpenOrca examples via five independent judge passes; unanimous labels are 97.3 percent precise (compliance) / 86.7 percent (noncompliance); single-pass flags are 52-60 percent unstable ("Repeated passes do not produce better labels, but exclude the 3.97% of rows on which the judge is unstable"). Pipeline cost: 21.17M classifications, 15.19B tokens, ~101 GPU-hours-class active time.
- 2609.37624 Correct Don't Delete (abstract read): on Qwen2.5-14B, correcting a quarter of poisoned rows cuts emergent-misalignment ~one-third while deleting the same rows shows little effect; "In the settings we tested, correcting harmful training data reduces EM more than deleting it."
- 2609.37914 (abstract read): training-data-attribution scores can rank which fine-tuning rows drive behavior change, and filtering on them "can substantially enhance or attenuate EM".
Estate resonance: laws.md:50 (verified line) shows our own quantized-thought corpus already marks every raw_count as "inflated echo - provenance only" - the same honesty CompOrca brings. The audit recipe for 11,870 seat_pool rows: multi-pass label with unanimity gating (not single-pass), attribute before reweighting, correct rather than delete. Corpus.md:34 (verified) already flags our domain labels as path-inferred OWED, so a content-read audit is exactly the missing instrument.

## Q3 - what training/loop_gaps.jsonl shows recurs, and is it finetunable

I read all 332 lines of training/loop_gaps.jsonl this session. The recursion is dominated by four dedupe keys, loop after loop since 2026-08-06:
- lifecycle_gap:ollama ("should be on but actual off", dedupe 2b8549d4a15ab722): ~40 rows, recurs 2026-08-06 through 2026-09-30T11:45Z.
- lifecycle_waste:drainer ("should be off but still on", dedupe c6106f660fed3962, later 10bd1c26d7c1f079/dcacf6aa11dde927): ~45 rows, recurs daily, and the 09-29/09-30 rows carry signals/prev_verdict/flip:false showing the same verdict repeating across hosts (e26f592620cd, d3dd25f90a2a).
- missing_seat browser_env_not_wired (dedupe 9dbe58099056d6a9): ~15 rows.
- test_gap_unique_xyz: known unit-test pollution, annotated in place per B2-79 (no-erase law).
Verdict, stated honestly: this gap class is a lifecycle-controller state defect (a process that should be toggled is not), not a model adaptation failure and not an architecture gap - it is the third category, control-plane bug, and I found no in-window arXiv paper that classifies such harness-lifecycle regressions as finetunable. The finetunable surface in the same literature is the routing/retrieval layer (2609.10750: yes, with the rank-8 + retention-regularizer recipe) and 2609.37836 (2026-09-29) adds the caveat that even after 50,000 common updates networks retain measurable training-history residue ("behavioral convergence need not imply representational convergence") - i.e., weights fix behavior mappings, not process state. Banking "finetune the janitors to fix the drainer gap" would be a category error; the loop recurs because the controller, not a model, is wrong.

## Q4 - when distillation from funded primes beats direct dispatch, cost per correct verdict

Baseline instrument read: training/cost_ledger.jsonl rows 2410-2439 (live through 2026-09-30T12:49Z). The churn regime is already visible: deepseek rows at price_band 0.0007 with outcome success:false, waste_kind "agent_churn", usd_per_leaf null, estimate_error up to 68.0 (row 2439: 2,913,163 prompt tokens, 152 calls, 0.0483 USD, failed); ollama rows succeed at 0.0 USD. That is exactly the regime where training a local successor wins: repeated paid dispatches that end in churn.
In-window evidence on the mechanism side, read in full text:
- 2609.37868 GRAFT (2026-09-29): heterogeneous peers exchanging stored trajectories (no shared weights) keep most of the co-training gain - "+1.8 points on average" over GRPO = 84 percent of the online gain, with compute cut 27-76 percent, and 35.25 pair-mean at 40.9 GPU-hours = 0.45x the compute of GRPO n=32 while beating it by 1.18 points. Directly validates seat-tape/trajectory reuse between fleet members without a designated teacher.
- 2609.37510 MAESTRO OPD (2026-09-29): on-policy distillation with triggered teacher intervention beats plain SFT distillation badly (17.82 percent vs 27.16 vs 31.36 macro on a 0.6B student across 8 math benchmarks) at a teacher budget of only ~1.05x baseline tokens; moderate intervention raises peak accuracy, deeper intervention improves retention.
Named condition per the ONE-BUG law (laws.md:18, verified line 18): these numbers are their instruments, their moments, their GPUs (H20/H100) and math benchmarks; the estate transfer claim is scoped to "churn-regime dispatch" until replayed on our ledger. Cost-per-correct-verdict crossover is therefore OWED as a measurement: the ledger already records the denominator (usd_per_leaf on success), so the experiment is a replayed A/B, not new plumbing.

## Q5 - license/ToS screens on session-derived corpora vs the counsel triage law

The counsel triage law (laws.md:42, verified: "Licenses gate training-corpus eligibility; platform ToS gates what we scrape or automate", RIB_LAWYER_BOOT_20260904.md:8-30) is NOT yet mirrored in this window's visible arXiv dataset practice. Honest findings:
- The one corpus-scale labelling paper I read end to end (2609.37807 CompOrca) labels behavioral compliance (refusal vs attempt), explicitly with "no policy, license, or copyright-based definition"; it releases MIT-licensed labels over the already-MIT OpenOrca.
- No in-window arXiv paper applying license/ToS screens specifically to session-derived or conversation-derived corpora was found via my doors. Closest lead found outside arXiv via WebSearch: "Can Performant LLMs Be Ethical?" (OpenReview, robots.txt and browsewrap ToS discussion) - unverified on arXiv, OWED. Common Corpus (2506.01732, June 2026, outside window) established permissive-license-only sourcing but predates the window.
Verdict: the estate's law runs ahead of this window's practice; nothing in-window contradicts it, and CompOrca's unanimity-gated row triage is compatible with it as an eligibility instrument.

## Overlap register (grep evidence, run this session)

- 2609.10750: grep -cF "When Synthetic Data Hurts" = 0 and "Skill Retrieval for LLM Agents" = 0 in catalog/catalog.jsonl (691,788 rows); no memory/ hits. NEW.
- 2609.38027: "Layer-Informed Fine-Tuning" = 0, "Functional Segmentation" = 0. NEW.
- 2609.37868, 2609.37510, 2609.37836, 2609.37807, 2609.37887, 2609.37624: catalog.jsonl exactly 1 hit each = abstract stubs at state/arxiv/2026-09-30/<id>v1.txt (mtime 2026-09-30T06:31:01Z, age_days 0, 1.4-2.0 KB each, verified by row extraction). Another lane banked stubs this morning; this sweep adds the first full-text reads. memory/ hits were only my own session trajectory echo (memory/trajectory/steps.jsonl), not holdings.
- OPD neighborhood already partially mined: memory/arxiv_mine/ledger.jsonl holds "Latent On-Policy Self-Distillation" 2608.13040 (2026-08-15); catalog holds "What Does Privileged Information Add to On-Policy Self-Distillation?" (age 8d) and "BAS-OPD" (age 3d). This window's 2609.37510/37915 are still new.
- 2609.37914: catalog 1 hit (today's stub wave), no memory hits.

## OWED (not done, not guessed)

- arXiv API path never succeeded this session; if the API was transiently healthy later, additional in-window items may exist beyond the 34 considered.
- Non-arXiv QLoRA leads (OpenReview Zero-Search recipe; ResearchGate acquisition-retention frontier) not verified on arXiv; unbanked.
- No content-read of seat_pool rows; no replay A/B of distill-vs-dispatch on cost_ledger; the crossover number is OWED as a measured experiment.
- Quote fidelity: quotes were extracted from fetched pages by the fetch instrument's extraction pass and marked VERBATIM by it; I cross-checked two per paper against surrounding numbers but did not diff raw HTML bytes.
