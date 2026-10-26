# SWEEP: swarm-orchestration via hn (frontier_olm_2026-10-06)

source-fetched: 2026-10-06

Seat: sweep gopher, area "swarm-orchestration via hn", door = Hacker News (Algolia API + item pages).
Laws held: no fabrication, no em/en dashes, every claim cites what was fetched or grepped this sitting.

## Method (what was actually run)

Pass 1, broad: 7 Algolia queries against hn.algolia.com/api/v1 (search_by_date with
numericFilters=created_at_i>1788652800 plus relevance search), queries: "multi-agent",
"Claude Code agents", "multi-agent orchestration", "knowledge graph", "rate limit agents",
"concurrent writes file", "plan mode coding agent", "subagents", "git worktree",
"retry backoff API". Unique story candidates considered from the last 30 days: 60+ lines
returned; 30+ distinct candidates screened, including: Offrun (49942434, 78/66), Pizza Bot
(49713894, 61/37), Riftri CoW worktrees (49807251), OctoShell worktree isolation (49892358),
Worktrunk (49924905), Git Worktree Gotchas (49728190), Rashomon execution record (49968377),
Agent-blackbox flight recorder (49947646), Relay request pacing (49800187), Magnitude
(49911995, 194/99), Extraordinary Multi-Agent Delusions (49911816), Coordination Backbone
(49658727), durable subagents (49659415), Scalable subagents (49845032), Swarm message board
(49901831), Local Software Factory (49818439), Wb-flow markdown state (49830875), cellaflow
(49923523), Omnesis (49877752), Novgraph (49672213), ctx (49727859), Type.com (49626148),
Magit worktrees (49606281, 147/52). Pass 2, deep: 10 HN item pages fetched end to end
(news.ycombinator.com/item?id=49831324, 49789356, 49924268, 49877499, 49847249, 49934037,
49684835, 49715388, 49923523, 49888734) plus the linked polylane.com article behind 49715388
(the HN page carried no body and zero comments, so the article is the read). Quotes below came
through the WebFetch door summarization pass, kept under 40 words to limit paraphrase risk;
none were byte-verified against raw HTML this sitting, hence confidence < 0.85 across the board.
No door 403'd; Algolia, news.ycombinator.com, and polylane.com all answered on the first try.

## Estate mapping (why each find lands where it does)

Grounded in the ask plus lens files read this sitting:
- Q1 write seams: R3 named the multi-seat tree-sweep defect class and the stash incident
  (3 stashes sitting) and fold_gate is the one serializer so far
  (watch/inbox/frontier_olm_2026-10-06/lens/burns.md:127-129, 183-186); LIVE_REPORT mtime
  inversion is the row-0a wound (AGENTS.md load-order row 0a).
- Q2 mesh/frontier boundary: question class explains 36.3 pct of variance, family 3.6 pct;
  the mesh reads, the frontier simulates; battery is 17 questions at one sitting
  (lens/laws.md:39-40, 87).
- Q3 graph wiring: knots 400, doctrine 217, steal 140 nodes all degree 0; 285 of 300 case
  laws sit on module:skills_pack.py; mcp_stateless and webmcp families zero edges
  (lens/graph.md:25-29).
- Q4 subagent rate-limit resets: the ClaudeDevs day-5 find is banked
  (lens/burns.md:79); envelope laws live in AGENTS.md fan-out width law.
- Q5 planning-mode gate: n_planning_mode at degree 0, cold-seam tesuji orders the build
  (lens/laws.md:95).

## Banked finds (8, strongest first)

1. Resume Claude Code subagents killed by a usage limit (HN 49831324, 2026-09-24,
   github.com/error0702/agent-limit-retry). Q4 direct hit with numbers: "449 subagents cut
   off by limits, 8 resumed by id (all 8 before the reset, so they died again), 438 redone."
   and "The exact reset time is in the transcript as quotaLimits.resetsAt". That is the
   provider-side reset surface our envelope laws never measured: resume-before-reset dies
   again, so the dispatch shape law needs a reset-clock term, not just rolling throughput.
   Mechanism is 4 hooks plus a status-line tap, portable to our lane runners.
   Overlap: rg over catalog/catalog.jsonl and memory/ found zero hits for "agent-limit-retry";
   the day-5 ClaudeDevs find (burns.md:79) is a different source, no URL collision.

2. Foremerge (HN 49789356, 2026-09-21, github.com/naw103/foremerge, 45 pts / 20 comments).
   Q1 contract candidate: "Claims are advisory leases, not locks so two agents can still hold
   the same scope without deadlock." Author claims "tested this up to 98 parallel agents all
   working on the same repo with zero conflicts". The general lock/receipt contract our
   tree-sweep class needs is plausibly: advisory leases + conflict sweep + receipts, with the
   hard mutex (fold_gate) reserved for cross-run folds only. Their advisory-lease stance is
   the counterweight to our serializer instinct; both belong in the same design fight.
   Overlap: zero hits for "Foremerge" in catalog/memory.

