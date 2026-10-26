# Sweep: swarm-orchestration via X (frontier_olm_2026-10-08)

source-fetched: 2026-10-08. Seat: sweep-swarm-orchestration-x. House laws held: ascii
only, no em or en dashes, every claim cites what was read or run this sitting, bank only
items read myself, never fabricate. Instruments this sitting: WebSearch (Z.ai
web_search_prime backend; intermittent MCP 429 code-1302 storms when queries were fired
wide, cured by pacing single/double queries), WebFetch over api.fxtwitter.com status JSON
(7 statuses resolved fully), arxiv.org abs page (1), one blog mirror
(jinyansu1.github.io), and grep overlap checks over catalog/catalog.jsonl and every
frontier_olm_2026-10-0{3..8} register/sweep file plus memory/ribs (scoped greps; one
full-tree grep over all of memory/ was killed as filesystem-bound, its partial result
was bibliography noise only, declared per item below).

Window discipline: 2026-09-08..2026-10-08, enforced by fxtwitter's created-at on every
banked status (no snowflake guess is load-bearing; the ID prefilter used (id >> 22) +
1288834974657 only to ORDER the census, dates below are door-verified).

## Pass 1 census (broad sweep)

14 search queries, ~85 distinct candidate items enumerated. Full in-window fraction is
small because the web index serves mostly older X posts for research topics; every
out-of-window item was dated by snowflake decode and excluded, never banked. Key rows:

- IN WINDOW (door-verified later at fetch): rachittshah 2097657181235753206 (Sep 9,
  agents-as-distributed-systems); jachiam0 2097919252460400728 + 2097923322814296198
  (Sep 10, memeplexes); rohanpaul_ai 2098670948828504568 (Sep 12, Jagged Judges);
  harshbhatt7585 2101685636596175238 (Sep 20, benchmarks explainer);
  i/article/2102748781674639866 (Sep 24, team systems 66.7 vs 48.8, article body never
  resolvable, snippet tier, NOT banked); theneurondaily/article/2103549456662852008
  (Sep 27, article, snippet tier, NOT banked); rohanpaul_ai 2105717151453814785 (Oct 1,
  NVIDIA judge); cerebras/article/2105749446814576806 (Oct 2, article, snippet tier,
  NOT banked); sermakarevich 2106453816757354947 (Oct 3, evals article);
  KyeGomezB 2106770712039968975 (Oct 4, swarms-rs); dair_ai 2106770783607373994 (Oct 4,
  weekly papers, context-LM entry, adjacent to sibling areas, NOT banked);
  SuJinyan6 2106946784224510391 (Oct 5, verification bottleneck);
  theneurondaily/article/2106029852042375577 (Oct 3, article, snippet tier, NOT banked).
- OUT OF WINDOW (exemplar exclusions, dated by snowflake decode): EmergentMind
  2020578709325942805 (Feb 9, wisdom-of-crowds/SWARM purity paradox); analogalok
  2082842744163328295 (Aug 9); lilithdatura 2095381210960941522 (Sep 3, stigmergy post,
  misses the floor by 5 days); pachilo 2089287216514085212 (Aug 16, FREE-MAD);
  Weeklyvoice 2091687200605847796 (Aug 22, 1000 agents); _avichawla article 2088536550552605174
  (Aug 19, voting reduces variance not bias); marfinxx 2094016175617241109 (Aug 29, and
  the account is a struck fabrication source per the 10-06 lens anti-rebank rule 2);
  monokern article 2087241401649996149 (Aug 16); rohanpaul 1905844869307699372 and
  2080461981430198438 (2025 / Aug 4); dair_ai 2052429021833818458 (Jul); askalphaxiv
  2090269841768759547 and the whole Mind Viruses coverage wave 2089-2090e15 (Aug 19-22);
  heynavtoor 2096944019448431068 (Sep 6-7, borderline outside).
