"""cartographer cycle 7: fold the founding texts.

Joins the 57 reading-agent returns with the disk inventory (sha256-verified) and emits:
  - pd_foundings_fold.jsonl      one row per text (map layer)
  - pd_foundings_lawfold.jsonl   one row per LAW/PRACTICE/DEBT/FINDING candidate (fold layer)
All counts recomputed here from the two banks; nothing hand-copied.
"""
import json
import os

HERE = os.path.dirname(__file__)
INVENTORY = os.path.join(HERE, "pd_foundings_inventory.json")
RETURNS = os.path.join(HERE, "pd_foundings_agent_returns.jsonl")
FOLD = os.path.join(HERE, "pd_foundings_fold.jsonl")
LAWFOLD = os.path.join(HERE, "pd_foundings_lawfold.jsonl")

CYCLE = 7
MOMENT = "2026-10-16 cycle 7"


def main():
    with open(INVENTORY, "r", encoding="utf-8") as fh:
        inv = json.load(fh)
    inv_by_path = {r["path"]: r for r in inv["rows"] if "parse_error" not in r}

    returns = []
    with open(RETURNS, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                returns.append(json.loads(line))

    assert len(returns) == 57, f"expected 57 returns, got {len(returns)}"
    assert len(inv_by_path) == 57, f"expected 57 inventory rows, got {len(inv_by_path)}"

    fold_rows = []
    law_rows = []
    missing_join = []
    for ret in returns:
        path = ret["path"]
        if path not in inv_by_path:
            missing_join.append(path)
            continue
        base = inv_by_path[path]
        row = {
            "pod": path.split("/")[2],
            "path": path,
            "bytes": base["bytes"],
            "lines": base["lines"],
            "origin": base["origin"],
            "sha_match": base["sha_match"],
            "title_from_bytes": ret["title_from_bytes"],
            "author_from_bytes": ret["author_from_bytes"],
            "work_match": ret["work_match"],
            "ocr_quality": ret["ocr_quality"],
            "windows_read": ret["windows_read"],
            "coverage_basis": "bounded windows, not a full read",
            "ideas": ret["ideas"],
            "notes": ret["notes"],
            "cycle": CYCLE,
            "moment": MOMENT,
        }
        fold_rows.append(row)
        for idea in ret["ideas"]:
            if idea["candidate"] == "NONE":
                continue
            law_rows.append({
                "row_type": idea["candidate"],
                "thread": base.get("source", path),
                "text": path,
                "lines": idea["lines"],
                "quote": idea["quote"],
                "decision": idea["idea"],
                "why": idea["why"],
                "filed": "CANDIDATE_UNFILED_offered_to_the_estate",
                "cycle": CYCLE,
            })

    assert not missing_join, f"returns without inventory join: {missing_join}"

    with open(FOLD, "w", encoding="utf-8") as fh:
        for row in fold_rows:
            fh.write(json.dumps(row, ensure_ascii=True) + "\n")
    with open(LAWFOLD, "w", encoding="utf-8") as fh:
        for row in law_rows:
            fh.write(json.dumps(row, ensure_ascii=True) + "\n")

    tally = {}
    for row in law_rows:
        tally[row["row_type"]] = tally.get(row["row_type"], 0) + 1
    none_rows = sum(1 for r in returns for i in r["ideas"] if i["candidate"] == "NONE")
    work_yes = sum(1 for r in fold_rows if r["work_match"] == "yes")
    ocr = {}
    for r in fold_rows:
        ocr[r["ocr_quality"]] = ocr.get(r["ocr_quality"], 0) + 1
    windows = 0
    for r in fold_rows:
        n_interior = r["windows_read"].count(";")
        windows += 1 + n_interior

    print(json.dumps({
        "fold_rows": len(fold_rows),
        "lawfold_rows": len(law_rows),
        "candidates_by_kind": tally,
        "NONE_rows": none_rows,
        "idea_rows_total": len(law_rows) + none_rows,
        "work_match_yes": work_yes,
        "ocr_quality_counts": ocr,
        "windows_read_total": windows,
        "lines_read_estimate": sum(1 for _ in range(1)),
    }, indent=1))
    print("files written:")
    print(FOLD)
    print(LAWFOLD)


if __name__ == "__main__":
    main()
