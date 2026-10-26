# THE_LENSING: frontier judgment on the route (MC6 paid ask)

Status: ok. Metered cost: $0.1349. Seconds: 86.7. Usage: {"prompt_tokens": 1099, "completion_tokens": 6525, "total_tokens": 7624, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 1675, "image_tokens": 0, "audio_tokens": 0}, "cost": 0.134896, "cost_details": {"source": "openrouter_list", "floor_applied": false, "rate_source": "openrouter_catalog"}}. Finish: stop.
Prompt sha256: 539cdcf73e17796349ffb81d92d53dd2126658eede6c29f6e2ed2b50d5562280 (2891B).
Full return below, verbatim. Em-dash count in return body: 0.

---

# Propagation Engineering: How Frontier Judgment Moves Through Agent Meshes

## Bottom line

The main risk in your mesh is probably not that a frontier verdict loses force as it becomes doctrine. The literature and my inference both point the other way. **A verdict gains force and loses scope.** Caveats, conditions and confidence levels are the first things stripped at each hop. The imperative survives. Your $0.42 lensing verdict is more likely to be over-applied in lane 37 than under-applied.

Your loop (observe→profile→rib→boot→harness→observe) is more instrumented than most published practice on the model side. It is weak on the verdict side. You fingerprint the executors but, as far as the context shows, not the judgments.

---

## 1. What production meshes actually use

**Shared doctrine files** [public]
- The dominant pattern is static markdown injected at boot: AGENTS.md, CLAUDE.md, .cursor/rules, and Copilot instructions files.
- These are versioned in git but almost never carry provenance. They don't record which model, on what date, answering what question, produced the rule.
- Doctrine is treated as code, not as evidence.

**Per-model profiles** [public/inference]
- Most shops stop at routing config: LiteLLM or OpenRouter model lists, fallback chains, and per-model temperature and max-tokens settings.
- Behavioral per-model layers exist mostly inside tooling vendors. Examples are model-specific system prompts in coding agents, and Aider's per-model edit-format settings, which reflect measured differences in how models follow diff formats.
- Fingerprint-bound behavioral profiles, where a profile is invalidated when the model identity changes, are rare in anything published. I can't verify private practice. The instrument that would close this is a survey of agent-framework configs, or conversations with platform teams at a few agent shops.

**Ledger/routing layers** [public]
- Observability products capture traces and costs: LangSmith, Braintrust, Langfuse, Helicone.
- Routing is usually cost/latency/capability based. It is rarely judgment-provenance based.
- I know of no mainstream tool that tracks "this downstream action was licensed by verdict V-0042."

**MCP server patterns** [public]
- MCP is mostly used for tool and resource exposure: filesystems, databases, and APIs.
- "Prompts" and "resources" primitives exist and can serve doctrine dynamically.
- Using MCP as a *judgment distribution bus*, which your framing describes, is uncommon. My inference is that it is architecturally sound. It is better than static files because it allows central revocation, but only if lanes actually re-fetch rather than cache.

**Cache-aware prompt design** [public]
- Anthropic, OpenAI, DeepSeek and others discount cached prefixes. Standard practice is: stable doctrine first, volatile task last.
- My inference is that this creates **economic pressure against doctrine freshness**. Every rib edit invalidates the prefix cache across every lane that shares it.
- At ~1B tokens/day, you have a cost gradient that silently rewards not updating doctrine. Nobody writes this down as a design force, but it is one.

## 2. What research says about judgment decay across hops

There is no study, that I know of, specifically of "frontier verdict → doctrine file → executor model." The adjacent literature is consistent enough to reason from.

**Transmission chains converge to attractors.**
- LLM "telephone game" studies [public: Perez et al. 2024, "When LLMs Play the Telephone Game"] find that iterated LLM rewriting drifts toward model-specific attractors in length, toxicity and positivity.
- Content converges toward what the *transmitting* model prefers, not what the source said.
- **Implication [inference]:** if GLM-5.3 paraphrases or summarizes doctrine for downstream lanes, the doctrine drifts toward GLM-5.3's priors. That drift is fastest for the parts that conflict with them.

**Instruction adherence decays within a session.**
- Persona/instruction drift work [public: Li et al. 2024, "Measuring and Controlling Instruction (In)Stability"] shows system-prompt adherence degrading over a handful of turns.
- Long-context position effects [public: Liu et al. 2023, "Lost in the Middle"] show that mid-context material is under-used.
- A rib buried in a large boot prefix competes with 1M tokens of context.

