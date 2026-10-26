# B2-09 receipt: prompt-uplift-lane deep dive (2026-09-26)

## Verdict

steal

## Evidence

All three OWED items from the 09-25 pass-b receipt resolved full-text today.

Kim CVPR 2026 = arXiv 2512.03534, method PRIS: it "revises the original prompt p into a revised prompt p'" that "explicitly reinforces overlooked elements while preserving those already well addressed"; its EFC verifier uses "a set of verifiable atomic semantic elements" with NLI labels; yet "nothing constrains exact wording" and with no failing element "PRIS instead treats the prompt itself as the refinement target." No saturation criterion.

VisualPrompter = arXiv 2506.23138v2 (ICLR 2026): TSPO "retains textual descriptions that are already accurately reflected in the generated images to avoid unnecessary modifications"; "if no missing concepts are detected, no further modifications will be made"; no verbatim guarantee; Appendix L admits "the use of the same VLM for both the internal optimization feedback and the final evaluation may introduce potential bias."

GEPA = arXiv 2507.19457, Observation 4: "prompts produced by GEPA and GEPA+Merge are up to 9.2× shorter than those from MIPROv2." Pass-b's watch item ("9.2x longer") is INVERTED; full text kills it. GEPA mutates instructions only; MIPROv2 "jointly optimizes both instructions and demonstrations."

VQQA re-verified first-hand (2603.12310 s3.2.2): the rater "assesses each candidate against the original prompt p0" and the judge prompt closes "Respond with only a number between 0 and 100." Appendix D.2 shows the prompt substantially rewritten every iteration: no candidate-side lock.

Consumer guard-check, full docs: Vertex improves "the system instructions," no protected-section feature; Anthropic's improver "Rewrites the prompt" and mutates examples ("Example enrichment"), no preservation statement. New to the class, TARA (arXiv 2607.18724): "adopts the repair iff s(x̂)>s(x0) and otherwise reverts"; "This accept-or-revert regression guard is not a best-of-N selector"; gate removal costs 3.6 points in ablation.

## Steal or Vacuous

Steal: three law rulings, two fresh failure modes.

1. Law 1 HOLD, split in two: judge-side ANCHOR (VQQA p0 scoring, now first-hand canon) versus candidate-side LOCK (ships nowhere; PRIS and VisualPrompter rewrite freely). FAIL(BIB_LAUNDER) survives as the lock; GEPA proves instructions-only mutation is implementable.
2. Law 3 HOLD, stronger than the class: all three academic judges are score-only or label-only (number, binary VQA, NLI count). Amendment: the judge seat returns element + quote + verdict. "Only a number" is the named anti-pattern.
3. Law 5 extension: PRIS regenerates with "the top-k noise seeds," seed-paired so the delta measures the prompt, not noise. New sub-clause: hold generation seeds fixed across candidate prompts.
4. FRESH MODE, comparative snippet inversion: pass-b read GEPA's 9.2x as longer; full text says shorter than MIPROv2. A snippet stripped of its comparative frame flips direction. Trust bytes, not reports.
5. FRESH MODE, anchor asymmetry: the whole class anchors judges and unlocks candidates. Anchor without lock is half a law.
6. TARA enforcement: flag-only is insufficient; adopt-iff-score-improves-else-revert is the shipped pattern.
7. Valora lens HOLD: entropy gate confirmed twice ("no further modifications"; PRIS acts only under 50 percent); judge independence named by VisualPrompter Appendix L.

## Falsifier

none proposed (no build). Kill condition: a shipped optimizer that natively locks a user-fact block, or hard-anchors candidates to p0, demotes FAIL(BIB_LAUNDER) from law-patch to interop note. TARA is the closest live threat.

## Bibliography

Closed; read today (2026-09-26):

- roblox/prompts/: README, ONE_SHOT_GAME, DETAIL, PORT_GAME, CLONE_WHEEL, NPC_HEAD
- watch/inbox/: BURN_prompt-uplift-lane_20260925.md and _b.md; SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md (sections 3, 5)
- arxiv.org/html/2603.12310v1 (VQQA); 2507.19457 html plus abs plus HF mirror (GEPA, corroboration); 2512.03534v1 (PRIS); 2506.23138v2 (VisualPrompter); 2607.18724v1 (TARA); export.arxiv.org API (2 queries)
- docs.cloud.google.com Vertex AI Prompt Optimizer overview; claude.com/blog/prompt-improver
- Dead ends: platform.claude.com prompt-engineering page (best practices, not the improver); arxiv.science home; alphaxiv.org/abs/2603.00483 (timed out, unread)
