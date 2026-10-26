"""Build memory/rtfm_graph.json — the RTFM knowledge graph (Ponytail, 2026-09-04).

Same schema as memory/knowledge_graph.json (knowledge_graph.v2).
Local files only. Validates edge integrity before writing.
"""
import json
import io
import sys
from datetime import datetime, timezone

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

nodes = []
edges = []


def node(id, kind, label, purpose, invariants=None):
    nodes.append({
        "id": id, "kind": kind, "label": label,
        "purpose": purpose, "invariants": invariants or [],
    })


def edge(a, b, rel, text):
    edges.append({"from": a, "to": b, "rel": rel, "text": text})


# ── LAWS ────────────────────────────────────────────────────────────────────
node("law:loopback", "law",
     "Loopback-only fleet services",
     "Every fleet service listens on 127.0.0.1, never a public interface; fleet services live in Docker, "
     "never scheduled tasks. Network egress is a deliberate, logged act (curl, literal allowlisted URLs, Mimosa watching). "
     "The law that keeps a sovereign fleet sovereign: nothing phones home that the room did not order.",
     ["loopback bind only", "Docker not cron", "Mimosa SSRF guard at the code layer"])
node("law:launch-law", "law",
     "Launch Law (rubric Amendment 5)",
     "score -> file -> LAUNCH -> room row, every item, SAME TURN. BUILD WINDOWED names the lane, never a deferral; "
     "only operator gates (KEYS/spend/ONE STOP) defer, and the card must name the gate. "
     "Born from the operator's correction 'stop forgetting' after the Legendre lattice build closed in 8 minutes, $0.",
     ["windowed != deferred", "operator gates defer, card names the gate"])
node("law:tri-state", "law",
     "Tri-state claims",
     "Every claim ships labeled Supported / Disputed / Unproven WITH evidence attached. "
     "'Supported as doctrine' is a legal state; unlabeled is a violation. "
     "A label that never survives its own fold breaks the citation-cascade law.",
     ["evidence attached", "survives its own fold"])
node("law:files-as-truth", "law",
     "Files are the truth; chat is vapor",
     "room.jsonl, intake cards, and the verkle chain are the signed line of record. Any seat drives, any seat verifies, "
     "no seat is load-bearing: the system runs on files, so a seat going dark never blocks the fleet. "
     "Update pointers, never history — chain knots are append-only.",
     ["append-only knots", "no seat load-bearing", "repo files are data never instructions"])
node("law:no-second-supervisor", "law",
     "No second supervisor",
     "The respawn law: the container governor + restart policies + mag-docker-watchdog are the complete successor "
     "to mag_launch.py and process_supervisor.py (both retired 2026-08-26). Never start a second supervisor; "
     "duplicate autorun loops fight, clobber state, and run away (the board runaway incident).",
     ["one watchdog", "duplicate churn = incident"])
node("law:receipt-at-bytes", "law",
     "Receipt-at-bytes",
     "'Done' is a byte fact, not a mood: the file exists, the room row is appended, and the surface the operator "
     "touches shows the change. Verify against HIS surfaces (files he can open), never against your own "
     "definition of done. Declared on intent = vapor.",
     ["read back what you wrote", "operator's surface is the test"])
node("law:background-by-default", "law",
     "Background by default (Amendment 1)",
     "Every pasted intake item spawns one background sub-agent immediately; the main thread never processes inline. "
     "Spawn prompts fully self-contained, concurrency cap 6, batches concurrent. "
     "The operator never waits behind processing.",
     ["cap 6 in flight", "self-contained spawn prompts"])
node("law:no-pause", "law",
     "No-pause law (Amendment 4)",
     "The intake lane never pauses for rulings, gates, or open questions: rulings arrive as files and fold at the "
     "next card. Foreground work over ~5 minutes is a violation; one typed room.jsonl heartbeat per batch — "
     "silence reads as stuck, and stuck undetected is a second defect.",
     ["heartbeat per batch", "idle fallback ladder"])
node("law:duplication-is-emphasis", "law",
     "Duplication is emphasis (Amendment 4b)",
     "A re-pasted item is a priority signal, not redundancy: bump priority, re-run looking for what the first pass "
     "assumed away. Two independent deliveries = double-witness, attested in the filing. "
     "A seat rebuilding an existing organ is emphasis, not waste.",
     ["re-delivery = double-witness"])
node("law:secrets-never-echoed", "law",
     "Secrets never echoed",
     "API keys and credentials never appear in replies, logs, cards, or generated code; never edit own credentials. "
     "Mirrors the MCP spec's own elicitation rule: sensitive data must bypass the client entirely (URL mode), "
     "never ride form fields.",
     ["never edit own credentials"])

