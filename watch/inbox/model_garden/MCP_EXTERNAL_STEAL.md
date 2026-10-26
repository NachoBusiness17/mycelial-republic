# MCP_EXTERNAL_STEAL - Lane MCP-3 external sweep for the MCP lattice (2026-10-02)

PROVENANCE: Lane MCP-3 (EXTERNAL STEAL ON THE GAPS), mission from the operator's
MCP-lattice vision. Priority list source: `watch/inbox/model_garden/MCP_LATTICE_SPEC_SEED.md`
own gaps (verified by directory read: MCP_LATTICE_5W.md does not exist as of 2026-10-02,
so the spec-seed's gap list is the priority list: get_law, get_terrain, get_position,
get_context, pull-equals-ledger-row, hot-first, cache scaffold >=5,120).

METHOD: five sweep areas, all claims web-cited (fetched/searched 2026-10-01..02).
Estate baseline is byte-backed: mag/mcp_server.py pins `PROTOCOL_VERSION = "2025-06-18"`
(line ~60, 565 lines, hand-rolled stdio JSON-RPC, pin gate, profiles, quantize
cartridges); mag/mcp_http.py (HTTP gateway); mag/context_compression.py (LLMLingua
lineage, budget law); mag/context_pack.py; the RIB-fork KG (3,804 nodes / 744 edges
per the spec-seed); tools/hermes_burn.py (usage.jsonl per-dispatch burn banking);
tools/meter_patrol.py + tools/quota_ledger.py.

## S1. MCP in production 2026 (the protocol moved under us)

### S1.1 The 2026-07-28 spec revision: MCP went STATELESS
What: sessions removed, `Mcp-Session-Id` gone, `initialize`/`notifications/initialized`
handshake removed; every request carries protocol version + client capabilities in
`_meta`; a new MUST-implement `server/discover` RPC; `subscriptions/listen` replaces
resource subscription; `resultType` required on all results; MRTR (Multi Round-Trip
Requests, not "multi-root") replaces server-initiated roots/sampling/elicitation with
client-driven retry round trips; JSON Schema 2020-12 fully allowed (SEP-2106).
Cite: https://modelcontextprotocol.io/specification/2026-07-28/changelog ,
https://modelcontextprotocol.io/specification/2026-07-28/basic
VERDICT: WE-LACK-ADOPT. mag/mcp_server.py implements the 2025-06-18 handshake shape
(initialize -> initialized -> tools/list), one full revision behind; 2025-11-25 is
also superseded. Ticket T2.

### S1.2 CacheableResult: the estate cache law is now protocol-native
What: minor change #5 in the 2026-07-28 changelog requires `ttlMs` (freshness hint)
and `cacheScope` ("public"/"private") on results from tools/list, resources/list,
resources/read, resources/templates/list via a `CacheableResult` interface; and minor
change #3 says servers SHOULD return tools/list in deterministic order explicitly
"to enable client-side caching and improve LLM prompt cache hit rates".
Cite: https://modelcontextprotocol.io/specification/2026-07-28/changelog
VERDICT: WE-LACK-ADOPT (design-in from day one). The spec-seed's law 5 (cache
scaffold >=5,120 tokens) now has carrier fields: hot lattice rows = short ttlMs,
cold rows = long ttlMs; deterministic tool order is the scaffold stability the
prompt-cache vendors price (S4.5). Zero external invention needed, just adopt the
field names. Ticket T1 (folded).

### S1.3 Tasks extension (io.modelcontextprotocol/tasks): durable async handles
What: long-running tool calls return `CreateTaskResult` (taskId, ttlMs, pollIntervalMs);
clients poll `tasks/get`; states working / input_required / completed / failed /
cancelled; mid-flight input via `tasks/update`; task survives client crash
("durably created before the response is sent"). Made an official extension in
2026-07-28 (SEP-2663).
Cite: https://modelcontextprotocol.io/extensions/tasks/overview
VERDICT: WE-LACK-ADOPT. This is the wire shape for the estate's k8s bridge
(mag/rib_k8s.py brute fan-outs) and the operator promote gate: a k8s batch job
dispatched through the lattice returns a task handle; the human gate is literally
`input_required`. Ticket T4.

