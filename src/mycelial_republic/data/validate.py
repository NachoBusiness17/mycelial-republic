"""Validate annotated training JSONL against Sprint 0.1 acceptance criteria."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from mycelial_republic.data.schema import TrainingExample


def run_validate(inp: str, min_examples: int = 800) -> int:
    path = Path(inp)
    if not path.is_file():
        print(f"Not found: {path}", file=sys.stderr)
        return 1

    examples: list[TrainingExample] = []
    errors: list[str] = []
    tag_counts: Counter[str] = Counter()
    signal_counts: Counter[str] = Counter()

    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError as e:
            errors.append(f"line {i}: invalid JSON ({e})")
            continue
        ex = TrainingExample(
            id=str(d.get("id", "")),
            source=d.get("source", ""),
            text=d.get("text", ""),
            instruction=d.get("instruction", ""),
            response=d.get("response", ""),
            knot_tags=list(d.get("knot_tags") or []),
            signal=d.get("signal", "high"),
            rope_note=d.get("rope_note", ""),
            chord_note=d.get("chord_note", ""),
            refusal_note=d.get("refusal_note", ""),
            created_at=d.get("created_at", ""),
            meta=dict(d.get("meta") or {}),
        )
        for err in ex.validate():
            errors.append(f"line {i} id={ex.id}: {err}")
        examples.append(ex)
        for t in ex.knot_tags:
            tag_counts[t] += 1
        signal_counts[ex.signal] += 1

    n = len(examples)
    high = signal_counts.get("high", 0)
    print(f"Examples: {n}")
    print(f"Signal:   {dict(signal_counts)}")
    print(f"Tags:     {dict(tag_counts)}")
    print(f"Errors:   {len(errors)}")
    for e in errors[:20]:
        print(f"  - {e}", file=sys.stderr)
    if len(errors) > 20:
        print(f"  ... and {len(errors) - 20} more", file=sys.stderr)

    ok = True
    if n < min_examples:
        print(f"FAIL: need ≥{min_examples} examples, have {n}", file=sys.stderr)
        ok = False
    else:
        print(f"PASS count: {n} ≥ {min_examples}")

    # Soft quality gates for Sprint 0.1
    if high < min(min_examples // 2, n // 2) and n > 0:
        print(
            f"WARN: high-signal count ({high}) is low — hand-annotate more chord/refusal/rope rows",
            file=sys.stderr,
        )
    if tag_counts.get("refusal", 0) < 5 and n >= 50:
        print("WARN: few refusal examples — scaffold needs sovereign refusal density", file=sys.stderr)
    if tag_counts.get("chord", 0) < 5 and n >= 50:
        print("WARN: few chord examples — mirror may not learn the ritual", file=sys.stderr)

    if errors:
        ok = False
        print("FAIL: schema validation errors present", file=sys.stderr)

    return 0 if ok else 2


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--min", type=int, default=800)
    a = ap.parse_args()
    raise SystemExit(run_validate(a.inp, min_examples=a.min))