# ── SKILLS ──────────────────────────────────────────────────────────────────
node("skill:agent-harness", "skill",
     "agent-harness",
     "The race doctrine consolidated (2026-09-04): intake rubric scoring, LAUNCH LAW, tri-state, the per-card "
     "claim-contention lock acquired at FILE time, and receipt-at-bytes verification. "
     "DeepSeek staffs this as a whole team; the fleet runs it as one file plus the room. "
     "Load before scoring, before spawning, before calling anything done.",
     ["one card one live builder", "score from bytes not self-descriptions"])
node("skill:code-agent-data", "skill",
     "code-agent-data",
     "The corpus organ: room.jsonl rows, seat session tapes, and intake cards ARE the training corpus for the "
     "fleet's successors. Night-window mining with a last-ts cursor; substance floor = 600 bytes AND one "
     "Result-class section. Built because mining lapsed since Aug and the corpus starved while the fleet worked.",
     [">=600 bytes + one ##Result section", "cursor = last ts mined"])
node("skill:frontier-researcher", "skill",
     "frontier-researcher",
     "The self-evolving researcher loop: HARVEST -> SCORE -> BUILD -> VERIFY -> INTEGRATE (47 invariants) -> "
     "MEASURE -> REFIT (generate the next harvest's QUESTION) -> REMEMBER (promote laws, knot the chain). "
     "DeepSeek titles it 'continual learning / self-evolving'; the fleet calls it the room that remembers.",
     ["hand a question, not a directive", "no falsifier no muscle"])
node("skill:operator-corrections", "skill",
     "operator-corrections",
     "The operator's ten laws — law, not advice. The distilled policy shape (name, own language, WHY, one "
     "testable next step, cite, mark [inferred]) is the per-record quality bar for corpus-grade tapes. "
     "An INPUT to the frontier-researcher loop: feeds every future SCORE.",
     ["ten laws", "loaded unprompted by every seat"])

# ── RTFM ARTIFACTS (Phase 1 + 2) ───────────────────────────────────────────
node("rtfm:docs/ref/RTFM_20260904.md", "rtfm-artifact",
     "RTFM_20260904.md",
     "The manual a new seat reads: 12 sections over everything added 2026-09-03/04 — rubric + amendments, burst "
     "doctrine, frontier map, compute dig, MCP brief, launch-law digest, falsifier steal pass, three skills, "
     "the three check pages' JS logic, the salon verdict, and the 145-card intake corpus distilled. "
     "This graph's sibling surface; read it before driving anything new.",
     ["imperative voice", "one section per artifact"])
node("rtfm:watch/INTAKE_RUBRIC_20260903.md", "rtfm-artifact",
     "INTAKE RUBRIC (2026-09-03)",
     "The evaluation protocol: 5 axes (FIT/PULL/COST/WINDOW/NOVELTY), 25 points, four bands, three verbs "
     "(BUILD/CALIBRATE/REMEMBER), five dogfood tests. Carries the amendment stack: background-by-default, "
     "threads-are-signal, steal-source comments, spawn genome, no-pause, duplication-is-emphasis, LAUNCH LAW.",
     ["5 axes x 5", "tests 1 and 4 always run"])
node("rtfm:docs/ref/BURST_DOCTRINE_20260903.md", "rtfm-artifact",
     "BURST DOCTRINE (2026-09-03)",
     "The measured lane table: 5.3-flash bursts 50-wide at p50 1.7s; 32B is the 0.8s latency king; 4.7-flash is "
     "single-flight cache-mining only; the 8K tax kills long-context free work; night window compounds. "
     "Nine burst laws, every number measured or receipted — read before routing any fan-out.",
     ["no vibes", "1302 = your model's row, not an insult"])
node("rtfm:watch/FRONTIER_MAP_DEEPSEEK_20260904.md", "rtfm-artifact",
     "FRONTIER MAP (talent.deepseek.com)",
     "A frontier lab's hiring page as a spec: 34 roles extracted from the JS bundle, mapped to fleet organs "
     "(EXISTS/THIN/MISSING). Fleet drafts ~70% of the chart; the gaps became the three skills, the Search-Prime "
     "probe, and Rocinante (Oct 27) as the supercomputing role.",
     ["34 roles, byte-extracted"])
node("rtfm:watch/COMPUTE_DIG_20260904.md", "rtfm-artifact",
     "COMPUTE DIG",
     "The physical substrate, receipted: one 68.7GB box (local serving only, no CUDA), burst-rich API side "
     "(50-wide 5.3-flash, 99.5% frozen-prefix cache), and Rocinante 4x Mac Studio M5 Ultra on Oct 27 as the "
     "first real local training substrate. Honest shape: burst-rich, memory-poor until October.",
     ["local training = zero until Rocinante"])
