// MAG Framework Map — custom VS Code pane for the local_sovereign_agent framework.
// Scans the project's real command surface (main.py subcommands, mag modules,
// tools, launchers, REST routes, providers) and renders it as a searchable map.
"use strict";

const vscode = require("vscode");
const fs = require("fs");
const path = require("path");
const { execFile } = require("child_process");
const http = require("http");

const DASH_HOST = "127.0.0.1";
const DASH_PORT = 8765;

// Fetch JSON from the dashboard REST API. Resolves null on any failure so the
// caller can fall back to a local scan.
function fetchJson(apiPath) {
  return new Promise((resolve) => {
    const req = http.get(
      { host: DASH_HOST, port: DASH_PORT, path: apiPath, timeout: 4000 },
      (res) => {
        let body = "";
        res.on("data", (c) => (body += c));
        res.on("end", () => {
          try { resolve(JSON.parse(body)); } catch { resolve(null); }
        });
      }
    );
    req.on("timeout", () => req.destroy());
    req.on("error", () => resolve(null));
  });
}

// ---------------------------------------------------------------------------
// Project root resolution
// ---------------------------------------------------------------------------
function findProjectRoot() {
  const cfgRoot = vscode.workspace.getConfiguration("magMap").get("projectRoot");
  if (cfgRoot && fs.existsSync(path.join(cfgRoot, "main.py"))) return cfgRoot;

  const folders = vscode.workspace.workspaceFolders || [];
  for (const f of folders) {
    const cand = f.uri.fsPath;
    if (fs.existsSync(path.join(cand, "main.py")) && fs.isDirectory && fs.existsSync(path.join(cand, "mag"))) {
      return cand;
    }
    // single-workspace parents that contain the project as a subfolder
    const proj = path.join(cand, "local_sovereign_agent");
    if (fs.existsSync(path.join(proj, "main.py"))) return proj;
  }
  return folders.length ? folders[0].uri.fsPath : null;
}

// ---------------------------------------------------------------------------
// Scanner — mirrors tools/capability_manifest.py so the pane never goes stale
// ---------------------------------------------------------------------------
function readText(p) {
  try {
    return fs.readFileSync(p, "utf8");
  } catch {
    return "";
  }
}

// ---------------------------------------------------------------------------
// Functional grouping — the Framework Map is regrouped BY FUNCTION, not by
// file kind. Each item is assigned to a functional group, given a curated
// description, and an example showing how it's actually used.
// ---------------------------------------------------------------------------
const GROUPS = [
  { id: "steer",    icon: "🎛️", label: "Steer",    blurb: "Shape the running agent — ghost, inbox, skills, aimbot" },
  { id: "decide",   icon: "🧭", label: "Decide",   blurb: "Routing, tiers & escalation — the router's judgment" },
  { id: "state",    icon: "🗃️", label: "State",    blurb: "Persistent memory — piles, verkle, ledger, case law" },
  { id: "learn",    icon: "📈", label: "Learn",    blurb: "Self-improvement — fold outcomes into better defaults" },
  { id: "run",      icon: "⚙️", label: "Run",      blurb: "Pipeline & execution — queue, jobs, spec-gated work" },
  { id: "ops",      icon: "🩺", label: "Ops",      blurb: "Health & observability — watch, diagnose, graph" },
  { id: "agents",   icon: "🤝", label: "Agents",   blurb: "Multi-agent orchestration — desks, seats, arenas" },
  { id: "launcher", icon: "🚀", label: "Launch",   blurb: "One-click .cmd launchers" },
  { id: "route",    icon: "🔌", label: "Routes",   blurb: "Dashboard REST endpoints" },
  { id: "provider", icon: "🧠", label: "Providers", blurb: "Model providers in providers.yaml" },
];

