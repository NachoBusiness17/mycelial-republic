# STEAL CARD: swarm-orchestration via x (frontier OLM 2026-10-09, ROUND 1)

Two confirmed finds from the X door, both carried by today's sweep receipt
(watch/inbox/frontier_olm_2026-10-09/sweep/swarm-orchestration-x.md, read in full this
session) with the raw door JSONs cached beside it: _fx_shashj.json (2,542 bytes) and
_fx_sethlazar.json (3,909 bytes). Both quotes re-verified byte-present this session:
grep -c returns 1 for each quote phrase and grep -o finds each status ID in its file.
Grounding rule: every claim cites path:line or URL; anything this seat did not read or
run this session is OWED, never asserted. No em dashes.

## R1. PRIOR HOLDINGS (reconciled before banking; re-banking known work is waste)

Width economics:
- The estate's measured THROUGHPUT envelope is standing law, read at source this
  session: AGENTS.md:35 (fan-out width law: Task agents clean at widths 3/6/10/12,
  width 10 banking 109.4M tok/h, the limit is rolling throughput, not width-only) and
  AGENTS.md:36 (max-concurrency standing law: 5 gated workflows at max_concurrency 10,
  first rate-limit contact is a HOLD signal, not a width cut).
- The same round's arxiv sibling card (watch/inbox/frontier_olm_2026-10-09/steal/
  swarm-orchestration.md, read in full this session) already banks the Ord composed
  law (lambda*gamma) as EWMA width shaping (its FIND 1, :70-92) and the SquidAgent
  predicted-token parallelize test in the G8 family (its FIND 2, :113-137). NOT
  re-banked here.
- The underlying Toby Ord "Swarm Scaling" essay is estate-held (sweep :118-124:
  memory/runs/quote_audit_wide_20260925/inbox_concat.txt:1563, the 10-01 sweep's
  lambda tweet, the 10-02 HN sibling baseline).
- The genuinely new bytes in FIND 1 below are ONLY the practitioner pricing split
  (2x total tokens, 0.5x tokens per agent, 0.5x wall clock at N=4) and its port as a
  budget line; the sibling card carries no such split (verified by read, this
  session), and no card in this dir carries it.

Collective model:
- The gate already enforces the pass-off shape: tools/workflow_gate.py:15 (G2 passoff:
  "an earlier actor's output feeds a later ask", check registration at :159-160) and
  Mickey17 per-item named actors at :14. The G2 PLACEMENT law (:86-108, from the
  10-07 ArcticSwarm card) fixes WHERE the interagent feed lives (at review, never
  during search).
- tools/receipt_xref_gate.py:2-11 meters dead citations inside watch/inbox receipts
  (WARN-only by default, :23-28). None of these measures whether a downstream actor
  holds an explicit model of who holds what. The gap Lazar names is real: verified
  absent this session.

## FIND 1 (PRIMARY): the Joshi width-pricing split -> a water-graph width-price line + a context-pack per-child shrink

Source: https://x.com/shashj/status/2107117440303833257 (2026-10-05 14:35Z, 7,474
views per sweep :128). Quote verbatim, byte-verified in _fx_shashj.json this session:
"The 4-agent swarm needed about twice the total number of tokens to get the same
performance, but in terms of tokens per agent, it only needed half as many. Since the
agents are run in parallel, this means it can theoretically achieve the same task in
half the time" (full two-sentence form carried by sweep :129-132). Carrier: Import AI
475 (importai.substack.com/p/import-ai-475-swarm-scaling-google, fetched in full by
the sweep lane this sitting, sweep :132-136); the study is Toby Ord's, NOT Google
DeepMind (the slug's "google" is newsletter section branding, the sweep's correction
at :134-136).

Port, two moves on two organs:

(a) WATER GRAPH, the price line. The bill lands on TOTAL tokens, so width gets a
budget line, not just a speed line. The host exists: memory/workflows/FIRE_LEDGER.jsonl
rows already carry fired_width beside max_concurrency and width_discrepancy (tail row
read this session: ts 2026-10-07T14:02:19Z, fired_width 50, width_discrepancy true,
max_concurrency 3; the exact columns the gate docstring promises at
tools/workflow_gate.py:81-84). Port: join fired_width to the burn ledger
memory/runs/hermes_burn/usage.jsonl (702,596 bytes, ls this session) and stamp, per
gated run, a width-price forecast whose prior is the Joshi point (about 2x total
tokens at 4x width, sublinear), with the estate's own exponent to be measured, never
assumed. This gives AGENTS.md:36's "maintain this shape usefully" clause its cost
number: the fleet is useful when the total-token price per wall-clock hour saved
beats the serial alternative.

