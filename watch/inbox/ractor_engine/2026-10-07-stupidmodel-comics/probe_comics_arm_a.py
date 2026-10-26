#!/usr/bin/env python3
"""economics-lens comic probe, ARM A: the queue door (what the gauntlet can
ship TODAY). Stages line-grammar panel-spec trials into the free-lane queue
(same door the gauntlet feeder uses, schema {id, kind, prompt}), then scores
the fleet ledger rows mechanically after a cycle fires them.

No subprocess spawns (urllib/file IO only), so the win32 CREATE_NO_WINDOW
law is satisfied by construction.

Usage:
  python probe_comics_arm_a.py --stage    # drop 13 queue files
  python probe_comics_arm_a.py --score    # score ledger rows, bank results
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
QUEUE = ROOT / "watch" / "inbox" / "free_lane_queue"
LEDGER = ROOT / "memory" / "runs" / "free_lane_fleet" / "ledger.jsonl"
OUT = Path(__file__).resolve().parent / "econ_probe_results_arm_a.json"

POSES = {"flail", "kick", "shimmy", "strut", "pointy", "spirit", "stomp"}
WHOS = {"stickman", "operator", "robot"}

# Real estate bytes read this sitting (sources named in the receipt .md).
SUBJECTS = [
    ("a01", "a free-fleet grader scored a model 0 out of 4 because the grading regex demanded an ms suffix the answer format never mandated"),
    ("a02", "eleven falsifier trials ran overnight on free API seats for zero dollars and zero paid models"),
    ("a03", "a tiny 2B model scored 0 of 30 on valid JSON until a format schema was switched on, then scored 30 of 30"),
    ("a04", "the operator ordered xkcd-style stick-figure panel comics for the chat relay, drawn by a really stupid cheap model"),
    ("a05", "an auto-regenerated live report stole the newest-file crown from the night crew's log because it refreshed every five minutes"),
    ("a06", "the free fleet drains the work queue two slots per provider every thirty minutes, all day, all free"),
    ("a07", "the stick-figure dance crew held the beat grid perfectly for eight counts and fell apart at twelve"),
    ("a08", "a cheap actor contested the sealed dice roll it was never allowed to see"),
    ("a09", "asked to verify a dice claim with no hash function available, the small model correctly suspended judgment to the deterministic tool"),
    ("a10", "a five-year-old graphics card runs the tiny model at eighty tokens per second, one hundred percent on GPU"),
    ("a11", "a hand-copied test count rode the readme for twelve days while the real tree grew forty files"),
    ("a12", "the mountain climb continues: the same voxel hill the game seats dig is the hill the comics would draw"),
    ("a13", "three machines on the mesh, each one keeping the same comic strip from a different angle"),
]

PROMPT = (
    "3-panel stick-figure comic, xkcd register: plain minimal figures, the "
    "joke lands in the captions. Subject: {subj}. Output EXACTLY 12 lines in "
    "this grammar, nothing else:\n"
    "PANEL 1\n"
    "WHO: <one or two of stickman / operator / robot, joined by ' + '>\n"
    "POSE: <exactly one of: flail kick shimmy strut pointy spirit stomp>\n"
    "CAP: <caption, max 10 words>\n"
    "PANEL 2\n"
    "WHO: <same rule>\n"
    "POSE: <same rule>\n"
    "CAP: <caption, max 10 words>\n"
    "PANEL 3\n"
    "WHO: <same rule>\n"
    "POSE: <same rule>\n"
    "CAP: <the punchline, max 10 words>\n"
    "No markdown. No JSON. No other text.")


def stage() -> int:
    QUEUE.mkdir(parents=True, exist_ok=True)
    n = 0
    for tid, subj in SUBJECTS:
        qpath = QUEUE / ("comic_econ_" + tid + ".json")
        if qpath.exists():
            continue
        qpath.write_text(json.dumps(
            {"id": "comic:econ:" + tid, "kind": "comic-probe",
             "prompt": PROMPT.format(subj=subj)}, ensure_ascii=False),
            encoding="utf-8")
        n += 1
    print(f"ARM-A STAGED: {n} queue files at {QUEUE}")
    return 0


PANEL_RE = re.compile(
    r"PANEL\s+(\d)\s*\n\s*WHO:\s*(.+?)\s*\n\s*POSE:\s*(.+?)\s*\n\s*CAP:\s*(.+?)\s*(?=\n|$)",
    re.I)


def score_text(text: str) -> dict:
    panels = PANEL_RE.findall(text)
    parseable = len(panels) >= 3
    poses = {p[2].strip().lower() for p in panels}
    whos = set()
    for p in panels:
        for tok in re.split(r"\+|,| and ", p[1]):
            tok = tok.strip().lower()
            if tok:
                whos.add(tok)
    in_vocab = (poses <= POSES and whos <= WHOS) if panels else False
    caps_ok = all(len(p[3].split()) <= 10 for p in panels) if panels else False
    minimal = ("```" not in text and "here is" not in text.lower()
               and len(text) <= 700)
    ok = parseable and in_vocab and caps_ok and minimal
    return {"n_panels": len(panels), "parseable": parseable,
            "poses": sorted(poses), "whos": sorted(whos),
            "in_vocab": in_vocab, "caps_ok": caps_ok, "minimal": minimal,
            "verdict": "PASS" if ok else "FAIL",
            "fail_reason": [] if ok else [
                x for x, y in (("parseable", parseable), ("in_vocab", in_vocab),
                               ("caps_ok", caps_ok), ("minimal", minimal)) if not y]}


def score() -> int:
    rows = {}
    if LEDGER.exists():
        for line in LEDGER.read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(line)
            except Exception:
                continue
            wid = str(r.get("work_id", ""))
            if wid.startswith("comic:econ:") and r.get("ok"):
                rows.setdefault(wid, []).append(r)
    out = []
    for tid, subj in SUBJECTS:
        wid = "comic:econ:" + tid
        fired = rows.get(wid) or []
        if not fired:
            out.append({"id": wid, "fired": False})
            continue
        row = fired[-1]
        s = score_text(str(row.get("detail", "")))
        out.append({"id": wid, "fired": True, "provider": row.get("provider"),
                    "model": row.get("model"), "chars": row.get("chars"),
                    "subject": subj, **s,
                    "raw": str(row.get("detail", ""))[:600]})
    fired = [r for r in out if r.get("fired")]
    passed = [r for r in fired if r.get("verdict") == "PASS"]
    summary = {"arm": "A: queue door, unconstrained line grammar",
               "n_staged": len(SUBJECTS), "n_fired": len(fired),
               "n_pass": len(passed),
               "by_model": {}}
    for r in fired:
        m = str(r.get("model"))
        summary["by_model"].setdefault(m, {"fired": 0, "pass": 0})
        summary["by_model"][m]["fired"] += 1
        if r.get("verdict") == "PASS":
            summary["by_model"][m]["pass"] += 1
    OUT.write_text(json.dumps({"summary": summary, "rows": out},
                              indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=1))
    print("BANKED " + str(OUT))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", action="store_true")
    ap.add_argument("--score", action="store_true")
    a = ap.parse_args()
    if a.stage:
        return stage()
    if a.score:
        return score()
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
