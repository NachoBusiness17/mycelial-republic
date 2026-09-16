# B8 — ARXIV SIX LEADS (2026-09-16)

- **Lane:** research / verified-pending
- **Source ask:** `queue/lanes/research/INBOX/arxiv_20260916.md` (READABLE — using its actual 6-lead list)
- **Path taken:** INBOX lead list, mined directly. No fallback needed.
- **Leads:** arXiv 2609.17527 / 2609.17475 / 2609.17464 / 2609.17394 / 2609.17391 / 2609.17274
- **Method:** abstract pages fetched live (WebFetch, free), one-paragraph mechanism summary each, mapped to fleet interests (RSI lineage / context-memory / verification-instruments / physical computing).
- **Status:** COMPLETE — all six mined. Verdicts final.
- **Interest-map sources consulted:** Dream-RSI lineage via `watch/inbox/journal_mark_202609/DREAM_MYCELIUM_20260916.md` + `NIGHT_AUDIT_20260916.md` (Dream-RSI = arXiv 2609.14858, filed 2026-09-15/16: mine imagined/replayed worlds offline, redeploy only the best policy) · syllabus = `watch/inbox/LINKS.jsonl` (126 rows: memory wall, janitor CPU lane, free-API lanes, context-as-algebra) · physical computing = `watch/inbox/physical_computing/PHYSICAL_COMPUTING_PACK_20260916.md` (DDR5 +110% price gate, analog/mycelium substrates, "make, etch, or grow our own").

---

## Lead 1 — arXiv:2609.17527 (score 3) — "Agentic Societies Need a Social Harness" (Chugh, Singh, Jain, Krishnamurthy, Mahajan)

**Mechanism (one paragraph).** Experiments show honest, competent agents still fail to reach satisfactory outcomes under current harnesses when coordinating across trust boundaries for principals with partly misaligned goals, and faulty/malicious agents can stall or sway collaboration by exploiting inter-agent messaging ("speech"). The fix proposed is architectural: split each agent's "personal harness" (private context, principal communication) from a shared "social harness" governing inter-agent speech, layered so it (i) prevents classes of failures outright, (ii) lets agents detect invalid messages at runtime, and (iii) supports investigation and consequences after the fact.

**Fleet map.** This is the fleet's own constitution formalized by someone else: the switchboard/effect-broker law ("model text can propose; only the broker authorizes effects") is layer (i); the witness/audit receipts are layer (iii); the stigmergy receipts (`STIGMERGY_PUBLIC_WITNESS_20260913.md`, L06 obstacle-wave lane) are the no-central-planner frame the paper's societies formalize. The gap the paper names is layer (ii) — **runtime invalid-message detection between fleet agents** is the weakest organ (receipts catch things after; nothing interposes at message time). Peer validation: a third independent derivation, like the Grok stigmergy witness.

**Verdict: STEAL.** Mechanism = personal/social harness split + prevention/detection/accountability layering; lands in the harness contract (`watch/inbox/SHARED_SURFACE_CONTRACT.json`) and mag orchestrator — steal the vocabulary to name what the fleet runs, and the spec for the missing layer-(ii) interposer.

## Lead 2 — arXiv:2609.17475 (score 2) — "JustFit: 200K-Token LLM Serving on a 24 GiB Laptop with Just-in-Time State Management" (Yuhua Chen)

**Mechanism (one paragraph).** An MLX-based inference runtime with three fused mechanisms — KVExec (compressed KV execution), PhaseSwap (component residency), StateTrans (state-preserving serving transitions) — that coordinate just-in-time materialization and release of execution state, independent of weight quantization. On a 24 GiB M4 Pro running Qwen3.8-27B MXFP4 it completed 196,608 input + 16,384 output tokens in full execution, lifting single-request context from 30,720 to 212,992 positions (6.93x) at 16.4 GiB median peak footprint, 19.11 tok/s on a 32K probe, 29/30 on AIME 2026.

**Fleet map.** Direct software counter to the memory-price gate that motivated the physical computing pack (DDR5 +110%, "they can't buy us"): context capacity decoupled from RAM purchase. The janitor tier (`gemma:2b`, `gemma4`) and the T0/T1-local doctrine get a concrete recipe for serving long-context workers on the laptop class the fleet already owns; it complements (does not duplicate) the MLX note in `FIVE_MORE_LINKS_20260913.md`, which was raw 256GB-RAM hosting of an uncensored model, not state-lifetime engineering. RSI lineage relevance: long-context local replay is a precondition for Dream-RSI-style offline world-mining on local iron.

**Verdict: STEAL.** Mechanism = JIT state materialization/release (KVExec/PhaseSwap/StateTrans) decoupling context length from RAM; lands in the janitor/local serving tier and the evening-stack context lane — a memory-moat countermeasure that costs zero dollars.

