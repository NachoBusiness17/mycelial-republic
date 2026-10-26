source-fetched: 2026-10-11

# SWEEP: swarm-orchestration via X (frontier_olm_2026-10-11, gopher actor)

Seat: sweep gopher, area "swarm-orchestration via x". Door per the ask's fetch recipe:
WebSearch with site:x.com / twitter.com / status-ID-prefix queries for the topic, then
resolve single posts through the fxtwitter door https://api.fxtwitter.com/<user>/status/<id>.
House laws held: ascii only, no em or en dashes, every claim cites what was read or fetched
this sitting, quotes verbatim from the fetched pages. Bank only what I fetched and read
myself.

## Method (instruments, this sitting)

- 42 WebSearch queries (site:x.com, site:twitter.com, ID-prefix "status/2109" style,
  account-targeted, topic+date phrasings; full list summarized in the candidate log).
- 17 WebFetch reads: 6 fxtwitter API resolutions (4 in-window, 2 out-of-window probes),
  understandingai.org x3 (archive + two full posts), alphaXiv 2610.12176, arxiv.org abs
  2609.11873, langchain.com blog post, greaterwrong.com user page + lesswrong.com Swarm
  Scaling post, tobyord.com root, plus 2 fetches that 404'd (explainx.ai/Blog/Topics,
  a guessed lesswrong slug) and 1 landing-page-only fetch (understandingai.org root,
  superseded by the /archive fetch). WebSearch allowed_domains=["x.com"] was ignored by
  the search backend and one such call timed out; recorded as tool limits, not door 403s.
- 2 venv python snowflake decodes (.venv/Scripts/python.exe, ids >> 22 + 1288834974657):
  window start 2026-09-11 = status id >= 2098199843435446272, today ceiling
  2109433867269046272. Decodes: Coxon 2097476196791709843 = 2026-09-09T00:04Z (out by
  2 days); MajmudarAdam 2098881885200081234 = 2026-09-12T21:10Z; deredleritt3r
  2099720642807382262 = 2026-09-15T04:43Z; chehendriksen 2099717883311845573 =
  2026-09-15T04:32Z; swarms_corp 2044051206897566161 = 2026-04-14; reach2ratan
  2093904060311015480 = 2026-08-30; AnthropicAI 2036481033621623056 = 2026-03-24.
- Overlap greps (rg): catalog/catalog.jsonl (1,136,889 lines by wc -l, same instrument
  the HN sibling used) for 10 patterns; bounded memory dirs (memory/rib,
  memory/research_polished, memory/press, memory/lenses, memory/frontier,
  memory/knowledge_graph.json, memory/research, memory/attention.md, corpus/steal,
  memory/corpus/LINKS.jsonl); sibling surfaces (frontier_olm_adhoc,
  frontier_olm_2026-10-10/sweep, frontier_olm_2026-10-11/sweep incl. the HN sibling bank).
- Estate files read this sitting to ground the five research questions:
  watch/inbox/frontier_olm_2026-10-11/lens/burns.md (268 lines, full) and lens/laws.md
  (124 lines, full), watch/inbox/gstd_perimeter_build_20261010/LOOP_CLOSED.md (full),
  watch/inbox/awesome_rsi_drop_20261010/CARD.md (full), watch/inbox/mass_sakana_drop_
  20261010/CARD.md (head 40 lines), frontier_olm_adhoc/register.jsonl (the 6
  swarm-orchestration rows), AGENTS.md line 35 (fan-out width law, rg -n confirmed),
  and the sibling bank sweep/swarm-orchestration-hn.md (full, anti-rebank surface).

## Door status

fxtwitter answered 200 on all 6 resolutions, no 403s, no degraded JSON. The honest
degradation is index sparsity: search engines surfaced exactly two organic x.com status
URLs in 42 queries (both out of window), and every in-window X item I banked was reached
by harvesting status URLs out of in-window secondary pages that quote X, then resolving
them through the door. The X surface wire OWED (commit e8eedd8eb, x-history miner named
the cure) is re-confirmed by this sweep: search-side X mining cannot reach the last 30
days; only history-side mining can.

