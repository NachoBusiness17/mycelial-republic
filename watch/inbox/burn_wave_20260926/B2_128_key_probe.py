# B2-128: re-GET both openrouter /key endpoints and persist the raw bodies.
# The B2-04 round-2 probe reported() the /key calls, which kept only choices
# content (empty), so the $4.608 / $0.7377 usage figures in
# B2_04_provider_health_20260926.md had no JSON bytes on disk. This probe
# lands those bytes. /key responses carry metadata only, no secret material.
import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "B2_128_keymeta_results.json")


def load_env():
    env = {}
    with open(os.path.join(REPO, ".env"), encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*=\s*(.*)$", line)
            if m:
                env[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return env


def get_key(key):
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/key",
        headers={"Authorization": "Bearer " + key,
                 "HTTP-Referer": "http://127.0.0.1:8765",
                 "X-Title": "Mag Resource Harness",
                 "User-Agent": "Mozilla/5.0 MagProbe/1.0 B2-128"},
        method="GET")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            return {"status": r.status, "latency_s": round(time.time() - t0, 2),
                    "body": json.loads(r.read().decode("utf-8", errors="replace"))}
    except Exception as e:
        raw = ""
        if hasattr(e, "read"):
            try:
                raw = e.read().decode("utf-8", errors="replace")[:240]
            except Exception:
                pass
        return {"status": getattr(e, "code", 0), "latency_s": round(time.time() - t0, 2),
                "body_raw": raw or (type(e).__name__ + ": " + str(e)[:200])}


def main():
    env = load_env()
    res = {}
    for idx, kk in (("1", "OPENROUTER_API_KEY"), ("2", "OPENROUTER_API_KEY_2")):
        res["openrouter_key" + idx + "_keymeta"] = get_key(env[kk])
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1)
    for k, v in res.items():
        d = v.get("body", {}).get("data", {})
        print(k, "status", v["status"], "usage", d.get("usage"), "limit", d.get("limit"),
              "is_free_tier", d.get("is_free_tier"))
    print("WROTE " + OUT)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
