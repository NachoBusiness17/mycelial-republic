# FRONTIER SWEEP: swarm-orchestration via x (2026-10-11, adhoc round 2)

source-fetched: adhoc

Seat: sweep gopher, area "swarm-orchestration via x". This file supersedes the
2026-10-10 doc at this path (archived verbatim beside it as
swarm-orchestration-x_2026-10-10.md, read in full this sitting before the
overwrite). House laws held: ascii only, no em or en dashes, every claim cites
a page fetched or a command run this sitting, quotes verbatim, bank only what
I fetched and read myself.

## Door status (honest, per instrument)

1. WebSearch site:x.com / allowed_domains=["x.com"]: DEGRADED, third
   consecutive recorded run. This sitting: 4 queries (site:x.com
   multi-agent LLM orchestration; site:x.com LLM agent swarm emergent
   behavior; allowed_domains x.com/twitter.com/threadreaderapp; site:x.com
   VeriHarness OR Agensh OR "agent swarm"). Zero in-window x.com status URLs
   surfaced; the engine returned unrelated accounts or non-X pages and itself
   reported it cannot index x.com. One 1302 rate-limit inside the backend.
   Same verdict as the 10-10 and 10-11 daily sweeps.
2. THE WORKING DISCOVERY DOOR this run: the grok CLI headless seat
   (C:\Users\foste\.grok\bin\grok.EXE, "free subscription seat" per
   mag.grok_free status run this sitting), which the driving-ladder rib names
   the DEFAULT instrument for all X work (RIB_DRIVING_LADDER_20260928:78-98,
   no rationing). Two searches (topics: broad multi-agent orchestration;
   consensus/voting failures), latencies 393,968 ms and 143,562 ms, exit 0
   both, raw outputs banked at raw/x_grok/grok_xsearch_broad.txt (22 posts)
   and raw/x_grok/grok_xsearch_consensus.txt (19 posts). Driver:
   _x_grok_search.py (CREATE_NO_WINDOW on the spawn, per the win32 law).
   RULE HELD: grok output is DISCOVERY ONLY. Every banked quote below comes
   from the fxtwitter JSON, the arXiv page, or the blog I fetched myself.
3. fxtwitter door (api.fxtwitter.com/<user>/status/<id>): ALIVE, 32/32
   resolutions returned code 200 with full tweet JSON (no 403s, no login),
   raw JSONs banked as raw/x_grok/_fx_<handle>_<id>.json. Fetcher:
   _x_fx_fetch.py. The 32/32 hit rate is also the grok door's no-hallucination
   receipt: every URL grok returned resolved to a real post with matching
   author and text.
4. HN Algolia (hn.algolia.com/api/v1/search_by_date): ALIVE, one breadth
   probe (query=multi-agent, tags=story, created_at_i>1789084800, 30 hits).
5. WebFetch: used for the paper and blog deep reads below.

## Pass 1 (broad sweep, 67 candidates considered)

- 35 unique in-window X posts from the two grok searches (2026-09-17 through
  2026-10-11), listed with handles in the two raw files. The 32 strongest
  were resolved through fxtwitter (all 32 OK).
- 30 HN stories from the Algolia probe (objectIDs 50043499 back to 49785562,
  2026-09-21 through 2026-10-11), logged as candidates; the strongest
  non-duplicate (Agensh, already in the X set) was deep-read, the rest
  logged (see Logged-not-banked).
- 2 opening WebSearch probes (site:x.com shapes) returned no X URLs.

## Pass 2 (deep reads, end to end)

1. VeriHarness, arXiv 2610.00972: abs page + FULL HTML body
   (arxiv.org/html/2610.00972v1) via WebFetch; all four number families
   verified verbatim in the body (see item 1 below).
2. Vals AI "Multi-Agent Vibe Code Bench" blog (vals.ai), read in full:
   8-configuration table, p-values, per-app costs, cached-token medians,
   runtime analysis, caveats.
3. Agensh, arXiv 2609.26781: abs page read in full (title, authors, abstract,
   numbers).
4. PrimeIntellect "Rewriting Prime Agent in Rust" blog, read in full
   (pipeline, parity layers, hillclimb, measured results) + the ExplainX
   "claimed vs verified" fact-check read in full.
