"""Cartographer cycle 20261012: fold the nacho walk into thread -> decision ->
filed-law-or-debt rows. Reads nacho_walk.jsonl plus the two parent ask files.
Verdict grammar (deterministic, from write targets and ask shape):
  FILED_STEAL      wrote STEAL_* memory
  FILED_PROOF      produced afk speak_proof / speak string evidence
  FILED_SURFACE    wrote dashboard/static (wave/table) or produced/ code
  FILED_STEER      filed party_subchain/steer one-liners
  ROUTINE_FIRE     routine automation fire, nothing else filed
  BARE             no write signal at all
A thread can carry multiple verdicts (ordered by the list above).
"""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "watch" / "inbox" / "mates_leave_protocol" / "receipts" / "cartographer_20261012_data"
LOGS = ROOT / "logs" / "mates" / "cartographer"

FIRE_RE = re.compile(r"fired (\d+/\d+/\d+), (\d+:\d+:\d+) (AM|PM)")


def load_walk():
    return [json.loads(l) for l in (DATA / "nacho_walk.jsonl").open(encoding="utf-8")]


def verdicts(r):
    wt = " ".join(r["write_targets"].keys())
    v = []
    if "STEAL_" in wt or "memory/steal" in wt or "memory\\steal" in wt:
        v.append("FILED_STEAL")
    if "speak_proof" in wt:
        v.append("FILED_PROOF")
    if "dashboard/static/wave" in wt or "dashboard/static/table" in wt or "mag-live" in wt or "mag-patch" in wt:
        v.append("FILED_SURFACE")
    if "party_subchain/steer" in wt or "party_subchain\\steer" in wt or "steer_line" in wt:
        v.append("FILED_STEER")
    if not v:
        v = ["BARE"]
    return v


def main():
    rows = load_walk()
    out = []
    for r in rows:
        is_routine = bool(r["first_ask"] or "") and "AFK game chord" in (r["first_ask"] or "")
        v = verdicts(r)
        top_writes = list(r["write_targets"].items())[:6]
        decision = (r["first_ask"] or "")[:180].replace("\n", " ")
        out.append({
            "id": r["id"],
            "role": "subagent" if r["id"].startswith("sand-subagent") else "parent",
            "bytes": r["bytes"],
            "lines": r["lines"],
            "first_ts": r["first_ts"],
            "last_ts": r["last_ts"],
            "user_msgs": r["user_msgs"],
            "assistant_msgs": r["assistant_msgs"],
            "decision_extract": decision,
            "verdicts": v,
            "top_writes": top_writes,
            "law_hits": r["law_hits"],
        })
    with (DATA / "nacho_thread_map.jsonl").open("w", encoding="utf-8") as w:
        for o in out:
            w.write(json.dumps(o, ensure_ascii=False) + "\n")

    verdict_counter = Counter()
    for o in out:
        for v in o["verdicts"]:
            verdict_counter[v] += 1

    # routine fire census across all transcripts (unique fire timestamps)
    fires = set()
    ct = ROOT / "corpus" / "oral_history" / "nacho_archaeology" / "extracted" / \
        "nacho-archaeology-part1-chats-produced" / "chat-transcripts"
    for f in ct.glob("*/*.jsonl"):
        for line in f.open(encoding="utf-8", errors="replace"):
            if "AFK game chord" in line and "fired" in line:
                m = FIRE_RE.search(line)
                if m:
                    fires.add(f"{m.group(1)} {m.group(2)} {m.group(3)}")

    # unique-ask dedup for both parents
    dedup = {}
    for tid in ("4a30dd44", "3d371c13"):
        rows_p = [json.loads(l) for l in (DATA / ("nacho_parent_asks_" + tid + ".jsonl")).open(encoding="utf-8")]
        uniq = {}
        for a in rows_p:
            key = (a["ts"], a["text"][:120])
            uniq.setdefault(key, a)
        dedup[tid] = {"total_rows": len(rows_p), "unique": len(uniq)}

    summary = {
        "threads": len(out),
        "verdicts_multi_count": dict(verdict_counter),
        "primary_verdicts": dict(Counter(o["verdicts"][0] for o in out)),
        "routine_fires_unique": len(fires),
        "routine_fires_first": sorted(fires)[0] if fires else None,
        "routine_fires_last": sorted(fires)[-1] if fires else None,
        "parent_ask_dedup": dedup,
    }
    (DATA / "nacho_fold_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