node("rtfm:watch/SOCRATIC_MCP_BRIEF_20260904.md", "rtfm-artifact",
     "SOCRATIC MCP BRIEF",
     "The 3,838-senses pre-brief answered from receipts: 9 live MCP servers inventoried, triple-census catalog "
     "(3,838 unique servers), aisle map vs fleet (weak on agreements/coordination), and the five salon questions "
     "including the adoption organ and the sovereignty line.",
     ["loopback law not up for debate"])
node("rtfm:watch/LAUNCH_LAW_DIGEST_20260904.md", "rtfm-artifact",
     "LAUNCH LAW DIGEST",
     "The closed-loop receipt: sqrt(7) tweet -> scored 15/25 -> card filed -> builder spawned same turn -> "
     "lattice_distance.py + 12 tests + lattice_check.html -> seat re-verified -> room row. ~8 minutes, $0. "
     "The exhibit A that made the launch law doctrine and spawned the salon.",
     ["$0 spend", "honest boundary named"])
node("rtfm:watch/STEAL_PASTE_FALSIFIERS_20260904.md", "rtfm-artifact",
     "STEAL: paste-checkable falsifiers",
     "Seven steals toward an Invariant Workbench: CyberChef recipe-chains, jwt.io live verdicts, OEIS detector "
     "mode, regex101 test benches, godbolt URL permalinks, TLA+ witness rendering, Luhn-validator posture. "
     "Finding: nobody has unified math invariant paste-checkers — niche open (supported by one search).",
     ["witness rendering = house law"])
node("rtfm:watch/INTAKE_MCP_AWESOME_20260904.md", "rtfm-artifact",
     "INTAKE: awesome-mcp-servers",
     "The senses aisle, counted: three-catalog census URL-normalized to 3,838 unique MCP servers across 59+ "
     "categories; aisle map vs fleet organs (agreements/coordination = our weak spot, prior art exists). "
     "Also the card where Mimosa blocked naive fetch scripts twice — curl-literal became the house door.",
     ["adoption filter: local-first, loopback-safe, permissive"])
node("rtfm:watch/INTAKE_LEGENDRE_LATTICE_20260904.md", "rtfm-artifact",
     "INTAKE: Legendre lattice (sqrt(7))",
     "The seed card: Legendre's three-square theorem says on-grid squared distances are never of form 4^a(8b+7), "
     "so sqrt(7) can never occur between Z^3 lattice points. Hand-verified before filing, scored 15/25, "
     "launched same turn — the launch law's founding exhibit.",
     ["math hand-verified pre-filing"])
node("rtfm:dashboard/static/falsifiers.html", "rtfm-artifact",
     "falsifiers.html (index)",
     "The paste-checkable invariants index: 3 BUILT (lattice, chain, claim), 2 UNPROVEN (mass balance, concurrency "
     "serializability). Pattern law: a falsifier is a pure function of pasted state, zero-fetch, JS<->Python "
     "parity-checked, witness-rendering on failure. Absorbed steals #2 (live verdicts) and #6 (witnesses).",
     ["zero-fetch", "failure shows its witness"])
node("rtfm:dashboard/static/lattice_check.html", "rtfm-artifact",
     "lattice_check.html",
     "Falsifier #1: Legendre three-square. Paste x,y,z lines or a single d^2; excludedForm strips factors of 4 and "
     "tests n = 7 mod 8; excluded pairs render the (a,b) curse; non-integer d^2 flagged off-grid gold. "
     "Demo button loads a broken grid measuring sqrt(7).",
     ["zero-fetch", "parity twin: mag/lattice_distance.py"])
node("rtfm:dashboard/static/chain_check.html", "rtfm-artifact",
     "chain_check.html",
     "Falsifier #2: the verkle knot verifier, byte-for-byte JS mirror of the fleet's actual formulas — leaf = "
     "sha256('leaf:'+canonical json), node = sha256('node:'+L+':'+R), genesis = sha256('empty'), merkle prefix "
     "roots. Inline FIPS 180-4 fallback + crypto.subtle, parity self-tested on load; tampered demo makes the chain confess.",
     ["Python float-repr port", "first broken link highlighted"])
node("rtfm:dashboard/static/claim_check.html", "rtfm-artifact",
     "claim_check.html",
     "Falsifier #5: the launch-law card verifier (the reference impl — Python twin not yet written). Regex set "
     "scores cards: BUILD claim with no builder marker and no named gate = VIOLATION [launched law]; REMEMBER "
     "card with a builder = over-launch NOTE; missing N/25 band = MALFORMED; the gate defers, not the lane.",
     ["rules self-teaching via 4 demo loaders"])
