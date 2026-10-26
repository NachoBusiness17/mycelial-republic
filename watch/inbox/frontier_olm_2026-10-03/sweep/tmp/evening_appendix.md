
---

# SWEEP: swarm-orchestration via x, EVENING PASS (2026-10-03, second same-day door run)

source-fetched: 2026-10-03. Seat: sweep-swarm-orchestration-x (evening rerun actor). This pass
runs BELOW the morning seat's record above, which is left verbatim (open-append, no rewrite).
Every claim below cites a page fetched or command run this evening. No em or en dashes in this
seat's own prose; quotes are verbatim from the fetched pages.

## Door status (honest, this evening)

- WebSearch (z.ai web_search_prime backend): site:x.com queries half return zero (x.com is
  poorly crawled), half return results with every URL truncated to bare https://x.com (same
  truncation the morning seat hit), and the backend 1302-stormed repeatedly live: raw output
  "MCP error -429: {\"error\":{\"code\":\"1302\",\"message\":\"Rate limit reached for requests\"}}"
  observed on at least four queries this evening (two tool timeouts, two in-band 1302 strings),
  plus sleeps of 30-60s between queries to keep the door alive. This is the estate's own
  rolling-throughput law (AGENTS.md fan-out width law) re-observed from inside the tooling.
- fxtwitter door (api.fxtwitter.com/<user>/status/<id>): 10/10 resolutions succeeded via curl,
  zero failures, JSON with full text, author, likes, views, created_at.
- Full status IDs surfaced this evening: TheZvi/status/2086547497145532522,
  walden_yan/article/2047054401341370639, emollick/status/1998459579697381694,
  mweinbach/status/2039392782167482662, levie/status/2040528801386361128,
  _avichawla/status/2025095663122616755, HarperSCarroll/status/2064816260844511266,
  lennysan/status/2058914803360600238, alex_prompter/status/2003051248820613174,
  rohanpaul_ai/status/1977207609104196018. ALL TEN resolve to posts outside the 30-day window
  (Dec 2025 through Aug 2026 by their own created_at fields; TheZvi = Sun Aug 09 2026 20:17:44Z,
  the most recent). The X index is serving this topic's older viral layer, not the last 30 days.
- Consequence: the strongest in-window finds this evening came from non-X URLs that the X-door
  searches surfaced. That is within the recipe's fallback (bank what the door gives, say so);
  it is not a claim that X itself was read for those items.

## Pass 1: candidate register (36 considered; window 2026-09-03..2026-10-03 unless noted)

