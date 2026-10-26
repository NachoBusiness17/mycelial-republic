"""operator_go - canonical reader for watch/inbox/OPERATOR_GO.jsonl (B2-425).

The surface: watch/inbox/OPERATOR_GO.jsonl, one JSON row per TRANSCRIBED
operator order, schema operator_go.v1:

  {"schema": "operator_go.v1", "ts": "...Z", "gate": "<gate-id>",
   "order": "<the order, transcribed verbatim or near-verbatim>",
   "source_transcript": "<file:line or chat surface that holds it>",
   "transcribed_by": "<lane>"}

Appended ONLY by lanes transcribing a real operator order (no-fabrication
law: an order that exists only in untranscribed chat gets a row only when a
lane actually transcribes it with its source named). A gate with no row is
NO-GO-on-file; prose grepping in gate cards is retired in favor of this
reader.

CLI:
  python tools/operator_go.py <gate-id>     exit 0 + row if GO on file,
                                            exit 1 if NO-GO-on-file
  python tools/operator_go.py --all        list every gate's newest row
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GO_PATH = ROOT / "watch" / "inbox" / "OPERATOR_GO.jsonl"


def load_rows() -> list[dict]:
    rows: list[dict] = []
    if not GO_PATH.is_file():
        return rows
    for line in GO_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        if r.get("schema") == "operator_go.v1":
            rows.append(r)
    return rows


def has_go(gate: str) -> dict | None:
    """Newest transcribed order for the gate, or None = NO-GO-on-file."""
    rows = [r for r in load_rows() if r.get("gate") == gate]
    return rows[-1] if rows else None


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 2
    if argv[0] == "--all":
        gates: dict[str, dict] = {}
        for r in load_rows():
            gates[r["gate"]] = r
        if not gates:
            print("NO-GO-on-file for every gate (surface empty)")
            return 1
        for gate, r in gates.items():
            print(f"GO {gate}: {r['ts']} {r['order'][:80]} (source: {r['source_transcript']})")
        return 0
    gate = argv[0]
    row = has_go(gate)
    if row is None:
        print(f"NO-GO-on-file: {gate}")
        return 1
    print(json.dumps(row, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
