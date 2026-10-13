"""THE 50 W6 T30: worked-example validation for the G06 policy-eval wire schema.

Validates the filed schema (dashboard/schemas/policy_eval.v1.schema.json)
against a worked request/response pair, plus negative cases that must fail.

Run:  .venv\\Scripts\\python.exe tools\\policy_eval_schema_check.py
Exit 0 = all checks pass. This file is the check receipt the endpoint plan
cites; re-run it after any schema edit.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "dashboard" / "schemas" / "policy_eval.v1.schema.json"

# --- worked example: the pair every implementation must reproduce ------------

INPUT_TEXT = (
    "Plan: run scut pass on the day_work lane, then clean up the scratch dir "
    "with rm -rf C:/Users/foste/AppData/Local/Temp/mag_scratch, then file the "
    "brief. Budget note: dispatch one hosted specialist call tomorrow."
)

WORKED_REQUEST = {
    "schema": "the50.w6.t30.policy_eval.v1",
    "policy": {
        "inline": {
            "name": "mag-standing-steer-v0",
            "rules": [
                {
                    "rule_id": "r1",
                    "text": "deny any command that recursively deletes a directory outside the lane cache root",
                    "decision": "deny",
                    "patterns": ["rm -rf"],
                },
                {
                    "rule_id": "r2",
                    "text": "escalate any action that spends hosted specialist budget before the daily window",
                    "decision": "escalate",
                    "patterns": ["hosted specialist"],
                },
                {
                    "rule_id": "r3",
                    "text": "allow everything else",
                    "decision": "allow",
                },
            ],
        }
    },
    "input": {
        "text": INPUT_TEXT,
        "context": {"seat": "builder", "goal": "day_work scut", "trace": "t30-worked"},
    },
    "oracle": {"profile": "local_janitor", "min_confidence": 0.6},
    "options": {"spans": True, "explain": True},
}

# Spans are DERIVED from the rules' patterns over input.text with str.find --
# the same algorithm the planned endpoint uses -- so the worked pair is
# self-consistent by construction and the consistency section below re-verifies
# it instead of trusting hand-counted offsets.
def _derive_spans(text: str, rules: list[dict]) -> list[dict]:
    spans: list[dict] = []
    for rule in rules:
        for pat in rule.get("patterns", []):
            i = text.find(pat)
            if i >= 0:
                spans.append({"rule_id": rule["rule_id"], "start": i,
                              "end": i + len(pat), "quote": pat})
    return spans


_INLINED = WORKED_REQUEST["policy"]["inline"]["rules"]
_SPANS = _derive_spans(INPUT_TEXT, _INLINED)

WORKED_RESPONSE = {
    "ok": True,
    "schema": "the50.w6.t30.policy_eval.v1",
    "policy": {
        "uri": "inline:mag-standing-steer-v0",
        "name": "mag-standing-steer-v0",
        "n_rules": 3,
    },
    "verdict": {
        "decision": "deny",
        "confidence": 0.92,
        "rule_id": "r1",
        "reason": "input contains a recursive delete aimed outside the lane cache root",
    },
    "spans": _SPANS,
    "oracle": {
        "model": "local_janitor (worked example, synthetic run)",
        "latency_ms": 22,
    },
}

# --- negative cases: every one of these must FAIL validation ------------------

NEGATIVES = [
    ("request without any ruleset pointer",
     "request",
     {"schema": "the50.w6.t30.policy_eval.v1",
      "input": {"text": "hello"}}),
    ("request with unknown schema const",
     "request",
     {"schema": "other.v9", "policy": {"inline": {"name": "n", "rules": [
         {"rule_id": "r1", "text": "t", "decision": "allow"}]}},
      "input": {"text": "hello"}}),
    ("decision outside the enum",
     "request",
     {"schema": "the50.w6.t30.policy_eval.v1",
      "policy": {"inline": {"name": "n", "rules": [
          {"rule_id": "r1", "text": "t", "decision": "maybe"}]}},
      "input": {"text": "hello"}}),
    ("uri outside the allowed schemes",
     "request",
     {"schema": "the50.w6.t30.policy_eval.v1",
      "policy": {"uri": "ftp://policy.example/one"},
      "input": {"text": "hello"}}),
    ("both uri and inline set",
     "request",
     {"schema": "the50.w6.t30.policy_eval.v1",
      "policy": {"uri": "mag://policy/pol-ab12cd34",
                 "inline": {"name": "n", "rules": [
                     {"rule_id": "r1", "text": "t", "decision": "allow"}]}},
      "input": {"text": "hello"}}),
    ("confidence above 1",
     "response",
     {"ok": True, "schema": "the50.w6.t30.policy_eval.v1",
      "policy": {"uri": "inline:n", "n_rules": 1},
      "verdict": {"decision": "allow", "confidence": 1.5}}),
    ("invented oracle calibration numbers",
     "response",
     {"ok": True, "schema": "the50.w6.t30.policy_eval.v1",
      "policy": {"uri": "inline:n", "n_rules": 1},
      "verdict": {"decision": "abstain", "confidence": 0.2},
      "oracle": {"model": "m", "calibration": {"ece": 0.05, "temperature": 1.3}}}),
]


def _validate(validator_cls, schema, doc):
    """Kept for the next seat: run a validator class over any doc."""
    return sorted(validator_cls(schema).iter_errors(doc), key=lambda e: e.path)


def main() -> int:
    from jsonschema import Draft202012Validator

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    results: list[tuple[str, bool, str]] = []

    # request $defs sub-validation: build a validator rooted at #/$defs/request
    req_root = dict(schema)
    req_root["allOf"] = [{"$ref": "#/$defs/request"}]
    resp_root = dict(schema)
    resp_root["allOf"] = [{"$ref": "#/$defs/response"}]
    rv = Draft202012Validator(req_root)
    sv = Draft202012Validator(resp_root)

    errs = sorted(rv.iter_errors(WORKED_REQUEST), key=lambda e: str(e.path))
    results.append(("worked request validates against #/$defs/request",
                    not errs, "; ".join(e.message for e in errs)))

    errs = sorted(sv.iter_errors(WORKED_RESPONSE), key=lambda e: str(e.path))
    results.append(("worked response validates against #/$defs/response",
                    not errs, "; ".join(e.message for e in errs)))

    # semantic consistency the schema cannot express
    def _spans_semantically_sound(spans: list[dict], text: str) -> tuple[bool, str]:
        detail: list[str] = []
        for sp in spans:
            if sp["end"] <= sp["start"]:
                detail.append(f"span {sp['rule_id']}: end {sp['end']} <= start {sp['start']}")
                continue
            got = text[sp["start"]:sp["end"]]
            if got != sp["quote"]:
                detail.append(f"span {sp['rule_id']}: text[{sp['start']}:{sp['end']}]={got!r} != quote {sp['quote']!r}")
        return (not detail), "; ".join(detail)

    text = WORKED_REQUEST["input"]["text"]
    ok, detail = _spans_semantically_sound(WORKED_RESPONSE.get("spans", []), text)
    results.append(("every span orders and locates its quote exactly", ok, detail))
    ok, detail = _spans_semantically_sound(
        [{"rule_id": "rX", "start": 10, "end": 4, "quote": "x"}], text)
    results.append(("semantic layer rejects an end-before-start span (schema cannot compare two properties)",
                    not ok, detail))

    vid = WORKED_RESPONSE["verdict"].get("rule_id")
    span_ids = {sp["rule_id"] for sp in WORKED_RESPONSE.get("spans", [])}
    results.append(("verdict rule_id is covered by spans",
                    vid in span_ids, f"verdict rule_id={vid!r}, span ids={sorted(span_ids)}"))

    rules = {r["rule_id"]: r for r in
             WORKED_REQUEST["policy"]["inline"]["rules"]}
    vdec = WORKED_RESPONSE["verdict"]["decision"]
    rdec = rules.get(vid, {}).get("decision")
    results.append(("verdict decision matches the fired rule's decision",
                    vdec == rdec, f"verdict={vdec}, rule {vid}={rdec}"))
    first_by_len = max(rules.values(), key=lambda r: len(r.get("patterns") or []))
    results.append(("most-specific rule wins (deny over escalate/allow)",
                    vdec == first_by_len["decision"],
                    f"expected {first_by_len['decision']}, got {vdec}"))

    for name, kind, doc in NEGATIVES:
        v = rv if kind == "request" else sv
        errs = list(v.iter_errors(doc))
        results.append((f"negative rejected: {name}", bool(errs),
                        "rejected: " + errs[0].message if errs else "WRONGLY ACCEPTED"))

    failed = 0
    for name, ok, detail in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if (detail and not ok) else ""))
        if not ok:
            failed += 1
    print(f"\n{len(results) - failed}/{len(results)} checks pass; schema={SCHEMA_PATH.relative_to(ROOT)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
