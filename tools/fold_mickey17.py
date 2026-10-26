#!/usr/bin/env python3
"""fold_mickey17.py — deterministic fold of the Mickey 17 digestion wave.

Reads every memory/runs/mickey17/digest_*.jsonl, recounts by script (never trusting
agent self-reports), and writes the MASTER_INDEX + OPERATOR_BRIEFING markdown.
"""
import glob
import json
import os
import re
from collections import Counter, defaultdict

RUNS = os.path.join(os.path.dirname(__file__), "..", "memory", "runs", "mickey17")

def main():
    rows = []
    lanes = defaultdict(Counter)
    for p in sorted(glob.glob(os.path.join(RUNS, "digest_*.jsonl"))):
        lane = re.sub(r"_\d+$", "", os.path.basename(p)[len("digest_"):].replace(".jsonl", ""))
        for line in open(p, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                lanes[lane]["parse_error"] += 1
                continue
            d["_lane"] = lane
            rows.append(d)
            lanes[lane][d.get("status", "?")] += 1

    tot = Counter(r.get("status", "?") for r in rows)
    # W4 lesson (2026-09-25): runs shipped summaries with no verdict for 24 days.
    # The summary now renders the verdict field and screams when it is missing.
    verdicts = Counter(r.get("verdict") or "" for r in rows)
    unverified = sum(1 for v in verdicts.items() if not v[0])
    out = ["# MICKEY 17 — MASTER INDEX (2026-09-20)", "",
           f"Recounted by script from {len(glob.glob(os.path.join(RUNS, 'digest_*.jsonl')))} register files. "
           f"{len(rows)} files of the estate digested.", "",
           "## TOTALS", "",
           "| status | count |", "|---|---|"]
    for k in ("LIVE", "DONE", "OWED", "STALE"):
        out.append(f"| {k} | {tot.get(k, 0)} |")
    out += ["", "## VERDICTS", "",
            f"rows with a verdict: {len(rows) - unverified} / {len(rows)}"]
    for v, n in verdicts.most_common():
        if v:
            out.append(f"- {v}: {n}")
    if unverified:
        out.append(f"- **{unverified} rows carry NO verdict — unevaluated work is not done work.**")
    out += ["", "## BY LANE", "", "| lane | files | LIVE | DONE | OWED | STALE |", "|---|---|---|---|---|---|"]
    for lane in sorted(lanes):
        c = lanes[lane]
        n = sum(v for k, v in c.items() if k != "parse_error")
        out.append(f"| {lane} | {n} | {c.get('LIVE', 0)} | {c.get('DONE', 0)} | {c.get('OWED', 0)} | {c.get('STALE', 0)} |")

    # Cross-slice convergence: same-ish steal text appearing across lanes
    steal_words = Counter()
    for r in rows:
        s = (r.get("steal") or "")
        if not s or s == "null":
            continue
        wl = re.findall(r"[a-zA-Z_]{4,}", s.lower())
        for w in set(wl):
            steal_words[w] += 1
    hot = [w for w, c in steal_words.most_common(40) if c >= 4 and w not in
           ("the", "with", "that", "this", "into", "from", "fleet", "card", "operator", "memory", "build")]
    out += ["", "## CONVERGING ACTION-WORDS (appearing in 4+ slices' steals)", ""]
    out.append(", ".join(f"{w}×{steal_words[w]}" for w in hot[:24]))

    out += ["", "## ROWS", "", "<details><summary>full register (one line per estate file)</summary>", ""]
    for r in sorted(rows, key=lambda x: (x["_lane"], x.get("file", ""))):
        vd = f" [verdict: {r['verdict']}]" if r.get("verdict") else ""
        out.append(f"- **[{r.get('status','?')}]** `{r.get('file','?')}` — {r.get('what','')}{vd}")
    out += ["", "</details>", ""]
    with open(os.path.join(RUNS, "MASTER_INDEX_20260920.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"rows={len(rows)} lanes={len(lanes)} totals={dict(tot)}")
    print("master index ->", os.path.join(RUNS, "MASTER_INDEX_20260920.md"))

if __name__ == "__main__":
    main()
