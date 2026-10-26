# Sweep: evals-self-improvement via arxiv - 2026-10-11 (run 2, amended)

source-fetched: adhoc

Door: arXiv (export.arxiv.org Atom API for pass 1; arxiv.org/abs pages for pass 2) via
WebFetch. Door status, disclosed: single sequential calls answer reliably; a 2-way
parallel call timed out at 60s twice-for-two at session start and one later query
(organizational memory) also timed out once. No 403s anywhere. Shape law for this door:
serialize the calls. No fallback door was needed, so none is claimed.

This file supersedes the same-path mint written 2026-10-11T01:18 by the prior adhoc run's
actor (preserved byte-identical as evals-self-improvement-arxiv.prior-2026-10-11T0118.md,
13,446 bytes; that file banked 2610.11116, 2610.12083, 2609.33044, 2609.34320, 2609.27176,
2610.10263, 2610.05140, 2609.37362 - all eight are estate holdings now and none are
re-banked here). A third same-lane sibling exists and was read in full this session:
watch/inbox/frontier_olm_2026-10-11/sweep/evals-self-improvement-arxiv.md (10,437 bytes,
8 items: 2610.08902, 2610.11647, 2610.09239, 2610.11655, 2610.11464, 2610.04829,
2610.09008, 2610.09229 - zero collision with this bank).

## Pass 1 (broad)

13 API queries against https://export.arxiv.org/api/query with
submittedDate:[202609110000 TO 202610112359] preference (sortBy submittedDate desc):
(1) abs:"failure attribution" AND abs:"agent" (25 entries, 12 in window);
(2) abs:"inter-rater" AND abs:"LLM" (24); (3) abs:"judge ensemble" OR abs:"judge panel"
(25); (4) abs:"variance decomposition" AND cat:cs.CL (10); (5) abs:"benchmark variance"
OR abs:"reliability of benchmarks" (25); (6) agent memory dedup/redundancy/consolidation
(19); (7) abs:"duplicate bug reports" OR abs:"link rot" (25); (8) abs:"skill library"
AND abs:"agent" (25); (9) abs:"tamper-evident" OR abs:"audit trail" AND abs:"agent" (25);
(10) abs:"task type" AND abs:"model choice" (1); (11) difficulty AND pass rate AND code
generation (13); (12) abs:"self-improvement" AND abs:"verification" (25);
(13) abs:"incident" AND abs:"postmortem" (10). Total entries seen: ~250 across queries;
60+ distinct items sit inside the strict last-30-days window, well over the 30 floor.

## Pass 2 (deep reads; every banked item read end to end on its abs page this session)

Ten papers read in full on arxiv.org/abs: 2610.11781, 2609.21277, 2609.35815, 2610.05437,
2610.07645, 2609.19616, 2609.12582, 2610.10611, 2610.01256, 2609.14438. Eight banked
below. Two deep-read and DROPPED for overlap (the checks that dropped them are the
overlap ledger's proof of work): 2610.11781 Skill-V (banked by the 10-10 memory lane,
watch/inbox/frontier_olm_2026-10-10/sweep/agent-memory-continuity-arxiv.md item 1 and its
steal card steal/agent-memory-continuity.md; three raw abs captures also sit in that
run's sweep/_tmp/) and 2609.35815 evalstats (banked by the 10-09 same-lane sweep,
watch/inbox/frontier_olm_2026-10-09/sweep/evals-self-improvement-arxiv.md item 5).

## Banked items (strongest first)

### 1. How Many Humans Are 32 LLM Judges Worth? (arXiv 2609.21277, v2 2026-09-24, cs.CL+cs.LG)

Quote: "a binary-error diagnostic credits the same panels with only $1.971$--$2.227$
effective votes."

Why: The judge-panel IRR question in its strongest published form. A 32-judge panel is
worth only 2.3-6.5 human-equivalent independent votes (method-dependent), and the panels
measured are already at 94.0-96.3 pct of their effective-size asymptote - adding judges
buys almost nothing. The lever that works is composition: greedily swapping at most two
members yields 24.8-56.0 pct higher effective size at slightly higher accuracy, because
what matters is the orientation of residual error variation, not member count. This is
the independent literature grounding for the estate law that judge two must be a
different family chosen for complementary errors (watch/inbox/frontier_olm_adhoc/lens/
laws.md:108), and it reframes the corpus fold's judge-panel result (dependence-aware
Ising aggregation 9-14 pct over weighted majority, corpus/steal/
CORPUS_FOLD_FRONTIER_OLM_20261001.md:13): the calibrated-judge instrument 2609.18005
raises measured agreement, but this paper says the panel's information ceiling is set by
error-orientation diversity, so judge number two should be selected by residual-error
complementarity, not by calibration alone.

