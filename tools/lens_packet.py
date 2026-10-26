#!/usr/bin/env python3
"""lens_packet -- one map, ten lenses, many lanes; convergence is the measurement.

Law this tests (2026-10-24): a message cannot carry its own key. So the brief is a
MAP (relations only, no conclusions), the LENS is a question frame that makes one
class of feature salient, and the QUESTION is asked naked. If independent readers
with different frames converge on the same decision, the nuance was in the map.
If they scatter, the map is ambiguous - and the pattern of disagreement names the
ambiguous edge.

    python tools/lens_packet.py --lanes a,b,c --workers 6
    python tools/lens_packet.py --report memory/runs/lens/lens_XXXX.jsonl
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from burn_lanes import LANES, http_lane  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "memory" / "runs" / "lens"

# ── the map: relations only. No recommendation, no ranking, no "should". ──
MAP = """MAP — the explore queue, 2026-10-24

NODES
  explore.jsonl        3,482 rows; 1,521 status=open, 961 done/explored; writer appends
  explore_decay.jsonl  848 classification rows; marks open rows dead after 14d
  invariants.json      2,400 rows; 17 promoted to the readable surface; 963 edges
  falsifiers.jsonl     17 kill conditions; 6 checkable, 11 manual debts
  commit_sweeper.py    sole git writer; 10-minute cadence; singleton-guarded
  cockpit.py           8 signals, one next-action ladder; read-only
  receipts             memory/runs/* and watch/inbox/*; append-only, ignored by git
  budget               ~$0.03 per 40-call wave; free lanes carry most volume

EDGES
  writers -> explore.jsonl : percolator mine, seat runs, decay classifications
  explore.jsonl -> readers : NONE at present (no consumer process exists)
  invariants -> falsifiers : 17/17 promoted rows have a kill condition
  invariants -> explore    : promotion reads counts; explore does not feed promotion
  sweeper -> receipts      : commits only what the index holds; ignores memory/runs
  cockpit -> all           : reads every signal, writes nothing

CONSTRAINTS
  one writer per surface; the queue file is never rewritten, only appended
  a claim without a falsifier is a debt, not a finding
  anything >32MB stays out of git; history holds 15GB of old data-lake blobs
  free lanes: deepseek, z.ai coding, openrouter :free, nous, groq, ollama

OPEN EDGES (unknown, not merely unfinished)
  what a "candidate" is has no schema anywhere in the estate
  nobody has measured how many of the 1,521 are the same observation in different words
  the cost of consuming one row is unmeasured
"""

# ── lenses: each is a question frame, and none names its own answer ──
LENSES = {
    "fermat": "You are FERMAT. Ask only: what is the cheapest path that reaches the "
              "same place? Cost is measured in calls, bytes, and operator minutes.",
    "foucault": "You are FOUCAULT. Ask only: which arrangement makes this speak, and who "
                "benefits from the queue staying in its current state?",
    "diogenes": "You are DIOGENES. Ask only: what is everyone pretending not to see here?",
    "jung": "You are JUNG. Ask only: what has been disowned and given a seat elsewhere in "
            "the system, and what returns because of it?",
    "ellul": "You are ELLUL. Ask only: where has the method become autonomous - which step "
             "continues because it is the method, not because anyone chose it?",
    "mcluhan": "You are McLUHAN. Ask only: what does the FORM of this queue do to whoever "
               "reads it, independent of its contents?",
    "hall": "You are HALL. Ask only: who is the intended reader, who is the actual reader, "
            "and what does each decode differently?",
    "wallas": "You are WALLAS. Ask only: what desire is the motive power here, and which "
              "stage of the process is being skipped?",
    "bernays": "You are BERNAYS. Ask only: what would make this queue's output wanted, and "
               "by whom, before it is correct?",
    "baudrillard": "You are BAUDRILLARD. Ask only: where has the signal become its own "
                   "referent - which number is being produced for its own sake?",
}

QUESTION = ("Given the map, decide what to do about the 1,521 open rows. "
            "Return ONLY JSON: {\"decision_key\": \"<=6 words\", \"decision\": \"<=60 words\", "
            "\"hazards\": [\"...\"], \"blind_spot\": \"<=20 words\", \"confidence\": 0.0}")

LANE_SET = ["deepseek-flash", "deepseek-v4-pro", "zcode-1", "zcode-2", "zcode-3",
            "or-liquid", "or-flint", "or-nemotron", "nous-longcat", "nous-beam",
            "groq-nacho", "groq-sd", "ollama-nacho", "ollama-sd"]


def cluster(key: str) -> str:
    """Lexical distinctness overstates divergence: spawn_consumer /
    create consumer pipeline / process via free lanes are one decision.
    Cluster before counting (2026-10-24: 51/52 distinct became 7 symbols)."""
    k = (key or "").lower()
    if re.search(r"consumer|reader|pipeline|spawn|build.*(consumer|reader)|process via", k):
        return "build-consumer"
    if re.search(r"schema|definition|define|canonical|dedupe|cluster", k):
        return "define-schema"
    if re.search(r"prune|archive|delete|drop|discard|expire", k):
        return "prune"
    if re.search(r"freeze|stop|pause|halt|do not|don't|quarantine|hold", k):
        return "freeze-intake"
    if re.search(r"measure|audit|instrument|baseline|triage", k):
        return "measure-first"
    if re.search(r"demand", k):
        return "demand-first"
    return "other"


def parse_json(text: str) -> dict:
    t = (text or "").strip()
    if "{" in t and "}" in t:
        t = t[t.index("{"): t.rindex("}") + 1]
    try:
        d = json.loads(t)
        return d if isinstance(d, dict) else {}
    except Exception:  # noqa: BLE001
        return {}


def cell(lane: dict, lens_id: str) -> dict:
    prompt = f"{MAP}\n\nLENS: {LENSES[lens_id]}\n\nQUESTION: {QUESTION}"
    res = http_lane(lane, prompt, 1600)
    rec = {"lane": lane["id"], "lens": lens_id, "ok": bool(res.get("ok")),
           "latency_s": res.get("latency_s"), "cost_usd": res.get("cost_usd") or 0,
           "chars": res.get("chars", 0),
           "prompt_tokens": res.get("prompt_tokens") or 0,
           "completion_tokens": res.get("completion_tokens") or 0,
           "finish": res.get("finish"), "attempt": res.get("attempt") or 1}
    if not res.get("ok"):
        rec["error"] = res.get("error")
        return rec
    d = parse_json(res.get("text", ""))
    rec.update({"decision_key": (d.get("decision_key") or "").strip().lower()[:60],
                "decision": (d.get("decision") or "").strip()[:200],
                "hazards": d.get("hazards") or [],
                "blind_spot": (d.get("blind_spot") or "").strip()[:120],
                "confidence": d.get("confidence")})
    return rec


def report(path: Path) -> None:
    rows = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    ok = [r for r in rows if r.get("ok") and r.get("decision_key")]
    print(f"# {path.name}: {len(rows)} calls, {len(ok)} parsed")
    per_lens = defaultdict(list)
    for r in ok:
        per_lens[r["lens"]].append(r)
    print(f"{'lens':12s} {'n':>2s} {'distinct':>8s}  modal decision")
    for lens, rs in sorted(per_lens.items()):
        keys = Counter(cluster(r["decision_key"]) for r in rs)
        top, n = keys.most_common(1)[0]
        print(f"{lens:12s} {len(rs):2d} {len(keys):8d}  {n}/{len(rs)} :: {top[:48]}")
    allkeys = Counter(r["decision_key"] for r in ok)
    print(f"\ndistinct decisions overall: {len(allkeys)} across {len(ok)} answers")
    print(f"top 6: {allkeys.most_common(6)}")
    print("\n## what each lens saw that others did not (blind_spot)")
    for lens, rs in sorted(per_lens.items()):
        spots = Counter((r.get("blind_spot") or "").lower().strip() for r in rs if r.get("blind_spot"))
        if spots:
            text, n = spots.most_common(1)[0]
            print(f"  {lens:12s} {n}x {text[:88]}")
    print("\n## hazards named, by frequency")
    hz = Counter(h.lower().strip()[:60] for r in ok for h in (r.get("hazards") or []) if h)
    for h, n in hz.most_common(8):
        print(f"  {n:2d}x {h}")
    conf = [r["confidence"] for r in ok if isinstance(r.get("confidence"), (int, float))]
    if conf:
        print(f"mean confidence {sum(conf)/len(conf):.2f}")
    print(f"spend ${round(sum(r.get('cost_usd') or 0 for r in rows), 4)}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lanes", default=",".join(LANE_SET))
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--limit", type=int, default=100)
    ap.add_argument("--report", default=None)
    args = ap.parse_args(argv)
    if args.report:
        report(Path(args.report))
        return 0
    want = set(args.lanes.split(","))
    lanes = [l for l in LANES if l["id"] in want]
    lens_ids = list(LENSES)
    # round-robin both axes: 100 cells -> ~7 per lane, 10 per lens, evenly spread
    jobs = [(lanes[i % len(lanes)], lens_ids[i % len(lens_ids)])
            for i in range(args.limit)]
    OUT.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = OUT / f"lens_{stamp}.jsonl"
    rows = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futs = {pool.submit(cell, lane, lens): (lane, lens) for lane, lens in jobs}
        for fut in as_completed(futs):
            rows.append(fut.result())
    with path.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"receipt {path}")
    report(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
