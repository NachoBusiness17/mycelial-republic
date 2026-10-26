# BURN rsi-harness _b — 2026-09-25

## Verdict
steal

## Evidence
- arXiv abs 2609.24972: title is "RRSI: Regularized Recursive Self-Improvement of Agent Harnesses", 14 Google authors, v1 21 Sep 2026, v2 23 Sep 2026. The prior burn's secondary title ("Improving Agent Harness Evolution") is superseded by the primary.
- Full text (arXiv html v2), on gates: acceptance requires the noise-adjusted floor (Eq. 5, score at least running best minus noise band); above-band gains face "additional inference cost must be justified by measurable performance improvement" (ΔC ≤ β0 + β1ΔS); within-band candidates need "w_s ΔS − w_c ΔC + w_n ν_t(H′) > 0" and "the coding instance sets w_s = 0". "If none is admissible, the incumbent is retained."
- Full text, on human/regression gates: "held-out and OOD benchmarks are not used for tuning". No human approval, held-out regression check, or merge gate appears anywhere in the loop; the only pre-evaluation screen is an automated LLM leakage critic that "rejects edits that explicitly encode task names, entity names, task-specific values, answers".
- Full text, evolve set: "The 160 tasks are partitioned once into a 120-task evolve set and a 40-task held-out set, and the partition is fixed for the experiment." Failure traces feed the proposer; the task set never grows. Paper concedes the payoff shape: "large in-distribution gains that shrink or even vanish on out-of-distribution benchmarks".
- Web search for amendment/merge gates for self-improving agent systems (2026-09-25): backend rate-limited once, then returned only irrelevant results (drill bits, OSRS guides, unrelated science.gov pages). No admissible result to fetch. Filed as owed: late-Sept-2026 state of agent-authored PR merge policy is uncovered, unfetched, unsynthesized.

## Steal or Vacuous
Steal, one confirmation and one sharpening.
1. Gateless is now primary-source fact, not secondary coverage. RRSI gates its loop with regularization only (noise floor, cost cap, leakage critic, pruner, annealed edit budget) and pays with a fixed evolve set plus admitted overfitting risk. This strengthens the prior burn's LAW-11 case: the frontier runs the loop with no human gate and no growing scenario set. Our promote --apply plus evals-from-traces lane is the alternative; LAW-11 amendment_gate must encode the regression criterion, not just a signature.
2. The w_s = 0 detail is the sharpest steal: in their coding instance a within-noise score bump alone cannot admit a candidate. Fleet translation: an amendment that misses the dual-runtime bar cannot be admitted on novelty or cost vibes. Write the LAW-11 acceptance as non-compensatory (no trading runtime health against cost or novelty), same form as their floor.
Registry gains nothing new this pass; the LAW-11 draft text is the deliverable, falsifier already pre-registered in BURN_rsi-harness_20260925.md.

## Falsifier
none proposed

## Bibliography
1. watch/inbox/SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md, section 4, repo, read 2026-09-25
2. memory/law/registry.json, repo, read 2026-09-25
3. watch/inbox/BURN_rsi-harness_20260925.md, repo, read 2026-09-25
4. https://arxiv.org/abs/2609.24972, fetched 2026-09-25
5. https://arxiv.org/html/2609.24972v2, fetched 2026-09-25
(Web search returned no admissible source; none cited. Owed: fresh coverage of agent PR merge gates.)