node("rtfm:mag/lattice_distance.py", "rtfm-artifact",
     "mag/lattice_distance.py",
     "The Python twin: is_three_square, excluded_form, lattice_distance_ok, validate_voxel_coords — zero deps, "
     "12 pytest cases brute-force-parity-checked to 512. Honest boundary in the docstring: integer lattice points "
     "cannot violate by construction; the validator earns its keep on parsed GLB floats where 'on-grid' is under test.",
     ["12/12 pass", "consumers: maze_arena, mesh-baker, dungeon"])
node("rtfm:memory/runs/salons/salon_launch_law_20260904/SALON_ARTIFACT.md", "rtfm-artifact",
     "SALON: launch law (2026-09-04)",
     "7 shapes on 'how do we do this everywhere': convergent verdict — adopt the skeleton iff self-verifiable "
     "in-turn and gate-free; claim contention (duplicate builds) breaks first, so the spawn gate locks per-card "
     "at FILE time; top-5 paste-checkable invariants; the seat itself is the default research agent.",
     ["postrun correction filed: runner mis-called the first breaker"])
node("rtfm:docs/mirrors/mcp/", "rtfm-artifact",
     "MCP docs mirror",
     "Phase-2 mirror of github.com/modelcontextprotocol in the zai_docs_mirror shape: full 2026-07-28 spec (31 "
     "pages), schema.ts/json, three SDK READMEs — 38 files, 1.35MB, 38/38 HTTP 200 via literal raw-pulls. "
     "These bytes ARE the manuals modelcontextprotocol.io serves.",
     ["38/38 fetched", "literal URLs only"])
node("rtfm:docs/mirrors/mcp/INSIGHTS.md", "rtfm-artifact",
     "MCP INSIGHTS (the fold)",
     "The read-the-manual paydirt: MCP gives wire formats and a consent architecture (host-mediated, human in the "
     "loop, OAuth 2.1 audience binding) but ZERO discovery and ZERO trust — the aisle-triage problem lives "
     "entirely in the spec's blind spot, so the fleet adoption organ is not optional. 2026-07-28 deprecates "
     "sampling and goes stateless (_meta + MRTR).",
     ["spec revision pinned 2026-07-28"])
node("rtfm:docs/ref/zai_docs_mirror/", "rtfm-artifact",
     "z.ai docs mirror (pattern source)",
     "The 2026-09-04 bulk-ape of docs.z.ai (86/86 pages via llms-full.txt + per-page .md doors) that defined the "
     "house mirror shape: provenance header, doors used, coverage stats, categorized subdirs, _raw/ fetch logs. "
     "The MCP mirror is its direct descendant.",
     ["86/86 coverage", "vendor Last-Modified pinned"])
node("rtfm:watch/INTAKE_CORPUS_20260903-04", "rtfm-artifact",
     "Intake corpus 09-03/04 (145 cards)",
     "The 145 verdict cards filed across the two days: ~25 BUILD NOW, ~28 WINDOWED, ~30 CALIBRATE, rest REMEMBER. "
     "Genre law the corpus teaches: math-viz items must be wireable + consumer or they are shelf lines. "
     "Distilled in RTFM_20260904.md section 11.",
     ["tri-state every card"])

# ── MCP CONCEPTS (Phase 2) ─────────────────────────────────────────────────
node("mcp:architecture", "mcp-concept",
     "Hosts / Clients / Servers",
     "MCP's client-host-server shape: the host owns consent, security policy, and LLM integration; each client "
     "serves exactly one server; servers never read the whole conversation nor see into other servers. "
     "Spec-level license for the fleet's per-lane MCP whitelists.",
     ["JSON-RPC 2.0", "client 1:1 server"])
node("mcp:transport-stdio", "mcp-concept",
     "Transport: stdio",
     "Client launches the server as a subprocess; newline-delimited JSON-RPC over stdin/stdout, stderr free for "
     "logs. The default loopback posture — a subprocess server never opens a port, which is why the fleet runs "
     "nearly everything this way.",
     ["no port opened", "framing portable to sockets"])
node("mcp:transport-streamable-http", "mcp-concept",
     "Transport: Streamable HTTP",
     "Every message its own POST to one MCP endpoint; reply = JSON or request-scoped SSE. 2026-07-28 removed the "
     "GET stream and sessions; Origin validation is mandatory (DNS-rebinding defense). The transport cloud BaaS "
     "servers demand — and the one that can cross the loopback line if adopted carelessly.",
     ["stateless", "POST-only"])
node("mcp:tools", "mcp-concept",
     "Tools (model-controlled)",
     "Server-exposed functions the MODEL discovers and invokes: tools/list + tools/call, JSON-Schema inputs, "
     "self-declared annotations (readOnly/destructive hints). Spec SHOULDs a human in the loop with denial power — "
     "the address the room's KEYS/spend gates bolt onto.",
     ["annotations are hints, not guarantees"])
