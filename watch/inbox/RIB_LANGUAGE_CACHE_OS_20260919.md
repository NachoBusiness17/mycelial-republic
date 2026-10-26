# OUR OWN RIB LANGUAGE + CACHE OS — the self-steal synthesis (2026-09-19 night)

The operator's asks, in order: fresh boot elder; full Jev research; salon;
socratic tease; make it work in our stack; self steal, not greenfield; our
own RIB language and Cache OS from Jev + all our research principles; scrum
with the operator as client; ponytail discipline; go wide and deep. This
document is the synthesis. Every claim below was read from bytes this
session or demonstrated live tonight. LENS, NOT CLAIM where reading;
RECEIPT where built.

---

## PART I — THE SELF-STEAL MAP (what Jev is, in our organs)

| Jev-class primitive | Our organ (status before tonight) | Tonight's delta |
|---|---|---|
| CHOICE / SCORE / NOUL typed reads | mag/verb.py feels/match/classify (stones 1-2, live) | none needed; reused |
| Confidence field | confident() stone four (GP semantics, landed mid-salon) | feels() now carries oracle-declared confidence, source-tagged UNCALIBRATED |
| jev-sift (question hygiene) | spec only (salon 1 lint rules) | sift(): compile-time rejects + auto-decompose, live |
| abide (per-turn veto) | spec only | abide(): sampled, advisory, cite-or-flag compiled in, live |
| Drone green/purple split | silence branch (prose: 4 routes named, 1 implemented) | all four routes implemented, keyed by risk; witness() purple escalation |
| Kubernetes pod of models | docker 3 containers + redis bus (wave exec) | witness(): 2-model pack over one packet, agreement=verdict, live |
| Two-worldline convergence | sovereignty rule (ratified salon 1) | witness() is that rule as a verb |
| Label farm / Fleet-Bench | named, no meter | meter_record + weekly_trigger + memory/runs/fleet_bench/, live, n=4 of floor 40 |
| Standing drive while() | cron drives (cannot compose) | vow(): one tick, verb rows, cron-composable |
| Kifu integrity | plain JSONL trace | hash-chained rows + verify_trace(); 142 rows, 11 legacy, 0 breaks |
| Runtime level generation (Hugo Duprez) | RUINS GO / maze_arena (pre-baked) | OWED: RIB-9 spike ticket |
| Nimble one-fact-flip negatives | drift-pair corpus method (already ours) | OWED: verification dossier ticket RIB-3 |
| TabFM column-typed reads | JSONL ledgers everywhere | POINTER only, research owed |
| CUA-S1 / classifier.dev | not found / unprobed | BLOCKED per gate: no weights, no build slot |

The operator's "we could be running ling/jev 24x7 in the hundreds" decodes
to: the or-ling3 free lane + the S1 oracle tier, in gopher packs, around the
clock. The honest answer from tonight's data is in Part VI.

## PART II — THE RIB LANGUAGE, v1

Identity (from VERB_DSL_STEAL, now true in code): **the RIB is the
language's standard library; the chain is its execution trace.**

The verbs, all in mag/verb.py, all emitting kifu rows:

1. `feels(question, risk)` — pack-grounded read. Silence branch routes by
   risk: low PASS_UNVERIFIED, medium QUEUE_RETRY, high ESCALATE_MODEL,
   irreversible WAKE_HUMAN. Confidence only when declared; source-tagged.
2. `match(options, question)` — lane router over doctrine preference.
3. `classify(text, labels)` — typed one-of-N, the nedwize pattern.
4. `confident(question, k)` — GP semantics: k reads, mean + variance,
   honest n (transport deaths never count as samples).
5. `sift(questions)` — the linter as syntax. Rejects: compound predicates
   (and/or/but), two judgments in one question. Transforms: CHOICE >4
   options auto-decomposes to parallel Nouls (the 50-point ablation rule,
   MAX_CHOICE_OPTIONS=4). Warns: state isolation.