### S1.4 Skills over MCP went FINAL (SEP-2640, merged 2026-09-13)
What: official Skills extension `io.modelcontextprotocol/skills`, Resources-based:
skills (SKILL.md-shaped structured instructions) discovered and consumed through
MCP as resources; WG maintained by Anthropic/Bloomberg/Nordstrom maintainers;
conformance scenarios merged 2026-09-11.
Cite: https://modelcontextprotocol.io/community/working-groups/skills-over-mcp ,
extension repo https://github.com/modelcontextprotocol/ext-skills
VERDICT: WE-LACK-ADOPT (medium). The estate already owns a skill surface
(.agents/skills/, skill_ledger surfaces in the swarm file lists); serving it over
the lattice as MCP resources makes the swarm's skill knowledge pull-shaped instead
of seat-local. Ticket T7.

### S1.5 Pagination: cursors are the spec's right-sizing primitive for lists
What: MCP paginates list operations via opaque cursors; servers yield pages, clients
page through large result sets.
Cite: https://modelcontextprotocol.io/specification/2026-07-28/server/utilities/pagination
VERDICT: WE-HAVE-EQUIVALENT conceptually (context_compression enforces byte/token
budgets on content), but get_context paging should still speak cursor so a model
can pull "next slice" instead of re-asking. Fold into T1 tool design.

### S1.6 Authorization: OAuth 2.1 resource-server model
What: MCP client = OAuth 2.1 client, MCP server = resource server; PKCE; Protected
Resource Metadata discovery; RFC 9207 `iss` validation; Dynamic Client Registration
now DEPRECATED in favor of Client ID Metadata Documents (2026-07-28 changelog).
Cite: https://modelcontextprotocol.io/specification/draft/basic/authorization ,
https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/authorization
VERDICT: ORTHOGONAL for now. mag/mcp_server.py's stdio posture is already documented
as "transport, not authority" and spawns grant nothing the backend lacks. Becomes
WE-LACK-ADOPT only the day mcp_http.py serves off-host; then it is token+scope per
profile. No ticket today.

### S1.7 Reference servers: archived; registry is the discovery point
What: modelcontextprotocol/servers slimmed to a maintained few; the classic
filesystem/memory/git/fetch/postgres reference implementations live in
modelcontextprotocol/servers-archived "as-is"; discovery consolidates into the
official MCP registry (registry.modelcontextprotocol.io).
Cite: https://github.com/modelcontextprotocol/servers ,
https://github.com/modelcontextprotocol/servers-archived
VERDICT: WE-HAVE-EQUIVALENT (the estate's own TOOL_MAP + pin ledger + profiles are
a private registry with drift teeth, stronger than the public one for our threat
model). ORTHOGONAL otherwise.

### S1.8 Sampling is DEPRECATED (design warning)
What: 2026-07-28 deprecates Roots, Sampling, and Logging; suggested migration for
Sampling: "integrate directly with LLM provider APIs" instead of asking the client
model to serve the server.
Cite: https://modelcontextprotocol.io/specification/2026-07-28/changelog
VERDICT: ORTHOGONAL (do-not-build). Kill any idea of lattice-side compression via
MCP sampling; the compression organ calls the provider lane directly, which is what
the spec now tells everyone to do.

## S2. RAG-vs-tool context: the JIT debate is settled toward PULL OVER DUMP

### S2.1 Anthropic's own engineering went just-in-time
What: "Effective context engineering for AI agents" (Anthropic): agents keep
lightweight identifiers (file paths, stored queries, links) and load data at
runtime via tools; Claude Code loads only CLAUDE.md up front and pulls the rest
with glob/grep; attention is a finite budget, context rot degrades recall as
tokens grow; the governing principle: "find the smallest set of high-signal
tokens that maximize the likelihood of your desired outcome"; long-horizon
techniques: compaction at window limit (preserving architectural decisions),
structured note-taking outside context (NOTES.md), sub-agent architectures
whose children return condensed summaries of typically 1,000-2,000 tokens.
Cite: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
VERDICT: WE-HAVE-EQUIVALENT doctrine (PULL OVER DUMP + right-sized + compaction
organ + pile habit are all this exact doctrine). The steal is the concrete number:
sub-agent returns sized 1,000-2,000 tokens = the default budget band for
get_context pulls between swarm bodies. Ticket T6.

### S2.2 Anthropic replaced their RAG with agentic search (the debate's direction)
What: analysis of Anthropic's deployment: agentic search beat pre-indexed RAG on
accuracy, operational simplicity, and avoided pre-index security/staleness;
companion piece argues context engineering is ~80% agentic search.
Cite: https://robertheubanks.substack.com/p/anthropic-replaced-their-rag-pipeline ,
https://leoniemonigatti.com/blog/agentic-search-for-context-engineering.html ,
https://www.anthropic.com/engineering/contextual-retrieval
VERDICT: WE-HAVE-EQUIVALENT (the 239KB dump class and DUEL2 empty-evidence class
are exactly the two failure modes the external world names: dump bloat and stale
pre-index). Law 1 of the spec-seed is externally validated doctrine.

