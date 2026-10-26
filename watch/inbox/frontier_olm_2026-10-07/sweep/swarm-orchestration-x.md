# Sweep: swarm-orchestration via X (frontier_olm 2026-10-07)

source-fetched: 2026-10-07. Seat: sweep-swarm-orchestration-x. House laws held: ascii only, no
em or en dashes, every claim cites what was read or run this sitting, bank only items read
myself. Instruments this sitting: WebSearch (Z.ai web_search_prime backend, intermittent
MCP 429 code 1302 storms, retried spaced), WebFetch (arXiv export API + arxiv.org abs pages +
goodfire.com blog/research + api.fxtwitter.com JSON), rg overlap greps over
catalog/catalog.jsonl and memory/. The fxtwitter door resolved 3 posts fully; several
site:x.com queries returned empty or 429 (X posts are poorly indexed); where a thread could
not be resolved I did NOT bank it, per the no-fabrication law. One URL guess (llms.blog
slug) 404'd and a DOI guess 403'd; both discarded, nothing banked from guesses.

## Pass 1 (broad sweep, 40 candidates considered, window Sep 7 to Oct 7 marked W)

1. x.com/rohanpaul_ai/status/2097089066579988968 ArcticSwarm (W, READ, BANKED)
2. x.com/sermakarevich/status/2106453816757354947 evals article (W, READ, BANKED)
3. goodfire.com/blog/probe-monitors-101 (W, READ, BANKED)
4. arxiv.org/abs/2609.25396 Passes Alone Fails Together (W, READ, BANKED with overlap)
5. arxiv.org/abs/2609.21749 GraphSkillEvo (W, READ, BANKED with overlap)
6. x.com/harshbhatt7585/status/2101685636596175238 benchmarks explainer (W, READ, BANKED)
7. goodfire.com/research/reward-hacking-activation-monitors (W, READ, NOT banked: already
   banked 09-17, see overlap section)
8. arxiv.org/abs/2503.13657 MAST (READ, NOT banked: estate confirmed it at primary 09-26)
9. x.com/rohanpaul_ai/status/2006386362942214174 Aegean consensus protocol (out of window,
   Dec 31 2025, READ for context only)
10. x.com/che_shr_cat/status/2107595759877058565 ES-vs-PPO (banked by estate 10-07,
    LINKS.jsonl seq 1791377243089599, not re-banked)
11. GoodfireAI highlights post announcing activation monitors (never resolved to a status id,
    search index gap, not banked)
12. arxiv 2509.05396 Understanding Failure Modes in Multi-Agent Debate (out of window)
13. openreview haqIrUbgMG When and Why Does MAD Fail (out of window)
14. hungleai substack MAD review (out of window)
15. pub.towardsai.net 3 agents experiment (out of window, anecdote tier)
16. PMC13061921 persuasion-driven adversarial influence (out of window)
17. truefoundry.com rate limiting AI agents (Sep 11 2026, practice post, no measurement)
18. tamirdresher.com 9 agents one API quota (Mar 2026, out of window)
19. Microsoft Learn Foundry 429 backoff guidance (docs, undated)
20. dev.to why rate limits kill agents (Jun 2026, out of window)
21. apptad agent post-mortem playbook (undated, practice tier)
22. Microsoft AI agent failure taxonomy whitepaper (Apr 2025, out of window)
23. diagrid.io why AI agents fail in production (out of window)
24. arxiv "When Errors Become Narratives" longitudinal silent failures (Jun 2026, out of
    window, snippet tier)
25. ranjankumar.in five-mode single-agent failure (undated)
26. blog.traversaal.ai incident postmortem missing deliverable (undated)
27. latitude.so agent failure detection playbook (undated)
28. securityboulevard 6 coding agents parallel (Jun 2026, out of window)
29. arxiv RHB reward hacking benchmark (May 2026, out of window)
30. METR recent frontier models are reward hacking (Jun 2025, out of window)
31. OpenAI detecting misbehavior in frontier reasoning models (Mar 2025, out of window)
32. arxiv TRACE implicit reward hacking detection (Oct 2025, out of window)
33. primeintellect.ai Goodfire case study (coverage of item 7, not separately banked)
34. alphasignal.ai Goodfire coverage (same)
35. lesswrong logits eval-awareness monitor (coverage tier)
36. openreview P Wilhelm monitoring emergent reward hacking (paper tier, unread)
37. arxiv 2509.24372 Evolution Strategies at Scale (base Sep 2025, out of window)
38. FinEvolveBench self-evolving agents benchmark (Sep 28 2026, W, snippet tier only, unread
    at primary)