// Curated metadata keyed by `<kind>:<name>`. Falls back to assignGroup() +
// scanned help for anything not listed here.
const CURATED = {
  // ── STEER ────────────────────────────────────────────────────────────────
  "mag:ghost": {
    group: "steer",
    help: "Silent situational steer — sense state, deploy test vectors",
    desc: "Senses the agent's situation (CURRENT.md, briefs, agent_state, VS Code context), matches context, and deploys contextual test vectors through operator_inbox. Gated: suppresses auto-deploy during unattended autonomy runs or when the operator is active.",
    example: "python -m mag.ghost --sense   # see what the ghost perceives\npython -m mag.ghost --deploy \"Check FKB before retrying\"",
  },
  "mag:steer_bridge": {
    group: "steer",
    help: "Push guidance into the running agent via operator_inbox",
    desc: "Commits a guidance message to operator_inbox; the agent drains it at its next checkpoint (_absorb_operator_inbox). Idempotent drop-file push with --sync for reliable delivery.",
    example: "python main.py steer-agent \"Prefer the spec over the tier\" --sync",
  },
  "mag:operator_inbox": {
    group: "steer",
    help: "Operator breadcrumbs the agent absorbs at checkpoints",
    desc: "The interference channel: operator notes/steers queued here get absorbed by the running agent every checkpoint. The seam ghost and steer_bridge both inject through.",
    example: "python -m mag.operator_inbox commit_guidance --text \"<steer>\"",
  },
  "mag:pro_library": {
    group: "steer",
    help: "Aimbot — transferable winning moves injected like a scope",
    desc: "SENSE (state) → MATCH (signature overlap) → INJECT (steer/skill/spec/tip via operator_inbox) → LEARN (outcome). Seeded with discovered wins; fires proven moves automatically.",
    example: "python main.py pro-library   # aim at current state\npython main.py pro-library --list",
  },
  "mag:tesuji_shell": {
    group: "steer",
    help: "Capture a winning move as reusable case law",
    desc: "Records a proven move so pro_library can aim it later. The tesuji is the loop: measure → fold → apply.",
    example: "python -m mag.tesuji_shell capture --move \"<signature>:<inject>\"",
  },
  "mag:skill_drop": {
    group: "steer",
    help: "Drop a skill into the running agent's context",
    desc: "Injects a skill/spec via the operator_inbox seam so the next checkpoint inherits it.",
    example: "python -m mag.skill_drop --skill research_sprint",
  },
  "mag:intention_brief": {
    group: "steer",
    help: "Write the intent the next run should absorb",
    desc: "Composes an intention brief the agent consumes on start — the 'frozen spec' that makes a cheap tier render well.",
    example: "python -m mag.intention_brief --goal \"<goal>\"",
  },
  "mag:clippy": {
    group: "steer",
    help: "Propose the next action from folded choices",
    desc: "Suggestions that fold recorded choices back into better proposals.",
    example: "python -m mag.clippy",
  },
  "mag:compass": {
    group: "steer",
    help: "Constitutional compass — route a question against the law",
    desc: "Binds to Mycelial Republic constitution; checks a goal against T0–T3 tiers and fork equality.",
    example: "python -m mag.compass \"<question>\"",
  },
  "tools:pupeteer_gauntlet": {
    group: "steer",
    help: "Prove steering works — run local models through tests they're too dumb for",
    desc: "Control vs puppeteer arms, all real model calls. Probes: memory-edit flip, spec_gate drift block, job_floor walking, aimbot fire, silent steer. Report → memory/runs/pupeteer/.",
    example: "python tools/pupeteer_gauntlet.py --live",
  },
  "tools:steer_compare": {
    group: "steer",
    help: "A/B two steer vectors against the same state",
    desc: "Measures which steer changes the outcome, per steer_telemetry policy.",
    example: "python tools/steer_compare.py --a \"<v1>\" --b \"<v2>\"",
  },
  // ── DECIDE ───────────────────────────────────────────────────────────────
  "mag:decision_framework": {
    group: "decide",
    help: "Compass + case law + behavioral leaves → surface_tips() / decide()",
    desc: "The framework decision channel. Combines compass, skill_ledger case law, and behavioral leaves to surface tips and make decisions. Owns the loop-escalation ladder (ollama → deepseek → overmind → grok).",
    example: "python -m mag.decision_framework decide --goal \"<goal>\"",
  },
  "mag:router": {
    group: "decide",
    help: "Heuristic tier/route + model soft decisions → final route+seat",
    desc: "The router channel. Decides provider/tier and seat. Router/supervisor.py is the heuristic gate that produces the final route.",
    example: "python -m mag.router --goal \"<goal>\"",
  },
  "mag:supervisor": {
    group: "decide",
    help: "Router supervisor — authoritative route+seat decision",
    desc: "Heuristic routing gate (router/supervisor.py) that picks provider, tier, and seat.",
    example: "python -m mag.supervisor --goal \"<goal>\"",
  },
  "mag:fork_router": {
    group: "decide",
    help: "Route questions to the right fork",
    desc: "Decides which fork/strategy handles a question.",
    example: "python -m mag.fork_router --goal \"<goal>\"",
  },
  "mag:routing_concert": {
    group: "decide",
    help: "Concert routing — multiple signals into one route",
    desc: "Coordinates several routing signals into a single route decision.",
    example: "python -m mag.routing_concert",
  },
  "mag:rails": {
    group: "decide",
    help: "Hard rails — guard which routes/seats are allowed",
    desc: "Enforces routing constraints so the agent stays on allowed tracks.",
    example: "python -m mag.rails",
  },
  "tools:tier_probe": {
    group: "decide",
    help: "Right-size the tier empirically — A/B, objective scoring",
    desc: "Tests routing assumptions: 2 task shapes × 4 tiers, real model calls, objective scoring (no LLM judge), real prices. Adopted the 'test the assumption' ledger.",
    example: "python tools/tier_probe.py --design --exec",
  },
  "mag:temperature_stack": {
    group: "decide",
    help: "Temperature by task shape",
    desc: "Sets sampling temperature per task kind for stable output.",
    example: "python -m mag.temperature_stack --kind research",
  },
  "mag:refine_chain": {
    group: "decide",
    help: "Refine an answer through successive cheap passes",
    desc: "Chains cheap refinements instead of one expensive ask.",
    example: "python -m mag.refine_chain --goal \"<goal>\"",
  },
  // ── STATE ────────────────────────────────────────────────────────────────
  "mag:state_snapshot": {
    group: "state",
    help: "In-the-moment state classification → state_summaries.jsonl",
    desc: "capture_summary(goal, outcome, tier, kind, lessons) appends a structured, deduped row to the pile — the training + posterity feed.",
    example: "python -m mag.state_snapshot capture --goal \"<goal>\" --outcome ok",
  },
  "mag:verkle_audit": {
    group: "state",
    help: "Audit the verkle state tree, fix drift",
    desc: "Runs a full audit and repairs the verkle tree (freeze/check/gate a file's sha256 base before a spec applies).",
    example: "python -m mag.verkle_audit --full ; python -m mag.verkle_audit --fix",
  },
  "mag:verkle_knot": {
    group: "state",
    help: "Fold a leaf into the verkle knowledge knot",
    desc: "Writes a reasoning leaf into the tree so cheap models inherit strong output.",
    example: "python -m mag.verkle_knot --leaf \"<nugget>\"",
  },
  "mag:context_pack": {
    group: "state",
    help: "Compose the frozen context pack for a model",
    desc: "Builds the byte-identical prefix (system + bootloader + manifest + TIP + decision-DAG) so any tier reads the same state at cache-hit price.",
    example: "python -m mag.context_pack --goal \"<goal>\"",
  },
  "mag:memory_events": {
    group: "state",
    help: "Log memory events (read/write/fold)",
    desc: "Tracks what entered/exited memory for auditing and resonance.",
    example: "python -m mag.memory_events",
  },
  "mag:training_events": {
    group: "state",
    help: "Emit labeled training rows",
    desc: "Feeds the training pipeline with real decisions.",
    example: "python -m mag.training_events",
  },
  "mag:failure_kb": {
    group: "state",
    help: "Failure knowledge base — signatures + remedies",
    desc: "Stores failure signatures and maps them to remedies (FKB). The anti-cheat pattern detector.",
    example: "python -m mag.failure_kb --match \"<signature>\"",
  },
  "mag:run_trail": {
    group: "state",
    help: "Trail of runs — what happened, when, with what cost",
    desc: "Durable run history; the L1 self-improvement layer.",
    example: "python -m mag.run_trail --recent",
  },
  "mag:run_worth": {
    group: "state",
    help: "Score whether a run was worth it",
    desc: "Behavioral scoring of a run's value → feeds skill_ledger.",
    example: "python -m mag.run_worth --run <id>",
  },
  "mag:skill_ledger": {
    group: "state",
    help: "Case law ledger — record decisions + labeled rows",
    desc: "The right-sizing counter: record_decision (case-law pairs) + record_labeled_row (training rows) + progress(). Targets 1000 decisions / 5000 labeled rows.",
    example: "python main.py skill-ledger --progress",
  },
  "mag:idea_graph": {
    group: "state",
    help: "Map ideas into a knowledge graph",
    desc: "Builds an idea graph from packs and training rows; under-coverage drives next research topics.",
    example: "python -m mag.idea_graph --rebuild",
  },
  "mag:resonance": {
    group: "state",
    help: "Corpus lens — echo what's relevant to the goal",
    desc: "Cross-walks the current goal against historical behavior to surface resonance.",
    example: "python -m mag.resonance --goal \"<goal>\"",
  },
  "tools:pile_classify": {
    group: "state",
    help: "Long overnight job — drain the pile, classify with a local model",
    desc: "Drains state_summaries, classifies each with a LOCAL model (default gemma4), folds into skill_ledger + training_rows. Idempotent by id. Built for scheduler/downtime.",
    example: "python tools/pile_classify.py --limit 50",
  },
  "tools:classify_corpus": {
    group: "state",
    help: "Auto-producer — bulk classify the corpus into labeled rows",
    desc: "Local bulk classify (gemma4) + deepseek-v4-flash sample audit → labeled training rows.",
    example: "python tools/classify_corpus.py",
  },
  // ── LEARN ────────────────────────────────────────────────────────────────
  "mag:improve_loop": {
    group: "learn",
    help: "Behavioral compounding — L1→L4 self-improvement loop",
    desc: "L1 files trails, L2 scores training_events/FKB into candidates, L3 steps into RUN sheets/factory config, L4 talks via Grove poems and office cards.",
    example: "python -m mag.improve_loop",
  },
  "mag:behavioral_synth": {
    group: "learn",
    help: "Synthesize behavioral themes into a daily leaf",
    desc: "Turns behavioral events into a daily synthesized leaf.",
    example: "python -m mag.behavioral_synth --day today",
  },
  "mag:behavior_catch": {
    group: "learn",
    help: "Catch behavior events for scoring",
    desc: "Logs behavioral events (pro_fire/pro_learn, fake_success) that feed scoring.",
    example: "python -m mag.behavior_catch --event <event>",
  },
  "mag:grove": {
    group: "learn",
    help: "Talk back — Grove poems / office cards",
    desc: "The L4 'talk' layer that narrates what the loop learned.",
    example: "python -m mag.grove --poem",
  },
  "mag:remedy": {
    group: "learn",
    help: "Apply the remedy for a known failure signature",
    desc: "Maps an FKB signature to the fix and applies it.",
    example: "python -m mag.remedy --signature <sig>",
  },
  "mag:attention_ranker": {
    group: "learn",
    help: "Rank what deserves attention next",
    desc: "Prioritizes candidates from scoring for the next step.",
    example: "python -m mag.attention_ranker",
  },
  "mag:token_economy": {
    group: "learn",
    help: "Track token spend across tiers",
    desc: "Measures token/cost so the cheap-window doctrine is enforced with data.",
    example: "python -m mag.token_economy --report",
  },
  "mag:cost_ledger": {
    group: "learn",
    help: "Ledger of cost per run/provider",
    desc: "Records real cost so tier decisions are price-aware.",
    example: "python -m mag.cost_ledger --recent",
  },
  "mag:research_director": {
    group: "learn",
    help: "Direct research — pick topics from under-coverage",
    desc: "Selects the next research topic from idea-graph gaps.",
    example: "python -m mag.research_director --next",
  },
  "tools:topic_research": {
    group: "learn",
    help: "Research a topic → packs → idea graph + training rows",
    desc: "Drives a research topic through pack classification into the idea graph.",
    example: "python tools/topic_research.py --topic \"<topic>\"",
  },
  // ── RUN ──────────────────────────────────────────────────────────────────
  "mag:orchestrator": {
    group: "run",
    help: "Core orchestrator — queue, drain, reconcile",
    desc: "The drainer: pulls from the FIFO queue, runs agents, reaps stale/completed pids, reconciles the queue. The heart of the sovereign loop.",
    example: "python -m mag.orchestrator drain-once",
  },
  "mag:job_floor": {
    group: "run",
    help: "Designation manager on top of the orchestrator",
    desc: "States designated→claimed→executing→verifying→done|needs_escalate|stuck. Watchdog: stuck_jobs(max_s). The sandbox/containment layer.",
    example: "python main.py job-floor --status",
  },
  "mag:spec_gate": {
    group: "run",
    help: "Wrong-offset gate — freeze/check/gate a file before applying a spec",
    desc: "Blocks blind apply on drift. 'Trust bytes, not reports.' The authoritative server that never trusts the client.",
    example: "python main.py spec-gate --file <path> --spec <spec>",
  },
  "tools:spec_execute": {
    group: "run",
    help: "Frozen state → penny spec → local executes inside the spec",
    desc: "The 'spend on the spec, not the tier' pipeline: deepseek-v4-flash (thinking off) writes a penny spec, local executes inside it.",
    example: "python tools/spec_execute.py --goal \"<goal>\"",
  },
  "tools:local_bench": {
    group: "run",
    help: "Benchmark harness — task shapes × local models",
    desc: "Measures verifiable ok + fake_success across task shapes. Proved tool_plan was a broken verifier. Results → memory/runs/local_bench/.",
    example: "python tools/local_bench.py --shapes 9",
  },
  "tools:code_execution": {
    group: "run",
    help: "Sandboxed code execution",
    desc: "Executes code in a contained environment (job_floor containment).",
    example: "python tools/code_execution.py --check <file>",
  },
  "mag:factory_gate": {
    group: "run",
    help: "Factory phase gate",
    desc: "Gates whether a factory phase may run.",
    example: "python -m mag.factory_gate --phase <n>",
  },
  "mag:factory_machine": {
    group: "run",
    help: "Factory machine — run a factory phase",
    desc: "Executes a factory (v3 substrate) phase.",
    example: "python -m mag.factory_machine --phase <n>",
  },
  "mag:tripartite_boot": {
    group: "run",
    help: "Boot the tripartite loop",
    desc: "Starts the sovereign tripartite (route/queue/drain) loop.",
    example: "python -m mag.tripartite_boot",
  },
  "mag:operating_protocol": {
    group: "run",
    help: "Operating protocol — how the loop should behave",
    desc: "The rules the loop follows; the constitution at runtime.",
    example: "python -m mag.operating_protocol",
  },
  // ── OPS ──────────────────────────────────────────────────────────────────
  "mag:nervous_system": {
    group: "ops",
    help: "At-a-glance health — keys, ports, containment, gates",
    desc: "Probes keys (.env), ports (providers), containment (Docker), gate status (T0–T3). Feeds context_pack L0a, dashboard body, governance alerts. Trust glance + doctor JSON.",
    example: "python main.py nervous --json",
  },
  "mag:ops_graph": {
    group: "ops",
    help: "Categorize + visualize live telemetry as a knowledge graph",
    desc: "collect() live ops telemetry → categorize() into typed nodes/edges → render() live SVG radial. REST: GET /api/v1/graph/ops.",
    example: "python main.py ops-graph --ingest",
  },
  "mag:drainer_stats": {
    group: "ops",
    help: "Drainer status + queue stats",
    desc: "Reports drainer/queue/operator/fleet health. REST: GET /api/v1/drainer/stats.",
    example: "python -m mag.drainer_stats",
  },
  "mag:health": {
    group: "ops",
    help: "Health check endpoint",
    desc: "Liveness/health of the framework.",
    example: "python -m mag.health",
  },
  "mag:live_feed": {
    group: "ops",
    help: "Tail a live trail (overseer / ghost / drainer)",
    desc: "Streams a live feed of a subsystem's trail to the terminal.",
    example: "python -m mag.live_feed ghost",
  },
  "mag:governor": {
    group: "ops",
    help: "Governor — the autorun heartbeat",
    desc: "Supervises the autorun loop cadence.",
    example: "python -m mag.governor --status",
  },
  "mag:governor_autorun": {
    group: "ops",
    help: "Autorun loop — fills the queue when unattended",
    desc: "Fills the queue automatically (skips 'done') so the system works without being asked.",
    example: "python -m mag.governor_autorun --once",
  },
  "mag:janitor": {
    group: "ops",
    help: "Janitor — clean stale state / verkle / temp",
    desc: "Housekeeping: verkle audit + fix, temp cleanup.",
    example: "python -m mag.janitor --all",
  },
  "mag:system_map": {
    group: "ops",
    help: "Map of the whole system",
    desc: "Renders the framework system map.",
    example: "python -m mag.system_map",
  },
  "mag:spider": {
    group: "ops",
    help: "Watchdog — orchestrator stalls + FKB patterns",
    desc: "Watches for stalls and failure patterns, writes spider_trail.jsonl.",
    example: "python -m mag.spider --once",
  },
  // ── AGENTS ───────────────────────────────────────────────────────────────
  "mag:agent_cli": {
    group: "agents",
    help: "The coding agent — the running worker",
    desc: "Runs the agent loop: absorbs operator inbox at checkpoints, mutating tools, false-success guard, escalates on loop.",
    example: "python main.py agent --provider deepseek --query \"<goal>\"",
  },
  "mag:agent_desk": {
    group: "agents",
    help: "Desk — an agent workspace/seat",
    desc: "Runs an agent in a desk with its own context.",
    example: "python -m mag.agent_desk --seat <name>",
  },
  "mag:coding_session_orchestrator": {
    group: "agents",
    help: "Orchestrate a coding session",
    desc: "Coordinates the coding session lifecycle (steal_protocol integrated).",
    example: "python -m mag.coding_session_orchestrator",
  },
  "mag:coding_session_runner": {
    group: "agents",
    help: "Run a coding session",
    desc: "Executes a coding session against a goal.",
    example: "python -m mag.coding_session_runner --goal \"<goal>\"",
  },
  "mag:conductor": {
    group: "agents",
    help: "Conductor — direct the multi-agent ensemble",
    desc: "v4 MOLD conductor orchestrates desks/agents.",
    example: "python -m mag.conductor",
  },
  "mag:steward": {
    group: "agents",
    help: "Steward — manage seats",
    desc: "Tends the seats/fleet.",
    example: "python -m mag.steward --status",
  },
  "mag:seat_registry": {
    group: "agents",
    help: "Register seats",
    desc: "Tracks available seats/providers.",
    example: "python -m mag.seat_registry --list",
  },
  "mag:peer_handoff": {
    group: "agents",
    help: "Hand a task off between agents",
    desc: "Queues a handoff request another agent executes.",
    example: "python -m mag.peer_handoff --to <agent> --ask \"<ask>\"",
  },
  "mag:handoff_inbox": {
    group: "agents",
    help: "Handoff inbox — incoming asks",
    desc: "Lists/picks handoff requests.",
    example: "python -m mag.handoff_inbox --list",
  },
};

