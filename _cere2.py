"""Test the two real Cerebras public models."""
import json
import time
import urllib.request
from pathlib import Path

ROOT = Path("c:/Users/foste/Documents/projects/local_sovereign_agent")
key = ""
for l in (ROOT / ".env").read_text(encoding="utf-8", errors="replace").splitlines():
    if l.startswith("CEREBAS_API_KEY="):
        key = l.split("=", 1)[1].strip()

for model in ("gpt-oss-120b", "gemma-4-31b"):
    body = json.dumps({"model": model,
                       "messages": [{"role": "user", "content": "Reply with exactly: OK"}],
                       "max_tokens": 20}).encode()
    req = urllib.request.Request("https://api.cerebras.ai/v1/chat/completions", data=body,
                                 headers={"Authorization": f"Bearer {key}",
                                          "Content-Type": "application/json"}, method="POST")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            b = json.loads(r.read().decode("utf-8"))
        txt = ((b.get("choices") or [{}])[0].get("message") or {}).get("content", "")[:20]
        u = b.get("usage") or {}
        print(f"{model}: OK {round((time.time()-t0)*1000)}ms tok={u.get('total_tokens')} | {txt!r}")
    except Exception as e:
        print(f"{model}: FAIL {str(e)[:100]}")
