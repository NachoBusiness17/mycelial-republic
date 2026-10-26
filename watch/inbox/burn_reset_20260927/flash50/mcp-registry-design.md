# MCP TOOL REGISTRY DESIGN (mcp_registry.v1) - flash50 item mcp-patterns, 2026-09-28

Ask: design the estate's MCP TOOL REGISTRY, one config file declaring every
available MCP tool (name, surface, inputs, outputs, cost, tier) so the context
pack can present the right tools to each seat, with tier-gating (free lanes
get free tools, funded lanes get all tools). Deliver: schema, sample,
composition pattern.

## 0. Rib check: what already exists (read before designing)

The estate has four MCP organs. This registry does not replace any of them;
it is the missing fifth piece, the composition index they all implicitly
assume but no file provides.

| Organ | File | What it does | What it lacks |
|---|---|---|---|
| Pack manifest spec | `docs/ref/MCP_MANIFEST_SPEC.md` (v0.1, SPEC DRAFT, no enforcement organ, its own TRI-STATE) | per-server pack manifests `mcp.pack.manifest.v1`, epoch pinning, perception/hands tiering, quota gate, fail-close | one file per server, requires authoring per pack; no cross-server index; no funding tiers |
| House MCP server | `mag/mcp_server.py` (410 lines) | serves `tools.TOOL_MAP` over stdio; ROLE_TOOLSETS personas (`mag/mcp_server.py:47`); `_tool_meta` effect_class/cost_kind (`mag/mcp_server.py:121`); quantized cartridges | projects ONE server (mag); no external surfaces; no funding concept |
| Schema pin + drift alarm | `tools/mcp_pin.py` (488 lines, `mcp_pin.v1`) | pins name+description+inputSchema hashes at first connect, alarms on drift, repin() is the only past it (`tools/mcp_pin.py:134`) | ledger only; does not decide who SEES a tool |
| Lane whitelists | `queue/lanes/<name>/manifest.md:4` (seven lanes, grepped 2026-09-28) | per-lane `mcp_whitelist:` lines (day_work: mag, web_reader; research: mag, browser_use, node_repl; elder: mag, web_reader, image_search; ...) | bare names, no cost, no tier, no context-pack presence |

Related cost/config ground: `configs/lanes.yaml` (L0 local ollama, L1
free_remote, L2 specialist, L3 human; hermes block), `configs/cost_rates.yaml`
(schema cost_rates.v2; glm-4.7-flash and glm-4.5-flash carry `free: true`,
`configs/cost_rates.yaml:25,29`), `configs/spend_overlay.yaml`
(spend_overlay.v1: "the layers no receipt stream can see"; groq free tier
"100 calls / 100K tok per day"), `configs/data_tiers.yaml` (data sensitivity
T0-T3, orthogonal to tool tiers), and the MCP spec mirror at
`docs/mirrors/mcp/` including `spec/2026-07-28/server/tools.mdx`.

The 2026-08-26 operator GO (`docs/ref/MCP_MANIFEST_SPEC.md:17-27`) already
named the requirements the registry inherits: epoch-pinned byte-stable
manifests, read-only perception packs for quantized tiers, write-capable
tools only for the primary planner, quota gate on per-call credit weights
("web search 1.2 credits/call"), fail-close on unknowns.

## 1. The two-axis model

The ask's "tier" conflates two things that must stay separate axes, because
the estate already enforces them differently:

- **Funding tier** (who pays, what the ladder allows): `free` < `funded` <
  `operator`. Grounded in the DRIVING LADDER (AGENTS.md, 2026-09-28):
  "Free stealth lanes are a SENSING surface only - their outputs are banked
  as findings, never as done/trusted work; verification climbs to the funded
  tier. ONLY Hermes is funded ($180 Nous credits: glm-5.3-prime /
  qwen3.8-max-prime)." Maps onto lanes.yaml: L0/L1 -> free, L2/hermes ->
  funded, L3/operator seats -> operator.
- **Mode** (what the tool does to the world): `perception` (read_only) |
  `hands` (write-capable). Carried VERBATIM from MCP_MANIFEST_SPEC.md
  sections 2 and 4 ("Quantized tiers never get hands", refusal at spawn not
  a runtime warning).

Two axes, because funding gates COST while mode gates DANGER. A free lane may
read the world with free tools but must never get hands regardless of funding
(manifest spec section 4); a funded lane gets all costs but still only the
hands its lane whitelist names.

## 2. Cost classes

Six declared classes, each grounded in an existing instrument:

