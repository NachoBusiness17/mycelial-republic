# SPOT-CHECK PROTOCOL (falsifier F2, judge lane) - B2-193, 2026-09-26

F2 (B2_08_judge_lane_20260926.md:31): "if >15% of confidence >= 0.9 verdicts
overturn at spot-check, local confidence is uncalibrated; all verdicts defer
to frontier until recalibrated." Until now F2 had no sampler, no sample size,
no filing home, and no denominator. This protocol pins all four.

## The four definitions

1. DENOMINATOR: all GATE_VERDICT_V2 verdicts whose max axis confidence is
   >= CAW_CONF_HIGH (0.90, mag/lane_runner.py) in the population being
   judged - NOT all verdicts, NOT only escalated verdicts. The automatic
   confident_and_wrong detector (escalation-parent proxy, rate over
   MIN_RATE_EVENTS=10 events) stays the always-on tripwire; the spot-check
   rate is the calibration verdict of record.
2. WHO SAMPLES: the rolling cluster organ (mag/lane_runner.py
   cluster_report_step) samples automatically - every CLUSTER_REPORT carries
   up to SPOTCHECK_SAMPLE_K=5 verdict_ids, chosen deterministically (first K
   window verdicts whose max axis confidence >= 0.90). No RNG, no pinning
   disputes; the sample is a byproduct of the report the lane already files.
3. WHO EXECUTES: the operator is the spot-checker of record (re-judge the
   original gate input independently; the residual file is the input). The
   local janitor tier (ollama) may pre-score to save operator time, but a
   janitor re-score is recorded as assistance, never counted as calibration:
   F2 is about local confidence lying, and a second local opinion cannot
   calibrate the first.
4. HOW MANY: a calibration verdict needs at least 20 executed spot-checks
   since the last calibration verdict (aligns with MIN_RATE_EVENTS=10 so the
   rate denominators are never toy samples; 20 gives a 95% binomial bound of
   roughly +/-15 percentage points at p=0.15). Short of 20 at pass close, the
   pass files the shortfall and F2 stays OPEN, never quietly closed.

## Filing home

- Execution rows: watch/inbox/SPOTCHECK_<lane>_<yyyymmdd>.jsonl, one JSON row
  per executed spot-check: {"verdict_id", "window_ts", "original_decision",
  "spotcheck_decision", "overturns": bool, "by", "ts", "note"} (append-only).
- The CLUSTER_REPORT (queue/lanes/<lane>/surface) carries the sample that
  created the obligation; the executed file is the discharge.
- The B2-113 falsifier run reads the SPOTCHECK_*.jsonl files, computes
  overturns / executed (denominator rule 1+4), and files the calibration
  verdict in its pass receipt. >= 0.15 overturns = F2 fires (all verdicts
  defer to frontier until recalibration).

## Decidability

cluster_report_step now emits, inside every CLUSTER_REPORT JSON, a
"spot_check" section: {sample_ids, sample_k, population, protocol}. A pass
cannot claim calibration without discharged samples; a discharged file whose
verdict_ids do not appear in some CLUSTER_REPORT is void (no spot-checks
without a sampled obligation).
