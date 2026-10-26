# SWARM MECHANICS STEAL (STEAL-1) - external swarm mechanics swept and diffed against ours

**Schema:** steal.swarm-mechanics.v1 - **ts:** 2026-10-02T01:05Z - **lane:** STEAL-1 (ZCode subagent)
**Mission (operator):** "steal externally for any swarm mechanics we might miss... i want the swarm
communicating in ribs and doing our genetic lensing and algos"
**Method:** prior-art sweep first (estate corpus: `corpus/library/jev_steal_library/sovereign_ai_fleet_consolidated_bibliography (2).md`,
ms-agents-beginners A2A chapter), then live sweep of 2025-2026 external work. research-pack was used
for one primary source (AlphaEvolve: pack `memory/research_packs/20261002T003151Z_alphaevolve-steal.json`,
text at `memory/ingest/local/web/deepmind.google-2993a5d8d0f3.txt`); the rest rode WebSearch with
per-citation provenance marks. Search lane was rate-limited (1302s) for a stretch; every citation
below carries its provenance so nothing unverifiable is laundered into fact.

**Provenance marks:** `[V]` = URL surfaced by a live search/fetch this session - `[E]` = already
verified inside the estate corpus bibliography - `[M]` = arXiv id/venue from model memory, facts
consistent with what the sweep surfaced, exact id unverified this session. Treat `[M]` rows as
leads, not law.

## OURS (the estate inventory this receipt diffs against)

1. **tools/code_swarm.py** (SWARM-1, 2026-10-01): 3 near-free families (kimi, glm-flash, deepseek)
   x target files, ThreadPoolExecutor width 10, sha-stamped manifest rows, contract bytes IDENTICAL
   across families (G2 law), inference_budget rail (recipes, refusal + EMPTY_REASONING terminals),
   usd cap checked per dispatch, claim-level convergence: 2+ families + line-window overlap +
   lexical claim overlap = REAL; same window different diagnosis = CO-LOCATION, never agreement.
   Receipt: `watch/inbox/model_garden/SWARM_1.md` (159 asks, $0.218 of $2.00, 50 REAL / 35
   CO-LOCATION / 194 UNIQUE).
2. **The salon mesh** (`watch/salon_runner.py` v4 + `.agents/skills/salon/SKILL.md`): 7 shapes fired
   simultaneously at 7 distinct vendors; blind divergence by construction (MAG CHORD v4: never read
   another post before writing yours), then intercommunication (posts read each other) and
   convergence (fold, gate floor 150 chars, tri-state Supported/Disputed/Unproven, S6/S7 synthesis).
   `mag/frontier_salon.py` adds the roshomon combine (shared invariant + distinct contributions)
   with the Huang gate on roundtable escalation.
3. **Stigmergy + shared mind** (`mag/swarm_tools.py`): content-addressed pheromone marks
   (trail/fruitful/dead/here/danger/signal/drift), drift-targets, blackboard with decisions +
   conflicts pinned forever and non-pinned evicted past 4000, steer gating, switchboard authority
   on pinned kinds, stateless content-addressed scratchpad (knots), swarm_sense fog-of-war fusion,
   memlance (mount ribs + fold back), trust-gated verkle_write.
4. **Ribs as law substrate** (`memory/rib/`, rib_bus mount/publish): boot order load ribs -> load
   state -> act; AGENTS.md carries machine-parsed law (census carrier grammar, fail-close tripwire).
5. **Claritas faces** (`mag/claritas.py`): per-vendor system prompts distilled from the CL4R1T4S
   corpus + behavioral animal_profiles rows.
6. **inference_budget gates** (`mag/inference_budget.py`, rib RIB_INFERENCE_BUDGET_20261001):
   plan_call recipes per animal, reasoning-burn class-kill, usage ledger.

## THEIRS (27 mechanisms, each: cite, one line, verdict)

### A. Agent-to-agent protocols

