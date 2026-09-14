"""perplexity_research — deep web research with citations, folded into the corpus.

Perplexity Sonar API: real-time web search + cited sources — the "deep research
elevation and steal" engine. Unlike Grok (closed reasoning), Sonar returns live,
cited findings we can steal mechanisms from (RenderMan / particle physics / Houdini /
ShaderToy / geometric calculus -> flocking + AI interaction).

Requires PERPLEXITY_API_KEY (operator-provided secret — never route through the model).

Schema: perplexity_research.v1
CLI: python -m mag.perplexity_research "<query>" [--model sonar|sonar-pro|sonar-deep-research]
     python -m mag.perplexity_research status
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from config import ROOT
except Exception:
    ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

SCHEMA = "perplexity_research.v1"
API_URL = "https://api.perplexity.ai/chat/completions"
LEAF_DIR = ROOT / "memory" / "runs" / "perplexity"

_KEY_ENVS = ("PERPLEXITY_API_KEY", "PPLX_API_KEY")
SYSTEM = (
    "You are a deep research engine. Given a query, return the load-bearing, cited "
    "mechanisms and insights. Prefer concrete, stealable mechanisms over vague overviews. "
    "Always cite sources inline. Be dense and structured."
)


def key() -> str:
    for e in _KEY_ENVS:
        v = os.environ.get(e)
        if v:
            return v
    return ""


def status() -> dict[str, Any]:
    return {"ok": bool(key()), "has_key": bool(key()),
            "envs": list(_KEY_ENVS), "api_url": API_URL,
            "note": "set PERPLEXITY_API_KEY to enable deep research"}


def research(query: str, *, model: str = "sonar", max_tokens: int = 2000,
             timeout: float = 120.0) -> dict[str, Any]:
    """Run one Perplexity Sonar deep-research call. Returns content + citations."""
    if not key():
        return {"ok": False, "error": "PERPLEXITY_API_KEY not set (operator must provide it)",
                "schema": SCHEMA}
    body = {
        "model": model,
        "messages": [{"role": "system", "content": SYSTEM},
                     {"role": "user", "content": (query or "").strip()}],
        "max_tokens": max_tokens,
    }
    req = urllib.request.Request(
        API_URL, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {key()}"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"ok": False, "schema": SCHEMA, "model": model,
                "error": f"HTTP {e.code}: {e.read()[:200]}"}
    except Exception as e:
        return {"ok": False, "schema": SCHEMA, "model": model, "error": str(e)[:200]}

    content = (raw.get("choices") or [{}])[0].get("message", {}).get("content", "")
    citations = raw.get("citations") or []
    usage = raw.get("usage") or {}
    LEAF_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    leaf = {"schema": SCHEMA, "ts": ts, "query": query[:400], "model": model,
            "content": content, "citations": citations[:20], "usage": usage}
    (LEAF_DIR / f"leaf-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}.json").write_text(
        json.dumps(leaf, ensure_ascii=False, default=str, indent=2), encoding="utf-8")
    # (best-effort fold into the corpus is handled by the caller / cadence loop)
    return {"ok": True, "schema": SCHEMA, "model": model, "content": content,
            "n_citations": len(citations), "citations": citations,
            "usage": usage, "saved_to": str(LEAF_DIR)}


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "status":
        print(json.dumps(status(), indent=2, default=str))
        return 0
    model = "sonar"
    if "--model" in argv:
        i = argv.index("--model")
        model = argv[i + 1]
        del argv[i:i + 2]
    q = " ".join(argv).strip()
    if not q:
        print(json.dumps(status(), indent=2, default=str))
        return 0
    r = research(q, model=model)
    print(json.dumps({"ok": r.get("ok"), "model": r.get("model"),
                      "n_citations": r.get("n_citations"), "error": r.get("error")}, indent=2))
    if r.get("ok"):
        print("===== CONTENT =====")
        print(r["content"])
        print("===== CITATIONS =====")
        for i, c in enumerate(r.get("citations", []), 1):
            print(f"[{i}] {c}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