### 2. A latent dimension of Condorcet's jury theorem for multiple AI advisers (arXiv 2609.14438, v2 2026-09-28, cs.CY+cs.AI+cs.HC+cs.MA)

Quote: "such disagreement does not by itself indicate aggregation failure"

Why: The dissent-vs-reliability trade for every quorum the estate runs. Reliability and
visible disagreement both approach certainty as the panel grows, and their rates cross at
adviser accuracy 0.8: below that, visible dissent outruns correct majorities, so a
divided-looking panel can still be aggregating correctly. Separates aggregation from
disclosure (disagreement is a disclosure property, testable independently). Directly
governs how the judge-two quorum reads its own splits: a mandatory re-look (the cheap-seat
dissent rule, laws.md:48) is a disclosure trigger, not an overrule, and panel split alone
must never be scored as verdict failure when member accuracy is under 0.8.

### 3. TeleTune: Evolving Agent Skills From Offline Telemetry (arXiv 2610.05437, v2 2026-10-06, cs.AI+cs.CL)

Quote: "logs requires addressing three challenges: (1) Goal Underspecification, since
logs do not record the goal behind each action"

Why: The exact skill_ledger problem stated and solved on real user telemetry. Logs lack
recorded goals, cannot be replayed, and interleave tasks; TeleTune still evolves a
textual skill library from them by scoring proposed edits on held-out action-prediction
accuracy ("skill-guided progress", which correlates with live success), keeping only
edits that improve it, at 5-75x fewer tokens than validating by live episodes. Wins on
WorkArena 77.1 pct and Online-Mind2Web 80.6 pct over AWM baselines. For the estate:
memory/improve/skill_ledger.jsonl (2,929,694 bytes, mtime 2026-10-11T15:57, checked this
session) is exactly a non-replayable, goal-free log; the steal is the offline validation
gate - no skill edit lands without a held-out prediction-accuracy pass.

### 4. DeFA: Dependency-Guided Failure Attribution for LLM Agents (arXiv 2610.01256, 2026-10-01, cs.AI)

Quote: "We introduce DeFA, a dependency-guided framework for agent failure attribution."

Why: The case-law coverage cure. DeFA builds an event dependency graph (protocol plus
semantic edges), finds requirement-violating events, traces them into a failure
propagation graph, and names the decisive error, responsible agent, and error category;
long trajectories get segmented with cross-segment summaries. Highest responsible-agent
and exact-step accuracy on Who and When across all tested backbones, works multimodal,
and its feedback lifts a Trace2Skill skill-evolution pipeline 6-15 points downstream.
Estate wiring: graph.md:10 records that 272 of 300 case_law nodes collapse onto
module:skills_pack.py telemetry and 28 onto module:skill_ledger.py - the ledger surface,
not the failing modules. DeFA's dependency-plus-decisive-error shape is what case law
must record (responsible module, error category, exact step) so case_law maps onto the
modules that actually fail.

### 5. SkillPoison: Progressive Skill Poisoning via Successful Experiences (arXiv 2610.07645, 2026-10-06, cs.CR+cs.AI)

Quote: "skill poisoning can arise even from verified successful experiences"

Why: The adversarial case for what skill_ledger MUST record. No malicious trajectory is
needed: build verified, task-correct experiences that reinforce a target behavior, then
strip the contextual conditions that bound when that behavior applies, steering the
skill extractor's generalization; 95.71 pct attack success with every injected experience
passing verification and lexical inspection. Defense shape: the ledger must carry
applicability/context conditions per skill entry and per contributing experience, so
boundary-stripping is visible at audit time. Corroborates the estate's own
poisoning-repelled history (memory/rib/RIB_MEMWEAVE_MINDWEAVE_TESTED_20260810.md:26-33,
via laws.md:113) and gives the skill_ledger its security spec.

### 6. The Complexity Kink: A Prompt-Side Structural Complexity Index for Code-Generation Reliability (arXiv 2609.19616, v2 2026-09-28, cs.LG+cs.SE, NeurIPS 2026 Evaluations and Datasets Track)

Quote: "Task-type fixed effects shift the breakpoint to 10.75 and cut the regime gap
from 7.6 to 2.1 points."

Why: The nearest in-window instrument to the question-class law. A six-dimension
prompt-side complexity index scored BEFORE generation (ICC 0.872 across four out-of-panel
raters, 19,997 score rows, 105,000 generations over 21 models); unadjusted pass rate has
a nonmonotone breakpoint at composite 13.75 (79.9 vs 87.6 pct), and task-type fixed
effects absorb most of the regime gap. HONEST LIMIT, stated: this is not a variance
decomposition of class versus family and does not replicate the estate's 36.3-vs-3.6
pct law (memory/rib/RIB_ROUTING_CLASSES_20261002.md:11-16). What it gives the estate is
the pre-dispatch classifier the second blind audit needs: a reproducible prompt-side
index (inter-rater-reliable, task-type-conditional) to bin asks before routing, so the
audit can measure class effects with an instrument instead of hand labels.

