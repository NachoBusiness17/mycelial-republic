# B2-04 free-lane live probe harness (2026-09-26).
# Probes every free lane in configs/providers.yaml that has a key in .env.
# Per lane: GET /models, 3 tiny alive calls, then 3 synthetic estate prompts
# (public-domain summarize, Go position classify, word count). Records
# latency, status, rate-limit headers (the measured denominator) and usage.
# Synthetic prompts only. No repo contents, no private material, ever.
import json
import os
import re
import ssl
import sys
import time
import urllib.request
import urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
RESULTS_PATH = os.path.join(HERE, "B2_04_probe_results.json")
TIMEOUT = 30

ALIVE_PROMPT = "Reply with the single word: ALIVE."
BURN_PROMPTS = [
    ("summarize_public_domain",
     "Summarize this public-domain paragraph (Lincoln, Gettysburg Address, 1863) "
     "in exactly one sentence: Four score and seven years ago our fathers brought "
     "forth on this continent, a new nation, conceived in Liberty, and dedicated "
     "to the proposition that all men are created equal."),
    ("go_position_classify",
     "In a game of Go, Black has stones at Q16 and R14; White has stones at Q4 "
     "and D16. Fewer than 10 stones are on the board. Classify the phase in one "
     "word, one of: opening, middle, endgame."),
    ("count_words",
     "Count the words in this sentence and reply with only the number: "
     "The quick brown fox jumps over the lazy dog beside the quiet river bank."),
]


def load_env():
    env = {}
    path = os.path.join(REPO, ".env")
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*=\s*(.*)$", line)
            if m:
                env[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return env


def mask(v):
    return (v[:6] + "...") if v else "MISSING"


def http(method, url, key, body=None, extra_headers=None, timeout=TIMEOUT):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36 MagProbe/1.0",
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json",
    }
    if extra_headers:
        headers.update(extra_headers)
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            return {
                "status": resp.status,
                "latency_s": round(time.time() - t0, 2),
                "body": raw,
                "rl": rate_limit_headers(dict(resp.headers)),
            }
    except urllib.error.HTTPError as e:
        raw = ""
        try:
            raw = e.read().decode("utf-8", errors="replace")
        except Exception:
            pass
        return {"status": e.code, "latency_s": round(time.time() - t0, 2),
                "body": raw, "rl": rate_limit_headers(dict(e.headers or {}))}
    except Exception as e:
        return {"status": 0, "latency_s": round(time.time() - t0, 2),
                "body": type(e).__name__ + ": " + str(e)[:200], "rl": {}}


def rate_limit_headers(h):
    out = {}
    for k, v in h.items():
        lk = k.lower()
        if "ratelimit" in lk.replace("-", "") or "quota" in lk or "retry-after" in lk:
            out[k] = v
    return out


def chat(url_base, key, model, prompt, max_tokens, extra=None, extra_headers=None):
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0,
    }
    if extra:
        payload.update(extra)
    return http("POST", url_base + "/chat/completions", key, payload, extra_headers)


def trimmed(s, n=110):
    s = re.sub(r"\s+", " ", s or "").strip()
    return s[:n]


def extract_content(resp):
    try:
        j = json.loads(resp["body"])
        return j["choices"][0]["message"].get("content") or ""
    except Exception:
        return ""


def extract_usage(resp):
    try:
        u = json.loads(resp["body"]).get("usage") or {}
        return {k: u.get(k) for k in ("prompt_tokens", "completion_tokens", "total_tokens")}
    except Exception:
        return {}