## Pass-1 candidate log (42 considered; last-30-day window marked)

Resolved through the fxtwitter door:
- IN: @MajmudarAdam 2098881885200081234 (2026-09-12, 639,729 views, 2,710 likes), the
  scaling-law essay -> BANKED below.
- IN: @deredleritt3r 2099720642807382262 (2026-09-15, 31 likes), speculative reply ->
  BANKED below.
- IN: @chehendriksen 2099717883311845573 (2026-09-15, 12 likes), quote-tweet endorsing
  the Majmudar essay as "the clearest explanation you will get" -> considered, NOT banked
  (endorsement, no mechanism content; the fetch's reply-direction fields contradicted
  each other across the two resolutions, so I also flag a small-model garble risk there).
- OUT: @swarms_corp 2044051206897566161 (2026-04-14) "Definitive Guide to Multi-Agent
  Harness Engineering" -> resolved, out of window, logged.
- OUT: @reach2ratan 2093904060311015480 (2026-08-30) 2026 AI stack infographic ->
  resolved, out of window, logged.
- OUT: @AnthropicAI 2036481033621623056 (2026-03-24) multi-agent harness post -> snippet
  only, out of window, logged.

Identified but NOT resolvable through the door (no status URL surfaced anywhere):
- Sakana MASS announcement thread (Oct 8): alphaXiv abs page has an EMPTY discussion
  section; the mass_sakana card's "elvis @omarsar0, 7.6k views" thread is unverifiable
  through this door; Elvis Saravia's "Top AI Papers of the Week" blurb surfaced only as a
  newsletter search snippet.
- @SakanaAILabs Schmidhuber / RSI Lab announcement (Sep 24): only the sakana.ai blog and
  ITmedia/ActuIA coverage surfaced; no status URL.
- Noam Brown "feel the AGI" post (~Sep 8, out of window by 3 days anyway), Hanson Wang
  post, Jeff Clune posts (his essay + LinkedIn surfaced, no X URL), Toby Ord X posts,
  Kye Gomez @KyeGomezB reposts (profile page only), Peter J. Liu post, Daniel Mac post
  re Clune memory-mechanism agents: all snippet-class only, logged.
- @hilbertspaess (Jacob Coxon) 2097476196791709843, 170M+ views, Sep 9: out of window by
  2 days (article-identified; not resolved directly). MrinankSharma Feb 2026 and TMZ Sep
  posts: out of window or out of area.

Non-X items the X-discourse trail surfaced (door noted per item; the decisive ones read
end to end):
- IN: Toby Ord "Swarm Scaling" (LessWrong, 2026-09-21, 355 points) -> BANKED below.
- IN: "The Last AI Built by Humans" (arXiv 2609.11873, v1 Sep 10, v3 Sep 22) -> BANKED
  below.
- IN: LangChain "Organizing Context in a Multi-Agent Harness" (fetch header: September 8,
  2026; one search snippet said Sept 17; the fetch is primary) -> BANKED below.
- IN: Understanding AI "Why agent swarms could be the next 'scaling law'" (Oct 5, Dan
  Kagan-Kans) -> read in full; it is the hub that yielded the two in-window tweets; not
  banked as an item (its content lives in the tweets and the Brown interview summary).
- IN: Understanding AI "How a single tweet transformed the AI safety debate" (Sep 17, Kai
  Williams) -> read in full; yielded the out-of-window Coxon tweet; not banked (safety
  debate, not orchestration).
- alphaXiv 2610.12176 MASS page -> read in full to verify MASS claims first-hand (the
  adhoc register row 1 already banked the body read; this was verification, not a bank).
- IN, logged not read: "Swarm Organization as the Exponent on Test-Time Compute"
  (LessWrong, Sep 17); Ord "AI Scaling vs Human Scaling" (Oct 9); NYT "The Liftoff
  Scenario That Terrifies A.I. Doomsayers" (Sep 16); Import AI 475 (~Oct 5).
