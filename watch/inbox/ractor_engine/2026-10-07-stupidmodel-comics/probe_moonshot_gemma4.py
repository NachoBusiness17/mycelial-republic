"""Moonshot probe (moonshot-1 lens, stupid-model comics ractor, 2026-10-07).

Fires the panel-spec trial at gemma4:latest - the LOCAL Google multimodal
seat (architecture gemma4, 7,996,157,674 params, vision+audio towers,
verified this sitting via /api/show) and the estate's existing "gemma4 short
worker" per AGENTS.md. Two arms x 8 prompts, $0, local ollama only:

  format_json  : the M1 schema door (body["format"]="json")
  line_grammar : the beat-family's proven door (PANEL n / POSE / WHO / LINE
                 plain lines, per operations.md F2) - never tested on any seat

Scoring MECHANICAL (no eyeballs): parses, spec_valid (3-4 panels, caption
str, characters list, bubbles <=2 {who,text}), caption <= 12 words, pose
in-vocabulary (7 dance poses + shrug/sit/point owed set).
"""
from __future__ import annotations

import json
import re
import time
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parent / "probe_moonshot_gemma4_results.json"
URL = "http://localhost:11434/api/generate"
MODEL = "gemma4:latest"
POSES = {"flail", "kick", "shimmy", "strut", "pointy", "spirit", "stomp", "shrug", "sit", "point"}

JSON_SPEC = (
    'Output ONLY a JSON object of shape {"title": str, "panels": [{"caption": str, '
    '"characters": [str], "pose": str, "bubbles": [{"who": str, "text": str}]}]} with '
    "exactly 3 or 4 panels, at most 2 characters total, at most 1 speech bubble per "
    "panel, bubble text under 12 words. No markdown, no commentary."
)

LINE_SPEC = (
    "Output ONLY plain lines, one per line, no markdown, no commentary. Grammar: "
    "TITLE <text> then for each of exactly 3 or 4 panels: PANEL <n> / POSE <one of "
    "flail kick shimmy strut pointy spirit stomp shrug sit point> / WHO <character "
    "names comma-separated, max 2> / LINE <speech under 12 words>."
)

PROMPTS = [
    "Session summary: the night shift ran 412 tests, 3 failed on a stale cache, the fix was one line, the janitor model wrote the changelog.",
    "Session summary: operator asked for a cheap comic of the week. The fleet said the free seats already passed the dice-honesty trial 2 for 2.",
    "Session summary: the drone got lost in fog, climbed to 4000m, saw the whole valley, and landed on the exact pad it left.",
    "Session summary: two agents argued about a number for an hour; the deterministic tool answered in 40 milliseconds and both went quiet.",
    "Session summary: the model claimed it could not draw. The renderer drew the model's words as stick figures and everyone laughed.",
    "Session summary: 402 quota wall at 09:05Z, eight automatic retries, eight denials; the ledger recorded every one and the balance never moved.",
    "Session summary: the mountain climb game needed a river; the hydrology tool carved one overnight and the map was never the same.",
    "Session summary: the operator said keep it stupid, keep it cheap, make it a comic strip; the fleet asked how stupid, exactly.",
]


def call(arm: str, prompt: str, timeout: int = 180) -> str:
    spec = JSON_SPEC if arm == "format_json" else LINE_SPEC
    body = {
        "model": MODEL,
        "prompt": f"Turn this session summary into a 3-4 panel xkcd-style comic spec. {spec}\n\nSession summary: {prompt}",
        "stream": False,
        "options": {"temperature": 0.3, "num_predict": 400},
    }
    if arm == "format_json":
        body["format"] = "json"
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())["response"]


def wc(s: str) -> int:
    return len(s.split())


