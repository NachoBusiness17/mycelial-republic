"""fastsearch-probe: does HERMES_API_KEY_1 expose a search route on inference-api.nousresearch.com?

Owed probe from GO_LIST_EXECUTION_20260925.md (P2, "Still OWED (small)").
Cap: 5 HTTP probe calls total. Keys are read from .env and NEVER printed.
"""
import json
import sys
import urllib.request
import urllib.error

ENV = r"C:/Users/foste/Documents/projects/local_sovereign_agent/.env"
BASE = "https://inference-api.nousresearch.com/v1"


def load_key():
    for line in open(ENV, encoding="utf-8", errors="replace"):
        line = line.strip()
        if line.startswith("HERMES_API_KEY_1="):
            return line.split("=", 1)[1].strip()
    return None


def probe(key, method, path, body=None):
    url = BASE + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + key)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except Exception as e:  # transport death: name it, do not fake it
        return None, f"TRANSPORT-ERROR {type(e).__name__}: {e}"


def snippet(text, n=600):
    text = " ".join(text.split())
    return text[:n] + (" ...[truncated]" if len(text) > n else "")


def main():
    key = load_key()
    if not key:
        print("FAIL: HERMES_API_KEY_1 not found in .env")
        sys.exit(1)
    print(f"key: HERMES_API_KEY_1 loaded, length={len(key)}, prefix={key[:4]}***")

    budget = 5
    used = 0

    # Probe 1: models catalog — look for anything search-shaped
    used += 1
    st, body = probe(key, "GET", "/models")
    print(f"\n=== PROBE 1 GET /v1/models -> {st} ===")
    search_hits = []
    try:
        ids = [m.get("id", "") for m in json.loads(body).get("data", [])]
        print(f"models returned: {len(ids)}")
        for mid in ids:
            if any(t in mid.lower() for t in ("search", "sonar", "perplexity", "pplx")):
                search_hits.append(mid)
        print("search/sonar/perplexity-named models:", search_hits or "NONE")
        print("sample catalog:", snippet(json.dumps(ids[:20])))
    except Exception as e:
        print("parse error:", e, "| body:", snippet(body))

    # Probe 2: /v1/search
    used += 1
    st, body = probe(key, "POST", "/search", {"query": "what day is it in Perth right now"})
    print(f"\n=== PROBE 2 POST /v1/search -> {st} ===")
    print(snippet(body))

    # Probe 3: /v1/tools/search
    used += 1
    st, body = probe(key, "POST", "/tools/search", {"query": "what day is it in Perth right now"})
    print(f"\n=== PROBE 3 POST /v1/tools/search -> {st} ===")
    print(snippet(body))

    # Probe 4: chat/completions with a web_search tool declared (Perplexity-style passthrough probe)
    used += 1
    st, body = probe(key, "POST", "/chat/completions", {
        "model": "z-ai/glm-5.3-prime",
        "messages": [{"role": "user", "content": "Use your web search tool if you have one; otherwise say NO_SEARCH_TOOL."}],
        "tools": [{"type": "function", "function": {
            "name": "web_search",
            "description": "Search the web",
            "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}}],
        "max_tokens": 200,
    })
    print(f"\n=== PROBE 4 POST /v1/chat/completions + web_search tool -> {st} ===")
    print(snippet(body, 900))

    print(f"\nprobe calls used: {used}/{budget}")


if __name__ == "__main__":
    main()
