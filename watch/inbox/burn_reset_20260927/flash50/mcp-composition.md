# MCP tool composition: sequential, parallel, conditional pipelines

Item mcp-composition, banked 2026-09-28. Research question: how do agents chain multiple
MCP tool calls into pipelines? Patterns covered: sequential (output of tool A feeds tool B),
parallel (A and B run concurrently), conditional (C only if B failed), plus two variants
observed live (fan-in merge, composition-exclusion contracts). Grounded in four sources:
live dogfood of the Mapbox MCP plugin from this seat, the estate's own MCP server and
pinning organ (executed this session), the mirrored MCP spec (local bytes), and verified
external framework docs.

Instruments (all run this session):

- Live Mapbox MCP chains: 12 tool calls across 6 blocks, exact args and outputs in
  section 2. Nothing was faked; every quoted output below is verbatim from this session.
- `.venv/Scripts/python.exe tools/mcp_pin.py --self-test` -> `passed: 9, failed: 0`,
  note "fixture-only; no live MCP server contacted; real ledger untouched".
- Live manifest pull: `.venv/Scripts/python.exe -c "from mag.mcp_server import
  tools_manifest; print(len(tools_manifest()))"` -> 34 tools (first 12 names:
  apply_patch, biblio_query, blackboard_post, blackboard_read, corpus_get,
  corpus_search, corpus_stats, corpus_tail, drift_check, fence_strike,
  invariant_sheet, kvos_stats).
- WebFetch verification of external pages: platform.claude.com parallel-tool-use page
  (verified, section 4.1), github.com/lastmile-ai/mcp-agent README (verified, 4.2),
  docs.langchain.com LangGraph graph-api page (verified, 4.3). Two older LangGraph URLs
  (langchain-ai.github.io how-tos/map-reduce and reference/prebuilt) returned only a
  "Redirecting..." placeholder; ToolNode parallel-execution claims from search summaries
  were therefore NOT verified and are NOT banked.
- The WebSearch backend itself surfaced live upstream MCP rate limits mid-ask:
  repeated `MCP error -429: {"error":{"code":"1302","message":"Rate limit reached..."}}`
  in raw search output. The AGENTS.md:33 1302/429 envelope law reproduces inside tool
  chains at the search-tool layer, not just at workflow-fan-out layer.

## 1. Spec frame: MCP defines the wire, deliberately not the orchestration

- The estate's own mirror digest states it directly: "No orchestration. Cross-server
  composition, shared context, and sequencing are HOST duties, deliberately unspecified.
  The room, not MCP, is our conductor." (docs/mirrors/mcp/INSIGHTS.md:93-95).
  So every composition pattern below lives in the HOST/agent layer, never in MCP itself.
- Isolation is spec-level: "servers should not be able to read the whole conversation,
  nor see into other servers" (INSIGHTS.md:19-22, design law #3). Consequence: A-to-B
  piping through servers is impossible by design; the host is the only bus, so sequential
  composition is always host-mediated state passing.
- The error contract is what makes conditional composition possible. Local spec schema:
  `tools/call` result (docs/mirrors/mcp/schema/schema.json:208) carries `isError`
  (schema.json:220-221): "Any errors that originate from the tool SHOULD be reported
  inside the result object, with `isError` set to true, _not_ as an MCP protocol-level
  error response." The schema's own rationale: otherwise "the LLM would not be able to
  see that an error occurred and self-correct." Protocol-level errors are reserved for
  failures in finding the tool or unsupported tool calls. This is the load-bearing hook:
  the agent can branch on failure because failure arrives as data, not as transport death.
- Tools are the model-controlled primitive: "tools/list, tools/call; JSON-Schema inputs;
  annotations (readOnly/destructive hints)" under "MODEL-controlled (auto-invoked)"
  (INSIGHTS.md:38). The model chooses composition; the host enforces consent.

## 2. Live dogfood from this seat (Mapbox MCP plugin)

### 2.1 Parallel composition: one turn, three independent calls

