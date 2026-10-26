import json
import sys
from collections import defaultdict


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else None
    rows = []
    if path is not None:
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except Exception:
                        continue
                    if not isinstance(obj, dict):
                        continue
                    if any(obj.get(k) is None for k in ("a_model", "b_model", "winner", "a_chars", "b_chars")):
                        continue
                    rows.append(obj)
        except Exception:
            rows = []

    out = []
    if rows:
        pairs = defaultdict(lambda: {"A": 0, "B": 0, "TIE": 0, "n": 0, "ac": 0, "bc": 0})
        crit_match = 0
        crit_total = 0
        for r in rows:
            key = (r["a_model"], r["b_model"])
            p = pairs[key]
            p["n"] += 1
            w = r["winner"]
            if w in ("A", "B", "TIE"):
                p[w] += 1
            p["ac"] += r["a_chars"]
            p["bc"] += r["b_chars"]
            crits = r.get("criteria")
            if isinstance(crits, list):
                for c in crits:
                    if isinstance(c, dict) and "a" in c and "b" in c:
                        crit_total += 1
                        if c["a"] == c["b"]:
                            crit_match += 1

        keys = sorted(pairs.keys())
        for a, b in keys:
            p = pairs[(a, b)]
            out.append(f"WINS|{a}|{b}|{p['A']}|{p['B']}|{p['TIE']}")
        for a, b in keys:
            p = pairs[(a, b)]
            out.append(f"AVGCHARS|{a}|{p['ac'] / p['n']:.1f}|{b}|{p['bc'] / p['n']:.1f}")
        if crit_total > 0:
            out.append(f"CRITAGREE|{crit_match}|{crit_total}|{crit_match / crit_total:.2f}")

    out.append(f"ROWS|{len(rows)}")
    sys.stdout.write("\n".join(out) + "\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