| # | Candidate | Where seen | Date | Disposition |
|---|---|---|---|---|
| 1 | Kilo Swarm results post (39 pct cost cut A/B) | blog.kilo.ai/p/kilo-swarm-a-39-cost-cut-on-the-task | 2026-09-23 | DEEP READ, banked item 1 |
| 2 | Kilo Swarm feature post (board_post/board_read mechanics) | blog.kilo.ai/p/swarm | 2026-09-14 | DEEP READ, banked item 2 |
| 3 | Parallel AI Coding Agents: Handle 429 Rate Limits | parallelcode.app/blog/parallel-ai-agent-rate-limits/ | 2026-09-27 | DEEP READ, banked item 3 |
| 4 | Consensus Protocols for Multi-Agent Decisions | tianpan.co/blog/2026/04/12/consensus-protocols-multi-agent-decisions-when-agents-disagree | 2026-04-12 (out of window, kept for RQ5 strength) | DEEP READ, banked item 4 |
| 5 | Talk Isn't Always Cheap (primary behind item 4) | arxiv.org/abs/2509.05396 | 2025-09-05 | ABSTRACT FETCHED, banked item 5 |
| 6 | 7 AI Agent Swarm Coordination Patterns + Failure Modes | kunalganglani.com/blog/ai-agent-swarm-coordination-patterns | 2026-09-19 | DEEP READ, banked item 6 |
| 7 | TheZvi multi-agent-risks post | x.com/TheZvi/status/2086547497145532522 | 2026-08-09 (out) | RESOLVED via fxtwitter, off-topic (OpenAI HF incident timeline), not banked |
| 8 | walden_yan "Multi-Agents: What's Actually Working" | x.com/walden_yan/article/2047054401341370639 | 2026-04-22 (out) | RESOLVED; fxtwitter returns empty text for /article/ URLs, body unread, not banked |
| 9-15 | emollick, mweinbach, levie, _avichawla, HarperSCarroll, lennysan, alex_prompter, rohanpaul_ai status posts | x.com (8 resolved via fxtwitter) | Dec 2025-Jun 2026 (all out) | RESOLVED, out of window, not banked |
| 16 | "THIS IS THE BEST AI AUTOMATION STACK" post citing a 2026 equal-budget study: single agents match multi-agent on reasoning at held-constant tokens | site:x.com search snippet, URL truncated to bare x.com | unknown | UNRESOLVABLE; snippet only; claim UNVERIFIED, no primary found; do not treat as evidence |
| 17 | Stanford AI Index coordination-quality claim ($100k/month AI post) | bare x.com snippet | unknown | UNRESOLVABLE snippet |
| 18 | "How to Build AI Agent Swarms (Complete Guide)" 300-parallel-agents claim | bare x.com snippet | 2026-06-04 (out) | UNRESOLVABLE, number unverified |
| 19 | Kimi Help Center Agent Swarm: up to 300 sub-agents, horizontal scaling, no predefined roles | kimi help center via search snippet | unknown | NOT FETCHED |
| 20 | SwarmBench: Can LLMs Act as Agent Swarms | arxiv.org via search snippet | 2026-08-31 | NOT FETCHED (window edge); snippet only |
| 21 | Evaluating Multi-Agent Orchestration Failure Modes (tool-vs-reasoning failure injection) | arxiv.org via search snippet | 2026-08-05 | NOT FETCHED (window edge) |
| 22 | TRIAGE: Severity-Ranked Multi-Agent Failure Attribution | openreview.net via search snippet | unknown | NOT FETCHED |
| 23 | Error Recovery in Multi-Agent Systems (circuit breakers) | blog.naitive.cloud snippet | unknown | NOT FETCHED |
| 24 | When AI Agents Collide (conflicting-instruction bounce) | cogentinfo.com snippet | unknown | NOT FETCHED |
| 25 | Trace-Driven Debugging for AI Agent Failures | zylos.ai snippet | unknown | NOT FETCHED |
| 26 | More Targets of the OpenAI Agent Swarm | fi-le.net (Sep 4 2026 per search) | 2026-09-04 | SITE WALKED (root, links, feed.xml, safety-blogs, hn, air, slug probes); post not reachable from site nav; URL UNRESOLVED, body unread |
| 27 | Vanderbilt link-shortener swarm incident (170+ short links) | Tennessean/Fortune/Register/X Sep 9-10 2026 via search snippets | 2026-09-09 | snippet-level only; incident family already estate-known via burns (OpenAI swarm incidents) |
| 28 | anthropics/claude-code issue 2387 usage-limit | github.com snippet | 2025-06 (out) | NOT FETCHED |
| 29 | BUG: Rate limits blocking multi-agent Claude Code | github issue via search snippet | unknown | NOT FETCHED |
| 30 | HubSpot docs: parallel agents collision warning | developers.hubspot.com snippet | 2026-09-09 | NOT FETCHED |
| 31 | How 7 Kilo Code Engineers Run Up to 20 Parallel Agents | blog.kilo.ai (slug not in archive index; 404 on guess) | unknown | NOT RESOLVED; the two Kilo swarm posts above are the same venue's better evidence |
| 32 | kunalganglani ai-agent-kill-switch-spend-limits | kunalganglani.com (found in blog index) | unknown | NOT FETCHED (adjacent to item 3's subject) |
| 33 | kunalganglani ai-coding-agent-harness-overhead-measurement | kunalganglani.com blog index | unknown | NOT FETCHED (RQ1-adjacent, owed) |
| 34 | Parallel Code homepage (worktree-per-agent workspace, MIT) | parallelcode.app | live | FETCHED while resolving item 3 |
| 35 | tianpan multi-model-consensus-architecture-llm-sign-off | tianpan.co sitemap | unknown | NOT FETCHED |
| 36 | persuasion-driven adversarial influence in MAS (adversary lowers accuracy 10-40 pct while raising wrong-consensus) | PMC via search snippet | unknown | NOT FETCHED |

## Pass 2: deep reads (6 fetched and read end to end this evening)

Items 1-6 in the register were each fetched by me this evening (curl to disk, then read in
segments covering the full body: item 1 full post incl. comments lead, item 2 full post, item 3
full article in three overlapping segments, item 4 main body plus patterns/failure-modes
sections, item 5 the arXiv abstract page, item 6 the full patterns table and termination
section). Local copies kept at sweep/tmp/x_evening/ (pc_429.html, kilo_swarm.html,
kilo_swarm_orig.html, kg_swarm.html, tianpan_consensus.html, arxiv_2509.05396.html, plus ten
fxtwitter JSONs). Quotes in the SweepResult are verbatim from these files.

## Findings against the research questions

### RQ1 (PANDA fault-tolerant mesh vs lane_runner retry asymmetry)

- External corroboration of the asymmetry shape: Gemini CLI documents general.maxAttempts with
  a default of 10 for requests to its main chat model, and the article's warning that lowering
  it surfaces persistent failures sooner while a wrapper's extra retry loop "can multiply
  requests" is the same retry-multiplication hazard the estate's maxAttempts-0-on-children rule
  guards (item 3). No public source found that differentiates retry policy by DISPATCH CLASS
  the way lane_runner does (workflow children 0 vs Task agents 11); the estate's split is ahead
  of the public record on that axis.
- Mesh-level resilience language found is topology advice, not retry policy: item 6's pattern
  table gives per-topology stop conditions and mitigations (supervisor: citations + verifier;
  mesh: add a reducer/judge). Nothing found ports PANDA-style checkpoint-inheritance claims
  beyond what the register already confirmed 2026-10-03 morning; do not re-mine.

### RQ2 (queue policy vs quota-wall lane deaths, code 1005)

- Item 3 is the strongest external anti-quota-wall playbook found: (a) a spend/allowance cap
  has NO retry-after and is identified by an error code (Claude enforced_spend_limit_reached),
  so retry pacing is the wrong medicine for that class, exactly the 1005-wall shape; (b) the
  salvage rule is preserve-and-resume: "preserve its current diff and prompt so it can resume
  after the applicable limit resets"; (c) concurrency is a budget per shared limiter, not one
  machine-wide setting; (d) "independent agents cannot coordinate their retries by
  themselves", which is the argument for the switchboard/effect-broker owning pacing.
- DEALS expertise-aware queuing (register r4) and item 3 agree on the preventive shape: the
  queue must know WHICH limiter is exhausted and resume from preserved state, not re-run blind.
  The owed limit-kill census over queue/lanes/*/trail.jsonl (DIGEST $0 probe 1) remains the
  estate-side half; this sweep adds the external vocabulary for its verdict classes.

### RQ3 (limit-retry census: 438 redone vs 8 resumed)

- No external source found that counts redo-vs-resume for subagents; the estate's census is
  unreplicated externally (OWED externally, and the estate-side probe is still owed too).
- Closest external support for resume-over-redo: item 3's preserve-and-resume rule, and item 4
  Pattern 5 "Checkpoint-and-rollback coordination ... roll back to the last known-good state
  rather than trying to patch a corrupted shared context".

### RQ4 (MAS collective-failure diagnosis for rib_bus)

- Item 2's design stance is directly portable: board messages are coordination data, not
  control signals; HOLD/VETO are advisory and do not pause a running agent; only the owning
  top-level session can reset the board. For rib_bus this is a concrete answer to "diagnose at
  the mesh without re-running blind": the bus carries an advisory failure picture while control
  stays with owners.
- Item 6's blackboard row names the mesh disease (shared memory poisoning) and its mitigation
  (write-once logs + append-only memory; scoped write permissions), which the rib_bus
  append-only doctrine already practices; the external novelty is pairing it with a
  no-state-change-for-2-rounds stop condition.
- Item 4's Pattern 4 (structured disagreement escalation: strong/weak/ambiguous disagreement
  routed to human review / confidence-weighted merge / evidence gathering) is a
  diagnose-at-the-mesh decision rule the estate can steal for the swarm_surface organ.

### RQ5 (cheap-seat flock vs single seat under the consensus-illusion verdict)

- Item 4 gives the sharpest external numbers: 23.9 pct of initially-disputed questions converge
  to unanimous WRONG consensus by round three; correct-to-incorrect flips outnumber the reverse
  in every tested configuration; protocol-task asymmetry (independent generation + voting
  better for reasoning tasks by 13.2 pct, iterative consensus better for knowledge tasks by
  2.8 pct; consensus costs ~5x single-agent tokens, voting ~10x); BFT arithmetic (N >= 3f+1, so
  a 3-agent flock tolerates zero Byzantine agents); duplication rates 72-86 pct in major
  frameworks. This MOVES nothing off the estate's valid-uses list for the flock (open-ended
  divergent sampling etc., lens/laws.md:43) but sharpens the same verdict: unanimity on
  grounded tasks is an anti-signal, and the fix is protocol-per-task-class plus capped rounds,
  not more agents. Its primary is item 5 (arXiv 2509.05396, abstract verified this evening).
- Item 1 is the first external A/B found where multi-agent coordination was measured per task
  class with an honest null: the board pays exactly on decomposable, expensive, multi-subagent
  tasks and is inconclusive elsewhere, and the authors' next step is a task-shape gate. That is
  the estate's routing-classes law (RIB_ROUTING_CLASSES_20261002) re-derived independently for
  swarm boards.

## Overlap ledger (greps run this evening)

- catalog/catalog.jsonl (full 261,013,216-byte file read once by python): "Kilo Swarm" 0,
  "2509.05396" 0, "parallelcode" 0, "enforced_spend_limit_reached" 0, "Consensus Protocols for
  Multi-Agent" 0, "7 AI Agent Swarm" 0, "Condorcet" 0, "Handle 429 Rate Limits" 0,
  "rs-archive-clone" 0, "Supervisor over-trusts" 0, "general.maxAttempts" 0, "unanimous wrong"
  0, "board_post" 38 (FALSE POSITIVES: sample shows "fix_blackboard_post_provenance.json" and
  "test_dashboard_post_normalizes0" substring hits, not the Kilo tool),
  "multi-agent debate" 2 (REAL prior: catalog rows "Remember and Reweight: Enhancing Multi-Agent
  Debate..." and "...Fabricated Consensus: The Active Provenance Gate for Multi-Agent Debate
  Synthesis", age_days 0, landed today by this run's lanes).
- memory/ walk (1,291 files, 30.4MB; subdirs rib, research_packs, burns, improve, lenses plus
  attention.md, policy.json, warm_state.json, knowledge_graph.json; corpus, agent_sessions,
  trajectory, runs, mycelium EXCLUDED for size, stated as scan scope): all item phrases 0
  except "multi-agent debate" 1 (research_packs/20260807T_hermes-agent-frameworks-comparative-
  research.md, concept prior) and "retry-after" 3 (research_packs fanout router pair +
  burns/LEDGER.jsonl, practiced concept).
- Verdict: items 1, 2, 3, 4, 6 are NEW as primaries; item 5 is NEW as a primary but its concept
  family (fabricated consensus) was banked estate-side TODAY, so it lands as corroborating
  evidence for the consensus-illusion verdict, not as a new estate concern.

## Gaps, not-run, honest

- The 30-day X-post layer is nearly empty through this door: every fxtwitter-resolvable status
  surfaced was out of window. In-window X coverage is limited to unresolvable bare-x.com
  snippets (register 16-18, 27). No X thread was deep-read this evening because none in window
  could be resolved; the 6 deep reads are non-X URLs surfaced by the X-door searches.
- fi-le.net "More Targets of the OpenAI Agent Swarm" (register 26) unresolved after site walk;
  body unread.
- The equal-budget study claim (register 16) has NO primary; UNVERIFIED, not banked as evidence.
- SwarmBench, orchestration-failure-modes arXiv, TRIAGE (register 20-22) are window-edge
  snippets not fetched; they are leads for a next pass, not findings.
- Runs/commands: all curl fetches this evening exited 0 (echoed $? at each step); the WebSearch
  tool 1302-stormed live at least four times (quoted above); the first two overlap grep loops
  were killed for slowness and replaced by the single-pass python scans whose outputs are
  quoted above; a third python scan over all of memory/ timed out at 306s and was narrowed to
  the named subdirs.
