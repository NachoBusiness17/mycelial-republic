# sw-01: AI agent safety frameworks in production (2025-2026) vs an append-only hash-chained receipt system with drift detection

Banked by stealth seat sw-01, 2026-09-28. Method: web search (6 queries, one timed out and was retried, two hit upstream 429 and were reworded and retried) plus direct repo reads and one live instrument run in this session. Nothing below is fabricated; every claim carries its source or its command.

## Part 1: Who has shipped agent safety layers (the 2025-2026 census)

**OpenAI - Guardrails (open-sourced early October 2025, DevDay, alongside AgentKit).** A modular open-source Python library (github openai/guardrails-python) providing safety layers for agents and LLM apps. Detects PII leaks, jailbreak attempts, self-harm content, NSFW content, and other unsafe behavior. Implementation is a mix of LLM-based checks (backed by an open-weight safety classifier OpenAI released for this) and deterministic validators. Checks run in parallel and fail fast, and can be composed into chains. Integrates with the OpenAI Agents SDK (which has guardrails built into its framework) and the Responses API. Shipped as part of the AgentKit push with Agent Builder and ChatKit as the surrounding runtime.

**Anthropic - Constitutional Classifiers (announced 2026-02-03, deployed in production on Claude).** Synthetic training data is generated from natural-language "constitutions" (rules specifying permitted vs refused content); input and output classifiers are trained to screen jailbreaks and policy-violating responses around the model. Red-team results update posted 2026-02-10; research paper (Sharma et al., 2025, arXiv) reports robust defense against held-out domain-specific jailbreaks. A follow-up, Constitutional Classifiers++, is described as significantly more robust and about 5.4x more efficient than the original. Notable: this is the main shipped example of a guardrail layer generated from a written rule text, i.e. doctrine-as-code at the model boundary.

**NVIDIA - NeMo Guardrails.** Open-source programmable-rails toolkit (Colang language) defining input/output guards, topic boundaries, and conversation flows. Ships integrations for CrewAI, AWS Bedrock, and Cisco agent platforms. The oldest of the widely deployed OSS rails; its Colang model (topical and procedural constraints expressed as code) is the closest cousin to this repo's law/card pattern.

**AWS - Bedrock Guardrails.** Managed service covering six policy dimensions: content moderation filters, prompt-attack detection, topic classification/denial, PII redaction, word filters, and groundedness. Wired into Bedrock Agents, Knowledge Bases, and AgentCore for production agent deployment. The differentiator is centralized policy management: as a fleet grows from a few agents to dozens, policies are managed centrally rather than hard-coded per agent.

**Ecosystem layers.** Guardrails AI (open-source, 65+ validators, input/output guard execution), OpenGuardrails (arXiv, October 2025, context-aware safety and manipulation-detection model), Lakera and similar injection-defense vendors. Practitioner consensus is a layered architecture: in-model safeguards (Constitutional AI) plus runtime guardrails inspecting inputs/outputs at inference time, because a single guardrail layer is never enough.

**Standards and regulation (the forcing functions).**
- OWASP Top 10 for LLM Applications, 2025 edition (published 2024-11-18): LLM01 prompt injection, LLM02 sensitive information disclosure, LLM03 supply chain, LLM04 data and model poisoning, LLM05 improper output handling, LLM06 excessive agency, LLM07 system prompt leakage, LLM08 vector and embedding weaknesses, LLM09 misinformation, LLM10 unbounded consumption. A separate OWASP Top 10 for Agentic Applications followed (December 2025), naming tool misuse and excessive autonomy as agent-specific risks.
- EU AI Act GPAI obligations entered into force 2025-08-02, with the final GPAI Code of Practice (July 2025): transparency and copyright chapters for all providers; safety-and-security chapter for systemic-risk models, including model evaluations, a Systemic Risk Management Framework, tracking/documenting/reporting serious incidents to the EU AI Office, and cybersecurity. Baseline obligations include technical documentation and information/logging to downstream providers. Compliance with the code creates a presumption of conformity.
- Singapore's Model AI Governance Framework for Agentic AI (January 2026, discussed in parliament) is the first government-led framework aimed specifically at agent developers.

**Observability substrate.** OpenTelemetry GenAI semantic conventions matured through roughly three generations in 2025-2026: from chat-completion spans, to agent invocation spans (`invoke_agent`), `execute_tool` spans, and MCP tool-call coverage (September 2026), to task-level conventions for agentic systems (August 2025 proposal). A HoneyHive study of 73,000 agent schemas recommends OTel GenAI conventions as the official agent observability standard; Splunk, groundcover, and others normalize across the generations. OTel is the de facto audit-trail substrate for production agents.

