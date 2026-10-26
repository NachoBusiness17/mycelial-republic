# mcp-multi-agent lane: byte-verified quote bank (division B)

Every quote below was extracted from raw page bytes saved on disk under
mcp-multi-agent.fetch/ (curl -sL, 2026-10-10), HTML-stripped and whitespace-normalized,
then substring-verified by mcp-multi-agent.quotecheck.py. Quotes are contiguous
substrings of the raw file bytes; truncation points are marked with [...] where a
sentence was cut only to drop em-dashes or trailing clauses. No em-dashes in this file.

## 1. MCP core architecture (multi-server composition shape)

Raw file: mcp-multi-agent.fetch/architecture.html
URL: https://modelcontextprotocol.io/docs/concepts/architecture

ARCH-1: "The MCP host accomplishes this by creating one MCP client for each MCP server."
ARCH-2: "Each MCP client maintains a dedicated connection with its corresponding MCP server."
ARCH-3: "Local MCP servers that use the STDIO transport typically serve a single MCP client, whereas remote MCP servers that use the Streamable HTTP transport will typically serve many MCP clients."

## 2. MCP security best practices (sandboxing / isolation / threat model)

Raw file: mcp-multi-agent.fetch/security_best_practices.html
URL: https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices
(note: fetched page header shows the docs site serving spec version 2025-11-25)

SEC-1: "Execute MCP server commands in a sandboxed environment with minimal default privileges"
SEC-2: "Launch MCP servers with restricted access to the file system, network, and other system resources"
SEC-3: "Local MCP servers are binaries that are downloaded and executed on the same machine as the MCP client."
SEC-4: "Attackers can exploit MCP proxy servers that connect to third-party APIs" [...continues: creating "confused deputy" vulnerabilities...]
SEC-5: "Maintain a registry of approved client_id values per user"

## 3. A2A protocol (agent-to-agent layer)

Raw file: mcp-multi-agent.fetch/a2a_readme.md
URL: https://raw.githubusercontent.com/a2aproject/A2A/main/README.md

A2A-1: "An open protocol enabling communication and interoperability between opaque agentic applications"
A2A-2: "Operate without exposing their internal state, memory, or tools."
A2A-3: "Learn how A2A complements MCP by enabling agents to collaborate with each other"

## 4. Anthropic engineering: code execution with MCP

Raw file: mcp-multi-agent.fetch/code_execution_mcp.html
URL: https://www.anthropic.com/engineering/code-execution-with-mcp

ANT-1: "The agent discovers tools by exploring the filesystem: listing the ./servers/ directory to find available servers"
ANT-2: "This reduces the token usage from 150,000 tokens to 2,000 tokens" [...continues: a time and cost saving of 98.7%]
ANT-3: "Presenting tools as code on a filesystem allows models to read tool definitions on-demand, rather than reading them all up-front."
ANT-4: "Agents can write intermediate results to files, enabling them to resume work and track progress"
ANT-5: "However, once too many servers are connected, tool definitions and results can consume excessive tokens, reducing agent efficiency."

## 5. OpenAI Agents SDK (framework speaking MCP)

Raw file: mcp-multi-agent.fetch/openai_agents_mcp.html
URL: https://openai.github.io/openai-agents-python/mcp/

OAI-1: "When you have multiple MCP servers, use MCPServerManager to connect them up front and expose the successfully connected subset of those servers to your agents."
OAI-2: "include_server_in_tool_names is opt-in. When enabled, each local MCP tool is exposed to the model with a deterministic server-prefixed name, which helps avoid collisions when multiple MCP servers publish tools with the same name."
(note: a third candidate quote about MCP tool failures raised as exceptions was dropped:
the page's own line-wrapped code comment inserts an artifact between its clauses, so no
clean contiguous substring exists; code comment, not page prose)

## 6. CrewAI (framework speaking MCP)

Raw file: mcp-multi-agent.fetch/crewai_mcp.html
URL: https://docs.crewai.com/en/mcp/overview

CREW-1: "The Model Context Protocol (MCP) provides a standardized way for AI agents to provide context to LLMs by communicating with external services, known as MCP Servers."
CREW-2: "Aggregate tools from several MCP servers simultaneously using a single adapter."
CREW-3: "Use the mcps field directly on agents for seamless MCP tool integration."

## 7. LangChain (framework speaking MCP)

Raw file: mcp-multi-agent.fetch/langchain_mcp.html
URL: https://docs.langchain.com/oss/python/langchain/mcp

LC-1: "Connect LangChain agents to MCP servers with MCPAdapter."
LC-2: "MCPAdapter is built on FastMCP"
LC-3: "discovers a server's tools and adapts them into LangChain tools you can pass straight to create_agent"

## 8. Cloudflare blog: Code Mode (tools as TypeScript API in a sandbox)

Raw file: mcp-multi-agent.fetch/cf_codemode.html
URL: https://blog.cloudflare.com/code-mode/

CM-1: "It turns out we've all been using MCP wrong."
CM-2: "Convert the MCP tools into a TypeScript API, and then ask an LLM to write code that calls that API."
CM-3: "We found agents are able to handle many more tools, and more complex tools, when those tools are presented as a TypeScript API rather than directly."
CM-4: "We'd like the AI agent to run in a sandbox such that it can only access the tools we give it."
CM-5: "MCP makes it possible for the agentic framework to implement this, by handling connectivity and authorization in a standard way, independent of the AI code."

## Negative / unverifiable findings (honest record)

- Cloudflare Agents MCP docs page (developers.cloudflare.com/agents/model-context-protocol/)
  and its security/ page, plus docs.docker.com/ai/mcp-catalog-and-toolkit/ and
  docs.docker.com/ai/sandboxes/: fetched raw bytes are nav/JS-shell only; no prose
  sentences extractable, so nothing from those pages is quoted. Their isolation
  claims (Durable Object per session; containerized servers) stay search-level
  notes, NOT verified quotes.
- MCP blog post "Multi-Agent Systems: Avoiding Statefulness, Complexity, and the
  50-Tool Threshold" (search result, dated 2026-01-16): URL returned network error
  twice via webReader and HTTP 404 via WebFetch; blog index fetched 2026-10-10 does
  not list it. Unverified, not quoted.
- Estate prior art: git grep -cil mcp across corpus/steal, memory/rib,
  .agents/skills, memory/skills matched only incidental mentions (zai-reference plan
  docs, OnionClaw third-party repo review, master dig notes). No dedicated
  multi-agent-over-MCP survey existed before this lane.
- Cross-check: sibling lane raw evidence _byproducts/mcp-spec-officials.spec-releases.raw.json shows the
  latest MCP spec release tag is 2026-07-28; the docs pages fetched here serve
  version 2025-11-25.