- Out of window, logged: swarms.ai AgentHQ (Aug 29); Sakana Fugu (Jun 2026); petruarakiss
  harness-engineering post (Jul 8).
- Logged, not read (weaker fit or non-window): SWARM+ arXiv (hierarchical multi-agent
  consensus for workload placement); desplega-ai/agent-swarm GitHub; agents.kour.me
  swarm-consensus pattern; mcpmarket Agent Swarm Consensus Mechanisms skill; Munder
  Difflin multi-agent harness; Anthropic engineering "Effective harnesses for
  long-running agents"; Addy Osmani "Agent Harness Engineering"; arXiv 2605.18747 "Code
  as Agent Harness" survey; AIDE2 (outer agent rewrites inner agent, alphaXiv); HN "How
  An AI math breakthrough ignited a controversy" (Sep 10); jeffclune.com "Why I work on
  self-improving AI despite the risks"; TowardsAI 500-agent simulation; HackerNoon
  scaling-laws critique.

## BANKED (5, strongest first; every quote verbatim from the page I fetched)

1. @MajmudarAdam post (2026-09-12, "adammaj", research @OpenAI per bio; 639,729 views,
   2,710 likes, 2,406 bookmarks).
   URL: https://x.com/MajmudarAdam/status/2098881885200081234
   Quote: "Or maybe there is some way to scale agent-clusters to collaborate up to N
   number of agents which we're already seeing lots of people try that represents a new
   way to saturate compute."
   Facts read (full text reproduced verbatim by the fxtwitter fetch): capability jumps
   come from scaling existing laws or discovering new ones; candidate unsaturated axes
   include "test-time training," agent-clusters, and "recursive-self improvement can be
   thought of as a scaling law"; internal scaling plots "have never lied (so far)";
   models near-superhuman at hacking/cyber; the past-two-weeks researcher alarm is fear
   of compounding scaling without control, "by no means a regulatory capture strategy."
   Why it matters: the most-viewed in-window articulation of swarm-clusters-as-scaling-
   axis that the five-axis emergent-vs-deterministic gates (lens/laws.md:61) must
   adjudicate, and the discourse frame (fear vs capture) the estate's X surface OWED
   covers; it names RSI itself as a scaling axis, the exact claim GSTD's
   consensus-ledger ("the network should learn on its own", LOOP_CLOSED.md:13-14)
   would need to beat a dead-salmon null to claim.
   Overlap: rg "Majmudar|2098881885200081234" over catalog.jsonl (1,136,889 lines) = 0;
   bounded memory dirs = 0; sibling sweeps = 0. Net-new.
   Confidence: 0.9.