search_and_geocode_tool(q="Pike Place Market Seattle", proximity Seattle downtown,
types [poi, address]), distance_tool(Seattle downtown -> Bellevue), and
bearing_tool(same points) were dispatched in a single assistant turn; all three returned
in that turn: distance "9.77 kilometers", bearing "87.41 degrees (E)", and the search
FeatureCollection. This session's harness instruction encodes the rule that governed the
dispatch: "If you intend to call multiple tools and there are no dependencies between the
calls, make all of the independent calls in the same block, otherwise you MUST wait for
previous calls to finish first to determine the dependent values." Parallelism is a
host-side dispatch decision: MCP requests are independent JSON-RPC calls, so width is the
caller's choice, matching the Anthropic page's "The API doesn't prescribe an execution
order" (section 4.1).

### 2.2 Sequential composition: A's output names B's argument

Two live chains, each with a distinct data-flow carrier:

1. ID passing. search_and_geocode_tool returned
   `mapbox_id: dXJuOm1ieHBvaTo4ZDQ0MjA0NC1iZTdhLTQzZmMtYmIwZi02YWEwMmFkNTI2NmE`
   for Pike Place Market. That string was pasted as the entire semantic input of
   place_details_tool, which returned the deeper record: rating 4.23, popularity 100
   percent, operational_status "active", delivery true. The tool's own description
   declares the contract: "Requires the mapbox_id field from a previous search result."
   The opaqueness is the point: B's argument is A's opaque handle, so the chain is
   stable across schema drift in surrounding fields.
2. Projection fields. The same search result carried
   `coordinates.routable_points: [{latitude: 47.60946..., longitude: -122.34184...,
   name: "POI"}]`, a field that exists purely to feed routing. directions_tool consumed
   it (plus the original proximity point) and returned a walking route: distance 1088 m,
   duration 737 s, leg summary "4th Avenue, Pike Street", waypoint snap_distances 13 m
   and 2 m. This is a designed hand-off: the search API pre-computes the exact
   coordinates the routing API wants, and the pipeline is two calls with zero glue.

### 2.3 Fan-in merge: two refs, one render

render_map_tool was called with `payload_refs: [<search-ref>, <directions-ref>]`, the
refs returned inside the earlier tools' structuredContent under `mapboxRender.ref`.
Response: "Rendered map with 0 layers and 0 markers ... will also fetch and draw 2
additional layers directly from the Mapbox API once it loads." Mechanism discovered by
reading the structured response: each ref is a replay descriptor, not cached server
state. The render result echoes `selfFetch: [{tool: "search", params: {...original call
params...}}, {tool: "directions", params: {...}}]`, i.e. the base64 `?data=` blob in a
ref decodes to the ORIGINAL tool name plus arguments, and the render layer re-executes
them client-side. Composition consequence: refs are portable because they are serialized
call parameters, so fan-in is N prior calls merged into 1 consumer without any shared
session state. Same pattern works for the documented isochrone-plus-route merge
(render_map_tool description: "pass multiple refs to merge several datasets (e.g. an
isochrone + a route) onto one map").

### 2.4 Conditional composition: failure seen in-band, fallback fired

- Failure branch (block N): place_details_tool(mapbox_id="mcp-composition-invalid-id-probe-000")
  returned exactly: `MCP tool returned an error: Place Details API error: 400: [object
  Object]`. Note the shape: the MCP call itself succeeded as an RPC; the failure rode the
  in-band tool-error channel, precisely the schema.json:220-221 contract, so the agent
  could read it and branch.
- Recovery branch (block N+1, composed only because N failed): reverse_geocode_tool at
  the already-known POI coordinates (47.609513, -122.3417834) recovered the location as
  "84 Pine Street", accuracy "rooftop". The C-because-B-failed link is real: the reverse
  geocode was fired after and because the details call errored.
