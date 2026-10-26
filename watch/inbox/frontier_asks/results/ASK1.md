# THE_LENSING: frontier judgment on the route (MC6 paid ask)

Status: ok. Metered cost: $0.1769. Seconds: 93.2. Usage: {"prompt_tokens": 1122, "completion_tokens": 8623, "total_tokens": 9745, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 3228, "image_tokens": 0, "audio_tokens": 0}, "cost": 0.176948, "cost_details": {"source": "openrouter_list", "floor_applied": false, "rate_source": "openrouter_catalog"}}. Finish: stop.
Prompt sha256: 805c0bff6f3442e7411d122e29909135e79224d377b2a9e727d46cc01299cb2b (2895B).
Full return below, verbatim. Em-dash count in return body: 0.

---

# Architecture Taxonomy: Cheap Driver + Rented Frontier Judgment Propagated Through a Mesh

**Scope caveat.** My public knowledge is fixed at my training cutoff. It predates GLM-5.3, the Anthropic Frontier Red Team (FRT) report and the CAISI benchmark. Anything tagged [public] is known to me from before that point. Treat it as a floor: newer tooling may exist that I cannot see. [report] means the evidence block you supplied. I have not seen those documents directly. "OpenClaude" is not a project I can verify. I treat it as the class of open forks and routers that point Claude-Code-style harnesses at other models, such as `claude-code-router`.

---

## Part 1: The Taxonomy

I sort patterns by **where escalation is decided**, **what carries the frontier output forward**, and **how long that output lives**.

### P1. Intra-turn architect/editor split
- **Who:** Aider's architect mode [public]. A reasoning model (o1/R1/Claude) plans, and a cheaper editor model applies diffs. Cline and Roo Plan/Act modes with per-mode model assignment are the same idea [public]. Claude Code's "opusplan"-style configs plan with Opus and execute with Sonnet [public].
- **Propagation:** The plan text is handed to the executor within a single request.
- **Rented:** Decomposition and design. **Owned:** Syntax-level execution.
- **Lifetime:** One turn.
- **Failure modes:**
  - The editor silently "fixes" the plan.
  - Nothing persists, so the same judgment is re-bought every session.
  - Cost scales with task count, not with novelty.

### P2. Oracle-as-tool (consult on demand)
- **Who:**
  - Sourcegraph Amp's "Oracle" subagent: the main agent calls a stronger reasoning model for hard debugging or review [public].
  - `zen-mcp-server`: Claude Code calls Gemini or o3 via MCP for "second opinion", "consensus" and "codereview" [public].
- **Propagation:** MCP or tool-call return value, injected into the driver's context.
- **Rented:** Hard-case diagnosis and review. **Owned:** Everything else, including the decision of *when* to consult.
- **Lifetime:** Context window.
- **Failure modes:**
  - The driver's self-assessment gates escalation, so a confidently-wrong driver never calls.
  - Oracle output is summarized lossily by the driver.
  - No durable artifact results.
- **Relevance:** This is the closest public analogue to "frontier reasoning via MCP servers."

### P3. Learned or confidence-gated routing and cascades
- **Who:** RouteLLM (LMSYS 2024), FrugalGPT cascades (Stanford 2023), and commercial routers such as Martian and Not Diamond [public]. LiteLLM and OpenRouter provide rule-based fallback [public].
- **Propagation:** None. Each query is routed independently.
- **Rented:** Answers to queries a classifier deems hard. **Owned:** Answers to easy queries.
- **Failure modes:**
  - Router miscalibration under distribution shift.
  - The router is trained on benchmark-shaped queries, not your workload.
  - No compounding: the frontier answer teaches the cheap model nothing.

### P4. Local-remote collaboration protocols
- **Who:** Stanford Hazy Research "Minions/MinionS" (early 2025) [public]. A remote frontier model decomposes the task and aggregates. A small on-device model reads the long private context in chunks. The reported result is roughly 5-6x remote-cost reduction while retaining most of the frontier-only quality [public; exact figures from memory, verify].
- **Propagation:** A structured protocol of subtask specs down and extracted evidence up.
- **Rented:** Decomposition and synthesis. **Owned:** Reading of private data.
- **Failure modes:**
  - The local model misses evidence, and the frontier cannot see what it was not shown.
  - Protocol overhead on short tasks.
- **Why it matters:** This is the only academically measured version of your ratio, and it treats the privacy boundary as a first-class design constraint.

### P5. Orchestrator-worker with frontier on top
- **Who:** Anthropic's multi-agent research system writeup (2025): an Opus lead with Sonnet subagents [public]. It follows Anthropic's "Building Effective Agents" patterns of routing, orchestrator-workers and evaluator-optimizer [public]. OpenAI cookbook examples use an o-series planner orchestrating a mini-model executor [public].
- **Propagation:** Task specs from lead to workers, results back up.
- **Rented:** Continuous supervision. **Owned:** Nothing structurally: workers are also rented, just cheaper.
- **Failure modes:**
  - Token cost multiplies; Anthropic itself reported multi-agent runs using many times the tokens of chat [public].
  - Spec ambiguity propagates to all workers.
