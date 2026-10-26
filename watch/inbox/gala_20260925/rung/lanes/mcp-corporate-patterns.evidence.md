# mcp-corporate-patterns: raw evidence ledger (division B)

Lane: mcp-corporate-patterns. All quotes below were fetched first-hand on 2026-10-10 via WebFetch of the primary pages named next to each quote. Quotes are transcribed from the rendered page text; where the source sentence was trimmed for length or emphasis markers were stripped, that is noted inline. No paraphrase inside quote blocks.

## 1. Anthropic, "Introducing the Model Context Protocol" (2024-11-25)

URL: https://www.anthropic.com/news/model-context-protocol (fetched 2026-10-10)

- "Today, we're open-sourcing the [Model Context Protocol](https://modelcontextprotocol.io) (MCP), a new standard for connecting AI assistants" (inline link kept as the page rendered it)
- "MCP addresses this challenge. It provides a universal, open standard for connecting AI systems with data sources"
- "Instead of maintaining separate connectors for each data source, developers can now build against a standard protocol."
- "Early adopters like Block and Apollo have integrated MCP into their systems, while development tools companies including Zed, Replit, Codeium, and Sourcegraph are working with MCP to enhance their platforms" (trimmed at an em-dash that continues with "enabling AI agents to better retrieve relevant information" on the page; the em-dash is excluded from the record quote)
- "All [Claude.ai](http://claude.ai/redirect/website.v1.358bd719-afe1-4c54-88b5-b4bf272034df) plans support connecting MCP servers to the Claude Desktop app." (inline redirect URL kept as rendered)
- "Claude for Work customers can begin testing MCP servers locally, connecting Claude to internal systems and datasets."

## 2. Anthropic, "Integrations" (2025-05-01, update 2025-06-03)

URL: https://claude.com/blog/integrations (reached via 308 redirect from https://www.anthropic.com/news/integrations; fetched 2026-10-10)

- "Today, we're introducing Integrations, allowing Claude to work seamlessly with remote MCP servers across the web and desktop apps."
- "Until now, support for MCP was limited to Claude Desktop through local servers."
- "Integrations and advanced Research are now available in beta on the Max, Team, and Enterprise plans, and will soon be available on Pro."
- Launch integrations named on the page: Atlassian (Jira and Confluence), Zapier, Cloudflare, Intercom, Asana, Square, Sentry, PayPal, Linear, Plaid; upcoming: Stripe, GitLab, Box.

## 3. OpenAI Agents SDK docs, "MCP Support"

URL: https://openai.github.io/openai-agents-python/mcp/ (fetched 2026-10-10)

