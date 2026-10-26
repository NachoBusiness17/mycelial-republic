# evals-self-improvement sweep + confirm pass, 2026-10-06.
# (a) confirm the day-5 evals-self-improvement items (frontier_olm_2026-10-05/sweep/
#     evals-self-improvement-{hn,arxiv,x,reddit}.md): refetch sources, check item
#     liveness + stored-quote fragment survival.
# (b) fresh HN pass 1: Algolia queries, last 30 days, 30+ candidates.
# (c) RQ3 instruments: usage.jsonl day histogram, duels.jsonl judge histogram.
# Allowlisted https hosts only; no file writes outside this directory; stdout only.
import json, time, urllib.request, urllib.parse, re, html as htmllib
from collections import Counter

ALLOWED = {"hn.algolia.com", "export.arxiv.org", "arxiv.org", "arctic-shift.photon-reddit.com", "api.fxtwitter.com"}
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) mag-frontier-sweep-1006"}

def get(url, timeout=40):
    parts = urllib.parse.urlsplit(url)
    if parts.scheme != "https" or (parts.hostname or "") not in ALLOWED:
        return None, "blocked non-allowlist host %s" % parts.hostname
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="replace"), None
    except Exception as e:
        return None, str(e)

def norm(s):
    s = htmllib.unescape(s or "")
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.lower()

def frag_ok(haystack, frag):
    f = norm(frag)
    f = re.sub(r"[^a-z0-9%. ]+", " ", f)
    f = re.sub(r"\s+", " ", f).strip()
    words = f.split()
    if not words:
        return None
    # try full, then first-6-words, then last-6-words as fallbacks
    for cand in (f, " ".join(words[:6]), " ".join(words[-6:])):
        if cand and cand in haystack:
            return cand
    return None

print("== (c) RQ3 instruments ==")
# usage.jsonl day histogram + last ts
days = Counter(); last_ts = ""; n = 0; after_0928 = 0
with open(r"C:\Users\foste\Documents\projects\local_sovereign_agent\memory\runs\hermes_burn\usage.jsonl", encoding="utf-8", errors="replace") as fh:
    for line in fh:
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except Exception:
            continue
        n += 1
        ts = str(row.get("ts", ""))
        if ts > last_ts:
            last_ts = ts
        d = ts[:10]
        days[d] += 1
        if d >= "2026-09-29":
            after_0928 += 1
print("usage.jsonl rows=%d last_ts=%s rows_dated_2026-09-29_or_later=%d" % (n, last_ts, after_0928))
print("usage.jsonl by day (last 12):", sorted(days.items())[-12:])

# duels.jsonl judge histogram
jd = Counter(); dj = Counter(); last_duel = ""
with open(r"C:\Users\foste\Documents\projects\local_sovereign_agent\logs\duel\duels.jsonl", encoding="utf-8", errors="replace") as fh:
    for line in fh:
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except Exception:
            continue
        jd[str(row.get("judge", ""))] += 1
        dj[str(row.get("ts", ""))[:10]] += 1
        t = str(row.get("ts", ""))
        if t > last_duel:
            last_duel = t
print("duels.jsonl judges:", dict(jd))
print("duels.jsonl last ts:", last_duel, "days:", sorted(dj.items())[-5:])

print()
print("== (a) confirm pass: day-5 evals items ==")
# HN thread ids from the day-5 file's pass-2 list + pass-1 names
HN_IDS = {
    "49716123": ("rekursiv auto-autoresearch (NanoChat)", "Auto-autoresearch"),
    "49962903": ("claude.dev automating eval design + hillclimbing", "hillclimbing"),
    "49931859": ("deepsense top-scoring-model production eval", "deepsense"),
    "49897103": ("duane.sh fine-tuning Qwen3.5-4B", "Qwen3.5-4B"),
    "49655621": ("danluu bad benchmarks / LLM grader flips", "danluu"),
    "49796714": ("Doyouok dead-man switch", "Doyouok"),
    "49911995": ("Magnitude Launch HN", "Magnitude"),
    "49916869": ("hamel auto-evals", "hamel"),
    "49742415": ("Mozilla local-LLM-servers bench (KNOWN-HELD)", "local-llm"),
    "49910150": ("Inspect AISI", "Inspect"),
}
for hid, (label, kw) in sorted(HN_IDS.items()):
    body, err = get("https://hn.algolia.com/api/v1/items/" + hid)
    if err:
        print("HN %s %s -> ERR %s" % (hid, label, err))
        continue
    try:
        j = json.loads(body)
        print("HN %s %-52s LIVE pts=%s type=%s title=%r" % (hid, label, j.get("points"), j.get("type"), (j.get("title") or "")[:70]))
    except Exception as e:
        print("HN %s %s -> PARSE ERR %s" % (hid, label, e))
    time.sleep(0.4)