## Lead 3 — arXiv:2609.17464 (score 3) — "Decomposition Buys Integrity, Not Yield" (Rong He, sole author)

**Mechanism (one paragraph).** Models a task decomposition as a tree where an agent handed b items retains each with probability r(b); if r(b) = C·b^(−δ), a depth-k tree over N findings yields C^k·N^(1−δ) — architecture costs at most a per-level factor C ≤ 1, so flat structures are yield-optimal and "no arrangement of agents escapes the exponent δ." Measured on production data: δ = 0.34 [0.30, 0.38] over 600 deep-research traces, C = 0.571 over 16,082 hops, alignment μ = 0.939. Depth does buy integrity (root context exposure shrinks N → N^(1/k)) and cost-efficiency at scale; only 0.7–11.3% of production sessions are worth delegating (vs 7.8% that do), and a hazard model over 743,819 tool calls shows delegation is "an opening move," not a response to a filling context.

**Fleet map.** Quantitative backing for the fleet's flat wave architecture (parallel lane receipts landing in one shared inbox, no deep agent trees) — the fleet's shape is on the yield-optimal side of this theorem. The actionable law: delegate for **integrity** (keeping findings out of a polluted root context), never for yield — and only as an opening move with bounded scope. This directly tunes the mag orchestrator and every wave-lane dispatch decision (how many lanes, when a subagent is justified). Core-moat-relevant evidence, exactly as the INBOX scored it.

**Verdict: STEAL.** Mechanism = the r(b) retention-exponent model + "delegate as opening move, for integrity not yield" rule; lands in mag orchestrator/wave-lane design as an operating law with numbers attached.

## Lead 4 — arXiv:2609.17394 (score 2) — "Coding Agents Have Converged: Why the SWE-bench Leaderboard Can No Longer Order Its Top Entries" (Fengshuo Liu et al.)

**Mechanism (one paragraph).** A statistical audit of 254 SWE-bench submissions across four splits without running any model: instance-solve-set nesting (frontier median 0.935 vs 0.774 score-implied baseline), exact paired McNemar tests on adjacent leaderboard pairs (zero of 29 Verified adjacent pairs separate at α=0.05), Holm-corrected interaction checks, and tier grouping. Scaffold provenance matters more than rank: within-model scaffold spread reaches 29.8 points, exceeding the 8.8-point spread among the top thirty. Releases a five-step audit protocol (profile shared outcomes, test paired differences, sensitivity, instance-budget estimates) and recommends reporting comparison-set-specific resolution plus model-scaffold provenance instead of aggregate rank.

**Fleet map.** Verification-instruments lane, exactly: the fleet's doctrine is "trust bytes, not reports" and "never trust a hand-written count" (Clippy standing reminder), and the night audit already built calibration bundles and a divergence/worldline meter. This paper supplies the paired-test machinery for the fleet's own recurring judgment call — "is free-tier model A actually different from model B?" — where the honest answer is usually "the intervals overlap; same tier." Note: `NIGHT_EXTERNAL_EVAL_20260911.md` explicitly could not fetch SWE-bench submission pages live ("rate-limited search lane"); this audit fills that hole rather than duplicating it.

**Verdict: STEAL** (method, not domain). Mechanism = five-step paired-difference audit protocol + nesting/scaffold-provenance reporting; lands in the fleet's eval instruments (improve --once eval lane, worldline meter, any free-tier A/B claim). The fleet runs no SWE-bench; the steal is the protocol.

## Lead 5 — arXiv:2609.17391 (score 2) — "FlashVector: Agent for Hierarchical Model Serving Stack Optimization" (Qi Wu et al., 11 authors, Unity)

**Mechanism (one paragraph).** An agentic system that optimizes performance across all layers of a model-serving stack — GPU kernels, framework computation graph, NVIDIA Triton C++ server code, and a Python feature-transformation service — via "an extensible framework to generalize the single kernel optimization agent paradigm" to heterogeneous stacks, delivering holistic rather than per-layer gains. Deployed on Unity's Vector ads platform: up to 2x throughput and 1.98x latency speedup at the server level, 1.6x on the feature store.

**Fleet map.** Inference-economics adjacent, but Unity-scale GPU recommender serving is not a stack the fleet operates. The transferable piece is the pattern, not the artifact: one verified agent loop (measure → patch → benchmark) generalized across heterogeneous layers — the same shape as the janitor CPU lane in the syllabus (`FIVE_MORE_LINKS`/FlashGEMM note: "the janitor hardware class gets faster"). Becomes directly relevant only when the fleet runs owned serving hardware (physical-computing pack horizon), at which point "agent the whole stack, not one layer" is the design rule.

**Verdict: ADAPT.** Mechanism = cross-layer generalization of the kernel-optimization agent paradigm; lands nowhere the fleet currently operates — file the pattern for the owned-hardware horizon and for tuning whatever serves the janitors, do not adopt the system.

