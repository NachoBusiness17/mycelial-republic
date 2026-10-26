"""B2-205 falsifier recount: quorum_* VERDICT.md files re-scored under the
p4 self-vote exclusion (author chair ABSTAIN on its own addition).

Read-only. For every memory/runs/salons/quorum_<date>[_variant] dir that has
FOLD.md + p4/*.md, this re-derives both rules from the same bytes the verdict
was written from:
  OLD: >=2/3 of ALL P1-returning chairs (paper denominator, all votes count)
  NEW: >=2/3 of the eligible set per addition (author excluded from tally and
       denominator)
and reports per-addition flips (PASSED<->NOT PASSED).

Run: .venv/Scripts/python.exe watch/inbox/burn_wave_20260926/B2_205_quorum_recount.py
"""
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SALONS = ROOT / "memory" / "runs" / "salons"
VOTE_RE = re.compile(r"VOTE:\s*(A\d+)\s+(YES|NO-WITH-OBJECTION)")


def recount_dir(d: Path) -> dict | None:
    fold = d / "FOLD.md"
    p4dir = d / "p4"
    if not fold.is_file() or not p4dir.is_dir():
        return None
    fold_text = fold.read_text(encoding="utf-8", errors="replace")
    add_block = fold_text.split("## DISSENT LOG")[0]
    add_author: dict[str, str] = {}
    for m in re.finditer(r"\*\*(A\d+)\*\*\s*\[[^\]]*\]\s*\(([^)\n]+)\)", add_block):
        add_author.setdefault(m.group(1), m.group(2).strip())
    add_ids = sorted(set(re.findall(r"\*\*(A\d+)\*\*", add_block)))
    if not add_ids:
        return None
    votes: dict[str, dict[str, str]] = {}
    for p in sorted(p4dir.glob("*.md")):
        if p.stem == "rejected_raw":
            continue
        raw = p.read_text(encoding="utf-8", errors="replace")
        votes[p.stem] = {m.group(1): m.group(2)
                         for m in (VOTE_RE.search(ln) for ln in raw.splitlines()) if m}
    denom = len(votes)
    need = math.ceil(2 * denom / 3)
    rows = []
    for aid in add_ids:
        author = add_author.get(aid)
        yes_all = sorted(c for c, v in votes.items() if v.get(aid) == "YES")
        yes_new = [c for c in yes_all if c != author]
        denom_new = denom - (1 if author in votes else 0)
        need_new = math.ceil(2 * denom_new / 3)
        old = len(yes_all) >= need
        new = len(yes_new) >= need_new
        rows.append({
            "addition": aid, "author": author or "-",
            "old_yes": len(yes_all), "old_denom": denom, "old_need": need,
            "old_passed": old,
            "new_yes": len(yes_new), "new_denom": denom_new, "new_need": need_new,
            "new_passed": new,
            "flip": ("PASSED->NOT PASSED" if old and not new
                     else "NOT PASSED->PASSED" if new and not old else "same"),
            "self_vote_cast": (author in votes and votes.get(author, {}).get(aid) == "YES"),
        })
    return {"dir": str(d.relative_to(ROOT)), "chairs": denom, "rows": rows}


def main() -> int:
    out = []
    if SALONS.is_dir():
        for d in sorted(SALONS.iterdir()):
            if d.is_dir() and d.name.startswith("quorum_"):
                r = recount_dir(d)
                if r:
                    out.append(r)
    flips = [row for r in out for row in r["rows"] if row["flip"] != "same"]
    selfs = [row for r in out for row in r["rows"] if row["self_vote_cast"]]
    print(json.dumps({"runs_recounted": len(out), "additions_recounted": sum(len(r["rows"]) for r in out),
                      "pivotal_self_votes_found": len(selfs), "outcome_flips": len(flips),
                      "flips": flips, "detail": out}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