| class | meaning | ground |
|---|---|---|
| `free-local` | deterministic local compute, $0 marginal | cost_rates.yaml seats.ollama `$0 marginal`; mag/mcp_server.py:121 cost_kind `deterministic_local` |
| `web-free` | public network read, no billed quota | web_reader, mapbox-docs fetches, image search |
| `api-metered` | billed per call/service | Mapbox Directions etc.; mcp_server.py cost_kind `unknown_until_metered` until the economist prices it |
| `quota-pooled` | consumes a plan quota pool sized for judgment | the GO's own example: web search 1.2 credits/call (MCP_MANIFEST_SPEC.md:23,79-81); groq 100 calls/day |
| `inference` | rides a model call | price = cost_rates.yaml model_rates join |
| `unmetered` | no weight known | FAIL-CLOSE: "unknown cost is a denial, not a free pass" (MCP_MANIFEST_SPEC.md:78-79); gate refuses until metered |

Empirical proof of the free-local / api-metered split, run this session:
`mapbox.distance` (tool description: "Works offline without API calls")
returned 3935.752 km NYC->LA instantly with no route service involved;
`mapbox.directions` is a Mapbox billed service per
docs.mapbox.com/api/navigation/directions (confirmed via the mapbox-docs
search tool this session). The split is real, not cosmetic.

## 3. Schema (mcp_registry.v1)

One file, `configs/mcp_registry.yaml`, canonical YAML. Sections:

- `schema`, `updated`
- `census` - declared-vs-live tool counts with the source of the live number;
  a row exists only when a live tool backs it (never padded)
- `tiers` - free/funded/operator with `rank`, `maps_lanes` (lanes.yaml ids),
  `seats`, `cost_classes` (allowed), `mode_max`, `law` (the doctrine line)
- `classes` - the six cost classes with one-line meanings
- `servers` - surface declarations: id, kind (house-stdio | hosted-mcp |
  node-kernel | planned), launch/tool/prefix, auth, lane-pin note
- `tools` - the rows. Required per row: `name` (namespaced), `server`,
  `funding_min`, `mode`, `cost` (with `class`; optional `per_call`/`unit`/
  `basis`), `inputs` (one-line summary), `outputs` (one-line summary).
  Optional: `gate` (extra admission condition, e.g. operator-explicit ask),
  `lane_pin` (lane whitelist that must also name it), `status: planned`,
  `evidence` (why the cost class is what it says).
- `composition` - context_pack hook (section 6), render rule, call rule
- `gates` - fail-close, refusals, pin_join, pack_join, budget_join

Field-law notes:

- inputs/outputs are ONE-LINE summaries, never full JSON Schema. Full schemas
  already live at the source (house: `_param_schema` compiled from signatures,
  mag/mcp_server.py:196; external: the tools/list the client already holds).
  The registry is the index, not a second schema to drift. The schema-drift
  referent stays mcp_pin.v1 (hash pins), keeping byte-stability in ONE place.
- A planned tool still declares inputs/outputs (the intended contract) and
  carries `status: planned`; only operator-tier renders include planned rows.
- Unknown tier, unknown server, unknown class: the row fails validation and
  is never presented (fail-close, carried from MCP_MANIFEST_SPEC.md:145-147).

## 4. Sample + validator (both ran green this session)

Files banked beside this doc:

