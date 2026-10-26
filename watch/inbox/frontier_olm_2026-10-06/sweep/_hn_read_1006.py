# Deep-read the new decision-model cluster threads (HN items API = JSON of item?id).
# stdout only; allowlisted host; redirects blocked.
import json, sys, time, re, html as htmllib, urllib.request, urllib.parse

ALLOWED_HOST = "hn.algolia.com"

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

OPENER = urllib.request.build_opener(NoRedirect)

def get(oid):
    url = "https://" + ALLOWED_HOST + "/api/v1/items/" + oid
    parts = urllib.parse.urlsplit(url)
    assert parts.scheme == "https" and parts.hostname == ALLOWED_HOST
    req = urllib.request.Request(url, headers={"User-Agent": "mag-frontier-sweep/2026-10-06"})
    for a in range(3):
        try:
            with OPENER.open(req, timeout=40) as r:
                return json.loads(r.read().decode("utf-8", "replace"))
        except Exception as e:
            if a == 2:
                raise
            time.sleep(2 * (a + 1))

def strip(s):
    s = htmllib.unescape(s or "")
    s = re.sub(r"<p>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    return s.strip()

def walk(n, depth, out, budget):
    if not isinstance(n, dict) or budget[0] <= 0:
        return
    a = n.get("author") or "?"
    tx = strip(n.get("text"))
    if tx:
        out.append("%s> @%s: %s" % ("  " * depth, a, tx.replace("\n", " ")[:600]))
        budget[0] -= len(tx)
    for c in n.get("children") or []:
        walk(c, depth + 1, out, budget)

THREADS = sys.argv[1:]
for oid in THREADS:
    d = get(oid)
    print("=" * 100)
    print("ITEM %s | pts=%s | %s | url=%s" % (oid, d.get("points"), d.get("title"), d.get("url")))
    st = strip(d.get("text"))
    if st:
        print("STORY TEXT: %s" % st[:2600])
    out, budget = [], [14000]
    walk(d, 0, out, budget)
    for line in out[:80]:
        print(line)
    print("[comments shown: %d, budget left: %d]" % (min(len(out), 80), budget[0]))
    time.sleep(0.8)
