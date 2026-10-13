"""Retry Cerebras: check both key names (fresh value?) and probe the two valid models."""
import json
import time
import urllib.request
from pathlib import Path

ROOT = Path("c:/Users/foste/Documents/projects/local_sovereign_agent")
keys = {}
for l in (ROOT / ".env").read_text(encoding="utf-8", errors="replace").splitlines():
    for w in ("CEREBRAS_API_KEY", "CEREBAS_API_KEY"):
        if l.startswith(w + "="):
            keys[w] = l.split("=", 1)[1].strip()
print("keys present:", {k: len(v) for k, v in keys.items()})

for name, key in keys.items():
    for model in ("gpt-oss-120b", "gemma-4-31b"):
        body = json.dumps({"model": model,
                           "messages": [{"role": "user", "content": "Reply with exactly: OK"}],
                           "max_tokens": 20}).encode()
        req = urllib.request.Request("https://api.cerebras.ai/v1/chat/completions", data=body,
                                     headers={"Authorization": f"Bearer {key}",
                                              "Content-Type": "application/json"}, method="POST")
        t0 = time.time()
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                b = json.loads(r.read().decode("utf-8"))
            txt = ((b.get("choices") or [{}])[0].get("message") or {}).get("content", "")[:20]
            print(f"{name} / {model}: OK {round((time.time()-t0)*1000)}ms | {txt!r}")
        except Exception as e:
            print(f"{name} / {model}: FAIL {str(e)[:80]}")
