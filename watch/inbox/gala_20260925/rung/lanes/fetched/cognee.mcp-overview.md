> ## Documentation Index
> Fetch the complete documentation index at: https://docs.cognee.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Cognee MCP Memory Server

> Cognee MCP is a memory server for AI assistants: give Claude Code, Claude Desktop, Cursor, Cline, Continue and Codex persistent memory through the Model Context Protocol

## What Cognee MCP is

Cognee MCP is a Model Context Protocol server that gives AI assistants persistent memory backed by a Cognee knowledge graph. Any MCP client, such as Claude Code, Cursor or Codex, can store and recall memories through its `remember`, `recall` and `forget` tools. Run it standalone for one user, or in [API Mode](#architecture-modes) so several assistants share one knowledge graph.

## What is MCP?

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) is a standard for adding specialized tools to AI assistants. It allows AI tools like Claude or Cursor to work with external systems such as databases, APIs, and AI platforms.

Without MCP, each AI assistant needs custom integrations for every external system. This creates duplication and inconsistency across tools.

MCP provides a single method for extending AI assistants with:

* **Standardized connections** between AI tools and external systems
* **Secure data access** with built-in authentication and permissions
* **Tool interoperability** so you can switch between AI providers
* **Persistent memory** that survives across conversations and sessions

## How Cognee MCP Works

Cognee MCP exposes specialized tools through the MCP protocol. These tools handle memory management, code intelligence, and data operations. You access them through MCP-compatible AI assistants like Cursor, Claude Desktop, Continue, Cline, and Codex.

To keep the tool payload small, the server lists only a subset of its catalog in `tools/list` by default and makes the rest discoverable through tool search. The remaining tools stay callable by name. See [Tool modes](/cognee-mcp/mcp-tools#tool-modes) for the modes and how to restore the full listing.

The tools enable your AI assistant to:

* Store and retrieve knowledge from previous conversations
* Build persistent understanding of your codebase and projects
* Access structured memories across different sessions

For new integrations, prefer the v1.0 memory tools (`remember`, `recall`, `forget`). The legacy tools remain available when you need lower-level control.

See the [Tools Reference](/cognee-mcp/mcp-tools) for all available operations.

## Architecture Modes

Cognee MCP can run in two modes:

**Standalone Mode**: The MCP server manages its own database and processing. Each MCP instance maintains separate data. Use this for personal development or when clients need isolated environments. Out of the box it uses SQLite, LanceDB, and the embedded Ladybug (Kuzu) graph store — see [Default databases](/cognee-mcp/mcp-local-setup#further-details) for details and how to switch to Neo4j or Postgres.

**API Mode**: The MCP server connects to a centralized Cognee backend via API. Multiple MCP instances can share the same knowledge graph. Use this when you want team members to access shared memory or when running multiple AI clients that need consistent data. Each instance authenticates with a single token, so everything it writes belongs to one Cognee user — see [Running in API Mode](/cognee-mcp/mcp-local-setup#running-in-api-mode) for what that means when several tenants share one deployment.

<Info>
  **Do I need to install Cognee separately?** No. The `cognee-mcp` package bundles the full Cognee library, so following any setup guide ([Docker](/cognee-mcp/mcp-quickstart) or [Local Setup](/cognee-mcp/mcp-local-setup)) installs the complete Cognee stack together with the MCP tools — you get "everything plus MCP." In **Standalone Mode** the server runs the entire Cognee pipeline (ingestion, graph building, and search) locally with its own database; no extra Cognee install or running backend is required. You only need a separate [Cognee REST API](/guides/deploy-rest-api-server) when you switch to **API Mode** to share one knowledge graph across clients.
</Info>

## Setup Options

Choose your deployment method:

<CardGroup cols={3}>
  <Card title="Docker Quickstart" href="/cognee-mcp/mcp-quickstart" icon="docker">
    **Recommended for most users**

    Get running in minutes with a pre-built container.
  </Card>

  <Card title="API Mode (Shared)" href="/cognee-mcp/mcp-quickstart#api-mode-shared-knowledge-graph" icon="network">
    **For teams**

    Connect multiple clients to a shared knowledge graph.
  </Card>

  <Card title="Local Setup" href="/cognee-mcp/mcp-local-setup" icon="code">
    **For development**

    Install the PyPI release with `uvx`, or build from source for full control and latest features.
  </Card>
</CardGroup>

<Info>
  **Using Cognee Cloud?** Cognee MCP and Cognee Cloud are separate systems with different APIs and authentication schemes. See [Cognee Cloud & MCP](/cognee-mcp/mcp-cloud-connection) to understand how they relate and when to use each.
</Info>

## Next Steps

<CardGroup cols={2}>
  <Card title="Tools Reference" href="/cognee-mcp/mcp-tools" icon="wrench">
    See all available MCP tools and operations
  </Card>

  <Card title="Client Integrations" href="/cognee-mcp/integrations" icon="code">
    Connect with Cursor, Claude, Continue, and more
  </Card>
</CardGroup>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.