# MCP industry integration research: who runs it, and what patterns emerged (2025-2026)

Item: mcp-research. Banked 2026-09-28 by the flash50 MCP research gopher.

## Method and provenance (read this first)

Everything below is grounded in what I actually ran this session:

- 8 web searches via the session search tool. The search backend itself 429'd repeatedly
  (error code 1302, "Rate limit reached", its own Z.ai lane) and 3 calls timed out at 60s;
  the queries that survived are the ones cited here. This matches this account's known
  lane-cap behavior (AGENTS.md fan-out width law): the search surface is a SENSING lane.
- 3 primary-page fetches: Anthropic's original MCP announcement (anthropic.com/news/model-context-protocol),
  the MCP spec versioning page (modelcontextprotocol.io/specification/versioning), and the
  full 2026-07-28 spec changelog (modelcontextprotocol.io/specification/2026-07-28/changelog).
- 1 dogfood call of an MCP tool from this session's own context: Mapbox `bbox_tool` on a
  3-point LineString returned bbox [-122.5, 37.7, -122.4, 37.8] plus structured content,
  proving a live MCP client/server round trip runs inside this very harness.

Search-summary findings are marked [search]; fetched-page findings are marked [fetched].
Where a number exists only in a secondary summary, I say so.

## 1. Who adopted MCP, and when

