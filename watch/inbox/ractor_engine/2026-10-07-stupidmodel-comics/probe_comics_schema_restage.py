#!/usr/bin/env python3
"""comics L1 restage: the 13 arm-A subjects re-run as SCHEMA trials through
the queue door. The arm-A run (econ_probe_results_arm_a.json) fired the same
13 subjects as unconstrained line grammar and passed 2/13; the arm-B direct
door (econ_probe_results_arm_b.json) went 10/10 json_ok. This probe lands the
middle cell: same subjects, same queue door as arm A, but each queue item now
carries the arm-B typed schema, and fire() passes it through
(tools/free_lane_fleet.py, schema door 2026-10-07).

Also --gemma-ni: the no-instruction rerun the fold owed (SYNTHESIS.md
residue). One direct ollama fire at gemma:2b, schema ON, prompt reduced to
the bare subject (no instruction preamble), same subject as arm-B gemma row
1 so the row-to-row delta is instruction-only. Settles whether the format
door rescues gemma:2b or only buys latency. Direct because the fleet's
ollama seat is qwen2.5:7b by PROVIDERS law; a queue item cannot address
gemma:2b. urllib only, no subprocess (CREATE_NO_WINDOW moot).

Usage:
  python probe_comics_schema_restage.py --stage     # drop 13 schema queue items
  python probe_comics_schema_restage.py --score     # grade ledger rows, bank
  python probe_comics_schema_restage.py --gemma-ni  # one gemma:2b no-instr fire
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
QUEUE = ROOT / "watch" / "inbox" / "free_lane_queue"
LEDGER = ROOT / "memory" / "runs" / "free_lane_fleet" / "ledger.jsonl"
OUT = Path(__file__).resolve().parent / "econ_probe_restage_schema.json"
OUT_NI = Path(__file__).resolve().parent / "gemma2b_noinstruction_result.json"
OLLAMA = "http://localhost:11434/api/generate"

POSES = ["flail", "kick", "shimmy", "strut", "pointy", "spirit", "stomp"]
SCHEMA = {
    "type": "object",
    "properties": {
        "panels": {
            "type": "array",
            "minItems": 3,
            "maxItems": 3,
            "items": {
                "type": "object",
                "properties": {
                    "who": {"type": "array",
                            "items": {"type": "string",
                                      "enum": ["stickman", "operator", "robot"]}},
                    "pose": {"type": "string",
                             "enum": POSES},
                    "cap": {"type": "string"},
                },
                "required": ["who", "pose", "cap"],
            },
        },
    },
    "required": ["panels"],
}

# The 13 arm-A subjects, byte-identical (econ_probe_results_arm_a.json rows).
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

# Arm-B instruction prompt, verbatim shape (econ_probe_results_arm_b.json).
PROMPT = (
    "You are the writer of a 3-panel stick-figure comic in the xkcd register "
    "(plain minimal figures, the joke lands in the captions). Subject: {subj}. "
    "Emit the comic spec as JSON matching the given schema: panels is exactly "
    "3 items; each panel has who (array of names, each one of stickman / "
    "operator / robot), pose (one of flail / kick / shimmy / strut / pointy / "
    "spirit / stomp), cap (the caption, max 10 words). Nothing else.")


def stage() -> int:
    QUEUE.mkdir(parents=True, exist_ok=True)
    n = 0
    for tid, subj in SUBJECTS:
        qpath = QUEUE / ("comic_econ2_" + tid + ".json")
        if qpath.exists():
            continue
        qpath.write_text(json.dumps(
            {"id": "comic:econ2:" + tid, "kind": "comic-probe",
             "prompt": PROMPT.format(subj=subj), "schema": SCHEMA},
            ensure_ascii=False), encoding="utf-8")
        n += 1
    print(f"RESTAGE STAGED: {n} schema queue files at {QUEUE}")
    return 0


def score_spec(text: str) -> dict:
    try:
        spec = json.loads(text)
    except Exception:
        return {"json_ok": False, "verdict": "FAIL", "fail_reason": ["json"]}
    panels = spec.get("panels") if isinstance(spec, dict) else None
    if not isinstance(panels, list) or len(panels) != 3:
        return {"json_ok": True, "n_panels": len(panels) if isinstance(panels, list) else -1,
                "verdict": "FAIL", "fail_reason": ["panels!=3"]}
    poses, whos, caps_ok = set(), set(), True
    for p in panels:
        poses.add(str(p.get("pose", "")).lower())
        for w in (p.get("who") or []):
            whos.add(str(w).lower())
        if len(str(p.get("cap", "")).split()) > 10:
            caps_ok = False
    in_vocab = poses <= set(POSES) and whos <= {"stickman", "operator", "robot"}
    ok = in_vocab and caps_ok
    return {"json_ok": True, "n_panels": 3, "poses": sorted(poses),
            "whos": sorted(whos), "in_vocab": in_vocab, "caps_ok": caps_ok,
            "verdict": "PASS" if ok else "FAIL",
            "fail_reason": [] if ok else [
                x for x, y in (("in_vocab", in_vocab), ("caps_ok", caps_ok)) if not y]}


def score() -> int:
    rows = {}
    if LEDGER.exists():
        for line in LEDGER.read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(line)
            except Exception:
                continue
            wid = str(r.get("work_id", ""))
            if wid.startswith("comic:econ2:") and r.get("ok"):
                rows.setdefault(wid, []).append(r)
    out = []
    for tid, subj in SUBJECTS:
        wid = "comic:econ2:" + tid
        fired = rows.get(wid) or []
        if not fired:
            out.append({"id": wid, "fired": False, "pending_next_cycle": True})
            continue
        row = fired[-1]
        s = score_spec(str(row.get("detail", "")))
        out.append({"id": wid, "fired": True, "provider": row.get("provider"),
                    "model": row.get("model"), "chars": row.get("chars"),
                    "schema_flag": row.get("schema"), "subject": subj, **s,
                    "raw": str(row.get("detail", ""))[:600]})
    fired = [r for r in out if r.get("fired")]
    passed = [r for r in fired if r.get("verdict") == "PASS"]
    summary = {"arm": "restage: queue door + typed schema pass-through "
                      "(fire() schema door, 2026-10-07)",
               "baseline_arm_a_line_grammar_pass": 2,
               "baseline_arm_b_json_ok": "10/10 (gemma:2b 5/5, qwen2.5:7b 5/5)",
               "n_staged": len(SUBJECTS), "n_fired": len(fired),
               "n_pass": len(passed),
               "n_json_ok": sum(1 for r in fired if r.get("json_ok")),
               "by_model": {}}
    for r in fired:
        m = str(r.get("model"))
        summary["by_model"].setdefault(m, {"fired": 0, "json_ok": 0, "pass": 0})
        summary["by_model"][m]["fired"] += 1
        if r.get("json_ok"):
            summary["by_model"][m]["json_ok"] += 1
        if r.get("verdict") == "PASS":
            summary["by_model"][m]["pass"] += 1
    OUT.write_text(json.dumps({"summary": summary, "rows": out},
                              indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=1))
    print("BANKED " + str(OUT))
    return 0


def gemma_ni() -> int:
    # The fold's owed rerun: schema ON, instruction preamble OFF. Same subject
    # as arm-B gemma row 1, so the only delta vs that banked row is the prompt.
    subj = SUBJECTS[0][1]
    body = json.dumps({
        "model": "gemma:2b", "prompt": subj,
        "stream": False, "temperature": 0.3,
        "format": SCHEMA,
        "options": {"num_predict": 300},
    }).encode()
    req = urllib.request.Request(OLLAMA, data=body,
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            d = json.loads(r.read().decode("utf-8"))
    except Exception as e:
        print("GEMMA-NI FIRE FAIL: " + type(e).__name__ + ": " + str(e)[:120])
        return 1
    ms = int((time.time() - t0) * 1000)
    text = str(d.get("response", ""))
    s = score_spec(text)
    row = {"trial": "gemma:2b no-instruction, schema ON (format=json schema), "
                    "temp 0.3, prompt = bare subject, no preamble",
           "subject": subj, "fired": True, "ms": ms, "chars": len(text),
           **s, "raw": text[:800],
           "arm_b_gemma_row1_baseline": {"ms": 17518, "verdict": "FAIL",
                                         "json_ok": True, "fail": ["caps_ok"]}}
    OUT_NI.write_text(json.dumps(row, indent=1, ensure_ascii=False),
                      encoding="utf-8")
    print(json.dumps({k: v for k, v in row.items() if k != "raw"}, indent=1))
    print("BANKED " + str(OUT_NI))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", action="store_true")
    ap.add_argument("--score", action="store_true")
    ap.add_argument("--gemma-ni", action="store_true")
    a = ap.parse_args()
    if a.stage:
        return stage()
    if a.score:
        return score()
    if a.gemma_ni:
        return gemma_ni()
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
