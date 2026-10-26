"""sw-03 lane debug: raw JSON from llm7 (keyless) + one OpenRouter retry.

Prints status, top-level keys, choice structure, usage so failures are
attributable. urllib only, no subprocess.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
try:
    from models.env_load import load_dotenv
    load_dotenv()
except Exception as e:
    print(f"dotenv load skipped: {e}")

OR2 = os.environ.get("OPENROUTER_API_KEY_2") or ""
ASK = ("In 300 words: what does published evidence say about token cost per "
       "completed AI agent task (e.g. Anthropic 4x agentic token multiplier) "
       "and free-tier vs paid API models for production work? Name sources; "
       "say OWED if you cannot verify.")


def call(base: str, key: str, model: str) -> None:
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": ASK}],
        "max_tokens": 900,
    }).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    req = urllib.request.Request(base, data=body, headers=headers)
    print(f"\n=== {model} @ {base.split('/')[2]}")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            d = json.loads(r.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read()[:300]}")
        return
    print(f"top keys: {sorted(d.keys())}")
    ch = (d.get("choices") or [{}])[0]
    msg = ch.get("message") or {}
    print(f"finish: {ch.get('finish_reason')} | msg keys: {sorted(msg.keys())}")
    txt = (msg.get("content") or msg.get("reasoning_content") or "").strip()
    print(f"text chars: {len(txt)} | usage: {json.dumps(d.get('usage'))}")
    print(f"head: {txt[:500]}")


call("https://api.llm7.io/v1/chat/completions", "", "gpt-4o-mini")
if OR2:
    call("https://openrouter.ai/api/v1/chat/completions", OR2,
         "inclusionai/ling-3.0-flash-sante:free")
else:
    print("\nOPENROUTER_API_KEY_2 not in env; OpenRouter retry skipped")