2. Swarm Scaling (Toby Ord, LessWrong, 2026-09-21, curated, 355 points / 46 comments).
   URL: https://www.lesswrong.com/posts/6cb7qd3RSkgnviCpf/swarm-scaling
   Quote: "In total, one could achieve the task in about 1/4 the time for 4x the cost."
   Facts read: economists' parallelization frame, n workers = one worker n^lambda times
   as long, lambda the "stepping on toes" parameter; measured from OpenAI GPT 5.6 Sol
   launch charts (1/4/16-agent swarms): BrowseComp lambda 0.68 (90% CI 0.63-0.76),
   SEC-Bench Pro 0.57 (0.52-0.61), Terminal-Bench 0.48 (0.40-0.57); a 4-agent swarm
   needs about 2x total tokens for equal performance; swarm compute buys "a little over
   half as much gain in capability for the same scale-up of compute", so swarms buy
   speed, not capability; the 10,000-agent Navier-Stokes run = 88 hours, 5M messages,
   300B tokens, ~$20M at API prices; Ord REMOVED his closing swarm-scaling speculation
   after two sources confirmed OpenAI's chart "only showed the effect of longer CoT, not
   larger swarms"; comment thread: mixed-model-family swarms (Claude, GLM, Astra)
   outperform same-model swarms and heterogeneity may push lambda toward or above 1
   (Tim L, Julian Bradshaw, citing "Scaling Discovery through Test-Time
   Communication"), swarm critics as error-dampeners against hallucination cascades
   (chiamarc).
   Why it matters: the five-axis gates' cost-per-unit-outcome and variance axes get
   published numbers; the speed-not-capability finding is the exact hypothesis the
   GSTD-vs-single-seat A/B (research question 4) must test; the heterogeneous-swarm
   comments externally support GSTD's 5-heterogeneous-model shape (question 5) while
   the chart-label retraction is a field-logged case of the estate's trust-bytes law
   (lens/laws.md:13).
   Overlap: the HN sibling bank logged the Ord items "considered; superseded by 49871574
   read" and cited the 0.48-0.68 range secondhand via the Chai blog
   (sweep/swarm-orchestration-hn.md:66, :199); catalog "swarm scaling" 0 hits per that
   receipt; my bounded memory rg "Swarm Scaling|stepping on toes" = 0. This first-hand
   read is additive (per-benchmark lambdas with CIs, the verbatim token/time line, the
   retraction, the heterogeneous-swarm comments), never a re-bank of the HN lane's bank.
   Confidence: 0.9.

3. Organizing Context in a Multi-Agent Harness (LangChain blog, Thushanth Bengre +
   Chester Curme; fetch header: September 8, 2026).
   URL: https://www.langchain.com/blog/organizing-context-in-a-multi-agent-harness
   Quote: "Subagents spawn with a fresh context window, receiving only the task
   description specified by the supervisor."
   Facts read: two subagent context modes in deepagents: "isolated" (default, fresh
   context) and "fork" (supervisor state propagates; state minus the trailing tool call;
   task becomes a user message); forked subagents are faster/cheaper via prompt caching;
   the post's own warning: verifiers should stay independent because "inheriting the
   supervisor's reasoning can be counterproductive" since they get anchored by the
   supervisor's diagnosis or expectations; forking parallel researchers would duplicate
   history. No benchmarks in the post.
   Why it matters: the independence condition behind the consensus-illusion law
   (lens/laws.md:60, "high-strength consensus was wrong 3/3") is now a shipped
   engineering default in mainstream tooling, with the anchoring failure named in the
   vendor's own docs; that is the Q1 answer landing in the field, and the isolated/fork
   switch is a concrete dispatch-shape control for the estate's lanes (Q5).
   Overlap: rg "Organizing Context in a Multi-Agent" over catalog + bounded memory +
   sibling sweeps = 0. Net-new.
   Confidence: 0.85.

4. The Last AI Built by Humans: Toward Genuine Recursive Self-Improvement (Yi Duan et
   al., 35 authors, arXiv 2609.11873; v1 2026-09-10, v3 2026-09-22, cs.LG).
   URL: https://arxiv.org/abs/2609.11873
   Quote: "Recursive self-improvement (RSI) enables AI systems to turn experience and
   feedback into persistent changes"
   Facts read (arXiv abstract page, full): five-level roadmap by autonomy:
   improvement-execution, improvement-strategy, experience-acquisition,
   environment-adaptation, recursive meta-improvement; a "Headroom-Closed Index (HCI)"
   assessing existing LLMs; scenarios span scientific discovery, embodied intelligence,
   software engineering. Secondary coverage snippets (XNews, The Rundown AI via
   blockchain.news) add: 491 papers surveyed, under 6% reach Level 5, about 75% sit at
   Levels 1-2, and SCMP covered it in Sep 2026; those three numbers are snippet-class
   evidence only, I could not read them on the abstract page.
   Why it matters (question 2, second half): this is the newest public map of the RSI
   field and it PREDATES MASS (arXiv 2610.12176, submitted 2026-10-08) by 16 days, so
   with the lobehub awesome-rsi README (predates, banked 10-10) and the DAIR collection
   (excludes it, banked by the HN sibling today), the verified answer is: no public map
   ranks MASS yet. Its five autonomy levels also give the estate's harness-level,
   cryptographically-auditable loop a named slot in field vocabulary.
   Overlap: catalog id 83f1c7640578 already holds the abstract stub
   (state/arxiv/2026-09-11/2609.11873v1.txt, 1,358 bytes, mtime 2026-09-11T06:30Z), and
   the adhoc sweep's _ftread_2610.12002.txt cites it in a reference list. Additive here:
   the level names, HCI, and the map-ranking verdict; the abstract itself is NOT
   re-banked.
   Confidence: 0.85.

5. @deredleritt3r reply ("prinz", 2026-09-15, 31 likes, reply to @chehendriksen's
   quote-tweet of the Majmudar essay).
   URL: https://x.com/deredleritt3r/status/2099720642807382262
   Quote: "One might imagine that this scaling law is multi-agent."
   Facts read: speculation that OpenAI's new scaling axis "is multi-agent," referencing
   "the multiplicative effect of scaling laws that has been observed (see Noam Brown's
   interview today)"; the fetch reproduced only short exact excerpts (small-model
   quoting limit on the ~517-char text), so this quote is a verified verbatim fragment,
   not the full text; flagged honestly.
   Why it matters: the swarm-as-scaling-law meme in its raw speculative form, one hour
   after the endorsement quote-tweet; banks as discourse evidence for questions 4 and 5
   (what the market believes vs what Ord measured), not as mechanism.
   Overlap: rg "deredleritt3r" over catalog + bounded memory + sibling sweeps = 0.
   Net-new.
   Confidence: 0.7.