- **Direction:** This is the *inverse* of yours. The frontier is the always-on driver.

### P6. Doctrine/memory files as propagation
- **Who:** CLAUDE.md, AGENTS.md (the Codex-originated cross-tool convention), .cursorrules/Cursor Rules, Cline "Memory Bank", and Windsurf memories [public]. Letta/MemGPT does this at runtime with self-edited memory blocks [public].
- **Propagation:** Prose files loaded into every session's context.
- **Rented:** Whatever judgment produced the file, often a frontier session, often the human. **Owned:** Interpretation at run time by whichever model loads it.
- **Lifetime:** Until someone edits the file.
- **Failure modes:**
  - Staleness.
  - Contradiction accumulation.
  - Model-dependent interpretation: the same sentence reads differently to different families.
  - No test that a rule is being followed.
  - Prompt injection into memory if agents can write to it.

### P7. Compiled or distilled propagation
- **Who:**
  - DSPy optimizers using a strong "teacher" model to write prompts or demos for a cheap student [public].
  - OpenAI's stored-completions-to-fine-tune distillation product [public].
  - The general practice of distilling frontier traces into open-weight fine-tunes [public].
- **Propagation:** Optimized prompts or weights, gated by an eval set.
- **Rented:** Labeled judgment at build time. **Owned:** Execution at inference time.
- **Failure modes:**
  - Eval overfit.
  - Terms-of-service constraints on training from frontier outputs.
  - Distilled behavior is brittle outside the eval distribution.
- **Distinction:** Of all the patterns, this one converts rented judgment into owned capability with a *measured* retention check.

### P8. Cross-family jury/judge
- **Who:** Cohere's "Replacing Judges with Juries" (PoLL, 2024): a panel of smaller, diverse-family models outperformed a single large judge on agreement with humans and reduced self-preference bias [public]. zen-mcp "consensus" does the same thing ad hoc [public].
- **Propagation:** A verdict gates an output.
- **Rented:** Evaluation. **Owned:** Generation.
- **Failure modes:**
  - Correlated errors across families trained on overlapping data.
  - Judges reward style.

### P9. Harness-level model routing in agent CLIs
- **Who:** `claude-code-router`, which routes background, think and long-context subtasks to different providers [public]. OpenHands, Goose, Continue and Cline all support BYO-model with per-role assignment [public]. Ollama and llama.cpp serve as the local backend [public].
- **Propagation:** Harness config.
- **Rented/Owned:** Set statically per role.
- **Failure modes:**
  - Harness prompts tuned for one family degrade on another.
  - Silent provider or model substitution.
  - Tool-call format mismatches.

---

## Part 2: Where the Operator Sits

### What is standard

**Doctrine files as the propagation medium (P6).** This is mainstream. Your verdict flowing into doctrine is structurally CLAUDE.md/AGENTS.md practice.

**Cheap driver plus on-demand frontier consult via MCP-style calls (P2).** Amp and zen-mcp shipped this [public]. Your framing, "frontier reasoning via mcp servers," describes an existing pattern, not a new one [inference].

**Second-family judge rules (P8).** PoLL-style cross-family judging is published and increasingly common [public].

**Rate envelopes.** Measuring your own limits instead of trusting published ones is ordinary SRE practice [inference]. Not publishing them is also normal.

### What is unusual

**1. The spend ratio and the escalation unit.** Roughly 1B driver tokens against $1.48 of frontier spend in a day [report] is more extreme than any published pattern I know.
- P4 Minions reports single-digit-multiple savings.
- P2 oracles fire per hard task.
- Your escalation unit is the *engineering route*, not the task: one $0.42 verdict reshaped a week [report].
- That is closer to buying a consultant's memo than to routing queries [inference].

**2. Durable fan-out from a single verdict.** Most patterns keep frontier output inside one context (P1-P5). You push one verdict through doctrine, a per-model layer and MCP into ~40 executed lanes [report]. That gives high leverage and equally high blast radius.
- I see no public pattern that fans a single rented judgment across that many heterogeneous agents without a per-lane check [inference].
- **Disconfirming evidence I lack:** whether the 40 lanes were actually better off. "Propagated into 40 lanes" measures reach, not correctness.

**3. The per-model behavioral layer.** Model-specific prompt variants exist in harnesses such as Cline and the router transformers [public]. Treating per-family interpretation of doctrine as an explicit governed layer is less common [inference].
- It directly targets P6's worst failure mode: the same doctrine read differently by different models.

