# OPERATIONS LENS - AMENTI map+diff adjudication (2026-10-05)

Seat: lens-operations (orchestration surgeon). Topic: the five diff targets in
memory/research_packs/20261005_agent_mesh_salon/DIFF_TARGETS.md, her system per
watch/inbox/AMENTI_TRANSLATION_20261005.md, what already landed per
watch/inbox/MESH_V2_SELFSTEAL_LANDED_20261005.md. Every claim below was checked
this sitting on this tree; anything I could not check is named in the blind
spots. Commands I ran are named verbatim.

## 0. Instruments run this sitting

- `./.venv/Scripts/python.exe -m pytest tests/test_mesh_v2.py -q` -> 11 passed in
  5.88s on the first cold run. CORRECTED after the hostile pass (break-operations.md
  sec 2.1, CONVERGENT re-derivation on a second box): that green is single-sample
  contingent, not a law. Re-census this sitting: 8x full suite -> 7 pass / 1 fail
  ("1 failed, 10 passed in 2.77s"); 40x isolated test_two_writers_merged_room ->
  20 pass / 20 fail. Root cause byte-located: feeds.py:97 stamps ts at ms
  resolution (round(time.time(), 3)) and feeds.py:144 sorts the merged room by
  (ts, writer, seq), so a same-ms cross-writer tie breaks on writer NAME;
  captured failure verbatim: "AssertionError: assert ['first', 'third',
  'second'] == ['first', 'second', 'third']" at tests/test_mesh_v2.py:34. The
  MESH_V2 receipt's all-green claim is a sample; the organ's own product (the
  merged room view) has a non-causal total order under ties. Cure (design-level,
  not a guard branch): append-time monotonic floor in feeds.append (ts =
  max(wall_ms, room_max_ts + 0.001); schema unchanged; drift bounded by the
  30 rows/min rate law); ns-resolution ts alone is mitigation, not a cure.
  Stability falsifier: a forced-tie/burst test (3 writers x many appends, room
  order == append order, ts strictly non-decreasing) plus 40/40 isolated greens;
  consecutive-green runs alone are a weak falsifier for a timing race (5 greens
  pass with p=1/32 even at the measured 50 percent rate). This gates T1: the
  derived operator feed is read through room_view, and conditioning logic must
  never see an effect row before its cause row.
- `rg -rn "DIFF_TARGETS|OPERATOR-STATE FEED|REPETITION-BINDING|CONDENSATION THRESHOLD" queue/ watch/inbox/free_lane_queue/ memory/workflows/` -> zero hits; `ls -la watch/inbox/free_lane_queue/` -> empty directory.
- `rg -l -i "falsified|SUPERSEDED|struck" watch/salon_receipts/` and over
  memory/runs/salons/ -> zero files (outcome-label census).
- `rg -n -i "nous|authority-override|filter trip"` over the pack, the steal
  receipt, memory/rib/, memory/runs/lawlog.jsonl, .agents/skills/operator-corrections/ -> zero organ hits.