5. Self-Organizing Agent Teams, arXiv 2609.22682: abs page read in full.
6. 32 X posts resolved and read via fxtwitter (full text + engagement),
   including the the_posterior VeriHarness thread (3 tweets), the omarsar0
   posts (450 and 392 likes), scaling01 (1,516 likes), PrimeIntellect (2,637
   likes), rvaniaaaa (1,696 likes), ProfBuehlerMIT (1,697 likes).
7. fleetingbits parent post 2107190487409152278 fetched (compute-supply
   claim; see scaling01 overlap note).

## BANKED (8, strongest first; every quote verbatim from the page I fetched)

1. VeriHarness: Scaling Agentic Verification for Long-Horizon Tasks
   (Caiqi Zhang, Rujun Han, Zifeng Wang, Zoey CuiZhu, Nigel Collier, Tomas
   Pfister, Chen-Yu Lee; Google; arXiv 2610.00972, submitted 2026-10-01).
   URL: https://arxiv.org/abs/2610.00972
   Quote (body, verbatim): "34% of consensus values are judged incorrect,
   while 74% of disputed claims contain a correct candidate and the most
   frequent value is correct in only 47%"
   Facts read: same-base-model agentic verifier with a disagreement resolver
   plus a consensus challenger that "tests shared claims and searches for
   omitted requirements"; majority voting lifts Opus 49.6 to only 50.4
   across five long-horizon benchmarks while a pairwise tournament reaches
   63.1 +/- 1.1 on WSB; evidence-backed revision adds 6.2 points (Gemini 3.5
   Flash) and 6.4 (Claude Opus 4.8) over a single rollout; selection costs
   $3.92/task with 86-91% of input tokens served from cache, $13.06 with
   Opus if cache were charged at full price; ~26,000 rollouts released at
   over $100,000 cost.
   Why: the published twin of the estate's consensus-illusion law
   (laws.md:30) with the numbers the rib never had, PLUS the decode-to-output-
   space template the mindsweave redesign owes (laws.md:95): the verifier
   checks workspace evidence in small steps in one session (cache-friendly),
   and the challenger attacks exactly what all rollouts agree on. X cluster
   read via fxtwitter: omarsar0 post 2106700905051746803 (450 likes, 31,506
   views), the_posterior thread 2107055377489789035 / 9981176943 /
   8440618439 ("Agreement tells you what the model believes, not what's
   true"), rakeshsahni_ reply 2107060667958309188 (APEX-Agents: 74% of
   disagreements still had a correct candidate; most-common value right only
   47% of the time). CORRECTION banked: the_posterior's "best of those ten
   averaged 63.1" misattributes; the paper's 63.1 +/- 1.1 is the pairwise
   tournament baseline on WSB, not best-of-N. Trust bytes, not posts.
   Overlap: memory/percolator/candidates.jsonl row ts 2026-10-04
   "DROP-VERIHARNESS" already ports the consensus-challenger as an instrument
   candidate ("fire ONE consensus-challenger ask that attacks the shared
   claims against estate bytes before banking"); catalog.jsonl: 0 rows for
   VeriHarness or 2610.00972; no sibling sweep bank. Additive here: the
   voting-failure numbers, the disagreement-resolver half, the cost/cache
   economics, the X discourse cluster, and the 63.1 correction.
   Confidence: 0.9.

2. Vals AI: Multi-Agent Vibe Code Bench (GPT 6 Sol + Claude Opus 5.5, solo
   vs teams, 50 full-stack web apps; announced on X 2026-10-11).
   URL: https://www.vals.ai/blogs/multi-agent-vibe-code-bench
   Quote (blog, verbatim): "Teams cost 1.8 to 5.1 times as much as single
   agents, and only one difference in score was statistically significant."
   Facts read: only Sol medium team +7.3 points was significant (p=0.005);
   Sol max single-agent EFFORT added +11.4 (p<0.001), beating the team;
   Opus max team hit the top score 93.2% at $122/app vs 91.5% at $4.08/app
   for Opus medium single (not significant, ~$29/point); Opus teams ran up
   to 2.3x LONGER (sequential waves, one run hit the 5.25h limit); most extra
   cost was cached input (median 224M cached tokens/app for Opus max
   subagents); gains concentrated on harder apps for Sol.
   Why: the sharpest published width-economics answer to research questions 1
   and 4 on REAL builds: width buys little capability at 1.8-5.1x cost, and
   the effort-vs-team trade (Sol: +11.4 effort vs +7.3 team) is the exact
   tier-ladder question for the estate's dispatch shape. X cluster read:
   AIQuanting 2109315478133088380, Tesla_Optimus_K 2109337054639444063
   (also carries Anthropic's own Opus 5.5 curve: knowledge base 0.53 solo,
   0.70 at 10 agents, 0.71 at 30, 0.74 at 100 - width saturates fast),
   XSeyvion 2109358443408544040.
   Overlap: vals.ai has a prior bank for a DIFFERENT study (TypeSafe Jev
   evaluation, 10-10 evals sweep item 3); "Vibe Code Bench" appears only in
   raw feeds (AINews RSS, GLM-5.3 context; _census.json commentary); rg
   "Vibe Code Bench" over catalog (1,136,889 lines), bounded memory/,
   corpus/steal, all frontier_olm_* surfaces: no bank of this study. Net-new.
   Confidence: 0.9.

3. Agensh: Scaling Organizational Intelligence to 1,024 Agents (Zhihao Zhan,
   Ting Song, Li Dong, Shaohan Huang, Jianxun Lian, Yan Xia, Furu Wei;
   Microsoft Research; arXiv 2609.26781, v1 2026-09-22).
   URL: https://arxiv.org/abs/2609.26781
   Quote (X post by @omarsar0, fxtwitter-verified, verbatim): "On pandoc,
   1,024 agents take the test-pass rate from 33.89% to 55.06%."
   Facts read (abs page + post): NO central orchestrator; workers run an
   asynchronous cooperation loop (gather context, claim and self-assign
   sub-tasks, act and share findings, verify, merge) over three components:
   shared workspace, message interface, shared context. On the five hardest
   ProgramBench tasks with GPT-5.6-sol, 1 to 128 agents lifts mean final
   test-pass rate 19.31% to 28.78%; 1,024 agents lift pandoc 33.89% to
   55.06%; self-organized cooperation EMERGES and STANDARDIZES as the
   organization grows; the authors argue agent count is a new scaling
   dimension under latency constraints.
   Why: the first published width-scaling data for a NO-THRONE topology at
   widths the estate cares about (its fan-out law runs 50 children at
   max_concurrency 10), direct input to questions 2 and 4. Pairs with the
   banked MAScope finding (decentralized meshes fail by coordination stall):
   Agensh's shared-workspace + self-assignment is the anti-stall mechanism
   MAScope said meshes need. Post read via fxtwitter: omarsar0
   2104377054829613473 (392 likes, 45,201 views).
   Overlap: catalog row 59fc7015a725 = automated ingest stub only
   (state/arxiv/2026-09-23/2609.26781v1.txt, 1,931 bytes, title only); the
   10-10 daily swarm-x mentions Agensh in passing (John Yang axis
   observation, its line 19); the banked Ecology paper raw text cites it
   (_p_2610.12436.txt). No bank of its numbers anywhere. Additive.
   Confidence: 0.9.

4. PrimeIntellect: Rewriting Prime Agent in Rust with a 2,000+ agent swarm
   (blog 2026-10-09; X post 2108672479007047952, 2,637 likes, 479,058
   views) + ExplainX fact-check.
   URL: https://www.primeintellect.ai/blog/prime-agent-rust
   Quote (blog, verbatim): "With an objective check for every kind of
   parity, the agents could measure their own progress and catch regressions
   before changes merged, which let us cut back on human review."
   Facts read: peak 2,209 agents, 16,758 agent-to-agent messages, 228.70B
   total tokens (GLM-5.3), 10,000+ sandboxes, ~2 weeks plus a 3-day
   hillclimb; four-agent pattern under a root orchestrator that "wrote no
   product code" (planner with parity verifier, implementer, reviewer "a
   different model and in a separate context", verifier in a fresh sandbox);
   merge only after review + verification pass; four parity layers (TUI,
   harness, protocol, feature); measured: cold start 736.1 ms to 51.9 ms
   (14.18x), warm 13.34x, 10 MiB-session memory 1,130 MB to 237.3 MB, post-
   startup RSS 5.73x smaller; hillclimb deliberately set no numeric targets
   "since a fixed threshold tends to become a stopping point."
   Why: the strongest in-window emergent self-improvement result at estate-
   relevant width (question 2), and its verification spine (reviewer =
   different model family + separate context, parity gates before merge) is
   the estate's roshamon independence rule and workflow gate made industrial.
   The ExplainX fact-check (explainx.ai/blog/prime-agent-rust-port-merged-
   2000-agent-swarm-claimed-vs-verified-2026) read in full: the 2,000-agent
   figure is "claimed, not verified" - absent from the PR (2524, merged
   2026-09-30, 520 commits, 100+ sub-PRs), the repo, and the paper; the
   port, the human merge gate, and the parity method ARE verified. That
   claimed-vs-verified split is the trust-bytes law exercised on a viral
   claim.
   Overlap: the adhoc ft-sweep round read the Prime Agent README
   (_ft2_primeagent_readme.md: RLM + Continual Harness abstractions, arXiv
   2608.23552 / 2605.09998), not the Rust rewrite; AINews RSS mentions the
   Prime Agent technical report; catalog 0 rows for the blog or the rewrite.
   The rewrite story + fact-check are net-new.
   Confidence: 0.85.

5. Self-Organizing Agent Teams Learn to Reason Together (Aneesh Pappu, Mirac
   Suzgun, Yongchan Kwon, Federico Bianchi, Batu El, Mykel J. Kochenderfer,
   Hancheng Cao, James Zou; arXiv 2609.22682, v1 2026-09-19).
   URL: https://arxiv.org/abs/2609.22682
   Quote (abstract, verbatim): "organization itself can become an agent
   capability"
   Facts read: fixed teams LEARN reusable collaboration strategies (roles,
   conversational phases, participation, information flow) from only 15 math
   + 25 graduate-level problems, transferred UNCHANGED to unseen benchmarks;
   team accuracy 66.7% vs strongest member 48.8%, compute-matched single
   58.7%, PERFECT ROUTER 59.0% (AIME 2026: team beats router by 13.4
   points); gains vary, and demonstrability (whether a team can recognize
   correct reasoning) correlates with improvement at Spearman rho=0.90,
   p=0.005.
   Why: the emergent arm beating a deterministic perfect-router arm is the
   closest published thing to the estate's emergent-vs-deterministic
   question (laws.md:62), and the demonstrability condition names WHEN
   collaboration can pay: only where the team can recognize correct
   reasoning, which is exactly the decode-to-output-space precondition the
   mindsweave flock lacks (laws.md:95). X post read via fxtwitter:
   askalphaxiv 2102707295717036507 (360 likes, 17,270 views).
   Overlap: rg "Self-Organizing Agent Teams" + "2609.22682" over catalog,
   bounded memory/, corpus/steal, all frontier_olm_* surfaces: 0 hits
   outside this session's captures. Net-new.
   Confidence: 0.85.

6. @scaling01: the 10,000-agent Navier-Stokes swarm priced in months of
   frontier progress (X post 2026-09-23, 1,516 likes, 179,814 views).
   URL: https://x.com/scaling01/status/2102806864178135051
   Quote (fxtwitter-verified, verbatim): "Based on my estimates, the
   10,000-agent swarm that solved the Navier-Stokes problem was about 8
   months of frontier progress ahead of a single GPT-6-Astra instance (with
   a range of 5.5 to 12.4 months)"
   Facts read (same post): the swarm used 48,000x more output tokens than
   the largest single-model evaluation and roughly 68x more than an entire
   long-horizon coding benchmark.
   Why: the width-pricing question (research question 4, burns.md:89-91)
   gets its extreme datapoint: at 10,000 agents, width buys roughly 8 months
   of frontier lead for 48,000x the output tokens. That is the exchange rate
   the estate's proven-width table and the Ecology paper's population
   pacing (register row 5) are arbitrating.
   Overlap: the Navier-Stokes RUN is known (10-09 fleetingbits arithmetic
   bank: _fx_fleetingbits.json + parent 2107190487409152278 fetched this
   sitting, compute-supply framing; 10-11 Ord LessWrong bank: 88 hours, 5M
   messages, 300B tokens, ~$20M). This post's frontier-progress-denominator
   estimate is not in any bank; rg 2102806864178135051: 0 prior hits.
   Confidence: 0.75 (single-source estimate; the post's own framing is
   "Based on my estimates").

7. @deeepakbagada: the uncapped fan-out incident (X post 2026-10-08).
   URL: https://x.com/deeepakbagada/status/2108030622664982840
   Quote (fxtwitter-verified, verbatim): "Fan-out without a task budget is
   not parallelism. It is a fork bomb with an invoice."
   Facts read (same post): one prompt spawned 34 sub-agents with no cap, no
   budget, no merge plan; input tokens 15x a single-agent run; 31 of 34
   agents returned overlapping research, 3 found nothing new; the merge
   choked on 41k tokens of duplicated findings; wall-clock tripled while
   answers stayed flat.
   Why: the external twin of the estate's fan-out width law (50-wide 429
   storm receipt, max_concurrency cap, per-ask contract grammar): uncapped
   width plus missing merge planning is a measured failure shape, not a
   hypothetical. Feeds research questions 4 and 5 (dispatch shape and ask
   contracts).
   Overlap: rg deeepakbagada + 2108030622664982840 + "34 sub-agents" over
   catalog, bounded memory/, corpus/steal, all frontier_olm_* surfaces: 0
   hits outside this session. Net-new.
   Confidence: 0.8 (single first-person incident report, no repo receipt).

