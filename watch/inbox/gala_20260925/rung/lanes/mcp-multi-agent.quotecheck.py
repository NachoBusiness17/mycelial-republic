import html, re, io, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(BASE, "mcp-multi-agent.fetch")

def norm_text(fn):
    raw = io.open(os.path.join(D, fn), encoding="utf-8", errors="replace").read()
    raw = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
    txt = re.sub(r"(?s)<[^>]+>", " ", raw)
    txt = html.unescape(txt)
    txt = txt.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    txt = txt.replace("\u2014", "--").replace("\u2013", "--")
    txt = re.sub(r"\s+", " ", txt)
    return txt

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

QUOTES = [
    ("ARCH-1", "architecture", "The MCP host accomplishes this by creating one MCP client for each MCP server."),
    ("ARCH-2", "architecture", "Each MCP client maintains a dedicated connection with its corresponding MCP server."),
    ("ARCH-3", "architecture", "Local MCP servers that use the STDIO transport typically serve a single MCP client, whereas remote MCP servers that use the Streamable HTTP transport will typically serve many MCP clients."),
    ("SEC-1", "security", "Execute MCP server commands in a sandboxed environment with minimal default privileges"),
    ("SEC-2", "security", "Launch MCP servers with restricted access to the file system, network, and other system resources"),
    ("SEC-3", "security", "Local MCP servers are binaries that are downloaded and executed on the same machine as the MCP client."),
    ("SEC-4", "security", "Attackers can exploit MCP proxy servers that connect to third-party APIs"),
    ("SEC-5", "security", "Maintain a registry of approved client_id values per user"),
    ("A2A-1", "a2a", "An open protocol enabling communication and interoperability between opaque agentic applications"),
    ("A2A-2", "a2a", "Operate without exposing their internal state, memory, or tools."),
    ("A2A-3", "a2a", "Learn how A2A complements MCP by enabling agents to collaborate with each other"),
    ("ANT-1", "anthropic", "The agent discovers tools by exploring the filesystem: listing the ./servers/ directory to find available servers"),
    ("ANT-2", "anthropic", "This reduces the token usage from 150,000 tokens to 2,000 tokens"),
    ("ANT-3", "anthropic", "Presenting tools as code on a filesystem allows models to read tool definitions on-demand, rather than reading them all up-front."),
    ("ANT-4", "anthropic", "Agents can write intermediate results to files, enabling them to resume work and track progress"),
    ("ANT-5", "anthropic", "However, once too many servers are connected, tool definitions and results can consume excessive tokens, reducing agent efficiency."),
    ("OAI-1", "openai", "When you have multiple MCP servers, use MCPServerManager to connect them up front and expose the successfully connected subset of those servers to your agents."),
    ("OAI-2", "openai", "include_server_in_tool_names is opt-in. When enabled, each local MCP tool is exposed to the model with a deterministic server-prefixed name, which helps avoid collisions when multiple MCP servers publish tools with the same name."),
    ("CREW-1", "crewai", "The Model Context Protocol (MCP) provides a standardized way for AI agents to provide context to LLMs by communicating with external services, known as MCP Servers."),
    ("CREW-2", "crewai", "Aggregate tools from several MCP servers simultaneously using a single adapter."),
    ("CREW-3", "crewai", "Use the mcps field directly on agents for seamless MCP tool integration."),
    ("LC-1", "langchain", "Connect LangChain agents to MCP servers with MCPAdapter."),
    ("LC-2", "langchain", "MCPAdapter is built on FastMCP"),
    ("LC-3", "langchain", "discovers a server's tools and adapts them into LangChain tools you can pass straight to create_agent"),
    ("CM-1", "codemode", "It turns out we've all been using MCP wrong."),
    ("CM-2", "codemode", "Convert the MCP tools into a TypeScript API, and then ask an LLM to write code that calls that API."),
    ("CM-3", "codemode", "We found agents are able to handle many more tools, and more complex tools, when those tools are presented as a TypeScript API rather than directly."),
    ("CM-4", "codemode", "We'd like the AI agent to run in a sandbox such that it can only access the tools we give it."),
    ("CM-5", "codemode", "MCP makes it possible for the agentic framework to implement this, by handling connectivity and authorization in a standard way, independent of the AI code."),
]

results = []
for qid, doc, q in QUOTES:
    results.append((qid, doc, q in DOCS[doc], q))

fails = [r for r in results if not r[2]]
for qid, doc, ok, q in results:
    print("%s %s %s (words=%d)" % ("PASS" if ok else "FAIL", qid, doc, len(q.split())))
print("TOTAL: %d PASS / %d FAIL of %d" % (len(results) - len(fails), len(fails), len(results)))
sys.exit(1 if fails else 0)
