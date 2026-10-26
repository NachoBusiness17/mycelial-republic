# Six tests, six lenses (plan, 2026-10-24)

Everything here reuses machinery that exists: `lens_packet.py` (map + lens + naked
question), `ractor_salon.py` (kabuki cast), `burn_lanes.py` (lanes, LESSIG rails,
receipts), `burn_gated.py` (two-pass), `burn_briefs.py` (rule compliance),
`map_audit.py` (planted premises), `queue_census.py`, `shannon_report.py`,
`prior_art_check.py`. No new framework is proposed. Budget assumes free/cheap lanes at
today's measured rates (~$0.001/call on groq/ollama/nous, ~$0.01 on z.ai).

---

## T1 — BERN AYS: can demand be manufactured instead of discovered?

**Question the lens asks:** who is made to want this, and how?
**Hypothesis:** a consumer binds only when an output is wanted *before* it exists;
discovering demand after building is the estate's expensive habit.
**Design:** take 60 live explore rows. Produce two artifacts from the same rows — a
one-page digest and a stub spec — and place them where seats already read
(`watch/inbox/`). Over 48 h, count citations of each in new receipts, `state/*.md` and
queue hints, against a control set of rows with no artifact.
**Cost:** ~20 calls ($0.02) + 48 h observation. Zero-cost in waiting.
**Falsifier:** if neither artifact is cited while the control set is, demand is not
created by artifacts here — it is created by the operator asking, and the whole
"build a consumer" line dies.
**Learn:** whether the queue's problem is supply (no consumer) or demand (nobody wants
the rows). This decides T5 and the roadmap.
**Artifact:** `watch/inbox/DEMAND_PROBE_<date>.md` + citation counts.

## T2 — ELLUL: how much of the work is method, not choice?

**Question:** where does the method continue because it is the method?
**Hypothesis:** in any multi-step wave, a measurable share of steps is justified only by
"the procedure says so", and that share grows with tooling depth.
**Design:** instrument one real wave (the audit + falsifier run) with a per-step field:
`why: chosen | procedure`. Two independent seats classify the 30 steps blind; keep only
steps both agree on. Report the ratio and the cost of the procedure-only steps.
**Cost:** ~10 calls ($0.01) + one wave's normal compute.
**Falsifier:** if blind classifiers agree on <60% of steps, "procedure-only" is not a
stable category — the lens is producing a feeling, not a measurement.
**Learn:** the estate's ritual overhead in time and dollars; which checks earn their
keep and which are habit.
**Artifact:** `watch/inbox/METHOD_INERTIA_<date>.md` with the step table.

## T3 — McLUHAN: does the surface change the decision?

**Question:** what does the form do to the reader, independent of content?
**Hypothesis:** the same finding delivered as chat prose, a receipt, a cockpit signal,
and a JSON table produces measurably different actions — form is not neutral.
**Design:** one finding, four surfaces, six lanes each. Ask each lane: "what is the next
action, and how confident are you?" Score action agreement per surface. (Operator-facing
version: same page as cockpit widget vs markdown, measure which he acts on first.)
**Cost:** 24 calls ($0.02).
**Falsifier:** if all four surfaces produce the same modal action, form is cosmetic and
the cockpit's design effort should stop.
**Learn:** which surface to standardise for decisions versus for evidence.
**Artifact:** `watch/inbox/SURFACE_EFFECT_<date>.md`.

## T4 — JUNG: what returns because it was disowned?

**Question:** which suppressed function comes back as a shadow?
**Hypothesis:** laws that forbid a capability (no second scheduler; no seat load-bearing;
chain is read-only) push that capability into unlogged ad-hoc scripts and scheduled tasks.
**Design:** census every scheduled task, every script that writes outside the sweeper, and
every process that holds a lock, then map each to the law it would violate if named.
Count shadow infrastructure: things doing forbidden work without a name.
**Cost:** 0 calls — filesystem + schtasks only.
**Falsifier:** if every shadow process maps to a named, lawful owner, nothing is disowned
and the lens is projecting.
**Learn:** whether the estate's prohibitions are creating the very redundancy they forbid.
**Artifact:** `watch/inbox/SHADOW_CENSUS_<date>.md` (also a cockpit signal candidate).

## T5 — FERMAT: what is the cheapest true path?

**Question:** what is the cheapest route to the same place, counting everything?
**Hypothesis:** free lanes are not cheaper once silences, retries and operator minutes are
priced; the local ollama battery wins on repeated small tasks, paid lanes win on one-shot
judgment.
**Design:** five representative tasks (parable, audit, census summary, code fix, long
synthesis) × three routes (local 7B, free lanes, DeepSeek/z.ai) with wall-clock, tokens,
retries, dollars, and a blind quality score from a different lane.
**Cost:** ~45 calls ($0.06) + local compute.
**Falsifier:** if the local route is both cheaper and not worse on all five, the free-lane
rotation is unnecessary complexity and should be retired.
**Learn:** a cost table that can be quoted in future routing decisions instead of taste.
**Artifact:** `watch/inbox/ROUTE_COST_<date>.md` + machine table.

## T6 — HALL: intended reader vs actual reader

**Question:** who is this for, who actually reads it, and what does each decode?
**Hypothesis:** receipts are written for the writer, not the next seat; the implied action
is recoverable only by the author.
**Design:** three artifacts (a wave receipt, the cockpit output, the queue census). Ask a
fresh seat, a future-seat simulation (same lane, no context), and the operator: "what
action does this imply?" Measure three-way agreement on the implied action.
**Cost:** ~18 calls ($0.02) + one operator question.
**Falsifier:** if a fresh seat recovers the intended action ≥80% of the time, receipts are
already decoded and the readability work is unnecessary.
**Learn:** whether the estate's documents carry action or only record.
**Artifact:** `watch/inbox/READER_TEST_<date>.md`.

---

## What the six share

All six are **binding tests**, not capability tests. Today's finding was that statements
do not bind — not prohibitions, not laws, not map premises. Every test above measures
whether a *thing* (artifact, surface, route, receipt) changes behaviour, and each has a
falsifier that kills the lens's reading rather than confirming it.

## How Hermes and the skills layer should carry this

1. **One skill, not six.** Capture today's method as `estate-lens-lab`: the three-regime
   table, the harness commands, the traps (prohibition priming, self-audit role collapse,
   erasure/rails, wording-vs-meaning), and the falsifier discipline. The next seat loads
   it instead of re-deriving — which is precisely the failure today documented.
2. **Subagents for parallel waves.** `delegate_task` runs T1–T6 as six isolated children;
   each returns a receipt, the parent folds. That keeps the main context clean (today's
   session spent its window on one thread).
3. **Cron for the slow ones.** T1 (demand), T4 (shadow census) and the queue `live`
   counter are observational, not interactive — `cronjob_manage` runs them daily and
   appends to the tape, no seat awake.
4. **Widgets for the operator surface.** T3's finding should land as a cockpit signal, not
   a receipt, so the next decision is a glance. (The `::preview` surface already works.)
5. **fact_store for the durable claims**, receipts for the evidence, skills for the
   procedure. Today's lesson stored as a fact was fine; the *method* belongs in the skill,
   or the next seat re-runs the discovery.
6. **prior_art_check stays in front of all of it.** Each test above names the machinery it
   reuses; a new one that does not should not exist.

## Suggested order

T4 (free, immediate, feeds the cockpit) → T2 (cheap, explains today's waste) → T5 (cost
truth) → T1 (48 h clock, start early) → T3 (surface standard) → T6 (readability audit).
