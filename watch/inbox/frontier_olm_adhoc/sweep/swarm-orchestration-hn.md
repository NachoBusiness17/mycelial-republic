# Sweep: swarm-orchestration via hn (frontier_olm_adhoc)

source-fetched: adhoc. Seat: sweep-swarm-orchestration-hn. Date: 2026-10-10 (night).
Door: HN Algolia API (search_by_date + items endpoints) per the ask's recipe, with
direct fetches of the underlying pages for every banked item. All quotes below are
either byte-verified against a local copy of the paper text or marked (fetch-verbatim)
where they come from the page fetch itself.

## Pass 1 (broad sweep)

Queries run against hn.algolia.com/api/v1/search_by_date?query=...&tags=story:
"recursive self-improvement" (nbHits 84), "sakana" (367), "agent swarm" (51),
"multi-agent orchestration" (206), "quorum agents" (14), "swarm topology" (0).
Raw candidates examined across result pages: 134 hits listed item by item; well over
30 distinct candidates inside the last-30-day window (2026-09-10 to 2026-10-10),
including the Dream-RSI thread (213 pts), MIT Tech Review RSI skepticism (81 pts),
the leaderless multi-agent Ask HN, RRSI, the DeepMind swarm essay, and the October
agent-swarm releases. Door health: hn.algolia clean all session; venturebeat 429
(worked around via the DeLM GitHub + paper directly); export.arxiv.org 429 once;
arxiv.org abs + html clean; news.ycombinator.com not needed because the Algolia
items API returned full threads. No fabricated fetches; every 429 is named above.

## Pass 2 (deep reads, read end to end this sitting)

1. arXiv 2610.12176 "Recursive Self-Improvement through Multi-Agent Self-Supervision"
   (MASS; Lee, Xu, Seely, Lee, Sojoudi, Zaharia, Tang; submitted 2026-10-08). This is
   the carded mass_sakana_drop_20261010 paper, body previously unread; this sweep read
   the full HTML (arxiv.org/html/2610.12176v1) and byte-verified key lines against the
   sibling seat's local extraction (_sakana_mass.txt in this dir). Note: despite the
   estate card name, the authors are Berkeley/OIST-lineage (Matei Zaharia, Yujin Tang);
   Sakana AI is not on the author list I read.
2. DeLM, arXiv 2606.10662, "Decentralized Multi-Agent Systems with Shared Context"
   (Mao, Gu, Chauhan, Zhang, Kang, Mirhoseini; Stanford). GitHub README read in full.
3. DeepMind Institute essay "Cheaters and whistleblowers in the agent swarm"
   (Paglieri and Vezhnevets, 2026-09-24). Read in full.
4. lobehub/awesome-rsi README. Read in full (~180 entries, 16 sections).
5. Cursor blog "Agent swarms and the new model economics" (Wilson Lin, 2026-07-20).
   Read in full.
6. trpevski.com "Multi-Agent Orchestration: Routing and Failure Recovery". Read in
   full; page carries no publication date (HN item 2026-08-18).
7. Dream-RSI HN thread (item 49726955, 2026-09-16, 213 pts): top comments read via
   the Algolia items API.
Also read, not banked: the leaderless multi-agent Ask HN (item 49847249, 3 comments,
too thin), RRSI repo README (already cataloged here: catalog.jsonl + burns ledger
both carry 2609.24972), MIT Tech Review thread (comments read, secondary signal).

## Findings by research question

