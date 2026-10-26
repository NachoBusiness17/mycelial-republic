# BURN judge-lane-spec 2026-09-27

## Verdict

steal

## Evidence

arXiv 2609.26550, "JEV-as-a-Judge: Accept When Confident, Escalate When Unsure" (Li, Miao, Krishnan, Padman, submitted 22 Sep 2026), abstract: "within three percentage points of a state-of-the-art LLM judge, our strongest comparator, on ordinary preference and evidence-grounded factuality at 0.36% of the comparator's fee." Also: "A frozen cascade that accepts confident verdicts and escalates uncertain ones retains 99% of the comparator's accuracy at lower cost." Also: "Larger gaps arise when judgments require checking a derivation or resisting an elaborately written wrong answer." Carrier-drift catch: the fleet copy (SIX_DROPS item 3, LINKS-329) says "0.36x the fee"; the source says 0.36%. Three orders of magnitude. Quote the source.

arXiv 2604.24842, "Co-Director: Agentic Generative Video Storytelling" (Song et al., submitted 27 Apr 2026), abstract: "a multi-armed bandit globally identifies promising creative directions" plus a local refinement loop against identity drift. Honesty note: the abstract page does not carry the factored-reward or MLLM-judge detail; that shape lives in the fleet receipt GOOGLE_CODIRECTOR_STEAL_20260925.md, including its pre-registered falsifier "factored rewards reduce repeat infra-class failures vs the scalar-verdict baseline (39/41 pattern)."

LEDGER.jsonl row b2-32: "two-band cascade per B2_08 item 2 with band_routine tau=0.90 on the three axes (accept/escalate), band_derivation policy always_escalate", registered in configs/lanes.yaml lines 110-145, dormant, wiring self-fed B2-108. Row b2-34: cluster organ detectors in mag/lane_runner.py, "form_over_substance = receipt_completeness >= 0.90 with build_quality <= 0.50" and "confident_and_wrong = escalation overturns of confidence >= 0.90 verdicts... calibration_tripwire > 0.15 (falsifier F2)", "organ dormant on live lanes by design".

Fresh search: judge-overconfidence calibration is an active 2026 lane (arXiv 2508.06225, "Overconfidence in LLM-as-a-Judge: Diagnosis and Mitigation", snippet-read only), but the search itself reports no match for the combination of factored verdict axes plus cascade. Nothing found supersedes the fleet spec; the confident_and_wrong tripwire is the fleet's own overconfidence diagnosis.

## Steal or Vacuous

Steal, already in canon, no new build owed. The judge lane spec is the wave's convergence: per-axis verdicts on governor-controlled axes, a two-band confidence cascade (routine tau=0.90 accepts, derivation always-escalates to frontier; the JEV result vindicates both bands), and the cluster organ between judging and proposing. All three are landed and registered (b2-32, b2-34), dormant by design until V2 emission flips. Cold edge per the ledger: no writer emits GATE_VERDICT_V2 rows, so cascade and organ consume rows nobody writes; the emitter spec is filed un-applied. Fleet action: keep falsifiers F1 and F2 armed on the 50-wide burn; correct the 0.36x-to-0.36% drift in the LINKS-329 carrier.

## Bibliography

- watch/inbox/GOOGLE_CODIRECTOR_STEAL_20260925.md
- watch/inbox/SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md
- https://arxiv.org/abs/2609.26550 (abstract page, fetched)
- https://arxiv.org/abs/2604.24842 (abstract page, fetched)
- memory/burns/LEDGER.jsonl rows b2-32 and b2-34, plus the two judge-lane-spec rows of 2026-09-26 returned by the same grep
- WebSearch results page for "LLM judge factored verdict axes confidence calibration cascade 2026" (snippet level, no page deep-read)
