"""Pass 2 deep-read fetcher (2026-10-03): pull full HTML (or abs fallback) for the
shortlist. Saves to _raw/q_<id>.<ext>; prints which door served each."""
import urllib.request, sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
IDS = ["2609.39801", "2609.04098", "2609.38169", "2609.38166",
       "2609.37887", "2609.23587", "2609.19441", "2609.28007"]
HDRS = {"User-Agent": "Mozilla/5.0 (research sweep; contact: estate-local)"}
for aid in IDS:
    got = None
    for ext, url in [
        ("html", f"https://arxiv.org/html/{aid}v1"),
        ("html", f"https://arxiv.org/html/{aid}"),
        ("abs", f"https://arxiv.org/abs/{aid}"),
    ]:
        try:
            req = urllib.request.Request(url, headers=HDRS)
            with urllib.request.urlopen(req, timeout=60) as r:
                body = r.read()
                if r.status == 200 and len(body) > 2000:
                    got = (ext, url, body)
                    break
        except Exception as e:
            print(f"{aid} miss {url}: {e}")
            continue
    if not got:
        print(f"{aid} FETCH FAILED all doors")
        continue
    ext, url, body = got
    path = f"_raw/q_{aid}.{ext}"
    with open(path, "wb") as f:
        f.write(body)
    print(f"{aid} OK {ext} {len(body)} bytes from {url} -> {path}")
