# sweep: swarm-orchestration via x (frontier_olm 2026-09-30)

source-fetched: 2026-09-30

Seat: sweep-swarm-orchestration-x. Predecessor: `watch/inbox/frontier_olm_20260928/sweep/swarm-orchestration-x.md`
(read in full this ask; its 11 banked items are the dedupe baseline and none are re-banked).
Estate grounding read this ask: `watch/inbox/frontier_olm_2026-09-30/lens/burns.md` (driver-restart
line 66-67, percolator headline lines 86-89), `watch/inbox/frontier_olm_2026-09-30/lens/laws.md`
(orchestration-tax line 68, runaway-python opens line 66), `mag/seed_percolator.py:1-16`
(paired-blind gate, elder design), and the heal-merge region of `mag/percolator.py` (note: the
bare-counter promote gate the ask cites at `mag/percolator.py:264-272` has DRIFTED in the working
tree; lines 255-285 now hold the Z15 heal-merge MAX code, the promote gate sits elsewhere in the
file. The cite is from burns.md:86-89, carried from the 09-28 dig, not re-verified line-exact
this ask).

## Door health (honest)

- X door DEGRADED this cycle, same shape as 09-28: site:x.com queries came back nearly empty
  (the backend holds almost no x.com index) and the Z.ai search backend threw 1302/429
  rate-limit storms on 4 separate query shapes mid-sweep (the sweep instrument re-corroborated
  the fan-out law the hard way).
- Because zero x.com status URLs surfaced, ZERO fxtwitter resolutions were attempted or made.
  No status id, no door. Per recipe fallback, X-adjacent claims are carried only as
  search-result snippets with their URLs, and every one is listed in OWED below. Nothing
  X-resolved is asserted as read.
- Non-X sources were read end to end where reachable (11 reads, listed in Pass 2). Two fetch
  instruments degraded: WebFetch timed out twice (blakecrosley.com/guides/feed.xml, and the
  first try of arxiv 2609.02246 abs, recovered via the /html/ URL); mg6.net returns TLS
  cert-mismatch (host served under a different altnames cert) and is snippet-only.

## Pass 1: candidate pool (35 considered, last 30 days = 2026-09-01..09-30 where dated)

In-window candidates: arXiv 2609.34320 (09-28), 2609.34198 (09-28/29), 2609.12191 GAUGE (09-10),
2609.02783 EarlyEval (09-02), 2609.02246 PROCTOR (09-02), paddo.dev raise-that-is-a-cut (09-04),
anthropic.com/news Sept-14 limits (09-14, via paddo + search), Hermes Agent practitioner's
reference (blakecrosley.com, ~09-24 per search), Hermes Agent Sept changelog (gradually.ai),
solomonneas.dev intel briefings, mg6.net delegation-fails-at-scale (date unknown, TLS-broken),
digitalapplied Claude-Code-2.1.224 cross-session messaging, aigentlab.tech subagent-limit
3-changes-in-10-days, vibecode247 subagent guardrails coverage, dailyaithread weekly-limit
briefing, DEMM-Bench family (bytez/aointegrity, paper 2606.20634 = May, out), Gaia2 ICLR 2026,
FDE-Bench (ResearchGate), agentic-ai.readthedocs.io harness taxonomy (undated, current ~mid-2026),
github multi-agent-topology-taxonomy.md, simorconsulting.com handoff-amplification (Jun),
letsaskclaire.com state-failure framing, akoode.com orchestration patterns, nextdot.co.in error
propagation, massivue.com disagreement post (Aug, MAST pointer), morphllm usage-limits reference,
explainx.ai limit-math post, evomap.ai usage-limits agent, github anthropics/claude-code feature
request auto-continue-after-reset, dev.to sub-agent token-burn resume pattern, claudefa.st
persistent sub-agents, digitalapplied amp event-driven orbs, togetherbench, AI DevKit, agentic
skill catalog X-fetch tooling.

Out-of-window candidates considered and flagged (read or snippeted anyway, none promoted above
in-window items without reason): anthropics/claude-code#67636 (06-11), openai/codex#15379
(03-21), Anthropic dynamic-workflows cookbook (07-22), digitalapplied subagent-guardrails
(07-21..24), oneaway.io agent-teams (02-09), tianpan.co orchestration-overhead dollars (02),
mg6 stat mirrors, fanaticalfuturist 16-agent compiler (01-15), nxcode.io agent-teams guide.

