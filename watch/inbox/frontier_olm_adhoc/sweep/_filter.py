"""Filter the 30-day census to quant/compression-relevant candidates, ranked by score."""
import json, re, datetime

rows = json.load(open(r"C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/frontier_olm_adhoc/sweep/_census.json", encoding="utf-8"))

PAT = re.compile(
    r"(quant|gguf|imatrix|importance matrix|awq|gptq|exl2|fp4|nvfp4|mxfp4|fp8|int8|int4|"
    r"\bq[234568]_|\biq[1-6]\b|\bq[234568]\b|k-quants|kv ?cache|vram|bits per weight|bpw|"
    r"1\.58|bitnet|compression|compress|llama-?cpp|ggml|sub-4|low ?bit|w4a16|w8a8|"
    r"structured output|json schema|tool call|function call|temperature)",
    re.I,
)

def relevance(p):
    t = (p.get("title") or "") + " " + (p.get("selftext") or "")
    hits = len(PAT.findall(t))
    strong = len(re.findall(r"quant|gguf|imatrix|q[234568]_|iq[1-6]|awq|gptq|exl2|fp4|mxfp4|bitnet|bpw", (p.get("title") or "") + " " + (p.get("selftext") or ""), re.I))
    return hits, strong

cands = []
for p in rows:
    hits, strong = relevance(p)
    if strong >= 1 or hits >= 3:
        dt = datetime.datetime.utcfromtimestamp(p["created_utc"]).strftime("%Y-%m-%d")
        cands.append({
            "score": p.get("score") or 0, "comments": p.get("num_comments") or 0,
            "date": dt, "sub": p.get("subreddit"), "title": p["title"],
            "permalink": p.get("permalink"), "strong": strong, "hits": hits,
            "selftext_len": len(p.get("selftext") or ""),
            "id": p["id"],
        })

cands.sort(key=lambda c: (-c["strong"], -c["score"]))
print("CENSUS_WINDOW rows:", len(rows), "quant-relevant candidates:", len(cands))
for c in cands[:45]:
    print(f'{c["strong"]}s{c["score"]} c{c["comments"]} {c["date"]} r/{c["sub"]} :: {c["title"][:110]}')
    print(f'    https://www.reddit.com{c["permalink"]}  [selftext {c["selftext_len"]} ch]')
