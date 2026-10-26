# HN Algolia census for finetuning-adaptation sweep 2026-10-06.
# Both endpoints per recipe: search_by_date + relevance search.
# Window: created_at_i >= 1788652800 (2026-09-06T00:00:00Z), computed locally.
# Hardened per Mimosa findings: fixed-allowlist https host, redirects blocked,
# no file writes (stdout only; receipt captured via shell redirection).
import json, time, urllib.request, urllib.parse

ALLOWED_HOST = "hn.algolia.com"
FLOOR = 1788652800  # 2026-09-06T00:00:00Z
QUERIES = [
    "fine-tuning", "finetune", "LoRA", "QLoRA", "fine-tune small model",
    "distillation small model", "decision model", "adapter fine-tuning",
    "synthetic training data", "catastrophic forgetting", "unsloth",
    "on-device fine-tuning", "edge model training", "Gemma fine-tune",
]

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

OPENER = urllib.request.build_opener(NoRedirect)

def fetch(path_and_query):
    url = "https://" + ALLOWED_HOST + path_and_query
    parts = urllib.parse.urlsplit(url)
    if parts.scheme != "https" or parts.hostname != ALLOWED_HOST:
        return {"_error": "blocked non-allowlist url"}
    req = urllib.request.Request(url, headers={"User-Agent": "mag-frontier-sweep/2026-10-06"})
    for attempt in range(3):
        try:
            with OPENER.open(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            if attempt == 2:
                return {"_error": str(e)}
            time.sleep(2 * (attempt + 1))

seen = set()
rows = []
errcount = 0
for q in QUERIES:
    for endpoint, extra in (("search_by_date", "&numericFilters=created_at_i>%d" % FLOOR), ("search", "")):
        pq = ("/api/v1/%s?query=%s&tags=story&hitsPerPage=50%s"
              % (endpoint, urllib.parse.quote(q), extra))
        data = fetch(pq)
        if "_error" in data:
            errcount += 1
            print("ERR %s %s: %s" % (endpoint, q, data["_error"]), flush=True)
            continue
        for h in data.get("hits", []):
            oid = h.get("objectID")
            if not oid or oid in seen:
                continue
            seen.add(oid)
            rows.append({
                "id": oid, "q": q, "ep": endpoint,
                "title": h.get("title") or h.get("story_title") or "",
                "pts": h.get("points") or 0, "ncom": h.get("num_comments") or 0,
                "url": h.get("url") or "", "author": h.get("author") or "",
                "created": (h.get("created_at") or "")[:10],
            })
        time.sleep(0.6)

rows = [r for r in rows if r["created"] >= "2026-09-06"]
rows.sort(key=lambda r: (r["pts"], r["ncom"]), reverse=True)
print("CENSUS ROWS: %d  QUERY_ERRORS: %d" % (len(rows), errcount))
for r in rows:
    print("%s | %s pts %d com %d | %s | %s" % (r["id"], r["created"], r["pts"], r["ncom"], r["q"], r["title"][:110]))
