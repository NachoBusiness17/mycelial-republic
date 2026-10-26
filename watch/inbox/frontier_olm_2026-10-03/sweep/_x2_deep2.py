# pass 2b: four more candidates end to end
# runs: .venv/Scripts/python.exe watch/inbox/frontier_olm_2026-10-03/sweep/_x2_deep2.py
import urllib.request, urllib.parse, xml.etree.ElementTree as ET

NS = {"a": "http://www.w3.org/2005/Atom"}
BASE = "https://export.arxiv.org/api/query"

IDS = [
    "2609.19526",  # self improvement via fast tree-search
    "2609.30849",  # self-consistency assessment via perturbation strength
    "2609.30290",  # auditing and repairing LLM-as-judge failures in production
    "2609.31857",  # LLM judge validation under sparse overlap
    "2609.23264",  # judging a review by its cover
]

url = BASE + "?" + urllib.parse.urlencode({"id_list": ",".join(IDS), "max_results": len(IDS)})
with urllib.request.urlopen(url, timeout=90) as r:
    data = r.read()

root = ET.fromstring(data)
for e in root.findall("a:entry", NS):
    eid = e.find("a:id", NS).text.rsplit("/", 1)[-1]
    ti = " ".join(e.find("a:title", NS).text.split())
    pub = e.find("a:published", NS).text[:10]
    upd = e.find("a:updated", NS).text[:10]
    summ = " ".join(e.find("a:summary", NS).text.split())
    c = e.find("{http://arxiv.org/schemas/atom}comment")
    comm = " ".join(c.text.split()) if c is not None and c.text else "(no comment field)"
    authors = [a.find("a:name", NS).text for a in e.findall("a:author", NS)]
    print("=" * 100)
    print(f"ID: {eid} | pub {pub} | upd {upd} | n_authors {len(authors)}")
    print(f"TITLE: {ti}")
    print(f"COMMENT: {comm}")
    print(f"AUTHORS: {', '.join(authors[:6])}{' et al' if len(authors) > 6 else ''}")
    print(f"ABSTRACT ({len(summ)} chars): {summ}")
