#!/usr/bin/env python3
"""DOLLAR BURN sweep aggregator (2026-10-01).

Reads targets.jsonl (grep sets) + results_*.jsonl (DeepSeek verdicts), emits:
  - sweep_grid.json  (machine copy: every file, per-organ verdict + line + reason)
  - aggregate.json   (counts per organ, worst files, delta inputs, cost, empties)
No em-dashes in emitted files (lane law).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

WORK = Path(__file__).resolve().parent
ROOT = WORK.parents[3]

V = re.compile(r"^([abc])\)\s*(YES-compliant|NO-violation|NA)\s*(?:line\s*(\d+))?\s*(?:-\s*)?(.*)$")

ORGANS = ("a", "b", "c")
ORGAN_NAMES = {
    "a": "LLM fire path without mag.inference_budget",
    "b": "remote fetch without browser User-Agent",
    "c": "json/jsonl write without atomic tmp+replace",
}


def main() -> None:
    targets = {}
    for line in (WORK / "targets.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            t = json.loads(line)
            targets[t["id"]] = t

    rows = []
    empties, unparseable = [], []
    for res in sorted(WORK.glob("results_*.jsonl")):
        for line in res.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            rows.append(json.loads(line))

    grid = {}
    for r in rows:
        fid = r["id"]
        verdicts = {}
        for ln in (r.get("out") or "").splitlines():
            m = V.match(ln.strip())
            if m:
                verdicts[m.group(1)] = {
                    "v": m.group(2),
                    "line": int(m.group(3)) if m.group(3) else None,
                    "why": m.group(4).strip()[:120],
                }
        if not r.get("ok"):
            empties.append({"id": fid, "attempts": r.get("attempts"), "out": (r.get("out") or "")[:160]})
        elif len(verdicts) != 3:
            unparseable.append({"id": fid, "out": (r.get("out") or "")[:200]})
        grid[fid] = {
            "ok": bool(r.get("ok")),
            "verdicts": verdicts,
            "cost_usd": r.get("cost_usd", 0.0),
            "attempts": r.get("attempts"),
        }

    def verdict(fid: str, organ: str) -> str:
        g = grid.get(fid)
        if not g or not g["ok"] or organ not in g["verdicts"]:
            return "MISSING"
        return g["verdicts"][organ]["v"]

    counts = {o: {"YES-compliant": 0, "NO-violation": 0, "NA": 0, "MISSING": 0} for o in ORGANS}
    for fid in grid:
        for o in ORGANS:
            counts[o][verdict(fid, o)] += 1

    # worst files: violations desc, then applicable organs desc, then path
    def score(fid: str):
        v = [verdict(fid, o) for o in ORGANS]
        nviol = v.count("NO-violation")
        napp = nviol + v.count("YES-compliant")
        return (-nviol, -napp, fid)

    worst = sorted(grid, key=score)[:10]

    # delta vs census: census frame was mag/+tools/ only; ours is mag/+tools/+server/+scripts/+main.py
    def in_census_frame(fid: str) -> bool:
        return fid.startswith("mag/") or fid.startswith("tools/")

    sweep_fire_applicable = [f for f in grid if verdict(f, "a") != "NA"]
    sweep_fetch_applicable = [f for f in grid if verdict(f, "b") != "NA"]
    sweep_write_violators = [f for f in grid if verdict(f, "c") == "NO-violation"]
    census_frame_fire = [f for f in sweep_fire_applicable if in_census_frame(f)]
    census_frame_fetch = [f for f in sweep_fetch_applicable if in_census_frame(f)]

    # grep-set vs model disagreements (denominator audit)
    grep_fire_na = [f for f in grid if targets.get(f, {}).get("fire_lines") and verdict(f, "a") == "NA"]
    grep_fetch_na = [f for f in grid if targets.get(f, {}).get("fetch_lines") and verdict(f, "b") == "NA"]
    grep_write_na = [f for f in grid if targets.get(f, {}).get("write_lines") and verdict(f, "c") == "NA"]
    model_fire_new = [f for f in grid if not targets.get(f, {}).get("fire_lines") and verdict(f, "a") != "NA"]
    model_write_new = [f for f in grid if not targets.get(f, {}).get("write_lines") and verdict(f, "c") == "NO-violation"]
    model_fetch_new = [f for f in grid if not targets.get(f, {}).get("fetch_lines") and verdict(f, "b") != "NA"]

    total_cost = round(sum(g["cost_usd"] for g in grid.values()), 4)
    out = {
        "files_swept": len(grid),
        "targets_selected": len(targets),
        "batches": len(list(WORK.glob("results_*.jsonl"))),
        "total_cost_usd": total_cost,
        "attempt_histogram": {},
        "empties": empties,
        "unparseable": unparseable,
        "organ_counts": counts,
        "organ_names": ORGAN_NAMES,
        "worst_10": [
            {
                "file": f,
                "a": verdict(f, "a"),
                "b": verdict(f, "b"),
                "c": verdict(f, "c"),
                "lines": {o: grid[f]["verdicts"].get(o, {}).get("line") for o in ORGAN_NAMES},
                "reasons": {o: grid[f]["verdicts"].get(o, {}).get("why", "") for o in ORGAN_NAMES},
            }
            for f in worst
        ],
        "census_delta": {
            "sweep_fire_applicable_total": len(sweep_fire_applicable),
            "sweep_fire_applicable_mag_tools_only": len(census_frame_fire),
            "census_hand_claim_fire_files_mag_tools": 184,
            "fire_YES_compliant_files": [f for f in grid if verdict(f, "a") == "YES-compliant"],
            "sweep_fetch_applicable_total": len(sweep_fetch_applicable),
            "sweep_fetch_applicable_mag_tools_only": len(census_frame_fetch),
            "census_hand_claim_fetch_files_mag_tools": 141,
            "sweep_write_violators_total": len(sweep_write_violators),
            "sweep_write_violators": sorted(sweep_write_violators),
            "grep_fire_but_model_NA": sorted(grep_fire_na),
            "grep_fetch_but_model_NA": sorted(grep_fetch_na),
            "grep_write_but_model_NA": sorted(grep_write_na),
            "model_fire_no_grep_hit": sorted(model_fire_new),
            "model_fetch_no_grep_hit": sorted(model_fetch_new),
            "model_write_violation_no_grep_hit": sorted(model_write_new),
        },
    }
    att = {}
    for g in grid.values():
        att[g["attempts"]] = att.get(g["attempts"], 0) + 1
    out["attempt_histogram"] = att

    (WORK / "sweep_grid.json").write_text(
        json.dumps(grid, indent=1, sort_keys=True), encoding="utf-8")
    (WORK / "aggregate.json").write_text(
        json.dumps(out, indent=1, sort_keys=True), encoding="utf-8")

    slim = {k: v for k, v in out.items()
            if k not in ("organ_names", "census_delta")}
    slim["census_delta_sizes"] = {k: (len(v) if isinstance(v, list) else v)
                                  for k, v in out["census_delta"].items()}
    print(json.dumps(slim, indent=1))


if __name__ == "__main__":
    main()
