"""F4 scorer - per-shape quality table from f4_census_rows.jsonl (2026-09-30).

Reads the banked census rows (never re-fires anything) and prints:
  win rate per shape (flash / max / tie, errors and unparsed named),
  response richness (mean words, chars, headers per model per shape),
  error rate (contender errors, judge unparsed, extraction JSON validity),
  cost per answer, and the slot tally (position-bias check).

Every number comes from the rows file; nothing is projected.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent

SHAPES = ["code-writing", "analysis", "extraction", "judgment", "creative"]


def load() -> list[dict]:
    rows: list[dict] = []
    with (HERE / "f4_census_rows.jsonl").open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def dedupe_last(rows: list[dict]) -> list[dict]:
    """One verdict per task: a |rejudge repair row supersedes its original
    UNPARSED row (append-only file; the original stays banked above it)."""
    last: dict[str, dict] = {}
    for r in rows:
        last[r["task_id"].split("|")[0]] = r
    return list(last.values())


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def main() -> int:
    all_rows = load()
    rows = dedupe_last(all_rows)
    print(f"rows={len(rows)} tasks (file holds {len(all_rows)} incl. rejudge repairs)")
    total = {"flash": 0.0, "max": 0.0, "judge": 0.0}
    per_shape: dict[str, dict] = defaultdict(lambda: {
        "flash": 0, "max": 0, "tie": 0, "error": 0, "unparsed": 0, "n": 0,
        "flash_words": [], "max_words": [], "flash_chars": [], "max_chars": [],
        "flash_headers": [], "max_headers": [], "flash_cost": [], "max_cost": [],
        "flash_json": [], "max_json": [], "crit_flash": [], "crit_max": []})
    slot_wins = defaultdict(int)
    judge_costs: list[float] = []

    for r in rows:
        s = per_shape[r["shape"]]
        s["n"] += 1
        w = r.get("winner")
        if w == "flash":
            s["flash"] += 1
        elif w == "max":
            s["max"] += 1
        elif w == "TIE":
            s["tie"] += 1
        elif w in ("ERROR",):
            s["error"] += 1
        else:
            s["unparsed"] += 1
        for side in ("flash", "max"):
            rec = r[side]
            s[side + "_words"].append(rec["words"])
            s[side + "_chars"].append(rec["chars"])
            s[side + "_headers"].append(rec["headers"])
            s[side + "_cost"].append(rec["cost"])
            total[side] += rec["cost"]
            if "json_valid" in rec:
                s[side + "_json"].append(1.0 if rec["json_valid"] else 0.0)
        jc = r.get("judge_cost") or 0.0
        judge_costs.append(jc)
        total["judge"] += jc
        # per-criterion points (a=flash, b=max), decided rows only
        if w in ("flash", "max", "TIE"):
            for c in r.get("criteria", []):
                s["crit_flash"].append(c["a"])
                s["crit_max"].append(c["b"])
        if w in ("flash", "max"):
            slot_of_winner = r["slot_of_flash"] if w == "flash" else (
                "B" if r["slot_of_flash"] == "A" else "A")
            slot_wins[slot_of_winner] += 1

    print("\n== PER-SHAPE TABLE (winner | richness flash vs max | errors) ==")
    hdr = (f"{'shape':<14} {'n':>2} {'flash':>5} {'max':>4} {'tie':>4} "
           f"{'err':>3} {'unp':>3} | {'words f/m':>11} {'chars f/m':>11} "
           f"{'hdr f/m':>7} | {'crit f/m':>9} | {'cost f/m':>13}")
    print(hdr)
    for shape in SHAPES:
        s = per_shape.get(shape)
        if not s:
            print(f"{shape:<14}  (no rows)")
            continue
        print(f"{shape:<14} {s['n']:>2} {s['flash']:>5} {s['max']:>4} "
              f"{s['tie']:>4} {s['error']:>3} {s['unparsed']:>3} | "
              f"{mean(s['flash_words']):>5.0f}/{mean(s['max_words']):<5.0f} "
              f"{mean(s['flash_chars']):>5.0f}/{mean(s['max_chars']):<5.0f} "
              f"{mean(s['flash_headers']):>3.1f}/{mean(s['max_headers']):<3.1f} | "
              f"{mean(s['crit_flash']):>4.2f}/{mean(s['crit_max']):<4.2f} | "
              f"{mean(s['flash_cost']):>5.4f}/{mean(s['max_cost']):<5.4f}")

    print("\n== EXTRACTION JSON VALIDITY (error-rate signal) ==")
    for shape in ("extraction",):
        s = per_shape[shape]
        print(f"{shape}: flash {sum(s['flash_json']):.0f}/{len(s['flash_json'])} "
              f"valid, max {sum(s['max_json']):.0f}/{len(s['max_json'])} valid")

    print("\n== ERRORS ==")
    err_rows = [(r["task_id"], r["shape"], r["winner"],
                 (r.get("flash", {}).get("error"), r.get("max", {}).get("error"),
                  r.get("judge_error")))
                for r in rows
                if r.get("winner") in ("ERROR", "JUDGE_ERROR", "UNPARSED")
                or r.get("flash", {}).get("error") or r.get("max", {}).get("error")]
    for e in err_rows:
        print(" ", e)
    if not err_rows:
        print("  none")

    print("\n== SLOT TALLY (position-bias check) ==")
    print(f"  slot A wins {slot_wins['A']}, slot B wins {slot_wins['B']}")

    print("\n== COST ==")
    judge_all = sum(float(r.get("judge_cost") or 0.0) for r in all_rows)
    superseded_judge = judge_all - total["judge"]
    print(f"  metered total: ${total['flash'] + total['max'] + judge_all:.4f} "
          f"(flash ${total['flash']:.4f}, max ${total['max']:.4f}, judge ${judge_all:.4f} "
          f"of which ${superseded_judge:.4f} on superseded/unparsed first passes)")
    print(f"  judge mean ${mean(judge_costs):.4f} over {len(judge_costs)} calls")

    print("\n== PER-TASK DETAIL ==")
    for r in rows:
        print(f"  {r['task_id']:<18} {r['shape']:<14} winner={r['winner']:<6} "
              f"slot_flash={r['slot_of_flash']} "
              f"rationale={r.get('rationale', '')[:80]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