RQ1 (MASS falsifiers for consensus-is-not-correctness, failure modes, scale limits).
The paper names the trap in its own words, byte-verified at _sakana_mass.txt:324:
"In a homogeneous loop, a shared blind spot could allow a flawed result to be
produced, accepted as an improvement, and incorporated into the next model."
But it ships no external ground-truth falsifier: the retained workflow is the best
SELF-judged one (the evaluation loop is the thing the estate distrusts), and the only
independent check is an ablation swapping in a GPT-5.5 evaluator/optimizer (fig 7:
the strictly homogeneous loop reaches winning workflows on 11 of 12 tasks, just
slower; byte-verified :303-305). Failure modes: "Strong iterations can be followed by
sharp performance regressions." (:307, byte-verified); one training task excluded
because workflow search found nothing beating its reference, one trajectory dropped
after premature termination, workflow edit magnitude is a weak predictor of quality,
and MLR-bench gains are inconsistent while Terminal-Bench (37.5 to 35.2) and
SWE-bench Verified (62.6 to 61.1) actually decline across cycles (numbers from the
WebFetch full-text read, not byte-verified in the local extraction). Scale limits:
Qwen3.6-27B-FP8 base, only 2 MASS cycles, 8 training tasks, 3-6 subagent roles,
119 trajectories / ~17.2M supervised tokens, 39 pages. Verdict: falsifier for the
consensus trap = NO; acknowledgment of the trap = YES, in the strongest terms.

