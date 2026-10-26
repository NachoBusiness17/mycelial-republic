# sw-14 source fetcher round 2: full Wikipedia plain text + PubMed batch abstracts. Read-only GETs.
import html as htmllib
import io
import re
import sys

import requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
UA = {"User-Agent": "sw-14-research/1.0 (local research harness)"}


def plain(url, cap=5200):
    r = requests.get(url, headers=UA, timeout=40)
    print("====", url, "status", r.status_code)
    t = r.text
    t = re.sub(r"(?s)<(script|style).*?</\1>", " ", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = htmllib.unescape(t)
    t = re.sub(r"\s+", " ", t)
    print(t[:cap])
    print("----")


plain("https://en.wikipedia.org/wiki/Water_integrator")
plain("https://en.wikipedia.org/wiki/Fluidics")

r = requests.get(
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi",
    params={"db": "pubmed", "id": "17289994,19256943,34040102,31794181", "rettype": "abstract", "retmode": "text"},
    headers=UA,
    timeout=40,
)
print("==== PUBMED BATCH")
print(r.text[:4200])