### S2.3 Contextual retrieval: the corpus/lattice retrieval quality steal
What: prepending a Claude-generated 1-2 sentence chunk-context to each chunk before
indexing cut top-20 retrieval failure 49% (contextual embeddings + contextual
BM25, 5.7% -> 2.9%) and 67% with reranking; hybrid keyword+embedding beats either
alone for exact tokens (law-row identifiers, coordinates).
Cite: https://www.anthropic.com/engineering/contextual-retrieval
VERDICT: WE-LACK-ADOPT. corpus FTS is FTS5 keyword-only today; law rows and corpus
chunks should carry stable contextual prefixes (source doc + coordinate +
temperature) and a hybrid lexical+vector lane behind get_law/get_context. Ticket T5.

## S3. Knowledge-graph serving: the hot lattice's external cousins

### S3.1 MemGPT/Letta: paging as the memory model (the closest external shape)
What: LLM-as-OS: main context = RAM, archival/recall = disk; the model itself
issues function calls to page data between tiers; Letta ships "core memory
blocks", discrete named in-context blocks the agent reads/writes, plus a
benchmark practice for paging.
Cite: https://arxiv.org/pdf/2310.08560 ,
https://www.letta.com/blog/agent-memory ,
https://www.letta.com/blog/memory-blocks ,
https://www.letta.com/blog/benchmarking-ai-agent-memory
VERDICT: WE-HAVE-EQUIVALENT architecture (hot lattice + compression organ +
context packs are a paging system), WE-LACK-ADOPT the API shape: named,
addressable memory blocks (law_block, terrain_block, position_block) that bodies
page in/out beat four ad-hoc tool surfaces; get_law/get_terrain/get_position
should be block-shaped (read one block under budget). Fold into T1.

### S3.2 Zep/Graphiti: bi-temporal edges, invalidation over deletion
What: temporal KG for agent memory: every edge carries valid_time (true in the
world) and ingestion/provenance time; superseded facts are invalidated, never
deleted; episodic/semantic/community subgraphs; the Zep paper reports up to
+18.5% accuracy and ~90% latency reduction vs full-context MemGPT-style baselines
on Deep Memory Benchmark.
Cite: https://arxiv.org/abs/2501.13956 ,
https://github.com/getzep/graphiti ,
https://www.getzep.com/ai-agents/temporal-knowledge-graph ,
https://medium.com/neo4j/graphiti-knowledge-graph-memory-for-a-post-rag-agentic-world-0fd2366ba27d
VERDICT: WE-LACK-ADOPT (the biggest quality steal in this file). The estate KG has
provenance (residual DNA) but lattice edges lack the bi-temporal pair; law rows
supersede by replacement today. Ticket T3: edges gain valid_from + ingested_at +
invalidated_at; get_terrain's family-convergence history becomes a first-class
bi-temporal query; hot-tier promotion/decay can key on invalidation density.

### S3.3 GraphRAG production numbers: refresh drift justifies the standing wave
What: production GraphRAG reports: KGs without automated refresh drift 15-20% from
ground truth per quarter; Microsoft GraphRAG improved comprehensiveness +26% and
diversity +57% vs vector-only retrieval; 2026 production guidance centers on
connected multi-hop traceable context.
Cite: https://tianpan.co/blog/2026/04/09/graphrag-production-when-vector-search-hits-ceiling ,
https://microsoft.github.io/graphrag ,
https://www.paperclipped.de/en/blog/graph-rag-production ,
https://iclr.cc/virtual/2026/poster/10007992
VERDICT: WE-HAVE-EQUIVALENT direction (hot-first + GPS temperature IS a freshness
mechanism), WE-LACK-ADOPT the drift measurement: the lattice needs a quarterly
drift probe (sample law rows, verify against receipts) so hot-tier demotion is
evidence-driven, not vibes. Fold into T3 acceptance criteria.

### S3.4 Lattice/wave-shaped stores: none exist externally
What: searched for standing-wave/lattice-shaped serving stores; nothing outside
the estate names a hot "standing wave over a KG" as a serving tier. The closest
shapes are Letta's block paging (S3.1) and Zep's temporal invalidation (S3.2).
VERDICT: the wave is original estate IP. Nothing to adopt; something to publish.

## S4. Compute-to-asset accounting: everyone meters tokens, nobody meters knowledge