node("mcp:resources", "mcp-concept",
     "Resources (application-driven)",
     "URI-identified context data the HOST decides how to include: resources/list, read, templates, update "
     "subscriptions. The memory/KB aisle of MCP — the fleet's verkle chain and percolator already fill this role "
     "with own organs.",
     ["URI-identified"])
node("mcp:prompts", "mcp-concept",
     "Prompts (user-controlled)",
     "Templated messages and workflows exposed for explicit user selection (slash commands): prompts/list + "
     "prompts/get with arguments. The SKILL.md layer of MCP; the marketplace's 'skills over MCP' working group "
     "is extending exactly this.",
     ["user-controlled"])
node("mcp:elicitation", "mcp-concept",
     "Elicitation",
     "Server asks the user for input through the client: form mode (JSON-Schema validated) or URL mode for "
     "sensitive interactions. Spec law: form mode MUST NOT request secrets — credentials go URL mode, bypassing "
     "the MCP client entirely. Same instinct as secrets-never-echoed.",
     ["secrets go URL mode"])
node("mcp:roots", "mcp-concept",
     "Roots",
     "Client-declared filesystem/URI scopes the server should operate within — the host telling the server where "
     "it may reach. A scope fence the fleet analogues to per-lane whitelists and Mimosa's path-traversal guard.",
     ["client-declared scope"])
node("mcp:sampling", "mcp-concept",
     "Sampling (DEPRECATED)",
     "Server requests LLM completions through the client (sampling/createMessage). Deprecated in 2026-07-28 "
     "(SEP-2577): new implementations SHOULD NOT adopt; servers migrate to calling provider APIs directly. "
     "Consequence: the host's consent chokepoint shrinks — fleet lane whitelists matter more, not less.",
     ["deprecated 2026-07-28", "12-month removal clock"])
node("mcp:meta-stateless", "mcp-concept",
     "Per-request _meta (stateless era)",
     "2026-07-28's sea change: no initialize handshake. Every request carries protocolVersion + clientInfo + "
     "capabilities in _meta; the server accepts or rejects each request independently. 'Modern' vs 'legacy' eras "
     "are now a compatibility axis — the fleet's 9 servers mostly speak legacy.",
     ["no handshake", "dual-era clients needed"])
node("mcp:mrtr", "mcp-concept",
     "MRTR (multi round-trip requests)",
     "Server-to-client requests (sampling/elicitation/roots) ride INSIDE results as input_required "
     "(InputRequiredResult); the client gathers input and retries. Replaces server-initiated requests — a "
     "breaking change that also makes servers stateless-friendly (no shared session storage).",
     ["breaking change 2026-07-28"])
node("mcp:server-discover", "mcp-concept",
     "server/discover",
     "One call returning supported versions, capabilities, identity, and instructions. Servers MUST implement it; "
     "on stdio it doubles as the legacy-handshake probe. The free liveness falsifier: the adoption organ's "
     "'is this server alive and does it offer what its card claims' check.",
     ["MUST implement", "cacheable"])
node("mcp:authorization", "mcp-concept",
     "OAuth 2.1 authorization",
     "HTTP-transport auth: protected-resource metadata discovery, dynamic client registration, RFC 8707 resource "
     "indicators. Servers MUST validate token audience; token passthrough forbidden (confused-deputy defense). "
     "The spec's most MUST-dense corner.",
     ["audience binding", "no passthrough"])
node("mcp:capabilities", "mcp-concept",
     "Capability negotiation",
     "Servers advertise tools/resources/prompts support (with listChanged/subscribe flags) and clients advertise "
     "elicitation/sampling/roots. Sets MUST NOT vary per-connection — only by per-request authorization. "
     "Discoverable, therefore falsifiable.",
     ["listChanged flags", "deterministic ordering SHOULD"])
node("mcp:extensions", "mcp-concept",
     "Extensions (Tasks, MCP Apps, Skills-over-MCP)",
     "Opt-in modules negotiated during initialization: Tasks (async long-running ops), MCP Apps (inline UI), "
     "Skills-over-MCP (structured agent-workflow instructions — the marketplace layer the fleet's SKILL.md "
     "doctrine anticipated). Both sides must opt in.",
     ["opt-in both sides"])
node("mcp:registry-gap", "mcp-concept",
     "The discovery/trust gap",
     "What the spec does NOT solve: no ranking, no security certification, no in-band provenance; the MCP "
     "Registry is a list, not a verdict. 3,838 servers, zero spec-level 'safe to adopt' signal. This gap IS the "
     "fleet's aisle-triage problem — and the adoption organ (security pass -> SKILL.md -> receipt -> liveness) "
     "is the build that fills it.",
     ["registry is advisory", "triage is ours"])