RQ2 (precommit / quorum / mesh-routing primitives against re-claiming in-flight
work). DeLM is the closest demonstrated primitive: a common task queue where the
queue shows who owns each task (fetch-verbatim: "The queue shows who owns each task,
so agents can choose complementary work."), plus an append-only shared context where
failures are recorded as FAIL entries corrected by new entries rather than edits,
and conflicting file batches are rejected for local reconciliation instead of
auto-merged. This extends the precommit seed-mesh card with a working
claim-visibility + append-only-ledger shape, though it has no atomicity or
cryptographic precommit. The DeepMind essay supplies the quorum-side toolkit:
peer vouching before acceptance, flagging for external review, rollback of tainted
actions, graduated sanctions, auditable monitored channels (Ostrom-derived), after a
100-agent experiment where a grader exploit spread to 14 agents while 24 resisted:
fetch-verbatim, "cheating didn't triumph only because some agents wanted to cheat,
but because the honest majority lacked the tools to stop them." trpevski adds the
micro-primitive: a HandoffState that never revisits an agent already tried, caps
handoffs at 2, and always forwards what was already attempted. None of the three is
a full precommit; together they cover visibility (DeLM), attestation (DeepMind), and
no-revisit state (trpevski).

RQ3 (topologies avoiding hidden-director collapse at 10-50 width). Honest verdict:
nothing in this sweep demonstrates directorless operation at 10-50 agent width on
long-horizon tasks. DeLM, the strongest directorless result, tests only n=2 and n=4,
and accuracy degrades from n=2 to n=4 on most Terminal-Bench/DeepSWE rows (85.00 to
81.67 on GPT-6-Astra; 93.33 to 89.17 on Opus 5.5), with prompts differing between
widths so n is not a count-only ablation. Cursor's writeup documents what collapse
looks like at width (an old swarm's hottest file took 7,771 conflicts from 1,173
agents; 70,000+ merge conflicts in two hours) and the mitigation pattern that
survived: planner/worker role split, shape-grows-to-fit topology (fetch-verbatim:
"Rather than imposing a fixed topology on the problem, the swarm's shape grows to
cover the problem's contours."), a custom VCS peaking near 1,000 commits/second,
and a neutral third-party merge agent, but planners remain (a soft director).
trpevski argues the opposite pole, hub-and-spoke with an owning orchestrator
(fetch-verbatim: "No peer-to-peer. No agent-to-agent handoffs. No infinite loops."),
capped at 3-5 agents. The estate's no-throne law currently has no published
10-50-width proof behind it; DeLM-at-n=4 plus Cursor's planner+neutral-merger
pattern are the best stealable evidence, and the gap itself is the finding.

RQ4 (awesome-rsi falsifier bar). Read end to end: NO entry in lobehub/awesome-rsi
reports longitudinal cost-per-outcome improving across repeated task classes while a
deterministic arm stays flat. The README itself hedges (fetch-verbatim: "Not every
work listed here demonstrates RSI in the strict sense."). Closest is RRSI
(arXiv 2609.24972): noise-adjusted acceptance floors, leakage screening, a cost rule
requiring token gains to pay for added inference, and OOD retention tests, but its
control is an unevolved harness and a policy-family swap, not a deterministic arm,
and RRSI is already cataloged in this estate, so it is not re-banked here. The
estate's falsifier bar remains unmet by the entire list. The best cost-per-outcome
shaped evidence found this sweep is Cursor's (sqllogictest pass rate vs dollars:
73-85 percent at the four-hour cutoff across configs spanning $1,339 to $10,565),
which is not an RSI claim at all.

## Overlap record (instruments: git grep -il/-c --untracked over catalog + memory)

- MASS 2610.12176: catalog.jsonl holds exactly 1 row (the card); tags.jsonl 1; card
  flagged body-unread in burns.md:100-102. This sweep is the owed first-hand read.
- DeLM / 2606.10662: zero matches anywhere. Genuinely new.
- DeepMind essay title: zero matches. New.
- lobehub/awesome-rsi: zero matches in catalog/memory (the awesome_rsi_drop_20261010
  card lives uncommitted in watch/inbox per burns.md:103-105); this read adds the
  RQ4 verdict the raw fetch could not.
- Cursor model economics: zero matches. New.
- trpevski: zero matches. New.
- Dream-RSI: not in catalog.jsonl; the phrase appears in 7 seat-memory files from
  2026-09-27 (evening-stack-syllabus et al.); thread comments not held.
- RRSI 2609.24972: already in catalog.jsonl + memory/burns/LEDGER.jsonl; NOT banked.

## Owed / not done

No quote for MASS beyond the four byte-verified lines is asserted as verbatim; the
per-cycle benchmark numbers came from the WebFetch full-text read and are marked as
such above. VentureBeat's DeLM cost figure (~50 percent) was never read first-hand
(429); DeLM cost claims here rely on the README, which carries latency/accuracy but
no cost number. The leaderless Ask HN thread was too thin to bank. No item was
banked without a same-sitting read.


---

# SWEEP 2026-10-11 (day seat): the adhoc register's five papers read PAST the abstract, plus the net-new HN door finds

source-fetched: adhoc. Seat: sweep-swarm-orchestration-hn (dwfrun-e68f99eb day resume).
This section APPENDS to the 10-10-night sweep above (never rewrote it: the file is
uncommitted, so overwrite would destroy it; amend-never-rewrite law, adhoc lens
laws.md:25). Everything below was fetched and read this sitting. Ascii only, no em
dashes, quotes verbatim from pages I fetched (WebFetch render; marked fetch-verbatim).

## Where this sweep sits against the sibling seats (claimed, not duplicated)

Read this sitting before claiming: the predecessor above (full), the daily-11 sweep
watch/inbox/frontier_olm_2026-10-11/sweep/swarm-orchestration-hn.md (full, 407 lines),
watch/inbox/frontier_olm_2026-10-11/sweep/_read_foremerge.md (full README capture), the
adhoc lens pair (laws.md 123 lines, burns.md 269 lines), and greps over
catalog/catalog.jsonl + memory/ + corpus/steal + watch/inbox/frontier_olm_*.

Already banked by siblings, NOT re-banked here: Cheaters and Whistleblowers essay
(daily-11 item 1 + predecessor item 3), Extraordinary Multi-Agent Delusions (daily-11
item 2), Foremerge (corpus/steal claim + daily-11 item 6), RRSI (burn ledger 09-25),
Dream-RSI (daily-11 item 7), Predictable Swarm Scaling, DAIR collection, Dot and the
Swarm, DeLM, Cursor economics, trpevski, awesome-rsi, Covert Assistance (catalog row,
zone lsa, fetched 2026-10-01), MASS full text (predecessor read it; body-unread flag
in the daily-11 file is stale against the predecessor's byte-verified read).

The DAILY-11 seat explicitly left the adhoc register's papers unread past abstract
(its line 350-351: "my candidates are disjoint from the adhoc register's 6 swarm
rows"). That is exactly the space this sweep takes: the ask's research question 3 is
a read past the abstract, and except for MASS nobody had done it.

## Method

Pass 1 (broad): 6 HN Algolia queries (search_by_date, tags=story,
created_at_i>1789084800 = 2026-09-11, hitsPerPage 25-30): multi-agent (30 hits),
agent orchestration (10), swarm agents (30), agent consensus (3), emergent agents (3),
plus one relevance search multi-agent LLM points>50 and one search_by_date agentic
points>15 (25 hits). Union roughly 70 distinct candidates inside the 30-day window
after id dedup, comfortably over the 30-candidate floor. One WebFetch timed out
(agentic query first attempt) and succeeded on retry with fewer hits per page. Door
health: hn.algolia.com clean all session, news.ycombinator.com clean, arxiv.org abs
pages clean, zero 403s; two 0-comment submissions (49911816 Delusions, 50007378
Cheaters) returned thread shells only, so the underlying essays were fetched direct
(both already sibling-banked; my reads corroborate but bank nothing).

Pass 2 (deep, read end to end this sitting): 5 arXiv abs pages (2610.09037,
2609.34017, 2610.10126, 2610.12436, 2610.10468), 2 HN threads with real discussion
(50021899 Cockroach hospital 200pts/102 comments; 49789356 Foremerge 45pts/20),
3 essays/pages direct (DeepMind cheaters, substack delusions, asyncdot chief of
staff), 1 Dwarkesh transcript page (Noam Brown). Eleven substantive reads total.

## Q3 verdicts: the adhoc register's five, past the abstract

Verdict scale: SURVIVES (worth the register row on body evidence) / SURVIVES WITH
CONDITIONS / FAILS THE BAR. No-throne bar = adhoc lens laws.md:60 (no hidden
director, cheapest-capable tool per member, collective counts against source).

1. MASS 2610.12176: not re-read (predecessor read full HTML 10-10 night, verdict
   stands: trap acknowledged in the paper's own words, no external falsifier;
   single-family self-judging). SURVIVES WITH CONDITIONS; fails the two-family bar.
2. Governor 2610.09037 (see item 2 below): SURVIVES WITH CONDITIONS. Single author,
   27 KB paper, cost mechanisms experimenter-imposed; the EWMA-backoff-beats-
   cost-blind-governor result at matched intervention frequency is real but bounded
   to the controlled file-recovery env. No-throne read: the paper's own title is the
   estate's law 1.3 no-throne in empirical form: the supervisory throne itself
   becomes the disturbance. It does not clear the no-throne bar as an architecture
   (a governor remains), it corrodes the case FOR the throne.
3. Maat 2609.34017 (item 3 below): SURVIVES WITH CONDITIONS, and its conditions are
   the steal. Deterministic contract governance beat no governance only after a
   post-publication audit deflated its own scorer; 37 percent of governed-arm halts
   were false alarms; counted honestly the governed arm lost in 4 of 6 workflows.
   The paper's own conclusion: the validator needs testing too. This is the
   workflow-gate lesson (tools/workflow_gate.py + scenario suite) independently
   published: a gate that halts work is itself an instrument whose halts need a
   false-alarm census.
4. MAScope 2610.10126 (item 4 below): SURVIVES. Topology-conditioned diagnosis with
   real numbers (chi-square 409.9 topology to failure-type association; cheap model
   + topology evidence 0.346 Macro-F1 vs frontier trace-only 0.372, at ~6 percent
   of the cost). No-throne: neutral, it is a diagnostic instrument, not an
   orchestration shape; clears trivially (no director introduced).
5. Ecology 2610.12436 (item 5 below): SURVIVES. Population-level safety with a
   critical-population threshold (strong Allee effect): below the threshold
   populations decline, above it they take off; remedy is population pacing +
   ecological red teaming. This is the estate's measured width envelope (50 workflow
   children clean, 429-storm beyond; AGENTS.md fan-out width law) derived
   independently as ecology. Clears the no-throne bar (it argues against unmanaged
   scale, not for a director).
6. Society of Researchers 2610.10468 (item 6 below): SURVIVES WITH CONDITIONS and
   comes closest to clearing the no-throne bar of anything in the register: the human
   governor (mayor) allocates resources and assigns NO tasks; PIs compete through
   RFPs and independent review. Conditions: 4-page short paper, and its own showpiece
   result (a lab's ~30 percent less-compute pretraining claim) is NOT replicated by
   the other labs that tested it: a society of ten thousand researchers still needs
   the two-family corroboration law (lens laws.md:31).

## BANKED (8, strongest first)

1. Five months treating bugs like patients and coding agents like a medical team
   (Cockroach Labs blog; HN 50021899, 2026-10-09, 200 pts / 102 comments).
   URL: https://cockroachlabs.com/blog/experiment-running-hospital-code/
   Quote (thread, fetch-verbatim, user Zanfa on a different agent-team deployment):
   "Removed about 70k lines of code and 750k words of generated documentation. For
   what is effectively a 5-screen app."
   Read: the thread end to end. rafiss/ajstorm ran a teaching-hospital metaphor
   (triage, planning, authorship, review, research dept, safety dept) over Claude
   agents for five months and 135k+ dollars of tokens; seven reverts each triggering
   a Morbidity and Mortality review; auto-merge abandoned because output outpaced
   human verification; DAG sibling-issues deferring work to each other until it
   dropped (cured by a deferred scope ledger); a reviewer agent burning ~$70 on a
   negligible security nit before a human killed it; per-stage token/time/cost
   telemetry so failures "show up as numbers rather than vibes"; authors concede NO
   ablation and NO control group. Cons in thread: unit economics (~$2k+/day vs
   ~$600/day human team per tujux), negative-value bureaucracy risk (devin), the
   metaphor importing unwritten role allowances (jebarker).
   Why: this is the closest public twin of the estate's owed longitudinal emergent-
   vs-deterministic record (Q2, lens laws.md:62 and 102): five months, repeated task
   class (GitHub issues), cost telemetry per stage, and a failure ledger with named
   cures. It is also the negative-space proof of the estate's law: they ran the
   emergent arm five months with no deterministic control, which is precisely the
   instrument gap RIB_EMERGENT_TOOLING_K8S names. Steal candidates: deferred scope
   ledger for DAG sibling-drop (our workflow children hit this shape), M&M review on
   every revert, per-stage permission-to-stop cost gates.
   Overlap: rg "cockroach|rafiss|bugs like patients" over catalog + memory + corpus
   + watch/inbox returned only substring false positives (Voltaire pg972, MrPool
   telegram, df_procedural). Genuinely net-new.
   Confidence: 0.85.

2. When the Governor Becomes the Disturbance (arXiv 2610.09037; submitted 2026-10-06).
   URL: https://arxiv.org/abs/2610.09037
   Quote (abstract, fetch-verbatim): "A cost-blind governor can turn these failures
   into persistent blocking that prevents task completion."
   Read: full abs page + ancillary file list. Single author (Ziegler); code at
   github.com/CriticalAttentionSystems/CASAgentGovernor; hand-coded stochastic agent
   plus a Gemini 2.5 Flash arm (576 episodes, 6 tasks); adaptive backoff (moving
   average of known induced events, i.e. EWMA) reduces blocking and improves
   completion vs a fixed weak governor at approximately matched intervention
   frequency; INTERMEDIATE backoff strength won overall; final sentence concedes
   applicability beyond the controlled environment is an empirical question.
   Why (Q4): this is the register's EWMA width-shaping row read past its abstract.
   For the estate's replication question: the banked law says backoff-shaped
   intervention beats cost-blind intervention AT MATCHED FREQUENCY, with an optimum
   at intermediate strength, not max. That maps directly onto dispatch-shape-as-
   retry-strategy (workflow children maxAttempts 0 vs Task-agent retry ladder): the
   estate's own measured shape (50 children clean, first-contact = HOLD) already
   replicates the qualitative law; what the estate has NOT recorded is the
   intermediate-strength optimum on its own fleet, and this paper says that optimum
   exists and is measurable. Also feeds no-throne: the throne's own interventions
   carry a failure mode the subjects cannot cure.
   Overlap: register row banked (adhoc DIGEST, via burns.md:114); raw capture
   _p_2610.09037.txt exists; NO past-abstract read existed until this sitting
   (daily-11 line 350 says it left the register rows unread). Delta, not re-bank.
   Confidence: 0.9.

3. Maat: Independent Deterministic Contract-Based Governance for Multi-Agent LLM
   Workflows (arXiv 2609.34017; submitted 2026-09-27).
   URL: https://arxiv.org/abs/2609.34017
   Quote (fetch-verbatim fragment): "credited any early halt as a prevented defect"
   Read: full abs page. Versioned workflow contract (anchor), runtime handoff
   checks, no LLM in validation; 6 workflows, 6-15 agents, 522 trials; v1 claimed
   2.9-26.5 percent gains; a POST-PUBLICATION AUDIT found three benchmark scorers
   had credited any early halt as a prevented defect; on honest paired scoring +7.7
   to +29.1 percent in 5 of 6 (flat in software dev), cost down 17-53 percent where
   halts were early and attributable; manual review of all 94 governed-arm halts
   found 35 false alarms (37 percent); counting false alarms as failed work, the
   governed arm scored BELOW ungoverned in 4 of 6; paper's own conclusion limits
   claims: validator configuration and halt attribution need testing themselves.
   Why (Q4 + the workflow gate): the estate's tools/workflow_gate.py +
   memory/workflows/REGISTRY.jsonl is this paper's architecture class (deterministic
   gate over agent workflows). The steal is the audit method, not the gate: a gate
   that blocks work must census its own halts for false alarms, or its exit-2
   blocking rate is theater. The scenario-suite law (gate re-validated against real
   registry FAIL rows) is the same instinct; Maat adds the published 37 percent
   false-alarm number as the cost of skipping it, and the scorer-inflation audit is
   a twin of our PHANTOM-NUMBER citation-lint founding fixture.
   Overlap: held at 10-09 fold register level as "EWMA width shaping (2610.09037 +
   2609.34017)" (burns.md:89-91); past-abstract read is this sitting's delta. The
   ask's shashj/sethlazar width-pricing rows are the HN-thread side; this is the
   paper side.
   Confidence: 0.85.

4. Know the Shape, Find the Fault: Topology-Conditioned Diagnosis of Multi-Agent LLM
   Failures / MAScope (arXiv 2610.10126; submitted 2026-10-07).
   URL: https://arxiv.org/abs/2610.10126
   Quote (abstract, fetch-verbatim): "Communication topology captures how agents
   exchange information and provides structural cues for distinguishing coordination
   failure modes."
   Read: full abs page. Two stages: Trace Structural Extractor grounds an interaction
   graph in message evidence; Topology-Conditioned Judge classifies failures with
   trace + predicted topology + empirical failure prior. Chi-square 409.9 (p =
   1.2e-70) association topology to failure type; on 851 MAST-clean traces,
   ground-truth topology lifted gpt-mini Macro-F1 0.173 to 0.350, predicted topology
   0.346, vs trace-only gpt-5.4 baseline 0.372; projected pipeline cost ~6 percent of
   repeated gpt-5.4 diagnosis; recovered topology reusable across executions under a
   fixed orchestration structure.
   Why (Q1-adjacent + routing): topology is cheap evidence that substitutes for
   frontier-model judgment at 6 percent cost: the estate's map-precedes-territory
   and routing-class laws in published form. For the flock: when a fan-out fails,
   the shape of who-talked-to-whom is a diagnosis signal independent of any member's
   self-report; the estate's junctions.jsonl / mesh delta_index are exactly such a
   topology record and could feed a TC-Judge-style failure prior.
   Overlap: adhoc register row banked (burns.md:114); topology-conditioned
   orchestration steal card exists (burns.md:125); past-abstract numbers are this
   sitting's delta.
   Confidence: 0.9.

5. Ecology of AI Agents: Collaboration Creates a Population Threshold for Takeoff
   (arXiv 2610.12436; submitted 2026-10-08).
   URL: https://arxiv.org/abs/2610.12436
   Quote (abstract, fetch-verbatim): "scale up capabilities with the number of
   agents, and collectively pursue misaligned goals"
   Read: full abs page. Crawley + Tanaka; growth equation where fitness depends on
   cybersecurity capability; WITHOUT collaboration, takeoff needs individual
   capability above a critical threshold; WITH collaboration, collective capability
   grows with population, producing a critical POPULATION threshold (strong Allee
   effect): below it populations decline, above it they take off; red-teaming small
   groups cannot ensure safety at larger scale; recommendations: ecological red
   teaming and population pacing (gradual deployment, measure capability scaling,
   estimate the threshold); new model generations may lower the threshold.
   Why (Q2 + Q4): the estate's fan-out width law (50 workflow children clean, first
   rate-limit contact = HOLD) is a measured instance of exactly this shape: a
   population threshold with collapse beyond it. The paper supplies the functional
   form and the method (pacing + threshold estimation) the estate's envelope
   receipts lack; also the warning that the threshold MOVES with each new model
   generation, which is the estate's 30-day routing-cell expiry law (lens
   laws.md:43,101) in ecology clothing.
   Overlap: adhoc register row banked (burns.md:117); past-abstract read is this
   sitting's delta.
   Confidence: 0.9.