### S4.1 OpenTelemetry GenAI semantic conventions: the field-name standard
What: standardized span attributes gen_ai.usage.prompt_tokens /
gen_ai.usage.completion_tokens / gen_ai.usage.total_tokens plus histogram metrics
for token usage and operation duration; cost is derived by joining token counts
with per-model pricing, not defined in-spec; MCP 2026-07-28 also documents OTel
trace-context propagation in `_meta` (traceparent/tracestate/baggage, SEP-414).
Cite: https://opentelemetry.io/blog/2026/genai-observability ,
https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai ,
https://github.com/open-telemetry/semantic-conventions-genai
VERDICT: WE-LACK-ADOPT (cheap, high leverage). Ledger rows for every pull should
use semconv names for the token fields and carry traceparent as the corr_id wire
form, so the pull ledger exports to any OTel-compatible tool unchanged. Ticket T1.

### S4.2 Stripe Meters: aggregation rules as first-class objects
What: usage-based billing internals: a meter = named aggregation rule over an
event stream (sum/count/max/last/distinct) attached to a price; meter events are
append-only customer actions; v2 Meter Event Stream for high throughput with
idempotency keys and client-side pre-aggregation (Edgee case: billions of
events); usage retrieval is a separate aggregated read over dimensions.
Cite: https://docs.stripe.com/api/billing/meter ,
https://docs.stripe.com/api/v2/meter-event-streams ,
https://stripe.dev/blog/implementing-scalable-metered-billing-with-stripe-how-edgee-handles-billions-of-events
VERDICT: WE-HAVE-EQUIVALENT substrate (usage.jsonl append-only event log +
hermes_burn carrier), WE-LACK-ADOPT the abstraction: named meters over the pull
ledger (tokens_served by coordinate family, by model, by surface; price_usd as a
derived join) instead of per-report ad-hoc sums. Ticket T1 (ledger schema) +
T8-adjacent tooling.

### S4.3 OpenRouter: accounting attached to the response envelope
What: every API response carries a usage object (prompt/cached/completion tokens
and cost) so tracking needs zero extra calls; per-key credit limits act as spend
caps; 402 when credits exhausted; GET /api/v1/key returns per-key usage.
Cite: https://openrouter.ai/docs/cookbook/administration/usage-accounting ,
https://openrouter.ai/docs/api_reference/limits
VERDICT: WE-LACK-ADOPT (small). Every get_context/get_law result should carry
_meta {tokens_served, price_usd_est, coordinate, ttlMs}: the model and the ledger
see the price of the pull in the same envelope. Ticket T1.

### S4.4 Prompt caching economics: the numbers behind the >=5,120 scaffold law
What: cache write 1.25x base input price (2x for 1-hour TTL), cache read 0.1x;
break-even at ~1.39 reads, so a stable prefix reused twice inside the TTL already
wins; up to 4 breakpoints; minimum cacheable prefix 1,024-2,048 tokens; mutating
prefixes make caching a net loss (FinOps warning).
Cite: https://platform.claude.com/docs/en/build-with-claude/prompt-caching ,
https://gingerlabs.ai/blog/prompt-caching-break-even-analysis ,
https://www.finout.io/blog/the-discount-you-now-pay-for-prompt-caching-just-became-a-finops-problem
VERDICT: WE-HAVE-EQUIVALENT (spec-seed law 5 already encodes the threshold from
the DEEPSEEK_API_DOSSIER). External math sharpens enforcement: the lattice's
shared scaffold must be byte-stable (deterministic ordering, S1.2) or the 1.25x
write premium burns on every pull.

### S4.5 Spend tied to KG assets specifically: nobody does it
What: across OTel (per-model token attributes), Stripe (per-customer event
meters), and OpenRouter (per-key credits), every metering standard prices
tokens-per-model-per-caller. None carries a knowledge-asset dimension (which
fact, which graph coordinate, which freshness) in the metered event.
VERDICT: TANGIBLE BOOKS is the novel contribution, not a catch-up item. The
coordinate field in the pull-ledger schema (T1) is the thing the external world
lacks.

## S5. K8s-hosted MCP/context serving: the operator pattern arrives

### S5.1 Kubernetes AI Gateway Working Group (March 2026)
What: k8s project formed an AI Gateway WG; gateway API extensions covering AI
gateways with MCP and agent networking patterns (routing, quota, auth at the
edge for model/context traffic).
Cite: https://kubernetes.io/blog/2026/03/09/announcing-ai-gateway-wg
VERDICT: WE-LACK-ADOPT (deferred). Today's shape (mcp_http.py inside the Docker
Desktop mag namespace) is right-sized for one host. The adoption trigger is
multi-node or off-host swarm members; then mcp_http becomes a Deployment behind
a Gateway CRD. Ticket T8 (trigger-based).

