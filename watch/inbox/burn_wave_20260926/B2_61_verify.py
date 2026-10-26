# B2-61 roster purge: one live verification call per planned change, BEFORE
# any providers.yaml write. Keys are read from .env and never printed (prefix
# only). Synthetic prompt only (public-domain sentence), never repo material.
#
# Planned changes and their live gates:
#  1. openrouter drop 3 stale :free ids  -> GET /api/v1/models: old ids absent,
#     stealth/space-bunny-alpha present; repoint candidate chat-verified (200).
#  2. nvidia dormant + roster purge      -> chat on deepseek-ai/deepseek-v4-flash-0731
#     expected 404/410 "Not found for account".
#  3. gemini dormant                     -> chat on gemini-2.0-flash via the
#     openai-compat base expected 401 "API keys are not supported".
#  4. mistral dormant (+ default repoint if absent) -> chat on mistral-large-latest
#     expected 429 x-ratelimit-limit-req-minute: 0; catalog GET for id presence.
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "B2_61_verify_results.json")

PROMPT = "Reply with exactly one word: ALIVE"


def env_key(*names):
    path = os.path.join(REPO, ".env")
    want = set(names)
    found = {}
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            m = re.match(r"^([A-Za-z0-9_\-]+)\s*=\s*(.*)$", line.strip())
            if m and m.group(1) in want:
                v = m.group(2).strip().strip('"').strip("'")
                if v:
                    found[m.group(1)] = v
    return found


def call(url, key, body=None, method=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) MagProbe/1.0",
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json",
    }
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, headers=headers, data=data, method=method)
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            status, raw, hdrs = resp.status, resp.read().decode("utf-8", errors="replace"), dict(resp.headers)
    except urllib.error.HTTPError as e:
        status, raw, hdrs = e.code, e.read().decode("utf-8", errors="replace"), dict(e.headers)
    except Exception as e:
        return {"status": 0, "latency_s": round(time.time() - t0, 2),
                "error": "%s: %s" % (type(e).__name__, e)[:160], "rl": {}}
    rl = {k: v for k, v in hdrs.items() if k.lower().startswith(("x-ratelimit", "ratelimit"))}
    content, err = "", ""
    try:
        j = json.loads(raw)
        if status == 200 and isinstance(j, dict):
            ch = (j.get("choices") or [{}])[0]
            content = ((ch.get("message") or {}).get("content") or "")[:120]
        else:
            err = raw[:220]
    except Exception:
        err = raw[:220]
    return {"status": status, "latency_s": round(time.time() - t0, 2),
            "content": content, "body_err": err, "rl": rl}


def chat(url, model, key):
    return call(url.rstrip("/") + "/chat/completions", key, body={
        "model": model,
        "messages": [{"role": "user", "content": PROMPT}],
        "max_tokens": 16,
    })


def main():
    keys = env_key("OPENROUTER_API_KEY", "NVIDIABuild", "NVIDIA_API_KEY",
                   "NVIDIABuild-Autogen-46", "GEMINI_API_KEY", "MISTRAL_API_KEY")
    out = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "keys_seen": sorted(keys)}

    # 1. openrouter catalog + repoint probe
    if "OPENROUTER_API_KEY" in keys:
        k = keys["OPENROUTER_API_KEY"]
        cat = call("https://openrouter.ai/api/v1/models", k)
        ids = []
        if cat["status"] == 200:
            req = urllib.request.Request("https://openrouter.ai/api/v1/models", headers={
                "User-Agent": "Mozilla/5.0 MagProbe/1.0", "Authorization": "Bearer " + k})
            with urllib.request.urlopen(req, timeout=45) as resp:
                ids = [m.get("id", "") for m in json.loads(resp.read().decode("utf-8")).get("data", [])]
        free = sorted(i for i in ids if i.endswith(":free"))
        out["openrouter_catalog"] = {
            "status": cat["status"], "model_count": len(ids),
            "old_ids_absent": {
                "meta-llama/llama-3.3-70b-instruct:free": "meta-llama/llama-3.3-70b-instruct:free" not in ids,
                "google/gemma-2-9b-it:free": "google/gemma-2-9b-it:free" not in ids,
                "deepseek/deepseek-r1:free": "deepseek/deepseek-r1:free" not in ids,
            },
            "stealth_present": "stealth/space-bunny-alpha" in ids,
            "auto_present": "openrouter/auto" in ids,
            "free_ids": free,
        }
        # repoint candidate: first non-stealth :free id, chat-verified once
        cand = next((i for i in free if "space-bunny" not in i), None)
        if cand:
            out["openrouter_repoint_probe"] = {"model": cand, **chat("https://openrouter.ai/api/v1", cand, k)}

    # 2. nvidia: one chat call on the yaml default_model
    nk = keys.get("NVIDIABuild") or keys.get("NVIDIA_API_KEY") or keys.get("NVIDIABuild-Autogen-46")
    if nk:
        out["nvidia_chat"] = chat("https://integrate.api.nvidia.com/v1",
                                  "deepseek-ai/deepseek-v4-flash-0731", nk)

    # 3. gemini: one chat call via the openai-compat base
    if "GEMINI_API_KEY" in keys:
        out["gemini_chat"] = chat("https://generativelanguage.googleapis.com/v1beta/openai",
                                  "gemini-2.0-flash", keys["GEMINI_API_KEY"])

    # 4. mistral: one chat call on the yaml default + catalog presence check
    if "MISTRAL_API_KEY" in keys:
        mk = keys["MISTRAL_API_KEY"]
        out["mistral_chat"] = chat("https://api.mistral.ai/v1", "mistral-large-latest", mk)
        mcat = call("https://api.mistral.ai/v1/models", mk)
        mids = []
        if mcat["status"] == 200:
            req = urllib.request.Request("https://api.mistral.ai/v1/models", headers={
                "User-Agent": "Mozilla/5.0 MagProbe/1.0", "Authorization": "Bearer " + mk})
            with urllib.request.urlopen(req, timeout=45) as resp:
                mids = [m.get("id", "") for m in json.loads(resp.read().decode("utf-8")).get("data", [])]
        out["mistral_catalog"] = {"status": mcat["status"], "model_count": len(mids),
                                  "mistral_large_latest_present": "mistral-large-latest" in mids,
                                  "mistral_small_latest_present": "mistral-small-latest" in mids}

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out, indent=1))
    print("WROTE " + OUT)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