(b) CONTEXT PACK, the shrink corollary. 0.5x tokens per agent means width is also a
context SPLITTER, not only a speed device: at 4-wide and equal performance, each
child's ask+pack can shrink toward half the monolith pack. Host verified first-hand
this session: the child-ask construction sites in .zcode/workflows/olm-mine.dwf.ts
(the areas config carries per-area questions + estate_map at :143-148, including
swarm-orchestration "Gopher fleet, envelope law, workflow gate" at :146; the
steal-round ask reads the confirmed finds at :396-404). The sibling card's G8
predicted-token check (its FIND 2) is the adjudicator for whether the shrunk parallel
estimate still beats serial; this card adds the sizing prior that check consumes.
Honest limit: the 0.5x is measured on Ord's swarm-scaling task family, not on estate
asks; the estate's own per-agent shrink number is OWED to measurement, and both
priors are stamped as priors, never as local truth.

## FIND 2: the Lazar collective model -> a who-holds-what roster in every pass-off ask (soft G2 row)

Source: https://x.com/sethlazar/status/2099142728168697912 (2026-09-13 14:26Z, 2,056
views per sweep :185). Quote verbatim, byte-verified in _fx_sethlazar.json this
session: "One of the most interesting things about the swarm is how the agents relate
to one another, what their model of the collective is and how self interest (under
some description) and collective interest map." Thin pointer item: the "here" link
target is not resolvable from the fetched JSON (sweep :195, OWED).

Port, one mechanism: every ask that consumes an earlier actor's output carries TWO new
lines: (i) the pointer to the upstream artifact (path and/or hash, so the consumer
loads rather than re-derives), and (ii) a one-line who-holds-what roster (which seats
own which slices, so the consumer knows what NOT to redo). This complements the G2
placement law (WHERE the feed lives, tools/workflow_gate.py:86-108) with WHO is
modeled inside the feed, exactly the variable Lazar names. Landing shape: a WARN-level
soft row beside the G2 check, in the same soft family the gate already runs for the
G6 dated stamp and the G3 judge-model stamp (tools/workflow_gate.py:101-104), under
the gate's own stated epistemics (:105-108): the detector is a grep approximation by
design, and a false warn is a review conversation, not a blocked push.

Why it lands on the gopher fleet: the fleet's passes are already named-actor shaped
(tools/workflow_gate.py:14) and the registry already records per-check verdicts (tail
row of memory/workflows/REGISTRY.jsonl read this session: G1 through G5 all ok:true
with descs, ts 2026-10-07T14:02:19Z), so the roster is a one-line ask convention plus
a soft gate row, not new plumbing. The receipt-xref gate (tools/receipt_xref_gate.py)
already proves pointers resolve once written; this find makes the pointer EXIST at the
pass-off, upstream of that gate.

## ESTATE MAP SUMMARY

- gopher fleet: both finds. FIND 1 prices the width dial in total tokens (fire-ledger
  join); FIND 2 puts the collective roster in every pass-off ask.
- water graph: the FIND 1 width-price meter beside token burn (FIRE_LEDGER.fired_width
  joined to memory/runs/hermes_burn/usage.jsonl); flow-vocabulary home
  tools/k8s_water_sim.py and tests/test_k8s_water.py both verified on disk this
  session (ls).
- context pack: the FIND 1 per-child shrink prior, stamped at the child-ask
  construction sites (olm-mine.dwf.ts:143-148, :396-404), adjudicated by the sibling
  card's G8 predicted-token check (tools/workflow_gate.py:385/:427 per the sibling
  card, not re-verified by this seat).
- workflow gate (named host inside the fleet): the soft G2 collective-model row,
  soft-family precedent tools/workflow_gate.py:101-108.
- quantizer: NOT a host. mag/auto_quantize.py:56 (class Quantum) and :110 (class
  AutoQuantizer) verified this session as storage-state quantization, matching the
  sibling card's finding; no token-budget surface there.
- percolator and sovereign mirror: no direct feed this round, stated as such, not
  stretched. configs/mirrors.json head read this session: it is the provider mirror
  census (hosts/models/churn rows, ts 2026-10-09T16:15:05Z), no pass-off surface.

## PROBE (one falsifiable probe, offline, this week, zero paid dispatch)

The cite-vs-restate census over the estate's own pass-offs. Corpus verified this
session: memory/workflows/REGISTRY.jsonl carries 125 G2-passoff rows (grep -c);
.zcode/workflows holds 20 scripts, all 20 carrying report() (grep -l | wc -l);
.zcode/workflow-drafts holds 94 more. Method: for each script with a G2 row, find the
downstream ask that consumes an earlier actor's output; classify CITES (the ask
interpolates a path/hash/report() pointer to the upstream artifact) vs RESTATES (the
ask embeds a content copy with no pointer). PRE-REGISTERED threshold, fixed before
running: if MORE than half of classified pass-offs already CITE, Lazar's variable is
already implicit in estate practice and this card's port collapses to a name (the
falsifier fires; the soft row is not drafted); if half or fewer CITE, the collective
model is a measured gap and the soft G2 row gets drafted with the census as its
founding evidence. Cost: greps and reads over on-disk scripts, about one seat-hour,
no dispatch.

