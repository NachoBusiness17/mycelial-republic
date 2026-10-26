#!/usr/bin/env python3
"""dogfood-lens CONTROL arm (post-critique): same JSON panel-spec prompt as
arm C, response_format door REMOVED. One variable isolated: the door.

The hostile second pass ran break_dogfood_nodoor.py and got identical
results to arm C, falsifying the flip ATTRIBUTION (arm A vs arm C differed
in BOTH prompt grammar and door). This control re-runs the same test
first-hand so the correction rests on bytes I fired, not on the critic's
report. Also banks whether no-door outputs carry markdown fences or other
contamination (the door's residual value if the flip is prompt-carried).

$0, 9 calls, no subprocess spawns. Usage: python probe_dogfood_control.py
"""
from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
OUT = Path(__file__).resolve().parent / "probe_dogfood_control_results.json"

SEATS = [
    {"id": "mistral", "url": "https://api.mistral.ai/v1/chat/completions",
     "key_env": "MISTRAL_API_KEY", "model": "open-mistral-nemo"},
    {"id": "nvidia-1", "url": "https://integrate.api.nvidia.com/v1/chat/completions",
     "key_env": "NVIDIABuild", "model": "meta/llama-3.2-11b-vision-instruct"},
    {"id": "cohere-free", "url": "https://api.cohere.com/v2/chat",
     "key_env": "COHERE_API_KEY_FREE", "model": "command-r7b-12-2024"},
]

SPEC = (
    'Output ONLY a JSON object of shape {"title": str, "panels": [{"caption": str, '
    '"characters": [str], "bubbles": [{"who": str, "text": str}]}]} with exactly 3 '
    "panels, at most 2 characters total, at most 1 speech bubble per panel, bubble "
    "text under 12 words. Characters must be one of: stickman, operator, robot. "
    "No markdown, no commentary."
)
PROMPTS = [
    "Session summary: the night shift ran 412 tests, 3 failed on a stale cache, the fix was one line, the janitor model wrote the changelog.",
    "Session summary: the drone got lost in fog, climbed to 4000m, saw the whole valley, and landed on the exact pad it left.",
    "Session summary: the operator said keep it stupid, keep it cheap, make it a comic strip; the fleet asked how stupid, exactly.",
]


def _env(name: str) -> str:
    for line in (ROOT / ".env").read_text(encoding="utf-8", errors="replace").splitlines():
        if line.strip().startswith(name + "="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_OPENER = urllib.request.build_opener(_NoRedirect)


def call(seat: dict, prompt: str) -> tuple[str, str]:
    key = _env(seat["key_env"])
    if not key:
        return "", "no key in .env: " + seat["key_env"]
    body = {
        "model": seat["model"], "stream": False, "max_tokens": 700,
        "temperature": 0.3,
        "messages": [{"role": "user", "content":
                      f"Turn this session summary into a 3 panel xkcd-style comic spec. {SPEC}\n\nSession summary: {prompt}"}],
        # DOOR REMOVED: no response_format key at all
    }
    req = urllib.request.Request(
        seat["url"], data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + key})
    try:
        with _OPENER.open(req, timeout=90) as r:
            d = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = ""
        try:
            detail = e.read().decode("utf-8", errors="replace")[:200]
        except Exception:
            pass
        return "", f"HTTP {e.code} {detail}"
    except Exception as e:
        return "", type(e).__name__ + ": " + str(e)[:120]
    if seat["id"] == "cohere-free":
        msg = d.get("message") or {}
        content = msg.get("content")
        if isinstance(content, list):
            content = " ".join(str(b.get("text", "")) for b in content if isinstance(b, dict))
        text = str(content or "")
    else:
        msg = (d.get("choices") or [{}])[0].get("message") or {}
        content = msg.get("content")
        if isinstance(content, list):
            content = " ".join(str(b.get("text", "")) for b in content if isinstance(b, dict))
        text = str(content or msg.get("reasoning_content") or "")
    return text.strip(), ""


def score(raw: str) -> dict:
    txt = re.sub(r"<think>.*?</think>", "", raw, flags=re.S).strip()
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
                ok = ok and isinstance(p, dict) and isinstance(p.get("caption"), str) and bool(str(p["caption"]).strip())
                ch = p.get("characters")
                ok = ok and isinstance(ch, list) and all(isinstance(c, str) for c in ch)
                bub = p.get("bubbles")
                ok = ok and isinstance(bub, list) and len(bub) <= 2
                if isinstance(bub, list):
                    for b in bub:
                        ok = ok and isinstance(b, dict) and isinstance(b.get("who"), str) \
                             and isinstance(b.get("text"), str) and bool(str(b["text"]).strip())
        spec = bool(ok)
    fenced = bool(re.search(r"```", raw))
    prefix = txt[:1] == "{"
    return {"parses": parses, "spec_valid": spec, "fenced": fenced,
            "json_first_char": prefix,
            "raw_head": (raw[:90] + "...") if len(raw) > 90 else raw}


def main() -> int:
    rows = []
    for seat in SEATS:
        for i, p in enumerate(PROMPTS):
            t0 = time.time()
            raw, err = call(seat, p)
            s = score(raw) if raw else {"parses": False, "spec_valid": False, "fenced": False,
                                        "json_first_char": False, "raw_head": ""}
            rows.append({"seat": seat["id"], "model": seat["model"], "prompt_i": i,
                         "secs": round(time.time() - t0, 1), "error": err, **s})
            print(seat["id"], i, "parses", s["parses"], "spec", s["spec_valid"],
                  "fenced", s["fenced"], ("ERR " + err[:60]) if err else "", flush=True)
            time.sleep(2)
    summary = {}
    for seat in SEATS:
        sub = [r for r in rows if r["seat"] == seat["id"]]
        summary[seat["id"]] = {
            "model": seat["model"], "n": len(sub),
            "parses": sum(r["parses"] for r in sub),
            "spec_valid": sum(r["spec_valid"] for r in sub),
            "fenced": sum(r["fenced"] for r in sub),
            "json_first_char": sum(r["json_first_char"] for r in sub),
            "errors": sum(1 for r in sub if r["error"]),
            "mean_secs": round(sum(r["secs"] for r in sub) / max(len(sub), 1), 1),
        }
    OUT.write_text(json.dumps(
        {"ts": time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime()),
         "arm": "CONTROL: remote free seats, JSON prompt, NO door (isolates the door variable)",
         "summary": summary, "rows": rows}, indent=1), encoding="utf-8")
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
