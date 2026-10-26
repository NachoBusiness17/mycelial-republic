---
name: drift-instrument-metric-referent-20260918
description: THE DRIFT INSTRUMENT BUILT (tools/drift.py) — metric-referent decoupling organ; drift_check computes corr(ΔM,ΔR), verdicts VACUOUS/ALIGNED/DRIFTING/INVERTED; operator NAMED IT "worldline lenses" (2026-09-18); CORRECTION 9/26 burn lane B2-05: "registry 32" was false against bytes, true registry is 12 pairs / 14 checks; 5 pairs stamped (2 ALIGNED / 3 DRIFTING); thrash-register sibling built
metadata:
  node_type: memory
  type: project
  originSessionId: sess_c424b80a-5f44-4511-bcdb-8dcec10fdce9
---

The operator pasted a five-document triangulation
(watch/inbox/METRIC_REFERENT_TRIANGULATION_20260918.md, itself the product
of his manual 11-model bus + DeepSeek merge) whose identity finding:
**metric-referent decoupling** — a system measures its rate of change (cheap)
and calls that orientation, while the truth instrument that would say whether
the movement is north (expensive) sits unbuilt. All five documents (fleet,
FedNow briefing, chronicle, fold, bibliography) share one missing number:
corr(ΔM, ΔR). The doc ends with a dare: build the drift instrument or shelve
it like everything else.

**Built the same hour:** `tools/drift.py` (pure compute, read-only,
registered in TOOL_MAP, MCP-exposed; NOTE the "registry 32" once written here
was disproven by burn lane B2-05 on 2026-09-26 against bytes: drift.py holds
no registry file, true count 12 pairs / 14 checks in
tools/drift_pairs_stamp.py + memory/runs stamps). `drift_check(metric,
referent, window, label)` computes deltas, Pearson corr(ΔM, ΔR), and stamps
verdicts: VACUOUS (referent never moved — the metric measures motion with no
measured destination) / ALIGNED (corr ≥ +0.5) / DRIFTING (weak) / INVERTED
(corr ≤ −0.5, stop trusting the metric) / INSUFFICIENT (<3 deltas).
`drift_check_cmd` takes comma-separated series for MCP/CLI callers.

**First honest stamp fired at ourselves:** metric = fleet tools added this
window (28,31,31,31), referent = measured queries served through those tools
(0,0,0,0 — we have no usage meter). Verdict: **VACUOUS.** The askability
program added tools without ever measuring whether anyone asked. The stamp
is the correction the whole window was building toward.

**Operator naming (2026-09-18, same day): "it's like worldline lenses."**
Each drift pair = two worldlines read against each other over one window;
corr(ΔM,ΔR) = the divergence meter between them; VACUOUS = a frozen worldline
(referent never moved), ALIGNED = one line, DRIFTING = separated lines,
INVERTED = anti-worldline (instrument lying with precision). Lineage: crab
canon TSVF + Steins;Git divergence meter (battery A08) + the triangulation's
missing number. Filed as LINKS row WORLDLINE-LENS.

**First five real pairs stamped (memory/runs/adv_arc_50/drift_stamps.jsonl):**
builder/day_work ALIGNED; Mr Pool downloads vs channel media ALIGNED (the
reconstruction is proportionally true); research-activity vs LINKS-added
DRIFTING; lane-activity vs git-commits DRIFTING; night-lane vs elder-lane
DRIFTING (night produces, elder audit surface not moving with it).

**Sibling instrument built same hour:** thrashing coefficient register
(ADV-I-7, memory/runs/adv_arc_50/thrash_register.json) — CYCLE_FAIL/committed
rows per lane; fleet max 0.125 (harvest, small n), research 0.029 at n=1343
→ broadcast-only coordination healthy, no private-channel debt; caveat:
elder shows 0.0 only because CYCLE_FAIL rows exist since the 09-18 fix.

**Law:** a rate metric answers "is it moving"; only corr(ΔM, ΔR) answers
"is it moving north." Apply to every fleet metric: LINKS rows vs links
actually cited, receipts vs actions changed, vision passes vs decisions
informed. The VACUOUS stamp is not shame — it is the pre-registration that
makes the metric honest.

**Arc sequence executed same day (all filed):** four-condition experiment
PRE-REGISTERED (watch/inbox/FOUR_CONDITION_PREREGISTRATION_20260918.md —
cold/warm-static/warm-append-only/warm-deleting, SCS = 1 − pairwise JSD,
5 fixed decision rules, amendment ledger opened so thresholds can't move
silently; v1 = 12-seat pods, scaling claim out of scope); tombstone GC
boundary law + DISTINGUISH schema drafted for operator gate
(watch/inbox/ARC_LAWS_20260918.md — "the archive remembers; the active view
is innocent; the tombstone stands between them"; G02 pack-watermark race
named as first enforcement fix; DISTINGUISH = narrowest-predicate-wins,
never model-voted).

**BKM twin + the CLIFF SCALAR law (2026-09-18 evening):** the worldline lens
has a PDE twin — Beale-Kato-Majda: a smooth flow dies only if the
time-integral of PEAK vorticity diverges, i.e. a system can look fully
smooth while an unwatched integral of an extreme grows silently toward a
cliff. Law candidate filed (SELF_STEAL_CORPUS_SKILLS_20260918.md): EVERY
INSTRUMENT MUST NAME ITS CLIFF SCALAR (integral of an extreme, not an
average, whose growth the headline metric can mask); an instrument that
cannot name one is decoration. Fleet cliff scalars: thrash coefficient,
corr(dM,dR), ink coastline; first corpus application: Mr Pool countdown
density (see [[riddle-triad-cadence-20260918]]). Also from the same fold:
the BARRIER-METHOD doctrine (Tao averaged blowup = the DeepSeek arc in PDE
form): to prove a structure load-bearing, build the averaged model that
strips it and break the average on purpose; barrier first, build second.

Related: [[corpus-map-salon-20260918]], [[self-steal-deep-20260918]],
[[riddle-triad-cadence-20260918]], [[codex-lens-pilot-design-20260918]]