**Prompt behavior doesn't port cleanly across models.**
- Formatting sensitivity work [public: Sclar et al. 2023] shows large performance swings from semantically irrelevant formatting changes, and these swings differ by model.
- A rib worded for Claude may bind differently on GLM-5.3. That is presumably why you built per-model profiles, and it is the correct response.

**Multi-agent failures cluster at handoffs.**
- The MAST taxonomy [public: Cemri et al. 2025, "Why Do Multi-Agent LLM Systems Fail?"] attributes a large share of failures to specification ambiguity and inter-agent misalignment rather than raw capability.
- Doctrine is a specification. Ambiguity in it is multiplied by lane count.

**Model behavior drifts under a stable name.**
- [public: Chen, Zaharia, Zou 2023] documented large behavior changes in same-named API models over months.
- This is the canonical citation for "verify the propagated judgment still applies." It targets the *executor*, not the *verdict*.

**Disconfirming evidence for "decay happens":**
- Most telephone-chain decay requires *paraphrase*. If your ribs are propagated verbatim via MCP, transmission is near-lossless. The decay then moves to *interpretation*, meaning how each executor reads identical text.
- That is a different failure with a different fix: per-model compliance probes, not provenance tracking.
- If you already propagate verbatim, half of this section applies less. The instrument is to diff rib text as served against rib text as written, per lane.

**The finding I'd weight most [inference, supported by the attractor results]:** conditionals are fragile and imperatives are sticky.
- "Prefer X when Y, confidence moderate" becomes "prefer X" within one or two summarization hops.
- The verdict doesn't lose force. It loses its *domain of validity*.

## 3. How others verify propagated judgment after drift

Honestly: mostly they don't. They verify *outputs*, not *judgments*.

**Regression eval suites** [public]
- Tools: promptfoo, Braintrust, OpenAI Evals, and golden-set CI.
- These are run when prompts or models change. They catch output regressions, not "this rule is now wrong."

**Canary/shadow traffic** [public]
- Some shops shadow a new model version on production traffic before cutover.
- This validates the executor, not the doctrine's premises.

**LLM-as-judge with cross-family judges** [public]
- Self-preference bias in judges is documented [Panickssery et al. 2024]. Your second-family judge rule is the right mitigation, and most teams don't do it.
- But the judge evaluates outputs *against the doctrine*. If the doctrine is stale, the judge enforces staleness competently.

**Constitution-style re-derivation** [public/inference]
- Labs periodically revisit rule sets like constitutions and model specs, with human review.
- That is the closest analog to "re-ask the frontier whether the verdict still holds," and it is human-gated and slow.

**The gap the field hasn't closed [inference]:** verdict expiry. I know of no common practice that attaches "re-derive by date D or when condition C changes" to a propagated rule.

Your own evidence packet illustrates why this matters:
- The Anthropic red-team read and the NIST CAISI benchmark disagree on GLM-5.3's cyber capability, two weeks apart [report].
- A mesh that had propagated either verdict as doctrine on day one, without the contradiction attached, would be confidently wrong in one direction.
- That is the exact shape of the risk for your $0.42 verdict.

## 4. Rating your loop against the field

**observe→profile→rib→boot→harness→observe**

| Stage | Field norm | You | Rating |
|---|---|---|---|
| observe | traces/cost dashboards | measured rate envelopes, in-game behavioral measurement | ahead [report/inference] |
| profile | routing config | per-animal behavioral profiles, fingerprint-bound | well ahead |
| rib | static markdown, no provenance | doctrine files + per-model layer, provenance unknown | parity-to-ahead; provenance unclear |
| boot | prefix injection, cache-optimized | MCP-served into ~40 lanes | ahead (revocable) if lanes re-fetch |
| harness | eval CI on change | second-family judges | ahead on judge independence |
| observe (close) | output regression | unclear whether you observe *verdict validity* vs *executor compliance* | likely the gap |

**Overall [inference]:**
- Your loop is a strong **executor-drift** loop.
- It closes on "is the model still behaving as profiled?"
- It does not visibly close on "is the rib still true?"
- Those need different instruments. The loop as described has only the first.