// Keyword-based fallback classifier for anything not curated above.
function assignGroup(name) {
  const n = String(name).toLowerCase();
  if (/(ghost|steer|inbox|skill_drop|tesuji|pro_library|clippy|socratic|intention_brief|compass|gauntlet)/.test(n)) return "steer";
  if (/(decision|router|supervisor|fork_router|routing_concert|tier_probe|temperature|refine|rails|ollama_policy|dispatch|fork)/.test(n)) return "decide";
  if (/(state_snapshot|verkle|context_pack|memory_events|training_events|failure_kb|run_trail|run_worth|skill_ledger|idea_|resonance|records|diary|biography|dossier|session_card|pile|ledger|knot)/.test(n)) return "state";
  if (/(improve|behavioral|behavior_|grove|story|remedy|attention_ranker|token_economy|cost_ledger|research|classify|topic)/.test(n)) return "learn";
  if (/(nervous|ops_graph|drainer|health|live_feed|governor|janitor|system_map|audit|spider|autorun|doctor|status)/.test(n)) return "ops";
  if (/(orchestrator|job_floor|spec_|local_bench|code_exec|factory|tripartite|boot|runtime|launch_pad|lifecycle|operating_protocol)/.test(n)) return "run";
  if (/(agent|desk|session|conductor|steward|seat|arena|autopilot|campaign|game_|handoff|coordination|voice_)/.test(n)) return "agents";
  return "ops";
}

