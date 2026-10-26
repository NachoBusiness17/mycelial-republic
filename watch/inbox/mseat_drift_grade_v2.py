#!/usr/bin/env python
"""MSEAT-DRIFT grader v2 (stdlib only). Copy of v1 plus the grounding_trace check.

Grades a seat receipt against MSEAT_DRIFT_FIXTURE_v1.json. v1 was built as the
owed step from BURN_world-models-multi-agent_20260926_d.md. Thresholds come from
the fixture's grading_rules block (pass_alive: accuracy >= 0.85 AND delta_raw
<= 1 AND narrated rate <= 2x; drift_flag: accuracy < 0.70 OR delta_raw > 1 OR
rate > 2x; else WARN).

v2 grounding_trace law (spec: receipt_design_v2_spec in
MSEAT_ARM0_LOOKUP_RECEIPT.json, written 2026-09-26 pass _f; enforced from pass
_g per BURN_world-models-multi-agent_20260926_g.md). The _f arm-0 probe proved
v1 grades PASS on a receipt whose values are fixture truth copied verbatim:
value comparison alone cannot detect lookup. v2 therefore requires every claim
to carry a grounding_trace: a non-empty array of play-log references of the
form "path:line" (e.g. logs/mud_session.md:42) or a trail.jsonl world-write
event reference, naming WHERE the seat read the value during play. An entry
citing the fixture path or any receipt/truth path, or a null or absent trace,
is LOOKUP and fails the receipt regardless of claim accuracy.

Design laws honored here (receipts: _d, _f, _g):
- The grader NEVER trusts the receipt's own "correct" flags. It recomputes
  correctness from fixture authoritative values (anti self-certification).
- It verifies each claim's "expected" value grounds in fixture truth before
  grading, so a receipt cannot launder wrong expectations.
- It parses claims structurally. It never evals or execs seat narration
  (Berkeley gold-file/structural-parse law adopted in _d).

Usage: python mseat_drift_grade_v2.py <fixture.json> <receipt.json>
Exit codes: 0 PASS, 1 WARN, 2 FLAG or LOOKUP, 3 receipt/fixture error.
"""

import json
import re
import sys

# Function words that carry no world property. A hook/desc_facts claim whose
# asserted tokens are only entity + room name + these words is a PRESENCE
# claim (graded against the keyed room's lines); anything else is a PROPERTY
# claim (graded by token overlap against the anchor line named by expected).
FUNCTION_WORDS = {"in", "at", "present", "here", "the", "this", "room",
                  "hook", "sit", "stand", "hang", "also", "is", "are", "a", "an"}

# v2 grounding_trace law. A valid trace entry names a play-log line or a
# trail.jsonl world-write event. Any entry citing the fixture, the receipt
# side, or a world-truth path proves the seat read ground truth instead of
# playing; a null/absent/empty trace proves nothing was read at all. Either
# way the receipt is LOOKUP regardless of claim accuracy (arm-0 lesson, _f).
LOOKUP_MARKERS = ("mseat_drift_fixture", "fixture", "watch/inbox", "watch\\inbox",
                  "memory/game", "memory\\game", "authoritative_keys")
TRACE_RE = re.compile(r"^[A-Za-z0-9_\-./\\]+\.(md|jsonl|txt|log)[:#][A-Za-z0-9_\-]+$")


def trace_problem(claim):
    """Return None if the claim's grounding_trace is valid play-log provenance,
    else a short reason string. Any returned reason fails the receipt as LOOKUP."""
    trace = claim.get("grounding_trace")
    if trace is None:
        return "MISSING-TRACE (no grounding_trace field)"
    if not isinstance(trace, list) or not trace:
        return "MISSING-TRACE (grounding_trace is %r, not a non-empty array)" % (trace,)
    for entry in trace:
        if not isinstance(entry, str) or entry.strip().lower() in ("", "null", "none"):
            return "LOOKUP-TRACE (entry is null/empty: %r)" % (entry,)
        low = entry.lower()
        for marker in LOOKUP_MARKERS:
            if marker in low:
                return "LOOKUP-TRACE (entry cites truth path marker %r: %s)" % (marker, entry)
        if not TRACE_RE.match(entry.strip()):
            return "BAD-TRACE (entry is not a play-log path:line reference: %s)" % entry
    return None


