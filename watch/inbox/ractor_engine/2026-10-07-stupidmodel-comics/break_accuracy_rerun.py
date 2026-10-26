"""break-accuracy reproduction of probe_panel_spec.py (2026-10-07).

Identical prompts/arms/options, ONE scorer fix (guard the bubbles loop that
crashed on null). Fresh independent arm: does qwen2.5:3b-instruct reproduce
7/8 spec_valid? Local ollama only, $0. Output: break_accuracy_rerun_results.json
"""
from __future__ import annotations

import json
import re
import time
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parent / "break_accuracy_rerun_results.json"
URL = "http://localhost:11434/api/generate"

SPEC = (
    'Output ONLY a JSON object of shape {"title": str, "panels": [{"caption": str, '
    '"characters": [str], "bubbles": [{"who": str, "text": str}]}]} with exactly 3 or 4 '
    "panels, at most 2 characters total, at most 1 speech bubble per panel, bubble text "
    "under 12 words. No markdown, no commentary."
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


def call(model: str, prompt: str, constrained: bool, timeout: int = 180) -> str:
    body = {
        "model": model,
        "prompt": f"Turn this session summary into a 3-4 panel xkcd-style comic spec. {SPEC}\n\nSession summary: {prompt}",
        "stream": False,
        "options": {"temperature": 0.3, "num_predict": 400},
    }
    if constrained:
        body["format"] = "json"
    req = urllib.request.Request(
        URL, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())["response"]


def score(raw: str) -> dict:
    t0 = raw
    think = ""
    m = re.search(r"<think>(.*?)</think>", raw, re.S)
    if m:
        think, t0 = m.group(1), raw[m.end():]
    txt = t0.strip()
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
    if parses and isinstance(obj, dict):
        title = obj.get("title")
        panels = obj.get("panels")
        ok = isinstance(title, str) and bool(title.strip())
        ok = ok and isinstance(panels, list) and 3 <= len(panels) <= 4
        if ok:
            for p in panels:
                ok = ok and isinstance(p, dict) and isinstance(p.get("caption"), str) and bool(p["caption"].strip())
                ok = ok and isinstance(p.get("characters"), list) and all(isinstance(c, str) for c in p["characters"])
                bub = p.get("bubbles")
                ok = ok and isinstance(bub, list) and len(bub) <= 2
                for b in (bub if isinstance(bub, list) else []):  # THE FIX
                    ok = ok and isinstance(b, dict) and isinstance(b.get("who"), str) and isinstance(b.get("text"), str) and bool(b["text"].strip())
        spec = bool(ok)
    return {
        "parses": parses,
        "spec_valid": spec,
        "had_think_block": bool(think),
        "raw_head": (raw[:90] + "...") if len(raw) > 90 else raw,
    }


def main() -> None:
    rows = []
    seats = ["gemma:2b", "qwen2.5:3b-instruct", "deepseek-r1:1.5b"]
    arms = [(m, True) for m in seats] + [("gemma:2b", False)]
    for model, constrained in arms:
        for i, p in enumerate(PROMPTS):
            t = time.time()
            try:
                raw = call(model, p, constrained)
                s = score(raw)
                err = ""
            except Exception as e:
                raw, s, err = "", {"parses": False, "spec_valid": False, "had_think_block": False, "raw_head": ""}, f"{type(e).__name__}: {e}"
            rows.append({
                "model": model, "arm": "format_json" if constrained else "unconstrained",
                "prompt_i": i, "secs": round(time.time() - t, 1), "error": err, **s,
            })
            print(model, ("json" if constrained else "free"), i, "parses", s["parses"], "spec", s["spec_valid"], flush=True)
    summary = {}
    for model, arm in {(r["model"], r["arm"]) for r in rows}:
        sub = [r for r in rows if r["model"] == model and r["arm"] == arm]
        summary[f"{model}:{arm}"] = {
            "n": len(sub),
            "parses": sum(r["parses"] for r in sub),
            "spec_valid": sum(r["spec_valid"] for r in sub),
            "errors": sum(1 for r in sub if r["error"]),
            "mean_secs": round(sum(r["secs"] for r in sub) / len(sub), 1),
        }
    OUT.write_text(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime()), "note": "break-accuracy reproduction, scorer bubbles-loop guarded", "summary": summary, "rows": rows}, indent=1), encoding="utf-8")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