- `mcp_registry.sample.yaml` - 8 server surfaces, 25 tool rows, all real
  (house mag read/hands rows, mapbox free-local math + api-metered services +
  hands style admin, web_reader, image_search, mimosa, android, node_repl,
  zai.web_search planned with the GO's verbatim 1.2 credits/call weight).
- `mcp_registry_check.py` - validator: top-level sections, per-row required
  fields, referential integrity (servers/tiers/classes), tier-gate
  invariants, per-tier render + budget fit.

Command run and result (venv python 3.11.15):

```
.venv/Scripts/python.exe watch/inbox/burn_reset_20260927/flash50/mcp_registry_check.py \
    watch/inbox/burn_reset_20260927/flash50/mcp_registry.sample.yaml
-> ok: true, 25 checks passed, 0 failed
   renders: free 8 tools / 324 chars, funded 22 / 918, operator 25 / 1073
```

The first run FAILED 1 of 24 checks and the failure was kept as evidence the
validator is not theater: `zai.web_search` shipped without inputs/outputs
(caught by rows_complete). The same run also exposed a false pass in my own
budget check (budgets keyed by pack mode never matched tier render keys, so
`0 <= 400` passed vacuously); budgets were re-keyed to tiers and a
render_nonempty guard added so a vacuous block can never pass again.

Tier-gate invariants enforced (and green):

- `free_gets_free_only`: funding_min free -> mode perception AND class in
  {free-local, web-free} (the ask's rule: free lanes get free tools)
- `hands_never_free`: mode hands -> funding_min funded or operator
- `unmetered_operator_only`: class unmetered -> funding_min operator
- `free_block_smallest`: free 8 <= funded 22 <= operator 25

## 5. Live census (the honest denominator)

Counted from this session's own live tool list, 2026-09-28:

| surface | tools |
|---|---|
| mapbox core | 31 |
| mapbox-devkit | 22 |
| mapbox-docs | 3 |
| web_reader | 1 |
| mimosa | 5 |
| android_emulator | 23 |
| image_search | 1 |
| node_repl (browser/computer kernel) | 1 |
| external subtotal | 87 |
| house mag (`python -m mag.mcp_server --list`, run this session) | scout 17 / full 34 |
| total live | 121 |

The sample declares 25 of 121 rows. The remaining ~96 rows are a mechanical
fill-in (name/server/class/mode per live descriptor), declared OWED in
section 8, not invented here. `_mcpatterns_scout.json` in this directory is
the raw scout-profile --list receipt.

## 6. Composition pattern (how a seat gets the right tools)

Three joins, each verified to exist today:

1. **Registry -> context pack.** `mag/context_pack.py` `build_context_pack`
   (line 571) assembles gated sections off MODE_CONFIG flags
   (`include_resonance` gate at line 651, `include_skills` at 685). The
   registry adds one more: `include_mcp_tools` + `budgets_chars`, and a
   `mcp_tier` key resolved from the seat's lane via `lane_map`
   (L0->free, L1->free, L2/hermes->funded, L3->operator). Renderer emits one
   line per visible tool, name + cost class + verb phrase
   ("mapbox.directions [api-metered] route/ETA"; hands rows marked "writes
   state"). Input schemas are never rendered into the pack: the token tax of
   schemas belongs to the client's own tools/list, and this estate's pack
   budget law (janitor 1200 chars total, context_pack.py:57) cannot carry it.
   Measured block sizes fit the sample budgets: 324/918/1073 chars.
2. **Registry -> lane whitelist.** The pack block is PRESENTATION; admission
   stays two-keyed: a seat may call a tool only if the tier block presented
   it AND the lane's `mcp_whitelist` names its server
   (queue/lanes/<name>/manifest.md:4, seven lanes). Presentation without
   admission would repeat mcp_server.py:43's own warning: these are
   capability projections, not permission sets.
3. **Registry -> gates.** pin_join: a tool whose surface drifts at reconnect
   (mcp_pin.v1 DRIFT verdict) is dropped from presentation until repin()
   ("Senses EXPIRE; nothing whitelists forever", mcp_pin.py:13). pack_join:
   when MCP_MANIFEST_SPEC pack manifests are authored, a row may carry
   `pack: <pack_id>@<epoch_sha256_16>` and the spawn check verifies the pin
   (manifest spec sections 3 and 8). budget_join: the pack prices, the lane
   pays (manifest spec section 5); spend surfaces through spend_overlay.v1.

Fail-close, inherited whole: unknown tool/tier/class -> not presented; called
anyway -> refuse + receipt. A lane whose whitelist names an undeclared server
fails validation loudly rather than rendering an empty block.

## 7. Tier-gating summary (the ask's core rule, restated as law)

- free seat: sees only free-local/web-free perception tools (8 in the
  sample). Its outputs are findings, never done work (DRIVING LADDER). It
  pays nothing, so it risks nothing the estate cannot afford.
- funded seat: sees all cost classes and hands-level tools that its lane
  whitelist names (22 in the sample). This is "funded lanes get all tools",
  with the manifest spec's hands discipline (planner-only) intact.
- operator seat: sees everything including unmetered and planned rows
  (25 in the sample). Only the operator can admit an unmetered tool, because
  only the operator can decide to eat an unknown cost.

## 8. OWED (declared, not done)

- O1: full census fill-in, ~96 remaining rows from the live 121, mechanical
  descriptor-to-row mapping per surface. The 25-row sample plus the census
  block is the honest increment landed today.
- O2: quota weights for api-metered tools (Mapbox per-service pricing, z.ai
  suite weights beyond the GO's 1.2) are Unproven until metered, same
  tri-state the manifest spec already carries for its own weights.
- O3: `include_mcp_tools` wiring in mag/context_pack.py MODE_CONFIG is
  designed (section 6) but not coded in this item; this is a design+sample
+composition ask, not a build ask.
- O4: zai_suite row is `status: planned` against the 2026-08-26 GO; the four
  z.ai servers are not connected in this session (nothing here verifies them
  live).

## 9. Files banked (this directory)

- `mcp-registry-design.md` = `mcp-patterns.md` (byte-identical, this doc)
- `mcp_registry.sample.yaml` (25 rows, validator-green)
- `mcp_registry_check.py` (25-check validator, exit 0 on the sample)
- `_mcpatterns_scout.json` (house server --list scout-profile receipt)

Checks run this session: validator (above), house `--list` scout/full counts,
mapbox.distance live probe (3935.752 km), mapbox-docs search for the
Directions pricing page, em/en dash scan of the banked docs via venv python
(result recorded in the commit message).
