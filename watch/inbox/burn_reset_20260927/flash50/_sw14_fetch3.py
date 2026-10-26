# sw-14 source fetcher round 3: MONIAC full text, Fluidics remainder, Springer bucket paper. Read-only GETs.
import html as htmllib
import io
import re
import sys

import requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
UA = {"User-Agent": "sw-14-research/1.0 (local research harness)"}


def plain(url, start=0, cap=5500, label=""):
    r = requests.get(url, headers=UA, timeout=40)
    print("====", label or url, "status", r.status_code)
    t = r.text
    t = re.sub(r"(?s)<(script|style).*?</\1>", " ", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = htmllib.unescape(t)
    t = re.sub(r"\s+", " ", t)
    print(t[start : start + cap])
    print("----")


plain("https://en.wikipedia.org/wiki/MONIAC", cap=6200, label="MONIAC")
plain("https://en.wikipedia.org/wiki/Fluidics", start=5200, cap=3600, label="FLUIDICS-TAIL")
try:
    plain("https://link.springer.com/chapter/10.1007/978-3-540-39432-7_63", cap=2200, label="BUCKET-SPRINGER")
except Exception as e:
    print("BUCKET-SPRINGER FAILED:", e)