def probe_lane(name, base, key, models_path, model_chain, max_tokens, extra=None,
               extra_headers=None, do_models=True):
    lane = {"lane": name, "endpoint": base, "key": mask(key), "models": None,
            "alive_calls": [], "burn": [], "verdict": ""}
    # 1) model list
    if do_models:
        r = http("GET", base + models_path, key, extra_headers=extra_headers)
        try:
            ids = [m.get("id") for m in json.loads(r["body"]).get("data", [])]
            lane["models"] = {"status": r["status"], "latency_s": r["latency_s"],
                              "count": len(ids), "sample": ids[:6],
                              "chain_present": [m for m in model_chain if m in ids][:3]}
        except Exception:
            lane["models"] = {"status": r["status"], "latency_s": r["latency_s"],
                              "error": trimmed(r["body"], 160)}
    # 2) three alive calls
    ok = 0
    for i in range(3):
        r = chat(base, key, model_chain[0], ALIVE_PROMPT, min(max_tokens, 40),
                 extra, extra_headers)
        c = extract_content(r)
        entry = {"i": i + 1, "status": r["status"], "latency_s": r["latency_s"],
                 "content": trimmed(c, 40), "usage": extract_usage(r)}
        if r["status"] == 400 and extra:  # retry without provider-specific extras
            r = chat(base, key, model_chain[0], ALIVE_PROMPT, min(max_tokens, 40),
                     None, extra_headers)
            entry = {"i": i + 1, "status": r["status"], "latency_s": r["latency_s"],
                     "content": trimmed(extract_content(r), 40),
                     "usage": extract_usage(r), "note": "retried without extras"}
        entry["rl"] = r["rl"]
        lane["alive_calls"].append(entry)
        if r["status"] == 200 and c.strip():
            ok += 1
        elif r["status"] in (404, 400) and len(model_chain) > 1:
            model_chain = model_chain[1:]  # fall through chain on next iteration
    lane["model_used"] = model_chain[0]
    if ok == 0:
        last = lane["alive_calls"][-1] if lane["alive_calls"] else {}
        lane["verdict"] = "DEAD status=%s body=%s" % (
            last.get("status"), trimmed(str(last.get("content", "")) or "", 120))
        return lane
    # 3) burn the synthetic estate prompts
    for tag, prompt in BURN_PROMPTS:
        r = chat(base, key, model_chain[0], prompt, max_tokens, extra, extra_headers)
        c = extract_content(r)
        if (not c.strip()) and r["status"] == 200 and max_tokens < 900:
            r2 = chat(base, key, model_chain[0], prompt, 1200, extra, extra_headers)
            c2 = extract_content(r2)
            if c2.strip():
                r, c = r2, c2
                lane["burn"].append({"tag": tag, "status": r["status"],
                                     "latency_s": r["latency_s"], "content": trimmed(c),
                                     "usage": extract_usage(r), "rl": r["rl"],
                                     "note": "empty at small budget, retried at 1200"})
                continue
        lane["burn"].append({"tag": tag, "status": r["status"], "latency_s": r["latency_s"],
                             "content": trimmed(c), "usage": extract_usage(r), "rl": r["rl"]})
    lane["verdict"] = "ALIVE"
    return lane


def verdict_only(name, endpoint, why):
    return {"lane": name, "endpoint": endpoint, "verdict": why}