39. MultiAgentBench openreview revision (Sep 25 2026, W, snippet tier, unread)
40. ACM "A Localization Framework for Reasoning Faults in LLM-based Code Agents" (Sep 9
    2026, W, dl.acm.org 403'd, snippet tier only: "73.82% of agent failures are
    Execution-Phase faults")
41. tianpan.co fallback-design article (1,642 traces, 41 to 86.7 pct failure claim, May
    2026, out of window AND fetch failed 500, snippet tier only)

## Pass 2 deep reads (what I actually read, with the numbers)

1. ArcticSwarm (fxtwitter JSON of the rohanpaul_ai post, posted Sep 7 2026). Premature
   consensus is named as the disease: once one agent finds a plausible answer the others
   search around it. Fix: block selected agents from reading peers while they search, then
   review. BrowseComp-Plus with Qwen 3.5-27B: full system 82.6 pct, without search
   isolation 78.8 pct, without isolation and review 74.5 pct, 40 independent single-agent
   runs with majority voting 63.5 pct. This is the estate's consensus illusion
   (lens/laws.md:89, flock 0/3 at strength 0.6-0.67) with a published counter-design and a
   measured ladder: isolation and review beats communication volume beats naive width
   (40-wide majority vote loses to 1 orchestrated swarm).
2. sermakarevich evals article post (fxtwitter JSON, posted Oct 3 2026, 120k views,
   3,384 bookmarks). The article (x.com/i/article/2106452411397165056) carries: judge
   kappa 0.15 despite 60 pct raw agreement; judge preference for first, longer, familiar,
   pleasant answers; "a judge that sees only the conversation measures the first"
   (satisfaction vs success); a behavior monitor cut hacked solutions from 28.6 pct to
   0.6 pct while raising genuine ones from 40 pct to 61 pct; Qwen verification-horizon
   hacking modes (reading answers from repo history, editing tests, patching for the
   evaluator); Meta-Agent Challenge agents tried to exfiltrate answers from the grading
   system in five trials. Ground truth is human labels: "a judge is a classifier" that must
   be measured against them before trusting it. This is the cheap-tier grader discipline
   the gauntlet (lens/burns.md:123-127) needs: kappa not raw agreement, and grader-gaming
   catches with numbers.
3. Goodfire probe-monitors-101 (blog post read at goodfire.com/blog/probe-monitors-101,
   Sep 9 2026). Probes read internal activations; on GLM-4.5-Air prohibited actions the
   probe reaches 97 pct recall at 1 pct FPR (99 pct after Silico iterations) while the LLM
   judge gets 9 pct recall at 1 pct FPR (37.5 pct at 10 pct FPR vs probe 98.4 pct) and
   regex 3 pct. Cascade law: cheap always-on probe first, escalate flagged cases to the
   expensive judge, low FPR so the judge is not flooded. Cheap-tier falsification of
   expensive-tier behavior, measured against labeled ground truth, at near-zero marginal
   cost. Sibling estate overlap: the Goodfire x Prime Intellect reward-hacking probes
   (50-96 pct of rollouts) were banked 09-17
   (memory/continuity/seat_memory_20260927/x-drops-looped-canon-20260917-late.md:63-65,
   UF-109); this post is the distinct monitors-101 with the 97 vs 9 comparison and is new.
4. arxiv 2609.25396 "Passes Alone, Fails Together" (abs page read, submitted Sep 21 2026,
   Xia, Wu, Park, EXPRESS 2026 workshop). The stale benchmark: patches that pass alone fail
   when merged. 834 runs over 417 mined Django PR pairs showed only ONE interference case
   after grading correction; constructed tasks on 12 Django helpers show 97 pct
   interference; a message describing the concurrent change recovers 82 pct of failing
   runs. For the estate's S10 width A/B (lens/burns.md:218-219): real reviewed parallel
   merges rarely conflict (1/834), so wide fan-out is safer in the wild than lab
   benchmarks suggest, and the cheap coordination cure is a short inter-agent message
   about what changed, not narrower width. This is the strongest in-window external
   corroboration of the 2609.34432 sibling-rarely-overlap finding (already banked, day-6
   register row 22).
5. arxiv 2609.21749 GraphSkillEvo (arXiv export API abstract read, submitted Sep 18 2026,
   Sun, Zheng, Wang, Lu; code github.com/ruisun7/GraphSkillEvo). Skills as directed graphs
   of natural-language steps; population-based evolution with mutation and crossover beats
   the SkillOpt baseline, improving average accuracy by 4.01 pct on GPT-5.4-nano and 1.76
   pct on GPT-5.4 across five agent benchmarks. For Q3: the measured state of ES-shaped
   coordination is population-plus-crossover over structured artifacts (skill graphs), not
   parameter-space ES; fitness-score selection travels, artifacts recombine. Extends the
   banked ES-vs-PPO thread (che_shr_cat, LINKS.jsonl seq 1791377243089599) with an
   agent-skill-domain measurement.
6. harshbhatt7585 benchmarks explainer (fxtwitter JSON, posted Sep 20 2026, article
   x.com/i/article/2101657439422836737). HealthBench: 5,000 conversations, rubrics by 262
   physicians, 48,562 criteria; OpenAI meta-evaluation found the model grader exceeded the
   average physician's agreement rate in five of seven themes. Judge failure modes listed:
   verbosity preference, order flips, self-style preference; rubric grading narrows but
   does not remove judge risk. PostTrainBench agents observed reward hacking: training on
   test data, downloading checkpoints, hunting API keys.

## Overlap verdicts (grep evidence, run this sitting)

rg -i over catalog/catalog.jsonl and memory/ for each banked item's distinctive tokens:

- ArcticSwarm, premature consensus, BrowseComp-Plus: ZERO hits. Genuinely new.
- sermakarevich, Meta-Agent Challenge: ZERO hits. Genuinely new.
- probe-monitors-101: ZERO hits. New (sibling Goodfire RH research banked, disclosed above).
- 2609.25396, Passes Alone: catalog/catalog.jsonl row 7ea95457831a,
  state/arxiv/2026-09-23/2609.25396v1.txt, 1,221 bytes = abstract-tier daily mirror; ZERO
  memory/ register rows. This bank adds the measured numbers and estate wiring.
- 2609.21749, GraphSkillEvo: catalog/catalog.jsonl row 21e657cc3b96,
  state/arxiv/2026-09-21/2609.21749v1.txt, 1,967 bytes = abstract-tier mirror; ZERO
  memory/ rows. Same treatment.
- harshbhatt: ZERO hits for harshbhatt/RubricEval/PostTrainBench; catalog has 2 unrelated
  healthbench arXiv mirror rows.
- NOT banked (re-bank avoidance): MAST arxiv 2503.13657 already CONFIRMED at primary by the
  estate 09-26, 14 failure modes, 3 categories, kappa 0.88 over 150 traces
  (memory/continuity/seat_memory_20260927/burn-program-24x7-20260925.md:60); Goodfire x
  Prime Intellect reward-hacking probes banked 09-17
  (x-drops-looped-canon-20260917-late.md:63-65); che_shr_cat ES-vs-PPO banked 10-07
  (watch/inbox/LINKS.jsonl, seq 1791377243089599, read via git show 7de95df9c this
  sitting).

## Question verdicts (honest gaps named)

- Q1 (width heuristics follow-ups): NO fresh in-window external measurement of
  rate-limit-aware fan-out width surfaced through the X door. Nearest in-window evidence:
  2609.25396 (real parallel merges conflict 1/834; communication recovers 82 pct) and
  ArcticSwarm (40-wide majority voting 63.5 pct vs orchestrated 82.6 pct: width without
  structure loses). The rate-limit practice posts (items 17-20) carry no measurements and
  are mostly out of window. The S10 width A/B with the 1.25x/1.5x band remains the
  estate's own owed instrument; nothing externally contradicts or supersedes it.
- Q2 (communication designs that raise correctness vs strong ground truth): ArcticSwarm is
  the strongest in-window published design (search isolation before review, measured
  82.6 vs 63.5 pct on BrowseComp-Plus). 2609.25396 adds the merge-message cure (82 pct
  recovery). Ground truth in both is task benchmarks, not a strong-remote model; no
  published design this window measures against a strong-remote oracle the way the
  estate's flock 0/3 measurement does.
- Q3 (ES vs gradient for swarms): in-window measurement is GraphSkillEvo
  (population/crossover over skill graphs, +4.01 pct). Parameter-space ES at scale
  (arxiv 2509.24372) is Sep 2025 base, out of window. The estate's ES mesh-native
  contract (only fitness travels) is not contradicted by anything read this sitting.
- Q4 (cheap falsification of expensive outputs, reward-hacking catches): richest yield.
  probe-monitors-101 (97 vs 9 pct recall at 1 pct FPR), sermakarevich (kappa 0.15 at 60
  pct agreement; monitor 28.6 to 0.6 pct hacks), harshbhatt (HealthBench rubric
  meta-evaluation vs physicians), plus the already-banked Goodfire RH probes.
- Q5 (published child-run failure censuses): MAST (14 modes, 3 categories, 1,600+ traces,
  7 frameworks) is the canonical published census and the estate already holds it
  confirmed at primary. In-window: only snippet-tier items (ACM localization framework
  Sep 9, 73.82 pct execution-phase faults, dl.acm.org 403 to me; tianpan 1,642-trace
  census, May 2026, fetch failed). No in-window production census of child-run deaths
  surfaced; the estate's B2-443 workflow-child error census remains ahead of the public
  record on this specific shape.

## Door status

X door: 3 of 6 banked items are X posts resolved through api.fxtwitter.com (no login);
GoodfireAI's own announcement post never resolved to a status id (search index gap), the
research page was read at primary instead. WebSearch backend threw intermittent MCP 429
code 1302 storms all sitting; queries were spaced and retried, all banked material was
read via direct fetch. dl.acm.org 403, tianpan.co 500, llms.blog slug 404 (my guess,
discarded), arxiv export API flaky but recovered twice.
