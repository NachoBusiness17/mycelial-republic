# sweep: swarm-orchestration via arxiv - 2026-09-30

source-fetched: 2026-09-30. Seat: sweep gopher (swarm-orchestration via arxiv), carrier
`watch/inbox/frontier_olm_2026-09-30/`. Window: submittedDate [2026-08-31 .. 2026-09-30].
All estate citations below were read in this session; all quotes are verbatim from pages
fetched this session.

## Doors run (commands/URLs)

7 arXiv export API queries (`https://export.arxiv.org/api/query?search_query=...` with
`submittedDate:[202608310000 TO 202609302359]`, sorted by submittedDate desc):

1. `("multi-agent" AND "orchestration")` - 39 of 52 feed entries rendered (DEGRADED: feed
   truncated mid-way through entry 39; entry 39's author list cut).
2. `("swarm" AND "LLM")` - 10 entries.
3. `("rate limit" OR "backoff" OR "retry") AND ("LLM agent" OR "multi-agent")` - 9 entries.
4. `("handoff" OR "inter-agent communication" OR "agent handoff")` - 30 entries.
5. `("supervisor" OR "watchdog" OR "self-healing" OR "crash recovery") AND ("multi-agent" OR "agentic")` - 15 entries.
6. `("confidence sequence" OR "always-valid" OR "sequential test" OR "certified acceptance") AND ("LLM" OR "agent" OR "policy")` - 4 entries.
7. `("throttling" OR "load shedding" OR "circuit breaker" OR "concurrency limit") AND ("agent" OR "API")` - 1 entry.

Raw rows listed: 108; unique candidates after 5 cross-query duplicate IDs: ~103. No door
403'd. Pass 2 read: 6 full HTML texts end to end (`arxiv.org/html/...`): REUSE v2, Maat,
MeshHeal, Agensh, Do Not Restart (CFRC), Translating the Translator; plus 2 abstract pages
(`arxiv.org/abs`): Hard Stop, LIMBO.

## Overlap receipts (run this session)

`rg`/`grep` of `catalog/catalog.jsonl`, `memory/`, and the 09-28 predecessor carrier
(`watch/inbox/frontier_olm_20260928/register.jsonl`, `percolator_candidates.jsonl`,
`sweep/swarm-orchestration-arxiv.md`, 60 unique arXiv IDs) for each candidate ID/title:

- **REUSE 2609.33180: ALREADY BANKED 09-28** - `register.jsonl:9` (evals-self-improvement
  area) + `percolator_candidates.jsonl:1` (full port plan naming `mag/percolator.py:264-272`
  and the dormant seed gate) + `watch/inbox/frontier_olm_2026-09-30/lens/burns.md:86-89`
  ("certified-decision acceptance (REUSE, arXiv 2609.33180) is the named upgrade path").
  NOT re-banked here. New texture this session: the abs page shows **v2 revised 2026-09-29**
  (our banked row cites v1), and the v2 HTML still carries the guarantee sentence verbatim:
  "with probability at least 1-alpha, every promoted modification over the entire
  self-improvement process is a genuine population improvement on the underlying task
  distribution." Mechanism read end to end: paired sign test per candidate vs incumbent,
  per-round error budget delta_{t,p} = alpha*w_t*v_p / (C(t-1,p) * K^(p+1)) spread over ALL
  decision histories, decision-only feedback (search never sees scores), measured false
  promotions: naive best-of-K 75/2000 and 71/10000 (up to 20.7% of promotions at worst) vs
  REUSE 0 at both n, final population improvement within 0.04 pp of the best baseline. Cost
  is statistical: fewer promotions (3.2 vs 13.0 for best-of-K at n=2000), not a dollar
  figure.
- **MeshHeal 2609.29015**: prior sweep full-text read it, then EXCLUDED it from its banked
  eight with an explicit deferral: "MeshHeal ... is the closest published analog to
  rib_bus + burn lanes and deserves a full-text steal despite the abstract already being
  held" (prior sweep file line 25). This sweep completes that steal; catalog holds only the
  raw abstract snapshot (`catalog/catalog.jsonl:445586`, zone lsa).
- **LIMBO 2609.29095**: prior sweep abstract-read it and cited its 28-to-4% and 90% stats in
  its RQ1 answer (line 29); `memory/runs/mickey17_v2/.../ttc-week` lane already checked the
  90% stat (prior sweep line 25). Never registered. Banked here for the unbanked Q5 angle.
- **Agensh 2609.26781** (`catalog/catalog.jsonl:445335`) and **Hard Stop 2609.29808**
  (`catalog/catalog.jsonl:445685`): raw abstract snapshots only (zone lsa, auto-harvest);
  zero register/steal/prior-sweep hits. Genuinely new banked findings.
- **2609.13800, 2609.34017, 2609.15079**: zero hits anywhere in catalog register, memory/,
  or the prior carrier. Genuinely new.

## Answers to the five research questions

**Q1 - certified acceptance for the promote gate.** REUSE (v1 banked 09-28) still holds as
the upgrade, now stronger: v2 (09-29) keeps the guarantee, and the full text shows the
acceptance rule IS a paired blind comparison (paired sign test vs frozen incumbent) with a
per-promotion error budget that survives adaptive dependence - the exact failure class the
estate hit in the flesh (heal-merge SUM triple-counting, `mag/percolator.py:258-266`; the
232,214 echo-inflated top count, `memory/corpus/quantized_thought/instructions_frontier.jsonl:7`).
So the wiring move is unchanged and legal under the no-fallback-branch law: replace the
recurrence counter's promote verdict with the REUSE predicate; the estate's dormant paired
gate (`mag/seed_percolator.py:7-12`: 55%+ win-rate, 30 pairs/epoch, 3 consecutive epochs,
null-variant canary) supplies the measurement shape, REUSE supplies the certified verdict -
one predicate swap, no guard branches. Newest published reinforcement (post-09-28): **Maat**
(2609.34017, 09-27) puts deterministic gates BETWEEN agents on handoff edges -
PASS/WARN/BLOCK verdicts from a versioned anchor contract with "no language model in the
validation or scoring path", plus a G6 circuit breaker (0% false trips reported) - the
gate-as-control-point pattern, not a fallback branch.

**Q2 - published width 15+ measurements and the orchestration tax.** **Agensh** (2609.26781,
09-22) is the first published curve above the estate's measured width-10 rung: 1, 8, 32,
128 agents move mean final test-pass 19.31%, 20.68%, 26.52%, 28.78% (five ProgramBench
tasks), and 1, 128, 1024 on pandoc move 33.89%, 50.94%, 55.06%; 128 agents hit 30% pass at
30 min vs 60/90 min for 32/8. But it measures QUALITY and TIME only: "No total
token/cost-at-scale measurements are reported" (my full-text read). **Translating the
Translator** (2609.15079, 09-14) measures a communication tax - 13.0 (Spanish) to 30.6
(Hindi) EM points lost by forcing inter-agent handoffs through English - and explicitly
analyzes no token counts. Verdict: the grok-4.5 critique stands. No paper in the window
reports the orchestration tax in tok/h; the estate's 109.4M tok/h at width 10 (AGENTS.md
clippy, B2-476 amendment) remains the only number of its kind I found in this window's
literature.