def main():
    env = load_env()
    out = []

    # --- ollama local (context row, not an external burn) ---
    r = http("GET", "http://127.0.0.1:11434/v1/models", "ollama", timeout=6)
    try:
        n = len(json.loads(r["body"]).get("data", []))
    except Exception:
        n = 0
    out.append(verdict_only("ollama-local", "http://127.0.0.1:11434/v1",
                            "models_status=%s count=%d" % (r["status"], n)))

    # --- saelis: declared dormant, one probe attempt per law ---
    r = http("GET", "http://127.0.0.1:8080/v1/models", "saelis", timeout=4)
    out.append(verdict_only("saelis-dormant", "http://127.0.0.1:8080/v1",
                            "dormant per providers.yaml; one probe status=%s" % r["status"]))

    # --- groq (free tier, 2 keys) ---
    k = env.get("GROQ_API_KEY", "")
    if k:
        out.append(probe_lane(
            "groq", "https://api.groq.com/openai/v1", k, "/models",
            # B2-115 dated-frozen 2026-09-26: chain kept as a period artifact.
            # qwen/qwen3.6-27b and groq/compound-mini were 404-dead on groq as of
            # 2026-09-26 (post-surgery roster); a rerun burns 404s on them before
            # falling through. Fix this roster before any rerun, or read
            # configs/providers.yaml for the live set.
            ["openai/gpt-oss-120b", "qwen/qwen3.6-27b", "groq/compound-mini"],
            160, extra={"reasoning_effort": "low"}))
    else:
        out.append(verdict_only("groq", "https://api.groq.com/openai/v1", "no key"))

    # --- cerebras (free tier; key under the typo'd CEREBAS name) ---
    k = env.get("CEREBRAS_API_KEY") or env.get("CEREBAS_API_KEY", "")
    if k:
        out.append(probe_lane(
            "cerebras", "https://api.cerebras.ai/v1", k, "/models",
            ["gpt-oss-120b", "llama-3.3-70b"], 160, extra={"reasoning_effort": "low"}))
    else:
        out.append(verdict_only("cerebras", "https://api.cerebras.ai/v1", "no key"))

    # --- nvidia build (free credits) ---
    k = env.get("NVIDIABuild", "") or env.get("NVIDIA_API_KEY", "")
    if k:
        out.append(probe_lane(
            "nvidia", "https://integrate.api.nvidia.com/v1", k, "/models",
            ["meta/llama-3.1-8b-instruct", "meta/llama-3.3-70b-instruct",
             "deepseek-ai/deepseek-v4-flash-0731"], 100))
    else:
        out.append(verdict_only("nvidia", "https://integrate.api.nvidia.com/v1", "no key"))

    # --- gemini (free tier) ---
    k = env.get("GEMINI_API_KEY") or env.get("GOOGLE_API_KEY", "")
    if k:
        out.append(probe_lane(
            "gemini", "https://generativelanguage.googleapis.com/v1beta/openai", k,
            "/models", ["gemini-2.0-flash", "gemini-2.5-flash", "gemini-1.5-flash"], 100))
    else:
        out.append(verdict_only("gemini",
                                "https://generativelanguage.googleapis.com/v1beta/openai",
                                "no key"))

    # --- openrouter free lanes (2 operator keys) ---
    OR_HEADERS = {"HTTP-Referer": "http://127.0.0.1:8765", "X-Title": "Mag Resource Harness"}
    for idx, kk in enumerate(("OPENROUTER_API_KEY", "OPENROUTER_API_KEY_2"), 1):
        k = env.get(kk, "")
        if k:
            out.append(probe_lane(
                "openrouter-key%d" % idx, "https://openrouter.ai/api/v1", k, "/models",
                ["meta-llama/llama-3.3-70b-instruct:free", "google/gemma-2-9b-it:free"],
                100, extra_headers=OR_HEADERS))
        else:
            out.append(verdict_only("openrouter-key%d" % idx,
                                    "https://openrouter.ai/api/v1", "no key"))

    # --- z_ai2 Pro + z_ai3 Lite (free: true, coding-plan path per endpoint law) ---
    for name, kk in (("zai-pro", "ZAI_API_KEY_Pro"), ("zai-lite", "ZAI_API_KEY_Lite")):
        k = env.get(kk, "")
        if k:
            out.append(probe_lane(
                name, "https://api.z.ai/api/coding/paas/v4", k, "/models",
                ["glm-4.7-flash", "glm-5.3-flash"], 150))
        else:
            out.append(verdict_only(name, "https://api.z.ai/api/coding/paas/v4", "no key"))

    # --- nous (Hermes keys; stealth catalog free during window) ---
    k = env.get("HERMES_API_KEY_1", "")
    if k:
        out.append(probe_lane(
            "nous-hermes", "https://inference-api.nousresearch.com/v1", k, "/models",
            ["meituan/longcat-2.0:free", "stealth/space-bunny-alpha",
             "inclusionai/ling-3.0-flash-sante:free"], 200))
    else:
        out.append(verdict_only("nous-hermes",
                                "https://inference-api.nousresearch.com/v1", "no key"))

    # --- together (free trial credits) ---
    k = env.get("TOGETHER_API_KEY", "")
    if k:
        out.append(probe_lane(
            "together", "https://api.together.xyz/v1", k, "/models",
            ["deepseek-ai/DeepSeek-V4-Flash-0731", "meta-llama/Llama-3.3-70B-Instruct-Turbo"],
            200))
    else:
        out.append(verdict_only("together", "https://api.together.xyz/v1", "no key"))

    # --- cohere (trial key, free name) ---
    k = env.get("COHERE_API_KEY_FREE", "") or env.get("COHERE_API_KEY", "")
    if k:
        out.append(probe_lane(
            "cohere", "https://api.cohere.com/compatibility/v1", k, "/models",
            ["command-r-plus-08-2024", "command-r-08-2024"], 100))
    else:
        out.append(verdict_only("cohere", "https://api.cohere.com/compatibility/v1", "no key"))

    # --- mistral (La Plateforme free tier) ---
    k = env.get("MISTRAL_API_KEY") or env.get("Mistral_API_KEY", "")
    if k:
        out.append(probe_lane(
            "mistral", "https://api.mistral.ai/v1", k, "/models",
            ["mistral-small-latest", "open-mistral-nemo", "ministral-8b-latest"], 100))
    else:
        out.append(verdict_only("mistral", "https://api.mistral.ai/v1", "no key"))

    # --- no-key free lanes: verdict lines ---
    out.append(verdict_only("hf_router", "https://router.huggingface.co/v1",
                            "no HF_TOKEN on file; no probe possible"))
    out.append(verdict_only("github_models", "https://models.inference.ai.azure.com",
                            "no GITHUB_MODELS_TOKEN on file; gh CLI token also absent"))
    out.append(verdict_only("dashscope", "https://dashscope.aliyuncs.com/compatible-mode/v1",
                            "no DASHSCOPE_API_KEY on file"))
    out.append(verdict_only("moonshot", "https://api.moonshot.ai/v1", "no MOONSHOT_API_KEY on file"))
    out.append(verdict_only("fireworks", "https://api.fireworks.ai/inference/v1",
                            "no FIREWORKS_API_KEY on file"))
    out.append(verdict_only("zai-main-and-sdmax",
                            "https://api.z.ai/api/paas/v4",
                            "opencode_only per providers.yaml law; raw-API use skipped (fence risk)"))

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)

    # digest
    for lane in out:
        line = [lane["lane"], lane.get("verdict", "")]
        for b in lane.get("burn", []) or []:
            u = b.get("usage") or {}
            line.append("%s=%s(%s/%s/%s)" % (b["tag"][:12], b["status"],
                                             u.get("prompt_tokens"), u.get("completion_tokens"),
                                             u.get("total_tokens")))
        print(" | ".join(str(x) for x in line))
    print("WROTE " + RESULTS_PATH)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
