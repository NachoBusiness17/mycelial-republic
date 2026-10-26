# sw-14 source fetcher: PubMed esearch/efetch + Crossref. Read-only network GETs, no subprocess.
import io
import sys
import time
import xml.etree.ElementTree as ET

import requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

UA = {"User-Agent": "sw-14-research/1.0 (local research harness)"}


def pm_search_title(title):
    r = requests.get(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
        params={"db": "pubmed", "term": title, "retmode": "json"},
        headers=UA,
        timeout=30,
    )
    ids = r.json()["esearchresult"]["idlist"]
    print("PM_SEARCH", title, "->", ids)
    return ids


def pm_fetch(pmid):
    r = requests.get(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi",
        params={"db": "pubmed", "id": pmid, "rettype": "abstract", "retmode": "text"},
        headers=UA,
        timeout=30,
    )
    print("PM_ABSTRACT", pmid)
    print(r.text[:1800])
    print("----")


def crossref(query, rows=4):
    r = requests.get(
        "https://api.crossref.org/works",
        params={"query.bibliographic": query, "rows": rows},
        headers=UA,
        timeout=30,
    )
    print("CROSSREF", query, "status", r.status_code)
    if r.status_code != 200:
        print(r.text[:300])
        return
    for it in r.json()["message"]["items"]:
        title = (it.get("title") or ["?"])[0]
        year = None
        for k in ("published-print", "published-online", "issued"):
            if it.get(k, {}).get("date-parts"):
                year = it[k]["date-parts"][0][0]
                break
        cont = (it.get("container-title") or ["?"])[0]
        print("  *", year, "|", cont, "|", title, "| doi:", it.get("DOI"))
        if it.get("abstract"):
            txt = it["abstract"].replace("\n", " ")
            print("    abs:", txt[:600])
    print("----")


# 1. The MIT bubble logic paper (Prakash & Gershenfeld, Science 2007)
pmids = pm_search_title("Microfluidic Bubble Logic")
if pmids:
    time.sleep(1)
    pm_fetch(pmids[0])

# 2. Reservoir computing with water: the bucket paper
crossref("Pattern recognition in a bucket Fernando Sojakka")

# 3. Modern embedded fluidic logic in soft robots
crossref("fluidic logic soft robot autonomous embedded")
crossref("pneumatic digital logic elastomer microfluidic gates")

# 4. Fluidic amplifiers / fluidics state of field reviews
crossref("fluidic logic review fluid amplifier")