Companion calibration read for FIND 1 (cheap, not the probe): join FIRE_LEDGER
fired_width rows to daily burn in usage.jsonl and report the burn-per-width-point
scatter. The Joshi prior predicts sublinear scaling (about 2x at 4x). Confound named
in advance: heterogeneous tasks and no same-performance control offline, so this is
calibration, not a test; the real test needs the sibling card's forward G8 estimate
data.

## V. VERIFICATION LOG (all commands and reads run this session, this seat)

1. Quote byte-presence: grep -c "twice the total number of tokens"
   watch/inbox/frontier_olm_2026-10-09/sweep/_fx_shashj.json = 1; grep -o
   "2107117440303833257" present; grep -c "model of the collective"
   .../sweep/_fx_sethlazar.json = 1; grep -o "2099142728168697912" present. wc -c:
   2,542 and 3,909 bytes.
2. Sweep receipt read in full this session: FIND 1 = its item 2 (:126-145, including
   the "half the time" sentence :129-132, the Import AI 475 fetch and the not-Google
   correction :132-136), FIND 2 = its item 4 (:183-196, thin item, "here" link OWED
   at :195), RQ4 verdict (:238-243), overlap greps (:245-258).
3. Standing laws read at source: grep -n on AGENTS.md returns the fan-out width law
   at :35 and the max-concurrency standing law at :36.
4. Gate anchors: tools/workflow_gate.py:80-108 read (G2 placement law with the
   soft-family precedent at :101-108); check table at :14-15 and registration at
   :156-160 (grep output).
5. Prior holdings: the same-round arxiv sibling card read in full (FIND 1 :70-92,
   FIND 2 :113-137, estate map :181-197); the 10-07 card's steal summary read
   (ArcticSwarm ladder, its :299-302) and its JSON-block convention located at :292
   (grep -n "Machine-readable card").
6. tools/receipt_xref_gate.py:1-60 read (dead-citation meter for receipts, WARN-only
   :23-28, skills_lint self-steal :9-11).
7. Organ files: mag/auto_quantize.py grep (class Quantum :56, class AutoQuantizer
   :110); tools/k8s_water_sim.py and tests/test_k8s_water.py exist (ls);
   memory/runs/hermes_burn/usage.jsonl exists, 702,596 bytes; configs/mirrors.json
   head read (provider census shape).
8. Ledger schemas: tail -1 of memory/workflows/FIRE_LEDGER.jsonl (fired_width 50,
   width_discrepancy true, max_concurrency 3, ts 2026-10-07T14:02:19Z); tail -1 of
   memory/workflows/REGISTRY.jsonl (checks array, G1-G5 ok:true, same ts).
