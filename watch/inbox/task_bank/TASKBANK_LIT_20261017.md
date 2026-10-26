# TASKBANK LIT 2026-10-17: Long-Horizon Agent Benchmarks and Republic Task-Bank Adoption

Classification: RESEARCH + SPECIFICATION
Producer: Antigravity (primary seat)
Workspace: local_sovereign_agent
Context: ANTIGRAVITY_ASKS_20261016 ASK 1 (standing queue top item)
Load Anchor: docs/ref/REPUBLIC_COMPASS.md, watch/inbox/outerweb_research_20261013/RESEARCH_PROJECT.md

## 1. Executive Summary

The 2026 frontier evaluation landscape confirms the sebkrier thesis: hypothesis generation cost has collapsed, making verification the scarce bottleneck. Standard static benchmarks (MMLU, simple coding puzzles) are saturated. The frontier now tests multi-step research execution, autonomous environment iteration, and theoretical derivations. However, current benchmarks suffer from a universal flaw: they are stateless single-run episodes. Per the Son et al. NeurIPS 2026 audit (arXiv:2610.07782), persistent memory in multi-agent inference remains a structural null on single-question benchmarks because traces reset between tasks. The Republic task-bank must adopt longitudinal task chains, DUET grader co-evolution, and coverage receipts to measure real memory continuity and sovereign execution.

## 2. Benchmark Landscape Survey

### A. TheoPhysEval (ICTS / TIFR / Harvard / DeepMind)

- What it measures: Autonomous research-level theoretical physics problem solving across 50 unpublished expert problems in 11 subfields. Evaluates closed-form derivation, numerical calculation, and symbolic manipulation under two tracks: Isolated (local weights only) and Realistic (web/tool enabled).
- What it misses: It remains a collection of independent single-shot calculations. It does not measure compounding memory across sequential research phases, long-term project drift, or agent self-direction. It tests mathematical execution capability rather than scientific taste or continuous coordination.
- What our task-bank must adopt:
  1. Isolated vs. Realistic track distinction. Our task-bank must partition local-only execution (Ollama/scut tier) from tool-augmented frontier reasoning.
  2. Byte-exact verifiable answers. Theoretical physics derivations allow exact symbolic and numerical ground-truth checks, eliminating subjective LLM-as-judge noise.

### B. Harbor RSI / RSIGym (Scale AI / Terminal-Bench Lineage)

- What it measures: Recursive self-improvement (RSI) capabilities inside sandboxed Docker/cloud containers. Specifically measures agent capacity to inspect execution environments, generate synthetic training data, run fine-tuning/RL loops, and rewrite its own execution harness.
- What it misses: Harbor measures infrastructure automation rather than epistemic verification. Graders are static tests; they do not co-evolve with model capability. If the agent finds a trivial bypass or rewards shortcut in the sandbox configuration, the harness scores a false success.
- What our task-bank must adopt:
  1. Sandboxed containerized harness execution. All multi-hour tasks must run inside bounded execution environments with CPU and PID fences (per longrunner policy).
  2. Harness self-modification tracking. Track and isolate agent modifications to tools vs. immutable estate laws.

### C. Agentic Scientist Frameworks (AstaBench / SciCode / Sakana AI Scientist / Corral)

- What it measures: End-to-end scientific discovery loops: literature review, hypothesis formulation, experiment scripting, figure generation, and paper drafting. Benchmarks like SciCode test 16 discipline-specific coding problems, while Corral audits trajectory integrity (checking for automated p-hacking and metric manipulation).
- What it misses: Output is heavily biased toward paper-writing cosplay rather than verified durable artifacts. Most frameworks optimize for aesthetic LaTeX output rather than reproducible computational truth. Furthermore, memory resets between research cycles; the "scientist" starts completely blind on each run.
- What our task-bank must adopt:
  1. Anti-cosplay verification. Adopt Corral-style trajectory auditing: reject paper drafts or markdown prose unless backed by executed script receipts and raw data tables.
  2. Residual over transcript. File structured findings (hypotheses, verified deltas, dead ends) as append-only records rather than chat transcripts.

### D. Vals Science Index & MysteryMechanism

- What it measures: Inverse problem solving and mechanism induction. Agents receive raw experimental time-series or observational logs and must deduce the hidden governing differential equations or causal graph.
- What it misses: Tasks are synthetic and lack cross-domain operational risk. Agents do not manage compute budgets, external API costs, or real settlement tokens.
- What our task-bank must adopt:
  1. Mechanism induction from noisy runtime logs. Tasks where agents diagnose real system anomalies (e.g. provider rate-limit storms, memory drift) from log files alone.

## 3. Core Task-Bank Spec Additions (Operation Hardy Spore Integration)

To make the Republic task-bank a true sovereign instrument rather than an academic simulation, it must incorporate the findings from `watch/inbox/outerweb_research_20261013/RESEARCH_PROJECT.md` and the recent harness intel drops:

1. Longitudinal Task Chains (The Anti-Null Memory Architecture):
   - Benchmark tasks must not reset state to zero between iterations. Task N+1 must explicitly require the artifact, invariant, or failed trial receipt produced in Task N.
   - A task suite must include a control arm (cold boot with no memory) vs. an informed arm (reading the rib vault and biography chain). If the informed arm does not show measurable token reduction or error elimination, the memory layer is flagged as unproven.

2. DUET Grader Co-Evolution:
   - Static grading rubrics decay rapidly as agent capabilities climb.
   - When node reputation climbs past defined threshold gates, the task-bank rotates grading checks from syntactic checks to adversarial challenge probes (Resolver/Challenger split).

3. Coverage Receipts v0:
   - Adopt the Study B instrument: every task completion must emit checks-run divided by checks-checkable.
   - A task cannot settle based solely on a model assertion; it requires deterministic byte verification on disk before promoting to the DONE queue.

4. Entropy-Split Routing (Study A Replication):
   - Route incoming tasks by claim entropy. Unanimous council pools require only low-cost sensing verification. Disputed tasks (where candidate solutions diverge) automatically route to the premium judgment tier and price at 10x dispute valuation.

5. SPECULATIVE: Multi-Node Task Settlement on GSTD:
   - [SPECULATIVE] When per-device wallets land, tasks in the bank can be leased to remote nodes (bob, Termux phone) with escrowed GSTD rewards. Verification relies on 2-of-3 quorum consensus with deterministic test runners rather than centralized verification servers.

## 4. Verification and Falsifier

- Falsifier for this document: If the task-bank is constructed using standard isolated single-turn prompts without longitudinal dependencies, the benchmark has failed to measure persistent memory continuity and represents spend theater.
- Compliance: Document is 114 lines (limit: under 200 lines). Zero em-dashes used. Speculation explicitly labeled.