**Q3 - first-contact rate limits: HOLD vs width cut.** Not directly studied: query 7
(throttling/load shedding/circuit breaker + agent/API) returned exactly one window paper
(Hard Stop); query 3's retry/backoff hits bear on retry semantics, not dispatch shape. No
published evidence found that refines or contradicts the standing-law reading that first
rate-limit contact is a HOLD signal rather than a width cut (AGENTS.md max-concurrency law).
Nearest adjacent published pattern: **MeshHeal** (2609.29015) - its slow timescale does NOT
shrink steady-state width on first detection of a degraded agent; it isolates that agent
from routing while recovery probes run, then reintegrates on probe pass (detector: 0 missed
/ 0 false isolations; reintegration after about 45-46 tasks). Structurally HOLD-and-probe,
and the closest published analog to the rib_bus/burn-lane shape, as the 09-28 sweep already
suspected. Stated plainly: this is adjacency, not confirmation - nobody publishes 429
semantics.

**Q4 - driver supervision for the world-models-multi-agent restart gap** (still NOT done,
`watch/inbox/frontier_olm_2026-09-30/lens/burns.md:66-67`). Three published pattern classes:
(a) **Do Not Restart / CFRC** (2609.13800, 09-12): do not restart at all - freeze a residual
contract from the accepted trajectory and trusted receipts BEFORE the successor proposes,
let it author a complete continuation on an isolated replica, admit the evidence-linked
graph against the contract, grant write authority only then; GPT-5.4-mini successors hit
70.8% macro accuracy at 34.6% of the strong-anchor cost; contract audit recovered 62/68
write obligations (91.2% recall); all 124 interventions fired before the first live write.
Their stated limit: weak cheap models poison the contract (Haiku 4.5/Sol minus 5.0 pts at
57.4% cost), and there is no rollback after a live call - so the estate driver should
freeze the contract at tick boundaries, not mid-call. (b) **Hard Stop** (2609.29808,
09-24): the reaper design class - out-of-band supervisory control of discrete event systems
(Ramadge-Wonham) with "microsecond-scale (4.8 $\mu$s median / $< 0.154$ ms WCET bound)
POSIX preemption buses", containment before off-target egress; born from a real 4.5-day
rogue-agent incident (17,600 actions, 6,280 clusters, 136 secrets). This is the structural
closure direction for the runaway-python opens
(`watch/inbox/frontier_olm_2026-09-30/lens/laws.md:66`): move the kill out-of-band and
preemptive (source-tree-scoped sentinel with a preempt bus) instead of deduping process
trees at read time. (c) **MeshHeal**: two-timescale supervision - fast peer-review-and-
correct before use, slow detect/isolate/probe/reintegrate. None of the three answers the
Windows CIM/job-object attribution question directly (OWED: no window paper on Windows job
objects surfaced).