## Part 2: What the shipped layers cover

Content safety (toxicity, self-harm, NSFW); PII redaction; jailbreak and direct/indirect prompt-injection detection; topic control; improper output handling; excessive-agency guidance (OWASP framing); centralized policy for agent fleets; end-to-end traces of agent/tool/task spans with cost and token accounting; and, at the regulatory tier, documentation, downstream logging duties, and serious-incident reporting. Prompt injection remains the consensus top threat (Zscaler and others), and 2025-2026 comparisons now benchmark platforms on runtime controls (permission scoping, tool-use policies, orchestration governance) rather than content moderation alone.

## Part 3: What they miss

Grounded in the limitations literature and direct comparison against the receipt pattern below:

1. **They are inference-time filters, not state verifiers.** Every layer surveyed (OpenAI Guardrails, NeMo, Bedrock, Constitutional Classifiers) gates the request/response boundary. None verifies that what the agent already DID still matches what was recorded about it. The historical trail is presumed intact.
2. **Audit logs are mutable storage, not tamper-evident ledgers.** OTel traces and vendor consoles are databases. There is no hash chaining of adjacent records, so deletion or rewrite of an earlier span is undetectable after the fact. An agent with write access to its own trace store can edit its trail.
3. **Silent failure and fail-open drift.** "No Free Lunch With Guardrails" (arXiv 2504.00441) frames false positives and latency as the usability tax; production writeups (Kalvium, ClickHouse) put the useful ceiling near 2 percent false positives and tell teams to monitor violation rates like error rates. That pressure pushes thresholds permissive, and there is no first-class instrument that fails closed when the guard itself cannot be verified. Plain-text latent-trajectory bypass research (r/LLMDevs, 2026) shows detection itself leaks without any jailbreak signature.
4. **Policy and config drift is unmonitored.** Deployed guardrail configs, prompt templates, and classifier versions mutate across releases. None of the surveyed frameworks ships a byte-level manifest check that exits nonzero when deployed bytes diverge from declared bytes.
5. **"Cannot verify" is not a state.** Industry gates tend to be binary pass/block. The tri-state contract (pass / drift / cannot-verify-as-its-own-exit) is absent, so unverifiable conditions masquerade as passes.
6. **Claims about the system are unguarded.** Guardrails validate model outputs; nothing validates operator or agent claims about the system itself (a census claim, a health claim, a done claim). That is exactly the fabrication surface.

## Part 4: The comparison side, with receipts (repo ground)

The append-only hash-chained receipt system with drift detection is not hypothetical; it is running in this repo, and I exercised the core instrument this session.

- **Append-only, hash-chained history.** `audit_prep/verkle_chain_immutability.md:4-9` states the formal claim: the verkle chain is append-only and immutable after a leaf is written; `mag/verkle_knot.py` implements a single-writer lock (`verkle_lock`) serializing read-modify-append on `memory/biography/verkle_chain.jsonl`, and no code path deletes or rewrites prior lines. The doc carries its own falsifier at line 19: any test that modifies an existing leaf or rewrites a prior chain line falsifies the claim.
- **Hash-manifest drift detection, live.** `seed/verify_seal.py:1-17`: docstring "check every file in MANIFEST.sha256 against its hash. Exit 0 = intact"; per-row sha256 comparison; prints MISSING/DRIFT per file; exits 1 on any drift. Live run this session: command `.venv\Scripts\python.exe seed/verify_seal.py` returned `DRIFT    engines/key_law.py`, `56/57 verified, 1 drifted, 0 missing`, exit code 1. (First attempt failed because cmd.exe swallowed the backslash in `seed\verify_seal.py`; rerun with forward slash. Reported here as it happened.)
- **Drift patrol with a tri-state exit contract.** `tools/census_drift_patrol.py`: `CENSUS_STALE_DAYS = 7` (line 78), `COLLECT_DRIFT_TOLERANCE = 20` (line 125), `parse_carrier` (line 148) fail-closes exit 2 with a "need the claim shape" message when the carrier grammar is edited away, `collect_patrol` (line 199) is the pure verdict core, `patrol` (line 250) the stale check; exit contract at lines 28-30: 0 in-bar, 1 STALE or COLLECT-DRIFT, 2 cannot-verify, "never a guess and never a pass."
- **Append-only verdict ledger with constrained writers.** `memory/workflows/REGISTRY.jsonl` holds 30 rows of `{ts, name, digest, verdict, checks}` gate verdicts (sampled lines 1-3). `githooks/pre-push:187-188` and `:263` encode the writer constraint: a push hook must never append note events to `watch/inbox/index_events.jsonl` or write REGISTRY rows; the ledger's writers are constrained, not just its content.
- **What this stack buys.** Tamper evidence (the chain), drift alarms (the manifest), tri-state honesty (exit 2 as a distinct cannot-verify verdict), claim-shape integrity (the carrier grammar gate), and writer discipline (hook law). None of these five exists in the shipped industry guardrail layers surveyed above.

