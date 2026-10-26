# stealth-sw-10: Formal Verification of AI Agent Behavior

Topic: model checking, theorem proving, and runtime verification applied to LLM agents.
Researched 2026-09-28. Method: WebSearch plus direct fetches of arXiv abstract pages and the arXiv export API during this ask. Every claim is tagged [fetched] (primary abstract or API record read this session) or [search] (surfaced in search results, not opened). Classic-background claims are tagged [background, unfetched]. Nothing is asserted from memory alone.

## 1. Why the classical verification stack broke

Classical verification assumes a finite, known transition system. An LLM agent breaks all three premises: the decision policy is a network with parameter counts in the hundreds of billions whose per-step transition relation nobody can enumerate [background, unfetched], the action space is open-world (any tool call, URL, or shell command), and the environment responds non-deterministically. The field's response has not been to verify the network. It has been to relocate verification outside the network into specs, monitors, automata, and proof assistants wrapped around it.

The clearest theoretical statement of that move is the LLM-Modulo position [fetched, arXiv 2402.01817, first author Subbarao Kambhampati, v1 2024-02-02]: auto-regressive LLMs "cannot, by themselves, do planning or self-verification," so the LLM should be treated as a "universal approximate knowledge source" in a tight bi-directional loop with external model-based verifiers. Proposal inside the LLM, proof outside it: that is the organizing pattern of everything below.

Empirical confirmation that self-checking fails: the TRAIL benchmark [fetched, arXiv 2505.08638, first author Darshan Deshpande, v1 2025-05-13] supplies 148 human-annotated agent traces with a formal error taxonomy across single- and multi-agent systems and finds the best evaluated model, Gemini-2.5-pro, scoring a mere 11% at localizing issues in traces. A verifier cannot simply be another LLM of the same class as the verified.

## 2. Runtime verification and enforcement (the deployable tier)

This is where the most concrete numbers live.

AgentSpec [fetched, arXiv 2503.18666, first author Haoyu Wang, v1 2025-03-24]: a lightweight domain-specific language for specifying and enforcing runtime constraints on LLM agents; a rule pairs a trigger, predicates, and an enforcement mechanism. Abstract numbers: prevents unsafe executions in over 90% of code-agent cases, eliminates all hazardous actions in embodied-agent tasks, 100% compliance in autonomous-vehicle scenarios, millisecond-level overhead; LLM-automated rule generation with o1 reaches 95.56% precision and 70.96% recall on embodied agents and flags 87.26% of risky code. This is runtime enforcement in the classic sense (the monitor intervenes, not just observes [background, unfetched: the monitoring vs enforcement taxonomy of the 2009 runtime-verification literature]).

GuardAgent [fetched, arXiv 2406.09187, first author Zhen Xiang, v1 2024-06-13]: the guardrail is itself an LLM agent that first plans from a safety request, then translates the plan into executable guardrail code, blocking unsafe inputs and outputs deterministically. Reported guardrail accuracy exceeds 98% on its EICU-AC healthcare access-control benchmark and 83% on Mind2Web-SC web-agent safety policies. Note the tension: an LLM writing the monitor reintroduces the trusted-base problem; determinism comes from the compiled code, not from the LLM that wrote it.

VeriGuard [fetched, arXiv 2510.05156, first author Lesly Miculicich, v1 2025-10-03]: the cleanest two-phase shape in the space. Offline: clarify user intent into a precise safety specification, synthesize a behavioral policy, and prove compliance by testing plus formal verification, iterating until correct. Online: a lightweight runtime monitor checks each proposed agent action against the pre-verified policy before execution. This is the standard runtime-verification economics (heavy monitor construction offline, cheap check online) ported to agents, aimed at sensitive domains like healthcare.

Search-surfaced, not opened [search]: MI9, a runtime governance framework for agentic AI (arXiv, Oct 2025); QuadSentinel, sequent-based machine-checkable safety specs reporting guardrail gains on ST-WebAgentBench and AgentHarm; a survey "Toward Safe LLM Agents: Specification, Verification, and Enforcement" that organizes the field into exactly those three tiers; and Maris, a privacy-policy framework claiming provable enforcement via the MonPoly temporal-logic runtime verification tool. Caveat on Maris: my arXiv API query for Maris + MonPoly returned 0 results this session, so that item remains unverified.

## 3. Model checking and conformance checking

Formal-LLM [fetched, arXiv 2402.00798, first author Zelong Li, v1 2024-02-01] is the earliest widely cited move in this direction: the developer writes the space of valid plans as an automaton, and plan generation runs under the automaton's supervision via a stack-based process so invalid plans cannot be emitted, with over 50% overall performance increase on benchmark and real tasks. This is model checking by construction: the accepted-language constraint replaces post-hoc checking.

