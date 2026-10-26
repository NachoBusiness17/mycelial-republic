"""Pass 1 batch 2 (2026-10-03): RQ5 empty-reasoning x quantization, and the latest
2610.* (post-10-01) quantization submissions."""
import urllib.request, urllib.parse, xml.etree.ElementTree as ET, sys, io, json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
NS = {"a": "http://www.w3.org/2005/Atom"}
BASE = "https://export.arxiv.org/api/query?search_query={q}&sortBy=submittedDate&sortOrder=descending&max_results={n}"
QUERIES = {
    "RQ5_think_quant": '(abs:quantization AND abs:"chain-of-thought") AND cat:cs.CL',
    "RQ5_think_quant2": '(abs:quantized AND abs:"reasoning model")',
    "RQ5_slm_reasoning": '(abs:quantization AND abs:"small language model")',
    "LATEST_all_quant": 'abs:quantization AND (cat:cs.CL OR cat:cs.LG)',
    "RQ1_quant_agentbench": '(abs:quantization AND abs:"agent benchmark")',
    "RQ5_empty_response": '(abs:quantization AND (abs:"failure mode" OR abs:"error analysis")) AND cat:cs.CL',
}
seen = {}
for tag, q in QUERIES.items():
    url = BASE.format(q=urllib.parse.quote(q), n=25)
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            data = r.read()
    except Exception as e:
        print(f"### {tag}: FETCH FAILED {e}")
        continue
    root = ET.fromstring(data)
    entries = root.findall("a:entry", NS)
    print(f"### {tag}: {len(entries)} entries")
    for e in entries:
        aid = e.find("a:id", NS).text.split("/abs/")[-1]
        title = " ".join(e.find("a:title", NS).text.split())
        pub = e.find("a:published", NS).text[:10]
        summ = " ".join(e.find("a:summary", NS).text.split())[:220]
        if pub >= "2026-09-03":
            mark = "" if aid not in seen else " [dup]"
            seen.setdefault(aid, (title, pub, summ))
            print(f"{aid} | {pub} | {title[:110]}{mark}")
    print()
print(f"TOTAL DISTINCT IN-WINDOW (batch2 union incl prior): {len(seen)}")
with open("_raw/q2_candidates.json", "w", encoding="utf-8") as f:
    json.dump({k: {"title": v[0], "date": v[1], "abs_snip": v[2]} for k, v in seen.items()}, f, indent=1)