## Research questions: verdicts from what was read this sitting

Q1 (GSTD STRUCTURE verdict vs consensus-illusion rib). The X-door evidence sharpens the
settings difference rather than changing the HN sibling's verdict: LangChain ships the
independence condition as a default (isolated mode) and names the failure of the other
setting (verifiers anchored by inherited supervisor reasoning), which is the engineering
twin of the rib's finding that the Mindsweave flock's shared surrogate decode vocabulary
decoupled consensus from correctness (lens/laws.md:60). GSTD answers independently per
model in the actual task output space with a dead-salmon null (LOOP_CLOSED.md:5-8,
69.23 pct vs 25.5 pct, STRUCTURE only). Governing law unchanged: the MINDSWEAVE
consensus-illusion law plus the verdict-without-conditions law (lens/laws.md:19, :60);
consensus is a STRUCTURE claim unless (a) independent voters, (b) decode in the actual
task output space, (c) an external check.

Q2 (MASS). Verified first-hand via alphaXiv this sitting: "Recursive Self-Improvement
through Multi-Agent Self-Supervision", Hyunin Lee, Jinglue Xu, Jeffrey Seely, Donghyun
Lee, Somayeh Sojoudi, Matei Zaharia, Yujin Tang (Berkeley/Sakana per the page), submitted
2026-10-08; alternates "evolutionary workflow optimization and supervised fine-tuning on
self-generated trajectories" under "an evolutionary search constrained by structural
guardrails"; 1.2-1.6x performance per output token on four open-ended benchmarks
(MLR-Bench 1.60x, DSBench 1.35x, ScienceAgentBench 1.20x, AstaBench E2E-Hard 1.28x),
and DECLINES on verifiable suites (Terminal-Bench 2.0 0.96x, SWE-bench Verified 0.94x);
multi-agent student 68.3% win share after 28.82M tokens vs single-agent 64.0% after
42.00M (not matched-data). These match the adhoc register row 1's first-hand body read,
so nothing new is claimed there. Ranking: no public map includes it (body of Q2 above).
The X announcement thread is unresolvable through this door (alphaXiv discussion empty;
no status URL surfaced); the mass_sakana card's elvis/7.6k-view provenance stays
unverified, and Sakana institutionalized the direction Sep 24 (Schmidhuber as Chief
Scientific Advisor + a dedicated RSI Lab, sakana.ai blog; X post unresolved).

