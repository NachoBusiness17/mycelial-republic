# B2-63 lane probe: identify the correct auth shape for the AQ.* (Vertex AI
# express mode) key on the native endpoint. One minimal generate call licensed
# by the lane brief. Synthetic prompt only, key never printed.
# Hypothesis (from docs.cloud.google.com/vertex-ai/generative-ai/docs/start/
# express-mode/overview, fetched 2026-09-26): express keys work on
# aiplatform.googleapis.com/v1/publishers/google/models/{model}:generateContent
# via ?key= param or the x-goog-api-key header, NOT on generativelanguage.
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "B2_63_vertex_probe_results.json")
MODEL = "gemini-2.5-flash"  # in the express-mode docs model table (10 RPM band)
BODY = {"contents": [{"parts": [{"text": "Reply with the single word: ALIVE."}]}],
        "generationConfig": {"maxOutputTokens": 16, "temperature": 0}}


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


def post(url, headers, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"),
                                 headers=headers, method="POST")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            return {"status": r.status, "latency_s": round(time.time() - t0, 2),
                    "body": r.read().decode("utf-8", errors="replace")}
    except urllib.error.HTTPError as e:
        raw = ""
        try:
            raw = e.read().decode("utf-8", errors="replace")
        except Exception:
            pass
        return {"status": e.code, "latency_s": round(time.time() - t0, 2), "body": raw}
    except Exception as e:
        return {"status": 0, "latency_s": round(time.time() - t0, 2),
                "body": type(e).__name__ + ": " + str(e)[:200]}


def summarize(tag, r):
    out = {"tag": tag, "status": r["status"], "latency_s": r["latency_s"]}
    try:
        j = json.loads(r["body"])
    except Exception:
        out["body_head"] = re.sub(r"\s+", " ", r["body"])[:240]
        return out
    if r["status"] == 200:
        cand = (j.get("candidates") or [{}])[0]
        parts = ((cand.get("content") or {}).get("parts") or [{}])[0]
        out["text"] = parts.get("text", "")
        out["usageMetadata"] = j.get("usageMetadata", {})
        out["modelVersion"] = j.get("modelVersion")
    else:
        err = j.get("error", {})
        out["error_status"] = err.get("status")
        out["error_message"] = re.sub(r"\s+", " ", str(err.get("message", "")))[:240]
    return out


def main():
    env = load_env()
    key = env["GEMINI_API_KEY"]
    same = "GOOGLE_API_KEY" in env and env["GOOGLE_API_KEY"] == key
    res = {"model": MODEL, "keys_identical": same, "key_prefix": key[:6]}
    base = "https://aiplatform.googleapis.com/v1/publishers/google/models/"
    url = base + MODEL + ":generateContent"

    # Attempt 1: x-goog-api-key header (no key in URL).
    r = post(url, {"Content-Type": "application/json", "x-goog-api-key": key}, BODY)
    res["header_auth"] = summarize("vertex native x-goog-api-key", r)
    print("header_auth ->", res["header_auth"])

    # Attempt 2 (only if the documented header form failed): ?key= query param,
    # the exact URL shape quoted in the express-mode docs table.
    if res["header_auth"]["status"] != 200:
        r2 = post(url + "?key=" + key, {"Content-Type": "application/json"}, BODY)
        res["query_param_auth"] = summarize("vertex native ?key=", r2)
        print("query_param_auth ->", res["query_param_auth"])

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1)
    print("WROTE " + OUT)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
