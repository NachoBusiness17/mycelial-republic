# second same-day pass, evals-and-self-improvement x door, 2026-10-03 evening
# arXiv API candidate resolution (title lookups + window sweeps)
# runs: .venv\Scripts\python.exe watch\inbox\frontier_olm_2026-10-03\sweep\_x2_sweep.py
import urllib.request, urllib.parse, xml.etree.ElementTree as ET, sys

NS = {"a": "http://www.w3.org/2005/Atom"}
BASE = "https://export.arxiv.org/api/query"

def q(search_query, maxr=15, sort="submittedDate"):
    url = BASE + "?" + urllib.parse.urlencode({
        "search_query": search_query, "start": 0, "max_results": maxr,
        "sortBy": sort, "sortOrder": "descending"})
    with urllib.request.urlopen(url, timeout=60) as r:
        data = r.read()
    root = ET.fromstring(data)
    out = []
    for e in root.findall("a:entry", NS):
        eid = e.find("a:id", NS).text.rsplit("/", 1)[-1]
        ti = " ".join(e.find("a:title", NS).text.split())
        pub = e.find("a:published", NS).text[:10]
        upd = e.find("a:updated", NS).text[:10]
        out.append((eid, pub, upd, ti))
    return out

LOOKUPS = [
    'ti:"Monitoring and Discovering Reward Hacking with Internal Representations"',
    'ti:"LLM-as-Judge on a Budget"',
    'ti:"DAREBench"',
    'ti:"Robust Conformal Consensus"',
    'ti:"Unreliable Judges"',
    'ti:"Coding Model Stack"',
]

SWEEPS = [
    ('abs:"LLM-as-a-Judge"', 40),
    ('abs:"judge" AND abs:"ensemble"', 20),
    ('abs:"reward hacking" AND abs:"probe"', 15),
    ('abs:"self-consistency" AND abs:"hallucination"', 15),
]

for s in LOOKUPS:
    try:
        rows = q(s, 3, "relevance")
        print("LOOKUP:", s)
        for r in rows:
            print("  ", r[0], "| pub", r[1], "| upd", r[2], "|", r[3][:110])
    except Exception as ex:
        print("LOOKUP FAILED:", s, "->", repr(ex))

for s, m in SWEEPS:
    try:
        rows = q(s, m)
        print("SWEEP:", s, f"(top {len(rows)})")
        for r in rows:
            if r[1] >= "2026-08-26":  # window edge + small slack
                print("  ", r[0], "| pub", r[1], "| upd", r[2], "|", r[3][:110])
    except Exception as ex:
        print("SWEEP FAILED:", s, "->", repr(ex))
