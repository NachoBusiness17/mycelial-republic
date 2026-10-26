#!/usr/bin/env python3
"""break-dogfood confound control: arm C prompt MINUS the response_format door.

The dogfood lens's flip (mistral 0/4 -> 3/3, cohere 0/3 -> 3/3) compares arm A
(LINE grammar prompt, no door) against arm C (JSON spec prompt + door): two
variables moved. This control holds the prompt byte-identical to arm C and
removes ONLY response_format, on the same seats. If spec_valid stays high, the
flip is the PROMPT, not the door, and F1's passthrough loses its measured
value. $0 free lanes, urllib only, no subprocess spawns.
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
import probe_dogfood_arm_c as m  # noqa: E402  (same SEATS/PROMPTS/_env/_OPENER/score)


def call_nodoor(seat: dict, prompt: str) -> tuple[str, str]:
    key = m._env(seat["key_env"])
    if not key:
        return "", "no key in .env: " + seat["key_env"]
    body = {
        "model": seat["model"], "stream": False, "max_tokens": 700,
        "temperature": 0.3,
        "messages": [{"role": "user", "content":
                      f"Turn this session summary into a 3 panel xkcd-style comic spec. {m.SPEC}\n\nSession summary: {prompt}"}],
        # THE DOOR REMOVED: no response_format key at all
    }
    req = urllib.request.Request(
        seat["url"], data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + key})
    try:
        with m._OPENER.open(req, timeout=90) as r:
            d = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return "", f"HTTP {e.code}"
    except Exception as e:
        return "", type(e).__name__
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


def main() -> int:
    rows = []
    for seat in m.SEATS:
        for i, p in enumerate(m.PROMPTS):
            t0 = time.time()
            raw, err = call_nodoor(seat, p)
            s = m.score(raw) if raw else {"parses": False, "spec_valid": False, "raw_head": ""}
            rows.append({"seat": seat["id"], "prompt_i": i,
                         "secs": round(time.time() - t0, 1), "error": err, **s})
            print(seat["id"], i, "parses", s["parses"], "spec", s["spec_valid"],
                  ("ERR " + err[:60]) if err else "", flush=True)
            time.sleep(2)
    summary = {}
    for seat in m.SEATS:
        sub = [r for r in rows if r["seat"] == seat["id"]]
        summary[seat["id"]] = {"n": len(sub),
                               "parses": sum(r["parses"] for r in sub),
                               "spec_valid": sum(r["spec_valid"] for r in sub),
                               "errors": sum(1 for r in sub if r["error"])}
    out = HERE / "break_dogfood_nodoor_results.json"
    out.write_text(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime()),
                               "arm": "control: arm C prompt, NO response_format door",
                               "summary": summary, "rows": rows}, indent=1), encoding="utf-8")
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