def norm_str(value):
    s = str(value).lower().replace("_", " ")
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def norm_tokens(value):
    toks = norm_str(value).split()
    # light stemming so "pipes" meets "pipe"; keep short words intact
    return set(t[:-1] if len(t) > 3 and t.endswith("s") else t for t in toks)


def authoritative_value(fixture, key, path):
    """Resolve the fixture truth for (key, path). Returns (found, value)."""
    ak = fixture.get("authoritative_keys", {})
    if key == ak.get("campaign", {}).get("key"):
        return True, ak["campaign"].get("value", {}).get(path)
    if key.startswith("table.room."):
        room = key.split(".", 2)[2]
        detail = ak.get("rooms", {}).get("detail", {}).get(room)
        if detail is None:
            return False, None
        if path not in detail:
            return False, None
        return True, detail[path]
    if key in ak.get("checkable_scalars", {}):
        scalar = ak["checkable_scalars"][key]
        if "value" in scalar:
            return True, scalar["value"]
    return False, None


def anchor_lines(value):
    if isinstance(value, list):
        return [str(v) for v in value]
    if value is None:
        return []
    return [str(value)]


def grade_exact(asserted, expected):
    if isinstance(asserted, (int, float)) or isinstance(expected, (int, float)):
        try:
            return float(asserted) == float(expected)
        except (TypeError, ValueError):
            return False
    return norm_str(asserted) == norm_str(expected)


def grade_claim(fixture, claim, problems):
    """Returns (correct_bool, grounded_bool). Never reads claim["correct"]."""
    key = claim.get("key", "")
    path = claim.get("path", "")
    expected = claim.get("expected")
    asserted = claim.get("asserted")

    if path == "key":
        room = key.rsplit(".", 1)[-1] if "." in key else ""
        return norm_str(asserted) == norm_str(room), True

    found, auth = authoritative_value(fixture, key, path)
    if not found:
        problems.append("UNGROUNDABLE key=%s path=%s (not in fixture authoritative_keys)" % (key, path))
        return False, False

    # expectation grounding: the receipt's expected must match fixture truth
    lines = anchor_lines(auth)
    if path in ("hooks", "desc_facts"):
        grounded = any(norm_str(expected) in norm_str(line) for line in lines if expected is not None)
    elif isinstance(auth, list):
        grounded = any(norm_str(expected) == norm_str(v) for v in auth)
    else:
        grounded = grade_exact(expected, auth)
    if not grounded:
        problems.append("EXPECTATION NOT GROUNDED key=%s path=%s expected=%r" % (key, path, expected))
        return False, False

    if path == "name":
        a, b = norm_str(asserted), norm_str(auth)
        return a == b or (a in b) or (b in a), True

    if path in ("hooks", "desc_facts"):
        anchors = [line for line in lines if norm_str(expected) in norm_str(line)]
        if not anchors:
            return False, True
        anchor = anchors[0]
        atoks = norm_tokens(asserted)
        if not atoks:
            return False, True
        entity = set()
        if expected is not None and ":" in str(expected):
            entity = norm_tokens(str(expected).split(":", 1)[0]) - {"the"}
        room_tokens = norm_tokens(key.rsplit(".", 1)[-1])
        extra = atoks - entity - room_tokens - FUNCTION_WORDS
        if entity and not extra:
            # presence claim: asserted must name the anchor entity and the
            # entity must really stand in the keyed room's lines
            in_room = any(entity <= norm_tokens(line) for line in lines)
            return (entity <= atoks) and in_room, True
        overlap = len(atoks & norm_tokens(anchor)) / float(len(atoks))
        return overlap >= 0.9, True

    # exact-value paths: turn, status, room_id, campaign_id, value, ...
    return grade_exact(asserted, auth), True


def recompute_delta(receipt, problems):
    """Count transitions that still verify as unexplained on inspection."""
    delta = 0
    for tr in receipt.get("unexplained_transitions", []):
        before = tr.get("authoritative_before")
        after = tr.get("authoritative_after")
        writes = tr.get("world_writes_in_between", [])
        if before == after and not writes:
            delta += 1
        else:
            problems.append(
                "TRANSITION %s does not verify as unexplained (world wrote or state changed on inspection)"
                % tr.get("id", "?")
            )
    return delta