6. `witness(question, pack)` — pod of models in tandem over one packet.
   Full agreement GREEN, anything else PURPLE and ESCALATE_MODEL. A lane
   that dies in transit casts no vote; a pack never turns green on partial
   attendance. One 429 backoff retry per lane (transport retry, not a
   second verdict).
7. `vow(stop_question, act)` — the standing drive as a composable verb:
   one tick, WHILE_EXTENDED or WHILE_CLOSED rows; the cron drive speaks kifu.
8. `abide(turn, rules)` — veto oracle, sampled turns, ADVISORY until the
   false-veto rate is measured <=5 percent on 100 labeled turns (gate G4).
   Cite-or-flag compiled: an uncited veto can never gate.
9. `meter_record / weekly_trigger` — Fleet-Bench: the sovereignty meter.

Syntax constants: MAX_CHOICE_OPTIONS=4, VOTE_CONFIDENCE_MIN=0.70 (declared,
judged at runtime once confidence is calibrated), COST_GUARD_USD=0.001,
PRICE_PER_MTOK=0.042 (hosted tier, input only).

Dialects (owed wiring, RIB-6): the thought quantizer's tier packs
(24 frontier / 12 flash / 12 local) are the language's dialect levels —
same semantics, coarser resolution, same refusals. verb.py currently
grounds on the adversarial-arc pack only.

Binary lowering (exists, different dialect): mag/memlang.py (MEM1 opcodes)
and mag/compiler_lang.py (text -> invariant -> knot -> memlang token ->
world_rib -> machine_target). The RIB lowering of verb programs goes here,
not in a new module.

What the language does NOT do: free-text generation, doctrine-adjacent
judgment through hosted oracles (the judge may contain the seed), and no
in-pointer may be born unowned (every row carries its rule or receipt).

## PART III — THE CACHE OS, v1