function enrichItem(it) {
  const curated = CURATED[`${it.kind}:${it.name}`];
  it.group = (curated && curated.group) || assignGroup(it.name);
  if (curated && curated.help) it.help = curated.help;
  it.desc = (curated && curated.desc) || it.help;
  it.example = (curated && curated.example) || it.run || "";
  return it;
}

function scanSubcommands(root) {
  const txt = readText(path.join(root, "main.py"));
  const out = [];
  const re = /add_parser\(\s*"([a-z0-9_-]+)"\s*(?:,\s*help\s*=\s*"([^"]*)")?/g;
  let m;
  const seen = new Set();
  while ((m = re.exec(txt))) {
    if (seen.has(m[1])) continue;
    seen.add(m[1]);
    out.push({
      id: `cli:${m[1]}`,
      kind: "cli",
      name: m[1],
      help: m[2] || "",
      run: `${py(root)} main.py ${m[1]}`,
      file: "main.py",
      line: null,
    });
  }
  return out;
}

function scanModules(root, subdir) {
  const dir = path.join(root, subdir);
  if (!fs.existsSync(dir)) return [];
  const out = [];
  for (const f of fs.readdirSync(dir).sort()) {
    if (!f.endsWith(".py") || f === "__init__.py") continue;
    const txt = readText(path.join(dir, f));
    const m = txt.match(/"""(.*?)(?:\n\s*""")/s);
    let head = m ? m[1].split("\n")[0].trim() : "";
    head = head.split(" — ")[0].split(".")[0];
    out.push({
      id: `${subdir}:${f}`,
      kind: subdir,
      name: f.replace(/\.py$/, ""),
      help: head.slice(0, 120),
      run: subdir === "tools" ? `${py(root)} tools/${f}` : null,
      file: `${subdir}/${f}`,
      line: null,
    });
  }
  return out;
}