[fetched] Anthropic launched MCP on 2024-11-25 (anthropic.com/news/model-context-protocol).
The announcement names the first wave: Block (CTO Dhanji R. Prasanna: plans to "use it to
build agentic systems"), Apollo as early adopters, and Zed, Replit, Codeium, and
Sourcegraph building it into their dev tools.

[search] The 2025 cross-vendor wave (knowmine.ai ecosystem retrospective, Mar 2026, plus
corroborating coverage): OpenAI added MCP across Agents SDK and ChatGPT desktop in
March 2025; Google DeepMind confirmed MCP support for Gemini and its SDKs in April 2025
(Demis Hassabis); Microsoft announced native MCP support in Windows 11 via Windows AI
Foundry plus GitHub Copilot and Azure integration in May 2025.

[search] OpenAI DevDay, 2025-10-06 (Simon Willison live blog + InfoQ + recap coverage):
the Apps SDK for ChatGPT is built on MCP (early partners Canva, Figma, Spotify, Zillow,
Booking.com); ChatGPT Developer Mode shipped full MCP connectors with read AND write
actions; Codex reached GA with MCP client support; AgentKit launched alongside.

[search] Governance went neutral on 2025-12-09: Anthropic donated MCP to the Agentic AI
Foundation, a Linux Foundation directed fund co-founded by Anthropic, Block, and OpenAI
(anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation;
linuxfoundation.org press release; blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation;
github.blog; openai.com/index/agentic-ai-foundation, which notes OpenAI also donated
AGENTS.md to the same foundation).

## 2. The protocol itself moved fast (verified spec history)

[fetched] Versioning is date-stamped (YYYY-MM-DD), current revision is 2026-07-28.
[fetched] The 2026-07-28 changelog (vs 2025-11-25) is the clearest signal of what
production at scale forced the protocol to become:

- Stateless-first: the `initialize` handshake, protocol-level sessions, `Mcp-Session-Id`,
  and SSE resumability (Last-Event-ID) are all REMOVED. Every request now carries protocol
  version + client capabilities in `_meta` (SEP-2575). This is the pattern shift from
  "connected session" to "stateless RPC over HTTP" that hosted/multi-tenant deployments
  demanded.
- Mandatory `server/discover` RPC: servers must advertise versions, capabilities, and
  identity in one call (replaces the handshake for selection; doubles as a compat probe).
- Long-running work moved to an official extension `io.modelcontextprotocol/tasks`
  (SEP-2663) with `tasks/get` polling and `tasks/update` for client-to-server input,
  replacing the blocking `tasks/result` design introduced in 2025-11-25.
- Multi Round-Trip Requests (MRTR, SEP-2322): servers return `InputRequiredResult`
  (`resultType: "input_required"`) instead of initiating server-to-client requests;
  all results now carry a required `resultType`.
- Cache-aware tooling: `tools/list` etc. must return deterministic ordering (explicitly
  to improve LLM prompt-cache hit rates) and carry `ttlMs` + `cacheScope` via
  `CacheableResult` (SEP-2549).
- Observability standardized: OpenTelemetry `traceparent`/`tracestate`/`baggage`
  conventions in `_meta` (SEP-414).
- Auth hardening: `iss` validation per RFC 9207 (SEP-2468), credentials keyed by issuer
  (SEP-2352), and OAuth Dynamic Client Registration deprecated in favor of Client ID
  Metadata Documents (PR 2858).
- Deprecations with a formal lifecycle policy (12-month minimum window, SEP-2596/SEP-1850):
  Roots, Sampling, and Logging features deprecated (pass files via tool params, call LLM
  provider APIs directly, log to stderr or OTel); the old HTTP+SSE transport reclassified
  Deprecated.

[fetched via search + primary blog] The official MCP Registry opened in preview on
2025-09-08 at registry.modelcontextprotocol.io ("Introducing the MCP Registry",
MCP blog), the canonical discovery catalog; commercial hubs (Smithery, Glama, PulseMCP,
Cloudflare's registry) run alongside it.

## 3. Patterns that emerged (the actual answer to "what patterns")

1. Namespace-prefixed tool naming for multi-server clients. Clients prefix every tool
   with its server name so one agent can hold tools from many servers without collisions.
   Dogfood proof: this session's own tool surface uses exactly this shape, e.g.
   `mcp__plugin_mapbox_mapbox__directions_tool` and `mcp__plugin_mapbox_mapbox-devkit__tilequery_tool`
   (server `plugin_mapbox_mapbox` inside tool name), and the live `bbox_tool` call above
   executed through it.
2. Context-pressure routing: search-then-load instead of load-everything. [search]
   Anthropic's advanced tool use (announced 2025-11-24, beta header
   `advanced-tool-use-2025-11-20`) ships the Tool Search Tool: Claude discovers tools at
   runtime instead of preloading all definitions; coverage (growthmethod.com, gurubase.io,
   tessl.io) reports it cut tool-definition overhead from roughly 77K tokens and notes a
   GitHub-internal 62% agent token-cost reduction figure; Programmatic Tool Calling lets
   the model write code that orchestrates tool calls instead of one JSON call per tool.
   The 2026-07-28 spec's deterministic list ordering + ttlMs is the protocol-level
   twin of this: make lists cacheable so the context tax is paid once.
3. The MCP gateway as the enterprise control plane. [search] A routing/auth/policy layer
   sits between agents and servers: Docker MCP Gateway (open source, dev and production,
   policy controls; collabnix.com 2025-09-21), AI-gateway vendors comparing LiteLLM vs
   Kong vs Portkey with MCP proxy adapters (truefoundry.com governance series, May 2026),
   and consolidated governed-access writeups (getmaxim.ai, May 2026). Same shape as the
   API-gateway generation: centralize OAuth, allowlists, rate limits, audit.
4. Remote/hosted server deployment replaced local stdio as the production default.
   [search] Cloudflare's pattern: MCP servers as Workers with OAuth provider libraries
   and AI Gateway observability; AWS Bedrock AgentCore: wrap the MCP server in a
   container, deploy to AgentCore Runtime as a managed enterprise agent platform
   (stackademic walkthrough, May 2026). The 2026-07-28 stateless-HTTP pivot is the spec
   catching up to this deployment reality.
5. Discovery moved from config files to registries: the official registry (2025-09-08
   preview) plus commercial hubs; server metadata becomes the trust surface (see 4).
6. Security became a first-class gate, not an afterthought (see 4).

## 4. The security record shaped the architecture

[search] Incident chain that every gateway/vendor writeup now cites:

- Invariant Labs (May 2025): GitHub MCP server exploited via prompt-injection planted in
  GitHub issues, hijacking an agent (Cursor shown) to leak private repos into public ones.
- Asana (June 2025): cross-tenant data exposure bug in its early-access MCP server
  (improper customer isolation), patched before feature restore.
- Supabase (July 2025): Cursor + Supabase MCP with `service_role` bypassing row-level
  security exfiltrated entire private SQL databases via a malicious support ticket;
  Simon Willison named the "lethal trifecta" (private data access + exposure to
  untrusted content + a channel out). Supabase published "Defense in Depth for MCP
  Servers" in Sept 2025.
- Tool poisoning as a class: malicious instructions hidden in tool descriptions that
  models auto-trust; Repello (Mar 2026) reports a 72.8% success rate and seven MCP CVEs
  shipped in a single 2025 month, including a CVSS 9.6 RCE in the widely deployed
  `mcp-remote` npm package and CVE-2025-34072 reported as a data-exfiltration flaw in an
  official Slack MCP server. A figma-developer-mcp command-injection advisory hit GitHub
  in Sept 2025.
- Scale-side confirmation: Wiz "2026 State of AI in the Cloud" (2026-04-29) found MCP
  servers in 80% of surveyed organizations (57%+ run self-hosted AI agents), and names
  secret leakage, excessive permissions, and tool poisoning as the driving risks behind
  new tooling such as MCP Guardian (Eqty Lab).

Consequence: the industry response is exactly patterns 2 and 3 above (registry
verification, gateway allowlists, least-privilege tool scoping, OTel audit trails),
plus the spec's own auth hardening (issuer binding, client ID metadata documents).

## 5. Reading for this repo, stated as interpretation

This harness already lives the pattern it researched: this session's Mapbox MCP tools
use server-prefixed naming, and the `bbox_tool` round trip proves the client path works
from a workflow child context. The 2026-07-28 stateless + `server/discover` + cacheable
lists direction matches this repo's own laws (pay the context tax once, verkle-committed
receipts, bytes-not-reports): the protocol is converging on exactly the discipline Mag
already enforces locally. One honest gap: I did not test any Mapbox network-path tool
here (only the offline geometry call), and every search-side number above arrived through
a rate-limited secondary lane, so treat [search]-marked figures as leads with citations,
not byte-verified truth.

