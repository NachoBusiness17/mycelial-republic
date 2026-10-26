# BURN receipt: prompt-uplift-lane (2026-09-25, pass c)

## Verdict

steal

## Evidence

GEPA primary text (arXiv 2507.19457v2, "GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning", Agrawal et al., ICLR 2026 Oral; HTML full text read 2026-09-25, cross-checked on ar5iv). This resolves pass b's watch item, and the direction INVERTS.

1. Observation 4: "prompts produced by GEPA and GEPA+Merge are up to 9.2x shorter than those from MIPROv2" (Figure 18). Confirmed identically across arxiv HTML (two passes) and ar5iv. Pass b's snippet reading ("9.2x longer/more detailed") is refuted: the figure is real, the comparator was flipped by the secondary summaries. Related, same observation: GEPA-style instructions "are often much shorter and thus computationally more efficient than few-shot demonstration prompts", "reducing runtime cost for downstream tasks (as all API-providers meter the input tokens), but also decreasing latency."
2. Compactness is empirical, not enforced: reflectively evolved instructions "maintain compactness while providing large performance gains", and "optimizers that achieve higher performance tend to produce shorter prompts" (Figure 17). No length constraint, penalty, or parsimony metric appears anywhere in the algorithm. Appendix E, Figure 15 caption: "GEPA consistently produces prompts that are around less than 33% of the size of" MIPROv2's prompts.
3. Budget accounting counts rollouts and dollars, not downstream tokens: a rollout is "invocations of" the policy "plus evaluation by" the metric, capped by "#rollouts <= B"; Appendix E.3 reports GEPA ~$86 vs MIPROv2 ~$76, total under $500 (single-read figures). Prompt tokens are never itemized, and prompt growth relative to GEPA's own SEED prompt is never reported; every length comparison is against MIPROv2's few-shot prompts.

## Steal or Vacuous

1. Watch item WITHDRAWN. Pass b's "GEPA prompt inflation, 9.2x longer" is refuted by primary text; the ledger's only prompt-inflation charge against the optimizer class falls. Correct the record.
2. The inversion is the receipt for law 3 applied inward: a numeric claim with a direction (X times longer/shorter) is CLAIMED until the primary sentence is quoted. Pass b held the item at snippet scope with full text owed; that discipline is exactly what caught the flip. Adopt as canon: direction-bearing figures never graduate from snippet reads.
3. Inverse steal: the class's own parsimony observation ("higher performance tends to shorter prompts", Figure 17) corroborates the fleet's brevity law from outside. But its compactness is an outcome, not a mechanism: nothing enforces it, budget is rollouts, and the seed-prompt growth curve is unreported. Law 1's capped tail remains the only enforced length control in play; keep it that way when borrowing optimizer moves. FAIL(BIB_LAUNDER) from pass a stands unchallenged: no bibliography guard exists in GEPA either.

## Falsifier

none proposed

## Bibliography

Closed. Read in full (repo): roblox/prompts/README.md, DETAIL.prompt.md, CLONE_WHEEL.prompt.md, ONE_SHOT_GAME.prompt.md, PORT_GAME.prompt.md, NPC_HEAD.prompt.md; watch/inbox/SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md (sections 3, 5); watch/inbox/BURN_prompt-uplift-lane_20260925.md; watch/inbox/BURN_prompt-uplift-lane_20260925_b.md.

Web (2026-09-25): https://arxiv.org/abs/2507.19457 (abstract); https://arxiv.org/html/2507.19457v2 (full text, two extraction passes); https://ar5iv.labs.arxiv.org/html/2507.19457 (full text, cross-check).

Carried from pass b, now flagged direction-inverted hearsay, superseded by primary text: dspy.ai Optimizers page; particula.tech GEPA vs MIPROv2 comparison. Still OWED: VisualPrompter OpenReview full text; Kim CVPR 2026 PDF.
