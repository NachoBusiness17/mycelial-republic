import html, re, io, os

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
    ("architecture.html", ["dedicated connection", "composition model", "route messages", "MUST"]),
    ("security_best_practices.html", ["tool name", "server name", "confused", "Consent", "registry", "distinct", "monolithic"]),
    ("a2a_readme.md", ["memory", "Autonomy", "opaque participation", "top of", "Opportunit"]),
    ("code_execution_mcp.html", ["TypeScript", "filesystem", "progressive disclosure", "skill", "compos", "volunteer", "listing"]),
    ("cf_agents_mcp.html", ["Durable", "stateful", "McpAgent ", "isolation"]),
    ("openai_agents_mcp.html", ["hosted MCP server tools", "approval", "before a tool"]),
    ("docker_mcp_toolkit.html", ["catalog", "Toolkit", "one-click"]),
    ("crewai_mcp.html", ["mcps field", "DSL", "simplest"]),
]

for fn, terms in JOBS:
    txt = norm_text(fn)
    print("=" * 20, fn)
    for t in terms:
        for m in list(re.finditer(re.escape(t), txt, re.I))[:2]:
            s = max(0, m.start() - 260)
            e = min(len(txt), m.end() + 320)
            print("  [%s] ...%s..." % (t, txt[s:e]))
    print()
