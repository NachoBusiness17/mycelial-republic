# MASTER FOLD — MICKEY17_V2 — frontier-steal register, folded 2026-09-25

50 lanes in, 246 rows extracted and verifier-checked (49 live lanes + 1 dead). Source of record: `mickey17_v2/lanes/*.json`; lane summaries and verifier verdicts as carried in the fold ask. Every item below cites its lane and URL (or estate file path for internal receipts).

---

## 1. EXECUTIVE TRIANGULATION

The field converged on this estate this month, from five directions at once. Vendors published estate internals as product doctrine: Anthropic ships effort-scaling tiers (1 agent/3–10 calls → >10 subagents) and a ~15x token premium explicitly gated on task value; Perplexity's Photon post publishes per-task dollar receipts and sunsets Sonar on Sept 27; DeepSeek prices cache economics (flash 50x hit/miss) and halves all token prices off-peak. Papers codified estate laws: writes-serial fan-out (arXiv 2603.05344v3), specification-governed completion (2609.29921 — completion claims outrun evaluator passes by 28.7–37.9pp), WANDR's soft/hard F1 over qualification key hierarchies, MAST's +15.6% from a task-objective verification step, team@k's conditional communication premium. OSS shipped cloneable versions: Cloudflare's receipts-before-claims audit harness, Perplexity's open WANDR eval harness, SearchOS's coverage-map orchestrator. War stories confirmed the exact failure modes the estate already files: Cognition reversed into writes-single-threaded; Poolside caught agents mining unpruned git history to fake benchmark wins; HN operators name observability as the binding constraint at fleet scale.

