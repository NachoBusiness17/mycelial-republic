"""DeepSeek off-peak authenticated hammer, 2026-09-28 pass h; --chat added pass i.

pass h fires the owed probe from BURN_free-resource-landscape_20260928_f.md:
single authenticated GET against the DeepSeek models endpoint, inside the
officially pinned off-peak window (weekdays 10:00Z to 01:00Z next day,
peak bands being 01:00-04:00 and 06:00-10:00 UTC Mon-Fri ex-Chinese-holidays).

pass i (BURN_free-resource-landscape_20260928_i.md falsifier, per pass h's
pre-registered build) adds --chat: one minimal POST /chat/completions
inference call inside the window, printing the usage object off a real
off-peak response. No arguments still runs the pass h GET probe.

Rules honored:
- stdlib only.
- Key material is never printed. Name-presence and length only.
- Output: HTTP code, model count, model names (GET) or HTTP code, usage
  object, response content (chat). Nothing that reveals the key.
- Exit 0 on HTTP 200, exit 2 on any other code.
"""

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
MODELS_URL = "https://api.deepseek.com/models"
CHAT_URL = "https://api.deepseek.com/chat/completions"


def load_key(env_path):
    """Parse DEEPSEEK_API_KEY=<value> from the .env file. Never print value."""
    with open(env_path, "r", encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if line.startswith("DEEPSEEK_API_KEY="):
                value = line.split("=", 1)[1].strip().strip('"').strip("'")
                if value:
                    print("DEEPSEEK_API_KEY present, length=%d" % len(value))
                    return value
    print("DEEPSEEK_API_KEY missing")
    return None


def fetch(req):
    """Return (http_code, body_bytes); (None, b"") on transport error."""
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        try:
            return exc.code, exc.read()
        except Exception:
            return exc.code, b""
    except urllib.error.URLError as exc:
        print("HTTP code=URLError reason=%s" % exc.reason)
        return None, b""


def run_models(key):
    req = urllib.request.Request(
        MODELS_URL,
        headers={
            "Authorization": "Bearer " + key,
            "Accept": "application/json",
        },
        method="GET",
    )
    code, body = fetch(req)
    if code is None:
        return 2

    print("HTTP code=%s" % code)
    if code != 200:
        return 2
    try:
        payload = json.loads(body.decode("utf-8"))
        models = [m.get("id", "?") for m in payload.get("data", [])]
    except Exception:
        print("model-count=parse-error")
        return 2
    print("model-count=%d" % len(models))
    for name in models:
        print("model=%s" % name)
    return 0


def run_chat(key):
    """One minimal off-peak inference call; prints usage only, never key."""
    req_body = json.dumps({
        "model": "deepseek-flash",
        "messages": [{"role": "user", "content": "reply with the single word ok"}],
        "max_tokens": 5,
    }).encode("utf-8")
    req = urllib.request.Request(
        CHAT_URL,
        data=req_body,
        headers={
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    code, body = fetch(req)
    if code is None:
        return 2
    print("HTTP code=%s" % code)
    if code != 200:
        return 2
    try:
        payload = json.loads(body.decode("utf-8"))
    except Exception:
        print("usage=parse-error")
        return 2
    usage = payload.get("usage", {})
    print("usage=" + json.dumps(usage, sort_keys=True))
    choices = payload.get("choices", [])
    if choices:
        print("finish_reason=%s" % choices[0].get("finish_reason"))
        content = (choices[0].get("message") or {}).get("content", "")
        print("content=%s" % content)
    if "prompt_tokens" not in usage or "completion_tokens" not in usage:
        print("billing-fields=absent")
    return 0


def main():
    key = load_key(ENV_PATH)
    if key is None:
        return 2
    if "--chat" in sys.argv[1:]:
        return run_chat(key)
    return run_models(key)


if __name__ == "__main__":
    sys.exit(main())
