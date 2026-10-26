# BURN: judge-lane-spec pass g (2026-09-26)

## Verdict

steal

## Evidence

- Re-verified byte-true today: grep GATE_VERDICT_V2 across queue/lanes/*/trail.jsonl = 0 rows everywhere; scalar GATE_VERDICT present (builder 13, research 14). The V2 writer exists (mag/lane_runner.py gate_drop_v2 :301) but nothing calls it: gate_drop :171 emits only the scalar at :192.
- Seat wall: build_gate_verdict :237 refuses any judge_seat not in gate_verdict_v2.judge_seats [local, flash, frontier]. The b2-32 block's cascade.cascade_exempt_seats: [rule] (rule backend mag/desk_conductor.py:319) is read by no code, so no deterministic verdict can be emitted as V2.
- Callers: cycle_research :733, cycle_builder :769. The ask's "~352/388" is stale (pre-B2-111 dist_audit copy, :329/:365).
- configs/lanes.yaml gate_verdict_v2 has no emitters key; writable_by: governor.

## Steal or Vacuous

Patch (draft, not applied):

1. lane_runner.py, inside gate_drop after the scalar _trail (:192): `_emit_gate_verdict_v2(lane, item, ok, reasons)` plus, after gate_drop_v2:

```python
def _emit_gate_verdict_v2(lane: str, item: dict, ok: bool, reasons: list[str]) -> None:
    try:
        block = load_gate_block()
        if not ((block.get("emitters") or {}).get("gate_drop")):
            return
        fam = lambda p: ",".join(r for r in reasons if r.startswith(p))
        axes = {"brief_fidelity": {"score": 0.0 if fam("missing:") else 1.0,
                "confidence": 1.0, "evidence_quote": fam("missing:")},
                "build_quality": {"score": 0.0 if fam("anchor:") else 1.0,
                "confidence": 1.0, "evidence_quote": fam("anchor:")},
                "receipt_completeness": {"score": 0.0 if fam("ttl:") else 1.0,
                "confidence": 1.0, "evidence_quote": fam("ttl:")}}
        gate_drop_v2(lane, str(item.get("anchor") or item.get("task") or ""), axes,
                     "rule", failure_class="none" if ok else "infra",
                     failure_detail=",".join(reasons))
    except Exception as e:  # noqa: BLE001
        _log(f"gate emitter exc {lane}: {e}")
```

Confidence by construction: the rule seat invents no calibration, so confidence is 1.0 on every axis; non-1.0 scores carry the gate's own reason strings as verbatim quotes (the evidence-quote law).

2. build_gate_verdict :237 becomes: `if judge_seat not in seats and judge_seat not in ((block.get("cascade") or {}).get("cascade_exempt_seats") or []):`
3. configs/lanes.yaml, inside gate_verdict_v2:
```yaml
  emitters:
    gate_drop: false   # dormant by default; governor flips to true (B2-111)
```
4. Callers :733/:769 need zero edits, the emitter rides gate_drop. Test (test_lane_runner_cluster.py style, monkeypatching lr.LANES and lr.load_gate_block to a stub with emitters.gate_drop true): a PASS drop (five fields, future ttl) through lr.gate_drop(item, "builder") must land exactly one GATE_VERDICT and one GATE_VERDICT_V2, judge_seat rule, all axis scores and confidences 1.0, decision accept; a FAIL drop (ts removed) must land failure_class infra, brief_fidelity 0.0 with evidence_quote "missing:ts", decision escalate; a flag-absent stub lands only the scalar.

## Falsifier

Pre-registered: after the governor flips emitters.gate_drop to true, the next 100 scalar GATE_VERDICT rows must be accompanied by >= 1 GATE_VERDICT_V2 row; zero V2 rows at 100 proves the wiring vacuous. Secondary: every V2 row must carry judge_seat "rule" and confidence exactly 1.0 on all three axes; anything else falsifies the confidence-by-construction guard.

## Bibliography

- Read: mag/lane_runner.py; configs/lanes.yaml gate_verdict_v2; BURN_JUDGE_LANE_BUILD_20260925.md s1-s2b; BURN_judge-lane-spec_20260926_f.md; tests/test_lane_runner_cluster.py; mag/desk_conductor.py :315-325; queue/lanes/*/trail.jsonl.
- No web search spent: the claim is byte-verifiable locally.
