# BURN: judge-lane-spec pass c (2026-09-25)

## Verdict

steal

## Evidence

- mag/lane_runner.py line 169: "def gate_drop(item: dict, lane: str) -> tuple[bool, list[str]]", docstring "Returns (ok, reasons); every verdict is trailed." The row envelope (lines 85-86): `{"ts": _ts(), "actor": f"{lane}-cage", "event": event, "detail": detail[:400], "artifacts": artifacts or []}`. The 400-char detail cap means the full verdict object cannot ride in detail; it needs its own row key.
- BURN_JUDGE_LANE_BUILD_20260925.md: "Escalate to the frontier judge when ANY of: (a) any axis confidence < 0.7; (b) any axis score < 0.5 AND confidence > 0.7"; "thresholds live in configs/lanes.yaml, writable only by the governor."
- configs/lanes.yaml L2 block: "require_priority: true". Conflict: judge escalations routed to L2 would die at the priority marker gate.
- Fresh JEV calibration web search returned MCP 429 rate-limit, zero results. Filed owed; nothing synthesized.

## Steal or Vacuous

Three executable drafts. No files edited.

(a) GATE_VERDICT_V2 row as emitted into queue/lanes/<lane>/trail.jsonl (envelope unchanged, verdict nested under "verdict" to clear the detail cap):

```json
{"ts": "2026-09-25T12:00:00Z", "actor": "build-cage", "event": "GATE_VERDICT_V2",
 "detail": "<task_ref> -> PASS escalate=false axes=1.0/0.9/1.0 conf=0.9/0.9/0.9 class=none",
 "artifacts": ["queue/handoff/<drop-id>.json"],
 "verdict": {"verdict_id": "<uuid4>", "ts_utc": "2026-09-25T12:00:00Z", "lane": "build",
   "task_ref": "queue/handoff/<drop-id>.json",
   "axes": {"brief_fidelity": {"score": 1.0, "confidence": 0.9, "evidence_quote": "verbatim"},
            "build_quality": {"score": 0.9, "confidence": 0.9, "evidence_quote": "verbatim"},
            "receipt_completeness": {"score": 1.0, "confidence": 0.9, "evidence_quote": "verbatim"}},
   "failure_class": "none", "failure_detail": "", "judge_seat": "local",
   "escalated_from": null, "escalate": false, "escalate_reason": null}}
```

Delta the build order implied but never spelled: escalate + escalate_reason as derived fields. Draft axis mapping for the deterministic gate: missing field -> build_quality 0.0; anchor missing -> brief_fidelity 0.0; ttl bad -> receipt_completeness 0.0; all at confidence 1.0, failure_class infra.

(b) configs/lanes.yaml judge_gate block:

```yaml
judge_gate:
  writable_by: governor
  conf_floor: 0.7
  confident_fail_escalate: {score_below: 0.5, confidence_above: 0.7}
  derivation_class_list: [math-derivation, protocol-proof, security-claim]
  escalation_lane: L2  # conflicts with require_priority: true; governor must waive priority for judge escalations or define a judge_frontier seat
  cluster_window_n: 20
  infra_repeat_alarm: 0.60
```

(c) One signature change, gate_drop: `def gate_drop(item: dict, lane: str, cfg: dict | None = None) -> tuple[bool, list[str], dict]`, returning (ok, reasons, verdict). Callers at lines 352 (cycle_research) and 388 (cycle_builder) unpack three values.

## Falsifier

Pre-registered: replay the drafted schema over existing gate_drop verdict history. If every FAIL row escalates by rule (b) and no PASS row can ever escalate, escalate-rate is schema-determined, not calibrated: rule rows carry confidence 1.0 by construction, so the conf_floor statistic is dead on deterministic lanes. Required fix if this fires: mark judge_seat=rule rows cascade-exempt, counted in clustering but excluded from calibration stats (`cascade_exempt_seats: [rule]` in judge_gate) before any 50-wide burn.

## Bibliography

- watch/inbox/GOOGLE_CODIRECTOR_STEAL_20260925.md (read)
- watch/inbox/SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md (read)
- watch/inbox/BURN_judge-lane-spec_20260925.md (read)
- watch/inbox/BURN_JUDGE_LANE_BUILD_20260925.md (read)
- mag/lane_runner.py (read: gate_drop, _trail, _state, _save_state)
- configs/lanes.yaml (read)
- JEV cascade calibration follow-up search: owed (429 rate-limit, zero results)