Q3 (flock decode redesign). Nothing read this sitting names an owner; the HN sibling's
"advanced partially, still ownerless" stands. The X-discourse adds a reason it matters:
the field now treats agent-clusters as a candidate scaling axis (Majmudar) while Ord's
measured lambdas show the gains are task-parallelization, not per-agent quality, so a
flock whose decode is surrogate cannot even measure its own axis. Redesign stays OWED.

Q4 (GSTD vs single-seat deterministic baseline). The A/B is not run (LOOP_CLOSED.md and
RUNNERS.md hold no single-seat arm; confirmed by the HN sibling and unchanged by
anything I read). It is exactly the OWED five-axis harness run (lens/laws.md:88).
Prediction from evidence read, not measurement: Ord's numbers say the flock arm buys
speed at ~2x cost for equal performance, so on cost-per-unit-outcome the single seat
wins and consensus must earn its slot on variance or generalization; the swarm-as-
scaling-law meme (Majmudar, deredleritt3r) is belief, the Ord lambdas are the
measurement, and the five-axis gates are the arbiter.

Q5 (width law vs 5-model heterogeneous consensus). The fan-out width law (AGENTS.md:35)
binds the z.ai account's dispatch shape and is untouched: it is about retry surfaces on
one account, not about quorum composition. The external evidence cuts the other way
from homogeneity: Ord's comment thread argues mixed-model-family swarms outperform
same-model swarms and heterogeneity may raise lambda, which supports GSTD's 5
heterogeneous models. What still needs a NEW dispatch-shape receipt is the remote/paid
case: five heterogeneous providers means a 429 on one judge changes the quorum, which
the proven-width table (homogeneous session agents on one account) does not cover; the
HN sibling reached the same verdict and my reads add the heterogeneity-hypothesis
support plus Ord's cost curves for sizing it.

## Not run / not verified this sitting

- No GSTD harness run, no A/B, no pytest: this is a mining sweep, not a build seat.
- The MASS X announcement thread, Sakana Schmidhuber announcement post, Noam Brown /
  Hanson Wang / Jeff Clune / Toby Ord X posts: no resolvable status URLs surfaced in 42
  queries; nothing was guessed or fabricated for any of them.
- The 491-papers / <6% L5 / 75% L1-2 distribution for arXiv 2609.11873 is snippet-class
  (XNews, The Rundown AI via blockchain.news), not read on the abstract page itself.
- The chehendriksen and deredleritt3r fetches each reported reply-direction fields that
  conflict across the two resolutions (each claiming to reply to the other); timestamps
  and content indicate chehendriksen quote-tweeted Majmudar at 04:32 and deredleritt3r
  replied at 04:43; the exact parent-child edges are recorded with that uncertainty.
- Anti-rebank compliance: nothing in the burns-lens section-2 union, the adhoc register's
  23 rows (its 6 swarm rows are all arXiv-door: 2610.12176, 2610.10126, 2610.10468,
  2610.09037, 2610.12436, 2610.07535), the 10-10 run's sweep files, or the HN sibling's
  8 banks was re-confirmed as new; overlaps are stated per item.

## Receipt

- Instruments run this sitting: 42 WebSearch queries; 17 WebFetch reads (6 fxtwitter
  resolutions, 2 404s, 1 landing-page-only, 10 substantive page reads); 2 venv python
  snowflake decodes via .venv/Scripts/python.exe; 3 rg overlap batches (catalog.jsonl
  wc -l = 1,136,889 lines; bounded memory dirs; sibling sweep dirs); reads of lens/
  burns.md, lens/laws.md, gstd LOOP_CLOSED.md, awesome_rsi + mass_sakana cards, adhoc
  register rows, AGENTS.md line 35, and the sibling HN bank.
- Written to: watch/inbox/frontier_olm_2026-10-11/sweep/swarm-orchestration-x.md (this
  file).