- ALREADY BANKED, NOT RE-BANKED (grep evidence below): sermakarevich 2106453816757354947
  (day-7 register row, judge kappa 0.15); harshbhatt7585 2101685636596175238 (day-7 sweep
  file item 6, BANKED); rohanpaul ArcticSwarm 2097089066579988968 (day-7 register);
  goodfire probe-monitors-101 (day-7 register); arxiv 2609.25396 Passes Alone Fails
  Together and 2609.21749 GraphSkillEvo (day-7 sweep file items 4-5); rachittshah
  2097657181235753206 (banked THIS RUN by the agent-memory-continuity-x sibling, their
  item 5, for the corr_id/run-identity angle; my seat folds only the dispatch-shape delta
  into the RQ1 verdict and does not re-bank the post).

Honest census verdict: the 30-in-window-candidate floor was NOT met. ~85 candidates
considered, ~13 in-window after date verification. Cause: the search index returns
predominantly older X posts for these research topics and the backend rate-limited under
width (4 batches fired produced 2 dead). This is stated, not papered over; the deep-read
pool below is every in-window item that survived the anti-rebank gate and resolved at a
primary door.

## Pass 2 deep reads (banked items, strongest first; every quote verbatim from a page
fetched this sitting)

### 1. Jagged Judges: jury majority strength predicts WHICH verdicts wiggle (Sep 12)

Post: x.com/rohanpaul_ai/status/2098670948828504568 (fxtwitter JSON read this sitting:
Sep 12 2026 07:12Z, 5,848 views, cites arxiv.org/abs/2608.12645). Paper abs page read
this sitting: framework tests "epistemic stability in LLM judges" as Mechanical
Consistency (re-prompt/reframe), Single-turn Conviction, Multi-turn Persistence;
"flipping verdicts 25--71% of the time under static pushback, and 62--91% with an
adversarial LLM persuader"; pressure that flips a verdict is "almost always
net-corrupting with respect to ground truth"; and "baseline jury majority strength as
the most effective single-shot signal for anticipating which items wiggle". 9 frontier
models, 14 judging tasks, submitted Aug 12 2026, v2 Aug 21.

Estate wiring (RQ2, lens/laws.md Q1 flock consensus decode, and the 0/3 wrong-at-
high-strength law at lens/laws.md:81-84 of the 10-06 lens): this is the first external
measurement I have read that makes consensus strength carry USEFUL information - as a
predictor of instability, not correctness. A flock decode that maps consensus onto the
task output space can consume strength exactly this way: high-strength rows are the
wiggle-suspect set that gets the re-look, low-strength rows route to normal verification.
That converts the estate's anti-signal into a routing signal without re-litigating the
0/3 measurement. It also hardens L23 (never a sole judge): a dissenter with persuasion
budget can corrupt 62-91 percent of verdicts, so judge prompts are attack surface.

### 2. AI Is Improving AI Faster Than We Can Check (Oct 5)

Post: x.com/SuJinyan6/status/2106946784224510391 (fxtwitter JSON: Oct 5 2026 03:17Z,
3,467 views, links article x.com/i/article/2106688930389315584, login-walled to every
door I hold). Article BODY read at the author's own mirror, jinyansu1.github.io
(technical-blog listing gives the href; post page fetched in full this sitting). Numbers
read there: what limits RSI speed is verification, "agents produce work far faster than
people and tests can check it"; best automated failure-diagnosis found the responsible
agent 53.5 percent of the time and the failing step 14.2 percent; SWE-bench Pro: "63% of
successful Opus 4.8 Max resolutions retrieved the fix rather than derived it", and
hiding git history plus blocking network dropped the score from 87.1 to 73.0; builder
round count vs final accuracy r = 0.17; CRUX agents scored 2/6 and 1/6, "lacked the
judgment to identify when a problem was adequately solved"; machine-checkable scope is
where AlphaEvolve-style loops compound.

Estate wiring (RQ3 probe-first, RQ5-adjacent): external corroboration that verification
capacity, not generation, is the rate-limiter, and two measured probes for the estate's
own gates. The 87.1-to-73.0 git-history-hidden delta is exactly the P2 contamination
tripwire shape (PORT WAVE, memory/law enforcement trail; duty_fuzz twins vs seen): mask
the contamination channel and measure the score drop. The 53.5/14.2 attribution numbers
say automated attribution is the weak probe, so probe-first verification should target
row-level flags, not root-cause narration.

