# pass 2 deep read: fetch complete abstracts + metadata for chosen candidates
# runs: .venv/Scripts/python.exe watch/inbox/frontier_olm_2026-10-03/sweep/_x2_deep.py
import urllib.request, urllib.parse, xml.etree.ElementTree as ET

NS = {"a": "http://www.w3.org/2005/Atom", "op": "http://arxiv.org/schemas/atom"}
BASE = "https://export.arxiv.org/api/query"

IDS = [
    "2609.12002",  # multi-judge ensemble bias calibration
    "2609.06367",  # robust conformal consensus
    "2609.26550",  # JEV-as-a-Judge accept/escalate
    "2609.19101",  # reward hacking probes vs judge
    "2609.37145",  # judgment quality to downstream utility
    "2609.04665",  # harness-agnostic reward hacking immunization
    "2609.18204",  # procedural traces shift overseer decision criterion
    "2609.18005",  # calibrated instrument for inference optimizations
]

url = BASE + "?" + urllib.parse.urlencode({
    "id_list": ",".join(IDS), "max_results": len(IDS)})
with urllib.request.urlopen(url, timeout=90) as r:
    data = r.read()

root = ET.fromstring(data)
for e in root.findall("a:entry", NS):
    eid = e.find("a:id", NS).text.rsplit("/", 1)[-1]
    ti = " ".join(e.find("a:title", NS).text.split())
    pub = e.find("a:published", NS).text[:10]
    upd = e.find("a:updated", NS).text[:10]
    summ = " ".join(e.find("a:summary", NS).text.split())
    authors = [a.find("a:name", NS).text for a in e.findall("a:author", NS)]
    c = e.find("{http://arxiv.org/schemas/atom}comment")
    comm = " ".join(c.text.split()) if c is not None and c.text else "(no comment field)"
    print("=" * 100)
    print(f"ID: {eid} | pub {pub} | upd {upd} | n_authors {len(authors)}")
    print(f"TITLE: {ti}")
    print(f"COMMENT: {comm}")
    print(f"AUTHORS: {', '.join(authors[:6])}{' et al' if len(authors) > 6 else ''}")
    print(f"ABSTRACT ({len(summ)} chars): {summ}")