function scanLaunchers(root) {
  const out = [];
  for (const f of fs.readdirSync(root).sort()) {
    if (!f.endsWith(".cmd")) continue;
    const txt = readText(path.join(root, f));
    const m = txt.match(/REM\s+(.*)/);
    out.push({
      id: `launcher:${f}`,
      kind: "launcher",
      name: f.replace(/\.cmd$/, ""),
      help: m ? m[1].trim() : "",
      run: `"${path.join(root, f)}"`,
      file: f,
      line: null,
    });
  }
  return out;
}

function scanRoutes(root) {
  const txt = readText(path.join(root, "dashboard", "rest.py"));
  const out = [];
  const re = /\(\s*"(GET|POST|PUT|DELETE)",\s*"([^"]+)"/g;
  let m;
  const seen = new Set();
  while ((m = re.exec(txt))) {
    const key = `${m[1]} ${m[2]}`;
    if (seen.has(key)) continue;
    seen.add(key);
    out.push({
      id: `route:${m[1]}:${m[2]}`,
      kind: "route",
      name: `${m[2]}`,
      help: `${m[1]} — dashboard REST endpoint`,
      run: `curl -s http://127.0.0.1:8765${m[2]}`,
      file: "dashboard/rest.py",
      line: null,
    });
  }
  return out;
}

function scanProviders(root) {
  const txt = readText(path.join(root, "configs", "providers.yaml"));
  const out = [];
  const lines = txt.split("\n");
  let inProviders = false;
  for (let i = 0; i < lines.length; i++) {
    const ln = lines[i];
    if (/^providers:\s*$/.test(ln)) { inProviders = true; continue; }
    if (!inProviders) continue;
    const m = ln.match(/^  ([a-z0-9_]+):\s*$/);
    if (m) {
      const nameLine = lines[i + 1] || "";
      const nm = nameLine.match(/name:\s*(.*)/);
      out.push({
        id: `provider:${m[1]}`,
        kind: "provider",
        name: m[1],
        help: nm ? nm[1].trim() : "",
        run: null,
        file: "configs/providers.yaml",
        line: i + 1,
      });
    }
  }
  return out;
}

