# w3-research-swarm-scale: production swarm scale research · 2026-09-28

**Ask:** Research what is the maximum demonstrated concurrent agent swarm in production (not benchmark). Who runs it, what orchestrator, what failure modes. Compare to our 14-wide machine ceiling. OWED if unverifiable.

## Headline finding

**No vendor publishes a verified maximum-concurrent-LLM-agents figure for a production system.** Production disclosures come in exactly two shapes: (a) per-query fan-out width, verifiable and small, and (b) volume metrics (conversations, rides, PRs) that say nothing about simultaneous agent counts. The fleet-level concurrent agent count of every production LLM swarm I probed this session is **OWED (unverifiable from public sources)**. The only production autonomous-agent fleets with published concurrency are non-LLM: Waymo's robotaxi fleet and military drone swarms.

## Production LLM agent swarms: best evidence

| system | who runs it | orchestrator | demonstrated concurrency | fleet-level concurrency |
|---|---|---|---|---|
| Anthropic Research feature (multi-agent research system) | Anthropic, production since ~2025-06-13 | lead agent + orchestrator-worker subagent spawn | **3-5 subagents typical, >10 for complex queries, 3+ parallel tool calls per subagent** (primary source, fetched this session) | OWED: users/sessions served never published |
| GitHub Copilot coding agent | GitHub/Microsoft, GA | per-task GitHub Actions job | no published figure found this session | OWED |
| Devin | Cognition, enterprise | per-session cloud VM agent | no verified concurrent-session figure found this session | OWED |
| Salesforce Agentforce | Salesforce + customers | platform agent runtime, priced per conversation / Flex Credits | no verified figure; Benioff's "1 billion agents" is a stated goal, not a measured count (weak secondary source) | OWED |
| Sierra (Brett Taylor) | Sierra, CX voice/chat agents | managed per-customer agent platform | no verified figure surfaced in this session's searches | OWED |

