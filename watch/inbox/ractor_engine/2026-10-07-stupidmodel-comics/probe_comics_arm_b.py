#!/usr/bin/env python3
"""economics-lens comic probe, ARM B: the M1 format-schema door.
Direct Ollama calls with body["format"] = JSON schema (the exact door M1
proved: tools/m1_grammar_bench.py:36-38, watch/inbox/48h_synth/m1_bench.json
0/30 unconstrained vs 30/30 schema on gemma:2b), comic-shaped schema, on the
two local seats gemma:2b and qwen2.5:7b. urllib only (no subprocess spawns;
CREATE_NO_WINDOW moot by construction), one shot per trial, retry never.
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parent / "econ_probe_results_arm_b.json"
URL = "http://localhost:11434/api/generate"

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

SUBJECTS = [
    "a free-fleet grader scored a model 0 out of 4 because the grading regex demanded an ms suffix the answer format never mandated",
    "a tiny 2B model scored 0 of 30 on valid JSON until a format schema was switched on, then scored 30 of 30",
    "the operator ordered xkcd-style stick-figure panel comics for the chat relay, drawn by a really stupid cheap model",
    "the stick-figure dance crew held the beat grid perfectly for eight counts and fell apart at twelve",
    "asked to verify a dice claim with no hash function available, the small model correctly suspended judgment to the deterministic tool",
]

MODELS = ["gemma:2b", "qwen2.5:7b"]

PROMPT = (
    "You are the writer of a 3-panel stick-figure comic in the xkcd register "
    "(plain minimal figures, the joke lands in the captions). Subject: {subj}. "
    "Emit the comic spec as JSON matching the given schema: panels is exactly "
    "3 items; each panel has who (array of names, each one of stickman / "
    "operator / robot), pose (one of flail / kick / shimmy / strut / pointy / "
    "spirit / stomp), cap (the caption, max 10 words). Nothing else.")


def ask(model: str, subj: str) -> tuple[bool, str, int]:
    body = json.dumps({
        "model": model, "prompt": PROMPT.format(subj=subj),
        "stream": False, "temperature": 0.3,
        "format": SCHEMA,
        "options": {"num_predict": 300},
    }).encode()
    req = urllib.request.Request(URL, data=body,
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            d = json.loads(r.read().decode("utf-8"))
    except Exception as e:
        return False, type(e).__name__ + ": " + str(e)[:120], 0
    dt = int((time.time() - t0) * 1000)
    return True, str(d.get("response", "")), dt


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
    pose_set = set(POSES)
    in_vocab = poses <= pose_set and whos <= {"stickman", "operator", "robot"}
    ok = in_vocab and caps_ok
    return {"json_ok": True, "n_panels": 3, "poses": sorted(poses),
            "whos": sorted(whos), "in_vocab": in_vocab, "caps_ok": caps_ok,
            "verdict": "PASS" if ok else "FAIL",
            "fail_reason": [] if ok else [
                x for x, y in (("in_vocab", in_vocab), ("caps_ok", caps_ok)) if not y]}


def main() -> int:
    rows = []
    for model in MODELS:
        for i, subj in enumerate(SUBJECTS):
            ok, text, dtms = ask(model, subj)
            if not ok:
                rows.append({"model": model, "i": i + 1, "fired": False,
                             "error": text})
                print(f"{model} t{i+1}: FIRE FAIL {text}")
                continue
            s = score_spec(text)
            rows.append({"model": model, "i": i + 1, "fired": True,
                         "ms": dtms, "chars": len(text), **s,
                         "raw": text[:600]})
            print(f"{model} t{i+1}: {s['verdict']} ({dtms}ms, {len(text)} ch)"
                  + (" " + ",".join(s.get("fail_reason", [])) if s["verdict"] == "FAIL" else ""))
    summary = {"arm": "B: format-schema door (direct ollama, body.format=schema)",
               "by_model": {}}
    for model in MODELS:
        mrows = [r for r in rows if r.get("model") == model and r.get("fired")]
        summary["by_model"][model] = {
            "fired": len(mrows),
            "pass": sum(1 for r in mrows if r.get("verdict") == "PASS"),
            "json_ok": sum(1 for r in mrows if r.get("json_ok")),
            "median_ms": sorted(r["ms"] for r in mrows)[len(mrows)//2] if mrows else None}
    OUT.write_text(json.dumps({"summary": summary, "rows": rows},
                              indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=1))
    print("BANKED " + str(OUT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
