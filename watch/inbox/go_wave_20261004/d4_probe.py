#!/usr/bin/env python3
"""d4_thinking_probe - settle the DeepSeek v4 thinking-omission default by
measurement (go_wave 2026-10-04, lane A / d4).

Contradiction being settled (memory/runs/mickey17_v2/runs/run-0/lanes/):
  - a08-rails-laws r5 (configs/providers.yaml:367): "DeepSeek v4 defaults
    thinking ON"
  - a06-sacred-cow#3 / tools/ds_workhorse.py:86-87: "the v4 family disables
    reasoning unless a thinking object is present; omitting it IS the off
    state"

Method: 3 identical asks, varying ONLY the thinking parameter.
  arm1 omitted   : no thinking key in the body at all
  arm2 disabled  : "thinking": {"type": "disabled"}   (providers.yaml + route_chat wire form)
  arm3 enabled   : "thinking": {"type": "enabled"}    (route_chat depth="design" wire form)
Per arm banked: finish_reason, content, reasoning_content chars, full usage
block (reasoning tokens ride completion_tokens_details per the vendor docs).
"""
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
API = "https://api.deepseek.com/v1/chat/completions"
MODEL = "deepseek-v4-flash"
PROMPT = "Reply with the single word: pong"


def load_key() -> str:
    for line in (ROOT / ".env").read_text(encoding="utf-8",
                                          errors="replace").splitlines():
        if line.startswith("DEEPSEEK_API_KEY="):
            return line.partition("=")[2].strip()
    raise SystemExit("no DEEPSEEK_API_KEY in .env")


def arm_body(thinking):
    body = {"model": MODEL,
            "messages": [{"role": "user", "content": PROMPT}],
            "max_tokens": 512,
            "temperature": 0.3,
            "stream": False}
    if thinking is not None:
        body["thinking"] = thinking
    return body


def run_arm(name, thinking, key):
    body = json.dumps(arm_body(thinking)).encode()
    req = urllib.request.Request(API, data=body, method="POST", headers={
        "Authorization": "Bearer " + key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            resp = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        print(json.dumps({"arm": name, "http_error": exc.code,
                          "body": exc.read().decode("utf-8", "replace")[:400]}))
        return
    choice = (resp.get("choices") or [{}])[0]
    msg = choice.get("message", {})
    reasoning = msg.get("reasoning_content") or ""
    print(json.dumps({
        "arm": name,
        "finish_reason": choice.get("finish_reason"),
        "content": (msg.get("content") or "")[:200],
        "content_chars": len((msg.get("content") or "").strip()),
        "reasoning_content_chars": len(reasoning.strip()),
        "reasoning_head": reasoning.strip()[:120],
        "usage": resp.get("usage"),
    }, ensure_ascii=False))


def main() -> None:
    key = load_key()
    run_arm("omitted", None, key)
    run_arm("disabled", {"type": "disabled"}, key)
    run_arm("enabled", {"type": "enabled"}, key)


if __name__ == "__main__":
    main()
