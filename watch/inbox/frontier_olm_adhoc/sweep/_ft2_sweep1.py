# Pass 1 broad sweep, HN Algolia, window 2026-09-11..2026-10-11 (created_at_i>1789084800)
# Fetches search_by_date for a fixed literal query battery against the single
# allowlisted public host hn.algolia.com (the ask's own fetch recipe).
# SSRF hardening: scheme locked to https, host locked by allowlist check before
# any request, redirects refused, no user input reaches the URL builder.
import json, time, urllib.request, urllib.parse

ALLOWED_HOSTS = {"hn.algolia.com"}
SINCE = 1789084800  # 2026-09-11T00:00:00Z, 30 days before 2026-10-11
QUERIES = [
    "fine-tuning", "finetuning", "LoRA", "QLoRA", "unsloth", "peft",
    "adapter", "test-time", "TTT", "self-improving", "GRPO", "verl", "trl",
    "distill", "GGUF", "RLHF", "on-device", "SLM", "continual", "forgetting",
    "SFT", "reward model", "Gemma", "small language model", "quantization aware",
    "train a model", "local LLM train", "fine tune",
]


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise RuntimeError("redirect refused: " + str(newurl))


def build_url(query):
    # Fixed scheme + fixed allowlisted host; only the q param varies, from the
    # literal list above. Parse result is re-validated before the request fires.
    u = urllib.parse.urlparse("https://hn.algolia.com/api/v1/search_by_date")
    if u.scheme != "https" or u.hostname not in ALLOWED_HOSTS:
        raise RuntimeError("host not allowlisted")
    qs = urllib.parse.urlencode({
        "query": query, "tags": "story",
        "numericFilters": "created_at_i>" + str(SINCE), "hitsPerPage": 30,
    })
    return urllib.parse.urlunparse(u._replace(query=qs))


def fetch(url):
    p = urllib.parse.urlparse(url)
    if p.scheme != "https" or p.hostname not in ALLOWED_HOSTS:
        raise RuntimeError("refusing non-allowlisted target: " + str(p.hostname))
    opener = urllib.request.build_opener(NoRedirect)
    req = urllib.request.Request(url, headers={"User-Agent": "mag-frontier-sweep/1.0"})
    with opener.open(req, timeout=25) as r:
        return json.loads(r.read().decode("utf-8"))


seen = {}
errors = []
for q in QUERIES:
    try:
        data = fetch(build_url(q))
        for h in data.get("hits", []):
            oid = h.get("objectID")
            if not oid:
                continue
            if oid not in seen:
                seen[oid] = {
                    "id": oid, "pts": h.get("points") or 0,
                    "date": (h.get("created_at") or "")[:10],
                    "title": h.get("title") or "", "url": h.get("url") or "",
                    "comments": h.get("num_comments") or 0,
                }
        time.sleep(0.4)
    except Exception as e:
        errors.append((q, repr(e)))

rows = sorted(seen.values(), key=lambda x: (x["date"], x["pts"]), reverse=True)
print("TOTAL_UNIQUE", len(rows), "ERRORS", len(errors))
for q, e in errors:
    print("ERR", q, e)
for r in rows:
    print("|".join([r["id"], str(r["pts"]), str(r["comments"]), r["date"], r["title"][:110], r["url"][:100]]))
