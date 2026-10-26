# B2-04 probe round 2: targeted diagnostics + deferred burns on lanes that
# answered in round 1 only with empty/429. Synthetic prompts only.
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "B2_04_probe_results2.json")
TIMEOUT = 40

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
    with open(os.path.join(REPO, ".env"), encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*=\s*(.*)$", line)
            if m:
                env[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return env


def http(method, url, key, body=None, headers=None, timeout=TIMEOUT):
    hdrs = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36 MagProbe/1.0",
            "Authorization": "Bearer " + key, "Content-Type": "application/json"}
    if headers:
        hdrs.update(headers)
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
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


def trim(s, n=200):
    return re.sub(r"\s+", " ", s or "").strip()[:n]


def content_of(r):
    try:
        j = json.loads(r["body"])
        c = j["choices"][0]["message"]
        return (c.get("content") or "") or ("[reasoning_only] " + trim(str(c.get("reasoning_content") or c.get("reasoning") or ""), 60))
    except Exception:
        return ""


def usage_of(r):
    try:
        u = json.loads(r["body"]).get("usage") or {}
        return {k: u.get(k) for k in ("prompt_tokens", "completion_tokens", "total_tokens")}
    except Exception:
        return {}


def chat(base, key, model, prompt, mt, headers=None):
    return http("POST", base + "/chat/completions", key,
                {"model": model, "messages": [{"role": "user", "content": prompt}],
                 "max_tokens": mt, "temperature": 0}, headers)


def report(tag, r):
    out = {"tag": tag, "status": r["status"], "latency_s": r["latency_s"],
           "content": trim(content_of(r)), "usage": usage_of(r),
           "body_err": "" if r["status"] == 200 else trim(r["body"], 240)}
    print(tag, "->", out["status"], "|", out["content"][:90], "|", out["usage"],
          ("| ERR: " + out["body_err"]) if out["body_err"] else "")
    return out


def report_keymeta(tag, r):
    """Persist the raw JSON body for keymeta (/key) calls (B2-128, 2026-09-26).

    report() stores only choices content, which is always empty for /key, so
    the usage/limit figures quoted in B2_04_provider_health_20260926.md had no
    JSON bytes on disk. The /key response carries key metadata only (label,
    usage, limit, rate_limit), no secret material, so the parsed body is safe
    to persist verbatim.
    """
    out = {"tag": tag, "status": r["status"], "latency_s": r["latency_s"]}
    try:
        out["body"] = json.loads(r["body"])
    except Exception:
        out["body_raw"] = trim(r["body"], 240)
    print(tag, "->", out["status"], "| keymeta captured:", "body" in out)
    return out


def main():
    env = load_env()
    res = {}

    # ---- round-1 alive lanes: pull rl headers + burn quotes ----
    with open(os.path.join(HERE, "B2_04_probe_results.json"), encoding="utf-8") as f:
        r1 = json.load(f)
    for lane in r1:
        if lane.get("verdict") == "ALIVE":
            res[lane["lane"] + "_model_used"] = lane.get("model_used")
            res[lane["lane"] + "_rl"] = {}
            for b in lane.get("burn", []):
                if b.get("rl"):
                    res[lane["lane"] + "_rl"] = b["rl"]
                    break
            res[lane["lane"] + "_quotes"] = {b["tag"]: b["content"] for b in lane.get("burn", [])}

    # ---- nvidia: chat with a model id actually in the returned list ----
    k = env["NVIDIABuild"]
    r = chat("https://integrate.api.nvidia.com/v1", k, "01-ai/yi-large",
             "Reply with the single word: ALIVE.", 40)
    res["nvidia_listed_model_diag"] = report("nvidia yi-large alive", r)
    if r["status"] == 200 and content_of(r).strip():
        burns = []
        for tag, p in BURN_PROMPTS:
            burns.append(report("nvidia burn " + tag,
                                chat("https://integrate.api.nvidia.com/v1", k,
                                     "01-ai/yi-large", p, 100)))
        res["nvidia_burn"] = burns

    # ---- gemini: native generateContent (openai-compat 404ed round 1) ----
    k = env.get("GEMINI_API_KEY") or env.get("GOOGLE_API_KEY", "")
    url = ("https://generativelanguage.googleapis.com/v1beta/models/"
           "gemini-2.5-flash:generateContent")
    r = http("POST", url, k,
             {"contents": [{"parts": [{"text": "Reply with the single word: ALIVE."}]}]},
             headers={"x-goog-api-key": k})
    res["gemini_native_diag"] = report("gemini native alive", r)
    if r["status"] == 200:
        try:
            j = json.loads(r["body"])
            txt = j["candidates"][0]["content"]["parts"][0].get("text", "")
            um = j.get("usageMetadata", {})
            print("  native content:", trim(txt, 60), "| usage:", um)
            res["gemini_native_usage_fields"] = sorted(um.keys())
        except Exception as e:
            res["gemini_native_usage_fields"] = "parse-fail " + str(e)[:80]
        burns = []
        for tag, p in BURN_PROMPTS:
            rb = http("POST", url, k,
                      {"contents": [{"parts": [{"text": p}]}],
                       "generationConfig": {"maxOutputTokens": 200, "temperature": 0}},
                      headers={"x-goog-api-key": k})
            e = report("gemini burn " + tag, rb)
            try:
                jb = json.loads(rb["body"])
                e["content"] = trim(jb["candidates"][0]["content"]["parts"][0].get("text", ""))
                e["usage"] = {kk: jb.get("usageMetadata", {}).get(kk) for kk in
                              ("promptTokenCount", "candidatesTokenCount", "totalTokenCount")}
                print("   parsed:", e["content"][:80], e["usage"])
            except Exception:
                pass
            burns.append(e)
        res["gemini_burn"] = burns

    # ---- openrouter: stealth model present in today's 458-model catalog ----
    ORH = {"HTTP-Referer": "http://127.0.0.1:8765", "X-Title": "Mag Resource Harness"}
    for idx, kk in (("1", "OPENROUTER_API_KEY"), ("2", "OPENROUTER_API_KEY_2")):
        k = env[kk]
        r = chat("https://openrouter.ai/api/v1", k, "stealth/space-bunny-alpha",
                 BURN_PROMPTS[0][1], 1500, ORH)
        e = report("openrouter-k%s stealth summarize" % idx, r)
        if r["status"] == 200 and content_of(r).strip():
            e["go"] = report("openrouter-k%s stealth go" % idx,
                             chat("https://openrouter.ai/api/v1", k,
                                  "stealth/space-bunny-alpha", BURN_PROMPTS[1][1], 1500, ORH))
            e["count"] = report("openrouter-k%s stealth count" % idx,
                                chat("https://openrouter.ai/api/v1", k,
                                     "stealth/space-bunny-alpha", BURN_PROMPTS[2][1], 1500, ORH))
        res["openrouter_key" + idx + "_stealth"] = e
        # rate-limit headers ride on every response; grab from /models call
        rm = http("GET", "https://openrouter.ai/api/v1/key", k, headers=ORH)
        res["openrouter_key" + idx + "_keymeta"] = report_keymeta("openrouter-k%s /key" % idx, rm)

    # ---- zai pro / lite: bigger budget + spacing for 429 ----
    for name, kk in (("zai-pro", "ZAI_API_KEY_Pro"), ("zai-lite", "ZAI_API_KEY_Lite")):
        k = env[kk]
        base = "https://api.z.ai/api/coding/paas/v4"
        burns = []
        alive = 0
        for tag, p in [("alive", "Reply with the single word: ALIVE.")] + BURN_PROMPTS:
            time.sleep(6)
            r = chat(base, k, "glm-4.7-flash", p, 600)
            e = report("%s %s" % (name, tag), r)
            if r["status"] == 429:
                time.sleep(15)
                r = chat(base, k, "glm-4.7-flash", p, 600)
                e = report("%s %s RETRY" % (name, tag), r)
            if r["status"] == 200 and content_of(r).strip():
                alive += 1
            burns.append(e)
        res[name] = {"alive_ok": alive, "calls": burns}

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1)
    print("WROTE " + OUT)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