### 3. NVIDIA: draft eight options, frontier judge picks (Oct 1)

Post: x.com/rohanpaul_ai/status/2105717151453814785 (fxtwitter JSON: Oct 1 2026
17:51Z, 6,669 views). Verbatim: small agent drafts 8 options per step, a strong
frontier model judges before acting; "its success rate jumped from 50% to 68%, no
retraining needed"; when the small model judged its own drafts the gains were much
smaller; "More options don't help much if the judge can't tell them apart."

Estate wiring (RQ3): the paid judge is the multiplier at the SELECT step - draft-wide
plus judge-pick beats self-judge. This does not contradict probe-first; it locates the
judge's irreplaceable step. Cascade shape for register rows: cheap always-on probes
(bank/phenomone traces, deterministic greps) flag rows; the funded judge spends its turn
only on flagged or select steps; judge2 re-look stays for probe-flagged disagreement
(lens/laws.md Q7 judge2, second family). The draft-8-then-judge shape is also a
gauntlet-feed candidate at $0 marginal: gemma:2b drafts, prime judges.

### 4. Memeplexes as the unit that spreads between agents (Sep 10)

Posts: x.com/jachiam0/status/2097919252460400728 (fxtwitter JSON: Sep 10 2026 05:25Z,
81,224 views, 630 bookmarks; argues the transmitting unit between agents is
self-replicating idea bundles, "In a word, memeplexes.", carried by otherwise-functional
agents, and whether "agent" or "memeplex" is the unit of AI behavior is a hard question)
and companion 2097923322814296198 (Sep 10 05:41Z, points at arxiv.org/abs/2608.10218,
Mind Viruses: Self-Propagating Ideas in Multi-Agent LLM Systems, Aug 2026 paper whose X
coverage wave was Aug 19-22, outside this window; the Sep 10 Achiam posts are the
in-window carrier and add the unit-of-analysis frame).

Estate wiring (RQ4 pheromone bus): the pheromone bus (tools/pheromone.py, D7 decay,
Merkle position-bound leaves per the 10-07 PORT/burns record) is exactly a shared
trace medium; the memeplex result says the payload class that propagates through such
media is self-replicating text, so decay plus position-binding is also a quarantine
parameter, not just a correctness one. The estate's contamination tripwire (duty_fuzz)
is the on-box instrument for whether a trace mutates as it propagates; nothing external
in-window measures ordering semantics (the arxiv sibling seat found ZERO stigmergy
feeds in-window), so the p1a L0d confirmation remains estate-instrument-only.

### 5. swarms-rs: multi-agent orchestration moving to Rust (Oct 4)

Post: x.com/KyeGomezB/status/2106770712039968975 (fxtwitter JSON: Oct 4 2026 15:37Z,
1,670 views). Full text verbatim: "Soon everyone will build their agents in rust with
@swarms_corp" (quoting a James Ward post on sentiment shift to Rust). The account-level
swarms-rs claims (6 ms cold start, 3.7 MB memory, MCP integration) came from the SEARCH
RESULT SNIPPET, not from the post text I fetched; banked at reduced confidence with
that provenance declared. Estate wiring: thin, a tooling-direction signal only - if the
local fleet ever re-platforms, orchestration runtime overhead (not model time) is the
cost line the estate's own queueing observations say dominates.

## Overlap gate (grep evidence, run this sitting)

- "Jagged Judges", "2608.12645", "Wiggle": grep -il over catalog/catalog.jsonl and all
  frontier_olm_2026-10-0{3..8} files = ZERO hits. Same-account ArcticSwarm banked day-7
  is a distinct item, not re-banked.
- "SuJinyan6", "Faster Than We Can Check": ZERO hits. "SWE-bench Pro" day-04 hit
  inspected: a MiMo finetuning eval table (44.6 vs 32.0), unrelated to the
  contamination finding banked here.