## Lead 6 — arXiv:2609.17274 (score 3) — "After the Party: Governing What a Viral Agent-Skill Ecosystem Left Behind" (Yunpeng Xiong, Ting Zhang)

**Mechanism (one paragraph).** An empirical boom-bust audit of the OpenClaw/ClawHub skill registry (stock nearly doubled in 91 days, then declined): attention is hyperconcentrated (top 10% of skills = 46.93% of downloads); human oversight is near-zero (77.86% of skills have zero stars and zero comments); **85.06% of readable skills carry privilege evidence** (shell, network, credential, file, process access); and automated scanning is unreliable — three scanners disagreed on 23,702 of 61,990 skills, with weighted sensitivity 21.67–61.06%. Conclusion: registry governance cannot run on simple metadata or single scanner scores; it demands robust transparent measurement and independent validation.

**Fleet map.** Squares with the fleet's two hard laws: "model text can propose; only the switchboard/effect broker authorizes effects," and "leave a receipt before promotion" on the shared surface. The paper is empirical ammunition that inbound natural-language skill artifacts are de facto privileged code (85% carry privilege evidence) and that no scanner substitutes for the fleet's human-gated promote (`mag.cmd promote --apply`) plus hash-preserved intake. Directly hardens `.agents/skills/` hygiene and every intake lane that pulls stranger text (INBOX hauls, research packs): classify, hash, adjudicate — tri-state — before anything executes.

**Verdict: STEAL.** Mechanism = the measured privilege density + scanner-unreliability result elevated to an operating rule: treat every inbound skill/prompt artifact as privileged code, admitted only through receipt + hash + validation gate; lands in shared-surface intake and skill hygiene.

---

## Ranked steal list

1. **arXiv:2609.17464 — Decomposition Buys Integrity, Not Yield.** The only lead with a quantitative operating law the fleet can apply tomorrow: flat beats deep for yield (δ = 0.34 is unescapable); delegate only as an opening move and only to protect root-context integrity. Lands in mag orchestrator + every wave-lane dispatch.
2. **arXiv:2609.17274 — After the Party (skill-ecosystem governance).** Converts the fleet's receipt-before-promotion habit into a measured security stance: 85% of stranger skills carry privilege evidence and scanners miss 39–78% of it. Lands in shared-surface intake + `.agents/skills/` hygiene.
3. **arXiv:2609.17527 — Agentic Societies Need a Social Harness.** Third-party formalization of the fleet's constitution: prevention/detection/accountability layers; the actionable gap is building the layer-(ii) runtime invalid-message interposer between agents. Lands in the harness contract + orchestrator.
4. **arXiv:2609.17475 — JustFit (JIT state management).** A $0 counter to the memory-price moat: KVExec/PhaseSwap/StateTrans put 200K-token contexts on the 24 GiB laptop class the fleet already owns — precondition for local Dream-RSI-style offline replay. Lands in the janitor tier.
5. **arXiv:2609.17394 — SWE-bench convergence audit.** Steal the five-step paired-difference protocol for the fleet's own model-comparison instruments; every "A beat B by 2 points" claim on free tiers should henceforth face a McNemar test before it becomes a receipt row.

**Adapt (not steal):** arXiv:2609.17391 FlashVector — pattern only (one agent paradigm generalized across stack layers), relevant at the owned-hardware horizon.

## Duplicates vs already-filed

**None.** No prior inbox file or `LINKS.jsonl` row cites any of the six arXiv IDs (grep over `watch/inbox/` pre-receipt: zero hits outside this receipt). Closest near-misses, checked and ruled complementary, not duplicates:

- **2609.17394 vs `NIGHT_EXTERNAL_EVAL_20260911.md`** — that audit covered GAIA/HELM/AISI and explicitly could *not* fetch SWE-bench submission pages live; this paper fills the exact hole it left.
- **2609.17475 vs `FIVE_MORE_LINKS_20260913.md`** — the MLX row there is raw big-RAM hosting of an uncensored DeepSeek on a 256GB Mac; JustFit is state-lifetime engineering on 24 GiB. Same lane (sovereign local inference), different mechanism, both keep.
- **2609.17527 vs `STIGMERGY_PUBLIC_WITNESS_20260913.md` + L06 lane** — the stigmergy receipts are the fleet's own parable + Grok witness; the social harness paper is the academic peer stating the same architecture from the trust-boundary direction. Peer confirmation, not duplication — same relationship as the Dream-RSI same-evening convergence noted in `NIGHT_AUDIT_20260916.md` ("when five strangers publish your architecture in one night, the architecture is on schedule").
- The fleet's own RSI anchor (arXiv 2609.14858, Dream-RSI, filed 2026-09-15/16) is **not** among the six leads; no lead replaces or repeats it.