AgentRFC [fetched via arXiv API, arXiv 2603.23801, published 2026-03-25]: a 6-layer Agent Protocol Stack, eleven security principles formalized in TLA+ (Lamport's temporal logic of actions), and an AgentConform conformance checker that finds security gaps in real agent protocols including MCP and A2A, including composition-related weaknesses. This is protocol-level model checking: the formal object is the inter-agent protocol, not the LLM.

Agentic Model Checking [fetched via arXiv API, arXiv 2605.21434, first author Youcheng Sun, submitted 2026-05-20]: couples LLM agents with bounded model checking under the slogan "agents propose, solvers verify," evaluated on LLM-generated C and Rust kernel and compiler code. Verification OF agent output, with a solver as oracle.

Event-B Agent [fetched via arXiv API, arXiv 2605.17475, first author Hongshu Wang, accepted FSE 2026]: the reverse direction, an LLM agent that synthesizes Event-B formal models from natural-language requirements and repairs them iteratively using model-checking feedback. Same split: agent as search, checker as oracle.

## 4. Theorem proving (two directions, one mature, one nascent)

Mature direction, agents as provers [search, individual papers not opened]: Prover Agent integrates LLM natural-language reasoning with Lean-checked output; CoqPilot generates Coq proofs with LLMs; NLIR uses a natural-language intermediate representation where the agent describes goals in prose then compiles them to machine-checkable Coq steps; EPFL demonstrated agentic proof automation with off-the-shelf LLMs inside proof assistants. The pattern is again LLM proposes, assistant disposes.

Nascent direction, provers as agent verifiers: I found no fetched primary source this session that runs Lean, Coq, or Isabelle against a full LLM agent trajectory to prove behavioral properties. The closest verified anchors are VeriGuard's offline policy verification (prover unspecified in the abstract) and AgentRFC's TLA+ conformance route. Honest verdict: machine-checked proofs of agent behavior properties remain an open slot; what actually exists today is DSL-level enforcement and automaton-level supervision.

## 5. Synthesis: what actually holds

1. Convergent architecture. All eight fetched papers share one skeleton: a nondeterministic proposal component, a deterministic checking component, and feedback or enforcement between them. The disagreement is only about where the checker lives (DSL, automaton, compiled monitor, protocol spec, solver).
2. Verification relocated to the wrapper. Nobody verifies the weights; formal verification of an LLM at scale is beyond current constraint-solving capability [background, unfetched]. Every deployed guarantee in this space lives in a DSL, automaton, monitor, or protocol specification.
3. Spec acquisition is the new bottleneck. Formal-LLM needs a developer-written automaton; VeriGuard needs intent clarified into a spec; AgentSpec mitigates with LLM-generated rules but at 95.56% precision and 70.96% recall, far from complete; GuardAgent's LLM-written monitors inherit the trusted-base problem. Who writes the specification is now a bigger open problem than how to check it.
4. Benchmarks are young. TRAIL's 11% best score on trace-issue localization says even debugging-grade analysis of agent traces is unsolved. Claims of "verified agents" today should be read as verified wrappers with unverified interiors.
5. In-house echo. This repo already runs the same skeleton on itself: the workflow gate, violation ratchet, and config seal are LLM-proposes-verifier-disposes applied to seat behavior; AgentSpec's trigger/predicate/enforcement rule shape maps onto gate checks, and the accept-debt-by-name law is spec acquisition by explicit registration (comparison drawn by me from AGENTS.md in this repo, not from any fetched paper).

## Sources

Fetched this session (arXiv abstract pages unless noted):
- arXiv 2402.01817 LLMs Can't Plan, But Can Help Planning in LLM-Modulo Frameworks
- arXiv 2505.08638 TRAIL: Trace Reasoning and Agentic Issue Localization
- arXiv 2503.18666 AgentSpec: Customizable Runtime Enforcement for Safe and Reliable LLM Agents
- arXiv 2406.09187 GuardAgent: Safeguard LLM Agents by a Guard Agent via Knowledge-Enabled Reasoning
- arXiv 2510.05156 VeriGuard: Enhancing LLM Agent Safety via Verified Code Generation
- arXiv 2402.00798 Formal-LLM: Integrating Formal Language and Natural Language for Controllable LLM-based Agents
- arXiv API records: 2603.23801 AgentRFC, 2605.21434 Agentic Model Checking, 2605.17475 Event-B Agent
Search-only (not opened): MI9, QuadSentinel, Safe-LLM-Agents survey, Maris/MonPoly (arXiv API 0 results, unverified), Prover Agent, CoqPilot, NLIR, EPFL agentic proof automation.

## Session checks

Ran during this ask: 5 WebSearch queries; 5 arXiv abstract fetches; 3 arXiv export API queries (one returned 0 results, reported above). Em/en dash scan and char count on this file via repo venv python, result recorded in the submit note.
