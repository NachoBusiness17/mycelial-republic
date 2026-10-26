"""B2-129: capture the gemini Bearer 401 body that B2_04 lost.

PROVIDER_HEALTH_20260926.md:24 quotes generateContent 401 as Bearer
("invalid authentication credentials") but neither B2_04_probe_results.json
nor B2_04_probe_results2.json holds that body (the persisted gemini_native_diag
carries only the native API-key 401 "API keys are not supported by this API",
B2_04_probe_results2.json:64-74). This script fires generateContent twice with
the same key, once per auth mode, and persists BOTH full bodies so the next
run closes the gap. Synthetic prompt only ("ping"), never private material.
Key is read from .env GEMINI_API_KEY and masked in every output byte.

Usage: .venv/Scripts/python.exe B2_129_gemini_bearer_retry.py [out.json]
Exit 0 when both bodies persisted, 1 on transport failure, 2 on missing key.
"""
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
URL = ("https://generativelanguage.googleapis.com/v1beta/models/"
       "gemini-2.5-flash:generateContent")
BODY = json.dumps({"contents": [{"parts": [{"text": "ping"}]}]}).encode()
DEFAULT_OUT = Path(__file__).resolve().parent / "B2_129_gemini_auth_bodies.json"


def read_key() -> str:
    env = ROOT / ".env"
    for ln in env.read_text(encoding="utf-8").splitlines():
        if ln.startswith("GEMINI_API_KEY="):
            return ln.split("=", 1)[1].strip()
    return ""


def mask(k: str) -> str:
    return (k[:5] + "...") if len(k) > 8 else "***"


def fire(mode: str, key: str) -> dict:
    if mode == "bearer":
        headers = {"Authorization": "Bearer " + key,
                   "Content-Type": "application/json"}
    else:
        headers = {"x-goog-api-key": key,
                   "Content-Type": "application/json"}
    req = urllib.request.Request(URL, data=BODY, headers=headers, method="POST")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read().decode("utf-8", "replace")
            status = r.status
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        status = e.code
    except Exception as e:  # noqa: BLE001
        return {"mode": mode, "status": 0, "transport_error": repr(e)[:200],
                "latency_s": round(time.time() - t0, 2)}
    return {"mode": mode, "status": status, "body": raw,
            "latency_s": round(time.time() - t0, 2)}


def main() -> int:
    key = read_key()
    if not key:
        print("GEMINI_API_KEY not found in .env")
        return 2
    out_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUT
    results = [fire("native_key", key), fire("bearer", key)]
    doc = {"tool": "B2_129_gemini_bearer_retry.py",
           "url": URL,
           "key_masked": mask(key),
           "prompt": "ping (synthetic)",
           "results": results}
    out_path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    for r in results:
        head = r.get("body", r.get("transport_error", ""))[:120]
        print(f"{r['mode']}: status {r['status']} :: {head}")
    print("persisted:", out_path)
    return 0 if all(r.get("status") for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