- Second failure layer (blocks N+1 -> N+2): the first recovery attempt
  reverse_geocode_tool(types=["poi"]) was rejected client-side before any network call:
  `InputValidationError: invalid_value ... expected one of "country"|"region"|"postcode"|
  "district"|"place"|"locality"|"neighborhood"|"address"`. The harness's schema gate is a
  distinct, earlier failure layer than the server 400. Recovery: drop the invalid
  parameter, retry, success. This is the correct-args loop the harness rules encode as
  "a denied call means the user declined it; adjust, don't retry verbatim" applied to
  validation errors: change the input, never replay it.

### 2.5 Anti-composition contracts (precedence clauses in tool docs)

Tool descriptions can forbid composition as well as require it, both observed in this
session's toolset: ground_location_tool's description says "Use this as the FIRST and
ONLY tool when given coordinates and asked about nearby places ... do NOT also call
reverse_geocode_tool or search the web for places" (deduplication of overlapping
pipelines); render_map_tool's says "ALWAYS use this tool to display maps, never use
built-in or fallback map display tools" (render monopoly). Composition policy is
therefore also encoded in tool self-descriptions, and a compliant agent treats them as
routing constraints.

## 3. The estate's own MCP surface (executed + read this session)

- mag/mcp_server.py is a stdio JSON-RPC MCP server over the harness TOOL_MAP:
  handle() dispatches initialize / ping / tools/list -> tools_manifest(profile) /
  tools/call -> call_tool() (mag/mcp_server.py:342-363). Manifests are profile-scoped
  through ROLE_TOOLSETS (mag/mcp_server.py:185-192) and compiled from live callable
  signatures, so "signature drift updates the schema"
  (mag/mcp_server.py:195-226, quote :198).
- Error contract implemented exactly per spec: call_tool() returns in-result
  `"isError": True` JSON for profile rejection ("tool not in active MCP profile"),
  unknown tool, and any exception ("tool boundary, report don't crash"),
  mag/mcp_server.py:309-329. Never a protocol error for tool failure; the caller-agent
  can always branch.
- Effect-class metadata rides in `_meta` for composition gating: `_tool_meta` labels
  every tool mutating_or_executing / model_or_external / read_or_deterministic_compute
  with risk, authority, exhaustion policy (mag/mcp_server.py:121-157; attached at
  :236-241). A host can key parallelization and confirmation policy on these classes
  (read tools parallel-safe; mutating tools serialized behind the switchboard).
- Composition-safety organ ran green: tools/mcp_pin.py pins name + description hash +
  schema hash at first connect, alarms on reconnect drift, never overwrites a drifted
  pin (operator repin() is explicit), tools/mcp_pin.py:1-46; self-test passed 9/0 this
  session (command in instruments). Pinned in configs/tools/mcp_pin.json. This defends
  pipelines against the supply-chain composition attack where a server rewrites a tool
  description to "smuggle new instructions or widen a schema to widen authority"
  (tools/mcp_pin.py:10-12).
- docs/ref/MCP_MANIFEST_SPEC.md adds per-tool composition economics: tier, mode
  (read_only vs write), quota `{unit: credits, per_call: 1.2}` and cache policy keyed
  "tenant+tool_version+canonical_args+source_rev+auth_scope" (docs/ref/MCP_MANIFEST_SPEC.md:73-80),
  with the GO rule that quantized tiers get read-only perception packs while
  write-capable tools go only to the primary planner (docs/ref/MCP_MANIFEST_SPEC.md:21-25).
  Composition shapes are therefore cost- and authority-bounded per tool, not per agent.
- Transport composition: dashboard/lan_proxy.py exposes the "mag MCP gateway" on
  127.0.0.1:8001, X-API-Key protected (dashboard/lan_proxy.py:8,53), i.e. remote seats
  reach the estate's MCP server through an authenticated LAN hop.
