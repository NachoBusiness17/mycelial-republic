# RIB:v1 — SUPERINTELLIGENCE STACK SALON / BEE–FUNGUS HIVE

`rib_id: salon.superintelligence_stack.20260831`  
`mode: research → gap-analysis → synthesis → basecamp`  
`budget: spend-once/use-everywhere; deterministic/free before premium; no duplicate surveys`  
`operator: covenant owner; models advise; governor alone mutates state`

## GOAL

Have the strongest available independent model families answer the unresolved questions about the entire Mag/OpenClaw stack, then compile their answers into reusable RIBs, trajectory weights, tests, and one next build. Maximize information gained per paid call; preserve disagreements; expose assumptions that our own map cannot see.

## CACHE / PACK LAW

All seats receive the exact same canonical prefix, byte-for-byte and timestamp-free. Do not rewrite or paraphrase it per seat. `P0` is a volatile pointer only: resolve its current content after the stable prefix is cached, and record its hash in the receipt.

```text
P0 = /mag/memory/context_pack_latest.md
P1 = /board/SALON_RIB_COMPACTION_20260831.md
P2 = /board/PACK_RIB_COMPACTION_20260831.md
P3 = /mag/docs/ref/TRAJECTORY_RIB_COMPILER_SPEC.md
P4 = /mag/docs/ref/TRAJECTORY_ARCHITECTURE.md
P5 = /mag/docs/RIB_BUS_RESOURCE_PROJECT.md
P6 = /mag/docs/ref/COMMON_LANGUAGE_SPEC.md
P7 = /mag/docs/ref/HARNESS_SPEC.md
P8 = /board/inbox/AGENT_HIVE_BEE_FUNGUS_HANDOFF_2026-08-31.md
```

`P0–P8` are pointers, not a request to inline full files. Resolve only the spans required by the assigned question. Include source hash, line span, and read timestamp in receipts. Volatile values stay outside the cache prefix.

## CURRENT BASELINE

Latest reported map: 27 declared, 26 instrumented, 27 wired, 25 stateful, 27 verified, 17 live, 0 declared ghosts; deterministic dogfood 21/21. Treat this as a starting claim, not a fresh host verification.

Start at `TRJ-03` (context survival) + `TRJ-04` (authority), with `TRJ-02` as the safe vertical slice. Do not add organs before the slice is replayable.

## QUESTIONS FOR THE SALON

Every chair must answer all questions briefly and identify the one question it thinks the other chairs will miss.

```text
Q1  What is the canonical world record, and can every state change be replayed from it?
Q2  Which organs are genuinely live, versus only declared, imported, or historically invoked?
Q3  Can any text, board post, consensus result, tool, model call, or lane spawn bypass authority?
Q4  What must happen before context pressure, compaction, or cache loss occurs?
Q5  Which information is safe to compact, which must remain verbatim, and what proves the difference?
Q6  How should bee-like thresholds, recruitment, stop signals, and quorum alter routing?
Q7  How should fungus-like edges, transport, reinforcement, pruning, fusion, and quarantine alter memory?
Q8  What is the single largest cost leak across subscriptions, providers, local GPU, Vast.ai, and off-hours work?
Q9  Which existing tool or surface can be reused instead of creating a new organ?
Q10 What evidence would falsify the current architecture or its biological analogy?
Q11 What should be built first, by which existing surface, at what cost, with what acceptance command?
Q12 What does the system currently assume exists that has not been proved in territory?
```

## CHAIRS / ROLE SUFFIXES

The common prefix ends before the role suffix. Chairs work blind in Round 1; later rounds receive normalized claim IDs, not full essays.

```text
A  Architecture + compaction: bounds, scopes, cache, archive, spore, replay
B  Authority + adversary: switchboard, broker, taint, injection, false consensus
C  Fleet economics: provider choice, subscriptions, Vast.ai, latency, off-hours, ROI
D  Evidence + zeitgeist: current field practice; primary sources; mature vs hype
E  Bee/fungus systems: thresholds, inhibition, transport, resilience, fusion, pruning
F  Implementation elder: smallest safe build; falsifier; missing organ assumptions
G  Operator/Basecamp: map coverage, human controls, handoff, what must be obvious
H  Chair: compile only after A–G; preserve disputes and weight deltas
```

## SALON PROTOCOL

```text
R0  free/deterministic inventory; resolve P0–P8 pointers; no model needed
R1  independent chairs answer Q1–Q12; one answer per question; cite receipts
R2  elder cross-examines only disputed, high-weight, or unsupported claims
R3  chair compiles claim ledger, trajectory weights, gaps, actions, falsifiers
R4  free/local verifier runs acceptance commands; rejected claims remain UNPROVEN
R5  publish one canonical RIB; route only named next action to Basecamp
```

No chair may vote a claim into truth. Consensus increases confidence only. Authority remains with the switchboard/governor policy.

## PRICE / EXTRACTION LAW

