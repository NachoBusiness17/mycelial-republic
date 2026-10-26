"""Deep-read arXiv abstracts verbatim for the evals-and-self-improvement sweep (2026-10-03)."""
import urllib.request, xml.etree.ElementTree as ET, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
NS = {"a": "http://www.w3.org/2005/Atom", "ar": "http://arxiv.org/schemas/atom"}
IDS = ["2609.34198", "2609.33955", "2609.35815", "2610.01073", "2609.31937", "2609.34017"]

url = "https://export.arxiv.org/api/query?id_list=" + ",".join(IDS) + "&max_results=10"
with urllib.request.urlopen(url, timeout=90) as r:
    data = r.read()
root = ET.fromstring(data)
for e in root.findall("a:entry", NS):
    arxid = e.find("a:id", NS).text.rsplit("/", 1)[-1]
    title = " ".join(e.find("a:title", NS).text.split())
    pub = e.find("a:published", NS).text[:10]
    upd = e.find("a:updated", NS).text[:10]
    summ = " ".join(e.find("a:summary", NS).text.split())
    authors = [a.find("a:name", NS).text for a in e.findall("a:author", NS)]
    comment = e.find("ar:comment", NS)
    print("=" * 100)
    print(f"ID: {arxid} | published {pub} | updated {upd}")
    print(f"TITLE: {title}")
    print(f"AUTHORS: {', '.join(authors)}")
    if comment is not None:
        print(f"COMMENT: {comment.text}")
    print(f"ABSTRACT: {summ}")
    print()