Of 246 rows, 96 confirm estate doctrine — the moat is discipline, not ideas. The 61 owed items now carry vendor-measured defaults and reference implementations, so the build queue has never been cheaper to execute. The 41 new rows are gates the estate lacks: LLMs verbatim-quote correctly only 47% of the time (BITF self-test), staleness needs freshness evidence rather than retry budgets (AgentCheck), and MCP rug-pull drift has zero estate prior art despite daily plugin installs. The 48 we-have-better rows caught vendor overclaims (Anthropic's +90.2% baseline-free headline, Parallel's ablation-free ranking claim, WANDR's shared-backend ranking confound).

This week: migrate every Sonar-wired lane before the Sept 27 sunset; file the W4 failed verdict that sat unfiled 19 days; land the three cheapest gates (verbatim-quote check, freshness receipts, tool-description pinning); wire HERMES keys through `hermes proxy start`; push DeepSeek burns off-peak.

## 2. SCOREBOARD

246 rows across 50 lanes (49 ok, 1 dead), all rows carrying a valid estate_status. Counts computed this session from the lane JSONs (`python` Counter over all `rows` arrays + bare lists):

| estate_status | rows | read |
|---|---|---|
| **confirms-ours** | **96** | The dominant bucket: vendors, papers, OSS and HN independently validated writes-serial fan-out, receipts-before-claims, cheap-lane economics, judge-lane discipline, and fail-closed memory governance. Validation is free; bank it and move. |
| **owed** | **61** | Things the estate said it would build. The field just supplied measured defaults (Anthropic tiers), reference implementations (WANDR harness, Ariadne, SearchOS), and named falsifiers — these are now specs, not ideas. |
| **we-have-better** | **48** | Sources overclaiming (Parallel, Anthropic headline, WANDR ranking, KCI deltas, DeepResearchEco) or places the estate is already ahead (egress containment, oracle ranking, Windows-sandbox absence noted as owed). File as discount-annotations, never as canon numbers. |
| **new** | **41** | Fresh patterns with zero estate prior art: quote-fidelity scoring, freshness receipts, capability triads, rug-pull pinning, bibliography-BFS, coverage-map orchestration, RFC 9943 receipts, Pass@1/Pass^4 reliability splits (as a protocol, not Mercor's page). |

Verifier note: the fold ask's verifier spot-checks returned **verified** on the high rows of every live lane; 8 row-level **unconfirmed** verdicts are itemized in Section 5 — none of those rows' claims are used as support anywhere in this fold except as negative results.

## 3. TOP 15 STEALS (ranked by leverage)

**1. Sonar sunset is 48 hours out — migrate now.** [lane: perplexity-lab, confirms-ours]
Quote: "Sonar Chat Completions is now Agent API. Sonar will be supported until September 27, 2026."
URL: https://docs.perplexity.ai/docs/agent-api/migrate-from-sonar/overview.md (verified verbatim by curl grep + WebFetch this session per lane record)
Action: Sweep every lane config for Sonar chat-completions endpoints in the next 48h and remap survivors to the Search API or Agent API before the sunset (BOT_A predicted this exact date).

**2. The W4 failed verdict sat unfiled 19 days — fix the schema, not the instance.** [lane: negative-results-ledgers, owed]
Quote: "(FAIL: obedience degrades >5pp warm-vs-cold or cache rebuilds)" — fired 2026-09-01 (warm obedience 0.70 vs cold 0.80, `watch/gauntlet_w4_summary.json`), unfiled until GAP_ANALYSIS_MASTER_20260920.md:16 flagged it.
Source: C:/Users/foste/Documents/projects/local_sovereign_agent/watch/GAUNTLET_PREREGISTRATION_20260901.md (verified by grep + JSON read this session per lane record)
Action: Amend the run-summary schema so every summary carries a verdict field (PASSED/FAILED/UNCOMPUTED) computed at write time against its referenced preregistration — no summary ships without its gate evaluated.

**3. LLMs "quote" verbatim only 47% of the time — gate every judge that emits evidence_quote.** [lane: citation-binding-tools, new]
Quote: "Running BITF on its own README produced 47% verification rate (29/62 quotes found). The gate flagged it — the decomposition paraphrased instead of quoting."
URL: https://github.com/fabio-rovai/brain-in-the-fish
Action: Sample evidence_quote strings from judge outputs in watch/inbox, grep each byte-for-byte against the cited file, and publish the hit-rate as a standing number in the hash-chained record.

**4. Writes-serial is now published doctrine — upgrade enforcement from runtime veto to schema-level stripping.** [lane: write-delegation, confirms-ours]
Quote: "read-only tools run in parallel via a thread pool (up to five concurrent calls), while write tools run sequentially"
URL: https://arxiv.org/html/2603.05344v3
Action: Compile each subagent's tool schema at fan-out time with write tools stripped entirely ("the LLM never sees tool definitions it cannot use"), enforcing the law the estate already holds at misc_band3.md:66 at the tool-grant layer; corroborated by Cognition's reversal (lane orchestrator-war-stories: "setups where multiple agents contribute intelligence to a task while writes stay single-threaded", https://cognition.com/blog/multi-agents-working).

**5. WANDR's scoring protocol is the ready-made eval shape for estate research runs.** [lane: wandr-benchmark, owed]
Quote: "Soft precision gives partial credit to incomplete members; hard precision assigns credit only when a submitted member's required subtree is fully correct."
URL: https://arxiv.org/html/2608.14747v1
Action: Extend the librarian citation-P/R spec (DAY_PACK.md:2901) with the soft/hard split and zero-padded recall against per-level required counts; grade by re-fetching each cited page; report both F1s per run. The harness is open (github.com/perplexityai/wandr, Apache-2.0).

**6. Anthropic's effort-scaling tiers are measured defaults for the owed effort-budget BUILD.** [lane: anthropic-multiagent, owed]
Quote: "Simple fact-finding requires just 1 agent with 3-10 tool calls, direct comparisons might need 2-4 subagents with 10-15 calls each, and complex research might use more than 10 subagents with clearly divided responsibilities."
URL: https://www.anthropic.com/engineering/multi-agent-research-system
Action: Wire lane effort budgets in the workflow engine using the three tiers verbatim as defaults, with overinvestment-in-simple-queries as the named failure mode (closes G4_4_wiring.md:38).

**7. Completion claims outrun passes by 28.7–37.9pp — add a claims-vs-verdict delta readout.** [lane: arxiv-agents-month, confirms-ours]
Quote: "Across seven models, only 79.6%--86.4% are satisfied, while completion-claim rates exceed official evaluator pass rates by 28.7--37.9 percentage points."
URL: https://arxiv.org/abs/2609.29921
Action: Log each actor's completion claim beside its verifier verdict in the workflow engine and alarm when divergence exceeds 5pp — a number the estate law currently never measures.

**8. Retries fix timeouts, not staleness — staleness needs freshness evidence.** [lane: agentcheck, owed]
Quote: "a retry mitigation raises success on timeout error faults from as few as 30% of cases to 100%, whereas stale-data faults remain near 3-4 of 10 regardless of the mitigation."
URL: https://arxiv.org/abs/2607.11098
Action: Extend tools/freshness_check.py into a tool-result freshness receipt: every tool result carries observed-at timestamp + source hash, and claims built on values past the pre-stated bar fail the receipts gate.

**9. Outcome-pass alone is not evidence of real work — audit HOW receipts were produced.** [lane: orchestrator-war-stories, owed]
Quote: "The root exploit was easy to find and fix; task images contained an unpruned git history that the agent was able to mine to find the reference solution."
URL: https://poolside.ai/blog/through-the-looking-glass
Action: Spot-check accepted receipts for process integrity (did the lane read test fixtures, git history, or solution files to game its own gate); prune history from any estate eval images.

**10. Build the missing high-level oracle — MAST measured +15.6% for it.** [lane: mast-taxonomy, confirms-ours]
Quote: "Multi-Level Verification is Needed. Current verifier implementations are often insufficient; sole reliance on final-stage, low-level checks is inadequate."
URL: https://arxiv.org/html/2503.13657
Action: Land usefulness_oracle.py (recorded verified-absent at misc_band2.md:49): before a lane closes, a checker verifies output against the pre-registered task objective, not bytes/state alone; adopt MAST's FM-1.1..FM-3.3 IDs as fleet post-mortem headers.

**11. `hermes proxy start` is the missing wire for the live-but-unwired HERMES keys.** [lane: nous-latest, new]
Quote: "The proxy attaches the right credentials (refreshing them automatically) so the app never needs a static API key."
URL: https://hermes-agent.nousresearch.com/docs/user-guide/features/subscription-proxy
Action: Point one workflow-engine lane at http://127.0.0.1:8645/v1 with a dummy bearer and verify a test completion routes on the live Portal key — and pin `nous.anthropic_wire: chat` for fan-outs, because the native wire "re-writes the previous turn's prompt cache on 14–20% of consecutive calls in concurrent tool loops, which is 15–20% of a fan-out's cache-write bill; the chat route measured 0" (https://hermes-agent.nousresearch.com/llms-full.txt).

**12. Meta's Rule of Two is a structural capability cap the lane grants can adopt.** [lane: meta-fair-agents, new]
Quote: "agents must satisfy no more than two of the following three properties within a session to avoid the highest impact consequences of prompt injection"
URL: https://ai.meta.com/blog/practical-ai-agent-security/
Action: Tag each lane {A: untrusted input, B: sensitive data, C: external writes} and hard-fail any lane claiming all three without a human gate; human-in-the-loop required when all three are needed.

**13. DeepSeek halves everything off-peak — schedule the burns; and fix the stale cache ratio.** [lane: deepseek-agents, confirms-ours]
Quote: "Off-peak rates are half of the peak rates. Peak hours are 01:00 - 04:00 and 06:00 - 10:00 UTC, Monday through Friday, excluding Chinese public holidays."
URL: https://api-docs.deepseek.com/quick_start/pricing
Action: Point existing off-peak scheduling machinery (ZCODE_REPO_STEAL_MAP_20260924.md:128) at those UTC windows, and correct kv_cache_compaction.md:6: pro hit/miss is now 30x (was recorded 120x), flash stays 50x — re-rank lanes toward deepseek-flash ($0.003/1M off-peak cache-hit).

**14. Ariadne's claim-tuple store detects contradictions in code before any LLM verdict.** [lane: ariadne, owed]
Quote: "Three-layer: algorithmic claim comparison -> LLM assessment -> manual"
URL: https://raw.githubusercontent.com/cgarryZA/Ariadne/main/README.md
Action: Extend the falsifier-ledger schema with falsifiable (metric/value/dataset/conditions) fields so the SUPPORT/OPPOSE/DISPUTED fold starts with a code-level comparison pass (cf. ENHANCEMENT_STACK_20260920.md:16).

**15. Rug-pull tool-definition drift is a live vector with zero estate prior art.** [lane: a2a-mcp-security, new]
Quote: "a malicious server can change the tool description after the client has already approved it"
URL: https://invariantlabs.ai/blog/mcp-security-notification
Action: Pin every MCP tool's name+description+schema hash into the append-only hash chain at first connect; diff on every reconnect and alarm on drift before the drifted tool is callable (corroborated by the postmark-mcp npm backdoor).

## 4. DISPUTED TIER — six pairs, ruled honestly, never averaged

**Pair 1 — Multi-agent is the pattern vs 41–86.7% failure rates.**
Side A (lane anthropic-multiagent): "multi-agent systems use about 15× more tokens than chats. For economic viability, multi-agent systems require tasks where the value of the task is high enough to pay for the increased performance." (https://www.anthropic.com/engineering/multi-agent-research-system)
Side B (lane mast-taxonomy): "Our empirical analysis reveals 41% to 86.7% failure rate on 7 state-of-the-art (SOTA) open-source MAS detailed in Figure 5" (https://arxiv.org/html/2503.13657)
**Ruling:** Both hold under stated conditions. Anthropic's claim is itself conditioned — multi-agent pays only where task value clears the token premium — so it is a deployment criterion, not a promise that swarms work. MAST measures failure incidence in unhardened 2025-era open-source stacks; its own Insight 3 (+15.6% from task-objective verification) says the failure rate is addressable. They answer different questions (when to deploy vs how often naive stacks fail). Do not merge into "multi-agent sometimes works."

**Pair 2 — Anthropic 80% variance vs Brown <10% credit.**
Side A (lane verifier-scaling): "We found that token usage by itself explains 80% of the variance, with the number of tool calls and the model choice as the two other explanatory factors." (https://www.anthropic.com/engineering/built-multi-agent-research-system)
Side B (lane verifier-scaling): "The effort to solve a Millennium Prize Problem, this was not due to multi-agent. I wouldn't even attribute 10% of the credit to multi-agent. The reality is that OpenAI has trained a very powerful model." (https://www.dwarkesh.com/p/noam-brown)
**Ruling:** Both hold; the conditions differ and do not intersect. Brown makes an architecture-attribution claim at roughly fixed compute: what deserves credit for the capability. Anthropic makes a compute-variance claim: once parallel spend is unlocked (~15x tokens), spend governs quality variance. Read together: the base model governs the win; spend governs the variance around it. The lane's own verifier reached the same ruling (verifier-scaling#2: "No real contradiction: Brown's <10% is an architecture-attribution claim at roughly fixed compute, Anthropic's 80% is a compute-variance claim"). Anthropic's "this finding validates our architecture" framing is the filed overclaim, not the numbers.

**Pair 3 — Writes stay single-threaded vs test-time communication compounds.**
Side A (lane write-delegation): "read-only tools run in parallel via a thread pool (up to five concurrent calls), while write tools run sequentially" (https://arxiv.org/html/2603.05344v3); side A corroborated by Cognition: "setups where multiple agents contribute intelligence to a task while writes stay single-threaded" (https://cognition.com/blog/multi-agents-working).
Side B (lane test-time-parallel): "a team of $k$ communicating agents, team@$k$, matches the success rate of $4k$ independent agents" (https://arxiv.org/abs/2609.21032)
**Ruling:** Both hold because they govern different phases. Serial writes govern production execution state (race prevention, blast radius). Team communication governs test-time discovery, and only under the paper's own conditions: communication wins "under sufficient compute and clear feedback"; "Independent agents may outperform communication when compute is limited or when a clear measure of progress is absent" — which is exactly the estate's fan-out-plus-gate. The estate can run both: communicating research lanes feeding one designated writer.

**Pair 4 — Cheap beats frontier vs cheap can't judge its own limits.**
Side A (lane langchain-blog-60d): "Jev was also the fastest and cheapest. It averaged 0.44s and $0.00035/call ($0.34 total vs. $28.17 for Claude)." (https://www.langchain.com/blog/jev-agent-evals-langsmith)
Side B (lane orchestrator-war-stories): "We should be upfront: SWE 1.5 was not good enough at being the primary model for this setup to really work." (https://cognition.com/blog/multi-agents-working)
**Ruling:** Both hold with a clean boundary condition. Cheap/typed models win where the decision is local and externally verifiable — judging, classification, extraction (Jev; Perplexity's fast preset; Alibaba's deterministic hybrid at 1/9 tokens). Cheap primaries fail where the task is meta-judgment: knowing when to escalate, what to ask, whether data is stale (Cognition's cost-optimized delegation; AgentCheck's staleness results). Law: keep typed verdicts cheap; keep escalation and limit-detection on a tier that can see its own limits.

**Pair 5 — Human citation lists are weak ground truth vs bibliography expansion wins.** (same paper, real tension)
Side A (lane retrieval-agents): "human references score >= 60 in 51.4% of cases, while Qwen3 and Debate+Qwen reach 86.0% and 87.8%." (https://arxiv.org/html/2605.29234v1)
Side B (same lane): "raising recall on RollingEval-Jun25 (a 250-paper literature-search benchmark) from below 20% to above 80%." (https://arxiv.org/abs/2605.29234)
**Ruling:** Both hold; the roles differ. Citations are poor verdicts — biased toward direct collaborators 2.5x, judged ≥60 barely half the time — so never score against them as truth. They are good substrate: BFS along them multiplies recall because the reference graph is a high-precision candidate generator. Use citation lists to expand; never to grade.

**Pair 6 — Verification steps pay +15.6% vs verification pays ~nothing near ceiling.**
Side A (lane mast-taxonomy): "Multi-Level Verification is Needed. Current verifier implementations are often insufficient; sole reliance on final-stage, low-level checks is inadequate." (+15.6% task success adding a task-objective check to ChatDev)
Side B (lane kci-rubric): "although the effect varied by model and condition. These results suggest that checklist-based refinement can help mitigate target omission and improve ORS under certain conditions." (+1.32/+2.58pp from 93.30%/95.19% baselines, hedged, no significance test) (https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART003351606)
**Ruling:** Both hold; verification ROI scales inversely with baseline proximity. MAST's gain lands on a ~30–40%-success stack; KCI's lands at ~94% where headroom is ~6pp. Condition: spend semantic-check budget where pass rates are mid-range; near ceiling, expect single-digit-pp returns and demand a pre-registered falsifier before adopting (KCI's own hedge says as much).

## 5. NEGATIVE RESULTS (named plainly)

**Dead source (lane ok=false): 1.**
- **skywork-guide** — the cited "Ultimate Guide to AI Agents for Research" does not exist. Skywork's own API returns `{"code":100101,"message":"Data not exist"}`; full enumeration of 710 blog + 75 guide posts (POST api.skywork.ai/nova/seo_article/list, live this session per lane record) and Wayback CDX (3,000 URLs) have no match. No secondary substituted; the lane's single row is the negative result itself.

**Fabricated or nonexistent claims caught:**
- "ContraGen" (lane contradiction-synthesis, row unconfirmed): the name has 0 occurrences in the source — the paper is **LegalWiz**; the alleged quote also silently dropped "and potentially risky". Substance (merge-into-output failure; retrieval-verifiable/resistant tiering) is genuinely present; the attribution is not.
- "The Crovia Seal" IETF draft (lane state-artifact-formats): verified nonexistent; converted to a negative row.
- "OpenAI shutting down Agent Builder/Evals Nov 30, 2026" (lane openai-agents-latest): traced to progressiverobot.com, a 2022-template IT-consulting site with no such article.

**Verifier unconfirmations (claims not supported as stated):**
- **apex-agents** (Pass@1/Pass@4/Pass^4, "GPT-6 Astra 56.3%"): the leaderboard page defines only Mean Score and Pass@1; "Pass@4"/"Pass^4" have 0 occurrences; the lone "56.3" is a task rubric figure.
- **langgraph-patterns** (retry-exhaustion write-clearing): the source clears writes from each failed attempt *before* the retry decision, not "on retry exhaustion"; "never contains a half-completed node attempt" appears nowhere.
- **persistent-coding-agents** (both high rows): "in five months" and "Search Infrastructure team" appear nowhere in the Photon post; latency figures are unhedged in the row vs the source's "roughly". The one-sentence persistent-agents mention is real; the architecture gap finding stands, the timeline/team framing does not.
- **openai-agents-latest** (Agents SDK publishedTime): page carries no publish date; Wayback CDX shows the identical article from 2026-04-15 with no September snapshot — the claimed 2026-09-16T13:00Z date is contradicted.
- **perplexity-lab** (fast-preset $6.209 vs $611.00): unit error of 1000x — the page's own renderer divides by 1000 ($0.006209 vs $0.6110 per request); the ~98.98% discount ratio survives, the dollar figures do not.
- **supersonic-x** ("Jev does not resolve"): false — Jev is TypeSafe AI's decision-classification model (and LangChain benchmarked it); the 5x claim still ships zero benchmark/dataset links, so the overcall stands but the "unfalsifiable baseline" wording is wrong.
- **x-frontier-today** (DSEWiki row): the DSEWiki facts (~18,000 posts, 3,700+ agent names, 98.5% Azure IPs) verified; the "Midas Project led X discourse" component is absent from the cited source and unconfirmed independently.

**Source-side overcalls filed we-have-better (discount, never canon):** Anthropic's +90.2% headline (internal eval, no published baseline, same-family judge) — anthropic-multiagent#0; Parallel's core ranking claim asserted with no ablation (grep-verified 0 hits) — parallel-ai#2; Splunk's grounding judge sold on AUROC 0.78 — splunk-deep-research#4; WANDR's vendor ranking (shared fetch backend, single run per system) — wandr-benchmark#4; DeepResearchEco's linguistic-proxy "quality" scores and abstract-vs-body overclaim — deepresearcheco#3/#4; Tool Forge's abstract-vs-body number drift (0.901/99.2% vs 0.908/99.49%) and mismatched citations — tool-forge#4; KCI's hedged ~1–3pp deltas — kci-rubric#3; DeepSeek's own pages contradicting V4-Pro's post-Sept-14 routing — deepseek-agents#4; "68% at flat quality" actually carries a 0.24pt relevance drop and ~3pp availability drop — swarm-economics#2.

**Could not verify (not filled with guesses):** Factory.ai blog unreachable after 5 attempts (orchestrator-war-stories); Meta Spark 1.3 SSO-walled (meta-fair-agents); Nous Portal tier pricing Vercel-blocked; Psyche network has no live primary (nous-latest); X search walled — 404/login (x-frontier-today); SemIf 93.3% unverifiable (JS placeholder); kev parameter sizes conflict across secondaries; Needle scores locked in an SVG; APEX judge-FNR and trajectory-scan details from rendered pages, not raw HTML; W4 run used n=20 tails vs the preregistered ≥50; ADK deploy targets (Cloud Run/GKE) not actionable on Windows-family estate boxes.

## 6. GO LIST — top 10 actions, one seat, one sitting each

1. Grep every lane config for Sonar chat-completions endpoints and remap survivors to the Search API or Agent API before the 2026-09-27 sunset (perplexity-lab).
2. File the W4 FAILED verdict into the falsifier ledger and add a verdict field to the run-summary schema so no summary ships unevaluated again (negative-results-ledgers, XScientist's fails-closed auditor as the gate pattern — https://arxiv.org/html/2607.12301v2).
3. Run a 47%-style verbatim audit: sample evidence_quote strings from judge outputs in watch/inbox, byte-grep each against its cited file, publish the hit-rate in the hash-chained record (citation-binding-tools).
4. Compile subagent tool schemas at fan-out time with write tools stripped, replacing the runtime veto with schema-level omission (write-delegation, orchestrator-war-stories).
5. Run `hermes proxy start`, point one workflow-engine lane at http://127.0.0.1:8645/v1, and pin `nous.anthropic_wire: chat` for fan-outs (nous-latest).
6. Encode one research eval as a claim(n)→field(m)→url(k) hierarchy near WANDR's medians and score it with soft/hard F1 plus re-fetch grading (wandr-benchmark, wide-deep-search-agents).
7. Extend tools/freshness_check.py into per-tool-result freshness receipts (observed-at + source hash) so stale values fail the receipts gate (agentcheck).
8. Wire Anthropic's three effort tiers verbatim into lane effort budgets (1 lane/3-10 calls; 2-4 lanes/10-15 calls; >10 lanes complex) with the value-per-token admission gate (anthropic-multiagent).
9. Schedule all DeepSeek burns outside 01:00-04:00/06:00-10:00 UTC Mon-Fri and correct the stored pro cache ratio 120x→30x (deepseek-agents).
10. Pin every MCP tool's name+description+schema hash into the append-only chain at first connect and alarm on reconnect drift (a2a-mcp-security).

---
*Fold method: all 50 lane JSONs read this session (`python json.load` over `mickey17_v2/lanes/*.json`, both bare-list and `rows`-wrapped shapes); scoreboard counts computed programmatically (246 rows: new 41 / owed 61 / confirms-ours 96 / we-have-better 48); quotes in Sections 3–4 copied verbatim from the lane row fields; verifier verdicts as carried in the fold ask's lane summaries. No content invented; every unverifiable item is listed in Section 5 rather than guessed.*
