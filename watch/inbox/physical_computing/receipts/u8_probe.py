# U8 probe harness — stealth/union-alpha on OpenRouter.
# Rules honored: repo key never printed; only openrouter.ai endpoints; small payloads.
import sys, time, json, threading
import urllib.request, urllib.error

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
sys.path.insert(0, ROOT)
from mag.flight_recorder import load_env

ENV = load_env(ROOT)
KEY = ENV.get("OPENROUTER_API_KEY", "")
if not KEY:
    print("FATAL: no key found in .env")
    sys.exit(1)

URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json",
    "User-Agent": "u8-intel/1.0",
}
MODEL = "stealth/union-alpha"

RL_HEADERS = [
    "x-ratelimit-limit-requests", "x-ratelimit-limit-tokens",
    "x-ratelimit-remaining-requests", "x-ratelimit-remaining-tokens",
    "x-ratelimit-reset-requests", "x-ratelimit-reset-tokens",
    "ratelimit-limit", "ratelimit-remaining", "ratelimit-reset",
    "retry-after", "x-ratelimit-reset",
]


def probe(tag, messages, max_tokens=64, temperature=0.0):
    body = json.dumps({
        "model": MODEL, "messages": messages,
        "max_tokens": max_tokens, "temperature": temperature,
    }).encode("utf-8")
    req = urllib.request.Request(URL, data=body, headers=HEADERS, method="POST")
    t0 = time.perf_counter()
    rec = {"tag": tag, "ok": False}
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            dt = time.perf_counter() - t0
            data = json.loads(r.read().decode("utf-8"))
            rec.update(ok=True, latency_s=round(dt, 2), status=r.status)
            hdrs = {}
            for k in RL_HEADERS:
                v = r.headers.get(k)
                if v is not None:
                    hdrs[k] = v
            rec["rate_headers"] = hdrs
            rec["server_timing"] = r.headers.get("Server-Timing")
            rec["all_header_names"] = sorted(r.headers.keys())
            u = data.get("usage", {})
            rec["usage"] = {k: u.get(k) for k in
                            ("prompt_tokens", "completion_tokens", "total_tokens", "cost")}
            ch = (data.get("choices") or [{}])[0]
            msg = ch.get("message", {})
            txt = msg.get("content")
            if not txt and msg.get("reasoning"):
                txt = "<reasoning-only>"
            rec["model_reported"] = data.get("model")
            rec["text_head"] = (txt or "")[:300]
            rec["finish"] = ch.get("finish_reason")
            ct = u.get("completion_tokens")
            rec["tps"] = round(ct / dt, 2) if ct and dt > 0 else None
    except urllib.error.HTTPError as e:
        dt = time.perf_counter() - t0
        rec.update(latency_s=round(dt, 2), status=e.code)
        hdrs = {}
        for k in RL_HEADERS:
            v = e.headers.get(k)
            if v is not None:
                hdrs[k] = v
        rec["rate_headers"] = hdrs
        try:
            rec["error_body"] = json.loads(e.read().decode("utf-8"))
        except Exception:
            rec["error_body"] = "<unreadable>"
    except Exception as e:
        rec.update(error=repr(e)[:200])
    return rec


def burst(tag, n, messages, max_tokens=32):
    out = []
    lock = threading.Lock()

    def run(i):
        r = probe(f"{tag}-{i}", messages, max_tokens=max_tokens)
        with lock:
            out.append(r)

    ts = [threading.Thread(target=run, args=(i,)) for i in range(n)]
    t0 = time.perf_counter()
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    out.sort(key=lambda r: r["tag"])
    return out, round(time.perf_counter() - t0, 2)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "list"
    print(json.dumps({"mode": mode}))