**Q5 - pass-off reliability numbers / failure taxonomies.** Two gradeable comparanda for
the B2-443 workflow-child failure census: **Maat**'s handoff-edge gates over 522 trials,
six workflows (6-15 agents): 94 governed-arm halts = 45 caught injected defects + 13 caught
genuine un-injected defects + 35 false alarms (37% of halts were VALIDATOR defects -
circuit-breaker depth carryover, empty answers flagged as hollow), correctness +7.7% to
+29.1% in five workflows, cost down 17-53% where halts fire early. **LIMBO** (2609.29095):
25,930 episodes, nine models, twelve fault modes - frontier models duplicate a lost-ack
write in 0.5% of episodes but 56%/74% when reads cannot reveal the outcome (in-flight or
duplicated transport); "agents reported success in 90% of the episodes in which they had
duplicated an effect"; idempotency keys on every write cut duplicates 28% to 4%; plus a
proof that no verification-only policy is exactly-once under late commits without bounded
in-flight time. Direct steal for the effect broker: mint idempotency keys on effects so any
retry-with-lost-ack path cannot double-spend (the 09-28 sweep's RQ1 steal, now backed by
the full abstract number set and the in-flight breakdown it did not record). CFRC adds the
pre-write-intervention property (124/124 before first live write) as the pass-off safety
bar.

## Banked items (7, strongest first)

Full schema-conforming list in the submitted result; one-line index:

1. Agensh: Scaling Organizational Intelligence to 1,024 Agents - 2609.26781 (09-22). NEW.
2. Do Not Restart: Residual Completion for Stateful Agent Handoffs - 2609.13800 (09-12). NEW.
3. Maat: Independent Deterministic Contract-Based Governance... - 2609.34017 (09-27). NEW.
4. Translating the Translator: Decomposing the Cost of English-Forced Inter-Agent
   Communication - 2609.15079 (09-14). NEW.
5. Hard Stop: Kernel-Level Preemption and Containment for Rogue Agentic Execution -
   2609.29808 (09-24). Abstract snapshot in catalog only (row 445685).
6. Where Does Exactly-Once Live? (LIMBO) - 2609.29095 (09-24). Prior sweep abs-read only;
   not registered; banked here for the Q5 taxonomy angle.
7. MeshHeal: Two-Timescale Self-Healing for Gray Failures... - 2609.29015 (09-24). Completes
   the 09-28 sweep's explicit full-text-steal deferral.

## Leads left unbanked (pass 1 only, not read end to end)

ResonAct 2609.34701 (09-28, streaming runtime diagnosis/self-healing - post-09-28 gate
lead), Loop-Back Authority 2609.14767 (flat vs hierarchical paired experiment), Active
Provenance Gate 2609.31422, Backstitch 2609.27538 (request-causality restoration across a
production fleet), Waggle 2609.34136 (self-organizing LLM swarms), Emergent Cheating in
Autonomous Research Swarms 2609.04170, ICMAPE 2609.33986. REUSE 2609.33180 covered above,
not re-banked.

## OWED / not found (stated, not guessed)

- No published study of provider rate-limit first-contact semantics (429/1302 HOLD vs width
  cut) found in the window; the standing law stands unrefuted and unsupported.
- No published tok/h orchestration-tax measurement found at any width; Agensh and
  Translating the Translator both stop short of token economics.
- No Windows job-object/process-tree attribution paper surfaced for the runaway-python
  CIM walk open.
- Agensh's full text carries no cost-at-scale table (verified by targeted read); the width
  15-16 rung specifically is unmeasured in every window paper - Agensh's checkpoints are
  1/8/32/128/1024.