- "The Agents Python SDK understands multiple MCP transports."
- "This lets you reuse existing MCP servers or build your own to expose filesystem, HTTP, or connector backed tools to an agent."
- "MCP is an open protocol that standardizes how applications provide context to LLMs." (quoted from the official MCP docs within the page)
- "Hosted tools push the entire tool round-trip into OpenAI's infrastructure."
- Supported servers listed on the page: HostedMCPTool (Responses API calls a public MCP server on the model's behalf), MCPServerStreamableHttp, MCPServerSse (deprecated upstream), MCPServerStdio, plus MCPServerManager for coordinating multiple servers.

## 4. OpenAI API docs, Responses API MCP guide

URL: https://developers.openai.com/api/docs/guides/tools-connectors-mcp (reached via 301 from https://platform.openai.com/docs/guides/tools-connectors-mcp; fetched 2026-10-10). Rendered text, emphasis markers stripped.

- "you can give models new capabilities using remote MCP servers or Secure MCP Tunnel"
- "The Responses API works with remote MCP servers that support either the Streamable HTTP or the HTTP/SSE transport protocols."
- "By default, OpenAI will request your approval before any data is shared with a connector or remote MCP server."
- "If the model decides to use an MCP server, it will first make a request to list available tools from the server"
- "When the model decides to call an MCP tool, the API will make a request to the remote MCP server to call the tool"
- "`connector_id` is deprecated for models released after September 1, 2026." (deprecation of the legacy built-in connectors path, while MCP remains the live path)

## 5. Google ADK docs, "MCP Tools"

URL: https://adk.dev/tools-custom/mcp-tools/ (reached via redirects google.github.io/adk-docs/tools/mcp-tools/ to adk.dev/tools/mcp-tools/ to tools-custom; fetched 2026-10-10)

- "The Model Context Protocol (MCP) is an open standard for connecting generative AI models to external data sources, tools, and systems."
- "In ADK, you use the McpToolset class as an interface between MCP Servers and ADK agents."
- "It is also possible to configure an ADK server as an MCP server for use by other client systems."
- "Agent-Exposed MCP Server: When you build an MCP server that wraps ADK Tools using to_mcp_server."
- Named classes: McpToolset, StdioConnectionParams, StreamableHTTPConnectionParams, SseConnectionParams, StdioServerParameters (from the mcp package), to_mcp_server, AgentTool, LoadMcpResourceTool.
- Example remote MCP server on the page: Google Maps Grounding Lite at "https://mapstools.googleapis.com/mcp".

## 6. Google Gemini CLI README

URL: https://raw.githubusercontent.com/google-gemini/gemini-cli/main/README.md (fetched 2026-10-10)

- "Extensible: MCP (Model Context Protocol) support for custom integrations." (emoji stripped)
- "Use MCP servers to connect new capabilities, including media generation with Imagen, Veo or Lyria."
- "Configure MCP servers in `~/.gemini/settings.json` to extend Gemini CLI with custom tools"

## 7. Microsoft, Azure AI Foundry Build 2025 blog post (2025-05-19)

URL: https://azure.microsoft.com/en-us/blog/azure-ai-foundry-your-ai-app-and-agent-factory/ (fetched 2026-10-10)

- "All these models will be accessible through a unified API and Model Context Protocol (MCP) server for Azure AI Foundry models, making it" (trimmed mid-sentence)
- "We've also implemented open interoperability standards-such as Agent-to-Agent (A2A) communication, to enable different agents to exchange" (the page uses an em-dash here; transcribed with a hyphen for the record, trim noted)

## 8. Microsoft Learn, "Connect agents to MCP server endpoints - Microsoft Foundry" (ms.date 2026-08-26, updated_at 2026-09-04)

URL: https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/model-context-protocol (fetched 2026-10-10)

- "Connect your Foundry agents to [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) servers by using the MCP tool." (inline link kept as rendered)
- "Treat tool descriptions, annotations, and results from remote MCP servers as untrusted input. They can contain indirect prompt injection instructions."
- "The Agent Service runtime only accepts a remote MCP server endpoint. If you want to add tools from a local MCP server, you need to self-host it on [Azure Container Apps](https://github.com/Azure-Samples/mcp-container-ts) or [Azure Functions](https://github.com/Azure-Samples/mcp-sdk-functions-hosting-python/tree/main) to get a remote MCP server endpoint."
- "The toolbox MCP endpoint supports long-running operations through [MCP tasks](https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/tasks), which is in preview." (cites MCP spec version 2025-11-25)
- "Use an allow list of tools by using `allowed_tools`."
- Default approval posture: `require_approval` default is "always"; values documented: always, never, or per-tool lists.
- SDK support matrix on the page: Python, C#, JavaScript, Java, REST all check-marked for MCP connections; Basic and Standard agent setups both supported.

## 9. Agentic AI Foundation (Linux Foundation), About page

URL: https://aaif.io/about (fetched 2026-10-10). Home page https://aaif.io carries the tagline "Operationalizing agentic AI for enterprise scale".

- "The Agentic AI Foundation (AAIF) is a neutral, open foundation under the Linux Foundation that hosts open protocols and open source projects" (page sentence continues into the next quote)
- "including the Model Context Protocol (MCP), goose, AGENTS.md, Agent2Agent (A2A) and agentgateway."
- Platinum members listed on the page: AWS, Anthropic, Block, Bloomberg, Cloudflare, Google, Microsoft, and OpenAI.

## 10. Negatives and unverified items (honest ledger)

- https://openai.com/index/new-tools-for-building-agents/ returned HTTP 403 on fetch (2026-10-10): OpenAI's March 2025 Agents SDK launch post NOT read first-hand.
- The widely reported "Sam Altman announced OpenAI MCP adoption on 2025-03-26" is SECONDARY (web-search summaries: thenewstack.io, Wikipedia) and was NOT verified first-hand in this lane. What IS first-hand: OpenAI's own Agents SDK and Responses API docs (sections 3 and 4 above) ship MCP support today.
- https://www.fierce-network.com/newswire returned HTTP 403 (2026-10-10): the Linux Foundation Dec 9 2025 press release text NOT read first-hand. What IS first-hand: aaif.io/about (section 9) confirms AAIF under Linux Foundation hosting MCP, goose, AGENTS.md, A2A, agentgateway, with the eight platinum members listed.
- The 2025-03-26 OpenAI adoption date and the 2025-12-09 AAIF launch date appear only in secondary coverage in this lane's record; treat those two dates as secondary-sourced.