# arxiv ids: title live + stored-fragment check against returned abstract
ARX = {
    "2609.36043": ("SAGE statistical acceptance gate", "regression rate lowered"),
    "2610.02142": ("Keyword Harnesses Fail Open", "minutes of CPU time"),
    "2609.38652": ("AgBench", "hidden from the agent"),
    "2610.00025": ("Microtask eligibility gap", "eligibility"),
    "2609.07370": ("CPU reliability benchmark MCP sub-2B", "parseable JSON"),
    "2609.34924": ("Audit the Scaffold", "churn decays"),
    "2609.38812": ("self-verification detect little", "61.43"),
    "2609.36556": ("MAADBench", "refreshable"),
    "2610.02911": ("Probe the Harness", "looked consistent"),
}
ids = ",".join(ARX)
body, err = get("https://export.arxiv.org/api/query?id_list=" + ids + "&max_results=20")
if err:
    print("ARXIV BATCH ERR", err)
else:
    entries = re.findall(r"<entry>(.*?)</entry>", body, re.S)
    found = {}
    for e in entries:
        eid = re.search(r"<id>https?://arxiv.org/abs/([^<v]+)", e)
        ti = re.search(r"<title>(.*?)</title>", e, re.S)
        ab = re.search(r"<summary>(.*?)</summary>", e, re.S)
        if eid:
            found[eid.group(1).strip()] = (norm(ti.group(1) if ti else ""), norm(ab.group(1) if ab else ""))
    print("arxiv entries returned=%d" % len(found))
    for aid, (label, frag) in ARX.items():
        if aid in found:
            title, ab = found[aid]
            hit = frag_ok(ab, frag)
            print("ARX %s %-42s LIVE title=%r frag[%s]=%s" % (aid, label, title[:60], frag, "OK:" + hit[:40] if hit else "GONE"))
        else:
            print("ARX %s %-42s NOT-RETURNED" % (aid, label))

# reddit ids via arctic-shift: liveness + selftext fragment
REDDIT = {
    "1ws6bmh": ("Xyntetik width-halved 30B distill + task battery", "57 of 60 held-out closed-loop tasks"),
    "1wtzedu": ("BAAI AREX-2 27B self-improvement", "propose, measure, reflect, and revise"),
    "1waiu6b": ("Ollama Cloud grandfathered nerf", "Confirmed by my weekly Hermes analytics"),
    "1wpqbxp": ("rope_scaling silent RoPE base change", "RoPE base of 64 of 180"),
}
for rid, (label, frag) in REDDIT.items():
    body, err = get("https://arctic-shift.photon-reddit.com/api/posts/ids?ids=" + rid)
    if err:
        print("RD %s %-46s ERR %s" % (rid, label, err))
        continue
    try:
        j = json.loads(body)
        d = (j.get("data") or [{}])[0]
        st = norm(d.get("selftext") or "")
        hit = frag_ok(st, frag) if st else None
        import datetime
        ts = datetime.datetime.utcfromtimestamp(int(d.get("created_utc", 0))).strftime("%Y-%m-%d")
        print("RD %s %-46s LIVE date=%s score=%s frag=%s" % (rid, label, ts, d.get("score"), "OK:" + hit[:40] if hit else ("GONE" if st else "SELFTEXT-EMPTY")))
    except Exception as e:
        print("RD %s %s PARSE ERR %s" % (rid, label, e))
    time.sleep(0.4)

print()
print("== (b) fresh HN pass 1: last 30 days ==")
CUTOFF = 1788652800  # 2026-09-06T00:00Z
QUERIES = [
    ("search", "LLM judge evaluation"),
    ("search", "eval harness agents"),
    ("search", "SWE-bench"),
    ("search", "self-improving agent"),
    ("search", "benchmark gaming reward hacking"),
    ("search", "fine-tuning small model evals"),
    ("search_by_date", "RL fine-tuning open weights"),
    ("search_by_date", "evals"),
    ("search", "AI agent benchmark contaminated"),
]
seen = {}
for ep, q in QUERIES:
    url = ("https://hn.algolia.com/api/v1/%s?query=%s&tags=story&hitsPerPage=20&numericFilters=created_at_i>%d"
           % (ep, urllib.parse.quote(q), CUTOFF))
    body, err = get(url)
    if err:
        print("QUERY %-40r ERR %s" % (q, err))
        continue
    try:
        j = json.loads(body)
    except Exception as e:
        print("QUERY %-40r PARSE ERR %s" % (q, e))
        continue
    for h in j.get("hits", []):
        oid = h.get("objectID")
        if not oid:
            continue
        pts = h.get("points") or 0
        if oid not in seen or pts > seen[oid][1]:
            seen[oid] = (h.get("title") or h.get("story_title") or "", pts, h.get("created_at", "")[:10], q, h.get("url") or "")
    time.sleep(0.4)
print("unique candidates=%d" % len(seen))
for oid, (title, pts, d, q, u) in sorted(seen.items(), key=lambda kv: -kv[1][1]):
    print("%s pts=%-5s %s id=%s q=%r %s" % (d, pts, (title or "")[:88], oid, q, (u or "")[:70]))
