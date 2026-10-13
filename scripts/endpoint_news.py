"""endpoint_news — standing API/endpoint news harvester for the fleet.

Operator directive 2026-09-18: harvest all our endpoints and APIs for news —
NVIDIA, OpenRouter, Hermes, Hacker News, and the equivalent. Model-list churn
across the provider lanes is the cheapest actionable intel: new free models,
retirements, and price changes change the tier ladder.

Security: https-only, fixed host allowlist, resolved-IP boundary check
(private/loopback/link-local refused), redirects disabled (SSRF-hardened).

Run:
  .venv/Scripts/python.exe scripts/endpoint_news.py        # one pass
Every pass: fetch, diff against the stored snapshot, append diff rows to
watch/inbox/endpoint_news/endpoint_news.jsonl, refresh snapshots.
First pass writes the baseline (rows marked kind=baseline).
"""
from __future__ import annotations

import ipaddress
import json
import socket
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "watch" / "inbox" / "endpoint_news"
NEWS = OUT / "endpoint_news.jsonl"
ENV_FILES = [ROOT / ".env"]

ALLOWED_HOSTS = {
    "hn.algolia.com",
    "openrouter.ai",
    "api.groq.com",
    "api.cerebras.ai",
    "api.mistral.ai",
    "integrate.api.nvidia.com",
}


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


_OPENER = urllib.request.build_opener(_NoRedirect)


def _get(url: str, key: str | None = None, timeout: int = 25):
    p = urllib.parse.urlparse(url)
    if p.scheme != "https" or p.hostname not in ALLOWED_HOSTS:
        raise ValueError("host not allowed")
    for _family, _stype, _proto, _canon, sa in socket.getaddrinfo(p.hostname, 443):
        ip = ipaddress.ip_address(sa[0])
        if not ip.is_global:
            raise ValueError("resolved to non-global address")
    headers = {"User-Agent": "mag-endpoint-news/1.0"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    req = urllib.request.Request(url, headers=headers)
    with _OPENER.open(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def _env() -> dict:
    out = {}
    for p in ENV_FILES:
        if p.is_file():
            for ln in p.read_text(encoding="utf-8", errors="replace").splitlines():
                ln = ln.strip()
                if ln and not ln.startswith("#") and "=" in ln:
                    k, v = ln.split("=", 1)
                    out.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    return out


def hn_front() -> list:
    d = _get("https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=30")
    return [{"id": h.get("objectID"), "title": h.get("title"), "url": h.get("url"),
             "points": h.get("points"), "comments": h.get("num_comments")}
            for h in d.get("hits", [])]


def openrouter_models() -> list:
    d = _get("https://openrouter.ai/api/v1/models")
    out = []
    for m in d.get("data", []):
        p = m.get("pricing") or {}
        out.append({"id": m.get("id"), "free": str(p.get("prompt", "1")) == "0",
                    "prompt_price": p.get("prompt")})
    return out


def lane_models(url: str, key: str) -> list:
    d = _get(url, key=key)
    return [{"id": m.get("id")} for m in d.get("data", [])]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    env = _env()
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    rows = []

    def emit(row: dict):
        row["ts"] = now
        rows.append(row)

    # Hacker News front page
    try:
        stories = hn_front()
        snap_p = OUT / "snapshot_hn.json"
        prev = json.loads(snap_p.read_text()) if snap_p.exists() else []
        prev_ids = {s.get("id") for s in prev}
        for s in stories:
            if s.get("id") not in prev_ids:
                emit({"source": "hn", "kind": "front_page_story", **s})
        snap_p.write_text(json.dumps(stories, ensure_ascii=False, indent=0))
    except Exception as e:
        emit({"source": "hn", "kind": "error", "detail": str(e)[:80]})

    # Model-list lanes (churn diffing)
    lanes = [
        ("openrouter", "https://openrouter.ai/api/v1/models", None),
        ("groq", "https://api.groq.com/openai/v1/models", env.get("GROQ_API_KEY", "")),
        ("cerebras", "https://api.cerebras.ai/v1/models", env.get("CEREBRAS_API_KEY", "")),
        ("mistral", "https://api.mistral.ai/v1/models", env.get("MISTRAL_API_KEY", "")),
        ("nvidia", "https://integrate.api.nvidia.com/v1/models",
         env.get("NVIDIA_API_KEY", "")),
    ]
    for name, url, key in lanes:
        try:
            if name == "openrouter":
                models = openrouter_models()
            else:
                models = lane_models(url, key) if key else []
            ids = {m["id"] for m in models}
            snap_p = OUT / f"snapshot_{name}.json"
            prev = json.loads(snap_p.read_text()) if snap_p.exists() else []
            prev_ids = {m["id"] for m in prev}
            added = sorted(ids - prev_ids)
            removed = sorted(prev_ids - ids)
            free_new = [a for a in added if any(m["id"] == a and m.get("free") for m in models)]
            if not prev:
                emit({"source": name, "kind": "baseline", "count": len(ids)})
            else:
                for a in added:
                    emit({"source": name, "kind": "model_added", "model": a,
                          "free": a in free_new})
                for r in removed:
                    emit({"source": name, "kind": "model_removed", "model": r})
                if not added and not removed:
                    emit({"source": name, "kind": "no_change", "count": len(ids)})
            snap_p.write_text(json.dumps(models, ensure_ascii=False, indent=0))
        except Exception as e:
            emit({"source": name, "kind": "error", "detail": str(e)[:80]})

    with NEWS.open("a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    model_events = [r for r in rows if str(r.get("kind", "")).startswith("model")]
    print(json.dumps({"pass_complete": True, "rows": len(rows),
                      "model_events": model_events[:20]}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