function py(root) {
  const p = path.join(root, ".venv", "Scripts", "python.exe");
  return fs.existsSync(p) ? `& "${p}"` : "python";
}

function scanAll(root) {
  return {
    root,
    scannedAt: new Date().toISOString(),
    groups: GROUPS,
    items: [
      ...scanSubcommands(root),
      ...scanModules(root, "mag"),
      ...scanModules(root, "tools"),
      ...scanLaunchers(root),
      ...scanRoutes(root),
      ...scanProviders(root),
    ].map(enrichItem),
  };
}

// ---------------------------------------------------------------------------
// Webview provider
// ---------------------------------------------------------------------------
class MagMapProvider {
  constructor(extensionUri) {
    this._extensionUri = extensionUri;
    this._view = null;
    this._lastData = null;
    this._timer = null;
    this._source = "offline";
  }

  dispose() {
    if (this._timer) {
      clearInterval(this._timer);
      this._timer = null;
    }
    this._view = null;
  }

  // The framework's own rule system owns the map: we poll the REST endpoint
  // (regenerated + served by mag/framework_map.py) with auto-refresh. Local
  // scan is only a fallback when the dashboard is unreachable.
  async _load(push = true) {
    const api = await fetchJson("/api/v1/framework/map");
    if (api && Array.isArray(api.items)) {
      this._lastData = { root: api.root || findProjectRoot(), groups: api.groups, items: api.items };
      this._source = "framework";
    } else {
      this._lastData = scanAll(findProjectRoot());
      this._source = "offline";
    }
    if (push && this._view) {
      this._view.webview.postMessage({ type: "data", data: this._lastData, source: this._source });
    }
    return this._lastData;
  }

  refresh() {
    this._load(true);
  }

  resolveWebviewView(webviewView) {
    this._view = webviewView;
    webviewView.webview.options = {
      enableScripts: true,
      localResourceRoots: [vscode.Uri.joinPath(this._extensionUri, "media")],
    };
    webviewView.webview.html = this._html();

    webviewView.webview.onDidReceiveMessage(async (msg) => {
      switch (msg.type) {
        case "ready": {
          await this._load(true);
          // Auto-refresh: keep the map fresh without a manual rescan. Polls the
          // framework-owned REST payload so it stays in sync with the loop.
          if (this._timer) clearInterval(this._timer);
          const secs = Math.max(15, vscode.workspace.getConfiguration("magMap").get("refreshSeconds", 60));
          this._timer = setInterval(() => this._load(true), secs * 1000);
          break;
        }
        case "run": {
          const term = vscode.window.createTerminal({ name: "MAG", cwd: findProjectRoot() });
          term.show();
          term.sendText(msg.cmd);
          break;
        }
        case "open": {
          const root = findProjectRoot();
          const p = path.join(root, msg.file);
          if (fs.existsSync(p)) {
            const doc = await vscode.workspace.openTextDocument(p);
            const ed = await vscode.window.showTextDocument(doc);
            if (msg.line) {
              const range = new vscode.Range(msg.line - 1, 0, msg.line - 1, 0);
              ed.revealRange(range);
            }
          }
          break;
        }
      }
    });
  }