## Pass 2: items read end to end this ask (11)

1. arXiv 2609.34320 abs page (Certified Selective Automation of LLM Agent Evaluation).
2. arXiv 2609.34198 abs page (Frozen Judges, Moving Agents; v1 09-28, v2 09-29).
3. arXiv 2609.12191 abs page (GAUGE).
4. arXiv 2609.02246 html v1 (PROCTOR; abs URL timed out once, html fetched clean).
5. arXiv 2609.02783 abs page (EarlyEval).
6. platform.claude.com cookbook claude-agent-sdk-08-dynamic-workflows (full page).
7. paddo.dev/blog/the-raise-that-is-a-cut/ (full post).
8. github.com/anthropics/claude-code/issues/67636 (issue body + state).
9. github.com/openai/codex/issues/15379 (issue body + state).
10. oneaway.io/blog/claude-code-agent-teams (full article).
11. agentic-ai.readthedocs.io/en/latest/ (landing + taxonomy structure).

Only items I read myself are banked below.

## Verdicts per research question

**RQ1 (certified-decision acceptance as the promote-gate upgrade; post-09-28 gate designs for
the paired-blind gate):** YES, and sharper. REUSE (2609.33180, prior-cycle banked) said certify
the judge's auto-decisions; this week's 2609.34320 (09-28) shows the i.i.d. certificate behind
that idea OVERSTATES safety when trajectories cluster by task (agents attempting the same tasks
correlate their errors), and gives a cluster-valid task-level bootstrap certificate: a 4B judge
auto-decides 30-59% of evaluations at error budget alpha=0.1. The estate's percolator counts are
exactly correlated repeats (the same invariant re-hit across cycles; the Z15 heal-merge MAX fix
exists because counts were being re-added), so any certified gate imported into
mag/percolator.py must be the clustered variant, not the naive one. Same-week 2609.34198
(09-28/29) independently derives the estate's elder design: because a fixed judge's errors vary
by agent version (it falsely approves failed patches as agents get more capable), release
decisions should be PAIRED AUDITS of new-vs-old on the same tasks with execution-based
verification - which is mag/seed_percolator.py:6-16's paired blind win-rate vs frozen baseline
with judge rotation, already designed, still unwired. The published frontier moved TOWARD the
estate's gate, not past it. 2609.02246 PROCTOR (09-02) supplies the wiring shape without
fallback-branch creep: demote the judge from oracle to advisor, gate every change on a
deterministic verification layer, mechanical rejection always overrides LLM approval (never the
reverse), plus frozen holdouts with leak prohibition and canary integrity cases - a direct
published mirror of the seed gate's null-variant canary guard. GAUGE (09-10) audits the
promote-the-higher-judge-score scheme itself at release-decision stage. EarlyEval (09-02) adds
the cost side: a cheap LightGBM pair halts doomed runs mid-flight (13-26% of steps, up to 44.1%
of input tokens, 89-97% accuracy, 1-2 resolve points moved) - candidate pre-gate in front of
expensive paired judging. Net: certified acceptance still holds as the upgrade path; the delta
is (a) use the cluster-valid certificate, (b) wire the already-designed paired-blind gate as the
deterministic layer, (c) judge as one input, never the gate itself.

**RQ2 (published width 15-16+ dispatch measurements; the unmeasured orchestration tax):** No
published tokens-per-hour measurement at width 15-16+ was found - the estate's width-10
109.4M tok/h bank (AGENTS.md fan-out law) remains the sharpest number I can find anywhere, and
the grok-4.5 critique's orchestration-tax-at-scale warning (laws.md:68) stays unmeasured in
public. Nearest published shapes: Anthropic's own dynamic-workflows runtime keeps up to 16
agents running concurrently and caps a run at 1,000 agents (cookbook, 07-22, out-of-window
flagged) - a width-16 RUNTIME ceiling, but the cookbook publishes no throughput figure; its
overflow design is to QUEUE excess work until a slot frees, and its retry design is to redo
only the failed stage over cached completed agents. oneaway.io's agent-teams article (02-09,
flagged) reports the 16-agent / ~2,000-session stress test, token cost scaling LINEARLY with
teammates ("five teammates means roughly 5x the token usage"), $20k / 2B input tokens for the
compiler demo - a cost tax at width 16, not a throughput measurement. The tianpan.co
"$47,000/month orchestration overhead vs $22,700 single agent for 2.1% accuracy" claim and
mg6.net's "41-87% of multi-agent systems fail in production" range surfaced only as search
snippets (one unfetched, one TLS-broken): OWED, not asserted. Verdict: the rung above 10 is
architecturally confirmed to exist (vendor runtime caps at 16) but nobody publishes the tok/h
curve; measuring width 12-16 on this estate's own account is still an open, bankable
experiment.