## 5. Blind spots

**1. Single-sample verdicts propagated at fan-out 40.**
- One frontier call is one draw from a distribution.
- At $0.42, the variance of that verdict is unmeasured and cheap to measure. Re-ask 3-5 times, and across two frontier families, before a rib ships.
- Your second-family rule applies to *judges of output*. It should also apply to *authors of doctrine*.
- **Disconfirming:** if the verdict was re-derived and stable, ignore this. Nothing in the context says it was.

**2. Scope stripping.**
- Check whether each rib carries its conditions and falsifiers, or only the directive.
- If only the directive, your 40 lanes are applying it outside its domain, and your harness judges will approve because they read the same rib.

**3. The cache tax on freshness.**
- As above: updating doctrine costs cache hits across the fleet.
- Watch for rib edits being batched or deferred for cost reasons. That is doctrine ossification with a financial motive.

**4. Doctrine as an injection surface.**
- The red-team report you cite claims simple bypasses worked 64-100% of the time on GLM-5.3 [report].
- Your executors are GLM-5.3, and MCP-served doctrine is trusted boot context. A poisoned rib, whether from a compromised server, a sensing-fleet artifact that gets promoted, or a lane that writes back to doctrine, propagates to every lane at once.
- Fan-out is a blast radius.
- **Disconfirming:** NIST CAISI rates the model weaker on offense [report]. But bypass susceptibility is a different property from exploit capability, and neither report contradicts the other on that axis.
- **Instrument:** signed ribs, write-path audit, and a red-team probe that attempts to inject a rib through each ingress.

**5. Fingerprint binding catches swaps, not same-fingerprint drift.**
- Behavior changes with harness edits, context composition, quantization or serving-stack changes, and tool availability, all under an identical model ID.
- Your profile can be "valid" by fingerprint and wrong by behavior.

**6. Transfer of the positive-reinforcement steering law.**
- It was measured in-game on a school [report]. That result is interesting.
- Transfer to LLM agent steering is a hypothesis, not a finding. Reward-framed vs threat-framed prompts have mixed published evidence [public: the "emotional prompting" and threat/tip literature is small-n and inconsistent across models].
- If ribs are written under this law, you are propagating an untested transfer claim as doctrine. Blind spot #2 applies to your own doctrine too.

**7. The loop observes what the harness measures.**
- Goodhart: if "observe" reads harness outputs, and the harness is built from ribs, the loop can converge on self-consistency rather than correctness.
- You need at least one observation channel that doesn't pass through doctrine: ground-truth outcomes, human spot-checks, or external benchmarks.

## 6. Instruments to close the gaps

1. **Verdict ledger.** Each rib gets these fields:
   - source question (verbatim)
   - model and date
   - sample count and agreement rate
   - stated confidence
   - scope conditions
   - named falsifiers
   - expiry date or trigger condition
   - list of lanes consuming it

   This is cheap and has high leverage. It turns doctrine into evidence.
2. **Hop-fidelity probe.** Weekly, ask each lane's executor to restate a rib's *conditions* (not the directive), then diff against the ledger. Rising condition-loss means scope stripping is occurring.
3. **Rib ablation.** Run a sample of lanes with and without each load-bearing rib, and measure the outcome delta. A rib with no measurable effect is dead weight in your cached prefix. A rib with a large effect deserves re-derivation priority.
4. **Scheduled re-derivation.** Re-ask the original frontier question on expiry, with new evidence appended, across two families. At your spend profile, quarterly re-derivation of the top 20 ribs costs single-digit dollars.
5. **Per-model compliance canaries.** Build tasks where the rib should flip behavior, and track the compliance rate per executor per week. This detects same-fingerprint drift that binding misses.
6. **Doctrine-free outcome channel.** Track at least one outcome metric that doesn't route through rib-derived judges.

---

**Summary judgment [inference]:**
- On executor-side engineering, you are ahead of published practice: profiles, fingerprints, second-family judges and measured envelopes.
- On verdict-side engineering, you are at field parity, and field parity is poor. Provenance, variance, scope, expiry, and doctrine as an attack surface are largely unaddressed.
- The phrase "frontier reasoning via MCP servers" is accurate about the transport. What it obscures is that frontier reasoning, once served, stops being reasoning and becomes authority. Authority is what decays wrongly: it outlives its conditions.