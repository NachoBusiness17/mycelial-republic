# EXTERNAL STEAL MESH 20261002 - what exists like our design, and what beats us

Schema: external_steal.mesh.v1 · lane: research (read-only except this file) · grounding:
watch/inbox/mesh_foundations_selfsteal_20261002.md + full_width_fold_20261002.md Lane C ·
organs targeted: THOUGHT QUANTIZER (percolator -> tiered law packs, pack sha bound to chain
tip) + SYSTEM-ONE (cheap sub-second routing/guardrail/supervision over quantized state) ·
every external fact carries a fetched URL; zero em-dash bytes.

## 0. PRIOR-ART SWEEP COVERAGE (already banked, not re-stolen here)

- watch/inbox/localfirst/adjacent.md: Letta (MemFS git-tracked self-editing blocks), Mem0
  (April 2026 single-pass ADD-only), Zep CE dead / Graphiti survives, Khoj/AnythingLLM/
  Cognee/GroundMemory verdicts. Steals banked: selfblock rung, validity windows.
- watch/inbox/localfirst/atlas.md: Graphiti substrate-only verdict + the cascade-ledger port
  spec (impact BFS, 3-bucket routing, hash-chained cascade receipts) for the percolator.
- corpus/steal/CORPUS_FOLD_FRONTIER_OLM_20261001.md: quantization damage stratification
  (capability-classed batteries, cross-family witness rosters), judge-panel aggregation laws,
  HiveMind AIMD backpressure, EMIR2 SUPERSEDES/CONTRADICTS validity edges, reach meter.
- corpus/steal/MASTER_MICKEY17* + ZCODE_REPO_STEAL_MAP: ZCode harness internals only;
  "langgraph-patterns" there names a retry-write-clearing pattern in ZCode source, LangGraph
  as a product was never dug. NONE of the five classes below were covered.