**RQ3 (first-contact rate limits: HOLD vs backoff vs pause vs reroute):** No read source
publishes a HOLD-first rule; the estate's standing law (first contact is a HOLD signal, not a
width cut) remains unmatched in public. Closest structural corroboration: the cookbook's
runtime queues overflow and resumes within-session rather than failing agents, and treats
retry as cached-completed-plus-redo-failed-stage - i.e., the vendor's own shape agrees that
capacity loss should pause/slot-wait, not shrink. On the provider side, the one in-window
policy event read is paddo.dev (09-04): the +50% summer promo ends 09-14, the new permanent
weekly level is +25% vs standard, which is a 17% CUT against the promo-period level, alongside
doubled five-hour limits and removed peak-time restrictions (per the anthropic.com/news pointer
in that post and the search summary; the anthropic.com page itself was not fetched this ask -
snippet-level). Lesson banked: caps are rolling policy windows that move under a running fleet
(Anthropic moved its own limits 3x in 10 days per the aigentlab headline, unread, OWED), which
is the strongest public argument yet for HOLD-and-retry-internal: a width cut in response to
first contact would be calibrated to a cap that changes shape weekly.

**RQ4 (driver-supervision patterns for the not-done world-models driver restart; reaper /
process-tree / job-object attribution):** The restart is still not done (burns.md:66-67) and
no in-window published reaper design surfaced. The best class evidence remains
openai/codex#15379 (03-21, out-of-window flagged, read): "Exiting or force-stopping the parent
Codex process does not always terminate the spawned process tree" - open, no fix, reporter
asks for process-group teardown verification on all exit paths and reaper tasks that are not
aborted prematurely. anthropics/claude-code#67636 (06-11, flagged, read) is the sibling
failure tax: a wide spawn burst (10 agents) whose members each did reads then crashed,
"wasting a few million tokens," with 15 agents spawned minutes earlier for 1-2 agents' work -
supervision failure costing money, not just processes. Neither project has landed a structural
fix; both still route around it manually. The estate's own open questions (laws.md:66:
process-tree / job-object attribution via CIM, kill-by-source-tree vs blanket python.exe,
single canonical spawner) have no published counterpart I could find in-window. Two leads that
might carry implementation detail are unreachable this ask (see OWED): blakecrosley.com's
Hermes practitioner's reference (background-process handoff commit 3c0d90e8ef) and
solomonneas.dev's briefing on surfacing subagent rate-limit failures instead of silent drops.
Structural recommendation unchanged and now doubly evidenced: job-object/process-tree
teardown verified on ALL exit paths is the gap class, and two major harnesses still have it
open.

**RQ5 (published handoff reliability numbers / failure taxonomies to grade B2-443 against):**
Nothing published in-window with numbers. The strongest taxonomy artifact read is
agentic-ai.readthedocs.io (undated, current ~mid-2026): it consolidates two 2026 surveys (a
197-paper "Code as Agent Harness" survey, Ning et al. 2026, and a 110+ paper LLM Harness
Survey with the ETCLOVG seven-layer taxonomy and formal model H=(E,T,C,S,L,V)), but carries NO
dedicated handoff-reliability section - handoffs appear only inside multi-agent coordination
patterns. The mg6.net failure-percentage range that would have been the only quantitative
grading surface is TLS-broken (snippet-only). MAST (UC Berkeley NeurIPS 2025 production-trace
taxonomy) is the known prior art, out of window, and was not re-dug this cycle. Verdict: the
estate's B2-443 workflow-child failure census remains, as far as this sweep can verify, the
only measured failure census of its kind; there is still nothing external to grade it against.