**4. Fingerprint binding on harness profiles.** Verifying which model is actually answering is rare in public dev tooling [inference]. It addresses P9's silent-substitution failure.
- It matters more now. [report] says GLM-5.3 shipped an unplanned capability jump on the same base as 5.2.
- That means version identity is behaviorally load-bearing. A silent 5.2↔5.3 swap would change both capability and guardrail behavior.

**5. Positive-reinforcement steering law.** This is your least-supported claim as a general principle.
- The measurement is "in-game" [report]. Transfer from a game-school dynamic to LLM agent steering is an [inference] you have not shown me evidence for.
- Anthropic's prompting guidance to say what to do rather than what not to do is weakly consistent with it [public]. That is guidance, not a controlled result.
- **Instrument to close the gap:** matched A/B on your own lanes. Use the same task, reward-framed versus constraint-framed doctrine, and measure the compliance rate scored by a second-family judge.

### How the discourse bears on your placement

The CAISI-versus-FRT contradiction [report] is precisely why keeping *judgment* off GLM is defensible, independent of which benchmark is right. Your architecture treats the driver as capable-but-unverified [inference].

The FRT finding that "simple bypasses worked 64-100% of the time" [report] matters to you for a less-discussed reason: **injection susceptibility**.
- Your 24/7 sensing fleet ingests external content.
- If sensing output can reach doctrine files, an injected instruction could propagate through the same channel your $0.42 verdicts use [inference].
- The fan-out that makes good verdicts cheap makes bad inputs cheap too.
- **Instrument:** a canary-injection test. Plant benign marked instructions in sensed content and trace whether any reach doctrine or lane behavior.

There is also an unflattering observation Lilith's framing implies. Your architecture is structurally what the FRT report worries about: a cheap unlogged driver doing the volume, with the gated lab seeing only distilled asks [inference].
- For benign work, that is simply efficient.
- It also means the frontier vendor's monitoring sees $1.48 of questions and none of the 1B tokens of execution.
- Roon/Adi's "politics" reading and the security reading are both describing this same topology [inference].

### What appears absent elsewhere

Based on what I know publicly, the absent combination is this: human-curated, route-level escalation, plus durable multi-lane fan-out, plus per-family interpretation governance, plus identity verification [inference]. Each piece has precedent; the assembly does not have a published instance that I know of.

**Disconfirmation:** private enterprise meshes rarely publish their architecture, so "absent elsewhere" may only mean "unpublished elsewhere." I cannot close that gap. A practitioner survey or conference-talk sweep would.

---

## Part 3: The Three Patterns Others Run That He Does NOT

These are inferred from the receipts you listed. Absence of description is not proof of absence. If you run these, the critique shifts to "unreported."

### 1. Automatic, signal-gated escalation (P3/P4 style)
RouteLLM, FrugalGPT and Minions escalate based on measured uncertainty or learned difficulty [public]. Your escalation is operator-curated "concentrated judgment asks" [report]. That is excellent for known hard questions and structurally blind to unknown-unknowns: the driver's quiet errors that no one thinks to ask about.

**Instrument:** a blind escalation-miss audit.
1. Sample N routine driver decisions at random each week.
2. Send them post hoc to the frontier or a second family.
3. Measure the disagreement rate.

A low rate validates your gating. A high rate prices what the $1.48 is missing. It is cheap to run at your spend levels.

### 2. Compiled, eval-gated propagation (P7)
DSPy teacher-optimization and distillation pipelines turn rented judgment into prompts or weights, and check retention against a test set [public]. Your propagation is prose doctrine interpreted by heterogeneous models [report]. The per-model layer mitigates this, but nothing described *verifies* that lane behavior matches the verdict.

**Instrument:** per-verdict conformance evals.
1. Each frontier verdict ships with 5-10 test cases encoding its intent.
2. Each lane is scored against them by a second-family judge.
3. Rerun on every doctrine edit and every model version change.

This turns "propagated into 40 lanes" into "conforms in X of 40 lanes."

### 3. Closed-loop frontier review of downstream execution (P5 evaluator-optimizer / P2 oracle-on-diff)
Anthropic's orchestrator pattern and Amp-style oracle review put the stronger model back in the loop on *outputs*, not just on the initial question [public]. Your loop appears open: verdict out, execution by cheaper models, no described frontier audit of how the verdict was realized.

At $0.42 per verdict, a second call that spot-checks 2-3 of the 40 lane outputs against the original verdict is affordable. It is also the obvious guard against the blast-radius failure, where one wrong or misread verdict executes 40 times.

It also gives you a verdict-level correctness record. Doctrine files currently lack an expiry or reversal mechanism. With that record, "one verdict reshaped the week" becomes something you can grade after the fact, rather than a leverage story that only reports wins.