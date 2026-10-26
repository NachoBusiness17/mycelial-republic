# B2-114 groq third chat lane decision probe.
# Decision-grade evidence for: add openai/gpt-oss-20b as a third groq chat
# lane, or register the skip. Two live calls, synthetic prompt only:
#   1. GET  /openai/v1/models  -> is gpt-oss-20b still listed today?
#   2. POST chat/completions model=openai/gpt-oss-20b -> is it served, not
#      just listed (the B2-35 falsifier class "listed-but-unserved")?
# Key read from repo .env GROQ_API_KEY, never printed. Results land in
# B2_114_groq_20b_probe.json next to this script. Also parses the local
# providers.yaml groq guard so the receipt can quote the binding constraint.
import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "B2_114_groq_20b_probe.json")
BASE = "https://api.groq.com/openai/v1"
UA = "Mozilla/5.0 MagProbe/1.0 B2-114"


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


def call(method, path, key, body=None):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(
        BASE + path,
        data=data,
        headers={"Authorization": "Bearer " + key,
                 "User-Agent": UA,
                 "Content-Type": "application/json"},
        method=method)
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read().decode("utf-8", errors="replace")
            return {"status": r.status, "latency_s": round(time.time() - t0, 2),
                    "body": json.loads(raw)}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        return {"status": e.code, "latency_s": round(time.time() - t0, 2),
                "error_body": raw[:400]}


def main():
    env = load_env()
    key = env.get("GROQ_API_KEY")
    if not key:
        print("NO KEY: GROQ_API_KEY absent from .env", file=sys.stderr)
        return 2

    out = {"ts_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "key_env": "GROQ_API_KEY", "base": BASE}

    # 1. roster listing
    listing = call("GET", "/models", key)
    ids = []
    if listing.get("status") == 200:
        ids = sorted(m.get("id", "") for m in listing["body"].get("data", []))
    out["models_call"] = {k: listing[k] for k in ("status", "latency_s")}
    out["model_count"] = len(ids)
    out["gpt_oss_20b_listed"] = "openai/gpt-oss-20b" in ids
    out["ids"] = ids

    # 2. served check: one tiny synthetic chat call (never private material)
    served = call("POST", "/chat/completions", key, body={
        "model": "openai/gpt-oss-20b",
        "messages": [{"role": "user", "content": "Reply with the single word: pong"}],
        "max_completion_tokens": 64,
    })
    slim = {k: served[k] for k in ("status", "latency_s") if k in served}
    if served.get("status") == 200:
        ch = served["body"].get("choices", [{}])[0]
        slim["finish_reason"] = ch.get("finish_reason")
        content = (ch.get("message") or {}).get("content") or ""
        slim["content_len"] = len(content)
        slim["content_head"] = content[:80]
        slim["usage"] = served["body"].get("usage")
        slim["model_echo"] = served["body"].get("model")
    else:
        slim["error_body"] = served.get("error_body")
    out["gpt_oss_20b_chat"] = slim

    # 3. local guard bytes: the provider-level Mag soft guard on groq
    try:
        import yaml
        with open(os.path.join(REPO, "configs", "providers.yaml"),
                  encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        g = cfg["providers"]["groq"]
        out["local_guard"] = {"models": g.get("models"),
                              "default_model": g.get("default_model"),
                              "quota": {k: g.get("quota", {}).get(k)
                                        for k in ("period", "max_calls", "max_tokens")},
                              "out_of_routing_scope_count":
                                  len(g.get("out_of_routing_scope") or []),
                              "gpt_oss_20b_in_oors":
                                  "openai/gpt-oss-20b" in (g.get("out_of_routing_scope") or []),
                              "gpt_oss_20b_in_models":
                                  "openai/gpt-oss-20b" in (g.get("models") or [])}
    except Exception as e:  # noqa: BLE001 - probe records, does not hide
        out["local_guard_error"] = repr(e)[:200]

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    print(json.dumps({k: out[k] for k in
                      ("ts_utc", "model_count", "gpt_oss_20b_listed",
                       "gpt_oss_20b_chat", "local_guard")}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