1. **Google A2A (Agent2Agent) protocol** - Google Developers Blog, April 2025 announcement, donated
   to the Linux Foundation June 2025 `[M for URLs, facts E via corpus ms-agents-beginners/11-agentic-protocols]`
   (https://developers.googleblog.com/en/a2a-a-new-era-of-interoperability-for-ai-agents/).
   Open wire protocol for cross-vendor agents: agent cards at /.well-known (identity, capabilities,
   auth), task lifecycle state machine (submitted/working/input-required/completed/failed/canceled),
   SSE streaming, artifacts as deliverables.
   PRIOR ART THIS LANE ALMOST MISSED: the estate already interoped live -
   `watch/inbox/A2A_FIRST_PROBE_20260925.md` (PASS: a2a-sdk 1.1.5 installed in the estate venv,
   a real public agent card resolved off the wire and decoded into `a2a_pb2.AgentCard`, $0, full
   evidence filed beside it). The descent prior-art-sweep law paid for itself on this row.
   VERDICT: **WE-HAVE-BETTER** for our shape: our agents are same-estate processes and communicate
   through the shared inbox contract + switchboard authorization + content-hashed receipts, which
   out-audits a JSON task object; remote discovery we have already probed end-to-end, so the day
   Hermes/janitors serve off-box the wire is proven, not new.
2. **MCP multi-agent patterns** - Anthropic, "Building Effective Agents", Dec 2024, and the MCP
   spec (https://www.anthropic.com/engineering/building-effective-agents, https://modelcontextprotocol.io) `[M]`:
   orchestrator-workers, evaluator-optimizer, prompt-chaining as named composition patterns over a
   standard tool/server protocol.
   VERDICT: **WE-HAVE-IT** - orchestrator-workers is the garden/code_swarm shape, evaluator-optimizer
   is the salon fold; the missing sliver is an MCP client in the swarm toolbelt (workers could mount
   external MCP servers as organs). Noted, not top-3.
3. **OpenAI Agents SDK handoffs** - OpenAI Agents SDK, March 2025 (successor to the experimental
   Swarm framework), handoffs + agents-as-tools + guardrails + sessions + tracing
   (https://openai.github.io/agents-python/agents, cookbook
   https://developers.openai.com/cookbook/examples/agents_sdk/multi-agent-portfolio-collaboration/multi_agent_portfolio_collaboration) `[V]`:
   in-process agent-to-agent delegation as a first-class primitive.
   VERDICT: **WE-HAVE-BETTER** - our handoffs are file-mediated (ask dirs, manifests, receipts), so
   they survive crashes and are sha-auditable; SDK handoffs live and die with the process. Their
   unified tracing view is nice; our usage ledger + manifest is the auditable equivalent.

### B. Swarm topologies

4. **Multi-agent debate** - Du et al., "Improving Factuality and Reasoning in Language Models
   through Multiagent Debate", arXiv:2305.14325, ICML 2024 `[M]`; 2026 controlled follow-up "The
   Impact of Multi-Agent Debate Protocols on Debate Quality", arXiv:2603.28813 `[V]`
   (protocol details, not just debate-vs-solo, drive outcomes). N agents argue rounds, converge on
   answers.
   VERDICT: **WE-HAVE-IT** - salon S2 attacker + the mesh rounds are debate; and on the convergence
   side we are ahead of the literature: code_swarm's REAL vs CO-LOCATION split is a machine-checked
   debate verdict that refuses to count co-location as agreement (most debate papers still score
   majority vote).
5. **Mixture-of-Agents (MoA)** - Wang et al., "Mixture-of-Agents Enhances Large Language Model
   Capabilities", arXiv:2406.04692, 2024 `[M id, facts V via search]`: layered proposers feed an
   LLM aggregator; stackable layers; AlpacaEval 2.0 SOTA at GPT-4o-level quality for open-model cost.
   VERDICT: **WE-HAVE-BETTER** core, one gap: our rollup aggregator is deterministic (lexical sig
   + window union-find), $0 and reproducible where theirs pays an LLM judge per layer; the gap is
   stacked layers, which we do not need. Stealable sliver: one CHEAP judge pass to triage CO-LOCATION
   clusters only (folded into ticket T1's fitness loop, since the judge defines the reward).
6. **Societies of minds / mindstorms** - "Mindstorms in Natural Language-Based Societies of Minds",
   arXiv:2305.17066 `[V]`; benchmarks: MAS-BENCH distributed sorting under communication constraints
   (ACL 2026 Findings, https://aclanthology.org/2026.findings-acl.1698.pdf) `[V]`, AgentWorld
   long-horizon collaboration (arXiv:2609.31590, 2026) `[V]`; "Emergent Coordination in Multi-Agent
   Language Models", arXiv:2510.05174, 2025 `[V]` (information-theoretic higher-order coordination).
   Emergent consensus/collusion cascades in agent societies; benchmarks measuring coordination under
   partial observability.
   VERDICT: **WE-HAVE-IT** - we already banked the negative result as law:
   `memory/rib/RIB_MINDSWEAVE_EVAL_CONSENSUS_ILLUSION_20260810.md` (consensus illusion). The 2026
   benchmarks would let us MEASURE our mesh (salon intercommunication rounds as a MAS-BENCH-style
   constrained channel); candidate dogfood, not top-3.
7. **Dynamic team formation** - DyLAN, "A Dynamic LLM-Powered Agent Network for Task-Oriented Agent
   Collaboration", arXiv:2310.02170, COLM 2024 `[M id, V via 2609.05933 citation]`: agent-importance
   scoring prunes who stays in the team per task; "Rethinking the Evaluation of Efficiency Methods
   for Multi-Agent Systems", arXiv:2609.05933, 2026 `[V]` measures what such pruning actually buys.
   VERDICT: **WE-LACK-IT** -> ticket T2. Our family set and salon shape set are static; the estate
   already learned the manual version of this law (kimi EMPTY_REASONING terminals) but nothing
   measures per-family marginal contribution or demotes a family automatically.
8. **Topology as an optimizable graph** - GPTSwarm, "Language Agents as Optimizable Graphs",
   arXiv:2402.16823, ICML 2024 `[M]`; MacNet, "Scaling Large-Language-Model-based Multi-Agent
   Collaboration", arXiv:2406.07155 `[M]`: represent the swarm as a computational graph and optimize
   edges/nodes rather than hand-designing the org chart.
   VERDICT: **WE-LACK-IT** - nobody rewires our salon/code_swarm topology from measured outcomes;
   folded into tickets T1/T2 (the dispatch shape becomes an evolvable config).

### C. Evolutionary + search mechanics with LLMs

9. **FunSearch / AlphaEvolve evaluator-driven program evolution** - Romera-Paredes et al.,
   "Mathematical discoveries from program search with LLMs", Nature 621, 2023
   (https://www.nature.com/articles/s41586-023-06924-6) `[M]`; AlphaEvolve, DeepMind blog, May 2025
   `[V, primary text fetched via research-pack]`: prompt sampler assembles a prompt -> LLMs propose
   programs/diffs -> automated evaluators score -> a programs database implements the evolutionary
   algorithm that decides which programs seed future prompts (MAP-Elites-style islands).
   VERDICT: **WE-LACK-IT** -> ticket T1 (the single best adoption). We have every organ (graded
   rollup.json, sha manifests, gated rail, $ metering) but no loop: nothing mutates our CONTRACT or
   asks and retains winners by measured fitness.
10. **Darwin Godel Machine** - "Darwin Godel Machine: Open-Ended Evolution of Self-Improving
    Agents", Sakana AI + UBC, arXiv:2505.22954, May 2025 `[M]`: agents self-modify their own code,
    evaluated in an archive; island populations fight deception.
    VERDICT: **WE-LACK-IT** in the self-modification sense, deliberately: our ratchet + workflow
    gate + spec-before-behavior laws forbid ungated self-modification; the steal is the ARCHIVE
    (every mutation retained with its benchmark delta), folded into T1's program database and T3's
    rib fitness history.
11. **Automated agentic-system/workflow search** - ADAS, "Automated Design of Agentic Systems",
    arXiv:2408.08435, ICLR 2025 `[M]` (a meta-agent programs new agents in code); AFlow,
    "Automating Agentic Workflow Generation", arXiv:2410.10762, ICLR 2025 `[M]` (MCTS over workflow
    graphs, LLM mutations); "Evolutionary Generation of Multi-Agent Systems", arXiv:2602.06511,
    2026 `[V]` (evolves whole MAS, positions itself past per-agent evolution).
    VERDICT: **WE-LACK-IT** - no automated search over our dispatch shapes; T1 is the estate-sized
    version of this (search over contracts + family mix, fitness from rollups).
12. **EvoAgent** - "EvoAgent: Towards Automatic Multi-Agent Generation", arXiv:2406.14228, ACL 2025
    `[V]` (https://arxiv.org/abs/2406.14228): mutation + crossover over agent attributes (prompts,
    roles, tools) with selection into an agent population.
    VERDICT: **WE-LACK-IT** - our agent specs (families, shapes, toolbelts) are hand-written; the
    crossover operation over (contract, face, toolbelt) triples is exactly the genetic lensing the
    operator asked for; folded into T1.
13. **MasRouter** - "MasRouter: Learning to Route LLMs for Multi-Agent Systems", arXiv:2502.11133,
    ACL 2025 `[V]`: a learned cascaded controller picks collaboration mode, roles, and which LLM
    backbone each agent gets, trading performance vs cost.
    VERDICT: **WE-HAVE-BETTER for now**: our routing is LAW, not a learned network (driving ladder,
    tier ladder, RIB_MODEL_GARDEN_ROUTING), auditable and operator-owned; a learned router is
    unauditable and we do not have the volume to train one. Revisit only if the fleet grows past
    hand-law scale.
14. **GEPA** - "GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning",
    arXiv:2507.19457, 2025 `[V]`: reflective, textual mutation of prompts with multi-objective
    Pareto retention; beats GRPO by ~6% average while using up to 35x fewer rollouts.
    VERDICT: **WE-LACK-IT** -> the engine inside ticket T1. Our contracts/faces are hand-written;
    GEPA's reflective mutation + Pareto retention is the cheapest known loop for evolving them,
    and it needs only rollouts we already meter.

### D. Stigmergy + blackboard

15. **SwarmWorld** - "SwarmWorld: Stigmergic technological evolution in societies of language-model
    agents", MIT (Buehler group), arXiv:2608.26081, Aug 2026 `[V]`: LM agents coordinate through
    persistent artifacts and constructed traces in a shared world instead of messages; technological
    evolution emerges stigmergically.
    VERDICT: **WE-HAVE-IT** - pheromone marks + knots + ribs are our stigmergy, and ours is
    content-addressed and trust-gated where theirs is simulation-scale. Their lesson for us: the
    ARTIFACTS agents construct (not just marks) carry the evolution; our drift-targets already
    gesture at this.
16. **Pressure-field coordination** - "Emergent Coordination in Multi-Agent Systems via Pressure
    Fields", arXiv:2601.08129, 2026 `[V]`: scalar fields replace orchestrators/message-passing;
    agents need only local context.
    VERDICT: **WE-HAVE-IT** - pheromone kinds (danger/fruitful/dead/signal/drift) are our field;
    the 2026 paper's claim that field-mediated coordination cuts tokens matches our $0 no-message
    design.
17. **Classic blackboard architecture** - Hearsay-II (Erman, Hayes-Roth, Lesser, Reddy, "The
    Hearsay-II Speech-Understanding System", ACM Computing Surveys 12(2), 1980) and BB1 (Hayes-Roth,
    "A Blackboard Architecture for Control", Artificial Intelligence 26(3), 1985) `[E, corpus V]`.
    VERDICT: **WE-HAVE-IT** - swarm_blackboard is a direct descendant; the corpus bibliography's
    line is the law to remember: "blackboards died on scheduling, not representation", and our
    switchboard/effect broker is the scheduler answer those systems lacked.
18. **Governed shared memory for agent fleets** - "Governed Shared Memory for Multi-Agent LLM
    Systems", arXiv:2606.24535, 2026 `[V]`: moves fleets from isolated chat histories to shared
    state with governance.
    VERDICT: **WE-HAVE-BETTER** - our shared state (inbox, blackboard, knots) is governed by
    trust_gate verdicts, authority labels, pinned-kind switchboard authorization, and fail-closed
    writes; governance as a first-class verdict is ahead of the 2026 paper's shape.

### E. Shared-law-artifact communication (the ribs question)

19. **Linda generative communication** - Gelernter, "Generative Communication in Linda", ACM TOPLAS
    7(1), 1985 `[E, corpus V]`: agents communicate by dropping typed tuples into a shared tuple
    space, decoupled in time and process.
    VERDICT: **WE-HAVE-IT** - the shared inbox + content-addressed knots are a Linda with hashes;
    the md-record law (every durable write gets a register event) is the tracking Linda never had.
20. **ACE (Agentic Context Engineering)** - "Agentic Context Engineering: Evolving Contexts for
    Self-Improving Language Models", arXiv:2510.04618, ICLR 2026 `[V]`
    (https://arxiv.org/abs/2510.04618): worker + inspector + curator agents coordinate by reading
    and writing ONE evolving shared markdown playbook; reported ~10.6% benchmark gain with 86.9%
    latency and 75.1% cost cuts vs fine-tuning-style adaptation.
    VERDICT: **WE-HAVE-IT** (ribs ARE this: law files the swarm mounts before acting and folds back
    into) - but THEY have the loop we lack: an automated curator that edits the shared law with
    eval feedback. That loop is ticket T3.
21. **Letta shared memory blocks** - Letta (ex-MemGPT), 2025 product/docs `[V via secondary, M for
    canonical URL]`: editable core memory blocks shared across multiple agents as the coordination
    substrate.
    VERDICT: **WE-HAVE-BETTER** - ribs are versioned LAW with hash chains, trust gates, and
    boot-order enforcement, not scratch memory; their editable-blocks UX is the one polish worth
    noting (rib_bus.mount returns doctrine; a block-style diff view would make drift visible).
22. **MetaGPT SOPs** - Hong et al., "MetaGPT: Meta Programming for Multi-Agent Collaborative
    Framework", arXiv:2308.00352, ICLR 2024 `[E, corpus V]`: encodes Standardized Operating
    Procedures as prompt artifacts + a shared message pool with structured outputs, replacing
    unstructured chat.
    VERDICT: **WE-HAVE-IT** - AGENTS.md + the salon shape train + the load-order table are our SOP
    substrate; we additionally machine-enforce ours (parse_carrier tripwire), which MetaGPT does
    not.
23. **Anthropic Agent Skills** - "Equipping agents for the real world with Agent Skills", Anthropic
    Engineering, Oct 16 2025 `[V]`
    (https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills):
    SKILL.md folders with instructions/scripts/resources loaded on demand, now an open standard.
    VERDICT: **WE-HAVE-IT** - this seat runs on that exact mechanism (.agents/skills/salon is a
    SKILL.md); the estate additionally gates its skills' behavior with workflow-gate law.
24. **AGENTS.md standard** - open convention adopted across coding agents in 2025 `[M general]`:
    one law file at repo root that every agent loads first.
    VERDICT: **WE-HAVE-BETTER** - ours is not just loaded, it is PARSED AND ENFORCED: the census
    carrier grammar law (B2-249) fail-closes when the machine-readable claim shape is broken.
    External agents read their law; our law reads back.
25. **Anthropic multi-agent research system** - "How we built our multi-agent research system",
    Anthropic Engineering, June 2025 `[V facts via search, M for exact slug]`: orchestrator-worker
    with 3-5 subagents, ~90% win vs single-agent on research evals, token usage explaining ~80% of
    performance variance, compaction as the core skill.
    VERDICT: **WE-HAVE-IT** - garden lanes + the measured width envelope (proven-width table, 50
    workflow children sustained) are the same pattern with our own metering; their 80%-of-variance
    finding validates our tokens-maxed standing law.
26. **Cognition "Don't Build Multi-Agents"** - Cognition blog, June 2025 `[V for follow-up post
    cognition.com/blog/multi-agents-working, M for the original slug]`: context fragmentation
    compounds errors at every handoff; one full-context agent beats many fragmented ones; actions
    must carry their full context.
    VERDICT: **WE-HAVE-BETTER** - this critique is precisely what our G2 byte-identical contract
    law + sha-stamped asks + sha_drift_since_ask stamps answer: every family sees the same bytes
    and every claim is graded against the file hash it was asked about. We built the antidote
    before reading the diagnosis.
27. **Collective KV-cache sharing across agents** - KVFlow (arXiv:2507.07400, NeurIPS 2025),
    TokenCake (arXiv:2510.18586), TokenDance "Scaling Multi-Agent LLM Serving via Collective KV
    Cache Sharing" (arXiv:2604.03143), PBKV (arXiv:2605.06472) `[E, corpus V]`: serving-layer
    shared memory; agents that share prefixes share cached KV, and prediction of the next agent
    drives eviction/prefetch.
    VERDICT: **WE-HAVE-IT at the prompt layer** - the byte-stable brief law and the G2 byte-identical
    asks exist exactly to make prefix caches hit; the serving-layer machinery is only adoptable if
    the local ollama/k8s flock starts self-hosting the primes (deferred, noted for the GPU ladder).

## THE RIBS QUESTION (does anyone else communicate via shared law artifacts?)

Yes, and the set is small enough to name: the closest is **ACE** (worker/inspector/curator evolving
one shared playbook.md, ICLR 2026), then **MetaGPT** (SOP artifacts + structured shared pool),
**Anthropic Agent Skills** (SKILL.md as distributable instruction-artifact), the **AGENTS.md**
convention (law file every agent loads first), and **Letta** memory blocks (editable shared
memory). The deep lineage is Linda tuple spaces and Hearsay-II blackboards. What NO external work
does, and what the estate holds: law files bound to a hash chain (verkle knots), trust-gated
writes, fail-closed machine enforcement of the law text itself (census tripwire), and an authority
split (model text proposes, switchboard authorizes). The one thing they do that we do not: evolve
the shared law automatically from measured outcomes. That is the steal, and it is ticket T3.

## THE 3 BEST ADOPTIONS (tickets)

**T1. GENETIC LENSING ON code_swarm: GEPA/AlphaEvolve-style contract evolution**
- What: close the loop tools/code_swarm.py already has every organ for. Add a `--evolve` pass:
  after each run's rollup, mutate the CONTRACT (and per-family claritas face tail) via cheap
  reflective rewrites (GEPA-style: keep what graded well, mutate against the misses), retain a
  Pareto front of (REAL clusters per usd, cite-resolution rate, no-shape-violations) in a
  content-addressed contract database (AlphaEvolve's programs-database pattern, estate-sized),
  and stage the next run from the retained winners. Rollout cost is the near-free tier already
  metered ($0.218 per 159-ask run).
- Where: tools/code_swarm.py (new evolve step between fire and rollup), contract bank under
  watch/inbox/model_garden/<run>/contracts/, fitness fields read from rollup.json clusters.
- Acceptance: a lineage where descendant contracts beat the SWARM_1 baseline REAL-per-usd on the
  same target grid; every mutation sha-stamped with parent + fitness (the DGM archive rule).
- Citations: GEPA arXiv:2507.19457 `[V]`; AlphaEvolve (DeepMind, May 2025, fetched primary) `[V]`;
  AFlow arXiv:2410.10762 `[M]`; EvoAgent arXiv:2406.14228 `[V]`.

**T2. DYLAN-STYLE FAMILY IMPORTANCE SCORING (dynamic team formation for the swarm)**
- What: track per-family marginal contribution from rollups (REAL clusters this family was the
  second vote in, per usd, minus terminal waste), and let a kill/demote rule prune families whose
  rolling marginal rate collapses, exactly the manual kimi-EMPTY_REASONING lesson made automatic.
  Same scorer can reweight salon shape->vendor assignment (drop shapes a vendor keeps failing).
- Where: tools/code_swarm.py rollup (add per-family marginal stats), manifest staging (skip
  demoted families, name the remainder), watch/salon_runner.py shape/vendor table.
- Acceptance: the next triple-violator sweep auto-drops the weakest family with a named receipt
  row and no loss of 2-family coverage on any file.
- Citations: DyLAN arXiv:2310.02170 `[M]`; efficiency-eval arXiv:2609.05933 `[V]`.

**T3. RIB FITNESS LOOP (ACE-style curation of the law substrate)**
- What: ribs become evolutionary, not append-only: every rib gets a measured-use stat (times
  mounted by rib_bus, decisions it steered, citations in receipts) and a last-verified stamp; a
  curator pass (cheap lane, gated like improve) compacts or retires zero-use ribs, promotes
  contested ones to salon judgment, and files the delta as a rib amendment with its evidence.
  This is the swarm communicating in ribs AND improving the channel it communicates through.
- Where: mag/rib_bus.py (usage counters on mount), a tools/rib_fitness.py pass next to
  tools/md_record_audit.py, amendments appended per the open-append-single-item law.
- Acceptance: first curator pass lands with per-rib usage numbers and at least one retired rib
  plus one promoted rib, each with evidence; zero silent deletions (retire = register event).
- Citations: ACE arXiv:2510.04618 `[V]`; DGM archive rule arXiv:2505.22954 `[M]`.

## SPLIT SUMMARY

27 mechanisms swept: **12 WE-HAVE-IT, 7 WE-LACK-IT, 8 WE-HAVE-BETTER.** The lacks cluster in one
place: nothing in the estate evolves its own asks, families, or law from measured outcomes - which
is exactly the operator's "genetic lensing and algos" ask, and exactly what T1/T2/T3 close. No
commits made this lane; file writes only.
