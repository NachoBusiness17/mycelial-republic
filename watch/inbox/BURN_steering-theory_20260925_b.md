# BURN steering-theory 2026-09-25 _b

## Verdict
steal

## Evidence
- tools/drift.py: drift_check takes "numeric time series (same length, ordered oldest first)", needs ">= 3 deltas after windowing"; verdicts VACUOUS (referent never moved), ALIGNED (corr >= +0.5), DRIFTING, INVERTED (corr <= -0.5, "stop trusting the metric"). Line 83: "a rate metric answers 'is it moving'; only corr(delta-M, delta-R) answers 'is it moving north'".
- FOLD.json G31: "fit temperature on a 1k labeled set per decision class, set escalation threshold off the risk-coverage curve at target precision, refit weekly".
- arXiv 2508.06225v2 (fetched 2026-09-25; dated 11 Aug 2025): judges show "predicted confidence levels that significantly exceed their actual accuracy"; GPT-4o on JudgeBench has "high ECE values... (39.25 in SC, 47.09 in MP, 45.05 in LogP)". Confirms pair A's premise: self-confidence alone is a known-bad instrument.
- OpenReview B1ISNZQHuI ("Agentic Confidence Calibration", per snippet trains a predictor of LLM-judge correctness labels): bot-verification wall on fetch. OWED, never synthesized.
- Freshness datum: one search, nothing dated late September 2026; newest direct hit Aug 2025. Field quiet in-window; no freshness theater filed.

## Steal or Vacuous
Steal: the build step itself. These shrink the prior burn's 1k falsifier to a 20-task fast inner loop; the 1k set stays the G31 refit set. Each pair lands as label + two same-length series into drift_check.

PAIR A, label "lane=gemma4:A-conf-margin-vs-correctness". Metric sample: mean verdict-token logprob margin (p_max minus p_second) over the probe at cycle t. Referent: correct/20. Cadence: one probe per cycle, first verdict after >= 4 cycles. corr(dM,dR) expectation [+0.3, +0.8]. Kills: VACUOUS = probe saturated, referent flat >= 3 cycles (probe too easy; harden it). DRIFTING = 0 < corr < 0.5 (confidence decorative; cannot gate escalation). INVERTED = corr <= -0.5 (confidence up, correctness down: overconfidence collapse; dashboards still read healthy). Denominator law: fixed versioned 20-task probe, hash logged per cycle, never mix versions in one series; one task flip = 0.05, referent deltas < 0.1 are noise.

PAIR B, label "lane=gemma4:B-escalate-rate-vs-overturn-rate". Metric: escalated/total verdicts per cycle. Referent: frontier overturns/escalated. corr(dM,dR) expectation mild positive [0, +0.6] (tighter threshold pulls in more real doubt). Kills: VACUOUS = overturn rate flat (rubber-stamp, or total distrust; decorative either way). DRIFTING = uncorrelated movement (trigger keys on length/topic, not risk). INVERTED = corr <= -0.5: escalate-rate rises while overturn rate falls, that is escalation theater. Denominator law: two denominators per point; metric needs >= 20 verdicts, referent >= 5 escalations, else point not filed; never an overturn rate on < 5 escalations.

## Falsifier
Pre-registered: both pairs, both local lanes (gemma:2b, gemma4), >= 4 probe cycles. If BOTH pairs return only VACUOUS/DRIFTING/INVERTED on BOTH lanes, the confidence-as-drift-pair build is demoted VACUOUS and stops. One ALIGNED anywhere keeps it alive. Overfit guard: on pair A VACUOUS the probe is re-versioned immediately, refresh logged.

## Bibliography
- tools/drift.py (repo, 2026-09-25)
- memory/runs/gps_50/FOLD.json (repo, 2026-09-25)
- watch/inbox/BURN_steering-theory_20260925.md (prior burn, 2026-09-25)
- https://arxiv.org/html/2508.06225v2 (fetched 2026-09-25)
- https://openreview.net/forum?id=B1ISNZQHuI (bot wall, OWED)
- Search snippets only (futureagi.com, alphaxiv 2512.20578, ojs.aaai.org 40698): unread, uncited above.
