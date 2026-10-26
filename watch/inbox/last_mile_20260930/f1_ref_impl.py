"""F1 code-task reference implementation (the grader's ground truth).

Not a contender: this is the byte-truth oracle the two model outputs are
scored against on hidden fixtures. Written by the F1 lane owner,
2026-09-30, straight from f1_code_spec.md.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def load_valid(path: str) -> list[dict]:
    p = Path(path)
    if not p.is_file():
        return []
    rows: list[dict] = []
    with open(p, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(row, dict):
                continue
            for k in ("a_model", "b_model", "winner", "a_chars", "b_chars"):
                if row.get(k) is None:
                    break
            else:
                rows.append(row)
    return rows


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("ROWS|0")
        return 0
    rows = load_valid(argv[1])
    if not rows:
        print("ROWS|0")
        return 0
    pairs: dict[tuple[str, str], list[dict]] = {}
    for r in rows:
        pairs.setdefault((r["a_model"], r["b_model"]), []).append(r)
    for (am, bm), prows in sorted(pairs.items()):
        wa = sum(1 for r in prows if r["winner"] == "A")
        wb = sum(1 for r in prows if r["winner"] == "B")
        wt = sum(1 for r in prows if r["winner"] == "TIE")
        print(f"WINS|{am}|{bm}|{wa}|{wb}|{wt}")
    for (am, bm), prows in sorted(pairs.items()):
        ma = sum(r["a_chars"] for r in prows) / len(prows)
        mb = sum(r["b_chars"] for r in prows) / len(prows)
        print(f"AVGCHARS|{am}|{ma:.1f}|{bm}|{mb:.1f}")
    agree = total = 0
    for r in rows:
        for c in (r.get("criteria") or []):
            total += 1
            if c.get("a") == c.get("b"):
                agree += 1
    if total:
        print(f"CRITAGREE|{agree}|{total}|{agree / total:.2f}")
    print(f"ROWS|{len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