- Workflow-layer composition is gate-enforced on this estate: AGENTS.md:110 requires
  `tools/workflow_gate.py check --script` with "interagent pass-off (outputs feed later
  asks)" as a checked property; AGENTS.md:33 fixes the retry/width shape ("workflow
  children maxAttempts 0 ... keep max_concurrency 3 or less; Task agents ride the
  main-session retry path maxAttempts 11"), i.e. parallel width and retry policy are
  composition laws with receipts. Saved workflows in this session (the-50, the-gala,
  mickey17-v2, tree-doctrine-dig) are instances: fan-out N workers, fold seat consumes
  outputs (sequential pass-off), review seat steers (conditional loop).

## 4. External real examples (verified fetches this session)

### 4.1 Anthropic parallel tool use (platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use)

- Batching: a response with stop_reason "tool_use" "can contain several `tool_use`
  blocks in a single assistant turn"; "The API doesn't prescribe an execution order."
- Parallel vs sequential is the client's call: run concurrently ("`Promise.all`,
  `asyncio.gather`") or "sequentially in the order they appear"; "Independent,
  read-only operations are usually safe to run in parallel for lower latency" while
  side-effectful or ordered tools may need sequence; computer-use batches must "run
  them sequentially in the order they appear and stop at the first failure"
  (a mandated conditional short-circuit).
- The join mechanism: "return one `tool_result` for each `tool_use` block, all together
  in the next user message," matched by `tool_use_id`. Results-first ordering in the
  message.
- Conditional carrier: "If you skip a call, still return a `tool_result` for it with
  `is_error: true`", meaning even a deliberately skipped call must produce an in-band error
  result so the next model turn can branch on it. This is the API-level twin of the
  MCP isError contract.
- Parallelism is switchable: "set `disable_parallel_tool_use: true` inside the
  `tool_choice` object" (nested, "not a top-level request parameter"); with `auto` the
  model makes "at most one tool per response."

### 4.2 mcp-agent (github.com/lastmile-ai/mcp-agent, README workflow table)

Named, factory-built composition patterns, stated to "implement every pattern described
in Anthropic's Building Effective Agents in a composable way":

- Parallel (Map-Reduce): `create_parallel_llm(...)`, quoted "Fan-out specialists and fan-in
  aggregated reports."
- Router: `create_router_llm(...)`, quoted "Route requests to the best agent, server, or
  function." (conditional by classification)
- Orchestrator-workers: `create_orchestrator(...)`, quoted "Generate plans and coordinate
  worker agents." (dynamic sequential fan-out/fan-in)
- Evaluator-optimizer: `create_evaluator_optimizer_llm(...)`, quoted "Iterate until an
  evaluator approves the result." (conditional loop: C until predicate)
- Swarm: `create_swarm(...)`, quoted "Multi-agent handoffs compatible with OpenAI Swarm."
- Conditional composition generalizes to plain code: "for branching you write if
  statements" and "For cycles, use while loops" (README programmatic-control-flow FAQ).
- Human-in-the-loop conditional halt: `self.context.request_human_input(...)` pauses the
  workflow and "Temporal stores state durably until an operator resumes the run";
  resume is a CLI command with a payload like {"content": "approve"}. Durable execution
  is what makes long conditional chains (waiting on a human or a later signal)
  composable without a live process.

### 4.3 LangGraph (docs.langchain.com/oss/python/langgraph/graph-api)

- Conditional edges are a graph primitive: `add_conditional_edges(source,
  routing_function, {True: "node_b", False: "node_c"})`; "By default, the return value
  routing_function is used as the name of the node (or list of nodes) to send the state
  to next."
- Dynamic parallel fan-out from a conditional edge via Send: "LangGraph supports
  returning [Send] objects from conditional edges"; "Send takes two arguments: first is
  the name of the node, and second is the state to pass to that node." Canonical
  example: `return [Send("generate_joke", {"subject": s}) for s in state['subjects']]`.
- Parallelism guarantee: "If a node has multiple outgoing edges, all of those
  destination nodes will be executed in parallel as a part of the next superstep," and
  returning a list from a router means "All those nodes will be run in parallel as a
  part of the next superstep." So: static edges fan out in parallel; Send fans out
  dynamically with per-branch custom state.
