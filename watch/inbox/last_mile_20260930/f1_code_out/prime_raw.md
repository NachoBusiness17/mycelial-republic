import sys


def main():
    if len(sys.argv) < 2:
        print("ROWS|0")
        return
    try:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            lines = f.readlines()
    except OSError:
        print("ROWS|0")
        return

    pairs = {}
    crit_eq = 0
    crit_total = 0
    valid_rows = 0

    for line in lines:
        if not line.strip():
            continue
        try:
            obj = __import__("json").loads(line)
        except Exception:
            continue
        if not isinstance(obj, dict):
            continue
        a_model = obj.get("a_model")
        b_model = obj.get("b_model")
        winner = obj.get("winner")
        a_chars = obj.get("a_chars")
        b_chars = obj.get("b_chars")
        if a_model is None or b_model is None or winner is None or a_chars is None or b_chars is None:
            continue
        valid_rows += 1
        key = (a_model, b_model)
        if key not in pairs:
            pairs[key] = {"A": 0, "B": 0, "TIE": 0, "a_sum": 0, "b_sum": 0, "n": 0}
        p = pairs[key]
        if winner in ("A", "B", "TIE"):
            p[winner] += 1
        p["a_sum"] += a_chars
        p["b_sum"] += b_chars
        p["n"] += 1

        crit = obj.get("criteria")
        if crit:
            for c in crit:
                if isinstance(c, dict) and "a" in c and "b" in c:
                    crit_total += 1
                    if c["a"] == c["b"]:
                        crit_eq += 1

    if valid_rows == 0:
        print("ROWS|0")
        return

    for key in sorted(pairs.keys()):
        p = pairs[key]
        print("WINS|%s|%s|%d|%d|%d" % (key[0], key[1], p["A"], p["B"], p["TIE"]))
    for key in sorted(pairs.keys()):
        p = pairs[key]
        print("AVGCHARS|%s|%.1f|%s|%.1f" % (key[0], p["a_sum"] / p["n"], key[1], p["b_sum"] / p["n"]))
    if crit_total > 0:
        print("CRITAGREE|%d|%d|%.2f" % (crit_eq, crit_total, crit_eq / crit_total))
    print("ROWS|%d" % valid_rows)


if __name__ == "__main__":
    main()
