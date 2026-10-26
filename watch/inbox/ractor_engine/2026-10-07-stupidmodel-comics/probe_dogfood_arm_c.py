#!/usr/bin/env python3
"""dogfood-lens comic probe, ARM C: the grammar door on REMOTE free seats.

The missing arm. Arm A (econ) fired line grammar through the queue door on
remote seats: 2/13 PASS because free_lane_fleet.fire() carries no grammar
door at all. Arm B + probe_panel_spec (accuracy) proved the format door on
LOCAL ollama: 5/5 and 7/8 spec_valid. Nobody measured REMOTE + door, which
is the exact falsifier for the one-sitting port (add a format/response_format
passthrough to fire()).

This probe calls the provider URLs directly (same literals as
tools/free_lane_fleet.py PROVIDERS) WITH response_format json_object, JSON
panel-spec prompt, and scores with the SAME spec_valid logic as
probe_panel_spec.py. $0 (all free lanes). No subprocess spawns (urllib
only), so the win32 CREATE_NO_WINDOW law is satisfied by construction.

Usage:
  python probe_dogfood_arm_c.py
"""
from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
OUT = Path(__file__).resolve().parent / "probe_dogfood_arm_c_results.json"

# Mirrors of tools/free_lane_fleet.py:114-137 PROVIDERS rows (byte-same URLs).
SEATS = [
    {"id": "mistral", "url": "https://api.mistral.ai/v1/chat/completions",
     "key_env": "MISTRAL_API_KEY", "model": "open-mistral-nemo"},
    {"id": "nvidia-1", "url": "https://integrate.api.nvidia.com/v1/chat/completions",
     "key_env": "NVIDIABuild", "model": "meta/llama-3.2-11b-vision-instruct"},
    {"id": "cohere-free", "url": "https://api.cohere.com/v2/chat",
     "key_env": "COHERE_API_KEY_FREE", "model": "command-r7b-12-2024"},
    # the operator's named stupid model, free variant (accuracy F3)
    {"id": "openrouter-gemma4", "url": "https://openrouter.ai/api/v1/chat/completions",
     "key_env": "OPENROUTER_API_KEY", "model": "google/gemma-4-26b-a4b-it:free"},
]
ALLOWED = frozenset(s["url"] for s in SEATS)

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
    # same CR-strip law as tools/free_lane_fleet.py:_env
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
        # THE DOOR under test
        "response_format": {"type": "json_object"},
    }
    req = urllib.request.Request(
        seat["url"], data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + key})
    t0 = time.time()
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
    # same logic as probe_panel_spec.py:score (accuracy lens), bug-fixed
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
    return {"parses": parses, "spec_valid": spec,
            "raw_head": (raw[:90] + "...") if len(raw) > 90 else raw}


def main() -> int:
    rows = []
    for seat in SEATS:
        assert seat["url"] in ALLOWED
        for i, p in enumerate(PROMPTS):
            t0 = time.time()
            raw, err = call(seat, p)
            s = score(raw) if raw else {"parses": False, "spec_valid": False, "raw_head": ""}
            row = {"seat": seat["id"], "model": seat["model"], "prompt_i": i,
                   "secs": round(time.time() - t0, 1), "error": err, **s}
            rows.append(row)
            print(seat["id"], i, "parses", s["parses"], "spec", s["spec_valid"],
                  ("ERR " + err[:60]) if err else "", flush=True)
            time.sleep(2)  # be polite to free lanes
    summary = {}
    for seat in SEATS:
        sub = [r for r in rows if r["seat"] == seat["id"]]
        summary[seat["id"]] = {
            "model": seat["model"], "n": len(sub),
            "parses": sum(r["parses"] for r in sub),
            "spec_valid": sum(r["spec_valid"] for r in sub),
            "errors": sum(1 for r in sub if r["error"]),
            "mean_secs": round(sum(r["secs"] for r in sub) / max(len(sub), 1), 1),
        }
    OUT.write_text(json.dumps(
        {"ts": time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime()),
         "arm": "C: remote free seats + response_format json_object door",
         "summary": summary, "rows": rows}, indent=1), encoding="utf-8")
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