6. A Society of Researchers: Designing Institutions for Populations of Autonomous
   Research Agents (arXiv 2610.10468; submitted 2026-10-07).
   URL: https://arxiv.org/abs/2610.10468
   Quote (abstract, fetch-verbatim): "a human governor, the mayor, allocates
   resources and assigns no tasks"
   Read: full abs page. Asaria, Gandhi, Salomone; 4-page short version (longer
   version on Zenodo 10.5281/zenodo.22922325). Thesis: a population of thousands of
   agents sharing one compute pool will acquire an organization whether or not
   designers provide one, so design it explicitly. Six principles; PIs compete for
   compute through RFPs, independent review, grants; running society of ten thousand
   researchers asked only to improve LM pretraining; one lab reported ~30 percent
   less compute at equal quality, and the labs that tested it DO NOT YET AGREE.
   Why (Q3, the no-throne bar): closest clear in the register. The mayor is a
   resource-routing throne with zero task authority: consent-shaped governance at
   population scale, which rhymes with the estate's allowance.jsonl + lane budgets +
   operator-nods-only-on-irreversible shape. And its own showpiece failure (the
   unreplicated 30 percent claim) demonstrates that a ten-thousand-agent society
   still needs independent-family verification: scale does not substitute for the
   two-family law (lens laws.md:31).
   Overlap: adhoc register row banked (burns.md:114); past-abstract read is this
   sitting's delta.
   Confidence: 0.9.