def score_json(raw: str) -> dict:
    m = re.search(r"<think>(.*?)</think>", raw, re.S)
    txt = raw[m.end():].strip() if m else raw.strip()
    parses, spec, obj = False, False, None
    try:
        obj = json.loads(txt)
        parses = True
    except Exception:
        m2 = re.search(r"\{.*\}", txt, re.S)
        if m2:
            try:
                obj = json.loads(m2.group(0))
                parses = True
            except Exception:
                parses = False
    caption_ok = True
    pose_ok = True
    if parses and isinstance(obj, dict):
        title = obj.get("title")
        panels = obj.get("panels")
        ok = isinstance(title, str) and bool(title.strip())
        ok = ok and isinstance(panels, list) and 3 <= len(panels) <= 4
        if ok:
            for p in panels:
                if not isinstance(p, dict):
                    ok = False
                    break
                ok = ok and isinstance(p.get("caption"), str) and bool(p["caption"].strip())
                ok = ok and wc(p.get("caption", "")) <= 12
                ok = ok and isinstance(p.get("characters"), list) and len(p["characters"]) <= 2
                pose = p.get("pose", "")
                pose_ok = pose_ok and (str(pose).lower() in POSES)
                bub = p.get("bubbles")
                ok = ok and isinstance(bub, list) and len(bub) <= 2
                for b in bub or []:
                    ok = ok and isinstance(b, dict) and isinstance(b.get("who"), str) and isinstance(b.get("text"), str) and bool(str(b.get("text", "")).strip())
        spec = bool(ok)
    return {"parses": parses, "spec_valid": spec, "captions_ok": caption_ok, "poses_ok": pose_ok,
            "raw_head": (raw[:120] + "...") if len(raw) > 120 else raw}


def score_line(raw: str) -> dict:
    m = re.search(r"<think>(.*?)</think>", raw, re.S)
    txt = raw[m.end():].strip() if m else raw.strip()
    lines = [ln.strip() for ln in txt.splitlines() if ln.strip()]
    has_title = bool(lines) and lines[0].upper().startswith("TITLE")
    panels = [ln for ln in lines if ln.upper().startswith("PANEL")]
    pose_lines = [ln for ln in lines if ln.upper().startswith("POSE ")]
    poses_ok = bool(pose_lines) and all(ln.split(maxsplit=1)[1].strip().lower() in POSES if len(ln.split(maxsplit=1)) > 1 else False for ln in pose_lines)
    line_lines = [ln for ln in lines if ln.upper().startswith("LINE ")]
    lines_ok = all(wc(ln.split(maxsplit=1)[1]) <= 12 for ln in line_lines if len(ln.split(maxsplit=1)) > 1)
    parses = has_title and bool(panels)
    spec = parses and 3 <= len(panels) <= 4 and poses_ok and lines_ok
    return {"parses": parses, "spec_valid": spec, "captions_ok": lines_ok, "poses_ok": poses_ok,
            "raw_head": (raw[:120] + "...") if len(raw) > 120 else raw}


def main() -> None:
    rows = []
    for arm in ("format_json", "line_grammar"):
        for i, p in enumerate(PROMPTS):
            t = time.time()
            try:
                raw = call(arm, p)
                s = (score_json if arm == "format_json" else score_line)(raw)
                err = ""
            except Exception as e:
                raw, s, err = "", {"parses": False, "spec_valid": False, "captions_ok": False, "poses_ok": False, "raw_head": ""}, f"{type(e).__name__}: {e}"
            rows.append({"model": MODEL, "arm": arm, "prompt_i": i, "secs": round(time.time() - t, 1), "error": err, **s})
            print(MODEL, arm, i, "parses", s["parses"], "spec", s["spec_valid"], flush=True)
    summary = {}
    for arm in ("format_json", "line_grammar"):
        sub = [r for r in rows if r["arm"] == arm]
        summary[f"{MODEL}:{arm}"] = {
            "n": len(sub), "parses": sum(r["parses"] for r in sub), "spec_valid": sum(r["spec_valid"] for r in sub),
            "errors": sum(1 for r in sub if r["error"]), "poses_ok": sum(r["poses_ok"] for r in sub),
            "mean_secs": round(sum(r["secs"] for r in sub) / len(sub), 1),
        }
    OUT.write_text(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime()), "summary": summary, "rows": rows}, indent=1), encoding="utf-8")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
