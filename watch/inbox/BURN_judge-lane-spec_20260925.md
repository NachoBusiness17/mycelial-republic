# BURN: judge-lane-spec (2026-09-25)

## Verdict

steal

## Evidence

**JEV-as-a-Judge** (arXiv 2609.26550, Li, Miao, Krishnan, Padman, CMU). Title: "Accept When Confident, Escalate When Unsure". Abstract opens: "LLM-as-a-judge enables evaluation across diverse tasks, but inference cost and confidence reliability become critical at scale." A decision-only judge is benchmarked against "sixteen generative and reward-model judges, with blinded human adjudication". It lands "within three percentage points of a state-of-the-art LLM judge" on ordinary preference and evidence-grounded factuality at "0.36% of the cost". The gap concentrates when judgments require "checking a derivation or resisting an elaborately written wrong answer". A "frozen cascade that accepts confident verdicts and escalates uncertain ones" retains "99% of the comparator's accuracy at lower cost", and errors "are concentrated in low-confidence decisions". Note: the inbox fold says "0.36x the fee"; both abstract reads said 0.36%. Re-verify against the PDF before the number enters canon (owed).

**Co-Director** (arXiv 2604.24842, Song, Song, et al., Google). "A hierarchical multi-agent framework" formalizing video storytelling "as a global optimization problem"; chained pipelines fail from "semantic drift and cascading failures". The fix is "hierarchical parameterization": a "multi-armed bandit" exploring "creative directions" plus "a local multimodal self-refinement loop" ensuring "sequence-level consistency". Ships GenAD-Bench, "a 400-scenario dataset of fictional products for personalized advertising". The abstract never states the factored per-dimension judge reward; that shape is blog-sourced (LINKS-326), unverified here (owed).

## Steal or Vacuous

Four adoptions the fold missed:

1. **Escalation rate is the drift instrument.** JEV's errors concentrate "in low-confidence decisions", so a rising escalate-rate on stable workload is the earliest calibration-drift alarm. The fold treats the cascade as a static win. Adopt: log escalate-rate per lane; a drift in it means the gate is going blind before accuracy does.
2. **The gate stays frozen.** "Frozen cascade" means the judge never tunes its own escalation threshold. Law: a judge that can move its own gate stops being a meter (A3 consistent).
3. **Two-loop split.** The abstract separates global exploration (bandit over creative directions) from local per-segment self-refinement against sequence consistency. Fleet mapping: the governor explores tier and config globally; each lane refines locally against the original prompt, never its previous draft. This is the loop structure that justifies the VQQA referent rule already landed.
4. **Blinded adjudication as burn protocol.** JEV validates via blinded human adjudication across sixteen judges. The next 50-wide burn should blind the human gate to which judge tier produced each verdict.

Owed: both full PDFs unread; calibration-drift handling and cross-dimension judge-disagreement resolution appear in neither abstract.

## Falsifier

Pre-registered for the judge-lane build: during the next 50-wide burn, spot-check 10% of confidently-accepted local judge verdicts against a frontier judge. Falsifier: if the accepted-verdict error rate exceeds the local judge's measured low-confidence error rate, the frozen cascade has silently inverted (confidence no longer tracks correctness on the drifted distribution) and the spec is vacuous until a recalibration loop exists.

## Bibliography

- `watch/inbox/GOOGLE_CODIRECTOR_STEAL_20260925.md` (read)
- `watch/inbox/SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md` (read)
- arxiv.org/abs/2609.26550 abstract page (read)
- arxiv.org/abs/2604.24842 abstract page (read)
