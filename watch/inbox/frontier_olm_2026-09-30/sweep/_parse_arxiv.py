"""Parse arXiv Atom XML (as fetched via curl from export.arxiv.org) into a flat list.

Prints: index | arxiv id | published date | updated date | title | primary category | one-line summary.
Usage: python _parse_arxiv.py <feed.xml>
"""
import re
import sys
import xml.etree.ElementTree as ET

NS = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}

path = sys.argv[1]
tree = ET.parse(path)
root = tree.getroot()
entries = root.findall("a:entry", NS)
print(f"TOTAL_ENTRIES={len(entries)}")
for i, e in enumerate(entries, 1):
    eid = (e.findtext("a:id", default="", namespaces=NS) or "").strip()
    m = re.search(r"abs/([\w.\-/]+)$", eid)
    short = m.group(1) if m else eid
    pub = (e.findtext("a:published", default="", namespaces=NS) or "")[:10]
    upd = (e.findtext("a:updated", default="", namespaces=NS) or "")[:10]
    title = re.sub(r"\s+", " ", (e.findtext("a:title", default="", namespaces=NS) or "")).strip()
    cat_el = e.find("a:category", NS)
    cat = cat_el.get("term", "") if cat_el is not None else ""
    summ = re.sub(r"\s+", " ", (e.findtext("a:summary", default="", namespaces=NS) or "")).strip()
    if len(summ) > 300:
        summ = summ[:297] + "..."
    print(f"{i} | {short} | pub={pub} | upd={upd} | cat={cat} | {title}")
    print(f"    {summ}")