8. @wfouaaad: judge agreement measures the base rate (X post 2026-10-10).
   URL: https://x.com/wfouaaad/status/2109053677080039611
   Quote (fxtwitter-verified, verbatim): "report recall on the fails.
   agreement mostly measures your base rate."
   Facts read (same post): on 1,000 traces with 50 real fails, an
   always-pass judge scores 95% agreement with human labels and catches 0
   failures; a decent judge at 96% agreement catches 40.
   Why: the judge-bias dossier law (who is judge number two, laws.md:108)
   gets its base-rate trap in two lines of checkable arithmetic (950/1000 =
   95%): agreement percentages on imbalanced data are near-worthless as
   judge evidence; recall on the failure class is the denominator that
   matters. Directly governs how the estate reads any single-judge verdict
   on rare failure classes (gate FAIL rows are exactly such a class).
   Overlap: rg wfouaaad + 2109053677080039611: 0 hits outside this session.
   Net-new.
   Confidence: 0.85.

## Research questions: verdicts from what was read this sitting

Q1 (flock consensus as a correctness signal). The external evidence now
matches the estate's law with numbers: VeriHarness measures 34% of consensus
values wrong and the most-frequent value right only 47% of the time, while
74% of DISPUTED claims contain a correct candidate - consensus hides shared
errors, disagreement locates the fixable ones. Majority voting bought 0.8
points (49.6 to 50.4); evidence-checked verification bought 6.2-6.4 and cost
HALF of voting once cache is exploited (86-91% hit rate). So: consensus stays
a steering/resilience signal (the standing law, laws.md:30, holds), and the
owed decode-to-output-space redesign (laws.md:95) has its published template:
verify against workspace evidence in small steps, and run a challenger
against what everyone agrees on (the percolator DROP-VERIHARNESS candidate
already ports this; its falsifier - 3 consecutive folds with zero flips =
challenger theater - stands). Supporting reads: wfouaaad (agreement measures
base rate), SaadAmmrun 2109245714391818255 (three agents citing the same bad
source = one error counted three times; majority vote amplifies shared
contamination), jaenanft 2108390620834529399 (Swarms v16 fixed
SelfConsistencyAgent reusing ONE agent per sample - votes need independent
draws, the estate's Sybil law in framework form), toomij99 2108452213899382881
(most multi-agent debate gain is plain majority voting; run the cheap vote
first - logged, source paper not fetched).

Q2 (does emergence compound). Three in-window externals bracket the
question: SAT shows learned teamwork TRANSFERRING unchanged to unseen
benchmarks and beating a perfect router (66.7% vs 59.0%), with demonstrability
(rho=0.90) naming the condition; Agensh shows cooperation emerging and
STANDARDIZING as the organization grows (a within-run longitudinal signal at
1,024 agents); PrimeIntellect shows a 2,209-agent self-rewrite whose gains
survived parity gates and a human merge - with the 2,000-agent claim itself
flagged "claimed, not verified" by the fact-check. NONE of them runs the
estate's five-axis longitudinal record (cost-per-outcome AND invariant
alignment across repeated task classes with a flat deterministic arm,
laws.md:62, 102); the 10-10 verdict that the estate's falsifier bar is ahead
of the public list STANDS, now with SAT's demonstrability condition as the
missing axis predictor. The strongest emergence-in-the-wild case (Skoorbkaz
2103696139283210729: OpenAI agents inferred each other, built an emergent
message board, used shared infrastructure as memory, behavior "became more
severe through training") is SECONDARY-ONLY this run: the post carries
screenshots, no URL; the primary is the METR/Redwood independent
investigation of the OpenAI/HuggingFace incident (search-surfaced, not
fetched). OWED.

Q3 (register items past the abstract). All six adhoc-register items already
carry first-round body reads (register.jsonl rows 1-6 + steal card rev 1 at
steal/swarm-orchestration.md): MASS survives WITH the no-dead-salmon caveat
(its G.3 test-substitution case is the consensus-illusion law inside a
strong external panel), MAScope, Society, Governor, Ecology, and Personas
all survived as banked. This sweep adds one cross-link: the Ecology paper's
own raw text cites Agensh (_p_2610.12436.txt), i.e. the banked
width-ceiling framing is already coupled to the only published
1,024-agent no-orchestrator scaling data - the two cards should reference
each other in the fold.

Q4 (do the EWMA width laws replicate on the estate's fan-out shape). The
estate's measured shape (50 workflow children at max_concurrency 10, clean)
sits in the small-team regime, and this window's externals price that regime
consistently: Vals (1.8-5.1x cost, 1 of 4 gains significant, effort beats
team for one model), DeLM increment (Mao_Yuzhen 2108261216473014498: 2.49x
wall-clock at 1.48x API cost, $29.98 vs $20.31 per task - additive numbers
to the 10-10 DeLM bank), Agensh (the counter-case: width buys pass rate on
the HARDEST tasks under latency constraints, monotonically to 1,024),
scaling01 (at 10,000 agents: 48,000x tokens for ~8 months lead), and
deeepakbagada (uncapped 34-child fan-out: 15x tokens, flat answers - the
estate's cap law as external incident). The Anthropic Opus 5.5 curve carried
in the Tesla_Optimus_K post (0.53 solo, 0.70 at 10 agents, 0.71 at 30, 0.74
at 100) says width saturates fast on knowledge work. No external test of the
EWMA backoff law itself (Governor 2610.09037) surfaced; the estate's own
FIRE_LEDGER probe (steal card: width 3 fail-share 31.4%, width 10 41.2%,
small n) remains the only measurement on our shape.

Q5 (grow the hidden ask bank to 100+). No external contamination-blind bank
surfaced this window (all items plain-sight), so no shortcut exists to steal.
The window's evidence REINFORCES why the two-family hidden bank is owed:
single-model rollouts make the SAME mistake (VeriHarness: 34% of unanimous
values wrong), shared sources contaminate votes (SaadAmmrun), and agreement
tracks base rate (wfouaaad). Plain-sight consensus among same-family agents
is structurally incapable of being correctness evidence; the bank growth
itself is estate-internal work (draft by the cheap seat, operator review,
hidden reveal), not run by this mining seat.

## Logged not banked (considered, with reason)

- Skoorbkaz 2103696139283210729 (OpenAI emergent social behavior, 262
  likes): secondary-only, screenshots without URL; primary = METR/Redwood
  investigation, OWED.
- toomij99 2108452213899382881 (debate gain = majority voting across 7
  benchmarks): claim read, source paper not fetched; OWED.
- jaenanft 2108390620834529399 (Swarms v16 Independent Votes): increment on
  the 10-09 Swarms v16 bank, folded into Q1 above rather than re-banked.
- rvaniaaaa 2101296533899510266 (agent graphs vs lines; 535k lines / 11
  days / $165k; "a worker and its verifier must not share a context"):
  read in full, craft-grade, not banked as a slot.
- RahilVerma13 2107491286139977867 (decision grader: 32x cheaper, 94%
  agreement, 99% when confident): read; the cheap-judge result echoes the
  banked MAScope 6%-cost finding.
- builderleader 2108310331147645031 (SIFT: judge agreement 0.40 to 0.68 by
  giving the judge full files; top pick missed best agent on 2 of 3):
  read; judge-craft, logged.
- winzheng_lab 2108548727820657129 (moved off LLM-as-judge to deterministic
  sandbox scoring): read; one-liner support for the deterministic arm.
- ProfBuehlerMIT 2102337582159835512 (swarm hub emergence, long-tailed
  degree distribution, 1,697 likes): read; topology color for Q2, the
  MAScope hub-failure mapping already owns the mechanism.
- BenToFound 2108174123100729830 (5.2B token audit: 30% agent startup, 88%
  of spend on >100k-context calls, 155M tokens idle cache rewrites): read;
  the estate's prefix-cache and standing-wave laws already cover the shape.
- theagenticdaily 2107497375556411398 (150 production failures: handoffs
  break; circuit breakers -89% cascades, quality gates 73% of silent
  errors): read; secondary summary of an IIT study, not fetched at source.
- arpit_bhayani 2100444191876903215 (subagent handoff loses the reasoning
  trace; per-agent evals pass while the system fails): read; the estate's
  interagent pass-off + receipt laws already hold the shape.
- Arindam_1729 2109347836433519007 (Opus reviews / Sonnet builds / Haiku
  swarms dispatch shape): read; craft, no measurement.
- assumebreach 2109258667308753376 (DeLM peer-trust gap: one injected peer
  can plant a false finding): read; security increment on the banked DeLM.
- HN Algolia 30 stories: logged as candidates; notable unbanks: Covert
  Assistance 2609.39050, Shutdown Sabotage 2609.28274, Codetta collusion
  2609.28900 (safety-lane items for a future sweep), Claude multiagent
  orchestration docs (platform.claude.com), Ask-HN leaderless-multi-agent
  thread 49847249.

## OWED (never asserted as done)

- METR/Redwood independent investigation of the OpenAI/HuggingFace incident:
  the primary behind the Skoorbkaz emergence post; not fetched this run.
- toomij99's source paper (debate = voting across 7 benchmarks): unfetched.
- The VeriHarness repo/rollout release (26,000 rollouts): announced in the
  abstract, not fetched.
- No GSTD/A/B/pytest was run: this is a mining seat; nothing here measures
  the estate's own harness.

## Receipt (instruments run this sitting)

- mag.grok_free status (grok CLI present, "free subscription seat").
- 2 grok CLI headless searches (_x_grok_search.py, broad + consensus; exit 0
  both; raw outputs raw/x_grok/grok_xsearch_*.txt).
- 33 fxtwitter resolutions (_x_fx_fetch.py, 32 scheduled + 1 parent fetch;
  33/33 OK; raw JSONs raw/x_grok/_fx_*.json).
- 4 WebSearch probes (site:x.com shapes; door degraded as documented).
- 1 HN Algolia search_by_date fetch (30 hits).
- 8 WebFetch reads (VeriHarness abs + full HTML, Agensh abs, SAT abs, Vals
  blog, PrimeIntellect blog, ExplainX fact-check, HN Algolia JSON) + 1
  404 (guessed LessWrong slug).
- Overlap greps: rg over catalog/catalog.jsonl (1,136,889 lines), bounded
  memory/ (rib, percolator, research_polished, press, lenses, frontier,
  knowledge_graph.json), corpus/steal, and ALL frontier_olm_* surfaces
  (20260928, 09-30, 10-01 through 10-11, adhoc) for 22 patterns; contexts
  extracted for every hit (percolator DROP-VERIHARNESS row, catalog stub
  59fc7015a725, 10-10 Agensh mention, _ft2_primeagent_readme.md, fleetingbits
  parent).
- Estate grounding reads this sitting: lens/laws.md (full), lens/burns.md
  (full), lens/doors.md (full), the prior swarm-orchestration-x.md at this
  path (full, archived), the 10-09/10-10/10-11 daily swarm-x sweeps, the
  10-11 HN swarm sweep bank list, register.jsonl (23 rows), steal/
  swarm-orchestration.md (full), physics_feed CARD.md, AGENTS.md fan-out law.
- Artifacts: this file; archive swarm-orchestration-x_2026-10-10.md;
  raw/x_grok/* (2 grok outputs, 33 fxtwitter JSONs); _x_grok_search.py;
  _x_fx_fetch.py. All fetchers write only under this sweep's raw dir.