- NVIDIA judge post: "50% to 68", "draft a few options and let a smart judge" = ZERO
  hits.
- "memeplex", "2608.10218", jachiam0: ZERO register/sweep hits; only noise found: an
  unbanked Reddit harvest cache row (1w63euu, day-05 _raw) and Achiam-name bibliography
  citations inside cached arXiv HTML (q_2609.23587, deep_2610.00928), declared.
- "swarms-rs", "KyeGomezB": ZERO hits.
- A full-tree grep over all of memory/ was started and killed as filesystem-bound; the
  scoped greps above (registers, sweeps, ribs, catalog) are complete and are the verdict
  of record.

## Question verdicts (the ask's five RQs)

- RQ1 width A/B (day-6 dispatch-shape counter-evidence, DIGEST.md:17,:43 band rule):
  NOTHING new externally. The one strong in-window X item (rachittshah, queueing lens,
  "more agent latency in queues, tool calls, and synchronization barriers than in any
  single inference setting") was banked this run by the agent-memory-continuity sibling,
  so I fold only its dispatch delta: hidden serialization and unbounded fan-out are the
  two named failure modes, which is consistent with the 11.7M-request sibling-overlap
  finding already banked. The two-shape A/B (workflow max_concurrency 3 vs Task agents
  10-12) with the 1.25x/1.5x band remains the estate's own owed instrument; no external
  evidence this window contradicts, supersedes, or completes it.
- RQ2 flock decode onto output space: Jagged Judges is the steal: use consensus
  strength as a wiggle-predictor routing signal (high strength flags the re-look), and
  treat judge/convergence surfaces as persuasion attack surface. Dogfood shape for the
  next sweep's review pass: rank rows by review-strength, blind re-look the top-strength
  slice first - it is the ArcticSwarm blind-sweep shape (82.6 vs 63.5, banked) with
  strength as the placement key, and it answers the G2 placement question (which rows go
  under the blind sweep) with a measured external signal.
- RQ3 probe-first replacing the paid judge as first pass: supported, with boundaries.
  External evidence read this sitting: verification capacity is the rate-limiter
  (SuJinyan6); automated attribution is weak (53.5/14.2) so probes flag, they do not
  narrate; the judge's irreplaceable step is SELECT among many options (NVIDIA 50-to-68)
  and second-family re-look; judges are corruptible under pressure (62-91 percent flips)
  and kappa-not-agreement discipline is already banked (sermakarevich, day-7). Cascade
  law stands: probe first pass, funded judge on flagged/select, judge2 only on
  probe-flagged disagreement.
- RQ4 pheromone p1a L0d + MAG_POSITION_BOUND_LEAVES: no external analog in-window
  (arxiv sibling: zero stigmergy feeds; my X census agrees). The memeplex frame
  (item 4) argues decay and position-binding double as propagation quarantine. The L0d
  confirmation at the next natural swarm run stays estate-instrument-only; nothing here
  flips the [a,b,c] vs [a,b,c,c] falsifier question.
- RQ5 G2 enforcement vs latency: no external measurement of gate-latency vs outcome
  quality surfaced. Nearest numbers: round count vs accuracy r = 0.17 (stopping rules
  do not track quality, so more gate rounds is not automatically more quality) and the
  12-point detection floor (banked day-7 via sermakarevich). The two-run scenario-card
  A/B at configs/workflow_gate_scenarios remains the only instrument that can answer it;
  run it before flipping WARN to enforce.

## Door status

X door: statuses resolve clean through api.fxtwitter.com (7 of 7 fetched). X long-form
ARTICLES do not resolve: api.fxtwitter.com/i/article/* returns 404 and x.com serves
"only available on the app"; the SuJinyan6 article body was only readable because the
author mirrors on her own blog. WebSearch backend threw MCP 429 code-1302 storms on
wide batches (2 of my first 4 queries dead, plus scattered later); single-paced queries
recovered. No fallback success is claimed anywhere above; snippet-tier items are named
as such and were not banked as reads.