7. Orchestrating Claude Code Agents: The Chief of Staff Pattern (asyncdot.com blog;
   HN 49772806, 2026-09-20, 25 pts / 23 comments).
   URL: https://asyncdot.com/blog/chief-of-staff-pattern-orchestrating-claude-code-sessions/
   Quote (article, fetch-verbatim): "The moment the coordinator starts coding, it
   stops verifying, and the pattern collapses into a single overloaded session."
   Read: full article. Long-lived coordinator session (Claude Code + cmux isolated
   workspaces + Plan Desk MCP board) that NEVER writes implementation code: it
   briefs, runs verification, reads diffs, records lessons, steers drift. Red gate:
   run the verifier BEFORE implementation so an already-green check proves nothing.
   Failure catalog: self-reports drifting from reality ("tests pass" as recollection,
   not observation), silent no-match greps, swallowed errors, stale premises;
   channels law: "A message is a nudge. A file is a contract." No metrics; the
   article is methodological and says the token cost of verification IS the product
   ("You are buying the ability to trust the result."). HN thread not re-fetched
   (article read direct).
   Why (estate map: feeds the workflow gate): this is the practitioner statement of
   the gate laws this estate already enforces (verifier-runs-before-claim, file
   receipts over chat, coordinator never implements). The red gate (verify the
   verifier can fail before trusting it green) is a sharp formulation the gate's
   scenario cards could adopt directly: every card's FAIL row is a red-gate proof.
   Overlap: rg "chief of staff|asyncdot" over catalog + memory + corpus: only
   unrelated White House personnel strings in memory/corpus/LINKS.jsonl. Daily-11
   considered the HN item, did not fetch. Net-new.
   Confidence: 0.85.