## 1. MULTI-DEVICE AGENT MESHES / ORCHESTRATION
- LangGraph + Temporal plugin · VERIFIED: "The checkpoint preserves your data, not your
  execution"; "something has to detect the failure, decide where to re-enter the graph, and
  restart it"; recovery resumes "on the same worker or a different one"
  (https://temporal.io/blog/temporal-langgraph-plugin-durable-execution). WE LACK: exactly
  the detect + re-entry + restart leg; we move durable data (zips, inbox) but no organ
  watches a node (mag-openclaw sat offline 24d). STEAL: a watchdog loop behind the existing
  /api/v1/fleet/hypervisor surface (dashboard/rest.py:176-180): heartbeat absent -> re-entry
  = re-run rib_k8s desired-state checks for that node + one attention.md row.
- OpenAI Agents SDK · VERIFIED: "Run input validation and safety checks in parallel with
  agent execution, and fail fast when checks do not pass"; sessions are "a persistent
  memory layer for maintaining working context within an agent loop"
  (https://openai.github.io/openai-agents-python/). WE LACK: System-One guards run serially
  before dispatch; nobody races the call. STEAL: fire atomic-boolean guard asks CONCURRENT
  with the work ask, fail-fast on first false; supervision latency leaves the critical path.
- Claude Code subagents · VERIFIED: "Each subagent runs in its own context window with a
  custom system prompt, specific tool access, and independent permissions"; agent files are
  markdown + YAML frontmatter where "the body becomes the system prompt"; concurrency capped
  at 20 via CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS (https://code.claude.com/docs/en/sub-agents).
  WE LACK: the rib -> device-declaration compiler (mesh topic 2: rib_k8s compiles to k8s,
  nothing compiles ribs to "this node runs the janitor"). STEAL: frontmatter = the RIB
  4-tuple (id/predicate/action/anchor) + tools + permissions, body = rendered law rows; one
  markdown file per seat class per node. Riblang in a shape thousands of agents already
  parse; fits the R1 SEAT_KIND naming ruling unchanged.

## 2. CHEAP JUDGMENT / CONTROL PLANES
- LiteLLM budget fallbacks · VERIFIED: "budget_fallbacks lets you configure a per-model
  fallback chain on the key itself, so the request is silently rerouted"; spend is
  attributed to the fallback model; all-fallbacks-over-budget raises BudgetExceededError
  (https://docs.litellm.ai/docs/proxy/budget_fallbacks). WE LACK: LAW-11 ("credits over
  failure", memory/law/registry.json:101-111) is law prose; no organ reroutes AT BURN TIME.
  STEAL: a budget_fallbacks table in configs/providers.yaml (model -> ordered lane chain +
  per-lane daily cap) enforced in the switchboard dispatch path; the receipt row credits the
  fallback lane, not the dead one.
- RouteLLM · VERIFIED: "Each request is also associated with a cost threshold that
  determines the cost-quality tradeoff of that request"; routers "reduce costs by up to 85%
  while maintaining 95% GPT-4 performance" (https://github.com/lm-sys/RouteLLM). WE LACK:
  our gates (RIB_MODEL_GATES_20260901) are static per model; the threshold is per-ASK.
  STEAL: one threshold field on the ask envelope (strong-model win-rate cutoff, calibrated
  from GPS verdict history); crossing it downgrades the ask one rung unattended.
- NeMo Guardrails · VERIFIED: five rail classes; input rails "can reject the input,
  stopping any additional processing, or alter the input"; execution rails "applied to
  input/output of the custom actions (a.k.a. tools)"; Colang is "a modeling language
  specifically created for designing flexible, yet controllable, dialogue flows"
  (https://github.com/NVIDIA/NeMo-Guardrails). WE LACK: dialog rails, the class that
  influences prompting MID-FLOW; ours are pre-input (switchboard) or around-effects (effect
  broker). STEAL: name the missing rail in System-One: a mid-flight re-prompt hook on the
  seat contract when supervision booleans flip.

## 3. POLICY / LAW-AS-CODE REPLICATION
- OPA signed bundles · VERIFIED: "a signed bundle is a normal OPA bundle that includes a
  file named .signatures.json that dictates which files should be included in the bundle,
  what their SHA hashes are, and is cryptographically secure"; on any check failure OPA
  KEEPS THE EXISTING BUNDLE and reports via status API; revision is "a string value...
  typically a Git commit hash"; JSON/YAML files are canonicalized (fields sorted) before
  hashing so signatures are whitespace-independent
  (https://www.openpolicyagent.org/docs/latest/management-bundles/). WE LACK: the quantizer
  binds pack sha to chain tip but has no ACTIVATION LAW for a failed verification. STEAL:
  the OPA triple as the pack-loader contract: verify tip witness -> verify manifest file
  list -> verify per-file sha; any failure = keep serving the last good pack + status row;
  canonical field-sorted JSON hashing makes pack hashes stable across nodes. This is also
  the cross-node tip-exchange protocol's integrity half (mesh topic 4 gap).
- Langfuse prompt versioning · VERIFIED: "If you already have a prompt with the same name,
  the prompt will be added as a new version"; "we recommend using the production label to
  fetch the version intentionally chosen for production"; "the SDKs cache prompts
  client-side, so after the first fetch they are served from memory with no extra latency"
  (https://langfuse.com/docs/prompts). WE LACK: packs are fetched by path, not by label; no
  immutable-version + label indirection. STEAL: fetch law packs BY LABEL
  (seat_class:janitor@production), never by path; the label moves only after verification;
  the receipt pins {label, version, pack sha}. Rides the context_pack kernel's prefix hits.

## 4. K8S-NATIVE LLM SCHEDULING
- KubeAI · VERIFIED: the proxy handles "request queueing (while the system scales from zero
  replicas) and request retries"; a "prefix-aware load balancing strategy" optimizes KV
  cache across vLLM replicas; scale-from-zero needs NO Knative and NO Prometheus adapter
  (https://www.kubeai.org/). WE LACK: queue-while-waking for mesh nodes (moto/phone,
  sleeping laptop): a dark node just times out today. STEAL: the wake pattern for the node
  spine: work for node X queues (inbox row, status held) until X heartbeats, then dispatch.
- AIBrix · VERIFIED: "Cost-efficient and pluggable Infrastructure components for GenAI
  inference" with an "LLM App-Tailored Autoscaler" and "Distributed KV Cache: enables
  high-capacity, cross-engine KV reuse", v0.7.0 (2026-06-16)
  (https://github.com/vllm-project/aibrix). WE LACK: nothing structural (K8S_RACTOR ruled
  the control plane stays estate-native, batch executor only); the confirmation is that
  even dedicated platforms schedule on cache/SLO signals, NOT verified-evidence quality, so
  the GPS epistemic-scheduling claim survives contact with 2026 prior art. STEAL: one idea:
  warm-prefix affinity as a routing input (our context_pack frozen prefix already provides
  it); pin warmed asks to the node holding the warm cache.

## 5. QUANTIZED LAW TIERS PER MODEL CLASS
- LLMLingua · VERIFIED: "compress the prompt and KV-Cache, which achieves up to 20x
  compression with minimal performance loss"; it "utilizes a compact, well-trained language
  model (e.g., GPT2-small, LLaMA-7B) to identify and remove non-essential tokens"
  (https://github.com/microsoft/LLMLingua). WE LACK: cheap-seat packs are hand-tiered, never
  measured for how far they can compress. STEAL: an instrument, not a port: score tier-pack
  tokens with the janitor itself (gemma perplexity), drop what the cheap model already
  predicts, keep the imperative core; falsifier = janitor comprehension check on the
  compressed pack (their finding that strong models recover key info from compressed
  prompts is the tiering law in product form).
- Ollama Modelfile · VERIFIED: "The SYSTEM instruction specifies the system message to be
  used in the template"; the model artifact carries its system prompt and `ollama show
  --modelfile` reveals it (https://docs.ollama.com/modelfile). WE LACK: tier packs ride the
  harness, so any harness speaking to the janitor without our pack gets an unquantized seat.
  STEAL: bake the seat-class imperative core into a per-class Modelfile (FROM gemma:2b +
  SYSTEM = tier-pack render); the model IS the delivery vehicle and `ollama show` is the
  verification instrument, attacking the "janitor dialects never tested driving a tool
  loop" gap (mesh topic 2) from the artifact side.

## RANKED TOP 5 BY LEVERAGE
1. OPA activate-only-if-verified bundles (class 3): the activation law is the missing half
   of pack-sha-bound-to-tip AND of cross-node pack exchange. Organ: quantizer pack loader +
   verkle tip witness. Falsifier: a node serves a stale pack after failed verification with
   no status row.
2. LiteLLM budget_fallbacks (class 2): LAW-11 gains an executor at burn time. Organ:
   switchboard + configs/providers.yaml. Falsifier: a budget-crossed ask still errors
   instead of rerouting after the table lands.
3. Claude Code subagent frontmatter (class 1): the rib -> device-declaration compiler gets
   a target format agents already parse at scale. Organ: riblang lowering + seat_contract.
   Falsifier: a frontmatter-compiled brief fails to boot a real seat in one window.
4. Temporal durable-execution split (class 1): checkpoint-is-not-execution names the mesh's
   watchdog gap in one sentence; re-entry = rib_k8s re-apply. Organ: fleet hypervisor.
   Falsifier: a node goes dark again and the loop stays silent.
5. RouteLLM per-ask cost threshold (class 2): one envelope field turns static model gates
   into calibrated routing. Organ: RIB_MODEL_GATES + ask envelope. Falsifier: the threshold
   flips routing on under 5 percent of asks, proving the dial adds nothing.

FILED 2026-10-02 · research lane · 13 pages fetched, all claims carry their URL · read-only
except this receipt · zero em-dash bytes.
