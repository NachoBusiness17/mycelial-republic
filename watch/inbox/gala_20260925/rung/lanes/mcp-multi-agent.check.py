import html, io, json, os, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))
FETCH = os.path.join(BASE, "mcp-multi-agent.fetch")
LANE = os.path.join(BASE, "mcp-multi-agent.json")
SOURCES = os.path.join(BASE, "mcp-multi-agent.sources.md")

fail = []

# 1. lane JSON parses and has required fields
d = json.load(io.open(LANE, encoding="utf-8"))
for k in ["lane", "division", "ok", "note", "rows", "checks", "decision_changed", "artifact"]:
    if k not in d:
        fail.append("missing key %s" % k)
print("lane=%s division=%s ok=%s rows=%d checks=%d" % (d.get("lane"), d.get("division"), d.get("ok"), len(d.get("rows", [])), len(d.get("checks", []))))
print("decision_changed: %s" % d.get("decision_changed"))
print("artifact: %s" % d.get("artifact"))

# 2. row field + shape checks
REQ = ["law", "claim", "quote", "source", "steal", "falsifier", "leverage"]
for i, r in enumerate(d.get("rows", [])):
    for k in REQ:
        if not r.get(k):
            fail.append("row %d missing %s" % (i, k))
    if r.get("leverage") not in ("high", "medium", "low"):
        fail.append("row %d bad leverage %r" % (i, r.get("leverage")))
    wc = len(r.get("quote", "").split())
    if wc > 40:
        fail.append("row %d quote over 40 words (%d)" % (i, wc))
    print("row %2d %-30s leverage=%-6s quote_words=%d" % (i, r.get("law"), r.get("leverage"), wc))

# 3. em-dash law: no U+2014/U+2013 in lane JSON, sources, or this script
for p in [LANE, SOURCES, os.path.abspath(__file__)]:
    t = io.open(p, encoding="utf-8").read()
    n = t.count("\u2014") + t.count("\u2013")
    print("emdash %s -> %d" % (os.path.basename(p), n))
    if n:
        fail.append("em-dash found in %s" % p)

# 4. every row quote: substring of sources.md AND of >=1 normalized raw fetch file
def norm_text(fn):
    raw = io.open(os.path.join(FETCH, fn), encoding="utf-8", errors="replace").read()
    raw = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
    txt = re.sub(r"(?s)<[^>]+>", " ", raw)
    txt = html.unescape(txt)
    txt = txt.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    txt = txt.replace("\u2014", "--").replace("\u2013", "--")
    return re.sub(r"\s+", " ", txt)

DOCS = {k: norm_text(v) for k, v in {
    "architecture": "architecture.html",
    "security": "security_best_practices.html",
    "a2a": "a2a_readme.md",
    "anthropic": "code_execution_mcp.html",
    "openai": "openai_agents_mcp.html",
    "crewai": "crewai_mcp.html",
    "langchain": "langchain_mcp.html",
    "codemode": "cf_codemode.html",
}.items()}
src = io.open(SOURCES, encoding="utf-8").read()
for i, r in enumerate(d.get("rows", [])):
    q = r.get("quote", "")
    in_src = q in src
    hits = [k for k, t in DOCS.items() if q in t]
    print("quote row %2d: sources.md=%s raw_hits=%s" % (i, in_src, ",".join(hits) or "NONE"))
    if not in_src:
        fail.append("row %d quote not in sources.md" % i)
    if not hits:
        fail.append("row %d quote not in any raw fetch file" % i)
    if r.get("source", "").split("/")[-1] not in [v for k, v in {
        "architecture.html": 1, "security_best_practices.html": 1, "a2a_readme.md": 1,
        "code_execution_mcp.html": 1, "openai_agents_mcp.html": 1, "crewai_mcp.html": 1,
        "langchain_mcp.html": 1, "cf_codemode.html": 1}.items()] and os.path.basename(r.get("source", "")) not in DOCS.keys() and os.path.basename(r.get("source", "")) not in list(DOCS.values()):
        pass  # source path vetted below

# 5. each row source path exists on disk
for i, r in enumerate(d.get("rows", [])):
    p = r.get("source", "")
    if not os.path.isabs(p) or not os.path.exists(p.replace("/", os.sep)):
        fail.append("row %d source missing or not absolute: %s" % (i, p))
    else:
        print("source row %2d OK (%d bytes)" % (i, os.path.getsize(p.replace("/", os.sep))))

# 6. spec version markers seen in fetched pages
for fn in ["architecture.html", "security_best_practices.html"]:
    t = io.open(os.path.join(FETCH, fn), encoding="utf-8", errors="replace").read()
    print("version-marker %s: 2025-11-25 present=%s" % (fn, "2025-11-25" in t))

print("RESULT: %s (%d failures)" % ("PASS" if not fail else "FAIL", len(fail)))
for f in fail:
    print("  FAIL: %s" % f)
sys.exit(1 if fail else 0)
