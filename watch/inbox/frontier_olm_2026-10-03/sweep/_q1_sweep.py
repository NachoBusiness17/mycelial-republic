"""Pass 1 broad sweep, quantization-and-compression via arXiv (2026-10-03, this run).
Targeted at the ask's five research questions. Prints id | date | title for candidates.
"""
import urllib.request, urllib.parse, xml.etree.ElementTree as ET, sys, io, json, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
NS = {"a": "http://www.w3.org/2005/Atom", "op": "http://a9.com/-/spec/opensearch/1.1/"}
BASE = "https://export.arxiv.org/api/query?search_query={q}&sortBy=submittedDate&sortOrder=descending&max_results={n}"

QUERIES = {
    "RQ2_agentic_retention": '(abs:quantization AND (abs:"agentic" OR abs:"tool use" OR abs:"function calling")) AND cat:cs.CL',
    "RQ2_quant_reasoning": '(abs:quantization AND abs:reasoning) AND cat:cs.CL',
    "RQ4_linear_attention": '(abs:"linear attention" AND abs:quantization)',
    "RQ4_nvfp4": 'all:NVFP4',
    "RQ4_w4a4": 'abs:"W4A4"',
    "RQ5_blank_reasoning": '(abs:quantization AND (abs:"empty" OR abs:"blank" OR abs:degenerate OR abs:"repetition")) AND cat:cs.CL',
    "RQ3_gguf": 'all:GGUF',
    "RQ1_4bit_bench": '(abs:"4-bit" AND abs:benchmark AND abs:"language model") AND cat:cs.CL',
    "RQ4_deltanet": 'all:"DeltaNet"',
}
WIN_LO, WIN_HI = "2026-09-03", "2026-10-04"
seen = {}
for tag, q in QUERIES.items():
    url = BASE.format(q=urllib.parse.quote(q), n=20)
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
        if pub >= WIN_LO:
            mark = "" if aid not in seen else " [dup]"
            seen.setdefault(aid, (title, pub, summ))
            print(f"{aid} | {pub} | {title[:110]}{mark}")
    print()
print(f"TOTAL DISTINCT IN-WINDOW CANDIDATES: {len(seen)}")
os.makedirs("_raw", exist_ok=True)
with open("_raw/q1_candidates.json", "w", encoding="utf-8") as f:
    json.dump({k: {"title": v[0], "date": v[1], "abs_snip": v[2]} for k, v in seen.items()}, f, indent=1)
