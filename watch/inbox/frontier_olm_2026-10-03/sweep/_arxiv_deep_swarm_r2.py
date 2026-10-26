"""Pass-2 deep-read fetcher, swarm-orchestration second pass (2026-10-03).
Fetches full HTML from arxiv.org/html/<id>v1 for each shortlisted paper, strips tags to
flattened text, saves to _raw/<id>_fulltext.txt, prints byte count. Reading happens after,
via grep/Read on the flattened text.
"""
import urllib.request, re, sys, io, time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
IDS = ["2610.00349", "2609.04749", "2609.34701", "2609.25959", "2609.35875", "2609.34215", "2609.10964"]

TAG_RE = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.S | re.I)
ANYTAG = re.compile(r"<[^>]+>")
for arxid in IDS:
    url = f"https://arxiv.org/html/{arxid}v1"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research sweep)"})
        with urllib.request.urlopen(req, timeout=90) as r:
            html = r.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"{arxid}: FETCH FAILED {e}")
        continue
    body = TAG_RE.sub(" ", html)
    body = ANYTAG.sub(" ", body)
    body = re.sub(r"[ \t]+", " ", body)
    body = re.sub(r"\n\s*\n+", "\n", body)
    out = f"watch/inbox/frontier_olm_2026-10-03/sweep/_raw/{arxid}_fulltext.txt"
    with open(out, "w", encoding="utf-8") as f:
        f.write(body)
    print(f"{arxid}: {len(html)} bytes html -> {len(body)} chars text -> {out}")
    time.sleep(2)