Per-query fan-out width (Anthropic's 10+) is the largest LLM swarm concurrency that survives verification today, and it is the same order of magnitude as our own 14-wide lane runs.

## Largest production autonomous-agent fleets (non-LLM calibration)

**Waymo (Alphabet):** 4,000+ robotaxis operating concurrently in production, ~500,000 weekly paid rides (first announced ~March 2026), 220M+ cumulative rider-only miles, 1M weekly rides targeted by year-end 2026, ~20 cities. Source: secondary aggregator table dated 2026-09-04 (finance.biggo.com) surfaced by WebSearch; primary filing OWED. Orchestrator: per-vehicle autonomous driving stack + centralized fleet operations and depot (charging/maintenance) network.

**Waymo failure modes (documented via NHTSA actions and reporting, found via WebSearch this session):**
- Software flaw let vehicles drive into floodwater: recall of nearly 3,800 robotaxis (May 2026 reporting).
- Repeated failure to recognize ramp closures and construction zones, vehicles stuck or erratic: separate recall of nearly 3,900 robotaxis.
- Two vehicles crashed into the same tow-truck pickup; voluntary over-the-air software recall of the fleet.
- Immobilized vehicles blocking traffic, e.g. an Atlanta cul-de-sac jam; NHTSA warnings to robotaxi operators about traffic-blocking failures.
- Pattern: per-agent perception/edge-case failures (flood, construction, occlusion), which a 4,000-strong fleet converts into fleet-wide recall events; OTA update is the recovery path.

**Military drone swarms (found via WebSearch this session; secondary sources):**
- Ukraine is reported (WSJ, Sept 2025, via secondary) as the first country to routinely use AI-controlled drone swarms in combat; Swarmer's Primer/Styx coordinates multi-drone groups autonomously with humans retaining final targeting. Stated goal: one operator controlling dozens to hundreds of drones.
- Auterion: live-fire combat swarm with one operator engaging three targets (2026), plus 50,000 FPV drones with autonomous terminal (Skynode S) guidance delivered to Ukraine.
- Routine overnight waves of 100-150 drones per strike on both sides, though per-swarm autonomous coordination is dozens-scale.
- Demonstrations (not production): China 2025 single-operator 200+ AI drone demo; DARPA/SCO Perdix 103 autonomous micro-drones (2016). Preprogrammed drone light shows exceed 10,000 units but are not autonomous agents.

## LLM swarm failure modes (Anthropic primary source, fetched this session)

From "How we built our multi-agent research system" (anthropic.com/engineering/multi-agent-research-system, published Jun 13 2025):
1. Subagent over-spawning (early: 50 subagents for trivial queries)
2. Endless searching for nonexistent sources
3. Excessive cross-agent updates (subagents distracting each other)
4. Vague delegation and duplicated work across subagents
5. Poor effort calibration (overinvesting in simple queries)
6. Wrong tool selection (web-searching what lives in Slack)
7. Bad tool descriptions sending agents down wrong paths
8. Overly specific initial queries returning few results
9. Poor source-quality judgment (SEO farms over academic PDFs)
10. Opaque "not finding obvious information" failures, diagnosed via full production tracing
11. Sequential search slowness (early serial execution)
12. Synchronous bottleneck: lead agent cannot steer subagents mid-flight, blocks on the slowest subagent
13. Compound state errors cascading; costly full restarts, hence checkpoint/resume and "rainbow deployments"

Economics from the same source: multi-agent uses ~15x chat tokens; agents ~4x; token usage alone explains 80% of performance variance on BrowseComp; multi-agent beat single-agent Opus 4 by 90.2% on their internal research eval; parallelization cut research time up to 90%.

## Our own measured swarm failure modes (in-repo receipts, the comparison baseline)

- **Rate-limit storms:** workflow children carry maxAttempts 0 and die on first 429/1302; a 50-wide workflow dig on the z.ai account 429-storms and crashes tethered sessions; after a burst even 12-wide takes 1302s; the limit is rolling throughput, not width-only (AGENTS.md Clippy fan-out width law; receipts `corpus/steal/TETHERED_LINK_STEAL_20260925.md`, `watch/inbox/gala_20260925/AFTERPARTY_CLOSE_20260926.md`, `watch/inbox/ENVELOPE_50W_HIT_20260926.md`).
- **Concurrent-write corruption:** nav.js landed as a 532-byte truncated duplicate with a SyntaxError from concurrent writes, repaired in Q-028 (commit d90bc8607, session git status snapshot).
- **Sibling-lane tree-state interference:** full-suite test failures attributed to sibling-lane tree state rather than the change under test (Q-008, commit 4706d5a04, session git status snapshot).
- **Count drift across lanes:** never difference two counts taken at different moments (B2-216 census denominator law, AGENTS.md).
- **Width floor unenforced:** a 9-lane run fired against the ladder's own 14-wide day minimum and no gate noticed (watch/inbox/MICKEY17_V2_RUN_SPEC_ADDENDUM.md:52).

## Comparison to our 14-wide machine ceiling

Grounding for our side (read in-repo this session):
- `watch/inbox/SMITH_MAP_KV50_20260922.md:29`: "concurrency ('why skimping?') | 50 requested | machine ceiling = **14 concurrent** | hardware | not caution - physics"
- Same file line 36: the kv50 lift's run was amended max_concurrency 50 -> 14 = box ceiling; the 14 is a single Windows box process-concurrency limit (hardware), not an API limit.
- `watch/inbox/MICKEY17_V2_ENGINE_SPEC_20260924.md:97` and `_v2.1_20260925.md:75`: daily 14-wide burn minimum; standard 50-wide weekly burn, scheduled off-peak.
- AGENTS.md Clippy max-concurrency standing law: 5 concurrent gated workflows at max_concurrency 10 each (50 workflow children) plus hourly burn ran clean for hours; Task agents measured clean at widths 3/6/10/12, width 10 banking 109.4M tok/h.

The comparison, honestly framed:
1. **Same order at the orchestrator tier.** The only verifiable production LLM fan-out width (Anthropic: >10 subagents per query) sits exactly at our 14-wide lane scale. We are not behind the disclosed state of the art; the disclosed state of the art is roughly us.
2. **Fleet multiplication is where production differs.** Anthropic serves Research to every eligible Claude user and Waymo runs 4,000+ vehicles, but neither publishes a same-moment concurrent-agent count, so no apples-to-apples fleet number exists to lose to. Our own measured estate shape is ~50 concurrent workflow children (5 workflows x 10) on one box whose hard process ceiling is 14 per run.
3. **The binding walls match.** Anthropic's documented failure modes (synchronous bottleneck on the slowest subagent, compound state errors, over-spawning) and Waymo's recall classes (per-agent edge-case failure amplified fleet-wide, OTA as recovery) have direct analogs in our receipts: 1302/429 throughput walls, nav.js concurrent-write corruption, sibling-lane tree-state bleed, and the unenforced width floor. Convergent failure modes across three independent estates is the strongest signal in this research.
4. **What would actually beat 14:** distribution across machines plus a queue with retry/backoff, which is what Copilot Actions jobs, Devin VMs, and our own multi-workflow shape all are. The ceiling is per-box physics; the fleet law (max_concurrency 10 x N workflows) is how the estate already routes around it.

## OWED (unverifiable this session)

1. **Maximum concurrent LLM agents in any production system:** OWED. No public verified figure exists as of 2026-09-28 per this session's searches; vendor disclosures are volume-shaped, not concurrency-shaped. The honest answer to "what is the maximum demonstrated concurrent agent swarm in production" for LLM agents is: not publicly knowable; per-query width (Anthropic >10) is the largest verifiable production number.
2. **Devin / Copilot coding agent / Agentforce / Sierra concurrent-session counts:** OWED (searched, not found).
3. **Waymo same-moment concurrent vehicles in service:** OWED (4,000+ is a fleet stock figure from a secondary source, not a verified peak-concurrency number).

## Method and coverage note

Ran this session: repo grep for "14-wide / width 14 / machine ceiling" over watch/ memory/ docs/ corpus/; Read of watch/inbox/SMITH_MAP_KV50_20260922.md; WebFetch of the Anthropic engineering post; 6 WebSearch calls (Anthropic multi-agent, Devin concurrency, Copilot concurrency, Waymo scale, Agentforce/Sierra concurrency, drone swarms, Waymo recalls). Three WebSearch sub-queries returned MCP 1302 rate-limit errors (Devin, Copilot, Agentforce/Sierra probes), so coverage of those vendors is degraded and their OWED status partially reflects that. All in-repo failure-mode citations come from files read this session or the Q-028/Q-008 commit messages carried in this session's git status snapshot. Web tool results are treated as findings per the driving-ladder law, not as done work; the search backend was the fleet's own web_search_prime surface.

## Sources

- https://www.anthropic.com/engineering/multi-agent-research-system (primary, WebFetch, published 2025-06-13)
- https://docs.github.com/copilot/concepts/agents/cloud-agent/about-cloud-agent (WebSearch, no concurrency numbers)
- https://github.com/orgs/community/discussions/159068 (Copilot GA discussion, 180-minute job timeout requests)
- https://finance.biggo.com Waymo city-launch table 2026-09-04 (WebSearch summary, secondary)
- WKYC and related coverage of Waymo floodwater recall ~3,800 robotaxis, 2026-05-12 (WebSearch summary, secondary)
- WSJ-via-secondary on Ukraine routine AI drone swarms, 2025-09; Auterion 2026 live-fire swarm; China 200+ drone demo 2025; DARPA Perdix 103 (WebSearch summaries, secondary)
- Golem Cloud "The Rise of the Agent Runtime" (Agentforce pricing models; Benioff 1B agents goal, WebSearch summary, secondary)

---
_Filed by w3 gopher seat, 2026-09-28. Bank path per ask. OWED items marked; nothing invented to fill them._
