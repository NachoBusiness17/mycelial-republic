"""Pass-1 sweep helper: HN Algolia API queries for finetuning-adaptation door.

Fallback after two WebFetch timeouts (2026-10-05). Same endpoints the recipe names,
fetched with stdlib urllib. Prints candidate stories with metadata.
"""
import json
import sys
import time
import urllib.parse
import urllib.request

CUTOFF = 1788220800  # 2026-09-05T00:00:00Z = 30 days before 2026-10-05

QUERIES = [
    "LoRA", "fine-tuning", "finetuning", "tool calling", "function calling",
    "agentic training", "SFT", "GRPO", "eval harness", "distillation",
    "reasoning traces", "synthetic data", "SmolLM", "small model agent",
    "open weights license", "weight distillation", "benchmark regression",
    "model merging", "PEFT", "instruction tuning",
]

def fetch(url, retries=3):
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "mag-sweep-finetuning/1.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 * (i + 1))
    print(f"FETCH-FAIL {url}: {last}", file=sys.stderr)
    return None

seen = {}
for q in QUERIES:
    qs = urllib.parse.quote(q)
    for endpoint in ("search_by_date", "search"):
        url = (f"https://hn.algolia.com/api/v1/{endpoint}?query={qs}"
               f"&tags=story&hitsPerPage=15&numericFilters=created_at_i%3E{CUTOFF}")
        data = fetch(url)
        if not data:
            continue
        for h in data.get("hits", []):
            oid = h.get("objectID")
            if oid and oid not in seen:
                seen[oid] = {
                    "q": q,
                    "endpoint": endpoint,
                    "title": h.get("title"),
                    "url": h.get("url"),
                    "points": h.get("points"),
                    "num_comments": h.get("num_comments"),
                    "created_at": h.get("created_at"),
                    "objectID": oid,
                }
    time.sleep(0.4)

rows = sorted(seen.values(), key=lambda r: (r["points"] or 0), reverse=True)
for r in rows:
    print(f"{r['points']}\t{r['num_comments']}\t{r['created_at']}\t{r['objectID']}\t{r['endpoint']}\t{r['q']}\t{r['title']}\t{r['url']}")
print(f"TOTAL_CANDIDATES\t{len(rows)}", file=sys.stderr)
