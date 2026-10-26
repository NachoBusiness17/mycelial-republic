#!/usr/bin/env python3
"""ractor_salon -- put the kabuki cast on the day's evidence.

Self-stolen: the cast, personas and word caps come from configs/kabuki_cast.json
(kabuki_cast.v1, 2026-09-07). Nothing here invents a voice.

Law of the brief: it carries EVIDENCE and OPEN QUESTIONS, never the conclusion.
If the brief states what should be done, the cast only ratifies it and the salon
is decoration (the 2026-10-24 map audit: a framing in the map is adopted, not
audited).

    python tools/ractor_salon.py --lanes a,b,c --workers 6
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from burn_lanes import LANES, http_lane  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CAST = json.loads((ROOT / "configs" / "kabuki_cast.json").read_text(encoding="utf-8"))
OUT = ROOT / "memory" / "runs" / "ractor_salon"

BRIEF = """EVIDENCE — one working day on a local agent estate, 2026-10-24.

1. PARABLE GRID (40 calls, 10 lanes, 4 lens briefs). Each brief asked for a parable
   in one thinker's idiom. When the brief FORBADE the neighbouring thinker's
   vocabulary: 4/10 outputs were clean. With no prohibition: 8/10. With a second-pass
   self-audit: 9/10 in both cases, but one silence per cell.

2. MAP AUDIT (120 calls). Two maps of the same estate were given to ten lenses on six
   lanes. The false map contained two planted lies. Models called the planted lie
   "false" only 5% of the time, but "unverifiable" 90% of the time. On the true map,
   1.8% of answers called a true premise false.

3. LENS RUN (100 calls). One map, ten lenses, one open decision. Raw decisions looked
   maximally diverse (51 distinct strings in 52 answers). Clustered semantically, 42%
   converged on the same action and 8 of 10 lenses ranked it first. 47 calls returned
   nothing at all.

4. ERASURE FIX. The empty-answer bug was already solved in the repo (reasoning effort
   dial + 4x retry + bank the reasoning tail). Adopting it took the z.ai lanes from
   0/7 answered to 5/5.

5. QUEUE CENSUS. The estate believed it had 1,521 open items and no consumer. Measured:
   2,388 open, 62.5% are probe_* model chatter, ~750 distinct live observations, and
   sixteen existing code files already read the queue.

OPEN QUESTIONS (no answer is implied or preferred)
  - Which of the five findings is load-bearing, and which is instrumentation?
  - What should this estate stop doing?
  - What would make a future claim here trustworthy?

YOUR TASK: in at most {max_words} words, as {stage_name}, give (a) the one thing that
must change, (b) the evidence in the brief that supports it, (c) one falsifier that
would prove you wrong. Plain text, no preamble, no headings.
"""


def cell(lane: dict, actor: dict, brief: str = BRIEF) -> dict:
    prompt = brief.format(max_words=actor["max_words"], stage_name=actor["stage_name"])
    res = http_lane(lane, f"{actor['persona']}\n\n{prompt}", 1400)
    return {"actor": actor["stage_name"], "seat": actor.get("seat"), "lane": lane["id"],
            "ok": bool(res.get("ok")), "chars": res.get("chars", 0),
            "cost_usd": res.get("cost_usd") or 0, "attempt": res.get("attempt") or 1,
            "text": (res.get("text") or "")[:1800], "error": res.get("error")}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lanes", default="deepseek-flash,deepseek-v4-pro,groq-nacho,groq-sd,ollama-nacho,ollama-sd")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--report", default=None)
    ap.add_argument("--brief", default=None, help="path to a brief template with {max_words}/{stage_name}")
    args = ap.parse_args(argv)

    if args.report:
        rows = [json.loads(l) for l in Path(args.report).read_text(encoding="utf-8").splitlines() if l.strip()]
        by = defaultdict(list)
        for r in rows:
            if r.get("ok") and len(r.get("text", "")) > 120:
                by[r["actor"]].append(r)
        for actor, rs in by.items():
            print(f"\n=== {actor} ({len(rs)} voices) ===")
            for r in rs[:2]:
                print(f"  [{r['lane']}] {r['text'][:420].strip()}")
        return 0

    want = set(args.lanes.split(","))
    lanes = [l for l in LANES if l["id"] in want]
    jobs = [(lane, actor) for actor in CAST["actors"] for lane in lanes]
    OUT.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = OUT / f"salon_{stamp}.jsonl"
    brief = Path(args.brief).read_text(encoding="utf-8") if args.brief else BRIEF
    rows = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futs = {pool.submit(cell, lane, actor, brief): (lane, actor) for lane, actor in jobs}
        for fut in as_completed(futs):
            rows.append(fut.result())
    with path.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    ok = sum(1 for r in rows if r["ok"] and len(r.get("text", "")) > 120)
    print(f"receipt {path} · {len(rows)} calls · {ok} substantive · "
          f"${round(sum(r.get('cost_usd') or 0 for r in rows), 4)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
