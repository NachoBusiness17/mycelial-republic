"""arXiv broad sweep, swarm-orchestration area, second same-day pass (2026-10-03).
Window: submittedDate 2026-09-03..2026-10-04. Prints title | id | date | 300-char abstract.
Dedupes against the day's already-banked IDs so re-confirmation is visible, not silent.
"""
import urllib.request, urllib.parse, xml.etree.ElementTree as ET, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
NS = {"a": "http://www.w3.org/2005/Atom"}
WINDOW = "submittedDate:[202609030000 TO 202610042359]"
BANKED = {  # already confirmed in today's register / prior same-day sweep; re-hits get flagged
    "2609.38482": "PANDA", "2609.33768": "DEALS", "2609.38761": "WhereDoMASFail",
    "2610.00905": "OS-MAS-Issues", "2610.01160": "Retire", "2609.32802": "ReDerivability",
    "2609.29015": "MeshHeal", "2609.35381": "MCP-Errors", "2609.35732": "FailureTransparent",
    "2609.20889": "Proxifield", "2609.33914": "A2A-CaseVerify", "2609.27538": "Backstitch",
    "2610.00954": "SLM-Judge-Ensembles", "2609.14864": "GGUF-Throughput", "2609.04098": "GatedDeltaNet",
    "2610.02199": "TACO",
}
QUERIES = {
    "q1_fault_mesh": 'all:"multi-agent" AND (all:"fault-tolerant" OR all:"fault tolerance" OR all:"self-healing")',
    "q2_queue_sched": '(all:"LLM" OR all:"language model") AND (all:"load balancing" OR all:"job scheduling" OR all:"queueing") AND all:agent',
    "q3_retry_limit": 'all:agent AND (all:"rate limit" OR all:"backoff" OR all:"retry" OR all:"throttling")',
    "q4_collective_fail": '(all:"multi-agent" OR all:"multiagent") AND (all:"failure attribution" OR all:"failure diagnosis" OR all:"collective failure")',
    "q5_consensus_flock": '(all:"multi-agent" OR all:"multiagent") AND (all:"debate" OR all:"consensus" OR all:"agreement") AND (all:"diversity" OR all:"self-consistency" OR all:"reliability")',
    "q6_swarm_decent": 'all:"swarm" AND (all:"LLM" OR all:"language model agents")',
    "q7_orchestration": 'all:"orchestration" AND all:"multi-agent" AND (all:"LLM" OR all:"large language model")',
    "q8_resume_checkpoint": '(all:"agent" OR all:"workflow") AND (all:"resumption" OR all:"checkpoint" OR all:"interruptible" OR all:"preemption") AND all:"language model"',
}
BASE = ("https://export.arxiv.org/api/query?search_query={q}+AND+" + urllib.parse.quote(WINDOW)
        + "&sortBy=submittedDate&sortOrder=descending&max_results=15")

seen = {}
for tag, q in QUERIES.items():
    url = BASE.format(q=urllib.parse.quote(q))
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            data = r.read()
    except Exception as e:
        print(f"### {tag}: FETCH FAILED {e}")
        continue
    try:
        root = ET.fromstring(data)
    except ET.ParseError as e:
        print(f"### {tag}: PARSE FAILED {e}")
        continue
    print(f"### {tag}")
    for e in root.findall("a:entry", NS):
        arxid = e.find("a:id", NS).text.rsplit("/", 1)[-1]
        title = " ".join((e.find("a:title", NS).text or "").split())
        pub = (e.find("a:published", NS).text or "")[:10]
        summ = " ".join((e.find("a:summary", NS).text or "").split())[:300]
        tag2 = BANKED.get(arxid, "")
        flag = f" [BANKED:{tag2}]" if tag2 else ""
        if arxid in seen:
            print(f"DUP {arxid} (also {tag})")
            continue
        seen[arxid] = tag
        print(f"{arxid} | {pub} | {title}{flag}\n    {summ}")
    print()
print(f"TOTAL unique candidates: {len(seen)}")