```text
R0 and R4: FREE/LOCAL only; inventory, hashes, replay, tests, and dedupe
R1: one call per chair; max 1,200 words or 1,800 tokens; no restatement of P0–P8
R2: premium only for disputed claims with W >= .80 or safety impact >= .80
R2 input: claim IDs + evidence pointers + competing positions, never full essays
R3: one chair call; max 1,500 tokens; emits the reusable RIB and weight vector
R5: FREE/LOCAL validation; paid calls cannot substitute for acceptance commands
```

The salon spends once on judgment, then reuses claim rows, evidence pointers, tests, weights, and the compiled RIB everywhere. No paid call may answer a question already answered by a verified receipt.

## INDEPENDENCE LAW

Round 1 seats must be independent across provider, base model, prompt ancestry, cache, and evidence path where possible. Record the actual lineage. Three wrappers around one answer count as one lineage. If independence is unavailable, downgrade confidence and record the deficit instead of manufacturing quorum.

## REQUIRED OUTPUT: CLAIM LEDGER

Each chair returns compact rows; no essays.

```text
CLAIM <id>
class: FACT | INFERENCE | PROPOSAL | UNPROVEN | DISPUTE
statement: <one falsifiable sentence>
evidence: <canonical path:line-span OR DOI/URL; exact source type>
project_map: <organ/surface/trajectory ID>
gap: <what is missing or assumed>
confidence: HIGH | MEDIUM | LOW | UNKNOWN
falsifier: <test or observation that would overturn it>
action: <one smallest named next action>
reuse: <what existing tool/artifact is reused>
cost: FREE | LOCAL | PAID:<estimate> | UNKNOWN
weight_delta: <TRJ-id; M/S/F/L/T delta; reason>
receipt: <source hashes, commands run, commands not run>
```

## TRAJECTORY WEIGHTING

These are engineering attention weights, not probabilities:

```text
W = .30 mission + .25 safety + .20 failure_pressure + .15 leverage + .10 time
P0 >= .90; P1 = .80–.89; P2 = .70–.79; below .70 = research/defer
```

Base priority weights carried into the salon:

```text
TRJ-01=.89  epistemic truth       TRJ-02=.97  task execution
TRJ-03=.99  context survival       TRJ-04=.98  authority
TRJ-05=.86  resource/cost          TRJ-06=.81  agent roles
TRJ-07=.87  consensus              TRJ-08=.93  negative feedback
TRJ-09=.85  fusion                 TRJ-10=.80  topology
TRJ-11=.93  organ lifecycle        TRJ-12=.85  human control
TRJ-13=.96  terminal/recovery      TRJ-14=.84  learning
TRJ-15=.94  deployment truth
```

A weight may change only with a cited receipt, experiment, or verified contradiction. Chairs must return the full 15-ID vector, even when unchanged.

## REQUIRED SYNTHESIS

The chair must emit exactly:

```text
VERDICT: <one paragraph; what is actually true>
TOP_GAPS: <maximum 5; each keyed to TRJ-id>
NEXT_ACTION: <one action only; existing surface; FREE/LOCAL first>
TRAJECTORY_VECTOR: <TRJ-01..TRJ-15 with W and deltas>
REUSE_MAP: <claim → existing organ/tool/file>
DISPUTES: <claim IDs preserved, with competing evidence>
DO_NOT_BUILD: <new organs or work that duplicates existing capability>
ACCEPTANCE: <exact commands/tests and pass conditions>
HANDOFF: <start_at; files/spans; completed; open; blocked; next agent instruction>
```

## HARD LAWS / FORBIDDEN

- No full-chat replay; use pointers, spans, hashes, and bounded dereference.
- No paraphrasing operator-authored or operator-confirmed laws inside compaction.
- No board post becomes authority merely because models agree.
- No majority count without lineage independence.
- No external claim becomes canonical without primary evidence or explicit `UNPROVEN`.
- No new supervisor, gateway, ledger, directory, or model tier when an existing surface composes.
- No paid call that only restates a known claim; every paid call must produce reusable deltas, tests, or falsifiers.
- No live mutation from the salon; emit a proposal/patch receipt for the governor.
- No “fungal intelligence” or “hive mind” claim without a mechanism and falsifier.

## ACCEPTANCE GATE

The salon passes only if:

1. At least three independent model/provider lineages contribute, or the deficit is recorded.
2. Every promoted claim has an evidence pointer and classification.
3. Every open gap has one next action and one falsifier.
4. Every trajectory `TRJ-01…TRJ-15` has a current weight.
5. No weight change lacks a receipt.
6. At least one adversarial claim is rejected or downgraded.
7. The next action reuses existing machinery and has an acceptance command.
8. A fresh worker can resume from the handoff without replaying this salon.

## RECEIPT / HANDOFF

Write:

```text
/board/salon_superintelligence_stack_receipt.json
/board/salon_superintelligence_stack_claims.jsonl
/board/salon_superintelligence_stack_rib.md
```

The canonical output is the compiled RIB, not the individual essays. Preserve raw chair outputs as untrusted sidecars. The next starting point is `TRJ-03 + TRJ-04`, one dry-run vertical slice, then Basecamp chooses the next weighted gap.
