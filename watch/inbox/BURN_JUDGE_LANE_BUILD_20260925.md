# JUDGE LANE BUILD ORDER: 2026-09-25

**Spec sources:** GOOGLE_CODIRECTOR_STEAL_20260925.md + SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md (Google co-director factored reward, CMU JEV cascade, muratcan RSI harness). **Ground:** the fleet already trails gate verdicts (`mag/lane_runner.py` `gate_drop` trails `GATE_VERDICT` rows); this build upgrades the verdict shape, not the plumbing.

## 1. Three-axis verdict schema (JSON contract)

Every judge lane returns exactly this object, replacing scalar ok/fail:

```json
{
  "verdict_id": "uuid4",
  "ts_utc": "2026-09-25T12:00:00Z",
  "lane": "build",
  "task_ref": "queue/handoff/<drop-id>.json",
  "axes": {
    "brief_fidelity":   {"score": 0.0, "confidence": 0.0, "evidence_quote": "verbatim line from the brief or the output"},
    "build_quality":    {"score": 0.0, "confidence": 0.0, "evidence_quote": "verbatim"},
    "receipt_completeness": {"score": 0.0, "confidence": 0.0, "evidence_quote": "verbatim"}
  },
  "failure_class": "infra|merit|none",
  "failure_detail": "one line, taxonomy-matched",
  "judge_seat": "local|flash|frontier",
  "escalated_from": null
}
```

Scores are 0.0..1.0. Confidence is the judge's own calibrated certainty. **Every non-1.0 score must carry an evidence quote** (the evidence-quote falsifier law; a score-only judge is a lens with no quote, per the prompt-uplift burn).

**Escalation rule (JEV cascade):** the local/flash judge runs first. Escalate to the frontier judge when ANY of: (a) any axis confidence < 0.7; (b) any axis score < 0.5 AND confidence > 0.7 (confident failure: the expensive re-derivation cases, JEV's known residual); (c) `failure_class` requires checking a derivation (math, protocol proofs, security claims). Otherwise accept. **The judge never moves its own gate** (judge-lane-spec burn): thresholds live in `configs/lanes.yaml`, writable only by the governor.

## 2. Failure clustering (the standing organ)

The muratcan fold: cluster before propose, not once by hand. Append every verdict row to the lane's own trail, plus a rolling cluster step in the lane runner:

> **Canonical verdict store (amendment 2026-09-26, burn lane B2-192):** verdict rows live in
> `queue/lanes/<lane>/trail.jsonl` (the file the lane runner's `_trail`/GATE_VERDICT and
> GATE_VERDICT_V2 writers actually append to, and the only store the B2-34 cluster organ
> reads). The original sentence naming `memory/law/enforcement_trail.jsonl` was stale spec:
> that file is the LAW-enforcement trail (mag/law.py TRAIL, 935 law rows, zero verdict rows
> at amend time), a different schema. No verdict-row appender is to be pointed at it; the
> lane trail is canonical for verdicts.

- Key rows by `failure_class` + normalized `failure_detail` (strip lane ids, ts, paths; keep the verb: `timeout`, `200-error-body`, `404`, `empty_content`, `parse-fail`).
- Emit `CLUSTER_REPORT` every N=20 verdicts: counts per class, repeat-rate per class vs the previous window.
- **Alarm:** if infra-class repeat rate > 60% in a window (the 39/41 shape is 95%, so 60% is conservative), the cluster report becomes a P1 fix-order for the pipe, NOT a task for the chooser. Merit-class rows route to the chooser; infra-class rows route to pipe repair. This is the split the scalar verdict hid.

### 2b. Cluster detectors (amendment 2026-09-26, burn lane B2-34; spec filed BEFORE the code it owns)

Amends section 2 only. The CLUSTER_REPORT the lane runner emits every N=20
verdicts carries two detectors on top of the class counts and repeat rates:

1. **form_over_substance**: the elaborate-wrong-answer shape. A verdict row
   matches when `axes.receipt_completeness.score >= 0.90` AND
   `axes.build_quality.score <= 0.50`. The detector fires when the window
   contains >= 1 match; it lists the matched verdict ids (bounded 10) and
   routes `spot_check`. A flagged verdict is NEVER auto-accepted by anything:
   a complete receipt is not a built thing. JEV ground (arxiv 2609.26550,
   html read 2026-09-26): "JEV scores 84.0% when the two answers share a
   style but 74.8% when the rejected answer is the more elaborately written
   one"; reference-free prose judging sits near chance ("no threshold helps").
2. **confident_and_wrong**: escalation overturns of confidence >= 0.90
   verdicts. A pair (V1, V2) matches when V2.escalated_from == V1.verdict_id,
   max(V1 axis confidences) >= 0.90, and V2's final decision differs from
   V1's proposed decision (proposed/final = accept iff every axis score >=
   tau 0.90 AND failure_class == "none"; anything else rejects). The
   detector reports count and rate; the rate is computed only at >= 10
   matched escalation events (pass-e convention: never gate a rate below 10
   events). At rate > 0.15 the report sets `calibration_tripwire: true`,
   falsifier F2 (watch/inbox/burn_wave_20260926/B2_08_judge_lane_20260926.md):
   above that, local confidence is uncalibrated and all verdicts defer to
   frontier until recalibration. JEV ground: "JEV is wrong on a third of the
   pairs it scores in [0.9,0.95)"; "a typed probability output alone does not
   establish that it is calibrated."