## Overlap record (greps run this ask)

Baseline loop over catalog/catalog.jsonl (691,788 lines, 193,941,763 bytes) and memory/ +
watch/inbox/ (trajectory excluded), exact/distinctive phrases:
- "Certified Selective Automation": catalog 0, memory/inbox 0. CLEAN.
- "Frozen Judges, Moving Agents": catalog 0, memory/inbox 0. CLEAN.
- "demoted from oracle to advisor": catalog 0, memory/inbox 0. CLEAN.
- "EarlyEval": catalog 1 - the hit is a raw arXiv listing capture
  (`.../2026-09-06/2609.02783v1.txt`, 1,489 bytes, age_days 20, zone lsa). The listing text is
  in the raw corpus; no digest, steal-card, or mechanism note exists anywhere in memory/. The
  deep-read this cycle (classifier-pair halt mechanism, the 13-26%/44.1% numbers) is new work
  on top of a raw capture; banked with the overlap stated.
- "spawned process tree": catalog 0, memory/inbox 0. CLEAN.
- "raise that is a cut": catalog 0, memory/inbox 0. CLEAN.
- "1,000 agents": catalog 0; 2 generic memory/inbox hits
  (memory/percolator/explore_deepseek_drain.jsonl, memory/runs/adv_arc_50/ADV_ARC_PACK.md) -
  unrelated strings, not the cookbook. CLEAN for the cookbook item.
- Prior-cycle register cross-check: grep for all five arXiv ids (2609.34320, 2609.34198,
  2609.02246, 2609.12191, 2609.02783) over
  watch/inbox/frontier_olm_20260928/register.jsonl and percolator_candidates.jsonl = 0 hits.
  None of this cycle's items were banked by the 09-28 cycle. REUSE itself (2609.33180, title
  "Which Self-Improvements Should We Trust?...") IS in the prior register (evals area) and in
  burns.md:89 - it is background, not a banked item here.
- Baseline greps from ask start: "REUSE" catalog 5+ / agent_sessions only; "2609.33180" 0/0;
  "orchestration tax" catalog 0, memory 1 (the rib); "HOLD signal" catalog 0; "job object"
  catalog 0, memory RIB_RUNAWAY_PYTHON; "win-rate" catalog 1; "handoff" catalog 5+ generic.

One re-bank catch by the dedupe: none this cycle (the 09-28 sweep's items were all avoided by
baseline; OmniRoute et al. not re-encountered).

## OWED (unreachable this ask; snippets only, nothing asserted)

- mg6.net "Multi-Agent Orchestration: Why Delegation Fails at Scale": TLS cert mismatch
  (ERR_TLS_CERT_ALTNAME_INVALID, host served under backend-sandbox-6.reebuild.com). Snippet
  stat "41-87% fail in production" carried as snippet only.
- tianpan.co "$47,000/month overhead vs $22,700 single agent, 2.1% accuracy": never fetched
  this ask; search summary only.
- blakecrosley.com Hermes practitioner's reference: root domain is a portfolio; guide path
  unknown; /guides/feed.xml WebFetch timed out (60s).
- solomonneas.dev intel briefing on surfacing subagent rate-limit failures: root domain is a
  portfolio, briefing page not surfaced.
- anthropic.com/news Sept-14 higher-limits announcement: pointed to by paddo.dev and search;
  not fetched directly this ask.
- digitalapplied subagent-guardrails piece (07-21..24) and the aigentlab "3 changes in 10
  days" analysis: correct URL found late (…/claude-code-subagent-depth-limits-budget-caps-2026)
  after the first slug 404'd; not deep-read this ask, snippet-level.
- X generally: zero status ids surfaced; zero fxtwitter resolutions; X-door findings this
  cycle are all second-hand snippets. Say it plainly: this is an X-area sweep where the X door
  contributed nothing read directly, same failure shape as 09-28.
- DEMM-Bench (arXiv 2606.20634, May, out of window): bytez fetch returned nav chrome only;
  the "Source Review and Promotion Gate" phrase belongs to a sibling Quipu paper per snippet,
  not DEMM itself. Dropped.
- towardsai session-kills article: not fetched this ask (prior cycle had it 403/500-blocked).
