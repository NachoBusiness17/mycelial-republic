# THE_LENSING: frontier judgment on the route (MC6 paid ask)

Status: ok. Metered cost: $0.1195. Seconds: 67.9. Usage: {"prompt_tokens": 1093, "completion_tokens": 5754, "total_tokens": 6847, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 2344, "image_tokens": 0, "audio_tokens": 0}, "cost": 0.119452, "cost_details": {"source": "openrouter_list", "floor_applied": false, "rate_source": "openrouter_catalog"}}. Finish: content_filter.
Prompt sha256: e6ae0e665fbcc0d5608bae40f59c1709c547ddaf222a75036769e1a758740aa9 (2784B).
Full return below, verbatim. Em-dash count in return body: 0.

---

# Bibliography: Frontier Judgment over a Cheap-Token Mesh

**How to read the tags.** [public] means I can vouch the source exists and roughly what it says. [inference-from-coverage] means I know the source only through the discourse summary you supplied, so I cannot confirm its contents, and I will not invent titles or URLs for it. [report] marks a claim relayed from your evidence block. [inference] marks my own reasoning.

The two items your week turned on, the Anthropic Frontier Red Team (FRT) report and the CAISI GLM-5.3 evaluation, are both in the second category. That is the first finding of this bibliography: the load-bearing sources are the ones you have read least directly. Read them before anything else on this list.

---

## A. The dispute itself (read first, in full)

**1. Anthropic Frontier Red Team, GLM-5.3 cyber report (2026-09-29/30).** [inference-from-coverage]

- **What it teaches:** a gated-access lab's end-to-end exploit-development methodology. It reports ExploitBench 50/410 for GLM-5.3 against 56/410 for Mythos Preview, and says simple bypasses succeeded 64-100% of the time [report].
- **Why it's load-bearing:** your daily driver is the subject. If the capability claims hold, your free-lane fleet runs a model with a real offensive ceiling and weak refusals. That changes what your harness profiles must constrain, not just what they can exploit.
- **What to extract:**
  - the elicitation budget (scaffold, attempts, time);
  - whether "end to end" means autonomous or human-in-loop;
  - how "bypass" is defined.
- **Disconfirmer:** item 2.

**2. NIST CAISI cyber evaluation of GLM-5.3 (2026-09-17).** [inference-from-coverage]

- **What it teaches:** a government evaluator's read that GLM-5.3 is generally behind US models at bug-finding, with one narrow win [report].
- **Methodological precedent:** CAISI's *Evaluation of DeepSeek AI Models* (2025) [public] used a comparative benchmark suite plus cost and adoption framing. Expect similar structure.
- **Why it's load-bearing:** it directly contradicts item 1. You cannot resolve the contradiction from the headlines [inference]. The likely explanations are:
  - **Task mismatch:** bug-finding versus exploit development.
  - **Elicitation mismatch:** default scaffold versus red-team scaffold.
  - **Version or date mismatch.**
- **Instrument to close the gap:** a side-by-side table of task type, scaffold, pass@k, and model snapshot for both reports. If either report doesn't publish these, weight it down.

**3. Terminal-Bench (Laude Institute / Stanford; tbench.ai, 2025).** [public]

- **What it teaches:** a harness for agents doing real terminal tasks, with a public leaderboard where the scaffold is part of the entry.
- **Why it's load-bearing:** the 84.5% Terminal-Bench figure [report] is being cited as evidence of an "unplanned jump." Terminal-Bench scores are harness-sensitive [inference, consistent with the leaderboard listing agent-plus-model pairs].
- **Disconfirmer to check:** if the 84.5% was posted with Zhipu's own agent scaffold, it measures scaffold plus model, not a base-model capability jump. Verify which harness produced it before accepting the "same base as 5.2, unplanned jump" narrative.

**4. ExploitBench, with Cybench (Zhang et al., 2024) as the public anchor.** ExploitBench is [inference-from-coverage]; Cybench is [public].

- **What it teaches:** Cybench shows how professional-CTF tasks get decomposed into subtasks, and how unguided solve rates differ from subtask-guided ones.
- **Why it's load-bearing:** I cannot confirm ExploitBench's construction. Cybench teaches the right questions to ask of it:
  - Are subtask hints given?
  - Is first-blood time used as a difficulty proxy?
  - Is there contamination risk from public writeups?
- A 50-vs-56 out of 410 gap is roughly 1.5 percentage points. Without confidence intervals and pass@k, that gap may not be distinguishable from noise [inference].

**5. Zhu et al., "Establishing Best Practices for Building Rigorous Agentic Benchmarks" (2025, the ABC checklist).** [public]

