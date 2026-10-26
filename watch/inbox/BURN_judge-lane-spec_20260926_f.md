# BURN: judge-lane-spec pass f (2026-09-26)

## Verdict

steal

## Evidence

- mag/lane_runner.py:297: cluster_step is "Pure CLUSTER_REPORT computation over one window of verdict rows... Reads nothing, writes nothing." Constants :228-236: CLUSTER_WINDOW_N=20, INFRA_REPEAT_ALARM=0.60, MIN_RATE_EVENTS=10, CAW_TRIPWIRE=0.15. cluster_report_step :403 runs every cycle from run_lane ("the organ never breaks the lane loop") and returns "dormant(0 pending)" at zero verdicts.
- Probe (venv python, organ code unmodified, 249 ledger rows, MY keyword classifier supplies failure_class/failure_detail; the organ exposes none): failure rows 145/249, counts infra 71 / merit 74 / none 104; infra share of failures 49.0%. Twelve 20-windows: infra per window 3-9, all below MIN_RATE_EVENTS, repeat=None every window, route=split, alarm_windows=0, fos=0, caw_ev=0 everywhere. Half-split full ledger (infra cnt 34 clears min-events, prev window present): infra_repeat=0.0, route=split. The alarm does not fire on burn-ledger data.
- Trails: 12 lane trails (research 2001 rows, day_work 1471, builder 1012; 4,692 total); grep GATE_VERDICT_V2 across all: zero hits. Live gate still trails the scalar at lane_runner.py:190: `_trail(lane, "GATE_VERDICT", f"...{'PASS' if ok else 'FAIL: ' + ...}")`.
- Web search attempt 1 returned the infra class itself: MCP error -429 code 1302 "Rate limit reached for requests". Retry returned generic items only (arXiv LLM-as-judge grader pitfalls; preprints.org hallucination survey "cascading failures"; OpenReview rejection-sampling risk coverage). Nothing dated late September 2026 on cluster alarms; no fetch spent.

## Steal or Vacuous

Adopt:
1. Organ verified on real data: cluster_step is pure and behaves to build-doc spec over 249 real ledger rows; dormancy is byte-true (zero V2 rows in 4,692 trail rows), not asserted.
2. The alarm not firing on ledger data is instrument mismatch, not organ failure: the 95.1% baseline is a class SHARE on application-rejection populations; the organ gates a cross-window REPEAT rate of normalized detail keys at >= 10 events. Ledger one_line keys never recur verbatim (repeat 0.0 even at count 34), and ledger failures under my mapping split 49/51 infra/merit, byte-confirming pass e's "class taxonomy does not transfer": cluster keys are per-population.
3. Missing wiring named: B2-111 (V2 emitters) is the sole gap. b2-32 registered config only; the scalar gate at :190 emits no axes, confidence, verdict_id or escalated_from, so the 2b detectors (form_over_substance, confident_and_wrong) structurally cannot fire anywhere today. Fresh failure mode named: share-to-repeat instrument transposition (citing a class-share baseline from one population as the expected firing condition of a repeat-rate alarm on another).

## Falsifier

Pre-registered: wire one GATE_VERDICT_V2 emitter (B2-111) on the builder lane. Falsifier: within the first 20 V2 verdicts, cluster_report_step emits one CLUSTER_REPORT whose counts_by_class matches the trail's actual class distribution, and one deliberately injected escalation pair (parent conf >= 0.90, overturned) yields caw events=1 in the next report. Either miss means the organ does not run on live trails and the wiring build is vacuous.

## Bibliography

- Read: watch/inbox/ GOOGLE_CODIRECTOR_STEAL_20260925.md, SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md, BURN_judge-lane-spec_20260926_e.md; memory/burns/LEDGER.jsonl (b2-32, b2-34 rows; 249 rows parsed); mag/lane_runner.py :185-195, :215-464, :898-912; queue/lanes/*/trail.jsonl (grep + wc only)
- Searched: web "LLM judge cascade cluster failure alarms rejection sampling September 2026" (results listed above; none fetched)
