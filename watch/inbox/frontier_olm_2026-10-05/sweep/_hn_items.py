"""Pass-2 deep-read helper: dump HN story + comment text verbatim via Algolia items API."""
import html
import json
import re
import sys
import time
import urllib.request

IDS = sys.argv[1:] or ["49807413"]
TAG = re.compile(r"<[^>]+>")

def get(oid):
    url = f"https://hn.algolia.com/api/v1/items/{oid}"
    req = urllib.request.Request(url, headers={"User-Agent": "mag-sweep-finetuning/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))

def clean(t):
    if not t:
        return ""
    return html.unescape(TAG.sub(" ", t)).strip()

def walk(node, depth, out, budget):
    if budget[0] <= 0:
        return
    for c in node.get("children", []):
        if budget[0] <= 0:
            return
        txt = clean(c.get("text"))
        if txt:
            out.append(f"  [{'  ' * depth}{c.get('author')}] {txt[:900]}")
            budget[0] -= 1
        walk(c, depth + 1, out, budget)

for oid in IDS:
    try:
        d = get(oid)
    except Exception as e:  # noqa: BLE001
        print(f"=== {oid} FETCH-FAIL {e}")
        continue
    print(f"=== {oid} | {d.get('title')} | {d.get('url')} | pts={d.get('points')} | {d.get('created_at')}")
    st = clean(d.get("text") or "")
    if st:
        print(f"[STORY TEXT] {st[:1500]}")
    out, budget = [], [40]
    walk(d, 0, out, budget)
    print("\n".join(out) if out else "[no text comments]")
    print()
    time.sleep(0.5)