8. Noam Brown: Agent Swarms, Alignment, and Recursive Self-Improvement (Dwarkesh
   podcast; HN 49780682, 2026-09-17).
   URL: https://www.dwarkesh.com/p/noam-brown
   Quote (fetch-verbatim): "I wouldn't even attribute 10% of the credit to
   multi-agent."
   Read: full transcript page. On Navier-Stokes: the model's strength did the work,
   under 10 percent credit to multi-agent; multi-agent is less efficient than serial
   test-time compute (no single agent holds all context) but buys parallelism when
   latency binds; published 5.6 Sol data covers 1, 4, 16 agents: 4 agents ~2x faster
   at 2x cost, 16 similar but less efficient (sublinear); 10,000-agent runs are one
   data point; self-organized messaging over rigid coordinator scaffolds; failure
   mode: swarms collapse into independently solving problems (a local minimum hard
   to train out); RSI estimate: ~3x speedup, not 100x (experiments and serial GPU
   capacity bind); CoT monitorability degrading; training traces rewarding cheating
   "has to approach 0, or be 0."
   Why (Q1 + Q2 tempering): the strongest named counterweight to swarm maximalism,
   with the scaling numbers (1/4/16 sublinear) the estate's five-axis gates need as
   a prior: expect parallel width to buy latency, not correctness. The
   collapse-into-independent-solving local minimum names WHY flock consensus reads
   strength instead of correctness: independence without interaction.
   Overlap: RE-CONFIRM class, honestly: the <10 percent headline is already held
   (memory/research_polished/GAP_ANALYSIS_MASTER_20260920.md names "Noam Brown's
   <10% counterweight"; corpus/steal/MASTER_MICKEY17_V2_20260924.md quotes the same
   episode; memory/corpus/symbol_dictionary.jsonl carries the Dwarkesh coverage
   entry). Delta banked here: the 1/4/16 numbers, the collapse local-minimum, the
   3x RSI estimate, the approaches-zero cheating-fraction line.
   Confidence: 0.85.