9. Probe corpus census: grep -c "G2-passoff" memory/workflows/REGISTRY.jsonl = 125;
   grep -l "report(" .zcode/workflows/*.dwf.ts | wc -l = 20 of 20; ls count of
   .zcode/workflow-drafts/*.dwf.ts = 94.
10. Construction sites: grep on .zcode/workflows/olm-mine.dwf.ts (areas config with
    questions + estate_map at :143-148) and :396-404 read (the steal-round ask
    consuming confirmed finds).
11. URL slug check: grep -o "import-ai-475[a-z-]*" on the sweep receipt returns
    import-ai-475-swarm-scaling-google, matching the carrier URL in FIND 1.

## OWED (not asserted)

- The Ord essay's own numbers (gamma exponents, the 10,000x/20x token figures):
  carried by the sweep receipt read this session (:92-124), not independently
  re-fetched by this seat; the essay itself is estate-held per sweep :118-124.
- The Import AI 475 body: fetched in full by the sweep lane this sitting, not by this
  seat (sweep :132-136).
- The Lazar "here" link target: unresolvable from the fetched JSON (sweep :195 and
  the artifact list :272-273).
- The estate's own width-price exponent and per-agent shrink number: unmeasured; the
  Joshi/Ord values are priors only until the companion read and the G8 data land.
- The soft G2 collective-model row and the width-price meter: design banked here, not
  landed code; this card changes no behavior.

## Machine-readable card (identical to the returned StealCard JSON)

Appended by the drafting seat per the 10-07 sibling convention
(watch/inbox/frontier_olm_2026-10-07/steal/swarm-orchestration.md:292), as practiced
by today's arxiv sibling (:321-325); chars counts this file's characters including
this block, measured after the append.

```json
{
 "area": "swarm-orchestration via x",
 "steal": "Two mechanisms, holdings-reconciled against the same-round arxiv sibling card and the standing width laws. (1) PRIMARY, the Joshi width-pricing split (quote byte-verified in watch/inbox/frontier_olm_2026-10-09/sweep/_fx_shashj.json this session; carried by the sweep receipt :126-145 with its Import AI 475 correction: the study is Toby Ord's, not Google DeepMind): a 4-agent swarm costs about 2x TOTAL tokens, 0.5x tokens per agent, 0.5x wall clock at equal performance, so width buys time, not capability, and the bill lands on total tokens. Port on two organs: (a) water graph: a width-price budget line stamped per gated run by joining the fire ledger's existing fired_width column (memory/workflows/FIRE_LEDGER.jsonl tail row verified: fired_width 50, width_discrepancy true) to token burn in memory/runs/hermes_burn/usage.jsonl, prior = the Joshi 2x-at-4x point, the estate's own exponent to be measured never assumed, giving AGENTS.md:36's maintain-usefully clause its cost number; (b) context pack: the 0.5x-per-agent corollary makes width a context SPLITTER: per-child ask+packs may shrink toward half at width 4, stamped at the child-ask construction sites (.zcode/workflows/olm-mine.dwf.ts:143-148 areas config, :396-404 steal-round ask, verified first-hand) and adjudicated by the sibling card's G8 predicted-token check, priors marked as priors since the 0.5x is Ord's task family, not estate asks. (2) The Lazar collective model (quote byte-verified in _fx_sethlazar.json; sweep :183-196, thin pointer item, the 'here' link OWED): the gate enforces that a pass-off EXISTS (tools/workflow_gate.py:15) and WHERE it lives (placement law :86-108) but nothing measures whether the downstream actor holds a model of who holds what. Port: every pass-off ask carries (i) the upstream artifact pointer (path/hash) and (ii) a one-line who-holds-what roster, landed as a WARN-level soft row beside G2 under the gate's own soft-family precedent (:101-108: grep approximation by design, a false warn is a review conversation, not a blocked push); the receipt-xref gate (tools/receipt_xref_gate.py) already proves pointers resolve once they exist, this find makes them exist at the pass-off.",
 "source_url": "https://x.com/shashj/status/2107117440303833257",
 "estate_map": "gopher fleet: both finds, the width dial priced in total tokens and the collective roster in every pass-off ask; water graph: the FIND 1 width-price meter beside token burn (FIRE_LEDGER.fired_width joined to memory/runs/hermes_burn/usage.jsonl, 702,596 bytes verified), flow-vocabulary home tools/k8s_water_sim.py and tests/test_k8s_water.py verified on disk this session; context pack: the 0.5x per-agent shrink prior stamped at the child-ask construction sites (olm-mine.dwf.ts:143-148, :396-404) and adjudicated by the arxiv sibling's G8 predicted-token check (tools/workflow_gate.py:385/:427 per the sibling card, not re-verified by this seat); workflow gate: the soft G2 collective-model row beside the existing pass-off check (:15, registration :159-160, placement law :86-108, soft family :101-108); quantizer: NOT a host, mag/auto_quantize.py:56/:110 verified as storage-state quantization this session; percolator and sovereign mirror: no direct feed this round, stated as such (configs/mirrors.json head read: provider mirror census, no pass-off surface). Prior holdings honored: the Ord composed law and the SquidAgent test are the same-round arxiv sibling's bank, not re-banked; AGENTS.md:35/:36 are the base envelope, the pricing split is the only new byte; the G2 placement law already owns WHERE the feed lives, this card adds only WHO is modeled in it.",
 "probe": "The cite-vs-restate census over the estate's own pass-offs, offline, zero paid dispatch, corpus verified this session: memory/workflows/REGISTRY.jsonl carries 125 G2-passoff rows (grep -c), .zcode/workflows holds 20 scripts all carrying report() (grep -l | wc -l = 20 of 20), .zcode/workflow-drafts holds 94 more. Method: in each script with a G2 row, find the downstream ask that consumes an earlier actor's output; classify CITES (the ask interpolates a path/hash/report() pointer to the upstream artifact) vs RESTATES (the ask embeds a content copy with no pointer). PRE-REGISTERED before running: more than half CITES means Lazar's variable is already implicit in estate practice, the falsifier fires, and the soft G2 row is not drafted; half or fewer CITES means the collective model is a measured gap and the soft row gets drafted with the census as founding evidence. Cost: greps and reads over on-disk scripts, about one seat-hour. Companion calibration read for FIND 1 (not the probe): join FIRE_LEDGER fired_width rows to daily burn in usage.jsonl for a burn-per-width-point scatter; the Joshi prior predicts sublinear scaling (about 2x at 4x); named confound: heterogeneous tasks and no same-performance control offline, so calibration only, the real test needs the sibling card's forward G8 estimate data.",
 "chars": 18923
}
```
