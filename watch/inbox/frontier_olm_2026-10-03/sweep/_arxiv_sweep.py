"""arXiv bulk candidate sweep for evals-and-self-improvement area (2026-10-03).
Fetches recent submissions per research question, prints title | id | date | first 300 chars of abstract.
"""
import urllib.request, urllib.parse, xml.etree.ElementTree as ET, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

NS = {"a": "http://www.w3.org/2005/Atom"}
QUERIES = {
    "RQ1_judge_reliability": 'all:"LLM-as-a-judge" AND all:reliability',
    "RQ1_judge_calibration": 'all:"LLM judge" AND all:calibration',
    "RQ1_judge_agents": 'all:"LLM-as-judge" AND all:agent',
    "RQ2_self_improvement": 'all:"self-improving" AND all:agent',
    "RQ2_self_improve_loop": 'all:"self-improvement" AND all:evaluation',
    "RQ3_significance": 'all:"statistical significance" AND all:"language model"',
    "RQ3_prereg": 'all:"pre-registered" AND all:evaluation AND all:LLM',
    "RQ4_agent_failure": 'all:agent AND all:"failure analysis" AND all:benchmark',
    "RQ4_failure_attribution": 'all:"failure attribution" AND all:agent',
}
BASE = "https://export.arxiv.org/api/query?search_query={q}&sortBy=submittedDate&sortOrder=descending&max_results=12"

seen = {}
for tag, q in QUERIES.items():
    url = BASE.format(q=urllib.parse.quote(q))
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            data = r.read()
    except Exception as e:
        print(f"### {tag}: FETCH FAILED {e}")
        continue
    root = ET.fromstring(data)
    print(f"### {tag}")
    for e in root.findall("a:entry", NS):
        arxid = e.find("a:id", NS).text.rsplit("/", 1)[-1]
        title = " ".join(e.find("a:title", NS).text.split())
        pub = e.find("a:published", NS).text[:10]
        summ = " ".join(e.find("a:summary", NS).text.split())[:300]
        if arxid in seen:
            print(f"DUP {arxid} ({tag})")
            continue
        seen[arxid] = tag
        print(f"{arxid} | {pub} | {title}\n    {summ}")
    print()