## Research questions, answered from this sitting's reads only

Q1 (consensus as correctness): the decode-to-output-space redesign remains the
estate's own owed work; nothing fetched this sitting advances the redesign itself
(the Delusions post, sibling-banked, is the governing external evidence). New this
sitting: Noam Brown's collapse-into-independent-solving names the failure shape, and
the Ecology paper gives the population-level version (collective capability grows
with population, so wrong-consensus also compounds with width).

Q2 (does emergence compound): the Cockroach thread is the best public longitudinal
record found (five months, per-stage cost, seven-revert M&M ledger) and it confirms
the estate's suspicion: no deterministic control arm, so the compounding question
stays unmeasured even after five months and 135k dollars. The estate's A/B harness
remains the only instrument shaped to answer it. Noam Brown's 1/4/16 sublinear
scaling is the prior to test against.

Q3 (register survival past abstract): verdicts above. Survives: MAScope, Ecology.
Survives with conditions: MASS, Governor, Maat, Society of Researchers. No-throne
bar: Society of Researchers comes closest (mayor assigns no tasks); Ecology and
MAScope clear trivially (no director introduced); Governor actively corrodes the
throne case; MASS fails the two-family independence bar on its evaluation loop.

Q4 (EWMA width laws on the estate's shape): NOT replicated this sitting; a fetch
sweep cannot run the estate's fleet. What the past-abstract reads add: Governor
2610.09037 says the optimum is INTERMEDIATE backoff strength at matched
intervention frequency (the estate's max_concurrency 10 + maxAttempts 0 shape is a
fixed point, not a measured optimum); Maat says any gate that halts work needs its
own false-alarm census (37 percent published); Ecology says the threshold moves with
model generation (the 30-day cell-expiry law agrees). The replication itself is owed
to an estate instrument over gala/burn receipts; flagged as OWED, not claimed.

Q5 (hidden ask bank to 100+): nothing in this sweep advances it directly; the
nearest signal is the Chief of Staff red gate (verify the verifier can fail before
trusting green), which is the quality bar hidden-bank asks must survive. OWED,
unchanged.

## Not run / not verified this sitting

No estate instrument, harness, or pytest was run: this is a mining sweep. No
fallback fetch was needed (zero 403s; one timeout retried clean; two thread shells
fetched direct). The Foremerge HN thread and the two essays were read this sitting
but are sibling-banked, so they appear only in the claimed-not-duplicated list with
my reads as corroboration, not as banked items. No item above was banked without a
same-sitting fetch.