Frozen constants (registration values; the governor may move them into
configs/lanes.yaml `gate_verdict_v2` later, same writable_by law):
CLUSTER_WINDOW_N=20 · INFRA_REPEAT_ALARM=0.60 · MIN_RATE_EVENTS=10 ·
FOS_RECEIPT_HIGH=0.90 · FOS_BUILD_LOW=0.50 · CAW_CONF_HIGH=0.90 ·
CAW_TRIPWIRE=0.15 · CLUSTER_TAU=0.90 (mirrors
gate_verdict_v2.cascade.band_routine.tau, B2-32 registration).

Scope + honesty: the organ consumes GATE_VERDICT_V2 rows (nested `verdict`
object, pass-c draft shape) from `queue/lanes/<lane>/trail.jsonl`, the file
gate_drop actually trails. The lane runner still emits scalar GATE_VERDICT
rows (configs/lanes.yaml gate_verdict_v2 comment: "wiring this block into
code is a separate gated lane"), so the organ is DORMANT, an honest no-op,
until V2 rows exist; correctness is proven by replay tests over the frozen
schema, never by invented verdicts. Repeat-rate semantics stay as section 2
wrote them (per class vs the previous window); pass d's intra-window repeat
(key fires >= 2 in-window) is REPORTED beside it, never gated. Pass-e
proposed MSR classes (duplicate, agent_misalignment) are NOT canonical here:
pass e's own receipt re-proposes them as a writer default first; the organ
keys whatever failure_class a row carries and never crashes on unknown
values (unclassified keys land in their own bucket).

Sources for 2b (read 2026-09-26): arxiv.org/html/2609.26550 (quotes verbatim
above) · watch/inbox/burn_wave_20260926/B2_08_judge_lane_20260926.md ·
watch/inbox/BURN_judge-lane-spec_20260925_c.md ·
watch/inbox/BURN_judge-lane-spec_20260925_d.md ·
watch/inbox/BURN_judge-lane-spec_20260926_e.md · configs/lanes.yaml
gate_verdict_v2 · mag/lane_runner.py gate_drop + _trail · tools/drift.py
(VACUOUS verdict-shape precedent).

## 3. Chooser update rule (per-axis bandit)

The governor treats each axis as its own bandit arm set over lanes/tiers (Google fold: reward factored along the dimensions the chooser controls):

- On each verdict, for each axis: `arm_value[lane][axis] += (score - arm_value[lane][axis]) * alpha`, alpha = 0.1 (recency-weighted; the thought-quantizer weight law).
- Lane selection for the next task: sample softmax over `mean(axes)` with exploration floor epsilon = 0.2, but **infra-class failures do not lower `build_quality`**; they lower a separate `pipe_health` scalar that gates lane dispatch (a lane with dead pipes gets repaired, not avoided).
- A3 containment: per-axis rewards move lane/tier choices only. They never alter agent identity, prompts-of-record, or the constitution. The bandit is a meter that steers, not a government.

## 4. Pre-registered falsifier (50-wide burn)

Baseline: scalar-verdict rejection taxonomy, 41 rows, 39 infra / 2 merit (95.1% infra). Run one 50-wide burn with the three-axis schema wired. **Pass:** infra-class repeat rate across the burn's verdict rows drops below 70% (i.e. clustering + pipe-routing visibly drains the infra class), AND at least 20% of escalated verdicts are overturned-or-upgraded by the frontier judge (cascade is doing real work). **Fail:** infra repeat rate stays > 85% (scalar-level) or escalations are 100% upheld (escalation is theater). Either fail result files the schema as vacuous and reverts to scalar + manual cluster reports.

## Bibliography (closed)

- watch/inbox/GOOGLE_CODIRECTOR_STEAL_20260925.md (read)
- watch/inbox/SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md (read)
- mag/lane_runner.py `gate_drop` (read, lines 169-192)
- watch/inbox/REJECTION_TAXONOMY_20260917.md (read, grep-verified lines 5, 21, 29)