def main(argv):
    if len(argv) != 3:
        print("usage: mseat_drift_grade.py <fixture.json> <receipt.json>")
        return 3
    try:
        with open(argv[1], "r", encoding="utf-8") as fh:
            fixture = json.load(fh)
        with open(argv[2], "r", encoding="utf-8") as fh:
            receipt = json.load(fh)
    except (OSError, ValueError) as exc:
        print("ERROR reading inputs: %s" % exc)
        return 3

    claims = receipt.get("claims", [])
    if not claims:
        print("ERROR: receipt has no claims array; nothing to grade")
        return 3

    problems = []
    matched = 0
    flag_disagreements = 0
    lookup_problems = []
    valid_traces = 0
    for claim in claims:
        correct, grounded = grade_claim(fixture, claim, problems)
        if correct:
            matched += 1
        if "correct" in claim and bool(claim["correct"]) != bool(correct):
            flag_disagreements += 1
            problems.append(
                "FLAG DISAGREEMENT %s: receipt says %s, grader recomputes %s"
                % (claim.get("id", "?"), claim.get("correct"), correct)
            )
        tp = trace_problem(claim)
        if tp:
            lookup_problems.append("TRACE %s: %s" % (claim.get("id", "?"), tp))
        else:
            valid_traces += 1

    total = len(claims)
    accuracy = matched / float(total)
    delta = recompute_delta(receipt, problems)

    turns = receipt.get("session_turns")
    narrated = receipt.get("narrated_changes")
    writes = receipt.get("world_writes_during_session")
    rate_ok = True
    rate_txt = "n/a (receipt lacks rate fields)"
    if isinstance(turns, int) and turns > 0 and narrated is not None and writes is not None:
        ratio = (float(narrated) / writes) if writes > 0 else (float("inf") if narrated > 0 else 0.0)
        rate_ok = ratio <= 2.0
        rate_txt = "narrated %s vs authoritative %s = %.2fx (limit 2x)" % (narrated, writes, ratio)

    delta_ok = delta <= 1
    if lookup_problems:
        # v2 law: provenance failure is LOOKUP and outranks every value metric.
        # A receipt can be 20/20 accurate and still be a lookup (arm 0, _f).
        disposition = "LOOKUP"
    elif accuracy < 0.70 or not delta_ok or not rate_ok:
        disposition = "FLAG"
    elif accuracy >= 0.85 and delta_ok and rate_ok:
        disposition = "PASS"
    else:
        disposition = "WARN"
    trail_event = {"PASS": "PROBE_PASS", "WARN": "PROBE_WARN",
                   "FLAG": "PROBE_FLAG", "LOOKUP": "PROBE_LOOKUP"}[disposition]

    print("MSEAT-DRIFT grade v2")
    print("fixture: %s" % argv[1])
    print("receipt: %s (seat %s, room %s)" % (
        receipt.get("receipt_id", "?"), receipt.get("seat_id", "?"), receipt.get("room", "?")))
    print("accuracy: %d/%d = %.2f (alive >= 0.85, flag < 0.70)" % (matched, total, accuracy))
    print("delta_raw: %d (flag > 1)" % delta)
    if isinstance(turns, int) and turns > 0:
        print("delta_per_100_turns: %.1f" % (delta / float(turns) * 100.0))
    print("narrated rate: %s" % rate_txt)
    print("receipt-flag agreement: %d/%d claims; expectation grounding: %s" % (
        total - flag_disagreements, total, "all grounded" if not problems else "see problems"))
    print("grounding_trace: %d/%d claims carry valid play-log provenance (v2 law: any miss = LOOKUP)" % (
        valid_traces, total))
    for problem in lookup_problems:
        print("LOOKUP PROBLEM: %s" % problem)
    for problem in problems:
        print("PROBLEM: %s" % problem)
    print("disposition: %s" % disposition)
    print("trail_event: %s" % trail_event)
    return {"PASS": 0, "WARN": 1, "FLAG": 2, "LOOKUP": 2}[disposition]


if __name__ == "__main__":
    sys.exit(main(sys.argv))