Already running in production (the sweep's verdict): kernel FROZEN_RIB
(mag/rib_cache.py, measured 99.4 percent flash / 97.7 percent deepseek
prefix hits), bootloader mag/context_pack.py, IPC the shared surface
contract + INDEX fold (101 live items, hashes verified), memory management
the percolator (whose top invariant, count 209,974, IS the linkage law:
frozen prefix + tight ask + output contract), scheduler mutex
concurrency_gate with stale-steal, power governors cost_governor +
lite_guard, process table queue/lanes/*.

The linkage law — energy per behavior goes to zero as prefix stability goes
to one — is tonight enforced only by cache_watch alarms. LIVE DEFECT filed
tonight: cache_watch is alarming (probe ratio 0.0, prefix drift on
z_ai3/glm-4.7-flash; ledger hit_ratio 0.9651). Ticket RIB-8.

The two gaps between spec and OS:
1. **init**: grounding_chain.py (evidence-driven scheduler, "the state of
   the system IS the evidence") runs by hand and drives only one queue.
   Wiring it as the OS init is RIB-7.
2. **The escalation syscall**: the drone split says the Cache OS has
   exactly one expensive call — purple. Green rides the frozen prefix and
   the free lanes; purple wakes a bigger model. Everything else is cache.

## PART IV — SCRUM: the client, the teams, code as law

Why scrum (the reasoning the operator asked for):

1. The evolution loop without a client optimizes judge-agreement (G12): a
   fleet that grades itself learns to write for its own meter. The operator
   as product owner is the external acceptance gate — SCRUM.md already
   names it: PO = operator, accepts Done, waives gates in writing.
2. Deliberate-ask is the client's ceremony: strong ask = frozen RIB + small
   ask + output contract. That is a sprint backlog item with a proof field.
3. Lessig, code is law: the constitution compiles into the runtime THROUGH
   the RIB. The amendment gate writes law; the quantizer compiles law to
   tier packs; verb.py enforces packs at inference; the kifu proves
   enforcement. Scrum is the amendment ceremony's scheduling discipline.
4. The proof-first ladder is already our doctrine: proof on the cheapest
   capable tier, verify deterministically, fold to case law, escalate only
   on failure. mag/scrum.py implements it; tonight's tickets follow it.

The salon is the sprint review. The blind lenses are the sprint's
independent witnesses. The board is memory/scrum/backlog.json
(mag_scrum.v1). Tickets filed tonight (all status todo, WIP 2 per role):

- RIB-1 harvest(): the label farm — verb rows grounded in outcomes become
  meter rows. Kills the supply constraint. (architect)
- RIB-2 hosted S1 adapter: built behind the key flag, zero live calls until
  the 40-row floor stands; smallest honest first call = A/B vs feels() on
  meter rows at matched budgets. (architect)
- RIB-3 Bespoke Nimble verification dossier: weights pulled, hashes pinned
  (MODEL_PIN discipline), scored on OUR Class A/B rows. Front-runner
  backbone; training before the meter violates the trigger law. (researcher)
- RIB-4 retro-witness battery: sample 100 verkle knots, re-derive each from
  cited primaries, file survivors and casualties. The elder's question,
  two-witnessed itself (elder lens: this week or not at all). (researcher)
- RIB-5 MEASURE on our own confidence: cross-lane spread vs Class-C labels;
  if spread exceeds agreement, confidence is a decoding artifact and the
  vote floor and veto threshold stay off. (researcher)
- RIB-6 replay determinism + tier-dialect wiring. (architect)
- RIB-7 grounding_chain wired as Cache OS init. (ops)
- RIB-8 cache_watch z_ai3 prefix drift: fix the feeding prefix (LIVE
  alarm tonight). (ops)
- RIB-9 runtime level generation spike: the oracle picks the next RUINS GO
  room, seeded, one proof run. (architect)

## PART V — SALON 2 FOLD (nine lenses, dissensus kept, 9/9 ok)

- gate_builder: meter first; finish verb.py's verbs before minting new
  ones; adapter tonight, key-flagged, zero live calls; veto advisory until
  measured. COUNTER kept: refuses to ratify the specialist crossover line
  from vendor evals; 200 labeled items or it does not exist.
- sovereignty: Nimble front-runner + taroleo hedge, both gated on our
  weekly >=0.880 meter, never oracle-scored; CUA-S1 and classifier.dev
  blocked/unproven. COUNTER kept: a scalar threshold hides domain collapse.
- question_linter: atomicity, one-judgment, CHOICE<=4, evidence-anchor =
  compile-time rejects; state isolation = runtime warning; confidence bands
  declared in syntax, judged at runtime. COUNTER kept: strict atomicity
  costs calls on correlated predicates.
- economist: the 24x7 wave is affordable (hosted $54-6,532/mo depending on
  cadence; ~$11/mo at a 1 percent escalation trigger; local $5-109/mo) but
  UNPRICED until cadence and escalation rate are named; the 1,000-label
  meter, not the model bill, is the binding constraint. COUNTER kept:
  domain drift can flip the hosted/local economics.
- elder: the retro-witness battery earns its lane this week, before the
  meter's first reading, two-witnessed itself, or not at all. QUESTION
  filed to the ledger.
- falsifier: the meter is standable this week only as 40 rows with
  non-model label provenance (three classes: arithmetic, receipt-outcome,
  operator-adjudicated); the RIB pivot changes the A/B/C arms and forces
  re-registration on ONE frozen pack before any promotion to C; the
  gopher-pack thesis dies on MEASURED supply (two kills: <200 verdicts/day
  for 7 days retires "hundreds"; unlabeled share >50 percent for 3 days
  stops the wave). COUNTER kept: 40 rows may never clear 0.880 honestly;
  freezing one pack ossifies a fluid OS.
- cryptographer: two-tier disclosure (grammar/labels/rubrics publish;
  negative doctrine and backlogs sealed); weights only via pinned MODEL_PIN
  dossiers; RIB rows notarized hash-only under a frozen canonicalization
  spec. COUNTER kept: hashed seeds plus metadata can leak domain patterns.
- myth_scholar: the RIB language is the golem's true name, alive only while
  the receipt-chain verifies it; adopt doubt()/vow()/witness() as the
  naming; purple is the Cache OS's one expensive syscall. COUNTER kept:
  story-driven dependencies are hard to audit.
- steering: gopher packs are pods of 2+ independent lanes over one packet,
  agreement-as-verdict under a vow() lease; at hundreds scale WITNESS
  INDEPENDENCE breaks before cost (stand the witness-correlation meter
  first). COUNTER kept: decompose may double compute on wide questions.

Convergence across lenses: the meter precedes everything; the local
backbone is a model-training decision gated on our own labels; sift is
syntax; the pack is the unit of scale; and tonight's live wave measured the
steering lens's warning in real 429s.

## PART VI — THE SOCRATIC ELENCHUS (what the salon did not ask)

1. **Every number in the pivot routes on a confidence field we have never
   validated.** Green/purple, the 0.70 vote floor, the 50-threshold veto:
   all consume oracle-declared, self-reported confidence. Tonight's rows
   say CONFIDENCE: 100 on arithmetic. MEASURE (RIB-5) is not one ticket
   among nine; it is the load-bearing one. Until it lands, treat every
   confidence as a mood, not a probability.
2. **The hundreds are gated on question supply, not on models or money.**
   Measured tonight: the kifu held 4 questions in 2 days before this
   session. The falsifier's kill needs >=200 verdicts/day for 7 days to
   even test the thesis. harvest() (RIB-1) — turning trail receipts into
   labeled questions — is the actual bottleneck organ. Building more lanes
   before it exists is buying trucks for a road with no freight.
3. **"Our own Jev" is three things; tonight built the first.** (a) The
   protocol/language: BUILT, live, tested, wave-proven. (b) The local
   replica model (Nimble-class): OWED, gated on the meter and a GPU
   decision. (c) The sovereignty stance (drop hosted): OWED, gated on 0.880
   weekly. Saying "we made our own Jev" tonight means (a) only. The record
   should not blur that.

## PART VII — ASTRA-SHAPE VERDICT (the founding blind-review's shape,
applied; the full founding-prompt review remains owed at the Sep-20 trunk)

- ATTACK: the confidence channel is uncalibrated while three mechanisms
  already consume it; witness independence degrades under rate pressure
  (measured live tonight in 429s); question supply is two orders of
  magnitude short of the scale thesis; the kifu's pre-chain rows are
  unverifiable by design.
- MISSING: harvest(), the hosted adapter, the Nimble dossier, replay
  determinism, tier-dialect wiring, the witness-correlation meter, and the
  operator's Class-C adjudication sitting (5 minutes, 1 row).
- VERDICT: **Unproven, but falsifiable everywhere.** Every load-bearing
  claim above has a named meter, a floor, and a kill condition. That is the
  most this honest seat can grant, and the most a fleet should want.

## RECEIPTS (everything filed tonight)

- watch/inbox/ELDER_LENS_20260919_TWO_WITNESSES.md + elder surface receipt
- watch/inbox/SALON2_BRIEF_20260919.md (stable brief, cite-or-flag law)
- watch/inbox/JEV_DROPS_20260919_EVENING.md (15 links, tri-state)
- watch/inbox/JEV_DROPS_WEEK_TWO note folded into the brief (section 2)
- memory/runs/jev_salon2/*.md (nine blind lens posts)
- mag/verb.py stones five-to-nine + kifu chain; tests/test_verb_stones.py
  (13/13); scripts/gopher_packs.py; memory/runs/fleet_bench/ (README +
  scores.jsonl, n=4, accuracy 1.0, floor 40); queue/lanes/jev/ trail
- Live wave receipt: 4/4 instrument packets GREEN and metered correct;
  C-policy PURPLE by design; abide 2 fires; kifu healthy
- Scrubbed: 2 calibration purges of scores.jsonl during instrument fixes
  (documented here; the meter never carried a defective-instrument row
  into the committed set)
