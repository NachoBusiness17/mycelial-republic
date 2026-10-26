# BURN receipt: prompt-uplift-lane (2026-09-25, pass b)

## Verdict

steal

## Evidence

VQQA full text (arXiv 2603.12310v1, "VQQA: An Agentic Approach for Video Evaluation and Quality Improvement", Yiwen Song, Tomas Pfister, Yale Song; HTML full text reachable 2026-09-25). Global Selection confirmed, section 3.2.2: "The rater assesses each candidate against the original prompt p0" and "the final selection remains anchored to the user's primary goals." A Global VLM Rater scores the candidate set across refinement iterations; the ablation "We disable the Global Rater and simply accept the output of the final iteration" shows a drop the authors read as semantic drift. Affiliation is not shown in the HTML (renders as a broken variable); "Google" remains secondhand via six drops section 5.

This resolves owed item (a) of BURN_prompt-uplift-lane_20260925.md, which had the anchor rule "only partially corroborated by the snippet." Owed items (b) Kim CVPR 2026 PDF and VisualPrompter OpenReview full text remain unreachable, still OWED.

One fresh web search (2026-09-25): the optimizer class state of the art is DSPy GEPA (reflective, produces prompts "up to 9.2x longer/more detailed", +14% aggregate vs MIPROv2's +7%, per ICLR 2026 paper as surfaced in search snippets) and MIPROv2 (Bayesian instruction rewrite). No tool in the results ships any guard protecting a FACTS block or closed bibliography from the rewrite. Search summaries are snippet-level; GEPA figures are secondhand.

## Steal or Vacuous

1. Owed item RESOLVED: the anchor clause on law 1 (candidates scored against the ORIGINAL prompt, never against the previous candidate) is now full-text canon, not snippet hearsay. VQQA section 3.2.2 is the citable receipt.
2. FAIL(BIB_LAUNDER) patch named for the whole class: GEPA and MIPROv2 rewrite whole prompt text by design (GEPA's own win is length inflation). No bibliography guard exists anywhere in the class. The pass-a rule stands, now scoped to every optimizer: optimizer touches structure and instructions only; FACTS and bibliography lines carried byte-verbatim into every candidate; any delta is FAIL(BIB_LAUNDER). Applies to DSPy optimizers and the consumer Prompt Optimizer alike.
3. New watch item, snippet-level: GEPA's benchmark win rides prompt inflation (9.2x longer). Unbounded tail growth fights law 1's capped tail. Filed as a watch, not a law; GEPA full text owed before it becomes canon.

## Falsifier

none proposed

## Bibliography

Closed. Read in full this pass:
- roblox/prompts/README.md, DETAIL.prompt.md, CLONE_WHEEL.prompt.md, ONE_SHOT_GAME.prompt.md, PORT_GAME.prompt.md, NPC_HEAD.prompt.md
- watch/inbox/SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md (sections 3 and 5)
- watch/inbox/BURN_prompt-uplift-lane_20260925.md
- https://arxiv.org/abs/2603.12310 (abstract) and https://arxiv.org/html/2603.12310v1 (full text)
- https://arxiv.org/abs/2604.13452 (CANVAS: Continuity-Aware Narratives via Visual Agentic Storyboarding; different paper than the topic brief implied, same author group, no Global Selection)

Snippet-level, 2026-09-25 search (full texts OWED): dspy.ai Optimizers page; GEPA ICLR 2026 paper summary; particula.tech GEPA vs MIPROv2 comparison.