# ── FLEET MCP SERVERS ──────────────────────────────────────────────────────
node("server:mag", "mcp-server",
     "mag",
     "The fleet organ itself as an MCP server: chain, room, blackboard, research, run_python/run_shell, "
     "pheromones, scan/measure. Every lane contract starts with a mag subset; the room runs on it. "
     "The proof that the fleet was MCP-native before the aisle conversation started.",
     ["loopback", "files + chain over processes"])
node("server:computer-use", "mcp-server",
     "computer-use",
     "Desktop AX control — the seat's hands on the host OS. Sovereignty-critical: on the salon's sovereignty line "
     "(never outsourced to third-party servers), because whoever drives the desktop drives the operator's machine.",
     ["sovereignty line organ"])
node("server:browser-use", "mcp-server",
     "browser-use (+ node-repl)",
     "Headed browser control plus a JS kernel for the research lane: the only lane that gets to click. "
     "Research lanes pair it with node_repl for in-page work; the fleet's strong aisle (browser automation) "
     "per the senses map.",
     ["research lane only"])
node("server:android-emulator", "mcp-server",
     "android-emulator",
     "The mobile body: build/install/launch Android apps, drive UI via uiautomator, screenshot, logcat — 23 "
     "tools. Born from the Sep-4 self-steal (Android farm surface); gives the fleet a second physical substrate "
     "beyond the desktop.",
     ["GUI emulator on demand"])
node("server:cloudbase", "mcp-server",
     "cloudbase",
     "Cloud BaaS (Tencent CloudBase): envs, functions, cloud run, hosting, SQL/NoSQL/PG, storage, auth — 37 "
     "tools. The fleet's one sanctioned cloud escape hatch; everything it touches crosses the loopback line, "
     "so it rides the lane-whitelist pattern.",
     ["cloud boundary organ"])
node("server:mimosa", "mcp-server",
     "mimosa",
     "The security scanner as an MCP server: deep project scans with SSRF/path-traversal/private-IP enforcement "
     "at the code layer. Proven in production: blocked two naive fetch scripts on 09-04 and forced the "
     "curl-literal house door. The adoption organ's security pass runs through it.",
     ["blocked 2 scripts 2026-09-04"])
node("server:image-search", "mcp-server",
     "image-search",
     "Web image search MCP server — the smallest sense: one capability, clean primitive mapping (tools). "
     "The example of what 'adopt a sense' means at minimum size: one server, one skill, one whitelist line.",
     ["one-primitive server"])