### 7. NovaFabric: Tamper-Evident, Replayable Evidence for Autonomous AI Agent Runs (arXiv 2609.12582, 2026-09-11, cs.CR+cs.DC, 44pp preprint)

Quote: "a trace is mutable: alterable undetected, with no recipe for re-executing it"

Why: The REGISTRY-row incident's literature twin. NovaFabric seals run evidence into
portable Run Capsules (15-entity schema, DSSE signatures, RFC 3161 timestamps, Merkle
logs, redaction attestations) without altering agent logic, makes sealed runs re-executable
under a four-mode replay protocol, and - the load-bearing metric for the estate - measures
declared-stream completeness at 0.652 (+/-0.064): the fraction of run streams actually
captured is itself a first-class measured number. Tampering was rejected across all three
tested classes; honest limits include 2/10 replay completion for tool-using workloads and
a 61.6 req/s ingest cap. Steal shape: the workflow gate's REGISTRY row is a
declared-stream completeness instrument; an artifacts-minus-registry reconciliation probe
is how "run landed artifacts but no row" stops being invisible.

### 8. Verification and Self-Improvement in Agentic AI: Foundations and Limits (arXiv 2610.10611, 2026-10-07, cs.AI+cs.CC, 26pp, Lean formalization)

Quote: "A performance score does not distinguish these mechanisms."

Why: The theory spine under the whole area. Models improvement-via-search, via-support,
and via-procedure-change formally; proves bounded self-modification under a common sound
interpreter and fixed verification protocol remains within the same verification class,
and shows existential acceptance over random tapes can accept wrong outputs (a randomized
verifier class sandwiched Sigma_k^P to Sigma_k+1^P). Ships a Lean formalization plus
audit code. Estate reading: the workflow gate's self-steal ratchet holds for any bounded
change inside the gate protocol (you cannot ratchet yourself out of the class you verify
in), and the failure mode to guard is exactly the unverified-acceptance case - a run
whose checks never entered the registry is existential acceptance, the shape that accepts
wrong outputs.

## Answers to the research questions (estate cites from files read this session)

RQ1 (judge number two). No paper hands the estate a second judge family by name, and
that remains an estate decision with ember's dossier as the negative case
(watch/inbox/frontier_olm_adhoc/lens/laws.md:108). What the window's literature settles:
panel effective size saturates (item 1: 32 judges worth 2-6.5 humans, already at 94-96
pct of asymptote), so the calibrated-judge instrument 2609.18005 does not lower judge-panel
IRR by adding more judges - it cannot, information-theoretically; the IRR moves only
through member complementarity (the 24.8-56 pct swap lever) and through honest dissent
reading (item 2: split is a disclosure property below 0.8 member accuracy). Selection
rule for judge two: maximize residual-error orientation distance from judge one, then
calibrate. The statistics instrument for the panel itself is already held (2609.35815
evalstats, banked by the 10-09 lane, verified this session).

RQ2 (skill_ledger case law coverage). What the ledger must record, from this bank plus
the held Skill-V: per-skill versioned falsifiable contracts with operational boundaries
(2610.11781, held by the 10-10 memory lane), context/applicability conditions on every
skill and contributing experience (item 5, else poisoning via verified successes is
invisible), goal-inference provenance and a held-out offline validation score per edit
(item 3), and module-level decisive-error attribution: responsible module, error
category, exact step (item 4). With those fields, case_law nodes can map_to failing
modules instead of collapsing 272-of-300 onto skills_pack.py telemetry
(watch/inbox/frontier_olm_adhoc/lens/graph.md:10). The same-lane daily sibling's bank
adds the co-installation collision instrument (2610.11647 One Skill Too Many,
watch/inbox/frontier_olm_2026-10-11/sweep/evals-self-improvement-arxiv.md item 2).

RQ3 (whole-corpus law index). No in-window paper builds the full cross-referenced
index; the composite is: collisions via the sibling-banked deterministic-first similar-
pair census (2610.11647: 822,109 candidate pairs from 20,947 repos, 312 confirmed, LLM
judging only a stratified sample - the cheap-first routing shape for a 2,000-ask census,
laws.md:109) plus decisive-error clustering (item 4: many failure events resolving to one
root cause IS one-bug-many-jackets resolution); orphans via citation-health audits that
exist but sit outside the 30-day window (2601.17431 The 17 pct Gap, 2026-01: ~17 pct of
AI-survey citations unresolvable; 2604.03173 urlhealth, 3-13 pct hallucinated citation
URLs). Named, not banked: both are older than the window and were not fetched this
session beyond their pass-1 gists; pulling either is a cheap follow-up.

