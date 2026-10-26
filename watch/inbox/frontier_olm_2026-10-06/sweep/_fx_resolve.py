"""Resolve the 8 in-window X candidates through the fxtwitter door."""
import json
import re
import urllib.request
import urllib.error
import urllib.parse

ALLOWED = {"api.fxtwitter.com"}
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


class G(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if urllib.parse.urlsplit(newurl).hostname.lower() not in ALLOWED:
            raise urllib.error.URLError(f"redirect blocked: {newurl}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


OP = urllib.request.build_opener(G)


def fetch(url, timeout=40):
    scheme, host = urllib.parse.urlsplit(url)[:2]
    if scheme != "https" or host.lower() not in ALLOWED:
        raise urllib.error.URLError(f"blocked: {url}")
    req = urllib.request.Request(url, headers=UA)
    return OP.open(req, timeout=timeout).read().decode("utf-8", errors="replace")


CANDS = [
    ("TeksEdge", "2103001487240487265", "Macaron LoRAs"),
    ("sairahul1", "2100882424343265527", "fine-tune guide"),
    ("sairahul1", "2101250446329364542", "200-500 examples beat frontier"),
    ("JulianGoldieSEO", "2105305354787803178", "Julia 1 article"),
    ("sairahul1", "2101369479838253235", "Dario Amodei thread"),
    ("fastinoAI", "2099888422139900052", "American Open Weight status"),
    ("v_shakthi", "2095339203781640399", "orchestration"),
    ("dair_ai", "2099168306863190147", "papers of the week"),
]

for user, sid, label in CANDS:
    url = f"https://api.fxtwitter.com/{user}/status/{sid}"
    try:
        data = json.loads(fetch(url))
        t = data.get("tweet", {})
        text = (t.get("text") or "").replace("\n", " ")[:300]
        likes = t.get("likes", 0)
        created = t.get("created_at", "?")
        print(f"OK | {user}/{sid} | {label} | {created} | likes={likes}\n    text: {text}")
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code} | {user}/{sid} | {label}")
    except Exception as e:
        print(f"ERR {type(e).__name__} | {user}/{sid} | {label} | {e}")