3. Sub-agents are just wrong (HN 49715388, 2026-09-15, polylane.com blog, read end to end).
   Q1+Q2: they deleted the orchestrator/sub-agent split and shipped single-agent issue-to-PR;
   "Per-agent evaluations pass while the system fails, because the failures live between the
   agents." Median time-to-PR 2.2 h to 35 min per the fetched text. Direct evidence that the
   seam, not the seat, is the defect surface, which is the same verdict our relay chain and
   R3 tree-sweep findings point at from inside. The mesh/frontier question applies: their fix
   is the degenerate one-seat mesh; our counter-data is the 50-wide envelope running clean.
   Overlap: zero hits for "sub-agents are just wrong" in catalog/memory.

4. Ask HN: Is anybody producing good code with coding agents? (HN 49934037, 2026-10-02,
   29 pts / 45 comments). Q2 field census: the success reports are all evidence-readable
   small-chunk work ("I have it do small chunks I can quickly review", leros) and the failure
   report is runtime-simulation work: "Coding agents are RL'd to get the thing done, they'd
   rather get to 95%, not realize there's some fundamental architectural flaw, and hack the
   last 5%" (sigbottle). An independent 45-comment replication of the mesh-reads /
   frontier-simulates split (laws.md:40), on questions we did not write. Candidate battery
   extension questions for widening past 17.
   Overlap: zero hits for the title phrase in catalog/memory.

5. Ask HN: Has anyone built a leaderless multi-agent system? (HN 49847249, 2026-09-25).
   Q2+Q1: author runs an AI SRE as four concurrent agents on one incident and asks for
   leaderless coordination through shared state: "Multiple agents working on long lived
   records. Agents could be owned by the same or different parties." Multi-party writes to
   long-lived records is exactly our doctrine.json / registry.json seam shape, with parties
   as the missing axis in our single-operator locks.
   Overlap: zero hits for "leaderless multi-agent" in catalog/memory.

6. Ask HN: What broke when you added the second agent? (HN 49924268, 2026-10-01).
   Q1 corroboration, thin thread (one substantive comment): "the biggest issue I've seen are
   these inconsistencies, mistakes, bad assumptions, or side quests compounding" (verdverm),
   plus the asker's correlated-duplication observation (identical branch names from
   independent agents). Names the collision class we keep hitting: concurrent seats converge
   on the same artifact names, so the serializer must cover naming, not just bytes.
   Overlap: zero hits for the title phrase in catalog/memory.

7. LearnLance (HN 49684835, 2026-09-13, github.com/aeroscissorz/learnlance).
   Q3 wiring lead: "The graph is generated from your coding session." (pip install
   learnlance). The mechanism our three floating layers lack: edges minted at write-time from
   session events, instead of backfilled by a batch job. If knots/doctrine/steal got write-time
   linking on ingest (each stolen item names its target module at bank time), the 757
   degree-0 nodes stop accruing. Thin thread, mechanism unverified beyond the fetch.
   Overlap: zero hits for "learnlance" or "code AI writes" in catalog/memory.

8. Fable Decides, Opus and Sonnet Do the Work (HN 49888734, 2026-09-29,
   practicalsystems.io blog). Q4 dispatch shape: role-split routing under a usage ceiling,
   from the comments: "Your usage is limited, run the token-heavy work through Opus5.5
   subagents" and "It works, lets Fable orchestrate, plan, and verify work." Routes by ROLE
   (decider vs worker), our L18 routes by QUESTION-CLASS; the two axes are orthogonal and
   unmeasured against each other on our battery. One commenter's risk note: "Seems like a
   workaround that Anthropic might easily turn off."
   Overlap: zero hits for "Fable Decides, Opus and Sonnet" in catalog/memory.

## Exclusions and dedup

- HN 49877499 "I turned my team's coding-agent history into a knowledge graph" IS Motif
  (github.com/motif-Labs/motif), already a confirmed day-5 find (lens/burns.md:78). Overlap
  grep: "motif" hits catalog/catalog.jsonl, memory/burns/LEDGER.jsonl,
  memory/rib_bus/standing-wave.json. NOT re-banked.
- HN 49923523 cellaflow: fetched; page carried title only, no readable body or comments.
  Nothing to quote, dropped.
- HN 49715388 was banked only after reading the linked polylane article, not the empty HN page.

## Not done / caveats

- Quotes are WebFetch-door extractions, not raw-byte greps of the fetched HTML; treat as
  high-plausibility verbatim, confidence values reflect that.
- Q5 (planning-mode gate) produced no in-window HN find worth banking: the plan-mode candidates
  surfaced (PlanBridge 48139177, Typed Natural Language 47876350, inplan 48659617) all sit
  outside the 30-day window and were not deep-read this sitting; reported as considered, not read.