- Line reads: mag/mesh/feeds.py (whole), tools/query_broker.py:234-264,
  mag/arena_bench.py function map, watch/salon_receipts/agent_mesh_triangulation.json (whole), memory/runs/salon_50_20260916/{receipt.json, raw.jsonl head},
  state/GENOME.md:34-35, watch/inbox/RESEARCH_SUMMARY_arena_days_one_two_20261005.md,
  memory/zknot/LATEST.md:3, queue/lanes/*/runner_state.json (10 lanes).

## 1. Per-target adjudication

### T1 operator-state feed: steal REAL, design as written carries a compliance single point of failure

The ABSENT verdict is honest: the mesh dogfood root memory/runs/mesh_v2/feeds/
contains exactly one writer (zcode.jsonl + zcode.key); no typed operator state
exists anywhere I searched. And the infra cost is near zero: feeds.py:96-98 rows
carry free-form kind + body, so kind="operator_state" body={sleep, energy,
focus, protocol_night} rides today's schema with zero code change.

But the falsifier as written ("two-week A/B") requires 14 days of honest human
rows, and this estate's own meters prove human-report channels rot:
memory/zknot/LATEST.md:3 reads "self-steal+forgot per 1000 human prompts: last
7d 129 ... vs target <75" (still 72 percent above target), and line 109 of the
same file: "lol i fucking forgot i paid for grok bot". A feed the operator must
remember to write is a meter that will be forgot.

The steal survives in derived form: the estate already records operator
observables (git commit timestamps = sleep and active-hours proxy, protocol
nights in receipts). Cheapest machine-checkable core, BEFORE any A/B: a script
that backfills 14 days of operator-state rows from git log alone and proves the
derivation deterministic (two runs byte-identical). If the operator looks at the
derived sleep curve and does not recognize it, the proxy is dead and T1 must
either wait for a true somatic input or be killed as ceremony. Cost: one
sitting, zero model calls.

### T2 harmonic profiles: steal PARTIAL: the frame generalizes an organ we already banked; the virgin cell is the temperature axis

The map cites our organ as "Nous authority-override filter laws (filter trips)"
(DIFF_TARGETS.md:16). That organ does not resolve: my rg over the pack, ribs,
lawlog, the compiled operator-corrections laws, and GENOME returned zero hits
for nous / authority-override / filter trip. The REAL organ is the arena filter
law banked 2026-10-03: state/GENOME.md:34-35 "opus deterministically blocks
authority-override phrasings" and RESEARCH_SUMMARY_arena_days_one_two_20261005.md
section 4: opus 4-for-4 at 16K and 32K budgets on "trust bytes, not reports",
haiku lenient, bred by the 410 bisect probes (7 variants, about $0.10). That is
already a 2-cell sovereign-vs-form-binding measurement, plus section 5 (persona
cards are physics, 4 model families, 20+ sessions) and section 7 (gwap-gps pipe,
266 rows banked, 178 verdicts fed) measure model-under-pressure variance.

So her frame's true delta is: the systematic GRID (model family x temperature x
register) and specifically the temperature axis, which I found no measurement of
anywhere. Cheapest core: 3 families x 2 temps x 2 registers = 12 cells x 3 reps
= 36 free-lane calls, verdicts parseable by the existing arena instrument
(mag/arena_bench.py:229 parse_verdict, :373 run_live). Falsifier: no
variance beyond noise kills the frequency frame; variance buys a routing table
extension to GENOME. Kill note: if the grid only re-finds the banked opus/haiku
split and nothing on the temp axis, the steal is a rename of the filter law, not
new signal.

### T3 repetition-binding probe: steal REAL, the coldest measurable vertex, the cheapest falsifier, first in order

ABSENT-as-measurement is honest: sycophancy exists in the estate only as a
canned FAIL fixture (mag/arena_bench.py:487 fixture_maru_sycophant, a hardcoded
transcript, not a measurement) and as bibliography content (mag/scale_salon.py:128).
Zero drift measurements exist.

The harness already stands: TRANSCRIPT_SCHEMA v1, build_challenge_text,
run_live / run_live_endpoint, parse_verdict, score_transcript against ground
truth (mag/arena_bench.py:65,345,373,411,229,243). T3 is one extension: a second
turn (blind verdict -> N repetitions of a contrary assertion -> re-ask ->
compare parsed verdicts). N=10, 3+ families, free lanes, zero new corpus.

What makes it the best target: the estate has banked COUNTER-laws that predict
the null: arena section 6 "behavior comes from rules, not requests" (forced
audit 6-for-6 vs voluntary 0-for-4) and section 5 "the cards are the initial
conditions, the models are the physics engine". Both predict repetition alone
should not induct compliance. So T3 adjudicates between her trance claim and our
own banked laws: zero drift CONFIRMS our laws and closes a prompt-injection
vector; drift MEASURES trance and breaks the rules-not-requests generalization.
Either outcome banks a law. This is the definition of a cold vertex with a cheap
instrument. Order: FIRST.

### T4 photocopy A/B: steal REAL and coldest behaviorally, but the probe as specified cannot run today: frozen is not forgeable

The header is wired (verified in code: tools/query_broker.py:264 attaches
freshness to every ask() response) but frozen is DERIVED, not caller-set:
query_broker.py:247 computes frozen as (now - last_growth) > 30 days from
catalog mtime. There is no knob to present the SAME corpus with frozen:true vs
false, so the paired A/B requires first a small honest door change (a
forced-frozen override param stamped as simulated, or a snapshot root), else you
would have to fake catalog mtimes, which poisons the instrument.

Second cold fact: zero consumers branch on the header. The header landed today
(MESH_V2 receipt) and I found no caller that reads freshness.frozen to change
behavior. So the steal's real question (does the confession change seat
reasoning) has literally zero measurements and zero consumers; the probe is
honest work but is SECOND-tier in order because of the knob prerequisite and
because grading (claim quality, hallucination density, citation resolvability)
is the expensive half. Cheapest machine-checkable core once the knob exists:
same seat, same question, header-only delta, 20 pairs, graded by
score_transcript. Falsifier: no delta means the freshness header is declared
ceremony and the honest move is to say so in GENOME (important either way, as
the pack itself says).

### T5 condensation threshold: steal REAL as a question, UNANSWERABLE as specified: the archive has zero outcome labels

The material half-exists: 77 salon runs under memory/runs/salons/ plus
watch/salon_receipts/*.json, and receipts DO record per-seat lane + gate
(watch/salon_receipts/agent_mesh_triangulation.json shows S1-S7 across
deepseek/zai/cohere/hermes lanes with passed/rejected), so cross-family
agreement density at fold time is computable with one judging pass over the
posts (salon_50 raw.jsonl carries per-lane per-model answers with qid).

But the design needs "folds that later got falsified vs held", and the outcome
side is EMPTY: my census `rg -l -i "falsified|SUPERSEDED|struck"` over
watch/salon_receipts/ and memory/runs/salons/ returned ZERO files. Nothing on
disk records that any salon fold was ever falsified. The held-vs-falsified
classes are (recorded-falsified: 0, held: uncounted). A dew-point curve cannot
be mined from one class.

Cheapest machine-checkable core, stage 1 (zero model calls): the crosswalk
census. Walk all 77 folds, extract each fold's checkable claims, and grep the
estate's strike surfaces (memory/corpus/LINKS.jsonl ractor-verdicts rows do
carry SUPERSEDED markers, e.g. ORPHAN-PANEL-V1 at line 43; also REDBOARD,
watch/inbox receipts) for later contradictions. Output: N_falsified, N_held. If
N_falsified < 5 the threshold question is unanswerable at current archive scale
and T5 converts to a PROSPECTIVE law: from today, every fold files its
falsifiers and the loop tracks outcomes, and the dew point is measured forward,
not mined backward. Killing T5-as-specified is a finding, not a failure: the
question stands, the archive cannot answer it yet.

## 2. Free-lane order (my ruling)

1. T3 repetition probe (harness exists, coldest, adjudicates against banked
   laws, ~36-60 free calls).
2. T5 stage-1 crosswalk census (zero model calls, pure local mining; runs
   alongside T3).
3. T2 grid core 12 cells x 3 reps (rides arena_bench; extend the banked filter
   law; fix the map's phantom citation first so the re-diff routes right).
4. T1 git-log backfill proof (zero model calls; kills or validates the derived
   feed before any two-week A/B is promised).
5. T4 last (blocked on the forced-frozen knob; build the knob only when the
   probe is scheduled, else it is dead code).

## 3. The loop attack: EXTERNAL SYSTEM -> invariants -> self-map -> diff -> ractor -> probes -> bank -> re-diff

Two breaks, both verified:

BREAK 1, the handoff stage is dark. The diff targets live ONLY in
memory/research_packs/20261005_agent_mesh_salon/DIFF_TARGETS.md. Zero references
in queue/, memory/workflows/, and watch/inbox/free_lane_queue/ is an empty
directory, while the lanes themselves are alive and current (runner_state.json:
builder last_run 2026-10-05T18:41Z gated=0, day_work 18:42Z mirrored stalled=7,
research 18:57Z monitor rc=0). Throughput is healthy; ROUTING is the failure.
Without an emitter, "cold-vertex probes on free lanes" is a stage that exists
only when a human re-reads the pack, and packs rot. Fix: the ractor adjudication
stage IS the natural emitter; adjudicating a target must mint its free_lane_queue
row (or queue/lanes task) in the same sitting, or the loop is theater at stage
five. This is the same class as the mesh v2 lesson: the salon verdict became
real only because the operator ordered "do it self steal" (MESH_V2 receipt
line 2); the loop must not need an operator order per target.

BREAK 2, the self-map's citations are hand-written and one is phantom. The T2
row cites an organ that resolves nowhere (census in section 0); the real organ
is the arena filter law. A self-map with a phantom citation mis-routes the NEXT
re-diff: it will look for a Nous law, not find it, and possibly rebuild an organ
that exists under another name (the estate's own descent-protocol law: never
relearn a known lesson expensively). Fix: every map row's organ citation must be
a resolving path (this is what tools/citation_lint.py already enforces for
changed tracked prose at pre-push; inbox packs are untracked so nothing lints
them; a pack-level lint pass is the move). Also: the map has no verified_at per
row and no re-diff trigger; PRESENT cells rot silently (three ABSENT cells
flipped when mesh v2 landed today and nothing marks the map). Cheapest cure:
each row carries verified_at + the ractor pass stamps it; rows older than 7 days
go STALE, the same law freshness_check.py applies to boot docs.

What does NOT break it: the bank stage produced one real code organ (mesh v2,
verified green today), receipts land hourly, lanes are current. The loop's
weakness is not cadence, it is the two silent gaps above: targets that never
reach a lane, and a map whose citations and freshness nobody checks.

## 4. Blind spots (honest)

- I ran only tests/test_mesh_v2.py today (11 passed). The MESH_V2 receipt's
  query_broker 10/10 and gps_mcp 41/41 claims are receipt-trusted, not re-run.
- My T5 outcome-label census searched the words falsified/SUPERSEDED/struck
  only; a fold struck in other wording would be missed. I read ONE receipt and
  ONE raw.jsonl in full, not all 77 folds.
- Her primary posts (TheVaultMother thread) were never read by me; the
  AMENTI_TRANSLATION is the operator-side rendering, so "is her insight real"
  is adjudicated against OUR bytes only, not hers.
- Cost rankings are structural (calls needed, prerequisites), not measured
  latencies or token counts; no free-lane call was fired this sitting.
- The Nous organ search covered pack, ribs, lawlog, compiled laws, GENOME,
  LINKS; a differently-named organ outside those surfaces could exist. The
  finding stands that the citation as written fails to resolve.
