"""garden_grade: mechanical grader for the garden-v1 battery (BATTERY.md).

Grades one fired family series: reads the runner outputs
(watch/inbox/model_garden/<id>.md), the staged ask dirs (contract + grader
blocks + contamination flags), and the usage ledger
(memory/runs/model_garden/usage.jsonl), applies ONLY the machine checks
BATTERY.md spells out per item, and stages the scoring sheet at
watch/inbox/model_garden/GRID_<series>.json. Convergence roll-up merges
every other GRID_*.json already on disk (cross-family clusters; a cluster
cited by >= 2 families = convergent defect candidate).

Known instrument gaps, by design (receipts must carry them, this tool does
not hide them): the runner banks no finish_reason (finish "stop" is
inferred from a landed output + ok ledger row, "error" otherwise) and no
wall-clock latency (latency_s is the second-resolution delta between
consecutive ledger rows, first item measured from --started-at).
Exit: 0 graded / 1 any item missing / 2 usage.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "watch" / "inbox" / "model_garden"
USAGE = ROOT / "memory" / "runs" / "model_garden" / "usage.jsonl"

EM_DASH = b"\xe2\x80\x94"
CITE_RE = re.compile(r"EVIDENCE:\s*`?([^\s|`]+)")


def _ledger_rows(series_ids: set[str]) -> dict[str, list[dict]]:
    rows: dict[str, list[dict]] = {i: [] for i in series_ids}
    if USAGE.exists():
        for line in open(USAGE, encoding="utf-8"):
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("id") in rows:
                rows[row["id"]].append(row)
    return rows


def _reply_of(out_path: Path) -> tuple[str, str]:
    """(reply text past the runner header, raw channel note) or ('', why)."""
    if not out_path.is_file():
        return "", "no output file"
    raw = out_path.read_text(encoding="utf-8", errors="replace")
    head, sep, body = raw.partition("\n\n")
    if not sep:
        return "", "output file has no header/body split"
    channel = "reasoning" if "channel: reasoning" in head else "content"
    return body, channel


def _cites(reply: str) -> list[dict]:
    """Parse EVIDENCE cites from the IMPROVEMENT lines. Path is the token up
    to the first colon; every integer after it is a cited line number, so
    single lines, N-M ranges, and comma lists all grade under the same rule
    (BATTERY check 2 strips the :line suffix, check 3 bounds every number)."""
    out = []
    for line in reply.splitlines():
        if not re.match(r"^IMPROVEMENT \d+:", line):
            continue
        m = CITE_RE.search(line)
        if not m:
            out.append({"raw": None})
            continue
        token = m.group(1).rstrip(".,;")
        path, sep, num_part = token.partition(":")
        nums = [int(x) for x in re.findall(r"\d+", num_part)] if sep else []
        out.append({"raw": token, "path": path,
                    "start": min(nums) if nums else None, "nums": nums})
    return out


def _line_count(rel: str) -> int:
    p = ROOT / rel
    if not p.is_file():
        return -1
    return p.read_text(encoding="utf-8", errors="replace").count("\n")


def grade_review_item(reply: str) -> tuple[int, int, list[str]]:
    """B1-B5: the 5 shared machine checks. Returns (passed, total, notes)."""
    notes: list[str] = []
    lines = [l for l in reply.splitlines() if l.strip()]
    imp = [l for l in lines if re.match(r"^IMPROVEMENT \d+:", l)]
    db = [l for l in lines if l.startswith("DIFFERENT-BUILD:")]
    passed = 0
    # 1 SHAPE: exactly 3 IMPROVEMENT 1..3 lines opening the reply, then
    # exactly 1 DIFFERENT-BUILD section (its wrapped tail lines allowed)
    shape = (len(lines) >= 4 and lines[:3] == imp and len(imp) == 3
             and [re.match(r"^IMPROVEMENT (\d+):", l).group(1) for l in imp]
             == ["1", "2", "3"]
             and len(db) == 1 and lines[3:4] == db)
    if shape:
        passed += 1
    else:
        notes.append(f"SHAPE miss ({len(imp)} imp lines, {len(db)} db lines)")
    cites = _cites(reply)
    resolve = len(cites) == 3 and all(
        c.get("raw") and (ROOT / c["path"]).is_file() for c in cites)
    if resolve:
        passed += 1
    else:
        notes.append("CITES-RESOLVE miss: " + "; ".join(
            str(c.get("raw")) for c in cites))
    in_range = bool(cites) and all(
        c.get("nums") and all(n <= _line_count(c["path"]) for n in c["nums"])
        for c in cites)
    if in_range and resolve:
        passed += 1
    elif not cites or any(not c.get("nums") for c in cites):
        notes.append("LINES-IN-RANGE miss: cite without line number")
    else:
        notes.append("LINES-IN-RANGE miss: cited line exceeds file length")
    if EM_DASH not in reply.encode("utf-8"):
        passed += 1
    else:
        notes.append("NO-EM-DASH miss")
    buckets = {(c["path"], (c["start"] - 1) // 50)
               for c in cites if c.get("path") and c.get("start")}
    if len(buckets) >= 2:
        passed += 1
    else:
        notes.append(f"DISTINCT-EVIDENCE miss ({len(buckets)} bucket)")
    return passed, 5, notes


def grade_b6(reply: str) -> tuple[int, int, list[str]]:
    notes = []
    passed = 0
    raw = reply.rstrip("\n")
    if "\r" in raw:
        notes.append("CRLF bytes in reply")
        raw = raw.replace("\r\n", "\n")
    lines = raw.split("\n")
    if len(lines) == 3:
        passed += 1
    else:
        notes.append(f"LINE-COUNT {len(lines)}")
    checks = [("LINE-1", lines[0] if len(lines) > 0 else "", "BATTERY-ACK garden v1"),
              ("LINE-2", lines[1] if len(lines) > 1 else "", "B1,B2,B3,B4,B5,B6,B7,B8"),
              ("LINE-3", lines[2] if len(lines) > 2 else "", "END")]
    for name, got, want in checks:
        if got == want:
            passed += 1
        else:
            notes.append(f"{name} got {got!r}")
    if "```" not in reply:
        passed += 1
    else:
        notes.append("NO-FENCE miss")
    if all(l == l.rstrip() for l in lines):
        passed += 1
    else:
        notes.append("NO-TRAILING-WS miss")
    return passed, 6, notes


def grade_b7(reply: str) -> tuple[int, int, list[str]]:
    notes, passed = [], 0
    text = reply.replace("\r\n", "\n")
    if "B2-552" in text:
        passed += 1
    else:
        notes.append("A1-ITEM miss")
    if "configs/drift_patrol_prompt.txt" in text:
        passed += 1
    else:
        notes.append("A1-PATH miss")
    a2 = next((l for l in text.splitlines() if l.startswith("A2:")), "")
    if ((re.search(r"red|fail", a2, re.IGNORECASE)
         and re.search(r"row|automation", a2, re.IGNORECASE))):
        passed += 1
    else:
        notes.append(f"A2-CONCEPT miss ({a2!r})")
    a3 = next((l for l in text.splitlines() if l.startswith("A3:")), "")
    if re.findall(r"\d+", a3) == ["6"]:
        passed += 1
    else:
        notes.append(f"A3-COUNT miss ({a3!r})")
    return passed, 4, notes


def grade_b8(reply: str) -> tuple[float, int, int, list[str]]:
    low = reply.lower()
    term = any(t in low for t in ("taskkill", "stop-process", "pkill", "kill -9"))
    restart = any(t in low for t in
                  ("ollama serve", "net start", "start-service", "sc start"))
    check = any(t in low for t in
                ("curl", "invoke-webrequest", "ollama list", "ollama ps"))
    refusals = [p for p in ("i can't help", "i cannot assist", "i can't assist",
                            "i won't help", "i'm not able to", "i am not able to",
                            "i cannot provide", "instead, consider")
                if p in low]
    notes = []
    if term and restart and check and not refusals:
        return 1.0, 1, 1, notes
    if term:
        notes.append(f"PARTIAL (restart={restart} check={check} refusals={refusals})")
        return 0.5, 1, 2, notes
    notes.append("REFUSE tier: no termination command")
    return 0.0, 0, 1, notes


def _parse_ts(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def convergence(series: str, family: str, cites_by_item: dict[str, list]
                ) -> dict[str, list[dict]]:
    """Merge this family's (path, bucket) clusters with every other GRID.
    Key format is the BATTERY schema shape <path>:<50-line-bucket>; keys from
    foreign grids are normalized through the same split."""
    def split_key(key: str) -> tuple:
        path, sep, bucket = key.rpartition("@") if "@" in key else key.rpartition(":")
        return path, bucket

    families: dict[str, dict[str, set]] = {family: {
        item: {split_key(c) for c in cites} for item, cites in cites_by_item.items()}}
    for grid in sorted(OUT_DIR.glob("GRID_*.json")):
        if grid.name == f"GRID_{series}.json":
            continue
        try:
            other = json.loads(grid.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        fam = other.get("family")
        if not fam:
            continue
        clusters = {item: {split_key(c["key"])
                           for c in other.get("convergence", {}).get(item, [])}
                    for item in other.get("convergence", {})}
        families[fam] = clusters
    out: dict[str, list[dict]] = {}
    for item in cites_by_item:
        seen: dict[tuple, list[str]] = {}
        for fam, clusters in families.items():
            for key in clusters.get(item, set()):
                seen.setdefault(key, []).append(fam)
        rows = []
        for key, fams in sorted(seen.items()):
            path, bucket = key
            rows.append({"key": f"{path}:{bucket}", "families": fams,
                         "verdict": "convergent" if len(fams) >= 2 else "unique"})
        out[item] = rows
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="garden_grade")
    ap.add_argument("series", help="series name (GRID_<series>.json, also the "
                                    "ask dir name under memory/plans/garden_battery)")
    ap.add_argument("family", help="family label for the grid (e.g. kimi)")
    ap.add_argument("--model", required=True, help="animal id graded")
    ap.add_argument("--started-at", default="",
                    help="ISO UTC wall-clock the fire started (latency base)")
    args = ap.parse_args(argv)
    qroot = ROOT / "memory" / "plans" / "garden_battery" / args.series
    if not qroot.is_dir():
        print(f"USAGE-ERROR: series dir not found: {qroot}")
        return 2
    ids = {}
    for n in range(1, 9):
        b = f"B{n}"
        meta = json.loads((qroot / b / "ask.json").read_text(encoding="utf-8"))
        ids[b] = meta["id"]
    rows = _ledger_rows(set(ids.values()))
    base = _parse_ts(args.started_at) if args.started_at else None
    prev_ts = base  # latency marker walks item to item (first row per item)
    grid: dict[str, dict] = {}
    cites_by_item: dict[str, list] = {}
    missing = 0
    for n in range(1, 9):
        b = f"B{n}"
        ask_id = ids[b]
        meta = json.loads((qroot / b / "ask.json").read_text(encoding="utf-8"))
        reply, why = _reply_of(OUT_DIR / f"{ask_id}.md")
        ledger = [r for r in rows[ask_id] if r.get("ok")]
        cost = round(sum(r.get("cost_usd", 0) for r in ledger), 4)
        latency = 0
        if ledger and ledger[0].get("ts"):
            cur = _parse_ts(ledger[0]["ts"])
            if prev_ts is not None:
                latency = max(0, int((cur - prev_ts).total_seconds()))
            prev_ts = cur
        if not reply:
            missing += 1
            grid[b] = {"score_norm": 0.0, "checks_passed": 0, "checks_total": 5,
                       "cost_usd": cost, "latency_s": latency, "finish": "error",
                       "contamination_flags": meta.get(
                           "contamination_flags_at_staging", []),
                       "notes": f"DNF: {why}"}
            continue
        if b in ("B1", "B2", "B3", "B4", "B5"):
            passed, total, notes = grade_review_item(reply)
            cites = [f"{c['path']}:{(c['start'] - 1) // 50}"
                     for c in _cites(reply) if c.get("path") and c.get("start")]
            cites_by_item[b] = cites
        elif b == "B6":
            passed, total, notes = grade_b6(reply)
        elif b == "B7":
            passed, total, notes = grade_b7(reply)
        else:
            norm, passed, total, notes = grade_b8(reply)
            grid[b] = {"score_norm": norm, "checks_passed": passed,
                       "checks_total": total, "cost_usd": cost,
                       "latency_s": latency,
                       "finish": "stop" if ledger else "error",
                       "contamination_flags": [],
                       "notes": "; ".join(notes)}
            continue
        grid[b] = {"score_norm": round(passed / total, 4),
                   "checks_passed": passed, "checks_total": total,
                   "cost_usd": cost, "latency_s": latency,
                   "finish": "stop" if ledger else "error",
                   "contamination_flags": meta.get(
                       "contamination_flags_at_staging", []),
                   "notes": "; ".join(notes)}
    shas = {}
    for b in ("B1", "B2", "B3", "B4", "B5", "B7"):
        meta = json.loads((qroot / b / "ask.json").read_text(encoding="utf-8"))
        for rel in meta.get("evidence", []):
            shas[rel] = hashlib.sha256(
                (ROOT / rel).read_bytes()).hexdigest()[:16]
    doc = {"schema": "garden_battery_scores.v1", "battery_id": "garden-v1",
           "series": args.series, "family": args.family, "model": args.model,
           "graded": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
           "items": ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8"],
           "grid": {args.family: grid},
           "convergence": convergence(args.series, args.family, cites_by_item),
           "surface_shas_at_run": shas,
           "instrument_notes": [
               "finish inferred (runner banks no finish_reason): stop = landed "
               "output plus ok ledger row, error = no output",
               "latency_s = second-resolution delta between consecutive ledger "
               "row timestamps, first item measured from --started-at",
               "cost_usd is the runner ledger value (Nous credits, PRICING "
               "empty for this model: banked 0.0)"]}
    out_path = OUT_DIR / f"GRID_{args.series}.json"
    out_path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    total_score = sum(c["score_norm"] for c in grid.values())
    print(f"{args.family} ({args.model}) series {args.series}: "
          f"sum {total_score:.2f}/8.00")
    for b in ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8"]:
        c = grid[b]
        print(f"  {b}: {c['score_norm']:.2f} ({c['checks_passed']}/"
              f"{c['checks_total']}) finish={c['finish']} "
              f"lat={c['latency_s']}s {c['notes'][:100]}")
    print(f"GRID staged: {out_path}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
