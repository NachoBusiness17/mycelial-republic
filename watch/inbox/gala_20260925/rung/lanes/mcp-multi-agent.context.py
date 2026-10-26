import html, re, io, os, sys

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mcp-multi-agent.fetch")

def norm_text(fn):
    raw = io.open(os.path.join(D, fn), encoding="utf-8", errors="replace").read()
    raw = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
    txt = re.sub(r"(?s)<[^>]+>", " ", raw)
    txt = html.unescape(txt)
    txt = txt.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    txt = txt.replace("\u2014", "--").replace("\u2013", "--")
    txt = re.sub(r"\s+", " ", txt)
    return txt

JOBS = [
    ("architecture.html", ["1:1", "client-server architecture", "MUST establish", "composition model", "coordinator"]),
    ("security_best_practices.html", ["distinct, potentially untrusted", "name collisions", "sandbox", "informed consent", "Separate concerns"]),
    ("a2a_readme.md", ["opaque", "web standards", "complement", "Agent Card", "independent"]),
    ("code_execution_mcp.html", ["filesystem of TypeScript", "progressively", "98.7", "composes", "code execution approach"]),
    ("cf_agents_mcp.html", ["Durable Object", "session", "isolated", "remote MCP"]),
    ("openai_agents_mcp.html", ["MCPServerManager", "prefix", "guardrail", "Hosted MCP", "cach"]),
    ("crewai_mcp.html", ["multiple servers", "standardized", "simultaneously", "MCPServerAdapter"]),
    ("langchain_mcp.html", ["MCPAdapter", "transports", "multi-server"]),
    ("cf_codemode.html", ["sandbox", "TypeScript API", "using MCP wrong", "capabilities"]),
    ("docker_mcp_toolkit.html", ["isolated containers", "Toolkit", "container", "sandbox"]),
]

for fn, terms in JOBS:
    txt = norm_text(fn)
    print("=" * 20, fn, "len", len(txt))
    for t in terms:
        for m in list(re.finditer(re.escape(t), txt, re.I))[:2]:
            s = max(0, m.start() - 220)
            e = min(len(txt), m.end() + 260)
            print("  [%s] ...%s..." % (t, txt[s:e]))
    print()