  _html() {
    const media = (file) =>
      this._view.webview.asWebviewUri(vscode.Uri.joinPath(this._extensionUri, "media", file));
    return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="Content-Security-Policy"
  content="default-src 'none'; style-src ${this._view.webview.cspSource}; script-src ${this._view.webview.cspSource}; img-src ${this._view.webview.cspSource} data:;">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="${media("map.css")}" rel="stylesheet">
<title>MAG Framework Map</title>
</head>
<body>
  <header class="mh">
    <div class="mh-title">
      <span class="mh-badge">マグ</span>
      <div>
        <div class="mh-name">Framework Map</div>
        <div class="mh-root" id="mh-root">…</div>
      </div>
    </div>
    <div class="mh-tools">
      <input id="search" class="mh-search" type="text" placeholder="filter by name, description, file…" autocomplete="off" spellcheck="false">
      <select id="kind" class="mh-kind" title="filter by function"></select>
    </div>
    <div class="mh-stats" id="stats"></div>
  </header>
  <main id="list" class="ml"></main>
  <div id="tip" class="tip" hidden></div>
  <footer class="mf">
    <span id="f-count"></span>
    <span id="f-source" class="mf-src" title="where the map data comes from"></span>
    <button id="refresh" title="refresh now">⟳ refresh</button>
  </footer>
  <script src="${media("map.js")}"></script>
</body>
</html>`;
  }
}

// ---------------------------------------------------------------------------
// Activation
// ---------------------------------------------------------------------------
function activate(context) {
  const provider = new MagMapProvider(context.extensionUri);

  // ── MAG Section Views: each section is its own left-activity-bar button ──
  // (Replaces the monolithic Control Room, which crashed when any one section
  //  errored. Each view polls only its own endpoints — isolated and robust.)
  try {
    const { buildViews } = require("./mag_views.js");
    const views = buildViews();
    const viewMap = {
      "magControlRoom.thoughtSurface": views.thoughtSurface,
      "magControlRoom.drainerView": views.drainerView,
      "magControlRoom.ghostView": views.ghostView,
      "magControlRoom.opsGraph": views.opsGraph,
      "magControlRoom.handoffView": views.handoffView,
      "magControlRoom.surfaceHub": views.surfaceHub,
    };
    for (const [viewId, inst] of Object.entries(viewMap)) {
      context.subscriptions.push(
        vscode.window.registerWebviewViewProvider(viewId, inst, {
          webviewOptions: { retainContextWhenHidden: false },
        })
      );
    }
    context.subscriptions.push(
      vscode.commands.registerCommand("magMap.thoughtSurface", () =>
        vscode.commands.executeCommand("magControlRoom.thoughtSurface.focus")
      )
    );
    context.subscriptions.push(
      vscode.commands.registerCommand("magMap.opsGraphView", () =>
        vscode.commands.executeCommand("magControlRoom.opsGraph.focus")
      )
    );
    context.subscriptions.push(
      vscode.commands.registerCommand("magMap.drainerView", () =>
        vscode.commands.executeCommand("magControlRoom.drainerView.focus")
      )
    );
    context.subscriptions.push(
      vscode.commands.registerCommand("magMap.ghostView", () =>
        vscode.commands.executeCommand("magControlRoom.ghostView.focus")
      )
    );
    context.subscriptions.push(
      vscode.commands.registerCommand("magMap.surfaceAudit", () =>
        vscode.commands.executeCommand("magControlRoom.surfaceHub.focus")
      )
    );
    // Status-bar button — opens the Thought Surface (the live agent streams).
    const statusBtn = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 20);
    statusBtn.text = "$(pulse) MAG";
    statusBtn.tooltip = "MAG Thought Surface — live agent streams";
    statusBtn.command = "magMap.thoughtSurface";
    statusBtn.show();
    context.subscriptions.push(statusBtn);
  } catch (e) {
    // Section views are optional; framework map still works if they fail.
  }

  context.subscriptions.push(
    vscode.window.registerWebviewViewProvider("magMap.view", provider, {
      webviewOptions: { retainContextWhenHidden: false },
    })
  );
  context.subscriptions.push(provider);
  context.subscriptions.push(
    vscode.commands.registerCommand("magMap.open", () =>
      vscode.commands.executeCommand("magMap.view.focus")
    )
  );
  context.subscriptions.push(
    vscode.commands.registerCommand("magMap.refresh", () => provider.refresh())
  );
  context.subscriptions.push(
    vscode.commands.registerCommand("magMap.quickRun", async () => {
      const root = findProjectRoot();
      const data = scanAll(root);
      const picks = data.items
        .filter((i) => i.run)
        .map((i) => ({
          label: `$(terminal) ${i.name}`,
          description: i.help,
          detail: i.run,
          item: i,
        }));
      const picked = await vscode.window.showQuickPick(picks, {
        matchOnDescription: true,
        placeHolder: "Pick a framework command to run…",
      });
      if (picked) {
        const term = vscode.window.createTerminal({ name: "MAG", cwd: root });
        term.show();
        term.sendText(picked.item.run);
      }
    })
  );

  // ── Ghost commands ──

  context.subscriptions.push(
    vscode.commands.registerCommand("magMap.ghostSense", () => {
      const root = findProjectRoot();
      const term = vscode.window.createTerminal({ name: "MAG Ghost", cwd: root });
      term.show();
      term.sendText(`${py(root)} -m mag.ghost --sense`);
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand("magMap.ghostCatalog", () => {
      const root = findProjectRoot();
      const term = vscode.window.createTerminal({ name: "MAG Ghost", cwd: root });
      term.show();
      term.sendText(`${py(root)} -m mag.ghost --catalog`);
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand("magMap.ghostDeploy", async () => {
      const root = findProjectRoot();
      const text = await vscode.window.showInputBox({
        placeHolder: "Steer text to deploy through operator_inbox…",
        prompt: "Enter the test vector text. It will be injected into the running agent's context at the next checkpoint.",
        validateInput: (v) => v && v.trim().length >= 5 ? null : "Vector must be at least 5 characters",
      });
      if (text) {
        const escaped = text.replace(/"/g, '\\"');
        const term = vscode.window.createTerminal({ name: "MAG Ghost", cwd: root });
        term.show();
        term.sendText(`${py(root)} -m mag.ghost --deploy "${escaped}"`);
      }
    })
  );

  // ── Janitor commands ──

  context.subscriptions.push(
    vscode.commands.registerCommand("magMap.janitorVerkle", () => {
      const root = findProjectRoot();
      const term = vscode.window.createTerminal({ name: "MAG Janitor", cwd: root });
      term.show();
      term.sendText(`${py(root)} -m mag.verkle_audit --full ; ${py(root)} -m mag.verkle_audit --fix`);
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand("magMap.janitorCycle", () => {
      const root = findProjectRoot();
      const term = vscode.window.createTerminal({ name: "MAG Janitor", cwd: root });
      term.show();
      term.sendText(`${py(root)} -m mag.ghost --deploy "Check FKB before retrying. Apply remedy first." ; ${py(root)} -m mag.ghost --catalog`);
    })
  );

  // ── Live feeds: running terminal tabs tailing the overseer / ghost / drainer trails ──

  function openLiveFeed(root, kind, label) {
    const term = vscode.window.createTerminal({ name: label || `MAG ${kind}`, cwd: root });
    term.show();
    term.sendText(`${py(root)} -m mag.live_feed ${kind}`);
  }

  context.subscriptions.push(
    vscode.commands.registerCommand("magMap.liveOverseer", () => {
      openLiveFeed(findProjectRoot(), "overseer", "MAG Live · Overseer");
    })
  );
  context.subscriptions.push(
    vscode.commands.registerCommand("magMap.liveGhost", () => {
      openLiveFeed(findProjectRoot(), "ghost", "MAG Live · Ghost");
    })
  );
  context.subscriptions.push(
    vscode.commands.registerCommand("magMap.liveDrainer", () => {
      openLiveFeed(findProjectRoot(), "drainer", "MAG Live · Drainer");
    })
  );
  context.subscriptions.push(
    vscode.commands.registerCommand("magMap.drainerStats", () => {
      const root = findProjectRoot();
      const term = vscode.window.createTerminal({ name: "MAG Drainer Stats", cwd: root });
      term.show();
      term.sendText(`${py(root)} -m mag.drainer_stats`);
    })
  );

  // ── Ripgrep: fast project code search via rg (installed; no terminal tab) ──
  context.subscriptions.push(
    vscode.commands.registerCommand("magMap.rgSearch", async () => {
      const root = findProjectRoot();
      const pattern = await vscode.window.showInputBox({
        prompt: "Ripgrep pattern (fast code search)",
        placeHolder: "e.g. def sense_context",
      });
      if (!pattern) return;
      execFile(
        "rg",
        ["--no-ignore", "--hidden", "-n", "--max-count", "5", "--", pattern, root],
        { maxBuffer: 8 * 1024 * 1024 },
        async (err, stdout, stderr) => {
          if (!stdout) {
            vscode.window.showInformationMessage("rg: no matches");
            return;
          }
          const picks = stdout.split("\n").filter(Boolean).slice(0, 200).map((l) => {
            const i1 = l.indexOf(":");
            const i2 = l.indexOf(":", i1 + 1);
            const file = l.slice(0, i1);
            const line = parseInt(l.slice(i1 + 1, i2), 10) || 1;
            return { label: `$(search) ${file}:${line}`, description: l.slice(i2 + 1).slice(0, 140), file, line };
          });
          const picked = await vscode.window.showQuickPick(picks, {
            matchOnDescription: true,
            placeHolder: `${picks.length} matches — pick to open`,
          });
          if (picked) {
            const doc = await vscode.workspace.openTextDocument(path.join(root, picked.file));
            const ed = await vscode.window.showTextDocument(doc);
            ed.revealRange(new vscode.Range(picked.line - 1, 0, picked.line - 1, 0));
          }
        }
      );
    })
  );

  // ── Ops Knowledge Graph: categorized live telemetry as a webview panel ──
  context.subscriptions.push(
    vscode.commands.registerCommand("magMap.opsGraph", () => {
      const { OpsGraphPanel } = require("./graph.js");
      OpsGraphPanel.create(context.extensionUri);
    })
  );

  // ── Handoff requests: auto-open a new tab executing the ask ──

  const requestsDir = () => path.join(findProjectRoot(), "queue", "handoff", "requests");

  function readHandoffRequests(root) {
    const dir = path.join(root, "queue", "handoff", "requests");
    if (!fs.existsSync(dir)) return [];
    const out = [];
    for (const f of fs.readdirSync(dir).sort()) {
      if (!f.endsWith(".json")) continue;
      try {
        const req = JSON.parse(fs.readFileSync(path.join(dir, f), "utf8"));
        out.push({ file: path.join(dir, f), req });
      } catch {
        // skip malformed request files — do not delete, surface for operator
        out.push({ file: path.join(dir, f), req: { ask: `(malformed request: ${f})`, provider: "deepseek" } });
      }
    }
    return out;
  }

  function openAskTab(root, req, label) {
    const ask = (req.ask || req.goal || "").toString().trim();
    const provider = (req.provider || req.assignee || "deepseek").toString().trim() || "deepseek";
    const term = vscode.window.createTerminal({
      name: label || `MAG Handoff · ${provider}`,
      cwd: root,
      env: { MAG_HANDOFF_ASK: ask },
    });
    term.show();
    // One-shot agent run executes the ask in a fresh tab; fall back to steer if ask empty.
    if (ask) {
      const esc = ask.replace(/(["$`\\])/g, "\\$1").replace(/\r?\n/g, " ");
      term.sendText(`${py(root)} main.py agent --provider ${provider} --query "${esc}"`);
    } else {
      term.sendText(`# no ask text on request ${label || ""} — dropping to interactive REPL`);
      term.sendText(`${py(root)} main.py agent --provider ${provider}`);
    }
  }

  // Manual: pick a pending request and run it in a new tab.
  context.subscriptions.push(
    vscode.commands.registerCommand("magMap.handoffRun", async () => {
      const root = findProjectRoot();
      const requests = readHandoffRequests(root);
      if (requests.length === 0) {
        vscode.window.showInformationMessage("No pending handoff requests in queue/handoff/requests/");
        return;
      }
      const picks = requests.map((r) => ({
        label: `$(play) ${(r.req.ask || r.req.goal || r.req.id || "untitled").toString().slice(0, 60)}`,
        description: `${r.req.provider || r.req.assignee || "deepseek"} · ${path.basename(r.file)}`,
        item: r,
      }));
      const picked = await vscode.window.showQuickPick(picks, { matchOnDescription: true, placeHolder: "Pick a handoff request to execute in a new tab…" });
      if (picked) openAskTab(root, picked.item.req, `MAG Handoff · ${path.basename(picked.item.file, ".json")}`);
    })
  );

  // Auto: when a new request file lands, open a tab executing it immediately.
  const watcher = vscode.workspace.createFileSystemWatcher(
    new vscode.RelativePattern(findProjectRoot(), "queue/handoff/requests/*.json")
  );
  watcher.onDidCreate((uri) => {
    const root = findProjectRoot();
    try {
      const req = JSON.parse(fs.readFileSync(uri.fsPath, "utf8"));
      openAskTab(root, req, `MAG Handoff · ${path.basename(uri.fsPath, ".json")}`);
    } catch {
      vscode.window.showWarningMessage(`MAG: handoff request ${path.basename(uri.fsPath)} is not valid JSON — fix it before it can run.`);
    }
  });
  context.subscriptions.push(watcher);
  context.subscriptions.push(
    vscode.commands.registerCommand("magMap.handoffWatch", () => {
      vscode.window.showInformationMessage(
        "MAG is watching queue/handoff/requests/*.json — dropping a request opens a new tab that executes its ask."
      );
    })
  );
}

function deactivate() {}

module.exports = { activate, deactivate };
