"""Gopher packs — the fleet's S1 wave launcher (2026-09-19).

A pack is a pod of models in tandem over ONE packet (mag.verb.witness):
agreement is the verdict, disagreement or a transport death is purple and
escalates. A wave runs the RIB language's verbs over fleet-real packets and
feeds the Fleet-Bench meter with rows that carry non-model evidence, per the
falsifier's law. Class-C packets are recorded as owed operator adjudication,
never self-graded.

Usage:
    python scripts/gopher_packs.py --once    # one wave (free lanes, ~a dozen calls)
    python scripts/gopher_packs.py --check   # kifu chain + trigger status

The 24x7 drive: cron calls --once on cadence; the vow() rows make the
standing drive composable. Receipts land in queue/lanes/jev/trail.jsonl.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import verb  # noqa: E402

CURSOR = ROOT / "memory" / "runs" / "fleet_bench" / "harvest_cursor.json"


def _stable_id(pid: str, question: str, truth) -> str:
    h = hashlib.sha256((question + str(truth)).encode("utf-8")).hexdigest()[:8]
    return f"{pid}-{h}"


def harvest_kifu(k: int = 3) -> list:
    """JEV-1, first acre: kifu link checks as Class-A meter rows. Truth is
    recomputed from bytes (row[i+1].ph must equal row[i].h); the evidence
    rides in the question because the oracle has no disk. Offsets come from
    a rotating cursor -- sequence, never a clock -- so daily waves grow the
    labeled distribution instead of re-asking it."""
    rows = [json.loads(ln) for ln in
            verb.TRACE.read_text(encoding="utf-8").splitlines() if ln.strip()]
    links = [(i, rows[i].get("h"), rows[i + 1].get("ph"))
             for i in range(len(rows) - 1)
             if rows[i].get("h") and rows[i + 1].get("ph")]
    if not links:
        return []
    off = 0
    CURSOR.parent.mkdir(parents=True, exist_ok=True)
    if CURSOR.exists():
        off = json.loads(CURSOR.read_text(encoding="utf-8")).get("offset", 0) % len(links)
    picked = [links[(off + j) % len(links)] for j in range(min(k, len(links)))]
    CURSOR.write_text(json.dumps({"offset": (off + k) % len(links)}), encoding="utf-8")
    out = []
    for i, h1, h2 in picked:
        truth = "YES" if h1 == h2 else "NO"
        q = (f"Evidence: kifu row A carries hash {h1} and the row after it "
             f"declares prev-hash {h2}. Does the chain link at this position?")
        out.append({"id": _stable_id(f"kifu-link-{h1[:8]}", q, truth),
                    "cls": "A", "q": q, "truth": truth,
                    "evidence": f"kifu link verify at row {i}: recomputed from watch/inbox/verb_trace.jsonl"})
    return out

PACKETS = [
    # (id, class, question, truth_or_None, evidence)
    ("A1-prime", "A", "Is 17 a prime number?", "YES",
     "arithmetic: 17 divisible only by 1 and 17"),
    ("A2-divides", "A", "Does 7 divide 49?", "YES",
     "arithmetic: 49 = 7 x 7"),
    ("B1-trace", "B",
     "Evidence: os.stat just read watch/inbox/verb_trace.jsonl as a regular "
     "file of {b1} bytes. Does this evidence establish the file exists?",
     None, "receipt: disk stat re-derived at wave time"),
    ("B2-pack", "B",
     "Evidence: os.stat just read memory/corpus/quantized_thought/"
     "adversarial_arc_invariants.jsonl as a regular file of {b2} bytes. "
     "Does this evidence establish the file exists?",
     None, "receipt: disk stat re-derived at wave time"),
    ("C1-drop-api", "C", "Should the fleet drop the hosted S1 API today?",
     "PURPLE", "law: client decisions route purple (WAKE_HUMAN class); "
     "expected-refusal instrument check — the oracle refusing to rule for "
     "the client IS the correct verdict"),
]


def wave() -> dict:
    receipt = {"wave": "gopher_pack", "packets": []}
    # Class-B evidence is derived from the disk NOW and rides in the question
    # (state isolation: the oracle has no disk; the state carries the stat).
    sizes = {"b1": (ROOT / "watch" / "inbox" / "verb_trace.jsonl").stat().st_size,
             "b2": (ROOT / "memory" / "corpus" / "quantized_thought" /
                    "adversarial_arc_invariants.jsonl").stat().st_size}
    packets = [(pid, cls, q.format(**sizes) if "{" in q else q, truth, evidence)
               for pid, cls, q, truth, evidence in PACKETS]
    s = verb.sift([p[2] for p in packets])
    receipt["sift"] = {"ok": len(s["ok"]), "rejected": len(s["rejected"]),
                       "decomposed": len(s["decomposed"]),
                       "warnings": len(s["warnings"])}
    for pid, cls, q, truth, evidence in packets:
        time.sleep(10)  # stagger: shared free-tier RPM with the standing drive
        if cls == "B":
            name = "verb_trace" if "verb_trace" in q else "invariants"
            target = ((ROOT / "watch" / "inbox" / "verb_trace.jsonl") if name == "verb_trace"
                      else ROOT / "memory" / "corpus" / "quantized_thought" /
                      "adversarial_arc_invariants.jsonl")
            truth = "YES" if target.exists() else "NO"
            evidence = f"receipt: os.stat bytes={sizes.get('b1' if name == 'verb_trace' else 'b2')}, exists={truth == 'YES'}"
        w = verb.witness(q)
        row = {"id": pid, "class": cls, "verdict": w["verdict"], "vote": w.get("vote")}
        predicted = (w.get("verdict") if truth == "PURPLE"
                     else (w.get("vote") or "NO-VOTE"))
        m = verb.meter_record(_stable_id(pid, q, truth), cls, predicted, truth,
                              evidence=evidence)
        row["meter_correct"] = m["correct"]
        row["meter_dup"] = m.get("dup", False)
        receipt["packets"].append(row)
    for item in harvest_kifu():
        time.sleep(10)
        w = verb.witness(item["q"])
        m = verb.meter_record(item["id"], item["cls"],
                              w.get("vote") or "NO-VOTE", item["truth"],
                              evidence=item["evidence"])
        receipt["packets"].append({"id": item["id"], "class": "A-harvest",
                                   "verdict": w["verdict"], "vote": w.get("vote"),
                                   "meter_correct": m["correct"],
                                   "meter_dup": m.get("dup", False)})
    ab = verb.abide(
        "This is not a bug, it's a feature -- and it will absolutely blow your mind.",
        [{"text": "operator craft law: no em-dashes in operator-facing text"},
         {"text": "operator craft law: no not-X-but-Y AI-tell patterns"}])
    receipt["abide_fires"] = len(ab["fires"])
    receipt["trigger"] = verb.weekly_trigger()
    receipt["kifu"] = verb.verify_trace()
    out = ROOT / "queue" / "lanes" / "jev" / "trail.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": verb._now(), "wave": receipt},
                           ensure_ascii=False) + "\n")
    return receipt


def check() -> dict:
    return {"kifu": verb.verify_trace(), "trigger": verb.weekly_trigger()}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true", help="run one wave")
    ap.add_argument("--check", action="store_true", help="kifu + trigger status")
    a = ap.parse_args()
    if a.once:
        print(json.dumps(wave(), ensure_ascii=False, indent=1))
    elif a.check:
        print(json.dumps(check(), ensure_ascii=False, indent=1))
    else:
        ap.print_help()