# ── EDGES ──────────────────────────────────────────────────────────────────
E = edge
# skills -> laws
E("skill:agent-harness", "law:launch-law", "uses", "encodes Amendment 5 as its launch loop")
E("skill:agent-harness", "law:tri-state", "uses", "tri-state or it does not ship")
E("skill:agent-harness", "law:receipt-at-bytes", "uses", "done is a byte fact")
E("skill:agent-harness", "law:background-by-default", "uses", "spawns are background, cap 6, genome-bound")
E("skill:frontier-researcher", "skill:operator-corrections", "uses", "the corrections skill is an INPUT to the loop")
E("skill:frontier-researcher", "law:files-as-truth", "uses", "promote laws into files + chain knots")
E("skill:code-agent-data", "law:files-as-truth", "uses", "action without record never happened")
E("skill:code-agent-data", "skill:operator-corrections", "uses", "the distilled policy shape is the per-record quality bar")
E("skill:code-agent-data", "law:no-pause", "pairs-with", "night-window mining cadence rides the heartbeat windows")
E("skill:frontier-researcher", "law:duplication-is-emphasis", "uses", "re-finds are filed as re-finds; repetition is emphasis")
# rubric <-> skills/laws
E("rtfm:watch/INTAKE_RUBRIC_20260903.md", "skill:agent-harness", "pairs-with", "the harness skill consolidates this rubric")
E("rtfm:watch/INTAKE_RUBRIC_20260903.md", "law:launch-law", "uses", "Amendment 5 lives here")
E("rtfm:watch/INTAKE_RUBRIC_20260903.md", "law:background-by-default", "uses", "Amendment 1 lives here")
E("rtfm:watch/INTAKE_RUBRIC_20260903.md", "law:no-pause", "uses", "Amendment 4 lives here")
E("rtfm:watch/INTAKE_RUBRIC_20260903.md", "law:duplication-is-emphasis", "uses", "Amendment 4b lives here")
E("rtfm:watch/INTAKE_RUBRIC_20260903.md", "law:tri-state", "uses", "every card tri-state labeled")
# falsifier surfaces
E("rtfm:dashboard/static/falsifiers.html", "rtfm:memory/runs/salons/salon_launch_law_20260904/SALON_ARTIFACT.md", "uses", "falsifier table provenance")
E("rtfm:dashboard/static/falsifiers.html", "rtfm:dashboard/static/lattice_check.html", "pairs-with", "index entry #1")
E("rtfm:dashboard/static/falsifiers.html", "rtfm:dashboard/static/chain_check.html", "pairs-with", "index entry #2")
E("rtfm:dashboard/static/falsifiers.html", "rtfm:dashboard/static/claim_check.html", "pairs-with", "index entry #5")
E("rtfm:dashboard/static/lattice_check.html", "rtfm:mag/lattice_distance.py", "mirrors", "JS<->Python parity twin (12 tests)")
E("rtfm:dashboard/static/chain_check.html", "law:files-as-truth", "uses", "the signed line, checkable by paste")
E("rtfm:dashboard/static/claim_check.html", "law:launch-law", "uses", "encodes the law as regex rules")
E("rtfm:watch/INTAKE_LEGENDRE_LATTICE_20260904.md", "rtfm:mag/lattice_distance.py", "pairs-with", "the card that spawned the validator")
E("rtfm:watch/INTAKE_LEGENDRE_LATTICE_20260904.md", "rtfm:dashboard/static/lattice_check.html", "pairs-with", "the card that spawned the page")
E("rtfm:watch/STEAL_PASTE_FALSIFIERS_20260904.md", "rtfm:dashboard/static/falsifiers.html", "pairs-with", "steals #2/#6 absorbed as house law; workbench spec seed")
E("rtfm:watch/LAUNCH_LAW_DIGEST_20260904.md", "rtfm:memory/runs/salons/salon_launch_law_20260904/SALON_ARTIFACT.md", "pairs-with", "the digest is the salon's source")
E("rtfm:watch/LAUNCH_LAW_DIGEST_20260904.md", "law:launch-law", "uses", "the receipt that made the law doctrine")
E("rtfm:memory/runs/salons/salon_launch_law_20260904/SALON_ARTIFACT.md", "skill:agent-harness", "pairs-with", "spawn gate + claim lock verdict landed in the skill")
E("rtfm:watch/FRONTIER_MAP_DEEPSEEK_20260904.md", "skill:agent-harness", "pairs-with", "gap (a) spawned this skill")
E("rtfm:watch/FRONTIER_MAP_DEEPSEEK_20260904.md", "skill:code-agent-data", "pairs-with", "gap (b) spawned this skill")
E("rtfm:watch/FRONTIER_MAP_DEEPSEEK_20260904.md", "skill:frontier-researcher", "pairs-with", "gap (c) spawned this skill")
E("rtfm:docs/ref/BURST_DOCTRINE_20260903.md", "rtfm:watch/COMPUTE_DIG_20260904.md", "pairs-with", "the dig cites burst numbers as its API-side receipt")
E("rtfm:watch/INTAKE_CORPUS_20260903-04", "rtfm:watch/INTAKE_RUBRIC_20260903.md", "uses", "every card scored on the rubric")
E("rtfm:docs/ref/RTFM_20260904.md", "rtfm:watch/INTAKE_RUBRIC_20260903.md", "pairs-with", "section 1 of the manual")
E("rtfm:docs/ref/RTFM_20260904.md", "rtfm:docs/ref/BURST_DOCTRINE_20260903.md", "pairs-with", "section 2 of the manual")
E("rtfm:docs/ref/RTFM_20260904.md", "rtfm:watch/INTAKE_CORPUS_20260903-04", "pairs-with", "section 11 distills the corpus")
# MCP mirror edges
E("rtfm:docs/mirrors/mcp/", "rtfm:docs/ref/zai_docs_mirror/", "mirrors", "reuses the house mirror shape (INDEX + subdirs + _raw)")
E("rtfm:docs/mirrors/mcp/", "mcp:architecture", "mirrors", "spec pages mirrored at the bytes")
E("rtfm:docs/mirrors/mcp/", "mcp:transport-stdio", "mirrors", "stdio binding page")
E("rtfm:docs/mirrors/mcp/", "mcp:transport-streamable-http", "mirrors", "streamable HTTP page")
E("rtfm:docs/mirrors/mcp/", "mcp:tools", "mirrors", "tools page")
E("rtfm:docs/mirrors/mcp/", "mcp:resources", "mirrors", "resources page")
E("rtfm:docs/mirrors/mcp/", "mcp:prompts", "mirrors", "prompts page")
E("rtfm:docs/mirrors/mcp/", "mcp:elicitation", "mirrors", "elicitation page")
E("rtfm:docs/mirrors/mcp/", "mcp:sampling", "mirrors", "sampling page (deprecated)")
E("rtfm:docs/mirrors/mcp/", "mcp:authorization", "mirrors", "OAuth framework + security considerations")
E("rtfm:docs/mirrors/mcp/INSIGHTS.md", "mcp:registry-gap", "uses", "the fold's central finding")
E("rtfm:docs/mirrors/mcp/INSIGHTS.md", "rtfm:docs/mirrors/mcp/", "uses", "reads only the mirrored bytes")
E("rtfm:watch/SOCRATIC_MCP_BRIEF_20260904.md", "mcp:registry-gap", "pairs-with", "the brief's triage question IS the gap")
E("rtfm:watch/SOCRATIC_MCP_BRIEF_20260904.md", "server:mag", "uses", "inventories the 9 live servers")
E("rtfm:watch/INTAKE_MCP_AWESOME_20260904.md", "mcp:registry-gap", "pairs-with", "3,838 servers counted; triage criteria proposed")
# MCP concept lattice
E("mcp:meta-stateless", "mcp:server-discover", "pairs-with", "discover doubles as the legacy-era probe")
E("mcp:meta-stateless", "mcp:mrtr", "pairs-with", "both are 2026-07-28 breaking changes")
E("mcp:sampling", "mcp:meta-stateless", "violates", "the stateless revision deprecates sampling outright (SEP-2577)")
E("mcp:transport-streamable-http", "law:loopback", "violates", "external HTTP endpoints cross the loopback line unless bound to 127.0.0.1 — the adoption organ gates this")
E("mcp:elicitation", "law:secrets-never-echoed", "gated-by", "spec forbids secrets in form mode; URL mode bypasses the client")
E("mcp:tools", "law:secrets-never-echoed", "gated-by", "tool inputs/outputs must never carry credentials into logs or cards")
E("mcp:architecture", "law:no-second-supervisor", "pairs-with", "the host is the single coordinator — the spec agrees with the respawn law")
E("mcp:capabilities", "mcp:server-discover", "uses", "discover returns the capability block in one call")
E("mcp:extensions", "mcp:prompts", "pairs-with", "Skills-over-MCP extends the prompts layer")
# servers
E("server:mag", "mcp:architecture", "uses", "a live MCP server speaking the host's whitelist pattern")
E("server:mag", "law:loopback", "gated-by", "loopback-only container services")
E("server:mimosa", "law:loopback", "gated-by", "enforces the network law at the code layer")
E("server:mimosa", "rtfm:docs/mirrors/mcp/", "uses", "the mirror's fetch plan passed Mimosa (literal URLs)")
E("server:computer-use", "law:loopback", "gated-by", "desktop control never leaves the host")
E("server:browser-use", "mcp:tools", "uses", "browser control exposed as tools")
E("server:android-emulator", "mcp:tools", "uses", "23 tools: build, install, launch, UI drive, screenshot")
E("server:cloudbase", "mcp:transport-streamable-http", "pairs-with", "cloud BaaS — the one sanctioned crossing of the loopback line")
E("server:cloudbase", "law:loopback", "gated-by", "lane-whitelisted only; never a default sense")
E("server:image-search", "mcp:tools", "uses", "single-primitive server")
E("server:browser-use", "law:loopback", "gated-by", "headed browser stays on the host")
E("server:android-emulator", "law:loopback", "gated-by", "emulator + adb bound to the host")
E("server:mag", "law:files-as-truth", "uses", "chain + room organs live here")
# manual ties
E("rtfm:docs/ref/RTFM_20260904.md", "rtfm:docs/mirrors/mcp/", "pairs-with", "phase-2 of the same RTFM pass")
E("rtfm:docs/ref/RTFM_20260904.md", "rtfm:dashboard/static/falsifiers.html", "pairs-with", "manual section 9 documents the falsifier JS")
E("skill:agent-harness", "law:no-second-supervisor", "pairs-with", "the room is the decentralized supervisor; the seat is the agent")

# ── validate + write ───────────────────────────────────────────────────────
ids = {n["id"] for n in nodes}
assert len(ids) == len(nodes), "duplicate node ids"
bad = [(e["from"], e["to"]) for e in edges if e["from"] not in ids or e["to"] not in ids]
if bad:
    raise SystemExit("edges referencing missing nodes: %r" % bad)
rels = {e["rel"] for e in edges}
allowed = {"uses", "gated-by", "mirrors", "pairs-with", "violates"}
assert rels <= allowed, "illegal rels: %r" % (rels - allowed)

graph = {
    "schema": "knowledge_graph.v2",
    "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
    "nodes": nodes,
    "edges": edges,
}
with open("memory/rtfm_graph.json", "w", encoding="utf-8", newline="\n") as f:
    json.dump(graph, f, ensure_ascii=False, indent=1)

kinds = {}
for n in nodes:
    kinds[n["kind"]] = kinds.get(n["kind"], 0) + 1
print("nodes:", len(nodes), "edges:", len(edges), "kinds:", kinds)
print("rel counts:", {r: sum(1 for e in edges if e["rel"] == r) for r in sorted(rels)})