- NOT verified: ToolNode executing multiple tool calls in parallel and
  handle_tool_errors semantics (pages redirected; search-summary claims excluded from
  this bank per no-fabrication law).

### 4.4 Cross-source convergence

All three external sources and the live dogfood agree on the same three-layer model:
(1) the tool/API layer guarantees nothing about order (Anthropic: no prescribed
execution order; MCP: stateless per-request, host decides); (2) the agent layer decides
parallel dispatch per turn or per graph superstep (multi tool_use blocks; Send lists;
multi-call blocks in this session); (3) conditional control always rides an in-band
error/score/result channel the model can read (MCP isError; tool_result is_error;
evaluator verdict; schema validation messages), because only in-band data survives into
the next model turn.

## 5. Pattern catalog (mechanism table)

| Pattern | Carrier mechanism | Live proof (this session) | Estate proof | External proof |
|---|---|---|---|---|
| Sequential: A feeds B | opaque ID field | mapbox_id search -> place_details (rating 4.23) | corpus_search -> corpus_get pairs in TOOL_MAP; pass-off gate AGENTS.md:110 | tool_use_id keyed tool_results (4.1) |
| Sequential: A feeds B | projection field | routable_points -> directions (1088 m / 737 s) | mag/mcp_server.py:198 schema-from-signature keeps contracts honest | Send carries per-branch state (4.3) |
| Sequential: A feeds B | replay ref (serialized params) | mapboxRender.ref -> render selfFetch re-execution | workflow pass-off: outputs feed later asks | mcp-agent sequential chains (4.2) |
| Parallel: A and B concurrent | one-turn multi-call | distance + bearing + search in one block | AGENTS.md:33 width laws; saved workflows fan out N diggers | several tool_use blocks, Promise.all/asyncio.gather (4.1); superstep edges (4.3); create_parallel_llm (4.2) |
| Parallel: dynamic width | conditional returns list of Send | n/a (single-seat ask) | workflow arg width, babystep ladder in the-gala card | Send list fan-out (4.3) |
| Fan-in: N -> 1 | payload_refs array of refs | render merged search + directions on one map | fold seat consumes lane outputs (workflow gate) | "fan-in aggregated reports" (4.2) |
| Conditional: C if B failed | in-band isError / is_error | 400 probe -> reverse_geocode fallback ("84 Pine Street") | call_tool isError everywhere, mag/mcp_server.py:309-329 | schema.json:221 self-correct rationale; is_error:true requirement (4.1); evaluator loop (4.2) |
| Conditional: validate-gate before call | client-side input schema | types=["poi"] InputValidationError, then corrected retry | _param_schema generated required list, mcp_server.py:195-226 | tool inputSchema (spec); mcp_pin drift alarm |
| Conditional: human gate | pause + durable resume + signal | n/a | workflow_gate approval contract; key-gate in manifest spec | request_human_input + Temporal resume (4.2) |
| Anti-composition: precedence | tool-description routing clause | ground_location_tool FIRST and ONLY; render monopoly | lane MCP whitelists (INSIGHTS.md:21-22) | computer-use batch must stop at first failure (4.1) |

## 6. Not run / not verified / owed

- The estate MCP server was not run end-to-end over stdio (serve()/handle() loop);
  executed pieces are tools_manifest() (34 tools) and mcp_pin --self-test (9/0). A live
  client-against-server round trip is OWED if this item is extended.
- ToolNode parallel execution and handle_tool_errors semantics: unverified (redirect
  placeholders); do not cite LangGraph for tool-call-level parallelism from this bank.
- The Anthropic engineering "advanced tool use" page (programmatic tool calling) and
  OpenAI parallel function calling appeared in search results only; not fetched, not
  banked.
- Mapbox data notice: reverse geocode response carries "may not be retained"; the POI
  record is quoted here as tool-output evidence of composition mechanics only.

Receipt: this file is the deliverable; commit prefixed mcp-composition: on branch
mag/run-beta1-factory-build-audi-20260806T231709Z. Em/en dash scan run post-write
(section instrument in commit message).