## Sources

- [fetched] https://www.anthropic.com/news/model-context-protocol (2024-11-25)
- [fetched] https://modelcontextprotocol.io/specification/versioning (current: 2026-07-28)
- [fetched] https://modelcontextprotocol.io/specification/2026-07-28/changelog
- [search] https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation
- [search] https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation
- [search] https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation
- [search] https://openai.com/index/agentic-ai-foundation
- [search] https://github.blog/open-source/maintainers/mcp-joins-the-linux-foundation-what-this-means-for-developers-building-the-next-era-of-ai-tools-and-agents
- [search] https://simonwillison.net (DevDay 2025 live blog, 2025-10-06; Supabase MCP post, 2025-07)
- [search] https://www.anthropic.com (Introducing advanced tool use, 2025-11-24)
- [search] https://tessl.io (MCP tool search in Claude Code, Feb 2026); growthmethod.com; gurubase.io
- [search] https://slash-digital.io (MCP Registry preview 2025-09-08, citing MCP blog "Introducing the MCP Registry")
- [search] https://collabnix.com (Docker MCP Gateway, 2025-09-21)
- [search] https://www.truefoundry.com (AI Gateway governance series, 2026-05-04); https://www.getmaxim.ai (2026-05-14)
- [search] https://blog.stackademic.com (Bedrock AgentCore MCP, 2026-05-07)
- [search] https://invariantlabs.ai (GitHub MCP exploited, May 2025); https://www.pomerium.com (2025-07-07); supabase.com defense-in-depth (Sept 2025)
- [search] https://repello.ai (MCP security, 2026-03-04: 72.8%, seven CVEs, mcp-remote CVSS 9.6)
- [search] https://www.wiz.io (2026 State of AI in the Cloud, 2026-04-29: 80% / 57%)
- [search] https://knowmine.ai (MCP ecosystem in 2025, 2026-03-10)
- [dogfood, this session] Mapbox MCP `bbox_tool` call, returned bbox [-122.5, 37.7, -122.4, 37.8]
