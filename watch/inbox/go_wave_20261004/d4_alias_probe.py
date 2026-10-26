#!/usr/bin/env python3
"""d4_alias_probe - the SAME 3-arm thinking probe on MODEL=deepseek-chat, the
tools/ds_workhorse.py:64 alias ("v4.1-flash mapping per provider docs").

B7 filed-not-fixed sweep item 4 (2026-10-05). The 2026-10-04 d4 probe settled
the omission default for the canonical name deepseek-v4-flash (thinks by
default; receipt watch/inbox/go_wave_20261004/d4_thinking_probe.md). The alias
every ds_workhorse batch actually rides was never measured: if the alias maps
to a different underlying default, the workhorse's explicit
thinking:{type:disabled} is load-bearing in a way the canonical probe alone
does not prove. Method identical: 3 asks, ONLY the thinking key varies.
"""
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
API = "https://api.deepseek.com/v1/chat/completions"
MODEL = "deepseek-chat"
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
