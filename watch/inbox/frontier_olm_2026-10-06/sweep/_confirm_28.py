# Confirmation pass over the 28 finetuning-adaptation items banked 2026-10-05
# (watch/inbox/frontier_olm_2026-10-05/sweep/finetuning-adaptation-{hn,arxiv,reddit,x}.md).
# For each item: refetch its source, check item liveness + stored-quote fragment survival.
# Allowlisted https hosts only, redirects blocked, stdout only (no file writes).
import json, time, urllib.request, urllib.parse, re, html as htmllib

ALLOWED = {"hn.algolia.com", "export.arxiv.org", "arxiv.org", "api.fxtwitter.com", "arctic-shift.photon-reddit.com", "www.reddit.com"}

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

OPENER = urllib.request.build_opener(NoRedirect)

def get(url, timeout=40):
    parts = urllib.parse.urlsplit(url)
    if parts.scheme != "https" or parts.hostname not in ALLOWED:
        return None, "blocked non-allowlist host %s" % parts.hostname
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) mag-frontier-sweep"})
    try:
        with OPENER.open(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="replace"), None
    except Exception as e:
        return None, str(e)

def norm(s):
    s = htmllib.unescape(s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace("\\n", " ").replace("\\\"", '"')
    s = re.sub(r"[^a-z0-9%., ]+", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()

def check(name, url, fragments, kind="html"):
    body, err = get(url)
    if body is None:
        print("%-28s UNREACHABLE %s (%s)" % (name, url[:70], err))
        return
    if kind == "json":
        try:
            body = json.dumps(json.loads(body), ensure_ascii=False)
        except Exception:
            pass
    nb = norm(body)
    live = "ITEM-LIVE"
    frags = []
    for f in fragments:
        ok = norm(f) in nb
        frags.append(("QUOTE-OK " if ok else "QUOTE-GONE") + " [" + f[:48] + "]")
    print("%-28s %s %s" % (name, live, " | ".join(frags)))

# ---------------- HN items (items API = JSON of thread) ----------------
hn_items = [
    ("HN1 duane.sh RAG finetune", "49897103", ["71% less cost", "every system appears in every position equally"]),
    ("HN2 FrogNano", "49627340", ["frontier of learnability"]),
    ("HN3 EasyCommand dirac.run", "49966238", ["evaluating the actual quantized file", "independent holdout"]),
    ("HN4 Shrewd", "49807276", ["repeated LLM classification calls", "statistical bound on held-out rows"]),
    ("HN5 Clef", "49923692", ["BERT based decision model", "vastly cheaper decision model"]),
    ("HN6 Cactus Needle 3", "49748553", ["360B tokens of structured data", "anti use case clearly", "at least as important as the modeling"]),
    ("HN7 Ask HN worth it", "49807413", ["decent sample size of data", "almost never worth it"]),
    ("HN8 RPi Needle 14MB", "49826663", ["turns plain English into local actions"]),
]
for name, oid, frags in hn_items:
    body, err = get("https://hn.algolia.com/api/v1/items/" + oid)
    if body is None:
        print("%-28s UNREACHABLE (%s)" % (name, err)); continue
    try:
        d = json.loads(body)
        title = d.get("title", "?"); pts = d.get("points"); nb = norm(json.dumps(d, ensure_ascii=False))
        fr = " | ".join(("QUOTE-OK[" + f[:40] + "]" if norm(f) in nb else "QUOTE-GONE[" + f[:40] + "]") for f in frags)
        print("%-28s ITEM-LIVE pts=%s %s | %s" % (name, pts, title[:60], fr))
    except Exception as e:
        print("%-28s PARSE-FAIL %s" % (name, e))
    time.sleep(0.7)

# duane.sh blog itself (story source page)
check("HN1-src duane.sh blog", "https://duane.sh/blog/2026/09/29/fine-tuning-qwen-for-rag/", ["71% less cost"])

# ---------------- arxiv items (export API, one batched call) ----------------
ids = "2609.17848,2610.02142,2609.10750,2609.23916,2609.24115,2609.35259,2609.19513,2502.06659"
body, err = get("https://export.arxiv.org/api/query?id_list=" + ids + "&max_results=20")
if body is None:
    print("ARXIV BATCH UNREACHABLE (%s)" % err)
else:
    nb = norm(body)
    titles = re.findall(r"<title>(.*?)</title>", body, re.S)
    print("ARXIV BATCH LIVE titles=%d" % (len(titles) - 1))
    arx = [
        ("AX1 2609.17848 SFT-vs-RL tools", "preserves pretrained agentic behavior"),
        ("AX2 2610.02142 fail-open ladder", "minutes of CPU time"),
        ("AX3 2609.10750 synthetic hurts", "causes catastrophic forgetting"),
        ("AX4 2609.23916 time-incremental", "stays within 0.01 of the base"),
        ("AX5 2609.24115 EDGEGEN", "requires no human annotation"),
        ("AX6 2609.35259 distill dynamics", "rollouts are inherently preferable"),
        ("AX7 2609.19513 QVAC III", "ARC-E"),
        ("AX8 2502.06659 who taught you", "reliable teacher inference"),
    ]
    for name, frag in arx:
        # arxiv API returns all abstracts in one doc; a fragment may live in any entry,
        # so match against the whole batch then locate which entry carries the id
        ok = norm(frag) in nb
        idprefix = name.split()[1]
        idok = idprefix in body
        print("%-30s %s %s %s" % (name, "ID-LIVE" if idok else "ID-MISSING", "QUOTE-OK" if ok else "QUOTE-ABSENT-IN-BATCH", frag[:44]))

# ---------------- X items (fxtwitter) ----------------
x_items = [
    ("X1 omarsar0 harness coevolution", "omarsar0", "2097958286146605446", ["dropped on all seven tasks", "adopts the expert's planning strategy"]),
    ("X2 zafstojano recursive synth", "zafstojano", "2097689256961466486", ["Recursive Synthetic"]),
    ("X3 ArtificialAnlys II40", "ArtificialAnlys", "2098148674203488422", ["552B parameters"]),
    ("X4 Sumanth HarnessDev", "Sumanth_077", "2098053941800100294", ["34 of 64 harness changes"]),
    ("X5 shikibmehri data lever", "shikibmehri", "2098233059242099175", ["army of agents"]),
    ("X6 ValsAI config", "ValsAI", "2098125177116848591", ["384 max output tokens"]),
]
for name, user, sid, frags in x_items:
    body, err = get("https://api.fxtwitter.com/%s/status/%s" % (user, sid))
    if body is None:
        print("%-28s UNREACHABLE (%s)" % (name, err)); continue
    try:
        d = json.loads(body)
        text = ((d.get("tweet") or {}).get("text")) or ""
        article = ((d.get("tweet") or {}).get("article")) or {}
        atext = article.get("text") or ""
        blob = norm(text + " " + atext)
        fr = " | ".join(("QUOTE-OK[" + f[:40] + "]" if norm(f) in blob else "QUOTE-GONE[" + f[:40] + "]") for f in frags)
        print("%-28s ITEM-LIVE len=%d %s" % (name, len(text) + len(atext), fr))
    except Exception as e:
        print("%-28s PARSE-FAIL %s" % (name, e))
    time.sleep(0.7)

# ---------------- reddit items (Arctic Shift) ----------------
rids = ["1wc6tka", "1wdp9qc", "1r6gx75", "1wu6cbl", "1wdasar", "1wlhh08"]
body, err = get("https://arctic-shift.photon-reddit.com/api/posts/ids?ids=" + ",".join(rids))
if body is None:
    print("REDDIT ARCTIC-SHIFT UNREACHABLE (%s)" % err)
else:
    try:
        d = json.loads(body)
        rows = d.get("data") if isinstance(d, dict) else d
        if isinstance(rows, dict):
            rows = rows.get("data", [])
        got = {}
        for p in rows or []:
            got[p.get("id")] = p.get("title", "")
        for rid in rids:
            print("RD %-12s %s %s" % (rid, "LIVE" if rid in got else "MISSING", got.get(rid, "")[:70]))
    except Exception as e:
        print("REDDIT ARCTIC-SHIFT PARSE-FAIL %s" % e)