### S5.2 Operator-managed MCP serving exists as product
What: Kong Context Mesh + Kong Operator (deploy an MCP server on an
operator-managed data plane), Red Hat OpenShift MCP Gateway (technology preview,
traffic control between agents and MCP servers at the infra layer), Solo agent
gateway with kagent (A2A + MCP on k8s).
Cite: https://developer.konghq.com/context-mesh/get-started ,
https://www.redhat.com/en/blog/control-your-ai-agent-traffic-scale-model-context-protocol-gateway-red-hat-openshift-now-technology-preview ,
https://www.solo.io/blog/updated-a2a-and-mcp-gateway
VERDICT: ORTHOGONAL to the brain law (K8S_RACTOR: k8s is batch executor, never
the brain), COMPATIBLE with the serving layer: the lattice server is I/O-shaped
(retrieval + compression + ledger), not judgment-shaped, so operator-managed
serving does not violate the verdict. Steal nothing today; cite when the
completion line (docker+k8s) lands.

### S5.3 Toolset selection to shrink context (right-sizing the tool list)
What: containers/kubernetes-mcp-server exposes selectable toolsets so the client
enables only needed Kubernetes functionality, explicitly to reduce context usage.
Cite: https://github.com/containers/kubernetes-mcp-server
VERDICT: WE-HAVE-EQUIVALENT (mcp_server.py --profile builder is the same
mechanism, plus quantized cartridges). External confirmation, no ticket.

## RANKED ADOPTIONS (the tickets)

1. T1 (LAND FIRST, cheap + carries the core law): lattice pull schema as
   protocol-native envelope. get_law/get_terrain/get_position/get_context results
   carry `_meta` with ttlMs + cacheScope (S1.2), tokens_served + price_usd_est +
   coordinate (S4.3), semconv-named token fields + traceparent corr_id (S4.1);
   tools/list deterministic order (S1.2); blocks-shaped surfaces per S3.1;
   Stripe-style named meters defined over the pull ledger (S4.2). This makes
   "every pull = one ledger row" a wire fact, not a convention.
2. T3: bi-temporal lattice edges (valid_from, ingested_at, invalidated_at) +
   invalidation-over-deletion (S3.2) + quarterly drift probe keyed to hot-tier
   demotion (S3.3). Biggest quality steal; feeds get_terrain convergence history.
3. T2: protocol rev 2025-06-18 -> 2026-07-28 in mag/mcp_server.py (stateless
   per-request _meta, server/discover, resultType; keep the old handshake as a
   compatibility path during migration) (S1.1).
4. T4: Tasks extension over the k8s bridge: fan-out dispatches return task
   handles; the operator promote gate maps to input_required + tasks/update (S1.3).
5. T5: contextual prefixes + hybrid retrieval for law rows and corpus chunks;
   target the 49% failure-rate class of gains (S2.3).
6. T6: default get_context budget band 1,000-2,000 tokens (Anthropic sub-agent
   return size) with the >=5,120 scaffold reserved for repeat-call headers (S2.1,
   S4.4).
7. T7: serve the estate skill surface as MCP Skills resources per
   io.modelcontextprotocol/skills (S1.4).
8. T8 (trigger-based): k8s Gateway/Deployment exposure of mcp_http when the swarm
   goes multi-node (S5.1, S5.2).

## THE SURPRISE

The external world independently converged on the estate's own doctrine and
then stopped one step short. Anthropic replaced RAG with just-in-time agentic
search (law 1), MCP went stateless so context-serving scales horizontally and
standardized ttlMs/cacheScope caching plus deterministic ordering for prompt-cache
hits (law 5), Letta shipped paging between hot and cold tiers (law 3), and
every metering standard prices tokens-per-model. But nobody, anywhere in
production 2026, meters the knowledge asset itself: no standard carries a graph
coordinate, a freshness, or a fact identity inside the billed event. TANGIBLE
BOOKS (compute priced against KG assets) is the one leg of the vision with no
external equivalent, which also means no external ceiling to copy.

SOURCE COUNT: 42 distinct cited URLs (byte-counted from this file with
`grep -oE "https://..." | sort -u | wc -l`, 2026-10-02): spec/changelog/extension
pages 8; Anthropic engineering 3; retrieval/context analyses 2; MemGPT/Letta 4;
Zep/Graphiti 4; GraphRAG production 4; OTel 3; Stripe 3; OpenRouter 2; prompt
caching 3; k8s/gateway 4; kubernetes-mcp-server + reference-server repos 3.