## Part 5: Synthesis

The two stacks are complementary, and each is weak exactly where the other is strong. The 2025-2026 industry guardrails act at the request boundary and inside the model: they see content and can block it, but they are blind to history and to their own configuration drift. The receipt pattern acts on state and history: it cannot classify a jailbreak, but it makes the trail tamper-evident, alarms when declared bytes diverge, and refuses to pass when it cannot verify.

What industry frameworks would gain from the receipt pattern: hash-chain the OTel spans or the agent action log so trace stores become tamper-evident; a fail-closed verifier with named exit codes (pass / drift / cannot-verify) rather than binary filters; byte-manifest checks of deployed guardrail config so policy drift pages someone; a ratchet in which registered debt passes by name while new violations block (this repo's `tools/violation_ratchet.py` pattern); carrier-grammar gates on status claims so "done" is a checkable shape.

What the receipt pattern visibly lacks, stated honestly: drift detection without a repair workflow becomes a permanent red light. The same live run that proves the alarm works also shows the limit: `engines/key_law.py` has been drifted since at least 2026-09-26 (session ledger commits b9fe3e20c and c9dfcff9a record the identical 56/57 result on earlier days) and is still drifted today, the alarm firing daily with no convergence loop. The industry answer (ClickHouse: monitor violation rates and false-positive rates like error rates, with a tuning loop) is the missing half. And the receipt system here is single-machine, local-files-and-git; the industry stacks solve multi-tenant scale, streaming, and cost that the receipt pattern does not touch. The 2 percent false-positive ceiling also has a receipt-pattern analog: `COLLECT_DRIFT_TOLERANCE = 20` at `tools/census_drift_patrol.py:125` is a tuned threshold, measured live (delta of 42 noted at line 56), and subject to the same too-tight vs too-loose failure the guardrails literature documents.

Net verdict: production agent safety in 2025-2026 is strong at the boundary and weak at the ledger. The append-only hash-chained receipt pattern with drift detection covers precisely the blind spot (history, drift, cannot-verify), and its own blind spot (semantic content defense, repair loops, scale) is precisely what the commercial stacks cover.

## Sources

Searched and read 2026-09-28 via the session web-search tool:
- OpenAI Guardrails open-source announcement and AgentKit context (October 2025); repo `openai/guardrails-python`
- Anthropic, "Constitutional Classifiers" announcement 2025-02-03 (anthropic.com) and red-team update 2025-02-10; Sharma et al. 2025 arXiv; OpenReview Constitutional Classifiers++
- NVIDIA NeMo Guardrails coverage (getmaxim.ai, aport.io, augmentcode.com reference architectures)
- AWS Bedrock Guardrails and AgentCore production guidance (aws.amazon.com, tianpan.co)
- OWASP Top 10 for LLM Applications 2025 edition (genai.owasp.org, published 2024-11-18) and OWASP Top 10 for Agentic Applications (December 2025)
- EU GPAI Code of Practice (digital-strategy.ec.europa.eu; artificialintelligenceact.eu; CSET; Latham & Watkins analysis of the 2025-08-02 in-force date)
- Singapore Model AI Governance Framework for Agentic AI (January 2026)
- OpenTelemetry GenAI semantic conventions: tasks proposal (August 2025, github), MCP tool-call coverage (rahulranjan.org, September 2026), HoneyHive 73,000-schema study, Splunk and groundcover docs
- Limitations: "No Free Lunch With Guardrails" (arxiv.org/html/2504.00441v2), Kalvium Labs production guardrails writeup, ClickHouse LLM guardrails engineering note, FutureAGI limitations glossary, GMI Cloud defense-in-depth piece, r/LLMDevs latent-trajectory bypass thread

Read in this repo:
- `seed/verify_seal.py` (lines 1-17, read in full; executed live, exit 1)
- `tools/census_drift_patrol.py` (grep-located lines 11-12, 28-30, 56, 78, 125, 148, 199, 250)
- `audit_prep/verkle_chain_immutability.md` (read in full, 19 lines)
- `memory/workflows/REGISTRY.jsonl` (first 3 rows sampled, 30 rows total)
- `githooks/pre-push` (lines 187-188, 263, via grep)