RQ4 (does 36.3-vs-3.6 replicate). Still NO independent replication found; this sweep's
verdict agrees with the prior file's (prior same-path mint section OWED) and the X
sibling's. The falsifier named at memory/rib/RIB_ROUTING_CLASSES_20261002.md:28-30 stays
unfired. What is new is the instrument for the estate's own second audit: item 6's
prompt-side complexity index (ICC 0.872, task-type-conditional breakpoints) is the
published shape of a pre-generation ask classifier; the estate should run its second
blind audit with a complexity-plus-class index computed before dispatch, so the audit
yields the variance decomposition the literature has not yet published.

RQ5 (does the ratchet hold with artifacts but no REGISTRY row). Local incident verified
this session: memory/workflows/REGISTRY.jsonl holds 177 rows, latest ts
2026-10-11T02:07:34Z (mcp-landscape-wide-dig), and ZERO rows mention the adhoc run or
either dwfrun id (5d623493, e68f99eb) - while the adhoc artifacts landed 01:14-06:59
(sweep files 01:14/01:18, register.jsonl 04:48, DIGEST 05:04, RECEIPT 06:59). The
incident stands as lens/burns.md records it (watch/inbox/frontier_olm_adhoc/lens/
burns.md:126-131: "an incident, not registered debt"). Theory answer (item 8): the
ratchet's guarantee is scoped to runs inside the verification protocol; an artifact
landing without a registry row is outside that scope, the existential-acceptance case,
which the theory says can accept wrong outputs. Practical answer (item 7): adopt
declared-stream completeness as a gate metric - a periodic reconciliation of landed
watch/inbox artifacts against REGISTRY rows, with the gap published, is the missing
organ. This sweep notes itself: its own artifact lands in the same exposure until this
run's gate check writes its row.

## Overlap ledger (commands run this session)

- catalog/catalog.jsonl streamed in full (1.1M rows) for all 10 deep-read ids plus
  distinctive titles. Hits: 2609.21277 -> state/arxiv/2026-09-21/2609.21277v1.txt (raw
  daily-feed intake, title-grade, no curated citation); 2610.11781 -> three raw captures
  in the 10-10 run's sweep/_tmp/ (followed to its bank: dropped); 2609.18005 ->
  state/arxiv/2026-09-17/2609.18005v1.txt (confirms the ask's "banked calibrated-judge
  instrument" is register-banked, its raw feed row notwithstanding). All other ids: zero.
- Scoped memory/ + tree grep (memory/frontier, memory/improve, memory/rib, memory/lenses,
  memory/press, memory/workflows, memory/zknot/LATEST.md, CORPUS_CATALOG.md, and all four
  watch/inbox/frontier_olm* trees, .md/.jsonl/.txt only, _tmp/raw/_fx/.mimosa excluded):
  2609.14438 zero; 2610.05437 named-only on the 10-10 memory lane's shortlist (in-window
  candidates list, not banked - banking here is the pull it was named for); 2610.01256
  zero; 2610.07645 zero; 2609.19616 zero; 2609.12582 zero; 2610.10611 named-only in the
  prior same-path mint's near-miss list as the recommended dedicated follow-up (this
  sweep is that follow-up); 2609.21277 zero anywhere except the raw feed row above.
- Dropped after deep read: 2610.11781 (banked, 10-10 memory lane), 2609.35815 (banked,
  10-09 same-lane sweep, item 5 of its file). The sibling X sweep's candidate list
  (watch/inbox/frontier_olm_adhoc/sweep/evals-self-improvement-x.md) names 2605.29800
  "Nine Judges, Two Effective Votes" - same finding-family as bank item 1; item 1's delta
  is the matching-method decomposition, the saturation asymptote, and the member-swap
  composition lever, none of which 2605.29800 carries.

## OWED after this sweep

- RQ4 falsifier still unbanked anywhere in the estate: no published class-vs-family
  variance decomposition on agent workloads exists in this window. The estate's own
  second blind audit (with item 6's index as the pre-dispatch classifier) is the only
  path; nothing external will fire it.
- Orphan-side RQ3 citations (2601.17431, 2604.03173) seen at gist level only, outside
  window; fetch either before citing numbers beyond the gists above.
- The REGISTRY reconciliation probe named in RQ5 is designed, not built; nothing in this
  session wrote a REGISTRY row or modified tools/workflow_gate.py.
- Full-text (HTML) reads: none; all ten reads are abs-page depth. Quotes are verbatim
  fragments as marked by the fetch layer; no quote is hand-copied from memory.
