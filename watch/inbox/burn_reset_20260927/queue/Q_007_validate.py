"""Q-007 validator: schema, uniqueness, em-dash law, and anti-fabrication anchors.

Checks watch/inbox/burn_reset_20260927/queue/Q_007_rows.jsonl against:
  1. exact quantizer stream row schema (mirrors mycelial-republic mirror_train.jsonl shape)
  2. one id per row, unique, no collision with the 115 existing stream ids
  3. at least one non-empty note (rope/chord/refusal) per row
  4. no em-dash or en-dash anywhere in the rows file (harness law)
  5. anchor substrings per row must exist in the cited source file (no fabrication)
Run: .venv/Scripts/python.exe watch/inbox/burn_reset_20260927/queue/Q_007_validate.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
ROWS_PATH = ROOT / "watch/inbox/burn_reset_20260927/queue/Q_007_rows.jsonl"
STREAM_PATH = Path(
    r"C:\Users\foste\Documents\projects\mycelial-republic\data\annotated\mirror_train.jsonl"
)
SCHEMA_KEYS = [
    "id", "source", "text", "instruction", "response", "knot_tags", "signal",
    "rope_note", "chord_note", "refusal_note", "created_at", "meta",
]

# id -> (source_path, [anchor substrings that must appear in that file])
ANCHORS = {
    "q7-001": ("memory/runs/astra_convo_20260911/ANSWER_3.md", [
        "does not clear the pre-seal gate",
        "Hash agreement establishes which bytes were reviewed, not their correctness",
    ]),
    "q7-002": ("memory/runs/astra_convo_20260911/ANSWER_3.md", [
        "zero-based index 5 selects C06",
        "A containment grep cannot establish independent derivations",
    ]),
    "q7-003": ("memory/runs/astra_convo_20260911/DISPATCH_1.txt", [
        "silently eaten by except-pass for five days",
        "failures stay in the denominator",
    ]),
    "q7-004": ("memory/runs/astra_convo_20260911/DISPATCH_1.txt", [
        "receipt spine survives deletion",
        "operator authorization for human-facing consequences",
    ]),
    "q7-005": ("memory/runs/astra_convo_20260911/ANSWER_3.md", [
        "reduces evidence or workload",
        "information-access-only sham rule",
    ]),
    "q7-006": ("memory/runs/astra_ask_20260913/A7_the_smell_test.md", [
        "everything else is scaffolding",
        "The names are canon; the ledger is load",
    ]),
    "q7-007": ("memory/runs/astra_ask_20260913/A7_the_smell_test.md", [
        "a second signing path",
        "in-place renames of canon",
    ]),
    "q7-008": ("memory/runs/astra_ask_20260913/A7_the_smell_test.md", [
        "poison when it reaches files the append-only line preserves forever",
    ]),
    "q7-009": ("memory/runs/astra_ask_20260913/A8_the_operators_question.md", [
        "constitution cosplay",
        "violated his own constitution while defending it",
    ]),
    "q7-010": ("memory/runs/ocean_v2_bernays_20260920/receipt.json", [
        "refuse outright if the deliverable could be pasted into a persuasion campaign",
        "Now I only take it apart",
    ]),
    "q7-011": ("memory/runs/ocean_v2_bernays_20260920/receipt.json", [
        "manufactures the evidence that later indicts it",
        "it found the sponsor",
    ]),
}


def main() -> int:
    raw = ROWS_PATH.read_text(encoding="utf-8")
    errors: list[str] = []

    if "\u2014" in raw or "\u2013" in raw:
        errors.append("em-dash or en-dash found in rows file")

    rows = []
    for n, line in enumerate(raw.splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            errors.append(f"line {n}: not JSON: {exc}")
    if errors:
        print("\n".join(errors))
        return 1

    ids = [r.get("id") for r in rows]
    if len(ids) != len(set(ids)):
        errors.append("duplicate ids in rows file")

    existing_ids = set()
    if STREAM_PATH.is_file():
        for line in STREAM_PATH.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.strip():
                try:
                    existing_ids.add(json.loads(line).get("id"))
                except json.JSONDecodeError:
                    pass
    collisions = sorted(existing_ids & set(ids))
    if collisions:
        errors.append(f"id collision with stream: {collisions}")

    for r in rows:
        rid = r.get("id", "?")
        if list(r.keys()) != SCHEMA_KEYS:
            errors.append(f"{rid}: key order/set mismatch: {list(r.keys())}")
        notes = [r.get(k, "") for k in ("rope_note", "chord_note", "refusal_note")]
        if not any(n.strip() for n in notes):
            errors.append(f"{rid}: all three notes empty")
        if r.get("signal") not in ("high", "medium", "low"):
            errors.append(f"{rid}: bad signal {r.get('signal')!r}")
        if not str(r.get("text", "")).strip():
            errors.append(f"{rid}: empty text")

    for rid, (rel, anchors) in ANCHORS.items():
        src = ROOT / rel
        if not src.is_file():
            errors.append(f"{rid}: source missing: {rel}")
            continue
        body = " ".join(src.read_text(encoding="utf-8", errors="replace").split())
        for a in anchors:
            # wrap-insensitive: compare against whitespace-normalized body
            if a not in body:
                errors.append(f"{rid}: anchor not found in {rel}: {a!r}")

    if errors:
        print("FAIL")
        print("\n".join(errors))
        return 1
    print(f"OK: {len(rows)} rows; schema, ids, notes, dashes, and {len(ANCHORS)} anchor sets all pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