- **What it teaches:** that popular agentic benchmarks have task-validity and outcome-validity flaws, including graders that accept wrong answers and tasks solvable by shortcuts. These can shift scores substantially.
- **Why it's load-bearing:** this is your adjudication tool for items 1-4. Run each report through the checklist before letting either one propagate into doctrine files.
- **Why this matters especially for you:** one $0.42 verdict fanned out to about 40 lanes [report]. Your architecture amplifies whatever epistemic quality the source had.

## B. The open-weights policy frame

**6. Kapoor, Bommasani et al., "On the Societal Impact of Open Foundation Models" (2024).** [public]

- **What it teaches:** the *marginal risk* framework. It asks what open weights add over existing tools, such as other models or existing exploit kits, rather than asking whether a model can do harm at all.
- **Why it's load-bearing:** this is the rigorous version of Lilith Datura's "matters at the margin."
  - It lets you separate the Roon/Adi political critique from the capability question.
  - It forces the right comparison: GLM-5.3 against a skilled human with Metasploit, not against zero.
- **Disconfirmer:** marginal-risk analyses from 2024 assumed open models lagged the frontier substantially. If item 1 is correct about near-parity, the framework's reassuring conclusions weaken, even though its structure survives.

**7. NTIA, "Dual-Use Foundation Models with Widely Available Model Weights" (July 2024).** [public]

- **What it teaches:** the US government's prior position, which recommended monitoring rather than restricting open weights, with explicit triggers for revisiting.
- **Why it's load-bearing:** the Anthropic and CAISI reports are effectively arguments about whether those triggers have fired. Read the trigger conditions, then check which report's evidence meets them.
- **For your mesh specifically [inference]:** a policy shift here is a supply-chain risk to your daily driver, separate from any capability question.

## C. Your propagation substrate

**8. Model Context Protocol specification (modelcontextprotocol.io; Anthropic, Nov 2024 onward, with revisions).** [public]

- **What it teaches:** the primitives:
  - tools, resources, and prompts;
  - client/server roles;
  - the authorization model (OAuth in later revisions);
  - sampling, where a server requests completions through the client.
- **Why it's load-bearing:** "frontier reasoning via MCP servers" means your frontier verdicts enter lanes as tool outputs or resources. The spec defines what provenance and trust metadata you *can* attach. My read is that the answer is "not much natively" [inference], so fingerprint binding is your own layer, not the protocol's.

**9. MCP security literature.** [public]

- **Sources:**
  - Invariant Labs, the tool-poisoning disclosure (2025);
  - Simon Willison's "lethal trifecta": private data plus untrusted content plus an exfiltration channel (2025);
  - Radosevich & Halloran, "MCP Safety Audit" (2025).
- **What it teaches:** tool descriptions and outputs are an instruction-injection surface, and cross-server shadowing is possible.
- **Why it's load-bearing:** your 24/7 sensing fleet ingests untrusted content, and your mesh propagates text into about 40 executing lanes. Your mesh therefore meets at least two legs of the trifecta by design [inference].
- **Combined with item 1:** the reported 64-100% bypass rates suggest the open model in those lanes may be the component least able to refuse injected instructions [inference, only if the report generalizes to injection, which it may not].
- **Instrument:** a canary injection in a sensing-fleet input, traced through propagation.

**10. Anthropic, "Building Effective Agents" (Dec 2024) and "How we built our multi-agent research system" (2025).** [public]

- **What it teaches:**
  - workflows versus agents;
  - orchestrator-worker patterns;
  - that multi-agent systems burn many times the tokens of single chats, and pay off mainly on parallelizable breadth tasks.
- **Why it's load-bearing:** your architecture inverts their cost assumption. Tokens are nearly free on the daily driver, and judgment is the scarce input. Read these texts for their failure modes (coordination overhead, compounding errors), not their economics.

**11. Cemri et al., "Why Do Multi-Agent LLM Systems Fail?" (2025, the MAST taxonomy).** [public]

- **What it teaches:** an empirically derived taxonomy of multi-agent failures:
  - specification failures;
  - inter-agent misalignment;
  - verification and termination failures.
- **Why it's load-bearing:** your doctrine-file propagation is a specification channel. MAST predicts that errors enter at specification and survive verification. Use it to audit whether the $0.42 verdict was correctly *translated* at each hop, not just correct at the source.

## D. Routing and cascades (the economic spine)

**12. Chen, Zaharia, Zou, "FrugalGPT" (2023).** [public]

- **What it teaches:** LLM cascades. Try cheap models first, use a learned scorer to decide when to escalate, and match expensive-model quality at a fraction of the cost.
- **Why it's load-bearing:** this is the formal ancestor of your cash-rail design.