"""D22 provider probe — pass 2 (wave gen-2).

Free-tier only, $0. No repo code edited: imports the registry + env loader from
mag.research_fanout. Appends every result (success OR failure) to a JSONL receipt
as it lands, so a gen-3 can pick up mid-run.

Phases:
  1. re-verify  8 lanes gen-1 logged ALIVE at 17:46 UTC — one minimal call each ("RIGHT NOW" check)
  2. retry      3 lanes gen-1 logged DEAD (429) — one classified call each, capture 429 body + headers
  3. models     1 un-metered GET /models per provider — quota-headroom signals

Total metered calls: 11. Total GETs: 5 (un-metered). Well under the 20-call cap.
Run: .venv\\Scripts\\python.exe watch\\inbox\\wave_20260916\\D22_probe_pass2.py
"""
import json
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
sys.path.insert(0, ROOT)
from mag.research_fanout import LANES, _env  # registry + env loader only, read-only

OUT = ROOT + r"\watch\inbox\wave_20260916\receipts\D22_probe_pass2.jsonl"

ALIVE_8 = ["groq-qwen", "groq-oss", "groq-oss20", "cerebras-oss", "cerebras-qwen",
           "mistral-min8", "or-nemotron", "or-ling3"]
DEAD_3 = ["mistral-small", "zai-air", "or-glm52"]  # zai-47 NEVER called (paid wall, order)
PROVIDERS = [  # (name, base, key env) for un-metered GET /models
    ("groq", "https://api.groq.com/openai/v1", "GROQ_API_KEY"),
    ("cerebras", "https://api.cerebras.ai/v1", "CEREBAS_API_KEY"),
    ("mistral", "https://api.mistral.ai/v1", "Mistral_API_KEY"),
    ("zai", "https://api.z.ai/api/paas/v4", "ZAI_API_KEY"),
    ("openrouter", "https://openrouter.ai/api/v1", "OPENROUTER_API_KEY"),
]
PROMPT = "Reply with exactly: READY"  # same probe string as gen-1 pass 1 / probe_lanes()
LOCK = __import__("threading").Lock()


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def emit(rec: dict) -> None:
    with LOCK:
        with open(OUT, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=True) + "\n")
        print(json.dumps({k: rec.get(k) for k in
                          ("phase", "lane", "provider", "ok", "error", "latency_ms")},
                         ensure_ascii=True), flush=True)


def rl_headers(headers) -> dict:
    """Keep only rate/quota-relevant headers (values are public limits, not secrets)."""
    out = {}
    try:
        for k, v in headers.items():
            lk = k.lower()
            if any(t in lk for t in ("rate", "limit", "remaining", "reset", "retry", "quota")):
                out[k] = v
    except Exception:
        pass
    return out


def chat_probe(lane: dict, key: str, phase: str, timeout: int = 60) -> dict:
    t0 = time.time()
    rec = {"phase": phase, "lane": lane["id"], "model": lane["model"], "ts": now()}
    body = {"model": lane["model"], "temperature": 0.2, "max_tokens": 2600,
            "messages": [{"role": "system", "content": "You are a probe. Reply with the exact word requested."},
                         {"role": "user", "content": PROMPT}]}
    req = urllib.request.Request(
        lane["base"].rstrip("/") + "/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                 "User-Agent": "mag-d22-probe/2.0",
                 "HTTP-Referer": "https://local-sovereign-agent.invalid",
                 "X-Title": "Mag D22 Provider Probe"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.loads(r.read().decode("utf-8", "replace"))
            rec["resp_headers"] = rl_headers(r.headers)
        msg = d["choices"][0]["message"]
        txt = (msg.get("content") or "").strip()
        if not txt:
            rec.update({"ok": False, "error": "empty_content",
                        "detail": (msg.get("reasoning") or msg.get("reasoning_content") or "")[:160],
                        "finish_reason": d["choices"][0].get("finish_reason")})
        else:
            rec.update({"ok": True, "sample": txt[:40], "usage": d.get("usage") or {}})
    except urllib.error.HTTPError as e:
        rec.update({"ok": False, "error": f"HTTP {e.code}",
                    "detail": e.read().decode("utf-8", "replace")[:500],
                    "resp_headers": rl_headers(e.headers or {})})
    except Exception as e:
        rec.update({"ok": False, "error": f"{type(e).__name__}: {str(e)[:160]}"})
    rec["latency_ms"] = int((time.time() - t0) * 1000)
    emit(rec)
    return rec


def models_probe(name: str, base: str, key_env: str, env: dict) -> dict:
    t0 = time.time()
    rec = {"phase": "models", "provider": name, "ts": now()}
    headers = {"User-Agent": "mag-d22-probe/2.0"}
    if env.get(key_env):
        headers["Authorization"] = f"Bearer {env[key_env]}"
    req = urllib.request.Request(base.rstrip("/") + "/models", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read().decode("utf-8", "replace"))
            rec["resp_headers"] = rl_headers(r.headers)
        ids = [m.get("id") for m in (d.get("data") or d.get("models") or []) if m.get("id")]
        rec.update({"ok": True, "model_count": len(ids), "models_sample": sorted(ids)[:6]})
    except urllib.error.HTTPError as e:
        rec.update({"ok": False, "error": f"HTTP {e.code}",
                    "detail": e.read().decode("utf-8", "replace")[:200],
                    "resp_headers": rl_headers(e.headers or {})})
    except Exception as e:
        rec.update({"ok": False, "error": f"{type(e).__name__}: {str(e)[:160]}"})
    rec["latency_ms"] = int((time.time() - t0) * 1000)
    emit(rec)
    return rec


def main() -> int:
    env = _env()
    by_id = {l["id"]: l for l in LANES}
    print(f"=== D22 pass-2 probe start {now()} ===", flush=True)

    # Phase 1: re-verify the 8 lanes gen-1 logged ALIVE
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = []
        for lid in ALIVE_8:
            lane = by_id[lid]
            key = env.get(lane["key"], "")
            if not key:
                emit({"phase": "reverify", "lane": lid, "ok": False, "error": "NO_KEY",
                      "ts": now(), "latency_ms": 0})
                continue
            futs.append(ex.submit(chat_probe, lane, key, "reverify"))
        for f in futs:
            f.result()

    # Phase 2: classified retry on the 3 lanes gen-1 logged DEAD (429)
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = []
        for lid in DEAD_3:
            lane = by_id[lid]
            key = env.get(lane["key"], "")
            if not key:
                emit({"phase": "retry", "lane": lid, "ok": False, "error": "NO_KEY",
                      "ts": now(), "latency_ms": 0})
                continue
            futs.append(ex.submit(chat_probe, lane, key, "retry"))
        for f in futs:
            f.result()

    # Phase 3: un-metered GET /models per provider (quota-headroom signals)
    with ThreadPoolExecutor(max_workers=5) as ex:
        futs = [ex.submit(models_probe, n, b, k, env) for (n, b, k) in PROVIDERS]
        for f in futs:
            f.result()

    print(f"=== D22 pass-2 probe done {now()} — results: {OUT} ===", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
