# B2-105 mistral lane surgery: verify the landed state against live bytes and
# one live call per arm, BEFORE writing the receipt. Keys are read from .env
# case-insensitively and never printed (prefix only). Synthetic prompt only,
# one token max, two calls total (new default + old default for contrast).
#
# Checks:
#  A. configs/providers.yaml mistral block: default_model == mistral-small-latest,
#     dormant true, roster holds only the catalog-present id, nameplate + quota
#     note carry the measured shapes, routing lists exclude mistral.
#  B. models.providers.load_providers estate: mistral reads the same fields.
#  C. mag.doctor.check_provider_endpoints (default, no probe env): mistral reads
#     DORMANT, probe none(dormant), and no issue names mistral.
#  D. Live: chat on mistral-small-latest (the yaml default) must answer the
#     B2-04 zero-quota shape (429 + x-ratelimit-*-limit: 0), NOT the 403
#     tier_not_allowed the old default produced; chat on mistral-large-latest
#     must still 403, proving the 403 rode the id and the surgery moved it off
#     the default seat.
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "B2_105_verify_results.json")

PROMPT = "Reply with exactly one word: ALIVE"


def env_key(*names):
    path = os.path.join(REPO, ".env")
    want = {n.lower() for n in names}
    found = {}
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            m = re.match(r"^([A-Za-z0-9_\-]+)\s*=\s*(.*)$", line.strip())
            if m and m.group(1).lower() in want:
                v = m.group(2).strip().strip('"').strip("'")
                if v:
                    found[m.group(1)] = v
    return found


def call(url, key, body):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) MagProbe/1.0",
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(
        url, headers=headers, data=json.dumps(body).encode("utf-8"), method="POST")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            status, raw, hdrs = (resp.status, resp.read().decode("utf-8", errors="replace"),
                                 dict(resp.headers))
    except urllib.error.HTTPError as e:
        status, raw, hdrs = e.code, e.read().decode("utf-8", errors="replace"), dict(e.headers)
    except Exception as e:
        return {"status": 0, "latency_s": round(time.time() - t0, 2),
                "error": "%s: %s" % (type(e).__name__, e)[:160], "rl": {}}
    rl = {k: v for k, v in hdrs.items()
          if k.lower().startswith(("x-ratelimit", "ratelimit"))}
    return {"status": status, "latency_s": round(time.time() - t0, 2),
            "rl": rl, "body": raw[:300]}


def main():
    out = {}

    # A. yaml bytes
    import yaml
    with open(os.path.join(REPO, "configs", "providers.yaml"),
              encoding="utf-8", errors="replace") as f:
        cfg = yaml.safe_load(f)
    m = cfg["providers"]["mistral"]
    out["yaml_mistral"] = {
        "name": m.get("name"),
        "dormant": m.get("dormant"),
        "models": m.get("models"),
        "default_model": m.get("default_model"),
        "quota_note": m.get("quota", {}).get("note"),
    }
    routing = cfg.get("routing", {})
    out["routing_mistral_hits"] = {k: v for k, v in routing.items()
                                   if "mistral" in (v or [])}
    out["routing_lists"] = sorted(routing.keys())

    # B. estate loader
    sys.path.insert(0, REPO)
    from models.providers import load_providers
    provs = load_providers()
    hits = [p for p in provs if getattr(p, "name", "") == "mistral"]
    if hits:
        p = hits[0]
        out["estate_mistral"] = {
            "default_model": getattr(p, "default_model", None),
            "dormant": getattr(p, "dormant", None),
            "models": list(getattr(p, "models", []) or []),
        }
    else:
        out["estate_mistral"] = "NOT FOUND in %d providers" % len(provs)
    out["estate_count"] = len(provs)

    # C. doctor default-path status (statuses: provider -> string;
    # providers: list of detail rows)
    from mag import doctor
    r = doctor.check_provider_endpoints()
    out["doctor_mistral_status"] = r["statuses"].get("mistral")
    pv = r.get("providers")
    if isinstance(pv, dict):
        pv = [dict(v, provider=k) for k, v in pv.items()]
    out["doctor_mistral_detail"] = [x for x in pv if x.get("provider") == "mistral"]
    out["doctor_issues_mistral"] = [i for i in r.get("issues", [])
                                    if "mistral" in str(i).lower()]

    # D. live probes (two one-token calls)
    keys = env_key("MISTRAL_API_KEY", "Mistral_API_KEY")
    key_name = sorted(keys)[0] if keys else None
    out["key"] = {"name": key_name,
                  "prefix": (keys[key_name][:6] + "...") if key_name else None}
    if key_name:
        body = {"model": None, "messages": [{"role": "user", "content": PROMPT}],
                "max_tokens": 1}
        for model in ("mistral-small-latest", "mistral-large-latest"):
            body["model"] = model
            out["probe_" + model] = call("https://api.mistral.ai/v1/chat/completions",
                                         keys[key_name], body)
            time.sleep(2)

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
