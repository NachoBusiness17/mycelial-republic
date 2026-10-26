# B2-35 groq lane surgery: single live verification call before config write.
# One GET /openai/v1/models with the operator key from .env. The key is never
# printed. Confirms: qwen/qwen3.8-27b present (docs replacement), qwen/qwen3.6-27b
# absent, groq/compound-mini absent, openai/gpt-oss-120b present (survivor).
import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "B2_35_groq_models.json")
URL = "https://api.groq.com/openai/v1/models"


def load_key():
    path = os.path.join(REPO, ".env")
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            m = re.match(r"^(GROQ_API_KEY|GROQ_API_KEY_2)\s*=\s*(.*)$", line.strip())
            if m and m.group(2).strip().strip('"').strip("'"):
                return m.group(1), m.group(2).strip().strip('"').strip("'")
    return None, None


def main():
    env_name, key = load_key()
    if not key:
        print("BLOCKED: no GROQ_API_KEY in .env")
        sys.exit(2)
    req = urllib.request.Request(URL, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) MagProbe/1.0",
        "Authorization": "Bearer " + key,
    })
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            status = resp.status
            raw = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:  # noqa: F821
        status = e.code
        raw = e.read().decode("utf-8", errors="replace")
    ids = sorted(m.get("id", "") for m in json.loads(raw).get("data", [])) if status == 200 else []
    checks = {
        "qwen_qwen3_8_27b_present": "qwen/qwen3.8-27b" in ids,
        "qwen_qwen3_6_27b_absent": "qwen/qwen3.6-27b" not in ids,
        "groq_compound_mini_absent": "groq/compound-mini" not in ids,
        "gpt_oss_120b_present": "openai/gpt-oss-120b" in ids,
    }
    result = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "url": URL,
        "key_env": env_name,
        "status": status,
        "latency_s": round(time.time() - t0, 2),
        "model_count": len(ids),
        "ids": ids,
        "checks": checks,
        "surgery_go": status == 200 and all(checks.values()),
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=1)
    print(json.dumps({k: v for k, v in result.items() if k != "ids"}, indent=1))
    print("IDS:")
    for i in ids:
        print(" ", i)
    print("WROTE " + OUT)
    sys.exit(0 if result["surgery_go"] else 1)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
